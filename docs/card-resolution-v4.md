# V4程序与流程契约

本文件细化[卡牌基本模型](card-model.md)，供[V4基本算子](basic-operators-api-v4.md)使用。以下是程序节点和数据结构，不属于`ops`函数，也不计入60个基本算子。本文定义接口，未实现执行引擎。

## 1. 能力定义与运行上下文

```text
AbilitySpec = id + entries + program + constraints
```

| 结构 | 必须明确的内容 |
| --- | --- |
| entries | 非空EntrySpec列表；每个入口有kind、有效区域、条件和绑定规则。kind为direct／active／event／continuous／replacement |
| event入口 | EventPattern及delivery=pending或inline；普通触发创建pending，inline只可用于明确开放的过程阶段 |
| continuous入口 | 条件及依赖；登记持续贡献，不反复执行即时抽牌、伤害等动作 |
| replacement入口 | 待发生事件及RewriteSpec；在动作提交前处理 |
| constraints | 已解析的选择、费用、额度、登记期限与绑定声明；仅允许省略已有明确默认规则的项 |
| Context | 来源、能力控制者、行动者、决策者、事件引用、已选对象、付款、局部变量及关联存储；与静态定义分开 |

入口集合采用或匹配。同一实际事件的不同视图命中同一条件时去重；不同能力、不同事件分别处理。条件立即跟随触发入口时在事件处检查，程序内条件在对应指令处检查，持续条件按依赖重算，不能一律在结算时重检。

源对象的拥有者、当前控制者、能力控制者和行动者分别保存；战场能力的玩家归属按该能力明确选择规则绑定。对象离场信息按授权保存LKI，不按同名卡共享上下文。

## 2. 程序节点

节点的字段都是类型化表达式或已定义程序；不接受原始卡牌文本、未知节点或任意执行代码。下表给出逻辑字段，编写器可使用等价的声明式序列化格式。

| 节点 | 字段 | 处理职责 |
| --- | --- | --- |
| Call | op、args、kwargs、store | op必须是60个正式算子之一；按签名校验参数，把Result绑定到store |
| Sequence | steps | 按顺序执行，不在普通“然后”处自动新建链项 |
| If | condition、then、else | 到达该处时判断；条件只能读取已授权信息 |
| Optional | player、stage、body、store | 在允许时点决定是否执行；不擅自消耗被拒绝的可选额度 |
| Choose | player、kind、candidates、minimum、maximum、targeting、stage、shortage、store | 统一选择对象、值、名称、类型、领域、标签、模式或排列，见下方约束 |
| Pay | player、cost、binding、store | 在CostBinding指定的角色与时点调用费用流程，不自行改变后续打出的费用政策 |
| ForEach | objects、item、body | 对已绑定集合顺序执行；对象是否仍合法在各指令处检查 |
| Repeat | count、body、bindings | 同一程序重复；关键词Repeat使用预先定稿的逐遍选择，不重打卡牌 |
| Batch | policy、steps | simultaneous用共同快照同批提交；player_procedure按规则跨玩家完成同一指令后再执行下一条 |
| Bind | key、value、scope、duration | 保存引用／快照；key有类型声明，scope仅local／source_instance／deck_setup／link，跨区域保留须授权 |
| Register | ability、duration、limit、link、store | 动态登记延迟、过程内联或替代能力，保留完整入口与代码体；不当场执行能力，不给其他对象凭空增加固有能力 |
| Enqueue | source、ability、bindings、link、store | 创建已定义能力的pending实例，可引用获授权LKI；不伪造触发事件、不马上结算、不自动构成一次卡牌打出 |
| Keyword | spec、player、link、store | 执行已登记的结构宏；本版独立程序宏仅Predict与ShowOff，参数和收据见第4节 |

普通固有入口由能力定义直接提供，不再在每次结算时重复Register。给目标对象授予能力特征仍使用`ops.grant_ability`；改变已有链项选择仍须`ops.redo_choices`授权，不能借Choose任意重选。

### 选择与绑定

- Choose.kind仅object／value／name／type／domain／tag／mode／order。名称来自合法注册表，order必须是获授权集合的完整排列；对象选择的targeting必须明确，其他选择不伪装成目标。
- stage仅setup／trigger／finalization／resolution，必须在真正对应阶段执行。少于minimum时shortage仅as_many_as_possible或fail；足够时仍须满足minimum，成本选择必须fail。
- 动态选择器保存条件及求值时点；冻结引用不等于冻结战力、位置或控制者。ChoiceBinding保存目标、模式、原选择位置及费用分支，结算重检合法性，不自行重选失效目标。
- 私密牌堆选择、正式目标、公开展示是独立规则。统一选择流程仍处理target事件和Deflect等附加费用，不能因移出算子层丢失这些规则。

### 费用与回执

- Cost保存Energy、分领域Power、具名动作费用与组合；CostBinding区分基础／替代基础／额外／目标附加／指令内／替代门槛费用，并指向具体卡牌、能力或动作。
- 基础、额外和替代费用由定稿流程计算，先支付资源再处理非标准动作费用；指令内Pay保留在程序原位置。折扣后为0仍保留选过哪个费用分支的记录，缺失费用不能当0。
- PaymentReceipt分别保存选择分支、规则上是否支付、实际资源／动作及替代轨迹；ActionReceipt记录实际发生的动作。费用被替代后是否视为已付由费用规则决定，不能直接以原动作没发生就判未付。
- Pay失败不能继续依赖该支付的分支；“如果这样做”必须绑定对应PaymentReceipt或ActionReceipt。规则不明的费用政策显式拒绝，不由流程猜测。

### 次数、期限与关联

- 事件粒度、历史第N次、每回合使用额度及Repeat是四套独立信息。UsageLimit明确count、reset=never／each_turn、consume=on_accept／on_finalize／on_success、optional、scope_key、计数单位；on_success还要指定成功事件及阶段。
- scope_key区分能力实例、玩家、对象、批次或明确共享组；历史第一次发生不会因拒绝可选能力而回滚。预防量等数值额度与触发次数分别计数。
- Bind的key须预先声明类型和作用域；局部值不自动跨回合保存，实例关联不按同名卡共享，过期与离区清理按具体授权处理。
- Register.duration控制登记项生存期，程序中各修饰仍有自己的duration；来源离场不默认取消全部延迟能力。指定时点已经过去时不补触发或挪到下次。

## 3. 统一调度

```text
匹配入口／主动请求
→ 检查有效区域、条件及次数
→ 建立pending实例或登记持续／替代规则
→ 按真正时点选择、算费、付款与检查合法性
→ 立即结算分支或正常优先权流程
→ 执行程序，保留当前结算帧
→ 登记事件、后续pending与Outstanding任务
→ 按规则调度继续处理
```

定稿失败按规则回退该过程及其派生事件，不把尚待合法性确认的付款副作用永久提交。单位、装备及产资源能力的立即结算分支保留；其他链项按对应优先权流程处理。

每个动作形成待发生事件，在允许窗口处理内联规则、修饰、预防和替代，再提交实际结果，按规则层重算依赖并检查状态跨阈值。被忽略与被阻止／替代的指令分开记录，后续关联据具体结果判断。

Batch不能跨顺序指令吞并动作；其Result在提交前不可读取。play、Enqueue、Register不能任意塞进simultaneous批次改变链时序。当前链项未执行完时不递归结算新pending，也不提前执行Cleanup。效果在结算中离链时，后续指令按离链规则停止。

## 4. 关键词程序宏

KeywordSpec是带关键词身份及结构参数的已解析定义；未知名字拒绝。其他固有关键词编译为对应入口、费用、许可或具名动作，不新增通用效果执行器。

| 宏 | 参数 | 展开契约与回执 |
| --- | --- | --- |
| Predict | count | 一次查看顶count张，选择可回收子集，回收，再按规则安排获授权余牌；多张不等于逐张Predict 1。保留looked、实际recycled、kept_on_top及次序，不伪造回到顶部的已离区牌 |
| ShowOff | requirement | requirement明确数量、手牌／场上候选、差异性约束；在finalization用Choose及必要reveal完成混合亮出，保留手牌展示、场上挑选及当时属性快照，不把所有挑选都当target |

Repeat固有宏在定稿时保存每遍模式／目标和附加费用，结算用Repeat节点；Flow定义废牌堆来源许可、替代基础费及对应item离链放逐替代，包括反制，明确的自身指令离链例外。宏展开不能与原固有关键词再重复登记。

## 5. 替代与内联结构

RewriteSpec明确before、replacement、after程序、resume_original布尔、可选patch及PaymentGate。PaymentGate包含payer／Cost／CostBinding，完整接受支付后才接受该替代；拒绝或失败保留原动作。resume_original时按合法来源重新求值，不复用越权预读。

| 原事件 | 允许的patch |
| --- | --- |
| PLAY | entry、destination、明确授权的新token同模板数量 |
| CHANNEL | 每枚符文entry序列及明确追加数量，保留原数量与归因 |
| LOOK / REVEAL | 保留来源／数量，before完成后重新求值 |
| LEAVE_CHAIN | destination、identity，限定指定item及自身指令离链例外 |
| DIE / ZONE_TRANSFER / DISCARD / BANISH / COMBAT_TIE / STUN / MIGHT_CHANGE / GAIN_POINTS | 取消匹配部分并执行明确替代程序，不连带取消同批其他对象 |

未知patch拒绝。inline只开放PLAY.as_play／before_finalize、LOOK／REVEAL.as_each和ATTACH.as_attach等明确过程点；before不是任意执行程序的授权，resolved／complete的普通触发不能改成inline。替代嵌套遵守选择权与自重入规则，不自行固定全局执行顺序。

<a id="事件契约"></a>
## 6. 事件契约

EventPattern字段为kind、stage、actor、source、objects、filter、granularity、matching和可选transition。filter仅访问该阶段已授权信息；matching仅ALL／FIRST，FIRST须说明历史计数范围。EventRef保存event_id、action_id、batch_id，区域变化另有transition_id及实际对象与归因。

| EventKind | 阶段与必要数据 |
| --- | --- |
| PLAY | as_play／before_finalize／finalized／entered／resolved；card/item、choices、payment、原选择位置、实际入场位置 |
| USE_ABILITY | before_finalize／finalized／resolved；主动能力实例、来源、行动玩家、费用特征、选择及付款 |
| HIDE | before／complete；card引用、来源、战场及授权；不额外公开隐藏属性 |
| DISCARD / BANISH | before／complete；实际集合、行动玩家、拥有者及源／目的区域；弃置另保留决策者 |
| SPEND_BUFF | before／complete；单位、实际计数物引用、逐单位数量、总计与费用角色 |
| LOOK / REVEAL | before／as_each／complete；已获授权的实际牌与信息范围 |
| ATTACH | as_attach／complete；gear、host、previous_host |
| MOVE | before／complete；原地点、目的地及原批次 |
| DIE / LEAVE_BOARD / ZONE_TRANSFER | before／complete；对象、LKI、源／目的区域及动作身份 |
| DAMAGE | before／complete；来源、目标、数量、实例及分配批次 |
| STUN | before／complete；真正可执行的新眩晕、对象及来源选择记录 |
| MIGHT_CHANGE | before／complete；给予的非零有符号差值及共同快照，不代表所有最终战力变化 |
| STATE_TRANSITION / BECOME_MIGHTY | complete；对象、前后规则值与原因；后者为战力跨5阈值的具名视图 |
| GAIN_POINTS | before／complete；玩家、数量、cause、来源战场及回合序号 |
| TURN_PHASE | start／end；玩家、具体阶段及回合序号 |
| HOLD / CONQUER / ATTACK / DEFEND / COMBAT_START / COMBAT_WIN / COMBAT_TIE | 对应规则边界；玩家、地点、单位及结果快照 |
| SHOWDOWN_START | start；showdown_id、战场、focus_player及combat_id或None；非战斗对决也发布 |
| COMBAT_END | end；combat_id、战场、结果及参加过的单位历史，包括No Result |
| CHOOSE / DRAW / RECYCLE / BURN / CHANNEL / BUFF / EMPOWER / DISEMPOWER / EXHAUST / READY / XP | before／complete及实际对象、数量与归因；CHOOSE保留targeting，XP保留gain／spend |
| LEAVE_CHAIN | before／complete；item/card、执行／反制／外部动作原因及自身指令离链标志 |

- PLAY.finalized用于已定稿历史；PLAY.resolved与USE_ABILITY.resolved用于成功结算后的相应触发。反制不发resolved，正常结算但无可执行效果仍可完成。entered只指永久物入场；下一张打出修饰仍绑定打出流程。
- granularity仅per_event／per_object／per_batch／per_counter。DISCARD／BANISH／SPEND_BUFF原生事件为同次指令实际完成集合；per_batch按action_id、actor和指令匹配一次，不合并不同顺序指令或不同玩家；per_counter只用于实际消耗的增益。
- 所有实际区域变化提供ZONE_TRANSFER视图，包括各独立动作、离链与离场；身份由实际动作产生，调用者不能指定成其他动作。同一对象的待转移在具名及通用视图共享transition_id，同一修饰不能因换视图重复适用。局部替代保留其他对象，替代后只对真正发生的动作发完成事件。
- 没有实际完成部分不发原动作complete。move／recall仅改变Board内地点，排序仅改变牌堆顺序，均不凭空制造区域转移；新实例没有旧区域时源值为None，不伪造先前位置。
- StateTransitionSpec仅field="might"、comparison="ge"、明确value、direction="false_to_true"；按规则可观察变化的前后值比较，BECOME_MIGHTY固定value=5。装备、控制／位置、增益、持续修饰到期等依赖变化都参与；同批用共同快照，不观察内部计算暂态，不额外Cleanup。没有前值或数值未知时不默认0。
- STATE_TRANSITION只有事后观察，不开放before／inline／patch。已满足条件时登记不补触发，持续满足不重复触发；无行动玩家的规则到期保留actor=None。
- COMBAT_END保留参加历史，历史引用不直接充当仍在场Unit。SHOWDOWN_START不会因同一对决转成战斗对决再发一次开始。离场触发按替代后的真实动作和LKI处理，不统一推迟到来源已失效之后检查。

## 7. 最小结构示例

以下是能力定义的声明式示意；Choice、费用和程序节点由编写器按本契约编译，不是可直接运行的Python引擎。

```yaml
id: discard_then_ready
entries:
  - kind: event
    active_zone: board
    event:
      kind: DISCARD
      stage: complete
      actor: controller
      granularity: per_batch
program:
  - Call:
      op: orient
      args: [[self], ready]
  - Call:
      op: modify_might
      args: [[self], 1]
      kwargs: {duration: THIS_TURN}
```

同一卡的另一个能力另存一条AbilitySpec。多入口能力在entries中列出多个入口，共用program与明确的额度作用域，无须增加事件登记算子。
