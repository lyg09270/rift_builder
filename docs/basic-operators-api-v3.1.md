# 基本算子 API 参考 V3.1

版本：2026-10-28，V3.1。共71个正式函数；[V3接口](basic-operators-api-v3.md)和[V2.1接口](basic-operators-api-v2.1.md)仅供迁移对照。函数数量不等于不同游戏动作的数量。

采用 Python 风格签名。`ops` 绑定当前执行上下文；下列函数是接口定义，参数中的对象均指具体实例。

## 公共类型

| 类型 | 定义 |
| --- | --- |
| `Player` | 玩家引用 |
| `Card` | 卡牌实例引用；保存拥有者，与控制者分开 |
| `Permanent` | 场上单位或装备；不包含符文、传奇、战场 |
| `Orientable` | Unit、Gear、Rune、Legend；具有活跃／横置朝向的对象 |
| `ObjectRef[T]` | 稳定实例引用；区域、类型、控制者在实际执行时重新检查，不以旧Python类当游戏类型 |
| `Unit` / `Gear` / `Rune` | 单位／装备／符文实例 |
| `Battlefield` / `Legend` | 战场／传奇实例 |
| `ChainItem` | 链上的法术或能力实例 |
| `Source` | 效果来源；默认 `SOURCE`，即当前能力或法术 |
| `Zone` | 具体玩家的手牌、牌堆、废牌堆、放逐区、链、传奇区等区域 |
| `Location` | 场上具体基地或战场 |
| `Selection[T]` | 已绑定对象集合或待求值选择器；保存筛选条件、是否目标和绑定时点 |
| `IntExpr` | 整数或整数表达式，支持计数、求和、差值、最大值、倍数、属性引用 |
| `Predicate` | 明确的布尔条件表达式 |
| `Duration` | `PERMANENT`、`THIS_TURN`、`THIS_COMBAT`、`WHILE_SOURCE_PRESENT`、`UNTIL(event)`、`WHILE(condition)`；`UNTIL_EFFECT_END` 为当前效果结束的简写 |
| `Modifier` | 已登记的持续／限次修饰引用；用end_modifier结束指定修饰，用link关联具体来源实例 |
| `Link` | 同一来源能力建立的实例关联，不按卡名共享 |
| `Ability` | 完整能力：kind、timing、source、controller、trigger、condition、cost、choices及EffectProgram；非原始自然语言 |
| `EffectProgram` | 只含本表登记调用及明确的if/else/for/先后节点；每个引用必须有本卡代码体，未知节点拒绝 |
| `EventPattern` | kind、stage、actor、source、objects、filter、granularity、matching及可选transition；取值与匹配语义见第12节，不接受未登记事件 |
| `EventRef` | 阶段有效的事件引用；event_id、action_id、batch_id、actor、source及实际对象；区域变化另有transition_id，集合事件保留各对象对应的transition_id |
| `StateTransitionSpec` | 明确状态字段、比较关系、阈值及转换方向；字段闭集与重算边界见第12节 |
| `UsageLimit` | count、reset（never/each_turn）、consume（on_accept/on_success/on_finalize）、optional、group；拒绝可选项不耗额度 |
| `EventRewrite` | before、replacement、after三个显式EffectProgram；resume_original布尔值及闭集EventPatch；可选cost/payer/CostBinding组成PaymentGate，完整支付才接受替代；不是原始文本执行器 |
| `MemoryKey` | Ability预先声明的带类型字段；按来源实例／构筑选择作用域保存；未声明键拒绝 |
| `Result[T]` | `value: T \| None`、`changed: bool`、`events: list[EventRef]`；单对象动作未成功时可返回 `None` |

| 复合参数 | 定义 |
| --- | --- |
| `CardTemplate` / `TokenTemplate` | 有明确属性与能力的卡牌／衍生物定义，不是场上实例 |
| `CopyTemplate` | 来源实例、可复制特征、取值时点构成的新实例模板 |
| `CopyTraits` | 允许复制的字段集合，按复制规则检查 |
| `EntryState` | 入场朝向及明确授权的初始状态；`DEFAULT_ENTRY` 使用该对象类型的默认规则 |
| `ResourceBundle` | `energy` 数量与分领域 `power` 数量；资源数量不得为负 |
| `Cost` | Energy要求、Power领域选择组、具名动作费用及组合关系 |
| `CostPolicy` | `NORMAL_COST`、替代基础费用、`IGNORE_BASE_COST`、忽略Energy、忽略全部费用 |
| `CostChange` | 明确的费用分量增减、基础费用替代、额外成本或忽略政策 |
| `NumericChange` | `add`、`multiply`、`set` 三者择一；值为明确的数值表达式；MightChange另有同快照swap模式 |
| `MightChange` | add(delta)、set(value,direction)、swap(other)三种互斥模式；set/swap结算时取差值快照 |
| `ResourceChange` | 对特定产费动作的Energy／Power数量或领域修改 |
| `ChoiceBinding` | 决策者、目标、模式、其他选择及其绑定时点 |
| `SetupChoiceRef` | choose(bind_at="setup")与remember保存的合法预选引用；保留所属玩家／套牌与来源能力 |
| `PermissionSpec` / `RestrictionSpec` | 动作标识与时机、区域、目的地、对象、例外等明确约束 |
| `HidePermission` / `PlayPermission` | 对盖放／打出动作的具体授权，不自动绕过未覆盖限制 |
| `PlayConstraint` | 正向打出位置要求：destinations、when、grant_destination、payment_binding；按第9节仲裁，不等于禁止其他位置 |
| `ShowOffRequirement` | 亮出数量、候选属性、差异性约束及相依引用 |

通用约定：

- `IntExpr` 在指定绑定时点求值；持续表达式在其依赖变化时重算，明确的快照值不重算。
- 数量、资源、伤害分配量要求非负；负战力修饰等仅在允许带符号的参数中使用。
- 普通效果尽可能执行；成本由费用流程检查并完整支付。动作未发生或未成功登记修饰时返回 `changed=False`，不伪造成功事件。
- 参数类型错误、来源数据缺失、未知规则项或未解析文本显式报错；未知数值不按零处理。
- 返回集合包含实际完成该动作的对象；被替代或失败的部分通过事件记录区分。修饰函数返回的 `Modifier` 表示登记成功，不等于被修饰事件已经发生。
- `PERMANENT` 表示没有另设到期时间，仍遵守对象离场等默认清理。跨区域引用与最后已知信息只按明确授权使用。
- 动作的actor与来源、能力控制者、对象控制者、拥有者是四个独立字段。带actor的函数默认CONTROLLER（当前执行能力控制者）；显式actor仅改变行动归属，不偷偷转移能力控制权。
- 函数参数中的查询表达式不能读取尚未授权的隐藏信息。条件、数量、对象、卡名和来源均不得以缺值默认0或任意原文占位。
- 普通卡牌能力入口以完整Ability头绑定；关键词按下方闭集宏约定展开。只给出play(me)不能证明该卡所有固有效果已分解。
- ChoiceBinding在定稿时保存目标、模式、目的地及费用选择；效果结算时重检合法性，不在结算中重新选择一个原本应于定稿选择的目标。
- 清理严格遵守规则319–323：正在结算链项时不能执行Cleanup，只登记Outstanding任务；单个动作或batch提交也不能强行提前清理。伤害的实际致死关联在规则允许的清理／结果阶段确认，不在damage返回时凭战力比较预判。
- 同一个printings文本的空值不是零费用证明；模板明确给出的费用和战力优先按该模板字段使用，未给出值保持未知。

## 1. 信息与选择

### `draw` 抽牌

```python
draw(player: Player, count: IntExpr = 1, *, cards: Selection[Card] | None = None) -> Result[list[Card]]
```

- `player`：执行抽牌的玩家。`count`：数量。`cards=None`：从主牌堆顶部抽取；指定牌时必须有相应抽取授权，且数量与 `count` 一致。
- 返回：实际抽取的卡牌，顺序与抽取顺序一致。
- 语义：保留抽牌事件；主牌堆不足按耗尽流程处理，不等于普通回手。

```python
ops.draw(player, 2)
```

### `look` 查看

```python
look(player: Player, zone: Zone, count: IntExpr | All, *, position: str = "top") -> Result[list[Card]]
```

- `position`：`top` 或 `bottom`；`count=ALL` 表示查看整个区域。
- 返回：按区域次序排列的已查看牌；只授予 `player` 相应信息。
- 语义：不公开、不转移区域。数量不足时查看现有牌，不触发耗尽。

```python
ops.look(player, player.main_deck, 3)
```

### `reveal` 展示或依次展示

```python
reveal(cards: Selection[Card] | None = None, *, actor: Player = CONTROLLER,
       viewers: Selection[Player] = ALL_PLAYERS, duration: Duration = UNTIL_EFFECT_END,
       zone: Zone | None = None, count: IntExpr | All | None = None,
       until: Predicate | None = None, include_match: bool = True) -> Result[RevealReceipt]
```

- 显式cards与zone模式互斥。zone模式逐张授权并展示；until只能检查已展示对象，命中即停，不预先窥视停止位置。count限制最多张数；耗尽时不凭空制造对象。
- 返回cards、matched、公开范围及实际信息事件；普通展示不改区域。as-revealed内联通过on_event(..., timing="inline")进入。
- 显式actor保存谁展示，viewers只说明谁知道，不替代行动玩家。

```python
ops.reveal(cards, actor=opponent)
```

### `choose` 选择对象

```python
choose(player: Player, candidates: Selection[T], *, minimum: IntExpr = 1,
       maximum: IntExpr = 1, targeting: bool = True, bind_at: str = "finalization",
       shortage: str = "as_many_as_possible", link: Link | None = None) -> Result[list[T]]
```

- bind_at为setup、trigger、finalization或resolution；必须位于真正对应阶段，不准追溯。setup返回可被remember保存的构筑预选，数量／异名条件明确校验。
- 效果候选少于minimum时，as_many_as_possible强制选尽现有候选；足够时仍必须满足minimum，不变成可任意少选。成本选择必须shortage="fail"。
- targeting区分正式目标与非目标挑选；返回实际绑定对象。关联未来读取必须显式link或remember。

### `declare` 宣告值或选择合法模式

```python
declare(player: Player, options: list[T], *, minimum: int = 1, maximum: int = 1,
        kind: str = "value", bind_at: str = "resolution", link: Link | None = None) -> Result[list[T]]
```

- kind仅value、name、type、domain、tag、mode；options必须是规则允许的有限值或合法名称注册表。模式不是目标选择。
- bind_at同choose，且必须匹配实际能力时点；返回所选值。需要跨回合／多次技能读取时用remember，不隐含保存到所有同名卡。

### `predict` 洞察

```python
predict(player: Player, count: IntExpr = 1) -> Result[PredictReceipt]
```

- 返回：`looked`、`recycled`、`kept_on_top`，均保留具体实例及顺序。
- 语义：查看顶牌，可回收任意张，其余按允许次序回顶；不足不触发耗尽。多张洞察不是逐张洞察一的循环。

```python
ops.predict(player, 2)
```

### `show_off` 亮出

```python
show_off(player: Player, requirement: ShowOffRequirement, *, link: Link) -> Result[ShowOffReceipt]
```

- `requirement`：数量、合格属性及不同名称等约束。`link`：该能力的关联记录。
- 返回：手牌展示对象、场上挑选对象及亮出时属性快照。
- 语义：可按规则混合手牌与场上对象；相依效果读取亮出快照，后续改变不反向修改快照。

```python
ops.show_off(player, requirement, link=ability_link)
```

## 2. 区域与地点

### `transfer` 区域转移

```python
transfer(cards: Selection[Card], source: Zone | ZoneMap, destination: Zone | ZoneMap, *,
         order: str = "preserve", actor: Player = CONTROLLER,
          identity: ActionIdentity = ZONE_TRANSFER,
          position: str | None = None) -> Result[list[Card]]
```

- ZoneMap按实例给出来源／目的区域，所有对象属于同一指令批次；开始时读取来源快照，统一提交再处理清理与触发。允许分别回各拥有者手牌。
- identity仅ZONE_TRANSFER或BURN；后者只允许规则441.1授权的牌堆顶部入废，保留对应事件与被替代部分。不得选择DRAW/DISCARD/KILL等来绕过独立动作约束。
- 不自动生成抽牌、弃置、摧毁、放逐或回收事件。显式BURN请求与真实来源不符时失败，不替换为任意牌。
- position仅None、top、bottom；top/bottom要求目的区域为有序牌堆，表示本次区域转移直接放到对应一端，不产生第二次排序或转移。order仅决定同批对象的内部次序，不能用它暗示顶／底。
- 顶／底由卡文指定的玩家在指定时点决定，可先用declare获得值再传position。actor是执行放置的玩家；选择者、拥有者和能力控制者仍分别绑定。

### `move` 移动

```python
move(objects: Selection[Permanent], destination: Location | LocationMap, *,
     origin: Location | LocationMap | None = None, simultaneous: bool = True,
     actor: Player = CONTROLLER, join: EventRef | None = None) -> Result[list[Permanent]]
```

- LocationMap按实例绑定地点，支持同时交换位置、分别回不同控制者基地；统一读取出发快照并提交，不能在第一名移动后提前检查另一名的战斗。
- join只能在规则明确授权的过程窗口加入仍待执行的原move批次，不能加入已提交的移动。“当……移动”首先按事件后触发处理，不能仅因“随之”二字强制回填原批次；其移动指令使用新的move，保留原事件引用所需地点。
- 移动不自带普通移动横置成本，不改变控制者；只有实际变位者产生move事件。

### `recall` 召回

```python
recall(objects: Selection[Permanent], *, actor: Player = CONTROLLER) -> Result[list[Permanent]]
```

- 各对象送回其控制者对应基地，同批提交；不算move，不被move限制阻止，不回手。返回实际完成召回的对象。

### `discard` 弃置

```python
discard(player: Player, count: IntExpr, *, cards: Selection[Card] | None = None,
        chooser: Player | None = None) -> Result[list[Card]]
```

- `cards=None`：由 `chooser` 选择合法手牌；`chooser=None` 默认由行动玩家决定。
- 返回：实际从 `player` 手牌弃入其废牌堆的牌。
- 语义：效果不足则尽可能执行；作为成本时必须满足完整支付要求。强制弃置他人选中的牌须显式绑定 `cards`。
- 同一弃置指令产生一个`DISCARD.complete`集合事件，objects只含实际弃置的牌；逐牌的区域变化共享action_id。可按第12节选择逐对象或同批一次匹配。全部被替代时不产生弃置完成事件。

```python
ops.discard(player, 1)
```

### `recycle` 回收

```python
recycle(cards: Selection[Card], *, actor: Player = CONTROLLER) -> Result[list[Card]]
```

- 同一指令可跨玩家、跨区域；回到各拥有者对应牌堆底。主牌堆同时回收多张的牌底次序随机，符文由各自拥有者排序；不洗整个牌堆。
- 保留执行玩家与各对象实际结果；不会因选择者或拥有者不同而改写actor。

### `banish` 放逐

```python
banish(cards: Selection[Card | ChainItem], *, link: Link | None = None,
       actor: Player = CONTROLLER) -> Result[list[Card]]
```

- 接受场上／其他区域卡牌或明确链项，链项通过其card实例关联放逐；不能把能力链项当卡牌放逐。
- 不算摧毁或弃置；保存来源实例link与实际card身份。链项关联卡离链时按规则处理剩余执行体，不把放逐误作counter。
- 实际放逐提供`BANISH.complete`及对应`ZONE_TRANSFER.complete`视图；“放逐一张牌”可按per_object匹配，同批多张不丢失各自对象与拥有者。被替代而未放逐的对象不进入完成集合。

### `burn` 燃烧

```python
burn(player: Player, count: IntExpr, *, cards: Selection[Card] | None = None) -> Result[list[Card]]
```

- cards=None正常从顶部燃烧count并在不足时按耗尽流程继续。指定cards仅作用于已授权的明确剩余顶部牌，不补烧不在原集合的新牌；count必须与明确对象数量相符。
- 返回实际燃烧对象，保留Burn事件身份。非顶部来源不合法，不能把任意废牌转移伪装燃烧。

### `channel` 召出符文

```python
channel(player: Player, count: IntExpr, *, exhausted: bool = False) -> Result[list[Rune]]
```

- `exhausted`：入场朝向；默认活跃。
- 返回：实际从符文牌堆顶部召出的符文。
- 语义：不足则召出现有数量；休眠／活跃是入场状态，不另制造横置／活跃事件。

```python
ops.channel(player, 1, exhausted=True)
```

### `reorder` 调整次序

```python
reorder(cards: Selection[Card], zone: Zone, *, position: str,
        policy: str, chooser: Player | None = None) -> Result[list[Card]]
```

- `position`：`top` 或 `bottom`。`policy`：`preserve`、`choose` 或 `random`；`choose` 必须指定决定者。
- 返回：排序后的对象次序。
- 语义：只作用于指定集合；不自动查看、展示、抽取或回收。

```python
ops.reorder(cards, player.main_deck, position="top", policy="choose", chooser=player)
```

### `hide` 盖放

```python
hide(card: Card, battlefield: Battlefield, *, permission: HidePermission,
     link: Link | None = None) -> Result[Card]
```

- `permission`：明确的盖放授权，包含来源区域、容量、控制条件、未来打出权限及失控处理。
- 返回：实际盖放的牌。
- 语义：不算打出，不进入普通打出链。费用由所属盖放流程支付；本函数不再次扣费。
- 实际完成盖放后产生`HIDE.complete`，保存actor、card引用、来源区域、战场及盖放授权。失败／取消不产生完成事件；盖放不会产生`PLAY`事件。卡牌引用不额外公开盖放牌的名称、类型或规则文字。

```python
ops.hide(card, battlefield, permission=hidden_permission)
```

## 3. 打出与生成

### `play` 打出

```python
play(card: Card | TokenTemplate | CopyTemplate, player: Player, *, origin: Zone | None,
     destination: Zone | Location, cost_policy: CostPolicy = NORMAL_COST,
     permission: PlayPermission | None = None, choices: ChoiceBinding | None = None,
     entry: EntryState | None = None, link: Link | None = None) -> Result[PlayReceipt]
```

- 现有卡必须真实origin；新token/其副本用模板且origin=None，由本流程在链上创建，不先create在场上。免费只忽略被指定的费用，不绕过合法目标和地点。
- 打出流程：建立待处理项→as-play内联钩子/ShowOff/命名→模式和目标与费用选择→计算与支付全部适用费用→成为已定稿链项；之后按正常链流程轮到该项时才结算。永久物完成入场提供entered；卡牌成功结算后提供resolved。各钩子严格在所属阶段运行，play返回不等于该卡已结算。
- `PLAY.finalized`用于按已定稿统计的打出历史；“当你打出……”触发使用`PLAY.resolved`。被反制而未结算的卡不产生resolved，仍可存在finalized历史。正常结算但全部效果无法执行仍算结算完成。下一张打出优惠等过程引用继续在as_play／before_finalize绑定，不移到resolved。
- PlayReceipt为item、card、choices、payment、entry、link、是否已定稿等。item是ChainItem；不是已落地Unit。play返回后不能据此直接ready/attach新单位，应由queue_effect或on_event关联card在合法后续时点执行。
- ChainItem.card稳定标识其实体。只有卡面授权重打正在执行的自身时才允许origin=该链区；新的play拥有独立item和选择／费用记录，link可跨重打保存本能力声明的计数快照，不能擅自copy当前法术。
- “支付X以打出该牌”的CostBinding必须由具体规则确定其为触发基础费、替代打出费用还是其他成本；不能默认免费，也不能默认再收一份印刷费。触发基础费按383.3.b在触发定稿时支付；未确定费用角色的转换必须标待核，不凭参数扩充宣布正确。
- Repeat宏：可选附加费定稿决定是否支付，每一遍的模式/目标在当次法术定稿中分别保存；原链项结算按顺序执行多遍effect，未重复play事件。Flow宏：废牌堆来源权限＋替代基础费；对该次已定稿item建立离链放逐替代，包括被counter，明确由自身指令离链时除外。宏必须由KeywordSpec的闭集结构描述，不能读原文临时猜测。
- 入场entry由当前打出ChoiceBinding、付款回执和ShowOff快照求值，不能在已知付款之前伪造成功回执。

### `create` 生成卡牌、传奇或战场

```python
create(template: CardTemplate | CopyTemplate | SetupChoiceRef, count: IntExpr, *,
       owner: Player, controller: Player | None, destination: Zone | Location,
       state: EntryState = DEFAULT_ENTRY, duration: Duration = PERMANENT,
       link: Link | None = None) -> Result[CreateReceipt]
```

- count要求非负；新实例各有独立ID。战场controller必须None；单位、装备、符文、传奇初始控制者须为owner，除非来源明确授权其他情况。
- SetupChoiceRef须校验来源预选、不同名、剩余合法项和是否已在场；传奇从该预选产生时返回legends，并以link关联来源实例。duration到期按该创建授权的回收／移除约定清理，不擅自kill传奇。
- CreateReceipt含cards、units、gear、runes、legends、battlefields类型视图。生成不是打出，要求play的token用play(TokenTemplate,...origin=None)。


### `replace_battlefield` 替换或恢复战场

```python
replace_battlefield(target: Battlefield, template: CardTemplate | None = None, *,
                    mode: str = "replace", link: Link) -> Result[Battlefield | None]
```

- replace要求template；保存原战场，继承原有关状态／效果／引用，原牌暂存不制造普通banish事件。
- restore要求template=None；用同次link恢复既存原牌，无可恢复对象返回None。两种模式均继承当前相关状态，不能重找同名新牌。


## 4. 状态与战力

### `orient` 改变活跃／横置朝向

```python
orient(objects: Selection[Orientable], state: str, *, simultaneous: bool = True,
       actor: Player = CONTROLLER) -> Result[list[Orientable]]
```

- state闭集为ready、exhausted。接受Unit/Gear/Rune/Legend；仅返回实际改变朝向的对象。
- ready模式产生READY事件；exhausted模式产生EXHAUST事件，分别适用对应替代、限制和触发；不能使用一个通用“状态改变”事件抹平二者。
- 已处于目标朝向不重复成功。进入场上的朝向使用play.entry或modify_entry；本函数只改变已存在对象的朝向。
- simultaneous及actor的意义与原ready／exhaust相同；作为费用时仍须完整支付，不把尽可能执行的效果冒充支付。

```python
ops.orient(selected_units, "ready")
ops.orient(selected_runes, "exhausted")
```

### `buff` 给予增益

```python
buff(units: Selection[Unit]) -> Result[list[Unit]]
```

- 返回：实际新获得增益计数物的单位。
- 语义：默认每次给予一个、每单位至多一个、每个+1战力；超出上限不成功，不产生获得增益事件。明确的数量上限与贡献修饰仍适用。

```python
ops.buff(selected_units)
```

### `spend_buff` 消耗增益

```python
spend_buff(player: Player, units: Selection[Unit], *,
           count_each: IntExpr | dict[Unit, int] = 1) -> Result[CounterReceipt]
```

- count_each可为统一数量或按实例数量，所有消耗组成一个指令批次；返回各对象实际消耗数和总计。
- player须控制相应单位；友方含队友不代表能花队友计数物。作为成本时必须完整支付，不能用少消耗冒充已付。
- 实际消耗产生`SPEND_BUFF.complete`，含每单位实际消耗数量及被消耗计数物的稳定引用；“每当消耗一个增益”使用per_counter，同一指令消耗多个就按实际数量分别匹配。`BUFF`仅表示获得，不表示消耗；离场清理移除增益也不算spend_buff。

### `stun` 眩晕

```python
stun(units: Selection[Unit]) -> Result[list[Unit]]
```

- 返回：实际新变为眩晕的单位。
- 语义：不横置、不扣战力；已眩晕不再次成功。按默认规则解除，不贡献战斗伤害但仍按正常致死要求承伤。
- 只有本来可以实际发生的眩晕动作生成STUN.before；已眩晕或禁止眩晕的单位没有可替代的再次眩晕事件。选择该单位本身合法，不保证存在眩晕动作。

```python
ops.stun(enemy_units)
```

### `change_empowerment` 强化／解除一层强化

```python
change_empowerment(objects: Selection[Permanent | Legend], mode: str, *,
                   actor: Player = CONTROLLER) -> Result[list[Permanent | Legend]]
```

- mode闭集为empower、disempower；每次至多对各对象增加／移除一层，返回实际完成该模式动作的对象。
- empower模式保留EMPOWER动作身份：默认二元状态，已强化不再次成功；明确可叠层的对象检查自己的上限。
- disempower模式保留DISEMPOWER动作身份：未强化不变化；多层时只移除一层，不直接设成未强化。
- 模式分别适用成本、限制、替代和触发。判断成功使用实际返回对象，不以模式请求推定已发生；不改动规则所定义的强化期限。

```python
ops.change_empowerment(selected_units, "empower")
ops.change_empowerment(selected_units, "disempower")
```

### `modify_might` 调整、设至或交换战力

```python
modify_might(units: Selection[Unit], delta: IntExpr | None = None, *,
             change: MightChange | None = None, duration: Duration,
             floor: IntExpr | None = None, ceiling: IntExpr | None = None) -> Result[list[Modifier]]
```

- delta是add简写，与change互斥。MightChange.add为有符号增减；set(value,direction)使用本次执行战力差快照，direction为both/increase_only/decrease_only；swap(other)要求units恰一名，与other共享同一快照并同批登记差值。
- floor/ceiling只限制本修饰；set/swap不是持续强制最终战力等于某数，不移走装备或增益，也不改变基础战力层。
- 同指令多个不同修饰用batch；不以总数值相同冒充装备贡献层相同。
- set/swap先算完本次共同快照的有符号差值，再为各对象的非零差值生成MIGHT_CHANGE.before。替代一名对象的负差值不回算其他对象的差值；差值为零不生成负战力事件。
- MIGHT_CHANGE在此表示施加战力增减修饰的动作，不是任意最终战力下降；移除装备、修饰到期、角色切换等不会自动伪造一个“给予负战力”的动作。基础战力层另由set_base_might处理。

```python
ops.modify_might([u], change=MightChange.set(5, direction="increase_only"), duration=THIS_TURN)
```


### `set_base_might` 修改基础战力

```python
set_base_might(units: Selection[Unit], value: IntExpr, *,
               duration: Duration) -> Result[list[Modifier]]
```

- 返回：基础战力修饰。
- 语义：只修改基础值；增益、装备与其他修饰继续按层应用。

```python
ops.set_base_might(selected_units, 3, duration=WHILE_SOURCE_PRESENT)
```


## 5. 伤害与摧毁

### `damage` 造成伤害

```python
damage(units: Selection[Unit], amount: IntExpr, *, source: Source = SOURCE,
       mode: str = "each", allocation: dict[Unit, int] | None = None,
       use_all: bool = True, simultaneous: bool = True,
       actor: Player = CONTROLLER) -> Result[DamageReceipt]
```

- each为每目标同一数值；split为总池，必须给出合法分配。Bonus对each每个目标分别应用，对split只增加总池；不能用split表达不等值的独立逐目标伤害。
- 不同source或不同数值的同指令伤害用batch(SIMULTANEOUS)，在共享伤前快照取Might，所有伤害提交前不致死清理。
- “Deal X for each Y”按418.8为一个数值X×Y的实例，非Y次循环。伤害不扣战力；0不产生实际伤害事件。
- 返回每目标分配、修饰后、实际、过量及来源；死亡随后由规则清理产生，不由返回伤害值直接猜测。

### `prevent_damage` 预防伤害

```python
prevent_damage(units: Selection[Unit], amount: IntExpr | Infinity, *,
               source_filter: Predicate = ANY_SOURCE, duration: Duration,
               limit: UsageLimit | None = None) -> Result[list[Modifier]]
```

- 每目标amount额度按实际预防量扣减；INFINITY预防所有匹配伤害。limit可限定下一伤害事件且每目标独立消耗，不把“下一次”变为全回合所有次。
- limit的计数单位必须damage_event或instruction_batch，按卡面写明；同次分配多个目标保留原实例分组，不无效化整项能力。

### `heal` 治疗

```python
heal(units: Selection[Unit]) -> Result[HealReceipt]
```

- 返回：各单位实际清除的伤害量。
- 语义：清除已受伤害，不增加战力；原本无伤害时不伪造清除量。

```python
ops.heal(friendly_units)
```

### `kill` 摧毁

```python
kill(objects: Selection[Permanent], *, source: Source = SOURCE,
     simultaneous: bool = True, actor: Player = CONTROLLER) -> Result[list[Card]]
```

- 先处理将死替代；返回真正因本动作死亡的card，保存伤前／死亡前信息和行动者。
- 同批杀多个对象或多位玩家分别杀各自对象时用batch并各传actor；死亡被召回替代则不返回已死、不触发死亡能力。

## 6. 装备、控制与复制

### `attach` 贴附

```python
attach(gear: Gear, host: Unit) -> Result[Attachment]
```

- 返回：实际建立的贴附关系；已贴附同宿主时不产生新贴附。
- 语义：旧贴附按规则解除；装备自身规则与宿主获得的效果文字分开处理。位置随宿主变化，但本动作不算移动或活跃，也不支付装配费用。

```python
ops.attach(gear, friendly_unit)
```

### `detach` 卸除

```python
detach(gear: Selection[Gear]) -> Result[list[Gear]]
```

- 返回：实际解除贴附的装备。
- 语义：移除宿主获得的相应效果及武装战力，恢复装备自身文本；未贴附则不变化。位置及后续召回由规则处理。

```python
ops.detach(selected_gear)
```

### `change_control` 改变控制

```python
change_control(objects: Selection[Permanent | ChainItem], player: Player, *,
               duration: Duration = PERMANENT,
               link: Link | None = None) -> Result[list[Modifier]]
```

- `duration/link`：保存控制权持续期及归还条件。
- 返回：控制权修饰。
- 语义：拥有者不变，不自动移位置，不自动重新选择链项的目标。

```python
ops.change_control([spell], player)
```

### `end_modifier` 结束指定修饰

```python
end_modifier(modifiers: Selection[Modifier], *,
             link: Link | None = None) -> Result[list[Modifier]]
```

- 参数必须是已取得的具体Modifier引用；只结束效果明确授权结束的修饰，不按对象或卡名删除其他来源的全部修饰。link给出时校验本次实例关联。
- 返回实际结束的修饰；空集合、已结束或因对象离区失效的修饰不重复成功。不会撤销已经发生的支付、伤害、移动或抽牌。
- 结束控制权修饰时重新求当前有效控制关系，不强行设回拥有者或某个旧控制者。后续recall按结束后的实际控制关系和对象合法性执行。
- 调用在当前指令处立即结束修饰；不另开链项、不等到回合清理。链项结算中的Cleanup仍按通用约定延后。

### `copy` 复制特征

```python
copy(target: Permanent, original: Permanent, *, traits: CopyTraits = COPYABLE_TRAITS,
     duration: Duration) -> Result[Modifier]
```

- `traits`：允许复制的特征范围，不包含未明确授权的实例状态。
- 返回：目标实例上的复制修饰。
- 语义：不创建新实例；不默认复制伤害、计数物、临时战力或控制权。生成复制体使用 `create(CopyTemplate(...), ...)`。

```python
ops.copy(target, original, duration=THIS_TURN)
```

### `copy_text` 复制文本

```python
copy_text(target: Permanent, original: Permanent, *, from_field: str,
          to_field: str, duration: Duration, link: Link | None = None) -> Result[Modifier]
```

- `from_field/to_field`：`rules_text` 或 `effect_text`；复制范围、取值时点及指代按能力明确绑定。
- 返回：文本复制修饰。
- 语义：不复制整个对象；按复制层、能力层与依赖关系处理，不能递归拼接自身新获得文本。

```python
ops.copy_text(gear, host, from_field="rules_text", to_field="effect_text",
              duration=WHILE(attached_to(gear, host)))
```

### `copy_abilities` 取得指定能力

```python
copy_abilities(target: Permanent, originals: Selection[Permanent | Legend], *,
               ability_filter: Predicate, duration: Duration) -> Result[list[Modifier]]
```

- `ability_filter`：如费用包含横置的主动能力。`originals` 可以是持续求值的集合。
- 返回：取得能力的修饰，保留原能力身份、来源及第一人称绑定规则。
- 语义：不等于复制整张牌，不把同一派生能力无限递归复制。

```python
ops.copy_abilities(unit, friendly_objects, ability_filter=HAS_EXHAUST_COST,
                   duration=WHILE_SOURCE_PRESENT)
```

## 7. 能力与特征修饰

### `grant_ability` 赋予能力

```python
grant_ability(objects: Selection[Permanent | Card], ability: Ability, *,
              duration: Duration, link: Link | None = None) -> Result[list[Modifier]]
```

- 返回：能力授予修饰。
- 语义：保存完整能力、来源、主体及关联；不在授予时立即执行被授予的效果。

```python
ops.grant_ability(selected_units, ability, duration=THIS_TURN)
```

### `suppress_ability` 使能力失活

```python
suppress_ability(objects: Selection[Permanent | Card], ability_filter: Predicate, *,
                 duration: Duration) -> Result[list[Modifier]]
```

- 返回：指定能力范围的失活修饰。
- 语义：只抑制匹配能力，不删除类型、战力或无关文本；失活期限结束后重新按规则判断生效。

```python
ops.suppress_ability(selected_units, selected_ability, duration=THIS_TURN)
```

### `grant_keyword` 赋予关键词

```python
grant_keyword(objects: Selection[Permanent | Card], keyword: Keyword, *,
              parameters: KeywordParameters = EMPTY,
              duration: Duration) -> Result[list[Modifier]]
```

- `parameters`：该关键词明确需要的数值、费用等，按其类型检查。
- 返回：关键词修饰。
- 语义：按关键词本身的重复／加总规则处理；授予关键词不等于当场执行其效果。

```python
ops.grant_keyword(selected_units, GANKING, duration=THIS_TURN)
```

### `modify_keyword` 修改关键词参数

```python
modify_keyword(objects: Selection[Permanent | Card], keyword: Keyword, *,
               parameter: str, operation: str, value: IntExpr,
               duration: Duration) -> Result[list[Modifier]]
```

- `operation`：`add`、`multiply` 或 `set`；`parameter` 必须是该关键词公开的数值或费用字段。
- 返回：关键词参数修饰。
- 语义：修改坚守值不直接修改战力；进攻／防守条件仍由该关键词决定。

```python
ops.modify_keyword(selected_units, SHIELD, parameter="value", operation="multiply",
                    value=2, duration=THIS_TURN)
```

### `set_types` 修改类型集合

```python
set_types(objects: Selection[Permanent | Card], types: set[CardType], *,
          mode: str = "replace", duration: Duration) -> Result[TypeChangeReceipt]
```

- mode为add/remove/replace。返回modifiers及按当前实际类型生成的units/gear等视图；类型变化后同ID引用按新类型重检。
- Gear增加UNIT后可用receipt.units调用set_base_might，不在类型未改变时强制转型；集合类型不丢原装备属性。

### `set_tags` 修改标签集合

```python
set_tags(objects: Selection[Permanent | Card], tags: set[Tag], *,
         mode: str = "add", duration: Duration) -> Result[list[Modifier]]
```

- `mode`：`add`、`remove` 或 `replace`。
- 返回：标签修饰。
- 语义：改变玩法标签，不更改卡名；动态标签集合须保留表达式依赖。

```python
ops.set_tags(selected_units, {MECH}, duration=WHILE_SOURCE_PRESENT)
```

## 8. 资源、费用与分数

### `add_resources` 获得资源

```python
add_resources(player: Player, resources: ResourceBundle, *,
              restriction: Predicate = UNRESTRICTED,
              expires: ResourceExpiry = NORMAL_POOL_EXPIRY) -> Result[ResourceReceipt]
```

- `ResourceBundle`：`energy: IntExpr`、`power: list[PowerAmount(domain, count)]`。
- 返回：实际加入的资源批次，保存领域、来源、限制和到期。
- 语义：产费不是减费，不自动执行符文的横置或回收；产费能力的特殊结算时机由所属流程处理。

```python
ops.add_resources(player, ResourceBundle(energy=2))
```

### `pay` 支付费用

```python
pay(player: Player, cost: Cost, *, binding: CostBinding) -> Result[PaymentReceipt]
```

- `Cost`：资源要求与具名动作费用的组合。`binding`：基础／额外／替代／指令内／动作附加费用及对应时点。
- 返回：完整支付凭据，包含实际资源、动作、替代处理及对应效果关联。
- 语义：支付失败不能执行其相依效果；不因费用被替代就一律判未付。单纯支付后检查实际结果的指令使用其对应规则，不冒充基础费用。
- 触发能力首部的“支付X以执行Y”按触发基础费用定稿支付；“为X打出”与这种费用角色不能仅凭数值相同互换。pay不自动改变后续play的基础费用；后者政策必须另有规则依据。受限资源按实际支付的是能力还是卡牌检查。

```python
ops.pay(player, cost, binding=ability_cost_binding)
```

### `modify_cost` 调整费用

```python
modify_cost(subjects: CostSelection, change: CostChange, *, duration: Duration,
            uses: int | None = None, limit: UsageLimit | None = None,
            link: Link | None = None) -> Result[Modifier]
```

- uses为UsageLimit(count=uses,reset="never",consume="on_finalize")简写，与limit互斥。可选每回合一次优惠必须limit指定each_turn和optional=True；拒绝不耗次数。
- CostChange字段闭集：energy_delta、power_discount、power_add、base_replace、ignore_base、ignore_energy、additional_actions。可选附加成本由ChoiceBinding选定，完整支付后形成PaymentReceipt。
- 目标费用、替代基础费、额外费用与指令内付款分开；不改印刷费用，不返还已付资源。Power折扣按规则分配领域，不擅自优先扣某一领域。
- link保存本次费用选择与目的地／入场／后续效果的关联；正向强制位置要求使用modify_rule(PLAY_LOCATION_REQUIREMENT, ...)，具体PlayConstraint见第9节，不能只grant_permission而漏掉强制目的地。

### `change_xp` 经验变化

```python
change_xp(player: Player, amount: IntExpr, *, mode: str = "gain") -> Result[int]
```

- gain增加XP并发获得事件，spend消耗XP并发消耗事件；amount均非负，结果为实际变化量。
- spend不足失败；作为成本由pay检查整套成本，不能先扣一部分再执行相依效果。等级依赖随实际XP变化重算。


### `gain_points` 获得分数

```python
gain_points(player: Player, amount: IntExpr, *,
            source: Source = SOURCE, cause: PointCause = CARD_EFFECT) -> Result[int]
```

- `cause`：实际增分来源，用于适用相应限制和替代。
- 返回：实际增加分数；被替代为其他动作的部分单独记录。
- 语义：不伪造征服、据守或Scored事件；最后一分限制按来源判断。
- 正数的合法增分尝试在提交前提供GAIN_POINTS.before；保留player、amount、cause、来源战场及该玩家自己的回合序号。禁止增分或原规则已改为抽牌时，不另制造一个可被再次替代的增分尝试。
- 替代只取消该次增分动作；若原因为HOLD/CONQUER，不取消已发生的据守／征服及已记入的本回合战场得分记录。complete仅记录实际增分部分。

```python
ops.gain_points(player, 1)
```

### `win` 获胜

```python
win(player: Player, *, authorization: WinAuthorization) -> Result[GameOutcome]
```

- `authorization`：已满足条件的明确卡牌效果或规则授权。
- 返回：对局结果。
- 语义：不等于加分，不允许用任意布尔值跳过明示的胜利条件。

```python
ops.win(player, authorization=resolved_win_effect)
```

## 9. 规则修饰

### `modify_damage` 修改伤害

```python
modify_damage(events: DamageSelection, change: NumericChange, *,
               duration: Duration, uses: int | None = None) -> Result[Modifier]
```

- `events`：来源、受害对象、战斗／非战斗等筛选。`change`：加值或规则允许的翻倍等修改。
- 返回：伤害修饰，不立即造成伤害。
- 语义：额外伤害、翻倍和预防按各自规则处理；不能用战力变化替代。

```python
ops.modify_damage(friendly_spell_damage, NumericChange(add=1), duration=THIS_TURN)
```

### `modify_effect_value` 修改效果参数

```python
modify_effect_value(effects: EffectSelection, parameter: EffectParameter,
                     change: NumericChange, *, duration: Duration) -> Result[Modifier]
```

- `parameter`：已登记的具体效果字段，如负战力幅度，不能是任意文字或任意数字位置。
- 返回：对应参数修饰。
- 语义：只修改匹配指令；不把所有文本数字一并增减。

```python
ops.modify_effect_value(friendly_might_reductions, REDUCTION_AMOUNT,
                         NumericChange(add=1), duration=WHILE_SOURCE_PRESENT)
```

### `modify_trigger_count` 修改触发次数

```python
modify_trigger_count(triggers: TriggerSelection, extra: IntExpr, *,
                      duration: Duration) -> Result[Modifier]
```

- 返回：指定触发种类的次数修饰。
- 语义：不重复打出来源牌，不复制整张牌的无关能力。

```python
ops.modify_trigger_count(conquer_triggers, 1, duration=THIS_TURN)
```

### `modify_resource_output` 修改产费

```python
modify_resource_output(actions: ResourceActionSelection, change: ResourceChange, *,
                        duration: Duration) -> Result[Modifier]
```

- `change`：具体资源的数量／领域修改。
- 返回：指定产费动作的修饰。
- 语义：保持资源来源与使用限制，不直接改玩家当前资源池。

```python
ops.modify_resource_output(friendly_gold, ResourceChange(energy_delta=1),
                            duration=WHILE_SOURCE_PRESENT)
```

### `modify_buff_value` 修改增益贡献

```python
modify_buff_value(units: Selection[Unit], delta_each: IntExpr, *,
                   duration: Duration) -> Result[Modifier]
```

- 返回：每个增益计数物战力贡献的修饰。
- 语义：不放置新增益、不触发获得增益事件；计数物数量上限另行修改。

```python
ops.modify_buff_value(friendly_units, 1, duration=THIS_TURN)
```

### `grant_permission` 赋予动作权限

```python
grant_permission(subjects: PermissionSelection, permission: PermissionSpec, *,
                  duration: Duration, uses: int | None = None) -> Result[Modifier]
```

- `PermissionSpec`：明确动作，以及新增时机、来源区域、目的地或合法选择。
- 返回：带适用范围及期限的权限记录。
- 语义：只扩大指明权限，不自动忽略费用或无关限制。

```python
ops.grant_permission(selected_card, play_from_trash, duration=THIS_TURN, uses=1)
```

### `restrict_action` 限制动作

```python
restrict_action(subjects: PermissionSelection, restriction: RestrictionSpec, *,
                 duration: Duration) -> Result[Modifier]
```

- `RestrictionSpec`：被禁止的具体动作、对象、来源与例外。
- 返回：限制记录。
- 语义：禁止被选为目标不等于免疫所有效果；禁止增分不等于禁止Scored流程。

```python
ops.restrict_action(enemy_players, CANNOT_GAIN_POINTS, duration=WHILE_SOURCE_PRESENT)
```

### `modify_rule` 修改明确规则项

```python
modify_rule(key: RuleKey, scope: RuleScope, change: RuleChange, *,
            duration: Duration) -> Result[Modifier]
```

- 仅接受下表注册键及其匹配结构；不接受任意自然语言、任意键或未解析效果。

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
| PLAY_LOCATION_REQUIREMENT | RuleScope的players、cards、link过滤当前打出实例；RuleChange仅play_constraint: PlayConstraint |

- ignore_keywords不抹除单位持有的关键词，只改变该分配者适用的承伤顺序。

`PLAY_LOCATION_REQUIREMENT`参数：

| 字段 | 类型与语义 |
| --- | --- |
| `destinations` | `Selection[Location]`；在该次打出选择阶段求值的正向目的地要求 |
| `when` | `Predicate`；明确何时启用，如已选择本次附加费用分支；不得提前读取尚不存在的支付回执 |
| `grant_destination` | `bool`；True同时授权这些目的地，仍受全部硬性禁止限制；False仅约束已有合法选择 |
| `payment_binding` | `CostBinding \| None`；与可选附加费相关时必须指向同次选择及支付记录，不另外扣费 |

- `RuleChange(play_constraint=...)`只登记正向位置要求，不将未选位置改写为can't。对象、付款分支和来源通过同次link关联；不选可选付费分支时不启用这一分支的要求。
- 在定稿的选择阶段，将所有适用正向要求分为不能再加入其他相容要求的极大相容组。相容要求必须共同满足；多个组互相冲突时由打出玩家选一个组并忽略其他组，所选组写入ChoiceBinding。不允许任意丢弃可以共同满足的要求。
- 禁止／only限制始终单独强制检查，不能作为可丢弃的正向要求参与仲裁。无法作出合法选择或完整支付时定稿失败；不能通过忽略硬性限制完成定稿。
- 位置要求在选择时依据已声明的费用分支生效；该分支的费用仍在正常付费阶段完整支付。最终ChoiceBinding保存目的地与要求组，PaymentReceipt保存实际付款，不倒置先选后付的顺序。
- 后续“改为进入某处”的入场替代由PLAY入场替代处理，保存最终入场位置；不回写最初选择的地点，不把入场替代混成选择限制。

## 10. 链与回合流程

### `counter` 无效化

```python
counter(item: ChainItem, *, destination: Zone | None = None) -> Result[ChainItem]
```

- `destination=None`：正常离链目的地；明确回手等修饰时指定对应区域，仍处理适用替代。
- 返回：实际被无效化的链项。
- 语义：原效果不执行，已付费用不返还；不视为正常执行完成的打出事件。

```python
ops.counter(spell, destination=spell.owner.hand)
```

### `redo_choices` 重做链项选择

```python
redo_choices(item: ChainItem, player: Player, *,
              fields: set[ChoiceField] = ALL_ALLOWED_CHOICES) -> Result[ChoiceBinding]
```

- `fields`：目标、模式及其他明确允许重做的选择。
- 返回：新的选择绑定，替换对应旧选择。
- 语义：不自动夺取控制权，不重复已支付费用，也不将全部选择缩减为重选单个目标。

```python
ops.redo_choices(spell, new_controller)
```

### `execute_effect` 执行明确能力效果

```python
execute_effect(source: Source, ability: AbilityRef, *, count: IntExpr = 1,
               choices: ChoiceBinding | None = None,
               mode: str = "pending", link: Link | None = None) -> Result[list[ChainItem]]
```

- pending创建相应已知效果的待处理项，不伪造原事件；可从LKI引用已离场来源的明确能力。
- repeat_inline只用于Repeat宏已经完成多遍选择定稿后的同链项重复原效果，不建新法术，不额外产生spell-play事件；choices须保存每遍独立的完整选择。
- 不接受未知文字，不能用execute_effect(raw_text)兜底。

### `skip_procedure` 跳过流程

```python
skip_procedure(player: Player, procedure: ProcedureRef, *,
                 occurrence: str = "next", duration: Duration) -> Result[Modifier]
```

- `procedure`：明确的回合、阶段、步骤或子步骤。`occurrence`：下一次或期限内所有匹配项。
- 返回：延迟流程替代记录。
- 语义：被跳过流程不发生，也不产生该流程发生的触发事件。

```python
ops.skip_procedure(player, DRAW_PHASE, duration=UNTIL_NEXT_TURN_END)
```

### `extra_turn` 追加回合

```python
extra_turn(player: Player, count: IntExpr = 1, *,
             after: TurnRef = CURRENT_TURN) -> Result[list[TurnRef]]
```

- `after`：插入锚点，不默认放到自然轮转末尾。
- 返回：新增回合引用，顺序与插入顺序一致。
- 语义：追加完整回合；不提前执行额外回合内动作，也不延迟当前效果的后续指令。

```python
ops.extra_turn(player, after=CURRENT_TURN)
```

## 11. 批次、事件及关联

### `batch` 同指令批次

```python
batch(*, policy: BatchPolicy = SIMULTANEOUS) -> BatchScope
```

- 作为with上下文使用。SIMULTANEOUS在开始时冻结共同输入快照，内部登记的动作共同提交，提交后按原链流程登记触发和待办清理，不在当前链项结算内执行Cleanup；返回的Result提交前不可读取。不同来源、行动者、目的地仍分别记录。
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
- `PLAY.resolved`、`USE_ABILITY.resolved`、HIDE／DISCARD／BANISH／SPEND_BUFF的complete、状态转换及战斗／对决边界均是事件发生后的触发入口，不能用inline提前执行。USE_ABILITY只包括真实激活的主动能力，Weaponmaster内部计算及支付Equip费用不伪造使用主动能力事件。
- 事件引用提供actor、source、card/item、objects、原地点、伤前战力、支付回执和关联快照；只能读取该阶段真实存在的信息。
- bind-next用EventPattern(kind=PLAY,matching=FIRST,filter=明确条件)、inline及UsageLimit(1)绑定真实下一个对象；不提前猜手牌，消费点按被接受事件指定。
- ability必须有完整代码体，源离场是否仍生效由明确duration决定，不自动随登记者离场取消所有延迟能力。
- “回合末”的触发匹配当前回合Ending阶段开始的指定时点，不等于所有THIS_TURN修饰的自动到期。若该时点在本回合已过去，不补触发、不挪到下回合；应忽略该项延迟能力的生成。延迟项已创建时，其显式参数可保存此前取得的Modifier引用。
- 战场能力明确指定某玩家作选择时，Ability.controller绑定该玩家；不默认使用战场拥有者、战场当前控制者或回合玩家。未指定时才采用战场能力的一般控制规则。

```python
# ability参数均须预先提供完整Ability头和EffectProgram。
ops.on_event(EventPattern(kind="PLAY", stage="resolved", actor=player),
             when_played_ability, duration=WHILE_SOURCE_PRESENT)
ops.on_event(EventPattern(kind="DISCARD", stage="complete", actor=player,
                          granularity="per_batch"),
             when_discarded_ability, duration=WHILE_SOURCE_PRESENT)
ops.on_event(EventPattern(kind="STATE_TRANSITION", stage="complete", objects=[unit],
                          transition=StateTransitionSpec(field="might", comparison="ge",
                                                         value=10, direction="false_to_true")),
             when_reached_ten_ability, duration=WHILE_SOURCE_PRESENT)
```

### `replace_event` 登记待发生事件替代

```python
replace_event(events: EventPattern, rewrite: EventRewrite, *, duration: Duration,
              optional: bool = False, limit: UsageLimit | None = None,
              link: Link | None = None) -> Result[Modifier]
```

- 匹配待发生事件，在提交前适用；rewrite明确保留／取消原事件及替代动作。带PaymentGate时先在该费用角色下调用pay完整支付，支付失败或拒绝则不接受此替代，原事件照常发生；不能先取消死亡再检查付不付钱。PaymentGate的cost/payer/binding及相依program均须明确，不接受仅写“可付费救援”的原文。
- before在原动作前执行（如展示前看顶牌）；resume_original为True时重新按获授权来源求本来要展示的牌，不复用越权预读列表。after在原动作同过程指定位置执行，不能代替需要上链的then-do-this。
- 自身替代不会无限重新匹配自己的替代展开；仍按官方多替代选择及适用规则处理。每次事件的消费额度与事件身份单独保存。
- EventPatch字段闭集如下；其他变化须用已经分解的EffectProgram，不能填自然语言patch。
- 同一区域变化的具名动作与ZONE_TRANSFER是同一待发生转移的两种视图，共享transition_id。任一视图上的替代都作用于同一原转移；同一个修饰不能因匹配两种视图而重复应用。具体去重、实际动作身份及批次规则见第12节。

| 原事件 | 允许Patch |
| --- | --- |
| PLAY | entry、destination、额外同模板token数量（只限授权新token） |
| CHANNEL | 每枚符文的entry序列，包含原数量/朝向和明确追加枚数 |
| REVEAL/LOOK | 保留原来源/数量，在before结束后重新求值对象 |
| LEAVE_CHAIN | destination、identity、只匹配指定item且排除自身指令离链 |
| DIE、ZONE_TRANSFER、DISCARD、BANISH、COMBAT_TIE、STUN、MIGHT_CHANGE、GAIN_POINTS | 取消匹配的原事件并执行明确替代program；同批其他对象／事件不随之取消，不得把事后补偿当替代 |

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

### 事件匹配结构

| EventPattern字段 | 约定 |
| --- | --- |
| `kind` / `stage` | 必须是下表登记组合；不省略有歧义的阶段，PLAY触发不得以finalized代替resolved |
| `actor` / `source` / `objects` | 明确行动玩家、效果来源、对象引用或筛选器；未提供的过滤项不限制该字段 |
| `filter` | 明确Predicate，可检查该阶段实际可得的地点、区域、类型、领域、支付与历史快照；不授权隐藏信息 |
| `granularity` | per_event（默认）、per_object、per_batch、per_counter；规则见下方，非法组合拒绝 |
| `matching` | ALL（默认）或FIRST；FIRST必须明确计数对象与UsageLimit复位／消费点，不默认逐玩家或逐卡名 |
| `transition` | `StateTransitionSpec \| None`；仅STATE_TRANSITION使用；BECOME_MIGHTY采用下方固定结构 |

| EventKind | 开放的阶段及数据 |
| --- | --- |
| PLAY | as_play、before_finalize、finalized、entered、resolved；仅卡牌打出，含card/item、actor、choices、payment、选择位置与实际入场位置；entered只表示永久物已完成入场，resolved表示卡牌成功结算完成 |
| USE_ABILITY | before_finalize、finalized、resolved；主动能力实例、source、actor、controller、Energy等费用特征、choices、payment；使用／打出主动能力触发匹配resolved，反制不产生resolved |
| HIDE | before、complete；card、actor、来源区域、battlefield、permission与费用回执；只含获授权的信息，不等于PLAY |
| DISCARD | before、complete；player、actor、chooser、objects、各对象实际来源／目的区域及action_id；complete默认同一弃置指令的实际完成集合 |
| BANISH | before、complete；actor、source、objects、拥有者、来源区域、各自放逐区、link；complete默认同一放逐指令的实际完成集合 |
| SPEND_BUFF | before、complete；player/actor、各unit、实际计数物引用、count_each、total、费用／效果角色；per_counter仅对实际消耗逐个匹配 |
| LOOK / REVEAL | before、as_each、complete；真实已授权牌及所看牌堆，不提供未来牌序 |
| ATTACH | as_attach、complete；gear/host/previous_host |
| MOVE | before、complete；各对象原地点与目的地、actor、原批次ID |
| DIE / LEAVE_BOARD / ZONE_TRANSFER | before、complete；对象、LKI、源/目的区域、动作身份及transition_id；所有真实区域变化必须提供ZONE_TRANSFER视图，具体映射与去重见下方 |
| DAMAGE | before、complete；来源、目标、数量、实例和分配批次 |
| STUN | before、complete；实际可执行的眩晕动作、对象、actor、来源及该来源链项的选择记录；已眩晕／不可眩晕不生成before |
| MIGHT_CHANGE | before、complete；施加的非零有符号差值、对象、持续期、来源、原指令及选择记录；set/swap的共同快照差值先于替代计算，不代表任意派生战力变化 |
| STATE_TRANSITION | complete；对象、明确状态字段、前后规则值、转换条件、causes及同批快照；依赖重算后的状态边沿，只观察而不制造新动作 |
| BECOME_MIGHTY | complete；STATE_TRANSITION中might由<5变为≥5的具名视图，与对应状态转换共享事件关联，不额外重复触发 |
| GAIN_POINTS | before、complete；player、amount、cause（HOLD/CONQUER/CARD_EFFECT）、source、来源战场、玩家自己的回合序号；不替代Scored流程 |
| TURN_PHASE | start/end及具体玩家、阶段、回合序号 |
| HOLD / CONQUER / ATTACK / DEFEND / COMBAT_START / COMBAT_WIN / COMBAT_TIE | 对应规则事件，含玩家、地点、参战单位及过量分配快照 |
| SHOWDOWN_START | start；showdown_id、battlefield、focus_player、参与者及combat_id或None；非战斗对决也发布，同一对决转为战斗对决不重复发布开始 |
| COMBAT_END | end；combat_id、battlefield、玩家、结果及参加过的单位历史引用；按468.7的战斗结束边界发布，包括No Result，不等于COMBAT_WIN/TIE |
| CHOOSE / DRAW / RECYCLE / BURN / CHANNEL / BUFF / EMPOWER / DISEMPOWER / EXHAUST / READY / XP | before/complete及具体actor、对象、实际完成数量；普通选择不假冒target |
| LEAVE_CHAIN | before/complete；item、card、原因（执行/无效/外部动作）、自身指令离链标志 |

### 阶段、批次与实际结果

- resolved只表示对应卡牌／主动能力完成正常结算，complete用于表中具名动作的实际完成；两者不是任意互换的别名。能力来源离场、移位或改变控制者时仍保留item、actor和来源引用，不据此伪造结算失败。
- per_event按该种事件原生粒度匹配。DISCARD／BANISH／SPEND_BUFF的原生粒度为同一指令的完成集合；per_object按实际对象分别匹配；per_counter仅用于SPEND_BUFF，按每个实际消耗计数物匹配。
- per_batch按同一action_id、actor及该次指令批次匹配一次，objects保存该指令实际完成对象。不同顺序指令、不同玩家的动作、跨回合动作不能因有共同外层batch_id而合并。“弃一张或多张”采用DISCARD.complete的per_batch；“放逐一张”采用BANISH.complete的per_object。
- 替代、禁止或执行失败的对象不进入原动作complete集合；实际完成集合为空不产生该动作complete。原动作的before不能作为“已经完成”的证据。来源触发的有效区域与LKI仍按383.2.c检查。
- 一个Ability的同一触发条件若以或关系同时匹配具名与通用视图，对同一实际发生只建一个待处理项；不同能力保留各自触发。不能以去重为由吞掉真正不同的顺序动作或多个被消耗增益。
- COMBAT_END保存该次战斗参加过的稳定实例引用；这些历史引用不等于仍在场的合法Unit。参与历史只供触发条件使用，执行能力体时仍按原卡有效区域、LKI及对象合法性重检。结束边界、角色移除及THIS_COMBAT修饰到期遵守468.7，不提前执行清理。

### 独立区域动作的通用视图

- 每个真实的区域变化均发布ZONE_TRANSFER.before／complete，包括DRAW、DISCARD、BURN、RECYCLE、BANISH、KILL、CHANNEL、HIDE、PLAY、CREATE与普通ZONE_TRANSFER，以及离链／离场流程导致的转移。identity记录实际负责该转移的具名动作；cause保存其父动作、链项或规则流程。CREATE的新实例源区域为None，不能伪造先前所在区域；没有区域变化的生成部分不发布转移视图。
- 函数仍各自校验原动作的来源、权限、费用与触发语义；transfer不能传入DISCARD等identity来冒充独立动作。通用视图的存在只提供统一观察／替代入口，不使动作互相等价。
- before保存真实待转移对象与原始源／目的区域；具名动作、LEAVE_BOARD、LEAVE_CHAIN与通用视图在涉及同一转移时共享transition_id。集合指令保留每对象transition_id，局部替代只影响对应对象。不存在的转移、已被禁止或已被取消的转移不再制造可替代尝试。
- 同一转移的多个替代遵守官方替代选择、适用与自重入规则；记录已应用修饰，不能因更换事件视图清空已应用记录。替代产生的另一个真实动作保留cause链，并以该动作身份记录完成；原动作被完全取代时不发布原动作complete。
- 例如“从非主牌堆进入己方废牌堆改为放逐”可统一匹配ZONE_TRANSFER.before的source/destination；这将拦截弃置等具名动作的相应入废部分。成功改为放逐后发BANISH.complete，不额外宣称原DISCARD或DIE已完成。
- 同一Board区域内的move／recall是地点变化，不伪造ZONE_TRANSFER。只有后续另行发生真实区域变化时才提供区域视图。牌堆内部排序也不算区域转移。

### 状态跨阈值

`StateTransitionSpec`字段闭集：field="might"，comparison="ge"，value为明确整数或已绑定IntExpr，direction="false_to_true"。事件仅在前值<value且后值≥value时匹配；注册时已经满足条件不会补触发，持续满足不会反复触发。BECOME_MIGHTY固定为value=5，无须另建动作函数。

- 前后值按各自时点的区域规则计算：场上用当前完整战力，非场上按印刷战力；缺值保持未知并显式报错，不能视为0或False。新实例不存在可比较的前值时不凭空制造跨阈值。
- 在每个规则可观察的实际状态变化前后，保存快照并按依赖重算连续效果，包括装备贴附／脱离、增益、强化、条件能力、控制／地点变化及持续修饰的生效／到期。只看modify_might的算术事件不足以完成此检查。
- 同一同时指令使用共同前后快照，不观察内部计算的暂态；顺序执行的两次真实状态变化分别检查，不把整条链的最终状态当作唯一后值。不为检查状态转换额外调用Cleanup。
- STATE_TRANSITION与BECOME_MIGHTY只有事后complete，不开放before、inline或EventPatch；需要改动原因动作时对真实原因动作使用替代或修饰。actor来自可确定的真实原因动作，规则到期等没有行动玩家的变化保留None。

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

## 14. V2.1入口迁移

| V2.1入口 | V3正式调用 | 必须保留 |
| --- | --- | --- |
| ready(objects, ...) | orient(objects, "ready", ...) | READY事件与实际横置→活跃结果 |
| exhaust(objects, ...) | orient(objects, "exhausted", ...) | EXHAUST事件与实际活跃→横置结果 |
| empower(objects) | change_empowerment(objects, "empower") | 默认二元、特例叠层上限、EMPOWER事件 |
| disempower(objects) | change_empowerment(objects, "disempower") | 仅移除一层、DISEMPOWER事件 |

这四个旧函数名不属于V3正式API；成本类型中的具名动作、关键词和事件仍保留原本游戏身份。其余V2.1签名保持。
