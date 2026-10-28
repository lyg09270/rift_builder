"""Author the explicitly reviewed 12-card documentation; no game execution."""
from pathlib import Path
import hashlib,json,re

ROOT=Path(__file__).resolve().parents[1]
D=ROOT/'docs'
old={r['number']:r for r in map(json.loads,(ROOT/'tmp/card-api-review-v2.jsonl').read_text(encoding='utf-8').splitlines())}
api_hash=hashlib.sha256((D/'basic-operators-api.md').read_bytes()).hexdigest()
rows=[]

def record(n, verdict, conclusion, basis, *, calls=None, bindings=None, window=None, pending=None):
    r=dict(old[n])
    r.update(scope='12-card-targeted-rulings',api_version='2.1',api_sha256=api_hash,
             verdict=verdict,conclusion=conclusion,basis=basis)
    if calls is not None:r['calls']=calls
    if bindings is not None:r['bindings']=bindings
    if window is not None:r['window']=window
    r['gaps']=[pending] if pending else []
    rows.append(r)

record(201,'verify','重打权限及任意Power1替代基础费明确；跨重打计数与Bonus适用时点未获充分裁定。下列仍为候选草稿，不是已确认程序。',
       '卡图0201；规则124、356.1.a、359.3.e.15、712–715。',
       pending='VERIFY:仍待明确跨重打伤害历史、旧Bonus是否继承及新Bonus何时生效；不写死伤害序列。')
record(286,'verify','普通英文卡图确认己方沙兵百炼及装备历史门槛；金属奖品印刷措辞不同，未查到可统一授权范围的官方勘误。',
       '卡图0286；目录两组EN；规则821。',
       pending='VERIFY:Your Sand Soldiers与Sand Soldiers you play的控制、区域及特征引用边界未证实等价。')
record(338,'verify','首部Fury1是触发能力定稿费用；其与后续打出印刷费的精确联系未取得充分官方裁定。',
       '卡图0338；规则204.1.c、383.3.b、404.1.b.1；社区QOTD仅作检索线索。',
       bindings='cost:Cost=Fury1;binding:CostBinding=可选弃置触发的基础费用，在触发定稿时支付;dest:Location=该次打出的合法单位目的地;permit:PlayPermission=该次弃置触发允许从p废牌打出me;policy:CostPolicy=尚待权威依据绑定的后续打出政策，当前不得执行此候选程序',
       calls='''# 触发定稿阶段（已查实）
paid = ops.pay(p, cost, binding=binding)
# 下方play仅为待核候选；policy尚无确认取值，禁止据此执行或计通过
if paid.value is not None:
    ops.play(me, p, origin=p.trash, destination=dest, cost_policy=policy, permission=permit)''',
       pending='VERIFY:不能仅凭触发费用角色推定后续免费或追加印刷费；policy未核，程序不准执行。')
record(367,'confirmed','按勘误及专门FAQ，补实际眩晕、给予负战力与回手三种替代；交换先算共同差值，零减值或无法实际眩晕不替代。',
       '卡图0367；Vendetta勘误及2026-08-14 FAQ的Switcheroo、Blast Cone、Back Off、Stupefy例子。',
       window='主动Body2仅未强化时可用；持续替代仅me在场且已强化，事件来源必须是选择me的法术／能力',
       bindings='cost:Cost=Body2;binding:CostBinding=仅未强化主动基础费用;stun_events:EventPattern=kind STUN且stage before，对象me，来源法术或能力的选择记录含me，且原眩晕动作实际可发生;might_events:EventPattern=kind MIGHT_CHANGE且stage before，对象me，计算后delta小于0，来源法术或能力选择记录含me;return_events:EventPattern=kind ZONE_TRANSFER且stage before，对象me由场上回手，来源法术或能力选择记录含me;rewrite:EventRewrite=resume_original False，replacement为下方本回合加三调用；其余程序为空;dur:Duration=WHILE(me在场且已强化)',
       calls='''# 主动能力定稿付款，结算强化
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 持续替代登记：三种事件共享同一明确替代程序
ops.replace_event(stun_events, rewrite, duration=dur)
ops.replace_event(might_events, rewrite, duration=dur)
ops.replace_event(return_events, rewrite, duration=dur)
# rewrite.replacement执行体
ops.modify_might([me], 3, duration=THIS_TURN)''')
record(440,'confirmed','夺控不是无条件THIS_TURN到期；在指定回合末延迟能力中精确结束关联控制，再召回。已过结束阶段开始时点则不生成延迟能力。',
       '卡图0440；规则359.3.e.16的Hostile Takeover直接例子；当前控制及召回规则。',
       window='待命宏保留；法术先夺控并活跃，再按本回合尚未过去的结束阶段开始时点建立延迟能力',
       bindings='u:Unit=定稿选择的战场敌军实例，结算重检且离区不追踪新对象;link:Link=本法术该单位与该次控制修饰关联;ending_start_is_future:bool=本回合Ending阶段开始时点尚未过去；规则359.3.e.16已过时为False;ending_event:EventPattern=本回合TURN_PHASE的start，phase为Ending，保存当前回合身份;once:UsageLimit=count为1且reset为never;return_ability:Ability=完整延迟触发，controller为p，保存u及本次control_modifiers引用，执行下方两步',
       calls='''control = ops.change_control([u], p, duration=PERMANENT, link=link)
control_modifiers = control.value or []
ops.ready([u])
if ending_start_is_future:
    ops.on_event(ending_event, return_ability, duration=THIS_TURN, limit=once, link=link)
# return_ability结算体；以上取得的引用被保存在延迟能力参数中
ops.end_modifier(control_modifiers, link=link)
ops.recall([u])''')
record(453,'verify','首部Energy1与Fury1是触发基础费用；法术击杀归属、自身死后在废牌触发已核。后续打出费用政策仍需权威依据。',
       '卡图0453；规则383.2.c.1、383.3.b、404.1.b.1、429.5；Vendetta FAQ。',
       bindings='cost:Cost=Energy1及Fury1;binding:CostBinding=首部触发基础费用，在触发定稿支付;dest:Location=合法打出地点;permit:PlayPermission=该次法术击杀触发准许从己废牌打出me;policy:CostPolicy=尚待权威依据绑定的后续打出政策，当前不得执行此候选程序',
       calls='''# 固有ASSAULT 2按闭集宏保留
# 触发定稿阶段（费用阶段已查实）
paid = ops.pay(p, cost, binding=binding)
# 下方play仅为待核候选；不能省略cost_policy后默认为NORMAL_COST
if paid.value is not None:
    ops.play(me, p, origin=p.trash, destination=dest, cost_policy=policy, permission=permit)''',
       pending='VERIFY:触发基础费与随后打出印刷费的联系未充分核实；不默认替代费，也不重复收费；policy未核，程序不准执行。')
record(504,'confirmed','施法者选战场敌军，拥有者在结算时选择并执行一次牌堆顶／底放置；不是回收或两次动作。',
       '卡图0504；全部本地语言版本；区域及选择通则。',
       bindings='u:Unit=定稿选择且结算仍合法的战场敌军;origin:Zone=u当前场上区域',
       calls='''position_result = ops.declare(u.owner, ["top", "bottom"], kind="value", bind_at="resolution")
if position_result.value:
    ops.transfer([u], origin, u.owner.main_deck, actor=u.owner, position=position_result.value[0])''')
record(541,'verify','普通look→可选指定draw→指定余牌入废及Flow明确；draw被替代时rest的排除依据与BURN授权边界未找到专门裁定。',
       '卡图0541；规则359.3.e.14、441及Flow；未将普通对局说明当特殊交互裁定。',
       pending='VERIFY:rest是所选之外还是实际完成抽取之外，及抽取被替代后指定余牌燃烧的授权仍待核；旧草稿不计正确。')
record(656,'confirmed','在每名玩家自己的第1／2回合，把其因HOLD／CONQUER将获得的1分替换为该玩家抽1；保留征服据守及Scored流程。',
       '卡图0656；规则470–473；增分与战场得分过程不同。',
       bindings='point_events:EventPattern=GAIN_POINTS.before，amount为1，cause为HOLD或CONQUER，受益玩家此刻为自己的第1或第2回合；不只匹配p;score_player:Player=当前匹配增分事件的player;rewrite:EventRewrite=resume_original False，replacement为下方draw，before及after为空',
       calls='''ops.replace_event(point_events, rewrite, duration=WHILE_SOURCE_PRESENT)
# rewrite.replacement执行体，在匹配的增分提交前执行
ops.draw(score_player, 1)''')
record(836,'confirmed','规则187.11与卡图确认0战力；进攻触发的放逐是结算效果，不是发动费用。实际放逐后才本回合获强攻4。',
       '卡图0836右上0；规则187.11、204–205、383.3及实际动作结果。',
       window='进攻事件产生可选触发；定稿选择是否执行及所选废牌单位，结算时放逐，成功后强攻4；无放逐基础费用',
       bindings='u:Card=定稿选择的p废牌堆单位，结算时重检区域与类型；不是费用对象;params:KeywordParameters=Assault4；本卡模板might为0，依据规则187.11及实卡图，源目录null保持不改',
       calls='''# 仅在接受该可选进攻触发后进入其结算体
banished = ops.banish([u], actor=p)
if banished.value:
    ops.grant_keyword([me], ASSAULT, parameters=params, duration=THIS_TURN)''')
record(922,'confirmed','撤销强制加入原移动批次。按移动后触发及触发信息保存通则，跟随原事件目的地，执行普通移动。此结论为通则推导。',
       '卡图0922；官方赛事规则以本卡为移动触发例子；核心规则383.2.c、359.3.f.3、448–455。',
       window='友军从自身位置移动的事件后产生可选触发；该触发结算时再移动me，保留原事件目的地',
       bindings='dest:Location=从触发条件对应移动事件中取得并保存的目的地，不取友军后续最新位置;accept:bool=按可选触发流程接受本能力；不产生普通移动横置费用',
       calls='''if accept:
    ops.move([me], dest)''')
record(1025,'confirmed','战场能力指定打出者作选择，该玩家控制本触发；旧p与actor可能不同的绑定撤销。付Energy1定稿，结算给予实际新增益。',
       '卡图1025；规则190.6.c；Unleashed FAQ的Control of Battlefield Abilities。',
       window='在此处打出单位，Ability.controller明确绑定该次打出的玩家；其可选付Energy1定稿，结算buff该单位',
       bindings='u:Selection[Unit]=该次在此处打出且仍可被指令操作的单位引用;cost:Cost=Energy1;binding:CostBinding=当前能力控制者p的可选触发基础费用，在定稿支付',
       calls='''paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.buff(u)''')

assert len(rows)==12 and sum(r['verdict']=='confirmed' for r in rows)==7
(ROOT/'tmp/card-api-rulings-v2.1.jsonl').write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8')
by={r['number']:r for r in rows}
for path in sorted((D/'card-operator-reading').glob('*.md')):
    original=path.read_text(encoding='utf-8')
    originals=re.findall(r'~~~text\n(.*?)\n~~~',original,re.S)
    text=original.replace('[V2 API](../basic-operators-api.md)','[V2 API存档](../basic-operators-api-v2.md)')
    chunks=re.split(r'(?=<a id="card-\d+">)',text)
    for i,ch in enumerate(chunks):
        m=re.match(r'<a id="card-(\d+)">',ch)
        if not m or int(m[1]) not in by:continue
        r=by[int(m[1])]
        ch=re.sub(r'\n<!-- RULES-REVIEW-START -->.*?<!-- RULES-REVIEW-END -->\n','\n',ch,flags=re.S)
        ch=ch.replace('### 第二轮：72算子API分解','### 第二轮历史：72算子API分解')
        lines=['<!-- RULES-REVIEW-START -->','### 当前专项核验：V2.1真实效果与分解\n',
               '- 日期：2026-10-28；本次只复核原12张问题卡，不是新一轮全库阅读。',
               '- 本卡当前判定：**'+('专项人工语义确认' if r['verdict']=='confirmed' else '语义待核，不计通过；调用仅作候选草稿')+'**。',
               '- 核验结论：'+r['conclusion'],'- 规则依据：'+r['basis'],
               '- 能力入口：'+r['window'],
               '- 公共绑定：p为当前能力控制者，me为本实例，here为按规则绑定地点；不同注释标出的阶段／程序是独立入口，不能顺序执行整块。所有未决参数未绑定前禁止执行候选程序。',
               '\n参数绑定：\n','| 名称 | 类型 | 精确含义 |','| --- | --- | --- |']
        for binding in r['bindings'].split(';'):
            if not binding.strip():continue
            left,meaning=binding.split('=',1);name,typ=left.split(':',1)
            lines.append(f'| `{name.strip()}` | `{typ}` | {meaning.replace("|","&#124;")} |')
        lines+=['\nAPI调用：\n','```python',r['calls'],'```']
        if r['gaps']:lines+=['\n未决项：\n']+['- '+g for g in r['gaps']]
        lines+=['\n[真实功能、裁定依据与修订理由](../card-effect-rulings-review.md) · [当前73函数API](../basic-operators-api.md)。下方第二轮段落是历史判定，以本段为当前结论。',
                '<!-- RULES-REVIEW-END -->\n']
        pos=ch.index('<!-- API-REVIEW-START -->')
        chunks[i]=ch[:pos]+'\n'.join(lines)+'\n'+ch[pos:]
    text=''.join(chunks)
    assert originals==re.findall(r'~~~text\n(.*?)\n~~~',text,re.S),path
    if text!=original:path.write_text(text,encoding='utf-8')

report=D/'card-api-coverage.md'
text=report.read_text(encoding='utf-8')
text=text.replace('# 第二轮：72算子API全库阅读评估','# 第二轮全库结果与V2.1专项核验',1)
text=text.replace('[V2 API](basic-operators-api.md)','[V2 API存档](basic-operators-api-v2.md)',1)
insert=['## 当前专项核验：先查真实功能，再修订API\n',
        '2026-10-28，原12张问题卡已重读全部目录文本／勘误并逐张查看一张普通英文卡图；检索官方核心规则、勘误及FAQ。详细依据见[专项文档](card-effect-rulings-review.md)，当前[API V2.1](basic-operators-api.md)为73个正式函数。\n',
        '| 项目 | 本次结果 |','| --- | ---: |','| 本次核验 | 12张 |','| 专项人工语义确认 | 7张 |','| 仍待规则核验 | 5张 |','| 本次已确认而尚缺API的效果 | 0张 |',
        '\n待核为0201曼舞手雷、0286沙漠皇帝、0338嚼火者手雷、0453不朽凤凰、0541奥义！雷铠。没有足够规则依据的费用／计数／剩余集合不因API可接参数而计通过。\n',
        '原六张未覆盖项中，普朗克、恶意收购、持卫的裁决、章獭按已核效果补足契约；隐秘追踪者取消强制join，偶像谷修正能力控制者。影分身依据规则187.11及卡图确认零战力，并把错误的放逐成本改为结算效果。\n',
        '**范围限制：这是12张专项修订，未重新完整阅读其余1094张。下方1106张指标属于原V2第二轮，不是73函数V2.1的新全库覆盖率或正确率。** [原报告独立存档](operator-audits/round-2-coverage.md)。\n',
        '## 以下为原V2第二轮历史结果\n']
pos=text.index('状态：完整阅读已完成')
text=text[:pos]+'\n'.join(insert)+'\n'+text[pos:]
report.write_text(text,encoding='utf-8')

index=D/'card-operator-reading.md'
text=index.read_text(encoding='utf-8')
notice='\n当前补充：[12张真实效果专项核验](card-effect-rulings-review.md)已写回对应笔记；[API V2.1](basic-operators-api.md)共73函数。专项确认7张、仍待核5张；不代表第三轮全库阅读。\n'
pos=text.index('\n');text=text[:pos]+notice+text[pos:]
index.write_text(text,encoding='utf-8')

for name in ['card-api-changes-v2.md','operator-audits/round-2-validation.md']:
    p=D/name;text=p.read_text(encoding='utf-8')
    text=text.replace('](basic-operators-api.md)','](basic-operators-api-v2.md)').replace('](../basic-operators-api.md)','](../basic-operators-api-v2.md)')
    p.write_text(text,encoding='utf-8')

overlap=D/'card-api-overlap.md'
text=overlap.read_text(encoding='utf-8')
text=text.replace('检查对象：[V2的72个API](basic-operators-api.md)。','当前：[V2.1的73个API](basic-operators-api.md)；下列为V2全库冗余检查及本次增量补充。')
text+='''\n## V2.1专项修订后的增量检查\n
按[12张真实功能核验](card-effect-rulings-review.md)，新增end_modifier，72→73函数；transfer增加position，补STUN／MIGHT_CHANGE／GAIN_POINTS事件，没有增加卡牌专用算子。

- end_modifier只结束取得的修饰引用；change_control建立新控制修饰，两者不等价。
- transfer(position=...)是跨区域时直接放到指定端；reorder调整既有区域内所选集合的次序，保留独立用途。
- on_event是在事件后创建能力，replace_event在事件提交前替代；隐秘追踪者不能为了“随之”而强制使用join。
- 影分身的banish是效果，pay是支付费用；将前者误写为后者属于语义错误，不是可合并接口。

本次没有确认新的完全同义函数；未重做其余1094张的完整语义阅读，不能将增量结果描述为V2.1全库等价性认证。
'''
overlap.write_text(text,encoding='utf-8')
print(json.dumps({'reviewed':len(rows),'confirmed':7,'verify':5,'api_functions':73,'api_sha256':api_hash,'notes_original_text_preserved':True},ensure_ascii=False))
