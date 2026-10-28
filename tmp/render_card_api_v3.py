"""Render R3 authored records; does not certify semantics or execute card effects."""
import hashlib,json,re
from pathlib import Path
from read_card_operators import ROOT,CARDS,variants,SOURCE
D=ROOT/'docs';P=ROOT/'tmp/card-api-review-v3.jsonl'
rows=[json.loads(x) for x in P.read_text(encoding='utf-8').splitlines()] if P.exists() else []
by={r['number']:r for r in rows};N=len(CARDS)
assert len(by)==len(rows)
api_hash=hashlib.sha256((D/'basic-operators-api.md').read_bytes()).hexdigest()
assert all(r['api_sha256']==api_hash for r in rows)
def cardlink(n,prefix=''):
 a=(n-1)//100*100+1;b=min(a+99,N)
 return f'[{n:04d} {CARDS[n-1][1]["name"]}]({prefix}card-operator-reading/{a:04d}-{b:04d}.md#card-{n:04d})'
for path in sorted((D/'card-operator-reading').glob('*.md')):
 text=path.read_text(encoding='utf-8');originals=re.findall(r'~~~text\n(.*?)\n~~~',text,re.S)
 chunks=re.split(r'(?=<a id="card-\d+">)',text)
 for i,ch in enumerate(chunks):
  m=re.match(r'<a id="card-(\d+)">',ch)
  if not m or int(m[1]) not in by:continue
  n=int(m[1]);r=by[n]
  expected=[t if t is not None else 'null' for (l,a,b),faces in variants(CARDS[n-1][0]) for t in (a,b)]
  assert re.findall(r'~~~text\n(.*?)\n~~~',ch,re.S)==expected,n
  ch=re.sub(r'\n?<!-- R3-START -->.*?<!-- R3-END -->\n?','\n',ch,flags=re.S)
  ch=ch.replace('### 当前专项核验：V2.1真实效果与分解','### V2.1专项核验历史（当前以第三轮为准）')
  label={'confirmed':'本轮已确认','verify':'本轮待核，不计确认覆盖','uncovered':'本轮未完整覆盖'}[r['status']]
  body=['<!-- R3-START -->','### 第三轮：V3的71函数API分解\n',f'- 判定：**{label}**。',f'- 本轮完整阅读记录：{r["review"]}',f'- 能力入口与条件：{r["window"]}',
        '- 公共绑定：p为当前能力控制者，me为本实例，here依本卡指代规则绑定。不同注释是独立能力、阶段或回调程序体，不能把整块依次执行。目标／模式、费用与结算选择按绑定时点保存；固有关键词按实际卡文的V3闭集宏展开，显式展开替代宏，不重复授予。来源缺值保留未知，规则明确值须注明来源。',
        '\n参数绑定：\n','| 名称 | 类型 | 精确含义 |','| --- | --- | --- |']
  for x in r['bindings'].split(';'):
   if not x.strip():continue
   left,meaning=x.split('=',1);name,typ=left.split(':',1)
   body.append(f'| `{name.strip()}` | `{typ}` | {meaning.replace("|","&#124;")} |')
  body+=['\nAPI调用'+('（候选；待核参数确认前禁止执行）' if r['status']!='confirmed' else '')+'：\n','```python',r['calls'],'```']
  if r['gaps']:body+=['\n待核／未覆盖／来源问题：\n']+['- '+g for g in r['gaps']]
  body+=['\n[第三轮覆盖报告](../card-api-coverage.md) · [当前V3 API](../basic-operators-api.md) · [修订与简化](../card-api-changes-v3.md)。下方旧轮次仅供追溯。','<!-- R3-END -->\n']
  offsets=[ch.find(k) for k in ['<!-- RULES-REVIEW-START -->','<!-- API-REVIEW-START -->','### 文本组'] if ch.find(k)>=0]
  pos=min(offsets);chunks[i]=ch[:pos]+'\n'.join(body)+'\n'+ch[pos:]
 result=''.join(chunks)
 assert originals==re.findall(r'~~~text\n(.*?)\n~~~',result,re.S)
 if result!=text:path.write_text(result,encoding='utf-8')
confirmed=sum(r['status']=='confirmed' for r in rows);verify=sum(r['status']=='verify' for r in rows);uncovered=sum(r['status']=='uncovered' for r in rows)
report=['# 第三轮：71函数API全库阅读与覆盖评估\n',
        '[基本算子参考](basic-operators-api.md) · [修订与简化依据](card-api-changes-v3.md) · [逐卡笔记](card-operator-reading.md) · [原第二轮报告](operator-audits/round-2-coverage.md)\n',
        f'状态：{"全部本体完整复读完成" if len(rows)==N else "全库复读进行中，尚不能给出最终全库覆盖结论"}。已读**{len(rows)}/{N}**；API固定指纹`{api_hash}`。\n',
        '## 口径\n',
        '本轮重新读取每个本体全部可用EN／SC／TC卡面规则、装备效果、基础属性与勘误；每张有独立本轮记录。不是把第二轮成功记录直接重命名。自动语法迁移只供人工对照，不能自动判通过。所有图片未逐图全库核验。\n',
        '**确认覆盖率**＝本轮完整分解且没有已知语义错误、API缺口或规则待核的卡数÷1106。该指标把待核与未读排除分子。**结构表达率**＝已有登记API／闭集宏候选结构的卡数÷1106；它包括语义待核草稿，不代表可执行正确，更不能单凭这一数值宣称全部真实效果完整覆盖。\n',
        '核验项目：入口／时点／次数；控制者／拥有者／行动者；目标／范围／信息权限；费用／数值／快照；顺序／批次／实际结果；期限／关联／关键词／勘误。没有独立裁判真值或执行引擎，不把人工确认率称为实战正确概率。\n',
        '| 指标 | 分子／分母 | 当前值 |','| --- | ---: | ---: |',f'| 完整复读 | {len(rows)}/{N} | {len(rows)/N:.2%} |',f'| 确认覆盖率 | {confirmed}/{N} | {confirmed/N:.2%} |',f'| 结构表达率（含待核草稿） | {confirmed+verify}/{N} | {(confirmed+verify)/N:.2%} |',f'| 已读但语义待核 | {verify} | — |',f'| 已读但API未覆盖 | {uncovered} | — |',f'| 尚未阅读 | {N-len(rows)} | — |',
        '\n## 未完整覆盖及待核\n','| 卡牌 | 状态 | 具体问题 |','| --- | --- | --- |']
for r in rows:
 if r['status']=='confirmed':continue
 issues=[g for g in r['gaps'] if not g.startswith(('DATA:','LANG:'))]
 report.append(f'| {cardlink(r["number"])} | {r["status"]} | {"；".join(issues).replace("|","&#124;")} |')
report+=['\n## 本轮修订及简化\n',
         '73→71函数：ready／exhaust合为orient；empower／disempower合为change_empowerment。保留动作模式、事件身份、成本及叠层限制。其余接口保留理由见[简化依据](card-api-changes-v3.md)。\n',
         '每条人工记录保留原文组指纹与V3 API指纹。原始目录及5542个原文规则／装备字段不手改；中文缺文、版本差异另列源问题。待核数可能在完整复读中增加，不能沿用上一轮只有五张的假设。\n',
         '文档接口没有对应的执行引擎。本轮不运行项目测试套件；结构核对只说明调用名、签名、引用与原文留存的一致性。\n']
(D/'card-api-coverage.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
idx=D/'card-operator-reading.md';text=idx.read_text(encoding='utf-8')
text=re.sub(r'\n<!-- R3-INDEX-START -->.*?<!-- R3-INDEX-END -->\n','\n',text,flags=re.S)
notice=f'\n<!-- R3-INDEX-START -->\n当前第三轮V3（71函数）：已完整复读{len(rows)}/{N}，确认{confirmed}，待核{verify}，未覆盖{uncovered}。[报告](card-api-coverage.md) · [修订与简化](card-api-changes-v3.md)。以下旧轮次数值仅供历史追溯。\n<!-- R3-INDEX-END -->\n'
pos=text.find('\n');text=text[:pos]+notice+text[pos:];idx.write_text(text,encoding='utf-8')
print(json.dumps(dict(read=len(rows),confirmed=confirmed,verify=verify,uncovered=uncovered,unread=N-len(rows)),ensure_ascii=False))
