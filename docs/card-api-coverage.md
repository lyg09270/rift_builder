# 第三轮：71函数API全库阅读与覆盖评估

[本轮冻结V3参考](basic-operators-api-v3.md) · [修订与简化依据](card-api-changes-v3.md) · [逐卡笔记](card-operator-reading.md) · [本轮校核](operator-audits/round-3-validation.md) · [冗余审查](operator-audits/round-3-redundancy.md) · [原第二轮报告](operator-audits/round-2-coverage.md)

状态：全部本体完整复读完成。已读**1106/1106**；API固定指纹`2530366c3f814b7f77f992ffe36c7c5bf3a0ad5fa23812de34119a6ea4dd03a3`。

**结论：尚未完全覆盖。**1059张确认覆盖，7张待核验，40张未完整覆盖；确认覆盖率**95.75%**。71个函数的2335次调用均符合API签名，但没有独立测得语义正确率，不能称为正确率100%。

当前参考已进入[V4](basic-operators-api.md)，见[V4迁移表](card-api-changes-v4.md)与[V4流程契约](card-resolution-v4.md)；此前的[V3.1契约补充](card-api-changes-v3.1.md)另有存档。本报告及下列卡牌状态仍是冻结V3的第三轮结果，尚未按新版重新评估。

## 口径

本轮重新读取每个本体全部可用EN／SC／TC卡面规则、装备效果、基础属性与勘误；每张有独立本轮记录。不是把第二轮成功记录直接重命名。自动语法迁移只供人工对照，不能自动判通过。所有图片未逐图全库核验。

**确认覆盖率**＝本轮完整分解且没有已知语义错误、API缺口或规则待核的卡数÷1106。该指标把待核与未读排除分子。**结构表达率**＝已有登记API／闭集宏候选结构的卡数÷1106；它包括语义待核草稿，不代表可执行正确，更不能单凭这一数值宣称全部真实效果完整覆盖。

核验项目：入口／时点／次数；控制者／拥有者／行动者；目标／范围／信息权限；费用／数值／快照；顺序／批次／实际结果；期限／关联／关键词／勘误。没有独立裁判真值或执行引擎，不把人工确认率称为实战正确概率。

| 指标 | 分子／分母 | 本轮结果 |
| --- | ---: | ---: |
| 完整复读 | 1106/1106 | 100.00% |
| 确认覆盖率 | 1059/1106 | 95.75% |
| 结构表达率（含待核草稿） | 1066/1106 | 96.38% |
| 已读但语义待核 | 7 | — |
| 已读但API未覆盖 | 40 | — |
| 尚未阅读 | 0 | — |
| API调用签名符合率 | 2335/2335 | 100.00% |
| 独立语义正确率 | 未测得 | — |

## 未覆盖问题分类

| 契约缺口 | 未覆盖卡数 | 说明 |
| --- | ---: | --- |
| 打出成功结算后的触发阶段 | 24 | `PLAY.finalized`不能代替成功结算后的触发；`entered`不覆盖法术 |
| 缺少事件种类或状态转换事件 | 15 | 战斗结束、盖放、对决开始、主动能力使用、消耗增益、弃置、放逐、强力／战力阈值转换 |
| 跨独立区域动作的替代事件契约 | 1 | 不能凭`ZONE_TRANSFER`存在就假定其覆盖所有独立动作的替代入口 |
| 强制打出目的地与冲突仲裁 | 1 | 正向的必须打出位置不能改写成优先级不同的禁止规则 |

分类有交集：Katarina, Reckless同时涉及盖放与打出完成阶段，故41项问题对应40张卡。7张待核卡另列，不计入确认覆盖分子。完整卡名、入口与候选调用见下表及链接笔记。

## 未完整覆盖及待核

| 卡牌 | 状态 | 具体问题 |
| --- | --- | --- |
| [0002 Abandoned Hall](card-operator-reading/0001-0100.md#card-0002) | uncovered | EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [0006 Affectionate Poro](card-operator-reading/0001-0100.md#card-0006) | uncovered | EVENT_KIND:缺COMBAT_END，原生战斗结束触发也须采用闭集EventPattern，COMBAT_WIN/TIE不能代替所有战斗结束。 |
| [0008 Agony’s Embrace](card-operator-reading/0001-0100.md#card-0008) | uncovered | EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [0052 Astral Heron](card-operator-reading/0001-0100.md#card-0052) | uncovered | EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [0067 Bandle Scouts’ Academy](card-operator-reading/0001-0100.md#card-0067) | uncovered | EVENT_KIND:缺HIDE；盖放不是PLAY，不能用从盖放打出替代该触发入口。 |
| [0088 Black Market Broker](card-operator-reading/0001-0100.md#card-0088) | uncovered | EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [0156 Chemtech Cask](card-operator-reading/0101-0200.md#card-0156) | uncovered | EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [0172 Commander Ledros](card-operator-reading/0101-0200.md#card-0172) | verify | VERIFY:Commander Ledros的每个以此方式被摧毁数量在杀费用被替代时如何参与预先总费计算，本轮未找到足够逐卡裁定；不沿用先杀再算费。 |
| [0196 Curator of the Sands](card-operator-reading/0101-0200.md#card-0196) | uncovered | EVENT_KIND:本卡明确包括使用主动能力；闭合表未定义ACTIVATE/USE_ABILITY的完成入口，不能只覆盖单位与装备打出。 |
| [0201 Dancing Grenade](card-operator-reading/0201-0300.md#card-0201) | verify | VERIFY:曼舞手雷跨重打历史次数与Bonus适用时点未核；不得写死伤害序列或执行未知候选。 |
| [0206 Darius, Trifarian](card-operator-reading/0201-0300.md#card-0206) | uncovered | EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [0235 Diana, Lunari](card-operator-reading/0201-0300.md#card-0235) | uncovered | EVENT_KIND:缺SHOWDOWN_START；原生Ability.trigger也须采用合法EventPattern，单有pay/predict/reveal/draw能力体不足以完整覆盖。 |
| [0236 Diana, No Longer Human](card-operator-reading/0201-0300.md#card-0236) | uncovered | EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [0257 Dragon Roost](card-operator-reading/0201-0300.md#card-0257) | uncovered | PLAY_LOCATION_REQUIREMENT:grant_permission只扩大许可，restrict_action会形成can't而错误压过其他正向要求；缺可冲突仲裁的强制打出目的地绑定契约。 |
| [0284 Ember Monk](card-operator-reading/0201-0300.md#card-0284) | uncovered | EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [0286 Emperor of the Sands](card-operator-reading/0201-0300.md#card-0286) | verify | VERIFY:Your Sand Soldiers与Sand Soldiers you play在区域、控制及关键词特征引用上的范围待核，不能以普通打出场景相同证明所有场景等价。 |
| [0292 Endless Riches](card-operator-reading/0201-0300.md#card-0292) | uncovered | EVENT_IDENTITY:替代任何非主牌堆入己废牌需要覆盖DISCARD等独立区域动作；V3未明确所有这些动作均发布带身份的ZONE_TRANSFER.before，现有枚举不能证明无遗漏。 |
| [0300 Evelynn, Consuming](card-operator-reading/0201-0300.md#card-0300) | uncovered | EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [0315 Fae Dragon](card-operator-reading/0301-0400.md#card-0315) | uncovered | EVENT_KIND:缺少明确的SPEND_BUFF或BUFF事件mode=spend契约，不能把消耗增益入口当成获得BUFF入口；基本动作体可表达但完整能力入口未覆盖。 |
| [0331 Fiora, Worthy](card-operator-reading/0301-0400.md#card-0331) | uncovered | EVENT_KIND:没有BECOME_MIGHTY或状态谓词由假变真事件契约；仅以MIGHT_CHANGE会遗漏装备、持续能力变化造成的强力转换。 |
| [0338 Flame Chompers](card-operator-reading/0301-0400.md#card-0338) | verify | VERIFY:触发定稿支付Fury1后续打出的基础费用政策尚无可靠官方核验，policy未绑定，禁止执行或计入确认覆盖；闭合事件表亦未明确DISCARD入口。 |
| [0343 Forbidden Technique](card-operator-reading/0301-0400.md#card-0343) | uncovered | EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [0349 Forgotten Library](card-operator-reading/0301-0400.md#card-0349) | uncovered | EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [0384 Grand Duelist](card-operator-reading/0301-0400.md#card-0384) | uncovered | EVENT_KIND:缺BECOME_MIGHTY或状态谓词假转真事件，算术MIGHT_CHANGE不足覆盖装备与持续修饰引起的强力转换。 |
| [0412 Heart of the Tempest](card-operator-reading/0401-0500.md#card-0412) | uncovered | EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [0453 Immortal Phoenix](card-operator-reading/0401-0500.md#card-0453) | verify | VERIFY:触发基础费与后续打出基础费的关系未获权威明确核验，policy仍未绑定；不能默认免费或重复收费，候选程序不执行不计确认覆盖。 |
| [0490 Jinx, Rebel](card-operator-reading/0401-0500.md#card-0490) | uncovered | EVENT_KIND:缺DISCARD.complete及同次弃一或多牌的批次契约；不能以每卡ZONE_TRANSFER触发代替同批一次，完整能力未覆盖。 |
| [0497 Katarina, Reckless](card-operator-reading/0401-0500.md#card-0497) | uncovered | EVENT_KIND:缺HIDE完成事件；盖放不是打出，不能把两条触发合并成同一PLAY入口。；EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [0523 Lady of Luminosity, Starter](card-operator-reading/0501-0600.md#card-0523) | uncovered | EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [0541 Lightning Rush](card-operator-reading/0501-0600.md#card-0541) | verify | VERIFY:rest按选定之外或实际抽取之外的定义及抽取被替代后指定余牌burn授权未完成权威核验，原候选不作为已确认可执行分解。 |
| [0559 Lux, Illuminated](card-operator-reading/0501-0600.md#card-0559) | uncovered | EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [0570 Mask Mother](card-operator-reading/0501-0600.md#card-0570) | uncovered | EVENT_KIND:缺明确DISCARD完成事件；不能在未声明通用区域事件必含弃置事件身份及其触发语义的情况下计完整覆盖。 |
| [0573 Master of Shadows](card-operator-reading/0501-0600.md#card-0573) | uncovered | EVENT_KIND:未明确BANISH完成事件；ZONE_TRANSFER表仅列动作身份数据而未约定所有独立区域动作会发布对应通用事件，不能凭此补造放逐入口。 |
| [0588 Meticulous Restorationist](card-operator-reading/0501-0600.md#card-0588) | uncovered | EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [0615 Mournful Witness](card-operator-reading/0601-0700.md#card-0615) | uncovered | EVENT_KIND:缺COMBAT_END，COMBAT_WIN或COMBAT_TIE不能替代所有自己参加过的战斗结束事件。 |
| [0640 Noxus Saboteur](card-operator-reading/0601-0700.md#card-0640) | verify | VERIFY:需要权威确认该旧卡revealed的规则含义是从盖放打出而非所有公开信息动作；当前限制play草稿未获完整核验。 |
| [0679 Piltovan Guidebot](card-operator-reading/0601-0700.md#card-0679) | uncovered | EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [0704 Prize of Progress](card-operator-reading/0701-0800.md#card-0704) | uncovered | EVENT_KIND:缺ACTIVATE或USE_ABILITY事件，PLAY表只承诺card/item而未定义装备主动使用流程的触发身份，不可用打出gear事件冒充。 |
| [0732 Ravenbloom Student](card-operator-reading/0701-0800.md#card-0732) | uncovered | EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [0756 Renekton, Brute](card-operator-reading/0701-0800.md#card-0756) | uncovered | EVENT_KIND:缺通用战力阈值假转真事件；MIGHT_CHANGE仅算术修改，装备贴附与持续效果重算导致跨十点阈值不能完整捕获。 |
| [0767 Revna the Lorekeeper](card-operator-reading/0701-0800.md#card-0767) | uncovered | EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [0803 Sanctum Conservator](card-operator-reading/0801-0900.md#card-0803) | uncovered | EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [0812 Scrapheap](card-operator-reading/0801-0900.md#card-0812) | uncovered | EVENT_KIND:缺DISCARD完成入口，不能只因其他两个入口有定义就计整张卡覆盖。 |
| [1044 Viktor, Innovator](card-operator-reading/1001-1100.md#card-1044) | uncovered | EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。 |
| [1048 Virtuoso](card-operator-reading/1001-1100.md#card-1048) | uncovered | EVENT_STAGE:规则420.4.a是法术成功结算后的打出触发；PLAY.finalized过早且被反制也发生，entered只覆盖永久物，闭合表缺PLAY.resolved/complete。 |
| [1093 Yordle Explorer](card-operator-reading/1001-1100.md#card-1093) | uncovered | EVENT_STAGE:缺PLAY.resolved/complete用于法术成功结算后的打出触发，不能用PLAY.finalized把被反制法术也计入触发。 |
| [1102 Zero Point Inflection](card-operator-reading/1101-1106.md#card-1102) | uncovered | EVENT_STAGE:第一能力须在PLAY成功结算后触发，闭合事件表缺法术resolved/complete阶段；DRAW触发及后续动作体可表达但整卡未覆盖。 |

## 本轮修订及简化

73→71函数：ready／exhaust合为orient；empower／disempower合为change_empowerment。保留动作模式、事件身份、成本及叠层限制。其余接口保留理由见[简化依据](card-api-changes-v3.md)。

每条人工记录保留原文组指纹与V3 API指纹。原始目录及5542个原文规则／装备字段未改动。本轮读取2771组不同语言／效果文本，保留49张DATA来源问题及51张LANG语言／版本差异；这些问题集合与覆盖状态不是同一统计口径。确认覆盖不代表全部语言及全部印刷均无缺文。未逐图核验9039条印刷图片。

文档接口没有对应的执行引擎。本轮不运行项目测试套件；结构核对只说明调用名、签名、引用与原文留存的一致性。

