"""One card representation shared by lookup, retrieval and deck operations."""

from __future__ import annotations

import json
import re
import sqlite3
import unicodedata
from typing import Any, Iterable, cast

from .models import CardInfo


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
