"""R2 documentation rendering and contract audit; never executes a game engine."""
import ast,collections,hashlib,inspect,json,re
from pathlib import Path
from read_card_operators import ROOT,CARDS,SOURCE,variants
D=ROOT/'docs';A=D/'basic-operators-api.md';api=A.read_text(encoding='utf-8');digest=hashlib.sha256(A.read_bytes()).hexdigest()
sigs={}
for b in re.findall(r'```python\n(.*?)\n```',api,re.S):
 if not re.match(r'[a-z_]+\(',b):continue
 fn=ast.parse('def '+b+':\n pass').body[0];args=fn.args;ps=[];start=len(args.args)-len(args.defaults)
 for i,a in enumerate(args.args):ps.append(inspect.Parameter(a.arg,inspect.Parameter.POSITIONAL_OR_KEYWORD,default=inspect.Parameter.empty if i<start else None))
 for a,default in zip(args.kwonlyargs,args.kw_defaults):ps.append(inspect.Parameter(a.arg,inspect.Parameter.KEYWORD_ONLY,default=inspect.Parameter.empty if default is None else None))
 sigs[fn.name]=inspect.Signature(ps)
rows=list(map(json.loads,(ROOT/'tmp/card-api-review-v2.jsonl').read_text(encoding='utf-8').splitlines()));by={r['number']:r for r in rows}
if len(sigs)!=72 or len(by)!=len(rows):raise ValueError('definitions or duplicate card')
used=collections.Counter();syntax_errors=[]
for r in rows:
 try:
  t=ast.parse(r['calls'])
  for c in ast.walk(t):
   if isinstance(c,ast.Call) and isinstance(c.func,ast.Attribute) and isinstance(c.func.value,ast.Name) and c.func.value.id=='ops':
    name=c.func.attr
    if name not in sigs:raise ValueError('unknown '+name)
    sigs[name].bind(*[None]*len(c.args),**{k.arg:None for k in c.keywords});used[name]+=1
 except (ValueError,TypeError,SyntaxError) as e:syntax_errors.append((r['number'],str(e)))
if syntax_errors:raise ValueError(syntax_errors)
def defects(r):return [g for g in r['gaps'] if not g.startswith(('DATA:','LANG:','VERIFY:'))]
def covered(r):return not defects(r)
def confirmed(r):return covered(r) and not any(g.startswith('VERIFY:') for g in r['gaps'])
def status(r):
 if defects(r):return '未完整覆盖'
 if not confirmed(r):return '已表达／语义待核'
 if not re.search(r'\bops\.',r['calls']):return '无独立动作／已确认'
 return '已表达／人工复核通过'
def link(n,prefix=''):
 start=(n-1)//100*100+1;end=min(start+99,len(CARDS));return f'[{n:04d} {CARDS[n-1][1]["name"]}]({prefix}card-operator-reading/{start:04d}-{end:04d}.md#card-{n:04d})'
fields=0;anchors=[]
for f in sorted((D/'card-operator-reading').glob('*.md')):
 chunks=re.split(r'(?=<a id="card-\d+">)',f.read_text(encoding='utf-8'))
 for i,ch in enumerate(chunks):
  m=re.match(r'<a id="card-(\d+)">',ch)
  if not m:continue
  n=int(m[1]);anchors.append(n)
  original=re.findall(r'~~~text\n(.*?)\n~~~',ch,re.S);expected=[t if t is not None else 'null' for (l,a,b),faces in variants(CARDS[n-1][0]) for t in (a,b)]
  if original!=expected:raise ValueError('original text changed '+str(n))
  fields+=len(original)
  if n not in by:continue
  r=by[n];ch=re.sub(r'\n<!-- API-REVIEW-START -->.*?<!-- API-REVIEW-END -->\n','\n',ch,flags=re.S)
  lines=['<!-- API-REVIEW-START -->','### 第二轮：72算子API分解\n',f'- 判定：**{status(r)}**。',f'- 本轮完整阅读核验：{r["review"]}',f'- 能力入口：{r["window"]}。',
   '- 公共绑定：`p: Player`为当前能力控制者，`me`为本实例，`here`为绑定地点。友方含盟友，your仅p；目标、模式、费用与阶段均按本段绑定。不同注释是独立能力入口，不是连着执行。',
   '- 固有关键词依V2闭集宏保留其明确参数与身份；显式内部展开替代该宏，不重复叠加。未给出的属性保持未知。']
  bs=[b for b in r['bindings'].split(';') if b.strip()]
  if bs:
   lines+=['\n参数绑定：\n','| 名称 | 类型 | 精确含义 |','| --- | --- | --- |']
   for b in bs:
    left,meaning=b.split('=',1);name,typ=left.split(':',1);typ=typ.replace('/',' \\| ')
    lines.append(f'| `{name.strip()}` | `{typ}` | {meaning.replace("|","&#124;")} |')
  lines+=['\nAPI调用：\n','```python',r['calls'],'```']
  if r['gaps']:lines+=['\n未决项及来源问题：\n']+[f'- **{g.split(":",1)[0]}**：{g.split(":",1)[1]}' for g in r['gaps']]
  lines+=['\n[第二轮覆盖／正确性报告](../card-api-coverage.md) · [V2 API](../basic-operators-api.md) · [第一轮存档](../operator-audits/round-1-reading.md#card-'+f'{n:04d})','<!-- API-REVIEW-END -->\n']
  pos=ch.find('### 文本组');chunks[i]=ch[:pos].rstrip()+'\n\n'+'\n'.join(lines)+'\n'+ch[pos:]
 f.write_text(''.join(chunks),encoding='utf-8')
if sorted(anchors)!=list(range(1,len(CARDS)+1)):raise ValueError('missing original card')
N=len(CARDS);read=len(rows);cov=sum(covered(r) for r in rows);ok=sum(confirmed(r) for r in rows);pending=sum(covered(r) and not confirmed(r) for r in rows);complete=read==N
report=['# 第二轮：72算子API全库阅读评估\n','[V2 API](basic-operators-api.md) · [逐卡笔记](card-operator-reading.md) · [V2修订及冗余处理](card-api-changes-v2.md) · [第一轮报告](card-api-coverage-v1.md)\n',
 f'状态：{"完整阅读已完成" if complete else "完整阅读进行中"}；本轮已逐张重读 **{read}/{N}**，未读卡不算通过。',f'API SHA-256：`{digest}`。',f'目录 SHA-256：`{hashlib.sha256(SOURCE.read_bytes()).hexdigest()}`。\n',
 '## 统计口径\n',
 '本轮从固定目录重新读取每张的全部EN／SC／TC规则、装备效果、属性与勘误，再对照该卡调用逐项核查。不是只复核上一轮失败卡；原文保留，每张有独立本轮判定。'
 '原生关键词按V2闭集宏及本卡参数计入，未定义宏或缺失能力体仍算未覆盖。\n',
 '表达覆盖率＝所有指令均有已登记API／闭集宏表示的本体数÷1106；无独立动作的纯属性／提醒卡可计入，来源译文缺失不自动当缺算子。'
 '人工语义复核确认率（本轮文档正确率）＝完整分解且在六项人工核查中无已知差错、无待核规则项的本体数÷1106。待核、错误、未完整覆盖和未阅读均不计通过。\n',
 '六项核查：①入口、时点和次数；②主体、目标、控制者／拥有者／行动者；③数值、领域和费用；④顺序、批次和事件身份；⑤持续期、关联和信息权限；⑥关键词、勘误、全部效果句段。'
 '这是同一作者依原文和规则进行的人工文档审核，不是独立裁判真值、执行引擎对局测试或规则正确性认证；不能把它解释为实战错误概率。\n',
 '| 指标 | 分子／分母 | 当前值 |','| --- | ---: | ---: |',f'| 完整阅读覆盖 | {read}/{N} | {read/N:.2%} |',f'| 表达覆盖 | {cov}/{N} | {cov/N:.2%} |',f'| 人工语义复核确认（文档正确率） | {ok}/{N} | {ok/N:.2%} |',f'| 已表达但待核 | {pending} | — |',f'| 未完整覆盖 | {read-cov} | — |',f'| 未阅读 | {N-read} | — |',
 '\n## 未完整覆盖卡牌\n','| 卡牌 | 本轮缺口 |','| --- | --- |']
for r in rows:
 for g in defects(r):
  report.append(f'| {link(r["number"])} | {g.replace("|","&#124;")} |')
report+=['\n## 已表达但语义待核卡牌\n','以下不算API表达缺口，但不计入文档正确率。\n','| 卡牌 | 待确认内容 |','| --- | --- |']
for r in rows:
 for g in r['gaps']:
  if g.startswith('VERIFY:'):report.append(f'| {link(r["number"])} | {g.replace("|","&#124;")} |')
report+=['\n## 来源差异及缺文\n','以下与算子缺口分开统计；读取采用明确勘误优先，不用译文缺文猜测零值。\n','| 卡牌 | 来源问题 |','| --- | --- |']
for r in rows:
 for g in r['gaps']:
  if g.startswith(('DATA:','LANG:')):report.append(f'| {link(r["number"])} | {g.replace("|","&#124;")} |')
report+=['\n## 调用与阅读留档核对\n',f'- 正式函数{len(sigs)}个；本轮{sum(used.values())}处ops调用均可解析并匹配必需参数及关键字。该项只检验结构，不能替代上述语义复核。',f'- 全目录{len(anchors)}个原始编号无遗漏重复，{fields}个原文字段逐一与固定目录相等；本轮已读卡恰有一次第二轮记录。',f'- 已重读文本变体{sum(len(r["text_groups"]) for r in rows)}组；每张保存本轮文本组指纹，禁止把未读张数补成通过。',
 '- 源快照含1106个本体、9039个印刷、2771组EN／SC／TC规则和装备效果文本、73个目录勘误；递归包含背面。未逐图视觉核验全部卡图，不把该项描述为已完成。',
 '- 对照[2026-10-09官方核心规则留档](references/riftbound/riftbound-core-rules-2026-10-09-en.pdf)。文档API无对应执行库；没有运行游戏模拟或已有项目测试套件。\n','| API | 本轮调用处数 |','| --- | ---: |']
report += [f'| `{name}` | {used[name]} |' for name in sigs]
report += ['\n'+('结论以以上全量分母统计及逐卡未决项为准。' if complete else '本轮未完成全量阅读，以上仅为进度，不作为最终全库正确性结论。')]
if complete:report += ['\n[最终结构与原文留存核对](operator-audits/round-2-validation.md)记录调用签名、变量绑定、文本指纹、文档链接及本轮API版本指纹。']
(D/'card-api-coverage.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
idx=D/'card-operator-reading.md';text=idx.read_text(encoding='utf-8');text=re.sub(r'\n<!-- API-INDEX-START -->.*?<!-- API-INDEX-END -->\n','\n',text,flags=re.S)
notice=f'\n<!-- API-INDEX-START -->\n第二轮72算子API：已完整重读{read}/{N}本体。[覆盖率及文档正确率](card-api-coverage.md) · [修订依据](card-api-changes-v2.md)。第一轮已[单独存档](operator-audits/round-1-reading.md)。\n<!-- API-INDEX-END -->\n'
pos=text.find('\n');text=text[:pos]+notice+text[pos:];idx.write_text(re.sub(r'\n{3,}','\n\n',text),encoding='utf-8')
print(json.dumps(dict(read=read,total=N,covered=cov,confirmed=ok,pending=pending,ops=sum(used.values()),complete=complete),ensure_ascii=False))
