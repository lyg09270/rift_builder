"""Conservative card-text conversion. Unmapped clauses block all projections."""

import re
import json

from card import Card, Effect, PowerRequirement, number
from deck_support import DEFAULT_DB, connect, resolve_card
from game_state import DOMAINS


class CardConverter:
    def load(self, card_id, *, db_path=DEFAULT_DB, **reviewed_cost):
        connection = connect(db_path)
        try:
            return self.convert(resolve_card(connection, card_id), **reviewed_cost)
        finally:
            connection.close()

    def convert(self, record, *, power_cost=None, power_source=""):
        energy, power, might = (record[name] for name in ("energy", "power", "might"))
        for name, value in (("energy", energy), ("power", power), ("might", might)):
            if value is not None:
                number(value, name)
        if power_cost is None:
            encoded = record.get("power_cost_json")
            if encoded is not None:
                if not record.get("power_source"):
                    raise ValueError("Stored Power requirements need provenance")
                groups = json.loads(encoded) if isinstance(encoded, str) else encoded
                payment = tuple(PowerRequirement(group["amount"], tuple(group["domains"])) for group in groups)
                if power is not None and sum(r.amount for r in payment) != power:
                    raise ValueError("Stored Power groups differ from the source total")
                power_source = record["power_source"]
            else:
                payment = () if power == 0 else None
        else:
            if not power_source.strip():
                raise ValueError("Reviewed payment glyphs require a source, including test-only assumptions")
            if not isinstance(power_cost, dict) or not power_cost.keys() <= set(DOMAINS):
                raise ValueError("Power cost must map known domains to amounts")
            for amount in power_cost.values():
                if number(amount, "Power cost") != int(amount):
                    raise ValueError("Power cost must be an integer")
            if power is not None and sum(power_cost.values()) != power:
                raise ValueError("Reviewed glyphs differ from the known total Power cost")
            payment = tuple(PowerRequirement(int(amount), tuple(DOMAINS[:6]) if domain == "Universal" else (domain,))
                            for domain, amount in sorted(power_cost.items()) if amount > 0)
        text = record["effect_effective"]
        if not isinstance(text, str):
            raise ValueError("Full effective text is required")
        timing, effects, unknown = self._parse(text, record["card_type"])
        return Card(record["display_code"], record["full_name"], record["card_type"], energy, power, might,
                    tuple(record["domains"]), tuple(record["labels"]), tuple(record["tags"]), text,
                    record["effect_original"], record["source_url"], timing, effects, unknown,
                    payment, power_source)

    @staticmethod
    def _parse(text, card_type):
        body = " ".join(text.replace("’", "'").split())
        timing = "normal"
        match = re.match(r"^\[(Action|Reaction)\]\s*", body)
        if match:
            timing = match[1].lower()
            body = body[match.end():]
            for reminder in ("(Play on your turn or in showdowns.)", "(Play any time, even before spells and abilities resolve.)"):
                if body.startswith(reminder):
                    body = body[len(reminder):].strip()
        legion = re.fullmatch(r"\[Legion\]\s*[�—–:-]?\s*I cost \[(\d+)\] less\.\s*(?:\(Get the effect if you've played another card this turn\.\))?", body)
        trash = re.fullmatch(r"I cost \[(\d+)\] less for each card in your trash\.", body)
        conditional = re.fullmatch(r"When you play me, draw (\d+) if your other units have total Might (\d+) or more\.", body)
        if card_type == "Unit":
            if legion:
                return timing, (Effect("cost", "discount", int(legion[1]), "legion"),), ()
            if trash:
                return timing, (Effect("cost", "discount", int(trash[1]), "trash"),), ()
            if conditional:
                return timing, (Effect("play", "draw", int(conditional[1]), "other_might", int(conditional[2])),), ()

        event = "play"
        if card_type in ("Unit", "Gear"):
            prefix = re.match(r"^When you play (?:me|this),\s*", body)
            death = re.match(r"^When I die,\s*", body)
            deathknell = re.match(r"^\[Deathknell\]\s*(?:\[>\])?\s*", body)
            if prefix or death or deathknell:
                matched = prefix or death or deathknell
                event = "play" if prefix else "death"
                body = body[matched.end():]
                reminder = "(When I die, get the effect.)"
                if deathknell and body.startswith(reminder):
                    body = body[len(reminder):].strip()
                if deathknell and body.endswith(reminder):
                    body = body[:-len(reminder)].strip()
            elif body:
                return timing, (), (body,)
        if not body and card_type == "Spell":
            return timing, (), ("Missing spell text",)
        effects, unknown = [], []
        for clause in filter(None, re.split(r"\.\s*", body)):
            if match := re.fullmatch(r"Draw (\d+)", clause, re.I):
                effects.append(Effect(event, "draw", int(match[1])))
            elif match := re.fullmatch(r"Deal (\d+) to a unit( at a battlefield)?", clause, re.I):
                effects.append(Effect(event, "damage", int(match[1]), battlefield_only=bool(match[2])))
            elif match := re.fullmatch(r"Give a unit \+(\d+) \[(?:S|M)\] this turn", clause, re.I):
                effects.append(Effect(event, "buff", int(match[1]), duration="turn"))
            elif match := re.fullmatch(r"(Ready|Stun|Kill) a unit( at a battlefield)?", clause, re.I):
                operation = match[1].lower()
                effects.append(Effect(event, operation, 1, battlefield_only=bool(match[2]),
                                      duration="turn" if operation == "stun" else "instant"))
            elif match := re.fullmatch(r"(?:Gain|Score) (\d+) points?", clause, re.I):
                effects.append(Effect(event, "score", int(match[1])))
            elif match := re.fullmatch(r"Gain (\d+) XP", clause, re.I):
                effects.append(Effect(event, "xp", int(match[1])))
            else:
                unknown.append(clause)
        if sum(e.operation in ("damage", "buff", "ready", "stun", "kill") for e in effects) > 1:
            unknown.append("Multiple target instructions need an explicit selection/reference model")
        if event == "death" and any(e.operation in ("damage", "buff", "ready", "stun", "kill") for e in effects):
            unknown.append("A death ability needs separate dying-source and selected-target snapshots")
        return timing, tuple(effects), tuple(unknown)
