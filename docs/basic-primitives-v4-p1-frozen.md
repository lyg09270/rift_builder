# 底层原语草案 V4-P1

日期：2026-10-28。试拆为 **35个底层原语**，使用`p`命名空间；[现行V4](basic-operators-api-v4.md)的60个接口保留为对照。本草案是文档设计，尚未实现执行引擎。

```text
卡牌模型 → 具名规则模板 → 底层原语
```

规则模板负责权限、费用、替代、事件身份和期限；原语更新受控的状态结构。编译后的增益与摧毁等模板可以共享状态机制，各自规则仍独立存在。[全部60项映射及边界示例](card-api-primitives-v4-p1.md)

## 公共约定

- `p`绑定当前ActionFrame，内含模板身份、来源、玩家、已选对象、快照和作用域。调用者不能用任意identity字符串制造抽牌或死亡事件；原语变更与真实回执交给共同流程产生正确事件。
- 卡牌程序的Call先绑定具名模板，再展开为`p`调用。原语不绕过定稿、费用与替代；没有对应阶段授权的裸状态写入拒绝。选择、付款、批次、绑定、登记和pending调度继续使用[V4程序节点](card-resolution-v4.md)。
- `Selection`、`IntExpr`、`Duration`、来源／拥有者／控制者等采用V4定义。所有参数须有结构化定义；未知数值或规则拒绝，不能填零或自然语言占位。
- Result保留实际值、对象、数值、逐部分状态及原因关联。EffectHandle是带来源、主体、作用域和期限的登记记录；结束记录后重新计算，不恢复一个可能过时的旧值。
- 同时变化使用共同快照，同批提交后由规则调度清理。p调用不会递归执行新pending或提前Cleanup；规则自动清理与调度不计为卡牌效果原语。
- 条件使用显式All/Any/Not和类型化比较，分别绑定入口、指令或持续求值时点；不以复制同一操作模拟OR。替代先于提交，不用事后数值UNDO冒充规则替代。带选择／随机的重放输入包含选择记录、随机流和规则版本。

结构化效果与条件组织参考了本地[SES资料](references/card-effect-models/README.md)；采用范围及不适用算法已单独记录。

## 1. 实例、区域与地点（5）

### `instantiate` 建立新实例

```python
instantiate(template: EntityTemplate, count: IntExpr, *, owner: Player,
            controller: Player | None, initial: EntryState = DEFAULT_ENTRY) -> Result[list[StagedInstance]]
```

创建唯一身份的待提交实例。StagedInstance可传给本次zone_change或battlefield_bind，尚不算已入场；不虚构此前区域。初始控制、模板数据和新副本的可复制范围由模板校验，不提前触发入场能力。

### `zone_change` 区域归属变更

```python
zone_change(objects: Selection[Card | StagedInstance], source: Zone | ZoneMap | None,
            destination: Zone | ZoneMap, *, position: str | None = None,
            order: OrderSpec = KEEP_ORDER, entry: EntryState | EntryMap | None = None,
            entry_location: Location | LocationMap | None = None) -> Result[list[Card]]
```

同批改变区域归属，保留每对象transition_id及区域变更身份；source=None仅允许本次新实例。position仅None/top/bottom。抽牌、弃置、死亡等身份来自ActionFrame；本函数不决定耗尽、回收次序或死亡触发规则。entry和entry_location仅用于真正进入Board时原子绑定初态与位置，不另造移动或活跃事件；OrderSpec可按各目的牌堆分别绑定。

### `location_change` 场上地点变更

```python
location_change(objects: Selection[Permanent], destination: Location | LocationMap, *,
                origin: Location | LocationMap | None = None) -> Result[list[Permanent]]
```

更新Board内地点；移动与召回共享此机制，分别由模板检查限制和发布事件。保存共同出发快照，不修改控制者，不自动活跃或横置。

### `order_change` 有序区域重排

```python
order_change(cards: Selection[Card], zone: Zone, *, position: str,
             order: OrderSpec) -> Result[list[Card]]
```

position仅top/bottom，order为保持、随机或已合法绑定排列。重排不变更区域、不授权查看，也不假造回收；选择和随机策略来自模板。

### `battlefield_bind` 替换／恢复战场槽位

```python
battlefield_bind(slot: BattlefieldSlot, replacement: Battlefield | StagedInstance | None, *,
                 mode: str, link: Link) -> Result[Battlefield | None]
```

mode仅replace/restore；替换保存原对象及继承状态，恢复只取同次link暂存对象。新对象必须为战场。此特殊关系更新暂保留独立原语，不伪装成普通区域转移。

## 2. 状态、数量与属性（5）

### `orientation_set` 设置朝向

```python
orientation_set(objects: Selection[Orientable], state: str) -> Result[list[Orientable]]
```

state仅ready/exhausted；实际变化者才返回。入场朝向放在initial／入场规则中，不以一次横置／活跃动作模拟。

### `status_set` 设置有限状态

```python
status_set(objects: Selection[Card], status: str, value: bool) -> Result[list[Card]]
```

本版仅STUNNED（场上单位）和FACE_DOWN（获授权的卡牌展示状态），分别检查主体类型与阶段。它不接受任意属性路径；解除眩晕与新施加眩晕保留不同原因，盖放展示状态不等于公开信息已被忘记。

### `stack_change` 数量／层数变化

```python
stack_change(objects: Selection[Unit | Permanent | Legend], quantity: str, operation: str,
             count: IntExpr | CountMap = 1) -> Result[StackReceipt]
```

quantity仅BUFF／EMPOWER_LAYER；BUFF仅接受场上Unit，允许ADD/SPEND/REMOVE；EMPOWER_LAYER接受Permanent／Legend，仅ADD/REMOVE。共享数量、上限与实际变更记录，但BUFF是真实计数物，强化层数为内部表示，不能被增益效果引用。

上限、控制权、费用完整性及期限来自对应模板。BUFF收据保留实际计数物引用；清除不冒充SPEND。增益和强化的战力贡献由派生规则读取数量，不额外叠加一次永久战力。

### `might_contribute` 登记战力贡献

```python
might_contribute(subjects: MightSubjects, layer: str, change: NumericChange, *,
                 duration: Duration) -> Result[list[EffectHandle]]
```

layer仅BASE、ARITHMETIC、EQUIPMENT_BONUS、BUFF_VALUE，对应单位基础值、单位算术贡献、装备对宿主的贡献、每枚增益的贡献。BASE仅set，ARITHMETIC仅add，另外两层按其已登记数值变换处理；主体不匹配拒绝。

set最终战力、交换及上下限由模板在共同快照中计算差值，再登记ARITHMETIC贡献。持续重算不伪造新的给予战力动作；即时给予的MIGHT_CHANGE及替代在模板动作流程中处理。本原语只维护战力贡献，不处理费用、伤害或其他属性。

### `trait_change` 类型化集合变化

```python
trait_change(objects: Selection[Card], trait: str, operation: str, values: TraitSet, *,
             duration: Duration) -> Result[TraitReceipt]
```

trait仅TYPE/TAG，operation仅ADD/REMOVE/REPLACE，元素分别为CardType/Tag。按层保存集合贡献；类型变化后重检单位／装备视图，不修改卡名或能力文本。

## 3. 能力、关系与投影（6）

### `ability_add` 添加能力定义

```python
ability_add(objects: Selection[Card], ability: AbilitySpec, *,
            duration: Duration, link: Link | None = None) -> Result[list[EffectHandle]]
```

授予完整能力，保留来源、第一人称和关键词身份。关键词模板先展开为带KeywordSpec身份的能力，再登记；不能因展开就丢失关键词查询或叠加规则。

### `ability_mask` 使能力失活

```python
ability_mask(objects: Selection[Card], ability_filter: Predicate, *,
             duration: Duration) -> Result[list[EffectHandle]]
```

登记失活遮罩，保留底层能力定义；不是永久删除，也不抹去无关特征。到期重新求有效能力集合。

### `ability_patch` 修改已登记能力元数据

```python
ability_patch(abilities: AbilitySelection, patch: AbilityPatch, *,
              duration: Duration) -> Result[list[EffectHandle]]
```

仅三类补丁：KEYWORD_VALUE（Assault/Shield.value的add/multiply/set）、TRIGGER_EXTRA（非负额外实例数）、TRIGGER_EVENTS（仅增加HOLD/CONQUER）。每类有独立字段校验；不接受原文、任意能力字段或EffectProgram。

### `attachment_set` 设置装备宿主关系

```python
attachment_set(gear: Selection[Gear], host: Unit | None) -> Result[AttachmentReceipt]
```

host=None为解除关系。先处理旧关系，再统一更新宿主引用、有效文本和贡献依赖；不自付Equip费用。装备位置按贴附关系派生，解除后按规则决定位置与召回，不额外制造move事件。

### `control_contribute` 登记控制权贡献

```python
control_contribute(objects: Selection[Permanent | ChainItem], player: Player, *,
                   duration: Duration, link: Link | None = None) -> Result[list[EffectHandle]]
```

保留独立控制修饰及优先关系，不修改拥有者或位置。结束后重算当前有效控制者，不简单写回旧控制者。

### `copy_view` 登记受限复制投影

```python
copy_view(target: Permanent, view: CopyView, *,
          duration: Duration, link: Link | None = None) -> Result[list[EffectHandle]]
```

CopyView仅TRAITS/TEXT/ABILITIES：分别明确可复制特征、rules_text/effect_text字段映射、能力筛选。来源、snapshot/live取值方式、原能力身份、第一人称绑定与防派生循环均须声明。它不是复制任意Python对象或原文执行器；这组三类投影仍分别保留校验器。

## 4. 信息与登记项生命周期（2）

### `information_access` 授权信息访问

```python
information_access(cards: Selection[Card], viewers: Selection[Player], *,
                    mode: str, duration: Duration) -> Result[InformationReceipt]
```

mode仅LOOK/REVEAL；共享访问授权记录。逐张展示、直到命中、原始范围与信息事件由模板处理，访问前不读取未来牌面；到期结束当前可见性授权，不删除玩家曾合法获得的历史知识。

### `effect_end` 结束具体登记项

```python
effect_end(handles: Selection[EffectHandle], *, link: Link | None = None) -> Result[list[EffectHandle]]
```

只结束已取得、获授权的具体登记项，统一释放贡献、视图、遮罩或规则记录并重算依赖。不按卡名删全部效果，不回滚已经发生的抽牌、移动、伤害或付款。

## 5. 伤害与账本（5）

### `damage_record` 记录实际伤害

```python
damage_record(units: Selection[Unit], amounts: DamageMap, *,
               source: Source, actor: Player) -> Result[DamageReceipt]
```

只接收当前伤害动作在分配、修饰、预防与替代后确认的实际值和原因引用；不能绕过伤害管线。记录伤害不减战力，致死由正常清理确认。

### `damage_clear` 清除已受伤害

```python
damage_clear(units: Selection[Unit]) -> Result[HealReceipt]
```

清除真实伤害记录，保留实际清除量及治疗／规则清理原因；不以负伤害冒充治疗。

### `resource_credit` 增加资源批次

```python
resource_credit(player: Player, resources: ResourceBundle, *, restriction: Predicate,
                 expires: ResourceExpiry) -> Result[ResourceReceipt]
```

登记Energy与分领域Power批次，保留来源、使用限制和到期。费用支出仍通过统一Pay流程，不暴露任意资源余额写入。

### `xp_change` 经验变化

```python
xp_change(player: Player, amount: IntExpr, *, operation: str) -> Result[int]
```

operation仅GAIN/SPEND，amount非负。按实际变化重算等级，支付完整性另由费用流程处理；不把XP当作单位增益。

### `score_credit` 记录实际增分

```python
score_credit(player: Player, amount: IntExpr, *, cause: PointCause,
              source: Source) -> Result[int]
```

仅在对应增分动作完成限制和替代检查后提交。保留最后一分及来源政策；不替代据守／征服历史，也不能直接宣告获胜。

## 6. 特殊流程叶节点（5）

### `chain_cancel` 取消链项执行

```python
chain_cancel(item: ChainItem) -> Result[ChainItem]
```

标记对应项不再执行；其实体卡的离链转移另由原动作模板处理。反制权限、目的地、Flow替代及是否有实体卡均保留，不产生成功结算事件。

### `chain_choices_set` 更新已有链项选择

```python
chain_choices_set(item: ChainItem, choices: ChoiceBinding, *,
                   authorization: ChoiceRewriteAuthorization) -> Result[ChoiceBinding]
```

只写入在明确改选授权下重新合法绑定的选择，不自动夺控或重付成本；普通Choose没有此授权。

### `turn_insert` 插入完整回合

```python
turn_insert(player: Player, count: IntExpr, *, after: TurnRef) -> Result[list[TurnRef]]
```

按锚点插入，不提前执行新回合，不打断当前结算。暂保留为调度器叶节点。

### `procedure_skip` 登记跳过流程

```python
procedure_skip(player: Player, procedure: ProcedureRef, *, occurrence: str,
                 duration: Duration) -> Result[EffectHandle]
```

occurrence仅next/all_matching，流程必须明确。被跳过流程不发发生事件；不等于取消当前整个回合或法术。

### `outcome_set` 登记游戏结果

```python
outcome_set(player: Player, *, authorization: WinAuthorization) -> Result[GameOutcome]
```

只接受已满足的明确规则／卡牌授权，不接受任意布尔值；保留为终局叶节点。

## 7. 分域规则记录（7）

以下原语分别登记不同管线的数据；没有一个通用rule(kind, raw_effect)入口。每个Rule类型有固定字段，不能嵌入任意可执行程序。

### `cost_rule_add` 费用规则

```python
cost_rule_add(subjects: CostSelection, rule: CostRule, *, duration: Duration,
               limit: UsageLimit | None = None, link: Link | None = None) -> Result[EffectHandle]
```

CostRule仅Energy增减、Power分领域折扣／增加、基础费替换、忽略基础／Energy及具名额外费用。费用角色、可选分支、付款关联与消费时点必须明确，不处理伤害或印刷数值。

### `damage_rule_add` 伤害规则

```python
damage_rule_add(subjects: DamageSelection, rule: DamageRule, *,
                 duration: Duration, limit: UsageLimit | None = None) -> Result[list[EffectHandle]]
```

DamageRule仅ADJUST(NumericChange)或PREVENT(amount、source_filter、预算作用域)。数值预防池与事件次数额度分开，各目标独立／共享须明确；只作用于伤害管线，不等于反制整张牌。

### `output_rule_add` 产费规则

```python
output_rule_add(actions: ResourceActionSelection, rule: ResourceChange, *,
                 duration: Duration) -> Result[EffectHandle]
```

仅Energy增量及明确的分领域Power增量／领域替换；不改变现有资源余额、花费限制或其他产费动作。

### `entry_rule_add` 入场规则

```python
entry_rule_add(subjects: EntrySelection, state: EntryState, *, duration: Duration,
                limit: UsageLimit | None = None, link: Link | None = None) -> Result[EffectHandle]
```

只记录未来对象入场初态及范围，不能将入场活跃写成一次READY。原选择地点、真实入场地点和非play生成分别保留。

### `instruction_rule_add` 已登记指令参数规则

```python
instruction_rule_add(effects: EffectSelection, parameter: EffectParameter,
                      change: NumericChange, *, duration: Duration) -> Result[EffectHandle]
```

parameter仅REDUCTION_AMOUNT，表示匹配指令的负战力幅度；不改任意文本数字、不修改费用或伤害，不接受未知参数路径。

### `permission_rule_add` 动作许可／禁止

```python
permission_rule_add(subjects: PermissionSelection, rule: PermissionRule, *,
                     duration: Duration, limit: UsageLimit | None = None) -> Result[EffectHandle]
```

PermissionRule仅ALLOW(PermissionSpec)／DENY(RestrictionSpec)，限定动作、玩家、对象、时机、来源和例外。授权仍受硬性禁止；正向强制位置不写成DENY其他位置。

### `rule_value_add` 已登记规则配置

```python
rule_value_add(key: RuleKey, scope: RuleScope, change: RuleChange, *,
                duration: Duration) -> Result[EffectHandle]
```

仅保留V4已经登记的下列键；它们由固定规则求值器读取，没有原文执行或任意新键注册。此接口是P1暂保留的配置边界，不宣称这些规则已经拆到数学最小原子。

| RuleKey | 固定数据 |
| --- | --- |
| VICTORY_THRESHOLD | delta/set |
| HIDDEN_CAPACITY | 玩家／战场与delta |
| STARTING_BATTLEFIELD_ELIGIBILITY | eligible |
| COMBAT_DAMAGE_ORDER | first/normal/last、分配者、仅Tank/Backline的忽略范围 |
| LETHAL_DAMAGE_POLICY | 来源与positive_damage_is_lethal |
| EMPOWER_LIMIT / BUFF_LIMIT | 非负上限或INFINITY |
| CHANNEL_PHASE_COUNT | 基础召出量set |
| DECK_NAME_LIMIT | name/set |
| GEAR_RECALL_POLICY | 明确装备类别条件及recall_required |
| PLAY_LOCATION_REQUIREMENT | PlayConstraint：正向目的地、启用条件、许可、费用关联；按极大相容组仲裁，硬性禁止始终检查 |

## 结果口径

35是本草案的底层原语数量；具名模板、原有程序节点及固定规则求值器另计。部分Rule／View仍有闭集变体，特殊流程仍有专门叶节点，不能把它描述为35种语义覆盖了一切。

60项接口的映射及边界卡静态展开见配套文档。尚未将全部1106张卡改写并复核，也未测得执行正确率；当前V4参考和此前覆盖率保持原状态。
