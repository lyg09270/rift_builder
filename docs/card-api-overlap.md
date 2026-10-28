# 基本算子 API 功能重复检查

当前：[V2.1的73个API](basic-operators-api.md)；下列为V2全库冗余检查及本次增量补充。第一轮结果已[存档](card-api-overlap-v1.md)。下列5组关系已归并，6组封装交集继续保留；全库复核见[覆盖报告](card-api-coverage.md)。

## V2已归并的接口族

第一轮指出下列关系。V2已完成归并，迁移时保留表内语义条件。

| 接口 | 重叠部分 | 若合并需要保留什么 |
| --- | --- | --- |
| `gain_xp` / `spend_xp` | 同一XP计数的正／负变化 | 已统一change_xp的gain/spend模式；获得／消耗事件、余额合法性及成本角色仍须区分 |
| `set_might` / `modify_might` | set_might按执行时差值建立增减修饰 | 已统一modify_might的add／set模式，保留提高限定、快照、期限与局部上下限；不能把持续set误写成每次重算 |
| `swap_might` / `modify_might` | 交换由两个相反差值修饰构成 | 已统一modify_might的swap模式，保证共同快照与原子差值 |
| `add_legend` / `create` | 都产生一个传奇实例 | 已统一create，接受SetupChoiceRef、duration/link及传奇回执，严格检查预选 |
| `replace_battlefield` / `restore_battlefield` | 同一关联替换机制的两个方向 | 已统一replace／restore模式；恢复既存原牌与创建新模板不是同一参数来源 |

上述旧入口已从V2移除，共减少5个函数；新增8个机制后，正式函数为72个。

## 上层封装与底层动作重叠

| 接口 | 可分解的组成 | 为什么不能直接按重复删除 |
| --- | --- | --- |
| `predict` | `look`＋`recycle`＋`reorder` | 有洞察动作身份、实际结果分组、不足处理和次序规则；普通组合未必保留独立动作事件 |
| `show_off` | `reveal`／`choose`＋属性快照＋关联 | 相依效果读取亮出时快照；普通reveal/choose仍不自带完整ShowOff身份与as-play流程 |
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
| `set_base_might` / `modify_might(change=set)` | 基础层与算术调整层不同 |
| `modify_keyword(SHIELD)` / `modify_might` | 改关键词数值还影响关键词属性引用、叠加和角色条件 |
| `modify_rule(COMBAT_DAMAGE_ORDER)` / `grant_keyword(TANK或BACKLINE)` | 分配顺序相似，但是否拥有关键词也可被其他牌读取 |
| `damage` / `modify_damage` / `modify_effect_value` | 执行动作、未来伤害修饰、特定指令参数修饰分属不同层；后者也不能任意填写未登记参数来包办所有数值 |
| `add_resources` / `modify_resource_output` | 当前资源池增加与未来产费动作改变不同 |
| `look` / `reveal` / `show_off` | 私密查看、公开展示、带亮出快照与关联是不同信息操作 |
| `choose` / `declare` | 选择对象／目标与宣告一个合法值的规则身份、绑定时点不同；泛型T不代表二者可任意互换 |
| `channel` / `create` | 从符文牌堆召出既有卡与新建卡不同，召出事件和不足处理也不同 |

## 审核结论

第一轮5组可重构关系已完成归并；6组封装层交集保留。当前未确认参数、时点、返回语义与事件身份均相同的完全同义函数。组数是接口关系数，不是重复函数个数。

V2新增batch、on_event、replace_event、queue_effect、modify_entry、modify_equipment_bonus、modify_trigger_events、remember，分别处理批次、触发、替代、自反项、入场、装备贡献、触发类别和关联存储。on_event等待事件，queue_effect在明确自反指令处建项；on_event的事件后触发也不能取代replace_event的事件前替代。

第二轮发现的缺失事件或参数在覆盖报告单列，不以合并不同动作消除。本结论是文档契约审核，不是执行引擎等价性证明。修订细节见[变更依据](card-api-changes-v2.md)。

## V2.1专项修订后的增量检查

按[12张真实功能核验](card-effect-rulings-review.md)，新增end_modifier，72→73函数；transfer增加position，补STUN／MIGHT_CHANGE／GAIN_POINTS事件，没有增加卡牌专用算子。

- end_modifier只结束取得的修饰引用；change_control建立新控制修饰，两者不等价。
- transfer(position=...)是跨区域时直接放到指定端；reorder调整既有区域内所选集合的次序，保留独立用途。
- on_event是在事件后创建能力，replace_event在事件提交前替代；隐秘追踪者不能为了“随之”而强制使用join。
- 影分身的banish是效果，pay是支付费用；将前者误写为后者属于语义错误，不是可合并接口。

本次没有确认新的完全同义函数；未重做其余1094张的完整语义阅读，不能将增量结果描述为V2.1全库等价性认证。
