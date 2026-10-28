# 69算子 API：卡牌覆盖复读

[逐卡原阅读笔记](card-operator-reading.md) · [算子API](basic-operators-api-v1.md) · [算子功能重复检查](card-api-overlap-v1.md)

状态：全目录复读完成；已复读 **1106 / 1106** 个卡牌本体。
API SHA-256：`408787a290b9677c4956082fbd3b5f00d611ca7ed983700d3f48800fc029a95d`。
目录 SHA-256：`ad521068ff70def757a00ff18f049583e1e5dffdc3e0152515eb90007b54ca05`。

## 结论

**当前69个API不能完整覆盖本地全目录。** 已对全部本体写入调用／明确缺口；完整阅读覆盖不等于效果表达完整覆盖。未修改API参考来绕过缺口。

## 阅读范围

- 本地来源：`data/sources/openrift/catalog.json`，1106个本体，9039个印刷记录；递归纳入side2。
- 实际对照2771组EN／SC／TC规则＋装备效果文本变体，73个目录勘误。禁牌、token、提醒物及空白文本牌也纳入，未跳过。
- 范围固定为该本地快照。非上述三种语言的译文和所有卡图的逐图视觉核对不在本次完成声明内；没有用缺失译文推测效果。

## 判定口径

每张重新对照全部EN／SC／TC规则与装备效果变体及目录勘误，直接修改原分批笔记。接口保持69个，不增添调度器或万能效果函数来掩盖缺口。

调用中的选择器、费用、数值表达式等均在该牌参数表给出类型和精确含义。不同能力入口用代码注释分开，不表示全部能力连续执行。普通触发、主动时机、历史条件作为已绑定执行上下文列明；这不代表69个动作API本身实现了完整事件调度。新建未来触发、自反链项、改写待发生事件等若没有明确接口，单列未覆盖。

`THIS_PLAY`、`WHILE_CONDITION`、`WHILE_ATTACHED`等局部名称均在对应牌的参数表绑定为API的Duration值；不是新算子。大写关键词及规则名表示参考API的具名标识。选择、费用历史和亮出快照须由明确上下文提供，不能靠调用代码猜测。

固有关键词和基础属性保留原定义；写出内部展开时替代原宏执行，不叠加运行。Repeat、Flow和少量提醒模板未独立展开者另标“委托未展开”，不等于其宏委托一定不可用，也不算独立映射证明。无独立文本动作的提醒物／纯属性牌不伪造空算子。

| 状态 | 本体数 |
| --- | ---: |
| 已绑定上下文内覆盖 | 902 |
| 部分覆盖 | 157 |
| 委托未展开 | 35 |
| 无独立文本动作 | 12 |
| 尚未复读 | 0 |

“已绑定上下文内覆盖”仅表示在表内前置状态、选择、关键词定义和普通能力入口已提供时，效果体可表达；不是可直接运行的完整卡牌程序，也不是全规则认证。费用对象与选择器等以API的具名类型绑定，尚无对应运行库供运行时验证。


## 无法完整覆盖的卡牌

以下分列明确缺口／契约疑点和宏未展开。来源缺文另外列出，不混算缺算子。同一卡可能有多个问题，每行链接到具体调用和缺失句段。

### 动作缺口及待澄清契约

| 卡牌 | 问题 |
| --- | --- |
| [0003 Acceleration Gate](operator-audits/round-1-reading.md#card-0003) | RUNE_READY:原效果也可选择符文，但ready只接受Permanent，Rune不属于该类型 |
| [0004 Acceptable Losses](operator-audits/round-1-reading.md#card-0004) | BATCH:各玩家装备应同批处理，逐个kill的清理和触发边界不等价 |
| [0004 Acceptable Losses](operator-audits/round-1-reading.md#card-0004) | ACTOR:卡面指定其他玩家执行摧毁或移动，但对应kill/move无执行玩家参数；不能以选择权正确冒充动作归属正确 |
| [0016 Albus Ferros](operator-audits/round-1-reading.md#card-0016) | BATCH:各单位不同消耗数量只能分次调用，尚无同一原始spend-any批次的定义；后续channel已按每个实际消耗分别调用，不再把它合为一次channel(N) |
| [0018 Alpha Strike](operator-audits/round-1-reading.md#card-0018) | REFLEXIVE:缺按实际死亡逐一创建gain_xp(1)待处理链项的API |
| [0020 Altar of Blood](operator-audits/round-1-reading.md#card-0020) | REPLACE:没有死亡前替代登记API，不能以死后heal/exhaust/recall冒充 |
| [0031 Angler Beast](operator-audits/round-1-reading.md#card-0031) | BATCH:transfer只有共同source/destination，无法保证多地点多拥有者同时转移，逐次循环不等价 |
| [0032 Angler Wyrm](operator-audits/round-1-reading.md#card-0032) | ACTOR:卡面指定其他玩家执行摧毁或移动，但对应kill/move无执行玩家参数；不能以选择权正确冒充动作归属正确 |
| [0037 Aphelios, Exalted](operator-audits/round-1-reading.md#card-0037) | RUNE_READY:规则133.5.a.1/161.1.a明确Rune不是Permanent，ready签名不能接受该符文集合 |
| [0045 Arise!](operator-audits/round-1-reading.md#card-0045) | REFLEXIVE:then do this的后续活跃须新待处理项，play返回链项不是已落地单位，无调度/链项到新实例关联接口 |
| [0048 Ashe, Focused](operator-audits/round-1-reading.md#card-0048) | DELAY:缺少登记actor未来据守时transfer回手的一次触发接口 |
| [0048 Ashe, Focused](operator-audits/round-1-reading.md#card-0048) | ACTOR:卡面指定对手执行reveal，但reveal只有viewers而没有行动玩家，不能把公开对象/观众正确当成执行者正确 |
| [0053 Atakhan](operator-audits/round-1-reading.md#card-0053) | ACTOR:卡面指定其他玩家执行摧毁或移动，但对应kill/move无执行玩家参数；不能以选择权正确冒充动作归属正确 |
| [0072 Baron Nashor](operator-audits/round-1-reading.md#card-0072) | CREATE_NEUTRAL:create要求controller为Player，新增战场应无人控制，不能传None |
| [0072 Baron Nashor](operator-audits/round-1-reading.md#card-0072) | AS_PLAY:无定稿中先创建战场再按是否创建改变入场目的地的明确阶段钩子 |
| [0076 Battle Mistress](operator-audits/round-1-reading.md#card-0076) | LEGEND_READY:ready只收Permanent，me为Legend；规则175明确传奇不是永久物，不能调用ready([me]) |
| [0077 Battle Preparations](operator-audits/round-1-reading.md#card-0077) | RUNE_READY:规则133.5.a.1/161.1.a明确Rune不是Permanent，ready签名不能接受该符文集合 |
| [0079 Beast Below](operator-audits/round-1-reading.md#card-0079) | BATCH:不同来源和不同拥有者目的地的同时回手缺少批次API |
| [0091 Blade Dancer](operator-audits/round-1-reading.md#card-0091) | LEGEND_READY:征服后的活跃me要求Legend目标，ready签名只接受Permanent |
| [0101 Blind Fury](operator-audits/round-1-reading.md#card-0101) | ACTOR:卡面指定对手执行reveal，但reveal只有viewers而没有行动玩家，不能把公开对象/观众正确当成执行者正确 |
| [0111 Blue Sentinel](operator-audits/round-1-reading.md#card-0111) | DELAY:无登记下个自己主阶段开始再add_resources的接口；expires只控制资源到期不是开始 |
| [0115 Bone Skewer](operator-audits/round-1-reading.md#card-0115) | REFLEXIVE:勘误if they do then do this要求成功执行后的独立眩晕链项，不能依据play定稿返回直接stun |
| [0115 Bone Skewer](operator-audits/round-1-reading.md#card-0115) | ACTOR:卡面指定对手执行reveal，但reveal只有viewers而没有行动玩家，不能把公开对象/观众正确当成执行者正确 |
| [0120 Boy Who Shattered Time](operator-audits/round-1-reading.md#card-0120) | NEXT_ABILITY:grant_ability作用于具体对象集合且无次数/下一次打出钩子，不能把尚未绑定的未来下一单位当成现有实例授自毁 |
| [0134 Bushwhack](operator-audits/round-1-reading.md#card-0134) | ENTRY:play.entry只能修改一次打出，缺登记本回合所有己军未来打出/生成活跃入场的修饰API，不能用READY代替 |
| [0138 Call to Battle](operator-audits/round-1-reading.md#card-0138) | ACTOR:卡面指定其他玩家执行摧毁或移动，但对应kill/move无执行玩家参数；不能以选择权正确冒充动作归属正确 |
| [0145 Carnivorous Snapvine](operator-audits/round-1-reading.md#card-0145) | RECIPROCAL:单次damage只有一个来源和统一数值，缺多来源不同数值的同时伤害批次；逐次damage可能提前致死清理 |
| [0152 Challenge](operator-audits/round-1-reading.md#card-0152) | RECIPROCAL:缺多来源不同数值的同时伤害批次；连续两次damage不等价 |
| [0162 Clash of Giants](operator-audits/round-1-reading.md#card-0162) | RECIPROCAL:无法用一个damage描述多来源互殴，逐次调用不能保证同时清理 |
| [0175 Confront](operator-audits/round-1-reading.md#card-0175) | ENTRY:缺本回合未来所有打出单位入场状态登记；不能反复READY，因为不应产生活跃事件 |
| [0185 Counter Strike](operator-audits/round-1-reading.md#card-0185) | PREVENT_ONCE:prevent_damage无uses，INFINITY在THIS_TURN持续会预防多次；UNTIL事件的消耗边界未规定，不能伪称一次性完整覆盖 |
| [0189 Crescent Strike](operator-audits/round-1-reading.md#card-0189) | DAMAGE_BATCH:damage.each只有统一数值；split会改变额外伤害按总池而非逐目标适用的语义，缺非分配式不同数值同批伤害 |
| [0195 Cull the Weak](operator-audits/round-1-reading.md#card-0195) | ACTOR:卡面指定其他玩家执行摧毁或移动，但对应kill/move无执行玩家参数；不能以选择权正确冒充动作归属正确 |
| [0196 Curator of the Sands](operator-audits/round-1-reading.md#card-0196) | RUNE_READY:规则133.5.a.1/161.1.a明确Rune不是Permanent，ready签名不能接受该符文集合 |
| [0201 Dancing Grenade](operator-audits/round-1-reading.md#card-0201) | CHAIN_REPLAY:缺清楚定义在自身执行中由新玩家重打同一链上牌、跨重打保留伤害次数及将额外伤害绑定新链项的流程；不能把当前法术复制当作再打 |
| [0207 Dark Child, Starter](operator-audits/round-1-reading.md#card-0207) | RUNE_READY:规则133.5.a.1/161.1.a明确Rune不是Permanent，ready签名不能接受该符文集合 |
| [0210 Dazzling Aurora](operator-audits/round-1-reading.md#card-0210) | REVEAL_UNTIL:reveal接收预绑定对象集合，没有依次揭示至首命中并停止的接口；预先提供revealed会越权读取秘密次序，以上仅结果已知后的片段 |
| [0212 Deadly Flourish](operator-audits/round-1-reading.md#card-0212) | DELAY:缺登记该实例本回合死亡触发打休眠金币的接口，不等于当下若死即产金币 |
| [0213 Death from Below](operator-audits/round-1-reading.md#card-0213) | REFLEXIVE:勘误do this要求等当前法术正常离链后新待处理项重打，不能在当前结算立刻play已假定在trash的me |
| [0216 Deceiver](operator-audits/round-1-reading.md#card-0216) | REFLEXIVE:缺另一个待处理项绑定实际进场Reflection后copy并grant_keyword(Temporary)；play返回链项不能当Unit |
| [0218 Decree of Discord](operator-audits/round-1-reading.md#card-0218) | BATCH:transfer无异来源/目的地映射的同时集合转移；不能逐次回手改变统计和清理 |
| [0222 Decree of Strength](operator-audits/round-1-reading.md#card-0222) | ACTOR:recycle签名没有行动玩家参数，只能回拥有者牌堆，不能明确归属该对手执行的回收动作 |
| [0225 Defiant Dance](operator-audits/round-1-reading.md#card-0225) | MODIFIER_BATCH:原句同一指令的两种修饰，API无明确原子批次边界，逐条登记是否暴露中间状态尚未约定 |
| [0241 Disintegrate](operator-audits/round-1-reading.md#card-0241) | REFLEXIVE:勘误if this kills it do this要求后续独立抽牌链项，不能直接凭damage回执在同一项抽牌 |
| [0243 Disposal Order](operator-audits/round-1-reading.md#card-0243) | ACTOR:回收动作须分别归属各拥有者，recycle无行动玩家参数，不能仅凭目的牌堆正确认定动作归属已覆盖 |
| [0244 Divine Judgment](operator-audits/round-1-reading.md#card-0244) | CHOICE_SHORTAGE:choose未规定候选不足minimum时效果中的尽可能选择；不能把恰选2变成可选0，也不能假定会自动放宽minimum |
| [0253 Downwell](operator-audits/round-1-reading.md#card-0253) | BATCH:不同玩家和场上区域的统一同时回手无对应批次参数 |
| [0257 Dragon Roost](operator-audits/round-1-reading.md#card-0257) | COST_DESTINATION:缺将特定额外费选择与该次必须目的地me绑定的明确结构；仅grant_permission增加可选地点不等于付后强制去该处 |
| [0259 Dragon’s Rage](operator-audits/round-1-reading.md#card-0259) | REFLEXIVE:勘误then do this要求新待处理项与后选目标；RECIPROCAL:两单位同时按各自战力互殴也缺多来源批次 |
| [0269 Dune Surfer](operator-audits/round-1-reading.md#card-0269) | RULE_NARROW:modify_rule的COMBAT_DAMAGE_ORDER仅列先/正常/后，未定义只对某分配玩家忽略Tank而保留其他顺序约束的变更 |
| [0280 Ekko, Recurrent](operator-audits/round-1-reading.md#card-0280) | RUNE_READY:规则133.5.a.1/161.1.a明确Rune不是Permanent，ready签名不能接受该符文集合 |
| [0288 Emperor’s Divide](operator-audits/round-1-reading.md#card-0288) | MOVE_BATCH:友方含盟友，单位可能须去不同控制者基地，单目的move不能保证同一移动批次 |
| [0292 Endless Riches](operator-audits/round-1-reading.md#card-0292) | REPLACE:缺原区域不是主牌堆时进入己废牌改放逐的通用区域事件替代登记 |
| [0321 Fanfare](operator-audits/round-1-reading.md#card-0321) | DELAY:缺创建本回合限3次的未来打出单位触发接口，不能结算时立即draw3 |
| [0333 Firebrand Raider](operator-audits/round-1-reading.md#card-0333) | ENTRY:缺使未来其他单位包括生成均活跃入场的持续修饰；单次play.entry不覆盖全局 |
| [0334 Firelights’ Hideout](operator-audits/round-1-reading.md#card-0334) | NEXT_ABILITY:grant_keyword没有下一次打出绑定或uses，无法在下一单位定稿前仅赋其急速，不应先猜一张手牌 |
| [0337 Fizz, Trickster](operator-audits/round-1-reading.md#card-0337) | CHAIN_EXIT:then recycle it是离链回收的延迟替代，不能在play只完成定稿时马上recycle未执行法术，也不能只处理成功结算漏无效化 |
| [0338 Flame Chompers](operator-audits/round-1-reading.md#card-0338) | PLAY_COST:原句pay Fury to play的成本在该触发与后续牌打出基础费之间的精确定稿角色未由API明确；不能默认付Fury后还再付印刷Energy3 |
| [0339 Flash](operator-audits/round-1-reading.md#card-0339) | MOVE_BATCH:友方含盟友，单位可能须去不同控制者基地，单目的move不能保证同一移动批次 |
| [0343 Forbidden Technique](operator-audits/round-1-reading.md#card-0343) | CHAIN_EXIT:勘误then banish this须与该次废牌重打关联的离链放逐替代，缺登记接口 |
| [0351 Forgotten Relic](operator-audits/round-1-reading.md#card-0351) | REFLEXIVE:缺从本次实际燃烧的单位卡保存战力并创建独立待处理加战力项；不能立刻修改不明目标 |
| [0367 Gangplank, Naval](operator-audits/round-1-reading.md#card-0367) | REPLACE:缺对来自选中自身法术/技能的三种待发生动作的替代；suppress_ability或restrict_action都不能补上改为+3 |
| [0372 Gearhead](operator-audits/round-1-reading.md#card-0372) | MIGHT_BONUS:该调用复现宿主总战力数值，但API没有逐装备战力贡献层字段修饰，未证明完整层次及归属等价 |
| [0376 Gentle Gemdragon](operator-audits/round-1-reading.md#card-0376) | RUNE_READY:规则133.5.a.1/161.1.a明确Rune不是Permanent，ready签名不能接受该符文集合 |
| [0377 Gentlemen’s Duel](operator-audits/round-1-reading.md#card-0377) | RECIPROCAL:加战力后双方同时按各自当前战力伤害缺多来源批次；不能串两个damage冒充 |
| [0382 Glowstone](operator-audits/round-1-reading.md#card-0382) | ACTOR:交付后是所选玩家执行recall，而recall无行动玩家参数；不能只因目的基地正确就认定归属正确 |
| [0391 Grim Resolve](operator-audits/round-1-reading.md#card-0391) | DELAY:缺登记关联u本回合赢战斗的延迟触发；给u新能力会改变能力来源和控制归属，不直接视为等价 |
| [0394 Guardian Angel](operator-audits/round-1-reading.md#card-0394) | REPLACE:缺宿主死亡前替代登记，不能在死亡已发生后杀装备加治疗冒充；DATA:SC缺printedEffectText的完整死亡替代 |
| [0396 Guards!](operator-audits/round-1-reading.md#card-0396) | REFLEXIVE:勘误then do this后续付费活跃需独立链项；play返回ChainItem，不能当成已入场Unit |
| [0404 Hall of Legends](operator-audits/round-1-reading.md#card-0404) | LEGEND_READY:ready仅接受Permanent，不能把Legend传入 |
| [0413 Heartening Soul](operator-audits/round-1-reading.md#card-0413) | LEGEND_READY:打出触发活跃友方Legend不符合ready的Permanent类型 |
| [0415 Heimerdinger, Academy Instructor](operator-audits/round-1-reading.md#card-0415) | REPLACE:缺对将要打出的衍生物模板/目的地作事件替代的接口，CREATE或GRANT_PERMISSION都不替换原Play |
| [0426 Hexplosive Minefield](operator-audits/round-1-reading.md#card-0426) | DELAY:缺登记按本次实际杀数在本回合末打Bomb的触发；不能立即play也不能按被选数量代替实杀数 |
| [0435 Highlander](operator-audits/round-1-reading.md#card-0435) | REPLACE:缺下一次死亡前事件替代，不能用prevent_damage处理非伤害摧毁，也不能用gain_ability改变延迟效果来源 |
| [0440 Hostile Takeover](operator-audits/round-1-reading.md#card-0440) | DELAY:控制权期限可表示，但缺回合末失控之后再recall该实例的延迟步骤；不能现在召回 |
| [0448 Hwei, Brooding Painter](operator-audits/round-1-reading.md#card-0448) | RUNE_READY:gear分支要求活跃至多2符文，但ready只接受Permanent，不可传Rune |
| [0449 Iascylla](operator-audits/round-1-reading.md#card-0449) | DELAY:缺把原战场引用保存到下一主阶段的可选移动触发登记 |
| [0453 Immortal Phoenix](operator-audits/round-1-reading.md#card-0453) | PLAY_COST:pay X to play与印刷基础费之间的精确费用角色需规则核定；不能默认只付X或默认重复收两份 |
| [0454 Imperial Decree](operator-audits/round-1-reading.md#card-0454) | DELAY:缺创建本回合全局受伤后摧毁的延迟触发；这不是将伤害本身改成致死的替代 |
| [0458 Incorrigible Construct](operator-audits/round-1-reading.md#card-0458) | PHASE:show_off定义为as-play定稿选择步骤，而play也自行执行整个定稿；API没有注入该中途回执以设置entry的明确钩子，不能假定前置调用是合法完整流程 |
| [0461 Insightful Investigator](operator-audits/round-1-reading.md#card-0461) | ACTOR:卡面指定对手执行reveal，但reveal只有viewers而没有行动玩家，不能把公开对象/观众正确当成执行者正确 |
| [0462 Invert Timelines](operator-audits/round-1-reading.md#card-0462) | PLAYER_BATCH:discard/draw各只接受一个player，未定义各玩家同一指令的批次/顺序边界；不能每人弃完立即抽来替代全体先弃后抽 |
| [0474 Ivern, Nurturer](operator-audits/round-1-reading.md#card-0474) | REFLEXIVE:若本次展示Bird/Cat/Dog/Poro需另一个待处理项选择己军增益，不能立即buff |
| [0483 Jayce, Brilliant Inventor](operator-audits/round-1-reading.md#card-0483) | RUNE_READY:原文something包含休眠符文，但ready的Permanent排除Rune；LEGEND_READY:也包含休眠传奇，而ready排除Legend |
| [0485 Jayce, Man of Progress](operator-audits/round-1-reading.md#card-0485) | OPTIONAL_COST:uses1何时消耗未定义；原文可保留授权先打别的合格装备，不能误作自动优惠首个合格装备；需明确可选使用与次数共享 |
| [0492 Kai’Sa, Evolutionary](operator-audits/round-1-reading.md#card-0492) | CHAIN_EXIT:缺该次链项离链时回收替代，不能在play仅定稿后立即recycle |
| [0502 Keeper of Masks](operator-audits/round-1-reading.md#card-0502) | REFLEXIVE:勘误then do this要求后续待处理项绑定实际新单位后copy；不在play返回ChainItem时直接copy |
| [0504 Keeper’s Verdict](operator-audits/round-1-reading.md#card-0504) | ACTOR:原文由拥有者执行放置，transfer/reorder无独立行动玩家参数；选择位置不等于行动归属 |
| [0507 Kharox](operator-audits/round-1-reading.md#card-0507) | REFLEXIVE:then may do this要求后续独立待处理项选该对手废牌单位免费打出，不能预先选刚燃烧的秘密牌 |
| [0522 Lady of Clockwork](operator-audits/round-1-reading.md#card-0522) | TYPE_EVOLUTION:set_base_might只接受Unit，set_types仅返回Modifier，没有转换后Unit视图/同对象类型重绑定约定，不能继续把静态Gear直接作为Unit传入 |
| [0525 Last Caress](operator-audits/round-1-reading.md#card-0525) | NEXT_ABILITY:权限次数可登记，但缺与同一下一单位成功打出后的buff关联；不能猜手牌先buff或单独授权两次 |
| [0541 Lightning Rush](operator-audits/round-1-reading.md#card-0541) | ACTION_ID:剩余指定牌通常仍在牌堆顶部，441.1将顶牌入废定义为Burn；但burn没有cards参数，不能保证先前抽取遭替代后仍准确处理原rest且保留Burn身份，现transfer片段不作完整证明 |
| [0565 Magma Wurm](operator-audits/round-1-reading.md#card-0565) | ENTRY:play.entry只作用一次打出，缺持续修改所有其他己军入场状态的API |
| [0568 Marching Orders](operator-audits/round-1-reading.md#card-0568) | RECIPROCAL:缺多来源同时互殴批次；REPEAT:也缺回响各遍定稿及执行结构 |
| [0580 Mechanical Bandit](operator-audits/round-1-reading.md#card-0580) | ACTOR:原文各玩家分别reveal，reveal无行动玩家参数；不能用viewers改成各自秘密看牌 |
| [0590 Minah Swiftfoot](operator-audits/round-1-reading.md#card-0590) | PLAYER_BATCH:各玩家动作的同一指令批次/顺序边界未在当前API中明确，不能仅有循环就证明完整等价 |
| [0592 Mindsplitter](operator-audits/round-1-reading.md#card-0592) | ACTOR:reveal无行动玩家，原文They reveal不能仅以p的reveal(hand)认定主体已准确表达 |
| [0595 Mirror Image](operator-audits/round-1-reading.md#card-0595) | REFLEXIVE:勘误then do this要求新待处理项绑定实际Reflection后copy/Temporary，不能把ChainItem当Permanent |
| [0598 Miss Fortune, Captain](operator-audits/round-1-reading.md#card-0598) | RUNE_READY:原文明确包括Rune，ready签名排除；LEGEND_READY:也包含Legend；LANG:TC未明确排除自身，EN/SC排除 |
| [0610 Mordekaiser, Twice Slain](operator-audits/round-1-reading.md#card-0610) | REPLACE:缺每回合一次可选死亡前替代登记，放弃较早替代不应消耗后续次数 |
| [0622 Nami, Headstrong](operator-audits/round-1-reading.md#card-0622) | DELAY:据守后需登记下一次实际打出的单位再ready/buff，不能当作活跃入场也不能预先增益手牌 |
| [0629 Neeko, Blending In](operator-audits/round-1-reading.md#card-0629) | SETUP:69API没有构筑阶段的选择/保存SetupChoiceRef接口，choose.bind_at仅trigger/finalization/resolution；只能消费已提供预选，不能声称整条构筑能力已覆盖 |
| [0633 Nocturne, Horrifying](operator-audits/round-1-reading.md#card-0633) | AS_VIEW:look/reveal没有查看/展示进行中进入此能力的钩子；不得改成事后普通触发或先抽到手再发动 |
| [0638 Noxian Guillotine](operator-audits/round-1-reading.md#card-0638) | DELAY:未鼓舞分支缺登记该实例下一次实际受伤后的摧毁触发 |
| [0652 Orianna, Mechanical Marvel](operator-audits/round-1-reading.md#card-0652) | OPTIONAL_COST:uses只有次数没有每回合重置或拒绝不消耗的明确政策，不能把once-each-turn做成留场期间仅一次 |
| [0656 Otterpus](operator-audits/round-1-reading.md#card-0656) | REPLACE:缺按玩家回合序号与增分来源改写GainPoint为Draw的事件替代接口 |
| [0666 Party Favors](operator-audits/round-1-reading.md#card-0666) | PLAYER_BATCH:各对玩家同一指令的共同抽牌/召出批次未明定，不能只凭串行两调用证明等价 |
| [0709 Promising Future](operator-audits/round-1-reading.md#card-0709) | PLAYER_BATCH:各玩家看牌与放逐回收的批次边界未约定 |
| [0709 Promising Future](operator-audits/round-1-reading.md#card-0709) | ACTOR:banish/recycle无执行玩家参数，不能完整保存各玩家行动归属 |
| [0727 Rally the Troops](operator-audits/round-1-reading.md#card-0727) | DELAY:缺少建立本回合未来友方单位打出触发的API，不能现在buff尚不存在的单位 |
| [0728 Rampage](operator-audits/round-1-reading.md#card-0728) | RECIPROCAL:友敌相互同时以不同来源和数值造成伤害，damage单一source无法完整表达 |
| [0733 Ravenborn Tome](operator-audits/round-1-reading.md#card-0733) | NEXT_ABILITY:下一法术身份必须动态绑定且只消耗一次选择，DamageSelection的绑定/消耗契约未定义 |
| [0735 Realm of Death](operator-audits/round-1-reading.md#card-0735) | RECIPROCAL:同时不同来源相互战力伤害无完整调用 |
| [0735 Realm of Death](operator-audits/round-1-reading.md#card-0735) | MODIFIER_BATCH:同一指令不同对象的不同战力修饰批次边界未定义 |
| [0751 Rell, Magnetic](operator-audits/round-1-reading.md#card-0751) | REFLEXIVE:打出成功后须新建待处理附着能力项，不能当场把ChainItem当Gear附着 |
| [0754 Renata Glasc, Industrialist](operator-audits/round-1-reading.md#card-0754) | ENTRY:play.entry只覆盖单次打出，不能建立所有未来token入场活跃规则，ready会制造额外事件 |
| [0785 Royal Entourage](operator-audits/round-1-reading.md#card-0785) | LEGEND_READY:两个API均排除Legend，无法覆盖本牌的两种朝向选择 |
| [0795 Sabotage](operator-audits/round-1-reading.md#card-0795) | ACTOR:reveal缺少执行玩家，对手展示无法记归属；SC又指定对手回收，而EN/TC未如此写 |
| [0799 Safety Inspector](operator-audits/round-1-reading.md#card-0799) | ACTOR:kill无执行玩家，无法记录每人摧毁自己单位 |
| [0799 Safety Inspector](operator-audits/round-1-reading.md#card-0799) | PLAYER_BATCH:各人选择与同时摧毁的批次未规定 |
| [0802 Sanction](operator-audits/round-1-reading.md#card-0802) | DELAY:回合结束的反向强化/解除是未来动作，empower无duration不能代替，缺建立延迟触发接口 |
| [0817 Scuttle Crab](operator-audits/round-1-reading.md#card-0817) | ACTOR:对手执行展示动作，但reveal只有viewers没有actor |
| [0827 Seraphic Wyvern](operator-audits/round-1-reading.md#card-0827) | REPLACE:缺少改写所有待发生channel事件并追加不同朝向一枚的接口 |
| [0843 Shadows of the Past](operator-audits/round-1-reading.md#card-0843) | BATCH:transfer只支持单来源/目的区域，跨玩家同时回手事件批次不能由逐个transfer保证 |
| [0845 Shady Spectacles](operator-audits/round-1-reading.md#card-0845) | AS_ATTACH:选择与复制发生于as attached内联过程，而非之后触发，attach未提供该过程挂钩 |
| [0847 Shard of Undoing](operator-audits/round-1-reading.md#card-0847) | ACTOR:kill没有各对手执行者参数 |
| [0847 Shard of Undoing](operator-audits/round-1-reading.md#card-0847) | PLAYER_BATCH:各对手选择和摧毁的批次未约定 |
| [0864 Siphon Power](operator-audits/round-1-reading.md#card-0864) | MODIFIER_BATCH:同指令两种不同修饰能否作为同批次未由API约定 |
| [0865 Siphoning Strike](operator-audits/round-1-reading.md#card-0865) | DELAY:没有建立被选单位本回合未来死亡触发召出符文接口 |
| [0872 Skyfall of Areion](operator-audits/round-1-reading.md#card-0872) | TRIGGER_RETYPE:没有改已有能力触发事件或扩增触发类别的API，modify_trigger_count只改次数 |
| [0875 Smite](operator-audits/round-1-reading.md#card-0875) | REPLACE:没有登记本回合该单位死亡改放逐的事件替代API，不能先kill再banish |
| [0876 Smoke and Mirrors](operator-audits/round-1-reading.md#card-0876) | MOVE_BATCH:move一次仅一个目的地，先后两次move不保证同时交换及战斗检查边界 |
| [0885 Sona, Harmonious](operator-audits/round-1-reading.md#card-0885) | RUNE_READY:缺少对Rune合法重置接口 |
| [0886 Soraka, Wanderer](operator-audits/round-1-reading.md#card-0886) | REPLACE:治疗/横置/召回动作本身存在，但缺少在死亡前取消并替代死亡事件的API |
| [0909 Stalking Wolf](operator-audits/round-1-reading.md#card-0909) | COST_DESTINATION:费用选择单位与打出位置定稿的前后关联缺少明确CostBinding/Permission链接契约 |
| [0913 Star Spring](operator-audits/round-1-reading.md#card-0913) | ACTOR:move没有执行玩家参数，本动作由actor执行而非固定p |
| [0914 Star-Crossed](operator-audits/round-1-reading.md#card-0914) | BATCH:单一transfer无法同批次跨不同来源和不同拥有者手牌 |
| [0915 Stare Down](operator-audits/round-1-reading.md#card-0915) | MOVE_BATCH:各敌方控制者基地可能不同，逐个move不保证同一移动批次 |
| [0922 Stealthy Pursuer](operator-audits/round-1-reading.md#card-0922) | MOVE_FOLLOW:卡面with it涉及跟随同一移动批次；独立move不能保证批次和同时控制检查等价，需规则/契约补足 |
| [0933 Suave Negotiator](operator-audits/round-1-reading.md#card-0933) | PLAYER_BATCH:两个玩家同一指令抽牌的批次及顺序契约未定义 |
| [0936 Sun Disc](operator-audits/round-1-reading.md#card-0936) | ENTRY:无法建立本回合下一个单位的入场状态修饰，不能现在重置尚未确定单位 |
| [0941 Svellsongur](operator-audits/round-1-reading.md#card-0941) | AS_ATTACH:复制应在贴附内联发生，attach没有过程挂钩；SC持续表述与EN时点不完全相同 |
| [0945 Symbol of the Solari](operator-audits/round-1-reading.md#card-0945) | REPLACE:缺少替代战斗平局后流程为双方全部召回的接口；COMBAT_DAMAGE_ORDER不适用 |
| [0947 Tactical Retreat](operator-audits/round-1-reading.md#card-0947) | REPLACE:没有本回合仅一次死亡替代事件接口 |
| [0950 Targon’s Peak](operator-audits/round-1-reading.md#card-0950) | DELAY:缺少创建回合末重置触发 |
| [0950 Targon’s Peak](operator-audits/round-1-reading.md#card-0950) | RUNE_READY:ready不接受Rune |
| [0956 Temporal Portal](operator-audits/round-1-reading.md#card-0956) | NEXT_ABILITY:缺下一法术动态绑定/捕获费用并在其定稿前授予Repeat的动作，不能以不存在spell预绑定代替 |
| [0959 The Academy](operator-audits/round-1-reading.md#card-0959) | NEXT_ABILITY:无法独立表达下一个未知法术捕获基础费用并授予Repeat |
| [0962 The Boss](operator-audits/round-1-reading.md#card-0962) | REPLACE:缺可付费的单位死亡替代接口 |
| [0962 The Boss](operator-audits/round-1-reading.md#card-0962) | LEGEND_READY:征服重置传奇无合法ready调用 |
| [0966 The Exile](operator-audits/round-1-reading.md#card-0966) | ENTRY:缺持续修饰未来所有符合地点的单位entry接口 |
| [0970 The List](operator-audits/round-1-reading.md#card-0970) | CHOICE_LINK:declare返回值如何保存至卡实例供未来技能读取，接口未定义持久选择绑定 |
| [0971 The Papertree](operator-audits/round-1-reading.md#card-0971) | PLAYER_BATCH:跨玩家同一召出指令批次与次序未定义 |
| [0978 Threshold of the Gray](operator-audits/round-1-reading.md#card-0978) | PLAYER_BATCH:两位玩家同一指令获得资源的批次未约定 |
| [0983 Tideturner](operator-audits/round-1-reading.md#card-0983) | MOVE_BATCH:move单目的地不能保证双方同时交换 |
| [0988 Tornado Warrior](operator-audits/round-1-reading.md#card-0988) | DELAY:缺少登记本回合结束解除该对象强化的未来动作 |
| [1011 Twisted Fate, Gambler](operator-audits/round-1-reading.md#card-1011) | DAMAGE_BATCH:Fury分支不同目标不同伤害同一批次，damage单一amount的each不能覆盖，split会错误改变额外伤害规则 |
| [1016 Undertitan](operator-audits/round-1-reading.md#card-1016) | AS_VIEW:reveal没有as-revealed内联挂钩，不能改成展示后普通触发 |
| [1020 Unlicensed Armory](operator-audits/round-1-reading.md#card-1020) | REPLACE:缺少一次可付费死亡替代事件接口 |
| [1048 Virtuoso](operator-audits/round-1-reading.md#card-1048) | BATCH:四法术可能不同拥有者，逐个transfer不保证同一多目的批次 |
| [1048 Virtuoso](operator-audits/round-1-reading.md#card-1048) | CHAIN_TIMING:本句打出触发放逐的链上卡身份与链项后续处理需补明确契约，不把Card和ChainItem混用 |
| [1053 Void Hatchling](operator-audits/round-1-reading.md#card-1053) | REPLACE:没有通用展示前事件改写/中间步骤挂钩，不能展示后再洞察 |
| [1069 Whirlwind](operator-audits/round-1-reading.md#card-1069) | ACTOR:transfer没有执行玩家，无法保留各actor进行回手的行动归属 |
| [1072 Wild Claw](operator-audits/round-1-reading.md#card-1072) | REFLEXIVE:then you may do this须创建未来强化待处理链项，不能对play返回ChainItem调用empower |
| [1085 Wuju Master](operator-audits/round-1-reading.md#card-1085) | ENTRY:XP≥11的所有未来单位活跃进场缺全局entry修饰API |
| [1099 Zed, Without a Sound](operator-audits/round-1-reading.md#card-1099) | MOVE_BATCH:move一次仅一个目的地，无法保证me与ShadowClone同时换位 |
| [1103 Zhonya’s Hourglass](operator-audits/round-1-reading.md#card-1103) | REPLACE:没有用装备代死并取消单位死亡的替代接口 |
| [1106 Zilean, Time Mage](operator-audits/round-1-reading.md#card-1106) | REPLACE:缺少带每回合一次额度的token打出替代事件；copy只改已有Permanent而不能替代pendingPlay |

### 关键词／模板宏未独立展开

这些牌的已知单次效果照常写入原笔记；这里单列剩余宏的展开问题。例如Flow原生宏可以被保留，但原子展开时仍缺少离链替代契约。

| 卡牌 | 未展开部分 |
| --- | --- |
| [0081 Bellows Breath](operator-audits/round-1-reading.md#card-0081) | REPEAT:当前仅覆盖一遍效果；无按定稿时各遍选择/模式执行回响的明确调度API，不用即时for循环冒充 |
| [0107 Blood Rush](operator-audits/round-1-reading.md#card-0107) | REPEAT:单次效果可表达，回响各遍选择及执行调度未定义 |
| [0114 Bonds of Strength](operator-audits/round-1-reading.md#card-0114) | REPEAT:无回响定稿各遍选择与单链项重复效果的完整组合接口 |
| [0124 Brittle Steel](operator-audits/round-1-reading.md#card-0124) | FLOW_EXIT:从废牌替代费用可授权，但无通用已定稿链项非自身指令离链时放逐替代，不能用结算后banish冒充被无效化情形 |
| [0140 Called Shot](operator-audits/round-1-reading.md#card-0140) | REPEAT:单次效果可表达，回响重复及各遍定稿选择未有组合接口 |
| [0198 Curtain Call](operator-audits/round-1-reading.md#card-0198) | REPEAT:缺按三个各付一次回响费用创建同一链项多遍效果并限制各遍模式不重复的完整流程 |
| [0202 Danger Zone](operator-audits/round-1-reading.md#card-0202) | REPEAT:单遍效果可表达，多遍回响及预先选择流程未定义 |
| [0214 Death Mark](operator-audits/round-1-reading.md#card-0214) | FLOW_EXIT:缺已定稿流转链项离链放逐替代；分身模板能力不等于本法术有强攻 |
| [0231 Desert’s Call](operator-audits/round-1-reading.md#card-0231) | REPEAT:无同一法术按已支付回响重复效果和分别定稿选择的明确接口 |
| [0251 Double Trouble](operator-audits/round-1-reading.md#card-0251) | REPEAT:只能表达单遍，未定义回响各遍定稿与执行 |
| [0252 Downstage Dramatics](operator-audits/round-1-reading.md#card-0252) | REPEAT:缺回响重复效果的明确组合；一次draw不能证明额外付费路径覆盖 |
| [0256 Dragon Form](operator-audits/round-1-reading.md#card-0256) | FLOW_EXIT:缺流转链项离链放逐替代，不能以法术成功执行后的banish替代全流程 |
| [0265 Dredge Up](operator-audits/round-1-reading.md#card-0265) | FLOW_EXIT:从废牌替代费用可写，离链放逐替代不能完整登记 |
| [0305 Existential Dread](operator-audits/round-1-reading.md#card-0305) | REPEAT:只覆盖单遍条件效果，回响重复与各遍目标选择未提供调度 |
| [0323 Feral Strength](operator-audits/round-1-reading.md#card-0323) | REPEAT:未定义回响重复/每遍定稿选择完整流程 |
| [0360 Frigid Touch](operator-audits/round-1-reading.md#card-0360) | REPEAT:缺回响额外费和多遍预选/执行完整组合 |
| [0408 Hard Bargain](operator-audits/round-1-reading.md#card-0408) | REPEAT:单遍unless可描述，回响各遍目标选择与支付流程尚未定义 |
| [0472 Iterative Design](operator-audits/round-1-reading.md#card-0472) | FLOW_EXIT:缺本次流转定稿链项离链放逐替代 |
| [0521 Lacerate](operator-audits/round-1-reading.md#card-0521) | FLOW_EXIT:尚未独立描述从废牌流转后的链项离链放逐替代 |
| [0541 Lightning Rush](operator-audits/round-1-reading.md#card-0541) | FLOW_EXIT:尚未独立展开流转链项离链放逐替代 |
| [0648 Onslaught](operator-audits/round-1-reading.md#card-0648) | FLOW_EXIT:尚未独立展开流转离链放逐替代 |
| [0662 Pakaa Cub](operator-audits/round-1-reading.md#card-0662) | DELEGATED:只展示普通打出路径，未独立展开盖放费用、保持控制、下一回合反应授权及限定战场目标 |
| [0671 Perfect Execution](operator-audits/round-1-reading.md#card-0671) | FLOW_EXIT:尚未独立描述流转离链放逐替代 |
| [0676 Piercing Light](operator-audits/round-1-reading.md#card-0676) | REPEAT:只表达单遍两个顺序指令，未定义回响多遍定稿选择和执行 |
| [0712 Public Execution](operator-audits/round-1-reading.md#card-0712) | FLOW_EXIT:流转的离链放逐及从废牌堆替代费用未独立展开 |
| [0745 Reflection](operator-audits/round-1-reading.md#card-0745) | DELEGATED:仅有复制提醒，须和具体产生映像的卡一起展开，不能凭任意original调用copy |
| [0781 Rocket Barrage](operator-audits/round-1-reading.md#card-0781) | REPEAT:只展开单次效果，额外付款重复和多组预先定稿选择未独立展开 |
| [0837 Shadow Dash](operator-audits/round-1-reading.md#card-0837) | FLOW_EXIT:流转从废牌堆及离链放逐未独立展开 |
| [0859 Shuriken Flip](operator-audits/round-1-reading.md#card-0859) | FLOW_EXIT:流转完整流程未独立展开 |
| [0907 Square Up](operator-audits/round-1-reading.md#card-0907) | REPEAT:单次效果已写；回响额外弃牌及独立预选目标未展开 |
| [0957 Temptation](operator-audits/round-1-reading.md#card-0957) | REPEAT:单次效果已描述，回响额外费用和重复选择未独立展开 |
| [0980 Thwonk!](operator-audits/round-1-reading.md#card-0980) | REPEAT:回响能量2的重复付款及另组预选目标未独立展开 |
| [1009 Twilight Shroud](operator-audits/round-1-reading.md#card-1009) | FLOW_EXIT:流转的额外打出路径及离链放逐未独立展开 |
| [1010 Twilight Step](operator-audits/round-1-reading.md#card-1010) | FLOW_EXIT:流转流程未独立展开 |
| [1023 Up from the Deep](operator-audits/round-1-reading.md#card-1023) | FLOW_EXIT:流转能量3及离链放逐未独立展开 |
| [1024 Upstage Comedy](operator-audits/round-1-reading.md#card-1024) | REPEAT:回响能量2额外费与另一组选择未独立展开 |

### 问题类别统计

按受影响本体去重计数；类别之间有交集，不可相加当作未覆盖卡数。

| 问题标识 | 本体数 |
| --- | ---: |
| `ACTOR` | 22 |
| `REPEAT` | 19 |
| `REPLACE` | 18 |
| `DELAY` | 16 |
| `REFLEXIVE` | 15 |
| `FLOW_EXIT` | 15 |
| `RUNE_READY` | 12 |
| `BATCH` | 9 |
| `PLAYER_BATCH` | 9 |
| `ENTRY` | 8 |
| `RECIPROCAL` | 7 |
| `LEGEND_READY` | 6 |
| `NEXT_ABILITY` | 6 |
| `MOVE_BATCH` | 6 |
| `MODIFIER_BATCH` | 3 |
| `CHAIN_EXIT` | 3 |
| `DAMAGE_BATCH` | 2 |
| `COST_DESTINATION` | 2 |
| `PLAY_COST` | 2 |
| `OPTIONAL_COST` | 2 |
| `AS_VIEW` | 2 |
| `DELEGATED` | 2 |
| `AS_ATTACH` | 2 |
| `AS_PLAY` | 1 |
| `CREATE_NEUTRAL` | 1 |
| `PREVENT_ONCE` | 1 |
| `CHAIN_REPLAY` | 1 |
| `REVEAL_UNTIL` | 1 |
| `CHOICE_SHORTAGE` | 1 |
| `RULE_NARROW` | 1 |
| `MIGHT_BONUS` | 1 |
| `PHASE` | 1 |
| `TYPE_EVOLUTION` | 1 |
| `ACTION_ID` | 1 |
| `SETUP` | 1 |
| `TRIGGER_RETYPE` | 1 |
| `MOVE_FOLLOW` | 1 |
| `CHOICE_LINK` | 1 |
| `CHAIN_TIMING` | 1 |

## 来源缺文及语言差异

| 卡牌 | 来源问题 |
| --- | --- |
| [0011 Ahri, Inquisitive](operator-audits/round-1-reading.md#card-0011) | LANG:TC普通版为你进攻防守且缺此处，另版与EN/SC不同 |
| [0049 Aspirant’s Climb](operator-audits/round-1-reading.md#card-0049) | DATA:EN异画规则为null，不能据该面认定白板；其他印刷可解释本体 |
| [0049 Aspirant’s Climb](operator-audits/round-1-reading.md#card-0049) | DATA:同一本体有非空规则文本，但这些变体printedRulesText为空：EN OGN-276a |
| [0062 Baccai Witherclaw](operator-audits/round-1-reading.md#card-0062) | DATA:SC分隔标记损坏，EN及中文括号说明可支持解释但不改源文 |
| [0069 Bandle Tree](operator-audits/round-1-reading.md#card-0069) | DATA:EN异画null规则；其他印刷有能力 |
| [0069 Bandle Tree](operator-audits/round-1-reading.md#card-0069) | DATA:同一本体有非空规则文本，但这些变体printedRulesText为空：EN OGN-278a |
| [0092 Blade of the Exile](operator-audits/round-1-reading.md#card-0092) | DATA:SC缺printedEffectText，不能确认该中文面含宿主游走；EN有明确文本 |
| [0100 Blighted Battleaxe](operator-audits/round-1-reading.md#card-0100) | DATA:SC缺printedEffectText，EN的卸除伤害能力不能悄悄算作中文已提供 |
| [0113 Bomb](operator-audits/round-1-reading.md#card-0113) | DATA:仅EN背面有该本体，SC/TC没有卡面文本 |
| [0116 Boneshiver](operator-audits/round-1-reading.md#card-0116) | DATA:SC缺效果区，EN异画也缺效果区，普通EN有征服召符文 |
| [0116 Boneshiver](operator-audits/round-1-reading.md#card-0116) | DATA:同一本体有非空装备效果，但这些变体printedEffectText为空：EN SFD-118a, SC SFD-118 |
| [0117 Boots of Swiftness](operator-audits/round-1-reading.md#card-0117) | DATA:SC未提供printedEffectText中的宿主游走 |
| [0127 Brutalizer](operator-audits/round-1-reading.md#card-0127) | DATA:SC没有printedEffectText中的额外+2 |
| [0137 Caitlyn, Patrolling](operator-audits/round-1-reading.md#card-0137) | LANG:SC目标仅敌军，而EN/TC允许任意单位；并列保留不能统一当同一目标集合 |
| [0166 Cloth Armor](operator-audits/round-1-reading.md#card-0166) | DATA:SC缺printedEffectText中的坚守2 |
| [0194 Cull](operator-audits/round-1-reading.md#card-0194) | DATA:SC缺printedEffectText中的征服产金币 |
| [0200 Dame the Despoiler](operator-audits/round-1-reading.md#card-0200) | LANG:SC要求目标战力大于自己，EN任意此处单位但只提高，目标合法集合不同 |
| [0209 Dauntless Vanguard](operator-audits/round-1-reading.md#card-0209) | LANG:SC写敌方控制，EN为敌方occupied，不能默认两个谓词等同 |
| [0211 Deadbloom Predator](operator-audits/round-1-reading.md#card-0211) | LANG:SC为敌方控制的战场，EN/TC为敌方occupied |
| [0249 Doran’s Ring](operator-audits/round-1-reading.md#card-0249) | DATA:SC及一组EN印刷缺printedEffectText中的弃抽 |
| [0250 Doran’s Shield](operator-audits/round-1-reading.md#card-0250) | DATA:SC缺printedEffectText中的壁垒 |
| [0286 Emperor of the Sands](operator-audits/round-1-reading.md#card-0286) | LANG:两组EN分别写Your Sand Soldiers与Sand Soldiers you play，控制与打出历史范围未完全相同，未用同一选择器抹平 |
| [0289 Empowered](operator-audits/round-1-reading.md#card-0289) | DATA:SC文本仍是英文，不视为已提供中文翻译 |
| [0306 Experimental Hexplate](operator-audits/round-1-reading.md#card-0306) | DATA:SC没有printedEffectText的宿主Mech |
| [0308 Eye of the Herald](operator-audits/round-1-reading.md#card-0308) | DATA:SC及一组EN缺printedEffectText的宿主移动产随从 |
| [0311 Ezreal, Prodigy](operator-audits/round-1-reading.md#card-0311) | LANG:SC普通版限其他卡牌，另一SC版及EN未作此限制，不能把可选费用范围合一 |
| [0316 Fae Porter](operator-audits/round-1-reading.md#card-0316) | LANG:SC要求另一单位，EN没有排除自身，目标选择集合不同 |
| [0339 Flash](operator-audits/round-1-reading.md#card-0339) | LANG:SC仅允许战场上的己军，EN/TC未加该来源限制 |
| [0348 Forgefire Cape](operator-audits/round-1-reading.md#card-0348) | DATA:SC缺printedEffectText中的宿主群伤 |
| [0350 Forgotten Monument](operator-audits/round-1-reading.md#card-0350) | LANG:SC写不能从此处获得分数，EN为不能score here，Scored流程与增分有差别 |
| [0383 Gold](operator-audits/round-1-reading.md#card-0383) | DATA:目录勘误缺sourceUrl和effectiveDate，按给出内容保留不补官方日期 |
| [0406 Hand Hammer](operator-audits/round-1-reading.md#card-0406) | DATA:SC没有printedEffectText中的宿主条件+2 |
| [0416 Heimerdinger, Inventor](operator-audits/round-1-reading.md#card-0416) | LANG:SC明确其他友方对象，EN/TC含自身；要保留规则层防循环及来源差异，不直接字面无限复制 |
| [0425 Hexdrinker](operator-audits/round-1-reading.md#card-0425) | DATA:SC缺printedEffectText的法盾 |
| [0431 Hextech Gauntlets](operator-audits/round-1-reading.md#card-0431) | DATA:SC缺printedEffectText的过量分配条件抽牌 |
| [0444 Hunter’s Machete](operator-audits/round-1-reading.md#card-0444) | DATA:SC没有printedEffectText中的狩猎 |
| [0452 Illaoi, Prophet of the Great Kraken](operator-audits/round-1-reading.md#card-0452) | DATA:EN及目录勘误仍含rb_energy_1图标，SC和关联模板为1战力；保留疑点不改写 |
| [0476 Jagged Cutlass](operator-audits/round-1-reading.md#card-0476) | DATA:SC没有printedEffectText的宿主移动限制 |
| [0512 King’s Edict](operator-audits/round-1-reading.md#card-0512) | LANG:TC文字互相选择他人单位，与EN/SC固定排除施法者控制并非同一个筛选 |
| [0524 Last Breath](operator-audits/round-1-reading.md#card-0524) | LANG:SC省略明确伤害来源主语，EN/TC明确由单位而非法术造成；映射按EN保留单位来源 |
| [0526 Last Rites](operator-audits/round-1-reading.md#card-0526) | DATA:SC缺printedEffectText的废牌打出能力 |
| [0527 Last Stand](operator-audits/round-1-reading.md#card-0527) | LANG:SC瞬息提醒写你的下回合，EN/TC按当时单位控制者开始阶段，控制变化时不同 |
| [0539 Leona, Zealot](operator-audits/round-1-reading.md#card-0539) | LANG:TC异画写差不到3，EN/SC/TC普通版为≤3，边界不同 |
| [0562 Maduli the Gatekeeper](operator-audits/round-1-reading.md#card-0562) | LANG:SC目标写敌方控制战场而EN为敌方occupied，条件谓词不同 |
| [0620 Mystic Reversal](operator-audits/round-1-reading.md#card-0620) | LANG:SC只明确新目标，EN/TC可重做模式等选择；不把全部选择删成targets-only |
| [0627 Nazuman Ntofo](operator-audits/round-1-reading.md#card-0627) | DATA:SC缺printedEffectText的坚守2 |
| [0637 Noxian Emissary](operator-audits/round-1-reading.md#card-0637) | DATA:SC含损坏的嵌套绝念分隔标记，保留原文并参考EN与中文括号说明 |
| [0640 Noxus Saboteur](operator-audits/round-1-reading.md#card-0640) | LANG:EN/TC用revealed，SC明确翻开打出，不能把技术动作Reveal和Play直接等同；需旧术语解释 |
| [0650 Order Rune](operator-audits/round-1-reading.md#card-0650) | DATA:一EN印刷rules只有句点，不把句点当未解释效果；基础符文能力来自明确规则而非零值推测 |
| [0650 Order Rune](operator-audits/round-1-reading.md#card-0650) | DATA:同一本体有非空规则文本，但这些变体printedRulesText为空：EN OGN-214, SC OGN-214, TC OGN-214 |
| [0668 Peak Guardian](operator-audits/round-1-reading.md#card-0668) | LANG:SC第二步含自己且条件写打出到战场，EN/TC排除自己并读当前地点；增益上限例外下可能有实际差异 |
| [0669 Pendulum Blade](operator-audits/round-1-reading.md#card-0669) | DATA:SC未提供printedEffectText的宿主移动加战力 |
| [0706 Production Surge](operator-audits/round-1-reading.md#card-0706) | LANG:SC机器人译名与英文Mech不同，以tokenCardIds绑定 |
| [0709 Promising Future](operator-audits/round-1-reading.md#card-0709) | LANG:英文未勘误文本没有放逐；SC选择与TC放逐不同 |
| [0711 Protector’s Shield](operator-audits/round-1-reading.md#card-0711) | DATA:SC缺失装备EFFECT，依据EN保留Tank |
| [0720 Rabadon’s Deathcrown](operator-audits/round-1-reading.md#card-0720) | DATA:SC无装备EFFECT，EN明确额外伤害3 |
| [0733 Ravenborn Tome](operator-audits/round-1-reading.md#card-0733) | LANG:未勘误EN和SC少本回合限制，TC有 |
| [0743 Recurve Bow](operator-audits/round-1-reading.md#card-0743) | DATA:SC缺少装备EFFECT |
| [0746 Reinforce](operator-audits/round-1-reading.md#card-0746) | LANG:EN和SC原印刷没有放逐步骤，TC及勘误有；采用勘误 |
| [0748 Rek’Sai, Swarm Queen](operator-audits/round-1-reading.md#card-0748) | LANG:未勘误EN/SC缺少放逐且余牌回收顺序不同；采用勘误 |
| [0751 Rell, Magnetic](operator-audits/round-1-reading.md#card-0751) | LANG:原印刷直接附着，勘误增加自反链项 |
| [0759 Rengar, Trophy Hunter](operator-audits/round-1-reading.md#card-0759) | LANG:早期文本只扩展打出地点，勘误明确扩展Ambush |
| [0763 Resonating Strike](operator-audits/round-1-reading.md#card-0763) | LANG:未勘误EN/SC的反应提醒误写迅捷时机，按2026-07-23勘误 |
| [0773 Riposte](operator-audits/round-1-reading.md#card-0773) | DATA:SC的战力图标为损坏的[s]，按EN读取 |
| [0795 Sabotage](operator-audits/round-1-reading.md#card-0795) | LANG:SC回收执行人为对手，其他文本非明确相同 |
| [0797 Sacred Shears](operator-audits/round-1-reading.md#card-0797) | DATA:SC缺少装备EFFECT |
| [0829 Seraphine, Not Alone](operator-audits/round-1-reading.md#card-0829) | DATA:SC T1A-005名称与规则为空，其他印刷有完整文本 |
| [0831 Serrated Dirk](operator-audits/round-1-reading.md#card-0831) | DATA:SC缺少装备EFFECT |
| [0836 Shadow Clone](operator-audits/round-1-reading.md#card-0836) | DATA:ShadowClone本体might为null；其他产生它的卡明确指定0，不能把本体缺值默认视作0 |
| [0845 Shady Spectacles](operator-audits/round-1-reading.md#card-0845) | DATA:SC缺少提醒EFFECT但非独立效果 |
| [0858 Shurelya’s Requiem](operator-audits/round-1-reading.md#card-0858) | DATA:SC缺少装备EFFECT |
| [0872 Skyfall of Areion](operator-audits/round-1-reading.md#card-0872) | DATA:SC缺少装备EFFECT |
| [0885 Sona, Harmonious](operator-audits/round-1-reading.md#card-0885) | LANG:旧EN/SC要求4，勘误及TC为至多4 |
| [0889 Soul Sword](operator-audits/round-1-reading.md#card-0889) | DATA:SC缺少装备EFFECT |
| [0909 Stalking Wolf](operator-audits/round-1-reading.md#card-0909) | LANG:旧印刷只扩展play位置，勘误明确Ambush |
| [0931 Strike Down](operator-audits/round-1-reading.md#card-0931) | LANG:SC未明确友军为伤害来源，采用EN的It deals |
| [0937 Sunken Temple](operator-audits/round-1-reading.md#card-0937) | LANG:EN强调征服者有Mighty单位，SC写此处留存至少一Mighty，需按事件主体而非任意敌军检查 |
| [0950 Targon’s Peak](operator-audits/round-1-reading.md#card-0950) | LANG:旧SC还提前选择符文，勘误为回合末至多2，不能混用 |
| [0954 Teemo, Strategist](operator-audits/round-1-reading.md#card-0954) | LANG:未勘误EN/SC还包含从Hidden打出触发，TC不同印刷亦冲突；按目录勘误仅防守 |
| [0962 The Boss](operator-audits/round-1-reading.md#card-0962) | LANG:部分EN印刷缺征服句，旧文本及TC治愈步骤不一致，按勘误 |
| [0964 The Dreaming Tree](operator-audits/round-1-reading.md#card-0964) | LANG:旧EN/SC以you表述，勘误与TC明确每玩家 |
| [0968 The Grand Plaza](operator-audits/round-1-reading.md#card-0968) | DATA:EN OGN-293a规则空，其他EN/SC/TC有胜利效果 |
| [0973 The Syren](operator-audits/round-1-reading.md#card-0973) | LANG:早期EN为your base，勘误改its base与SC/TC相符 |
| [0975 The Zero Drive](operator-audits/round-1-reading.md#card-0975) | DATA:SC缺少装备EFFECT中的Deathknell放逐关联来源 |
| [0981 Tianna Crownguard](operator-audits/round-1-reading.md#card-0981) | LANG:原印刷score改gain，禁止范围扩大，按勘误 |
| [0983 Tideturner](operator-audits/round-1-reading.md#card-0983) | LANG:早期EN/SC未限定p控制和不同地点，按勘误 |
| [1002 Trinity Force](operator-audits/round-1-reading.md#card-1002) | DATA:SC缺少装备EFFECT |
| [1006 Tryndamere, Barbarian](operator-audits/round-1-reading.md#card-1006) | LANG:SC写得分+1可能误读成替代修饰，EN/TC是独立得1分 |
| [1016 Undertitan](operator-audits/round-1-reading.md#card-1016) | LANG:SC如果被展示的句式未明确as内联，采用EN |
| [1019 Unforgiven](operator-audits/round-1-reading.md#card-1019) | LANG:旧EN是your base，勘误为its base |
| [1020 Unlicensed Armory](operator-audits/round-1-reading.md#card-1020) | LANG:原印刷缺治愈及would，按勘误而非死后召回 |
| [1022 Unyielding Spirit](operator-audits/round-1-reading.md#card-1022) | LANG:TC“本回合不受”未写完整对象，按EN/SC全体法术技能伤害 |
| [1050 Void Burrower](operator-audits/round-1-reading.md#card-1050) | LANG:未勘误EN/SC缺放逐步骤，按2026-01-14勘误 |
| [1052 Void Gate](operator-audits/round-1-reading.md#card-1052) | LANG:旧SC为以此处单位作目标、EN为affecting，勘误不限选择目标 |
| [1054 Void Rush](operator-audits/round-1-reading.md#card-1054) | LANG:原印刷抽未打出牌；勘误改抽未放逐牌，打出失败亦不能抽被放逐者 |
| [1064 Warmog’s Armor](operator-audits/round-1-reading.md#card-1064) | DATA:SC缺少装备EFFECT |
| [1077 Windsinger](operator-audits/round-1-reading.md#card-1077) | DATA:EN Hidden未使用关键词方括号，结构化keywords为空但规则文本仍明确待命 |
| [1080 World Atlas](operator-audits/round-1-reading.md#card-1080) | DATA:一组EN和全部SC缺少装备EFFECT，另一EN组有 |
| [1081 Wraith of Echoes](operator-audits/round-1-reading.md#card-1081) | LANG:TC“你每回合”易误限自身回合，EN/SC为每个turn |
| [1088 XP Tracker](operator-audits/round-1-reading.md#card-1088) | DATA:SC栏仍是英文提醒文字，不能宣称具备实际中文译文 |
| [1092 Yone, Blademaster](operator-audits/round-1-reading.md#card-1092) | LANG:早期open表述改uncontrolled，按勘误检查征服前控制状态 |
| [1098 Zed, From the Shadows](operator-audits/round-1-reading.md#card-1098) | DATA:对应ShadowClone本体战力字段为null，但本牌明确指定0，不按null猜零 |
| [1099 Zed, Without a Sound](operator-audits/round-1-reading.md#card-1099) | DATA:token本体战力null，本卡明确0可用但不改源数据 |
| [1100 Zenith Blade](operator-audits/round-1-reading.md#card-1100) | LANG:TC多“此处的”友方限制，EN/SC无该来源限制 |
| [1103 Zhonya’s Hourglass](operator-audits/round-1-reading.md#card-1103) | LANG:旧EN/SC next-time与勘误If不同，旧文缺heal，按勘误 |

## 关键规则依据

[官方核心规则本地留档：2026-10-09](references/riftbound/riftbound-core-rules-2026-10-09-en.pdf)。卡面勘误的来源链接与生效日期保留在各卡原笔记中。

| 规则 | 本次判定用途 |
| --- | --- |
| 133.5.a.1、161.1.a、175 | 符文、传奇不属于Permanent，不能向只接受Permanent的ready/exhaust传入 |
| 383、387–390 | 区分普通触发入口、自反待处理链项及新建延迟能力 |
| 417、418.8 | 回收到底及次序；“造成X，每个……”为一个数量计算后的伤害实例 |
| 441.1、491.8.e、740.1.a | 顶牌入废的Burn身份；friendly包含盟友而your仅本玩家 |
| 715、829 | 分配与非分配伤害的Bonus处理不同；Flow的离链放逐是延迟替代 |

## 文档调用核对

逐块解析调用并对照参考文档签名，已记录 **2026** 处ops调用，未调用未登记函数、未漏必需参数、未使用未知关键字参数；代码块语法可解析。这只是文档结构核对，不执行游戏逻辑，不证明绑定对象的运行时有效性，也不是测试套件。

逐卡编号1至1106无遗漏或重复；每张恰有一个API复读区。原笔记中的5542个规则／装备效果原文字段逐一与固定目录的全部文本组相等，原文没有被调用摘要替换。

额外核对了入场状态类型、伤害/次数参数、弃牌数量与cards关键字，以及Rune／Legend不属于Permanent导致的朝向接口缺口。操作次序、动作归属、批次和延迟行为仍按上表保留疑点，不将语法通过等同语义通过。

| API | 已记录调用处数 |
| --- | ---: |
| `draw` | 154 |
| `look` | 15 |
| `reveal` | 29 |
| `choose` | 49 |
| `declare` | 5 |
| `predict` | 23 |
| `show_off` | 6 |
| `transfer` | 44 |
| `move` | 64 |
| `recall` | 3 |
| `discard` | 22 |
| `recycle` | 35 |
| `banish` | 32 |
| `burn` | 10 |
| `channel` | 31 |
| `reorder` | 2 |
| `hide` | 0 |
| `play` | 177 |
| `create` | 0 |
| `add_legend` | 1 |
| `replace_battlefield` | 1 |
| `restore_battlefield` | 1 |
| `exhaust` | 2 |
| `ready` | 50 |
| `buff` | 37 |
| `spend_buff` | 1 |
| `stun` | 25 |
| `empower` | 49 |
| `disempower` | 3 |
| `modify_might` | 199 |
| `set_might` | 2 |
| `set_base_might` | 4 |
| `swap_might` | 1 |
| `damage` | 99 |
| `prevent_damage` | 3 |
| `heal` | 1 |
| `kill` | 55 |
| `attach` | 62 |
| `detach` | 4 |
| `change_control` | 7 |
| `copy` | 1 |
| `copy_text` | 1 |
| `copy_abilities` | 1 |
| `grant_ability` | 6 |
| `suppress_ability` | 1 |
| `grant_keyword` | 104 |
| `modify_keyword` | 2 |
| `set_types` | 1 |
| `set_tags` | 2 |
| `add_resources` | 40 |
| `pay` | 316 |
| `modify_cost` | 94 |
| `gain_xp` | 19 |
| `spend_xp` | 1 |
| `gain_points` | 17 |
| `win` | 2 |
| `modify_damage` | 7 |
| `modify_effect_value` | 1 |
| `modify_trigger_count` | 4 |
| `modify_resource_output` | 1 |
| `modify_buff_value` | 1 |
| `grant_permission` | 25 |
| `restrict_action` | 37 |
| `modify_rule` | 16 |
| `counter` | 12 |
| `redo_choices` | 2 |
| `execute_effect` | 2 |
| `skip_procedure` | 1 |
| `extra_turn` | 1 |

结论：当前69个API**不能宣称完整覆盖全目录**。上列未覆盖项、委托展开及来源问题均须处理；已绑定上下文内覆盖也不等于完整对局规则认证。
