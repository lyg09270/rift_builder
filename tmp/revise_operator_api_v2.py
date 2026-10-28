"""Revise only the operator reference. Not an effect engine."""
from pathlib import Path
import re,ast
p=Path('docs/basic-operators-api.md');s=p.read_text(encoding='utf-8')
s=s.replace('# 基本算子 API 参考','# 基本算子 API 参考 V2',1)
s=s.replace('采用 Python 风格签名。','版本：2026-10-28。共72个正式函数；[V1接口](basic-operators-api-v1.md)仅供迁移对照。\n\n采用 Python 风格签名。',1)
s=s.replace('| `Permanent` | 场上永久物，包含单位、装备等 |','| `Permanent` | 场上单位或装备；不包含符文、传奇、战场 |\n| `Orientable` | Unit、Gear、Rune、Legend；具有活跃／横置朝向的对象 |\n| `ObjectRef[T]` | 稳定实例引用；区域、类型、控制者在实际执行时重新检查，不以旧Python类当游戏类型 |')
s=s.replace('| `Ability` | 完整能力定义，包含类型、条件、费用和效果 |','| `Ability` | 完整能力：kind、timing、source、controller、trigger、condition、cost、choices及EffectProgram；非原始自然语言 |\n| `EffectProgram` | 只含本表登记调用及明确的if/else/for/先后节点；每个引用必须有本卡代码体，未知节点拒绝 |\n| `EventPattern` | 只用下方事件表的kind、stage、actor、source、objects、地点／领域及谓词过滤器 |\n| `UsageLimit` | count、reset（never/each_turn）、consume（on_accept/on_success/on_finalize）、optional、group；拒绝可选项不耗额度 |\n| `EventRewrite` | before、replacement、after三个显式EffectProgram；resume_original布尔值及闭集EventPatch；不是原始文本执行器 |\n| `MemoryKey` | Ability预先声明的带类型字段；按来源实例／构筑选择作用域保存；未声明键拒绝 |')
s=s.replace('| `SetupChoiceRef` | 对局前已保存的合法选项引用 |','| `SetupChoiceRef` | choose(bind_at="setup")与remember保存的合法预选引用；保留所属玩家／套牌与来源能力 |')
s=s.replace('| `NumericChange` | `add`、`multiply`、`set` 三者择一；值为明确的数值表达式 |','| `NumericChange` | `add`、`multiply`、`set` 三者择一；值为明确的数值表达式；MightChange另有同快照swap模式 |\n| `MightChange` | add(delta)、set(value,direction)、swap(other)三种互斥模式；set/swap结算时取差值快照 |')
s=s.replace('- `PERMANENT` 表示没有另设到期时间，仍遵守对象离场等默认清理。跨区域引用与最后已知信息只按明确授权使用。','- `PERMANENT` 表示没有另设到期时间，仍遵守对象离场等默认清理。跨区域引用与最后已知信息只按明确授权使用。\n- 动作的actor与来源、能力控制者、对象控制者、拥有者是四个独立字段。带actor的函数默认CONTROLLER（当前执行能力控制者）；显式actor仅改变行动归属，不偷偷转移能力控制权。\n- 函数参数中的查询表达式不能读取尚未授权的隐藏信息。条件、数量、对象、卡名和来源均不得以缺值默认0或任意原文占位。\n- 普通卡牌能力入口以完整Ability头绑定；关键词按下方闭集宏约定展开。只给出play(me)不能证明该卡所有固有效果已分解。\n- ChoiceBinding在定稿时保存目标、模式、目的地及费用选择；效果结算时重检合法性，不在结算中重新选择一个原本应于定稿选择的目标。\n- 同一个printings文本的空值不是零费用证明；模板明确给出的费用和战力优先按该模板字段使用，未给出值保持未知。')
# Replace complete definition sections. All examples remain API-conforming.
def section(name,title,signature,description,example=None):
 global s
 block=f'### `{name}` {title}\n\n```python\n{signature}\n```\n\n{description}\n'
 if example:block+='\n```python\n'+example+'\n```\n'
 pattern=r'### `'+re.escape(name)+r'`[^\n]*\n.*?(?=\n### |\n## |\Z)'
 s,n=re.subn(pattern,lambda m:block,s,flags=re.S)
 if n!=1:raise ValueError((name,n))
def remove(name):
 global s
 s,n=re.subn(r'### `'+name+r'`[^\n]*\n.*?(?=\n### |\n## |\Z)','',s,flags=re.S)
 if n!=1:raise ValueError(name)
section('reveal','展示或依次展示',
'reveal(cards: Selection[Card] | None = None, *, actor: Player = CONTROLLER,\n       viewers: Selection[Player] = ALL_PLAYERS, duration: Duration = UNTIL_EFFECT_END,\n       zone: Zone | None = None, count: IntExpr | All | None = None,\n       until: Predicate | None = None, include_match: bool = True) -> Result[RevealReceipt]',
'- 显式cards与zone模式互斥。zone模式逐张授权并展示；until只能检查已展示对象，命中即停，不预先窥视停止位置。count限制最多张数；耗尽时不凭空制造对象。\n- 返回cards、matched、公开范围及实际信息事件；普通展示不改区域。as-revealed内联通过on_event(..., timing="inline")进入。\n- 显式actor保存谁展示，viewers只说明谁知道，不替代行动玩家。',
'ops.reveal(cards, actor=opponent)')
section('choose','选择对象',
'choose(player: Player, candidates: Selection[T], *, minimum: IntExpr = 1,\n       maximum: IntExpr = 1, targeting: bool = True, bind_at: str = "finalization",\n       shortage: str = "as_many_as_possible", link: Link | None = None) -> Result[list[T]]',
'- bind_at为setup、trigger、finalization或resolution；必须位于真正对应阶段，不准追溯。setup返回可被remember保存的构筑预选，数量／异名条件明确校验。\n- 效果候选少于minimum时，as_many_as_possible强制选尽现有候选；足够时仍必须满足minimum，不变成可任意少选。成本选择必须shortage="fail"。\n- targeting区分正式目标与非目标挑选；返回实际绑定对象。关联未来读取必须显式link或remember。')
section('declare','宣告值或选择合法模式',
'declare(player: Player, options: list[T], *, minimum: int = 1, maximum: int = 1,\n        kind: str = "value", bind_at: str = "resolution", link: Link | None = None) -> Result[list[T]]',
'- kind仅value、name、type、domain、tag、mode；options必须是规则允许的有限值或合法名称注册表。模式不是目标选择。\n- bind_at同choose，且必须匹配实际能力时点；返回所选值。需要跨回合／多次技能读取时用remember，不隐含保存到所有同名卡。')
section('transfer','区域转移',
'''transfer(cards: Selection[Card], source: Zone | ZoneMap, destination: Zone | ZoneMap, *,
         order: str = "preserve", actor: Player = CONTROLLER,
         identity: ActionIdentity = ZONE_TRANSFER) -> Result[list[Card]]''',
'- ZoneMap按实例给出来源／目的区域，所有对象属于同一指令批次；开始时读取来源快照，统一提交再处理清理与触发。允许分别回各拥有者手牌。\n- identity仅ZONE_TRANSFER或BURN；后者只允许规则441.1授权的牌堆顶部入废，保留对应事件与被替代部分。不得选择DRAW/DISCARD/KILL等来绕过独立动作约束。\n- 不自动生成抽牌、弃置、摧毁、放逐或回收事件。显式BURN请求与真实来源不符时失败，不替换为任意牌。')
section('move','移动',
'''move(objects: Selection[Permanent], destination: Location | LocationMap, *,
     origin: Location | LocationMap | None = None, simultaneous: bool = True,
     actor: Player = CONTROLLER, join: EventRef | None = None) -> Result[list[Permanent]]''',
'- LocationMap按实例绑定地点，支持同时交换位置、分别回不同控制者基地；统一读取出发快照并提交，不能在第一名移动后提前检查另一名的战斗。\n- join只能加入仍待执行的原move批次。友军“随之移动”依其规则窗口关联原批次，不能加入已提交的移动；其他移动不伪造相同行动者。\n- 移动不自带普通移动横置成本，不改变控制者；只有实际变位者产生move事件。')
section('recall','召回','recall(objects: Selection[Permanent], *, actor: Player = CONTROLLER) -> Result[list[Permanent]]',
'- 各对象送回其控制者对应基地，同批提交；不算move，不被move限制阻止，不回手。返回实际完成召回的对象。')
section('recycle','回收','recycle(cards: Selection[Card], *, actor: Player = CONTROLLER) -> Result[list[Card]]',
'- 同一指令可跨玩家、跨区域；回到各拥有者对应牌堆底。主牌堆同时回收多张的牌底次序随机，符文由各自拥有者排序；不洗整个牌堆。\n- 保留执行玩家与各对象实际结果；不会因选择者或拥有者不同而改写actor。')
section('banish','放逐','banish(cards: Selection[Card | ChainItem], *, link: Link | None = None,\n       actor: Player = CONTROLLER) -> Result[list[Card]]',
'- 接受场上／其他区域卡牌或明确链项，链项通过其card实例关联放逐；不能把能力链项当卡牌放逐。\n- 不算摧毁或弃置；保存来源实例link与实际card身份。链项关联卡离链时按规则处理剩余执行体，不把放逐误作counter。')
section('burn','燃烧','burn(player: Player, count: IntExpr, *, cards: Selection[Card] | None = None) -> Result[list[Card]]',
'- cards=None正常从顶部燃烧count并在不足时按耗尽流程继续。指定cards仅作用于已授权的明确剩余顶部牌，不补烧不在原集合的新牌；count必须与明确对象数量相符。\n- 返回实际燃烧对象，保留Burn事件身份。非顶部来源不合法，不能把任意废牌转移伪装燃烧。')
section('create','生成卡牌、传奇或战场',
'''create(template: CardTemplate | CopyTemplate | SetupChoiceRef, count: IntExpr, *,
       owner: Player, controller: Player | None, destination: Zone | Location,
       state: EntryState = DEFAULT_ENTRY, duration: Duration = PERMANENT,
       link: Link | None = None) -> Result[CreateReceipt]''',
'- count要求非负；新实例各有独立ID。战场controller必须None；单位、装备、符文、传奇初始控制者须为owner，除非来源明确授权其他情况。\n- SetupChoiceRef须校验来源预选、不同名、剩余合法项和是否已在场；传奇从该预选产生时返回legends，并以link关联来源实例。duration到期按该创建授权的回收／移除约定清理，不擅自kill传奇。\n- CreateReceipt含cards、units、gear、runes、legends、battlefields类型视图。生成不是打出，要求play的token用play(TokenTemplate,...origin=None)。')
remove('add_legend')
section('replace_battlefield','替换或恢复战场',
'''replace_battlefield(target: Battlefield, template: CardTemplate | None = None, *,
                    mode: str = "replace", link: Link) -> Result[Battlefield | None]''',
'- replace要求template；保存原战场，继承原有关状态／效果／引用，原牌暂存不制造普通banish事件。\n- restore要求template=None；用同次link恢复既存原牌，无可恢复对象返回None。两种模式均继承当前相关状态，不能重找同名新牌。')
remove('restore_battlefield')
for name,title,desc in [('ready','活跃','从横置到活跃'),('exhaust','横置','从活跃到横置')]:
 section(name,title,f'{name}(objects: Selection[Orientable], *, simultaneous: bool = True,\n        actor: Player = CONTROLLER) -> Result[list[Orientable]]',
 f'- 接受Unit/Gear/Rune/Legend；不再错误要求符文或传奇是Permanent。仅实际{desc}者返回且产生事件。\n- 已处于目标朝向不重复制造事件。入场朝向使用play.entry或modify_entry，不以本动作代替。')
section('spend_buff','消耗增益',
'''spend_buff(player: Player, units: Selection[Unit], *,
           count_each: IntExpr | dict[Unit, int] = 1) -> Result[CounterReceipt]''',
'- count_each可为统一数量或按实例数量，所有消耗组成一个指令批次；返回各对象实际消耗数和总计。\n- player须控制相应单位；友方含队友不代表能花队友计数物。作为成本时必须完整支付，不能用少消耗冒充已付。')
section('modify_might','调整、设至或交换战力',
'''modify_might(units: Selection[Unit], delta: IntExpr | None = None, *,
             change: MightChange | None = None, duration: Duration,
             floor: IntExpr | None = None, ceiling: IntExpr | None = None) -> Result[list[Modifier]]''',
'- delta是add简写，与change互斥。MightChange.add为有符号增减；set(value,direction)使用本次执行战力差快照，direction为both/increase_only/decrease_only；swap(other)要求units恰一名，与other共享同一快照并同批登记差值。\n- floor/ceiling只限制本修饰；set/swap不是持续强制最终战力等于某数，不移走装备或增益，也不改变基础战力层。\n- 同指令多个不同修饰用batch；不以总数值相同冒充装备贡献层相同。',
'ops.modify_might([u], change=MightChange.set(5, direction="increase_only"), duration=THIS_TURN)')
remove('set_might');remove('swap_might')
section('damage','造成伤害',
'''damage(units: Selection[Unit], amount: IntExpr, *, source: Source = SOURCE,
       mode: str = "each", allocation: dict[Unit, int] | None = None,
       use_all: bool = True, simultaneous: bool = True,
       actor: Player = CONTROLLER) -> Result[DamageReceipt]''',
'- each为每目标同一数值；split为总池，必须给出合法分配。Bonus对each每个目标分别应用，对split只增加总池；不能用split表达不等值的独立逐目标伤害。\n- 不同source或不同数值的同指令伤害用batch(SIMULTANEOUS)，在共享伤前快照取Might，所有伤害提交前不致死清理。\n- “Deal X for each Y”按418.8为一个数值X×Y的实例，非Y次循环。伤害不扣战力；0不产生实际伤害事件。\n- 返回每目标分配、修饰后、实际、过量及来源；死亡随后由规则清理产生，不由返回伤害值直接猜测。')
section('prevent_damage','预防伤害',
'''prevent_damage(units: Selection[Unit], amount: IntExpr | Infinity, *,
               source_filter: Predicate = ANY_SOURCE, duration: Duration,
               limit: UsageLimit | None = None) -> Result[list[Modifier]]''',
'- 每目标amount额度按实际预防量扣减；INFINITY预防所有匹配伤害。limit可限定下一伤害事件且每目标独立消耗，不把“下一次”变为全回合所有次。\n- limit的计数单位必须damage_event或instruction_batch，按卡面写明；同次分配多个目标保留原实例分组，不无效化整项能力。')
section('kill','摧毁',
'''kill(objects: Selection[Permanent], *, source: Source = SOURCE,
     simultaneous: bool = True, actor: Player = CONTROLLER) -> Result[list[Card]]''',
'- 先处理将死替代；返回真正因本动作死亡的card，保存伤前／死亡前信息和行动者。\n- 同批杀多个对象或多位玩家分别杀各自对象时用batch并各传actor；死亡被召回替代则不返回已死、不触发死亡能力。')
section('set_types','修改类型集合',
'''set_types(objects: Selection[Permanent | Card], types: set[CardType], *,
          mode: str = "replace", duration: Duration) -> Result[TypeChangeReceipt]''',
'- mode为add/remove/replace。返回modifiers及按当前实际类型生成的units/gear等视图；类型变化后同ID引用按新类型重检。\n- Gear增加UNIT后可用receipt.units调用set_base_might，不在类型未改变时强制转型；集合类型不丢原装备属性。')
section('modify_cost','调整费用',
'''modify_cost(subjects: CostSelection, change: CostChange, *, duration: Duration,
            uses: int | None = None, limit: UsageLimit | None = None,
            link: Link | None = None) -> Result[Modifier]''',
'- uses为UsageLimit(count=uses,reset="never",consume="on_finalize")简写，与limit互斥。可选每回合一次优惠必须limit指定each_turn和optional=True；拒绝不耗次数。\n- CostChange字段闭集：energy_delta、power_discount、power_add、base_replace、ignore_base、ignore_energy、additional_actions。可选附加成本由ChoiceBinding选定，完整支付后形成PaymentReceipt。\n- 目标费用、替代基础费、额外费用与指令内付款分开；不改印刷费用，不返还已付资源。Power折扣按规则分配领域，不擅自优先扣某一领域。\n- link保存本次费用选择与目的地／入场／后续效果的关联；可用PlayConstraint要求付了某附加费才可/必须去特定地点，不能只grant_permission而漏掉强制目的地。')
section('gain_xp','经验变化',
'''change_xp(player: Player, amount: IntExpr, *, mode: str = "gain") -> Result[int]''',
'- gain增加XP并发获得事件，spend消耗XP并发消耗事件；amount均非负，结果为实际变化量。\n- spend不足失败；作为成本由pay检查整套成本，不能先扣一部分再执行相依效果。等级依赖随实际XP变化重算。')
s=s.replace('### `gain_xp` 经验变化','### `change_xp` 经验变化')
remove('spend_xp')
section('modify_rule','修改明确规则项',
'''modify_rule(key: RuleKey, scope: RuleScope, change: RuleChange, *,
            duration: Duration) -> Result[Modifier]''',
'''- 仅接受下表注册键及其匹配结构；不接受任意自然语言、任意键或未解析效果。

| RuleKey | 允许字段 |
| --- | --- |
| VICTORY_THRESHOLD | delta/set |
| HIDDEN_CAPACITY | 玩家／战场与delta |
| STARTING_BATTLEFIELD_ELIGIBILITY | eligible布尔 |
| COMBAT_DAMAGE_ORDER | first/normal/last；assignment_player限定；ignore_keywords仅可Tank/Backline且只对指定分配者生效 |
| LETHAL_DAMAGE_POLICY | sources与positive_damage_is_lethal |
| EMPOWER_LIMIT / BUFF_LIMIT | 非负整数或INFINITY |
| CHANNEL_PHASE_COUNT | 基础召出数量set，不影响其他来源 |
| DECK_NAME_LIMIT | 具名卡的上限set |
| GEAR_RECALL_POLICY | 单位／非单位装备的清理召回条件 |

- ignore_keywords不抹除单位持有的关键词，只改变该分配者适用的承伤顺序。''')
section('execute_effect','执行明确能力效果',
'''execute_effect(source: Source, ability: AbilityRef, *, count: IntExpr = 1,
               choices: ChoiceBinding | None = None,
               mode: str = "pending", link: Link | None = None) -> Result[list[ChainItem]]''',
'- pending创建相应已知效果的待处理项，不伪造原事件；可从LKI引用已离场来源的明确能力。\n- repeat_inline只用于Repeat宏已经完成多遍选择定稿后的同链项重复原效果，不建新法术，不额外产生spell-play事件；choices须保存每遍独立的完整选择。\n- 不接受未知文字，不能用execute_effect(raw_text)兜底。')
section('play','打出',
'''play(card: Card | TokenTemplate | CopyTemplate, player: Player, *, origin: Zone | None,
     destination: Zone | Location, cost_policy: CostPolicy = NORMAL_COST,
     permission: PlayPermission | None = None, choices: ChoiceBinding | None = None,
     entry: EntryState | None = None, link: Link | None = None) -> Result[PlayReceipt]''',
'''- 现有卡必须真实origin；新token/其副本用模板且origin=None，由本流程在链上创建，不先create在场上。免费只忽略被指定的费用，不绕过合法目标和地点。
- 执行定稿的完整阶段：建立待处理项→as-play内联钩子/ShowOff/命名→模式和目标与费用选择→计算与支付全部适用费用→成为已定稿链项→永久物入场及打出触发；各钩子严格在所属阶段运行。
- PlayReceipt为item、card、choices、payment、entry、link、是否已定稿等。item是ChainItem；不是已落地Unit。play返回后不能据此直接ready/attach新单位，应由queue_effect或on_event关联card在合法后续时点执行。
- ChainItem.card稳定标识其实体。只有卡面授权重打正在执行的自身时才允许origin=该链区；新的play拥有独立item和选择／费用记录，link可跨重打保存本能力声明的计数快照，不能擅自copy当前法术。
- “支付X以打出该牌”不自动解释为免费。触发基础费按383.3.b在触发定稿时支付；后续play仍支付其适用基础费，除非文本／规则明确给出替代基础费或忽略政策。
- Repeat宏：可选附加费定稿决定是否支付，每一遍的模式/目标在当次法术定稿中分别保存；原链项结算按顺序执行多遍effect，未重复play事件。Flow宏：废牌堆来源权限＋替代基础费；对该次已定稿item建立离链放逐替代，包括被counter，明确由自身指令离链时除外。宏必须由KeywordSpec的闭集结构描述，不能读原文临时猜测。
- 入场entry由当前打出ChoiceBinding、付款回执和ShowOff快照求值，不能在已知付款之前伪造成功回执。''')
# Additional narrowly typed structural operators.
extra=r'''
## 11. 批次、事件及关联

### `batch` 同指令批次

```python
batch(*, policy: BatchPolicy = SIMULTANEOUS) -> BatchScope
```

- 作为with上下文使用。SIMULTANEOUS在开始时冻结共同输入快照，内部登记的动作共同提交，提交后才处理清理和普通触发；返回的Result提交前不可读取。不同来源、行动者、目的地仍分别记录。
- 一批只可放同一卡面指令中应同时发生的动作；不能跨“然后”吞并多个顺序步骤。玩家的目标／模式选择在提交前各自合法绑定，隐藏信息不提前暴露。
- PLAYER_PROCEDURE用于规则指定的跨玩家同一指令：按规定玩家次序各自完成选择与该阶段动作，之后才进入下一条指令；不把“每人弃后每人抽”写成每人弃完立即抽。
- 不能将on_event、replace_event、play整段任意嵌入SIMULTANEOUS来改变链时序；token批量打出依正常play流程。

```python
with ops.batch(policy=SIMULTANEOUS):
    ops.damage([a], b.might, source=b)
    ops.damage([b], a.might, source=a)
```

### `on_event` 登记触发、延迟或内联能力

```python
on_event(events: EventPattern, ability: Ability, *, duration: Duration,
         timing: str = "triggered", limit: UsageLimit | None = None,
         link: Link | None = None) -> Result[Modifier]
```

- triggered在匹配事件后创建待处理能力项，按规则定稿；不是现在执行。duration与usage独立，新建回合末／下个主阶段能力在其指定时点才执行。
- inline只允许下方表中开放的as-play、before-finalize、as-look、as-reveal、as-attach等阶段；嵌入原动作过程，不另开反应窗口。阶段不开放或动作已提交则拒绝。
- 事件引用提供actor、source、card/item、objects、原地点、伤前战力、支付回执和关联快照；只能读取该阶段真实存在的信息。
- bind-next用EventPattern(kind=PLAY,matching=FIRST,filter=明确条件)、inline及UsageLimit(1)绑定真实下一个对象；不提前猜手牌，消费点按被接受事件指定。
- ability必须有完整代码体，源离场是否仍生效由明确duration决定，不自动随登记者离场取消所有延迟能力。

### `replace_event` 登记待发生事件替代

```python
replace_event(events: EventPattern, rewrite: EventRewrite, *, duration: Duration,
              optional: bool = False, limit: UsageLimit | None = None,
              link: Link | None = None) -> Result[Modifier]
```

- 匹配待发生事件，在提交前适用；rewrite明确保留／取消原事件及替代动作。replacement已成功适用才取消原事件；可选付款不成功则原事件照常发生。
- before在原动作前执行（如展示前看顶牌）；resume_original为True时重新按获授权来源求本来要展示的牌，不复用越权预读列表。after在原动作同过程指定位置执行，不能代替需要上链的then-do-this。
- 自身替代不会无限重新匹配自己的替代展开；仍按官方多替代选择及适用规则处理。每次事件的消费额度与事件身份单独保存。
- EventPatch字段闭集如下；其他变化须用已经分解的EffectProgram，不能填自然语言patch。

| 原事件 | 允许Patch |
| --- | --- |
| PLAY | entry、destination、额外同模板token数量（只限授权新token） |
| CHANNEL | 每枚符文的entry序列，包含原数量/朝向和明确追加枚数 |
| REVEAL/LOOK | 保留原来源/数量，在before结束后重新求值对象 |
| LEAVE_CHAIN | destination、identity、只匹配指定item且排除自身指令离链 |
| DIE、ZONE_TRANSFER、COMBAT_TIE | 取消原事件并执行明确替代program；不得把死亡后治疗当替代 |

### `queue_effect` 创建自反待处理项

```python
queue_effect(source: Source, ability: Ability, *, link: Link | None = None,
             choices: ChoiceBinding | None = None) -> Result[ChainItem]
```

- 当前效果执行到“then do this / if you do, do this”对应点时调用，创建一个新的pending能力项；不马上执行能力体。
- 保留原来源与明确关联实例，定稿时重新选择其允许的目标／支付其费用。不能把play返回的ChainItem传给只接受Unit的动作。
- 每个实际满足条件的事件分别建项；原指令可选不执行时不创建。普通“然后”不自动拆新链项。

### `modify_entry` 修改未来入场状态

```python
modify_entry(subjects: EntrySelection, state: EntryState, *, duration: Duration,
             limit: UsageLimit | None = None, link: Link | None = None) -> Result[Modifier]
```

- subjects含控制者、类型、token身份、来源和目的地过滤；只改匹配对象入场朝向／明确授权初态，不发ready/exhaust状态变化事件。
- 所有未来匹配项或next/each-turn额度须明确；同次批量进入按该限定实际计数。原文“enter”不能只限“play”。

### `modify_equipment_bonus` 修改武装战力贡献

```python
modify_equipment_bonus(gear: Selection[Gear], change: NumericChange, *,
                       duration: Duration) -> Result[list[Modifier]]
```

- 只改每件武装赋予宿主的装备贡献层；保留装备归属、宿主、战力贡献来源和动态重算。不以给宿主同数值普通战力修饰代替。

### `modify_trigger_events` 扩展已有能力的触发类别

```python
modify_trigger_events(abilities: AbilitySelection, add: set[EventKind], *,
                      duration: Duration) -> Result[list[Modifier]]
```

- add只允许HOLD/CONQUER两类的明确互增；来源与能力体不变，相同事件不重复登记。不产生新的play效果，也不调用原能力一次当作持续扩展。

### `remember` 保存带类型的关联选择

```python
remember(source: Card | CardTemplate | AbilityRef, key: MemoryKey, value: T, *,
         duration: Duration, link: Link | None = None) -> Result[MemoryRef[T]]
```

- key必须由该Ability预先声明schema及作用域；value必须符合schema。保存如命名标签、命名法术、构筑额外传奇集合或指定快照，不接收任意文本作可执行效果。
- 实例作用域不按同名卡共享；构筑预选明确所属玩家／套牌。区分保存引用、执行时属性与当时快照；离场清理按duration及规则授权，不擅自跨区域保留临时对象状态。

## 12. 闭集事件与关键词约定

| EventKind | 开放的阶段及数据 |
| --- | --- |
| PLAY | as_play、before_finalize、finalized、entered；card/item、actor、choices、payment、entry、location |
| LOOK / REVEAL | before、as_each、complete；真实已授权牌及所看牌堆，不提供未来牌序 |
| ATTACH | as_attach、complete；gear/host/previous_host |
| MOVE | before、complete；各对象原地点与目的地、actor、原批次ID |
| DIE / LEAVE_BOARD / ZONE_TRANSFER | before、complete；对象、LKI、源/目的区域、动作身份 |
| DAMAGE | before、complete；来源、目标、数量、实例和分配批次 |
| TURN_PHASE | start/end及具体玩家、阶段、回合序号 |
| HOLD / CONQUER / ATTACK / DEFEND / COMBAT_START / COMBAT_WIN / COMBAT_TIE | 对应规则事件，含玩家、地点、参战单位及过量分配快照 |
| CHOOSE / DRAW / RECYCLE / BURN / CHANNEL / BUFF / EMPOWER / EXHAUST / READY / XP | before/complete及具体actor、对象、实际完成数量；普通选择不假冒target |
| LEAVE_CHAIN | before/complete；item、card、原因（执行/无效/外部动作）、自身指令离链标志 |

| 关键词 | 必须采用的内部结构 |
| --- | --- |
| Action / Reaction / Ambush | 明确时机、优先权和地点权限；反应不允许在所有无优先权时刻任意插入 |
| Assault / Shield / Ganking / Tank / Backline / Deflect | 角色条件数值／移动权限／承伤次序／目标附加费用；保留关键词身份与其叠加规则 |
| Equip / Weaponmaster / Quick-Draw | 主动费用后attach／打出触发折扣Equip／Reaction＋打出附着；装配不是免费attach的别名 |
| Accelerate | 选择附加Energy1及自身领域Power1，完整支付后ready入场，不产生ready事件 |
| Hidden | hide完整付费与战场盖放许可，容量与失控限制；下一回合按规则获Reaction且忽略基础费用，仍限合法地点/目标 |
| Predict / Vision / Show Off | 私密洞察／打出触发洞察／定稿亮出及快照，不用公开展示替代私密查看 |
| Repeat | 附加费用、同一链项每遍分别定稿选择、依序执行原effect；通过execute_effect(...mode="repeat_inline")，不重复play |
| Flow | 废牌堆打出来源许可、替代基础费用、该item的离链放逐替代；被counter也适用，自身执行指令离链例外 |
| Deathknell / Temporary / Deploy | 死亡触发／控制者开始阶段得分前默认清理／部署地点限制、清理召回例外及对手据守摧毁 |
| Empower / Empowered / Level / Mighty / Legion | 强化主动与状态条件／XP阈值／战力≥5／本回合打过其他牌的条件；Legion不是buff动作 |
| Hunt / Disarm / Unique / Buff / Stun / Burn / Add | 征服据守XP／进攻敌军减战力／同名构筑上限／具名动作；数值与费用严格读取卡面 |

固有关键词由卡牌基础能力定义提供；本卡代码中的宏展开取代该宏，不能再额外grant同一个固有关键词造成重复叠加。宏引用必须保留KeywordSpec与来源实例；未定义关键词不得仅凭名字默认支持。

## 13. V1迁移

| V1入口 | V2正式调用 |
| --- | --- |
| gain_xp / spend_xp | change_xp(mode="gain" / "spend") |
| set_might / swap_might | modify_might(change=MightChange.set / swap) |
| add_legend | create(SetupChoiceRef,1,...duration/link)并取receipt.legends |
| restore_battlefield | replace_battlefield(mode="restore",link=...) |
| 仅改变名额的uses | 保留简写；可选或每回合复位用UsageLimit |

这些旧名不属于V2正式API，不在新调用中保留别名。predict/show_off/copy_text等有事件、信息或复制层语义的封装继续保留；不能因终点相似而删除。
'''
s=s.rstrip()+'\n\n'+extra.strip()+'\n'
# Function count must reflect only definitions, not examples.
defs=[]
for b in re.findall(r'```python\n(.*?)\n```',s,re.S):
 if re.match(r'[a-z_]+\(',b):
  fn=ast.parse('def '+b+':\n pass').body[0];defs.append(fn.name)
if len(defs)!=72 or len(set(defs))!=72:raise ValueError((len(defs),defs))
p.write_text(s,encoding='utf-8');print('V2 canonical functions:',len(defs))
