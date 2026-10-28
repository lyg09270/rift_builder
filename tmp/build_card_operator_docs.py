"""Render the already-written manual reading notes into documentation only."""
from collections import Counter
import hashlib
import json
import re
from pathlib import Path

from read_card_operators import CAT, CARDS, FACES, ROOT, SOURCE, variants

DOCS = ROOT / 'docs'
OUT = DOCS / 'card-operator-reading'
OUT.mkdir(exist_ok=True)

notes = {}
for line in (ROOT / 'tmp/card-operator-notes.tsv').read_text(encoding='utf-8').splitlines():
    number, codes, note = line.split('|', 2)
    number = int(number)
    if number in notes:
        raise ValueError(f'Duplicate manual note {number}')
    notes[number] = (codes.split(','), note)
if set(notes) != set(range(1, len(CARDS) + 1)):
    raise ValueError('Manual reading coverage is incomplete')

def j(value):
    return json.dumps(value, ensure_ascii=False, separators=(',', ':'))

def txt(value):
    return 'null' if value is None else str(value)

def cell(value):
    return str(value).replace('|', '&#124;').replace('\n', '<br>')

def block(value, language='text'):
    value = txt(value)
    fence = '~' * max(3, max((len(m.group()) + 1 for m in re.finditer(r'~+', value)), default=3))
    return f'{fence}{language}\n{value}\n{fence}\n'

stats = {}
for lang in ('EN', 'SC', 'TC'):
    groups = [(cid, key, faces) for cid, _ in CARDS
              for key, faces in variants(cid) if key[0] == lang]
    stats[lang] = dict(cards=len({cid for cid, _, _ in groups}), variants=len(groups),
                       null_rules=sum(key[1] is None for _, key, _ in groups))

code_counts = Counter(code for codes, _ in notes.values() for code in codes)
main = (DOCS / 'card-operators.md').read_text(encoding='utf-8')
undefined = sorted(code for code in code_counts if f'`{code}`' not in main)
if undefined:
    raise ValueError(f'Undefined operator vocabulary: {undefined}')

all_links = []
for start in range(1, len(CARDS) + 1, 100):
    end = min(start + 99, len(CARDS))
    filename = f'{start:04d}-{end:04d}.md'
    all_links.append((start, end, filename))
    parts = [f'# 逐卡阅读 {start:04d}–{end:04d}\n',
             '[总索引](../card-operator-reading.md) · [算子定义](../card-operators.md)\n',
             '这是完整玩法文本的阅读留档。语义笔记和词汇由逐条阅读整理，'
             '不是自动关键词分类，也不是可执行规则映射。原始空值显示为 `null`。'
             '同文本组列代表印刷的精确位置；该组全部成员可从固定哈希的源文件重建。'
             '图片仅提供核对链接，本轮未逐张视觉校验。\n']
    for number in range(start, end + 1):
        cid, card = CARDS[number - 1]
        codes, note = notes[number]
        groups = variants(cid)
        names = {}
        for lang in ('EN', 'SC', 'TC'):
            names[lang] = sorted({f.get('printedName') for f in FACES[cid]
                                  if f['language'] == lang and f.get('printedName')})
        label = card['name']
        if names['SC']:
            label += '／' + names['SC'][0]
        parts += [f'<a id="card-{number:04d}"></a>\n', f'## {number:04d}. {label}\n',
                  f'- 身份：`{cid}`；[OpenRift](https://openrift.app/cards/{card["slug"]})；'
                  f'源位置：`cards["{cid}"]`。',
                  f'- 类型／超类型：`{j(card["types"])}`／`{j(card["superTypes"])}`；'
                  f'领域：`{j(card["domains"])}`。',
                  f'- Energy／Power／战力／武装战力：`{txt(card.get("energy"))}`／'
                  f'`{txt(card.get("power"))}`／`{txt(card.get("might"))}`／'
                  f'`{txt(card.get("mightBonus"))}`。',
                  f'- 标签：`{j(card.get("tags"))}`；目录关键词索引（含提及）：`{j(card.get("keywords"))}`。',
                  f'- 其他原始属性：`{j({k:v for k,v in card.items() if k not in ("name","slug","types","superTypes","domains","energy","power","might","mightBonus","tags","keywords","errata")})}`。',
                  '- 语义词汇：' + '、'.join(f'`{code}`' for code in codes) + '。',
                  f'- **人工阅读笔记：{note}**',
                  '- 文本组数：' + '；'.join(f'{lang}={sum(key[0] == lang for key, _ in groups)}'
                                           for lang in ('EN', 'SC', 'TC')) + '。\n']
        if not names['SC']:
            parts.append('- 简中印刷名称：当前来源未提供。\n')
        if not any(key[0] == 'SC' for key, _ in groups):
            parts.append('- **来源缺口：没有 SC 卡面，不以翻译补齐。**\n')
        for vi, ((lang, rules, effect), faces) in enumerate(groups, 1):
            face = min(faces, key=lambda f: (f.get('canonicalRank', 10**9), f['printing_id'], f['face_path']))
            group_names = sorted({txt(f.get('printedName')) for f in faces})
            shorts = sorted({f['shortCode'] for f in faces})
            pointer = f'printings["{face["printing_id"]}"]' + face['face_path'].removeprefix('front')
            parts += [f'### 文本组 {vi} · {lang}\n',
                      f'- 印刷名称：{j(group_names)}；短编号：`{j(shorts)}`；共 {len(faces)} 个面记录。',
                      f'- 代表来源：`{pointer}`；规范排序值：`{txt(face.get("canonicalRank"))}`'
                      '（仅选择展示代表，不据此裁决规则）。']
            image_ids = face.get('images', [])
            if isinstance(image_ids, list):
                image_keys = [im if isinstance(im, str) else im.get('imageId')
                              for im in image_ids if isinstance(im, (str, dict))]
                urls = [f'[图{i+1}](https://openrift.app/media/cards/{im}-full.webp)'
                        for i, im in enumerate(image_keys) if im]
                if urls:
                    parts.append('- 卡面图片：' + '、'.join(urls) + '。')
            parts += ['\n规则文本 `printedRulesText`：\n', block(rules)]
            parts += ['装备效果文本 `printedEffectText`：\n', block(effect)]
        if card.get('errata') is not None:
            parts += ['### 目录勘误（完整保留）\n',
                      block(json.dumps(card['errata'], ensure_ascii=False, indent=2), 'json')]
        else:
            parts.append('目录未附 `errata`；不由此断言不存在外部勘误。\n')
    (OUT / filename).write_text('\n'.join(parts).rstrip() + '\n', encoding='utf-8')

index = ['# 卡牌算子 V1：逐卡阅读索引\n', '[返回算子定义](card-operators.md)\n',
         '范围为本地 OpenRift 快照的全部1,106个卡牌本体。按英文名排序编号，'
         '每张保留人工阅读笔记、玩法属性、EN／SC／TC完整规则及装备效果文本和目录勘误。'
         '同玩法文本的印刷合组；不同文本不互相覆盖，递归包含背面。\n',
         f'源 SHA-256：`{hashlib.sha256(SOURCE.read_bytes()).hexdigest()}`。\n',
         '阅读整理日期：2026-10-27至2026-10-28。只生成文档；没有执行游戏转换或测试套件。\n',
         '| 语言 | 有卡面本体 | 文本组 | 规则字段为null的组 |',
         '| --- | ---: | ---: | ---: |']
for lang, s in stats.items():
    index.append(f'| {lang} | {s["cards"]} | {s["variants"]} | {s["null_rules"]} |')
index += ['\nnull可能表示纯属性卡，也可能表示该印刷缺文，须结合本体、其他印刷和笔记判断。'
          '未把缺中文、缺战力或损坏文本填成推测值。缺SC卡面：Bomb。\n',
          '## 分批记录\n', '| 批次 | 张数 |', '| --- | ---: |']
for start, end, filename in all_links:
    index.append(f'| [{start:04d}–{end:04d}](card-operator-reading/{filename}) | {end-start+1} |')
index += ['\n## 全卡目录\n',
          '词汇是语义阅读索引，不能仅凭有标签就宣称所有句段均已完成可执行映射。'
          '费用、数值、目标、期限等以分批附录原文及其来源为据。\n',
          '| 编号 | 英文名 | 简中印刷名 | 类型 | 语义词汇 |',
          '| --- | --- | --- | --- | --- |']
for number, (cid, card) in enumerate(CARDS, 1):
    start = ((number-1)//100)*100+1
    end = min(start+99,len(CARDS))
    names = sorted({f['printedName'] for f in FACES[cid]
                    if f['language']=='SC' and f.get('printedName')})
    index.append(f'| {number:04d} | [{cell(card["name"])}](card-operator-reading/{start:04d}-{end:04d}.md#card-{number:04d})'
                 f' | {cell("／".join(names) or "缺失")} | {cell("+".join(card["types"]))}'
                 f' | {", ".join(notes[number][0])} |')
index += ['\n## 词汇使用计数\n',
          '这是人工笔记显式列出的词汇次数；关键词内部展开未一律重复计入，'
          '不能解释为各类效果的统计总量。\n', '| ID | 涉及笔记数 |', '| --- | ---: |']
for code, count in sorted(code_counts.items()):
    index.append(f'| `{code}` | {count} |')
(DOCS/'card-operator-reading.md').write_text('\n'.join(index).rstrip()+'\n', encoding='utf-8')

print(json.dumps({'cards':len(notes),'languages':stats,'vocabulary':len(code_counts),
                  'batches':len(all_links),'errata_cards':sum(c.get('errata') is not None for _,c in CARDS),
                  'batch_bytes':sum(p.stat().st_size for p in OUT.glob('*.md'))},ensure_ascii=False))
