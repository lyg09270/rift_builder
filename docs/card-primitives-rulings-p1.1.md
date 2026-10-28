# P1.1：8张待核卡的规则复核

核验日期：2026-10-28。逐项复核本地卡文、目录勘误、官方核心规则及Origins／Spiritforged／Unleashed／Vendetta／Radiance公开说明。**3项可消除原疑点，5项仍保留核验状态；没有证据要求新增基本原语。** 这不是一次新的全库执行测试。

## 规则依据

- [官方规则中心](https://playriftbound.com/en-us/rules-hub/)列出的核心规则更新于2026-10-09；下载文件与[本地副本](references/riftbound/riftbound-core-rules-2026-10-09-en.pdf)字节相同，SHA-256为`94d41fee86f88b61c4157c0389c0595d990b98e5b42555c99d9f649ee64d1fec`。
- [Origins FAQ](https://playriftbound.com/en-us/news/rules-and-releases/riftbound-origins-faq/)有海兽钓钩的专门问答；它是历史解释材料，不能覆盖现行核心规则。[Origins勘误](https://playriftbound.com/en-us/news/rules-and-releases/riftbound-origins-card-errata/)确认先放逐再打出的新版文字。
- [Unleashed FAQ](https://playriftbound.com/en-us/news/rules-and-releases/unleashed-rules-faq-and-clarifications/)解释触发能力首部费用和后部指令内费用的区别。
- [Vendetta FAQ](https://playriftbound.com/en-us/news/rules-and-releases/vendetta-rules-faq-and-clarifications/)及[最新版补充说明](https://playriftbound.com/en-us/news/announcements/core-rules-radiance-patch-notes-effective-october-16-2026/)用于检查关联指令、信息引用与区域变化。

## 逐卡结论

| 卡牌 | 核验结论 | 对算子／流程的影响 |
| --- | --- | --- |
| 0066 海兽钓钩／Baited Hook | **原疑点已解决。** 自身能力实际摧毁该单位时，读取死亡前战力；死亡被替代时没有“被摧毁单位”，不能选择后续单位。若目标提前离场，同样不能选；查看与回收仍执行。Origins FAQ有专门回答，现行359.3.e.12–14支持此区分。 | 修正卡牌绑定：候选战力阈值依赖实际kill回执；不得无条件预存目标战力。沿用`zone_change`、`information_access`、`order_change`。 |
| 0172 莱卓斯指挥官／Commander Ledros | **按通用规则可解决原疑点，属于规则推导。** 355.1声明可选额外费用，356计算折扣，357先付资源再处理动作费用；203.2／357.2.a规定付款动作被替代仍视为已付。折扣按已承诺支付的这组额外费用计算，不等实际死亡事件发生后再重新定价。无法合法支付时不能定稿；不能凭空选择不能支付的单位。 | `CostBinding`保存额外费用的选择和折扣关联；`PaymentReceipt`与实际死亡收据分开。已有`cost_rule_add`足够。 |
| 0201 曼舞手雷／Dancing Grenade | **仍待核。** 已确认初次造成2点伤害、目标控制者可按任意符能1重打；当前公开材料未充分说明重打与124区域身份规则的衔接、伤害历史保留方式及Bonus精确生效窗口。不能给出未经证实的固定伤害序列。 | 候选继续使用`damage_record`、`damage_rule_add`和link；不为不确定解释新增原语。 |
| 0286 沙漠皇帝／Emperor of the Sands | **仍待核，主要为文本版本问题。** 821确认百炼是打出触发能力，因此通常打出沙兵时两种文本结果相同；不能据此证明“你的沙兵”和“你打出的沙兵”在夺控、未打出直接进入及关键词查询时等价。目录没有两版间的正式勘误记录。 | 两个文本组分别保留；不把同一选择器假装为已核定的规范版本。`ability_add`可表达各候选。 |
| 0338 嚼火者手雷／Flame Chompers | **仍待核，已收窄。** 204.1.c／383.3.b确认首部付款属于触发能力定稿费用；420.3.b又要求后续打出遵循通常流程，除非效果另有说明。尚未找到足够明确的专门依据，确定此处“pay…to play”是否还隐含改变后续基础费用。不能把一般首部费用规则直接当成免费打出的证明。 | 触发付款与后续play的CostBinding分别保留；后者政策未核不得执行。现有费用API能够表示候选。 |
| 0453 不朽凤凰／Immortal Phoenix | **仍待核，已收窄。** 383.2.c.1明确自己被法术杀死后可触发；首部Energy1／Fury1费用阶段也已确认。未决点仍是后续play基础费用政策，与嚼火者手雷相同。 | 保留Assault2和实际法术击杀归因；不默认免印刷费或重复收取印刷费。无需新增原语。 |
| 0541 奥义！雷铠／Lightning Rush | **按卡文和通用规则可解决原疑点，属于规则推导。** “其余”指本次查看集合中除所选牌外的牌，而非“减去实际成功抽到的牌”。选择后把集合绑定，抽取被替代不会把所选牌重新加入其余集合。余牌离开牌库后不强行追回，也不补搬新顶牌。 | 用已绑定对象执行`zone_change`。不把原集合转换成`burn(len(rest))`；符合441的真实顶牌入废仍由规则分类产生事件，卡牌程序不能任意指定BURN身份。 |
| 0640 诺克萨斯破坏者／Noxus Saboteur | **仍待核，主要为旧术语问题。** 425的Reveal是公开信息动作，811的从盖放打出是Play；811.5.a还规定盖放牌不以正面Hidden作通常特征查询。不能单凭中文“翻开打出”就把英文revealed确定为只禁止Play，也不能据此扩大成禁止所有区域的信息公开。未找到直接消除该措辞冲突的现行正式勘误。 | `permission_rule_add`足以表达不同限制，但规范动作／范围未定；候选禁止盖放Play不得视为已获规则认证。 |

## 必要修订

原语仍为35项。只澄清已有契约的三个边界：

1. 区分对象引用、实际动作回执、费用是否视为已付；不能共享一个成功布尔值。
2. 费用折扣可依赖定稿时声明的额外费用选择，资源先于非标准动作付款；不以后续实际死亡数回算已定稿费用。
3. “其余”集合在对应选择时绑定，不由后续动作实际完成集合倒推；精确集合迁移不以数量替换。

冻结P1报告、逐卡原稿与audit.json保留原结果；本文件为后续核验增量。新增JSON应同时保留冻结判定与本次结论，待核5张不能改标为语义通过。
