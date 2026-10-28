"""Internal card lookup, validation and export dependencies for deck projects.

No retrieval, recommendation, synchronization or standalone deckbuilding CLI.
"""

from __future__ import annotations

import json
import re
import sqlite3
import unicodedata
from collections import Counter
from pathlib import Path
from typing import Any, Iterable, cast

CardInfo = dict[str, Any]
ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "data" / "cards.sqlite"
DEFAULT_RULES = ROOT / "data" / "rules.json"


def name_key(text: str) -> str:
    normalized = unicodedata.normalize("NFKC", text).casefold()
    return re.sub(r"[\W_]+", " ", normalized, flags=re.UNICODE).strip()

def json_list(value: Any) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [str(item) for item in value if item is not None]
    if isinstance(value, str):
        try:
            decoded = json.loads(value)
            if isinstance(decoded, list):
                return [str(item) for item in decoded if item is not None]
        except json.JSONDecodeError:
            return [part.strip() for part in value.split(",") if part.strip()]
    return [str(value)]

def presentation_name(card: dict[str, Any]) -> str:
    full_name = card["full_name"]
    if card["card_type"].casefold() == "legend" and "," not in full_name and card.get("tags"):
        champion = card["tags"][0]
        if champion.casefold() not in full_name.casefold():
            return f"{champion}, {full_name}"
    return full_name

def decode_card(row: sqlite3.Row | dict[str, Any]) -> CardInfo:
    card = dict(row)
    card["display_code"] = public_card_id(card["set_code"], card["collector_number"], card["display_code"])
    card["domains"] = json_list(card.pop("domains_json", []))
    card["labels"] = json_list(card.pop("labels_json", []))
    card["tags"] = json_list(card.pop("tags_json", []))
    card["has_errata"] = bool(card.get("has_errata"))
    card["display_name"] = presentation_name(card)
    return cast(CardInfo, card)

def public_card_id(set_code: str, collector_number: str, fallback: str) -> str:
    """Use the official set/collector code, without the trailing set-size suffix.

    Preserve letter/star and R/T/SP prefixes; never infer a base printing by
    stripping a variant suffix or by truncating the number to three digits.
    """
    if not set_code or not collector_number:
        return fallback.upper()
    number = re.sub(r"-\d{3}$", "", collector_number)
    return f"{set_code}-{number}".upper()

def printing_preference(card: CardInfo) -> tuple:
    return (
        card["rarity"].casefold() in {"showcase", "alternate art", "promo"},
        "sp" in card["display_code"].casefold(),
        len(card["display_code"]),
        card["display_code"],
        card["source_code"],
    )

def preferred(cards: Iterable[CardInfo]) -> list[CardInfo]:
    by_name: dict[str, CardInfo] = {}
    for card in cards:
        key = card["full_name"].casefold()
        if key not in by_name or printing_preference(card) < printing_preference(by_name[key]):
            by_name[key] = card
    return list(by_name.values())

def connect(db_path: str | Path) -> sqlite3.Connection:
    path = Path(db_path)
    if not path.exists():
        raise FileNotFoundError(f"Card database not found: {path}. Restore the bundled data or provide --db.")
    connection = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
    connection.row_factory = sqlite3.Row
    return connection

def resolve_card(connection: sqlite3.Connection, reference: str) -> dict[str, Any]:
    ref = reference.strip()
    connection.create_function("public_card_id", 3, public_card_id, deterministic=True)
    rows = connection.execute(
        "SELECT * FROM cards WHERE public_card_id(set_code, collector_number, display_code) = ? COLLATE NOCASE OR source_code = ? COLLATE NOCASE",
        (ref, ref),
    ).fetchall()
    if not rows:
        rows = connection.execute("SELECT * FROM cards WHERE full_name = ? COLLATE NOCASE", (ref,)).fetchall()
    if not rows:
        raise ValueError(f"Unknown card: {reference}")
    decoded = preferred(decode_card(row) for row in rows)
    if len(decoded) > 1:
        codes = ", ".join(card["display_code"] for card in decoded)
        raise ValueError(f"Ambiguous card name {reference!r}; use a code: {codes}")
    return decoded[0]

def load_rules(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)

def read_deck(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)

def zone_entries(deck: dict[str, Any], zone: str) -> list[dict[str, Any]]:
    entries = deck.get(zone, [])
    if not isinstance(entries, list):
        raise ValueError(f"{zone} must be a list")
    return entries

def validate_deck(deck: dict[str, Any], connection: sqlite3.Connection, rules: dict[str, Any]) -> dict[str, Any]:
    errors: list[str] = []
    warnings: list[str] = []
    strategy = deck.get("strategy") or {}
    for field in ("style", "win_condition", "operating_plan", "core_cards"):
        if not strategy.get(field):
            errors.append(f"Missing strategy.{field}")

    def resolve(reference: str, context: str) -> dict[str, Any] | None:
        try:
            return resolve_card(connection, reference)
        except ValueError as error:
            errors.append(f"{context}: {error}")
            return None

    legend = resolve(str(deck.get("legend", "")), "legend")
    champion = resolve(str(deck.get("chosen_champion", "")), "chosen_champion")
    if legend and legend["card_type"].casefold() != "legend":
        errors.append(f"Legend is not a Legend card: {legend['full_name']}")
    if champion and "champion" not in {label.casefold() for label in champion["labels"]}:
        errors.append(f"Chosen champion lacks Champion label: {champion['full_name']}")
    if legend and champion:
        legend_identity = {tag.casefold() for tag in legend["tags"]} | {legend["name"].casefold()}
        champion_identity = {tag.casefold() for tag in champion["tags"]} | {champion["name"].casefold()}
        if not legend_identity & champion_identity:
            errors.append("Chosen champion does not match the Legend identity")

    zones = {zone: zone_entries(deck, zone) for zone in ("main_deck", "battlefields", "runes", "sideboard")}
    zone_cards: dict[str, list[tuple[int, dict[str, Any]]]] = {zone: [] for zone in zones}
    for zone, entries in zones.items():
        for index, entry in enumerate(entries):
            if not isinstance(entry, dict):
                errors.append(f"{zone}[{index}] must be an object")
                continue
            quantity = entry.get("quantity")
            if not isinstance(quantity, int) or isinstance(quantity, bool) or quantity <= 0:
                errors.append(f"{zone}[{index}] quantity must be a positive integer")
                continue
            card = resolve(str(entry.get("code", "")), f"{zone}[{index}]")
            if card:
                zone_cards[zone].append((quantity, card))

    totals = {zone: sum(quantity for quantity, _ in cards) for zone, cards in zone_cards.items()}
    expected = {
        "main_deck": rules["main_deck_size"],
        "battlefields": rules["battlefield_count"],
        "runes": rules["rune_deck_size"],
    }
    for zone, count in expected.items():
        if totals[zone] != count:
            errors.append(f"{zone} has {totals[zone]} cards; expected {count}")
    if totals["sideboard"] > rules["sideboard_max"]:
        errors.append(f"sideboard has {totals['sideboard']} cards; maximum is {rules['sideboard_max']}")

    expected_types = {"battlefields": "battlefield", "runes": "rune"}
    for zone, expected_type in expected_types.items():
        for _, card in zone_cards[zone]:
            if card["card_type"].casefold() != expected_type:
                errors.append(f"{card['full_name']} is not a {expected_type} card but appears in {zone}")
    for zone in ("main_deck", "sideboard"):
        for _, card in zone_cards[zone]:
            if card["card_type"].casefold() not in {"unit", "gear", "spell"}:
                errors.append(f"{card['full_name']} is not a valid Main Deck card")

    battlefield_names = [card["full_name"].casefold() for _, card in zone_cards["battlefields"]]
    if len(battlefield_names) != len(set(battlefield_names)):
        errors.append("Battlefields must have unique names")
    if champion:
        champion_count = sum(quantity for quantity, card in zone_cards["main_deck"] if card["full_name"].casefold() == champion["full_name"].casefold())
        if champion_count < 1:
            errors.append("Chosen champion is not included in canonical main_deck")

    if legend:
        identity = {domain.casefold() for domain in legend["domains"] if domain.casefold() != "colorless"}
        for zone in ("main_deck", "runes", "sideboard"):
            for _, card in zone_cards[zone]:
                domains = {domain.casefold() for domain in card["domains"] if domain.casefold() != "colorless"}
                if domains and not domains.issubset(identity):
                    errors.append(f"{card['full_name']} has domains {sorted(domains)} outside Legend identity {sorted(identity)}")

    combined = Counter()
    signature_count = 0
    for zone in ("main_deck", "sideboard"):
        for quantity, card in zone_cards[zone]:
            combined[card["full_name"]] += quantity
            if len(card["domains"]) > 1:
                signature_count += quantity
            if not card["effect_effective"]:
                warnings.append(f"No effective effect text for {card['display_code']} {card['full_name']}")
    for name, quantity in combined.items():
        if quantity > rules["copy_limit"]:
            errors.append(f"{name} has {quantity} copies across main deck and sideboard; maximum is {rules['copy_limit']}")
    if signature_count > rules["signature_limit"]:
        errors.append(f"Signature cards total {signature_count}; maximum is {rules['signature_limit']}")

    legal_sets = {item.upper() for item in rules["legal_sets"]}
    banned_cards = {name_key(item) for item in rules["banned_cards"]}
    banned_battlefields = {name_key(item) for item in rules["banned_battlefields"]}
    for zone, cards in zone_cards.items():
        for _, card in cards:
            if card["set_code"].upper() not in legal_sets:
                errors.append(f"{card['full_name']} is from non-legal set {card['set_code']}")
            if zone == "battlefields" and name_key(card["full_name"]) in banned_battlefields:
                errors.append(f"Banned battlefield: {card['full_name']}")
            if zone in {"main_deck", "sideboard"} and name_key(card["full_name"]) in banned_cards:
                errors.append(f"Banned card: {card['full_name']}")

    for reference in strategy.get("core_cards", []):
        resolve(str(reference), "strategy.core_cards")
    return {
        "valid": not errors,
        "rules_profile": rules["profile"],
        "rules_as_of": rules["as_of"],
        "totals": totals,
        "errors": errors,
        "warnings": warnings,
    }

def export_line(quantity: int, card: dict[str, Any], include_codes: bool) -> str:
    suffix = f" [{card['display_code']}]" if include_codes else ""
    return f"{quantity} {card['display_name']}{suffix}"

def export_riftatlas(deck: dict[str, Any], connection: sqlite3.Connection, include_codes: bool) -> str:
    legend = resolve_card(connection, deck["legend"])
    champion = resolve_card(connection, deck["chosen_champion"])
    sections: list[tuple[str, list[str]]] = [
        ("Legend", [export_line(1, legend, include_codes)]),
        ("Champion", [export_line(1, champion, include_codes)]),
    ]
    main_lines = []
    champion_removed = False
    for entry in zone_entries(deck, "main_deck"):
        card = resolve_card(connection, entry["code"])
        quantity = entry["quantity"]
        if not champion_removed and card["full_name"].casefold() == champion["full_name"].casefold():
            quantity -= 1
            champion_removed = True
        if quantity:
            main_lines.append(export_line(quantity, card, include_codes))
    sections.append(("MainDeck", main_lines))
    for title, zone in (("Battlefields", "battlefields"), ("Runes", "runes"), ("Sideboard", "sideboard")):
        lines = [export_line(entry["quantity"], resolve_card(connection, entry["code"]), include_codes) for entry in zone_entries(deck, zone)]
        sections.append((title, lines))
    return "\n\n".join(f"{title}:\n" + "\n".join(lines) for title, lines in sections) + "\n"
