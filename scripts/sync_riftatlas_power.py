"""Enrich the active card DB using RiftAtlas's public, pinned catalog release."""

import argparse
import ast
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import sqlite3
import urllib.request

from deck_support import DEFAULT_DB, decode_card, name_key, presentation_name
from game_state import DOMAINS


CATALOG_URL = "https://riftatlas.com/_next/static/immutable/chunks/43w1rdkmt0ytg.js"
RENDERER_URL = "https://riftatlas.com/_next/static/immutable/chunks/3yjnba3ykwj5_.js"
RULE = "Riftbound Core Rules 2026-10-09, 135.2.e.6: own-domain Power; multi-domain choices; domainless any-domain"
REVIEWED_NAMES = {
    "VEN-060": ("Sky Crusier", "Sky Cruiser"),
    "VEN-096": ("Shadowblade Lurker", "Shadowcloaked Lurker"),
    "SFD-179": ("Corinna Veraza", "Corina Veraza"),
}


def extract_catalog(source):
    """Read a literal array with ast.literal_eval; never execute downloaded JS."""
    match = re.search(r"\blet \w+=\[\{id:", source)
    if not match:
        raise ValueError("Catalog array not found in this release")
    start = source.index("[", match.start())
    quote, escape, depth = None, False, 0
    for end in range(start, len(source)):
        ch = source[end]
        if quote:
            if escape:
                escape = False
            elif ch == "\\":
                escape = True
            elif ch == quote:
                quote = None
        elif ch in ("\"", "'"):
            quote = ch
        elif ch == "[":
            depth += 1
        elif ch == "]":
            depth -= 1
            if depth == 0:
                break
    else:
        raise ValueError("Unclosed catalog array")
    raw = source[start:end + 1]
    parts = []
    for token in re.finditer(r'''"(?:\\.|[^"\\])*"|'(?:\\.|[^'\\])*'|[A-Za-z_$][\w$]*|![01]|.''', raw, re.S):
        value = token.group()
        if re.fullmatch(r"[A-Za-z_$][\w$]*", value):
            value = repr(value) if raw[token.end():].lstrip().startswith(":") else {
                "true": "True", "false": "False", "null": "None"}.get(value, value)
        elif value in ("!0", "!1"):
            value = "True" if value == "!0" else "False"
        parts.append(value)
    cards = ast.literal_eval("".join(parts))
    if not isinstance(cards, list) or any(not isinstance(c, dict) or not isinstance(c.get("id"), str) for c in cards):
        raise ValueError("Invalid catalog records")
    if len({card["id"] for card in cards}) != len(cards):
        raise ValueError("Duplicate source card IDs")
    return cards


def verify_zero_default(renderer):
    pattern = r'"number"==typeof (\w+)\.powerCost\?Math\.max\(0,Math\.trunc\(\1\.powerCost\)\):0'
    match = re.search(pattern, renderer)
    if not match:
        raise ValueError("This release no longer proves that absent powerCost means zero")
    return match.group()


def power_requirements(source_card):
    power = source_card.get("powerCost", 0)
    if isinstance(power, bool) or not isinstance(power, int) or power < 0:
        raise ValueError(f"Invalid Power on {source_card['id']}")
    domains = tuple(d for d in source_card.get("domains", ()) if d != "Unknown")
    if len(set(domains)) != len(domains) or any(d not in DOMAINS[:6] for d in domains):
        raise ValueError(f"Invalid domains on {source_card['id']}")
    # A group is an OR requirement, not one simultaneous charge for every domain.
    return power, ([] if power == 0 else [{"amount": power, "domains": list(domains or DOMAINS[:6])}])


def source_index(cards):
    exact = {card["id"]: card for card in cards}
    aliases = {}
    for card in cards:
        base = card.get("baseCardId")
        # Map the same explicitly declared foil printing; never strip to a base card.
        if card.get("isAltArt") and base and card["id"] == base + "S":
            aliases[base + "-STAR"] = card
    return exact, aliases


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(path)


def fetch(url, path, offline):
    if not offline:
        request = urllib.request.Request(url, headers={"User-Agent": "rift-builder-power-sync/1.0"})
        with urllib.request.urlopen(request, timeout=60) as response:
            content = response.read()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(content)
    return path.read_text(encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--offline", action="store_true", help="Use the archived release without network requests")
    args = parser.parse_args()
    db = args.db.resolve()
    if not db.is_file() or any(part in (".data_versions", "revisions") for part in db.parts):
        raise ValueError("Only an existing active DB can be enriched; immutable snapshots are forbidden")
    root = Path(__file__).resolve().parents[1]
    cache = root / "data" / "sources" / "riftatlas"
    catalog_js = fetch(CATALOG_URL, cache / "card-catalog.js", args.offline)
    renderer_js = fetch(RENDERER_URL, cache / "cost-renderer.js", args.offline)
    zero_evidence = verify_zero_default(renderer_js)
    cards = extract_catalog(catalog_js)
    atomic_json(cache / "catalog.json", cards)
    exact, aliases = source_index(cards)
    fetched_at = datetime.now(timezone.utc).isoformat()
    source_hash = hashlib.sha256(catalog_js.encode()).hexdigest()
    original_hash = hashlib.sha256(db.read_bytes()).hexdigest()
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    rows = [decode_card(row) for row in connection.execute("SELECT * FROM cards")]
    updates, missing, mismatches, non_applicable, other_differences = [], [], [], [], []
    for row in rows:
        applicable = row["card_type"] in ("Unit", "Spell", "Gear") and "Token" not in row["labels"]
        if not applicable:
            non_applicable.append(row["display_code"])
            continue
        source = exact.get(row["display_code"]) or aliases.get(row["display_code"])
        if source is None:
            missing.append(row["display_code"])
            continue
        same_name = name_key(source["name"]) == name_key(presentation_name(row))
        signature_name = source.get("signatureType") == row["card_type"] and name_key(source["name"]) == name_key(row["name"])
        reviewed_name = REVIEWED_NAMES.get(row["display_code"]) == (row["full_name"], source["name"])
        if not (same_name or signature_name or reviewed_name) or row["card_type"] not in source["type"].split():
            mismatches.append({"card_id": row["display_code"], "reason": "identity", "source_id": source["id"]})
            continue
        power, requirements = power_requirements(source)
        if row["power"] is not None and row["power"] != power:
            mismatches.append({"card_id": row["display_code"], "reason": "known_power_conflict",
                               "old": row["power"], "source": power})
            continue
        if row["energy"] != source.get("energyCost") or (row["card_type"] == "Unit" and row["might"] != source.get("might")):
            other_differences.append({"card_id": row["display_code"], "old_energy": row["energy"],
                                      "riftatlas_energy": source.get("energyCost"), "old_might": row["might"],
                                      "riftatlas_might": source.get("might"), "action": "unchanged; outside Power scope"})
        updates.append({"source_code": row["source_code"], "card_id": row["display_code"],
                        "source_id": source["id"], "old_power": row["power"], "power": power,
                        "power_cost": requirements, "url": "https://riftatlas.com/card/" + source["id"]})
    report = {"catalog_url": CATALOG_URL, "renderer_url": RENDERER_URL, "fetched_at": fetched_at,
              "catalog_sha256": source_hash, "renderer_sha256": hashlib.sha256(renderer_js.encode()).hexdigest(),
              "zero_default_evidence": zero_evidence, "power_domain_rule": RULE,
              "records": len(rows), "source_records": len(cards), "applicable": len(rows) - len(non_applicable),
              "matched": len(updates), "missing": missing, "conflicts": mismatches,
              "other_attribute_differences": other_differences,
              "non_applicable": non_applicable, "filled_null_power": sum(u["old_power"] is None for u in updates),
              "cost_groups": dict(Counter("zero" if not u["power_cost"] else "multi_domain" if len(u["power_cost"][0]["domains"]) > 1 else "single_domain" for u in updates)),
              "updates": updates}
    if missing or mismatches:
        connection.close()
        atomic_json(root / "reports" / "riftatlas-power-sync.json", report)
        print(json.dumps({k: v for k, v in report.items() if k not in ("updates", "non_applicable")}, ensure_ascii=True, indent=2))
        return 1  # No partial DB writes on an unresolved applicable card.
    backup = root / "data" / "backups" / f"cards-before-riftatlas-power-{original_hash[:16]}.sqlite"
    backup.parent.mkdir(parents=True, exist_ok=True)
    if not backup.exists():
        backup_db = sqlite3.connect(backup)
        try:
            connection.backup(backup_db)
        finally:
            backup_db.close()
    try:
        connection.execute("BEGIN IMMEDIATE")
        columns = {row[1] for row in connection.execute("PRAGMA table_info(cards)")}
        for name in ("power_cost_json", "power_source", "power_source_sha256", "power_verified_at"):
            if name not in columns:
                connection.execute(f"ALTER TABLE cards ADD COLUMN {name} TEXT")
        for update in updates:
            connection.execute("UPDATE cards SET power=?, power_cost_json=?, power_source=?, power_source_sha256=?, power_verified_at=? WHERE source_code=?",
                               (update["power"], json.dumps(update["power_cost"], sort_keys=True),
                                update["url"] + " | " + RULE, source_hash, fetched_at, update["source_code"]))
        connection.execute("INSERT OR REPLACE INTO meta(key,value) VALUES('riftatlas_power_source',?)",
                           (json.dumps({"url": CATALOG_URL, "sha256": source_hash, "verified_at": fetched_at}),))
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
    report["backup"] = str(backup)
    report["database_sha256"] = hashlib.sha256(db.read_bytes()).hexdigest()
    atomic_json(root / "reports" / "riftatlas-power-sync.json", report)
    manifest_path = db.parent / "cards.manifest.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        manifest["power_enrichment"] = {"source": CATALOG_URL, "catalog_sha256": source_hash,
                                        "verified_at": fetched_at, "applicable_records": len(updates),
                                        "complete_for_applicable_cards": True}
        atomic_json(manifest_path, manifest)
    print(json.dumps({k: v for k, v in report.items() if k not in ("updates", "non_applicable")}, ensure_ascii=True, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
