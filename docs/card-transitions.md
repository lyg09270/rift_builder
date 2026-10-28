# 卡牌文本与状态转移矩阵

## 当前实现

- `scripts/card.py`：`Card` 保存完整有效文本、原始文本、属性和来源；`Effect` 表示事件、操作、数量、条件、目标限制和持续时间；`PowerRequirement` 表示数量及允许支付的领域选择组。
- `scripts/card_converter.py`：`CardConverter.load(ID)` 通过本地牌库读取卡牌，`convert(record)` 将完整文本转成效果节点。只匹配明确支持的完整语句；任何未映射语句都会保留并阻止整张卡生成部分结果。
- `scripts/state_transition.py`：`StateTransition` 表示一次具体状态和上下文下的齐次仿射矩阵，提供 `apply()`、`changes()`、`then()`。

旧 `card_model.py` 中的定价与未实现推演接口已被替换，没有保留旧接口或定价层。

链路是：本地卡面 → 效果节点 → 当前状态／历史／目标绑定 → 条件判断、费用及操作结算 → 局部矩阵。

## 矩阵含义

原始状态 `s` 为 93 维；固定增减不是纯线性映射，增加常数坐标得到 94 维：

~~~text
z = [s, 1]
z_next = M @ z
~~~

当前矩阵是 `94 × 94` 的局部仿射表示：先在真实快照上计算支持的效果，再把结果差写入矩阵最后一列。它不是把有限游戏状态编号后得到的马尔可夫概率矩阵，也不是一张牌在任何局面都通用的固定矩阵。

条件降费、阈值、目标死亡、负战力截断等先根据当前状态与上下文决定。复用同一张 `Card` 时，应对新状态重新调用事件接口，不能拿旧矩阵应用到新局面。`apply()` 会拒绝不同的数值快照；相同向量不保证逐卡明细相同，调用者仍必须保证目标和上下文未变。

`then()` 按执行顺序计算 `M_second @ M_first`，要求第二张矩阵绑定第一张结果。它只复合数值转换，不合并完整目标明细、历史或持续效果记录；外层应逐步保管这些信息。

## 事件接口

| 方法 | 当前行为 |
| --- | --- |
| `Card.on_play(state, context)` | 从手牌或指定英雄区消耗该卡，支付已产生的资源，单位普通进场横置／装备进场，执行已映射的打出效果；法术结算后入墓地 |
| `Card.on_draw(state, context)` | 从主牌库抽取这一张牌，更新牌库／手牌计数；不会执行它的打出效果或支付出牌费用 |
| `Card.on_death(state, context)` | 移除这张单位的场面贡献，放入拥有者而非控制者的墓地，执行已映射的自身死亡效果 |

这些接口包含对应的基础生命周期，调用方不能先更新一次区域计数再调用，否则会重复结算。`on_death` 的目标快照是死亡前的单位。伤害导致目标死亡时只处理普通单位的移除，不会自动寻找其他卡牌的死亡能力；此类额外触发超出孤立模型。

`CardContext.isolated=True` 表示调用者已提供一个没有额外触发、装备附着影响或伤害替代的孤立场景，不是请求用户批准。当前只投影到事件完成后的观测向量，不提供完整规则引擎。

## 已支持的语义子集

- 普通单位进基地、普通非单位装备进场、法术结算入墓地。
- 抽固定数量的牌；可验证的直接得分／获得 XP 指令。
- Legion 条件减 Energy、按墓地数量减 Energy，费用下限为零。
- Kinkou Initiate 的其他友军总战力阈值抽牌，排除刚进场的自身。
- 单个已存在单位目标的直接伤害、正战力增益、Ready、Stun、Kill。
- 一部分直接打出或死亡触发；基础 Action／Reaction 时机标记。

未横置与晕眩独立处理；伤害不直接扣战力。负的实际战力保留在 `UnitTarget` 中，投影时对每个单位取零下限。`UnitTarget` 保存实例编号、卡牌 ID、拥有者、控制者、位置、战力、伤害、横置及晕眩状态；无法从总战力猜目标数据。

增益与 Stun 的 `Effect.duration` 保留为 `turn`，但当前不模拟回合结束或自动过期；外层需要登记并执行到期规则。`target_after` 提供更新后的单个目标快照。目标必须已存在于输入场面；新进场单位自身作为打出能力目标尚需更完整的实例上下文。

## 费用数据

本地未溯源的 `power=None` 仍表示未知，不自动当作零。现已通过 RiftAtlas 公开目录及费用组件，核实全部 1,143 条普通可打出记录；568 个原空值核实为无 Power 费用。转换器自动读取牌库的 `power_cost_json` 和来源，不再要求逐次手工补费用。传奇、战场、符文和衍生物等不适用普通支付，不把其空值伪装成缺失。

每个 `PowerRequirement(amount, domains)` 表示所需数量可从该组任一领域支付。多领域规则按照官方核心规则 135.2.e.6 处理：三个 Fury/Mind Power 可混合支付，不是每色都付三点；中立卡允许任意领域。资源池中的 Universal 始终可代替相应领域。

`CardContext.power_payment` 可显式指定花费；不指定时按允许领域顺序寻找合法方案，优先保留通用 Power，先分配较严格的领域组。不会自动横置或回收符文。手工 `power_cost={"Fury": 1}` 覆盖仍可用于新卡核对／合成测试，但必须提供 `power_source`，且总量须与已知数据相符；此字典中的 `Universal` 表示任意领域需求。

Legion 的 `played_other_card` 必须是明确的历史事实，不接受未提供时默认 False。当前不执行额外费用、替代支付或复杂费用限制。

## 示例

将 `scripts/` 加入导入路径后：

~~~python
from card import CardContext
from card_converter import CardConverter
from game_state import StateEnum as S, game_state

# 费用与来源已由 RiftAtlas 同步入库，无需手工覆盖。
card = CardConverter().load("OGN-012")
state = game_state()
state.update({S.PHASE: 6, S.P0_HAND_COUNT: 4, S.P0_DECK_COUNT: 30,
              S.P0_ENERGY: 6, S.P0_TRASH_COUNT: 1})
context = CardContext(played_other_card=True, isolated=True)
transition = card.on_play(state, context)
next_state = transition.apply(state)
print(transition.matrix.shape)  # (94, 94)
print(transition.changes())

# 下一次绑定使用新局面；矩阵不会跨不同快照复用。
second = card.on_play(next_state, context)
combined = transition.then(second)
result = combined.apply(state)
~~~

Power 的原始来源、哈希、别名核对和回填明细见 [同步报告](../reports/riftatlas-power-sync.json)；同步脚本为 `scripts/sync_riftatlas_power.py`。本轮不依据论文推断缺失费用。

## 验证命令与结果

本轮用户明确要求添加测试。运行：

~~~text
python tests/test_card_transitions.py
python tests/test_riftatlas_power.py
python scripts/audit_card_transitions.py
~~~

独立预期样例覆盖抽牌收支、进场横置、条件降费、其他友军阈值、伤害与战力区别、拥有者入墓地、晕眩与就绪区别、负战力、生命周期、矩阵快照绑定与组合、未知语句拒绝、衍生物、时机、盖放区清理和多领域支付等；27 项通过。另有 6 项来源解析、缺省费用证据、领域选择组和明确异画别名测试通过，共 33 项。

全牌库脚本实际遍历全部 1,407 条印刷记录、1,103 个不同名称，不跳过失败记录。对于不能映射的牌，验证其确实拒绝部分转换；对于已映射的普通卡牌，使用实际已溯源费用运行场景，并检查输入不变、卡牌数量守恒、交换双方后的对称性及状态一致性。不是只检查矩阵形状，也不再使用测试费用假设。

当前结果：费用信息核实 1,143 条；27 条记录通过 346 次孤立场景检查；1,380 条记录拒绝或尚不支持。Power 缺失已不再是阻塞原因。孤立场景依据本地效果文本，不能代替对最新勘误、完整互动和所有选择分支的核对；完整对局规则认证仍为零。未知文本、未建模类型和衍生物生命周期等原因有重叠，不能将原因数量直接相加。

输出：[逐牌报告](../reports/card-transition-audit.md)、[机器可读结果与完整未知文本](../reports/card-transition-audit.json)。脚本退出码 1 表示未完成全牌库认证，2 表示出现实现异常；当前为 1，且没有实现异常。这不等于所有卡牌都已正确实现。

当前还缺多目标／选择／指代、区域移动、持续与替代效果、完整触发互动、衍生物创建移除、符文能力、传奇与战场能力、Burn Out 和隐藏信息。基础 Power 数据已齐全，但额外费用和费用替代效果仍需建模。无法支持时返回带原因代码的 `TransitionError`，不会默默生成近似或零效果矩阵。
