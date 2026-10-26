#!/usr/bin/env python3
"""Local full-text Riftbound card database, deck validator, and exporter."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sqlite3
import sys
import tempfile
import urllib.parse
import urllib.request
from collections import Counter
from pathlib import Path
from typing import Any


# The project manager also loads this entrypoint by absolute path via importlib.
SCRIPT_DIR = str(Path(__file__).resolve().parent)
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

from riftbound_retrieval import CardFilters, KeywordQuery, KeywordRetriever, RetrievalRules
from riftbound_retrieval.cards import decode_card, json_list, name_key, preferred, public_card_id
from riftbound_retrieval.models import CARD_TYPES, COLORS


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DB = ROOT / "data" / "cards.sqlite"
DEFAULT_RULES = ROOT / "data" / "rules.json"
HF_ROWS = "https://datasets-server.huggingface.co/rows"


def eprint(*values: object) -> None:
    print(*values, file=sys.stderr)


def value(row: dict[str, Any], *names: str, default: Any = None) -> Any:
    for name in names:
        if name in row and row[name] is not None:
            return row[name]
    return default


def display_code(row: dict[str, Any]) -> str:
    set_code = str(value(row, "setCode", "set_code", default="")).upper()
    number = str(value(row, "cardNumber", "card_number", default=""))
    source = str(value(row, "cardCode", "card_code", default=""))
    return public_card_id(set_code, number, source)


def normalize_card(row: dict[str, Any]) -> dict[str, Any]:
    name = str(value(row, "name", default="")).strip()
    subtitle_raw = value(row, "subtitle")
    subtitle = str(subtitle_raw).strip() if subtitle_raw else ""
    full_name = str(value(row, "fullName", "full_name", default="")).strip()
    if not full_name:
        full_name = f"{name}, {subtitle}" if subtitle else name
    domains = json_list(value(row, "domains"))
    domain = value(row, "domain")
    if not domains and domain:
        domains = [str(domain)]
    labels = json_list(value(row, "cardTypeLabels", "card_type_labels"))
    tags = json_list(value(row, "tags"))
    original = value(row, "abilityOriginal", "ability_original", default="") or ""
    corrected = value(row, "abilityCorrected", "ability_corrected", default="") or ""
    effective = value(row, "abilityEffective", "ability_effective", default="") or corrected or original
    return {
        "source_code": str(value(row, "cardCode", "card_code", default="")).lower(),
        "display_code": display_code(row),
        "name": name,
        "subtitle": subtitle,
        "full_name": full_name,
        "set_code": str(value(row, "setCode", "set_code", default="")).upper(),
        "set_name": str(value(row, "cardSet", "card_set", default="") or ""),
        "collector_number": str(value(row, "cardNumber", "card_number", default="") or ""),
        "rarity": str(value(row, "rarity", default="") or ""),
        "domain": str(domain or ""),
        "domains": domains,
        "card_type": str(value(row, "cardType", "card_type", default="") or ""),
        "labels": labels,
        "tags": tags,
        "energy": value(row, "energy"),
        "power": value(row, "power"),
        "might": value(row, "might"),
        "effect_original": str(original),
        "effect_corrected": str(corrected),
        "effect_effective": str(effective),
        "has_errata": bool(value(row, "hasErrata", "has_errata", default=False)),
        "source_url": str(value(row, "sourceUrl", "source_url", default="") or ""),
        "scraped_at": str(value(row, "scrapedAt", "scraped_at", default="") or ""),
    }


def fetch_json(url: str) -> Any:
    request = urllib.request.Request(url, headers={"User-Agent": "riftbound-deck-mvp/1.0"})
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.load(response)


def extract_rows(payload: Any) -> list[dict[str, Any]]:
    if isinstance(payload, list):
        return payload
    if not isinstance(payload, dict):
        raise ValueError("Unsupported card JSON shape")
    for key in ("cards", "data"):
        if isinstance(payload.get(key), list):
            return payload[key]
    if isinstance(payload.get("rows"), list):
        return [item.get("row", item) if isinstance(item, dict) else item for item in payload["rows"]]
    raise ValueError("JSON contains no cards, data, or rows list")


def load_source(source: str) -> tuple[list[dict[str, Any]], str]:
    if source in ("hf", "huggingface"):
        rows: list[dict[str, Any]] = []
        offset = 0
        batch_size = 100
        total = None
        while total is None or offset < total:
            query = urllib.parse.urlencode({
                "dataset": "Wysme/riftbound-cards",
                "config": "default",
                "split": "train",
                "offset": offset,
                "length": batch_size,
            })
            payload = fetch_json(f"{HF_ROWS}?{query}")
            batch = extract_rows(payload)
            if total is None:
                total = int(payload.get("num_rows_total", len(batch)))
            if not batch:
                break
            rows.extend(batch)
            offset += len(batch)
            eprint(f"Fetched {len(rows)}/{total} cards")
        return rows, "https://huggingface.co/datasets/Wysme/riftbound-cards"
    if re.match(r"https?://", source):
        return extract_rows(fetch_json(source)), source
    path = Path(source).expanduser().resolve()
    with path.open("r", encoding="utf-8-sig") as handle:
        return extract_rows(json.load(handle)), str(path)


SCHEMA = """
CREATE TABLE meta (key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE cards (
  source_code TEXT PRIMARY KEY,
  display_code TEXT NOT NULL,
  name TEXT NOT NULL,
  subtitle TEXT NOT NULL,
  full_name TEXT NOT NULL,
  set_code TEXT NOT NULL,
  set_name TEXT NOT NULL,
  collector_number TEXT NOT NULL,
  rarity TEXT NOT NULL,
  domain TEXT NOT NULL,
  domains_json TEXT NOT NULL,
  card_type TEXT NOT NULL,
  labels_json TEXT NOT NULL,
  tags_json TEXT NOT NULL,
  energy REAL,
  power REAL,
  might REAL,
  effect_original TEXT NOT NULL,
  effect_corrected TEXT NOT NULL,
  effect_effective TEXT NOT NULL,
  has_errata INTEGER NOT NULL,
  source_url TEXT NOT NULL,
  scraped_at TEXT NOT NULL
);
CREATE INDEX idx_cards_display_code ON cards(display_code COLLATE NOCASE);
CREATE INDEX idx_cards_full_name ON cards(full_name COLLATE NOCASE);
CREATE INDEX idx_cards_type ON cards(card_type COLLATE NOCASE);
CREATE INDEX idx_cards_set ON cards(set_code COLLATE NOCASE);
"""


INSERT_CARD = """
INSERT INTO cards VALUES (
  :source_code, :display_code, :name, :subtitle, :full_name, :set_code,
  :set_name, :collector_number, :rarity, :domain, :domains_json, :card_type,
  :labels_json, :tags_json, :energy, :power, :might, :effect_original,
  :effect_corrected, :effect_effective, :has_errata, :source_url, :scraped_at
)
"""


def cmd_sync(args: argparse.Namespace) -> int:
    rows, source_name = load_source(args.source)
    normalized = [normalize_card(row) for row in rows]
    normalized = [card for card in normalized if card["source_code"] and card["full_name"]]
    if not normalized:
        raise RuntimeError("No valid cards found; existing database was not changed")
    target = Path(args.db).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary_name = tempfile.mkstemp(prefix="cards-", suffix=".sqlite", dir=target.parent)
    os.close(fd)
    temporary = Path(temporary_name)
    try:
        connection = sqlite3.connect(temporary)
        connection.executescript(SCHEMA)
        connection.execute("INSERT INTO meta VALUES (?, ?)", ("source", source_name))
        connection.execute("INSERT INTO meta VALUES (?, ?)", ("synced_at", dt.datetime.now(dt.timezone.utc).isoformat()))
        for card in normalized:
            db_card = dict(card)
            db_card["domains_json"] = json.dumps(card["domains"], ensure_ascii=False)
            db_card["labels_json"] = json.dumps(card["labels"], ensure_ascii=False)
            db_card["tags_json"] = json.dumps(card["tags"], ensure_ascii=False)
            db_card["has_errata"] = int(card["has_errata"])
            connection.execute(INSERT_CARD, db_card)
        connection.execute("INSERT INTO meta VALUES (?, ?)", ("row_count", str(len(normalized))))
        connection.commit()
        connection.close()
        os.replace(temporary, target)
    finally:
        if temporary.exists():
            temporary.unlink()
    manifest_path = target.with_suffix(".manifest.json")
    manifest = {
        "source": source_name,
        "synced_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "row_count": len(normalized),
        "complete": len(normalized) >= 500,
        "includes_full_effect_text": True,
    }
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Imported {len(normalized)} cards into {target}")
    return 0


def connect(db_path: str | Path) -> sqlite3.Connection:
    path = Path(db_path)
    if not path.exists():
        raise FileNotFoundError(f"Card database not found: {path}. Run sync first.")
    connection = sqlite3.connect(path)
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


def format_stat(value_: Any) -> str:
    if value_ is None:
        return "-"
    number = float(value_)
    return str(int(number)) if number.is_integer() else str(number)


def card_text(card: dict[str, Any]) -> str:
    domains = "/".join(card["domains"]) or "Colorless"
    tags = ", ".join(card["tags"]) or "-"
    effect = card["effect_effective"] or "(no effect text)"
    return (
        f"{card['display_code']} | {card['display_name']} | {card['card_type']} | {domains}\n"
        f"Cost E{format_stat(card['energy'])}/P{format_stat(card['power'])} | Might {format_stat(card['might'])} | Tags {tags}\n"
        f"Effect: {effect}"
    )


def cmd_info(args: argparse.Namespace) -> int:
    connection = connect(args.db)
    count = connection.execute("SELECT COUNT(*) FROM cards").fetchone()[0]
    unique_names = connection.execute("SELECT COUNT(DISTINCT full_name) FROM cards").fetchone()[0]
    effectful = connection.execute("SELECT COUNT(*) FROM cards WHERE effect_effective <> ''").fetchone()[0]
    errata = connection.execute("SELECT COUNT(*) FROM cards WHERE has_errata = 1").fetchone()[0]
    sets = connection.execute("SELECT set_code, COUNT(*) FROM cards GROUP BY set_code ORDER BY set_code").fetchall()
    meta = dict(connection.execute("SELECT key, value FROM meta").fetchall())
    print(json.dumps({
        "printings": count,
        "unique_names": unique_names,
        "records_with_effect_text": effectful,
        "errata_records": errata,
        "sets": dict(sets),
        "meta": meta,
    }, ensure_ascii=False, indent=2))
    return 0


def cmd_doctor(args: argparse.Namespace) -> int:
    db_path = Path(args.db)
    rules_path = Path(args.rules)
    manifest_path = db_path.with_suffix(".manifest.json")
    report: dict[str, Any] = {
        "ready": False,
        "database": str(db_path.resolve()),
        "database_exists": db_path.exists(),
        "manifest_complete": False,
        "rules_exists": rules_path.exists(),
        "problems": [],
    }
    manifest: dict[str, Any] = {}
    if manifest_path.exists():
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8-sig"))
            report["manifest_complete"] = manifest.get("complete") is True
            report["manifest"] = manifest
        except (OSError, json.JSONDecodeError) as error:
            report["problems"].append(f"Unreadable manifest: {error}")
    else:
        report["problems"].append(f"Missing manifest: {manifest_path}")
    if not db_path.exists():
        report["problems"].append("Missing local card database; run sync")
    else:
        try:
            connection = connect(db_path)
            report["printings"] = connection.execute("SELECT COUNT(*) FROM cards").fetchone()[0]
            report["records_with_effect_text"] = connection.execute(
                "SELECT COUNT(*) FROM cards WHERE effect_effective <> ''"
            ).fetchone()[0]
            connection.close()
            if report["printings"] < 500:
                report["problems"].append("Card database is marked too small to be complete")
        except sqlite3.Error as error:
            report["problems"].append(f"Unreadable card database: {error}")
    if not report["manifest_complete"]:
        report["problems"].append("Card manifest is not marked complete")
    if not rules_path.exists():
        report["problems"].append("Missing rules profile")
    else:
        try:
            rules = load_rules(rules_path)
            report["rules_profile"] = rules.get("profile")
            report["rules_as_of"] = rules.get("as_of")
        except (OSError, json.JSONDecodeError) as error:
            report["problems"].append(f"Unreadable rules profile: {error}")
    report["ready"] = not report["problems"]
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["ready"] else 2


def cmd_card(args: argparse.Namespace) -> int:
    card = KeywordRetriever(args.db).get_card(args.card_id)
    print(json.dumps(card, ensure_ascii=False, indent=2) if args.json else card_text(card))
    return 0


def load_rules(path: str | Path) -> dict[str, Any]:
    with Path(path).open("r", encoding="utf-8-sig") as handle:
        return json.load(handle)


def cmd_retrieve(args: argparse.Namespace) -> int:
    retriever = KeywordRetriever(args.db)
    allowed_domains = None
    if args.legend:
        legend = retriever.get_card(args.legend)
        if legend["card_type"].casefold() != "legend":
            raise ValueError(f"Not a Legend: {args.legend}")
        allowed_domains = tuple(legend["domains"])
    rules = None
    if args.legal or args.legend:
        data = load_rules(args.rules)
        rules = RetrievalRules(
            profile=data["profile"], as_of=data["as_of"],
            legal_sets=tuple(data["legal_sets"]),
            banned_cards=tuple(data["banned_cards"]),
            banned_battlefields=tuple(data["banned_battlefields"]),
        )
    query = KeywordQuery(
        keywords=tuple(args.keywords), match=args.match,
        filters=CardFilters(
            colors=tuple(args.colors) if args.colors is not None else None,
            color_mode=args.color_mode, card_type=args.type, set_code=args.set, tag=args.tag,
            max_energy=args.max_energy, min_might=args.min_might,
            allowed_domains=allowed_domains,
        ),
        rules=rules, limit=args.limit, offset=args.offset,
    )
    result = retriever.retrieve(query)
    print(json.dumps(result.to_dict(), ensure_ascii=False, indent=2))
    # An empty page is a successful retrieval, not a command error.
    return 0


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


def cmd_validate(args: argparse.Namespace) -> int:
    report = validate_deck(read_deck(args.deck), connect(args.db), load_rules(args.rules))
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0 if report["valid"] else 2


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


def cmd_export(args: argparse.Namespace) -> int:
    deck = read_deck(args.deck)
    connection = connect(args.db)
    report = validate_deck(deck, connection, load_rules(args.rules))
    if not report["valid"] and not args.allow_invalid:
        eprint(json.dumps(report, ensure_ascii=False, indent=2))
        eprint("Refusing to export an invalid deck; pass --allow-invalid to override.")
        return 2
    output = export_riftatlas(deck, connection, not args.no_codes)
    if args.output:
        Path(args.output).write_text(output, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(output, end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", default=str(DEFAULT_DB), help="Path to cards.sqlite")
    parser.add_argument("--rules", default=str(DEFAULT_RULES), help="Path to rules JSON")
    subparsers = parser.add_subparsers(dest="command", required=True)

    sync = subparsers.add_parser("sync", help="Import a complete local card database")
    sync.add_argument("--source", default="hf", help="hf, an HTTP JSON URL, or a local JSON path")
    sync.set_defaults(func=cmd_sync)
    doctor = subparsers.add_parser("doctor", help="Verify local cards and rules are ready for agent use")
    doctor.set_defaults(func=cmd_doctor)
    info = subparsers.add_parser("info", help="Show database metadata")
    info.set_defaults(func=cmd_info)
    card = subparsers.add_parser("card", help="Show one card with complete effect text")
    card.add_argument("card_id", help="Exact official set/collector code")
    card.add_argument("--json", action="store_true")
    card.set_defaults(func=cmd_card)
    retrieve = subparsers.add_parser("retrieve", help="Filter cards and return IDs; read full records with card")
    retrieve.add_argument("keywords", nargs="*", help="Literal keywords; quote a phrase as one argument")
    retrieve.add_argument("--match", choices=("all", "any"), default="all")
    retrieve.add_argument("--colors", nargs="+", choices=COLORS, help="Filter by official domain/color names")
    retrieve.add_argument("--color-mode", choices=("any", "all", "within", "exact"), default="any")
    retrieve.add_argument("--type", choices=CARD_TYPES)
    retrieve.add_argument("--set")
    retrieve.add_argument("--tag")
    retrieve.add_argument("--max-energy", type=float)
    retrieve.add_argument("--min-might", type=float)
    retrieve.add_argument("--legend", help="Restrict identity and apply the local rules profile")
    retrieve.add_argument("--legal", action="store_true", help="Apply legal sets and bans without a Legend")
    retrieve.add_argument("--limit", type=int, default=20)
    retrieve.add_argument("--offset", type=int, default=0)
    retrieve.set_defaults(func=cmd_retrieve)
    validate = subparsers.add_parser("validate", help="Validate a canonical deck JSON")
    validate.add_argument("deck")
    validate.set_defaults(func=cmd_validate)
    export = subparsers.add_parser("export", help="Export a canonical deck as RiftAtlas text")
    export.add_argument("deck")
    export.add_argument("--output")
    export.add_argument("--no-codes", action="store_true")
    export.add_argument("--allow-invalid", action="store_true")
    export.set_defaults(func=cmd_export)
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    try:
        return int(args.func(args))
    except (FileNotFoundError, ValueError, RuntimeError, sqlite3.Error) as error:
        eprint(f"error: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
