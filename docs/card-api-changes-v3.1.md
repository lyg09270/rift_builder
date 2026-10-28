# V3.1事件与规则契约补充

日期：2026-10-28。[本版API存档](basic-operators-api-v3.1.md) · [冻结V3参考](basic-operators-api-v3.md) · [第三轮评估](card-api-coverage.md)

本次按第三轮40张未完整覆盖卡的已记录缺口补齐API契约。正式函数仍为71个；新增的是事件种类、阶段、匹配参数、通用事件发布约定与规则键，没有恢复四个已合并的旧函数名。没有改动运行时代码、本地卡牌目录或逐卡分解结果。

## 补充项

| 第三轮缺口 | V3.1补充 | 涉及的第三轮未覆盖卡数 |
| --- | --- | ---: |
| 法术／卡牌成功结算后的打出触发 | PLAY.resolved；明确与finalized历史、entered入场及as_play过程引用的区别 | 24 |
| 主动能力使用触发 | USE_ABILITY.resolved；保存来源、费用特征与支付回执，反制不产生完成事件 | 2 |
| 盖放触发 | HIDE.complete，与从盖放打出的PLAY分开，保留隐藏信息边界 | 2 |
| 消耗增益触发 | SPEND_BUFF.complete；按实际消耗计数物逐个匹配，不将获得或离场清除当成消耗 | 1 |
| 弃牌触发及批次 | DISCARD.complete；支持同一指令一次、每张分别匹配，替代后的实际集合不混入未弃置牌 | 3 |
| 放逐触发 | BANISH.complete；支持按实际卡牌逐张匹配 | 1 |
| 对决开始触发 | SHOWDOWN_START.start；包括非战斗对决 | 1 |
| 战斗结束触发 | COMBAT_END.end；包含No Result，保存参加过的单位历史引用 | 2 |
| 强力及任意明确战力阈值转换 | STATE_TRANSITION.complete与BECOME_MIGHTY具名视图；在完整战力依赖重算后比较前后值 | 3 |
| 所有独立区域动作的入废替代 | ZONE_TRANSFER的统一发布、具名动作身份、transition_id、局部替代及去重契约 | 1 |
| 强制打出位置与冲突仲裁 | modify_rule的PLAY_LOCATION_REQUIREMENT键及PlayConstraint字段；区分正向要求与硬性禁止 | 1 |

卡数合计41项，Katarina, Reckless同时涉及盖放和打出完成阶段，因此对应40张卡。表中只统计第三轮未覆盖集合；例如Flame Chompers另有弃置入口问题，但其整体状态仍因费用解释待核而归入7张待核卡。

## 规则依据与接口选择

- 卡牌打出触发按成功结算判断，打出历史按定稿判断；下一张打出修饰仍绑定打出流程。主动能力的使用触发同样在结算后发生。相应接口采用PLAY.resolved与USE_ABILITY.resolved，未将它们混入finalized。[核心规则420.4、420.5、377.2](https://cmsassets.rgpub.io/sanity/files/dsfx7636/news_live/5c7946f7c3b8c6e0faff85ab6dadc6d2e721ea94.pdf)
- 正向位置要求先共同满足相容要求，冲突时选择一组；禁止／only规则仍必须遵守。接口通过PLAY_LOCATION_REQUIREMENT记录要求，不用restrict_action制造更强的禁止。[核心规则355.17](https://cmsassets.rgpub.io/sanity/files/dsfx7636/news_live/5c7946f7c3b8c6e0faff85ab6dadc6d2e721ea94.pdf)、[Vendetta官方FAQ](https://playriftbound.com/en-us/news/rules-and-releases/vendetta-rules-faq-and-clarifications/)
- 战斗结束、强力阈值与消耗增益分别采用独立事件边界。状态转换覆盖装备、持续效果等依赖变化，不只监听算术加减。[核心规则468.7、709、702.2](https://cmsassets.rgpub.io/sanity/files/dsfx7636/news_live/5c7946f7c3b8c6e0faff85ab6dadc6d2e721ea94.pdf)

EventPattern的granularity、事件ID与通用区域视图的发布／去重方式是本项目的接口设计，用于保留上述规则语义；这些字段名称不是官方规则术语，也不表示已有执行引擎实现。

## 评估版本边界

第三轮的1106张笔记、1059张确认、7张待核、40张未完整覆盖及95.75%确认覆盖率均绑定冻结V3，保留原结论。该版SHA-256为`2530366c3f814b7f77f992ffe36c7c5bf3a0ad5fa23812de34119a6ea4dd03a3`，已按原字节存入basic-operators-api-v3.md。

本次完成契约补充，尚未据V3.1重新逐卡分解并复核，因此没有把原40张直接改成确认覆盖，也没有上调覆盖率。7张待核卡的费用、历史计数、印刷范围及剩余集合解释仍须各自核验；新增事件不会自动解决这些问题。
