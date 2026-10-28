"""Query local costs, body, original text and symbolic primitive programs by card ID."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data/card-models/cards.json"


class CardCatalog:
    def __init__(self, path: str | Path = DEFAULT_DATA):
        self.path = Path(path)
        if not self.path.is_file():
            raise FileNotFoundError("缺少模型JSON；请先运行 python scripts/build_card_models.py")
        self.data = json.loads(self.path.read_text(encoding="utf-8"))
        if self.data.get("schema_version") != "1.0":
            raise ValueError("不支持的卡牌模型版本")

    def get(self, reference: str) -> dict:
        key = str(reference).strip().casefold()
        ids = self.data["lookup_index"].get(key, [])
        if not ids:
            raise ValueError(f"找不到卡牌编号：{reference}")
        if len(ids) != 1:
            choices = [f'{v}: {self.data["cards"][v]["name"]}' for v in ids]
            raise ValueError("编号或名称不唯一，请使用UUID：" + "; ".join(choices))
        return self.data["cards"][ids[0]]


def lookup_card(reference: str, data_path: str | Path = DEFAULT_DATA) -> dict:
    """Return a JSON-serializable record; unknown facts remain null/unknown."""
    return CardCatalog(data_path).get(reference)


def format_card(card: dict, *, language="SC", show_all_texts=False) -> str:
    names = card["names"].get(language) or [card["name"]]
    lines = [f'{" / ".join(names)} ({card["name"]})',
             "编号：" + ", ".join(v for v in card["codes"] if "/" not in v),
             f'阅读序号：{card["reading_number"]:04d}',
             "类型：" + " / ".join(card["base"]["types"])]
    def show_cost(part):
        if part["status"] == "not_applicable":
            return "不适用"
        return str(part["value"]) if part["status"] == "known" else "未知"
    lines.append(f'基础费用：能量 {show_cost(card["cost"]["energy"])}；符能 {show_cost(card["cost"]["power"])}')
    requirements = card["cost"]["power"]["requirements"]
    if requirements:
        lines.append("符能支付：" + "; ".join(f'{v["amount"]}，可从 {" / ".join(v["allowed_domains"])} 混合支付' for v in requirements))
    body = card["body"]
    lines.append(f'身材：战力 {body["might"] if body["might"] is not None else "不适用／未提供"}；装备战力加成 {body["might_bonus"] if body["might_bonus"] is not None else "不适用／未提供"}')
    review = card["review"]
    lines.append("效果状态：" + review["current_expression_status"] + "（符号流程，未认证执行正确性）")
    if card["effect_model"]["ruling_adjustments"]:
        lines.append("本次规则核验：" + card["effect_model"]["ruling_adjustments"])
    if review["current_expression_status"] == "verify":
        lines.append("待核项：" + "; ".join(review["historical_issues"]))
    lines.extend(["", "效果原文："])
    texts = card["texts"]
    if not show_all_texts:
        preferred = [v for v in texts if v["language"] == language]
        texts = preferred or [v for v in texts if v["language"] == "EN"] or texts
    for i, text in enumerate(texts, 1):
        lines.extend([f'[{text["language"]} 文本组{i}]', text["rules_text"] if text["rules_text"] is not None else "规则文字：未提供"])
        if text["effect_text"] is not None:
            lines.append("装备效果：" + text["effect_text"])
    if card["errata"]:
        lines.extend(["目录勘误：", json.dumps(card["errata"], ensure_ascii=False, indent=2)])
    model = card["effect_model"]
    lines.extend(["", "入口：" + model["entry_description"], "参数绑定：" + model["bindings_declaration"]])
    if model["rule_bindings"]:
        lines.extend(["结构化费用规则：", json.dumps(model["rule_bindings"], ensure_ascii=False, indent=2)])
    lines.append("效果流程（独立片段按各自入口执行）：")
    for ability in model["abilities"]:
        lines.extend(["", "入口／阶段：" + ability["entry"]["declaration"], ability["program_source"]])
    return "\n".join(lines)


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reference", nargs="?", help="如 OGN-006、0338、UUID或精确中英文名称")
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--json", action="store_true", help="返回完整逐卡JSON，含阶段索引和结构化程序")
    parser.add_argument("--language", choices=["SC", "EN", "TC"], default="SC")
    parser.add_argument("--all-texts", action="store_true", help="展示全部语言及文本版本")
    args = parser.parse_args()
    try:
        catalog = CardCatalog(args.data)
        def show(reference):
            card = catalog.get(reference)
            print(json.dumps(card, ensure_ascii=False, indent=2) if args.json else format_card(
                card, language=args.language, show_all_texts=args.all_texts))
        if args.reference is not None:
            show(args.reference)
        else:
            while True:
                try:
                    reference = input("卡牌编号（q退出）：").strip()
                except EOFError:
                    break
                if reference.casefold() in {"q", "quit", "exit"}:
                    break
                if reference:
                    try:
                        show(reference)
                    except ValueError as exc:
                        print(str(exc), file=sys.stderr)
    except (OSError, ValueError) as exc:
        print(str(exc), file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
