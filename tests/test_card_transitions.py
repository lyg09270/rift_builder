"""Explicitly requested semantic examples, independent expected state values."""

from dataclasses import replace
from pathlib import Path
import sys
import unittest

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from card import CardContext, UnitTarget
from card_converter import CardConverter
from game_state import STATE_SIZE, StateEnum as S, game_state
from state_transition import TransitionError


def fixture(text, *, card_type="Spell", energy=1, power=0, might=None):
    """Synthetic rules example; never inserted into the real card database."""
    return CardConverter().convert({
        "display_code": "FIXTURE-001", "full_name": "Rules example", "card_type": card_type,
        "energy": energy, "power": power, "might": might, "domains": ["Fury"],
        "labels": [card_type], "tags": [], "effect_effective": text,
        "effect_original": text, "source_url": "synthetic-test-only",
    })


def position(target=None):
    state = game_state()
    state.update({S.PHASE: 6, S.P0_HAND_COUNT: 5, S.P0_DECK_COUNT: 20,
                  S.P1_DECK_COUNT: 20, S.P0_ENERGY: 20, S.P1_ENERGY: 20,
                  S.P0_POWER_FURY: 10, S.P0_POWER_MIND: 10, S.P0_POWER_UNIVERSAL: 10})
    if target is not None:
        state.vector += target.contribution()
        if target.location != "base":
            state.vector[S[f"BF{target.location[-1]}_CONTROLLER"]] = target.controller
        state.validate()
    return state


class CardTransitionExamples(unittest.TestCase):
    def test_draw_and_affine_shape(self):
        state = position()
        original = state.to_vector()
        transition = fixture("Draw 4.", energy=6).on_play(state, CardContext(isolated=True))
        result = transition.apply(state)
        self.assertEqual(transition.matrix.shape, (STATE_SIZE + 1, STATE_SIZE + 1))
        self.assertEqual(result[S.P0_HAND_COUNT], 8)
        self.assertEqual(result[S.P0_DECK_COUNT], 16)
        self.assertEqual(result[S.P0_TRASH_COUNT], 1)
        self.assertEqual(result[S.P0_ENERGY], 14)
        np.testing.assert_array_equal(state.vector, original)

    def test_real_noxus_legion_and_entry(self):
        card = CardConverter().load("OGN-012")
        self.assertEqual(card.power, 0)
        self.assertIn("riftatlas.com/card/OGN-012", card.power_source)
        state = position()
        for enabled, energy in ((False, 16), (True, 18)):
            result = card.on_play(state, CardContext(played_other_card=enabled, isolated=True)).apply(state)
            self.assertEqual(result[S.P0_ENERGY], energy)
            self.assertEqual(result[S.P0_BASE_UNITS], 1)
            self.assertEqual(result[S.P0_BASE_MIGHT], 4)
            self.assertEqual(result[S.P0_BASE_READY_UNITS], 0)

    def test_missing_legion_history_is_not_false(self):
        card = fixture("[Legion] — I cost [2] less.", card_type="Unit", energy=4, might=4)
        with self.assertRaises(TransitionError) as error:
            card.on_play(position(), CardContext(isolated=True))
        self.assertEqual(error.exception.code, "missing_history")

    def test_unverified_null_power_is_not_zero(self):
        card = fixture("[Legion] — I cost [2] less.", card_type="Unit", energy=4, power=None, might=4)
        with self.assertRaises(TransitionError) as error:
            card.on_play(position(), CardContext(played_other_card=True, isolated=True))
        self.assertEqual(error.exception.code, "missing_cost")

    def test_trash_discount_has_zero_floor(self):
        card = fixture("I cost [1] less for each card in your trash.", card_type="Unit", energy=4, might=6)
        state = position()
        state[S.P0_TRASH_COUNT] = 8
        result = card.on_play(state, CardContext(isolated=True)).apply(state)
        self.assertEqual(result[S.P0_ENERGY], 20)
        self.assertEqual(result[S.P0_TRASH_COUNT], 8)
        self.assertEqual(result[S.P0_BASE_MIGHT], 6)

    def test_other_units_condition_excludes_entering_unit(self):
        card = fixture("When you play me, draw 1 if your other units have total Might 5 or more.",
                       card_type="Unit", energy=3, might=3)
        for other_might, expected_hand in ((2, 4), (5, 5)):
            state = position()
            state.update({S.P0_BASE_UNITS: 1, S.P0_BASE_MIGHT: other_might})
            result = card.on_play(state, CardContext(isolated=True)).apply(state)
            self.assertEqual(result[S.P0_HAND_COUNT], expected_hand)
            self.assertEqual(result[S.P0_BASE_MIGHT], other_might + 3)

    def test_nonlethal_damage_does_not_reduce_might(self):
        target = UnitTarget("unit-1", "VANILLA", 1, 1, "battlefield_0", 6, damage=1)
        state = position(target)
        result = fixture("Deal 3 to a unit at a battlefield.").on_play(
            state, CardContext(target=target, isolated=True)).apply(state)
        self.assertEqual(result[S.BF0_P1_DAMAGE], 4)
        self.assertEqual(result[S.BF0_P1_MIGHT], 6)
        self.assertEqual(result[S.BF0_P1_COMBAT_MIGHT], 6)

    def test_lethal_damage_uses_owner_trash_and_releases_control(self):
        target = UnitTarget("unit-1", "VANILLA", 0, 1, "battlefield_0", 3, damage=1)
        state = position(target)
        result = fixture("Deal 3 to a unit.").on_play(state, CardContext(target=target, isolated=True)).apply(state)
        self.assertEqual(result[S.BF0_P1_UNITS], 0)
        self.assertEqual(result[S.BF0_P1_MIGHT], 0)
        self.assertEqual(result[S.BF0_P1_DAMAGE], 0)
        self.assertEqual(result[S.P0_TRASH_COUNT], 2)  # Unit owner plus this spell.
        self.assertEqual(result[S.P1_TRASH_COUNT], 0)
        self.assertEqual(result[S.BF0_CONTROLLER], -1)

    def test_stun_is_not_exhaustion(self):
        target = UnitTarget("unit-1", "VANILLA", 1, 1, "battlefield_0", 5)
        state = position(target)
        result = fixture("Stun a unit.").on_play(state, CardContext(target=target, isolated=True)).apply(state)
        self.assertEqual(result[S.BF0_P1_COMBAT_MIGHT], 0)
        self.assertEqual(result[S.BF0_P1_READY_UNITS], 1)
        self.assertEqual(result[S.BF0_P1_READY_MIGHT], 5)
        self.assertEqual(result[S.BF0_P1_MIGHT], 5)

    def test_ready_does_not_cure_stun(self):
        target = UnitTarget("unit-1", "VANILLA", 0, 0, "battlefield_1", 5, exhausted=True, stunned=True)
        state = position(target)
        result = fixture("Ready a unit.").on_play(state, CardContext(target=target, isolated=True)).apply(state)
        self.assertEqual(result[S.BF1_P0_READY_UNITS], 1)
        self.assertEqual(result[S.BF1_P0_READY_MIGHT], 5)
        self.assertEqual(result[S.BF1_P0_COMBAT_MIGHT], 0)

    def test_buff_respects_negative_effective_might(self):
        target = UnitTarget("unit-1", "VANILLA", 0, 0, "base", -2)
        state = position(target)
        transition = fixture("Give a unit +1 [S] this turn.").on_play(state, CardContext(target=target, isolated=True))
        result = transition.apply(state)
        self.assertEqual(result[S.P0_BASE_MIGHT], 0)
        self.assertEqual(transition.target_after.might, -1)

    def test_buff_and_draw_keep_duration_metadata(self):
        target = UnitTarget("unit-1", "VANILLA", 0, 0, "battlefield_0", 3)
        state = position(target)
        card = fixture("Give a unit +2 [S] this turn. Draw 1.")
        result = card.on_play(state, CardContext(target=target, isolated=True)).apply(state)
        self.assertEqual(result[S.BF0_P0_MIGHT], 5)
        self.assertEqual(result[S.BF0_P0_READY_MIGHT], 5)
        self.assertEqual(result[S.P0_HAND_COUNT], 5)
        self.assertEqual(card.effects[0].duration, "turn")

    def test_on_draw_does_not_play_the_card(self):
        state = position()
        result = fixture("Draw 4.").on_draw(state, CardContext(isolated=True)).apply(state)
        self.assertEqual(result[S.P0_HAND_COUNT], 6)
        self.assertEqual(result[S.P0_DECK_COUNT], 19)
        self.assertEqual(result[S.P0_ENERGY], 20)
        self.assertEqual(result[S.P0_TRASH_COUNT], 0)

    def test_death_and_deathknell(self):
        card = fixture("When I die, draw 1.", card_type="Unit", might=4)
        target = UnitTarget("unit-1", card.card_id, 0, 0, "battlefield_0", 4, exhausted=True)
        state = position(target)
        result = card.on_death(state, CardContext(target=target, isolated=True)).apply(state)
        self.assertEqual(result[S.BF0_P0_UNITS], 0)
        self.assertEqual(result[S.P0_TRASH_COUNT], 1)
        self.assertEqual(result[S.P0_HAND_COUNT], 6)
        self.assertEqual(result[S.P0_ENERGY], 20)

    def test_burn_out_is_explicitly_unsupported(self):
        state = position()
        state[S.P0_DECK_COUNT] = 2
        with self.assertRaises(TransitionError) as error:
            fixture("Draw 4.").on_play(state, CardContext(isolated=True))
        self.assertEqual(error.exception.code, "burn_out")
        self.assertEqual(state[S.P0_HAND_COUNT], 5)

    def test_unknown_suffix_cannot_partially_execute(self):
        card = fixture("Draw 1. Choose an opponent and win the game.")
        state = position()
        with self.assertRaises(TransitionError) as error:
            card.on_play(state, CardContext(isolated=True))
        self.assertEqual(error.exception.code, "unmapped_text")
        self.assertEqual(state[S.P0_HAND_COUNT], 5)

    def test_multiple_target_choices_are_not_merged(self):
        card = fixture("Ready a unit. Kill a unit.")
        self.assertTrue(card.unmapped)

    def test_death_source_and_selected_target_are_not_merged(self):
        card = fixture("When I die, ready a unit.", card_type="Unit", might=4)
        self.assertTrue(card.unmapped)

    def test_token_is_not_a_free_normal_unit(self):
        card = replace(fixture("", card_type="Unit", might=1), labels=("Unit", "Token"), energy=None, power=None)
        with self.assertRaises(TransitionError) as error:
            card.on_play(position(), CardContext(isolated=True))
        self.assertEqual(error.exception.code, "token_lifecycle")

    def test_showdown_does_not_use_neutral_control_cleanup(self):
        target = UnitTarget("unit-1", "VANILLA", 1, 1, "battlefield_0", 3)
        state = position(target)
        state[S.WINDOW] = 1
        card = fixture("[Action] (Play on your turn or in showdowns.) Kill a unit.")
        result = card.on_play(state, CardContext(target=target, isolated=True)).apply(state)
        self.assertEqual(result[S.BF0_P1_UNITS], 0)
        self.assertEqual(result[S.BF0_CONTROLLER], 1)

    def test_hidden_cleanup_requires_actual_card_ownership(self):
        target = UnitTarget("unit-1", "VANILLA", 1, 1, "battlefield_0", 3)
        state = position(target)
        state[S.BF0_P1_HIDDEN_CARDS] = 1
        with self.assertRaises(TransitionError) as error:
            fixture("Kill a unit.").on_play(state, CardContext(target=target, isolated=True))
        self.assertEqual(error.exception.code, "hidden_cleanup")

    def test_matrix_is_bound_to_its_snapshot(self):
        state = position()
        transition = fixture("Draw 1.").on_play(state, CardContext(isolated=True))
        state[S.P0_HAND_COUNT] = 4
        with self.assertRaises(TransitionError) as error:
            transition.apply(state)
        self.assertEqual(error.exception.code, "stale_matrix")

    def test_two_cards_compose_in_execution_order(self):
        state = position()
        card = fixture("Draw 1.")
        first = card.on_play(state, CardContext(isolated=True))
        middle = first.apply(state)
        second = card.on_play(middle, CardContext(isolated=True))
        result = first.then(second).apply(state)
        self.assertEqual(result[S.P0_HAND_COUNT], 5)
        self.assertEqual(result[S.P0_DECK_COUNT], 18)
        self.assertEqual(result[S.P0_TRASH_COUNT], 2)
        self.assertEqual(result[S.P0_ENERGY], 18)

    def test_universal_payment_is_an_explicit_choice(self):
        record = {"display_code": "FIXTURE-002", "full_name": "Payment example", "card_type": "Spell",
                  "energy": 1, "power": 1, "might": None, "domains": ["Fury"], "labels": ["Spell"],
                  "tags": [], "effect_effective": "Draw 1.", "effect_original": "Draw 1.", "source_url": "fixture"}
        card = CardConverter().convert(record, power_cost={"Fury": 1}, power_source="synthetic fixture")
        state = position()
        state[S.P0_POWER_FURY] = 0
        result = card.on_play(state, CardContext(power_payment=(("Universal", 1),), isolated=True)).apply(state)
        self.assertEqual(result[S.P0_POWER_UNIVERSAL], 9)
        self.assertEqual(result[S.P0_POWER_FURY], 0)

    def test_real_multidomain_cost_accepts_either_domain(self):
        card = CardConverter().load("OGN-248")
        self.assertEqual(card.power_cost[0].amount, 3)
        self.assertEqual(set(card.power_cost[0].domains), {"Fury", "Mind"})
        target = UnitTarget("unit-1", "VANILLA", 1, 1, "battlefield_0", 20)
        state = position(target)
        state[S.P0_POWER_FURY] = 0
        state[S.P0_POWER_UNIVERSAL] = 0
        result = card.on_play(state, CardContext(target=target, isolated=True)).apply(state)
        self.assertEqual(result[S.P0_POWER_MIND], 7)
        self.assertEqual(result[S.P0_POWER_FURY], 0)

    def test_multidomain_cost_accepts_mixed_matching_payment(self):
        card = CardConverter().load("OGN-248")
        target = UnitTarget("unit-1", "VANILLA", 1, 1, "battlefield_0", 20)
        state = position(target)
        context = CardContext(target=target, isolated=True, power_payment=(("Fury", 1), ("Mind", 2)))
        result = card.on_play(state, context).apply(state)
        self.assertEqual(result[S.P0_POWER_FURY], 9)
        self.assertEqual(result[S.P0_POWER_MIND], 8)

    def test_multidomain_cost_rejects_unrelated_domain(self):
        card = CardConverter().load("OGN-248")
        target = UnitTarget("unit-1", "VANILLA", 1, 1, "battlefield_0", 20)
        state = position(target)
        state[S.P0_POWER_CHAOS] = 10
        with self.assertRaises(TransitionError) as error:
            card.on_play(state, CardContext(target=target, isolated=True, power_payment=(("Chaos", 3),)))
        self.assertEqual(error.exception.code, "invalid_payment")


if __name__ == "__main__":
    unittest.main(verbosity=2)
