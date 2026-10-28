"""Render manual API rereading into existing documentation, without game execution."""
import ast
from collections import Counter
import hashlib
import inspect
import json
import re
from pathlib import Path
from read_card_operators import ROOT, CARDS, SOURCE, CAT, FACES, variants

DOCS = ROOT / 'docs'
api_path = DOCS / 'basic-operators-api.md'
api = api_path.read_text(encoding='utf-8')
signatures = {}
for block in re.findall(r'```python\n(.*?)\n```', api, re.S):
    if not re.match(r'[a-z_]+\(', block):
        continue
    fn = ast.parse('def ' + block + ':\n    pass\n').body[0]
    args = fn.args
    parameters = []
    default_start = len(args.args) - len(args.defaults)
    for i, arg in enumerate(args.args):
        parameters.append(inspect.Parameter(arg.arg, inspect.Parameter.POSITIONAL_OR_KEYWORD,
                          default=inspect.Parameter.empty if i < default_start else None))
    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        parameters.append(inspect.Parameter(arg.arg, inspect.Parameter.KEYWORD_ONLY,
                          default=inspect.Parameter.empty if default is None else None))
    signatures[fn.name] = inspect.Signature(parameters)

rows = [json.loads(line) for line in (ROOT/'tmp/card-api-review.jsonl').read_text(encoding='utf-8').splitlines()]
by_number = {row['number']:row for row in rows}
if len(rows) != len(by_number):
    raise ValueError('Duplicate reading number')
errors = []
used = Counter()
for row in rows:
    try:
        tree = ast.parse(row['calls'])
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                    and isinstance(node.func.value, ast.Name) and node.func.value.id == 'ops'):
                continue
            name = node.func.attr
            if name not in signatures:
                raise ValueError(f'Unknown API: {name}')
            if any(kw.arg is None for kw in node.keywords):
                raise ValueError('Unspecified keyword unpacking')
            signatures[name].bind(*[None]*len(node.args), **{kw.arg:None for kw in node.keywords})
            used[name] += 1
    except (SyntaxError, ValueError, TypeError) as exc:
        errors.append((row['number'], str(exc)))
if errors:
    raise ValueError(errors)

MACRO_GAPS = ('DELEGATED', 'REPEAT', 'FLOW_EXIT')

def issues(row, excluded=('DATA','LANG')):
    return [g for g in row['gaps'] if g.split(':',1)[0] not in excluded]

def status(row):
    if any(g.split(':',1)[0] not in ('DATA','LANG',*MACRO_GAPS) for g in row['gaps']):
        return '部分覆盖'
    if any(g.split(':',1)[0] in MACRO_GAPS for g in row['gaps']):
        return '委托未展开'
    if not re.search(r'\bops\.',row['calls']):
        return '无独立文本动作'
    return '已绑定上下文内覆盖'

for file in (DOCS/'card-operator-reading').glob('*.md'):
    content = file.read_text(encoding='utf-8')
    chunks = re.split(r'(?=<a id="card-\d+">)', content)
    changed = False
    for i, chunk in enumerate(chunks):
        match = re.match(r'<a id="card-(\d+)">',chunk)
        if not match or int(match[1]) not in by_number:
            continue
        row = by_number[int(match[1])]
        chunk = re.sub(r'\n<!-- API-REVIEW-START -->.*?<!-- API-REVIEW-END -->\n', '\n', chunk, flags=re.S)
        bindings = [b for b in row['bindings'].split(';') if b.strip()]
        lines = ['<!-- API-REVIEW-START -->', '### 69算子 API 复读\n',
                 f'- 状态：**{status(row)}**。',f'- 执行入口／条件：{row["window"]}。',
                 '- 公共绑定：`p: Player` 为本能力控制者；`me` 为本卡实例；`here: Location` 为该能力绑定地点。'
                 '原有固有关键词及基础属性仍保留；显式写出的关键词内部调用用于替代该宏执行体，不与宏重复执行。'
                 '友方包含盟友；“p控制／your”仅指p；空缺属性必须报错，不当作0。']
        if bindings:
            lines += ['\n参数绑定：\n', '| 名称 | 类型 | 精确含义 |', '| --- | --- | --- |']
            for b in bindings:
                left, meaning = b.split('=',1)
                name, typ = left.split(':',1)
                typ=typ.replace('/', ' \\| ')
                lines.append(f'| `{name.strip()}` | `{typ}` | {meaning.replace("|","&#124;")} |')
        lines += ['\nAPI调用：\n','```python',row['calls'],'```']
        if row['gaps']:
            lines.append('\n未覆盖／来源问题：\n')
            lines += [f'- **{g.split(":",1)[0]}**：{g.split(":",1)[1]}' for g in row['gaps']]
        lines += ['\n[覆盖报告](../card-api-coverage.md) · [函数签名](../basic-operators-api.md)',
                  '<!-- API-REVIEW-END -->\n']
        insert = '\n'.join(lines)
        pos = chunk.find('### 文本组')
        if pos < 0:
            raise ValueError(f'No source text section for card {row["number"]}')
        chunks[i] = chunk[:pos].rstrip() + '\n\n' + insert + '\n' + chunk[pos:]
        changed = True
    if changed:
        file.write_text(''.join(chunks),encoding='utf-8')

def card_link(n):
    start=((n-1)//100)*100+1
    end=min(start+99,len(CARDS))
    return f'[{n:04d} {CARDS[n-1][1]["name"]}](card-operator-reading/{start:04d}-{end:04d}.md#card-{n:04d})'

counts=Counter(status(row) for row in rows)
complete=len(rows)==len(CARDS) and set(by_number)==set(range(1,len(CARDS)+1))
source_blocks=0
note_numbers=[]
for file in sorted((DOCS/'card-operator-reading').glob('*.md')):
    for chunk in re.split(r'(?=<a id="card-\d+">)', file.read_text(encoding='utf-8')):
        match=re.match(r'<a id="card-(\d+)">',chunk)
        if not match:
            continue
        n=int(match[1]);note_numbers.append(n)
        actual=re.findall(r'~~~text\n(.*?)\n~~~',chunk,re.S)
        expected=[text if text is not None else 'null'
                  for (lang,rules,effect),faces in variants(CARDS[n-1][0])
                  for text in (rules,effect)]
        if actual!=expected:
            raise ValueError(f'Raw source text changed or missing in card {n}')
        if n in by_number and chunk.count('<!-- API-REVIEW-START -->')!=1:
            raise ValueError(f'API section missing or duplicated for {n}')
        source_blocks+=len(actual)
if sorted(note_numbers)!=list(range(1,len(CARDS)+1)):
    raise ValueError('Existing reading note numbers missing or duplicated')
report=['# 69算子 API：卡牌覆盖复读\n',
        '[逐卡原阅读笔记](card-operator-reading.md) · [算子API](basic-operators-api.md) · [算子功能重复检查](card-api-overlap.md)\n',
        f'状态：{"全目录复读完成" if complete else "复读进行中"}；已复读 **{len(rows)} / {len(CARDS)}** 个卡牌本体。',
        f'API SHA-256：`{hashlib.sha256(api_path.read_bytes()).hexdigest()}`。',
        f'目录 SHA-256：`{hashlib.sha256(SOURCE.read_bytes()).hexdigest()}`。\n',
        '## 结论\n',
        '**当前69个API不能完整覆盖本地全目录。** 已对全部本体写入调用／明确缺口；'
        '完整阅读覆盖不等于效果表达完整覆盖。未修改API参考来绕过缺口。\n',
        '## 阅读范围\n',
        f'- 本地来源：`data/sources/openrift/catalog.json`，{len(CARDS)}个本体，{len(CAT["printings"])}个印刷记录；递归纳入side2。',
        f'- 实际对照{sum(len(variants(cid)) for cid,_ in CARDS)}组EN／SC／TC规则＋装备效果文本变体，'
        f'{sum(bool(c.get("errata")) for _,c in CARDS)}个目录勘误。禁牌、token、提醒物及空白文本牌也纳入，未跳过。',
        '- 范围固定为该本地快照。非上述三种语言的译文和所有卡图的逐图视觉核对不在本次完成声明内；没有用缺失译文推测效果。\n',
        '## 判定口径\n',
        '每张重新对照全部EN／SC／TC规则与装备效果变体及目录勘误，直接修改原分批笔记。'
        '接口保持69个，不增添调度器或万能效果函数来掩盖缺口。\n',
        '调用中的选择器、费用、数值表达式等均在该牌参数表给出类型和精确含义。'
        '不同能力入口用代码注释分开，不表示全部能力连续执行。普通触发、主动时机、历史条件作为已绑定执行上下文列明；'
        '这不代表69个动作API本身实现了完整事件调度。新建未来触发、自反链项、改写待发生事件等若没有明确接口，单列未覆盖。\n',
        '`THIS_PLAY`、`WHILE_CONDITION`、`WHILE_ATTACHED`等局部名称均在对应牌的参数表绑定为API的Duration值；'
        '不是新算子。大写关键词及规则名表示参考API的具名标识。选择、费用历史和亮出快照须由明确上下文提供，不能靠调用代码猜测。\n',
        '固有关键词和基础属性保留原定义；写出内部展开时替代原宏执行，不叠加运行。'
        'Repeat、Flow和少量提醒模板未独立展开者另标“委托未展开”，不等于其宏委托一定不可用，也不算独立映射证明。'
        '无独立文本动作的提醒物／纯属性牌不伪造空算子。\n',
        '| 状态 | 本体数 |', '| --- | ---: |']
for key in ('已绑定上下文内覆盖','部分覆盖','委托未展开','无独立文本动作'):
    report.append(f'| {key} | {counts[key]} |')
report += [f'| 尚未复读 | {len(CARDS)-len(rows)} |',
           '\n“已绑定上下文内覆盖”仅表示在表内前置状态、选择、关键词定义和普通能力入口已提供时，效果体可表达；'
           '不是可直接运行的完整卡牌程序，也不是全规则认证。费用对象与选择器等以API的具名类型绑定，尚无对应运行库供运行时验证。\n',
           '\n## 无法完整覆盖的卡牌\n',
           '以下分列明确缺口／契约疑点和宏未展开。来源缺文另外列出，不混算缺算子。'
           '同一卡可能有多个问题，每行链接到具体调用和缺失句段。\n',
           '### 动作缺口及待澄清契约\n',
           '| 卡牌 | 问题 |', '| --- | --- |']
for row in rows:
    for gap in issues(row):
        if gap.split(':',1)[0] not in MACRO_GAPS:
            report.append(f'| {card_link(row["number"])} | {gap.replace("|","&#124;")} |')
report += ['\n### 关键词／模板宏未独立展开\n',
           '这些牌的已知单次效果照常写入原笔记；这里单列剩余宏的展开问题。'
           '例如Flow原生宏可以被保留，但原子展开时仍缺少离链替代契约。\n',
           '| 卡牌 | 未展开部分 |', '| --- | --- |']
for row in rows:
    for gap in issues(row):
        if gap.split(':',1)[0] in MACRO_GAPS:
            report.append(f'| {card_link(row["number"])} | {gap.replace("|","&#124;")} |')
report += ['\n### 问题类别统计\n',
           '按受影响本体去重计数；类别之间有交集，不可相加当作未覆盖卡数。\n',
           '| 问题标识 | 本体数 |', '| --- | ---: |']
gap_counts=Counter(code for row in rows for code in set(g.split(':',1)[0] for g in issues(row)))
for code,n in gap_counts.most_common():
    report.append(f'| `{code}` | {n} |')
report += ['\n## 来源缺文及语言差异\n', '| 卡牌 | 来源问题 |', '| --- | --- |']
for row in rows:
    for gap in row['gaps']:
        if gap.startswith(('DATA:','LANG:')):
            report.append(f'| {card_link(row["number"])} | {gap.replace("|","&#124;")} |')
report += ['\n## 关键规则依据\n',
           '[官方核心规则本地留档：2026-10-09](references/riftbound/riftbound-core-rules-2026-10-09-en.pdf)。'
           '卡面勘误的来源链接与生效日期保留在各卡原笔记中。\n',
           '| 规则 | 本次判定用途 |', '| --- | --- |',
           '| 133.5.a.1、161.1.a、175 | 符文、传奇不属于Permanent，不能向只接受Permanent的ready/exhaust传入 |',
           '| 383、387–390 | 区分普通触发入口、自反待处理链项及新建延迟能力 |',
           '| 417、418.8 | 回收到底及次序；“造成X，每个……”为一个数量计算后的伤害实例 |',
           '| 441.1、491.8.e、740.1.a | 顶牌入废的Burn身份；friendly包含盟友而your仅本玩家 |',
           '| 715、829 | 分配与非分配伤害的Bonus处理不同；Flow的离链放逐是延迟替代 |']
report += ['\n## 文档调用核对\n',
           f'逐块解析调用并对照参考文档签名，已记录 **{sum(used.values())}** 处ops调用，'
           '未调用未登记函数、未漏必需参数、未使用未知关键字参数；代码块语法可解析。'
           '这只是文档结构核对，不执行游戏逻辑，不证明绑定对象的运行时有效性，也不是测试套件。\n',
           f'逐卡编号1至{len(CARDS)}无遗漏或重复；每张恰有一个API复读区。'
           f'原笔记中的{source_blocks}个规则／装备效果原文字段逐一与固定目录的全部文本组相等，原文没有被调用摘要替换。\n',
           '额外核对了入场状态类型、伤害/次数参数、弃牌数量与cards关键字，以及Rune／Legend不属于Permanent导致的朝向接口缺口。'
           '操作次序、动作归属、批次和延迟行为仍按上表保留疑点，不将语法通过等同语义通过。\n',
           '| API | 已记录调用处数 |', '| --- | ---: |']
for name in signatures:
    report.append(f'| `{name}` | {used[name]} |')
if not complete:
    report += ['\n尚未完成全量复读，暂不下全目录覆盖结论。\n']
else:
    report += ['\n结论：当前69个API**不能宣称完整覆盖全目录**。上列未覆盖项、委托展开及来源问题均须处理；'
               '已绑定上下文内覆盖也不等于完整对局规则认证。\n']
(DOCS/'card-api-coverage.md').write_text('\n'.join(report).rstrip()+'\n',encoding='utf-8')
index=DOCS/'card-operator-reading.md'
text=index.read_text(encoding='utf-8')
text=re.sub(r'\n<!-- API-INDEX-START -->.*?<!-- API-INDEX-END -->\n','\n',text,flags=re.S)
notice=('\n<!-- API-INDEX-START -->\n'
        f'69算子API复读：已完成 {len(rows)}/{len(CARDS)} 个本体。'
        '[覆盖／未覆盖清单](card-api-coverage.md) · [功能重复检查](card-api-overlap.md)。'
        '原分批笔记已就地加入调用与参数绑定，原文和旧阅读笔记保留。\n'
        '<!-- API-INDEX-END -->\n')
first=text.find('\n',text.find('\n')+1)
text=text[:first]+notice+text[first:]
index.write_text(re.sub(r'\n{3,}','\n\n',text),encoding='utf-8')
print(json.dumps({'reviewed':len(rows),'complete':complete,'statuses':dict(counts),'ops_calls':sum(used.values())},ensure_ascii=False))
