# V4算子简化与迁移

日期：2026-10-28。[卡牌模型](card-model.md) · [V4算子参考](basic-operators-api-v4.md) · [程序与流程契约](card-resolution-v4.md) · [V3.1存档](basic-operators-api-v3.1.md)

## 简化结果

**71→60个正式函数**。9项选择、付款、批次、记忆、事件登记与调度接口迁入模型层；2项关键词封装迁为结构宏。剩余60个具名接口继续保留各自对象范围、动作身份和规则层。

没有增加通用modify，也没有把不同修饰藏进kind参数。伤害预防、费用、基础战力、装备贡献、增益贡献及触发规则等15个具名修饰接口均保留。保留的modify_rule仍仅允许原有注册RuleKey及对应字段，不能充当任意效果入口。

60是动作／修饰函数数量，13个程序节点和2个独立关键词宏另列；总规则复杂度不会因为函数计数减少而消失。具体游戏动作与流程职责的拆分可避免卡牌反复手写事件、付费和调度样板。

## 全部71项的去向

“保留”表示接口语义继续存在，参数变化见下一节。迁出项不作为`ops`别名继续调用；新节点的字段必须按流程契约填写，不能只换名字。

| V3.1函数 | V4归属 | 具体去向 |
| --- | --- | --- |
| draw | 保留 | draw |
| look | 保留 | look |
| reveal | 保留 | reveal |
| choose | 流程 | Choose(kind="object") |
| declare | 流程 | Choose(kind为value/name/type/domain/tag/mode) |
| predict | 宏 | Keyword(spec=Predict)，保留多张洞察及实际结果收据 |
| show_off | 宏 | Keyword(spec=ShowOff)，保留定稿选择、混合来源与属性快照 |
| transfer | 保留 | transfer；动作身份固定ZONE_TRANSFER |
| move | 保留 | move |
| recall | 保留 | recall |
| discard | 保留 | discard |
| recycle | 保留 | recycle |
| banish | 保留 | banish |
| burn | 保留 | burn |
| channel | 保留 | channel |
| reorder | 保留 | reorder |
| hide | 保留 | hide |
| play | 保留 | play，委托统一打出流程 |
| create | 保留 | create |
| replace_battlefield | 保留 | replace_battlefield |
| orient | 保留 | orient |
| buff | 保留 | buff |
| spend_buff | 保留 | spend_buff |
| stun | 保留 | stun |
| change_empowerment | 保留 | change_empowerment |
| modify_might | 保留 | modify_might，保留即时给予与持续贡献的区别 |
| set_base_might | 保留 | set_base_might |
| damage | 保留 | damage |
| prevent_damage | 保留 | prevent_damage |
| heal | 保留 | heal |
| kill | 保留 | kill |
| attach | 保留 | attach |
| detach | 保留 | detach |
| change_control | 保留 | change_control |
| end_modifier | 保留 | end_modifier |
| copy | 保留 | copy |
| copy_text | 保留 | copy_text |
| copy_abilities | 保留 | copy_abilities |
| grant_ability | 保留 | grant_ability，参数采用AbilitySpec |
| suppress_ability | 保留 | suppress_ability |
| grant_keyword | 保留 | grant_keyword，保留关键词身份 |
| modify_keyword | 保留 | modify_keyword，本版显式登记Assault.value／Shield.value |
| set_types | 保留 | set_types |
| set_tags | 保留 | set_tags |
| add_resources | 保留 | add_resources |
| pay | 流程 | Pay与统一费用阶段，保留费用角色和PaymentReceipt |
| modify_cost | 保留 | modify_cost |
| change_xp | 保留 | change_xp |
| gain_points | 保留 | gain_points |
| win | 保留 | win |
| modify_damage | 保留 | modify_damage |
| modify_effect_value | 保留 | modify_effect_value，本版登记REDUCTION_AMOUNT |
| modify_trigger_count | 保留 | modify_trigger_count |
| modify_resource_output | 保留 | modify_resource_output |
| modify_buff_value | 保留 | modify_buff_value |
| grant_permission | 保留 | grant_permission |
| restrict_action | 保留 | restrict_action |
| modify_rule | 保留 | modify_rule，包含PLAY_LOCATION_REQUIREMENT |
| counter | 保留 | counter |
| redo_choices | 保留 | redo_choices；明确改选是游戏动作，普通Choose不能替代 |
| execute_effect | 流程 | pending模式用Enqueue；repeat_inline用已定稿选择的Repeat，不混成新play |
| skip_procedure | 保留 | skip_procedure；卡牌要求跳过流程是游戏效果 |
| extra_turn | 保留 | extra_turn；追加回合是游戏效果 |
| batch | 流程 | Batch，保留共同快照及player_procedure |
| on_event | 流程 | 固有能力直接写entries；动态延迟／inline能力用Register |
| replace_event | 流程 | 固有替代写replacement入口；动态项用Register与RewriteSpec |
| queue_effect | 流程 | Enqueue，保留自反pending与独立定稿 |
| modify_entry | 保留 | modify_entry |
| modify_equipment_bonus | 保留 | modify_equipment_bonus |
| modify_trigger_events | 保留 | modify_trigger_events |
| remember | 流程 | Bind，保留类型、来源实例／构筑作用域、link与期限 |

## 参数与返回值调整

| 调整 | V4要求 |
| --- | --- |
| move／orient／damage／kill移除simultaneous | 集合默认同一指令批次；跨调用同时用Batch，明确顺序用ForEach。迁移须保留原指令及动作子ID，不能只机械删除参数 |
| transfer移除identity | 不能再传BURN；对应获授权顶牌燃烧改用burn并保留原对象集合，不能补烧其他牌 |
| discard移除chooser | player自行选择为内建流程；其他选择者先用Choose绑定cards |
| reorder移除policy／chooser | order仅KEEP_ORDER、RANDOM_ORDER或已绑定排列；玩家排序先用Choose(kind="order") |
| transfer的chosen次序 | 选择结果保存在cards的已绑定排列中；order="chosen"不再暗含一次新选择 |
| modify_cost／modify_damage／grant_permission统一额度参数 | 只留limit，不保留uses简写；旧modify_cost的uses按on_finalize迁移，其他旧uses须按卡文明确消费阶段与作用域，不能只填count |
| grant_ability的Ability→AbilitySpec | 采用入口集合＋程序＋约束，完整定义不可只传原文或单个算子 |
| Result不依赖统一changed | 消费实际对象、数值、逐部分状态和事件；修饰引用表示已登记，PaymentReceipt独立判断规则上是否支付 |

以下边界继续保留：draw与普通transfer；kill／banish／discard／recycle／burn；move与recall；copy／copy_text／copy_abilities；普通战力、基础战力、装备及增益贡献；原选择位置与实际入场位置；瞬时给予动作与持续属性重算。

## 版本与核验范围

V3.1按原字节存档，SHA-256为`ab3923ba0ab876d2d3c95c8d6bcf13b0cf8ee0a9829ea504935ee7723a72badf`。V4为新文档接口，当前入口basic-operators-api.md与basic-operators-api-v4.md一致；历史逐卡笔记仍绑定其原版本，未自动重写或上调覆盖率。

本次完成文档、完整71项迁移去向与签名／链接校核；没有改运行时代码，没有运行项目测试套件，没有执行V4全库逐卡复核。7张真实规则待核卡也不会因模型迁移而自动获得确认。

统一调度、成功结算触发与费用阶段保留官方规则要求；节点和字段名称是项目设计。[核心规则](https://cmsassets.rgpub.io/sanity/files/dsfx7636/news_live/5c7946f7c3b8c6e0faff85ab6dadc6d2e721ea94.pdf)、[Radiance官方FAQ](https://playriftbound.com/en-us/news/organizedplay/radiance-rules-faq-and-clarifications/)
