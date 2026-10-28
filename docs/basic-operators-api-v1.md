# 基本算子 API 参考

采用 Python 风格签名。`ops` 绑定当前执行上下文；下列函数是接口定义，参数中的对象均指具体实例。

## 公共类型

| 类型 | 定义 |
| --- | --- |
| `Player` | 玩家引用 |
| `Card` | 卡牌实例引用；保存拥有者，与控制者分开 |
| `Permanent` | 场上永久物，包含单位、装备等 |
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
| `Modifier` | 已登记的持续／限次修饰引用，可用于取消或关联 |
| `Link` | 同一来源能力建立的实例关联，不按卡名共享 |
| `Ability` | 完整能力定义，包含类型、条件、费用和效果 |
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
| `NumericChange` | `add`、`multiply`、`set` 三者择一；值为明确的数值表达式 |
| `ResourceChange` | 对特定产费动作的Energy／Power数量或领域修改 |
| `ChoiceBinding` | 决策者、目标、模式、其他选择及其绑定时点 |
| `SetupChoiceRef` | 对局前已保存的合法选项引用 |
| `PermissionSpec` / `RestrictionSpec` | 动作标识与时机、区域、目的地、对象、例外等明确约束 |
| `HidePermission` / `PlayPermission` | 对盖放／打出动作的具体授权，不自动绕过未覆盖限制 |
| `ShowOffRequirement` | 亮出数量、候选属性、差异性约束及相依引用 |

通用约定：

- `IntExpr` 在指定绑定时点求值；持续表达式在其依赖变化时重算，明确的快照值不重算。
- 数量、资源、伤害分配量要求非负；负战力修饰等仅在允许带符号的参数中使用。
- 普通效果尽可能执行；成本由费用流程检查并完整支付。动作未发生或未成功登记修饰时返回 `changed=False`，不伪造成功事件。
- 参数类型错误、来源数据缺失、未知规则项或未解析文本显式报错；未知数值不按零处理。
- 返回集合包含实际完成该动作的对象；被替代或失败的部分通过事件记录区分。修饰函数返回的 `Modifier` 表示登记成功，不等于被修饰事件已经发生。
- `PERMANENT` 表示没有另设到期时间，仍遵守对象离场等默认清理。跨区域引用与最后已知信息只按明确授权使用。

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

### `reveal` 展示

```python
reveal(cards: Selection[Card], *, viewers: Selection[Player] = ALL_PLAYERS,
       duration: Duration = UNTIL_EFFECT_END) -> Result[list[Card]]
```

- `viewers`：获知玩家。`duration`：公开信息保留期限。
- 返回：实际展示的牌。
- 语义：牌仍在原区域；展示状态不是新区域。自主给别人看牌不自动视为规则中的展示动作。

```python
ops.reveal(selected_cards)
```

### `choose` 选择对象

```python
choose(player: Player, candidates: Selection[T], *, minimum: IntExpr = 1,
       maximum: IntExpr = 1, targeting: bool = True,
       bind_at: str = "finalization") -> Result[list[T]]
```

- `minimum/maximum`：数量范围。`targeting`：是否正式目标。`bind_at`：`trigger`、`finalization` 或 `resolution`；必须与当前选择流程一致，不能追溯到已过去的时点。
- 返回：按选择顺序绑定的对象引用。
- 语义：决定者不必是施法者；正式目标与非目标挑选分别适用合法性、附加费用及触发规则。

```python
ops.choose(opponent, friendly_gear, targeting=False, bind_at="resolution")
```

### `declare` 宣告值

```python
declare(player: Player, options: list[T], *, minimum: int = 1, maximum: int = 1) -> Result[list[T]]
```

- `options`：允许宣告的名称、类型、领域或标签，不接受任意自由文本代替合法集合。
- 返回：宣告值，供后续步骤读取。
- 语义：不选择卡牌为目标，也不生成触发条件。

```python
ops.declare(player, [UNIT, SPELL, GEAR])
```

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
transfer(cards: Selection[Card], source: Zone, destination: Zone, *,
         order: str = "preserve") -> Result[list[Card]]
```

- `source/destination`：具体区域。`order`：`preserve`、`owner_choice` 或 `random`，仅在目的地区分次序时使用。
- 返回：实际转移的牌。
- 语义：不自动生成抽牌、弃置、摧毁、放逐或回收事件；不替代这些具名动作。

```python
ops.transfer(cards, player.trash, player.hand)
```

### `move` 移动

```python
move(objects: Selection[Permanent], destination: Location, *,
     origin: Location | None = None, simultaneous: bool = True) -> Result[list[Permanent]]
```

- `origin=None`：使用各对象绑定时的实际位置；显式起点用于检查原位置要求。
- 返回：实际完成移动的对象。
- 语义：场上地点变化，可能引起争夺或战斗；不自带横置费用，不自动改变控制权。批量与逐次移动分开。

```python
ops.move(enemy_units, battlefield)
```

### `recall` 召回

```python
recall(objects: Selection[Permanent]) -> Result[list[Permanent]]
```

- 返回：实际召回的永久物。
- 语义：移到各对象自身对应基地，不算移动，不触发移动事件，也不是回手。

```python
ops.recall(selected_units)
```

### `discard` 弃置

```python
discard(player: Player, count: IntExpr, *, cards: Selection[Card] | None = None,
        chooser: Player | None = None) -> Result[list[Card]]
```

- `cards=None`：由 `chooser` 选择合法手牌；`chooser=None` 默认由行动玩家决定。
- 返回：实际从 `player` 手牌弃入其废牌堆的牌。
- 语义：效果不足则尽可能执行；作为成本时必须满足完整支付要求。强制弃置他人选中的牌须显式绑定 `cards`。

```python
ops.discard(player, 1)
```

### `recycle` 回收

```python
recycle(cards: Selection[Card]) -> Result[list[Card]]
```

- 返回：实际回收的牌。
- 语义：进入拥有者对应牌堆底部；同时回收多张主牌堆卡时随机其牌底次序，符文牌底次序由拥有者选择。不洗整个牌堆。

```python
ops.recycle(selected_runes)
```

### `banish` 放逐

```python
banish(cards: Selection[Card], *, link: Link | None = None) -> Result[list[Card]]
```

- `link`：记录本能力放逐的具体实例。
- 返回：实际放逐的牌。
- 语义：不算摧毁或弃置；同名来源的放逐关联不共享。

```python
ops.banish(cards, link=ability_link)
```

### `burn` 燃烧

```python
burn(player: Player, count: IntExpr) -> Result[list[Card]]
```

- 返回：实际由主牌堆顶燃烧到废牌堆的牌。
- 语义：保留燃烧事件，数量不足按耗尽流程继续处理。

```python
ops.burn(player, 3)
```

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

```python
ops.hide(card, battlefield, permission=hidden_permission)
```

## 3. 打出与生成

### `play` 打出

```python
play(card: Card | TokenTemplate, player: Player, *, origin: Zone | None,
     destination: Zone | Location,
     cost_policy: CostPolicy = NORMAL_COST,
     permission: PlayPermission | None = None,
     choices: ChoiceBinding | None = None,
     entry: EntryState | None = None) -> Result[ChainItem]
```

- `cost_policy`：正常费用、替代基础费用、忽略基础费用、忽略Energy或忽略全部费用；必须区分。
- `permission`：额外时机、来源区域或目的地授权。`entry`：进入场上的朝向／状态修饰。
- 现有卡牌必须指定真实来源区域；明确要求打出新衍生物时传入 `TokenTemplate` 和 `origin=None`，由该动作在链上创建实例并定稿，不先在场上生成一次。
- 返回：完成打出定稿的链项；最终是否执行成功另由该链项的事件记录确认。
- 语义：执行正常打出流程及合法性检查。免费不自动解除目标和目的地限制；入场活跃不算后续活跃动作。

```python
ops.play(card, player, origin=player.banishment,
         destination=player.base, cost_policy=IGNORE_BASE_COST)
```

### `create` 生成

```python
create(template: CardTemplate | CopyTemplate, count: IntExpr, *,
       owner: Player, controller: Player, destination: Zone | Location,
       state: EntryState = DEFAULT_ENTRY) -> Result[list[Card]]
```

- `template`：明确卡牌模板或合法复制模板；不接受未知文字代替模板。
- 返回：新实例；同一来源连续生成的对象仍有不同实例ID。
- 语义：直接在指定位置生成，不自动视为打出。原句要求打出新衍生物时使用 `play(TokenTemplate, ..., origin=None)`；不得先生成在场上再冒充打出。

```python
ops.create(recruit_template, 2, owner=player, controller=player, destination=player.base)
```

### `add_legend` 添加传奇

```python
add_legend(player: Player, choice: SetupChoiceRef, *,
           duration: Duration, link: Link) -> Result[Legend]
```

- `choice`：关联的构筑预选项。`duration`：存在期限及离场清理条件。
- 返回：添加的传奇实例。
- 语义：不能越过预选集合，也不能在受限情况下重复创建同一已在场对象。

```python
ops.add_legend(player, chosen_legend, duration=WHILE_SOURCE_PRESENT, link=ability_link)
```

### `replace_battlefield` 替换战场

```python
replace_battlefield(target: Battlefield, template: CardTemplate, *,
                    link: Link) -> Result[Battlefield]
```

- 返回：替换后的衍生战场。
- 语义：继承原战场的相关状态、效果与引用；原牌置于放逐区但不产生普通放逐动作，不能拆成放逐后正常打出。

```python
ops.replace_battlefield(battlefield, brush_template, link=ability_link)
```

### `restore_battlefield` 恢复原战场

```python
restore_battlefield(target: Battlefield, *, link: Link) -> Result[Battlefield | None]
```

- `link`：本次替换可追溯的原战场关联。
- 返回：成功恢复的原战场；无可恢复对象时返回 `None`。
- 语义：继承替换物当前相关状态与效果；不按同名牌另找一张恢复。

```python
ops.restore_battlefield(brush, link=ability_link)
```

## 4. 状态与战力

### `exhaust` 横置

```python
exhaust(objects: Selection[Permanent], *, simultaneous: bool = True) -> Result[list[Permanent]]
```

- 返回：实际从活跃变为横置的对象。
- 语义：已横置不再变化，不重复产生横置事件；同时横置与分次横置不同。

```python
ops.exhaust(selected_units)
```

### `ready` 活跃

```python
ready(objects: Selection[Permanent], *, simultaneous: bool = True) -> Result[list[Permanent]]
```

- 返回：实际从横置变为活跃的对象。
- 语义：已活跃不产生新事件；不用于表达活跃入场。

```python
ops.ready(friendly_runes)
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
           count_each: IntExpr = 1) -> Result[CounterReceipt]
```

- 返回：各单位实际消耗数量及合计。
- 语义：只能消耗可支配的己方增益；不是给予负战力。若作为成本，必须满足完整支付要求。

```python
ops.spend_buff(player, selected_units)
```

### `stun` 眩晕

```python
stun(units: Selection[Unit]) -> Result[list[Unit]]
```

- 返回：实际新变为眩晕的单位。
- 语义：不横置、不扣战力；已眩晕不再次成功。按默认规则解除，不贡献战斗伤害但仍按正常致死要求承伤。

```python
ops.stun(enemy_units)
```

### `empower` 强化

```python
empower(objects: Selection[Permanent | Legend]) -> Result[list[Permanent | Legend]]
```

- 返回：实际新增强化状态或一层强化的对象。
- 语义：默认二元状态；明确可叠层的对象使用其上限，不把已有强化一律判为还能新增。

```python
ops.empower(selected_units)
```

### `disempower` 解除强化

```python
disempower(objects: Selection[Permanent | Legend]) -> Result[list[Permanent | Legend]]
```

- 返回：实际移除一层强化的对象。
- 语义：没有强化则不变化；存在多层时只移除一层。

```python
ops.disempower(selected_units)
```

### `modify_might` 调整战力

```python
modify_might(units: Selection[Unit], delta: IntExpr, *, duration: Duration,
             floor: IntExpr | None = None,
             ceiling: IntExpr | None = None) -> Result[list[Modifier]]
```

- `delta`：正数增加、负数减少；`floor/ceiling` 只限制本修饰，不设全局战力上下限。
- 返回：登记的战力修饰。
- 语义：保持与基础战力、增益、装备、伤害分离；按持续期及规则层应用。

```python
ops.modify_might(enemy_units, -2, duration=THIS_TURN, floor=1)
```

### `set_might` 调整至指定战力

```python
set_might(units: Selection[Unit], value: IntExpr, *,
          direction: str = "both", duration: Duration) -> Result[list[Modifier]]
```

- `direction`：`increase_only`、`decrease_only` 或 `both`。
- 返回：按执行时数值差建立的修饰。
- 语义：“提高至”不得降低；持续期内保留该差值效果，不擅自抹除其他战力来源。

```python
ops.set_might(selected_units, 5, direction="increase_only", duration=THIS_TURN)
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

### `swap_might` 交换战力

```python
swap_might(first: Unit, second: Unit, *, duration: Duration) -> Result[list[Modifier]]
```

- 返回：两个按执行时战力差计算的修饰；数值相同时无实际变化。
- 语义：交换结果通过增减修饰实现，不交换装备、计数物或其他战力来源。

```python
ops.swap_might(first_unit, second_unit, duration=THIS_TURN)
```

## 5. 伤害与摧毁

### `damage` 造成伤害

```python
damage(units: Selection[Unit], amount: IntExpr, *, source: Source = SOURCE,
       mode: str = "each", allocation: dict[Unit, int] | None = None,
       use_all: bool = True, simultaneous: bool = True) -> Result[DamageReceipt]
```

- `mode="each"`：每个对象各受到 `amount`。`mode="split"`：`amount` 是总池，必须指定合法分配方案。
- `allocation`：各对象分配量，非负整数；`use_all=True` 要求用完总池，假则总量不得超过池。实际伤害仍受修饰和预防影响。
- 返回：每个对象的分配量、修饰后量、实际伤害、来源与事件关联。
- 语义：伤害不直接扣战力；正伤害、分配伤害、过量伤害与死亡分别记录。`amount=0` 不产生实际伤害事件。

```python
ops.damage(enemy_units, 2)
ops.damage([a, b], 5, mode="split", allocation={a: 2, b: 3})
```

### `prevent_damage` 预防伤害

```python
prevent_damage(units: Selection[Unit], amount: IntExpr | Infinity, *,
               source_filter: Predicate = ANY_SOURCE,
               duration: Duration) -> Result[list[Modifier]]
```

- `amount`：每个对象的可预防额度；无限表示全部。`source_filter`：受影响来源。
- 返回：各对象的延迟伤害替代记录。
- 语义：额度按实际预防量消耗；全部预防不算造成伤害，不是无效化整张法术或能力。

```python
ops.prevent_damage(selected_units, 3, duration=THIS_TURN)
```

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
     simultaneous: bool = True) -> Result[list[Card]]
```

- 返回：实际因本动作死亡、由场上进入废牌堆的牌。
- 语义：先处理替代效果；保留责任来源及死亡前信息。死亡被改成召回时，不返回该对象为已摧毁，也不触发其死亡能力。

```python
ops.kill(enemy_units)
```

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
          mode: str = "replace", duration: Duration) -> Result[list[Modifier]]
```

- `mode`：`add`、`remove` 或 `replace`。
- 返回：类型修饰。
- 语义：类型是集合；变成单位兼装备不能丢掉装备类型，相关贴附与状态规则仍执行。

```python
ops.set_types([gear], {UNIT}, mode="add", duration=WHILE_SOURCE_PRESENT)
```

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

```python
ops.pay(player, cost, binding=ability_cost_binding)
```

### `modify_cost` 调整费用

```python
modify_cost(subjects: CostSelection, change: CostChange, *,
            duration: Duration, uses: int | None = None) -> Result[Modifier]
```

- `change`：明确的基础替代、额外成本、Energy／Power增减、领域限制或忽略政策；各字段分开。
- `uses`：适用次数，`None` 表示期限内不限次。
- 返回：费用修饰。
- 语义：不修改印刷费用，不返还已付资源；任意领域Power折扣不得擅自扣指定领域需求。

```python
ops.modify_cost(next_spell, CostChange(energy_delta=-2), duration=THIS_TURN, uses=1)
```

### `gain_xp` 获得经验

```python
gain_xp(player: Player, amount: IntExpr) -> Result[int]
```

- 返回：实际增加的XP。
- 语义：独立于资源和分数；等级相依能力按新XP重新判断。

```python
ops.gain_xp(player, 2)
```

### `spend_xp` 消耗经验

```python
spend_xp(player: Player, amount: IntExpr) -> Result[int]
```

- 返回：实际消耗的XP。
- 语义：不能消耗不存在的XP；作为成本时按完整支付要求检查，等级相依能力可能因此失效。

```python
ops.spend_xp(player, 2)
```

### `gain_points` 获得分数

```python
gain_points(player: Player, amount: IntExpr, *,
            source: Source = SOURCE, cause: PointCause = CARD_EFFECT) -> Result[int]
```

- `cause`：实际增分来源，用于适用相应限制和替代。
- 返回：实际增加分数；被替代为其他动作的部分单独记录。
- 语义：不伪造征服、据守或Scored事件；最后一分限制按来源判断。

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

- `key` 与 `change` 按下表匹配，类型不匹配或未知键显式拒绝。
- 返回：具体规则项修饰，不接受原始自然语言作为可执行内容。

| `RuleKey` | `RuleChange` |
| --- | --- |
| `VICTORY_THRESHOLD` | 胜利分数增减值 |
| `HIDDEN_CAPACITY` | 指定玩家／战场盖放容量增减值 |
| `STARTING_BATTLEFIELD_ELIGIBILITY` | 是否允许作为开局战场 |
| `COMBAT_DAMAGE_ORDER` | 同控制者范围内先／正常／后分配致死伤害 |
| `LETHAL_DAMAGE_POLICY` | 指定来源的正伤害是否视为致死 |
| `EMPOWER_LIMIT` | 强化层数上限 |
| `BUFF_LIMIT` | 增益数量上限 |
| `CHANNEL_PHASE_COUNT` | 召出阶段的符文数量，不修改其他召出来源 |
| `DECK_NAME_LIMIT` | 构筑同名上限 |
| `GEAR_RECALL_POLICY` | 非单位装备在清理中的召回条件 |

```python
ops.modify_rule(BUFF_LIMIT, this_unit, RuleChange(set=INFINITY),
                 duration=WHILE_SOURCE_PRESENT)
```

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

### `execute_effect` 执行指定能力效果

```python
execute_effect(source: Permanent | Battlefield, ability: AbilityRef, *,
                count: IntExpr = 1) -> Result[list[ChainItem]]
```

- `ability`：原对象明确的能力引用，如征服效果；不得用未知文字代替。
- 返回：按指令创建的待处理能力项，定稿和执行仍遵守对应流程。
- 语义：不伪造原触发事件，不自动增分或改变战场控制权。

```python
ops.execute_effect(battlefield, battlefield.conquer_effect)
```

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
