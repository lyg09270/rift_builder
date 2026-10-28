"""Render the manually reviewed P1 ledger. No approval inference or game execution."""
import json,hashlib,re,sys
from pathlib import Path
from read_card_operators import ROOT,CARDS
sys.stdout.reconfigure(encoding='utf-8')
rows=[json.loads(x) for x in (ROOT/'tmp/card-primitives-review-p1.jsonl').read_text(encoding='utf-8').splitlines()]
meta=json.loads((ROOT/'tmp/card-primitives-p1-frozen.json').read_text(encoding='utf-8'))
out=ROOT/'docs/card-primitives-reading-p1';out.mkdir(exist_ok=True)
counts={k:sum(r['status']==k for r in rows) for k in ('covered','verify','uncovered')}
for a in range(1,len(CARDS)+1,100):
    b=min(a+99,len(CARDS));subset=[r for r in rows if a<=r['number']<=b]
    if not subset:continue
    doc=[f'# P1逐卡复读 {a:04d}–{b:04d}\n', '[本轮报告](../card-primitives-coverage-p1.md) · [编写约定](../card-primitives-reading-p1.md) · [冻结原语](../basic-primitives-v4-p1-frozen.md)\n']
    for r in subset:
        n=r['number'];card=CARDS[n-1][1]
        doc += [f'<a id="card-{n:04d}"></a>',f'## {n:04d} {r["name"]}\n',
                f'- 判定：**{r["status"]}**。',f'- 本轮独立复读：{r["review"]}',
                f'- 入口、条件和角色：{r["window"]}',f'- 参数绑定：{r["bindings"]}',
                '- 固有关键词核对：'+('；'.join(r['native']) if r['native'] else '无额外固有关键词；动作名、被授予关键词、状态条件及衍生物提醒按原文归属。'),
                f'- 本体属性：类型={card["types"]}；领域={card["domains"]}；Energy/Power/Might={card["energy"]}/{card["power"]}/{card["might"]}；标签={card["tags"]}。',
                f'- [历史原文与印刷属性](../card-operator-reading/{a:04d}-{b:04d}.md#card-{n:04d})。\n']
        for issue in r['source_issues']+r['issues']:doc.append('- 保留问题：'+issue)
        all_parts=r.get('primitive_sections',[dict(entry=r['window'],program=r['primitive_program'])])+r.get('native_sections',[])
        for part in all_parts:
            doc += ['', '**入口／片段：'+part['entry']+'**','', '```python',part['program'],'```']
        doc += ['', '**本次实际重读的原文组**','']
        for i,g in enumerate(r['text_groups'],1):
            doc += [f'{g["language"]} 组{i}，SHA-256：`{g["hash"]}`。','', '~~~text',
                    'RULES: '+(g['text'] if g['text'] is not None else '<null>'),
                    'EFFECT: '+(g['effect'] if g['effect'] is not None else '<null>'),'~~~','']
        if card.get('errata') is not None:doc += ['目录勘误：','```json',json.dumps(card['errata'],ensure_ascii=False,indent=2),'```','']
    (out/f'{a:04d}-{b:04d}.md').write_text('\n'.join(doc)+'\n',encoding='utf-8')

report=['# P1原语全库阅读与覆盖评估\n',
        '[逐卡笔记与编写约定](card-primitives-reading-p1.md) · [冻结35原语](basic-primitives-v4-p1-frozen.md)\n',
        f'本轮已完整复读 **{len(rows)}/{len(CARDS)}** 张本体；确认表达覆盖{counts["covered"]}，待核{counts["verify"]}，未完整覆盖{counts["uncovered"]}，未读{len(CARDS)-len(rows)}。',
        f'固定分母确认表达覆盖率：**{counts["covered"]/len(CARDS)*100:.2f}%**。'+('本轮全库阅读已完成，结果仍未达到100%覆盖。' if len(rows)==len(CARDS) else '尚未读完，不能视作最终全库结果。'),
        '\n本轮是卡牌模型＋具名模板＋35原语的表达审阅与文档调用检查；不是35原语执行引擎测试，也没有独立测得游戏语义正确率。未知费用和语言／印刷差异继续保留，不按零或白板处理。',
        '\nAPI SHA-256：`'+meta['docs/basic-primitives-v4-p1.md']+'`。',
        '\n## 未覆盖与待核\n','| 卡牌 | 判定 | 问题 |','| --- | --- | --- |']
for r in rows:
    if r['status']=='covered':continue
    n=r['number'];a=(n-1)//100*100+1;b=min(a+99,len(CARDS))
    report.append(f'| [{n:04d} {r["name"]}](card-primitives-reading-p1/{a:04d}-{b:04d}.md#card-{n:04d}) | {r["status"]} | '+(';'.join(r['issues']).replace('|','／'))+' |')
audit_path=ROOT/'tmp/card-primitives-p1-audit.json'
if audit_path.exists() and len(rows)==len(CARDS):
    audit=json.loads(audit_path.read_text(encoding='utf-8'))
    assert not audit['errors'] and not audit['direct_keyword_exceptions']
    (out/'audit.json').write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    report += ['\n## 检查结果\n',
               '| 指标 | 结果 |', '| --- | --- |',
               f'| 本体逐卡阅读 | {len(rows)}/{len(CARDS)}，100% |',
               f'| EN／SC／TC规则与效果原文组 | {audit["source_groups"]}组，全部已记录 |',
               f'| 所有能力均确认可表达 | {counts["covered"]}/{len(CARDS)}，{counts["covered"]/len(CARDS)*100:.2f}% |',
               f'| 契约缺口 | {counts["uncovered"]}张 |',
               f'| 待核验 | {counts["verify"]}张，不进入覆盖分子 |',
               f'| 原语名称及参数签名检查 | {audit["signatures_passed"]}/{audit["primitive_call_sites"]}处，100% |',
               f'| 已出现的闭集字面值检查 | {audit["literal_checks"]}处，无越界 |',
               '| 实战语义正确率 | 未测；没有35原语执行引擎或独立对局判定基准 |',
               '\n签名检查验证函数名、实参数量与关键字名称；不是所有符号绑定值的动态类型检查，也不证明目标、费用、替代、时序已被引擎正确执行。未覆盖和待核条目保留候选调用及阻塞原因，不作为可执行的通过案例。',
               '\n规范能力采用已核定英文及目录勘误；所有可用中文和印刷差异一起复读。100张保留DATA／LANG来源问题，详见逐卡条目。这些差异不能解释为所有语言文本彼此等价，卡面文本复读也不等于9039份印刷图逐图视觉认证。',
               '\n[机器可读检查记录](card-primitives-reading-p1/audit.json)保存冻结输入指纹、各原语调用数及检查边界。调用数是文档静态调用位置，分支和循环不按实际对局次数计。',
               '\n## 契约缺口与简化复核\n',
               '6张未覆盖都涉及费用降低但Energy最低为1。CostRule没有显式最低值字段，也未约定读取“本修饰施加前费用”的求值阶段；不能把最低值藏进自然语言差值。后续应先补费用规则的结构化字段及多修饰求值顺序，再重新检查这些牌，不必为此新增基本原语。',
               '\n35项原语在全库分解中均实际出现，未发现可直接删除且行为完全等价的一对API；这不等于已证明35是理论最小数量。以下相似接口仍有不同职责：',
               '\n| 相似接口 | 保留原因 |', '| --- | --- |',
               '| instantiate／zone_change | 建立新身份与迁移已有身份不同；play仅对新token先创建。 |',
               '| zone_change／location_change／order_change | 换区域、场上换位置、同牌堆重排分别保存不同身份与规则。 |',
               '| damage_record／damage_clear | 真实伤害与清除伤害不是正负同一数值操作，事件原因不同。 |',
               '| ability_add／ability_mask／ability_patch | 授新能力、临时失活与有限元数据修改不能互换。 |',
               '| 7项分域规则登记 | 费用、伤害、产费、入场、指令参数、权限、固定规则键各有闭集；合成通用modify会把复杂性藏进参数。 |',
               '\n## 本轮纠正\n',
               '逐卡复读修正了旧稿的自身play递归演示、父项提前等待子play定稿、当前位置与事件地点混用、选择结果未显式累计、关键词归属及独立入口串行混排。最终调用检查又发现并补展开一处嵌在布尔表达式里的banish，复查后无残留旧ops调用。原语API保持冻结，未借中途扩充接口提高覆盖率。']
report += ['\n## 已写入批次\n']
for a in range(1,len(CARDS)+1,100):
    b=min(a+99,len(CARDS));count=sum(a<=r['number']<=b for r in rows)
    if count:report.append(f'- [{a:04d}–{b:04d}](card-primitives-reading-p1/{a:04d}-{b:04d}.md)：{count}张。')
(ROOT/'docs/card-primitives-coverage-p1.md').write_text('\n'.join(report)+'\n',encoding='utf-8')
print(json.dumps(dict(read=len(rows),**counts),ensure_ascii=False))
