"""Literal keyword/color filtering returns IDs; full card text is loaded separately."""

from __future__ import annotations

import json
import sqlite3
from contextlib import closing
from pathlib import Path
from typing import Iterable

from .base import BaseRetriever
from .cards import decode_card, name_key, preferred, public_card_id
from .models import CardInfo, KeywordQuery


class KeywordRetriever(BaseRetriever[KeywordQuery]):
    name = "keyword"
    query_type = KeywordQuery

    def __init__(self, db_path: str | Path):
        self.db_path = Path(db_path).expanduser().resolve()

    def _connect(self) -> sqlite3.Connection:
        if not self.db_path.is_file():
            raise FileNotFoundError(f"Card database not found: {self.db_path}. Run sync first.")
        connection = sqlite3.connect(self.db_path.as_uri() + "?mode=ro", uri=True)
        connection.row_factory = sqlite3.Row
        connection.create_function("casefold", 1, lambda value: str(value).casefold(), deterministic=True)
        connection.create_function("name_key", 1, name_key, deterministic=True)
        connection.create_function("public_card_id", 3, public_card_id, deterministic=True)
        return connection

    def get_card(self, card_id: str) -> CardInfo:
        if not isinstance(card_id, str) or not card_id.strip():
            raise ValueError("card_id must be a nonempty official card code")
        with closing(self._connect()) as connection:
            rows = connection.execute(
                "SELECT * FROM cards WHERE public_card_id(set_code, collector_number, display_code) = ? COLLATE NOCASE",
                (card_id.strip(),),
            ).fetchall()
        cards = preferred(decode_card(row) for row in rows)
        if not cards:
            raise ValueError(f"Unknown card ID: {card_id}")
        if len(cards) != 1:
            raise ValueError(f"Ambiguous card ID in local data: {card_id}")
        return cards[0]

    @staticmethod
    def _like_literal(text: str) -> str:
        return "%" + text.casefold().replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_") + "%"

    @staticmethod
    def _colors(colors: tuple[str, ...], mode: str) -> tuple[str, list]:
        requested = sorted({value.casefold() for value in colors if value.casefold() != "colorless"})
        wants_colorless = any(value.casefold() == "colorless" for value in colors)
        actual = "(SELECT casefold(value) FROM json_each(cards.domains_json) WHERE casefold(value) != 'colorless')"
        neutral = f"NOT EXISTS {actual}"
        within = (
            "NOT EXISTS (SELECT 1 FROM json_each(cards.domains_json) "
            "WHERE casefold(value) != 'colorless' AND casefold(value) "
            "NOT IN (SELECT value FROM json_each(?)))"
        )
        contains_all = f"NOT EXISTS (SELECT 1 FROM json_each(?) WHERE value NOT IN {actual})"
        values = json.dumps(requested)
        if mode == "any":
            clause = (
                "EXISTS (SELECT 1 FROM json_each(cards.domains_json) "
                "WHERE casefold(value) IN (SELECT value FROM json_each(?)))"
            )
            return (f"({clause} OR {neutral})" if wants_colorless else clause), [values]
        if mode == "all":
            return (f"({contains_all} AND {neutral})" if wants_colorless else contains_all), [values]
        if mode == "within":
            return within, [values]
        return f"({within} AND {contains_all})", [values, values]

    def _retrieve(self, query: KeywordQuery) -> Iterable[str]:
        clauses: list[str] = []
        params: list = []
        filters = query.filters
        for column, expected in (("card_type", filters.card_type), ("set_code", filters.set_code)):
            if expected is not None:
                clauses.append(f"casefold({column}) = ?")
                params.append(expected.strip().casefold())
        if filters.tag is not None:
            clauses.append("EXISTS (SELECT 1 FROM json_each(cards.tags_json) WHERE casefold(value) = ?)")
            params.append(filters.tag.strip().casefold())
        for column, operator, number in (("energy", "<=", filters.max_energy), ("might", ">=", filters.min_might)):
            if number is not None:
                clauses.append(f"{column} {operator} ?")
                params.append(number)
        if filters.colors is not None:
            clause, values = self._colors(filters.colors, filters.color_mode)
            clauses.append(clause)
            params.extend(values)
        if filters.allowed_domains is not None:
            clause, values = self._colors(filters.allowed_domains, "within")
            # This identity exception is shared with the local constructed validator.
            clauses.append(f"(casefold(card_type) = 'battlefield' OR {clause})")
            params.extend(values)
        if query.rules is not None:
            rules = query.rules
            clauses.append("casefold(set_code) IN (SELECT casefold(value) FROM json_each(?))")
            params.append(json.dumps(rules.legal_sets))
            clauses.append("(casefold(card_type) NOT IN ('unit', 'gear', 'spell') OR "
                           "name_key(full_name) NOT IN (SELECT name_key(value) FROM json_each(?)))")
            params.append(json.dumps(rules.banned_cards))
            clauses.append("(casefold(card_type) != 'battlefield' OR "
                           "name_key(full_name) NOT IN (SELECT name_key(value) FROM json_each(?)))")
            params.append(json.dumps(rules.banned_battlefields))
        keyword_clauses = []
        for keyword in query.keywords:
            columns = [
                f"casefold({column}) LIKE ? ESCAPE '\\'"
                for column in ("full_name", "display_code", "effect_effective")
            ]
            columns.append("EXISTS (SELECT 1 FROM json_each(cards.tags_json) WHERE casefold(value) LIKE ? ESCAPE '\\')")
            keyword_clauses.append("(" + " OR ".join(columns) + ")")
            params.extend([self._like_literal(keyword)] * 4)
        scope = " AND ".join(clauses) if clauses else "1"
        keywords = (" AND " if query.match == "all" else " OR ").join(keyword_clauses) or "1"
        # Choose an eligible representative BEFORE text matching. Variant text can
        # be abbreviated; it must not generate a hit that the base text contradicts.
        # Only ID columns leave SQLite; get_card is the explicit hydration path.
        sql = f"""
            WITH scoped AS (
                SELECT cards.*,
                       ROW_NUMBER() OVER (
                           PARTITION BY casefold(full_name)
                           ORDER BY casefold(rarity) IN ('showcase', 'alternate art', 'promo'),
                                    instr(casefold(display_code), 'sp') > 0,
                                    length(public_card_id(set_code, collector_number, display_code)),
                                    public_card_id(set_code, collector_number, display_code), source_code
                       ) AS printing_rank
                FROM cards WHERE {scope}
            )
            SELECT public_card_id(set_code, collector_number, display_code) AS card_id
            FROM scoped AS cards
            WHERE printing_rank = 1 AND ({keywords})
            ORDER BY casefold(full_name), card_id, source_code
        """
        with closing(self._connect()) as connection:
            rows = connection.execute(sql, params).fetchall()
        return [row["card_id"] for row in rows]
