from __future__ import annotations

import hashlib
import json
import sqlite3
import subprocess
import sys
import tempfile
import unittest
from contextlib import closing
from dataclasses import dataclass, replace
from pathlib import Path
from unittest.mock import patch


WORKSPACE = Path(__file__).resolve().parents[1]
SKILL = WORKSPACE / ".agents" / "skills" / "riftbound-deck-mvp"
sys.path.insert(0, str(SKILL / "scripts"))

import riftbound
from riftbound_retrieval import (
    BaseRetriever, CardFilters, KeywordQuery, KeywordRetriever, RetrievalQuery,
    RetrievalResult, RetrievalRules,
)


class RetrievalTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory(prefix="riftbound-retrieval-test-")
        self.db = Path(self.temporary.name) / "cards.sqlite"
        with closing(sqlite3.connect(self.db)) as connection:
            connection.executescript(riftbound.SCHEMA)
        self.retriever = KeywordRetriever(self.db)

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def add_card(
        self, name="Alpha", code="TST-001", *, domains=("Body",),
        card_type="Unit", energy=2, might=3, tags=(), effect="Draw 1.",
        corrected="", rarity="Common", set_code="TST",
    ) -> None:
        card = riftbound.normalize_card({
            "cardCode": code.lower(), "setCode": set_code,
            "cardNumber": code.split("-", 1)[1], "name": name, "fullName": name,
            "domains": list(domains), "domain": domains[0] if domains else "",
            "cardType": card_type, "cardTypeLabels": [card_type],
            "energy": energy, "might": might, "power": 1,
            "tags": list(tags), "abilityOriginal": effect,
            "abilityCorrected": corrected, "hasErrata": bool(corrected),
            "rarity": rarity, "sourceUrl": "https://example.invalid/card",
        })
        for field in ("domains", "labels", "tags"):
            card[field + "_json"] = json.dumps(card[field])
        with closing(sqlite3.connect(self.db)) as connection, connection:
            connection.execute(riftbound.INSERT_CARD, card)

    def ids(self, query: KeywordQuery) -> tuple[str, ...]:
        return self.retriever.retrieve(query).card_ids

    def test_base_requires_a_backend(self) -> None:
        with self.assertRaises(TypeError):
            BaseRetriever()

    def test_retrieval_only_returns_ids_without_hydration(self) -> None:
        self.add_card()
        with patch.object(self.retriever, "get_card", side_effect=AssertionError("No eager hydration")):
            result = self.retriever.retrieve(KeywordQuery(keywords=("draw",)))
        self.assertIsInstance(result, RetrievalResult)
        self.assertEqual(result.card_ids, ("TST-001",))
        payload = result.to_dict()
        self.assertNotIn("hits", payload)
        self.assertNotIn("effect_effective", json.dumps(payload))
        self.assertEqual(payload["card_ids"], ["TST-001"])

    def test_get_card_returns_full_corrected_card_on_demand(self) -> None:
        text = "[Reaction]\nDraw 2.\n" + "Condition details. " * 80
        self.add_card(effect="Kill a unit.", corrected=text)
        self.assertEqual(self.ids(KeywordQuery(keywords=("draw",))), ("TST-001",))
        card = self.retriever.get_card("tst-001")
        self.assertEqual(card["effect_effective"], text)
        self.assertEqual(card["effect_original"], "Kill a unit.")
        self.assertTrue(card["has_errata"])
        self.assertEqual(card["domains"], ["Body"])
        self.assertEqual((card["energy"], card["power"], card["might"]), (2, 1, 3))
        self.assertEqual(self.ids(KeywordQuery(keywords=("kill",))), ())

    def test_get_card_is_exact_id_not_fuzzy_name(self) -> None:
        self.add_card()
        for value in ("Alpha", "TST-999", "", None):
            with self.subTest(value=value), self.assertRaises(ValueError):
                self.retriever.get_card(value)

    def test_all_and_any_keywords_can_match_different_fields(self) -> None:
        self.add_card(name="Runner", effect="Draw 1.")
        self.add_card(name="Other", code="TST-002", effect="Draw 2.")
        self.add_card(name="Runner Up", code="TST-003", effect="Move me.")
        query = KeywordQuery(keywords=("Runner", "draw"))
        self.assertEqual(self.ids(query), ("TST-001",))
        self.assertEqual(self.retriever.retrieve(replace(query, match="any")).total, 3)

    def test_phrase_is_literal_and_case_insensitive(self) -> None:
        self.add_card(effect="When you play me, draw 1.")
        self.add_card(name="Other", code="TST-002", effect="Play a unit for me.")
        self.assertEqual(self.ids(KeywordQuery(keywords=("PLAY ME",))), ("TST-001",))

    def test_name_code_and_tag_matches(self) -> None:
        self.add_card(name="ÉLAN", tags=("Hunter",), effect="")
        for keyword in ("élan", "tst-001", "hunter"):
            with self.subTest(keyword=keyword):
                self.assertEqual(self.ids(KeywordQuery(keywords=(keyword,))), ("TST-001",))

    def test_like_wildcards_and_backslash_are_literal(self) -> None:
        self.add_card(effect="Gain 10% and use a_b at C:\\cards.")
        self.add_card(name="Other", code="TST-002", effect="Ordinary text.")
        for keyword in ("%", "_", "\\", "a_b", "C:\\cards"):
            with self.subTest(keyword=keyword):
                self.assertEqual(self.ids(KeywordQuery(keywords=(keyword,))), ("TST-001",))

    def test_keywords_do_not_match_json_syntax(self) -> None:
        self.add_card(tags=("Hunter",), effect="")
        self.assertEqual(self.ids(KeywordQuery(keywords=('"',))), ())

    def test_sql_injection_is_not_executed(self) -> None:
        self.add_card()
        self.assertEqual(self.ids(KeywordQuery(keywords=("' OR 1=1; DROP TABLE cards; --",))), ())
        self.assertEqual(self.ids(KeywordQuery()), ("TST-001",))

    def test_filters_are_combined_and_tag_is_exact(self) -> None:
        self.add_card(tags=("Hunter",))
        self.add_card(name="Other", code="TST-002", domains=("Mind",), tags=("Hunterling",))
        query = KeywordQuery(filters=CardFilters(
            colors=("body",), card_type="unit", set_code="tst", tag="hunter", max_energy=2, min_might=3,
        ))
        self.assertEqual(self.ids(query), ("TST-001",))
        self.assertEqual(self.ids(replace(query, filters=replace(query.filters, tag="Hunt"))), ())

    def test_missing_stats_are_not_zero(self) -> None:
        self.add_card(energy=None, might=None)
        self.assertEqual(self.ids(KeywordQuery(filters=CardFilters(max_energy=0))), ())
        self.assertEqual(self.ids(KeywordQuery(filters=CardFilters(min_might=0))), ())

    def test_color_modes_handle_multicolor_and_both_colorless_encodings(self) -> None:
        self.add_card(name="Body", domains=("Body",))
        self.add_card(name="Dual", code="TST-002", domains=("Body", "Mind"))
        self.add_card(name="Neutral", code="TST-003", domains=())
        self.add_card(name="Explicit Neutral", code="TST-004", domains=("Colorless",))
        self.add_card(name="Mind", code="TST-005", domains=("Mind",))
        cases = [
            (("Body",), "any", {"TST-001", "TST-002"}),
            (("Body", "Mind"), "all", {"TST-002"}),
            (("Body",), "within", {"TST-001", "TST-003", "TST-004"}),
            (("Body",), "exact", {"TST-001"}),
            (("Body", "Mind"), "exact", {"TST-002"}),
            (("Colorless",), "exact", {"TST-003", "TST-004"}),
            (("Body", "Colorless"), "any", {"TST-001", "TST-002", "TST-003", "TST-004"}),
            (("Colorless",), "all", {"TST-003", "TST-004"}),
            ((), "within", {"TST-003", "TST-004"}),
        ]
        for colors, mode, expected in cases:
            with self.subTest(colors=colors, mode=mode):
                self.assertEqual(set(self.ids(KeywordQuery(filters=CardFilters(colors=colors, color_mode=mode)))), expected)

    def test_legend_identity_and_explicit_colors_are_intersected(self) -> None:
        self.add_card()
        self.add_card(name="Dual", code="TST-002", domains=("Body", "Mind"))
        self.add_card(name="Neutral", code="TST-003", domains=("Colorless",))
        query = KeywordQuery(filters=CardFilters(allowed_domains=("Body",), colors=("Mind",)))
        self.assertEqual(self.ids(query), ())
        query = replace(query, filters=CardFilters(allowed_domains=("Body",)))
        self.assertEqual(set(self.ids(query)), {"TST-001", "TST-003"})
        self.assertEqual(self.ids(replace(query, filters=CardFilters(allowed_domains=()))), ("TST-003",))

    def test_rules_filter_before_selecting_a_representative(self) -> None:
        self.add_card(name="Same", code="AAA-001", set_code="AAA")
        self.add_card(name="Same", code="TST-001")
        rules = RetrievalRules(profile="test", as_of="2026-10-26", legal_sets=("TST",))
        self.assertEqual(self.ids(KeywordQuery(rules=rules)), ("TST-001",))

    def test_variant_wording_is_not_used_instead_of_base_effect(self) -> None:
        self.add_card(name="Same", effect="Draw 1.")
        self.add_card(name="Same", code="TST-001a", effect="Kill a unit.", rarity="Showcase")
        self.assertEqual(self.ids(KeywordQuery()), ("TST-001",))
        self.assertEqual(self.ids(KeywordQuery(keywords=("kill",))), ())
        self.assertEqual(self.ids(KeywordQuery(keywords=("draw",))), ("TST-001",))

    def test_special_and_rune_ids_are_not_truncated_to_three_digits(self) -> None:
        self.add_card(name="Special", code="TST-SP1-005")
        self.add_card(name="Rune", code="TST-R01", card_type="Rune")
        result = self.ids(KeywordQuery())
        self.assertEqual(set(result), {"TST-SP1", "TST-R01"})
        self.assertEqual(self.retriever.get_card("TST-SP1")["display_code"], "TST-SP1")
        self.assertEqual(self.retriever.get_card("TST-R01")["display_code"], "TST-R01")

    def test_bans_and_battlefield_identity_exception(self) -> None:
        self.add_card(name="Banned Unit")
        self.add_card(name="Arena’s End", code="TST-002", card_type="Battlefield")
        self.add_card(name="Allowed Field", code="TST-003", card_type="Battlefield", domains=("Mind",))
        rules = RetrievalRules(
            profile="test", as_of="2026-10-26", legal_sets=("TST",),
            banned_cards=("banned unit",), banned_battlefields=("Arena's End",),
        )
        query = KeywordQuery(rules=rules, filters=CardFilters(allowed_domains=("Body",)))
        self.assertEqual(self.ids(query), ("TST-003",))

    def test_deduplication_before_limit_and_stable_pages(self) -> None:
        for number in range(12):
            self.add_card(name="Alpha", code=f"TST-{number:03d}", rarity="Promo" if number else "Common")
        self.add_card(name="Bravo", code="TST-020")
        self.add_card(name="Charlie", code="TST-021")
        query = KeywordQuery(limit=2)
        first = self.retriever.retrieve(query)
        second = self.retriever.retrieve(replace(query, offset=2))
        self.assertEqual(first.total, 3)
        self.assertEqual(first.card_ids, ("TST-000", "TST-020"))
        self.assertTrue(first.has_more)
        self.assertEqual(second.card_ids, ("TST-021",))
        self.assertFalse(second.has_more)

    def test_empty_and_out_of_range_pages_have_one_result_shape(self) -> None:
        self.add_card()
        for query, total in ((KeywordQuery(keywords=("missing",)), 0), (KeywordQuery(offset=100), 1)):
            result = self.retriever.retrieve(query)
            self.assertEqual(result.total, total)
            self.assertEqual(result.card_ids, ())
            self.assertFalse(result.has_more)
            self.assertEqual(json.loads(json.dumps(result.to_dict())), result.to_dict())

    def test_input_validation(self) -> None:
        for kwargs in ({"limit": 0}, {"limit": True}, {"offset": -1}, {"keywords": "draw"},
                       {"keywords": (" ",)}, {"match": "sql"}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                KeywordQuery(**kwargs)
        for kwargs in ({"max_energy": float("nan")}, {"min_might": -1}, {"max_energy": True},
                       {"colors": "Body"}, {"colors": ("Unknown",)}, {"color_mode": "sometimes"},
                       {"card_type": "Unknown"}, {"allowed_domains": "Body"}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                CardFilters(**kwargs)
        with self.assertRaises(ValueError):
            self.retriever.retrieve(RetrievalQuery())

    def test_missing_database_is_not_created(self) -> None:
        missing = self.db.with_name("missing.sqlite")
        for operation in (lambda: KeywordRetriever(missing).retrieve(KeywordQuery()),
                          lambda: KeywordRetriever(missing).get_card("TST-001")):
            with self.assertRaises(FileNotFoundError):
                operation()
        self.assertFalse(missing.exists())

    def test_retrieval_and_hydration_leave_database_unchanged(self) -> None:
        self.add_card()
        before = hashlib.sha256(self.db.read_bytes()).digest()
        self.ids(KeywordQuery(keywords=("draw",)))
        self.retriever.get_card("TST-001")
        self.assertEqual(hashlib.sha256(self.db.read_bytes()).digest(), before)

    def test_new_backend_is_not_coupled_to_keyword_query_or_card_hydration(self) -> None:
        @dataclass(frozen=True)
        class TextQuery(RetrievalQuery):
            text: str = ""

        class ExampleRetriever(BaseRetriever[TextQuery]):
            name = "example"
            query_type = TextQuery

            def _retrieve(self, query):
                return ["TST-001", "TST-001", "TST-002"]

            def get_card(self, card_id):
                raise NotImplementedError("Not used during retrieval")

        result = ExampleRetriever().retrieve(TextQuery(text="a natural language request", limit=1))
        self.assertEqual(result.card_ids, ("TST-001",))
        self.assertEqual(result.total, 2)
        self.assertEqual(result.to_dict()["query"]["text"], "a natural language request")
        self.assertNotIn("keywords", result.to_dict()["query"])

    def test_cli_returns_ids_and_card_command_hydrates_them(self) -> None:
        self.add_card()
        for keywords, total in ((["draw"], 1), (["missing"], 0)):
            completed = subprocess.run(
                [sys.executable, str(SKILL / "scripts" / "riftbound.py"), "--db", str(self.db), "retrieve", *keywords],
                cwd=self.temporary.name, capture_output=True, text=True, encoding="utf-8",
            )
            self.assertEqual(completed.returncode, 0, completed.stderr)
            result = json.loads(completed.stdout)
            self.assertEqual(result["total"], total)
            self.assertIsInstance(result["card_ids"], list)
        completed = subprocess.run(
            [sys.executable, str(SKILL / "scripts" / "riftbound.py"), "--db", str(self.db), "card", "TST-001", "--json"],
            cwd=self.temporary.name, capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        self.assertEqual(json.loads(completed.stdout)["effect_effective"], "Draw 1.")

    def test_removed_cli_commands_and_invalid_query_are_rejected(self) -> None:
        for arguments in (["search", "draw"], ["candidates"], ["retrieve", "--limit", "0"],
                          ["retrieve", "--domain", "Body"], ["retrieve", "--all-printings"]):
            completed = subprocess.run(
                [sys.executable, str(SKILL / "scripts" / "riftbound.py"), "--db", str(self.db), *arguments],
                capture_output=True, text=True, encoding="utf-8",
            )
            self.assertEqual(completed.returncode, 2)

    def test_cli_colors_and_legend_scope(self) -> None:
        completed = subprocess.run(
            [sys.executable, str(SKILL / "scripts" / "riftbound.py"), "retrieve",
             "--legend", "UNL-183", "--colors", "Body", "--color-mode", "exact", "--limit", "1"],
            capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(completed.returncode, 0, completed.stderr)
        result = json.loads(completed.stdout)
        self.assertEqual(result["query"]["rules"]["as_of"], "2026-10-09")
        self.assertEqual(result["query"]["filters"]["colors"], ["Body"])
        completed = subprocess.run(
            [sys.executable, str(SKILL / "scripts" / "riftbound.py"), "retrieve", "--legend", "SFD-025"],
            capture_output=True, text=True, encoding="utf-8",
        )
        self.assertEqual(completed.returncode, 2)


if __name__ == "__main__":
    unittest.main()
