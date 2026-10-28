"""Download the selected original papers and record auditable PDF metadata.

Run with Python 3 and pypdf installed. Existing PDFs are verified, not replaced.
"""

from __future__ import annotations

import concurrent.futures
import datetime as dt
import hashlib
import io
import json
from pathlib import Path
import urllib.request

from pypdf import PdfReader


ROOT = Path(__file__).resolve().parent
PAPERS = [
    {
        "id": "resource-scale-2019",
        "title": "Learning a Resource Scale for Collectible Card Games",
        "authors": ["Gianlucca Zuin", "Adriano Veloso"],
        "year": 2019, "venue": "IEEE Conference on Games (CoG)",
        "doi": "10.1109/CIG.2019.8847946",
        "filename": "2019-learning-a-resource-scale.pdf",
        "sources": [("https://ieee-cog.org/2019/papers/paper_119.pdf", "conference PDF")],
        "topic": "学习属性、效果文本与资源费用之间的关系；建立身材和效果的费用参照。",
        "limitation": "预测印刷费用，不直接预测入选价值或获胜贡献。",
        "priority": "核心，建议第一个阅读",
    },
    {
        "id": "evaluation-functions-2022",
        "title": "Evolving Evaluation Functions for Collectible Card Game AI",
        "authors": ["Radoslaw Miernik", "Jakub Kowalski"],
        "year": 2022, "venue": "ICAART 2022; arXiv preprint 2021",
        "doi": "10.5220/0010806900003116",
        "filename": "2022-evolving-evaluation-functions.pdf",
        "sources": [
            ("https://www.scitepress.org/Papers/2022/108069/108069.pdf", "published conference PDF"),
            ("https://arxiv.org/pdf/2105.01115", "arXiv preprint 2021, not the publisher version"),
        ],
        "topic": "单卡与场面特征评分；线性和树状表示；评分参数的对局验证。",
        "limitation": "LOCM 的规则与特征不同，不能直接移植评分权重。",
        "priority": "核心，建议第二个阅读",
    },
    {
        "id": "q-deckrec-2018",
        "title": "Q-DeckRec: A Fast Deck Recommendation System for Collectible Card Games",
        "authors": ["Zhengxing Chen", "Christopher Amato", "Truong-Huy D. Nguyen", "Seth Cooper", "Yizhou Sun", "Magy Seif El-Nasr"],
        "year": 2018, "venue": "IEEE CIG 2018; arXiv:1806.09771",
        "filename": "2018-q-deckrec.pdf",
        "sources": [("https://arxiv.org/pdf/1806.09771", "author preprint on arXiv")],
        "topic": "把构筑视为依赖当前套牌与对手的连续修改和搜索问题。",
        "limitation": "训练与评价依赖模拟器及代理打法；不提供跨游戏通用单卡分。",
        "priority": "核心，建议第三个阅读",
    },
    {
        "id": "chaos-cards-2020",
        "title": "Chaos Cards: Creating Novel Digital Card Games through Grammatical Content Generation and Meta-Based Card Evaluation",
        "authors": ["Tiannan Chen", "Stephen J. Guy"],
        "year": 2020, "venue": "AAAI AIIDE 2020",
        "doi": "10.1609/aiide.v16i1.7430",
        "filename": "2020-chaos-cards-meta-based-evaluation.pdf",
        "sources": [("https://cdn.aaai.org/ojs/7430/7430-52-10748-1-2-20200923.pdf", "published conference PDF")],
        "topic": "可执行卡牌效果、竞争套牌环境中的模拟评分，以及快速预测。",
        "limitation": "研究使用作者自己的 Hearthstone 类游戏，需要可靠的游戏实现。",
        "priority": "核心，后续强度验证参考",
    },
    {
        "id": "hearthstone-meta-2019",
        "title": "Evolving the Hearthstone Meta",
        "year": 2019, "venue": "IEEE CoG 2019; arXiv:1907.01623",
        "filename": "2019-evolving-the-hearthstone-meta.pdf",
        "sources": [
            ("https://ieee-cog.org/2019/papers/paper_134.pdf", "conference PDF"),
            ("https://arxiv.org/pdf/1907.01623", "author preprint on arXiv"),
        ],
        "topic": "打出胜率、抽到胜率和修改费用后的对局影响。",
        "limitation": "观测条件胜率不等同于替换卡位产生的因果收益。",
        "priority": "核心，统计指标参考",
    },
    {
        "id": "generalised-representations-2024",
        "title": "Learning With Generalised Card Representations for Magic: The Gathering",
        "authors": ["Timo Bertram", "Johannes Furnkranz", "Martin Muller"],
        "year": 2024, "venue": "IEEE CoG 2024; arXiv:2407.05879",
        "filename": "2024-generalised-card-representations.pdf",
        "sources": [("https://arxiv.org/pdf/2407.05879", "author preprint on arXiv")],
        "topic": "结合数值、类别与文本表示卡牌，支持未知卡牌的选牌预测。",
        "limitation": "预测玩家选牌不等同于预测胜率或单卡真实强度。",
        "priority": "补充，卡牌表示参考",
    },
    {
        "id": "draftencoder-2026",
        "title": "Predicting Drafted Deck Strength for Magic: the Gathering",
        "authors": ["Tomas Rigaux", "Hisashi Kashima"],
        "year": 2026, "venue": "arXiv:2607.04782; paper reports acceptance at CoG 2026",
        "filename": "2026-predicting-drafted-deck-strength.pdf",
        "sources": [("https://arxiv.org/pdf/2607.04782", "author preprint on arXiv")],
        "topic": "从卡牌和轮抽上下文预测最终套牌对局表现。",
        "limitation": "较新的数据驱动方法；依赖大量 MTG 数据，不能直接迁移到符文战场。",
        "priority": "补充，结果导向的套牌模型参考",
    },
]

UNAVAILABLE = [
    {
        "title": "Deep Learning Techniques for Explainable Resource Scales in Collectible Card Games",
        "year": 2022, "doi": "10.1109/TG.2020.3030742",
        "source_url": "https://doi.org/10.1109/TG.2020.3030742",
        "status": "not_downloaded",
        "reason": "未找到可公开取得的全文 PDF；已保存同一研究路线的 2019 年会议论文。",
    },
    {
        "title": "Deck Building in Collectible Card Games using Genetic Algorithms: A Case Study of Legends of Code and Magic",
        "year": 2021, "doi": "10.1109/SSCI50451.2021.9659984",
        "source_url": "https://web.ntnu.edu.tw/~tcchiang/publications/ssci2021a.htm",
        "status": "not_downloaded",
        "reason": "作者页面目前仅提供 DOI；未找到开放全文，不以摘要或目录充当论文。",
    },
]


def inspect_pdf(data: bytes) -> dict:
    if not data.startswith(b"%PDF-"):
        raise ValueError("Response is not an original PDF")
    reader = PdfReader(io.BytesIO(data))
    if not reader.pages:
        raise ValueError("PDF has no pages")
    first_page = reader.pages[0].extract_text() or ""
    if len(first_page.strip()) < 50:
        raise ValueError("Cannot verify the PDF's first-page text")
    return {
        "bytes": len(data), "pages": len(reader.pages),
        "sha256": hashlib.sha256(data).hexdigest(),
        "pdf_title": str((reader.metadata or {}).get("/Title", "")),
        "first_page_excerpt": " ".join(first_page.split())[:220],
    }


def download(paper: dict, previous: dict) -> dict:
    result = {key: value for key, value in paper.items() if key != "sources"}
    result["source_candidates"] = [url for url, _ in paper["sources"]]
    target = ROOT / paper["filename"]
    if target.exists():
        result.update(inspect_pdf(target.read_bytes()))
        for key in ("source_url", "resolved_url", "version", "downloaded_at_utc"):
            if key in previous:
                result[key] = previous[key]
        result["status"] = "downloaded"
        return result
    errors = []
    for url, version in paper["sources"]:
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "LocalResearchArchive/1.0"})
            with urllib.request.urlopen(request, timeout=35) as response:
                data = response.read(40_000_001)
                resolved_url = response.url
            if len(data) > 40_000_000:
                raise ValueError("PDF exceeds archive size limit")
            details = inspect_pdf(data)
            # Title terms catch login/notice PDFs or unrelated redirected documents.
            searchable = " ".join(PdfReader(io.BytesIO(data)).pages[0].extract_text().lower().split())
            anchor = {
                "resource-scale-2019": "resource scale",
                "evaluation-functions-2022": "evaluation functions",
                "q-deckrec-2018": "q-deckrec",
                "chaos-cards-2020": "chaos cards",
                "hearthstone-meta-2019": "hearthstone meta",
                "generalised-representations-2024": "card representations",
                "draftencoder-2026": "drafted deck strength",
            }[paper["id"]]
            if anchor not in searchable:
                raise ValueError(f"First page does not contain expected title: {anchor}")
            target.write_bytes(data)
            result.update(details, status="downloaded", source_url=url, resolved_url=resolved_url,
                          version=version, downloaded_at_utc=dt.datetime.now(dt.timezone.utc).isoformat())
            if errors:
                result["fallback_errors"] = errors
            return result
        except Exception as exc:
            errors.append({"url": url, "error": f"{type(exc).__name__}: {exc}"})
    result.update(status="not_downloaded", errors=errors)
    return result


def main() -> int:
    previous_file = ROOT / "manifest.json"
    previous = json.loads(previous_file.read_text(encoding="utf-8")) if previous_file.exists() else {}
    by_id = {p["id"]: p for p in previous.get("papers", [])}
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as executor:
        futures = {p["id"]: executor.submit(download, p, by_id.get(p["id"], {})) for p in PAPERS}
        results = []
        for paper in PAPERS:
            result = futures[paper["id"]].result()
            results.append(result)
            print(json.dumps({k: result[k] for k in ("id", "status", "pages", "version") if k in result}, ensure_ascii=False), flush=True)
    manifest = {
        "verified_at_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
        "validation": "Original PDF signature, pypdf parsing, page count, first-page title check, SHA-256; no edits to PDFs",
        "papers": results, "not_downloaded_references": UNAVAILABLE,
    }
    previous_file.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    lines = [
        "# TCG 卡牌评分与构筑研究", "",
        "保存原始论文 PDF，不改写正文。下载来源、版本、页数、时间和 SHA-256 见 [manifest.json](manifest.json)。", "",
        "建议先读 1、2、3；4、5 用于后续环境和统计验证；6、7 用于卡牌表示与数据驱动构筑。", "",
    ]
    for i, paper in enumerate(results, 1):
        title = f"[{paper['title']}]({paper['filename']})" if paper["status"] == "downloaded" else paper["title"]
        lines += [f"## {i}. {title}", "", f"- 年份与出处：{paper['year']}；{paper['venue']}",
                  f"- 优先级：{paper['priority']}", f"- 对应问题：{paper['topic']}",
                  f"- 解释边界：{paper['limitation']}"]
        if paper["status"] == "downloaded":
            lines += [f"- 保存版本：{paper['version']}；{paper['pages']} 页", f"- 原始来源：{paper['source_url']}"]
        else:
            lines += ["- 下载状态：未取得全文；详见 manifest 中的错误记录。"]
        lines += [""]
    lines += ["## 未取得公开全文的相关论文", ""]
    for paper in UNAVAILABLE:
        lines += [f"- [{paper['title']}]({paper['source_url']})（{paper['year']}）：{paper['reason']}"]
    lines += ["", "## 复核与重新下载", "", "运行 `python download_papers.py`（需要 pypdf）。已有 PDF 会复核且保留，不自动覆盖。", ""]
    (ROOT / "README.md").write_text("\n".join(lines), encoding="utf-8")
    return 0 if all(p["status"] == "downloaded" for p in results) else 2


if __name__ == "__main__":
    raise SystemExit(main())
