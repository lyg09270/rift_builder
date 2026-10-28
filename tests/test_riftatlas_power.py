"""Source parsing and domain-choice semantics; no network requests or DB writes."""

from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from sync_riftatlas_power import extract_catalog, power_requirements, source_index, verify_zero_default


class RiftAtlasPowerExamples(unittest.TestCase):
    def test_literal_parser_preserves_strings_and_handles_minified_booleans(self):
        cards = extract_catalog('let n=[{id:"X-001",name:"A [unit]",text:\'I can draw.\',powerCost:1,isAltArt:!0}];')
        self.assertEqual(cards[0]["name"], "A [unit]")
        self.assertEqual(cards[0]["text"], "I can draw.")
        self.assertTrue(cards[0]["isAltArt"])

    def test_downloaded_expressions_are_not_executed(self):
        with self.assertRaises((ValueError, SyntaxError)):
            extract_catalog('let n=[{id:"X-001",powerCost:dangerous_function()}];')

    def test_zero_default_needs_source_evidence(self):
        evidence = '"number"==typeof d.powerCost?Math.max(0,Math.trunc(d.powerCost)):0'
        self.assertEqual(verify_zero_default(evidence), evidence)
        with self.assertRaises(ValueError):
            verify_zero_default('return unknownCost;')
        self.assertEqual(power_requirements({"id": "X-001", "domains": ["Fury"]}), (0, []))

    def test_multidomain_requirement_is_one_choice_group(self):
        power, groups = power_requirements({"id": "X-001", "powerCost": 3, "domains": ["Fury", "Mind"]})
        self.assertEqual(power, 3)
        self.assertEqual(groups, [{"amount": 3, "domains": ["Fury", "Mind"]}])

    def test_domainless_requirement_accepts_all_six_domains(self):
        power, groups = power_requirements({"id": "X-001", "powerCost": 1, "domains": ["Unknown"]})
        self.assertEqual(power, 1)
        self.assertEqual(len(groups[0]["domains"]), 6)

    def test_foil_alias_requires_explicit_source_relationship(self):
        _, aliases = source_index([{"id": "X-001S", "baseCardId": "X-001", "isAltArt": True}])
        self.assertEqual(aliases["X-001-STAR"]["id"], "X-001S")
        _, aliases = source_index([{"id": "X-001S"}])
        self.assertEqual(aliases, {})


if __name__ == "__main__":
    unittest.main(verbosity=2)
