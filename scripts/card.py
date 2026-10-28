"""Card facts and isolated event projections onto the numeric advantage vector."""

from dataclasses import dataclass, replace
from collections import Counter
import math

import numpy as np

from game_state import DOMAINS, STATE_SIZE, StateEnum as S, game_state
from state_transition import StateTransition, TransitionError


def number(value, name, *, signed=False):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value):
        raise ValueError(f"{name} must be a finite number")
    if not signed and value < 0:
        raise ValueError(f"{name} must be nonnegative")
    return float(value)


@dataclass(frozen=True)
class Effect:
    event: str
    operation: str
    amount: float
    condition: str = ""
    threshold: float = 0
    battlefield_only: bool = False
    duration: str = "instant"


@dataclass(frozen=True)
class PowerRequirement:
    """Pay amount Power from any of these domains; Universal resources also work."""

    amount: int
    domains: tuple[str, ...]

    def __post_init__(self):
        if isinstance(self.amount, bool) or not isinstance(self.amount, int) or self.amount <= 0:
            raise ValueError("Power requirement amount must be a positive integer")
        if not self.domains or len(set(self.domains)) != len(self.domains) or any(d not in DOMAINS[:6] for d in self.domains):
            raise ValueError("Power requirements need distinct known domain choices")


def power_payment(requirements, available, chosen=None):
    pool = dict(available if chosen is None else chosen)
    if any(d not in DOMAINS or number(n, "Power payment") != int(n) for d, n in pool.items()):
        raise TransitionError("invalid_payment", "Invalid Power payment")
    if chosen is not None and sum(pool.values()) != sum(r.amount for r in requirements):
        raise TransitionError("invalid_payment", "Chosen payment has the wrong total")
    if any(n > available.get(d, 0) for d, n in pool.items()):
        raise TransitionError("unaffordable", "Insufficient floating Power for the chosen payment")
    pips = sorted((r.domains for r in requirements for _ in range(r.amount)), key=len)

    def assign(index):
        if index == len(pips):
            return []
        for domain in (*pips[index], "Universal"):
            if pool.get(domain, 0) > 0:
                pool[domain] -= 1
                suffix = assign(index + 1)
                pool[domain] += 1
                if suffix is not None:
                    return [domain, *suffix]
        return None

    payment = assign(0)
    if payment is None:
        code = "unaffordable" if chosen is None else "invalid_payment"
        raise TransitionError(code, "Available or chosen Power does not satisfy the allowed-domain groups")
    return dict(Counter(payment))


@dataclass(frozen=True)
class UnitTarget:
    """Actual target facts supplied by an outer context, not guessed from totals."""

    instance_id: str
    card_id: str
    owner: int
    controller: int
    location: str  # base, battlefield_0 or battlefield_1.
    might: float  # Signed effective Might; observations clamp each unit to zero.
    damage: float = 0
    exhausted: bool = False
    stunned: bool = False

    def __post_init__(self):
        if not self.instance_id or not self.card_id:
            raise ValueError("A target needs its instance and card IDs")
        if any(isinstance(p, bool) or not isinstance(p, int) or p not in (0, 1) for p in (self.owner, self.controller)):
            raise ValueError("Invalid target player")
        if self.location not in ("base", "battlefield_0", "battlefield_1"):
            raise ValueError("Invalid target location")
        number(self.might, "target Might", signed=True)
        number(self.damage, "target damage")
        if not isinstance(self.exhausted, bool) or not isinstance(self.stunned, bool):
            raise ValueError("Target statuses must be boolean")

    def contribution(self):
        prefix = f"P{self.controller}_BASE" if self.location == "base" else f"BF{self.location[-1]}_P{self.controller}"
        might = max(0, self.might)
        values = {"UNITS": 1, "MIGHT": might, "READY_UNITS": int(not self.exhausted),
                  "READY_MIGHT": 0 if self.exhausted else might, "DAMAGE": self.damage}
        if self.location != "base":
            values["COMBAT_MIGHT"] = 0 if self.stunned else might
        vector = np.zeros(STATE_SIZE)
        for name, value in values.items():
            vector[S[f"{prefix}_{name}"]] = value
        return vector


@dataclass(frozen=True)
class CardContext:
    player: int = 0
    source: str = "hand"  # hand or champion.
    target: UnitTarget | None = None
    played_other_card: bool | None = None
    power_payment: tuple[tuple[str, float], ...] | None = None
    isolated: bool = False  # Explicitly confirm no external triggers or target replacements.

    def __post_init__(self):
        if isinstance(self.player, bool) or not isinstance(self.player, int) or self.player not in (0, 1):
            raise ValueError("player must be 0 or 1")
        if self.source not in ("hand", "champion"):
            raise ValueError("Unsupported source zone")
        if not isinstance(self.isolated, bool):
            raise ValueError("isolated must be boolean")
        if self.target is not None and not isinstance(self.target, UnitTarget):
            raise ValueError("target must be a UnitTarget snapshot")
        if self.power_payment is not None and len(dict(self.power_payment)) != len(self.power_payment):
            raise ValueError("Power payment domains must not be duplicated")


@dataclass(frozen=True)
class Card:
    card_id: str
    name: str
    card_type: str
    energy: float | None
    power: float | None
    might: float | None
    domains: tuple[str, ...]
    labels: tuple[str, ...]
    tags: tuple[str, ...]
    text: str
    original_text: str
    source_url: str
    timing: str = "normal"
    effects: tuple[Effect, ...] = ()
    unmapped: tuple[str, ...] = ()
    power_cost: tuple[PowerRequirement, ...] | None = None
    power_source: str = ""

    def cost(self, state: game_state, context: CardContext):
        if self.unmapped:
            raise TransitionError("unmapped_text", "Cost cannot be certified while card clauses remain unmapped")
        if self.energy is None or self.power_cost is None:
            raise TransitionError("missing_cost", "Energy or reviewed Power glyphs are missing; null is not zero")
        reduction = 0
        for effect in self.effects:
            if effect.event != "cost":
                continue
            if effect.condition == "legion":
                if not isinstance(context.played_other_card, bool):
                    raise TransitionError("missing_history", "Legion needs played_other_card=True/False")
                reduction += effect.amount * context.played_other_card
            elif effect.condition == "trash":
                reduction += effect.amount * state[S[f"P{context.player}_TRASH_COUNT"]]
        return max(0, self.energy - reduction)

    def on_play(self, state: game_state, context: CardContext):
        return self._transition("play", state, context)

    def on_draw(self, state: game_state, context: CardContext):
        return self._transition("draw", state, context)

    def on_death(self, state: game_state, context: CardContext):
        return self._transition("death", state, context)

    def _transition(self, event, state, context):
        if "Token" in self.labels or self.card_type == "Token":
            raise TransitionError("token_lifecycle", "Tokens need creation/removal semantics, not normal draw/play/trash lifecycle")
        if self.unmapped:
            raise TransitionError("unmapped_text", "; ".join(self.unmapped))
        if self.card_type not in ("Unit", "Spell", "Gear"):
            raise TransitionError("unsupported_type", f"No {event} lifecycle for {self.card_type}")
        if not context.isolated:
            raise TransitionError("missing_context", "Confirm isolated resolution: no external triggers, attachments or replacement effects")
        state.validate()
        current = state.to_vector()
        player = context.player

        def add(name, amount):
            current[S[f"P{player}_{name}"]] += amount

        def draw(amount):
            if amount > current[S[f"P{player}_DECK_COUNT"]]:
                raise TransitionError("burn_out", "Burn Out needs full zone/effect context; drawing is not truncated")
            add("DECK_COUNT", -amount)
            add("HAND_COUNT", amount)

        target = context.target
        original_target = target
        targeted = any(e.event == event and e.operation in ("damage", "buff", "ready", "stun", "kill") for e in self.effects)
        if targeted or event == "death":
            if target is None:
                raise TransitionError("missing_target", "This event needs an actual unit snapshot")
            contribution = target.contribution()
            indices = np.flatnonzero(contribution)
            if np.any(current[indices] < contribution[indices]):
                raise TransitionError("invalid_target", "The target's contributions exceed the observed board")
            if target.damage > 0 and target.damage >= target.might:
                raise TransitionError("invalid_target", "The initial target already needs lethal-damage cleanup")
        elif target is not None:
            raise TransitionError("unused_target", "This event does not select a unit")

        if event == "play":
            # Priority is outside the observation, but obvious timing conflicts are rejected.
            neutral = state[S.WINDOW] == 0
            if neutral and (state[S.TURN_PLAYER] != player or state[S.PHASE] != 6):
                raise TransitionError("timing", "Neutral-open play requires the player's Main Phase")
            if not neutral and self.timing == "normal":
                raise TransitionError("timing", "This card lacks Action/Reaction for a Showdown")
            energy = self.cost(state, context)
            if current[S[f"P{player}_ENERGY"]] < energy:
                raise TransitionError("unaffordable", "Insufficient floating Energy; rune activation is a separate action")
            available = {domain: current[S[f"P{player}_POWER_{domain.upper()}"]] for domain in DOMAINS}
            payment = power_payment(self.power_cost, available, context.power_payment)
            for domain, amount in payment.items():
                index = S[f"P{player}_POWER_{domain.upper()}"]
                if current[index] < amount:
                    raise TransitionError("unaffordable", "Insufficient chosen Power; supply a legal payment or generate resources first")
                current[index] -= amount
            add("ENERGY", -energy)
            source = "HAND_COUNT" if context.source == "hand" else "CHAMPION_ZONE_COUNT"
            if context.source == "champion" and (self.card_type != "Unit" or "Champion" not in self.labels):
                raise TransitionError("invalid_source", "Only a chosen-champion unit can use the champion source")
            if current[S[f"P{player}_{source}"]] < 1:
                raise TransitionError("invalid_source", "No card in the selected source zone")
            add(source, -1)
            if self.card_type == "Unit":
                if self.might is None:
                    raise TransitionError("missing_might", "Unit Might is unknown")
                add("BASE_UNITS", 1)
                add("BASE_MIGHT", max(0, self.might))  # Ordinary units enter exhausted.
            elif self.card_type == "Gear":
                add("GEAR_COUNT", 1)
        elif event == "draw":
            draw(1)
        elif event == "death":
            if self.card_type != "Unit" or target.card_id != self.card_id or target.controller != player:
                raise TransitionError("invalid_target", "Death must refer to this card's controlled unit instance")
            current -= target.contribution()
            current[S[f"P{target.owner}_TRASH_COUNT"]] += 1
            target = None

        for effect in self.effects:
            if effect.event != event:
                continue
            if effect.condition == "other_might":
                other_might = sum(state[S[name]] for name in (f"P{player}_BASE_MIGHT", f"BF0_P{player}_MIGHT", f"BF1_P{player}_MIGHT"))
                if other_might < effect.threshold:
                    continue
            operation, amount = effect.operation, effect.amount
            if operation == "draw":
                draw(amount)
            elif operation in ("score", "xp"):
                add("SCORE" if operation == "score" else "XP", amount)
            else:
                if target is None:
                    raise TransitionError("invalid_target", "The selected target no longer exists")
                if effect.battlefield_only and target.location == "base":
                    raise TransitionError("invalid_target", "This effect requires a unit at a battlefield")
                if operation == "damage":
                    target = replace(target, damage=target.damage + amount)
                elif operation == "buff":
                    target = replace(target, might=target.might + amount)
                elif operation == "ready":
                    target = replace(target, exhausted=False)
                elif operation == "stun":
                    target = replace(target, stunned=True)
                elif operation == "kill":
                    current[S[f"P{target.owner}_TRASH_COUNT"]] += 1
                    target = None
                else:
                    raise TransitionError("unsupported_operation", operation)

        if original_target is not None and event != "death":
            current -= original_target.contribution()
            if target is not None and target.damage > 0 and target.damage >= target.might:
                current[S[f"P{target.owner}_TRASH_COUNT"]] += 1
                target = None
            if target is not None:
                current += target.contribution()
        if event == "play" and self.card_type == "Spell":
            add("TRASH_COUNT", 1)
        if state[S.WINDOW] == 0:
            for battlefield in (0, 1):
                controller = current[S[f"BF{battlefield}_CONTROLLER"]]
                if controller in (0, 1) and current[S[f"BF{battlefield}_P{int(controller)}_UNITS"]] == 0:
                    if any(current[S[f"BF{battlefield}_P{p}_HIDDEN_CARDS"]] for p in (0, 1)):
                        raise TransitionError("hidden_cleanup", "Losing control with hidden cards needs their ownership and zone context")
                    current[S[f"BF{battlefield}_CONTROLLER"]] = -1
        after = game_state(current)
        return StateTransition.between(f"{self.card_id}/{event}", state, after, target)
