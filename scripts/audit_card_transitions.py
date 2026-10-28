"""Audit every stored printing; scenario success is not full rules certification."""

import argparse
from collections import Counter
from dataclasses import asdict, replace
import json
from pathlib import Path

import numpy as np

from card import CardContext, UnitTarget
from card_converter import CardConverter
from deck_support import DEFAULT_DB, connect, decode_card
from game_state import DOMAINS, STATE_FIELDS, StateEnum as S, game_state
from state_transition import TransitionError


def swap_players(vector):
    result = vector.copy()
    for index in STATE_FIELDS:
        name = index.name.replace("P0", "TEMP").replace("P1", "P0").replace("TEMP", "P1")
        result[S[name]] = vector[index]
    for index in (S.TURN_PLAYER, S.BF0_CONTROLLER, S.BF1_CONTROLLER):
        result[index] = -1 if vector[index] == -1 else 1 - vector[index]
    return result


def card_mass(state):
    names = ("HAND_COUNT", "DECK_COUNT", "TRASH_COUNT", "CHAMPION_ZONE_COUNT", "BASE_UNITS", "GEAR_COUNT")
    return sum(state[S[f"P{p}_{name}"]] for p in (0, 1) for name in names) + sum(
        state[S[f"BF{b}_P{p}_UNITS"]] for b in (0, 1) for p in (0, 1))


def scenario(target=None, *, other_might=5):
    state = game_state()
    state.update({S.PHASE: 6, S.P0_HAND_COUNT: 8, S.P1_HAND_COUNT: 8,
                  S.P0_DECK_COUNT: 30, S.P1_DECK_COUNT: 30,
                  S.P0_TRASH_COUNT: 6, S.P1_TRASH_COUNT: 6,
                  S.P0_ENERGY: 50, S.P1_ENERGY: 50,
                  S.P0_BASE_UNITS: 1, S.P0_BASE_MIGHT: other_might})
    for player in (0, 1):
        for domain in DOMAINS:
            state.vector[S[f"P{player}_POWER_{domain.upper()}"]] = 10
    if target is not None:
        state.vector += target.contribution()
        if target.location != "base":
            state.vector[S[f"BF{target.location[-1]}_CONTROLLER"]] = target.controller
    state.validate()
    return state


def check_case(card, event, state, context):
    before = state.to_vector()
    transition = getattr(card, f"on_{event}")(state, context)
    result = transition.apply(state)
    if card_mass(result) != card_mass(state):
        raise AssertionError("An isolated supported event did not conserve physical card count")
    np.testing.assert_array_equal(before, state.vector, err_msg="Input state was mutated")
    target = context.target
    swapped_target = None if target is None else replace(target, owner=1 - target.owner, controller=1 - target.controller)
    swapped = game_state(swap_players(state.vector))
    swapped_context = replace(context, player=1, target=swapped_target)
    other_result = getattr(card, f"on_{event}")(swapped, swapped_context).apply(swapped)
    np.testing.assert_array_equal(other_result.vector, swap_players(result.vector), err_msg="Player symmetry failed")
    return transition.changes()


def audit_record(record, converter):
    card = converter.convert(record)
    reasons = []
    if card.card_type not in ("Unit", "Spell", "Gear"):
        reasons.append("unsupported_type")
    if card.unmapped:
        reasons.append("unmapped_text")
    if "Token" in card.labels or card.card_type == "Token":
        reasons.append("token_lifecycle")
    elif card.card_type in ("Unit", "Spell", "Gear"):
        if card.energy is None:
            reasons.append("missing_energy")
        if card.power is None:
            reasons.append("missing_power_total")
        if card.power_cost is None:
            reasons.append("missing_power_glyphs")
        if card.card_type == "Unit" and card.might is None:
            reasons.append("missing_might")
    entry = {"source_code": record["source_code"], "card_id": card.card_id, "name": card.name,
             "type": card.card_type, "text": card.text, "source_url": card.source_url,
             "effects": [asdict(effect) for effect in card.effects], "unmapped": card.unmapped,
             "reasons": reasons, "isolated_play_verified": False, "scenario_checks": 0,
             "payment_data_verified": card.power_cost is not None and card.energy is not None,
             "power_requirements": None if card.power_cost is None else [asdict(r) for r in card.power_cost],
             "power_source": card.power_source}
    if any(reason in reasons for reason in ("unsupported_type", "unmapped_text", "token_lifecycle")):
        # Verify rejection as well: unsupported cards must never return a partial matrix.
        try:
            card.on_play(scenario(), CardContext(played_other_card=True, isolated=True))
        except TransitionError as error:
            entry["rejection_code"] = error.code
        else:
            raise AssertionError("An unsupported card returned a transition")
        entry["status"] = "unsupported"
        return entry
    if any(reason in reasons for reason in ("missing_energy", "missing_might", "missing_power_total", "missing_power_glyphs")):
        entry["status"] = "missing_data"
        return entry
    targeted = [e for e in card.effects if e.event == "play" and e.operation in ("damage", "buff", "ready", "stun", "kill")]
    targets = [None]
    if targeted:
        effect = targeted[0]
        player = 0 if effect.operation in ("buff", "ready") else 1
        targets = [UnitTarget(f"target-{i}", "AUDIT-VANILLA", player, player, location, might,
                              damage=damage, exhausted=exhausted, stunned=stunned)
                   for i, (location, might, damage, exhausted, stunned) in enumerate((
                       ("battlefield_0", 20, 1, False, False),
                       ("battlefield_1", 2, 0, True, False),
                       ("battlefield_0", 6, 0, True, True),
                       ("base", -2, 0, False, False),
                   )) if not effect.battlefield_only or location != "base"]
    for target in targets:
        for enabled, other_might in ((False, 2), (True, 6)):
            context = CardContext(target=target, played_other_card=enabled, isolated=True)
            changes = check_case(card, "play", scenario(target, other_might=other_might), context)
            entry["scenario_checks"] += 2  # Includes the player-swapped case.
            entry.setdefault("example_changes", changes)
    check_case(card, "draw", scenario(), CardContext(isolated=True))
    entry["scenario_checks"] += 2
    if card.card_type == "Unit":
        target = UnitTarget("dying-source", card.card_id, 0, 0, "battlefield_0", card.might, exhausted=True)
        check_case(card, "death", scenario(target), CardContext(target=target, isolated=True))
        entry["scenario_checks"] += 2
    entry["status"] = "isolated_scenarios_passed"
    entry["isolated_play_verified"] = True
    return entry


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--db", type=Path, default=DEFAULT_DB)
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "reports" / "card-transition-audit.json")
    args = parser.parse_args()
    converter, entries = CardConverter(), []
    connection = connect(args.db)
    try:
        records = [decode_card(row) for row in connection.execute("SELECT * FROM cards ORDER BY source_code")]
    finally:
        connection.close()
    for record in records:
        try:
            entries.append(audit_record(record, converter))
        except Exception as error:
            entries.append({"source_code": record["source_code"], "card_id": record["display_code"],
                            "name": record["full_name"], "status": "implementation_failure",
                            "error_type": type(error).__name__, "error": str(error), "isolated_play_verified": False})
    statuses = Counter(entry["status"] for entry in entries)
    reasons = Counter(reason for entry in entries for reason in entry.get("reasons", ()))
    summary = {"records": len(entries), "distinct_card_ids": len({e["card_id"] for e in entries}),
               "distinct_card_names": len({e["name"] for e in entries}),
               "statuses": dict(statuses), "reason_counts": dict(reasons),
               "payment_data_verified": sum(e.get("payment_data_verified", False) for e in entries),
               "isolated_play_verified": sum(e["isolated_play_verified"] for e in entries), "full_game_verified": 0,
               "scenario_checks": sum(e.get("scenario_checks", 0) for e in entries), "all_cards_verified": False}
    report = {"scope": "All stored printings; real stored cost data and isolated scenarios, not full-game correctness",
              "limitations": ["Base Power data comes from the archived RiftAtlas catalog and documented domain rules",
                              "No external triggers, replacement effects, turn-end expiration or hidden-information policy",
                              "Conservation and symmetry are necessary checks, not a complete semantic oracle"],
              "summary": summary, "cards": entries}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = ["# 全牌库状态转移验收", "", "本报告覆盖全部印刷记录，使用本地已溯源的实际基础费用，不再使用测试费用假设；场景通过不代表完整对局规则已实现。", "",
             "```json", json.dumps(summary, ensure_ascii=False, indent=2), "```", "",
             "## 原因说明", "",
             "- unmapped_text：完整文本包含未支持的条件、关键词、目标、选择、区域或持续效果，整张卡拒绝生成部分矩阵。",
             "- unsupported_type：传奇、战场、符文等没有普通手牌出牌的生命周期模型。",
             "- token_lifecycle：衍生物需由效果创建／移除，不能按普通卡牌抽取、支付或进入墓地处理。",
             "- missing_power_total / missing_power_glyphs：费用总量或支付符号未认证；不把空值当零，也不按颜色猜符号。",
             "- missing_energy / missing_might：普通可打出牌缺少必要属性。",
             "- isolated_scenarios_passed：使用实际已溯源费用通过孤立场景，完整对局互动仍未实现。",
             "- implementation_failure：场景执行出现意外异常或违反验收性质；原因数量可能重叠。", "",
             "## 每张牌的状态", "", "| 卡牌 ID | 名称 | 状态 | 原因 |", "| --- | --- | --- | --- |"]
    for entry in entries:
        reason = "; ".join(entry.get("reasons", ())) or entry.get("error", "")
        lines.append(f"| {entry['card_id']} | {entry['name'].replace('|', '/')} | {entry['status']} | {reason.replace('|', '/')} |")
    args.output.with_suffix(".md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=True, indent=2))
    print("Report:", args.output)
    return 2 if statuses["implementation_failure"] else 1  # Nonzero: full-library verification remains incomplete.


if __name__ == "__main__":
    raise SystemExit(main())
