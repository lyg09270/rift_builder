"""Build a local, symbolic card-effect catalog from the complete reading notes.

No effect execution, eval, database migration, or network access is performed.
"""
from __future__ import annotations

import argparse
import ast
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import re
import unicodedata

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_OUTPUT = ROOT / "data/card-models/cards.json"
CATALOG = ROOT / "data/sources/openrift/catalog.json"
API = ROOT / "docs/basic-primitives-v4-p1.md"
NOTES = ROOT / "docs/card-primitives-reading-p1"
MODIFIERS = {
    "might_contribute", "trait_change", "ability_add", "ability_mask",
    "ability_patch", "control_contribute", "copy_view", "cost_rule_add",
    "damage_rule_add", "output_rule_add", "entry_rule_add",
    "instruction_rule_add", "permission_rule_add", "rule_value_add",
}
FLOORS = {38: -1, 75: None, 273: -1, 419: -2, 916: -2, 1038: -1}
RULINGS = {
    66: ("resolved", "实际kill回执无死亡对象时阈值为null，不允许后续选单位；仍查看并回收。"),
    172: ("resolved_by_rule_derivation", "折扣绑定已声明额外费用，不以后续真实死亡数反算资源；替代仍可视为已付。"),
    201: ("pending", "同实体链上重打的历史与Bonus精确生效窗口尚未确认。"),
    286: ("pending", "两种英文文本的全场景等价性及规范版本尚未确认。"),
    338: ("pending", "触发基础费用阶段已确认，后续play费用政策尚未确认。"),
    453: ("pending", "自身被法术杀死可触发；后续play费用政策尚未确认。"),
    541: ("resolved_by_rule_derivation", "其余=查看集合减所选牌；不按实际抽到的牌求补集，不补搬新的顶牌。"),
    640: ("pending", "旧revealed措辞对应的规范动作和范围尚未确认。"),
}


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_reviews() -> dict[int, dict]:
    """Read the persistent per-card notes, rather than depending on tmp ledgers."""
    result = {}
    for path in sorted(NOTES.glob("[0-9]*.md")):
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r'<a id="card-(\d+)"></a>(.*?)(?=<a id="card-|\Z)', text, re.S):
            number, block = int(match[1]), match[2]
            if number in result:
                raise ValueError(f"Duplicate reading number: {number}")
            def line(prefix):
                found = re.search(r"^- " + re.escape(prefix) + r"([^\n]*)$", block, re.M)
                if not found:
                    raise ValueError(f"Missing {prefix} on card {number}")
                return found[1].strip()
            title = re.search(r"^## \d+ (.+)$", block, re.M)
            sections = [{"entry": m[1], "program": m[2]} for m in re.finditer(
                r"\*\*入口／片段：(.*?)\*\*\s*```python\n(.*?)\n```", block, re.S)]
            if not title:
                raise ValueError(f"Missing title/program on card {number}")
            result[number] = {
                "name": title[1], "status": line("判定：").strip("*。"),
                "review": line("本轮独立复读："), "window": line("入口、条件和角色："),
                "bindings": line("参数绑定："), "native": line("固有关键词核对："),
                "issues": re.findall(r"^- 保留问题：(.+)$", block, re.M),
                "sections": sections, "path": path.relative_to(ROOT).as_posix(),
            }
    return result


def signatures() -> dict[str, ast.arguments]:
    result = {}
    for match in re.finditer(r"### `(\w+)`[^\n]*\n\n```python\n(.*?)\n```", API.read_text(encoding="utf-8"), re.S):
        function = ast.parse("def " + match[2] + ":\n    pass").body[0]
        result[match[1]] = function.args
    if len(result) != 35:
        raise ValueError(f"Expected 35 primitive signatures, got {len(result)}")
    return result


class ProgramEncoder:
    """Serialize syntax as data. Expressions stay symbolic; never evaluate them."""
    def __init__(self, specs, prefix):
        self.specs, self.prefix = specs, prefix
        self.calls, self.modifiers = [], []

    def expression(self, node, phase):
        if node is None:
            return None
        if isinstance(node, ast.Constant):
            return {"expr": "literal", "value": node.value}
        if isinstance(node, ast.Name):
            return {"expr": "symbol", "name": node.id}
        if isinstance(node, ast.Attribute):
            return {"expr": "attribute", "object": self.expression(node.value, phase), "name": node.attr}
        if isinstance(node, ast.Call):
            name = ast.unparse(node.func)
            args = [self.expression(v, phase) for v in node.args]
            kwargs = {v.arg: self.expression(v.value, phase) for v in node.keywords}
            if any(v.arg is None for v in node.keywords):
                raise ValueError("Unbounded keyword expansion is not permitted")
            if name.startswith("p."):
                op = name[2:]
                if op not in self.specs:
                    raise ValueError(f"Unknown primitive: {name}")
                sig = self.specs[op]
                positional = sig.posonlyargs + sig.args
                required = {v.arg for v in positional[:len(positional)-len(sig.defaults)]}
                required |= {a.arg for a, default in zip(sig.kwonlyargs, sig.kw_defaults) if default is None}
                supplied = {v.arg for v in positional[:len(node.args)]} | set(kwargs)
                valid = {v.arg for v in positional + sig.kwonlyargs}
                if (len(node.args) > len(positional) or not required <= supplied
                        or not set(kwargs) <= valid
                        or set(kwargs) & {v.arg for v in positional[:len(node.args)]}):
                    raise ValueError(f"Invalid signature: {ast.unparse(node)}")
                call = {"node": "Call", "id": f"{self.prefix}:call-{len(self.calls)+1}",
                        "op": op, "args": args, "kwargs": kwargs, "phase": phase,
                        "source": ast.unparse(node)}
                self.calls.append(call)
                if op in MODIFIERS:
                    self.modifiers.append(call["id"])
                return call
            return {"expr": "invoke", "function": name, "args": args, "kwargs": kwargs,
                    "domain": "flow" if name.startswith("flow.") else "symbolic_protocol"}
        if isinstance(node, (ast.List, ast.Tuple, ast.Set)):
            return {"expr": type(node).__name__.lower(), "items": [self.expression(v, phase) for v in node.elts]}
        if isinstance(node, ast.Dict):
            return {"expr": "map", "items": [{"key": self.expression(k, phase), "value": self.expression(v, phase)}
                                              for k, v in zip(node.keys, node.values)]}
        if isinstance(node, (ast.operator, ast.unaryop, ast.boolop, ast.cmpop, ast.expr_context)):
            return type(node).__name__
        # Type-preserving syntax data for comparisons, conditions, comprehensions,
        # subscripts and arithmetic. A future interpreter must whitelist it again.
        if isinstance(node, ast.AST):
            return {"expr": type(node).__name__, **{
                key: ([self.expression(v, phase) for v in value] if isinstance(value, list)
                      else self.expression(value, phase) if isinstance(value, ast.AST) else value)
                for key, value in ast.iter_fields(node)}}
        raise ValueError(f"Unserializable expression: {type(node).__name__}")

    def sequence(self, statements, phase="entry_execution"):
        return {"node": "Sequence", "steps": [self.statement(v, phase) for v in statements]}

    def statement(self, node, phase):
        if isinstance(node, ast.Expr):
            return self.expression(node.value, phase)
        if isinstance(node, ast.Assign):
            return {"node": "Bind", "targets": [self.expression(v, phase) for v in node.targets],
                    "value": self.expression(node.value, phase), "scope": "local", "phase": phase}
        if isinstance(node, ast.AugAssign):
            return {"node": "UpdateBinding", "target": self.expression(node.target, phase),
                    "operation": type(node.op).__name__, "value": self.expression(node.value, phase), "phase": phase}
        if isinstance(node, ast.If):
            return {"node": "If", "condition": self.expression(node.test, phase),
                    "then": self.sequence(node.body, phase), "else": self.sequence(node.orelse, phase)}
        if isinstance(node, ast.For):
            return {"node": "ForEach", "binding": self.expression(node.target, phase),
                    "objects": self.expression(node.iter, phase), "body": self.sequence(node.body, phase),
                    "else": self.sequence(node.orelse, phase)}
        if isinstance(node, ast.With) and len(node.items) == 1:
            context = node.items[0]
            call = context.context_expr
            if not isinstance(call, ast.Call):
                raise ValueError("Unknown context manager")
            name = ast.unparse(call.func)
            if name == "phase":
                stage = ast.literal_eval(call.args[0])
                return {"node": "Phase", "name": stage, "body": self.sequence(node.body, stage)}
            if name == "action_frame":
                template = ast.literal_eval(call.args[0])
                return {"node": "ActionFrame", "template": template,
                        "arguments": self.expression(call.args[1], phase),
                        "binding": self.expression(context.optional_vars, phase),
                        "body": self.sequence(node.body, phase)}
            if name in {"flow.Batch", "flow.Repeat"}:
                return {"node": name.split(".")[1], "arguments": self.expression(call, phase),
                        "body": self.sequence(node.body, phase)}
            raise ValueError(f"Unknown context protocol: {name}")
        raise ValueError(f"Unmapped program statement: {type(node).__name__}")


def normalize_name(value):
    return re.sub(r"[^\w]", "", unicodedata.normalize("NFKC", value).casefold())


def cost_data(card, printings, atlas, zero_proven):
    applicable = bool(set(card["types"]) & {"unit", "spell", "gear"}) and "token" not in card["superTypes"]
    energy, power = card["energy"], card["power"]
    source = "data/sources/openrift/catalog.json"
    power_source = source if power is not None else None
    evidence = []
    if applicable and power is None:
        for code in {v["shortCode"] for _, v in printings}:
            other = atlas.get(code)
            if (other and normalize_name(other["name"]) == normalize_name(card["name"])
                    and other.get("energyCost") == energy
                    and {v.casefold() for v in other.get("domains", [])} == set(card["domains"])
                    and other.get("type", "").casefold() in card["types"]):
                value = other.get("powerCost")
                if value is None and zero_proven:
                    value = 0
                if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
                    evidence.append({"code": code, "value": value, "absent_means_zero_verified": "powerCost" not in other})
        if evidence and len({v["value"] for v in evidence}) == 1:
            power = evidence[0]["value"]
            power_source = "data/sources/riftatlas/catalog.json"
    def status(value):
        return "not_applicable" if not applicable else "known" if value is not None else "unknown"
    domains = [d for d in card["domains"] if d != "colorless"]
    return {
        "energy": {"value": energy, "status": status(energy), "source": source},
        "power": {"value": power, "status": status(power), "source": power_source,
                  "requirements": None if power is None else [] if power == 0 else [
                      {"amount": power, "allowed_domains": domains or ["fury", "calm", "mind", "body", "chaos", "order"],
                       "payment": "any_mix_within_group"}], "evidence": evidence},
        "scope": "printed_base_only; additional/alternate costs remain in the effect model",
    }


def current_sections(number, review):
    sections = [dict(v) for v in review["sections"]]
    if number == 66:
        for part in sections:
            if "action_frame('kill'" in part["program"]:
                part["program"] = part["program"].replace("if take:", "if f1.result.value and take:")
    if number == 541:
        for part in sections:
            part["program"] = part["program"].replace(
                "with action_frame('burn', {'positional': (player, len(rest)), 'keywords': {'cards': rest}}) as f3:",
                "with action_frame('transfer', {'positional': (rest, player.main_deck, player.trash), 'keywords': {}}) as f3:")
    return sections


def rule_bindings(number):
    if number not in FLOORS:
        return {}
    delta = FLOORS[number]
    if delta is None:
        delta = {"expr": "negative_history_count", "event": "PLAY", "stage": "finalized",
                 "actor": "controller", "period": "current_turn", "exclude": "current_item"}
    fields = {"energy_delta": delta, "energy_floor": 1}
    if number in {38, 1038}:
        fields["power_discount"] = {"amount": 1, "allowed_domains": "any"}
    return {"discount" if number == 1038 else "change": {"type": "CostRule", "fields": fields}}


def build(output: Path = DEFAULT_OUTPUT):
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))
    reviews, specs = read_reviews(), signatures()
    ordered = sorted(catalog["cards"].items(), key=lambda v: (v[1]["name"].casefold(), v[0]))
    if set(reviews) != set(range(1, len(ordered)+1)):
        raise ValueError("Reading notes do not cover every canonical card")
    by_card = defaultdict(list)
    def add_face(printing_id, face, side="front"):
        if face["cardId"] not in catalog["cards"]:
            raise ValueError(f"Unknown cardId in printing {printing_id}")
        by_card[face["cardId"]].append((printing_id + ":" + side, face))
        if isinstance(face.get("side2"), dict):
            add_face(printing_id, face["side2"], side + ".side2")
    for key, value in catalog["printings"].items():
        add_face(key, value)
    atlas_path = ROOT / "data/sources/riftatlas/catalog.json"
    atlas = {v["id"]: v for v in json.loads(atlas_path.read_text(encoding="utf-8"))}
    renderer = ROOT / "data/sources/riftatlas/cost-renderer.js"
    zero_proven = bool(re.search(r'"number"==typeof (\w+)\.powerCost\?Math\.max\(0,Math\.trunc\(\1\.powerCost\)\):0',
                                 renderer.read_text(encoding="utf-8")))
    cards, index = {}, defaultdict(set)
    calls = Counter()
    for number, (card_id, base) in enumerate(ordered, 1):
        review, printing_records = reviews[number], by_card[card_id]
        if review["name"] != base["name"]:
            raise ValueError(f"Reading/source identity mismatch: {number}")
        texts = {}
        names = defaultdict(set)
        codes = set()
        for printing_id, printing in printing_records:
            codes.update(v for v in (printing.get("shortCode"), printing.get("publicCode")) if v)
            names[printing["language"]].add(printing["printedName"])
            key = (printing["language"], printing.get("printedRulesText"), printing.get("printedEffectText"))
            group = texts.setdefault(key, {"language": key[0], "rules_text": key[1], "effect_text": key[2],
                                           "printing_ids": [], "codes": []})
            group["printing_ids"].append(printing_id)
            if printing["shortCode"] not in group["codes"]:
                group["codes"].append(printing["shortCode"])
        abilities, phases, modifiers = [], defaultdict(list), []
        for i, section in enumerate(current_sections(number, review), 1):
            ability_id = f"{card_id}:fragment-{i}"
            encoder = ProgramEncoder(specs, ability_id)
            tree = ast.parse(section["program"])
            program = encoder.sequence(tree.body)
            for call in encoder.calls:
                phases[call["phase"]].append({"ability_id": ability_id, "call_id": call["id"], "op": call["op"]})
                calls[call["op"]] += 1
            modifiers.extend(encoder.modifiers)
            abilities.append({"id": ability_id, "entry": {"declaration": section["entry"],
                              "binding": "reviewed_symbolic_entry", "machine_activation_spec_complete": False},
                              "program": program, "program_source": section["program"],
                              "primitive_calls": encoder.calls})
        ruling = RULINGS.get(number)
        current = ("verify" if ruling and ruling[0] == "pending" else "expression_reviewed"
                   if ruling or number in FLOORS or review["status"] == "covered" else review["status"])
        model = {"schema_version": "1.0", "card_id": card_id, "reading_number": number,
                 "codes": sorted(codes), "name": base["name"],
                 "names": {k: sorted(v) for k, v in names.items()}, "base": base,
                 "cost": cost_data(base, printing_records, atlas, zero_proven),
                 "body": {"might": base["might"], "might_bonus": base["mightBonus"],
                          "health": None, "health_status": "not_a_separate_card_stat"},
                 "texts": list(texts.values()), "errata": base.get("errata"),
                 "effect_model": {"api_version": "V4-P1.1", "entry_description": review["window"],
                                  "bindings_declaration": review["bindings"], "rule_bindings": rule_bindings(number),
                                  "native_keywords_declaration": review["native"], "abilities": abilities,
                                  "phase_calls": dict(phases), "modifier_call_ids": modifiers,
                                  "phase_policy": "Nested Phase bodies run only when the scheduler reaches that phase; independent fragments are not a serial script.",
                                  "ruling_adjustments": ruling[1] if ruling else None},
                 "review": {"frozen_p1_status": review["status"], "current_expression_status": current,
                            "notes": review["review"], "historical_issues": review["issues"],
                            "ruling_status": ruling[0] if ruling else None,
                            "execution_certified": False,
                            "symbolic_bindings_require_runtime_context": True,
                            "source": review["path"] + f"#card-{number:04d}",
                            "rulings_source": "docs/card-primitives-rulings-p1.1.md" if ruling else None}}
        if number == 541:
            model["effect_model"]["bindings_declaration"] += "; P1.1修正：rest=本次查看集合减所选c；按选择绑定，不按实际抽取收据计算"
        if number == 66:
            model["effect_model"]["bindings_declaration"] += "; P1.1修正：v的阈值仅在本次kill回执有实际死亡单位时取该单位LKI，否则null"
        if number == 172:
            model["effect_model"]["bindings_declaration"] += "; P1.1修正：package折扣数量来自已声明的额外费用对象，不按事后实际死亡数回算"
        cards[card_id] = model
        # Exact aliases only: no suffix stripping, fuzzy name matching or guessed IDs.
        for alias in codes | {card_id, str(number), f"{number:04d}", base["name"]} | set().union(*names.values()):
            index[alias.casefold()].add(card_id)
    input_paths = [CATALOG, API, ROOT / "docs/card-model.md", ROOT / "docs/card-resolution-v4.md",
                   ROOT / "docs/card-primitives-rulings-p1.1.md", atlas_path, renderer,
                   ROOT / "docs/references/card-effect-models/ssrn-6566539.pdf"] + sorted(NOTES.glob("[0-9]*.md"))
    result = {
        "schema_version": "1.0", "api_version": "V4-P1.1", "kind": "symbolic_card_effect_catalog",
        "inputs": {p.relative_to(ROOT).as_posix(): digest(p) for p in input_paths},
        "pipeline": ["match_entry", "check_conditions_and_limits", "enqueue_or_register", "choose",
                     "calculate_cost", "pay", "check_legality", "dispatch", "execute_program",
                     "commit_actual_results", "publish_events", "schedule_pending_and_cleanup"],
        "boundaries": {"executes_effects": False, "semantic_execution_accuracy": None,
                       "entry_declarations_fully_machine_bound": False,
                       "symbolic_expressions_are_data_not_python_to_execute": True},
        "summary": {"canonical_cards": len(cards), "printings": len(catalog["printings"]),
                    "text_groups": sum(len(v["texts"]) for v in cards.values()),
                    "primitive_count": len(specs), "primitive_call_sites": sum(calls.values()),
                    "signature_checked_call_sites": sum(calls.values()), "primitive_usage": dict(sorted(calls.items())),
                    "expression_status_counts": dict(Counter(v["review"]["current_expression_status"] for v in cards.values())),
                    "power_status_counts": dict(Counter(v["cost"]["power"]["status"] for v in cards.values()))},
        "cards": cards, "lookup_index": {key: sorted(value) for key, value in sorted(index.items())},
    }
    output = output.resolve()
    if output == CATALOG.resolve() or any(part in {"sources", ".data_versions", "revisions"} for part in output.parts):
        raise ValueError("Output must not overwrite source data or managed snapshots")
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".tmp")
    temporary.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    temporary.replace(output)
    return result["summary"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    print(json.dumps(build(args.output), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
