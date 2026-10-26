from __future__ import annotations

import importlib.util
import argparse
import contextlib
import io
import json
import sqlite3
import copy
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("riftbound", ROOT / "scripts" / "riftbound.py")
RIFTBOUND = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(RIFTBOUND)


class RiftboundMvpTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.connection = RIFTBOUND.connect(ROOT / "data" / "cards.sqlite")
        cls.rules = RIFTBOUND.load_rules(ROOT / "data" / "rules.json")
        cls.deck = RIFTBOUND.read_deck(ROOT / "tests" / "fixtures" / "rengar-radiance.json")

    @classmethod
    def tearDownClass(cls) -> None:
        cls.connection.close()

    def test_database_is_complete_and_full_text(self) -> None:
        count = self.connection.execute("SELECT COUNT(*) FROM cards").fetchone()[0]
        effectful = self.connection.execute(
            "SELECT COUNT(*) FROM cards WHERE effect_effective <> ''"
        ).fetchone()[0]
        self.assertGreaterEqual(count, 500)
        self.assertGreater(effectful, 500)

    def test_doctor_reports_ready(self) -> None:
        arguments = argparse.Namespace(
            db=str(ROOT / "data" / "cards.sqlite"),
            rules=str(ROOT / "data" / "rules.json"),
        )
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exit_code = RIFTBOUND.cmd_doctor(arguments)
        report = json.loads(output.getvalue())
        self.assertEqual(exit_code, 0)
        self.assertTrue(report["ready"])

    def test_exact_lookup_preserves_complete_effect(self) -> None:
        card = RIFTBOUND.resolve_card(self.connection, "UNL-184")
        self.assertEqual(card["display_name"], "Thrill of the Hunt")
        self.assertIn("Banish a friendly unit", card["effect_effective"])

    def test_legend_name_is_export_ready(self) -> None:
        legend = RIFTBOUND.resolve_card(self.connection, "UNL-183")
        self.assertEqual(legend["display_name"], "Rengar, Pridestalker")

    def test_name_key_normalizes_smart_punctuation(self) -> None:
        self.assertEqual(
            RIFTBOUND.name_key("The Arena’s Greatest"),
            RIFTBOUND.name_key("The Arena's Greatest"),
        )

    def test_sample_deck_is_valid(self) -> None:
        report = RIFTBOUND.validate_deck(self.deck, self.connection, self.rules)
        self.assertTrue(report["valid"], json.dumps(report, ensure_ascii=False, indent=2))
        self.assertEqual(report["totals"]["main_deck"], 40)
        self.assertEqual(report["totals"]["sideboard"], 10)

    def test_colorless_label_does_not_violate_legend_identity(self) -> None:
        connection = sqlite3.connect(":memory:")
        try:
            self.connection.backup(connection)
            connection.row_factory = sqlite3.Row
            row = dict(connection.execute("SELECT * FROM cards WHERE display_code = 'OGN-136'").fetchone())
            row.update(
                source_code="ogn-998-test", display_code="OGN-998", collector_number="998-298",
                name="Neutral Test Unit", full_name="Neutral Test Unit", domains_json='["Colorless"]',
                domain="Colorless",
            )
            connection.execute(RIFTBOUND.INSERT_CARD, row)
            deck = copy.deepcopy(self.deck)
            entry = next(item for item in deck["main_deck"] if item["code"] == "OGN-136")
            entry["code"] = "OGN-998"
            report = RIFTBOUND.validate_deck(deck, connection, self.rules)
            self.assertTrue(report["valid"], report["errors"])
        finally:
            connection.close()

    def test_riftatlas_export_separates_champion(self) -> None:
        exported = RIFTBOUND.export_riftatlas(self.deck, self.connection, True)
        self.assertIn("1 Rengar, Pridestalker [UNL-183]", exported)
        self.assertIn("Champion:\n1 Rengar, Pouncing [SFD-025]", exported)
        main_section = exported.split("MainDeck:\n", 1)[1].split("\n\nBattlefields:", 1)[0]
        self.assertIn("1 Rengar, Pouncing [SFD-025]", main_section)


if __name__ == "__main__":
    unittest.main()
