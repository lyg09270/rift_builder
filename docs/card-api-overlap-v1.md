# 基本算子 API 功能重复检查

检查对象：[现有69个API](basic-operators-api-v1.md)，结合[全量逐卡复读](card-api-coverage-v1.md)。以下不修改接口，也不把终点相同当作相同动作。

## 可合并的接口族

当前没有发现“所有参数、时点、返回语义和事件都相同”的直接同义函数；以下存在可减少入口数的重叠。

| 接口 | 重叠部分 | 若合并需要保留什么 |
| --- | --- | --- |
| `gain_xp` / `spend_xp` | 同一XP计数的正／负变化 | 可用带方向的XP调整入口，但获得／消耗事件、余额合法性及成本角色仍须区分 |
| `set_might` / `modify_might` | set_might按执行时差值建立增减修饰 | 可统一为战力调整的add／set模式，保留提高限定、快照、期限与局部上下限；不能把持续set误写成每次重算 |
| `swap_might` / `modify_might` | 交换由两个相反差值修饰构成 | 需要同一取值快照和原子批次，当前两次普通调用尚不保证等价 |
| `add_legend` / `create` | 都产生一个传奇实例 | 可增加严格的预选与关联参数；create当前controller类型与创建规则仍须完善，不能直接删除专门入口 |
| `replace_battlefield` / `restore_battlefield` | 同一关联替换机制的两个方向 | 可统一为replace／restore模式；恢复既存原牌与创建新模板不是同一参数来源 |

这些是可重构的接口族，**不是已经可以无条件互换的别名**。

## 上层封装与底层动作重叠

| 接口 | 可分解的组成 | 为什么不能直接按重复删除 |
| --- | --- | --- |
| `predict` | `look`＋`recycle`＋`reorder` | 有洞察动作身份、实际结果分组、不足处理和次序规则；普通组合未必保留独立动作事件 |
| `show_off` | `reveal`／`choose`＋属性快照＋关联 | 相依效果读取亮出时快照；现有基础信息操作没有完整快照及相依登记接口 |
| `copy_abilities` | 取得来源能力后逐项`grant_ability` | 动态来源集合、能力身份与防自递归规则不能丢失 |
| `copy_text` | `copy`在特定特征范围上的专门形式 | 普通copy只允许可复制特征；复制到装备effect_text等跨字段目标不能直接当作既有copy参数 |
| `play(cost_policy=...)` / `modify_cost` | 单次打出时的替代／忽略成本 | 前者是单次流程参数，后者可跨多个未来事件登记；需要保留适用次数、时点及领域需求 |
| `play(permission=...)` / `grant_permission` | 单次打出的额外授权 | 前者不登记持续权限，后者具有范围、期限与次数 |

## 有表面交集但不能合并的算子

| 接口组 | 必须保留的差异 |
| --- | --- |
| `draw` / `transfer` | 抽牌事件、指定抽取、耗尽规则；不是一般回手 |
| `discard` / `burn` / `kill` / `banish` / `recycle` / `transfer` | 各有独立动作身份、来源限制和触发；摧毁还能被死亡替代 |
| `move` / `recall` | 召回不算移动，不被移动限制阻止 |
| `create` / `play` | 直接生成与经过链的打出事件不同；生成复制体也不等于复制既存对象 |
| `copy` / `create(CopyTemplate)` | 一个修改既有实例，一个创建新实例 |
| `ready` / `play(entry=...)` | 入场活跃不产生变为活跃事件 |
| `buff` / `modify_might` | 增益是有限数量计数物，实际获得与消耗有事件身份 |
| `modify_buff_value` / `modify_might` | 前者改每个计数物贡献并受其增减影响，不是固定战力加值 |
| `set_base_might` / `set_might` | 基础层与算术调整层不同 |
| `modify_keyword(SHIELD)` / `modify_might` | 改关键词数值还影响关键词属性引用、叠加和角色条件 |
| `modify_rule(COMBAT_DAMAGE_ORDER)` / `grant_keyword(TANK或BACKLINE)` | 分配顺序相似，但是否拥有关键词也可被其他牌读取 |
| `damage` / `modify_damage` / `modify_effect_value` | 执行动作、未来伤害修饰、特定指令参数修饰分属不同层；后者也不能任意填写未登记参数来包办所有数值 |
| `add_resources` / `modify_resource_output` | 当前资源池增加与未来产费动作改变不同 |
| `look` / `reveal` / `show_off` | 私密查看、公开展示、带亮出快照与关联是不同信息操作 |
| `choose` / `declare` | 选择对象／目标与宣告一个合法值的规则身份、绑定时点不同；泛型T不代表二者可任意互换 |
| `channel` / `create` | 从符文牌堆召出既有卡与新建卡不同，召出事件和不足处理也不同 |

## 审核结论

发现 **5组可重构接口族、6组封装层重叠**；未发现可以直接删除而不丢语义的完全同义函数。这两个组数是关系数，不是重复算子数，一个接口可以参与多种关系。

69个接口混合了基本动作、专门入口和规则组合，存在接口层次重叠。若后续精简，应先统一同族入口并保留事件身份，再处理组合封装。覆盖复读中发现的类型不匹配、事件替代及批次问题属于接口缺口，另见覆盖报告，不能用合并不同动作来消除。
