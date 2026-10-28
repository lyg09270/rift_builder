# V3算子修订与简化依据

日期：2026-10-28。[V3基本算子参考](basic-operators-api-v3.md) · [V2.1存档](basic-operators-api-v2.1.md) · [第三轮阅读进度与结果](card-api-coverage.md)

本轮已完整复读1106张，确认覆盖1059张（95.75%），待核7张、未完整覆盖40张。详细结果见[终审核对](operator-audits/round-3-validation.md)；函数使用情况及`reorder`的进一步精简空间见[冗余审查](operator-audits/round-3-redundancy.md)。下列V3修订发生在本轮全读之前，发现的新缺口没有静默补入冻结API。

先复查[12张真实效果核验](card-effect-rulings-review.md)的五张未决卡，再审查73个函数的语义重叠。补检官方规则入口、已有勘误、FAQ与逐卡资料后，尚无足够官方依据消除曼舞手雷的跨重打计数、沙漠皇帝的版本范围、嚼火者手雷／不朽凤凰的打出费用关系、奥义！雷铠的特殊剩余集合问题。保留待核；不会为迎合100%而写入猜测性规则。

后续事件／时点及位置要求补充已另记[V3.1修订](card-api-changes-v3.1.md)，本页保留第三轮前的V3简化依据。

## 已完成简化

| V2.1入口 | V3入口 | 保留的语义 |
| --- | --- | --- |
| ready / exhaust | orient(objects, state) | state只允许ready或exhausted；READY与EXHAUST事件、已有朝向无变化、actor与批次、成本完整性分别保留 |
| empower / disempower | change_empowerment(objects, mode) | mode只允许empower或disempower；默认二元、明确可叠层的上限、只去一层及两种事件身份分别保留 |

四个旧入口替换为两个新入口，**73→71个正式函数**。减少的是函数入口数量；游戏动作的区别没有删除。旧名不作为可调用别名保留，全部第三轮调用迁移到新入口。

## 继续保留的接口边界

| 接口关系 | 保留理由 |
| --- | --- |
| draw / transfer；kill / banish / recycle / discard / burn | 来源约束、动作身份、费用、触发及替代不同 |
| move / recall | 召回的规则与移动限制及移动触发不同 |
| buff / spend_buff | 获得的上限与消耗的控制权、计数回执和成本要求不同；本轮优先保留直观的具名动作 |
| attach / detach | 建立宿主关系与解除关系、返回值及对应贴附触发不同 |
| modify_might / set_base_might / modify_equipment_bonus | 算术修饰、基础特征层、装备贡献层需分别保留 |
| copy / copy_text / copy_abilities | 可复制特征、跨字段效果文字、动态能力集合及防自递归范围不同 |
| grant_ability / grant_keyword / modify_keyword | 完整能力体、关键词身份、修改已有参数的范围不同 |
| on_event / replace_event / queue_effect | 事件后触发、事件前替代、明确自反步骤生成待处理项的时序不同 |
| change_control / end_modifier | 新增控制修饰与结束取得的特定修饰不同 |
| play参数 / modify_cost或grant_permission | 单次动作参数与持续／限次登记的作用域不同 |

“同一个返回区域”“同样加战力”或“最终同样活跃”不足以证明两函数完全等价。参数化以闭集模式为限，不增加接受自然语言的通用效果入口。

## 第三轮阅读约束

V3在重新阅读前定稿；指纹为`2530366c3f814b7f77f992ffe36c7c5bf3a0ad5fa23812de34119a6ea4dd03a3`。本轮必须重新读取全部1106个本体的全部可用EN／SC／TC规则与装备效果、基础属性、目录勘误，并逐张写独立审核记录。语法迁移只产生候选，不自动形成通过判定。卡图没有被本轮逐图全库核验，不能把卡面文字完整阅读描述成全部图片视觉核验。

目录keywords是检索索引，可能包含提醒文字、被授予能力或产生的衍生物关键词；本轮按实际规则文字区分固有能力、条件授予及衍生物模板，不能把索引中的全部关键词免费授予卡牌本身。

遇到签名虽可写但费用角色、时点、行动归属或数据存在未解决疑问时，保留待核并排除确认覆盖分子；若闭集API无法表达，另列未覆盖。正式结果按1106个本体的固定分母计算，未阅读不能算通过。
