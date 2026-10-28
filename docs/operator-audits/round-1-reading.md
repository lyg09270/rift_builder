# 第一轮逐卡API分解存档


对应[69算子V1](../basic-operators-api-v1.md)。本页保存第二轮改写前的全部逐卡调用与判定。


<a id="card-0001"></a>

## 0001

法术结算；固有反应

spell:ChainItem=所选法术

```python

ops.counter(spell, destination=spell.owner.hand)
ops.predict(p)

```



<a id="card-0002"></a>

## 0002

任一玩家打出法术后，可选效果

actor:Player=打出法术的玩家;u:Unit=actor在此处控制的所选单位

```python

ops.modify_might([u], 1, duration=THIS_TURN)

```



<a id="card-0003"></a>

## 0003

法术结算

targets:Selection[Permanent]=所选单位和装备部分，不含符文；三类原要求合计至多4

```python

ops.ready(targets)

```

RUNE_READY:原效果也可选择符文，但ready只接受Permanent，Rune不属于该类型



<a id="card-0004"></a>

## 0004

法术结算，固有迅捷

players:Selection[Player]=所有玩家;chosen:dict[Player,Selection[Gear]]=每玩家自行选择的己方一件装备，无则空

```python

for actor in players:
    ops.kill(chosen[actor])

```

BATCH:各玩家装备应同批处理，逐个kill的清理和触发边界不等价

ACTOR:卡面指定其他玩家执行摧毁或移动，但对应kill/move无执行玩家参数；不能以选择权正确冒充动作归属正确



<a id="card-0005"></a>

## 0005

自身征服后，可选摧毁任意装备，实际如此做才增益

g:Gear=所选装备，不限己方

```python

r = ops.kill([g])
if r.changed:
    ops.buff([me])

```



<a id="card-0006"></a>

## 0006

参与过的战斗结束且本回合未曾受伤；历史条件

 

```python

ops.draw(p, 1)

```



<a id="card-0007"></a>

## 0007

法术结算；反应

u:Unit=友方战场单位;n:IntExpr=该单位地点敌军数

```python

ops.modify_might([u], 2 * n, duration=THIS_TURN)

```



<a id="card-0008"></a>

## 0008

每回合一次，从盖放打出牌后抽1，之后非己回合则弃1

off_turn:bool=抽牌后判断当前非p回合

```python

ops.draw(p, 1)
if off_turn:
    ops.discard(p, 1)

```



<a id="card-0009"></a>

## 0009

自身据守后

 

```python

ops.gain_points(p, 1)

```



<a id="card-0010"></a>

## 0010

自身有缴械；你使此处敌军实际降低≥1战力后

 

```python

ops.modify_might([me], 1, duration=THIS_TURN)

```



<a id="card-0011"></a>

## 0011

自身进攻/防守后

u:Unit=此处所选敌军

```python

ops.modify_might([u], -2, duration=THIS_TURN, floor=1)

```

LANG:TC普通版为你进攻防守且缺此处，另版与EN/SC不同



<a id="card-0012"></a>

## 0012

每回合第1次移动产费；第2次放逐顶牌并授权

first:bool=本回合该实例第1次移动;second:bool=第2次;top:Card=己主牌堆顶;bundle:ResourceBundle=Energy1和通用Power1;permit:PermissionSpec=仅允许p正常付费从放逐区打出本次top;expiry:Duration=直到p的下个结束阶段

```python

if first:
    ops.add_resources(p, bundle)
if second:
    ops.banish([top])
    ops.grant_permission(top, permit, duration=expiry)

```



<a id="card-0013"></a>

## 0013

强化主动；移动后可选伤害；强化时持续+1，三个独立能力入口

cost:Cost=Energy2/Fury1;binding:CostBinding=未强化才可发动的主动基础费用;u:Unit=移动起点或终点战场所选单位;e:bool=伤害结算时自身强化;dur:Duration=留场且强化期间

```python

# 强化主动入口
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 移动触发入口
ops.damage([u], 2 if e else 1)
# 持续能力入口
ops.modify_might([me], 1, duration=dur)

```



<a id="card-0014"></a>

## 0014

非战斗时不能被敌方选择；移到战场后+2

restriction:RestrictionSpec=敌方法术/能力不得选本实例为目标;dur:Duration=留场且非战斗期间

```python

# 持续入口
ops.restrict_action(me, restriction, duration=dur)
# 移入战场触发入口
ops.modify_might([me], 2, duration=THIS_TURN)

```



<a id="card-0015"></a>

## 0015

百炼；打出可选额外Body2；仅付后打出触发偷敌装

cost:Cost=Body2;binding:CostBinding=可选打出额外费用;paid_extra:bool=该次额外费用已付;g:Gear=选中敌方装备;dur:Duration=该me离场为止;is_equipment:bool=g有Equipment标签

```python

# 打出费用入口
ops.pay(p, cost, binding=binding)
# 已支付额外费用的打出触发入口
if paid_extra:
    ops.move([g], p.base)
    ops.change_control([g], p, duration=dur)
    if is_equipment:
        ops.attach(g, me)

```



<a id="card-0016"></a>

## 0016

打出触发；消耗任选己方增益，每个分别召符文

plan:dict[Unit,int]=任选己军及各自计划消耗数量，可含李青多层；不强制每单位相同;spent_total:int=所有spend_buff实际回执中的合计，在后续循环入口绑定

```python

for unit, count in plan.items():
    ops.spend_buff(p, [unit], count_each=count)
for i in range(spent_total):
    ops.channel(p, 1, exhausted=True)

```

BATCH:各单位不同消耗数量只能分次调用，尚无同一原始spend-any批次的定义；后续channel已按每个实际消耗分别调用，不再把它合为一次channel(N)



<a id="card-0017"></a>

## 0017

自身固有法盾；在战场时持续给其他此处己军法盾

others:Selection[Unit]=持续求值，此处其他己军;dur:Duration=me留场且在战场期间

```python

ops.grant_keyword(others, DEFLECT, duration=dur)

```



<a id="card-0018"></a>

## 0018

迅捷法术；所选友军为伤害源；每个因此死亡创建自反XP项

u:Unit=选中友军;targets:Selection[Unit]=战场敌军;m:IntExpr=u当前战力;allocation:dict[Unit,int]=合计m的合法分配

```python

ops.damage(targets, m, source=u, mode="split", allocation=allocation)

```

REFLEXIVE:缺按实际死亡逐一创建gain_xp(1)待处理链项的API



<a id="card-0019"></a>

## 0019

固有壁垒；持续保护此处低战力己军

allies:PermissionSelection=动态的此处战力低于me己军;restriction:RestrictionSpec=禁止敌方法术/能力将其选为目标

```python

ops.restrict_action(allies, restriction, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0020"></a>

## 0020

战斗中此处单位将死，其控制者可付任意Power3改治疗横置召回

u:Unit=将死亡单位;actor:Player=u控制者;cost:Cost=任意领域Power3;binding:CostBinding=选择死亡替代时指令内支付

```python

ops.pay(actor, cost, binding=binding)

```

REPLACE:没有死亡前替代登记API，不能以死后heal/exhaust/recall冒充



<a id="card-0021"></a>

## 0021

友军死亡后可横置me作触发基础费用，抽1后手牌放顶/底

cost:Cost=横置me;binding:CostBinding=可选触发基础费用;c:Card=抽牌后所选手牌;position:str=玩家选定top或bottom

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.draw(p, 1)
    ops.transfer([c], p.hand, p.main_deck)
    ops.reorder([c], p.main_deck, position=position, policy="preserve")

```



<a id="card-0022"></a>

## 0022

控制者据守此处后

recruit:TokenTemplate=完整1战力Recruit模板

```python

ops.play(recruit, p, origin=None, destination=p.base)

```



<a id="card-0023"></a>

## 0023

打出触发；炸弹能力在模板里，不归本单位

bomb:TokenTemplate=完整Bomb装备模板，含部署及死亡打2/杀其他炸弹;b:Battlefield=合法所选战场

```python

ops.play(bomb, p, origin=None, destination=b)

```



<a id="card-0024"></a>

## 0024

据守此处后可选

u:Unit=任意战场所选单位;base:Location=u对应基地

```python

ops.move([u], base)

```



<a id="card-0025"></a>

## 0025

强化主动Energy1/Order2；强化持续强攻2；强化进攻触发杀敌

cost:Cost=Energy1/Order2;binding:CostBinding=未强化时主动基础费用;params:KeywordParameters=Assault.value为2;dur:Duration=me留场且强化;u:Unit=此处战力严格低于me所选敌军

```python

# 强化主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 强化持续能力
ops.grant_keyword([me], ASSAULT, parameters=params, duration=dur)
# 强化进攻触发
ops.kill([u])

```



<a id="card-0026"></a>

## 0026

强化主动Energy3/Body1；强化+3，非战斗不能受伤

cost:Cost=Energy3/Body1;binding:CostBinding=未强化时主动基础费用;dur:Duration=留场且强化;safe:Duration=留场且强化且非战斗;restriction:RestrictionSpec=本单位不能受伤，非禁止选择

```python

# 强化主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 持续能力
ops.modify_might([me], 3, duration=dur)
ops.restrict_action(me, restriction, duration=safe)

```



<a id="card-0027"></a>

## 0027

迅捷法术；摧毁后原装备控制者打休眠金币

g:Gear=所选装备;actor:Player=g控制者死亡前快照;gold:TokenTemplate=完整金币模板;entry:EntryState=休眠入场

```python

ops.kill([g])
ops.play(gold, actor, origin=None, destination=actor.base, entry=entry)

```



<a id="card-0028"></a>

## 0028

反应产费主动，横置成本；结算付任意Energy换等量通用Power

cost:Cost=横置me;binding:CostBinding=主动基础费用;energy_cost:Cost=玩家选定数量Energy;inner:CostBinding=结算时指令内费用;bundle:ResourceBundle=实际支付Energy同量的通用Power

```python

base_paid = ops.pay(p, cost, binding=binding)
if base_paid.value is not None:
    paid = ops.pay(p, energy_cost, binding=inner)
    if paid.value is not None:
        ops.add_resources(p, bundle)

```



<a id="card-0029"></a>

## 0029

固有急速；强攻值动态等于此处敌军数

n:IntExpr=持续统计此处敌军数量

```python

ops.modify_keyword([me], ASSAULT, parameter="value", operation="set", value=n, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0030"></a>

## 0030

反应法术；同控制者单位和武装，贴附或从该单位卸除，抽1

u:Unit=选中单位;g:Gear=与u同控制者的所选武装;mode:bool=选贴附，否则卸除；卸除要求g已贴u

```python

if mode:
    ops.attach(g, u)
else:
    ops.detach([g])
ops.draw(p, 1)

```



<a id="card-0031"></a>

## 0031

打出触发；所有战力≤2单位同时回各拥有者手牌

u:Unit=全体合格单位中的一个，以下仅局部片段;origin:Zone=u的场上区域

```python

ops.transfer([u], origin, u.owner.hand)

```

BATCH:transfer只有共同source/destination，无法保证多地点多拥有者同时转移，逐次循环不等价



<a id="card-0032"></a>

## 0032

法盾；主动横置，选对手，该对手选己军移到me战场

cost:Cost=横置me;binding:CostBinding=主动基础费用;actor:Player=己方所选对手;candidates:Selection[Unit]=actor控制单位;location:Location=me战场

```python

base_paid = ops.pay(p, cost, binding=binding)
if base_paid.value is not None:
    chosen = ops.choose(actor, candidates, targeting=False, bind_at="resolution")
    ops.move(chosen.value, location)

```

ACTOR:卡面指定其他玩家执行摧毁或移动，但对应kill/move无执行玩家参数；不能以选择权正确冒充动作归属正确



<a id="card-0033"></a>

## 0033

自身进攻触发

enemies:Selection[Unit]=此处所有敌军

```python

ops.damage(enemies, 3)

```



<a id="card-0034"></a>

## 0034

留场期间持续

events:DamageSelection=p控制的法术/技能伤害

```python

ops.modify_damage(events, NumericChange(add=1), duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0035"></a>

## 0035

打出触发

c:Card=己方废牌堆所选法术

```python

ops.transfer([c], p.trash, p.hand)

```



<a id="card-0036"></a>

## 0036

活跃入场；打出后此处打活跃3战力Mech

dest:Location=me合法打出目的地;ready_entry:EntryState=活跃入场;mech:TokenTemplate=完整3战力Mech模板

```python

# 基础打出入口
ops.play(me, p, origin=p.hand, destination=dest, entry=ready_entry)
# 打出触发入口
ops.play(mech, p, origin=None, destination=here, entry=ready_entry)

```



<a id="card-0037"></a>

## 0037

给me贴武装后，从本回合未选模式中选一；各效果独立

mode:int=本回合未选模式，0活跃/1召出/2增益;runes:Selection[Rune]=所选2符文;u:Unit=所选友方单位

```python

if mode == 0:
    pass  # Rune不符合ready的Permanent参数类型
elif mode == 1:
    ops.channel(p, 1, exhausted=True)
else:
    ops.buff([u])

```

RUNE_READY:规则133.5.a.1/161.1.a明确Rune不是Permanent，ready签名不能接受该符文集合



<a id="card-0038"></a>

## 0038

强化Energy3；强化时己方法术Energy和任意Power各减1，Energy最低1

cost:Cost=Energy3;binding:CostBinding=未强化主动基础费用;spells:CostSelection=p的法术;change:CostChange=Energy减1且最低1，任意Power需求减1;dur:Duration=me留场且强化

```python

# 强化入口
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 持续入口
ops.modify_cost(spells, change, duration=dur)

```



<a id="card-0039"></a>

## 0039

强化Energy2；实际变为强化触发洞察2；强化持续+1

cost:Cost=Energy2;binding:CostBinding=未强化主动基础费用;dur:Duration=me留场且强化

```python

# 强化入口
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 成功强化触发入口
ops.predict(p, 2)
# 持续入口
ops.modify_might([me], 1, duration=dur)

```



<a id="card-0040"></a>

## 0040

移动后展示主牌堆顶，是装备抽取，否则回收

top:Card=己方主牌堆顶;is_gear:bool=top包含gear类型

```python

ops.reveal([top])
if is_gear:
    ops.draw(p, 1, cards=[top])
else:
    ops.recycle([top])

```



<a id="card-0041"></a>

## 0041

固有狩猎2；自身及其他友方单位可打到敌军落单的已占战场

cards:PermissionSelection=持续的友方单位；含自己在可打出区域;permit:PermissionSpec=额外合法目的地为仅有一名敌军的已占战场；不授反应;self_duration:Duration=自身该权限在非场上可打出区域生效;others:PermissionSelection=其他友方单位

```python

ops.grant_permission(me, permit, duration=self_duration)
ops.grant_permission(others, permit, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0042"></a>

## 0042

迅捷法术；放逐友方单位，由拥有者免费打出，再打战场敌军3，放逐自身

u:Unit=所选友方单位;owner:Player=u拥有者;dest:Location=owner所选合法打出地点;enemy:Unit=战场所选敌军

```python

ops.banish([u])
ops.play(u, owner, origin=owner.banishment, destination=dest, cost_policy=IGNORE_BASE_COST)
ops.damage([enemy], 3)
ops.banish([me])

```



<a id="card-0043"></a>

## 0043

主动横置，增益休眠友方单位

cost:Cost=横置me;binding:CostBinding=主动基础费用;u:Unit=所选休眠友方单位

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.buff([u])

```



<a id="card-0044"></a>

## 0044

活跃入场；主动横置让任意单位本回合+3

dest:Location=自身合法打出地点;entry:EntryState=活跃入场;cost:Cost=横置me;binding:CostBinding=主动基础费用;u:Unit=所选任意单位

```python

# 基础打出
ops.play(me, p, origin=p.hand, destination=dest, entry=entry)
# 主动入口
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_might([u], 3, duration=THIS_TURN)

```



<a id="card-0045"></a>

## 0045

法术；按己方武装数打沙兵，勘误后独立自反步骤活跃至多2个

n:int=己方武装数量;soldier:TokenTemplate=2战力沙兵;destinations:list[Location]=每个沙兵各自合法目的地

```python

for i in range(n):
    ops.play(soldier, p, origin=None, destination=destinations[i])

```

REFLEXIVE:then do this的后续活跃须新待处理项，play返回链项不是已落地单位，无调度/链项到新实例关联接口



<a id="card-0046"></a>

## 0046

固有关键词内部展开；不同注释为独立入口

dest:Location/Zone=本次合法打出位置;choices:ChoiceBinding=定稿选择是否支付急速附加费Energy1Fury1;subjects:CostSelection=本次打出me;extra:CostChange=该次所选急速附加费Energy1Fury1，不改印刷基础费;entry:EntryState=choices选择急速则ready否则默认，必须与完整费用支付一致;g:Gear=p控制武装;cost:Cost=g装配费用减任意Power1最低0;binding:CostBinding=可选百炼触发费用;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

# 急速内部费用与入场展开
ops.modify_cost(subjects, extra, duration=THIS_PLAY)
ops.play(me, p, origin=p.hand, destination=dest, choices=choices, entry=entry)
# 百炼打出触发
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(g, me)

```



<a id="card-0047"></a>

## 0047

固有坚守3壁垒；移动后可打任意战场单位，伤害等当前坚守值

u:Unit=所选战场单位;n:IntExpr=me当前坚守值，不是战力

```python

ops.damage([u], n)

```



<a id="card-0048"></a>

## 0048

打出后对手公开手牌，选其一放逐，其据守时返还，离场仍有效

actor:Player=所选对手;hand:Selection[Card]=其展示时的手牌快照;c:Card=从这些牌中选一;link:Link=本次放逐关联

```python

ops.reveal(hand)
ops.banish([c], link=link)

```

DELAY:缺少登记actor未来据守时transfer回手的一次触发接口

ACTOR:卡面指定对手执行reveal，但reveal只有viewers而没有行动玩家，不能把公开对象/观众正确当成执行者正确



<a id="card-0049"></a>

## 0049

持续胜利门槛+1；禁用不影响语义阅读

scope:RuleScope=该对局所有玩家;change:RuleChange=胜利分数增加1

```python

ops.modify_rule(VICTORY_THRESHOLD, scope, change, duration=WHILE_SOURCE_PRESENT)

```

DATA:EN异画规则为null，不能据该面认定白板；其他印刷可解释本体

DATA:同一本体有非空规则文本，但这些变体printedRulesText为空：EN OGN-276a



<a id="card-0050"></a>

## 0050

打出触发

c:Card=己方废牌堆所选装备

```python

ops.transfer([c], p.trash, p.hand)

```



<a id="card-0051"></a>

## 0051

主动Energy1/Fury1、回收己方废牌单位、横置me；打3战力Mech基地

cost:Cost=Energy1/Fury1及回收所选己方废牌单位及横置me;binding:CostBinding=完整主动基础费用;mech:TokenTemplate=3战力Mech

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.play(mech, p, origin=None, destination=p.base)

```



<a id="card-0052"></a>

## 0052

每回合打出首牌且me在战场时，勘误限定本回合下一牌折扣

next_card:CostSelection=该触发登记后下一张执行play动作的p卡牌;change:CostChange=Energy减2及任意Power需求减2

```python

ops.modify_cost(next_card, change, duration=THIS_TURN, uses=1)

```



<a id="card-0053"></a>

## 0053

固有游走；可杀友军作打出额外费按印刷费用折扣；进攻由防守者杀己军

cost:Cost=杀所选友军;binding:CostBinding=可选打出额外费;killed_cost:CostChange=按所杀友军的印刷Energy减少同量Energy，印刷Power减少同量Order;own_play:CostSelection=本次me打出费用;defender:Player=防守者;candidates:Selection[Unit]=defender在此处的单位

```python

# 打出费用入口
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_cost(own_play, killed_cost, duration=UNTIL_EFFECT_END, uses=1)
# 进攻触发入口
chosen = ops.choose(defender, candidates, targeting=False, bind_at="resolution")
ops.kill(chosen.value)

```

ACTOR:卡面指定其他玩家执行摧毁或移动，但对应kill/move无执行玩家参数；不能以选择权正确冒充动作归属正确



<a id="card-0054"></a>

## 0054

强化Energy3/Order1；强化时己方已强化单位+2，包含自己

cost:Cost=Energy3/Order1;binding:CostBinding=未强化主动基础费用;units:Selection[Unit]=动态的己方已强化单位，含me;dur:Duration=me留场且强化

```python

# 主动入口
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 持续入口
ops.modify_might(units, 2, duration=dur)

```



<a id="card-0055"></a>

## 0055

进攻可付Mind1，按勘误免费打手牌待命；仅单位打此处

cost:Cost=Mind1;binding:CostBinding=可选攻击触发基础费用;c:Card=手牌待命牌;dest:Location/Zone=单位打here，否则合法目的地;permit:PlayPermission=该攻击触发允许打出手牌卡及单位打here

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.play(c, p, origin=p.hand, destination=dest, cost_policy=IGNORE_BASE_COST, permission=permit)

```



<a id="card-0056"></a>

## 0056

法术结算

units:Selection[Unit]=全部玩家基地中的所有单位

```python

ops.damage(units, 3)

```



<a id="card-0057"></a>

## 0057

迅捷主动Calm1，每回合一次；交换原位置后可拿对方一武装

cost:Cost=Calm1;binding:CostBinding=每回合一次的迅捷主动基础费用;u:Unit=己方所选单位;old_me:Location=动作前me位置快照;old_u:Location=动作前u位置快照;take:bool=选择拿其武装;g:Gear=u的所选已贴附武装

```python

base_paid = ops.pay(p, cost, binding=binding)
if base_paid.value is not None:
    ops.move([me], old_u, origin=old_me)
    ops.move([u], old_me, origin=old_u)
    if take:
        ops.attach(g, me)

```



<a id="card-0058"></a>

## 0058

固有急速；进攻可选任意数量己方单位衍生物移入此战场

tokens:Selection[Unit]=任选己方单位衍生物

```python

ops.move(tokens, here)

```



<a id="card-0059"></a>

## 0059

武装+3为基础属性；装配Order1主动

cost:Cost=Order1;binding:CostBinding=装配主动基础费用;u:Unit=所选己方单位

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)

```



<a id="card-0060"></a>

## 0060

进攻可付Fury1获得本回合强攻2；非固有强攻

cost:Cost=Fury1;binding:CostBinding=可选攻击触发基础费用;params:KeywordParameters=Assault.value为2

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.grant_keyword([me], ASSAULT, parameters=params, duration=THIS_TURN)

```



<a id="card-0061"></a>

## 0061

强化Energy5，己符文≤4降3；强化期间法盾和强攻2

own_ability:CostSelection=该强化主动;discount:CostChange=Energy减3;few_runes:Duration=留场且p符文≤4;cost:Cost=应用折扣后的强化基础费用;binding:CostBinding=仅未强化主动;dur:Duration=me留场且强化;params:KeywordParameters=Assault.value为2

```python

# 费用修饰入口
ops.modify_cost(own_ability, discount, duration=few_runes)
# 主动入口
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 强化持续能力
ops.grant_keyword([me], DEFLECT, duration=dur)
ops.grant_keyword([me], ASSAULT, parameters=params, duration=dur)

```



<a id="card-0062"></a>

## 0062

强化Energy1/任意Power2；强化+2；以强化状态死亡才召2休眠符文

cost:Cost=Energy1/任意Power2;binding:CostBinding=仅未强化时主动;dur:Duration=留场且强化

```python

# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 持续
ops.modify_might([me], 2, duration=dur)
# 死亡前强化为真的绝念入口
ops.channel(p, 2, exhausted=True)

```

DATA:SC分隔标记损坏，EN及中文括号说明可支持解释但不改源文



<a id="card-0063"></a>

## 0063

固有待命/迅捷；眩晕，若从手牌打出再抽

u:Unit=所选单位;from_hand:bool=该次打出来源为手牌

```python

ops.stun([u])
if from_hand:
    ops.draw(p, 1)

```



<a id="card-0064"></a>

## 0064

反应法术；两名己军

units:Selection[Unit]=所选2名友方单位

```python

ops.modify_might(units, 2, duration=THIS_TURN)

```



<a id="card-0065"></a>

## 0065

单位从此处移出后

u:Unit=本次离开的单位，实例由移动事件绑定

```python

ops.modify_might([u], 1, duration=THIS_TURN)

```



<a id="card-0066"></a>

## 0066

主动Energy1/Order1横置，杀友军看5，按勘误放逐合格单位免费打出，余回收

cost:Cost=Energy1/Order1及横置me;binding:CostBinding=主动基础费用;u:Unit=要杀的友军;v:Card=顶5中可选单位，战力≤u死亡前战力+1;take:bool=选择打出;dest:Location=该单位正常合法目的地;rest:Selection[Card]=顶5中除本次选中v以外的牌，未选则全部

```python

base_paid = ops.pay(p, cost, binding=binding)
if base_paid.value is not None:
    ops.kill([u])
    ops.look(p, p.main_deck, 5)
    if take:
        ops.banish([v])
        ops.play(v, p, origin=p.banishment, destination=dest, cost_policy=IGNORE_BASE_COST)
    ops.recycle(rest)

```



<a id="card-0067"></a>

## 0067

在此处盖放后；不是打出待命牌事件

gold:TokenTemplate=完整金币装备模板;entry:EntryState=休眠

```python

ops.play(gold, p, origin=None, destination=p.base, entry=entry)

```



<a id="card-0068"></a>

## 0068

等级3时活跃入场

dest:Location=合法打出目的地;entry:EntryState=定稿时若pXP≥3则活跃，否则默认朝向

```python

ops.play(me, p, origin=p.hand, destination=dest, entry=entry)

```



<a id="card-0069"></a>

## 0069

控制者可此处额外盖放1张

scope:RuleScope=此战场盖放容量，适用有权盖放玩家;change:RuleChange=容量增加1

```python

ops.modify_rule(HIDDEN_CAPACITY, scope, change, duration=WHILE_SOURCE_PRESENT)

```

DATA:EN异画null规则；其他印刷有能力

DATA:同一本体有非空规则文本，但这些变体printedRulesText为空：EN OGN-278a



<a id="card-0070"></a>

## 0070

固有部署；此处友军持续强攻1

units:Selection[Unit]=此处动态友方单位

```python

ops.grant_keyword(units, ASSAULT, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0071"></a>

## 0071

打出可横置己传奇作额外费；已付后可移任意己军到一个开放战场

cost:Cost=横置己方传奇;binding:CostBinding=本次可选打出额外费用;paid_extra:bool=该费用已支付;units:Selection[Unit]=任选己军;b:Battlefield=所选open战场，不泛化为uncontrolled

```python

# 打出费用入口
ops.pay(p, cost, binding=binding)
# 打出触发入口
if paid_extra:
    ops.move(units, b)

```



<a id="card-0072"></a>

## 0072

定稿时若无男爵巢穴则添战场且自己在那里进场；持续保护自身和其他友方单位+2

restriction:RestrictionSpec=敌方法术/技能不得选me;others:Selection[Unit]=动态其他友方单位

```python

# 两项可表达的持续能力
ops.restrict_action(me, restriction, duration=WHILE_SOURCE_PRESENT)
ops.modify_might(others, 2, duration=WHILE_SOURCE_PRESENT)

```

CREATE_NEUTRAL:create要求controller为Player，新增战场应无人控制，不能传None

AS_PLAY:无定稿中先创建战场再按是否创建改变入场目的地的明确阶段钩子



<a id="card-0073"></a>

## 0073

单位可从任意场上地点移此处；不能开局携带衍生战场

units:PermissionSelection=全体单位;permit:PermissionSpec=允许标准移动从任意场上地点到me，不授免费横置;scope:RuleScope=本战场开局资格;change:RuleChange=禁止作为开局战场

```python

ops.grant_permission(units, permit, duration=WHILE_SOURCE_PRESENT)
ops.modify_rule(STARTING_BATTLEFIELD_ELIGIBILITY, scope, change, duration=PERMANENT)

```



<a id="card-0074"></a>

## 0074

传奇主动Energy4横置，每个友方瞬息单位减Energy1；打活跃瞬息3战力Sprite

ability:CostSelection=本主动费用;discount:CostChange=Energy减少动态友方瞬息单位数;cost:Cost=修改后Energy费用及横置me;binding:CostBinding=主动基础费用;sprite:TokenTemplate=3战力Sprite且有Temporary;entry:EntryState=活跃;dest:Location=正常所选合法地点

```python

# 费用修饰
ops.modify_cost(ability, discount, duration=PERMANENT)
# 主动结算
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.play(sprite, p, origin=None, destination=dest, entry=entry)

```



<a id="card-0075"></a>

## 0075

自身在可打出区域的持续降费，按本回合已定稿牌数，Energy最低1

subject:CostSelection=me打出费用;change:CostChange=Energy减该回合p已定稿牌数，Energy最低1;dur:Duration=该牌费用能力有效期间

```python

ops.modify_cost(subject, change, duration=dur)

```



<a id="card-0076"></a>

## 0076

回收符文后可横置传奇产休眠金币；一或多敌军死亡时活跃传奇

cost:Cost=横置me;binding:CostBinding=回收符文的可选触发基础费用;gold:TokenTemplate=金币;entry:EntryState=休眠

```python

# 回收符文触发入口
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.play(gold, p, origin=None, destination=p.base, entry=entry)

```

LEGEND_READY:ready只收Permanent，me为Legend；规则175明确传奇不是永久物，不能调用ready([me])



<a id="card-0077"></a>

## 0077

反应法术，定稿可亮出装备；结算给单位+2，若亮出则活跃至多2符文

requirement:ShowOffRequirement=手牌一件装备或场上一件友方装备;link:Link=本亮出与后续判断关联;u:Unit=所选单位;showed:bool=该关联亮出成功;runes:Selection[Rune]=选择至多2符文

```python

# 定稿亮出入口
ops.show_off(p, requirement, link=link)
# 法术结算入口
ops.modify_might([u], 2, duration=THIS_TURN)
if showed:
    pass  # Rune不符合ready的Permanent参数类型

```

RUNE_READY:规则133.5.a.1/161.1.a明确Rune不是Permanent，ready签名不能接受该符文集合



<a id="card-0078"></a>

## 0078

战场友装死亡后，可付Energy1将同一牌从废牌回拥有者手牌

cost:Cost=Energy1;binding:CostBinding=可选死亡触发基础费用;g:Card=本次死亡装备，保存拥有者

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.transfer([g], g.owner.trash, g.owner.hand)

```



<a id="card-0079"></a>

## 0079

打出后另一友方单位和敌军同时回各拥有者手牌

u:Unit=另一友方单位;v:Unit=所选敌军;origin_u:Zone=u场上区域;origin_v:Zone=v场上区域

```python

# 仅展示各单对象可表达的片段，不能当成同批转移
ops.transfer([u], origin_u, u.owner.hand)
ops.transfer([v], origin_v, v.owner.hand)

```

BATCH:不同来源和不同拥有者目的地的同时回手缺少批次API



<a id="card-0080"></a>

## 0080

固有待命；打出选战场，该处≥4单位可回一敌军手牌

b:Battlefield=选定战场;enough:bool=其单位总数≥4;take:bool=选择回手;u:Unit=该处敌军;origin:Zone=u场上区域

```python

if enough and take:
    ops.transfer([u], origin, u.owner.hand)

```



<a id="card-0081"></a>

## 0081

迅捷法术，回响Energy1/Mind1；每个效果对同地至多3单位各打1

units:Selection[Unit]=同一地点至多3所选单位

```python

ops.damage(units, 1)

```

REPEAT:当前仅覆盖一遍效果；无按定稿时各遍选择/模式执行回响的明确调度API，不用即时for循环冒充



<a id="card-0082"></a>

## 0082

打出触发

actor:Player=所选任意玩家

```python

ops.discard(actor, 1)

```



<a id="card-0083"></a>

## 0083

拥有增益期间有游走

dur:Duration=me留场且有增益期间

```python

ops.grant_keyword([me], GANKING, duration=dur)

```



<a id="card-0084"></a>

## 0084

打出触发

units:Selection[Unit]=至多2所选任意单位

```python

ops.damage(units, 1)

```



<a id="card-0085"></a>

## 0085

固有法盾1：对手以法术或技能选择本实例时附加任意Power1

subjects:CostSelection=对手法术/技能为选择me须付的目标附加费用，同一能力选择me不重复收取;change:CostChange=额外任意Power1

```python

ops.modify_cost(subjects, change, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0086"></a>

## 0086

此处所有有瞬息单位持续坚守1，不分玩家

units:Selection[Unit]=动态此处拥有Temporary的所有单位

```python

ops.grant_keyword(units, SHIELD, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0087"></a>

## 0087

每玩家自己回合一次均可发动，即使不控制战场；任意Power2抽1

actor:Player=当前发动玩家，必须在其回合且该玩家该回合尚未用;cost:Cost=任意Power2;binding:CostBinding=该玩家主动基础费用

```python

paid = ops.pay(actor, cost, binding=binding)
if paid.value is not None:
    ops.draw(actor, 1)

```



<a id="card-0088"></a>

## 0088

从盖放打出牌后

gold:TokenTemplate=金币模板;entry:EntryState=休眠

```python

ops.play(gold, p, origin=None, destination=p.base, entry=entry)

```



<a id="card-0089"></a>

## 0089

固有强攻1；绝念

 

```python

ops.channel(p, 1, exhausted=True)

```



<a id="card-0090"></a>

## 0090

对每位玩家分别计数，每回合其首个非衍生物在此处死亡后

actor:Player=该死亡单位控制者快照;recruit:TokenTemplate=1战力Recruit

```python

ops.play(recruit, actor, origin=None, destination=actor.base)

```



<a id="card-0091"></a>

## 0091

己军被你选为目标可横置传奇付任意Power1活跃该军；征服可Energy1活跃传奇

cost:Cost=横置me及任意Power1;binding:CostBinding=可选被选择触发基础费用;u:Unit=本次被选目标友军

```python

# 被选择触发入口
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.ready([u])

```

LEGEND_READY:征服后的活跃me要求Legend目标，ready签名只接受Permanent



<a id="card-0092"></a>

## 0092

武装+3；装配任意Power1或横置友军；效果区给宿主游走

cost:Cost=已选的任意Power1或横置一名合法友方单位；不同时付两者;binding:CostBinding=装配主动基础费用;u:Unit=所选p控制单位宿主;host:Selection[Unit]=当前贴附宿主;dur:Duration=本装备贴附该宿主期间

```python

# 装配入口
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 效果区持续入口
ops.grant_keyword(host, GANKING, duration=dur)

```

DATA:SC缺printedEffectText，不能确认该中文面含宿主游走；EN有明确文本



<a id="card-0093"></a>

## 0093

武装+4；装配Order1并杀友军

cost:Cost=Order1及杀所选友军;binding:CostBinding=装配主动基础费用;u:Unit=所选p控制单位宿主

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)

```



<a id="card-0094"></a>

## 0094

每回合自身首移触发

actor:Player=所选任意玩家

```python

ops.burn(actor, 1)

```



<a id="card-0095"></a>

## 0095

打出可移动敌军；每次你移动敌军可横置装备晕同一个

u:Unit=打出后所选敌军;dest:Location=其合法移动目的地;cost:Cost=横置me;binding:CostBinding=移动敌军后可选触发基础费用;v:Unit=该移动事件的敌军

```python

# 打出触发入口
ops.move([u], dest)
# 你移动敌军触发入口，不限由自身打出造成
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.stun([v])

```



<a id="card-0096"></a>

## 0096

打出可额外Energy1/Fury1；已付后打出触发打2战场单位

cost:Cost=Energy1/Fury1;binding:CostBinding=可选打出额外费用;paid_extra:bool=该费用已付;u:Unit=所选战场单位

```python

# 费用入口
ops.pay(p, cost, binding=binding)
# 打出触发
if paid_extra:
    ops.damage([u], 2)

```



<a id="card-0097"></a>

## 0097

迅捷法术

u:Unit=所选战场单位

```python

ops.kill([u])

```



<a id="card-0098"></a>

## 0098

固有待命；打出后任意单位本回合−2最低1

u:Unit=所选任意单位

```python

ops.modify_might([u], -2, duration=THIS_TURN, floor=1)

```



<a id="card-0099"></a>

## 0099

固有关键词内部展开；不同注释为独立入口

dest:Location/Zone=本次合法打出位置;choices:ChoiceBinding=定稿选择是否支付急速附加费Energy1Fury1;subjects:CostSelection=本次打出me;extra:CostChange=该次所选急速附加费Energy1Fury1，不改印刷基础费;entry:EntryState=choices选择急速则ready否则默认，必须与完整费用支付一致;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

# 急速内部费用与入场展开
ops.modify_cost(subjects, extra, duration=THIS_PLAY)
ops.play(me, p, origin=p.hand, destination=dest, choices=choices, entry=entry)

```



<a id="card-0100"></a>

## 0100

武装+4，装配Energy1/Fury1；宿主回合末未征服则卸除后对原宿主打4

cost:Cost=Energy1/Fury1;binding:CostBinding=装配主动基础费用;u:Unit=己方装配目标;host:Unit=效果区触发前原宿主快照，不是装备自己

```python

# 装配入口
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 宿主自己回合末且该回合未征服触发
ops.detach([me])
ops.damage([host], 4)

```

DATA:SC缺printedEffectText，EN的卸除伤害能力不能悄悄算作中文已提供



<a id="card-0101"></a>

## 0101

迅捷法术；按勘误各对手顶牌展示，选1先放逐再由p免费打，余回收

tops:Selection[Card]=各对手主牌堆顶牌集合;c:Card=其中选一;owner:Player=c拥有者;dest:Location/Zone=所选牌正常合法目的地;rest:Selection[Card]=未选展示牌

```python

ops.reveal(tops)
ops.banish([c])
ops.play(c, p, origin=owner.banishment, destination=dest, cost_policy=IGNORE_BASE_COST)
ops.recycle(rest)

```

ACTOR:卡面指定对手执行reveal，但reveal只有viewers而没有行动玩家，不能把公开对象/观众正确当成执行者正确



<a id="card-0102"></a>

## 0102

传奇主动Energy1横置，增益友方单位

cost:Cost=Energy1及横置me;binding:CostBinding=主动基础费用;u:Unit=所选友方单位

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.buff([u])

```



<a id="card-0103"></a>

## 0103

固有壁垒；打战场后可拉敌到此；据守后自身回拥有者手牌

u:Unit=所选敌军;origin:Zone=me场上区域

```python

# 打到战场触发入口
ops.move([u], here)
# 自身据守触发入口
ops.transfer([me], origin, me.owner.hand)

```



<a id="card-0104"></a>

## 0104

待命/迅捷法术；同一所选单位本回合坚守3壁垒

u:Unit=所选单位;params:KeywordParameters=Shield.value为3

```python

ops.grant_keyword([u], SHIELD, parameters=params, duration=THIS_TURN)
ops.grant_keyword([u], TANK, duration=THIS_TURN)

```



<a id="card-0105"></a>

## 0105

迅捷法术；杀战场≤2战力单位，按其死亡前友敌分别产1/2金币

u:Unit=所选战场战力≤2单位;friendly:bool=u死亡前由p控制;gold:TokenTemplate=金币;entry:EntryState=休眠

```python

ops.kill([u])
ops.play(gold, p, origin=None, destination=p.base, entry=entry)
if friendly:
    ops.play(gold, p, origin=None, destination=p.base, entry=entry)

```



<a id="card-0106"></a>

## 0106

打出单位可Energy1获XP；主动消耗XP3横置使单位活跃

trigger_cost:Cost=Energy1;tb:CostBinding=可选打出单位触发基础费用;active_cost:Cost=消耗XP3及横置me;ab:CostBinding=主动基础费用;u:Unit=所选任意单位

```python

# 打出单位触发
paid = ops.pay(p, trigger_cost, binding=tb)
if paid.value is not None:
    ops.gain_xp(p, 1)
# 主动入口
paid = ops.pay(p, active_cost, binding=ab)
if paid.value is not None:
    ops.ready([u])

```



<a id="card-0107"></a>

## 0107

迅捷/回响Energy1；勘误后强攻2仅本回合

u:Unit=所选单位;params:KeywordParameters=Assault.value为2

```python

ops.grant_keyword([u], ASSAULT, parameters=params, duration=THIS_TURN)

```

REPEAT:单次效果可表达，回响各遍选择及执行调度未定义



<a id="card-0108"></a>

## 0108

传奇主动Energy1横置；战场友方单位回其拥有者手牌，再打休眠金币

cost:Cost=Energy1及横置me;binding:CostBinding=主动基础费用;u:Unit=友方战场单位;origin:Zone=u场上区域;gold:TokenTemplate=完整金币模板;entry:EntryState=休眠

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.transfer([u], origin, u.owner.hand)
    ops.play(gold, p, origin=None, destination=p.base, entry=entry)

```



<a id="card-0109"></a>

## 0109

自身持续降费，本回合每征服战场Energy减2

subject:CostSelection=me打出费用;change:CostChange=Energy减少2乘p本回合实际征服战场数;dur:Duration=费用能力有效期间

```python

ops.modify_cost(subject, change, duration=dur)

```



<a id="card-0110"></a>

## 0110

固有部署；在此处赢战斗后

 

```python

ops.draw(p, 1)

```



<a id="card-0111"></a>

## 0111

固有坚守2；己方据守此处效果多触发一次；自身据守后下个自己主阶段产通用Power1

triggers:TriggerSelection=p据守此处的Hold触发，含本单位符合项

```python

ops.modify_trigger_count(triggers, 1, duration=WHILE_SOURCE_PRESENT)

```

DELAY:无登记下个自己主阶段开始再add_resources的接口；expires只控制资源到期不是开始



<a id="card-0112"></a>

## 0112

无独立印刷文字；按官方规则164.2分别有反应横置产Energy1和反应回收产所属领域Power1

exhaust_cost:Cost=横置该基础符文;exhaust_binding:CostBinding=反应产Energy主动基础费用;recycle_cost:Cost=回收该基础符文;recycle_binding:CostBinding=反应产Power主动基础费用;power:ResourceBundle=Body领域Power1

```python

# 横置产Energy的主动入口
paid = ops.pay(p, exhaust_cost, binding=exhaust_binding)
if paid.value is not None:
    ops.add_resources(p, ResourceBundle(energy=1))
# 回收产Power的独立主动入口
paid = ops.pay(p, recycle_cost, binding=recycle_binding)
if paid.value is not None:
    ops.add_resources(p, power)

```



<a id="card-0113"></a>

## 0113

Bomb固有部署；死亡前绑定地点，对此处敌军打2，再杀其他己方Bomb

u:Unit=死亡前地点所选敌军;bombs:Selection[Gear]=该地点其他己方Bomb，不含死亡的me

```python

ops.damage([u], 2)
ops.kill(bombs)

```

DATA:仅EN背面有该本体，SC/TC没有卡面文本



<a id="card-0114"></a>

## 0114

反应/回响Energy2；两友方单位本回合+1

units:Selection[Unit]=所选两友方单位

```python

ops.modify_might(units, 1, duration=THIS_TURN)

```

REPEAT:无回响定稿各遍选择与单链项重复效果的完整组合接口



<a id="card-0115"></a>

## 0115

待命法术；指定对手单位免费打到指定战场；成功后自反项眩晕

actor:Player=所选对手;hand:Selection[Card]=其展示时手牌;u:Card=其中所选单位;take:bool=选择该单位;b:Battlefield=先选定战场;permit:PlayPermission=仅本次允许actor将该牌打到b

```python

ops.reveal(hand)
if take:
    ops.play(u, actor, origin=actor.hand, destination=b, cost_policy=IGNORE_ALL_COSTS, permission=permit)

```

REFLEXIVE:勘误if they do then do this要求成功执行后的独立眩晕链项，不能依据play定稿返回直接stun

ACTOR:卡面指定对手执行reveal，但reveal只有viewers而没有行动玩家，不能把公开对象/观众正确当成执行者正确



<a id="card-0116"></a>

## 0116

武装+2；装配Energy1/Body1；宿主征服召1休眠符文

cost:Cost=Energy1/Body1;binding:CostBinding=装配基础费用;u:Unit=己方宿主

```python

# 装配入口
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 效果区宿主征服入口，p为宿主能力控制者
ops.channel(p, 1, exhausted=True)

```

DATA:SC缺效果区，EN异画也缺效果区，普通EN有征服召符文

DATA:同一本体有非空装备效果，但这些变体printedEffectText为空：EN SFD-118a, SC SFD-118



<a id="card-0117"></a>

## 0117

武装+2；装配Chaos1；宿主游走

cost:Cost=Chaos1;binding:CostBinding=装配基础费用;u:Unit=己方宿主;host:Selection[Unit]=当前宿主;dur:Duration=当前贴附期间

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 效果区持续
ops.grant_keyword(host, GANKING, duration=dur)

```

DATA:SC未提供printedEffectText中的宿主游走



<a id="card-0118"></a>

## 0118

自己主阶段开始可杀3其他友方单位/装备作为触发费用获1分

cost:Cost=同时杀恰3其他友方单位和或装备;binding:CostBinding=可选主阶段触发基础费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.gain_points(p, 1)

```



<a id="card-0119"></a>

## 0119

传奇主动横置；赋单位本回合游走

cost:Cost=横置me;binding:CostBinding=主动基础费用;u:Unit=所选任意单位

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.grant_keyword([u], GANKING, duration=THIS_TURN)

```



<a id="card-0120"></a>

## 0120

传奇强化Energy1横置；主动解除强化横置，下一单位降费且获回合末自毁

ecost:Cost=Energy1及横置me;eb:CostBinding=仅未强化的主动基础费用;cost:Cost=解除me一层强化及横置me;binding:CostBinding=另一主动基础费用;next_unit:CostSelection=本回合p下一张打出单位;change:CostChange=Energy减2及任意Power减1

```python

# 强化主动
paid = ops.pay(p, ecost, binding=eb)
if paid.value is not None:
    ops.empower([me])
# 解除强化主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_cost(next_unit, change, duration=THIS_TURN, uses=1)

```

NEXT_ABILITY:grant_ability作用于具体对象集合且无次数/下一次打出钩子，不能把尚未绑定的未来下一单位当成现有实例授自毁



<a id="card-0121"></a>

## 0121

迅捷法术；强攻值等执行时目标战力，持续本回合

u:Unit=所选单位;params:KeywordParameters=Assault.value为u执行时战力快照，不动态追随加值后的战力

```python

ops.grant_keyword([u], ASSAULT, parameters=params, duration=THIS_TURN)

```



<a id="card-0122"></a>

## 0122

打出时可弃1为额外费，已付则Energy减2

cost:Cost=弃所选手牌1;binding:CostBinding=可选打出额外费用;subject:CostSelection=本次me打出费用;change:CostChange=Energy减少2

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_cost(subject, change, duration=UNTIL_EFFECT_END, uses=1)

```



<a id="card-0123"></a>

## 0123

己方Mech持续法盾游走；有另一己方Mech则活跃入场

mechs:Selection[Unit]=动态己方Mech，含me在场时;entry:EntryState=定稿时有另一己方Mech则活跃，否则默认;dest:Location=合法打出地点

```python

# 基础打出
ops.play(me, p, origin=p.hand, destination=dest, entry=entry)
# 持续
ops.grant_keyword(mechs, DEFLECT, duration=WHILE_SOURCE_PRESENT)
ops.grant_keyword(mechs, GANKING, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0124"></a>

## 0124

法术杀装备；流转Energy4/Fury1为额外出牌路径

g:Gear=所选装备

```python

ops.kill([g])

```

FLOW_EXIT:从废牌替代费用可授权，但无通用已定稿链项非自身指令离链时放逐替代，不能用结算后banish冒充被无效化情形



<a id="card-0125"></a>

## 0125

此处五标签单位+1；此处Scored可恢复其替换的原战场

units:Selection[Unit]=此处Bird/Cat/Dog/Poro/Ivern任一标签单位；每单位只+1;link:Link=本草丛替换关联

```python

# 持续
ops.modify_might(units, 1, duration=WHILE_SOURCE_PRESENT)
# 此处Scored可选入口
ops.restore_battlefield(me, link=link)

```



<a id="card-0126"></a>

## 0126

强化Energy3；强化持续+2及游走

cost:Cost=Energy3;binding:CostBinding=仅未强化主动基础费用;dur:Duration=me留场且强化

```python

# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 持续
ops.modify_might([me], 2, duration=dur)
ops.grant_keyword([me], GANKING, duration=dur)

```



<a id="card-0127"></a>

## 0127

武装+1；装配Calm1；本回合贴给该宿主则宿主额外+2

cost:Cost=Calm1;binding:CostBinding=装配基础费用;u:Unit=己方装配目标;host:Selection[Unit]=当前宿主;dur:Duration=仍贴附且该贴附在当前回合发生期间

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 效果区持续
ops.modify_might(host, 2, duration=dur)

```

DATA:SC没有printedEffectText中的额外+2



<a id="card-0128"></a>

## 0128

自身打出触发，对手本回合不能打牌

opponents:PermissionSelection=所有对手;restriction:RestrictionSpec=不能执行play动作，不禁止非打出动作

```python

ops.restrict_action(opponents, restriction, duration=THIS_TURN)

```



<a id="card-0129"></a>

## 0129

自身打出触发

u:Unit=所选另一友方Mech单位

```python

ops.ready([u])

```



<a id="card-0130"></a>

## 0130

增益规则提醒物，不是赋予全场新规则的技能

 

```python

# 无对局可执行能力；不得调用modify_rule覆盖李青等明确例外

```



<a id="card-0131"></a>

## 0131

打出后可选抽1或增益自己，可整条放弃

draw_mode:bool=已选择抽牌模式，否则为增益模式

```python

if draw_mode:
    ops.draw(p, 1)
else:
    ops.buff([me])

```



<a id="card-0132"></a>

## 0132

迅捷法术；结算付任意Power数量，对指定战场全部敌军各同量伤害

cost:Cost=玩家选择数量的任意领域Power;binding:CostBinding=法术结算的指令内费用;n:IntExpr=该次实际支付Power数量;units:Selection[Unit]=所选战场所有敌军

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.damage(units, n)

```



<a id="card-0133"></a>

## 0133

放逐战力≤3单位或任意装备，然后燃烧2

c:Card=所选合法单位或装备

```python

ops.banish([c])
ops.burn(p, 2)

```



<a id="card-0134"></a>

## 0134

待命法术；本回合己方单位均活跃入场，再打休眠金币

gold:TokenTemplate=金币;entry:EntryState=休眠

```python

ops.play(gold, p, origin=None, destination=p.base, entry=entry)

```

ENTRY:play.entry只能修改一次打出，缺登记本回合所有己军未来打出/生成活跃入场的修饰API，不能用READY代替



<a id="card-0135"></a>

## 0135

固有部署；此战场由自己或盟友控制时，该玩家盖放容量+1

scope:RuleScope=动态的此战场己方或盟友控制者盖放容量;change:RuleChange=容量加1;dur:Duration=me留场且该控制条件满足

```python

ops.modify_rule(HIDDEN_CAPACITY, scope, change, duration=dur)

```



<a id="card-0136"></a>

## 0136

传奇反应产费，任意Power2横置换Energy2，限打单位和单位主动

cost:Cost=任意Power2及横置me;binding:CostBinding=反应产费主动基础费用;bundle:ResourceBundle=Energy2;restriction:Predicate=只可支付单位打出或单位主动费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.add_resources(p, bundle, restriction=restriction)

```



<a id="card-0137"></a>

## 0137

持续最后分配战斗伤害；在战场才可横置按自己战力打战场单位

scope:RuleScope=me同控制者的战斗伤害分配关系;last:RuleChange=me须在其他己军后分配致死伤害;cost:Cost=横置me;binding:CostBinding=仅自身在战场可发动的主动基础费用;u:Unit=EN/TC任意战场所选单位;m:IntExpr=me结算时战力

```python

# 持续
ops.modify_rule(COMBAT_DAMAGE_ORDER, scope, last, duration=WHILE_SOURCE_PRESENT)
# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.damage([u], m)

```

LANG:SC目标仅敌军，而EN/TC允许任意单位；并列保留不能统一当同一目标集合



<a id="card-0138"></a>

## 0138

法术先移己军到己控战场，再所选对手选其单位移同一战场

u:Unit=己方所选单位;b:Battlefield=己方控制的所选战场;actor:Player=所选对手;candidates:Selection[Unit]=actor控制单位

```python

ops.move([u], b)
chosen = ops.choose(actor, candidates, targeting=False, bind_at="resolution")
ops.move(chosen.value, b)

```

ACTOR:卡面指定其他玩家执行摧毁或移动，但对应kill/move无执行玩家参数；不能以选择权正确冒充动作归属正确



<a id="card-0139"></a>

## 0139

反应法术；打出可消耗增益作额外费以忽略基础费用；结算+3

cost:Cost=所选己方单位消耗一个增益;binding:CostBinding=可选打出额外费用;subject:CostSelection=本次me基础费用;change:CostChange=忽略本次基础费用，不再重复消耗增益;u:Unit=效果所选任意单位

```python

# 定稿费用入口
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_cost(subject, change, duration=UNTIL_EFFECT_END, uses=1)
# 法术结算入口
ops.modify_might([u], 3, duration=THIS_TURN)

```



<a id="card-0140"></a>

## 0140

迅捷/回响Chaos1；看2抽其中一张回收另一

c:Card=实际看见的牌中所选抽牌对象;rest:Selection[Card]=实际看见牌中其余牌，不足时不创造第二张

```python

ops.look(p, p.main_deck, 2)
ops.draw(p, 1, cards=[c])
ops.recycle(rest)

```

REPEAT:单次效果可表达，回响重复及各遍定稿选择未有组合接口



<a id="card-0141"></a>

## 0141

无独立印刷文字；按官方规则164.2分别有反应横置产Energy1和反应回收产所属领域Power1

exhaust_cost:Cost=横置该基础符文;exhaust_binding:CostBinding=反应产Energy主动基础费用;recycle_cost:Cost=回收该基础符文;recycle_binding:CostBinding=反应产Power主动基础费用;power:ResourceBundle=Calm领域Power1

```python

# 横置产Energy的主动入口
paid = ops.pay(p, exhaust_cost, binding=exhaust_binding)
if paid.value is not None:
    ops.add_resources(p, ResourceBundle(energy=1))
# 回收产Power的独立主动入口
paid = ops.pay(p, recycle_cost, binding=recycle_binding)
if paid.value is not None:
    ops.add_resources(p, power)

```



<a id="card-0142"></a>

## 0142

反应法术

units:Selection[Unit]=当前所有处于战斗的敌军

```python

ops.damage(units, 2)

```



<a id="card-0143"></a>

## 0143

持续给此处其他友方单位强攻1，不含自己

units:Selection[Unit]=此处其他友方单位

```python

ops.grant_keyword(units, ASSAULT, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0144"></a>

## 0144

打出后各玩家可打休眠金币，每个实际这样打的对手令p额外打一金币

actors:Selection[Player]=p与所有对手;accept:dict[Player,bool]=各玩家是否选择打金币;gold:TokenTemplate=金币;entry:EntryState=休眠;n:int=本次成功打出金币的对手数，不按初始愿望推断

```python

for actor in actors:
    if accept[actor]:
        ops.play(gold, actor, origin=None, destination=actor.base, entry=entry)
for i in range(n):
    ops.play(gold, p, origin=None, destination=p.base, entry=entry)

```



<a id="card-0145"></a>

## 0145

打出后与所选战场敌军互相按各自战力同时造成伤害

u:Unit=所选战场敌军;m:IntExpr=me伤害前战力快照;n:IntExpr=u伤害前战力快照

```python

# 以下是两个方向的独立片段，不能直接当作同时互殴程序
ops.damage([u], m, source=me)
ops.damage([me], n, source=u)

```

RECIPROCAL:单次damage只有一个来源和统一数值，缺多来源不同数值的同时伤害批次；逐次damage可能提前致死清理



<a id="card-0146"></a>

## 0146

绝念打1战力带法盾Bird到基地；法盾属于Bird模板

bird:TokenTemplate=1战力Bird且有Deflect

```python

ops.play(bird, p, origin=None, destination=p.base)

```



<a id="card-0147"></a>

## 0147

法术先禁对手本回合法术，再移友方单位到敌方占据战场

opponents:PermissionSelection=所有对手;restriction:RestrictionSpec=禁止打出spell类型，不禁止单位/装备;u:Unit=友方单位;b:Battlefield=敌方occupied战场

```python

ops.restrict_action(opponents, restriction, duration=THIS_TURN)
ops.move([u], b)

```



<a id="card-0148"></a>

## 0148

各玩家先各选一己军保留，再一次杀其余

players:Selection[Player]=全部玩家;candidates:dict[Player,Selection[Unit]]=各玩家己方单位;rest:Selection[Unit]=全部单位排除各次choose实际保留者，选择完成后绑定

```python

for actor in players:
    ops.choose(actor, candidates[actor], targeting=False, bind_at="resolution")
ops.kill(rest)

```



<a id="card-0149"></a>

## 0149

法术召2休眠，实际不足2则抽1

 

```python

r = ops.channel(p, 2, exhausted=True)
if len(r.value) < 2:
    ops.draw(p, 1)

```



<a id="card-0150"></a>

## 0150

打出后废牌单位回手

c:Card=己方废牌堆所选单位

```python

ops.transfer([c], p.trash, p.hand)

```



<a id="card-0151"></a>

## 0151

固有伏击；打出后此处其他己军本回合坚守1

units:Selection[Unit]=此处其他己方单位，不含me

```python

ops.grant_keyword(units, SHIELD, duration=THIS_TURN)

```



<a id="card-0152"></a>

## 0152

迅捷法术，己军与敌军互相同时按战力造成伤害

u:Unit=所选友军;v:Unit=所选敌军;m:IntExpr=u执行前战力快照;n:IntExpr=v执行前战力快照

```python

# 两方向独立片段，不能当作同一批次
ops.damage([v], m, source=u)
ops.damage([u], n, source=v)

```

RECIPROCAL:缺多来源不同数值的同时伤害批次；连续两次damage不等价



<a id="card-0153"></a>

## 0153

无独立印刷文字；按官方规则164.2分别有反应横置产Energy1和反应回收产所属领域Power1

exhaust_cost:Cost=横置该基础符文;exhaust_binding:CostBinding=反应产Energy主动基础费用;recycle_cost:Cost=回收该基础符文;recycle_binding:CostBinding=反应产Power主动基础费用;power:ResourceBundle=Chaos领域Power1

```python

# 横置产Energy的主动入口
paid = ops.pay(p, exhaust_cost, binding=exhaust_binding)
if paid.value is not None:
    ops.add_resources(p, ResourceBundle(energy=1))
# 回收产Power的独立主动入口
paid = ops.pay(p, recycle_cost, binding=recycle_binding)
if paid.value is not None:
    ops.add_resources(p, power)

```



<a id="card-0154"></a>

## 0154

法术移动敌军，目的地需正常合法

u:Unit=所选敌军;dest:Location=其合法移动目的地

```python

ops.move([u], dest)

```



<a id="card-0155"></a>

## 0155

自己或盟友据守可横置传奇产金币；距胜利≤3金币额外Energy1

cost:Cost=横置me;binding:CostBinding=可选据守触发基础费用;gold:TokenTemplate=金币;entry:EntryState=休眠;actions:ResourceActionSelection=自己控制的金币Add动作;change:ResourceChange=额外Energy1;dur:Duration=me在传奇区且己方得分距胜利≤3

```python

# 据守触发
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.play(gold, p, origin=None, destination=p.base, entry=entry)
# 持续产费修饰
ops.modify_resource_output(actions, change, duration=dur)

```



<a id="card-0156"></a>

## 0156

对手回合己方打出法术后，可横置装备产金币

cost:Cost=横置me;binding:CostBinding=可选触发基础费用;gold:TokenTemplate=金币;entry:EntryState=休眠

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.play(gold, p, origin=None, destination=p.base, entry=entry)

```



<a id="card-0157"></a>

## 0157

固有强攻2；打出必须弃1

 

```python

ops.discard(p, 1)

```



<a id="card-0158"></a>

## 0158

打出额外付任意Power，结算放逐同量己军；按己选顺序各由拥有者打回原地或基地

cost:Cost=玩家选定任意Power数量;binding:CostBinding=本次打出额外费用;units:Selection[Unit]=数量等实际支付Power的己军;ordered:list[Card]=本次实际放逐者按p决定的顺序;destinations:dict[Card,Location]=各自拥有者选择原地点快照或自己基地;permit:PlayPermission=仅本效果允许打回被放逐实例的原地点

```python

# 定稿额外费
ops.pay(p, cost, binding=binding)
# 结算
ops.banish(units)
for c in ordered:
    ops.play(c, c.owner, origin=c.owner.banishment, destination=destinations[c], cost_policy=IGNORE_BASE_COST, permission=permit)

```



<a id="card-0159"></a>

## 0159

p打出另一单位后

 

```python

ops.buff([me])

```



<a id="card-0160"></a>

## 0160

反应法术

 

```python

ops.predict(p, 5)
ops.draw(p, 2)

```



<a id="card-0161"></a>

## 0161

动态己方Mech获得缴械1，含自身

units:Selection[Unit]=己方所有Mech单位

```python

ops.grant_keyword(units, DISARM, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0162"></a>

## 0162

任选两单位互相同时按战力造成伤害，不限友敌

u:Unit=第一单位;v:Unit=第二单位;m:IntExpr=u事前战力;n:IntExpr=v事前战力

```python

# 仅独立方向片段
ops.damage([v], m, source=u)
ops.damage([u], n, source=v)

```

RECIPROCAL:无法用一个damage描述多来源互殴，逐次调用不能保证同时清理



<a id="card-0163"></a>

## 0163

迅捷法术

u:Unit=所选单位;params:KeywordParameters=Assault.value为3

```python

ops.grant_keyword([u], ASSAULT, parameters=params, duration=THIS_TURN)

```



<a id="card-0164"></a>

## 0164

打出或自身据守洞察3；绝念放逐己顶可忽略Energy打出

top:Card=己主牌堆顶;take:bool=选择打出;dest:Location/Zone=该牌合法目的地;policy:CostPolicy=仅忽略Energy，仍支付Power与其他成本

```python

# 打出/据守入口
ops.predict(p, 3)
# 绝念入口
ops.banish([top])
if take:
    ops.play(top, p, origin=p.banishment, destination=dest, cost_policy=policy)

```



<a id="card-0165"></a>

## 0165

可额外Calm1，勘误后打出成功且已付才触发抽1

cost:Cost=Calm1;binding:CostBinding=可选打出额外费用;paid_extra:bool=本次该额外费用已付

```python

# 定稿费用
ops.pay(p, cost, binding=binding)
# 打出触发，不是在费用阶段抽牌
if paid_extra:
    ops.draw(p, 1)

```



<a id="card-0166"></a>

## 0166

灵便免费打出贴附；独立装配Mind1；效果区宿主坚守2

u:Unit=对应入口所选己方宿主;cost:Cost=Mind1;binding:CostBinding=普通装配主动基础费用;host:Selection[Unit]=当前贴附宿主;dur:Duration=本装备仍贴附期间;params:KeywordParameters=Shield.value为2

```python

# 灵便打出触发入口，不付装配费
ops.attach(me, u)
# 装配主动入口
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 效果区持续能力的执行体
ops.grant_keyword(host, SHIELD, parameters=params, duration=dur)

```

DATA:SC缺printedEffectText中的坚守2



<a id="card-0167"></a>

## 0167

打出触发

 

```python

ops.draw(p, 1)

```



<a id="card-0168"></a>

## 0168

自己回合末，先同时回收己方全符文，再召4休眠

runes:Selection[Rune]=己方全部符文

```python

ops.recycle(runes)
ops.channel(p, 4, exhausted=True)

```



<a id="card-0169"></a>

## 0169

百炼打出触发：可装配p武装，装配费减任意Power1，允许已贴附武装

g:Gear=p控制的一件武装;cost:Cost=g的Equip费用减任意Power1最低0;binding:CostBinding=百炼可选触发费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(g, me)

```



<a id="card-0170"></a>

## 0170

反应法术；XP≥6改+3，否则+1

u:Unit=所选单位;level6:bool=效果读取时pXP≥6

```python

ops.modify_might([u], 3 if level6 else 1, duration=THIS_TURN)

```



<a id="card-0171"></a>

## 0171

模式1移友方部署装备到战场；模式2看5可展示装备抽取，余回收

move_mode:bool=定稿所选模式为移动;g:Gear=友方具有Deploy的所选装备;b:Battlefield=所选合法战场;take:bool=模式2选择装备;card:Card=实际看见顶5中所选装备;rest:Selection[Card]=看见牌中未抽取者，无选择则全部

```python

if move_mode:
    ops.move([g], b)
else:
    ops.look(p, p.main_deck, 5)
    if take:
        ops.reveal([card])
        ops.draw(p, 1, cards=[card])
    ops.recycle(rest)

```



<a id="card-0172"></a>

## 0172

固有法盾游走；可杀任意友方单位作额外费，按实际杀数减少Order

cost:Cost=任选数量友方单位的同时摧毁;binding:CostBinding=打出可选额外费用;subject:CostSelection=本次me费用;change:CostChange=Order需求减少本次实际摧毁单位数，不只按所选数

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_cost(subject, change, duration=UNTIL_EFFECT_END, uses=1)

```



<a id="card-0173"></a>

## 0173

XP≥6自身Energy减2，≥11改减4；结算抽2，不叠减6

subject:CostSelection=本次自身费用;change:CostChange=XP≥11减Energy4，否则≥6减2，否则0;dur:Duration=费用能力有效期间

```python

# 费用入口
ops.modify_cost(subject, change, duration=dur)
# 法术结算
ops.draw(p, 2)

```



<a id="card-0174"></a>

## 0174

固有部署；自身打出或p征服此处，可付Energy1打随从基地

cost:Cost=Energy1;binding:CostBinding=相应可选触发基础费用;recruit:TokenTemplate=1战力Recruit

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.play(recruit, p, origin=None, destination=p.base)

```



<a id="card-0175"></a>

## 0175

迅捷法术，自己本回合打出单位活跃入场，再抽1

 

```python

ops.draw(p, 1)

```

ENTRY:缺本回合未来所有打出单位入场状态登记；不能反复READY，因为不应产生活跃事件



<a id="card-0176"></a>

## 0176

可额外消耗XP5；据支付状态选战场敌军，夺控横置召回

cost:Cost=消耗XP5;binding:CostBinding=可选打出额外费用;u:Unit=已付则任意战场敌军，未付则战力≤3战场敌军

```python

# 定稿额外费
ops.pay(p, cost, binding=binding)
# 按支付记录筛选目标后的结算
ops.change_control([u], p)
ops.exhaust([u])
ops.recall([u])

```



<a id="card-0177"></a>

## 0177

反应法术

u:Unit=所选单位;params:KeywordParameters=Shield.value为2

```python

ops.grant_keyword([u], SHIELD, parameters=params, duration=THIS_TURN)
ops.predict(p)

```



<a id="card-0178"></a>

## 0178

待命/反应法术

 

```python

ops.draw(p, 2)

```



<a id="card-0179"></a>

## 0179

迅捷法术，对战场单位打2，每己方废牌同名额外伤害1

u:Unit=所选战场单位;events:DamageSelection=本次me直接伤害这一段;n:IntExpr=己方废牌中与me同名牌数快照

```python

ops.modify_damage(events, NumericChange(add=n), duration=UNTIL_EFFECT_END, uses=1)
ops.damage([u], 2)

```



<a id="card-0180"></a>

## 0180

反应法术，按勘误本回合提高友方单位至另一友方单位战力，不得降低

u:Unit=所选友方单位;m:IntExpr=另一友方单位执行时战力快照

```python

ops.set_might([u], m, direction="increase_only", duration=THIS_TURN)

```



<a id="card-0181"></a>

## 0181

固有急速；移动到战场后在此处打3随从

recruit:TokenTemplate=1战力Recruit

```python

for i in range(3):
    ops.play(recruit, p, origin=None, destination=here)

```



<a id="card-0182"></a>

## 0182

移到战场弃1；自身赢战斗抽1，两个独立入口

 

```python

# 移入战场触发
ops.discard(p, 1)
# 自身赢战斗触发
ops.draw(p, 1)

```



<a id="card-0183"></a>

## 0183

距胜利>3则活跃入场；进攻可移此处任意≤5战力敌军回其基地

dest:Location=自身合法打出地点;entry:EntryState=定稿时距胜利>3则活跃，否则默认;units:Selection[Unit]=此处任选战力≤5敌军;base:Location=此处敌方控制者对应基地

```python

# 基础打出
ops.play(me, p, origin=p.hand, destination=dest, entry=entry)
# 进攻触发
ops.move(units, base)

```



<a id="card-0184"></a>

## 0184

p据守此处时符文牌堆为空

 

```python

ops.gain_points(p, 1)

```



<a id="card-0185"></a>

## 0185

反应法术，预防所选单位本回合下一次全部伤害，之后抽1

u:Unit=所选单位

```python

ops.draw(p, 1)

```

PREVENT_ONCE:prevent_damage无uses，INFINITY在THIS_TURN持续会预防多次；UNTIL事件的消耗边界未规定，不能伪称一次性完整覆盖



<a id="card-0186"></a>

## 0186

强化Energy3；强化状态移动后抽1

cost:Cost=Energy3;binding:CostBinding=仅未强化主动基础费用

```python

# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 强化状态移动触发
ops.draw(p, 1)

```



<a id="card-0187"></a>

## 0187

进攻触发

u:Unit=此处所选敌军

```python

ops.damage([u], 1)

```



<a id="card-0188"></a>

## 0188

本回合已打出法术才可额外Chaos1活跃入场

dest:Location=合法目的地;choices:ChoiceBinding=仅满足该法术定稿历史条件时可选择Chaos1额外费用;entry:EntryState=仅该额外费实付则活跃，否则默认

```python

ops.play(me, p, origin=p.hand, destination=dest, choices=choices, entry=entry)

```



<a id="card-0189"></a>

## 0189

迅捷法术；先选战场及其中一敌军，对该军4且其他敌军各1

u:Unit=指定战场所选敌军;others:Selection[Unit]=该战场其他敌军

```python

# 两个可表达片段，不当作完整同批指令
ops.damage([u], 4)
ops.damage(others, 1)

```

DAMAGE_BATCH:damage.each只有统一数值；split会改变额外伤害按总池而非逐目标适用的语义，缺非分配式不同数值同批伤害



<a id="card-0190"></a>

## 0190

与另一单位一起作为进攻方时持续+2

dur:Duration=me留场且正与另一单位共同进攻期间

```python

ops.modify_might([me], 2, duration=dur)

```



<a id="card-0191"></a>

## 0191

固有狩猎1；主动消耗XP2增益自身

cost:Cost=消耗XP2;binding:CostBinding=主动基础费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.buff([me])

```



<a id="card-0192"></a>

## 0192

打出必须杀一友方单位作为额外费用

cost:Cost=杀所选友方单位一名;binding:CostBinding=本次打出强制额外费用

```python

ops.pay(p, cost, binding=binding)

```



<a id="card-0193"></a>

## 0193

反应法术；对手本回合已定稿另一法术才无效化

spell:ChainItem=所选链上法术;condition:bool=对手本回合已打出另一法术，历史条件明确提供

```python

if condition:
    ops.counter(spell)

```



<a id="card-0194"></a>

## 0194

武装+1；装配Chaos1；宿主征服打休眠金币

cost:Cost=Chaos1;binding:CostBinding=装配基础费用;u:Unit=己方宿主;gold:TokenTemplate=金币;entry:EntryState=休眠

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 宿主征服
ops.play(gold, p, origin=None, destination=p.base, entry=entry)

```

DATA:SC缺printedEffectText中的征服产金币



<a id="card-0195"></a>

## 0195

各玩家自行选一个己军，然后同时摧毁这些选择

players:Selection[Player]=所有玩家;candidates:dict[Player,Selection[Unit]]=每玩家己军;chosen_units:Selection[Unit]=所有choose的实际选择结果并集

```python

for actor in players:
    ops.choose(actor, candidates[actor], targeting=False, bind_at="resolution")
ops.kill(chosen_units)

```

ACTOR:卡面指定其他玩家执行摧毁或移动，但对应kill/move无执行玩家参数；不能以选择权正确冒充动作归属正确



<a id="card-0196"></a>

## 0196

p打出印刷Energy≥7单位/装备/主动能力时，可横置传奇活跃至多2符文

cost:Cost=横置me;binding:CostBinding=可选触发基础费用;runes:Selection[Rune]=至多2所选己方符文

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    pass  # Rune不符合ready的Permanent参数类型

```

RUNE_READY:规则133.5.a.1/161.1.a明确Rune不是Permanent，ready签名不能接受该符文集合



<a id="card-0197"></a>

## 0197

打出放逐己废牌全部单位并关联；主动横置正常付费打本实例放逐的单位

units:Selection[Card]=己方废牌单位;link:Link=本石棺这次能力关联;cost:Cost=横置me;binding:CostBinding=主动基础费用;c:Card=本实例确实放逐且仍在放逐区的所选单位;dest:Location=其正常合法打出地点;permit:PlayPermission=允许由本主动从该关联放逐集合打出，仍付费用

```python

# 打出触发
ops.banish(units, link=link)
# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.play(c, p, origin=p.banishment, destination=dest, permission=permit)

```



<a id="card-0198"></a>

## 0198

三项独立回响费用；各遍模式不能重复，四个效果体

mode:int=本遍已定稿的未重复模式0/1/2/3;u:Unit=mode1/3为战场目标，mode2为基地目标

```python

if mode == 0:
    ops.draw(p, 1)
elif mode == 1:
    ops.damage([u], 2)
elif mode == 2:
    ops.damage([u], 3)
else:
    ops.modify_might([u], -4, duration=THIS_TURN)

```

REPEAT:缺按三个各付一次回响费用创建同一链项多遍效果并限制各遍模式不重复的完整流程



<a id="card-0199"></a>

## 0199

活跃入场；己军四指定标签每种Energy−1；进攻齐四标签晕敌军

dest:Location=合法目的地;entry:EntryState=活跃;subject:CostSelection=me打出费用;change:CostChange=Energy减己军中Bird/Cat/Dog/Poro不同标签数；每种最多1;dur:Duration=自身费用能力有效期;u:Unit=此处所选敌军

```python

# 费用
ops.modify_cost(subject, change, duration=dur)
# 基础打出
ops.play(me, p, origin=p.hand, destination=dest, entry=entry)
# 齐四标签的进攻触发
ops.stun([u])

```



<a id="card-0200"></a>

## 0200

强化Energy5/Body1；强化进攻防守提高到此处单位战力再+1

cost:Cost=Energy5/Body1;binding:CostBinding=仅未强化主动基础费用;m:IntExpr=此处所选单位战力快照，不限定大于自己

```python

# 强化
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 强化进攻或防守
ops.set_might([me], m, direction="increase_only", duration=THIS_TURN)
ops.modify_might([me], 1, duration=THIS_TURN)

```

LANG:SC要求目标战力大于自己，EN任意此处单位但只提高，目标合法集合不同



<a id="card-0201"></a>

## 0201

法术对单位打2；其控制者可付任意Power1重新打此牌并按本回合既往伤害次数加额外伤害

u:Unit=所选单位

```python

ops.damage([u], 2)

```

CHAIN_REPLAY:缺清楚定义在自身执行中由新玩家重打同一链上牌、跨重打保留伤害次数及将额外伤害绑定新链项的流程；不能把当前法术复制当作再打



<a id="card-0202"></a>

## 0202

反应/回响Energy1及任意Power1；己方Mech本回合+1

units:Selection[Unit]=执行时所有己方Mech

```python

ops.modify_might(units, 1, duration=THIS_TURN)

```

REPEAT:单遍效果可表达，多遍回响及预先选择流程未定义



<a id="card-0203"></a>

## 0203

鼓舞条件为本回合已定稿另一牌；打出触发

u:Unit=所选任意单位

```python

ops.modify_might([u], 2, duration=THIS_TURN)

```



<a id="card-0204"></a>

## 0204

固有Assault1的内部持续效果：me进攻时战力加1

attacking:bool=me是进攻方;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if attacking:
    ops.modify_might([me], 1, duration=WHILE_CONDITION)

```



<a id="card-0205"></a>

## 0205

鼓舞打出后活跃自身；持续此处其他友方单位+1

others:Selection[Unit]=此处其他友方单位

```python

# 鼓舞打出入口
ops.ready([me])
# 持续入口
ops.modify_might(others, 1, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0206"></a>

## 0206

p每回合打出第二张牌后

 

```python

ops.modify_might([me], 2, duration=THIS_TURN)
ops.ready([me])

```



<a id="card-0207"></a>

## 0207

己回合末，勘误至多2符文

runes:Selection[Rune]=至多2所选己方符文

```python

pass  # Rune不符合ready的Permanent参数类型

```

RUNE_READY:规则133.5.a.1/161.1.a明确Rune不是Permanent，ready签名不能接受该符文集合



<a id="card-0208"></a>

## 0208

传奇反应产费，横置产通用Power1仅用于打出法术

cost:Cost=横置me;binding:CostBinding=反应产费主动基础费用;bundle:ResourceBundle=通用Power1;restriction:Predicate=仅可支付打出法术费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.add_resources(p, bundle, restriction=restriction)

```



<a id="card-0209"></a>

## 0209

自身可打敌方occupied战场，不授时机或忽略费用

permit:PermissionSpec=me打出目的地额外允许enemy-occupied战场;dur:Duration=me在可打出区域且能力有效期间

```python

ops.grant_permission(me, permit, duration=dur)

```

LANG:SC写敌方控制，EN为敌方occupied，不能默认两个谓词等同



<a id="card-0210"></a>

## 0210

自己回合末逐张展示直到单位，勘误先放逐该单位再免费打出，余回收

revealed:Selection[Card]=严格从己主牌堆顶依序到首单位为止，若无则全部，未查看牌不能预先获知;u:Card=所揭示首单位;found:bool=实际有单位;rest:Selection[Card]=其余实际展示牌;dest:Location=该单位合法目的地

```python

ops.reveal(revealed)
if found:
    ops.banish([u])
    ops.play(u, p, origin=p.banishment, destination=dest, cost_policy=IGNORE_BASE_COST)
ops.recycle(rest)

```

REVEAL_UNTIL:reveal接收预绑定对象集合，没有依次揭示至首命中并停止的接口；预先提供revealed会越权读取秘密次序，以上仅结果已知后的片段



<a id="card-0211"></a>

## 0211

固有法盾；额外允许打到敌方occupied战场

permit:PermissionSpec=打出目的地允许enemy-occupied，不授反应;dur:Duration=me可打出区域能力有效期间

```python

ops.grant_permission(me, permit, duration=dur)

```

LANG:SC为敌方控制的战场，EN/TC为敌方occupied



<a id="card-0212"></a>

## 0212

法术先对敌军打3，登记本回合该军死亡产金币

u:Unit=所选敌军

```python

ops.damage([u], 3)

```

DELAY:缺登记该实例本回合死亡触发打休眠金币的接口，不等于当下若死即产金币



<a id="card-0213"></a>

## 0213

杀战场单位；死亡前战力≤3则自反项可从废牌Power1重打

u:Unit=所选战场单位

```python

ops.kill([u])

```

REFLEXIVE:勘误do this要求等当前法术正常离链后新待处理项重打，不能在当前结算立刻play已假定在trash的me



<a id="card-0214"></a>

## 0214

燃烧3、打0战力带攻击放逐换强攻能力的影分身；流转Energy1/任意Power2

clone:TokenTemplate=完整0战力ShadowClone模板，含原触发能力;dest:Location=合法打出目的地

```python

ops.burn(p, 3)
ops.play(clone, p, origin=None, destination=dest)

```

FLOW_EXIT:缺已定稿流转链项离链放逐替代；分身模板能力不等于本法术有强攻



<a id="card-0215"></a>

## 0215

反应法术；勘误杀友军，若实杀则另一友方单位+死亡前战力；抽1独立

u:Unit=要杀的友方单位;v:Unit=另一友方单位;m:IntExpr=u死亡前战力快照

```python

r = ops.kill([u])
if r.changed:
    ops.modify_might([v], m, duration=THIS_TURN)
ops.draw(p, 1)

```



<a id="card-0216"></a>

## 0216

传奇征服/据守可弃1横置打活跃Reflection此处；勘误另自反项复制此处另一单位并赋瞬息

cost:Cost=弃1及横置me;binding:CostBinding=可选征服/据守触发基础费用;reflection:TokenTemplate=Reflection原模板;entry:EntryState=活跃;dest:Location=触发征服/据守的战场

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.play(reflection, p, origin=None, destination=dest, entry=entry)

```

REFLEXIVE:缺另一个待处理项绑定实际进场Reflection后copy并grant_keyword(Temporary)；play返回链项不能当Unit



<a id="card-0217"></a>

## 0217

迅捷法术

units:Selection[Unit]=执行时全体友方单位

```python

ops.modify_might(units, 2, duration=THIS_TURN)

```



<a id="card-0218"></a>

## 0218

选任意数量敌方Order单位，总战力≤5，回各拥有者手牌

u:Unit=该集合中的一个，仅单对象局部示例;origin:Zone=u场上区域

```python

ops.transfer([u], origin, u.owner.hand)

```

BATCH:transfer无异来源/目的地映射的同时集合转移；不能逐次回手改变统计和清理



<a id="card-0219"></a>

## 0219

反应法术；友方单位正与敌方Fury单位战斗或正被敌方Fury法术选择

u:Unit=满足两个条件之一的友方单位，不把其中或写成且

```python

ops.modify_might([u], 4, duration=THIS_TURN)

```



<a id="card-0220"></a>

## 0220

反应法术；自身支付时忽略法盾，敌方Body单位−5本回合

subject:CostSelection=本次法术费用;change:CostChange=只忽略由Deflect产生的额外费用，其余费用保留;u:Unit=所选敌方Body单位

```python

# 费用入口
ops.modify_cost(subject, change, duration=UNTIL_EFFECT_END, uses=1)
# 结算
ops.modify_might([u], -5, duration=THIS_TURN)

```



<a id="card-0221"></a>

## 0221

迅捷法术；本牌不能被无效化，打敌方Calm4

restriction:RestrictionSpec=其他效果不能counter本me对应的链项;u:Unit=所选敌方Calm单位;dur:Duration=本法术作为链项存在期间

```python

# 链上持续限制
ops.restrict_action(me, restriction, duration=dur)
# 结算
ops.damage([u], 4)

```



<a id="card-0222"></a>

## 0222

选对手展示手牌，己方从中选Mind卡，由该对手回收

actor:Player=所选对手;hand:Selection[Card]=展示时其手牌;c:Card=从这批展示牌中选的Mind牌，由actor执行回收

```python

ops.reveal(hand)
ops.recycle([c])

```

ACTOR:recycle签名没有行动玩家参数，只能回拥有者牌堆，不能明确归属该对手执行的回收动作



<a id="card-0223"></a>

## 0223

杀敌方Chaos单位或装备，Chaos限制两种类型

c:Permanent=所选敌方Chaos单位或装备

```python

ops.kill([c])

```



<a id="card-0224"></a>

## 0224

传奇强化Energy2/任意Power2；基础主动Energy1横置活跃1装，强化后另有相同费用活跃2装的主动

ecost:Cost=Energy2/任意Power2及未强化条件;eb:CostBinding=强化基础费用;cost:Cost=Energy1及横置me;binding:CostBinding=选中的另一主动基础费用;gear:Selection[Gear]=选择基础主动时1件，选择已强化额外主动时2件，不删除原1件能力

```python

# 强化主动
paid = ops.pay(p, ecost, binding=eb)
if paid.value is not None:
    ops.empower([me])
# 所选的活跃装备主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.ready(gear)

```



<a id="card-0225"></a>

## 0225

反应法术；两名不同单位分别+2与−2本回合

u:Unit=加战力目标;v:Unit=另一减战力目标

```python

ops.modify_might([u], 2, duration=THIS_TURN)
ops.modify_might([v], -2, duration=THIS_TURN)

```

MODIFIER_BATCH:原句同一指令的两种修饰，API无明确原子批次边界，逐条登记是否暴露中间状态尚未约定



<a id="card-0226"></a>

## 0226

反应法术；目标印刷Energy≤4且Power≤1，两项都满足

spell:ChainItem=符合上述两项印刷费用上限的法术

```python

ops.counter(spell)

```



<a id="card-0227"></a>

## 0227

打出触发

 

```python

ops.gain_xp(p, 1)

```



<a id="card-0228"></a>

## 0228

一或多友方单位同批死亡触发一次

u:Unit=所选友方单位

```python

ops.buff([u])

```



<a id="card-0229"></a>

## 0229

固有部署；友方单位进攻此处时给其中一军+2；据守此处可回本装手牌

u:Unit=本批进攻此处友方单位中所选一名;origin:Zone=me场上区域

```python

# 进攻触发
ops.modify_might([u], 2, duration=THIS_TURN)
# 自己据守此处的可选触发
ops.transfer([me], origin, me.owner.hand)

```



<a id="card-0230"></a>

## 0230

待命法术；选择友方单位后选移动到open或若无open则游走本回合

u:Unit=所选友方单位;move_mode:bool=所选移动模式;b:Battlefield=所选open战场;none_open:bool=结算时没有任何open战场

```python

if move_mode:
    ops.move([u], b)
elif none_open:
    ops.grant_keyword([u], GANKING, duration=THIS_TURN)

```



<a id="card-0231"></a>

## 0231

回响Energy2；一遍效果打2战力沙兵

soldier:TokenTemplate=2战力SandSoldier;dest:Location=该遍合法目的地

```python

ops.play(soldier, p, origin=None, destination=dest)

```

REPEAT:无同一法术按已支付回响重复效果和分别定稿选择的明确接口



<a id="card-0232"></a>

## 0232

自身不能move到基地，但不阻止recall

restriction:RestrictionSpec=只禁止me的move目的地为base，不禁止召回

```python

ops.restrict_action(me, restriction, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0233"></a>

## 0233

杀装备，其死亡前控制者抽2

g:Gear=所选装备;actor:Player=g控制者的死亡前快照

```python

ops.kill([g])
ops.draw(actor, 2)

```



<a id="card-0234"></a>

## 0234

固有部署；打出可杀另一友方单位/装备作为费抽1；此处友方绝念额外一次

cost:Cost=杀所选另一友方单位或装备;binding:CostBinding=可选打出触发基础费用;triggers:TriggerSelection=此处友方Deathknell能力

```python

# 打出触发
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.draw(p, 1)
# 持续
ops.modify_trigger_count(triggers, 1, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0235"></a>

## 0235

此处对决开始可付Energy1以洞察，再展示顶牌，是法术则抽取；按勘误to为触发费

cost:Cost=Energy1;binding:CostBinding=可选对决触发基础费用;top:Card=洞察后新的己方主牌堆顶，不预先冻结;spell:bool=该top含spell类型

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.predict(p)
    ops.reveal([top])
    if spell:
        ops.draw(p, 1, cards=[top])

```



<a id="card-0236"></a>

## 0236

固有伏击；每次p打出法术后

 

```python

ops.modify_might([me], 2, duration=THIS_TURN)

```



<a id="card-0237"></a>

## 0237

有另一己方Dragon则活跃入场

entry:EntryState=定稿时p控制另一Dragon则活跃，否则默认;dest:Location=合法目的地

```python

ops.play(me, p, origin=p.hand, destination=dest, entry=entry)

```



<a id="card-0238"></a>

## 0238

打出后可杀任意装备

g:Gear=所选装备

```python

ops.kill([g])

```



<a id="card-0239"></a>

## 0239

待命；自己位于战场且恰有一其他己军时坚守3

params:KeywordParameters=Shield.value为3;dur:Duration=me留场、在战场且该处其他己军恰1期间

```python

ops.grant_keyword([me], SHIELD, parameters=params, duration=dur)

```



<a id="card-0240"></a>

## 0240

反应法术

u:Unit=所选任意单位

```python

ops.modify_might([u], 2, duration=THIS_TURN)
ops.draw(p, 1)

```



<a id="card-0241"></a>

## 0241

迅捷法术；打3战场单位，若因此死亡则自反项抽1

u:Unit=所选战场单位

```python

ops.damage([u], 3)

```

REFLEXIVE:勘误if this kills it do this要求后续独立抽牌链项，不能直接凭damage回执在同一项抽牌



<a id="card-0242"></a>

## 0242

无其他己军时活跃入场；固有缴械2

entry:EntryState=定稿时p没有其他单位则活跃，否则默认;dest:Location=合法打出地点

```python

ops.play(me, p, origin=p.hand, destination=dest, entry=entry)

```



<a id="card-0243"></a>

## 0243

反应法术；模式为对手废牌总计至多3由各拥有者回收，或抽1

recycle_mode:bool=选择回收模式;cards:Selection[Card]=对手废牌堆合并至多3所选牌

```python

if recycle_mode:
    ops.recycle(cards)
else:
    ops.draw(p, 1)

```

ACTOR:回收动作须分别归属各拥有者，recycle无行动玩家参数，不能仅凭目的牌堆正确认定动作归属已覆盖



<a id="card-0244"></a>

## 0244

每玩家保留自己2单位/2装备/2符文/2手牌，其余同时回收

actors:Selection[Player]=全体玩家;units:dict[Player,Selection[Unit]]=各玩家己方单位;gear:dict[Player,Selection[Gear]]=各玩家己装;runes:dict[Player,Selection[Rune]]=各玩家己符文;hands:dict[Player,Selection[Card]]=各玩家手牌;rest:Selection[Card]=完成所有选择后各对应区域中未保留的牌，非该类别对象不自行加入

```python

for actor in actors:
    ops.choose(actor, units[actor], minimum=2, maximum=2, targeting=False, bind_at="resolution")
    ops.choose(actor, gear[actor], minimum=2, maximum=2, targeting=False, bind_at="resolution")
    ops.choose(actor, runes[actor], minimum=2, maximum=2, targeting=False, bind_at="resolution")
    ops.choose(actor, hands[actor], minimum=2, maximum=2, targeting=False, bind_at="resolution")
ops.recycle(rest)

```

CHOICE_SHORTAGE:choose未规定候选不足minimum时效果中的尽可能选择；不能把恰选2变成可选0，也不能假定会自动放宽minimum



<a id="card-0245"></a>

## 0245

预知打出洞察1；迅捷主动杀自己并横置，单位+2本回合

cost:Cost=杀me及横置me的同一合法基础费用组合;binding:CostBinding=迅捷主动基础费用;u:Unit=所选单位

```python

# 预知打出触发
ops.predict(p)
# 迅捷主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_might([u], 2, duration=THIS_TURN)

```



<a id="card-0246"></a>

## 0246

部署；打出放逐此处单位并关联；据守杀自己作费用，由p免费打关联卡

u:Unit=此处所选单位;link:Link=本实例本次放逐关联;cost:Cost=杀me;binding:CostBinding=据守触发基础费用;c:Card=关联中仍可打的实体卡，消失的衍生物不冒充Card;dest:Location=合法打出地点

```python

# 打出触发
ops.banish([u], link=link)
# 据守触发
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.play(c, p, origin=c.owner.banishment, destination=dest, cost_policy=IGNORE_BASE_COST)

```



<a id="card-0247"></a>

## 0247

迅捷法术；单位本回合战力翻倍并获任意Power2活跃自己的主动

u:Unit=所选单位;m:IntExpr=执行时u战力快照，翻倍用同量加值;ability:Ability=下方受授主动代码块，普通主动，基础费用任意Power2，无横置;actor:Player=受授能力发动时u控制者;cost:Cost=任意Power2;binding:CostBinding=受授主动基础费用

```python

# 法术结算
ops.modify_might([u], m, duration=THIS_TURN)
ops.grant_ability([u], ability, duration=THIS_TURN)
# 受授主动能力的独立执行体
paid = ops.pay(actor, cost, binding=binding)
if paid.value is not None:
    ops.ready([u])

```



<a id="card-0248"></a>

## 0248

武装+2；装配Body1

cost:Cost=Body1;binding:CostBinding=装配主动基础费用;u:Unit=所选己军

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)

```



<a id="card-0249"></a>

## 0249

武装+1；装配Chaos1；效果区宿主征服弃1再抽1

cost:Cost=Chaos1;binding:CostBinding=装配主动基础费用;u:Unit=所选己军

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 宿主征服入口
ops.discard(p, 1)
ops.draw(p, 1)

```

DATA:SC及一组EN印刷缺printedEffectText中的弃抽



<a id="card-0250"></a>

## 0250

武装+1；装配Calm1；效果区宿主壁垒

cost:Cost=Calm1;binding:CostBinding=装配主动基础费用;u:Unit=所选己军;host:Selection[Unit]=当前宿主;dur:Duration=本装备贴附期间

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 效果区持续
ops.grant_keyword(host, TANK, duration=dur)

```

DATA:SC缺printedEffectText中的壁垒



<a id="card-0251"></a>

## 0251

回响Energy2；看3可展示单位抽取，余回收

take:bool=选择抽单位;c:Card=实际看见牌中所选单位;rest:Selection[Card]=看见牌中未抽取者，未选则全部

```python

ops.look(p, p.main_deck, 3)
if take:
    ops.reveal([c])
    ops.draw(p, 1, cards=[c])
ops.recycle(rest)

```

REPEAT:只能表达单遍，未定义回响各遍定稿与执行



<a id="card-0252"></a>

## 0252

反应/回响Energy2

 

```python

ops.draw(p, 1)

```

REPEAT:缺回响重复效果的明确组合；一次draw不能证明额外付费路径覆盖



<a id="card-0253"></a>

## 0253

所有单位及装备同时回各拥有者手牌

u:Permanent=符合对象集合中的一个，仅局部片段;origin:Zone=u场上区域

```python

ops.transfer([u], origin, u.owner.hand)

```

BATCH:不同玩家和场上区域的统一同时回手无对应批次参数



<a id="card-0254"></a>

## 0254

战力动态+己废牌数；自己开始阶段回收废牌3

n:IntExpr=动态p废牌数量;cards:Selection[Card]=己废牌选择3，不足时尽可能执行

```python

# 持续
ops.modify_might([me], n, duration=WHILE_SOURCE_PRESENT)
# 自己开始阶段
ops.recycle(cards)

```



<a id="card-0255"></a>

## 0255

迅捷；从非手牌打出Energy−2；杀战场单位

subject:CostSelection=本次me打出费用;change:CostChange=Energy减2;dur:Duration=本次打出来源不是手牌时的费用计算期间;u:Unit=所选战场单位

```python

# 费用
ops.modify_cost(subject, change, duration=dur)
# 法术结算
ops.kill([u])

```



<a id="card-0256"></a>

## 0256

单位本回合基础战力5；流转Energy3

u:Unit=所选单位

```python

ops.set_base_might([u], 5, duration=THIS_TURN)

```

FLOW_EXIT:缺流转链项离链放逐替代，不能以法术成功执行后的banish替代全流程



<a id="card-0257"></a>

## 0257

任意玩家打Dragon可选额外Power2；若付则必须打此战场

dragons:CostSelection=任意玩家的Dragon打出费用;extra:CostChange=来自本战场的可选任意Power2额外费用

```python

ops.modify_cost(dragons, extra, duration=WHILE_SOURCE_PRESENT)

```

COST_DESTINATION:缺将特定额外费选择与该次必须目的地me绑定的明确结构；仅grant_permission增加可选地点不等于付后强制去该处



<a id="card-0258"></a>

## 0258

单位反应产费，横置产Energy1

cost:Cost=横置me;binding:CostBinding=反应产费主动基础费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.add_resources(p, ResourceBundle(energy=1))

```



<a id="card-0259"></a>

## 0259

先移动敌军，再自反项选目的地另一敌军互殴

u:Unit=所选敌军;dest:Location=其合法移动目的地

```python

ops.move([u], dest)

```

REFLEXIVE:勘误then do this要求新待处理项与后选目标；RECIPROCAL:两单位同时按各自战力互殴也缺多来源批次



<a id="card-0260"></a>

## 0260

打出展示各对手顶牌，选1放逐免费由p打，余回收

tops:Selection[Card]=各对手主牌堆顶牌;c:Card=其中选一;rest:Selection[Card]=未选展示牌;dest:Location/Zone=所选牌合法目的地

```python

ops.reveal(tops)
ops.banish([c])
ops.play(c, p, origin=c.owner.banishment, destination=dest, cost_policy=IGNORE_BASE_COST)
ops.recycle(rest)

```



<a id="card-0261"></a>

## 0261

绝念

 

```python

ops.predict(p, 2)

```



<a id="card-0262"></a>

## 0262

固有法盾；每回合首次赢战斗得1；战斗中死亡让选对手得1

actor:Player=死亡触发所选对手

```python

# 首次赢战斗
ops.gain_points(p, 1)
# 战斗中死亡
ops.gain_points(actor, 1)

```



<a id="card-0263"></a>

## 0263

战力动态加己分数

n:IntExpr=p当前分数，持续更新

```python

ops.modify_might([me], n, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0264"></a>

## 0264

赢战斗产金币；进攻防守可Fury1换本回合+2，按勘误to为触发费

gold:TokenTemplate=金币;entry:EntryState=休眠;cost:Cost=Fury1;binding:CostBinding=可选进攻/防守触发基础费用

```python

# 赢战斗
ops.play(gold, p, origin=None, destination=p.base, entry=entry)
# 进攻/防守
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_might([me], 2, duration=THIS_TURN)

```



<a id="card-0265"></a>

## 0265

抽1；流转Energy2

 

```python

ops.draw(p, 1)

```

FLOW_EXIT:从废牌替代费用可写，离链放逐替代不能完整登记



<a id="card-0266"></a>

## 0266

打出时控制装备≥2则活跃自身

 

```python

ops.ready([me])

```



<a id="card-0267"></a>

## 0267

固有法盾；可杀一友方单位作为打出额外费，付后Energy−2

cost:Cost=杀所选友方单位;binding:CostBinding=可选打出额外费用;subject:CostSelection=本次me费用;change:CostChange=Energy减2

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_cost(subject, change, duration=UNTIL_EFFECT_END, uses=1)

```



<a id="card-0268"></a>

## 0268

进攻且此处有活跃敌军则本回合+2，按勘误补持续期

 

```python

ops.modify_might([me], 2, duration=THIS_TURN)

```



<a id="card-0269"></a>

## 0269

只在p于此处分配战斗伤害时忽略Tank；不使敌军失去Tank

 

```python

# 不调用suppress_ability移除Tank，也不授予自己Tank

```

RULE_NARROW:modify_rule的COMBAT_DAMAGE_ORDER仅列先/正常/后，未定义只对某分配玩家忽略Tank而保留其他顺序约束的变更



<a id="card-0270"></a>

## 0270

自己手牌≤2活跃入场；自身据守抽2

entry:EntryState=实际进场检查时p手牌≤2则活跃，否则默认;dest:Location=合法地点

```python

# 基础打出
ops.play(me, p, origin=p.hand, destination=dest, entry=entry)
# 据守
ops.draw(p, 2)

```



<a id="card-0271"></a>

## 0271

p在此处防守触发，给此处己军壁垒本次战斗

u:Unit=此处所选己军

```python

ops.grant_keyword([u], TANK, duration=THIS_COMBAT)

```



<a id="card-0272"></a>

## 0272

自己开始阶段得分前，可杀此处己军为触发费用抽1

cost:Cost=杀所选此处己方单位;binding:CostBinding=可选开始阶段触发基础费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.draw(p, 1)

```



<a id="card-0273"></a>

## 0273

在战场时自己打出法术Energy−1最低1

spells:CostSelection=p的法术打出费用;change:CostChange=Energy减1最低1;dur:Duration=me留场且在战场

```python

ops.modify_cost(spells, change, duration=dur)

```



<a id="card-0274"></a>

## 0274

无条件活跃入场

dest:Location=合法打出地点;entry:EntryState=活跃

```python

ops.play(me, p, origin=p.hand, destination=dest, entry=entry)

```



<a id="card-0275"></a>

## 0275

反应法术

u:Unit=所选单位

```python

ops.modify_might([u], -4, duration=THIS_TURN)
ops.predict(p)

```



<a id="card-0276"></a>

## 0276

固有急速；移动后己方符文≤4则抽1

 

```python

ops.draw(p, 1)

```



<a id="card-0277"></a>

## 0277

实际成功眩晕一敌军后，活跃自身并本回合+1

 

```python

ops.ready([me])
ops.modify_might([me], 1, duration=THIS_TURN)

```



<a id="card-0278"></a>

## 0278

武装+2待命；盖放打出免费贴附；普通装配Chaos1

u:Unit=本次打出触发所选己军，范围按Hidden规则及勘误here提醒；普通装配可正常己军;cost:Cost=Chaos1;binding:CostBinding=普通装配主动基础费用

```python

# 从盖放打出触发
ops.attach(me, u)
# 普通装配主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)

```



<a id="card-0279"></a>

## 0279

固有游走；打出强制额外将友方单位回其拥有者手牌

cost:Cost=所选友方单位回拥有者手牌;binding:CostBinding=本次打出强制额外费用

```python

ops.pay(p, cost, binding=binding)

```



<a id="card-0280"></a>

## 0280

固有急速；死亡后以回收自身为绝念基础费用活跃己方全部符文

cost:Cost=回收本次死亡关联的自身牌;binding:CostBinding=绝念触发基础费用；在能力定稿时支付;runes:Selection[Rune]=执行时己方全部符文

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    pass  # Rune不符合ready的Permanent参数类型

```

RUNE_READY:规则133.5.a.1/161.1.a明确Rune不是Permanent，ready签名不能接受该符文集合



<a id="card-0281"></a>

## 0281

活跃入场/固有强攻1；迅捷主动弃1及Energy1/Fury1放逐自身再免费打自己基地

dest:Location=基础打出的合法地点;entry:EntryState=活跃;cost:Cost=弃1及Energy1/Fury1;binding:CostBinding=迅捷主动基础费用

```python

# 基础打出
ops.play(me, p, origin=p.hand, destination=dest, entry=entry)
# 迅捷主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.banish([me])
    ops.play(me, p, origin=me.owner.banishment, destination=p.base, cost_policy=IGNORE_BASE_COST, entry=entry)

```



<a id="card-0282"></a>

## 0282

己方正伤害对敌军足以致死；打出每地点至多1敌军各打1

scope:RuleScope=由p负责的伤害对敌军;policy:RuleChange=任何正伤害视为致死，0不算;units:Selection[Unit]=各场上地点至多一名所选敌军

```python

# 持续
ops.modify_rule(LETHAL_DAMAGE_POLICY, scope, policy, duration=WHILE_SOURCE_PRESENT)
# 打出触发
ops.damage(units, 1)

```



<a id="card-0283"></a>

## 0283

待命；打出给一友方单位+3本回合，再从盖放则回收自身；勘误允许自己

u:Unit=所选友方单位，可包括me;from_hidden:bool=本次实际从盖放打出

```python

ops.modify_might([u], 3, duration=THIS_TURN)
if from_hidden:
    ops.recycle([me])

```



<a id="card-0284"></a>

## 0284

p从待命状态打出牌后+2；本单位本身没有待命

 

```python

ops.modify_might([me], 2, duration=THIS_TURN)

```



<a id="card-0285"></a>

## 0285

自身据守后

gold:TokenTemplate=金币;entry:EntryState=休眠

```python

for i in range(2):
    ops.play(gold, p, origin=None, destination=p.base, entry=entry)

```



<a id="card-0286"></a>

## 0286

沙兵获百炼；本回合已打武装才能Energy1横置传奇打沙兵基地

soldiers:Selection[Card]=动态己方SandSoldier，须在打出触发能力可生效的区域授权;cost:Cost=Energy1及横置me;binding:CostBinding=本回合已打Equipment才能发动的主动基础费用;soldier:TokenTemplate=2战力SandSoldier

```python

# 持续
ops.grant_keyword(soldiers, WEAPONMASTER, duration=WHILE_SOURCE_PRESENT)
# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.play(soldier, p, origin=None, destination=p.base)

```

LANG:两组EN分别写Your Sand Soldiers与Sand Soldiers you play，控制与打出历史范围未完全相同，未用同一选择器抹平



<a id="card-0287"></a>

## 0287

征服此处，可Energy1加此处己军回手为触发费用，在此处打2战力沙兵

cost:Cost=Energy1及所选此处己军回拥有者手牌;binding:CostBinding=按勘误to的可选征服触发基础费用;soldier:TokenTemplate=2战力SandSoldier

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.play(soldier, p, origin=None, destination=here)

```



<a id="card-0288"></a>

## 0288

待命/迅捷法术；选择某战场任选友军回其基地，使用move而非recall

units:Selection[Unit]=所选友方单位含队友，同一战场任意数量；各自控制者基地不同;destinations:dict[Unit,Location]=各单位控制者基地

```python

for unit in units:
    ops.move([unit], destinations[unit])

```

MOVE_BATCH:友方含盟友，单位可能须去不同控制者基地，单目的move不能保证同一移动批次



<a id="card-0289"></a>

## 0289

强化状态提醒物，不是发动能力

 

```python

# 不对提醒物自身调用empower；只保存其规则说明

```

DATA:SC文本仍是英文，不视为已提供中文翻译



<a id="card-0290"></a>

## 0290

反应法术，先友方单位+1，再若此地仅此一友方单位则另+1

u:Unit=所选友方单位;alone:bool=第二步判断时该地只有该一名p单位

```python

ops.modify_might([u], 1, duration=THIS_TURN)
if alone:
    ops.modify_might([u], 1, duration=THIS_TURN)

```



<a id="card-0291"></a>

## 0291

从四模式选两个；按既定顺序执行，不自作重复选同模式

modes:list[int]=本次所选两模式及执行顺序，0伤害/1随从/2战力/3看牌;u:Unit=模式0所选任意单位;recruit:TokenTemplate=1战力Recruit;destinations:list[Location]=模式1两随从各自合法地点;units:Selection[Unit]=模式2至多2单位;c:Card=模式3实际看见顶2中抽取者;rest:Selection[Card]=模式3未抽取的实际看见牌

```python

for mode in modes:
    if mode == 0:
        ops.damage([u], 2)
    elif mode == 1:
        for dest in destinations:
            ops.play(recruit, p, origin=None, destination=dest)
    elif mode == 2:
        ops.modify_might(units, 1, duration=THIS_TURN)
    else:
        ops.look(p, p.main_deck, 2)
        ops.draw(p, 1, cards=[c])
        ops.recycle(rest)

```



<a id="card-0292"></a>

## 0292

打出放逐己手牌废牌再燃烧7；持续跳抽牌阶段，允许打废牌；非主牌堆进入废牌改放逐

cards:Selection[Card]=己方手牌和废牌并集;subjects:PermissionSelection=p可从废牌打出的卡;permit:PermissionSpec=从己方废牌正常付费打出，不改变时机目的地

```python

# 打出触发
ops.banish(cards)
ops.burn(p, 7)
# 持续
ops.skip_procedure(p, DRAW_PHASE, occurrence="all", duration=WHILE_SOURCE_PRESENT)
ops.grant_permission(subjects, permit, duration=WHILE_SOURCE_PRESENT)

```

REPLACE:缺原区域不是主牌堆时进入己废牌改放逐的通用区域事件替代登记



<a id="card-0293"></a>

## 0293

装备反应产费，横置产Energy1

cost:Cost=横置me;binding:CostBinding=反应产费主动基础费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.add_resources(p, ResourceBundle(energy=1))

```



<a id="card-0294"></a>

## 0294

固有狩猎1；主动消耗XP2增益自己

cost:Cost=消耗XP2;binding:CostBinding=主动基础费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.buff([me])

```



<a id="card-0295"></a>

## 0295

固有后排；据守时给此处所有单位增益，不限己方

units:Selection[Unit]=此处全体单位

```python

ops.buff(units)

```



<a id="card-0296"></a>

## 0296

可选活跃入场，若实际如此则该回合不能move

dest:Location=合法打出地点;entry:EntryState=玩家选择活跃或默认状态;entered_ready:bool=该可选入场替代实际生效；不只愿望;restriction:RestrictionSpec=禁止me本回合执行move，不禁止recall

```python

# 基础打出
ops.play(me, p, origin=p.hand, destination=dest, entry=entry)
# 实际选择活跃入场的入场条件入口
if entered_ready:
    ops.restrict_action(me, restriction, duration=THIS_TURN)

```



<a id="card-0297"></a>

## 0297

留场己军持续+2；p打出单位后杀本装备

units:Selection[Unit]=动态全体己军

```python

# 持续
ops.modify_might(units, 2, duration=WHILE_SOURCE_PRESENT)
# 打出单位触发
ops.kill([me])

```



<a id="card-0298"></a>

## 0298

强化以杀友方单位为主动费；强化持续+2

cost:Cost=杀所选友方单位;binding:CostBinding=仅未强化时的强化主动基础费用;dur:Duration=me留场且强化

```python

# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 持续
ops.modify_might([me], 2, duration=dur)

```



<a id="card-0299"></a>

## 0299

己符文≥7时，持续预防敌方法术和技能对自身全部伤害

enemies:Predicate=伤害来源为敌方法术或技能;dur:Duration=me留场且p符文≥7

```python

ops.prevent_damage([me], INFINITY, source_filter=enemies, duration=dur)

```



<a id="card-0300"></a>

## 0300

固有伏击；p从盖放打牌后活跃自身并本回合+1

 

```python

ops.ready([me])
ops.modify_might([me], 1, duration=THIS_TURN)

```



<a id="card-0301"></a>

## 0301

固有待命/后排；己回合从盖放打出后，可拉其他地点敌军到me战场

u:Unit=所选不同地点敌军

```python

ops.move([u], here)

```



<a id="card-0302"></a>

## 0302

固有缴械；据守且此处有己方盖放牌则额外得1

 

```python

ops.gain_points(p, 1)

```



<a id="card-0303"></a>

## 0303

打出触发；弃置不足也继续抽牌

 

```python

ops.discard(p, 1)
ops.draw(p, 1)

```



<a id="card-0304"></a>

## 0304

p打部署装备后，可横置传奇付任意Power1，移友方单位到该装战场

cost:Cost=横置me及任意Power1;binding:CostBinding=可选部署装备打出触发基础费用;u:Unit=所选友方单位;b:Battlefield=该部署装备实际打出的战场

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.move([u], b)

```



<a id="card-0305"></a>

## 0305

迅捷/回响Energy2；进攻敌军若已经晕则改回手，否则晕

u:Unit=所选进攻方敌军;already:bool=该步骤执行前u已眩晕;origin:Zone=u场上区域

```python

if already:
    ops.transfer([u], origin, u.owner.hand)
else:
    ops.stun([u])

```

REPEAT:只覆盖单遍条件效果，回响重复与各遍目标选择未提供调度



<a id="card-0306"></a>

## 0306

武装+1；装配Mind1；效果区令宿主有Mech标签

cost:Cost=Mind1;binding:CostBinding=装配主动基础费用;u:Unit=己方宿主;host:Selection[Unit]=当前宿主;tags:set[Tag]=仅Mech标签;dur:Duration=仍贴附本装备期间

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 宿主效果
ops.set_tags(host, tags, mode="add", duration=dur)

```

DATA:SC没有printedEffectText的宿主Mech



<a id="card-0307"></a>

## 0307

据守后，三个Bomb打到同一战场，部署是Bomb模板属性

bomb:TokenTemplate=完整Bomb模板;b:Battlefield=本次三个共用所选战场

```python

for i in range(3):
    ops.play(bomb, p, origin=None, destination=b)

```



<a id="card-0308"></a>

## 0308

武装+0；装配Order1；效果区宿主移动后在新地点打随从

cost:Cost=Order1;binding:CostBinding=装配主动基础费用;u:Unit=己方宿主;recruit:TokenTemplate=1战力Recruit;location:Location=宿主移动结束地点

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 宿主移动触发
ops.play(recruit, p, origin=None, destination=location)

```

DATA:SC及一组EN缺printedEffectText的宿主移动产随从



<a id="card-0309"></a>

## 0309

传奇迅捷主动横置给友方单位壁垒本回合

cost:Cost=横置me;binding:CostBinding=迅捷主动基础费用;u:Unit=友方所选单位

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.grant_keyword([u], TANK, duration=THIS_TURN)

```



<a id="card-0310"></a>

## 0310

进攻/防守按自身战力打此处敌军；不能造成战斗伤害；迅捷Mind1移己基地

u:Unit=此处所选敌军;m:IntExpr=me结算时战力;restriction:RestrictionSpec=只禁止me作为来源造成战斗伤害，不禁止该攻击触发伤害;cost:Cost=Mind1;binding:CostBinding=迅捷主动基础费用

```python

# 持续
ops.restrict_action(me, restriction, duration=WHILE_SOURCE_PRESENT)
# 进攻/防守触发
ops.damage([u], m)
# 迅捷主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.move([me], p.base)

```



<a id="card-0311"></a>

## 0311

打出弃1抽2；p支付的可选额外费用减少Energy1或任意Power1

subjects:CostSelection=p支付的每项可选额外费用;change:CostChange=对该项费用选Energy减1或任意Power减1，不能两个都减

```python

# 打出触发
ops.discard(p, 1)
ops.draw(p, 2)
# 持续费用修饰
ops.modify_cost(subjects, change, duration=WHILE_SOURCE_PRESENT)

```

LANG:SC普通版限其他卡牌，另一SC版及EN未作此限制，不能把可选费用范围合一



<a id="card-0312"></a>

## 0312

待命/迅捷法术；同战场一友方单位一敌军都眩晕

u:Unit=友方单位;v:Unit=与u同战场敌军

```python

ops.stun([u, v])

```



<a id="card-0313"></a>

## 0313

迅捷法术，任意装备回拥有者手牌

g:Gear=所选装备;origin:Zone=g当前场上区域

```python

ops.transfer([g], origin, g.owner.hand)

```



<a id="card-0314"></a>

## 0314

赋战场单位或任意装备瞬息；不限己方

c:Permanent=所选合法战场单位或装备

```python

ops.grant_keyword([c], TEMPORARY, duration=PERMANENT)

```



<a id="card-0315"></a>

## 0315

打出至多4友方单位增益；每次消耗一增益后打一休眠金币

units:Selection[Unit]=至多4友方所选单位;gold:TokenTemplate=金币;entry:EntryState=休眠

```python

# 打出
ops.buff(units)
# 每个实际增益消耗事件
ops.play(gold, p, origin=None, destination=p.base, entry=entry)

```



<a id="card-0316"></a>

## 0316

移到战场后可Chaos1将一己军移到该战场

cost:Cost=Chaos1;binding:CostBinding=可选移动触发基础费用;u:Unit=EN所选任一己军，包含me合法选择的可能;b:Battlefield=本次移动结束战场

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.move([u], b)

```

LANG:SC要求另一单位，EN没有排除自身，目标选择集合不同



<a id="card-0317"></a>

## 0317

打出后此处打随从

recruit:TokenTemplate=1战力Recruit

```python

ops.play(recruit, p, origin=None, destination=here)

```



<a id="card-0318"></a>

## 0318

打出宣告法术名；在战场时对手不能打该名法术

names:list[CardName]=规则允许的法术名称集合;opponents:PermissionSelection=所有对手;restriction:RestrictionSpec=禁止打出本次declare绑定名称的spell；同名非spell不扩大禁止;dur:Duration=me留场且在战场

```python

# 打出触发
ops.declare(p, names)
# 依赖该实例本次宣告值的持续限制
ops.restrict_action(opponents, restriction, duration=dur)

```



<a id="card-0319"></a>

## 0319

迅捷法术

u:Unit=所选战场单位

```python

ops.damage([u], 6)

```



<a id="card-0320"></a>

## 0320

按勘误两条独立伤害指令；不再按印刷do twice建立自反项

first:Unit=第一条所选单位;second:Unit=第二条所选单位，可相同

```python

ops.damage([first], 3)
ops.damage([second], 3)

```



<a id="card-0321"></a>

## 0321

本回合接下3次p打单位时各抽1

 

```python

# 以下仅未来触发的执行体，尚未登记
ops.draw(p, 1)

```

DELAY:缺创建本回合限3次的未来打出单位触发接口，不能结算时立即draw3



<a id="card-0322"></a>

## 0322

打出看4，可展示Energy≥4法术抽取，余回收

take:bool=选择抽牌;c:Card=实际看4中所选印刷Energy≥4法术;rest:Selection[Card]=实际看见未抽取者，无选择则全部

```python

ops.look(p, p.main_deck, 4)
if take:
    ops.reveal([c])
    ops.draw(p, 1, cards=[c])
ops.recycle(rest)

```



<a id="card-0323"></a>

## 0323

反应/回响Energy2；单遍给单位+2本回合

u:Unit=所选单位

```python

ops.modify_might([u], 2, duration=THIS_TURN)

```

REPEAT:未定义回响重复/每遍定稿选择完整流程



<a id="card-0324"></a>

## 0324

绝念打两个3战力Mech基地

mech:TokenTemplate=3战力Mech

```python

for i in range(2):
    ops.play(mech, p, origin=None, destination=p.base)

```



<a id="card-0325"></a>

## 0325

打出触发

u:Unit=所选单位

```python

ops.modify_might([u], 3, duration=THIS_TURN)

```



<a id="card-0326"></a>

## 0326

待命/迅捷法术；战场任意单位move回其基地

u:Unit=战场所选单位;base:Location=u对应基地

```python

ops.move([u], base)

```



<a id="card-0327"></a>

## 0327

迅捷法术

u:Unit=所选任意单位

```python

ops.damage([u], 8)

```



<a id="card-0328"></a>

## 0328

任一对手距胜利≤3则Energy−2；结算抽1并召1休眠

subject:CostSelection=本次me费用;change:CostChange=Energy减2;dur:Duration=费用计算时存在距胜利≤3的对手

```python

# 费用
ops.modify_cost(subject, change, duration=dur)
# 结算
ops.draw(p, 1)
ops.channel(p, 1, exhausted=True)

```



<a id="card-0329"></a>

## 0329

自身一对一进攻/防守触发，战力翻倍本战斗

m:IntExpr=该触发执行时me战力快照；不是基础战力

```python

ops.modify_might([me], m, duration=THIS_COMBAT)

```



<a id="card-0330"></a>

## 0330

自身为Mighty期间法盾游走坚守1；阈值状态而非变强力永久触发

dur:Duration=me留场且当前战力≥5期间

```python

ops.grant_keyword([me], DEFLECT, duration=dur)
ops.grant_keyword([me], GANKING, duration=dur)
ops.grant_keyword([me], SHIELD, duration=dur)

```



<a id="card-0331"></a>

## 0331

p单位实际跨阈值变Mighty，可Order1使同一单位活跃

cost:Cost=Order1;binding:CostBinding=可选变强力触发基础费用;u:Unit=本次从<5变为≥5的己方单位

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.ready([u])

```



<a id="card-0332"></a>

## 0332

传奇反应产费，横置产通用Power1，限打装备/用装备技能

cost:Cost=横置me;binding:CostBinding=反应产费基础费用;bundle:ResourceBundle=通用Power1;restriction:Predicate=只支付打出装备或使用装备能力费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.add_resources(p, bundle, restriction=restriction)

```



<a id="card-0333"></a>

## 0333

自身活跃入场；打出活跃全敌军；其他单位活跃入场；所有单位唤醒阶段不活跃

dest:Location=合法打出地点;entry:EntryState=活跃;enemies:Selection[Unit]=全体敌军;units:PermissionSelection=全部玩家单位;restriction:RestrictionSpec=仅在AwakenPhase不能执行ready，不跳过其他阶段/其他对象

```python

# 基础打出
ops.play(me, p, origin=p.hand, destination=dest, entry=entry)
# 打出触发
ops.ready(enemies)
# 持续唤醒限制
ops.restrict_action(units, restriction, duration=WHILE_SOURCE_PRESENT)

```

ENTRY:缺使未来其他单位包括生成均活跃入场的持续修饰；单次play.entry不覆盖全局



<a id="card-0334"></a>

## 0334

征服此处后，本回合下一打出单位获得急速

 

```python

# 无可在当前时点安全授予的确定单位实例

```

NEXT_ABILITY:grant_keyword没有下一次打出绑定或uses，无法在下一单位定稿前仅赋其急速，不应先猜一张手牌



<a id="card-0335"></a>

## 0335

法术对所选战场所有敌军打3

units:Selection[Unit]=所选战场全敌军

```python

ops.damage(units, 3)

```



<a id="card-0336"></a>

## 0336

打出让另一单位活跃，不限己方

u:Unit=除me外所选任意单位

```python

ops.ready([u])

```



<a id="card-0337"></a>

## 0337

打出可从己废牌打Energy≤3法术，仅忽略Energy，随后回收该法术

c:Card=己废牌中印刷Energy≤3法术;policy:CostPolicy=仅忽略Energy；其Power与其他费用保留;permit:PlayPermission=本触发允许该废牌打出;chain:Zone=该法术应进入的链区域

```python

ops.play(c, p, origin=p.trash, destination=chain, cost_policy=policy, permission=permit)

```

CHAIN_EXIT:then recycle it是离链回收的延迟替代，不能在play只完成定稿时马上recycle未执行法术，也不能只处理成功结算漏无效化



<a id="card-0338"></a>

## 0338

自身被弃置后，可Fury1将此牌打出

cost:Cost=Fury1;binding:CostBinding=可选被弃触发基础费用;dest:Location=合法单位目的地;permit:PlayPermission=仅本触发允许从己废牌打该me

```python

# 仅记录支持的付款片段；不错误重复收取印刷基础费用
ops.pay(p, cost, binding=binding)

```

PLAY_COST:原句pay Fury to play的成本在该触发与后续牌打出基础费之间的精确定稿角色未由API明确；不能默认付Fury后还再付印刷Energy3



<a id="card-0339"></a>

## 0339

反应法术，至多2友军move回基地

units:Selection[Unit]=所选友方单位含队友，任意地点至多2；各自控制者基地不同;destinations:dict[Unit,Location]=各单位控制者基地

```python

for unit in units:
    ops.move([unit], destinations[unit])

```

LANG:SC仅允许战场上的己军，EN/TC未加该来源限制

MOVE_BATCH:友方含盟友，单位可能须去不同控制者基地，单目的move不能保证同一移动批次



<a id="card-0340"></a>

## 0340

反应法术，对全部战场单位打1，所有玩家

units:Selection[Unit]=所有战场上的所有单位

```python

ops.damage(units, 1)

```



<a id="card-0341"></a>

## 0341

反应法术；选无效化或打4个1战力法盾Bird

counter_mode:bool=所选无效化模式;spell:ChainItem=所选法术;bird:TokenTemplate=完整1战力带Deflect的Bird;destinations:list[Location]=四Bird各自合法地点

```python

if counter_mode:
    ops.counter(spell)
else:
    for dest in destinations:
        ops.play(bird, p, origin=None, destination=dest)

```



<a id="card-0342"></a>

## 0342

反应法术，某战场友方单位本回合坚守2

units:Selection[Unit]=选定战场的全部友方单位;params:KeywordParameters=Shield.value为2

```python

ops.grant_keyword(units, SHIELD, parameters=params, duration=THIS_TURN)

```



<a id="card-0343"></a>

## 0343

法术活跃单位；在废牌时p打Energy≥7牌后可替代Energy1/Fury2打出并登记放逐

u:Unit=所选单位;chain:Zone=链区域;policy:CostPolicy=基础费替代为Energy1/Fury2;permit:PlayPermission=仅该废牌触发允许重打本me

```python

# 正常法术结算
ops.ready([u])
# 废牌区域触发的打出片段
ops.play(me, p, origin=p.trash, destination=chain, cost_policy=policy, permission=permit)

```

CHAIN_EXIT:勘误then banish this须与该次废牌重打关联的离链放逐替代，缺登记接口



<a id="card-0344"></a>

## 0344

此处单位独自防守期间战力−2，不限自己一方

units:Selection[Unit]=动态此处正独自防守的单位；独自按该单位友方数量判定

```python

ops.modify_might(units, -2, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0345"></a>

## 0345

己方Mech在所有相关区域有预知，必须赶在其打出效果捕获前生效

mechs:Selection[Card]=动态己方Mech，含me；相关区域按Vision打出触发生效规则

```python

ops.grant_keyword(mechs, VISION, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0346"></a>

## 0346

控制此战场时友方传奇获得横置后免费贴己方武装到己军的主动

legends:Selection[Card]=当前战场控制者的友方传奇，Legend按Card上界绑定;ability:Ability=下方受授主动执行体，基础费用横置该传奇;dur:Duration=p控制本战场期间;actor:Player=受授传奇主动控制者;cost:Cost=横置该受授传奇;binding:CostBinding=受授主动基础费用;g:Gear=actor控制的所选Equipment;u:Unit=actor控制的所选单位

```python

# 持续授予
ops.grant_ability(legends, ability, duration=dur)
# 受授传奇主动的独立执行体
paid = ops.pay(actor, cost, binding=binding)
if paid.value is not None:
    ops.attach(g, u)

```



<a id="card-0347"></a>

## 0347

打出基地随从；主动杀me为费，回收任意废牌合计至多4

recruit:TokenTemplate=1战力Recruit;cost:Cost=杀me;binding:CostBinding=主动基础费用;cards:Selection[Card]=所有废牌堆合计至多4所选牌

```python

# 打出触发
ops.play(recruit, p, origin=None, destination=p.base)
# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.recycle(cards)

```



<a id="card-0348"></a>

## 0348

固有Unique、武装+3；装配任意Power1；宿主进攻/防守此处全敌军打2

cost:Cost=任意Power1;binding:CostBinding=装配基础费用;u:Unit=己方宿主;enemies:Selection[Unit]=宿主能力绑定地点所有敌军

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 宿主进攻/防守
ops.damage(enemies, 2)

```

DATA:SC缺printedEffectText中的宿主群伤



<a id="card-0349"></a>

## 0349

控制此处时p打出法术，实际消耗Energy≥4才洞察；不是印刷费用

 

```python

ops.predict(p)

```



<a id="card-0350"></a>

## 0350

玩家各自第3回合之前不得在此处Scored，原文不只是禁增分

players:PermissionSelection=各自未到自己第三回合的玩家;restriction:RestrictionSpec=禁止在本战场执行Scored流程，不扩成所有地点禁增分

```python

ops.restrict_action(players, restriction, duration=WHILE_SOURCE_PRESENT)

```

LANG:SC写不能从此处获得分数，EN为不能score here，Scored流程与增分有差别



<a id="card-0351"></a>

## 0351

打出或自己开始阶段燃烧1，若燃烧单位则自反项给己军+该牌战力

 

```python

ops.burn(p, 1)

```

REFLEXIVE:缺从本次实际燃烧的单位卡保存战力并创建独立待处理加战力项；不能立刻修改不明目标



<a id="card-0352"></a>

## 0352

迅捷主动，横置己军及me，移另一己军到所横置单位地点

cost:Cost=横置选中的己方单位及横置me;binding:CostBinding=迅捷主动基础费用;u:Unit=不同于付费单位的所选己军;dest:Location=按原文引用规则读取该次付费横置单位的位置，不猜成p基地

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.move([u], dest)

```



<a id="card-0353"></a>

## 0353

自己开始阶段若符文少于至少一对手则+1本回合

 

```python

ops.modify_might([me], 1, duration=THIS_TURN)

```



<a id="card-0354"></a>

## 0354

p防守此处时，选任意单位得坚守2本次战斗；不擅加仅此处己军

u:Unit=所选合法任意单位;params:KeywordParameters=Shield.value为2

```python

ops.grant_keyword([u], SHIELD, parameters=params, duration=THIS_COMBAT)

```



<a id="card-0355"></a>

## 0355

待命/迅捷法术，杀同一战场任意单位总战力≤4

units:Selection[Unit]=同一所选战场任意所选单位，总计战力≤4

```python

ops.kill(units)

```



<a id="card-0356"></a>

## 0356

对决期间p打出单位后，可横置本装抽1

cost:Cost=横置me;binding:CostBinding=可选对决内打单位触发基础费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.draw(p, 1)

```



<a id="card-0357"></a>

## 0357

自身实际从休眠变活跃后，不包括活跃入场

 

```python

ops.modify_might([me], 2, duration=THIS_TURN)

```



<a id="card-0358"></a>

## 0358

反应法术，选任意单位，己方四指定标签每种+1本回合

u:Unit=所选任意单位;n:IntExpr=己军Bird/Cat/Dog/Poro存在的不同标签数，非总单位数

```python

ops.modify_might([u], n, duration=THIS_TURN)

```



<a id="card-0359"></a>

## 0359

每回合p抽第二张牌后

u:Unit=所选友方单位

```python

ops.modify_might([u], 2, duration=THIS_TURN)

```



<a id="card-0360"></a>

## 0360

反应/回响Energy2，单遍−2

u:Unit=所选任意单位

```python

ops.modify_might([u], -2, duration=THIS_TURN)

```

REPEAT:缺回响额外费和多遍预选/执行完整组合



<a id="card-0361"></a>

## 0361

打出此处打一Bird；该单位本身不因此有法盾

bird:TokenTemplate=1战力Deflect的Bird

```python

ops.play(bird, p, origin=None, destination=here)

```



<a id="card-0362"></a>

## 0362

可额外Mind1，实付后打出触发单位−2本回合

cost:Cost=Mind1;binding:CostBinding=可选打出额外费用;paid_extra:bool=本次额外费用已付;u:Unit=所选任意单位

```python

# 费用入口
ops.pay(p, cost, binding=binding)
# 打出触发
if paid_extra:
    ops.modify_might([u], -2, duration=THIS_TURN)

```



<a id="card-0363"></a>

## 0363

强化基础Energy12每己符文减1；强化持续+3

ability:CostSelection=本强化主动费用;change:CostChange=Energy减动态p符文数，不影响其他能力;cost:Cost=修改后强化Energy费用;binding:CostBinding=仅未强化主动基础费用;dur:Duration=me留场且强化

```python

# 持续降费
ops.modify_cost(ability, change, duration=WHILE_SOURCE_PRESENT)
# 强化主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 强化持续
ops.modify_might([me], 3, duration=dur)

```



<a id="card-0364"></a>

## 0364

每位玩家各自开始阶段，得分前

units:Selection[Unit]=此处所有单位

```python

ops.damage(units, 1)

```



<a id="card-0365"></a>

## 0365

无独立印刷文字；按官方规则164.2分别有反应横置产Energy1和反应回收产所属领域Power1

exhaust_cost:Cost=横置该基础符文;exhaust_binding:CostBinding=反应产Energy主动基础费用;recycle_cost:Cost=回收该基础符文;recycle_binding:CostBinding=反应产Power主动基础费用;power:ResourceBundle=Fury领域Power1

```python

# 横置产Energy的主动入口
paid = ops.pay(p, exhaust_cost, binding=exhaust_binding)
if paid.value is not None:
    ops.add_resources(p, ResourceBundle(energy=1))
# 回收产Power的独立主动入口
paid = ops.pay(p, recycle_cost, binding=recycle_binding)
if paid.value is not None:
    ops.add_resources(p, power)

```



<a id="card-0366"></a>

## 0366

固有法盾壁垒；自己不造成战斗伤害

restriction:RestrictionSpec=禁止me作为来源造成战斗伤害，保留承伤及被选规则

```python

ops.restrict_action(me, restriction, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0367"></a>

## 0367

强化Body2；强化时被选择的法术/技能将晕、减战力、回手改本回合+3

cost:Cost=Body2;binding:CostBinding=仅未强化的强化主动基础费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])

```

REPLACE:缺对来自选中自身法术/技能的三种待发生动作的替代；suppress_ability或restrict_action都不能补上改为+3



<a id="card-0368"></a>

## 0368

回收己废牌3、Energy1、横置me为主动费用抽1

cost:Cost=回收己方废牌3及Energy1及横置me;binding:CostBinding=完整主动基础费用，不足3不能付

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.draw(p, 1)

```



<a id="card-0369"></a>

## 0369

此处全部单位都获得横置自己得XP1主动，含敌军

units:Selection[Unit]=此处动态所有单位;ability:Ability=下方独立执行体，普通主动，横置其自身为费;actor:Player=发动该受授主动的单位控制者;cost:Cost=横置该单位自身;binding:CostBinding=受授主动基础费用

```python

# 战场持续
ops.grant_ability(units, ability, duration=WHILE_SOURCE_PRESENT)
# 每个受授主动的独立执行体
paid = ops.pay(actor, cost, binding=binding)
if paid.value is not None:
    ops.gain_xp(actor, 1)

```



<a id="card-0370"></a>

## 0370

此处其他友方单位持续+1

units:Selection[Unit]=此处其他友方单位

```python

ops.modify_might(units, 1, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0371"></a>

## 0371

强攻2与坚守2的内部展开

fighting:bool=me进攻或防守;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if fighting:
    ops.modify_might([me], 2, duration=WHILE_CONDITION)

```



<a id="card-0372"></a>

## 0372

固有急速；每件贴附武装提供双倍基础武装战力

n:IntExpr=当前贴附武装印刷基础mightBonus之和，不是宿主基础战力

```python

ops.modify_might([me], n, duration=WHILE_SOURCE_PRESENT)

```

MIGHT_BONUS:该调用复现宿主总战力数值，但API没有逐装备战力贡献层字段修饰，未证明完整层次及归属等价



<a id="card-0373"></a>

## 0373

打出后给任意单位游走本回合

u:Unit=所选单位

```python

ops.grant_keyword([u], GANKING, duration=THIS_TURN)

```



<a id="card-0374"></a>

## 0374

自身预知；其他友方单位在相关区域获预知

others:Selection[Card]=动态其他友方单位，在Vision需生效区域；不含me

```python

# 自身预知触发
ops.predict(p)
# 持续授予其他单位
ops.grant_keyword(others, VISION, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0375"></a>

## 0375

固有狩猎1；XP≥6持续+1

dur:Duration=me留场且pXP≥6

```python

ops.modify_might([me], 1, duration=dur)

```



<a id="card-0376"></a>

## 0376

p打出me或另一Dragon后

runes:Selection[Rune]=己方所选至多2符文

```python

pass  # Rune不符合ready的Permanent参数类型

```

RUNE_READY:规则133.5.a.1/161.1.a明确Rune不是Permanent，ready签名不能接受该符文集合



<a id="card-0377"></a>

## 0377

迅捷法术，先友方单位+3，再和所选敌军互殴

u:Unit=所选友方单位

```python

ops.modify_might([u], 3, duration=THIS_TURN)

```

RECIPROCAL:加战力后双方同时按各自当前战力伤害缺多来源批次；不能串两个damage冒充



<a id="card-0378"></a>

## 0378

迅捷法术，弃1，再按该牌印刷Energy打战场单位，忽略Power

u:Unit=所选战场单位;n:IntExpr=实际弃牌的印刷Energy，缺失不当0

```python

r = ops.discard(p, 1)
if r.value:
    ops.damage([u], n)

```



<a id="card-0379"></a>

## 0379

绝念可免费打己废牌Energy≤3且Power≤1单位

c:Card=符合两项印刷费用上限的己废牌单位;dest:Location=正常合法目的地;permit:PlayPermission=仅本次死亡触发允许该废牌打出

```python

ops.play(c, p, origin=p.trash, destination=dest, cost_policy=IGNORE_BASE_COST, permission=permit)

```



<a id="card-0380"></a>

## 0380

自己或盟友据守，可横置传奇为触发成本抽1

cost:Cost=横置me;binding:CostBinding=可选据守触发基础费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.draw(p, 1)

```



<a id="card-0381"></a>

## 0381

p赢战斗后，每场独立

 

```python

ops.draw(p, 1)

```



<a id="card-0382"></a>

## 0382

装备强化任意Power2；解除强化横置主动交给选玩家召回；自己回合末杀自己并己军全打5

ecost:Cost=任意Power2;eb:CostBinding=仅未强化主动基础费用;cost:Cost=解除me强化及横置me;binding:CostBinding=交付主动基础费用;actor:Player=所选玩家;units:Selection[Unit]=回合末能力控制者的全体己军

```python

# 强化
paid = ops.pay(p, ecost, binding=eb)
if paid.value is not None:
    ops.empower([me])
# 交付主动的可表达片段
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.change_control([me], actor)
    ops.recall([me])
# 当前控制者的自己回合末
ops.kill([me])
ops.damage(units, 5)

```

ACTOR:交付后是所选玩家执行recall，而recall无行动玩家参数；不能只因目的基地正确就认定归属正确



<a id="card-0383"></a>

## 0383

金币反应产费，杀自己且横置为完整成本，得通用Power1

cost:Cost=杀me及横置me的合法组合;binding:CostBinding=反应产费主动基础费用;bundle:ResourceBundle=通用Power1

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.add_resources(p, bundle)

```

DATA:目录勘误缺sourceUrl和effectiveDate，按给出内容保留不补官方日期



<a id="card-0384"></a>

## 0384

己军实际跨阈值变Mighty，可横置传奇召1休眠符文

cost:Cost=横置me;binding:CostBinding=可选变强力触发基础费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.channel(p, 1, exhausted=True)

```



<a id="card-0385"></a>

## 0385

迅捷法术，所有友方单位+5本回合

units:Selection[Unit]=执行时所有友方单位

```python

ops.modify_might(units, 5, duration=THIS_TURN)

```



<a id="card-0386"></a>

## 0386

传奇两个主动：Energy1横置贴未贴附己装；或横置贴已贴附己装

cost:Cost=所选第一主动Energy1并横置me，或第二主动仅横置me;binding:CostBinding=按所选主动分别绑定基础费用;g:Gear=第一项要求未贴附，第二项要求已贴附的己方Equipment;u:Unit=所选己军

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(g, u)

```



<a id="card-0387"></a>

## 0387

进攻/防守按自己战力打此处全敌军；自己不造成战斗伤害

units:Selection[Unit]=此处全敌军;m:IntExpr=me执行时战力;restriction:RestrictionSpec=仅禁止me来源的战斗伤害

```python

# 持续
ops.restrict_action(me, restriction, duration=WHILE_SOURCE_PRESENT)
# 进攻/防守触发
ops.damage(units, m)

```



<a id="card-0388"></a>

## 0388

部署；对手向此战场每批移动一或多单位须Energy1/任意Power1；绝念抽1

subjects:CostSelection=对手将一或多单位移入此战场的每批动作附加费槽，不按单位数乘算;change:CostChange=强制附加Energy1及任意Power1

```python

# 持续附加费
ops.modify_cost(subjects, change, duration=WHILE_SOURCE_PRESENT)
# 绝念
ops.draw(p, 1)

```



<a id="card-0389"></a>

## 0389

征服/据守可横置传奇，将该战场替换草丛

cost:Cost=横置me;binding:CostBinding=可选征服/据守触发基础费用;b:Battlefield=此次征服/据守战场;brush:CardTemplate=完整Brush战场衍生物模板;link:Link=原战场与此草丛替换关联

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.replace_battlefield(b, brush, link=link)

```



<a id="card-0390"></a>

## 0390

固有伏击；打出可让友方战场单位回拥有者手牌

u:Unit=所选友方战场单位;origin:Zone=u场上区域

```python

ops.transfer([u], origin, u.owner.hand)

```



<a id="card-0391"></a>

## 0391

迅捷法术，友方单位+3本回合；该军本回合赢战斗时原施法者XP2

u:Unit=所选友方单位

```python

ops.modify_might([u], 3, duration=THIS_TURN)

```

DELAY:缺登记关联u本回合赢战斗的延迟触发；给u新能力会改变能力来源和控制归属，不直接视为等价



<a id="card-0392"></a>

## 0392

据守此处

 

```python

ops.draw(p, 1)

```



<a id="card-0393"></a>

## 0393

强化Energy12每己符文减1；强化期间法盾坚守3

subject:CostSelection=该强化主动;change:CostChange=Energy减动态己方符文数;cost:Cost=修改后的强化Energy费用;binding:CostBinding=仅未强化主动基础费用;params:KeywordParameters=Shield.value为3;dur:Duration=me留场且强化

```python

# 费用修饰
ops.modify_cost(subject, change, duration=WHILE_SOURCE_PRESENT)
# 强化主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 强化持续
ops.grant_keyword([me], DEFLECT, duration=dur)
ops.grant_keyword([me], SHIELD, parameters=params, duration=dur)

```



<a id="card-0394"></a>

## 0394

武装+1；装配Calm1；宿主将死改杀守护天使并治疗横置召回宿主

cost:Cost=Calm1;binding:CostBinding=装配基础费用;u:Unit=己方宿主

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)

```

REPLACE:缺宿主死亡前替代登记，不能在死亡已发生后杀装备加治疗冒充；DATA:SC缺printedEffectText的完整死亡替代



<a id="card-0395"></a>

## 0395

自身据守可回收己废牌单位/装备到手牌，是return不是recycle

c:Card=己废牌所选单位或装备

```python

ops.transfer([c], p.trash, p.hand)

```



<a id="card-0396"></a>

## 0396

待命法术，打沙兵后自反项可Order1活跃该实际新单位

soldier:TokenTemplate=2战力SandSoldier;dest:Location=合法打出地点

```python

ops.play(soldier, p, origin=None, destination=dest)

```

REFLEXIVE:勘误then do this后续付费活跃需独立链项；play返回ChainItem，不能当成已入场Unit



<a id="card-0397"></a>

## 0397

己废牌至多2待命回手；本回合盖放忽略成本

cards:Selection[Card]=己废牌至多2Hidden牌;subjects:CostSelection=p本回合合法Hide动作成本，不扩大盖放资格;change:CostChange=忽略该Hide动作所有成本

```python

ops.transfer(cards, p.trash, p.hand)
ops.modify_cost(subjects, change, duration=THIS_TURN)

```



<a id="card-0398"></a>

## 0398

反应法术，战场≤3战力单位回拥有者手牌

u:Unit=所选战场战力≤3单位;origin:Zone=u场上区域

```python

ops.transfer([u], origin, u.owner.hand)

```



<a id="card-0399"></a>

## 0399

可额外Energy1；已付的打出触发以放逐任意废牌一张为触发费，给单位强攻2本回合

extra:Cost=Energy1;eb:CostBinding=可选打出额外费用;cost:Cost=从任意废牌放逐所选一张卡;binding:CostBinding=仅已支付额外费时的打出触发基础费用;u:Unit=所选单位;params:KeywordParameters=Assault.value为2

```python

# 打出额外费用
ops.pay(p, extra, binding=eb)
# 已付该额外费的打出触发
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.grant_keyword([u], ASSAULT, parameters=params, duration=THIS_TURN)

```



<a id="card-0400"></a>

## 0400

固有狩猎2；等级3持续+1及游走

dur:Duration=me留场且pXP≥3

```python

ops.modify_might([me], 1, duration=dur)
ops.grant_keyword([me], GANKING, duration=dur)

```



<a id="card-0401"></a>

## 0401

待命；定稿可亮出Hidden牌；成功后打出触发得通用Power1

requirement:ShowOffRequirement=手牌一张Hidden或场上另一友方Hidden牌；盖放牌不按拥有Hidden处理;link:Link=本次亮出与依赖触发关联;showed:bool=本次关联实际亮出成功;bundle:ResourceBundle=通用Power1

```python

# 定稿
ops.show_off(p, requirement, link=link)
# 打出触发
if showed:
    ops.add_resources(p, bundle)

```



<a id="card-0402"></a>

## 0402

自己开始阶段恰4手牌且战场己军总计恰4直接胜；主动弃1横置打Bird

authorization:WinAuthorization=该卡开始阶段触发中两项恰4条件已满足的明示胜利授权;cost:Cost=弃1及横置me;binding:CostBinding=主动基础费用;bird:TokenTemplate=完整1战力Deflect的Bird;dest:Location=合法打出地点

```python

# 条件满足的开始阶段触发
ops.win(p, authorization=authorization)
# 独立主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.play(bird, p, origin=None, destination=dest)

```



<a id="card-0403"></a>

## 0403

迅捷法术，单位+2，若已强化改+4

u:Unit=所选单位;empowered:bool=执行时u已强化

```python

ops.modify_might([u], 4 if empowered else 2, duration=THIS_TURN)

```



<a id="card-0404"></a>

## 0404

征服此处后可Energy1活跃自己的传奇

cost:Cost=Energy1;binding:CostBinding=可选征服触发基础费用

```python

ops.pay(p, cost, binding=binding)

```

LEGEND_READY:ready仅接受Permanent，不能把Legend传入



<a id="card-0405"></a>

## 0405

据守此处且英雄区为空，可将自己的ChosenChampion从己废牌回英雄区

champion:Card=己方选定英雄的该实体且现处己废牌，不任意选其他同名英雄

```python

ops.transfer([champion], p.trash, p.champion_zone)

```



<a id="card-0406"></a>

## 0406

武装+1；装配Calm1；宿主与恰一其他己军同在战场时+2

cost:Cost=Calm1;binding:CostBinding=装配基础费用;u:Unit=己军宿主;host:Selection[Unit]=当前宿主;dur:Duration=仍贴附且宿主战场其他己军恰1

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 宿主持续
ops.modify_might(host, 2, duration=dur)

```

DATA:SC没有printedEffectText中的宿主条件+2



<a id="card-0407"></a>

## 0407

传奇反应产费，横置；鼓舞满足p本回合已定稿卡牌才得Energy1

cost:Cost=横置me;binding:CostBinding=反应产费主动基础费用;legion:bool=p本回合已定稿过至少一张卡，传奇本身不当卡计数

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None and legion:
    ops.add_resources(p, ResourceBundle(energy=1))

```



<a id="card-0408"></a>

## 0408

反应/回响Energy2；对方法术控制者可结算付Energy2免无效化

spell:ChainItem=所选法术;actor:Player=spell控制者;cost:Cost=Energy2;binding:CostBinding=结算时支付动作，非该法术控制者原法术成本

```python

paid = ops.pay(actor, cost, binding=binding)
if paid.value is None:
    ops.counter(spell)

```

REPEAT:单遍unless可描述，回响各遍目标选择与支付流程尚未定义



<a id="card-0409"></a>

## 0409

打出杀任意敌军，无战场限定

u:Unit=所选敌军

```python

ops.kill([u])

```



<a id="card-0410"></a>

## 0410

自身从战场移走触发

 

```python

ops.modify_might([me], 2, duration=THIS_TURN)

```



<a id="card-0411"></a>

## 0411

装备横置主动任意单位+3本回合

cost:Cost=横置me;binding:CostBinding=主动基础费用;u:Unit=所选单位

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_might([u], 3, duration=THIS_TURN)

```



<a id="card-0412"></a>

## 0412

从非手牌打出卡牌后强化传奇；迅捷主动解除强化横置给单位强攻2

cost:Cost=解除me强化及横置me;binding:CostBinding=迅捷主动基础费用;u:Unit=所选任意单位;params:KeywordParameters=Assault.value为2

```python

# 非手牌打牌触发
ops.empower([me])
# 迅捷主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.grant_keyword([u], ASSAULT, parameters=params, duration=THIS_TURN)

```



<a id="card-0413"></a>

## 0413

打出活跃友方传奇；持续给友方传奇横置任意单位+3主动

legends:Selection[Card]=友方传奇集合;ability:Ability=下方受授主动执行体，横置该传奇为费，普通主动;actor:Player=发动该受授能力玩家;cost:Cost=横置被授予此能力的该传奇;binding:CostBinding=受授主动基础费用;u:Unit=所选任意单位

```python

# 持续授予
ops.grant_ability(legends, ability, duration=WHILE_SOURCE_PRESENT)
# 受授主动执行体
paid = ops.pay(actor, cost, binding=binding)
if paid.value is not None:
    ops.modify_might([u], 3, duration=THIS_TURN)

```

LEGEND_READY:打出触发活跃友方Legend不符合ready的Permanent类型



<a id="card-0414"></a>

## 0414

反应法术，强制杀友方单位作额外费；从废牌免费打费用两分量都≤所杀者的单位

cost:Cost=杀所选友方单位;binding:CostBinding=强制打出额外费用;c:Card=己废牌单位，印刷Energy及Power分别不高于所杀单位各自快照值;dest:Location=正常合法目的地;permit:PlayPermission=本法术允许该废牌单位打出

```python

# 定稿费用
ops.pay(p, cost, binding=binding)
# 结算
ops.play(c, p, origin=p.trash, destination=dest, cost_policy=IGNORE_BASE_COST, permission=permit)

```



<a id="card-0415"></a>

## 0415

自身在战场时，己方将打出单位衍生物可改同地打3战力Mech

 

```python

# 不在原衍生物已打出之后再play一个Mech

```

REPLACE:缺对将要打出的衍生物模板/目的地作事件替代的接口，CREATE或GRANT_PERMISSION都不替换原Play



<a id="card-0416"></a>

## 0416

动态拥有友方传奇单位装备所有横置能力，保留来源/指代且防自递归

originals:Selection[Permanent/Legend]=友方传奇单位装备的动态集合;ability_filter:Predicate=基础费用含横置的能力，按能力身份防止派生自递归

```python

ops.copy_abilities(me, originals, ability_filter=ability_filter, duration=WHILE_SOURCE_PRESENT)

```

LANG:SC明确其他友方对象，EN/TC含自身；要保留规则层防循环及来源差异，不直接字面无限复制



<a id="card-0417"></a>

## 0417

所有玩家为选择此处对象的法术/技能付费时忽略法盾

subjects:CostSelection=各玩家法术/技能选择此处对象的费用;change:CostChange=只忽略这些选择引入的Deflect额外费，不移除关键词或免普通费用

```python

ops.modify_cost(subjects, change, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0418"></a>

## 0418

装备强化Energy4/Calm1；对方法术Energy+1，强化时改再加任意Power1

cost:Cost=Energy4/Calm1;binding:CostBinding=仅未强化主动基础费用;spells:CostSelection=所有对手法术打出费用;change:CostChange=动态Energy增加1且当me强化时任意Power增加1，不再多加第二个Energy

```python

# 强化主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 持续费用修饰
ops.modify_cost(spells, change, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0419"></a>

## 0419

自己Dragon单位Energy−2最低1

subjects:CostSelection=p的Dragon单位打出费用;change:CostChange=Energy减2最低1

```python

ops.modify_cost(subjects, change, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0420"></a>

## 0420

固有狩猎1；打出获XP2

 

```python

ops.gain_xp(p, 2)

```



<a id="card-0421"></a>

## 0421

传奇Energy1横置主动，打随从到合法地点而非强制基地

cost:Cost=Energy1及横置me;binding:CostBinding=主动基础费用;recruit:TokenTemplate=1战力Recruit;dest:Location=合法所选地点

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.play(recruit, p, origin=None, destination=dest)

```



<a id="card-0422"></a>

## 0422

打出让一友方单位基础战力本回合5

u:Unit=所选友方单位

```python

ops.set_base_might([u], 5, duration=THIS_TURN)

```



<a id="card-0423"></a>

## 0423

待命/迅捷法术；可手牌单位打己控战场，Energy−3

c:Card=己方手牌单位;b:Battlefield=己控战场;subject:CostSelection=仅本效果接下来的这一次c打出费用;change:CostChange=Energy减3;permit:PlayPermission=本法术允许在结算内打出该单位到b

```python

ops.modify_cost(subject, change, duration=UNTIL_EFFECT_END, uses=1)
ops.play(c, p, origin=p.hand, destination=b, permission=permit)

```



<a id="card-0424"></a>

## 0424

迅捷法术，友方单位+1并晕其所在地点敌军

u:Unit=所选友方单位;v:Unit=与u同地点的所选敌军

```python

ops.modify_might([u], 1, duration=THIS_TURN)
ops.stun([v])

```



<a id="card-0425"></a>

## 0425

武装+1；装配Body1；宿主法盾1

cost:Cost=Body1;binding:CostBinding=装配基础费用;u:Unit=己方宿主;host:Selection[Unit]=当前宿主;dur:Duration=仍贴附期间

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 效果区持续
ops.grant_keyword(host, DEFLECT, duration=dur)

```

DATA:SC缺printedEffectText的法盾



<a id="card-0426"></a>

## 0426

迅捷法术，杀任选己Bomb，回合末打同样数量Bomb到单一战场

bombs:Selection[Gear]=任选友方Bomb

```python

ops.kill(bombs)

```

DELAY:缺登记按本次实际杀数在本回合末打Bomb的触发；不能立即play也不能按被选数量代替实杀数



<a id="card-0427"></a>

## 0427

传奇Energy1/任意Power1横置主动，打Bomb到战场

cost:Cost=Energy1/任意Power1及横置me;binding:CostBinding=主动基础费用;bomb:TokenTemplate=完整Bomb模板;b:Battlefield=所选合法战场

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.play(bomb, p, origin=None, destination=b)

```



<a id="card-0428"></a>

## 0428

反应产费，先横置为基础费，结算可付任意Power换等量Energy

cost:Cost=横置me;binding:CostBinding=反应产费主动基础费用;inner_cost:Cost=所选数量任意领域Power;inner:CostBinding=结算时指令内支付;n:IntExpr=该次实际支付Power总量

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    exchanged = ops.pay(p, inner_cost, binding=inner)
    if exchanged.value is not None:
        ops.add_resources(p, ResourceBundle(energy=n))

```



<a id="card-0429"></a>

## 0429

强化主动横置；另一主动解除强化Energy1横置打Mech基地

ecost:Cost=横置me;eb:CostBinding=仅未强化时强化主动基础费用;cost:Cost=解除me强化及Energy1及横置me;binding:CostBinding=另一主动基础费用;mech:TokenTemplate=3战力Mech

```python

# 强化主动
paid = ops.pay(p, ecost, binding=eb)
if paid.value is not None:
    ops.empower([me])
# 打Mech主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.play(mech, p, origin=None, destination=p.base)

```



<a id="card-0430"></a>

## 0430

装备休眠进场；主动横置强化另一装备，不限己方

entry:EntryState=休眠;cost:Cost=横置me;binding:CostBinding=主动基础费用;g:Gear=除me之外所选任意装备

```python

# 基础打出
ops.play(me, p, origin=p.hand, destination=p.base, entry=entry)
# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([g])

```



<a id="card-0431"></a>

## 0431

武装+3；装配Energy3/任意Power1，Energy减目标单位战力；宿主征服若已分配过量≥3抽1

subject:CostSelection=本装配主动的费用，不是打装备费用;change:CostChange=Energy减本次所选装配宿主执行前战力;cost:Cost=修改后的装配费;binding:CostBinding=装配主动基础费用;u:Unit=己军宿主

```python

# 装配费用及主动
ops.modify_cost(subject, change, duration=WHILE_SOURCE_PRESENT)
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 宿主征服且相关战斗分配过量≥3
ops.draw(p, 1)

```

DATA:SC缺printedEffectText的过量分配条件抽牌



<a id="card-0432"></a>

## 0432

迅捷法术

u:Unit=所选战场单位

```python

ops.damage([u], 3)

```



<a id="card-0433"></a>

## 0433

待命/迅捷法术，杀战场单位，其原控制者抽2

u:Unit=所选战场单位;actor:Player=u死亡前控制者快照

```python

ops.kill([u])
ops.draw(actor, 2)

```



<a id="card-0434"></a>

## 0434

反应法术，负战力等自己休眠单位数

u:Unit=所选任意单位;n:IntExpr=执行时p控制休眠单位数

```python

ops.modify_might([u], -n, duration=THIS_TURN)

```



<a id="card-0435"></a>

## 0435

反应法术，所选友方单位本回合下一次将死改治疗横置召回

u:Unit=所选友方单位

```python

# 无可立即执行的等价动作；不能先让其死亡再召回

```

REPLACE:缺下一次死亡前事件替代，不能用prevent_damage处理非伤害摧毁，也不能用gain_ability改变延迟效果来源



<a id="card-0436"></a>

## 0436

迅捷法术；本回合已把单位/装备打战场则Energy−2；单位+3

subject:CostSelection=本次me费用;change:CostChange=Energy减2;dur:Duration=费用计算期间满足本回合p已打单位或装备到战场的历史条件;u:Unit=所选单位

```python

# 费用
ops.modify_cost(subject, change, duration=dur)
# 结算
ops.modify_might([u], 3, duration=THIS_TURN)

```



<a id="card-0437"></a>

## 0437

绝念

gold:TokenTemplate=金币;entry:EntryState=休眠

```python

ops.play(gold, p, origin=None, destination=p.base, entry=entry)

```



<a id="card-0438"></a>

## 0438

装备休眠进场；基础反应横置Power1；等级6额外有横置Energy1/Power1主动

entry:EntryState=休眠;cost:Cost=横置me;binding:CostBinding=所选产费主动基础费用；增强主动仅XP≥6可选;bundle:ResourceBundle=基础主动通用Power1，增强主动Energy1加通用Power1，不能将两主动同时发动

```python

# 基础打出
ops.play(me, p, origin=p.hand, destination=p.base, entry=entry)
# 选择的一项反应产费主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.add_resources(p, bundle)

```



<a id="card-0439"></a>

## 0439

固有壁垒内部展开

scope:RuleScope=me在同控制者参战单位中的承伤次序;change:RuleChange=先承担致死伤害

```python

ops.modify_rule(COMBAT_DAMAGE_ORDER, scope, change, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0440"></a>

## 0440

待命法术，战场敌军夺控活跃；回合末失控再召回

u:Unit=所选敌方战场单位

```python

ops.change_control([u], p, duration=THIS_TURN)
ops.ready([u])

```

DELAY:控制权期限可表示，但缺回合末失控之后再recall该实例的延迟步骤；不能现在召回



<a id="card-0441"></a>

## 0441

主动Order1，须本回合选过敌军且每回合一次，活跃自己+1

cost:Cost=Order1;binding:CostBinding=具有上述历史与次数限制的主动基础费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.ready([me])
    ops.modify_might([me], 1, duration=THIS_TURN)

```



<a id="card-0442"></a>

## 0442

反应法术，活跃友方单位、该军不能move本回合、抽1

u:Unit=所选友方单位;restriction:RestrictionSpec=该单位不能执行move，不禁止recall

```python

ops.ready([u])
ops.restrict_action(u, restriction, duration=THIS_TURN)
ops.draw(p, 1)

```



<a id="card-0443"></a>

## 0443

每玩家在自己回合此处首个单位/装备Energy−1，单位和装备共用首个额度

subject:CostSelection=动态每玩家本回合在此处首个单位或装备的打出费；按每玩家各自历史共享一次;change:CostChange=Energy减1

```python

ops.modify_cost(subject, change, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0444"></a>

## 0444

武装+2；装配Body1；效果区宿主狩猎1

cost:Cost=Body1;binding:CostBinding=装配基础费用;u:Unit=己军宿主;host:Selection[Unit]=当前宿主;dur:Duration=仍贴附本装期间

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 宿主效果
ops.grant_keyword(host, HUNT, duration=dur)

```

DATA:SC没有printedEffectText中的狩猎



<a id="card-0445"></a>

## 0445

部署；打出可移敌军到此处；此处友方单位持续坚守2

u:Unit=所选敌军;units:Selection[Unit]=此处动态友方单位;params:KeywordParameters=Shield.value为2

```python

# 打出触发
ops.move([u], here)
# 持续
ops.grant_keyword(units, SHIELD, parameters=params, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0446"></a>

## 0446

绝念打1战力法盾Bird基地；法盾不属于本单位

bird:TokenTemplate=完整1战力Deflect的Bird

```python

ops.play(bird, p, origin=None, destination=p.base)

```



<a id="card-0447"></a>

## 0447

反应法术，无效化印刷Power≥2法术

spell:ChainItem=所选印刷Power总数≥2法术，不是本次实付量

```python

ops.counter(spell)

```



<a id="card-0448"></a>

## 0448

移动后抽1弃1，再按实际弃牌所有类型逐项执行；单位兼装备两项都符合

is_spell:bool=实际弃牌有spell类型;is_gear:bool=有gear类型;is_unit:bool=有unit类型

```python

ops.draw(p, 1)
ops.discard(p, 1)
if is_spell:
    ops.draw(p, 1)
if is_gear:
    pass  # 活跃符文未映射
if is_unit:
    ops.modify_might([me], 3, duration=THIS_TURN)

```

RUNE_READY:gear分支要求活跃至多2符文，但ready只接受Permanent，不可传Rune



<a id="card-0449"></a>

## 0449

自身据守后，下一次自己主阶段开始可移敌军到该战场

 

```python

# 不能在据守触发结算时立即move

```

DELAY:缺把原战场引用保存到下一主阶段的可选移动触发登记



<a id="card-0450"></a>

## 0450

按勘误六条独立指令，各对一单位打2；不是自反六链项，也不是分配12

targets:list[Unit]=六条指令各自选定的六个目标引用，可重复，按指令顺序

```python

for u in targets:
    ops.damage([u], 2)

```



<a id="card-0451"></a>

## 0451

自身进攻可Energy1让此处任意单位−1本回合

cost:Cost=Energy1;binding:CostBinding=可选攻击触发基础费用;u:Unit=此处所选任意单位

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_might([u], -1, duration=THIS_TURN)

```



<a id="card-0452"></a>

## 0452

打出或自身Scored打Tentacle；持续+己方单位衍生物数量

tentacle:TokenTemplate=tokenCardIds关联的Tentacle，目录战力1、Bilgewater标签；不从错误Energy图标捏造模板;dest:Location=合法目的地;n:IntExpr=动态p控制单位衍生物数

```python

# 打出/自身Scored触发
ops.play(tentacle, p, origin=None, destination=dest)
# 持续
ops.modify_might([me], n, duration=WHILE_SOURCE_PRESENT)

```

DATA:EN及目录勘误仍含rb_energy_1图标，SC和关联模板为1战力；保留疑点不改写



<a id="card-0453"></a>

## 0453

固有强攻2；在废牌时p以法术杀单位可Energy1/Fury1再打自身

cost:Cost=Energy1/Fury1;binding:CostBinding=该废牌触发中明示支付;dest:Location=合法单位目的地;permit:PlayPermission=此触发允许从废牌打该实例

```python

# 仅记录支持的付款片段；后续打出成本角色待核
ops.pay(p, cost, binding=binding)

```

PLAY_COST:pay X to play与印刷基础费之间的精确费用角色需规则核定；不能默认只付X或默认重复收两份



<a id="card-0454"></a>

## 0454

迅捷法术，本回合所有单位受到任何正伤害后被摧毁

 

```python

# 不立即kill所有单位，也不把伤害直接改为致死规则

```

DELAY:缺创建本回合全局受伤后摧毁的延迟触发；这不是将伤害本身改成致死的替代



<a id="card-0455"></a>

## 0455

移动后可将此处较低战力敌军移另一战场

u:Unit=当前此处战力低于me的所选敌军;b:Battlefield=不同于当前位置的合法战场

```python

ops.move([u], b)

```



<a id="card-0456"></a>

## 0456

迅捷法术，选择己装作为数值引用，伤害源仍为本法术

g:Gear=所选友方装备;u:Unit=所选战场单位;n:IntExpr=g印刷Energy费用，不读取Power

```python

ops.damage([u], n)

```



<a id="card-0457"></a>

## 0457

迅捷法术

u:Unit=所选战场单位

```python

ops.damage([u], 2)

```



<a id="card-0458"></a>

## 0458

定稿可亮出Mech，若实亮出则活跃入场

requirement:ShowOffRequirement=手牌Mech或场上另一友方Mech;link:Link=本次亮出关联;dest:Location=合法打出地点;entry:EntryState=本次show_off实际成功则活跃，否则默认

```python

# 定稿选择入口
ops.show_off(p, requirement, link=link)
# 同次打出使用已绑定亮出记录，不重复亮出
ops.play(me, p, origin=p.hand, destination=dest, entry=entry)

```

PHASE:show_off定义为as-play定稿选择步骤，而play也自行执行整个定稿；API没有注入该中途回执以设置entry的明确钩子，不能假定前置调用是合法完整流程



<a id="card-0459"></a>

## 0459

打出后此处打3战力Mech

mech:TokenTemplate=3战力Mech

```python

ops.play(mech, p, origin=None, destination=here)

```



<a id="card-0460"></a>

## 0460

伏击允许以反应打出到p有单位战场；固有强攻2

permission:PermissionSpec=以Reaction时机将me打出到p有单位战场；不忽略其他费用与限制;attacking:bool=me为进攻方;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

ops.grant_permission([me], permission, duration=WHILE_SOURCE_PRESENT)
if attacking:
    ops.modify_might([me], 2, duration=WHILE_CONDITION)

```



<a id="card-0461"></a>

## 0461

打出后对手展手牌，结算可消耗XP2选一牌，让该对手弃该牌抽1

actor:Player=所选对手;hand:Selection[Card]=其展示时手牌;pay_xp:bool=在展示后选择付XP2;chosen:Card=实际支付后从该手牌选择的牌，非预先目标

```python

ops.reveal(hand)
if pay_xp:
    spent = ops.spend_xp(p, 2)
    if spent.value == 2:
        ops.discard(actor, 1, cards=[chosen], chooser=p)
        ops.draw(actor, 1)

```

ACTOR:卡面指定对手执行reveal，但reveal只有viewers而没有行动玩家，不能把公开对象/观众正确当成执行者正确



<a id="card-0462"></a>

## 0462

每玩家先弃整手牌，随后各抽4

actors:Selection[Player]=所有玩家;hand_counts:dict[Player,int]=各玩家弃牌前手牌数快照

```python

# 各玩家动作片段；跨玩家同时边界未保证
for actor in actors:
    ops.discard(actor, hand_counts[actor])
for actor in actors:
    ops.draw(actor, 4)

```

PLAYER_BATCH:discard/draw各只接受一个player，未定义各玩家同一指令的批次/顺序边界；不能每人弃完立即抽来替代全体先弃后抽



<a id="card-0463"></a>

## 0463

打出友方单位+3；主动横置友方Mighty单位及me，抽1

u:Unit=打出触发所选友方单位;cost:Cost=横置一名友方当前Mighty单位并横置me;binding:CostBinding=主动基础费用

```python

# 打出
ops.modify_might([u], 3, duration=THIS_TURN)
# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.draw(p, 1)

```



<a id="card-0464"></a>

## 0464

自身征服后

u:Unit=所选友方单位

```python

ops.modify_might([u], 8, duration=THIS_TURN)

```



<a id="card-0465"></a>

## 0465

固有法盾；被p选为目标或被p成功活跃时各触发+1

 

```python

ops.modify_might([me], 1, duration=THIS_TURN)

```



<a id="card-0466"></a>

## 0466

己方法术将me选为目标时，可减Energy1或任意Power1

subjects:CostSelection=p的法术且该法术将me选为目标;change:CostChange=为本费用选Energy减1或任意Power减1，不能两项都减

```python

ops.modify_cost(subjects, change, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0467"></a>

## 0467

主动横置；若目标已有增益改本回合+2，否则给增益；在行动前判断

cost:Cost=横置me;binding:CostBinding=主动基础费用;u:Unit=所选单位;buffed:bool=该步骤执行前u有增益

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    if buffed:
        ops.modify_might([u], 2, duration=THIS_TURN)
    else:
        ops.buff([u])

```



<a id="card-0468"></a>

## 0468

装备休眠入场；横置主动战场单位打2

entry:EntryState=休眠;cost:Cost=横置me;binding:CostBinding=主动基础费用;u:Unit=所选战场单位

```python

# 基础打出
ops.play(me, p, origin=p.hand, destination=p.base, entry=entry)
# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.damage([u], 2)

```



<a id="card-0469"></a>

## 0469

传奇反应产费，放逐己废牌单位/装备及横置me，产通用Power1限打单位装备

cost:Cost=放逐所选己废牌单位或装备及横置me;binding:CostBinding=反应产费基础费用;bundle:ResourceBundle=通用Power1;restriction:Predicate=仅用于单位或装备打出，不用于主动技能

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.add_resources(p, bundle, restriction=restriction)

```



<a id="card-0470"></a>

## 0470

移动到战场后可拉一敌军到相同战场

u:Unit=所选敌军;b:Battlefield=本次移动后me的战场

```python

ops.move([u], b)

```



<a id="card-0471"></a>

## 0471

移动战场敌军回其基地，再若原战场敌军落单抽1

u:Unit=所选战场敌军;base:Location=u对应基地;alone:bool=移动完成后原战场存在落单敌军，非u现处基地状态

```python

ops.move([u], base)
if alone:
    ops.draw(p, 1)

```



<a id="card-0472"></a>

## 0472

打3战力Mech；流转Energy2/Mind1

mech:TokenTemplate=3战力Mech;dest:Location=合法打出地点

```python

ops.play(mech, p, origin=None, destination=dest)

```

FLOW_EXIT:缺本次流转定稿链项离链放逐替代



<a id="card-0473"></a>

## 0473

打出期间从四标签选一获得；自身征服/据守且己军齐四标签额外得1

options:list[Tag]=Bird/Cat/Dog/Poro四标签;dur:Duration=本me实例有效期间

```python

# 打出期间选择标签
r = ops.declare(p, options)
ops.set_tags([me], set(r.value), mode="add", duration=dur)
# 征服/据守且集齐四标签触发
ops.gain_points(p, 1)

```



<a id="card-0474"></a>

## 0474

打出或自身据守看3可展示单位抽取，余回收；展示四标签之一后自反项增益己军

take:bool=选择单位;c:Card=实际看见顶3中所选单位;rest:Selection[Card]=实际看见未抽取牌，无选择则全部

```python

ops.look(p, p.main_deck, 3)
if take:
    ops.reveal([c])
    ops.draw(p, 1, cards=[c])
ops.recycle(rest)

```

REFLEXIVE:若本次展示Bird/Cat/Dog/Poro需另一个待处理项选择己军增益，不能立即buff



<a id="card-0475"></a>

## 0475

p以法术将me选为目标时；不包含技能或非目标挑选

 

```python

ops.draw(p, 1)

```



<a id="card-0476"></a>

## 0476

武装+2；装配Body1；宿主不能被敌方法术/技能move

cost:Cost=Body1;binding:CostBinding=装配基础费用;u:Unit=己方宿主;host:PermissionSelection=当前宿主;restriction:RestrictionSpec=仅禁止敌方法术/技能造成的move，不禁止recall或自主移动;dur:Duration=仍贴附本装备

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 效果区持续
ops.restrict_action(host, restriction, duration=dur)

```

DATA:SC没有printedEffectText的宿主移动限制



<a id="card-0477"></a>

## 0477

固有反应；打出先治疗此处己军，再依勘误移至多1敌军回其基地

units:Selection[Unit]=此处全体己军;take:bool=选择移动一敌军而非0;u:Unit=此处所选敌军;base:Location=u对应基地

```python

ops.heal(units)
if take:
    ops.move([u], base)

```



<a id="card-0478"></a>

## 0478

己方部署装备所有相关区域获迅捷；征服且此处有友方部署装备召1休眠符文

gear:Selection[Card]=己方有Deploy的装备，含可打出区域

```python

# 持续授予时机
ops.grant_keyword(gear, ACTION, duration=WHILE_SOURCE_PRESENT)
# 满足装备条件的征服触发
ops.channel(p, 1, exhausted=True)

```



<a id="card-0479"></a>

## 0479

固有强攻1壁垒；进攻可移己军到me战场

u:Unit=所选己方单位

```python

ops.move([u], here)

```



<a id="card-0480"></a>

## 0480

固有急速；每己方Mighty单位自身Energy−2

subject:CostSelection=me打出费用;change:CostChange=Energy减2乘动态己方Mighty单位数;dur:Duration=自身费用能力有效期间

```python

ops.modify_cost(subject, change, duration=dur)

```



<a id="card-0481"></a>

## 0481

自身法盾；勘误后己方所有区域Equipment获灵便，不只手牌

gear:Selection[Card]=己方Equipment在所有相关区域的动态集合

```python

ops.grant_keyword(gear, QUICK_DRAW, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0482"></a>

## 0482

固有百炼；贴武装到me后可Energy1抽1

cost:Cost=Energy1;binding:CostBinding=可选贴附触发基础费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.draw(p, 1)

```



<a id="card-0483"></a>

## 0483

打出me或每回合首次打非衍生物装备，可活跃除me外任意休眠物体

objects:Selection[Permanent]=合法候选中的单位/装备部分，暂不含Rune/Legend

```python

ops.ready(objects)

```

RUNE_READY:原文something包含休眠符文，但ready的Permanent排除Rune；LEGEND_READY:也包含休眠传奇，而ready排除Legend



<a id="card-0484"></a>

## 0484

自身实际变活跃后，选择强攻2/法盾2/游走之一，本回合

mode:int=已选择模式0/1/2;params:KeywordParameters=对应Assault.value或Deflect.value为2

```python

if mode == 0:
    ops.grant_keyword([me], ASSAULT, parameters=params, duration=THIS_TURN)
elif mode == 1:
    ops.grant_keyword([me], DEFLECT, parameters=params, duration=THIS_TURN)
else:
    ops.grant_keyword([me], GANKING, duration=THIS_TURN)

```



<a id="card-0485"></a>

## 0485

打出可杀己装，实际如此做则本回合可选一次从手牌打Energy≤7装备并忽略Energy

g:Gear=所选友方装备;subjects:CostSelection=p本回合手牌Energy≤7装备;change:CostChange=忽略Energy保留Power

```python

r = ops.kill([g])
if r.changed:
    ops.modify_cost(subjects, change, duration=THIS_TURN, uses=1)

```

OPTIONAL_COST:uses1何时消耗未定义；原文可保留授权先打别的合格装备，不能误作自动优惠首个合格装备；需明确可选使用与次数共享



<a id="card-0486"></a>

## 0486

固有坚守1；预知打出触发

 

```python

ops.predict(p)

```



<a id="card-0487"></a>

## 0487

预知；本回合已花Energy≥4打一法术，可Mind1替代基础费用打自身

subject:CostSelection=me打出费用;change:CostChange=可选替代基础费为仅Mind1，不是只减Energy;dur:Duration=存在p本回合某次打出法术实花Energy≥4的历史时

```python

# 条件替代费用
ops.modify_cost(subject, change, duration=dur)
# 自身预知触发
ops.predict(p)

```



<a id="card-0488"></a>

## 0488

固有法盾游走；移动触发Energy1/通用Power1

bundle:ResourceBundle=Energy1及通用Power1

```python

ops.add_resources(p, bundle)

```



<a id="card-0489"></a>

## 0489

固有急速强攻2；打出必须弃2

 

```python

ops.discard(p, 2)

```



<a id="card-0490"></a>

## 0490

p每次弃一或多手牌，同批只触发一次，活跃me本回合+1

 

```python

ops.ready([me])
ops.modify_might([me], 1, duration=THIS_TURN)

```



<a id="card-0491"></a>

## 0491

打出后按己方Mighty单位数抽牌，包含已入场me若符合

n:IntExpr=执行时己方当前战力≥5单位总数

```python

ops.draw(p, n)

```



<a id="card-0492"></a>

## 0492

固有游走；征服可打己废牌印刷Energy严格小于己分数法术，仅免Energy，随后回收

c:Card=符合Energy小于分数的己废牌法术;chain:Zone=链区域;policy:CostPolicy=仅忽略Energy;permit:PlayPermission=本次征服触发授权从废牌打此牌

```python

ops.play(c, p, origin=p.trash, destination=chain, cost_policy=policy, permission=permit)

```

CHAIN_EXIT:缺该次链项离链时回收替代，不能在play仅定稿后立即recycle



<a id="card-0493"></a>

## 0493

固有缴械；自身参与对决时己方法术获反应

spells:Selection[Card]=己方法术，含可打出区域;dur:Duration=me留场且自己正在该Showdown中

```python

ops.grant_keyword(spells, REACTION, duration=dur)

```



<a id="card-0494"></a>

## 0494

固有急速；自身征服触发

 

```python

ops.draw(p, 1)

```



<a id="card-0495"></a>

## 0495

自身预知；按勘误每批回收一或多牌到主牌堆后增益友方单位，不因符文回收触发

u:Unit=该回收触发所选友方单位

```python

# 预知
ops.predict(p)
# 回收到主牌堆触发
ops.buff([u])

```



<a id="card-0496"></a>

## 0496

己方Deathknell多触发一次，不限定此处

triggers:TriggerSelection=所有己方Deathknell能力

```python

ops.modify_trigger_count(triggers, 1, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0497"></a>

## 0497

盖放卡牌后活跃自己；从盖放打牌后对任意敌军打2

u:Unit=所选任意敌军，不限此处

```python

# Hide事件触发
ops.ready([me])
# 从正面朝下Play事件触发
ops.damage([u], 2)

```



<a id="card-0498"></a>

## 0498

固有法盾；移入战场给另一友方单位本回合当前关键词及等自己战力加值

u:Unit=勘误限定另一友方单位;keywords:list[Keyword]=me执行时实际拥有的全部关键词实例，不是目录提及列表;params:dict[Keyword,KeywordParameters]=各关键词实例当时的数值/费用;m:IntExpr=me执行时战力快照

```python

for keyword in keywords:
    ops.grant_keyword([u], keyword, parameters=params[keyword], duration=THIS_TURN)
ops.modify_might([u], m, duration=THIS_TURN)

```



<a id="card-0499"></a>

## 0499

强化Energy3可最多3层；每层+2；3层时法盾3游走

change:RuleChange=me强化层数上限3;cost:Cost=Energy3;binding:CostBinding=强化层数<3时可发动，不是只未强化;n:IntExpr=动态me强化层数;dur:Duration=me留场且强化层数为3;params:KeywordParameters=Deflect.value为3

```python

# 规则上限
ops.modify_rule(EMPOWER_LIMIT, me, change, duration=WHILE_SOURCE_PRESENT)
# 强化主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 持续层数加值
ops.modify_might([me], 2 * n, duration=WHILE_SOURCE_PRESENT)
ops.grant_keyword([me], DEFLECT, parameters=params, duration=dur)
ops.grant_keyword([me], GANKING, duration=dur)

```



<a id="card-0500"></a>

## 0500

固有游走；本回合已经移动两次后不能受伤

restriction:RestrictionSpec=禁止任何来源对me造成伤害，不移除目标合法性;dur:Duration=me留场且该实例本回合移动次数已达到2

```python

ops.restrict_action(me, restriction, duration=dur)

```



<a id="card-0501"></a>

## 0501

控制某战场且该处单位总数恰2，Energy−2/Order−1

subject:CostSelection=me打出费用;change:CostChange=Energy减2及Order需求减1;dur:Duration=费用能力有效且p控制至少一个恰2单位战场

```python

ops.modify_cost(subject, change, duration=dur)

```



<a id="card-0502"></a>

## 0502

待命/瞬息；打出在此处打2Reflection，再自反项令它们复制me

reflection:TokenTemplate=Reflection原模板

```python

for i in range(2):
    ops.play(reflection, p, origin=None, destination=here)

```

REFLEXIVE:勘误then do this要求后续待处理项绑定实际新单位后copy；不在play返回ChainItem时直接copy



<a id="card-0503"></a>

## 0503

据守XP1；传奇主动XP3横置抽1

cost:Cost=消耗XP3及横置me;binding:CostBinding=主动基础费用

```python

# 据守触发
ops.gain_xp(p, 1)
# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.draw(p, 1)

```



<a id="card-0504"></a>

## 0504

迅捷法术，战场敌军由其拥有者选放主牌堆顶/底

u:Unit=所选战场敌军;origin:Zone=u场上区域;position:str=u拥有者选定top或bottom

```python

ops.transfer([u], origin, u.owner.main_deck)
ops.reorder([u], u.owner.main_deck, position=position, policy="preserve")

```

ACTOR:原文由拥有者执行放置，transfer/reorder无独立行动玩家参数；选择位置不等于行动归属



<a id="card-0505"></a>

## 0505

待命；打出或进攻可Energy2晕任意单位；此处有晕敌军持续+2

cost:Cost=Energy2;binding:CostBinding=可选打出/进攻触发基础费用;u:Unit=所选任意单位;dur:Duration=me留场且此处至少一眩晕敌军

```python

# 可选触发
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.stun([u])
# 持续
ops.modify_might([me], 2, duration=dur)

```



<a id="card-0506"></a>

## 0506

打出燃烧2；征服给己废牌法术本回合等其印刷费用的流转

c:Card=所选己废牌法术;params:KeywordParameters=Flow.cost等该法术印刷/复制Energy及Power领域要求，未知不按0

```python

# 打出触发
ops.burn(p, 2)
# 征服触发
ops.grant_keyword([c], FLOW, parameters=params, duration=THIS_TURN)

```



<a id="card-0507"></a>

## 0507

强化Energy6/Chaos2；强化后选对手燃烧3，之后可自反项从其废牌免费打一单位

cost:Cost=Energy6/Chaos2;binding:CostBinding=仅未强化主动基础费用;actor:Player=强化触发所选对手

```python

# 强化主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 实际强化触发
ops.burn(actor, 3)

```

REFLEXIVE:then may do this要求后续独立待处理项选该对手废牌单位免费打出，不能预先选刚燃烧的秘密牌



<a id="card-0508"></a>

## 0508

固有狩猎1；进攻可XP3按自身战力打此处敌军

cost:Cost=消耗XP3;binding:CostBinding=可选攻击触发基础费用;u:Unit=此处所选敌军;m:IntExpr=me执行时战力

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.damage([u], m)

```



<a id="card-0509"></a>

## 0509

固有伏击；进攻/防守且敌军在此落单，+2本回合及XP2

 

```python

ops.modify_might([me], 2, duration=THIS_TURN)
ops.gain_xp(p, 2)

```



<a id="card-0510"></a>

## 0510

反应法术，所选单位本回合累计预防下7点所有来源伤害

u:Unit=所选单位

```python

ops.prevent_damage([u], 7, duration=THIS_TURN)

```



<a id="card-0511"></a>

## 0511

迅捷法术，横置友方单位为强制额外费；结算晕任意单位

cost:Cost=横置所选友方单位;binding:CostBinding=强制打出额外费用;u:Unit=效果所选任意单位

```python

# 费用
ops.pay(p, cost, binding=binding)
# 结算
ops.stun([u])

```



<a id="card-0512"></a>

## 0512

从下一玩家起每个其他玩家依次选非p控制且本法术未选单位，再同时杀

actors:list[Player]=按回合顺序从下一玩家开始的其他玩家;available:dict[Player,Selection[Unit]]=每步重新排除本法术前面已选单位且不由p控制的单位;units:Selection[Unit]=所有实际选中者并集

```python

for actor in actors:
    ops.choose(actor, available[actor], targeting=False, bind_at="resolution")
ops.kill(units)

```

LANG:TC文字互相选择他人单位，与EN/SC固定排除施法者控制并非同一个筛选



<a id="card-0513"></a>

## 0513

打出后若其他己军总战力≥5，排除刚入场me

 

```python

ops.draw(p, 1)

```



<a id="card-0514"></a>

## 0514

强化Energy2；强化时持续+1游走

cost:Cost=Energy2;binding:CostBinding=仅未强化主动基础费用;dur:Duration=me留场且强化

```python

# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 持续
ops.modify_might([me], 1, duration=dur)
ops.grant_keyword([me], GANKING, duration=dur)

```



<a id="card-0515"></a>

## 0515

打出给至多两名其他友方单位增益，按勘误可不足/选择0

units:Selection[Unit]=至多2其他所选友方单位

```python

ops.buff(units)

```



<a id="card-0516"></a>

## 0516

此处有Tank的所有单位+1，不分友敌

units:Selection[Unit]=此处动态具有Tank的单位

```python

ops.modify_might(units, 1, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0517"></a>

## 0517

绝念，使用死亡前战场引用，所有玩家单位各打4，若死基地不凭空选战场

units:Selection[Unit]=me死亡前所在战场当前全体单位，死亡地点不是战场则为空

```python

ops.damage(units, 4)

```



<a id="card-0518"></a>

## 0518

固有急速强攻1；任意己方增益作打出额外费，每个消耗减少Body1

cost:Cost=任选己方增益的合法消耗；可含多层但须逐对象数量绑定;binding:CostBinding=可选打出额外费用;subject:CostSelection=本次me费用;change:CostChange=Body需求减少实际消耗增益合计，不按选中单位数

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_cost(subject, change, duration=UNTIL_EFFECT_END, uses=1)

```



<a id="card-0519"></a>

## 0519

固有急速/坚守2；据守召1默认活跃符文

 

```python

ops.channel(p, 1)

```



<a id="card-0520"></a>

## 0520

自身固有坚守1；进攻/防守令此处一己军当前坚守值翻倍本回合

u:Unit=此处所选己军

```python

ops.modify_keyword([u], SHIELD, parameter="value", operation="multiply", value=2, duration=THIS_TURN)

```



<a id="card-0521"></a>

## 0521

单位若强化先解除一层，再若战力≤3杀；流转Energy4/Order2

u:Unit=所选单位;empowered:bool=第一步前已强化;small:bool=解除后重新读取u当前战力≤3，不预冻战力

```python

if empowered:
    ops.disempower([u])
if small:
    ops.kill([u])

```

FLOW_EXIT:尚未独立描述从废牌流转后的链项离链放逐替代



<a id="card-0522"></a>

## 0522

自己主阶段开始可Energy1选己装，成为单位兼装备，基础战力=Energy，直到本传奇再选另一装

cost:Cost=Energy1;binding:CostBinding=可选主阶段触发基础费用;g:Gear=所选己装，授予unit前仍是Gear;n:IntExpr=g印刷/复制Energy费用;dur:Duration=直到同me实例再选择另一装备，来源离开不自动视为另选

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.set_types([g], {UNIT}, mode="add", duration=dur)

```

TYPE_EVOLUTION:set_base_might只接受Unit，set_types仅返回Modifier，没有转换后Unit视图/同对象类型重绑定约定，不能继续把静态Gear直接作为Unit传入



<a id="card-0523"></a>

## 0523

p打出印刷Energy≥5法术后，不看实际付费

 

```python

ops.draw(p, 1)

```



<a id="card-0524"></a>

## 0524

迅捷法术，先活跃友方单位再由该友方单位按战力对战场敌军伤害

u:Unit=所选友方单位;enemy:Unit=所选战场敌军;m:IntExpr=活跃动作完成后的u当前战力

```python

ops.ready([u])
ops.damage([enemy], m, source=u)

```

LANG:SC省略明确伤害来源主语，EN/TC明确由单位而非法术造成；映射按EN保留单位来源



<a id="card-0525"></a>

## 0525

反应法术，下一己方单位本回合可打任一战场含盖放路径，成功打出后增益

subjects:PermissionSelection=p本回合下一次play单位;permit:PermissionSpec=仅该次单位打出目的地任意战场，含从盖放打出，仍遵守其他未覆盖合法性

```python

ops.grant_permission(subjects, permit, duration=THIS_TURN, uses=1)

```

NEXT_ABILITY:权限次数可登记，但缺与同一下一单位成功打出后的buff关联；不能猜手牌先buff或单独授权两次



<a id="card-0526"></a>

## 0526

武装+2；装配Chaos1并回收己废牌2；效果区宿主征服/据守可正常付费打废牌单位

cost:Cost=Chaos1及回收己方废牌2;binding:CostBinding=装配基础费用;u:Unit=己方宿主;c:Card=效果触发所选己废牌单位;dest:Location=该单位正常合法目的地;permit:PlayPermission=本次宿主征服/据守触发允许从废牌打该单位，未免费用

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 宿主征服/据守
ops.play(c, p, origin=p.trash, destination=dest, permission=permit)

```

DATA:SC缺printedEffectText的废牌打出能力



<a id="card-0527"></a>

## 0527

迅捷法术，友方单位战力翻倍本回合，另赋瞬息永久至默认生命周期清理

u:Unit=所选友方单位;m:IntExpr=执行时u当前战力快照

```python

ops.modify_might([u], m, duration=THIS_TURN)
ops.grant_keyword([u], TEMPORARY, duration=PERMANENT)

```

LANG:SC瞬息提醒写你的下回合，EN/TC按当时单位控制者开始阶段，控制变化时不同



<a id="card-0528"></a>

## 0528

固有游走扩展普通移动路径

permission:PermissionSpec=me可从当前战场移动到其他战场，普通移动费用与其他限制仍适用

```python

ops.grant_permission([me], permission, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0529"></a>

## 0529

固有Assault2的内部持续效果：me进攻时战力加2

attacking:bool=me是进攻方;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if attacking:
    ops.modify_might([me], 2, duration=WHILE_CONDITION)

```



<a id="card-0530"></a>

## 0530

固有后排；自己战场的己方瞬息能力不触发；不移除Temporary属性

objects:Selection[Card]=自己战场的己方有Temporary实体;ability_filter:Predicate=仅Temporary生成的开始阶段死亡触发，不移除关键词本身

```python

ops.suppress_ability(objects, ability_filter, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0531"></a>

## 0531

固有强攻1；绝念通常抽1，若是自己开始阶段改抽2

own_beginning:bool=结算时当前处于p的BeginningPhase

```python

ops.draw(p, 2 if own_beginning else 1)

```



<a id="card-0532"></a>

## 0532

固有壁垒；打出

 

```python

ops.draw(p, 1)

```



<a id="card-0533"></a>

## 0533

固有坚守1；自身增益数量不限；主动横置增益

change:RuleChange=本me增益数量上限无限;cost:Cost=横置me;binding:CostBinding=主动基础费用

```python

# 上限例外
ops.modify_rule(BUFF_LIMIT, me, change, duration=WHILE_SOURCE_PRESENT)
# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.buff([me])

```



<a id="card-0534"></a>

## 0534

固有急速；自身战场其他有增益友方单位+2

units:Selection[Unit]=me所在战场其他有增益友方单位，不含me，自己不在战场则空

```python

ops.modify_might(units, 2, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0535"></a>

## 0535

强化任选Energy1或Body1；强化持续+1

cost:Cost=选择其中一个基础费用Energy1或Body1，非相加;binding:CostBinding=仅未强化主动基础费用;dur:Duration=me留场且强化

```python

# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 持续
ops.modify_might([me], 1, duration=dur)

```



<a id="card-0536"></a>

## 0536

打出强制己装回拥有者手牌作额外成本

cost:Cost=所选友方装备返回其拥有者手牌;binding:CostBinding=强制打出额外费用

```python

ops.pay(p, cost, binding=binding)

```



<a id="card-0537"></a>

## 0537

固有关键词内部展开；不同注释为独立入口

dest:Location/Zone=本次合法打出位置;choices:ChoiceBinding=定稿选择是否支付急速附加费Energy1Fury1;subjects:CostSelection=本次打出me;extra:CostChange=该次所选急速附加费Energy1Fury1，不改印刷基础费;entry:EntryState=choices选择急速则ready否则默认，必须与完整费用支付一致;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

# 急速内部费用与入场展开
ops.modify_cost(subjects, extra, duration=THIS_PLAY)
ops.play(me, p, origin=p.hand, destination=dest, choices=choices, entry=entry)

```



<a id="card-0538"></a>

## 0538

固有坚守1；进攻眩晕此处敌军

u:Unit=此处所选敌军

```python

ops.stun([u])

```



<a id="card-0539"></a>

## 0539

任一对手距胜利≤3活跃入场；此处晕敌军持续−8最低1

dest:Location=合法打出地点;entry:EntryState=定稿时任一对手距胜利≤3则活跃，否则默认;units:Selection[Unit]=此处动态眩晕敌军

```python

# 基础打出
ops.play(me, p, origin=p.hand, destination=dest, entry=entry)
# 持续
ops.modify_might(units, -8, duration=WHILE_SOURCE_PRESENT, floor=1)

```

LANG:TC异画写差不到3，EN/SC/TC普通版为≤3，边界不同



<a id="card-0540"></a>

## 0540

反应法术，横置友方单位作额外费，抽1召1休眠

cost:Cost=横置所选友方单位;binding:CostBinding=强制打出额外费用

```python

# 定稿额外费
ops.pay(p, cost, binding=binding)
# 结算
ops.draw(p, 1)
ops.channel(p, 1, exhausted=True)

```



<a id="card-0541"></a>

## 0541

看3可选一牌抽取，其余指定牌置废；流转Energy2任意Power1

take:bool=选择抽牌;c:Card=实际看3中所选牌;rest:Selection[Card]=实际看见未抽取牌，无选择则全部

```python

ops.look(p, p.main_deck, 3)
if take:
    ops.draw(p, 1, cards=[c])
ops.transfer(rest, p.main_deck, p.trash)

```

FLOW_EXIT:尚未独立展开流转链项离链放逐替代

ACTION_ID:剩余指定牌通常仍在牌堆顶部，441.1将顶牌入废定义为Burn；但burn没有cards参数，不能保证先前抽取遭替代后仍准确处理原rest且保留Burn身份，现transfer片段不作完整证明



<a id="card-0542"></a>

## 0542

固有急速；每次移动从某处离开，在原地点打3战力瞬息Sprite

sprite:TokenTemplate=3战力且有Temporary的Sprite;origin:Location=该次移动的起点快照，不是me现在所在地点

```python

ops.play(sprite, p, origin=None, destination=origin)

```



<a id="card-0543"></a>

## 0543

p打出单位衍生物后自身+1；己方单位衍生物有壁垒

tokens:Selection[Unit]=动态己方单位衍生物

```python

# 打出单位衍生物触发
ops.modify_might([me], 1, duration=THIS_TURN)
# 持续
ops.grant_keyword(tokens, TANK, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0544"></a>

## 0544

反应法术，无效化法术，禁止其原控制者本回合再打法术

spell:ChainItem=所选法术;actor:Player=无效化前该法术控制者;restriction:RestrictionSpec=actor不能play spell类型，不禁止主动能力

```python

ops.counter(spell)
ops.restrict_action(actor, restriction, duration=THIS_TURN)

```



<a id="card-0545"></a>

## 0545

本回合有己军或己装死亡则活跃入场，按死亡事件历史而非废牌数量

dest:Location=合法打出地点;entry:EntryState=该历史为真则活跃，否则默认

```python

ops.play(me, p, origin=p.hand, destination=dest, entry=entry)

```



<a id="card-0546"></a>

## 0546

绝念，死亡前落单则抽1，不能拿死亡后空场面判断

alone:bool=自身离场前该地点没有其他友方单位的快照

```python

if alone:
    ops.draw(p, 1)

```



<a id="card-0547"></a>

## 0547

武装+2灵便打出免费贴附；独立装配Fury1

u:Unit=对应入口所选己方宿主;cost:Cost=Fury1;binding:CostBinding=普通装配主动基础费用

```python

# 灵便打出触发
ops.attach(me, u)
# 普通装配主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)

```



<a id="card-0548"></a>

## 0548

自己开始阶段触发，结算时手牌≤1才抽1

few:bool=执行抽牌前p手牌数≤1；不把该if移到触发注册前

```python

if few:
    ops.draw(p, 1)

```



<a id="card-0549"></a>

## 0549

固有伏击；打出给此处其他己军本回合强攻1

units:Selection[Unit]=此处其他己方单位

```python

ops.grant_keyword(units, ASSAULT, duration=THIS_TURN)

```



<a id="card-0550"></a>

## 0550

迅捷法术选一：战场单位打4，或杀任意装备

damage_mode:bool=所选伤害模式;u:Unit=所选战场单位;g:Gear=所选装备

```python

if damage_mode:
    ops.damage([u], 4)
else:
    ops.kill([g])

```



<a id="card-0551"></a>

## 0551

待命/反应法术，使所选单位本回合所有来源伤害翻倍

events:DamageSelection=所有将对选中单位造成伤害的事件，含战斗、自己来源

```python

ops.modify_damage(events, NumericChange(multiply=2), duration=THIS_TURN)

```



<a id="card-0552"></a>

## 0552

绝念，死亡前未落单则抽1

not_alone:bool=死亡前同地有其他友方单位快照

```python

if not_alone:
    ops.draw(p, 1)

```



<a id="card-0553"></a>

## 0553

p防守某战场时，可从当前地点移动me到该战场

b:Battlefield=本次防守事件的战场

```python

ops.move([me], b)

```



<a id="card-0554"></a>

## 0554

固有强攻1；进攻按自己当前强攻值对敌军伤害

u:Unit=此处所选敌军;n:IntExpr=me当前Assault数值，不是me当前战力

```python

ops.damage([u], n)

```



<a id="card-0555"></a>

## 0555

固有百炼；自身每回合首个征服后

 

```python

ops.ready([me])

```



<a id="card-0556"></a>

## 0556

移动后可令另一单位基础战力4本回合，不限友敌

u:Unit=除me外所选任意单位

```python

ops.set_base_might([u], 4, duration=THIS_TURN)

```



<a id="card-0557"></a>

## 0557

反应法术；无手牌也尽可能弃后继续抽2

 

```python

ops.discard(p, 1)
ops.draw(p, 2)

```



<a id="card-0558"></a>

## 0558

反应产费，横置本单位产Energy2限打出法术

cost:Cost=横置me;binding:CostBinding=反应产费主动基础费用;restriction:Predicate=仅用于打出spell

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.add_resources(p, ResourceBundle(energy=2), restriction=restriction)

```



<a id="card-0559"></a>

## 0559

p打出印刷Energy≥5法术后，不用实付额判断

 

```python

ops.modify_might([me], 3, duration=THIS_TURN)

```



<a id="card-0560"></a>

## 0560

绝念，在基地打3随从

recruit:TokenTemplate=1战力Recruit

```python

for i in range(3):
    ops.play(recruit, p, origin=None, destination=p.base)

```



<a id="card-0561"></a>

## 0561

固有壁垒；打出后战场任意单位移其基地

u:Unit=任意所选战场单位;base:Location=u对应基地

```python

ops.move([u], base)

```



<a id="card-0562"></a>

## 0562

不能变活跃；主动Chaos1，在自己战力严格高于目标敌方occupied战场敌军总战力时移入

restriction:RestrictionSpec=禁止对me执行ready，不把活跃入场混成ready;cost:Cost=Chaos1;binding:CostBinding=上述严格战力条件满足的主动基础费用;b:Battlefield=合法敌方occupied战场

```python

# 持续限制
ops.restrict_action(me, restriction, duration=WHILE_SOURCE_PRESENT)
# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.move([me], b)

```

LANG:SC目标写敌方控制战场而EN为敌方occupied，条件谓词不同



<a id="card-0563"></a>

## 0563

对手同时移动多军到me战场，除首军外每军强制任意Power1

subjects:CostSelection=对手同时移动多军到me战场的动作附加费用槽;change:CostChange=每批任意Power增加max(0,该批单位数−1)，不是所有move固定1

```python

ops.modify_cost(subjects, change, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0564"></a>

## 0564

me在战场时对手单位仅可打其基地；所有法术技能不能活跃敌军/敌装

players:PermissionSelection=所有对手;play_restriction:RestrictionSpec=对手单位打出目的地只可各自base，限制所有其他地点;targets:PermissionSelection=相对p的敌方单位及装备;ready_restriction:RestrictionSpec=禁止任何玩家法术/技能效果ready这些对象，不禁唤醒;dur:Duration=me留场且在战场

```python

ops.restrict_action(players, play_restriction, duration=dur)
ops.restrict_action(targets, ready_restriction, duration=dur)

```



<a id="card-0565"></a>

## 0565

其他己军持续活跃入场，包含未来单位，不是入场后活跃

 

```python

# 没有与该持续入场修饰等价的现有调用

```

ENTRY:play.entry只作用一次打出，缺持续修改所有其他己军入场状态的API



<a id="card-0566"></a>

## 0566

迅捷产费，杀友方单位或装备并横置me作为成本，产通用Power2

cost:Cost=杀一所选友方单位或装备及横置me;binding:CostBinding=迅捷产费主动基础费用;bundle:ResourceBundle=通用Power2

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.add_resources(p, bundle)

```



<a id="card-0567"></a>

## 0567

控制此战场期间，友方每个Repeat费用Energy−1

subjects:CostSelection=友方所有Repeat关键词的可选额外费用项，不改法术印刷基础费用;change:CostChange=Energy减1;dur:Duration=p控制此战场期间

```python

ops.modify_cost(subjects, change, duration=dur)

```



<a id="card-0568"></a>

## 0568

迅捷/回响Energy3；友方单位任意地点与战场敌军互殴

u:Unit=所选任意地点友方单位;v:Unit=所选战场敌军;m:IntExpr=u伤害前战力;n:IntExpr=v伤害前战力

```python

# 两方向各自片段，不当作同时程序
ops.damage([v], m, source=u)
ops.damage([u], n, source=v)

```

RECIPROCAL:缺多来源同时互殴批次；REPEAT:也缺回响各遍定稿及执行结构



<a id="card-0569"></a>

## 0569

可额外Order1，实付后打出晕战场敌军

cost:Cost=Order1;binding:CostBinding=可选打出额外费用;paid_extra:bool=本次额外费已付;u:Unit=所选敌方战场单位

```python

# 费用入口
ops.pay(p, cost, binding=binding)
# 打出触发
if paid_extra:
    ops.stun([u])

```



<a id="card-0570"></a>

## 0570

自身被弃后可Energy1给友方单位+2本回合

cost:Cost=Energy1;binding:CostBinding=可选被弃触发基础费用;u:Unit=所选友方单位

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_might([u], 2, duration=THIS_TURN)

```



<a id="card-0571"></a>

## 0571

友方单位独自进攻/防守后，该军+1本回合

u:Unit=本次独自进攻或防守友方单位，按该事件友军数判断

```python

ops.modify_might([u], 1, duration=THIS_TURN)

```



<a id="card-0572"></a>

## 0572

百炼打出触发：可装配p武装，装配费减任意Power1，允许已贴附武装

g:Gear=p控制的一件武装;cost:Cost=g的Equip费用减任意Power1最低0;binding:CostBinding=百炼可选触发费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(g, me)

```



<a id="card-0573"></a>

## 0573

放逐p拥有的卡后强化传奇；迅捷主动解除强化横置，弃1抽1

cost:Cost=解除me一层强化及横置me;binding:CostBinding=迅捷主动基础费用

```python

# 自有卡被你放逐触发
ops.empower([me])
# 迅捷主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.discard(p, 1)
    ops.draw(p, 1)

```



<a id="card-0574"></a>

## 0574

固有游走；无条件活跃入场

dest:Location=合法打出地点;entry:EntryState=活跃

```python

ops.play(me, p, origin=p.hand, destination=dest, entry=entry)

```



<a id="card-0575"></a>

## 0575

己方符文≥8期间持续+4

dur:Duration=me留场且p符文≥8

```python

ops.modify_might([me], 4, duration=dur)

```



<a id="card-0576"></a>

## 0576

固有狩猎2；XP≥6获得法盾游走

dur:Duration=me留场且pXP≥6

```python

ops.grant_keyword([me], DEFLECT, duration=dur)
ops.grant_keyword([me], GANKING, duration=dur)

```



<a id="card-0577"></a>

## 0577

等级3/6/11分别替代折扣Energy2/Calm1、4/2、6/3，不叠加；等级16不能被敌方选

subject:CostSelection=me打出费用;change:CostChange=按当前最高符合等级选择一项折扣，不符合则0;cost_duration:Duration=自身费用能力有效期;restriction:RestrictionSpec=禁止敌方法术/能力选择me;dur:Duration=me留场且pXP≥16

```python

ops.modify_cost(subject, change, duration=cost_duration)
ops.restrict_action(me, restriction, duration=dur)

```



<a id="card-0578"></a>

## 0578

成功强化其他物体后强化传奇；解除强化/任意Power1/横置主动活跃单位

cost:Cost=解除me一层强化、任意Power1及横置me;binding:CostBinding=主动基础费用;u:Unit=所选任意单位

```python

# 其他物体实际强化触发
ops.empower([me])
# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.ready([u])

```



<a id="card-0579"></a>

## 0579

3战力Mech单位衍生物，无文本能力

 

```python

# 基础类型/标签/战力已保留，没有额外算子调用

```



<a id="card-0580"></a>

## 0580

自己开始阶段各玩家展示顶牌；若己牌为最低Energy含并列则抽取己牌，其他回收

tops:Selection[Card]=各玩家各自主牌堆顶的实际可展示牌;lowest:bool=己牌Energy不大于所有其他展示牌，含并列;c:Card=己方展示顶牌;rest:Selection[Card]=未抽取的全部展示牌

```python

ops.reveal(tops)
if lowest:
    ops.draw(p, 1, cards=[c])
ops.recycle(rest)

```

ACTOR:原文各玩家分别reveal，reveal无行动玩家参数；不能用viewers改成各自秘密看牌



<a id="card-0581"></a>

## 0581

己方Mech持续坚守1

units:Selection[Unit]=己方动态Mech单位

```python

ops.grant_keyword(units, SHIELD, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0582"></a>

## 0582

反应法术；可横置友方单位额外费，已付抽2否则抽1，成本发生在抽牌前

cost:Cost=横置所选友方单位;binding:CostBinding=可选打出额外费用;paid_extra:bool=本次额外费已付

```python

# 定稿费用
ops.pay(p, cost, binding=binding)
# 法术结算
ops.draw(p, 2 if paid_extra else 1)

```



<a id="card-0583"></a>

## 0583

无规则文字的普通单位，保留8战力及其他基础属性

 

```python

# 无额外文本能力，不为白板造空效果

```



<a id="card-0584"></a>

## 0584

主动XP3，给执行时此处所有己军游走本回合

cost:Cost=消耗XP3;binding:CostBinding=主动基础费用;units:Selection[Unit]=此处所有己军，含me

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.grant_keyword(units, GANKING, duration=THIS_TURN)

```



<a id="card-0585"></a>

## 0585

强化以弃一法术为费；实际变强化时放逐敌方战场≤3战力单位

cost:Cost=弃所选法术牌1;binding:CostBinding=仅未强化的强化主动基础费用;u:Unit=敌方战场战力≤3所选单位

```python

# 强化主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 实际变强化触发
ops.banish([u])

```



<a id="card-0586"></a>

## 0586

打出抽1；强化Energy3；强化时己方法术能力不可无效化，给所选单位负战力额外−1

cost:Cost=Energy3;binding:CostBinding=仅未强化主动基础费用;subjects:PermissionSelection=己方法术和能力链项;restriction:RestrictionSpec=不能被counter;effects:EffectSelection=己方法术/技能对其正式目标单位的负战力指令;dur:Duration=me留场且强化

```python

# 打出
ops.draw(p, 1)
# 强化
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 强化持续
ops.restrict_action(subjects, restriction, duration=dur)
ops.modify_effect_value(effects, REDUCTION_AMOUNT, NumericChange(add=1), duration=dur)

```



<a id="card-0587"></a>

## 0587

反应法术选友方单位回手或敌军−2本回合

return_mode:bool=所选回手模式;u:Unit=该模式要求友方单位，另一模式要求敌军;origin:Zone=u场上区域

```python

if return_mode:
    ops.transfer([u], origin, u.owner.hand)
else:
    ops.modify_might([u], -2, duration=THIS_TURN)

```



<a id="card-0588"></a>

## 0588

自己打Energy≥7牌时在己废牌的此牌可Order1替代基础费用打出

dest:Location=合法单位目的地;policy:CostPolicy=基础费替代为Order1;permit:PlayPermission=本次废牌触发允许该牌在此时打出

```python

ops.play(me, p, origin=p.trash, destination=dest, cost_policy=policy, permission=permit)

```



<a id="card-0589"></a>

## 0589

征服且该战场己军≥4触发

 

```python

ops.draw(p, 2)

```



<a id="card-0590"></a>

## 0590

移入战场后，模式全体各弃1或全体各抽1

actors:list[Player]=所有玩家按规则处理顺序;discard_mode:bool=所选弃置模式

```python

for actor in actors:
    if discard_mode:
        ops.discard(actor, 1)
    else:
        ops.draw(actor, 1)

```

PLAYER_BATCH:各玩家动作的同一指令批次/顺序边界未在当前API中明确，不能仅有循环就证明完整等价



<a id="card-0591"></a>

## 0591

基础Mind符文无文字；规则164.2赋予两项反应产费能力

exhaust_cost:Cost=横置该符文;exhaust_binding:CostBinding=反应产Energy基础费用;recycle_cost:Cost=回收该符文;recycle_binding:CostBinding=反应产Power基础费用;power:ResourceBundle=Mind领域Power1

```python

# 横置产Energy
paid = ops.pay(p, exhaust_cost, binding=exhaust_binding)
if paid.value is not None:
    ops.add_resources(p, ResourceBundle(energy=1))
# 回收产Power
paid = ops.pay(p, recycle_cost, binding=recycle_binding)
if paid.value is not None:
    ops.add_resources(p, power)

```



<a id="card-0592"></a>

## 0592

打出所选对手展手牌，己方选其中一张让该对手弃置

actor:Player=所选对手;hand:Selection[Card]=其展示时手牌;c:Card=p从这批手牌中选的牌

```python

ops.reveal(hand)
ops.discard(actor, 1, cards=[c], chooser=p)

```

ACTOR:reveal无行动玩家，原文They reveal不能仅以p的reveal(hand)认定主体已准确表达



<a id="card-0593"></a>

## 0593

征服此处，把己主牌堆顶2放废牌；按规则441.1的顶牌入废动作定义

 

```python

ops.burn(p, 2)

```



<a id="card-0594"></a>

## 0594

所有单位不能move到基地，不禁止recall

units:PermissionSelection=所有玩家单位;restriction:RestrictionSpec=move目的地不得为base

```python

ops.restrict_action(units, restriction, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0595"></a>

## 0595

选单位，打活跃Reflection基地，再自反项复制该单位并赋瞬息

reflection:TokenTemplate=Reflection原模板;entry:EntryState=活跃

```python

ops.play(reflection, p, origin=None, destination=p.base, entry=entry)

```

REFLEXIVE:勘误then do this要求新待处理项绑定实际Reflection后copy/Temporary，不能把ChainItem当Permanent



<a id="card-0596"></a>

## 0596

待命；仅打到战场时触发对该处敌军打2

u:Unit=该战场所选敌军

```python

ops.damage([u], 2)

```



<a id="card-0597"></a>

## 0597

自己可打到open战场；在场时其他友方单位也可打open；不授反应

permit:PermissionSpec=单位可从正常合法来源打到open战场;own_duration:Duration=自身在可打出区域且该权限有效期间;others:PermissionSelection=其他友方单位

```python

# 自身打出权限
ops.grant_permission(me, permit, duration=own_duration)
# 留场给其他单位权限
ops.grant_permission(others, permit, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0598"></a>

## 0598

固有急速游走；每回合首移可活跃另一休眠物体

objects:Selection[Permanent]=候选中的其他休眠单位/装备部分，不含me

```python

ops.ready(objects)

```

RUNE_READY:原文明确包括Rune，ready签名排除；LEGEND_READY:也包含Legend；LANG:TC未明确排除自身，EN/SC排除



<a id="card-0599"></a>

## 0599

固有急速；移到战场后XP2

 

```python

ops.gain_xp(p, 2)

```



<a id="card-0600"></a>

## 0600

成功给友方单位新增增益时，可Body1且横置本装使同军活跃

cost:Cost=Body1及横置me;binding:CostBinding=可选成功增益触发基础费用;u:Unit=该次实际新获增益友方单位

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.ready([u])

```



<a id="card-0601"></a>

## 0601

召1休眠，若实际没有召出则抽1

 

```python

r = ops.channel(p, 1, exhausted=True)
if not r.value:
    ops.draw(p, 1)

```



<a id="card-0602"></a>

## 0602

待命；打出触发若当前不是p回合则赋自身瞬息

off_turn:bool=该触发结算时当前回合非p

```python

if off_turn:
    ops.grant_keyword([me], TEMPORARY, duration=PERMANENT)

```



<a id="card-0603"></a>

## 0603

征服此处可消耗一个己方增益为触发费抽1

cost:Cost=消耗所选己方一个增益;binding:CostBinding=可选征服触发基础费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.draw(p, 1)

```



<a id="card-0604"></a>

## 0604

任一对手控制晕单位时，费用Energy−2且活跃入场

subject:CostSelection=me打出费用;change:CostChange=Energy减2;dur:Duration=费用有效区域且任一对手控制眩晕单位;dest:Location=合法打出地点;entry:EntryState=实际入场时该条件为真则活跃，否则默认

```python

# 费用
ops.modify_cost(subject, change, duration=dur)
# 基础打出
ops.play(me, p, origin=p.hand, destination=dest, entry=entry)

```



<a id="card-0605"></a>

## 0605

迅捷法术，打2战场单位，控制盖放卡则改4

u:Unit=所选战场单位;has_hidden:bool=结算时p控制至少一盖放卡，不当作检查Hidden关键词

```python

ops.damage([u], 4 if has_hidden else 2)

```



<a id="card-0606"></a>

## 0606

迅捷法术；选有己军战场，可移至多一敌军到此，再此处敌军全−2

b:Battlefield=有己军的所选战场;take:bool=选择移动一敌军;u:Unit=所选敌军;units:Selection[Unit]=移动后b内全敌军

```python

if take:
    ops.move([u], b)
ops.modify_might(units, -2, duration=THIS_TURN)

```



<a id="card-0607"></a>

## 0607

反应法术，单位−10本回合

u:Unit=所选任意单位

```python

ops.modify_might([u], -10, duration=THIS_TURN)

```



<a id="card-0608"></a>

## 0608

迅捷法术，己废牌单位回手

c:Card=所选己废牌单位

```python

ops.transfer([c], p.trash, p.hand)

```



<a id="card-0609"></a>

## 0609

自身打出或进攻可弃1作触发费，杀单位或装备

cost:Cost=弃所选手牌1;binding:CostBinding=可选打出/进攻触发基础费用;c:Permanent=所选任意单位或装备

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.kill([c])

```



<a id="card-0610"></a>

## 0610

固有急速强攻3；每回合一次将死可杀友军改治疗横置召回

 

```python

# 不立即kill友军再治疗已经死亡的me

```

REPLACE:缺每回合一次可选死亡前替代登记，放弃较早替代不应消耗后续次数



<a id="card-0611"></a>

## 0611

固有伏击；打出按目标当前伤害标记数量再伤害，不是战力减值

u:Unit=所选单位;n:IntExpr=执行时u已标记的伤害数量

```python

ops.damage([u], n)

```



<a id="card-0612"></a>

## 0612

狩猎2；等级3持续+1及法盾1

dur:Duration=me留场且pXP≥3

```python

ops.modify_might([me], 1, duration=dur)
ops.grant_keyword([me], DEFLECT, duration=dur)

```



<a id="card-0613"></a>

## 0613

无规则文字的10战力Dragon单位

 

```python

# 保留基础属性，无独立文本动作

```



<a id="card-0614"></a>

## 0614

绝念，可摧毁死亡前地点单位或装备，位置来自LKI

c:Permanent=死亡前地点合法所选单位或装备

```python

ops.kill([c])

```



<a id="card-0615"></a>

## 0615

自身参加过的战斗结束时强化；强化持续+2

dur:Duration=me留场且已强化

```python

# 战斗结束触发
ops.empower([me])
# 持续
ops.modify_might([me], 2, duration=dur)

```



<a id="card-0616"></a>

## 0616

自己开始阶段开始时，若战场控制盖放卡则抽1，按原句作为触发条件

 

```python

ops.draw(p, 1)

```



<a id="card-0617"></a>

## 0617

固有坚守2及壁垒内部展开

defending:bool=me为防守方;scope:RuleScope=me同控制者参战单位承伤顺序;change:RuleChange=先承担致死伤害;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if defending:
    ops.modify_might([me], 2, duration=WHILE_CONDITION)
ops.modify_rule(COMBAT_DAMAGE_ORDER, scope, change, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0618"></a>

## 0618

固有缴械2；打出洞察2

 

```python

ops.predict(p, 2)

```



<a id="card-0619"></a>

## 0619

仅预知；自身打出触发直接展开为洞察1

 

```python

ops.predict(p)

```



<a id="card-0620"></a>

## 0620

反应法术，夺法术控制权，可重做全部选择，非只改目标

spell:ChainItem=所选法术;redo:bool=新控制者选择重新作选择

```python

ops.change_control([spell], p)
if redo:
    ops.redo_choices(spell, p)

```

LANG:SC只明确新目标，EN/TC可重做模式等选择；不把全部选择删成targets-only



<a id="card-0621"></a>

## 0621

此处对决期间，所有玩家打有Reaction牌额外任意Power1，不扩成全部能力

subjects:CostSelection=此处Showdown期间实际有Reaction的卡牌打出费用；盖放的Reaction权限需下一回合已生效;change:CostChange=任意Power需求增加1;dur:Duration=该战场存在且此处Showdown进行中

```python

ops.modify_cost(subjects, change, duration=dur)

```



<a id="card-0622"></a>

## 0622

可额外Calm1，实付打出晕敌军；自身据守后本回合下一单位打出活跃并增益

cost:Cost=Calm1;binding:CostBinding=可选打出额外费用;paid_extra:bool=该次额外费已付;u:Unit=所选任意敌军

```python

# 额外费用
ops.pay(p, cost, binding=binding)
# 打出触发
if paid_extra:
    ops.stun([u])

```

DELAY:据守后需登记下一次实际打出的单位再ready/buff，不能当作活跃入场也不能预先增益手牌



<a id="card-0623"></a>

## 0623

固有法盾2；强化Energy8；强化时自身征服额外得1

cost:Cost=Energy8;binding:CostBinding=仅未强化主动基础费用

```python

# 强化主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 强化时自身征服触发
ops.gain_points(p, 1)

```



<a id="card-0624"></a>

## 0624

每回合一次，此处敌军死亡后召1休眠符文

 

```python

ops.channel(p, 1, exhausted=True)

```



<a id="card-0625"></a>

## 0625

p据守此处，给此处任意单位增益，不限己方

u:Unit=此处所选单位

```python

ops.buff([u])

```



<a id="card-0626"></a>

## 0626

固有法盾1：对手以法术或技能选择本实例时附加任意Power1

subjects:CostSelection=对手法术/技能为选择me须付的目标附加费用，同一能力选择me不重复收取;change:CostChange=额外任意Power1

```python

ops.modify_cost(subjects, change, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0627"></a>

## 0627

武装+0；装配Energy1；宿主坚守2

cost:Cost=Energy1;binding:CostBinding=装配基础费用;u:Unit=p控制的宿主;host:Selection[Unit]=当前宿主;params:KeywordParameters=Shield.value为2;dur:Duration=仍贴附期间

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 宿主效果
ops.grant_keyword(host, SHIELD, parameters=params, duration=dur)

```

DATA:SC缺printedEffectText的坚守2



<a id="card-0628"></a>

## 0628

固有坚守5壁垒；本回合每个通过Hold实际取得的分数减Energy2/Calm1

subject:CostSelection=me打出费用;change:CostChange=Energy减2乘该Hold实得分数，Calm减同量分数；不按Hold事件次数;dur:Duration=本费用能力有效期间

```python

ops.modify_cost(subject, change, duration=dur)

```



<a id="card-0629"></a>

## 0629

按勘误构筑另选至多3不同名额外传奇；打出从中选1加入传奇区直到me离场

choice:SetupChoiceRef=从该副牌构筑预选的不同名额外传奇中选定一项;link:Link=本Neeko实例与该传奇的关联;dur:Duration=仅该Neeko实例仍在场期间

```python

ops.add_legend(p, choice, duration=dur, link=link)

```

SETUP:69API没有构筑阶段的选择/保存SetupChoiceRef接口，choose.bind_at仅trigger/finalization/resolution；只能消费已提供预选，不能声称整条构筑能力已覆盖



<a id="card-0630"></a>

## 0630

固有伏击；自身赢战斗后

 

```python

ops.draw(p, 1)

```



<a id="card-0631"></a>

## 0631

固有急速游走；自身移动后

 

```python

ops.gain_xp(p, 1)

```



<a id="card-0632"></a>

## 0632

敌军进攻p控制战场后，逐个−1最低1本回合，按勘误

u:Unit=该次进攻p所控战场的敌军

```python

ops.modify_might([u], -1, duration=THIS_TURN, floor=1)

```



<a id="card-0633"></a>

## 0633

固有游走；按勘误在查看/展示己牌堆顶自己过程中可放逐并Power1打出

take:bool=选择放逐并打出;dest:Location=合法目的地;policy:CostPolicy=仅任意Power1替代基础费用;permit:PlayPermission=本次从主牌堆查看/展示过程放逐后允许打出自己

```python

# 仅在正确as-view钩子已提供时可执行的片段
if take:
    ops.banish([me])
    ops.play(me, p, origin=p.banishment, destination=dest, cost_policy=policy, permission=permit)

```

AS_VIEW:look/reveal没有查看/展示进行中进入此能力的钩子；不得改成事后普通触发或先抽到手再发动



<a id="card-0634"></a>

## 0634

反应法术，无效化敌方正式选择了己方单位/装备的法术或能力

item:ChainItem=符合该目标条件的敌方法术或能力

```python

ops.counter(item)

```



<a id="card-0635"></a>

## 0635

自身征服可杀印刷Energy≤自己当前战力装备

g:Gear=符合该Energy上限的所选任意装备

```python

ops.kill([g])

```



<a id="card-0636"></a>

## 0636

移动到战场后，在目的地打随从

recruit:TokenTemplate=1战力Recruit

```python

ops.play(recruit, p, origin=None, destination=here)

```



<a id="card-0637"></a>

## 0637

强化Energy1/Order1；以强化状态死亡才在基地打2随从

cost:Cost=Energy1/Order1;binding:CostBinding=仅未强化主动基础费用;recruit:TokenTemplate=1战力Recruit

```python

# 强化
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 死亡前强化状态为真的绝念
for i in range(2):
    ops.play(recruit, p, origin=None, destination=p.base)

```

DATA:SC含损坏的嵌套绝念分隔标记，保留原文并参考EN与中文括号说明



<a id="card-0638"></a>

## 0638

迅捷法术，鼓舞则立刻杀所选单位，否则本回合下一次受伤后杀

u:Unit=所选单位;legion:bool=本回合已定稿另一张卡

```python

if legion:
    ops.kill([u])

```

DELAY:未鼓舞分支缺登记该实例下一次实际受伤后的摧毁触发



<a id="card-0639"></a>

## 0639

鼓舞条件持续费用Energy−2

subject:CostSelection=me打出费用;change:CostChange=Energy减2;dur:Duration=费用计算且p本回合已定稿另一牌

```python

ops.modify_cost(subject, change, duration=dur)

```



<a id="card-0640"></a>

## 0640

自己所在战场对手不能从盖放翻开打牌；EN旧措辞reveal与SC翻开打出需区分

subjects:PermissionSelection=对手在此处的盖放牌;restriction:RestrictionSpec=禁止将这些牌从盖放执行play，不禁止规则要求的离区公开

```python

ops.restrict_action(subjects, restriction, duration=WHILE_SOURCE_PRESENT)

```

LANG:EN/TC用revealed，SC明确翻开打出，不能把技术动作Reveal和Play直接等同；需旧术语解释



<a id="card-0641"></a>

## 0641

迅捷法术，友方单位坚守2本回合，再法术对任意敌军按该军新坚守值伤害

u:Unit=所选友方单位;v:Unit=所选敌军，不限战场;params:KeywordParameters=Shield.value为2;n:IntExpr=授予后u的当前Shield总值，不是只有新加的2

```python

ops.grant_keyword([u], SHIELD, parameters=params, duration=THIS_TURN)
ops.damage([v], n)

```



<a id="card-0642"></a>

## 0642

自己开始阶段且符文少于至少一对手，+2和游走本回合

 

```python

ops.modify_might([me], 2, duration=THIS_TURN)
ops.grant_keyword([me], GANKING, duration=THIS_TURN)

```



<a id="card-0643"></a>

## 0643

每玩家自己的首个开始阶段开始，各该玩家召1默认活跃符文

actor:Player=当前进入自己第一个BeginningPhase的玩家

```python

ops.channel(actor, 1)

```



<a id="card-0644"></a>

## 0644

自身可打open；打出可回一非Dragon单位手牌

permit:PermissionSpec=me打出额外允许open战场，未改时机;dur:Duration=me在可打出区域且该权限生效;u:Unit=所选非Dragon单位，不限友敌;origin:Zone=u场上区域

```python

# 自身权限
ops.grant_permission(me, permit, duration=dur)
# 打出触发
ops.transfer([u], origin, u.owner.hand)

```



<a id="card-0645"></a>

## 0645

p自己第1/2/3回合不能打出此牌，其他玩家回合不无端套同一限制

restriction:RestrictionSpec=当前为p自己第1至第3回合时禁止play本卡;dur:Duration=本卡打出限制规则有效期间

```python

ops.restrict_action(me, restriction, duration=dur)

```



<a id="card-0646"></a>

## 0646

法术活跃p控制的所有单位

units:Selection[Unit]=p控制的全部单位

```python

ops.ready(units)

```



<a id="card-0647"></a>

## 0647

迅捷法术，给友方单位增益并晕敌军，不要求同地点

u:Unit=友方所选单位;v:Unit=敌方所选单位

```python

ops.buff([u])
ops.stun([v])

```



<a id="card-0648"></a>

## 0648

单位+6本回合；流转Energy4

u:Unit=所选单位

```python

ops.modify_might([u], 6, duration=THIS_TURN)

```

FLOW_EXIT:尚未独立展开流转离链放逐替代



<a id="card-0649"></a>

## 0649

装备横置主动，任意单位−1最低1本回合

cost:Cost=横置me;binding:CostBinding=主动基础费用;u:Unit=所选单位

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_might([u], -1, duration=THIS_TURN, floor=1)

```



<a id="card-0650"></a>

## 0650

基础Order符文，规则164.2两项反应产费

exhaust_cost:Cost=横置该符文;exhaust_binding:CostBinding=反应Energy主动基础费用;recycle_cost:Cost=回收该符文;recycle_binding:CostBinding=反应Power主动基础费用;power:ResourceBundle=Order领域Power1

```python

# 横置产Energy
paid = ops.pay(p, exhaust_cost, binding=exhaust_binding)
if paid.value is not None:
    ops.add_resources(p, ResourceBundle(energy=1))
# 回收产Power
paid = ops.pay(p, recycle_cost, binding=recycle_binding)
if paid.value is not None:
    ops.add_resources(p, power)

```

DATA:一EN印刷rules只有句点，不把句点当未解释效果；基础符文能力来自明确规则而非零值推测

DATA:同一本体有非空规则文本，但这些变体printedRulesText为空：EN OGN-214, SC OGN-214, TC OGN-214



<a id="card-0651"></a>

## 0651

固有坚守1；此处无己方装备时不能造成战斗伤害

restriction:RestrictionSpec=仅禁止me造成战斗伤害;dur:Duration=me留场且此处没有友方gear

```python

ops.restrict_action(me, restriction, duration=dur)

```



<a id="card-0652"></a>

## 0652

每回合一次可选，me在战场时打装备少Energy1/任意Power1，可保留不用

subjects:CostSelection=本回合玩家选择使用此优惠的那次gear打出费用;change:CostChange=Energy减1及任意Power减1;dur:Duration=me留场且在战场

```python

ops.modify_cost(subjects, change, duration=dur, uses=1)

```

OPTIONAL_COST:uses只有次数没有每回合重置或拒绝不消耗的明确政策，不能把once-each-turn做成留场期间仅一次



<a id="card-0653"></a>

## 0653

打出或据守看4，可展示装备抽取，余回收

take:bool=选择抽装备;c:Card=实际看4中所选gear;rest:Selection[Card]=实际看见未抽取者，无选择则全部

```python

ops.look(p, p.main_deck, 4)
if take:
    ops.reveal([c])
    ops.draw(p, 1, cards=[c])
ops.recycle(rest)

```



<a id="card-0654"></a>

## 0654

固有法盾2百炼；自身战力动态+友方装备数

n:IntExpr=动态友方gear数量，不仅Equipment

```python

ops.modify_might([me], n, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0655"></a>

## 0655

控制战场时，每回合首个friendly非衍生物gear的Energy−1

subjects:CostSelection=当回合首个符合friendly且非token的gear打出，不按每种类型另计;change:CostChange=Energy减1;dur:Duration=p控制本战场期间

```python

ops.modify_cost(subjects, change, duration=dur)

```



<a id="card-0656"></a>

## 0656

任意玩家自己第1/2回合将因征服/据守得1分时改抽1，Scored仍按规则处理

 

```python

# 不直接draw，也不禁止征服/据守流程

```

REPLACE:缺按玩家回合序号与增分来源改写GainPoint为Draw的事件替代接口



<a id="card-0657"></a>

## 0657

在战场且此处有友方Deploy装备，持续+1

dur:Duration=me留场且其战场有至少一友方Deploy装备

```python

ops.modify_might([me], 1, duration=dur)

```



<a id="card-0658"></a>

## 0658

迅捷法术，对每个p单位可消耗其一个增益来活跃，最后给所有p单位增益

chosen:list[Unit]=p选择消耗增益的单位；每个只消耗一个，即使李青有多层;costs:dict[Unit,Cost]=各单位消耗一个增益;bindings:dict[Unit,CostBinding]=对该单位活跃的指令内费用;units:Selection[Unit]=最后一步的所有p单位

```python

for u in chosen:
    paid = ops.pay(p, costs[u], binding=bindings[u])
    if paid.value is not None:
        ops.ready([u])
ops.buff(units)

```



<a id="card-0659"></a>

## 0659

自身防守可杀自己为触发基础费，将一攻击者移其基地

cost:Cost=杀me;binding:CostBinding=可选防守触发基础费用;u:Unit=所选攻击者;base:Location=u对应基地

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.move([u], base)

```



<a id="card-0660"></a>

## 0660

装备横置，将另一友方单位/装备/盖放牌回拥有者手牌，勘误不检查盖放牌Hidden属性

cost:Cost=横置me;binding:CostBinding=主动基础费用;c:Card=另一友方单位、装备或正面朝下牌；不含本装备;origin:Zone=c场上或盖放区域

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.transfer([c], origin, c.owner.hand)

```



<a id="card-0661"></a>

## 0661

此处所有Champion超类型单位+1，不限友敌

units:Selection[Unit]=此处动态Champion单位

```python

ops.modify_might(units, 1, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0662"></a>

## 0662

只有固有待命

dest:Location=基础打出合法地点

```python

ops.play(me, p, origin=p.hand, destination=dest)

```

DELEGATED:只展示普通打出路径，未独立展开盖放费用、保持控制、下一回合反应授权及限定战场目标



<a id="card-0663"></a>

## 0663

移动后展示己顶，是单位抽取，否则置废牌且自身+2

top:list[Card]=主牌堆顶部至多1张

```python

ops.reveal(top)
if top and "unit" in top[0].types:
    ops.draw(p, 1, cards=top)
else:
    if top:
        ops.burn(p, 1)
    ops.modify_might([me], 2, duration=THIS_TURN)

```



<a id="card-0664"></a>

## 0664

强制一友方单位回其拥有者手牌为打出额外费，战场单位打5

cost:Cost=所选友方单位回其拥有者手牌;binding:CostBinding=强制打出额外费用;u:Unit=所选战场单位

```python

# 费用
ops.pay(p, cost, binding=binding)
# 结算
ops.damage([u], 5)

```



<a id="card-0665"></a>

## 0665

固有壁垒；每个p控制休眠单位自身Energy−1

subject:CostSelection=me打出费用;change:CostChange=Energy减少动态p控制休眠单位数;dur:Duration=本费用能力有效期间

```python

ops.modify_cost(subject, change, duration=dur)

```



<a id="card-0666"></a>

## 0666

其他每名玩家先选Cards或Runes，再对每个结果让p与该玩家各抽1或各召1休眠

actors:list[Player]=除p外玩家，按规则处理顺序;options:list[ObjectCategory]=合法选项Cards和Runes;choices:dict[Player,ObjectCategory]=各declare实际结果

```python

for actor in actors:
    ops.declare(actor, options)
for actor in actors:
    if choices[actor] == CARDS:
        ops.draw(p, 1)
        ops.draw(actor, 1)
    else:
        ops.channel(p, 1, exhausted=True)
        ops.channel(actor, 1, exhausted=True)

```

PLAYER_BATCH:各对玩家同一指令的共同抽牌/召出批次未明定，不能只凭串行两调用证明等价



<a id="card-0667"></a>

## 0667

单位兼装备，默认休眠入场；打出且控制≥3其他gear则抽1，不将自身算其他装备

 

```python

ops.draw(p, 1)

```



<a id="card-0668"></a>

## 0668

打出先增益自身，再若位于战场增益其他友军

at_battlefield:bool=第二步执行时me在战场;others:Selection[Unit]=该战场其他friendly单位，不含me

```python

ops.buff([me])
if at_battlefield:
    ops.buff(others)

```

LANG:SC第二步含自己且条件写打出到战场，EN/TC排除自己并读当前地点；增益上限例外下可能有实际差异



<a id="card-0669"></a>

## 0669

武装+1；装配Fury1；宿主移到战场后本回合+2

cost:Cost=Fury1;binding:CostBinding=装配基础费用;u:Unit=p控制的宿主;host:Unit=本装备当前宿主

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 宿主移到战场触发
ops.modify_might([host], 2, duration=THIS_TURN)

```

DATA:SC未提供printedEffectText的宿主移动加战力



<a id="card-0670"></a>

## 0670

只能打到本回合已征服战场，不得打其他地点

restriction:RestrictionSpec=禁止me打到不属于p本回合已征服战场的地点，包含基地;permit:PermissionSpec=该牌卡面指明可打到p本回合已征服战场；其他未覆盖限制仍保留;dur:Duration=该牌可打出区域的能力有效期间

```python

ops.grant_permission(me, permit, duration=dur)
ops.restrict_action(me, restriction, duration=dur)

```



<a id="card-0671"></a>

## 0671

单位活跃并强攻3本回合；流转Energy3/Fury1

u:Unit=所选任意单位;params:KeywordParameters=Assault.value为3

```python

ops.ready([u])
ops.grant_keyword([u], ASSAULT, parameters=params, duration=THIS_TURN)

```

FLOW_EXIT:尚未独立描述流转离链放逐替代



<a id="card-0672"></a>

## 0672

自身战场每个p控制的Temporary单位自身+1，自己若符合也计入

n:IntExpr=动态me战场p控制且有Temporary单位数；非战场时0

```python

ops.modify_might([me], n, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0673"></a>

## 0673

本装备固有瞬息；friendly单位持续法盾1

units:Selection[Unit]=所有friendly单位，不只同地

```python

ops.grant_keyword(units, DEFLECT, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0674"></a>

## 0674

固有Assault1的内部持续效果：me进攻时战力加1

attacking:bool=me是进攻方;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if attacking:
    ops.modify_might([me], 1, duration=WHILE_CONDITION)

```



<a id="card-0675"></a>

## 0675

打出可杀Energy≤1任意装备，实际如此做产休眠金币

g:Gear=印刷Energy≤1所选任意装备;gold:TokenTemplate=金币;entry:EntryState=休眠

```python

r = ops.kill([g])
if r.changed:
    ops.play(gold, p, origin=None, destination=p.base, entry=entry)

```



<a id="card-0676"></a>

## 0676

回响Energy2/Fury1；先战场单位打2，再至多另一任意地点单位打2

first:Unit=所选战场单位;second:Selection[Unit]=至多1另一个单位，不限战场

```python

ops.damage([first], 2)
ops.damage(second, 2)

```

REPEAT:只表达单遍两个顺序指令，未定义回响多遍定稿选择和执行



<a id="card-0677"></a>

## 0677

部署；自身打出或p征服此处时友方单位增益

u:Unit=所选friendly单位，不限本地点

```python

ops.buff([u])

```



<a id="card-0678"></a>

## 0678

控制此战场时，每回合首个friendly装备主动能力Energy−1，不减装备打出费用

subjects:CostSelection=当前回合首个friendly gear的activated ability费用;change:CostChange=Energy减1;dur:Duration=p控制本战场

```python

ops.modify_cost(subjects, change, duration=dur)

```



<a id="card-0679"></a>

## 0679

p每次打牌后，可令自己基础战力本回合等该牌Energy

n:IntExpr=该次已打出牌的印刷/复制Energy，不读取实际花费

```python

ops.set_base_might([me], n, duration=THIS_TURN)

```



<a id="card-0680"></a>

## 0680

p征服且相关战斗分配过量≥3，可横置传奇活跃任意单位

cost:Cost=横置me;binding:CostBinding=具有该分配历史条件的可选征服触发基础费用;u:Unit=所选任意单位

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.ready([u])

```



<a id="card-0681"></a>

## 0681

由p实际使一friendly单位变活跃后，该单位+1本回合，不计活跃入场

u:Unit=本次实际被p活跃的friendly单位

```python

ops.modify_might([u], 1, duration=THIS_TURN)

```



<a id="card-0682"></a>

## 0682

p打出装备后

 

```python

ops.ready([me])

```



<a id="card-0683"></a>

## 0683

打出给另一friendly单位增益

u:Unit=除me外所选friendly单位

```python

ops.buff([u])

```



<a id="card-0684"></a>

## 0684

横置主动眩晕任意地点敌军

cost:Cost=横置me;binding:CostBinding=主动基础费用;u:Unit=所选敌军

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.stun([u])

```



<a id="card-0685"></a>

## 0685

装备休眠进场；强化Energy1横置；反应横置产Energy1，强化则改2

entry:EntryState=休眠;ecost:Cost=Energy1及横置me;eb:CostBinding=仅未强化主动基础费用;cost:Cost=横置me;binding:CostBinding=反应产费主动基础费用;empowered:bool=产费结算时me强化

```python

# 基础打出
ops.play(me, p, origin=p.hand, destination=p.base, entry=entry)
# 强化主动
paid = ops.pay(p, ecost, binding=eb)
if paid.value is not None:
    ops.empower([me])
# 反应产费
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.add_resources(p, ResourceBundle(energy=2 if empowered else 1))

```



<a id="card-0686"></a>

## 0686

普通5战力单位无规则文字

 

```python

# 只保留基础属性，不生成多余动作

```



<a id="card-0687"></a>

## 0687

固有法盾；p控制的每件gear令自身Energy−1

subject:CostSelection=me打出费用;change:CostChange=Energy减p当前控制的gear数;dur:Duration=费用能力有效期间

```python

ops.modify_cost(subject, change, duration=dur)

```



<a id="card-0688"></a>

## 0688

自身征服后

gold:TokenTemplate=金币;entry:EntryState=休眠

```python

ops.play(gold, p, origin=None, destination=p.base, entry=entry)

```



<a id="card-0689"></a>

## 0689

固有伏击壁垒；可XP3额外费用令自身Energy−3

cost:Cost=消耗XP3;binding:CostBinding=可选打出额外费用;subject:CostSelection=本次me费用;change:CostChange=Energy减3

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_cost(subject, change, duration=UNTIL_EFFECT_END, uses=1)

```



<a id="card-0690"></a>

## 0690

固有法盾；打出且对手距胜利≤3则活跃并XP3

 

```python

ops.ready([me])
ops.gain_xp(p, 3)

```



<a id="card-0691"></a>

## 0691

打出且p控制Poro时增益自身并抽1；抽牌不以实际新增增益成功为条件

 

```python

ops.buff([me])
ops.draw(p, 1)

```



<a id="card-0692"></a>

## 0692

打出抽1；主动Energy1/Calm1横置且杀自己抽1

cost:Cost=Energy1/Calm1、横置me及杀me的同一合法组合;binding:CostBinding=主动基础费用

```python

# 打出触发
ops.draw(p, 1)
# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.draw(p, 1)

```



<a id="card-0693"></a>

## 0693

部署；打出可Body1活跃此处任意单位；此处friendly单位持续游走

cost:Cost=Body1;binding:CostBinding=可选打出触发基础费用;u:Unit=此处所选任意单位;units:Selection[Unit]=此处动态friendly单位

```python

# 打出触发
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.ready([u])
# 持续
ops.grant_keyword(units, GANKING, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0694"></a>

## 0694

迅捷法术，放逐友方单位，再按勘误由拥有者免费打到其基地

u:Unit=所选friendly单位;owner:Player=u拥有者

```python

ops.banish([u])
ops.play(u, owner, origin=owner.banishment, destination=owner.base, cost_policy=IGNORE_BASE_COST)

```



<a id="card-0695"></a>

## 0695

迅捷法术，夺控战场敌军并召回，不横置

u:Unit=所选战场敌军

```python

ops.change_control([u], p)
ops.recall([u])

```



<a id="card-0696"></a>

## 0696

固有法盾1：对手以法术或技能选择本实例时附加任意Power1

subjects:CostSelection=对手法术/技能为选择me须付的目标附加费用，同一能力选择me不重复收取;change:CostChange=额外任意Power1

```python

ops.modify_cost(subjects, change, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0697"></a>

## 0697

据守此处可付任意Power4得1分

cost:Cost=任意Power4;binding:CostBinding=可选据守触发基础费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.gain_points(p, 1)

```



<a id="card-0698"></a>

## 0698

反应法术

 

```python

ops.draw(p, 3)

```



<a id="card-0699"></a>

## 0699

p本回合已在某次打法术实花Energy≥4期间持续+4，不按累计小法术花费相加

dur:Duration=me留场且本回合存在p单次打法术实际Energy支付≥4

```python

ops.modify_might([me], 4, duration=dur)

```



<a id="card-0700"></a>

## 0700

传奇Energy1横置，给friendly单位本回合“自身强攻等于自身坚守”的被动能力

cost:Cost=Energy1及横置me;binding:CostBinding=主动基础费用;u:Unit=所选friendly单位;ability:Ability=下方受授被动执行体，动态根据该u的Shield赋额外Assault实例;params:KeywordParameters=Assault.value为该u当前Shield总值，持续重算

```python

# 传奇主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.grant_ability([u], ability, duration=THIS_TURN)
# 受授被动执行体，与原有Assault来源叠加，不硬覆盖已有强攻总值
ops.grant_keyword([u], ASSAULT, parameters=params, duration=THIS_TURN)

```



<a id="card-0701"></a>

## 0701

p打出任意单位后，给任意单位+1本回合，不限己方

u:Unit=所选任意单位

```python

ops.modify_might([u], 1, duration=THIS_TURN)

```



<a id="card-0702"></a>

## 0702

迅捷法术，任意单位+7本回合

u:Unit=所选单位

```python

ops.modify_might([u], 7, duration=THIS_TURN)

```



<a id="card-0703"></a>

## 0703

定稿可亮出单位，结算仅亮出则按该单位亮出时战力对任意单位伤害

requirement:ShowOffRequirement=手牌单位或场上friendly单位;link:Link=本次亮出相依关联;showed:bool=该次实际亮出成功;u:Unit=伤害所选单位;m:IntExpr=该亮出关联中保存的单位战力快照，不读事后改变

```python

# 定稿亮出入口
ops.show_off(p, requirement, link=link)
# 法术结算入口
if showed:
    ops.damage([u], m)

```



<a id="card-0704"></a>

## 0704

p发动gear的主动能力后，不包括单位/传奇主动

 

```python

ops.modify_might([me], 1, duration=THIS_TURN)

```



<a id="card-0705"></a>

## 0705

传奇反应横置抽1；本回合至少两次以法术或单位技能选敌方单位/装备为目标才可发动

cost:Cost=横置me;binding:CostBinding=满足上述目标选择历史的反应主动基础费用；不是每回合只可用一次

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.draw(p, 1)

```



<a id="card-0706"></a>

## 0706

法术结算；控制机械则打出费用能量减2

cards:CostSelection=本法术;discount:CostChange=Energy减2且最低0;has_mech:bool=p控制机械;mech:TokenTemplate=3战力Mech;dest:Zone=p基地;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

# 费用入口
if has_mech:
    ops.modify_cost(cards, discount, duration=WHILE_CONDITION)
# 结算入口
ops.play(mech, p, origin=None, destination=dest)
ops.draw(p, 1)

```

LANG:SC机器人译名与英文Mech不同，以tokenCardIds绑定



<a id="card-0707"></a>

## 0707

打出触发；可解除己控物强化作为费用，强化另一传奇/单位/装备

cost:Cost=解除选定己控传奇/永久物一层强化;binding:CostBinding=此可选触发费用;u:Selection[Permanent/Legend]=目标传奇单位装备

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower(u)

```



<a id="card-0708"></a>

## 0708

法术结算

 

```python

ops.draw(p, 4)

```



<a id="card-0709"></a>

## 0709

采用2025-10-21勘误；各玩家看五放逐一回收其余，再从下一玩家起顺序打出

players:list[Player]=看牌阶段规则规定玩家次序;play_order:list[Player]=下一玩家开始的次序;top:dict[Player,list[Card]]=各自主牌堆前5实际存在牌;ignored_energy:CostPolicy=仅忽略Energy仍付Power;dest:dict[Player,Location/Zone]=各自合法打出位置

```python

chosen = {}
for actor in players:
    ops.look(actor, actor.main_deck, 5)
    one = ops.choose(actor, top[actor], targeting=False, bind_at="resolution").value
    chosen[actor] = one
    ops.banish(one)
    ops.recycle([c for c in top[actor] if c not in one])
for actor in play_order:
    for c in chosen[actor]:
        ops.play(c, actor, origin=actor.banish, destination=dest[actor], cost_policy=ignored_energy)

```

PLAYER_BATCH:各玩家看牌与放逐回收的批次边界未约定

ACTOR:banish/recycle无执行玩家参数，不能完整保存各玩家行动归属

LANG:英文未勘误文本没有放逐；SC选择与TC放逐不同



<a id="card-0710"></a>

## 0710

征服此处且p控制符文不多于4；可付能量1抽1

cost:Cost=Energy1;binding:CostBinding=此可选触发费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.draw(p, 1)

```



<a id="card-0711"></a>

## 0711

灵便打出附着与装配能量1主动；贴附时宿主壁垒

cost:Cost=Energy1;binding:CostBinding=装配主动费用;u:Unit=p控制的宿主;host:Selection[Unit]=贴附的宿主;WHILE_ATTACHED:Duration=WHILE(本装备仍贴附于该宿主)，宿主/装备关联按本实例保存

```python

# 灵便打出触发
ops.attach(me, u)
# 装配主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 贴附效果
ops.grant_keyword(host, TANK, duration=WHILE_ATTACHED)

```

DATA:SC缺失装备EFFECT，依据EN保留Tank



<a id="card-0712"></a>

## 0712

法术选择友军后摧毁战力更低敌军；流转另行处理

friendly:list[Unit]=所有友方含队友单位;enemies:list[Unit]=敌方单位

```python

u = ops.choose(p, friendly).value
if u:
    targets = ops.choose(p, [e for e in enemies if e.might < u[0].might]).value
    ops.kill(targets)

```

FLOW_EXIT:流转的离链放逐及从废牌堆替代费用未独立展开



<a id="card-0713"></a>

## 0713

迅捷法术结算

u:Selection[Unit]=一名单位

```python

ops.modify_might(u, 5, duration=THIS_TURN)

```



<a id="card-0714"></a>

## 0714

未强化时弃手牌强化；已强化持续+1

cost:Cost=弃1手牌;binding:CostBinding=仅未强化时可用的强化主动;empowered:bool=me已强化;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

# 强化主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 持续入口
if empowered:
    ops.modify_might([me], 1, duration=WHILE_CONDITION)

```



<a id="card-0715"></a>

## 0715

p控制每件武装额外提供强攻；只在该装备附着时授予对应宿主，每件一实例

hosts:list[Unit]=按p每件已贴附武装枚举宿主可重复;assault:KeywordParameters=Assault默认1;WHILE_ATTACHED:Duration=WHILE(本装备仍贴附于该宿主)，宿主/装备关联按本实例保存

```python

for host in hosts:
    ops.grant_keyword([host], ASSAULT, parameters=assault, duration=WHILE_ATTACHED)

```



<a id="card-0716"></a>

## 0716

可选额外Fury1；打出若已付则重置自身并本回合+2；待命游走保留

self_cost:CostSelection=me打出费用;extra:CostChange=可选附加PowerFury1;receipt:bool=确已支付该附加费;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

# 定稿费用
ops.modify_cost(self_cost, extra, duration=THIS_PLAY)
# 打出触发
if receipt:
    ops.ready([me])
    ops.modify_might([me], 2, duration=THIS_TURN)

```



<a id="card-0717"></a>

## 0717

每回合一次，me在战场时敌方死亡触发打出休眠金币；待命后排保留

gold:TokenTemplate=Gold;dest:Zone=p基地;entry:EntryState=exhausted

```python

ops.play(gold, p, origin=None, destination=dest, entry=entry)

```



<a id="card-0718"></a>

## 0718

征服触发二选一

runes:Selection[Rune]=p符文堆可召出1枚;options:list[ChoiceValue]=draw或channel;mode:list[str]=本入口合法模式选择结果单元素列表；普通法术/主动在定稿绑定，后续可选模式按指定结算时点绑定

```python

# mode由本入口明确的合法模式选择绑定；不是标签宣告
if mode == ["draw"]:
    ops.draw(p, 1)
else:
    ops.channel(p, 1, exhausted=True)

```



<a id="card-0719"></a>

## 0719

未强化时横置强化；解除强化加能量1横置抽1

empower_cost:Cost=横置me;empower_binding:CostBinding=未强化时主动;draw_cost:Cost=解除me强化且Energy1且横置me;draw_binding:CostBinding=抽牌主动费用

```python

# 强化主动
paid = ops.pay(p, empower_cost, binding=empower_binding)
if paid.value is not None:
    ops.empower([me])
# 抽牌主动
paid = ops.pay(p, draw_cost, binding=draw_binding)
if paid.value is not None:
    ops.draw(p, 1)

```



<a id="card-0720"></a>

## 0720

装配任意Power1；贴附时p法术技能额外伤害3；唯我保留

cost:Cost=任意Power1;binding:CostBinding=装配主动;u:Unit=p控制单位;events:DamageSelection=p法术和技能伤害含分配伤害池按规则715;bonus:NumericChange=add3;WHILE_ATTACHED:Duration=WHILE(本装备仍贴附于该宿主)，宿主/装备关联按本实例保存

```python

# 装配主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 贴附效果
ops.modify_damage(events, bonus, duration=WHILE_ATTACHED)

```

DATA:SC无装备EFFECT，EN明确额外伤害3



<a id="card-0721"></a>

## 0721

p一次眩晕一个或多个敌军触发一次增益友军

u:Selection[Unit]=一名友方含队友单位

```python

ops.buff(u)

```



<a id="card-0722"></a>

## 0722

强化费能量6Fury1；p单位持续+1，强化时改+2

cost:Cost=Energy6与Fury1;binding:CostBinding=未强化时强化主动;units:Selection[Unit]=p控制单位动态集合;empowered:bool=me已强化

```python

# 强化主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 持续入口
ops.modify_might(units, 2 if empowered else 1, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0723"></a>

## 0723

打出触发本回合下一个法术能量减5

spells:CostSelection=p本回合下一个打出法术;discount:CostChange=Energy减5最低0

```python

ops.modify_cost(spells, discount, duration=THIS_TURN, uses=1)

```



<a id="card-0724"></a>

## 0724

p本回合已弃牌时持续拥有强攻和游走

discarded:bool=p本回合实际弃过牌;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if discarded:
    ops.grant_keyword([me], ASSAULT, duration=WHILE_CONDITION)
    ops.grant_keyword([me], GANKING, duration=WHILE_CONDITION)

```



<a id="card-0725"></a>

## 0725

各玩家每回合第一次于此打出单位或装备触发该玩家洞察

actor:Player=事件打出者

```python

ops.predict(actor)

```



<a id="card-0726"></a>

## 0726

法术选一处被敌方占领战场并在那里打出3随从

battlefields:list[Battlefield]=敌方占领的战场;recruit:TokenTemplate=1战力Recruit

```python

b = ops.choose(p, battlefields).value
if b:
    for i in range(3):
        ops.play(recruit, p, origin=None, destination=b[0])

```



<a id="card-0727"></a>

## 0727

法术抽1，并要求创建本回合以后友军打出时增益的触发

 

```python

ops.draw(p, 1)

```

DELAY:缺少建立本回合未来友方单位打出触发的API，不能现在buff尚不存在的单位



<a id="card-0728"></a>

## 0728

可选附加Body1；结算友敌各一相互按自身战力造成伤害

self_cost:CostSelection=本法术;extra:CostChange=可选附加Body1;paid_extra:bool=确已支付;u:Selection[Unit]=选定友方单位;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

# 定稿费用
ops.modify_cost(self_cost, extra, duration=THIS_PLAY)
# 结算片段
if paid_extra:
    ops.modify_might(u, 2, duration=THIS_TURN)

```

RECIPROCAL:友敌相互同时以不同来源和数值造成伤害，damage单一source无法完整表达



<a id="card-0729"></a>

## 0729

迅捷法术重置p全部单位并本回合+3

units:Selection[Unit]=p控制的全部单位

```python

ops.ready(units)
ops.modify_might(units, 3, duration=THIS_TURN)

```



<a id="card-0730"></a>

## 0730

p防守此处时展示顶牌，法术入手否则回收

top:list[Card]=p主牌堆顶部至多1张

```python

ops.reveal(top)
if top:
    if top[0].card_type == "spell":
        ops.transfer(top, p.main_deck, p.hand)
    else:
        ops.recycle(top)

```



<a id="card-0731"></a>

## 0731

对手打出装备时可放逐me作为触发费用再放逐该装备

cost:Cost=放逐me;binding:CostBinding=此可选触发费用;gear:Selection[Gear]=触发的装备

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.banish(gear)

```



<a id="card-0732"></a>

## 0732

p打出法术触发me本回合+1

 

```python

ops.modify_might([me], 1, duration=THIS_TURN)

```



<a id="card-0733"></a>

## 0733

采用勘误横置：本回合p下一个法术全部伤害实例+1

cost:Cost=横置me;binding:CostBinding=主动费用;events:DamageSelection=本回合p下一个法术全部伤害；不能uses1耗于首个伤害实例;bonus:NumericChange=add1

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_damage(events, bonus, duration=THIS_TURN)

```

NEXT_ABILITY:下一法术身份必须动态绑定且只消耗一次选择，DamageSelection的绑定/消耗契约未定义

LANG:未勘误EN和SC少本回合限制，TC有



<a id="card-0734"></a>

## 0734

移动触发展示顶牌，强力则抽该牌否则回收

top:list[Card]=p主牌堆顶至多1张;is_mighty:bool=被展示牌是强力单位，按规则卡牌战力判定

```python

ops.reveal(top)
if top:
    if is_mighty:
        ops.draw(p, 1, cards=top)
    else:
        ops.recycle(top)

```



<a id="card-0735"></a>

## 0735

敌军本回合−2友军+2然后相互战力伤害

enemy:Selection[Unit]=一敌军;friendly:Selection[Unit]=一友军

```python

ops.modify_might(enemy, -2, duration=THIS_TURN)
ops.modify_might(friendly, 2, duration=THIS_TURN)

```

RECIPROCAL:同时不同来源相互战力伤害无完整调用

MODIFIER_BATCH:同一指令不同对象的不同战力修饰批次边界未定义



<a id="card-0736"></a>

## 0736

防守此处时可移动此处一友军回其控制者基地

units:list[Unit]=此处所有友方单位含队友;accept:bool=p选择执行

```python

if accept:
    u = ops.choose(p, units).value
    if u:
        ops.move(u, u[0].controller.base, origin=here)

```



<a id="card-0737"></a>

## 0737

迅捷法术将一战场单位回其拥有者手牌

u:Unit=选定战场单位;origin:Zone=u当前所在区域

```python

ops.transfer([u], origin, u.owner.hand)

```



<a id="card-0738"></a>

## 0738

反应选能量不高于4法术；可付任意Power1夺取控制和可重选否则无效

spell:ChainItem=定稿时选定能量费用至多4法术;cost:Cost=任意Power1;binding:CostBinding=结算中的可选支付非必选前置费;redo:bool=选择重做法术选择

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.change_control([spell], p)
    if redo:
        ops.redo_choices(spell, p)
else:
    ops.counter(spell)

```



<a id="card-0739"></a>

## 0739

me变休眠触发二选一；急速保留

options:list[ChoiceValue]=gold或draw;gold:TokenTemplate=Gold;dest:Zone=p基地;entry:EntryState=exhausted;cost:Cost=Chaos1;binding:CostBinding=抽牌模式触发费用;mode:list[str]=本入口合法模式选择结果单元素列表；普通法术/主动在定稿绑定，后续可选模式按指定结算时点绑定

```python

# mode由本入口明确的合法模式选择绑定；不是标签宣告
if mode == ["gold"]:
    ops.play(gold, p, origin=None, destination=dest, entry=entry)
else:
    paid = ops.pay(p, cost, binding=binding)
    if paid.value is not None:
        ops.draw(p, 1)

```



<a id="card-0740"></a>

## 0740

据守此处触发执行此处各单位的征服效果，不伪造征服事件

effects:list[tuple[Unit,AbilityRef]]=此处单位所有征服效果逐个明确引用

```python

for unit, ability in effects:
    ops.execute_effect(unit, ability)

```



<a id="card-0741"></a>

## 0741

随从指示物纯属性，无独立文本效果

 

```python

# 无独立文本动作

```



<a id="card-0742"></a>

## 0742

迅捷法术打出4随从，各自可选基地或p控制战场

recruit:TokenTemplate=1战力Recruit;destinations:list[Location/Zone]=4次打出的合法目的地，逐次规则选择

```python

for dest in destinations:
    ops.play(recruit, p, origin=None, destination=dest)

```



<a id="card-0743"></a>

## 0743

装配Fury1；宿主进攻或防守触发对同地敌军2

cost:Cost=Fury1;binding:CostBinding=装配费用;u:Unit=p控制单位;enemy:Selection[Unit]=宿主地点一敌方单位

```python

# 装配主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 宿主进攻/防守触发
ops.damage(enemy, 2)

```

DATA:SC缺少装备EFFECT



<a id="card-0744"></a>

## 0744

持续p在此处征服效果额外触发一次；me征服给予友军增益；急速保留

triggers:TriggerSelection=p征服me当前所在地所触发的己方征服效果含自身;extra:IntExpr=1;u:Selection[Unit]=一友方单位

```python

# 持续入口
ops.modify_trigger_count(triggers, extra, duration=WHILE_SOURCE_PRESENT)
# me征服触发
ops.buff(u)

```



<a id="card-0745"></a>

## 0745

映像提醒由产生它的卡牌指定复制对象，不独立创建复制效果

 

```python

# 复制来源与特征由实际打出映像的效果绑定，不从提醒文字猜测

```

DELEGATED:仅有复制提醒，须和具体产生映像的卡一起展开，不能凭任意original调用copy



<a id="card-0746"></a>

## 0746

采用勘误，查看5可放逐一单位打出减能量5，回收余牌

discount:CostChange=本次打出Energy减5最低0;dest:Location/Zone=所选单位本次合法位置;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

top = ops.look(p, p.main_deck, 5).value
u = ops.choose(p, [c for c in top if c.card_type == "unit"], minimum=0, targeting=False, bind_at="resolution").value
if u:
    ops.banish(u)
    ops.modify_cost(u, discount, duration=THIS_PLAY)
    ops.play(u[0], p, origin=p.banish, destination=dest)
ops.recycle([c for c in top if c not in u])

```

LANG:EN和SC原印刷没有放逐步骤，TC及勘误有；采用勘误



<a id="card-0747"></a>

## 0747

友方从非任何玩家手牌区域打出单位拥有急速；固有急速强攻保留

units:Selection[Card]=正在从非手牌打出的友方单位动态集合

```python

ops.grant_keyword(units, ACCELERATE, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0748"></a>

## 0748

攻击时可展示2，可放逐其中1再打出；单位可打出此处；回收余牌；采用勘误

top:list[Card]=p主牌堆顶部至多2;accept:bool=选择展示;dest:Location/Zone=所选牌合法位置，单位额外允许here;permission:PlayPermission=仅本次允许所选单位打出here

```python

if accept:
    ops.reveal(top)
    one = ops.choose(p, top, minimum=0, targeting=False, bind_at="resolution").value
    if one:
        ops.banish(one)
        ops.play(one[0], p, origin=p.banish, destination=dest, permission=permission)
    ops.recycle([c for c in top if c not in one])

```

LANG:未勘误EN/SC缺少放逐且余牌回收顺序不同；采用勘误



<a id="card-0749"></a>

## 0749

移动友军，可贴附同控制者至多1武装并赋本回合征服可移动回基地能力

u:Unit=友方单位;dest:Location=本次合法移动目的地;equipment:list[Gear]=控制者与u相同的武装;ability:Ability=本段征服触发能力引用，下方给出调用体;self_unit:Unit=该授予能力的宿主;accept:bool=宿主控制者可选择移动

```python

# 法术主体
ops.move([u], dest)
g = ops.choose(p, equipment, minimum=0).value
if g:
    ops.attach(g[0], u)
ops.grant_ability([u], ability, duration=THIS_TURN)
# 授予能力：宿主征服时
if accept:
    ops.move([self_unit], self_unit.controller.base)

```



<a id="card-0750"></a>

## 0750

p打出强力单位触发，可横置传奇me作为费用召出休眠符文

cost:Cost=横置传奇me;binding:CostBinding=此可选触发费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.channel(p, 1, exhausted=True)

```



<a id="card-0751"></a>

## 0751

进攻可免费打出能量至多2武装；采用勘误的然后做此事附着

equipment:list[Card]=p手牌中可打出且Energy至多2武装;dest:Location/Zone=合法打出位置

```python

g = ops.choose(p, equipment, minimum=0, targeting=False, bind_at="resolution").value
if g:
    ops.play(g[0], p, origin=p.hand, destination=dest, cost_policy=IGNORE_BASE_COST)

```

REFLEXIVE:打出成功后须新建待处理附着能力项，不能当场把ChainItem当Gear附着

LANG:原印刷直接附着，勘误增加自反链项



<a id="card-0752"></a>

## 0752

p打出另一单位触发me本回合+2

 

```python

ops.modify_might([me], 2, duration=THIS_TURN)

```



<a id="card-0753"></a>

## 0753

从p废牌堆免费打出至多3单位或装备；每张能量≤3符能≤1

eligible:list[Card]=废牌堆符合Unit/Gear且Energy≤3且Power≤1牌;destinations:list[Location/Zone]=各次合法打出位置

```python

cards = ops.choose(p, eligible, minimum=0, maximum=3, targeting=False, bind_at="resolution").value
for card, dest in zip(cards, destinations):
    ops.play(card, p, origin=p.trash, destination=dest, cost_policy=IGNORE_BASE_COST)

```



<a id="card-0754"></a>

## 0754

p指示物均以活跃状态进入

 

```python

# 缺少全局未来入场状态修饰接口

```

ENTRY:play.entry只覆盖单次打出，不能建立所有未来token入场活跃规则，ready会制造额外事件



<a id="card-0755"></a>

## 0755

仅me在战场可发动两个独立主动

draw_cost:Cost=Energy1Mind1;draw_binding:CostBinding=仅在战场可发动抽牌;score_cost:Cost=Energy4Mind4且横置me;score_binding:CostBinding=仅在战场可发动得分

```python

# 抽牌主动
paid = ops.pay(p, draw_cost, binding=draw_binding)
if paid.value is not None:
    ops.draw(p, 1)
# 得分主动
paid = ops.pay(p, score_cost, binding=score_binding)
if paid.value is not None:
    ops.gain_points(p, 1)

```



<a id="card-0756"></a>

## 0756

能量1主动本回合+1；战力变成≥10触发强化；强化状态持续法盾游走

cost:Cost=Energy1;binding:CostBinding=主动费用;empowered:bool=me已强化;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

# 战力主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_might([me], 1, duration=THIS_TURN)
# 战力由不足10变为≥10触发
ops.empower([me])
# 已强化持续入口
if empowered:
    ops.grant_keyword([me], DEFLECT, duration=WHILE_CONDITION)
    ops.grant_keyword([me], GANKING, duration=WHILE_CONDITION)

```



<a id="card-0757"></a>

## 0757

进攻且p控制符文≤4，对同地所有敌军2；急速保留

enemies:Selection[Unit]=me所在地所有敌方单位

```python

ops.damage(enemies, 2)

```



<a id="card-0758"></a>

## 0758

可打出到p进攻中的战场；反应强攻2保留

subjects:PermissionSelection=me;permission:PermissionSpec=打出目的地增加p正在进攻的战场

```python

ops.grant_permission(subjects, permission, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0759"></a>

## 0759

按勘误伏击可到有敌军而无p单位战场

subjects:PermissionSelection=me;permission:PermissionSpec=Ambush反应打出目的地包括有敌方单位战场且无需p在场

```python

ops.grant_permission(subjects, permission, duration=WHILE_SOURCE_PRESENT)

```

LANG:早期文本只扩展打出地点，勘误明确扩展Ambush



<a id="card-0760"></a>

## 0760

固有关键词内部展开；不同注释为独立入口

dest:Location/Zone=本次合法打出位置;choices:ChoiceBinding=定稿选择是否支付急速附加费Energy1Fury1;subjects:CostSelection=本次打出me;extra:CostChange=该次所选急速附加费Energy1Fury1，不改印刷基础费;entry:EntryState=choices选择急速则ready否则默认，必须与完整费用支付一致;attacking:bool=me为进攻方;target_costs:CostSelection=对手法术技能选择me时的目标附加费;deflect_cost:CostChange=额外任意Power1;ganking:PermissionSpec=me可从战场普通移动到其他战场;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

# 急速内部费用与入场展开
ops.modify_cost(subjects, extra, duration=THIS_PLAY)
ops.play(me, p, origin=p.hand, destination=dest, choices=choices, entry=entry)
# 强攻持续
if attacking:
    ops.modify_might([me], 2, duration=WHILE_CONDITION)
# 法盾与游走持续
ops.modify_cost(target_costs, deflect_cost, duration=WHILE_SOURCE_PRESENT)
ops.grant_permission([me], ganking, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0761"></a>

## 0761

强攻数值等于p控制装备数

n:IntExpr=p控制装备数动态值;params:KeywordParameters=Assault数值为n

```python

ops.grant_keyword([me], ASSAULT, parameters=params, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0762"></a>

## 0762

反应选一战场友军，无效只选该友军且不选任何其他友军的敌方法术或能力

u:Unit=战场一友方单位;eligible:list[ChainItem]=敌方链项且选择u且无其他友方单位目标

```python

item = ops.choose(p, eligible).value
if item:
    ops.counter(item[0])

```



<a id="card-0763"></a>

## 0763

采用勘误反应；选p控制战场及不同位置p单位，移过去本回合+2

u:Selection[Unit]=p控制且不在b单位;b:Battlefield=p控制的目标战场

```python

ops.move(u, b)
ops.modify_might(u, 2, duration=THIS_TURN)

```

LANG:未勘误EN/SC的反应提醒误写迅捷时机，按2026-07-23勘误



<a id="card-0764"></a>

## 0764

部署保留；p回合结束且控制该战场打出休眠金币

gold:TokenTemplate=Gold;dest:Zone=p基地;entry:EntryState=exhausted

```python

ops.play(gold, p, origin=None, destination=dest, entry=entry)

```



<a id="card-0765"></a>

## 0765

横置抽1并召出休眠符文；变休眠另触发友军+3

cost:Cost=横置me;binding:CostBinding=主动费用;u:Selection[Unit]=一友方单位

```python

# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.draw(p, 1)
    ops.channel(p, 1, exhausted=True)
# 变为休眠触发
ops.modify_might(u, 3, duration=THIS_TURN)

```



<a id="card-0766"></a>

## 0766

反应友军回拥有者手牌，然后拥有者召出休眠符文

u:Unit=一友方单位;origin:Zone=u原区域;owner:Player=u拥有者LKI

```python

ops.transfer([u], origin, owner.hand)
ops.channel(owner, 1, exhausted=True)

```



<a id="card-0767"></a>

## 0767

p打出法术且该次实际花费Energy≥4触发重置自身

 

```python

ops.ready([me])

```



<a id="card-0768"></a>

## 0768

自身费用每p废牌堆一牌能量减1

subject:CostSelection=me打出费用;discount:CostChange=Energy减p废牌堆牌数最低0

```python

ops.modify_cost(subject, discount, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0769"></a>

## 0769

me移动到战场触发另一友军本回合+1

u:Selection[Unit]=非me的一名友方单位

```python

ops.modify_might(u, 1, duration=THIS_TURN)

```



<a id="card-0770"></a>

## 0770

迅捷移动一友军并重置

u:Selection[Unit]=一友方单位;dest:Location=合法目的地

```python

ops.move(u, dest)
ops.ready(u)

```



<a id="card-0771"></a>

## 0771

移动到战场看3可展示单位抽该牌回收余牌；死亡从手牌打出单位至基地仅忽略能量

units:list[Card]=死亡效果p手牌单位;ignore_energy:CostPolicy=仅忽略Energy保留Power

```python

# 移动到战场触发
top = ops.look(p, p.main_deck, 3).value
u = ops.choose(p, [c for c in top if c.card_type == "unit"], minimum=0, targeting=False, bind_at="resolution").value
if u:
    ops.reveal(u)
    ops.draw(p, 1, cards=u)
ops.recycle([c for c in top if c not in u])
# Deathknell死亡触发
card = ops.choose(p, units, targeting=False, bind_at="resolution").value
if card:
    ops.play(card[0], p, origin=p.hand, destination=p.base, cost_policy=ignore_energy)

```



<a id="card-0772"></a>

## 0772

先抽1，再按p及盟友控制战场数抽牌

n:IntExpr=p或盟友控制战场总数不重复计

```python

ops.draw(p, 1)
ops.draw(p, n)

```



<a id="card-0773"></a>

## 0773

反应选友军和法术；无效法术后以该法术能量值给友军本回合战力

u:Selection[Unit]=一友方单位;spell:ChainItem=一法术;n:int=被选法术Energy费用LKI

```python

ops.counter(spell)
ops.modify_might(u, n, duration=THIS_TURN)

```

DATA:SC的战力图标为损坏的[s]，按EN读取



<a id="card-0774"></a>

## 0774

此处单位回玩家手牌触发该玩家可付能量1召出休眠符文

actor:Player=接收手牌玩家;cost:Cost=Energy1;binding:CostBinding=该玩家此可选触发费用

```python

paid = ops.pay(actor, cost, binding=binding)
if paid.value is not None:
    ops.channel(actor, 1, exhausted=True)

```



<a id="card-0775"></a>

## 0775

打出触发一敌军本回合−3；急速保留

u:Selection[Unit]=一敌方单位

```python

ops.modify_might(u, -3, duration=THIS_TURN)

```



<a id="card-0776"></a>

## 0776

打出触发战场上一敌军6伤害

u:Selection[Unit]=战场一敌方单位

```python

ops.damage(u, 6)

```



<a id="card-0777"></a>

## 0777

p此处单位强化费减能量1或任意符能1

subjects:CostSelection=p控制且在here单位的Empower费用;change:CostChange=付款者在Energy减1或Power减1中选择一种最低0

```python

ops.modify_cost(subjects, change, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0778"></a>

## 0778

变休眠触发选择本回合未选过模式；增益自身或消耗增益眩晕敌军/重置自己

options:list[ChoiceValue]=本回合未选择的buff/stun/ready模式；历史外部保存;cost:Cost=消耗me增益;binding:CostBinding=选定stun或ready模式的触发费用;u:Selection[Unit]=stun模式一敌方单位;mode:list[str]=本入口合法模式选择结果单元素列表；普通法术/主动在定稿绑定，后续可选模式按指定结算时点绑定

```python

# mode由本入口明确的合法模式选择绑定；不是标签宣告
if mode == ["buff"]:
    ops.buff([me])
else:
    paid = ops.pay(p, cost, binding=binding)
    if paid.value is not None:
        if mode == ["stun"]:
            ops.stun(u)
        else:
            ops.ready([me])

```



<a id="card-0779"></a>

## 0779

另一友军变休眠触发me+1；主动横置友军重置单位每回合一次

cost:Cost=横置一友方单位;binding:CostBinding=每回合只可一次的主动费用;u:Selection[Unit]=一名单位

```python

# 触发入口
ops.modify_might([me], 1, duration=THIS_TURN)
# 主动入口
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.ready(u)

```



<a id="card-0780"></a>

## 0780

百炼打出可付装配减任意符能1；进攻对同地一敌军造成2×自身贴附武装数单次伤害

gear:Gear=p控制的一件武装可已贴附;equip_cost:Cost=该武装装配费用减Power1最低0;binding:CostBinding=百炼可选触发的装配支付;accept:bool=选择百炼;u:Selection[Unit]=me所在地一敌方单位;n:IntExpr=me贴附武装数量

```python

# 百炼打出触发
if accept:
    paid = ops.pay(p, equip_cost, binding=binding)
    if paid.value is not None:
        ops.attach(gear, me)
# 进攻触发：规则418.8为单次伤害
ops.damage(u, 2 * n)

```



<a id="card-0781"></a>

## 0781

一次效果选择基地单位4伤或摧毁装备；回响要求另外定稿的重复选择

options:list[ChoiceValue]=damage或kill;u:Selection[Unit]=一基地单位;g:Selection[Gear]=一装备;mode:list[str]=本入口合法模式选择结果单元素列表；普通法术/主动在定稿绑定，后续可选模式按指定结算时点绑定

```python

# mode由本入口明确的合法模式选择绑定；不是标签宣告
if mode == ["damage"]:
    ops.damage(u, 4)
else:
    ops.kill(g)

```

REPEAT:只展开单次效果，额外付款重复和多组预先定稿选择未独立展开



<a id="card-0782"></a>

## 0782

所有单位不能打出到此处

subjects:PermissionSelection=所有单位牌;restriction:RestrictionSpec=禁止play的目的地为here

```python

ops.restrict_action(subjects, restriction, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0783"></a>

## 0783

强化能量3任意符能1；迅捷横置传奇，仅自己回合移动对决友军至基地，强化时重置该单位

empower_cost:Cost=Energy3PowerAny1;empower_binding:CostBinding=未强化时可用;move_cost:Cost=横置me传奇;move_binding:CostBinding=Action主动;own_turn:bool=现在p回合;u:Unit=处于showdown的一友军;empowered:bool=me已强化

```python

# 强化主动
paid = ops.pay(p, empower_cost, binding=empower_binding)
if paid.value is not None:
    ops.empower([me])
# 迅捷主动
paid = ops.pay(p, move_cost, binding=move_binding)
if paid.value is not None and own_turn:
    ops.move([u], u.controller.base)
    if empowered:
        ops.ready([u])

```



<a id="card-0784"></a>

## 0784

定稿可亮出Energy≥7牌；结算打出2或4随从到基地

requirement:ShowOffRequirement=Energy费用≥7的卡;link:Link=本次法术亮出凭证;showed:bool=该亮出凭证成功;recruit:TokenTemplate=1战力Recruit

```python

# 定稿亮出
ops.show_off(p, requirement, link=link)
# 结算
for i in range(4 if showed else 2):
    ops.play(recruit, p, origin=None, destination=p.base)

```



<a id="card-0785"></a>

## 0785

打出触发选择传奇重置或横置

 

```python

# ready/exhaust只接受Permanent，传奇不是Permanent，不能伪造合法调用

```

LEGEND_READY:两个API均排除Legend，无法覆盖本牌的两种朝向选择



<a id="card-0786"></a>

## 0786

打出触发于me所在地打出黄沙士兵

soldier:TokenTemplate=2战力SandSoldier

```python

ops.play(soldier, p, origin=None, destination=here)

```



<a id="card-0787"></a>

## 0787

持续禁止敌方法术技能选择me

subjects:PermissionSelection=me;restriction:RestrictionSpec=敌方法术或技能不能选择me为目标

```python

ops.restrict_action(subjects, restriction, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0788"></a>

## 0788

征服此处可弃1并召出休眠符文

cost:Cost=弃1手牌;binding:CostBinding=可选征服触发费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.channel(p, 1, exhausted=True)

```



<a id="card-0789"></a>

## 0789

死亡触发一敌军4伤害

u:Selection[Unit]=一敌方单位

```python

ops.damage(u, 4)

```



<a id="card-0790"></a>

## 0790

p机械强攻；征服可回收另一友军作为费，废牌堆机械打出能量减该单位战力

mechs:Selection[Unit]=p控制机械;cost:Cost=回收非me的一友军;binding:CostBinding=可选征服触发费用，保存被回收单位战力LKI;discount:CostChange=Energy减上述LKI战力最低0;card:Card=p废牌堆一机械单位;dest:Location/Zone=该单位合法目的地;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

# 持续入口
ops.grant_keyword(mechs, ASSAULT, duration=WHILE_SOURCE_PRESENT)
# 征服触发
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_cost([card], discount, duration=THIS_PLAY)
    ops.play(card, p, origin=p.trash, destination=dest)

```



<a id="card-0791"></a>

## 0791

p机械包括me持续+1；据守打出3战力机械至基地

mechs:Selection[Unit]=p控制机械;token:TokenTemplate=3战力Mech

```python

# 持续入口
ops.modify_might(mechs, 1, duration=WHILE_SOURCE_PRESENT)
# 据守触发
ops.play(token, p, origin=None, destination=p.base)

```



<a id="card-0792"></a>

## 0792

迅捷法术眩晕一单位

u:Selection[Unit]=一名单位

```python

ops.stun(u)

```



<a id="card-0793"></a>

## 0793

打出或离场触发放逐顶牌，直到p下个Ending可打出；主动能量2Fury1横置摧毁自己

top:list[Card]=p主牌堆顶部至多1;permission:PermissionSpec=可从放逐区打出该牌且正常付费;until:Duration=直到p下个EndingPhase;cost:Cost=Energy2Fury1横置me;binding:CostBinding=主动费用

```python

# 打出/离场触发
cards = ops.banish(top).value
ops.grant_permission(cards, permission, duration=until)
# 主动入口
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.kill([me])

```



<a id="card-0794"></a>

## 0794

可选额外弃1；迅捷结算战场单位3或5伤

subjects:CostSelection=本次法术;extra:CostChange=可选额外弃1手牌;paid_extra:bool=确实支付额外费用;u:Selection[Unit]=战场一单位;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

# 费用入口
ops.modify_cost(subjects, extra, duration=THIS_PLAY)
# 结算
ops.damage(u, 5 if paid_extra else 3)

```



<a id="card-0795"></a>

## 0795

选对手展示其手牌，再选非单位回收

opponent:Player=所选对手

```python

ops.reveal(opponent.hand)
card = ops.choose(p, [c for c in opponent.hand if c.card_type != "unit"], targeting=False, bind_at="resolution").value
ops.recycle(card)

```

ACTOR:reveal缺少执行玩家，对手展示无法记归属；SC又指定对手回收，而EN/TC未如此写

LANG:SC回收执行人为对手，其他文本非明确相同



<a id="card-0796"></a>

## 0796

除me在战场且恰有一个其他p控制单位同地，否则不造成战斗伤害

subjects:PermissionSelection=me;restriction:RestrictionSpec=不符合上述条件时禁止造成combat_damage

```python

ops.restrict_action(subjects, restriction, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0797"></a>

## 0797

装配Order1；宿主死亡触发抽1

cost:Cost=Order1;binding:CostBinding=装配费用;u:Unit=p控制单位

```python

# 装配主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 宿主Deathknell
ops.draw(p, 1)

```

DATA:SC缺少装备EFFECT



<a id="card-0798"></a>

## 0798

反应额外必须摧毁友方强力单位，抽2召出休眠符文

subjects:CostSelection=本次法术;extra:CostChange=必选额外摧毁一友方Mighty单位，战力≥5;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

# 定稿费用入口
ops.modify_cost(subjects, extra, duration=THIS_PLAY)
# 成功打出后的结算
ops.draw(p, 2)
ops.channel(p, 1, exhausted=True)

```



<a id="card-0799"></a>

## 0799

可选额外XP3；打出各玩家摧毁己方一单位，已付则p豁免

subjects:CostSelection=me本次打出;extra:CostChange=可选额外XP3;actors:list[Player]=所有玩家，支付XP3时移除p;units:dict[Player,list[Unit]]=各自控制单位;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

# 定稿费用
ops.modify_cost(subjects, extra, duration=THIS_PLAY)
# 打出触发片段
for actor in actors:
    chosen = ops.choose(actor, units[actor], targeting=False, bind_at="resolution").value
    ops.kill(chosen)

```

ACTOR:kill无执行玩家，无法记录每人摧毁自己单位

PLAYER_BATCH:各人选择与同时摧毁的批次未规定



<a id="card-0800"></a>

## 0800

可打出开放战场；预知打出触发

subjects:PermissionSelection=me;permission:PermissionSpec=打出目的地增加开放战场

```python

# 持续权限
ops.grant_permission(subjects, permission, duration=WHILE_SOURCE_PRESENT)
# Vision打出触发
ops.predict(p)

```



<a id="card-0801"></a>

## 0801

迅捷可摧毁至多一装备，然后必抽1

gear:list[Gear]=所有合法装备

```python

g = ops.choose(p, gear, minimum=0, maximum=1).value
ops.kill(g)
ops.draw(p, 1)

```



<a id="card-0802"></a>

## 0802

反应二选一强化单位或解除已强化单位，回合末执行反向动作

options:list[ChoiceValue]=empower或disempower;u:Selection[Unit]=模式相应合法单位，后者必须已强化;mode:list[str]=本入口合法模式选择结果单元素列表；普通法术/主动在定稿绑定，后续可选模式按指定结算时点绑定

```python

# mode由本入口明确的合法模式选择绑定；不是标签宣告
if mode == ["empower"]:
    ops.empower(u)
else:
    ops.disempower(u)

```

DELAY:回合结束的反向强化/解除是未来动作，empower无duration不能代替，缺建立延迟触发接口



<a id="card-0803"></a>

## 0803

p打出Energy费用≥7牌触发重置me

 

```python

ops.ready([me])

```



<a id="card-0804"></a>

## 0804

黄沙士兵纯属性指示物

 

```python

# 无独立文本动作

```



<a id="card-0805"></a>

## 0805

打出触发摧毁战力≤3敌军

u:Selection[Unit]=一敌方单位，战力≤3

```python

ops.kill(u)

```



<a id="card-0806"></a>

## 0806

me在战场时各玩家ChannelPhase开始只召出1枚

scope:RuleScope=所有玩家ChannelPhase的基础召出数量;change:RuleChange=固定为1;at_battlefield:bool=me当前在战场;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if at_battlefield:
    ops.modify_rule(CHANNEL_PHASE_COUNT, scope, change, duration=WHILE_CONDITION)

```



<a id="card-0807"></a>

## 0807

法术选择此处至少一名对该法术友方单位，其任意符能费用减1

subjects:CostSelection=选择此处一名或以上己方/盟友单位的法术；按法术控制者判友方;discount:CostChange=任意Power减1最低0

```python

ops.modify_cost(subjects, discount, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0808"></a>

## 0808

迅捷移动友军后打出炸弹至任一战场

u:Selection[Unit]=一友方单位;dest:Location=合法移动目标;b:Battlefield=打出炸弹目标战场;bomb:TokenTemplate=Bomb含Deploy与死亡2伤及杀同地其他己方Bomb

```python

ops.move(u, dest)
ops.play(bomb, p, origin=None, destination=b)

```



<a id="card-0809"></a>

## 0809

征服/据守狩猎2；p经验≥3持续+1并以活跃进场

level:bool=p经验≥3;entry:EntryState=活跃进场;dest:Location/Zone=合法打出地点;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

# Hunt触发
ops.gain_xp(p, 2)
# Level持续效果
if level:
    ops.modify_might([me], 1, duration=WHILE_CONDITION)
# 本牌打出入口，Level只影响自身
if level:
    ops.play(me, p, origin=p.hand, destination=dest, entry=entry)

```



<a id="card-0810"></a>

## 0810

迅捷同一战场分配总5伤害

units:Selection[Unit]=一战场选定若干单位;allocation:dict[Unit,int]=合法分配总5到目标，按715给总伤害池加Bonus

```python

ops.damage(units, 5, mode="split", allocation=allocation)

```



<a id="card-0811"></a>

## 0811

反应横置传奇加能量1，仅可在对决消耗

cost:Cost=横置me;binding:CostBinding=Reaction资源主动;resources:ResourceBundle=Energy1;restriction:Predicate=只可在showdown期间消耗

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.add_resources(p, resources, restriction=restriction)

```



<a id="card-0812"></a>

## 0812

此牌被打出/弃置/摧毁时触发抽1

 

```python

ops.draw(p, 1)

```



<a id="card-0813"></a>

## 0813

打出时本回合已打出过其他牌，弃2然后抽2

 

```python

ops.discard(p, 2)
ops.draw(p, 2)

```



<a id="card-0814"></a>

## 0814

能量1横置，选对手猜类型，展示顶牌，猜中回收否则抽该牌

cost:Cost=Energy1横置me;binding:CostBinding=主动费用;opponent:Player=选定对手;types:list[ChoiceValue]=unit/gear/spell;top:list[Card]=p主牌堆顶至多1

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    guess = ops.declare(opponent, types).value
    ops.reveal(top)
    if top:
        if top[0].card_type in guess:
            ops.recycle(top)
        else:
            ops.draw(p, 1, cards=top)

```



<a id="card-0815"></a>

## 0815

打出触发每一友军获得1XP

n:IntExpr=场上所有友方单位数量，含me与队友单位

```python

ops.gain_xp(p, n)

```



<a id="card-0816"></a>

## 0816

自身休眠进场；摧毁且能量1横置，洞察2抽1获得XP1

cost:Cost=摧毁me且Energy1且横置me;binding:CostBinding=主动复合费用，按同一支付流程;entry:EntryState=休眠进场;dest:Location/Zone=合法装备地点

```python

# 打出入口
ops.play(me, p, origin=p.hand, destination=dest, entry=entry)
# 主动入口
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.predict(p, 2)
    ops.draw(p, 1)
    ops.gain_xp(p, 1)

```



<a id="card-0817"></a>

## 0817

打出抽1；死亡选对手展示手牌并本回合可看其盖牌，获得XP1

opponent:Player=所选对手;subjects:PermissionSelection=p;permission:PermissionSpec=本回合可查看opponent的正面朝下牌

```python

# 打出触发
ops.draw(p, 1)
# 死亡触发
ops.reveal(opponent.hand)
ops.grant_permission(subjects, permission, duration=THIS_TURN)
ops.gain_xp(p, 1)

```

ACTOR:对手执行展示动作，但reveal只有viewers没有actor



<a id="card-0818"></a>

## 0818

可选额外能量1，打出已付则增益自身

subjects:CostSelection=me本次打出;extra:CostChange=可选额外Energy1;paid_extra:bool=确实支付;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

# 定稿费用
ops.modify_cost(subjects, extra, duration=THIS_PLAY)
# 打出触发
if paid_extra:
    ops.buff([me])

```



<a id="card-0819"></a>

## 0819

反应横置加Chaos1

cost:Cost=横置me;binding:CostBinding=Reaction资源主动;resources:ResourceBundle=PowerChaos1

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.add_resources(p, resources)

```



<a id="card-0820"></a>

## 0820

反应横置加Calm1

cost:Cost=横置me;binding:CostBinding=Reaction资源主动;resources:ResourceBundle=PowerCalm1

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.add_resources(p, resources)

```



<a id="card-0821"></a>

## 0821

反应横置加Mind1

cost:Cost=横置me;binding:CostBinding=Reaction资源主动;resources:ResourceBundle=PowerMind1

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.add_resources(p, resources)

```



<a id="card-0822"></a>

## 0822

反应横置加Fury1

cost:Cost=横置me;binding:CostBinding=Reaction资源主动;resources:ResourceBundle=PowerFury1

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.add_resources(p, resources)

```



<a id="card-0823"></a>

## 0823

反应横置加Body1

cost:Cost=横置me;binding:CostBinding=Reaction资源主动;resources:ResourceBundle=PowerBody1

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.add_resources(p, resources)

```



<a id="card-0824"></a>

## 0824

反应横置加Order1

cost:Cost=横置me;binding:CostBinding=Reaction资源主动;resources:ResourceBundle=PowerOrder1

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.add_resources(p, resources)

```



<a id="card-0825"></a>

## 0825

征服此处触发按p与盟友其他受控战场数抽牌

n:IntExpr=p或盟友控制的除here外战场总数

```python

ops.draw(p, n)

```



<a id="card-0826"></a>

## 0826

百炼打出可装配己方武装，装配费减任意符能1含已贴附装备

g:Gear=p控制的一件武装;cost:Cost=g装配费用减Power1最低0;binding:CostBinding=可选百炼触发费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(g, me)

```



<a id="card-0827"></a>

## 0827

将p每次召出替代为原数量原朝向加一枚休眠符文

 

```python

# 不能在召出后另channel伪装同一个替代事件

```

REPLACE:缺少改写所有待发生channel事件并追加不同朝向一枚的接口



<a id="card-0828"></a>

## 0828

进攻缴械2；每回合一次p同时横置至少3友军时可抽1

u:Selection[Unit]=同地一敌方单位;accept:bool=选择抽牌

```python

# Disarm进攻触发
ops.modify_might(u, -2, duration=THIS_TURN)
# 同时横置≥3友军触发
if accept:
    ops.draw(p, 1)

```



<a id="card-0829"></a>

## 0829

打出或变休眠打出随从基地；按其他p休眠单位数量持续加战力

recruit:TokenTemplate=1战力Recruit;n:IntExpr=p控制其他休眠单位数

```python

# 打出/变休眠触发
ops.play(recruit, p, origin=None, destination=p.base)
# 持续入口
ops.modify_might([me], n, duration=WHILE_SOURCE_PRESENT)

```

DATA:SC T1A-005名称与规则为空，其他印刷有完整文本



<a id="card-0830"></a>

## 0830

强化能量3；已强化法盾坚守3

cost:Cost=Energy3;binding:CostBinding=未强化时强化主动;empowered:bool=me已强化;shield:KeywordParameters=Shield3;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

# 强化主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 持续入口
if empowered:
    ops.grant_keyword([me], DEFLECT, duration=WHILE_CONDITION)
    ops.grant_keyword([me], SHIELD, parameters=shield, duration=WHILE_CONDITION)

```



<a id="card-0831"></a>

## 0831

装配Fury1，贴附时宿主强攻2

cost:Cost=Fury1;binding:CostBinding=装配主动;u:Unit=p控制单位;host:Selection[Unit]=贴附宿主;params:KeywordParameters=Assault2;WHILE_ATTACHED:Duration=WHILE(本装备仍贴附于该宿主)，宿主/装备关联按本实例保存

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 贴附效果
ops.grant_keyword(host, ASSAULT, parameters=params, duration=WHILE_ATTACHED)

```

DATA:SC缺少装备EFFECT



<a id="card-0832"></a>

## 0832

打出与征服增益自身；消耗自身增益主动本回合+4

cost:Cost=消耗me增益;binding:CostBinding=主动费用

```python

# 打出/征服触发
ops.buff([me])
# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_might([me], 4, duration=THIS_TURN)

```



<a id="card-0833"></a>

## 0833

me在战场，每一同地增益友军给me+1，包含有增益me；壁垒保留

n:IntExpr=me战场处有增益友方单位数，不在战场为0

```python

ops.modify_might([me], n, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0834"></a>

## 0834

打出至战场活跃进场；迅捷能量1任意符能1横置，眩晕此处进攻敌军

dest:Location/Zone=本次打出目的地;entry:EntryState=目的地为战场则ready，否则默认;cost:Cost=Energy1PowerAny1横置me;binding:CostBinding=Action主动;u:Selection[Unit]=进攻me所在地敌方单位

```python

# 打出入口
ops.play(me, p, origin=p.hand, destination=dest, entry=entry)
# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.stun(u)

```



<a id="card-0835"></a>

## 0835

p废牌堆有同名牌则自身活跃进场

dest:Location/Zone=合法打出目的地;entry:EntryState=有同名废牌则ready，否则默认

```python

ops.play(me, p, origin=p.hand, destination=dest, entry=entry)

```



<a id="card-0836"></a>

## 0836

进攻可放逐p废牌堆单位作为费，本回合强攻4

cost:Cost=放逐p废牌堆一单位;binding:CostBinding=可选进攻触发费用;params:KeywordParameters=Assault4

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.grant_keyword([me], ASSAULT, parameters=params, duration=THIS_TURN)

```

DATA:ShadowClone本体might为null；其他产生它的卡明确指定0，不能把本体缺值默认视作0



<a id="card-0837"></a>

## 0837

移动一敌军到p有单位战场；若p该处恰两单位则各+1本回合

u:Selection[Unit]=一敌方单位;b:Battlefield=p有单位战场;friendly:Selection[Unit]=移动后p在b恰两单位，否则空

```python

ops.move(u, b)
ops.modify_might(friendly, 1, duration=THIS_TURN)

```

FLOW_EXIT:流转从废牌堆及离链放逐未独立展开



<a id="card-0838"></a>

## 0838

强化能量2Fury1；已强化强攻3

cost:Cost=Energy2Fury1;binding:CostBinding=未强化时强化主动;empowered:bool=me已强化;params:KeywordParameters=Assault3;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 持续
if empowered:
    ops.grant_keyword([me], ASSAULT, parameters=params, duration=WHILE_CONDITION)

```



<a id="card-0839"></a>

## 0839

移动时可燃烧1作为费本回合自身+1

cost:Cost=Burn1从p主牌堆;binding:CostBinding=可选移动触发费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_might([me], 1, duration=THIS_TURN)

```



<a id="card-0840"></a>

## 0840

p据守此处燃烧3

 

```python

ops.burn(p, 3)

```



<a id="card-0841"></a>

## 0841

本回合pBeginningPhase有友军死亡，则me活跃进场

dest:Location/Zone=合法目的地;entry:EntryState=有上述死亡事件则ready否则默认

```python

ops.play(me, p, origin=p.hand, destination=dest, entry=entry)

```



<a id="card-0842"></a>

## 0842

每张p废牌堆同名牌减能量2

subjects:CostSelection=me打出费用;discount:CostChange=Energy减2乘p废牌堆同名卡数最低0

```python

ops.modify_cost(subjects, discount, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0843"></a>

## 0843

任意废牌堆至多2单位回各拥有者手牌

eligible:list[Card]=所有废牌堆单位;origins:dict[Card,Zone]=各牌来源废牌堆

```python

cards = ops.choose(p, eligible, minimum=0, maximum=2).value
for card in cards:
    ops.transfer([card], origins[card], card.owner.hand)

```

BATCH:transfer只支持单来源/目的区域，跨玩家同时回手事件批次不能由逐个transfer保证



<a id="card-0844"></a>

## 0844

给无瞬息友军瞬息然后抽2

u:Selection[Unit]=未有Temporary的一友方单位

```python

ops.grant_keyword(u, TEMPORARY, duration=PERMANENT)
ops.draw(p, 2)

```



<a id="card-0845"></a>

## 0845

装配能量1Order1；贴附时另选友军，宿主在贴附期间复制它

cost:Cost=Energy1Order1;binding:CostBinding=装配费用;host:Unit=p控制单位;original:Unit=另一友方单位;WHILE_ATTACHED:Duration=WHILE(本装备仍贴附于该宿主)，宿主/装备关联按本实例保存

```python

# 装配主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, host)
# 可表达复制动作片段
ops.copy(host, original, duration=WHILE_ATTACHED)

```

AS_ATTACH:选择与复制发生于as attached内联过程，而非之后触发，attach未提供该过程挂钩

DATA:SC缺少提醒EFFECT但非独立效果



<a id="card-0846"></a>

## 0846

敌军控制者决定让p抽2或受6伤

u:Unit=一敌方单位;options:list[ChoiceValue]=draw或damage;mode:list[str]=本入口合法模式选择结果单元素列表；普通法术/主动在定稿绑定，后续可选模式按指定结算时点绑定

```python

# mode由本入口明确的合法模式选择绑定；不是标签宣告
if mode == ["draw"]:
    ops.draw(p, 2)
else:
    ops.damage([u], 6)

```



<a id="card-0847"></a>

## 0847

每回合p开始阶段首次友军死亡，各对手须各摧毁己方1单位

opponents:list[Player]=p各对手;units:dict[Player,list[Unit]]=各对手控制单位

```python

for actor in opponents:
    chosen = ops.choose(actor, units[actor], targeting=False, bind_at="resolution").value
    ops.kill(chosen)

```

ACTOR:kill没有各对手执行者参数

PLAYER_BATCH:各对手选择和摧毁的批次未约定



<a id="card-0848"></a>

## 0848

固有关键词内部展开；不同注释为独立入口

dest:Location/Zone=本次合法打出位置;choices:ChoiceBinding=定稿选择是否支付急速附加费Energy1Fury1;subjects:CostSelection=本次打出me;extra:CostChange=该次所选急速附加费Energy1Fury1，不改印刷基础费;entry:EntryState=choices选择急速则ready否则默认，必须与完整费用支付一致;attacking:bool=me为进攻方;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

# 急速内部费用与入场展开
ops.modify_cost(subjects, extra, duration=THIS_PLAY)
ops.play(me, p, origin=p.hand, destination=dest, choices=choices, entry=entry)
# 强攻持续
if attacking:
    ops.modify_might([me], 4, duration=WHILE_CONDITION)

```



<a id="card-0849"></a>

## 0849

固有坚守2及壁垒内部展开；反应打出权限

defending:bool=me为防守方;scope:RuleScope=me同控制者参战单位承伤顺序;change:RuleChange=先承担致死伤害;permission:PermissionSpec=具有Reaction时机且仍检查优先权和合法地点，可到p控制战场;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if defending:
    ops.modify_might([me], 2, duration=WHILE_CONDITION)
ops.modify_rule(COMBAT_DAMAGE_ORDER, scope, change, duration=WHILE_SOURCE_PRESENT)
ops.grant_permission([me], permission, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0850"></a>

## 0850

据守且me同地恰有一个其他p单位触发得分1

 

```python

ops.gain_points(p, 1)

```



<a id="card-0851"></a>

## 0851

据守且me同地恰有一个其他p单位触发抽1

 

```python

ops.draw(p, 1)

```



<a id="card-0852"></a>

## 0852

打出XP1；装配花费XP1

cost:Cost=XP1;binding:CostBinding=Equip主动;u:Unit=p控制单位

```python

# 打出触发
ops.gain_xp(p, 1)
# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)

```



<a id="card-0853"></a>

## 0853

可选额外摧毁友方单位/装备；打出已付则对单位2

subjects:CostSelection=me本次打出;extra:CostChange=可选额外摧毁一友方单位或装备;paid_extra:bool=实际已付;u:Selection[Unit]=一单位;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

# 定稿费用
ops.modify_cost(subjects, extra, duration=THIS_PLAY)
# 打出触发
if paid_extra:
    ops.damage(u, 2)

```



<a id="card-0854"></a>

## 0854

纯基础属性单位，无规则文本

 

```python

# 无独立文本动作

```



<a id="card-0855"></a>

## 0855

控制已强化物体则能量减2；迅捷法术战场单位4伤

has_empowered:bool=p控制已强化传奇/单位/装备;subjects:CostSelection=本次法术;discount:CostChange=Energy减2最低0;u:Selection[Unit]=战场一单位;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

# 费用
if has_empowered:
    ops.modify_cost(subjects, discount, duration=WHILE_CONDITION)
# 结算
ops.damage(u, 4)

```



<a id="card-0856"></a>

## 0856

反应每一p强力单位抽1

n:IntExpr=p控制Mighty单位数，战力≥5

```python

ops.draw(p, n)

```



<a id="card-0857"></a>

## 0857

增益p基地一友军然后移至战场

u:Selection[Unit]=p基地一友方单位;b:Battlefield=合法目标战场

```python

ops.buff(u)
ops.move(u, b, origin=p.base)

```



<a id="card-0858"></a>

## 0858

装配任意符能1；打出重置p单位；贴附后同地p单位游走；唯我保留

cost:Cost=PowerAny1;binding:CostBinding=装配费用;u:Unit=p控制单位;units:Selection[Unit]=p控制全部单位;local_units:Selection[Unit]=装备宿主所在地p控制单位;WHILE_ATTACHED:Duration=WHILE(本装备仍贴附于该宿主)，宿主/装备关联按本实例保存

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 打出触发
ops.ready(units)
# 贴附效果
ops.grant_keyword(local_units, GANKING, duration=WHILE_ATTACHED)

```

DATA:SC缺少装备EFFECT



<a id="card-0859"></a>

## 0859

战场至多一敌军2伤，然后移动友军；流转保留待展开

enemies:list[Unit]=战场敌方单位;u:Selection[Unit]=一友方单位;dest:Location=合法移动目的地

```python

targets = ops.choose(p, enemies, minimum=0, maximum=1).value
ops.damage(targets, 2)
ops.move(u, dest)

```

FLOW_EXIT:流转完整流程未独立展开



<a id="card-0860"></a>

## 0860

征服此处必须回收一枚p符文；此操作不选择目标

runes:list[Rune]=p控制符文

```python

r = ops.choose(p, runes, targeting=False, bind_at="resolution").value
ops.recycle(r)

```



<a id="card-0861"></a>

## 0861

p实际给me增益触发重置me

 

```python

ops.ready([me])

```



<a id="card-0862"></a>

## 0862

至多2单位各6伤害同批次

units:list[Unit]=所有合法单位

```python

u = ops.choose(p, units, minimum=0, maximum=2).value
ops.damage(u, 6, mode="each", simultaneous=True)

```



<a id="card-0863"></a>

## 0863

进攻可付能量1将此处敌军移回其控制者基地

cost:Cost=Energy1;binding:CostBinding=可选进攻触发费用;u:Unit=同地一敌方单位

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.move([u], u.controller.base, origin=here)

```



<a id="card-0864"></a>

## 0864

选一战场友军+1敌军−1最低1本回合

friendly:Selection[Unit]=目标战场友方单位;enemies:Selection[Unit]=目标战场敌方单位

```python

ops.modify_might(friendly, 1, duration=THIS_TURN)
ops.modify_might(enemies, -1, duration=THIS_TURN, floor=1)

```

MODIFIER_BATCH:同指令两种不同修饰能否作为同批次未由API约定



<a id="card-0865"></a>

## 0865

战场一单位4伤，p符文≥7则7；其本回合死亡召出休眠符文

u:Selection[Unit]=战场一单位;n:int=p当前控制符文数

```python

ops.damage(u, 7 if n >= 7 else 4)

```

DELAY:没有建立被选单位本回合未来死亡触发召出符文接口



<a id="card-0866"></a>

## 0866

进攻缴械1，游走保留

u:Selection[Unit]=此处一敌方单位

```python

ops.modify_might(u, -1, duration=THIS_TURN)

```



<a id="card-0867"></a>

## 0867

反应移动本回合移动过的敌军

u:Selection[Unit]=一敌方且本回合有move记录单位;dest:Location=合法移动目的地

```python

ops.move(u, dest)

```



<a id="card-0868"></a>

## 0868

进攻后征服且给敌军分配过量≥5时可向一敌军造成相同伤害

u:Selection[Unit]=一敌方单位;n:IntExpr=本次进攻对敌军分配的总过量伤害;accept:bool=选择执行

```python

if accept:
    ops.damage(u, n)

```



<a id="card-0869"></a>

## 0869

p本回合已消耗至少2Power时持续+2与游走；急速保留

condition:bool=p本回合累计实际消耗Power≥2不限定领域; ;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if condition:
    ops.modify_might([me], 2, duration=WHILE_CONDITION)
    ops.grant_keyword([me], GANKING, duration=WHILE_CONDITION)

```



<a id="card-0870"></a>

## 0870

主动弃一装备加能量1横置，对战场单位4

cost:Cost=弃手牌一装备且Energy1且横置me;binding:CostBinding=主动费用;u:Selection[Unit]=战场一单位

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.damage(u, 4)

```



<a id="card-0871"></a>

## 0871

法术费用减p单位最高战力；迅捷战场单位5伤

subjects:CostSelection=本次法术;discount:CostChange=Energy减己方单位最高战力最低0，无单位不减;u:Selection[Unit]=战场一单位;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

# 费用
ops.modify_cost(subjects, discount, duration=THIS_PLAY)
# 结算
ops.damage(u, 5)

```



<a id="card-0872"></a>

## 0872

装配能量1Fury1，宿主据守效果也是征服效果反之亦然

cost:Cost=Energy1Fury1;binding:CostBinding=装配费用;u:Unit=p控制宿主

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)

```

TRIGGER_RETYPE:没有改已有能力触发事件或扩增触发类别的API，modify_trigger_count只改次数

DATA:SC缺少装备EFFECT



<a id="card-0873"></a>

## 0873

可选额外让友方装备回拥有者手，选付则本次能量减2；法盾保留

subjects:CostSelection=me本次打出;change:CostChange=可选费用分支：一友方装备回拥有者手牌并Energy减2最低0;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

ops.modify_cost(subjects, change, duration=THIS_PLAY)

```



<a id="card-0874"></a>

## 0874

移动敌军；p经验≥6另眩晕一敌军，可与前目标不同

u:Selection[Unit]=移动的一敌军;dest:Location=合法目的地;level:bool=pXP≥6;stun_target:Selection[Unit]=单独选定一敌军

```python

ops.move(u, dest)
if level:
    ops.stun(stun_target)

```



<a id="card-0875"></a>

## 0875

迅捷战场单位3伤，本回合将死改放逐

u:Selection[Unit]=战场一单位

```python

ops.damage(u, 3)

```

REPLACE:没有登记本回合该单位死亡改放逐的事件替代API，不能先kill再banish



<a id="card-0876"></a>

## 0876

选p两不同地点单位；至少一瞬息则交换位置；必抽1

a:Unit=p控制单位;b:Unit=p另一不同地点单位;eligible:bool=a或b有Temporary

```python

# 交换位置尚无合法同批次多目的move
ops.draw(p, 1)

```

MOVE_BATCH:move一次仅一个目的地，先后两次move不保证同时交换及战斗检查边界



<a id="card-0877"></a>

## 0877

反应一单位本回合−4最低1

u:Selection[Unit]=一单位

```python

ops.modify_might(u, -4, duration=THIS_TURN, floor=1)

```



<a id="card-0878"></a>

## 0878

可打出至开放战场

subjects:PermissionSelection=me;permission:PermissionSpec=play目的地增加开放战场

```python

ops.grant_permission(subjects, permission, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0879"></a>

## 0879

征服获得任意符能1资源

resources:ResourceBundle=PowerAny1

```python

ops.add_resources(p, resources)

```



<a id="card-0880"></a>

## 0880

死亡召出休眠符文1

 

```python

ops.channel(p, 1, exhausted=True)

```



<a id="card-0881"></a>

## 0881

打出选敌军，已眩晕杀否则眩晕

u:Unit=一敌方单位

```python

if u.stunned:
    ops.kill([u])
else:
    ops.stun([u])

```



<a id="card-0882"></a>

## 0882

打出眩晕一单位

u:Selection[Unit]=一单位

```python

ops.stun(u)

```



<a id="card-0883"></a>

## 0883

p摧毁眩晕敌军时可横置此装备为费抽1

cost:Cost=横置me;binding:CostBinding=可选触发费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.draw(p, 1)

```



<a id="card-0884"></a>

## 0884

强化能量2；已强化+1且法盾2

cost:Cost=Energy2;binding:CostBinding=未强化时强化主动;empowered:bool=me已强化;params:KeywordParameters=Deflect2;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 持续
if empowered:
    ops.modify_might([me], 1, duration=WHILE_CONDITION)
    ops.grant_keyword([me], DEFLECT, parameters=params, duration=WHILE_CONDITION)

```



<a id="card-0885"></a>

## 0885

按勘误p回合末me在战场，重置至多4友方符文

 

```python

# ready的Selection[Permanent]不含Rune

```

RUNE_READY:缺少对Rune合法重置接口

LANG:旧EN/SC要求4，勘误及TC为至多4



<a id="card-0886"></a>

## 0886

最后承战斗伤害；同地另一p单位战力低于me将死则改治愈横置召回

scope:RuleScope=me的战斗伤害分配次序;change:RuleChange=最后承担

```python

ops.modify_rule(COMBAT_DAMAGE_ORDER, scope, change, duration=WHILE_SOURCE_PRESENT)

```

REPLACE:治疗/横置/召回动作本身存在，但缺少在死亡前取消并替代死亡事件的API



<a id="card-0887"></a>

## 0887

摧毁战场战力≤3一单位

u:Selection[Unit]=战场战力≤3一单位

```python

ops.kill(u)

```



<a id="card-0888"></a>

## 0888

p指示物单位持续+1

units:Selection[Unit]=p控制token单位动态集合

```python

ops.modify_might(units, 1, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0889"></a>

## 0889

装配Calm1；宿主p经验≥3再+1

cost:Cost=Calm1;binding:CostBinding=装配费用;u:Unit=p控制单位;host:Selection[Unit]=当前宿主;level:bool=宿主效果控制者XP≥3;WHILE_ATTACHED:Duration=WHILE(本装备仍贴附于该宿主)，宿主/装备关联按本实例保存

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 贴附持续
if level:
    ops.modify_might(host, 1, duration=WHILE_ATTACHED)

```

DATA:SC缺少装备EFFECT



<a id="card-0890"></a>

## 0890

打出可从废牌堆打出单位，仅忽略能量

eligible:list[Card]=p废牌堆单位;dest:Location/Zone=合法目的地;ignore_energy:CostPolicy=只忽略Energy保留Power

```python

cards = ops.choose(p, eligible, minimum=0, targeting=False, bind_at="resolution").value
if cards:
    ops.play(cards[0], p, origin=p.trash, destination=dest, cost_policy=ignore_energy)

```



<a id="card-0891"></a>

## 0891

伏击允许以反应打出到p有单位战场

permission:PermissionSpec=以Reaction时机将me打出到p有单位战场；不忽略其他费用与限制

```python

ops.grant_permission([me], permission, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0892"></a>

## 0892

p强化其他物触发强化me；解除me强化横置传奇，使战场单位−2

cost:Cost=解除me强化且横置me传奇;binding:CostBinding=主动费用;u:Selection[Unit]=战场一单位

```python

# 强化其他物触发
ops.empower([me])
# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_might(u, -2, duration=THIS_TURN)

```



<a id="card-0893"></a>

## 0893

另一友军死亡触发自身本回合+2

 

```python

ops.modify_might([me], 2, duration=THIS_TURN)

```



<a id="card-0894"></a>

## 0894

打出可免费打出p废牌堆能量≤3符能≤1单位

eligible:list[Card]=p废牌堆符合两项费用限制单位;dest:Location/Zone=合法目的地

```python

cards = ops.choose(p, eligible, minimum=0, targeting=False, bind_at="resolution").value
if cards:
    ops.play(cards[0], p, origin=p.trash, destination=dest, cost_policy=IGNORE_BASE_COST)

```



<a id="card-0895"></a>

## 0895

同地每个p其他同名单位给me+1；组牌同名数量无限；待命保留

n:IntExpr=同地p控制其他同名单位数;scope:RuleScope=p套牌中名为Spiderling卡;change:RuleChange=同名张数无上限;DECK_CONSTRUCTION:Duration=PERMANENT，适用范围仅构筑检查

```python

# 持续战力
ops.modify_might([me], n, duration=WHILE_SOURCE_PRESENT)
# 构筑规则
ops.modify_rule(DECK_NAME_LIMIT, scope, change, duration=DECK_CONSTRUCTION)

```



<a id="card-0896"></a>

## 0896

灵便打出贴附；任意符能1装配；瞬息仅未贴附时开始阶段摧毁

cost:Cost=PowerAny1;binding:CostBinding=装配费用;u:Unit=p控制单位

```python

# 灵便打出触发
ops.attach(me, u)
# 装配主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 固有Temporary开始阶段且未贴附时
ops.kill([me])

```



<a id="card-0897"></a>

## 0897

可选额外友方装备回拥有者手牌；打出若付则自身重置且+该装备能量值本回合

subjects:CostSelection=me本次打出;extra:CostChange=可选额外友方装备回拥有者手;paid_extra:bool=实际支付;n:int=所返回装备Energy费用LKI;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

# 费用
ops.modify_cost(subjects, extra, duration=THIS_PLAY)
# 打出触发
if paid_extra:
    ops.ready([me])
    ops.modify_might([me], n, duration=THIS_TURN)

```



<a id="card-0898"></a>

## 0898

p以友军为目标触发，可付能量1横置抽1

cost:Cost=Energy1且横置me;binding:CostBinding=可选触发费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.draw(p, 1)

```



<a id="card-0899"></a>

## 0899

打出增益一友军；持续有增益且原无任何法盾的友军获得法盾

u:Selection[Unit]=一友方单位;eligible:Selection[Unit]=有buff且排除本授予效果后无Deflect的所有友军

```python

# 打出触发
ops.buff(u)
# 持续入口
ops.grant_keyword(eligible, DEFLECT, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0900"></a>

## 0900

本回合敌军曾死亡则本法术能量减2；反应抽2

subjects:CostSelection=本次法术;discount:CostChange=Energy减2最低0;enemy_died:bool=本回合有敌方单位死亡;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

# 费用
if enemy_died:
    ops.modify_cost(subjects, discount, duration=THIS_PLAY)
# 结算
ops.draw(p, 2)

```



<a id="card-0901"></a>

## 0901

精灵固有瞬息，在控制者开始阶段得分前摧毁

 

```python

ops.kill([me])

```



<a id="card-0902"></a>

## 0902

打出两活跃3战力瞬息精灵

sprite:TokenTemplate=3战力Sprite含Temporary;destinations:list[Location/Zone]=两次合法打出位置;entry:EntryState=ready

```python

for dest in destinations:
    ops.play(sprite, p, origin=None, destination=dest, entry=entry)

```



<a id="card-0903"></a>

## 0903

待命迅捷打出一活跃3战力瞬息精灵

sprite:TokenTemplate=3战力Sprite含Temporary;dest:Location/Zone=合法打出位置;entry:EntryState=ready

```python

ops.play(sprite, p, origin=None, destination=dest, entry=entry)

```



<a id="card-0904"></a>

## 0904

固有瞬息；打出活跃精灵基地；死亡重复该装备打出效果

sprite:TokenTemplate=3战力Sprite含Temporary;entry:EntryState=ready;play_effect:AbilityRef=本牌上述打出触发的明确引用

```python

# Temporary开始阶段
ops.kill([me])
# 打出触发
ops.play(sprite, p, origin=None, destination=p.base, entry=entry)
# 死亡触发，明确引用效果
ops.execute_effect(me, play_effect)

```



<a id="card-0905"></a>

## 0905

打出触发同地打出活跃3战力瞬息精灵

sprite:TokenTemplate=3战力Sprite含Temporary;entry:EntryState=ready

```python

ops.play(sprite, p, origin=None, destination=here, entry=entry)

```



<a id="card-0906"></a>

## 0906

打出或p开始阶段触发打出活跃3战力瞬息精灵至基地

sprite:TokenTemplate=3战力Sprite含Temporary;entry:EntryState=ready

```python

ops.play(sprite, p, origin=None, destination=p.base, entry=entry)

```



<a id="card-0907"></a>

## 0907

一次效果给予一单位本回合强攻4；回响额外弃1

u:Selection[Unit]=一单位;params:KeywordParameters=Assault4

```python

ops.grant_keyword(u, ASSAULT, parameters=params, duration=THIS_TURN)

```

REPEAT:单次效果已写；回响额外弃牌及独立预选目标未展开



<a id="card-0908"></a>

## 0908

迅捷看顶3，一张入手其余回收

 

```python

top = ops.look(p, p.main_deck, 3).value
one = ops.choose(p, top, targeting=False, bind_at="resolution").value
ops.transfer(one, p.main_deck, p.hand)
ops.recycle([c for c in top if c not in one])

```



<a id="card-0909"></a>

## 0909

必须额外摧毁p控制Bird/Cat/Dog/Poro，伏击可至其原战场；采用勘误

subjects:CostSelection=me打出费用;extra:CostChange=必选摧毁p控制Bird/Cat/Dog/Poro;permission:PermissionSpec=可Ambush到被支付摧毁单位的原战场即使不再有p单位，使用费用绑定LKI;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

ops.modify_cost(subjects, extra, duration=THIS_PLAY)
ops.grant_permission([me], permission, duration=THIS_PLAY)

```

COST_DESTINATION:费用选择单位与打出位置定稿的前后关联缺少明确CostBinding/Permission链接契约

LANG:旧印刷只扩展play位置，勘误明确Ambush



<a id="card-0910"></a>

## 0910

打出可摧毁Energy≤4装备；坚守2保留

eligible:list[Gear]=Energy费用≤4所有装备

```python

g = ops.choose(p, eligible, minimum=0).value
ops.kill(g)

```



<a id="card-0911"></a>

## 0911

防守时固有坚守+1

defender:bool=me为防守方;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if defender:
    ops.modify_might([me], 1, duration=WHILE_CONDITION)

```



<a id="card-0912"></a>

## 0912

增益一友军，本回合所有友军每个buff额外+1；待命迅捷保留

u:Selection[Unit]=一友方单位;friendly:Selection[Unit]=全体友方单位含队友和稍后进场者的动态集合

```python

ops.buff(u)
ops.modify_buff_value(friendly, 1, duration=THIS_TURN)

```



<a id="card-0913"></a>

## 0913

每玩家每回合首次在此打出非token单位，可将该玩家此处另一单位移基地

actor:Player=打出该非token的玩家;u:Selection[Unit]=actor此处另一单位;accept:bool=actor选择执行

```python

if accept:
    ops.move(u, actor.base, origin=here)

```

ACTOR:move没有执行玩家参数，本动作由actor执行而非固定p



<a id="card-0914"></a>

## 0914

反应友军敌军各一回各拥有者手牌

cards:list[Unit]=一友方一敌方单位;origins:dict[Unit,Zone]=两牌原区域

```python

for card in cards:
    ops.transfer([card], origins[card], card.owner.hand)

```

BATCH:单一transfer无法同批次跨不同来源和不同拥有者手牌



<a id="card-0915"></a>

## 0915

选友军及战场，将该处较低战力所有敌军移各自基地，得XP1

u:Unit=选定友方单位;b:Battlefield=选定战场;enemies:list[Unit]=b处当前战力低于u的敌军

```python

# 可表达动作片段
for enemy in enemies:
    ops.move([enemy], enemy.controller.base, origin=b)
ops.gain_xp(p, 1)

```

MOVE_BATCH:各敌方控制者基地可能不同，逐个move不保证同一移动批次



<a id="card-0916"></a>

## 0916

p从废牌堆打出Flow法术能量减2最低1

subjects:CostSelection=p从p废牌堆打出的Flow法术;change:CostChange=Energy减2，减费底线1，不把原本0提升为1

```python

ops.modify_cost(subjects, change, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0917"></a>

## 0917

打出将p废牌堆Bird/Cat/Dog/Poro回手

eligible:list[Card]=p废牌堆有上述任一标签卡

```python

card = ops.choose(p, eligible).value
ops.transfer(card, p.trash, p.hand)

```



<a id="card-0918"></a>

## 0918

可选额外同时横置传奇和3友军使法术能量减2

subjects:CostSelection=p打出法术;change:CostChange=可选附加横置me传奇与3友军，并该次Energy减2最低0；同一费用批次

```python

ops.modify_cost(subjects, change, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0919"></a>

## 0919

据守此处可召出1休眠符文

accept:bool=选择执行

```python

if accept:
    ops.channel(p, 1, exhausted=True)

```



<a id="card-0920"></a>

## 0920

固有强攻2坚守2

attacker:bool=me进攻方;defender:bool=me防守方;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if attacker or defender:
    ops.modify_might([me], 2, duration=WHILE_CONDITION)

```



<a id="card-0921"></a>

## 0921

me在战场且同地其他友方单位/装备合计≥2则+2；壁垒保留

condition:bool=满足战场和同地其他友方永久物至少2;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if condition:
    ops.modify_might([me], 2, duration=WHILE_CONDITION)

```



<a id="card-0922"></a>

## 0922

友军从me位置移动时，可将me随之移动

dest:Location=触发友军的目标地点;accept:bool=选择跟随

```python

if accept:
    ops.move([me], dest, origin=here)

```

MOVE_FOLLOW:卡面with it涉及跟随同一移动批次；独立move不能保证批次和同时控制检查等价，需规则/契约补足



<a id="card-0923"></a>

## 0923

强化能量7；已强化+7；固有法盾保留

cost:Cost=Energy7;binding:CostBinding=未强化时主动;empowered:bool=me已强化;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 持续
if empowered:
    ops.modify_might([me], 7, duration=WHILE_CONDITION)

```



<a id="card-0924"></a>

## 0924

me移动触发抽1

 

```python

ops.draw(p, 1)

```



<a id="card-0925"></a>

## 0925

灵便打出贴附；Calm1装配

cost:Cost=Calm1;binding:CostBinding=Equip主动;u:Unit=p控制单位

```python

# 灵便打出
ops.attach(me, u)
# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)

```



<a id="card-0926"></a>

## 0926

打出到战场时，可移另一同地p单位至p基地

u:Selection[Unit]=此处非me的p控制单位;accept:bool=选择执行

```python

if accept:
    ops.move(u, p.base, origin=here)

```



<a id="card-0927"></a>

## 0927

同地眩晕敌军死亡时抽1

 

```python

ops.draw(p, 1)

```



<a id="card-0928"></a>

## 0928

选p基地友军，伤害源为本法术，对某战场全敌军其战力值伤害，再移该友军过去

u:Unit=p基地一友方单位;b:Battlefield=目标战场;enemies:Selection[Unit]=b处全敌军;n:IntExpr=u当前战力

```python

ops.damage(enemies, n)
ops.move([u], b, origin=p.base)

```



<a id="card-0929"></a>

## 0929

打出召出1休眠符文；壁垒保留

 

```python

ops.channel(p, 1, exhausted=True)

```



<a id="card-0930"></a>

## 0930

变休眠触发洞察

 

```python

ops.predict(p)

```



<a id="card-0931"></a>

## 0931

装备友军以自身为source对敌军战力伤害，再卸一件武装

u:Unit=一配装友方单位;enemy:Selection[Unit]=一敌方单位;equipment:list[Gear]=结算伤害后仍贴附u的武装

```python

ops.damage(enemy, u.might, source=u)
g = ops.choose(p, equipment, targeting=False, bind_at="resolution").value
ops.detach(g)

```

LANG:SC未明确友军为伤害来源，采用EN的It deals



<a id="card-0932"></a>

## 0932

反应单位−1最低1本回合，然后抽1

u:Selection[Unit]=一单位

```python

ops.modify_might(u, -1, duration=THIS_TURN, floor=1)
ops.draw(p, 1)

```



<a id="card-0933"></a>

## 0933

打出选对手，p与其各抽1

opponent:Player=所选对手

```python

ops.draw(p, 1)
ops.draw(opponent, 1)

```

PLAYER_BATCH:两个玩家同一指令抽牌的批次及顺序契约未定义



<a id="card-0934"></a>

## 0934

待命迅捷法术战场单位2伤，进攻方改4

u:Unit=战场一单位

```python

ops.damage([u], 4 if u.attacker else 2)

```



<a id="card-0935"></a>

## 0935

固有反应瞬息；对手得分触发抽1

 

```python

# Temporary开始阶段
ops.kill([me])
# 对手得分触发
ops.draw(p, 1)

```



<a id="card-0936"></a>

## 0936

横置主动，若本回合已打过其他牌，则下一个p单位活跃进场

cost:Cost=横置me;binding:CostBinding=主动费用

```python

ops.pay(p, cost, binding=binding)

```

ENTRY:无法建立本回合下一个单位的入场状态修饰，不能现在重置尚未确定单位



<a id="card-0937"></a>

## 0937

携至少一强力单位征服此处，可付能量1抽1

cost:Cost=Energy1;binding:CostBinding=可选征服触发费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.draw(p, 1)

```

LANG:EN强调征服者有Mighty单位，SC写此处留存至少一Mighty，需按事件主体而非任意敌军检查



<a id="card-0938"></a>

## 0938

固有坚守与壁垒

defender:bool=me防守方;scope:RuleScope=me战斗承伤排序;change:RuleChange=先承担;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

# 坚守持续
if defender:
    ops.modify_might([me], 1, duration=WHILE_CONDITION)
# 壁垒规则
ops.modify_rule(COMBAT_DAMAGE_ORDER, scope, change, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0939"></a>

## 0939

法术单位5伤；me在p废牌堆，p征服可弃1为费回手

u:Selection[Unit]=一单位;cost:Cost=弃p手牌1;binding:CostBinding=废牌堆中可选征服触发费用

```python

# 法术结算
ops.damage(u, 5)
# 废牌堆征服触发
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.transfer([me], p.trash, p.hand)

```



<a id="card-0940"></a>

## 0940

单位10伤再抽2

u:Selection[Unit]=一单位

```python

ops.damage(u, 10)
ops.draw(p, 2)

```



<a id="card-0941"></a>

## 0941

装配能量1Calm1，as attached将宿主规则文字复制至装备效果文字

cost:Cost=Energy1Calm1;binding:CostBinding=装配费用;host:Unit=p控制宿主;WHILE_ATTACHED:Duration=WHILE(本装备仍贴附于该宿主)，宿主/装备关联按本实例保存

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, host)
# 复制动作片段
ops.copy_text(me, host, from_field="rules_text", to_field="effect_text", duration=WHILE_ATTACHED)

```

AS_ATTACH:复制应在贴附内联发生，attach没有过程挂钩；SC持续表述与EN时点不完全相同



<a id="card-0942"></a>

## 0942

预知打出洞察；征服且本回合打过非token单位、非token装备、法术三类得1分

 

```python

# Vision打出
ops.predict(p)
# 满足三类打出历史的征服触发
ops.gain_points(p, 1)

```



<a id="card-0943"></a>

## 0943

可用能量1替代任意符能1盖待命；能量1横置传奇将己有Teemo从英雄区或场上回手

subjects:CostSelection=p隐藏Hidden卡费用;change:CostChange=可选替代隐藏费用Energy1替PowerAny1;cost:Cost=Energy1横置me;binding:CostBinding=主动费用;u:Card=p拥有且位于英雄区或场上的Teemo单位;origin:Zone=u当前区域

```python

# 隐藏费用持续
ops.modify_cost(subjects, change, duration=WHILE_SOURCE_PRESENT)
# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.transfer([u], origin, p.hand)

```



<a id="card-0944"></a>

## 0944

待命迅捷，同一战场两单位本回合交换战力

a:Unit=同一战场第一单位;b:Unit=同战场另一单位

```python

ops.swap_might(a, b, duration=THIS_TURN)

```



<a id="card-0945"></a>

## 0945

p进攻的战斗伤害后平局，替代通常平局流程召回全部参战单位

 

```python

# 不能先执行通常平局退回再recall

```

REPLACE:缺少替代战斗平局后流程为双方全部召回的接口；COMBAT_DAMAGE_ORDER不适用



<a id="card-0946"></a>

## 0946

me处于showdown时p法术拥有回响能量2Chaos1

spells:Selection[Card]=p法术含尚未定稿者;params:KeywordParameters=Repeat费用Energy2Chaos1;in_showdown:bool=me在showdown;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if in_showdown:
    ops.grant_keyword(spells, REPEAT, parameters=params, duration=WHILE_CONDITION)

```



<a id="card-0947"></a>

## 0947

反应给友军本回合下次将死改治愈横置召回

 

```python

# 现有动作不足以登记和消耗一次死亡替代

```

REPLACE:没有本回合仅一次死亡替代事件接口



<a id="card-0948"></a>

## 0948

强化能量2Chaos1；变强化可选废牌堆能量≤3符能≤1单位免费打出基地

cost:Cost=Energy2Chaos1;binding:CostBinding=未强化时Empower主动;eligible:list[Card]=p废牌堆符合双费用限制单位

```python

# 强化主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.empower([me])
# 变为强化触发
cards = ops.choose(p, eligible, minimum=0).value
if cards:
    ops.play(cards[0], p, origin=p.trash, destination=p.base, cost_policy=IGNORE_BASE_COST)

```



<a id="card-0949"></a>

## 0949

pXP≥11时me+4

level:bool=pXP≥11;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if level:
    ops.modify_might([me], 4, duration=WHILE_CONDITION)

```



<a id="card-0950"></a>

## 0950

征服此处，本回合末重置至多2符文；按勘误

 

```python

# 不在征服结算时提前ready

```

DELAY:缺少创建回合末重置触发

RUNE_READY:ready不接受Rune

LANG:旧SC还提前选择符文，勘误为回合末至多2，不能混用



<a id="card-0951"></a>

## 0951

其他同地友军坚守；固有坚守壁垒保留

units:Selection[Unit]=非me且同地的友方单位动态集合

```python

ops.grant_keyword(units, SHIELD, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0952"></a>

## 0952

死亡召出2休眠符文抽1，急速保留

 

```python

ops.channel(p, 2, exhausted=True)
ops.draw(p, 1)

```



<a id="card-0953"></a>

## 0953

打出触发自身本回合+3，待命保留

 

```python

ops.modify_might([me], 3, duration=THIS_TURN)

```



<a id="card-0954"></a>

## 0954

按勘误仅防守触发，先选此处敌军展示顶5，造成待命牌数单次伤害再回收

u:Selection[Unit]=同地一敌方单位;top:list[Card]=p主牌堆顶至多5;n:int=本次展示具有Hidden牌数

```python

ops.reveal(top)
ops.damage(u, n)
ops.recycle(top)

```

LANG:未勘误EN/SC还包含从Hidden打出触发，TC不同印刷亦冲突；按目录勘误仅防守



<a id="card-0955"></a>

## 0955

放逐一单位，由拥有者免费打出到其原位置

u:Unit=目标单位;owner:Player=u拥有者;original_location:Location=该单位原地点LKI

```python

removed = ops.banish([u]).value
if removed:
    ops.play(removed[0], owner, origin=owner.banish, destination=original_location, cost_policy=IGNORE_BASE_COST)

```



<a id="card-0956"></a>

## 0956

任意符能1横置，使本回合下一个p法术回响等同其费用

cost:Cost=PowerAny1横置me;binding:CostBinding=主动费用

```python

ops.pay(p, cost, binding=binding)

```

NEXT_ABILITY:缺下一法术动态绑定/捕获费用并在其定稿前授予Repeat的动作，不能以不存在spell预绑定代替



<a id="card-0957"></a>

## 0957

移动敌军至其控制者另一单位所在位置

u:Selection[Unit]=一敌军;dest:Location=有相同控制者另一单位的位置

```python

ops.move(u, dest)

```

REPEAT:单次效果已描述，回响额外费用和重复选择未独立展开



<a id="card-0958"></a>

## 0958

触手纯属性指示物

 

```python

# 无独立文本动作

```



<a id="card-0959"></a>

## 0959

据守使本回合下一个p法术回响等同基础费用

 

```python

# 缺下一法术绑定与在打出定稿内授予能力的约定

```

NEXT_ABILITY:无法独立表达下一个未知法术捕获基础费用并授予Repeat



<a id="card-0960"></a>

## 0960

各玩家首个开始阶段开始时该玩家获得1分

actor:Player=进入自己首个BeginningPhase的玩家

```python

ops.gain_points(actor, 1)

```



<a id="card-0961"></a>

## 0961

打出或移动时二选一：抽1或同地全敌军2；部署及仅为单位时游走保留

options:list[ChoiceValue]=draw或damage;enemies:Selection[Unit]=me所在地所有敌方单位;mode:list[str]=本入口合法模式选择结果单元素列表；普通法术/主动在定稿绑定，后续可选模式按指定结算时点绑定

```python

# mode由本入口明确的合法模式选择绑定；不是标签宣告
if mode == ["draw"]:
    ops.draw(p, 1)
else:
    ops.damage(enemies, 2)

```



<a id="card-0962"></a>

## 0962

按勘误有增益p单位将死可付任意符能1横置传奇消耗buff，改治愈横置召回；征服重置传奇

 

```python

# 费用及动作可分别表达，但不能取消死亡事件；ready亦不接受传奇

```

REPLACE:缺可付费的单位死亡替代接口

LEGEND_READY:征服重置传奇无合法ready调用

LANG:部分EN印刷缺征服句，旧文本及TC治愈步骤不一致，按勘误



<a id="card-0963"></a>

## 0963

征服此处查看2可回收任意张余牌任意排序回顶，即洞察2

 

```python

ops.predict(p, 2)

```



<a id="card-0964"></a>

## 0964

按勘误各玩家每回合首次用法术选择此处友军时，该玩家抽1

actor:Player=法术选择的执行玩家

```python

ops.draw(actor, 1)

```

LANG:旧EN/SC以you表述，勘误与TC明确每玩家



<a id="card-0965"></a>

## 0965

定稿亮出牌；打出若成功则按其Power费用洞察再抽2

requirement:ShowOffRequirement=任意卡牌且场上不能选me;link:Link=此次亮出凭证;showed:bool=凭证成功;n:int=被亮出牌Power费用快照

```python

# 定稿
ops.show_off(p, requirement, link=link)
# 打出触发
if showed:
    ops.predict(p, n)
    ops.draw(p, 2)

```



<a id="card-0966"></a>

## 0966

p打出到p控制战场的单位活跃进场

 

```python

# 不能以打出后ready代替入场状态

```

ENTRY:缺持续修饰未来所有符合地点的单位entry接口



<a id="card-0967"></a>

## 0967

部署保留；打出弃1抽3；据守此处回拥有者手

hand:list[Card]=p手牌;origin:Zone=me当前区域

```python

# 打出触发
ops.discard(p, 1)
ops.draw(p, 3)
# 据守此处触发
ops.transfer([me], origin, me.owner.hand)

```



<a id="card-0968"></a>

## 0968

p据守此处且此处控制单位≥7则赢

authorization:WinAuthorization=本牌在据守触发结算时确认p控制here至少7单位的授权

```python

ops.win(p, authorization=authorization)

```

DATA:EN OGN-293a规则空，其他EN/SC/TC有胜利效果



<a id="card-0969"></a>

## 0969

从p废牌堆打出单位只忽略能量

eligible:list[Card]=p废牌堆单位;dest:Location/Zone=合法目的地;ignore_energy:CostPolicy=仅忽略Energy保留Power

```python

c = ops.choose(p, eligible, targeting=False, bind_at="resolution").value
if c:
    ops.play(c[0], p, origin=p.trash, destination=dest, cost_policy=ignore_energy)

```



<a id="card-0970"></a>

## 0970

打出定稿宣告标签；横置主动使该标签单位本回合−2

tags:list[ChoiceValue]=所有合法标签;cost:Cost=横置me;binding:CostBinding=主动费用;u:Selection[Unit]=具有已宣告标签的一单位

```python

# as-play宣告并保存为本实例选择
ops.declare(p, tags)
# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_might(u, -2, duration=THIS_TURN)

```

CHOICE_LINK:declare返回值如何保存至卡实例供未来技能读取，接口未定义持久选择绑定



<a id="card-0971"></a>

## 0971

据守此处所有玩家各召出1休眠符文

players:list[Player]=全部玩家

```python

for actor in players:
    ops.channel(actor, 1, exhausted=True)

```

PLAYER_BATCH:跨玩家同一召出指令批次与次序未定义



<a id="card-0972"></a>

## 0972

摧毁场上全部单位

units:Selection[Unit]=全场全部单位

```python

ops.kill(units)

```



<a id="card-0973"></a>

## 0973

按勘误能量1横置，将战场友军移动到其控制者基地

cost:Cost=Energy1横置me;binding:CostBinding=主动费用;u:Unit=战场一友方单位

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.move([u], u.controller.base)

```

LANG:早期EN为your base，勘误改its base与SC/TC相符



<a id="card-0974"></a>

## 0974

默认休眠金币1；p回合且本牌正面朝下打出则改活跃金币3

gold:TokenTemplate=Gold;enhanced:bool=p回合且本牌从face-down打出;ready_entry:EntryState=ready;exhausted_entry:EntryState=exhausted

```python

for i in range(3 if enhanced else 1):
    ops.play(gold, p, origin=None, destination=p.base, entry=ready_entry if enhanced else exhausted_entry)

```



<a id="card-0975"></a>

## 0975

装配能量1Mind1；宿主死后放逐宿主并与装备链接；未贴附主动能量3Mind1放逐装备，免费打出所有所链接单位

equip_cost:Cost=Energy1Mind1;equip_binding:CostBinding=Equip主动;u:Unit=p控制单位;host:Selection[Card]=死亡后宿主卡;link:Link=本装备放逐单位关联;release_cost:Cost=Energy3Mind1且放逐me;release_binding:CostBinding=仅未贴附可发动;linked:list[Card]=仍在放逐区与link关联单位;destinations:list[Location/Zone]=逐次合法地点

```python

# 装配
paid = ops.pay(p, equip_cost, binding=equip_binding)
if paid.value is not None:
    ops.attach(me, u)
# 宿主死亡触发
ops.banish(host, link=link)
# 释放主动
paid = ops.pay(p, release_cost, binding=release_binding)
if paid.value is not None:
    for card, dest in zip(linked, destinations):
        ops.play(card, p, origin=card.owner.banish, destination=dest, cost_policy=IGNORE_BASE_COST)

```

DATA:SC缺少装备EFFECT中的Deathknell放逐关联来源



<a id="card-0976"></a>

## 0976

迅捷摧毁所有装备

gear:Selection[Gear]=场上所有装备

```python

ops.kill(gear)

```



<a id="card-0977"></a>

## 0977

打出全体敌军本回合−3最低1，急速保留

enemies:Selection[Unit]=全场所有敌方单位

```python

ops.modify_might(enemies, -3, duration=THIS_TURN, floor=1)

```



<a id="card-0978"></a>

## 0978

此处开战，进攻者和防守者各加能量1

attacker:Player=此次战斗进攻者;defender:Player=此次战斗防守者;resources:ResourceBundle=Energy1

```python

ops.add_resources(attacker, resources)
ops.add_resources(defender, resources)

```

PLAYER_BATCH:两位玩家同一指令获得资源的批次未约定



<a id="card-0979"></a>

## 0979

放逐友军，由拥有者免费打出至任意战场

u:Unit=一友方单位;owner:Player=u拥有者;b:Battlefield=任意战场;permission:PlayPermission=本次可打出该单位到所选任意战场

```python

removed = ops.banish([u]).value
if removed:
    ops.play(removed[0], owner, origin=owner.banish, destination=b, cost_policy=IGNORE_BASE_COST, permission=permission)

```



<a id="card-0980"></a>

## 0980

迅捷一次效果眩晕进攻方单位

u:Selection[Unit]=一进攻单位

```python

ops.stun(u)

```

REPEAT:回响能量2的重复付款及另组预选目标未独立展开



<a id="card-0981"></a>

## 0981

me在战场时对手不能获得分数，采用gain勘误

subjects:PermissionSelection=p全部对手;restriction:RestrictionSpec=不能gain_points而非仅不能score;at_battlefield:bool=me在战场;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if at_battlefield:
    ops.restrict_action(subjects, restriction, duration=WHILE_CONDITION)

```

LANG:原印刷score改gain，禁止范围扩大，按勘误



<a id="card-0982"></a>

## 0982

打出对所有战场全部单位3伤含友军

units:Selection[Unit]=所有战场单位

```python

ops.damage(units, 3)

```



<a id="card-0983"></a>

## 0983

按勘误打出可选不同地点p单位，交换me和该单位位置

 

```python

# 不用两次独立move掩盖同时交换的批次问题

```

MOVE_BATCH:move单目的地不能保证双方同时交换

LANG:早期EN/SC未限定p控制和不同地点，按勘误



<a id="card-0984"></a>

## 0984

当前回合之后额外一个p回合，然后放逐本牌

 

```python

ops.extra_turn(p, 1, after=CURRENT_TURN)
ops.banish([me])

```



<a id="card-0985"></a>

## 0985

p打出战力严格大于场上每个其他单位时，横置me为触发费用抽1

cost:Cost=横置me;binding:CostBinding=此触发的必要费用，不能自愿免付而抽牌

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.draw(p, 1)

```



<a id="card-0986"></a>

## 0986

打出且p控制符文≥7，敌方装备已强化则解除否则摧毁

g:Gear=一敌方装备

```python

if g.empowered:
    ops.disempower([g])
else:
    ops.kill([g])

```



<a id="card-0987"></a>

## 0987

强化能量2；横置主动使单位本回合+2，me强化时改+4

empower_cost:Cost=Energy2;empower_binding:CostBinding=未强化时Empower主动;cost:Cost=横置me;binding:CostBinding=战力主动;u:Selection[Unit]=一单位;empowered:bool=me已强化

```python

# 强化
paid = ops.pay(p, empower_cost, binding=empower_binding)
if paid.value is not None:
    ops.empower([me])
# 战力主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_might(u, 4 if empowered else 2, duration=THIS_TURN)

```



<a id="card-0988"></a>

## 0988

从face-down打出时可强化同地物体，回合末解除其强化

objects:list[Permanent]=此处单位/装备;accept:bool=选择强化

```python

if accept:
    chosen = ops.choose(p, objects).value
    ops.empower(chosen)

```

DELAY:缺少登记本回合结束解除该对象强化的未来动作



<a id="card-0989"></a>

## 0989

固有坚守2壁垒

defender:bool=me防守方;scope:RuleScope=me战斗伤害分配;change:RuleChange=先承担;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if defender:
    ops.modify_might([me], 2, duration=WHILE_CONDITION)
ops.modify_rule(COMBAT_DAMAGE_ORDER, scope, change, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-0990"></a>

## 0990

本回合有任意单位死则活跃进场；强攻保留

dest:Location/Zone=合法打出位置;entry:EntryState=本回合单位死亡历史存在则ready否则默认

```python

ops.play(me, p, origin=p.hand, destination=dest, entry=entry)

```



<a id="card-0991"></a>

## 0991

Chaos1横置，友军回拥有者手，可免费打出较该单位原战力低单位

cost:Cost=Chaos1横置me;binding:CostBinding=主动费用;u:Unit=友方单位;origin:Zone=u原区域;n:int=u原战力LKI;hand:list[Card]=p手牌单位，战力严格<n;dest:Location/Zone=合法目的地

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.transfer([u], origin, u.owner.hand)
    card = ops.choose(p, hand, minimum=0, targeting=False, bind_at="resolution").value
    if card:
        ops.play(card[0], p, origin=p.hand, destination=dest, cost_policy=IGNORE_BASE_COST)

```



<a id="card-0992"></a>

## 0992

征服此处且分配过量伤害≥3，打出1战力法盾鸟

bird:TokenTemplate=1战力Bird含Deflect;dest:Location/Zone=合法目的地

```python

ops.play(bird, p, origin=None, destination=dest)

```



<a id="card-0993"></a>

## 0993

移动触发弃1再抽1

hand:list[Card]=p手牌

```python

ops.discard(p, 1)
ops.draw(p, 1)

```



<a id="card-0994"></a>

## 0994

征服此处可付能量1打出休眠金币

cost:Cost=Energy1;binding:CostBinding=可选触发费用;gold:TokenTemplate=Gold;entry:EntryState=exhausted

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.play(gold, p, origin=None, destination=p.base, entry=entry)

```



<a id="card-0995"></a>

## 0995

移动触发打出休眠金币

gold:TokenTemplate=Gold;entry:EntryState=exhausted

```python

ops.play(gold, p, origin=None, destination=p.base, entry=entry)

```



<a id="card-0996"></a>

## 0996

离场抽1召出休眠符文；Chaos1横置主动摧毁自己

cost:Cost=Chaos1横置me;binding:CostBinding=主动费用

```python

# 离场触发
ops.draw(p, 1)
ops.channel(p, 1, exhausted=True)
# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.kill([me])

```



<a id="card-0997"></a>

## 0997

据守打出活跃3战力瞬息精灵此处；固有坚守保留

sprite:TokenTemplate=Sprite含Temporary;entry:EntryState=ready

```python

ops.play(sprite, p, origin=None, destination=here, entry=entry)

```



<a id="card-0998"></a>

## 0998

任意数量同控制者敌军总战力≤8同时移动到同一地点

units:Selection[Unit]=合法选择的敌军集合，必须同一控制者且战力总和≤8;dest:Location=共同合法目的地

```python

ops.move(units, dest, simultaneous=True)

```



<a id="card-0999"></a>

## 0999

打出看4，可展示能量≤3符能≤1单位/装备抽该牌，其余回收

 

```python

top = ops.look(p, p.main_deck, 4).value
units_or_gear = [c for c in top if c.card_type in ("unit", "gear") and c.energy_cost <= 3 and c.power_cost <= 1]
one = ops.choose(p, units_or_gear, minimum=0, targeting=False, bind_at="resolution").value
if one:
    ops.reveal(one)
    ops.draw(p, 1, cards=one)
ops.recycle([c for c in top if c not in one])

```



<a id="card-1000"></a>

## 1000

本回合此前已打过其他牌，打出增益自身；Legion非无条件buff

 

```python

ops.buff([me])

```



<a id="card-1001"></a>

## 1001

此处所有单位持续+1，包括进攻方和敌军

units:Selection[Unit]=here处全部单位动态集合

```python

ops.modify_might(units, 1, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-1002"></a>

## 1002

装配Body1；宿主据守得分1

cost:Cost=Body1;binding:CostBinding=装配费用;u:Unit=p控制单位;host_player:Player=宿主据守效果控制者

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 宿主据守
ops.gain_points(host_player, 1)

```

DATA:SC缺少装备EFFECT



<a id="card-1003"></a>

## 1003

进攻缴械1

u:Selection[Unit]=此处一敌方单位

```python

ops.modify_might(u, -1, duration=THIS_TURN)

```



<a id="card-1004"></a>

## 1004

打出4休眠金币

gold:TokenTemplate=Gold;entry:EntryState=exhausted

```python

for i in range(4):
    ops.play(gold, p, origin=None, destination=p.base, entry=entry)

```



<a id="card-1005"></a>

## 1005

有另一p控制单位同地时me+1

condition:bool=p在me同地有非me单位;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if condition:
    ops.modify_might([me], 1, duration=WHILE_CONDITION)

```



<a id="card-1006"></a>

## 1006

进攻后征服且本次向敌军分配过量≥5得分1

 

```python

ops.gain_points(p, 1)

```

LANG:SC写得分+1可能误读成替代修饰，EN/TC是独立得1分



<a id="card-1007"></a>

## 1007

给一装备瞬息

gear:Selection[Gear]=一装备

```python

ops.grant_keyword(gear, TEMPORARY, duration=PERMANENT)

```



<a id="card-1008"></a>

## 1008

进攻触发重置另一友军

u:Selection[Unit]=非me的一友方单位

```python

ops.ready(u)

```



<a id="card-1009"></a>

## 1009

友军+1本回合，并本回合不可被敌方法术/能力选择

u:Selection[Unit]=一友方单位;restriction:RestrictionSpec=敌方法术和能力不能选择该单位

```python

ops.modify_might(u, 1, duration=THIS_TURN)
ops.restrict_action(u, restriction, duration=THIS_TURN)

```

FLOW_EXIT:流转的额外打出路径及离链放逐未独立展开



<a id="card-1010"></a>

## 1010

移动战力≤3单位

u:Selection[Unit]=战力≤3单位;dest:Location=合法目的地

```python

ops.move(u, dest)

```

FLOW_EXIT:流转流程未独立展开



<a id="card-1011"></a>

## 1011

进攻展示顶符文回收，按领域分支；Fury同地一敌军2其余1，Mind抽1，Order眩晕

top:list[Rune]=p符文堆顶至多1;domain:str=本次展示符文领域LKI;u:Selection[Unit]=Order分支一敌方单位

```python

ops.reveal(top)
ops.recycle(top)
if domain == "mind":
    ops.draw(p, 1)
elif domain == "order":
    ops.stun(u)
# Fury分支保留缺口，不错误拆成分配伤害

```

DAMAGE_BATCH:Fury分支不同目标不同伤害同一批次，damage单一amount的each不能覆盖，split会错误改变额外伤害规则



<a id="card-1012"></a>

## 1012

消耗me增益主动，选择本回合尚未选的4模式

cost:Cost=消耗me增益;binding:CostBinding=主动费用;options:list[ChoiceValue]=本回合未选的damage/stun/ready/ganking;u:Selection[Unit]=前两个模式战场一单位;mode:list[str]=本入口合法模式选择结果单元素列表；普通法术/主动在定稿绑定，后续可选模式按指定结算时点绑定

```python

# mode由本入口明确的合法模式选择绑定；不是标签宣告
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    if mode == ["damage"]:
        ops.damage(u, 2)
    elif mode == ["stun"]:
        ops.stun(u)
    elif mode == ["ready"]:
        ops.ready([me])
    else:
        ops.grant_keyword([me], GANKING, duration=THIS_TURN)

```



<a id="card-1013"></a>

## 1013

仅me在战场可横置主动打出2法盾鸟

cost:Cost=横置me;binding:CostBinding=仅me在战场可发动;bird:TokenTemplate=1战力Bird含Deflect;destinations:list[Location/Zone]=两次合法目的地

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    for dest in destinations:
        ops.play(bird, p, origin=None, destination=dest)

```



<a id="card-1014"></a>

## 1014

先横置所有友军，再对所有战场单位12伤

friendly:Selection[Unit]=全场友方单位;units:Selection[Unit]=全场位于战场单位含友军

```python

ops.exhaust(friendly)
ops.damage(units, 12)

```



<a id="card-1015"></a>

## 1015

死亡弃2然后抽2

 

```python

ops.discard(p, 2)
ops.draw(p, 2)

```



<a id="card-1016"></a>

## 1016

打出其他p单位本回合+2；从牌堆被展示的内联过程中产能量2

units:Selection[Unit]=非me的p控制单位;resources:ResourceBundle=Energy2

```python

# 打出触发
ops.modify_might(units, 2, duration=THIS_TURN)
# 被展示的内联效果片段
ops.add_resources(p, resources)

```

AS_VIEW:reveal没有as-revealed内联挂钩，不能改成展示后普通触发

LANG:SC如果被展示的句式未明确as内联，采用EN



<a id="card-1017"></a>

## 1017

本回合已打过其他牌，可从废牌堆以能量3Fury1打出me

condition:bool=本回合已打出其他牌;permission:PermissionSpec=允许从p废牌堆打出me;subjects:CostSelection=me从废牌堆打出的费用;alternate:CostChange=该来源替代基础费用Energy3Fury1;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if condition:
    ops.grant_permission([me], permission, duration=WHILE_CONDITION)
    ops.modify_cost(subjects, alternate, duration=WHILE_CONDITION)

```



<a id="card-1018"></a>

## 1018

若选择Bird/Cat/Dog/Poro则能量减2；p废牌堆费用≤能量2符能1单位免费打出

subjects:CostSelection=本次法术;discount:CostChange=选中上述标签单位时Energy减2最低0;tag_chosen:bool=定稿已选择符合标签单位;eligible:list[Card]=p废牌堆单位Energy≤2且Power≤1;dest:Location/Zone=合法目的地;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

# 定稿费用
if tag_chosen:
    ops.modify_cost(subjects, discount, duration=THIS_PLAY)
# 结算
c = ops.choose(p, eligible).value
if c:
    ops.play(c[0], p, origin=p.trash, destination=dest, cost_policy=IGNORE_BASE_COST)

```



<a id="card-1019"></a>

## 1019

按勘误能量2横置传奇，将友军移入或移出其控制者基地

cost:Cost=Energy2横置me;binding:CostBinding=主动费用;u:Selection[Unit]=一友方单位;dest:Location=本次合法目的地，必须一端为该单位控制者基地

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.move(u, dest)

```

LANG:旧EN是your base，勘误为its base



<a id="card-1020"></a>

## 1020

弃1横置主动，选友军，本回合下次将死可付Fury1改治愈横置召回

cost:Cost=弃1手牌且横置me;binding:CostBinding=主动费用

```python

ops.pay(p, cost, binding=binding)

```

REPLACE:缺少一次可付费死亡替代事件接口

LANG:原印刷缺治愈及would，按勘误而非死后召回



<a id="card-1021"></a>

## 1021

死亡且me死亡前战力≥5则抽2

was_mighty:bool=me死亡前最后战力≥5

```python

if was_mighty:
    ops.draw(p, 2)

```



<a id="card-1022"></a>

## 1022

反应预防本回合全部法术和技能伤害，不限定友军

units:Selection[Unit]=本回合所有单位动态集合含稍后入场;sources:Predicate=法术或技能，不含战斗

```python

ops.prevent_damage(units, INFINITY, source_filter=sources, duration=THIS_TURN)

```

LANG:TC“本回合不受”未写完整对象，按EN/SC全体法术技能伤害



<a id="card-1023"></a>

## 1023

打出2比尔吉沃特触手单位

tentacle:TokenTemplate=1战力Tentacle标签Bilgewater;destinations:list[Location/Zone]=两次合法目的地

```python

for dest in destinations:
    ops.play(tentacle, p, origin=None, destination=dest)

```

FLOW_EXIT:流转能量3及离链放逐未独立展开



<a id="card-1024"></a>

## 1024

一次效果重置一单位

u:Selection[Unit]=一单位

```python

ops.ready(u)

```

REPEAT:回响能量2额外费与另一组选择未独立展开



<a id="card-1025"></a>

## 1025

玩家此处打出单位，可付能量1增益它

actor:Player=该单位打出者;u:Selection[Unit]=该次打出单位;cost:Cost=Energy1;binding:CostBinding=actor的可选触发费用

```python

paid = ops.pay(actor, cost, binding=binding)
if paid.value is not None:
    ops.buff(u)

```



<a id="card-1026"></a>

## 1026

横置主动打出3随从，可各不同合法地点

cost:Cost=横置me;binding:CostBinding=主动费用;recruit:TokenTemplate=1战力Recruit;destinations:list[Location/Zone]=三个逐次合法位置

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    for dest in destinations:
        ops.play(recruit, p, origin=None, destination=dest)

```



<a id="card-1027"></a>

## 1027

自身活跃进场

dest:Location/Zone=合法目的地;entry:EntryState=ready

```python

ops.play(me, p, origin=p.hand, destination=dest, entry=entry)

```



<a id="card-1028"></a>

## 1028

本回合已打过其他牌，打出触发此处打出2随从

recruit:TokenTemplate=1战力Recruit

```python

for i in range(2):
    ops.play(recruit, p, origin=None, destination=here)

```



<a id="card-1029"></a>

## 1029

有增益友军死亡时，增益另一友军

u:Selection[Unit]=非死亡单位的一友方单位

```python

ops.buff(u)

```



<a id="card-1030"></a>

## 1030

纯属性单位，无规则文本

 

```python

# 无独立文本动作

```



<a id="card-1031"></a>

## 1031

迅捷给予单位本回合强攻2和游走

u:Selection[Unit]=一单位;params:KeywordParameters=Assault2

```python

ops.grant_keyword(u, ASSAULT, parameters=params, duration=THIS_TURN)
ops.grant_keyword(u, GANKING, duration=THIS_TURN)

```



<a id="card-1032"></a>

## 1032

据守此处使p非token单位本回合打出能量费+1

subjects:CostSelection=p非token单位打出费用;change:CostChange=Energy加1

```python

ops.modify_cost(subjects, change, duration=THIS_TURN)

```



<a id="card-1033"></a>

## 1033

敌方控制任一战场则自身活跃进场；征服可付能量1回拥有者手；强攻3保留

dest:Location/Zone=合法打出位置;entry:EntryState=对手控制战场则ready否则默认;cost:Cost=Energy1;binding:CostBinding=可选征服触发费用;origin:Zone=me当前区域

```python

# 打出入口
ops.play(me, p, origin=p.hand, destination=dest, entry=entry)
# 征服触发
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.transfer([me], origin, me.owner.hand)

```



<a id="card-1034"></a>

## 1034

征服此处可重置友方装备，若为武装还可卸除

eligible:list[Gear]=友方装备;detach_selected:bool=选择卸除

```python

g = ops.choose(p, eligible, minimum=0).value
if g:
    ops.ready(g)
    if "Equipment" in g[0].tags and detach_selected:
        ops.detach(g)

```



<a id="card-1035"></a>

## 1035

摧毁一单位

u:Selection[Unit]=一单位

```python

ops.kill(u)

```



<a id="card-1036"></a>

## 1036

百炼打出可付装配费减任意符能1，装配p武装到me

g:Gear=p控制武装可已贴附;cost:Cost=g装配费用减Power1最低0;binding:CostBinding=可选百炼触发费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(g, me)

```



<a id="card-1037"></a>

## 1037

me在战场时对手打出单位，眩晕它并该对手本回合不能移动它

u:Selection[Unit]=该次打出单位;restriction:RestrictionSpec=该次打出者本回合不能move该单位，非禁止所有玩家move它

```python

ops.stun(u)
ops.restrict_action(u, restriction, duration=THIS_TURN)

```



<a id="card-1038"></a>

## 1038

me战斗中友方法术Energy1Power1减费能量最低1，敌方法术两者各+1

friendly:CostSelection=友方法术含队友;enemy:CostSelection=敌方法术;discount:CostChange=Energy减1底线1且Power减1最低0;increase:CostChange=Energy加1且Power加1;in_combat:bool=me战斗中;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if in_combat:
    ops.modify_cost(friendly, discount, duration=WHILE_CONDITION)
    ops.modify_cost(enemy, increase, duration=WHILE_CONDITION)

```



<a id="card-1039"></a>

## 1039

p眩晕一战场敌军时可移动me至该战场；坚守壁垒保留

b:Battlefield=该被眩晕单位事件地点;accept:bool=选择移动

```python

if accept:
    ops.move([me], b)

```



<a id="card-1040"></a>

## 1040

回收p废牌堆1作为主动费，me本回合+1，可重复发动

cost:Cost=回收p废牌堆一张牌;binding:CostBinding=无每回合次数限制主动费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_might([me], 1, duration=THIS_TURN)

```



<a id="card-1041"></a>

## 1041

能量2Fury1主动以当前战力为快照再加同值本回合；法盾保留

cost:Cost=Energy2Fury1;binding:CostBinding=主动费用;n:int=结算翻倍指令时me战力快照

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.modify_might([me], n, duration=THIS_TURN)

```



<a id="card-1042"></a>

## 1042

进攻眩晕同地敌军；伏击保留

u:Selection[Unit]=同地一敌方单位

```python

ops.stun(u)

```



<a id="card-1043"></a>

## 1043

另一友军死亡获得XP1

 

```python

ops.gain_xp(p, 1)

```



<a id="card-1044"></a>

## 1044

p在对手回合打出牌触发打出随从至基地

recruit:TokenTemplate=1战力Recruit

```python

ops.play(recruit, p, origin=None, destination=p.base)

```



<a id="card-1045"></a>

## 1045

另一p控制非Recruit单位死亡触发打出随从基地

recruit:TokenTemplate=1战力Recruit

```python

ops.play(recruit, p, origin=None, destination=p.base)

```



<a id="card-1046"></a>

## 1046

同地战力低于me敌军不能造成战斗伤害；据守抽1；伏击保留

units:PermissionSelection=me同地且当前战力低于me的敌军动态集合;restriction:RestrictionSpec=禁止造成combat_damage

```python

# 持续入口
ops.restrict_action(units, restriction, duration=WHILE_SOURCE_PRESENT)
# 据守
ops.draw(p, 1)

```



<a id="card-1047"></a>

## 1047

单位不能从此处移动到基地

units:PermissionSelection=here全部单位;restriction:RestrictionSpec=禁止move从here到base，不禁止recall

```python

ops.restrict_action(units, restriction, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-1048"></a>

## 1048

p法术花费Energy≥4打出时可放逐并与传奇关联；关联恰4张则各入自己废牌堆，召出4活跃符文抽1

spell:Card=该次打出的法术实体;link:Link=此传奇关联放逐牌;accept:bool=选择放逐;linked:list[Card]=本次放逐后仍在放逐区且与此传奇关联的法术

```python

if accept:
    ops.banish([spell], link=link)
    if len(linked) == 4:
        for c in linked:
            ops.transfer([c], c.owner.banish, c.owner.trash)
        ops.channel(p, 4)
        ops.draw(p, 1)

```

BATCH:四法术可能不同拥有者，逐个transfer不保证同一多目的批次

CHAIN_TIMING:本句打出触发放逐的链上卡身份与链项后续处理需补明确契约，不把Card和ChainItem混用



<a id="card-1049"></a>

## 1049

先移动一友军，再移动一敌军；同时到未控战场时p为进攻者按正常过程

friendly:Selection[Unit]=一友军;enemy:Selection[Unit]=一敌军;friendly_dest:Location=友军目的地;enemy_dest:Location=敌军目的地

```python

ops.move(friendly, friendly_dest)
ops.move(enemy, enemy_dest)

```



<a id="card-1050"></a>

## 1050

按勘误征服可横置传奇，展示2可放逐1打出，回收其余

cost:Cost=横置me;binding:CostBinding=可选征服触发费用;top:list[Card]=p主牌堆顶至多2;dest:Location/Zone=所选牌合法打出位置

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.reveal(top)
    one = ops.choose(p, top, minimum=0, targeting=False, bind_at="resolution").value
    if one:
        ops.banish(one)
        ops.play(one[0], p, origin=p.banish, destination=dest)
    ops.recycle([c for c in top if c not in one])

```

LANG:未勘误EN/SC缺放逐步骤，按2026-01-14勘误



<a id="card-1051"></a>

## 1051

从非p手牌区域打出自身能量减2

subjects:CostSelection=me从非p手牌区域打出费用;discount:CostChange=Energy减2最低0

```python

ops.modify_cost(subjects, discount, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-1052"></a>

## 1052

按勘误所有法术/技能对此处单位额外伤害1

events:DamageSelection=全部玩家法术技能对here单位伤害，按715处理分配伤害池;bonus:NumericChange=add1

```python

ops.modify_damage(events, bonus, duration=WHILE_SOURCE_PRESENT)

```

LANG:旧SC为以此处单位作目标、EN为affecting，勘误不限选择目标



<a id="card-1053"></a>

## 1053

p将展示牌堆卡时，先看其顶牌可回收，再执行原展示

 

```python

# look/recycle存在，但缺向待发生reveal插入前置步骤并重新计算展示牌的接口

```

REPLACE:没有通用展示前事件改写/中间步骤挂钩，不能展示后再洞察



<a id="card-1054"></a>

## 1054

按勘误展示2可放逐1减能量2打出，抽未放逐者

top:list[Card]=p主牌堆顶至多2;discount:CostChange=本次Energy减2最低0;dest:Location/Zone=合法目的地;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

ops.reveal(top)
one = ops.choose(p, top, minimum=0, targeting=False, bind_at="resolution").value
if one:
    ops.banish(one)
    ops.modify_cost(one, discount, duration=THIS_PLAY)
    ops.play(one[0], p, origin=p.banish, destination=dest)
rest = [c for c in top if c not in one]
ops.draw(p, len(rest), cards=rest)

```

LANG:原印刷抽未打出牌；勘误改抽未放逐牌，打出失败亦不能抽被放逐者



<a id="card-1055"></a>

## 1055

迅捷对战场单位4伤再抽1

u:Selection[Unit]=战场一单位

```python

ops.damage(u, 4)
ops.draw(p, 1)

```



<a id="card-1056"></a>

## 1056

赢战斗XP1；XP1横置传奇增益单位；XP2横置传奇移休眠战场友军回其基地

buff_cost:Cost=XP1横置me;buff_binding:CostBinding=增益主动;u:Selection[Unit]=一单位;move_cost:Cost=XP2横置me;move_binding:CostBinding=移动主动;friend:Unit=战场一休眠友军

```python

# 赢战斗触发
ops.gain_xp(p, 1)
# 增益主动
paid = ops.pay(p, buff_cost, binding=buff_binding)
if paid.value is not None:
    ops.buff(u)
# 移动主动
paid = ops.pay(p, move_cost, binding=move_binding)
if paid.value is not None:
    ops.move([friend], friend.controller.base)

```



<a id="card-1057"></a>

## 1057

进攻将总5伤分配给此处任意敌军；法盾2保留

units:Selection[Unit]=此处选定敌军;allocation:dict[Unit,int]=按规则分配总5加池级额外伤害

```python

ops.damage(units, 5, mode="split", allocation=allocation)

```



<a id="card-1058"></a>

## 1058

对手移动到me不在的战场时抽1；坚守3壁垒保留

 

```python

ops.draw(p, 1)

```



<a id="card-1059"></a>

## 1059

征服或据守Hunt3

 

```python

ops.gain_xp(p, 3)

```



<a id="card-1060"></a>

## 1060

待命迅捷战场单位3伤后打出休眠金币

u:Selection[Unit]=战场一单位;gold:TokenTemplate=Gold;entry:EntryState=exhausted

```python

ops.damage(u, 3)
ops.play(gold, p, origin=None, destination=p.base, entry=entry)

```



<a id="card-1061"></a>

## 1061

打出选择对手，该对手打出法盾鸟；自身法盾保留

opponent:Player=选定对手;bird:TokenTemplate=1战力Bird含Deflect;dest:Location/Zone=由opponent选择其合法位置

```python

ops.play(bird, opponent, origin=None, destination=dest)

```



<a id="card-1062"></a>

## 1062

迅捷可选额外消耗一个buff代替本法术基础费用，结算重置单位

subjects:CostSelection=本法术;change:CostChange=可选分支消耗一个友方单位buff作为附加费用并忽略本法术基础费用，仍支付非被豁免附加费;u:Selection[Unit]=一单位;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

# 费用
ops.modify_cost(subjects, change, duration=THIS_PLAY)
# 结算
ops.ready(u)

```



<a id="card-1063"></a>

## 1063

打出触发单位本回合+2；急速保留

u:Selection[Unit]=一单位

```python

ops.modify_might(u, 2, duration=THIS_TURN)

```



<a id="card-1064"></a>

## 1064

Body1装配；宿主征服增益自身

cost:Cost=Body1;binding:CostBinding=Equip主动;u:Unit=p控制单位;host:Selection[Unit]=该能力宿主

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 宿主征服
ops.buff(host)

```

DATA:SC缺少装备EFFECT



<a id="card-1065"></a>

## 1065

自身活跃进场；进攻摧毁此处所有受伤敌军

dest:Location/Zone=合法打出位置;entry:EntryState=ready;enemies:Selection[Unit]=此处具有伤害标记的所有敌军

```python

# 打出入口
ops.play(me, p, origin=p.hand, destination=dest, entry=entry)
# 进攻触发
ops.kill(enemies)

```



<a id="card-1066"></a>

## 1066

p装备全部拥有法盾

gear:Selection[Gear]=p控制全部装备动态集合

```python

ops.grant_keyword(gear, DEFLECT, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-1067"></a>

## 1067

死亡抽1

 

```python

ops.draw(p, 1)

```



<a id="card-1068"></a>

## 1068

三个独立横置主动：金币、杀友方装备得随从、杀友军得机械

gold_cost:Cost=横置me;gold_binding:CostBinding=金币主动费用;recruit_cost:Cost=杀一友方装备且横置me;recruit_binding:CostBinding=随从主动费用;mech_cost:Cost=杀一友方单位且横置me;mech_binding:CostBinding=机械主动费用;gold:TokenTemplate=Gold;recruit:TokenTemplate=1战力Recruit;mech:TokenTemplate=3战力Mech;entry:EntryState=exhausted;recruit_dest:Location/Zone=合法随从位置;mech_dest:Location/Zone=合法机械位置

```python

# 金币主动
paid = ops.pay(p, gold_cost, binding=gold_binding)
if paid.value is not None:
    ops.play(gold, p, origin=None, destination=p.base, entry=entry)
# 随从主动
paid = ops.pay(p, recruit_cost, binding=recruit_binding)
if paid.value is not None:
    ops.play(recruit, p, origin=None, destination=recruit_dest)
# 机械主动
paid = ops.pay(p, mech_cost, binding=mech_binding)
if paid.value is not None:
    ops.play(mech, p, origin=None, destination=mech_dest)

```



<a id="card-1069"></a>

## 1069

从下位玩家开始各玩家可选一单位回拥有者手牌，顺序执行

players:list[Player]=下位玩家开始次序;units:dict[Player,list[Unit]]=轮到该玩家时全场合法单位;origins:dict[Unit,Zone]=各单位当时区域

```python

for actor in players:
    selected = ops.choose(actor, units[actor], minimum=0, targeting=False, bind_at="resolution").value
    if selected:
        u = selected[0]
        ops.transfer([u], origins[u], u.owner.hand)

```

ACTOR:transfer没有执行玩家，无法保留各actor进行回手的行动归属



<a id="card-1070"></a>

## 1070

打出一单位本回合+8

u:Selection[Unit]=一单位

```python

ops.modify_might(u, 8, duration=THIS_TURN)

```



<a id="card-1071"></a>

## 1071

独自进攻或独自防守时me+2

alone:bool=me是自己一方唯一进攻者或唯一防守者;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if alone:
    ops.modify_might([me], 2, duration=WHILE_CONDITION)

```



<a id="card-1072"></a>

## 1072

看顶5可放逐一单位或装备减能量5打出，回收余牌，再可做此事强化它

discount:CostChange=本次Energy减5最低0;dest:Location/Zone=合法位置;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

top = ops.look(p, p.main_deck, 5).value
one = ops.choose(p, [c for c in top if c.card_type in ("unit", "gear")], minimum=0, targeting=False, bind_at="resolution").value
if one:
    ops.banish(one)
    ops.modify_cost(one, discount, duration=THIS_PLAY)
    ops.play(one[0], p, origin=p.banish, destination=dest)
ops.recycle([c for c in top if c not in one])

```

REFLEXIVE:then you may do this须创建未来强化待处理链项，不能对play返回ChainItem调用empower



<a id="card-1073"></a>

## 1073

打出可消耗一友方buff为费，增益自身并重置

cost:Cost=消耗一个合法友方单位buff;binding:CostBinding=可选打出触发费用

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.buff([me])
    ops.ready([me])

```



<a id="card-1074"></a>

## 1074

p本回合曾获得XP则me+1且游走，之后花掉XP也不失效

gained:bool=p本回合有实际XP增加事件;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if gained:
    ops.modify_might([me], 1, duration=WHILE_CONDITION)
    ops.grant_keyword([me], GANKING, duration=WHILE_CONDITION)

```



<a id="card-1075"></a>

## 1075

迅捷选战场单位，战力≤3放逐否则回拥有者手

u:Unit=战场一单位;origin:Zone=u当前区域

```python

if u.might <= 3:
    ops.banish([u])
else:
    ops.transfer([u], origin, u.owner.hand)

```



<a id="card-1076"></a>

## 1076

反应无效法术

spell:ChainItem=所选法术

```python

ops.counter(spell)

```



<a id="card-1077"></a>

## 1077

打出可让非me战场战力≤3单位回拥有者手；Hidden文本未结构化亦保留

eligible:list[Unit]=非me且在战场战力≤3单位;origins:dict[Unit,Zone]=当前区域

```python

cards = ops.choose(p, eligible, minimum=0).value
if cards:
    u = cards[0]
    ops.transfer([u], origins[u], u.owner.hand)

```

DATA:EN Hidden未使用关键词方括号，结构化keywords为空但规则文本仍明确待命



<a id="card-1078"></a>

## 1078

此处全体单位游走含敌军

units:Selection[Unit]=here全部单位动态集合

```python

ops.grant_keyword(units, GANKING, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-1079"></a>

## 1079

有buff时自身额外+1，区别buff本体战力

buffed:bool=me拥有buff;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if buffed:
    ops.modify_might([me], 1, duration=WHILE_CONDITION)

```



<a id="card-1080"></a>

## 1080

Mind1装配，宿主据守打出2休眠金币

cost:Cost=Mind1;binding:CostBinding=Equip主动;u:Unit=p控制单位;gold:TokenTemplate=Gold;entry:EntryState=exhausted;host_player:Player=宿主据守效果控制者

```python

# 装配
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(me, u)
# 宿主据守
for i in range(2):
    ops.play(gold, host_player, origin=None, destination=host_player.base, entry=entry)

```

DATA:一组EN和全部SC缺少装备EFFECT，另一EN组有



<a id="card-1081"></a>

## 1081

每回合首次友军死亡抽1，不限p回合

 

```python

ops.draw(p, 1)

```

LANG:TC“你每回合”易误限自身回合，EN/SC为每个turn



<a id="card-1082"></a>

## 1082

自身活跃进场，固有坚守3

dest:Location/Zone=合法目的地;entry:EntryState=ready

```python

ops.play(me, p, origin=p.hand, destination=dest, entry=entry)

```



<a id="card-1083"></a>

## 1083

征服/据守XP1；pXP≥6时打出抽1

level:bool=pXP≥6

```python

# Hunt征服/据守
ops.gain_xp(p, 1)
# Level打出触发
if level:
    ops.draw(p, 1)

```



<a id="card-1084"></a>

## 1084

友军独自防守持续+2

units:Selection[Unit]=各战斗中属于友方且该方仅此一防守者的单位动态集合

```python

ops.modify_might(units, 2, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-1085"></a>

## 1085

pXP≥6时p单位+1；XP≥11时p单位活跃进场

units:Selection[Unit]=p控制单位动态集合;level6:bool=pXP≥6;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if level6:
    ops.modify_might(units, 1, duration=WHILE_CONDITION)

```

ENTRY:XP≥11的所有未来单位活跃进场缺全局entry修饰API



<a id="card-1086"></a>

## 1086

仅在战场主动Fury1横置，对一单位3伤

cost:Cost=Fury1横置me;binding:CostBinding=仅me位于战场可发动;u:Selection[Unit]=一单位

```python

paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.damage(u, 3)

```



<a id="card-1087"></a>

## 1087

p基地有至少2其他单位时自身活跃进场；壁垒保留

dest:Location/Zone=合法目的地;entry:EntryState=符合p基地其他单位≥2则ready否则默认

```python

ops.play(me, p, origin=p.hand, destination=dest, entry=entry)

```



<a id="card-1088"></a>

## 1088

经验记录提醒物，无独立行动

 

```python

# 提醒如何记录XP，不额外发放/花费经验

```

DATA:SC栏仍是英文提醒文字，不能宣称具备实际中文译文



<a id="card-1089"></a>

## 1089

进攻以技能为source，对此处一敌军造成等于me战力的伤害

u:Selection[Unit]=此处一敌方单位;n:IntExpr=me当前战力

```python

ops.damage(u, n)

```



<a id="card-1090"></a>

## 1090

每回合自身恰第三次移动触发得分1，不是每3次触发

 

```python

ops.gain_points(p, 1)

```



<a id="card-1091"></a>

## 1091

征服且分配过量≥3，打出2休眠金币

gold:TokenTemplate=Gold;entry:EntryState=exhausted

```python

for i in range(2):
    ops.play(gold, p, origin=None, destination=p.base, entry=entry)

```



<a id="card-1092"></a>

## 1092

百炼；征服此前未控制战场，伤害基地敌军等于me战力，采用勘误

g:Gear=p控制武装;cost:Cost=g装配费用减任意Power1最低0;binding:CostBinding=可选百炼费用;enemy:Selection[Unit]=基地一敌方单位;n:IntExpr=me当前战力

```python

# 百炼打出
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.attach(g, me)
# 征服此前uncontrolled战场
ops.damage(enemy, n)

```

LANG:早期open表述改uncontrolled，按勘误检查征服前控制状态



<a id="card-1093"></a>

## 1093

p打出Power费用≥2牌时抽1，非实际本次花费2条件

 

```python

ops.draw(p, 1)

```



<a id="card-1094"></a>

## 1094

进攻或防守，p此处另一单位本回合+3与壁垒

u:Selection[Unit]=非me且p控制同地单位

```python

ops.modify_might(u, 3, duration=THIS_TURN)
ops.grant_keyword(u, TANK, duration=THIS_TURN)

```



<a id="card-1095"></a>

## 1095

可选额外杀友方装备；打出若付则杀一装备

subjects:CostSelection=me本次打出;extra:CostChange=可选额外杀一友方装备;paid_extra:bool=实际支付;g:Selection[Gear]=一装备;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

# 费用
ops.modify_cost(subjects, extra, duration=THIS_PLAY)
# 打出触发
if paid_extra:
    ops.kill(g)

```



<a id="card-1096"></a>

## 1096

征服此处弃1再抽1

hand:list[Card]=p手牌

```python

ops.discard(p, 1)
ops.draw(p, 1)

```



<a id="card-1097"></a>

## 1097

打出让战场非me单位回拥有者手

u:Unit=非me且位于战场单位;origin:Zone=u当前区域

```python

ops.transfer([u], origin, u.owner.hand)

```



<a id="card-1098"></a>

## 1098

可选额外弃1；打出已付则打出0战力影分身

subjects:CostSelection=me本次打出;extra:CostChange=可选额外弃1;paid_extra:bool=实际支付;clone:TokenTemplate=0战力ShadowClone含进攻放逐废牌堆单位获得Assault4;dest:Location/Zone=合法目的地;THIS_PLAY:Duration=UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰

```python

# 费用
ops.modify_cost(subjects, extra, duration=THIS_PLAY)
# 打出触发
if paid_extra:
    ops.play(clone, p, origin=None, destination=dest)

```

DATA:对应ShadowClone本体战力字段为null，但本牌明确指定0，不按null猜零



<a id="card-1099"></a>

## 1099

征服打出0战力影分身基地；迅捷能量1Chaos1交换me与己方影分身位置

clone:TokenTemplate=0战力ShadowClone含固有攻击能力;cost:Cost=Energy1Chaos1;binding:CostBinding=Action主动费用

```python

# 征服触发
ops.play(clone, p, origin=None, destination=p.base)
# 主动费用片段
ops.pay(p, cost, binding=binding)

```

MOVE_BATCH:move一次仅一个目的地，无法保证me与ShadowClone同时换位

DATA:token本体战力null，本卡明确0可用但不改源数据



<a id="card-1100"></a>

## 1100

迅捷眩晕战场敌军，可移动友军至它战场

enemy:Unit=战场一敌方单位;b:Battlefield=该敌方单位地点绑定;friendly:Selection[Unit]=一友方单位;accept:bool=选择移动

```python

ops.stun([enemy])
if accept:
    ops.move(friendly, b)

```

LANG:TC多“此处的”友方限制，EN/SC无该来源限制



<a id="card-1101"></a>

## 1101

固有坚守1

defender:bool=me为防守方;WHILE_CONDITION:Duration=WHILE(该段入口中明确的持续条件)，依赖变化时重算

```python

if defender:
    ops.modify_might([me], 1, duration=WHILE_CONDITION)

```



<a id="card-1102"></a>

## 1102

打出牌抽2；抽至少一且有9张其他手牌时弃整手杀装备，对手得1分

hand:list[Card]=第二能力结算时p全部手牌;opponent:Player=所选对手

```python

# p打出牌触发
ops.draw(p, 2)
# 符合手牌数的抽牌触发
ops.discard(p, len(hand), cards=hand)
ops.kill([me])
ops.gain_points(opponent, 1)

```



<a id="card-1103"></a>

## 1103

按勘误友军将死改杀此装备，治愈横置召回该单位；Hidden保留

 

```python

# 缺少登记死亡前替代事件，不在死亡后执行治疗召回

```

REPLACE:没有用装备代死并取消单位死亡的替代接口

LANG:旧EN/SC next-time与勘误If不同，旧文缺heal，按勘误



<a id="card-1104"></a>

## 1104

能量1横置打出炸弹至战场；防守可杀友方装备使me本回合+2

cost:Cost=Energy1横置me;binding:CostBinding=炸弹主动费用;b:Battlefield=炸弹目的战场;bomb:TokenTemplate=Bomb含Deploy及死亡2伤杀其他同地己方Bomb;defend_cost:Cost=杀一友方装备;defend_binding:CostBinding=可选防守触发费用

```python

# 主动
paid = ops.pay(p, cost, binding=binding)
if paid.value is not None:
    ops.play(bomb, p, origin=None, destination=b)
# 防守触发
paid = ops.pay(p, defend_cost, binding=defend_binding)
if paid.value is not None:
    ops.modify_might([me], 2, duration=THIS_TURN)

```



<a id="card-1105"></a>

## 1105

打出炸弹至战场；友方装备技能额外伤害1

bomb:TokenTemplate=Bomb含Deploy及死亡能力;b:Battlefield=目的战场;events:DamageSelection=友方含队友装备的技能伤害;bonus:NumericChange=add1

```python

# 打出触发
ops.play(bomb, p, origin=None, destination=b)
# 持续入口
ops.modify_damage(events, bonus, duration=WHILE_SOURCE_PRESENT)

```



<a id="card-1106"></a>

## 1106

每回合一次me在战场时，可将即将打出单位token替代为它加一额外副本

 

```python

# 不在原token打出后另create伪装改写原打出过程

```

REPLACE:缺少带每回合一次额度的token打出替代事件；copy只改已有Permanent而不能替代pendingPlay

