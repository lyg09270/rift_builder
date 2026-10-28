# P1原语全库阅读与覆盖评估

[逐卡笔记与编写约定](card-primitives-reading-p1.md) · [冻结35原语](basic-primitives-v4-p1-frozen.md)

本轮已完整复读 **1106/1106** 张本体；确认表达覆盖1092，待核8，未完整覆盖6，未读0。
固定分母确认表达覆盖率：**98.73%**。本轮全库阅读已完成，结果仍未达到100%覆盖。

本轮是卡牌模型＋具名模板＋35原语的表达审阅与文档调用检查；不是35原语执行引擎测试，也没有独立测得游戏语义正确率。未知费用和语言／印刷差异继续保留，不按零或白板处理。

API SHA-256：`f76a76027f24165662f8e010d69a5ddad34b31ea132cda8fe6448878422462a6`。

## 未覆盖与待核

| 卡牌 | 判定 | 问题 |
| --- | --- | --- |
| [0038 Applied Researchers](card-primitives-reading-p1/0001-0100.md#card-0038) | uncovered | COST_FLOOR:P1 CostRule闭集未登记费用最低Energy1，不能仅有energy_delta/power_discount就隐含此约束。 |
| [0066 Baited Hook](card-primitives-reading-p1/0001-0100.md#card-0066) | verify | VERIFY_KILLED_REFERENCE:杀友军被替代时the killed unit能否继续提供后续合格战力阈值须进一步权威核验，不默认与实际杀成功等价。 |
| [0075 Battering Ram](card-primitives-reading-p1/0001-0100.md#card-0075) | uncovered | COST_FLOOR:Energy最低1未在P1 CostRule字段中登记，旧change文字不能充当新API参数。 |
| [0172 Commander Ledros](card-primitives-reading-p1/0101-0200.md#card-0172) | verify | VERIFY_LEDROS_COST:摧毁费用被替代后每个killed的折扣计数与预先总费用计算关系尚未获得可靠逐卡核验。 |
| [0201 Dancing Grenade](card-primitives-reading-p1/0201-0300.md#card-0201) | verify | VERIFY:同实体重打时历史伤害次数快照及Bonus生效窗口待官方裁定，不能确认完整语义覆盖。 |
| [0273 Eager Apprentice](card-primitives-reading-p1/0201-0300.md#card-0273) | uncovered | COST_FLOOR:CostRule闭集缺Energy最低一的字段，减一不能完整表达该卡费用规则。 |
| [0286 Emperor of the Sands](card-primitives-reading-p1/0201-0300.md#card-0286) | verify | VERIFY:Your Sand Soldiers和Sand Soldiers you play范围在非普通打出情境下未裁定，暂不能证明全场景等价。 |
| [0338 Flame Chompers](card-primitives-reading-p1/0301-0400.md#card-0338) | verify | VERIFY:弃置触发支付Fury1后打出所用基础费用政策未核，不能执行未绑定policy或计为确认覆盖。 |
| [0419 Herald of Scales](card-primitives-reading-p1/0401-0500.md#card-0419) | uncovered | COST_FLOOR:冻结CostRule未定义最低一及修饰前值求值序；不能用未授权动态费用读取绕过缺字段。 |
| [0453 Immortal Phoenix](card-primitives-reading-p1/0401-0500.md#card-0453) | verify | VERIFY:触发Energy1Fury1付款后自身废牌打出基础费用政策仍未核实，不默认免费或重复收费。 |
| [0541 Lightning Rush](card-primitives-reading-p1/0501-0600.md#card-0541) | verify | VERIFY:指定抽取被替代时rest集合及指定余牌burn授权未取得充分裁定，不能确认全情境。 |
| [0640 Noxus Saboteur](card-primitives-reading-p1/0601-0700.md#card-0640) | verify | VERIFY:旧卡revealed的官方术语含义未确认，不能直接等同从盖放打出或全部信息公开动作。 |
| [0916 Stargazer](card-primitives-reading-p1/0901-1000.md#card-0916) | uncovered | COST_FLOOR:Flow法术降Energy最低一的字段及费用中间值求值序未在冻结CostRule定义，不能用自然语言差值绕过。 |
| [1038 Vex, Cheerless](card-primitives-reading-p1/1001-1100.md#card-1038) | uncovered | COST_FLOOR:战斗中友方法术Energy最低一不在冻结CostRule契约；可表达敌方加费不等于整卡完整覆盖。 |

## 检查结果

| 指标 | 结果 |
| --- | --- |
| 本体逐卡阅读 | 1106/1106，100% |
| EN／SC／TC规则与效果原文组 | 2771组，全部已记录 |
| 所有能力均确认可表达 | 1092/1106，98.73% |
| 契约缺口 | 6张 |
| 待核验 | 8张，不进入覆盖分子 |
| 原语名称及参数签名检查 | 2767/2767处，100% |
| 已出现的闭集字面值检查 | 538处，无越界 |
| 实战语义正确率 | 未测；没有35原语执行引擎或独立对局判定基准 |

签名检查验证函数名、实参数量与关键字名称；不是所有符号绑定值的动态类型检查，也不证明目标、费用、替代、时序已被引擎正确执行。未覆盖和待核条目保留候选调用及阻塞原因，不作为可执行的通过案例。

规范能力采用已核定英文及目录勘误；所有可用中文和印刷差异一起复读。100张保留DATA／LANG来源问题，详见逐卡条目。这些差异不能解释为所有语言文本彼此等价，卡面文本复读也不等于9039份印刷图逐图视觉认证。

[机器可读检查记录](card-primitives-reading-p1/audit.json)保存冻结输入指纹、各原语调用数及检查边界。调用数是文档静态调用位置，分支和循环不按实际对局次数计。

## 契约缺口与简化复核

6张未覆盖都涉及费用降低但Energy最低为1。CostRule没有显式最低值字段，也未约定读取“本修饰施加前费用”的求值阶段；不能把最低值藏进自然语言差值。后续应先补费用规则的结构化字段及多修饰求值顺序，再重新检查这些牌，不必为此新增基本原语。

35项原语在全库分解中均实际出现，未发现可直接删除且行为完全等价的一对API；这不等于已证明35是理论最小数量。以下相似接口仍有不同职责：

| 相似接口 | 保留原因 |
| --- | --- |
| instantiate／zone_change | 建立新身份与迁移已有身份不同；play仅对新token先创建。 |
| zone_change／location_change／order_change | 换区域、场上换位置、同牌堆重排分别保存不同身份与规则。 |
| damage_record／damage_clear | 真实伤害与清除伤害不是正负同一数值操作，事件原因不同。 |
| ability_add／ability_mask／ability_patch | 授新能力、临时失活与有限元数据修改不能互换。 |
| 7项分域规则登记 | 费用、伤害、产费、入场、指令参数、权限、固定规则键各有闭集；合成通用modify会把复杂性藏进参数。 |

## 本轮纠正

逐卡复读修正了旧稿的自身play递归演示、父项提前等待子play定稿、当前位置与事件地点混用、选择结果未显式累计、关键词归属及独立入口串行混排。最终调用检查又发现并补展开一处嵌在布尔表达式里的banish，复查后无残留旧ops调用。原语API保持冻结，未借中途扩充接口提高覆盖率。

## 已写入批次

- [0001–0100](card-primitives-reading-p1/0001-0100.md)：100张。
- [0101–0200](card-primitives-reading-p1/0101-0200.md)：100张。
- [0201–0300](card-primitives-reading-p1/0201-0300.md)：100张。
- [0301–0400](card-primitives-reading-p1/0301-0400.md)：100张。
- [0401–0500](card-primitives-reading-p1/0401-0500.md)：100张。
- [0501–0600](card-primitives-reading-p1/0501-0600.md)：100张。
- [0601–0700](card-primitives-reading-p1/0601-0700.md)：100张。
- [0701–0800](card-primitives-reading-p1/0701-0800.md)：100张。
- [0801–0900](card-primitives-reading-p1/0801-0900.md)：100张。
- [0901–1000](card-primitives-reading-p1/0901-1000.md)：100张。
- [1001–1100](card-primitives-reading-p1/1001-1100.md)：100张。
- [1101–1106](card-primitives-reading-p1/1101-1106.md)：6张。
