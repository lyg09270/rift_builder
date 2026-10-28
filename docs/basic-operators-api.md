# 基本算子 API 参考 V4

日期：2026-10-28。共 **60个正式函数**，保留具名游戏动作与修饰。调用使用`ops`；选择、付款、批次、记忆及调度交给[卡牌模型](card-model.md)和[V4程序与流程契约](card-resolution-v4.md)。

## 公共约定

- 签名采用Python风格，定义文档接口。`SOURCE`、`CONTROLLER`来自本次结算上下文；拥有者、控制者、行动者与决策者分别保存。有明确行动玩家的动作按自身规则归属，不一律归能力控制者。
- `Selection[T]`是已绑定对象集合或获授权的动态选择器；正式目标在定稿选择、结算重检。`ObjectRef`保存实例引用与区域变更身份，不凭卡名重新寻找对象。
- `IntExpr`／`Predicate`为已解析表达式；显式区分快照与实时求值。未知值不当零，隐藏信息不越权读取，未知类型、键或文本显式拒绝。
- `Duration`包括`PERMANENT`、`THIS_TURN`、`THIS_COMBAT`、`WHILE_SOURCE_PRESENT`、`WHILE(condition)`、`UNTIL(event)`及`UNTIL_EFFECT_END`。期限附在相应效果上，不能补触发已经过去的时点。
- `Result[T]`保存`value`、实际事件和逐部分回执；回执区分实际执行、被忽略、被阻止／替代。集合只含实际完成对象，未完成可为None或空集合；是否支付费用另查PaymentReceipt，不用统一changed布尔值代替。
- 每个集合动作默认表示一条指令中的同批对象。跨调用的同时动作使用`Batch`节点，顺序逐对象动作使用`ForEach`；算子不再携带simultaneous开关。批次提交不提前执行Cleanup。
- 所有实际动作由流程发布具名事件、相关区域事件及必要的状态转换；使用者不能手工补造事件。动作身份、共享转移ID、替代去重和阶段沿用[V4事件契约](card-resolution-v4.md#事件契约)。
- `Permanent`为场上单位／装备；`Orientable`含单位、装备、符文、传奇；`Location`为基地／战场，`Zone`为区域。模板、费用、复制特征与收据的具名结构均须完整解析，不能以自然语言代替。

| 返回结构 | 字段 |
| --- | --- |
| Result[T] | value:T或None、parts:list[ActionReceipt]、events:list[EventRef] |
| ActionReceipt | 对象引用、requested、actual、status=executed／ignored／negated、replacement_trace、action_id及相关transition_id；部分成功拆分记录 |
| Modifier | 本次来源、主体、规则层、期限及具体修饰ID；供end_modifier精确结束 |

表中actual记录真实结果；status与替代轨迹共同解释未发生部分。支付是否视为完成另存PaymentReceipt，不由actual的真假推断。

## 1. 信息

### `draw` 抽牌

```python
draw(player: Player, count: IntExpr = 1, *, cards: Selection[Card] | None = None) -> Result[list[Card]]
```

正常抽主牌堆顶部；指定cards必须有特殊抽取授权，数量与count相符。返回实际抽牌，保留DRAW及耗尽流程，不等于普通回手。

### `look` 查看

```python
look(player: Player, zone: Zone, count: IntExpr | All, *, position: str = "top") -> Result[list[Card]]
```

position仅top／bottom，ALL表示整个区域。只向player授权信息，不公开、不转移区域；不足只看现有牌。

### `reveal` 展示

```python
reveal(cards: Selection[Card] | None = None, *, actor: Player = CONTROLLER,
       viewers: Selection[Player] = ALL_PLAYERS, duration: Duration = UNTIL_EFFECT_END,
       zone: Zone | None = None, count: IntExpr | All | None = None,
       until: Predicate | None = None, include_match: bool = True) -> Result[RevealReceipt]
```

显式cards与zone模式互斥；zone模式逐张展示，until只检查已展示对象，count为上限。返回cards、matched及信息范围，不预读后续牌。as_each内联入口按流程处理。

## 2. 区域与地点

### `transfer` 普通区域转移

```python
transfer(cards: Selection[Card], source: Zone | ZoneMap, destination: Zone | ZoneMap, *,
         order: str = "preserve", position: str | None = None,
         actor: Player = CONTROLLER) -> Result[list[Card]]
```

ZoneMap按实例指定区域；position仅None／top／bottom，顶底要求有序牌堆；order仅preserve／chosen／random，chosen须有已绑定排列。动作身份固定ZONE_TRANSFER，不能冒充抽牌、弃置、死亡或燃烧；去不同拥有者手牌等可同批完成。

### `move` 移动

```python
move(objects: Selection[Permanent], destination: Location | LocationMap, *,
     origin: Location | LocationMap | None = None, actor: Player = CONTROLLER,
     join: EventRef | None = None) -> Result[list[Permanent]]
```

读取共同出发快照后同批变位，可交换位置；不自带普通移动横置费用，不改变控制者。join只可加入规则明确授权且尚未提交的原移动，不将事后触发塞回原批次。

### `recall` 召回

```python
recall(objects: Selection[Permanent], *, actor: Player = CONTROLLER) -> Result[list[Permanent]]
```

送回各自当前控制者基地；不算move、不受移动限制阻止、不回手，也不自动活跃。

### `discard` 弃置

```python
discard(player: Player, count: IntExpr, *, cards: Selection[Card] | None = None) -> Result[list[Card]]
```

从player手牌弃入对应废牌堆。cards=None由统一选择流程让player选择；其他决策者须先用Choose绑定cards。效果不足尽可能执行，费用按完整支付规则检查；同一指令保留一次集合事件和逐牌结果。

### `recycle` 回收

```python
recycle(cards: Selection[Card], *, actor: Player = CONTROLLER) -> Result[list[Card]]
```

回各拥有者对应牌堆底；主牌同时回收多张按规则随机次序，符文按拥有者决定次序。不洗整个牌堆，不自动改写行动玩家。

### `banish` 放逐

```python
banish(cards: Selection[Card | ChainItem], *, link: Link | None = None,
       actor: Player = CONTROLLER) -> Result[list[Card]]
```

保留实际来源和实例关联；链项须有对应card，纯能力项不能作为卡放逐。不算摧毁、弃置或counter，实际放逐与被替代部分分开记录。

### `burn` 燃烧

```python
burn(player: Player, count: IntExpr, *, cards: Selection[Card] | None = None) -> Result[list[Card]]
```

正常燃烧主牌堆顶并处理耗尽。指定cards仅用于获授权的明确剩余顶牌，count须相符，不补烧原集合以外的新牌；非顶部来源拒绝。

### `channel` 召出符文

```python
channel(player: Player, count: IntExpr, *, exhausted: bool = False) -> Result[list[Rune]]
```

从符文牌堆顶召出现有数量；exhausted指定入场朝向，不另发READY／EXHAUST事件。返回原指令实际召出的符文，替代额外添加对象另保留归因。

### `reorder` 调整次序

```python
reorder(cards: Selection[Card], zone: Zone, *, position: str,
        order: OrderSpec = KEEP_ORDER) -> Result[list[Card]]
```

position仅top／bottom；OrderSpec仅KEEP_ORDER、RANDOM_ORDER或已绑定的完整排列。需要玩家排序时先用Choose(kind="order")，本动作不额外查看、展示或回收。

### `hide` 盖放

```python
hide(card: Card, battlefield: Battlefield, *, permission: HidePermission,
     link: Link | None = None) -> Result[Card]
```

permission完整定义来源、容量、控制条件、费用绑定、未来打出与失控处理；统一盖放流程付费一次。实际盖放发HIDE.complete，不发PLAY、不开放普通打出反应链，不公开隐藏属性。

## 3. 打出与生成

### `play` 打出

```python
play(card: Card | TokenTemplate | CopyTemplate, player: Player, *, origin: Zone | None,
     destination: Zone | Location, cost_policy: CostPolicy = NORMAL_COST,
     permission: PlayPermission | None = None, choices: ChoiceBinding | None = None,
     entry: EntryState | None = None, link: Link | None = None) -> Result[PlayReceipt]
```

委托统一打出流程建立pending项；不会在当前指令处擅自完成其结算。现有牌须真实origin，新衍生物／副本模板使用None。PlayReceipt提供item/card等关联引用，不将未入场card当现存Unit。

choices只提供流程允许的预绑定或相依约束，不跳过最终选择与合法性检查。IGNORE_BASE_COST只忽略基础费用；来源权限、额外费用与目标仍分别检查。链上重打自己须明确授权并创建新item，不能用复制代替。

### `create` 生成

```python
create(template: CardTemplate | CopyTemplate | SetupChoiceRef, count: IntExpr, *,
       owner: Player, controller: Player | None, destination: Zone | Location,
       state: EntryState = DEFAULT_ENTRY, duration: Duration = PERMANENT,
       link: Link | None = None) -> Result[CreateReceipt]
```

生成新实例，收据含cards/units/gear/runes/legends/battlefields视图。战场controller为None，其他初始控制者默认遵从拥有者规则，例外须授权。SetupChoiceRef验证构筑预选及剩余对象；到期按创建授权移除／恢复，不任意摧毁。要求“打出”的衍生物用play。

### `replace_battlefield` 替换／恢复战场

```python
replace_battlefield(target: Battlefield, template: CardTemplate | None = None, *,
                    mode: str = "replace", link: Link) -> Result[Battlefield | None]
```

replace须模板；restore须None并读取同次link暂存的原牌。继承对应状态与引用，不凭同名新建原牌，不制造普通放逐事件。

## 4. 状态、战力与伤害

### `orient` 活跃／横置

```python
orient(objects: Selection[Orientable], state: str, *,
       actor: Player = CONTROLLER) -> Result[list[Orientable]]
```

state仅ready／exhausted，分别保留READY／EXHAUST动作身份；已处目标朝向不重复成功。入场朝向使用entry，不调用本动作模拟入场。

### `buff` 给予增益

```python
buff(units: Selection[Unit]) -> Result[list[Unit]]
```

默认每次一个、每单位至多一个，每个贡献+1战力；明确上限或贡献修饰分别适用。返回实际新获增益者，未新增不发BUFF完成事件。

### `spend_buff` 消耗增益

```python
spend_buff(player: Player, units: Selection[Unit], *,
           count_each: IntExpr | dict[Unit, int] = 1) -> Result[CounterReceipt]
```

只消耗player控制单位的增益，同批记录各对象实际数量、计数物引用及总计。发SPEND_BUFF，不能将离场清除或BUFF获得当成消耗；费用完整性由费用流程检查。

### `stun` 眩晕

```python
stun(units: Selection[Unit]) -> Result[list[Unit]]
```

实际新增眩晕，不横置或减战力；已眩晕／禁止眩晕者不生成再次眩晕尝试。选中合法不保证动作成功。

### `change_empowerment` 强化／解除一层强化

```python
change_empowerment(objects: Selection[Permanent | Legend], mode: str, *,
                   actor: Player = CONTROLLER) -> Result[list[Permanent | Legend]]
```

mode仅empower／disempower，分别保留EMPOWER／DISEMPOWER身份。默认二元；明确可叠层时按其上限，每次至多增减一层，解除一层不等于全部清空。

### `modify_might` 给予战力变化

```python
modify_might(units: Selection[Unit], delta: IntExpr | None = None, *,
             change: MightChange | None = None, duration: Duration,
             floor: IntExpr | None = None, ceiling: IntExpr | None = None) -> Result[list[Modifier]]
```

delta为add简写，与change互斥。MightChange为add(delta)、set(value,direction)或swap(other)；direction仅both／increase_only／decrease_only。set/swap取共同快照算差值，不持续锁定最终战力；swap要求units恰一名。

即时给予的非零差值生成MIGHT_CHANGE；各差值替代互不回算。持续入口登记战力贡献，依赖重算不伪造新的给予动作。floor/ceiling只限制本修饰；基础战力、装备贡献、增益贡献分别由set_base_might、modify_equipment_bonus、modify_buff_value处理。

### `damage` 造成伤害

```python
damage(units: Selection[Unit], amount: IntExpr, *, source: Source = SOURCE,
       mode: str = "each", allocation: dict[Unit, int] | None = None,
       use_all: bool = True, actor: Player = CONTROLLER) -> Result[DamageReceipt]
```

each每目标独立同值；split为总池，allocation明确各目标分配，use_all指定是否必须用尽。Bonus分别作用各独立实例或一个分配池；不同数值／来源的同指令伤害用Batch。明确由单位造成时actor须绑定该单位控制者。

返回分配、修饰后、实际、过量及来源；0不发实际伤害事件。伤害不扣战力，致死由规则清理确认，不能按damage返回值立即摧毁。

### `heal` 治疗

```python
heal(units: Selection[Unit]) -> Result[HealReceipt]
```

清除已有伤害，返回实际清除量；不增加战力，不凭无伤害对象伪造治疗数量。

### `kill` 摧毁

```python
kill(objects: Selection[Permanent], *, source: Source = SOURCE,
     actor: Player = CONTROLLER) -> Result[list[Card]]
```

处理死亡替代后返回本动作实际死亡的牌，保存死亡前信息。被召回或其他动作替代的部分不能计为死亡；与放逐、弃置分开。

## 5. 装备、控制、复制与能力

### `attach` 贴附

```python
attach(gear: Gear, host: Unit) -> Result[Attachment]
```

建立宿主关系，处理旧贴附、宿主获授文本和武装贡献；同宿主不重复成功。不自付Equip费用，不算移动／活跃。

### `detach` 卸除

```python
detach(gear: Selection[Gear]) -> Result[list[Gear]]
```

解除关系及对应武装贡献／授予文本，恢复装备自身文本；后续位置与召回由规则处理。

### `change_control` 改变控制

```python
change_control(objects: Selection[Permanent | ChainItem], player: Player, *,
               duration: Duration = PERMANENT, link: Link | None = None) -> Result[list[Modifier]]
```

登记控制权修饰；拥有者不变，不自动移位或重选目标。归还通过结束具体修饰并重新计算控制关系。

### `end_modifier` 结束具体修饰

```python
end_modifier(modifiers: Selection[Modifier], *, link: Link | None = None) -> Result[list[Modifier]]
```

立即结束已取得且获授权的具体修饰引用，不按卡名删除所有来源，不撤销已发生动作。已失效不重复成功；控制权恢复取当前规则结果。

### `copy` 复制特征

```python
copy(target: Permanent, original: Permanent, *, traits: CopyTraits = COPYABLE_TRAITS,
     duration: Duration) -> Result[Modifier]
```

修改现有实例的可复制特征；不默认复制伤害、计数物、临时修饰或控制权。新复制体用CopyTemplate配合play／create。

### `copy_text` 复制文本字段

```python
copy_text(target: Permanent, original: Permanent, *, from_field: str,
          to_field: str, duration: Duration, link: Link | None = None) -> Result[Modifier]
```

字段仅rules_text／effect_text。按明确取值时点、复制层、第一人称和依赖处理，不递归拼接自身获得文本。

### `copy_abilities` 取得能力集合

```python
copy_abilities(target: Permanent, originals: Selection[Permanent | Legend], *,
               ability_filter: Predicate, duration: Duration) -> Result[list[Modifier]]
```

筛选如包含横置费用的主动能力，保留原能力身份和来源绑定；originals可动态求值，须防止无限派生自复制。

### `grant_ability` 赋予能力

```python
grant_ability(objects: Selection[Permanent | Card], ability: AbilitySpec, *,
              duration: Duration, link: Link | None = None) -> Result[list[Modifier]]
```

将完整能力加入对象的能力集合，不立即执行能力体。与仅登记一项作用域内延迟监听的Register节点区分。

### `suppress_ability` 使能力失活

```python
suppress_ability(objects: Selection[Permanent | Card], ability_filter: Predicate, *,
                 duration: Duration) -> Result[list[Modifier]]
```

只抑制匹配能力，不删除无关文本、类型或战力；期限结束重新判断是否有效。

### `grant_keyword` 赋予关键词

```python
grant_keyword(objects: Selection[Permanent | Card], keyword: Keyword, *,
              parameters: KeywordParameters = EMPTY, duration: Duration) -> Result[list[Modifier]]
```

保留关键词身份、参数、可叠加规则和对应宏；授予不等于执行其能力。固有关键词只展开一次。

### `set_types` 修改类型集合

```python
set_types(objects: Selection[Permanent | Card], types: set[CardType], *,
          mode: str = "replace", duration: Duration) -> Result[TypeChangeReceipt]
```

mode仅add／remove／replace。返回修饰和当前units／gear视图；类型改变后按新类型重检，不在变更前强制转型。

### `set_tags` 修改标签集合

```python
set_tags(objects: Selection[Permanent | Card], tags: set[Tag], *,
         mode: str = "add", duration: Duration) -> Result[list[Modifier]]
```

mode仅add／remove／replace；只改玩法标签，不改卡名，动态集合保留依赖。

## 6. 资源、分数与流程动作

### `add_resources` 产费

```python
add_resources(player: Player, resources: ResourceBundle, *,
              restriction: Predicate = UNRESTRICTED,
              expires: ResourceExpiry = NORMAL_POOL_EXPIRY) -> Result[ResourceReceipt]
```

ResourceBundle为Energy及分领域Power数量，均非负；返回独立来源、限制和到期批次。产费不等于减费，不自动横置／回收符文。

### `change_xp` 获得／消耗经验

```python
change_xp(player: Player, amount: IntExpr, *, mode: str = "gain") -> Result[int]
```

mode仅gain／spend，amount非负，分别保存事件身份；spend不足失败，费用完整性另由Pay流程检查，实际变化后重算等级。

### `gain_points` 获得分数

```python
gain_points(player: Player, amount: IntExpr, *, source: Source = SOURCE,
            cause: PointCause = CARD_EFFECT) -> Result[int]
```

cause仅HOLD／CONQUER／CARD_EFFECT。处理合法增分尝试、最后一分与替代，不伪造征服／据守／Scored；替代增分不取消已发生的战场得分记录。

### `win` 获胜

```python
win(player: Player, *, authorization: WinAuthorization) -> Result[GameOutcome]
```

authorization须指向已满足条件的明确规则或卡牌效果，不是任意布尔值，也不等同加分。

### `counter` 无效化

```python
counter(item: ChainItem, *, destination: Zone | None = None) -> Result[ChainItem]
```

实际无效化后不执行原效果，不返还已付费用；destination指定正常离链之外的授权区域，仍处理Flow等替代，不产生成功结算事件。

### `redo_choices` 重做链项选择

```python
redo_choices(item: ChainItem, player: Player, *,
             fields: set[ChoiceField] = ALL_ALLOWED_CHOICES) -> Result[ChoiceBinding]
```

这是卡牌明确授权改变已有选择的游戏动作；普通Choose只能作本次合法选择。fields限定目标／模式／其他合法选择，不自动改变控制者或重复付费。

### `skip_procedure` 跳过指定流程

```python
skip_procedure(player: Player, procedure: ProcedureRef, *,
               occurrence: str = "next", duration: Duration) -> Result[Modifier]
```

procedure为明确回合／阶段／步骤，occurrence仅next／all_matching。登记跳过，不发生的流程不产生发生触发；与调度器正常推进区分。

### `extra_turn` 追加回合

```python
extra_turn(player: Player, count: IntExpr = 1, *,
           after: TurnRef = CURRENT_TURN) -> Result[list[TurnRef]]
```

按指定锚点插入完整回合，不默认自然轮转末尾，不提前执行追加回合或延迟当前后续指令。

## 7. 具名修饰

下列函数分别定义作用对象、规则层和事件含义，不使用通用modify入口。持续修饰返回具体Modifier引用；登记成功不等于未来动作已经发生。

### `set_base_might` 修改基础战力

```python
set_base_might(units: Selection[Unit], value: IntExpr, *,
               duration: Duration) -> Result[list[Modifier]]
```

只改基础战力层，装备、增益和其他修饰仍按层应用，不等于给予同数值战力变化。

### `modify_equipment_bonus` 修改武装贡献

```python
modify_equipment_bonus(gear: Selection[Gear], change: NumericChange, *,
                       duration: Duration) -> Result[list[Modifier]]
```

只改装备赋予宿主的战力贡献，保留宿主关系与依赖重算，不能改写成普通宿主战力修饰。

### `modify_buff_value` 修改增益贡献

```python
modify_buff_value(units: Selection[Unit], delta_each: IntExpr, *,
                  duration: Duration) -> Result[list[Modifier]]
```

改变每个增益的战力贡献，不增加或消耗计数物，也不改变增益数量上限。

### `modify_keyword` 修改关键词数值

```python
modify_keyword(objects: Selection[Permanent | Card], keyword: Keyword, *,
               parameter: str, operation: str, value: IntExpr,
               duration: Duration) -> Result[list[Modifier]]
```

本版登记Assault.value和Shield.value，operation仅add／multiply／set。关键词对应的角色条件保持有效；未登记字段拒绝，费用调整使用modify_cost。

### `modify_cost` 调整费用

```python
modify_cost(subjects: CostSelection, change: CostChange, *, duration: Duration,
            limit: UsageLimit | None = None, link: Link | None = None) -> Result[Modifier]
```

CostChange只含energy_delta、power_discount、power_add、base_replace、ignore_base、ignore_energy、additional_actions。保留替代基础费、额外费与目标附加费的角色，不改印刷费、不返还已付费用；可选分支关联选择和付款回执。次数只用limit，不另设uses简写。

### `modify_damage` 修改伤害

```python
modify_damage(events: DamageSelection, change: NumericChange, *,
              duration: Duration, limit: UsageLimit | None = None) -> Result[Modifier]
```

仅修改匹配来源／受害对象的伤害加值、倍数或设值，不立即造成伤害。NumericChange仅add／multiply／set三者择一；预防用prevent_damage。

### `prevent_damage` 预防伤害

```python
prevent_damage(units: Selection[Unit], amount: IntExpr | Infinity, *,
               source_filter: Predicate = ANY_SOURCE, duration: Duration,
               limit: UsageLimit | None = None) -> Result[list[Modifier]]
```

各对象有独立剩余预防量，按实际预防量扣减；INFINITY表示不限量。limit另限事件次数，须明确damage_event或instruction_batch及逐目标／共享作用域，不将“下一次”扩成全回合。

### `modify_effect_value` 修改已登记效果参数

```python
modify_effect_value(effects: EffectSelection, parameter: EffectParameter,
                    change: NumericChange, *, duration: Duration) -> Result[Modifier]
```

本版parameter仅REDUCTION_AMOUNT，表示匹配指令的负战力幅度；不按文本位置修改任意数字。新增字段须明确注册规则含义。

### `modify_trigger_count` 增加触发次数

```python
modify_trigger_count(triggers: TriggerSelection, extra: IntExpr, *,
                     duration: Duration) -> Result[Modifier]
```

extra非负，只增加指定能力的触发实例数，不重打来源牌，不与程序内部Repeat或每回合额度混用。

### `modify_trigger_events` 扩展触发类别

```python
modify_trigger_events(abilities: AbilitySelection, add: set[EventKind], *,
                      duration: Duration) -> Result[list[Modifier]]
```

add仅HOLD／CONQUER；保留原来源、程序及条件，同一实际事件不重复登记，不生成额外play效果。

### `modify_resource_output` 修改产费

```python
modify_resource_output(actions: ResourceActionSelection, change: ResourceChange, *,
                       duration: Duration) -> Result[Modifier]
```

ResourceChange为energy_delta及明确的分领域Power增量／领域替换；仅改指定产费动作，保留资源来源、限制与到期，不直接修改池内现存资源。

### `modify_entry` 修改未来入场状态

```python
modify_entry(subjects: EntrySelection, state: EntryState, *, duration: Duration,
             limit: UsageLimit | None = None, link: Link | None = None) -> Result[Modifier]
```

限定对象、来源与目的地，改变未来入场朝向／明确授权初态；不发READY／EXHAUST。entered范围不能擅自缩成仅play，下一次／同批数量按limit明确计数。

### `grant_permission` 赋予动作权限

```python
grant_permission(subjects: PermissionSelection, permission: PermissionSpec, *,
                 duration: Duration, limit: UsageLimit | None = None) -> Result[Modifier]
```

只扩展指定动作时机、来源、目的地或合法选择，不绕过硬性禁止与费用。次数统一用limit，默认不额外限次。

### `restrict_action` 禁止明确动作

```python
restrict_action(subjects: PermissionSelection, restriction: RestrictionSpec, *,
                duration: Duration) -> Result[Modifier]
```

限制指定动作、对象、来源与例外；禁止被选不等于免疫所有效果，禁止增分不等于取消据守／征服。正向位置要求使用modify_rule的专门键。

### `modify_rule` 修改已登记规则项

```python
modify_rule(key: RuleKey, scope: RuleScope, change: RuleChange, *,
            duration: Duration) -> Result[Modifier]
```

仅接受下表注册键及对应字段；不能用任意规则名、属性路径或自然语言扩充行为。RuleScope按players／objects／locations／cards／link／filter限定范围，各key要求对应主体，无关字段拒绝。

| RuleKey | RuleChange允许字段 |
| --- | --- |
| VICTORY_THRESHOLD | delta／set |
| HIDDEN_CAPACITY | 玩家／战场范围与delta |
| STARTING_BATTLEFIELD_ELIGIBILITY | eligible布尔 |
| COMBAT_DAMAGE_ORDER | order=first／normal／last、assignment_player、ignore_keywords仅Tank／Backline；只改指定分配者的承伤顺序，不删除关键词 |
| LETHAL_DAMAGE_POLICY | sources、positive_damage_is_lethal |
| EMPOWER_LIMIT / BUFF_LIMIT | limit非负整数或INFINITY |
| CHANNEL_PHASE_COUNT | set；只改阶段基础召出量 |
| DECK_NAME_LIMIT | name、set |
| GEAR_RECALL_POLICY | 明确单位／非单位装备条件及recall_required布尔 |
| PLAY_LOCATION_REQUIREMENT | play_constraint:PlayConstraint |

PlayConstraint保存destinations、when、grant_destination、payment_binding：在选择阶段按已声明费用分支启用正向要求；相容要求共同满足，冲突要求选择极大相容组。禁止／only始终强制检查；付款仍在正常阶段完成。实际入场替代另行处理，不回写原选择位置。

```python
ops.set_base_might([unit], 3, duration=THIS_TURN)
ops.modify_damage(friendly_spell_damage, NumericChange(add=1), duration=THIS_TURN)
```

