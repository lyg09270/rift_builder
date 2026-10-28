# 第二轮：72算子API全库阅读评估

[V2 API](../basic-operators-api-v2.md) · [逐卡笔记](../card-operator-reading.md) · [V2修订及冗余处理](../card-api-changes-v2.md) · [第一轮报告](../card-api-coverage-v1.md)

状态：完整阅读已完成；本轮已逐张重读 **1106/1106**，未读卡不算通过。
API SHA-256：`d29a830f08fc455c8d1ed4eafa91bf32e38151568627d3c5361f1f053cbff015`。
目录 SHA-256：`ad521068ff70def757a00ff18f049583e1e5dffdc3e0152515eb90007b54ca05`。

## 统计口径

本轮从固定目录重新读取每张的全部EN／SC／TC规则、装备效果、属性与勘误，再对照该卡调用逐项核查。不是只复核上一轮失败卡；原文保留，每张有独立本轮判定。原生关键词按V2闭集宏及本卡参数计入，未定义宏或缺失能力体仍算未覆盖。

表达覆盖率＝所有指令均有已登记API／闭集宏表示的本体数÷1106；无独立动作的纯属性／提醒卡可计入，来源译文缺失不自动当缺算子。人工语义复核确认率（本轮文档正确率）＝完整分解且在六项人工核查中无已知差错、无待核规则项的本体数÷1106。待核、错误、未完整覆盖和未阅读均不计通过。

六项核查：①入口、时点和次数；②主体、目标、控制者／拥有者／行动者；③数值、领域和费用；④顺序、批次和事件身份；⑤持续期、关联和信息权限；⑥关键词、勘误、全部效果句段。这是同一作者依原文和规则进行的人工文档审核，不是独立裁判真值、执行引擎对局测试或规则正确性认证；不能把它解释为实战错误概率。

| 指标 | 分子／分母 | 当前值 |
| --- | ---: | ---: |
| 完整阅读覆盖 | 1106/1106 | 100.00% |
| 表达覆盖 | 1100/1106 | 99.46% |
| 人工语义复核确认（文档正确率） | 1094/1106 | 98.92% |
| 已表达但待核 | 6 | — |
| 未完整覆盖 | 6 | — |
| 未阅读 | 0 | — |

## 未完整覆盖卡牌

| 卡牌 | 本轮缺口 |
| --- | --- |
| [0367 Gangplank, Naval](../card-operator-reading/0301-0400.md#card-0367) | EVENT_KIND:V2封闭事件表及EventPatch未定义STUN和MIGHT_CHANGE，不能合法注册另两种替代分支 |
| [0440 Hostile Takeover](../card-operator-reading/0401-0500.md#card-0440) | CONTROL_END:THIS_TURN自动到期未保证在回合末待处理项结算内先移除本次控制修饰再召回，API缺按Modifier身份取消或明确对应结算阶段的契约 |
| [0504 Keeper’s Verdict](../card-operator-reading/0501-0600.md#card-0504) | ACTOR_REORDER:reorder的chooser只标记次序决定者，未定义实际执行放置的actor；transfer的order未定义top/bottom，不能凭签名字符串猜测可用 |
| [0656 Otterpus](../card-operator-reading/0601-0700.md#card-0656) | EVENT_KIND:V2未登记GAIN_POINTS或SCORE_POINT事件及其替代patch；不能把HOLD/CONQUER触发后抽牌冒充增分替代 |
| [0922 Stealthy Pursuer](../card-operator-reading/0901-1000.md#card-0922) | MOVE_FOLLOW:join只接受未提交批次，原生when触发通常在事件后；API未给此卡如何合法取得该跟随前置窗口的完整规则，不能用普通完成后触发强行回填批次 |
| [1025 Valley of Idols](../card-operator-reading/1001-1100.md#card-1025) | ACTOR_BUFF:buff只有units而无actor，API又默认当前能力控制者；当打出玩家不同于战场能力控制者时不能明确保存they buff的行动归属 |

## 已表达但语义待核卡牌

以下不算API表达缺口，但不计入文档正确率。

| 卡牌 | 待确认内容 |
| --- | --- |
| [0201 Dancing Grenade](../card-operator-reading/0201-0300.md#card-0201) | VERIFY:DancingGrenade跨重打的“次数”与Bonus是重打时快照还是后续伤害指令时重算，且旧Bonus是否继承，需要专门裁定；已可表示但不计语义正确 |
| [0286 Emperor of the Sands](../card-operator-reading/0201-0300.md#card-0286) | VERIFY:EN一版YourSandSoldiers、一版SandSoldiersYouPlay，无明确目录勘误；换控制与来源区域边界尚不能证明完全等价 |
| [0338 Flame Chompers](../card-operator-reading/0301-0400.md#card-0338) | VERIFY:payFury1toPlay与触发基础费及后续印刷费用的关系仍缺具体权威裁定，不计语义确认 |
| [0453 Immortal Phoenix](../card-operator-reading/0401-0500.md#card-0453) | VERIFY:pay X to play在此卡是触发基础费用还是替代打出费用仍待规则裁定，尚不能确认是否会重复收费 |
| [0541 Lightning Rush](../card-operator-reading/0501-0600.md#card-0541) | VERIFY:抽指定牌被替代而该牌仍处原顶部时，rest可能不构成连续顶部，burn(cards)的合法集合及未移动牌处理尚需规则确认 |
| [0836 Shadow Clone](../card-operator-reading/0801-0900.md#card-0836) | VERIFY:完整功能依赖基础战力，独立衍生物模板缺战力，本轮只确认卡文效果调用不捏造零值 |

## 来源差异及缺文

以下与算子缺口分开统计；读取采用明确勘误优先，不用译文缺文猜测零值。

| 卡牌 | 来源问题 |
| --- | --- |
| [0011 Ahri, Inquisitive](../card-operator-reading/0001-0100.md#card-0011) | LANG:TC普通版为你进攻防守且缺此处，另版与EN/SC不同 |
| [0049 Aspirant’s Climb](../card-operator-reading/0001-0100.md#card-0049) | DATA:EN异画规则为null，不能据该面认定白板；其他印刷可解释本体 |
| [0049 Aspirant’s Climb](../card-operator-reading/0001-0100.md#card-0049) | DATA:同一本体有非空规则文本，但这些变体printedRulesText为空：EN OGN-276a |
| [0062 Baccai Witherclaw](../card-operator-reading/0001-0100.md#card-0062) | DATA:SC分隔标记损坏，EN及中文括号说明可支持解释但不改源文 |
| [0069 Bandle Tree](../card-operator-reading/0001-0100.md#card-0069) | DATA:EN异画null规则；其他印刷有能力 |
| [0069 Bandle Tree](../card-operator-reading/0001-0100.md#card-0069) | DATA:同一本体有非空规则文本，但这些变体printedRulesText为空：EN OGN-278a |
| [0092 Blade of the Exile](../card-operator-reading/0001-0100.md#card-0092) | DATA:SC缺printedEffectText，不能确认该中文面含宿主游走；EN有明确文本 |
| [0100 Blighted Battleaxe](../card-operator-reading/0001-0100.md#card-0100) | DATA:SC缺printedEffectText，EN的卸除伤害能力不能悄悄算作中文已提供 |
| [0113 Bomb](../card-operator-reading/0101-0200.md#card-0113) | DATA:仅EN背面有该本体，SC/TC没有卡面文本 |
| [0116 Boneshiver](../card-operator-reading/0101-0200.md#card-0116) | DATA:SC缺效果区，EN异画也缺效果区，普通EN有征服召符文 |
| [0116 Boneshiver](../card-operator-reading/0101-0200.md#card-0116) | DATA:同一本体有非空装备效果，但这些变体printedEffectText为空：EN SFD-118a, SC SFD-118 |
| [0117 Boots of Swiftness](../card-operator-reading/0101-0200.md#card-0117) | DATA:SC未提供printedEffectText中的宿主游走 |
| [0127 Brutalizer](../card-operator-reading/0101-0200.md#card-0127) | DATA:SC没有printedEffectText中的额外+2 |
| [0137 Caitlyn, Patrolling](../card-operator-reading/0101-0200.md#card-0137) | LANG:SC目标仅敌军，而EN/TC允许任意单位；并列保留不能统一当同一目标集合 |
| [0166 Cloth Armor](../card-operator-reading/0101-0200.md#card-0166) | DATA:SC缺printedEffectText中的坚守2 |
| [0194 Cull](../card-operator-reading/0101-0200.md#card-0194) | DATA:SC缺printedEffectText中的征服产金币 |
| [0200 Dame the Despoiler](../card-operator-reading/0101-0200.md#card-0200) | LANG:SC要求目标战力大于自己，EN任意此处单位但只提高，目标合法集合不同 |
| [0209 Dauntless Vanguard](../card-operator-reading/0201-0300.md#card-0209) | LANG:SC写敌方控制，EN为敌方occupied，不能默认两个谓词等同 |
| [0211 Deadbloom Predator](../card-operator-reading/0201-0300.md#card-0211) | LANG:SC为敌方控制的战场，EN/TC为敌方occupied |
| [0249 Doran’s Ring](../card-operator-reading/0201-0300.md#card-0249) | DATA:SC及一组EN印刷缺printedEffectText中的弃抽 |
| [0250 Doran’s Shield](../card-operator-reading/0201-0300.md#card-0250) | DATA:SC缺printedEffectText中的壁垒 |
| [0286 Emperor of the Sands](../card-operator-reading/0201-0300.md#card-0286) | LANG:两组EN分别写Your Sand Soldiers与Sand Soldiers you play，控制与打出历史范围未完全相同，未用同一选择器抹平 |
| [0289 Empowered](../card-operator-reading/0201-0300.md#card-0289) | DATA:SC文本仍是英文，不视为已提供中文翻译 |
| [0306 Experimental Hexplate](../card-operator-reading/0301-0400.md#card-0306) | DATA:SC没有printedEffectText的宿主Mech |
| [0308 Eye of the Herald](../card-operator-reading/0301-0400.md#card-0308) | DATA:SC及一组EN缺printedEffectText的宿主移动产随从 |
| [0311 Ezreal, Prodigy](../card-operator-reading/0301-0400.md#card-0311) | LANG:SC普通版限其他卡牌，另一SC版及EN未作此限制，不能把可选费用范围合一 |
| [0316 Fae Porter](../card-operator-reading/0301-0400.md#card-0316) | LANG:SC要求另一单位，EN没有排除自身，目标选择集合不同 |
| [0339 Flash](../card-operator-reading/0301-0400.md#card-0339) | LANG:SC仅允许战场上的己军，EN/TC未加该来源限制 |
| [0348 Forgefire Cape](../card-operator-reading/0301-0400.md#card-0348) | DATA:SC缺printedEffectText中的宿主群伤 |
| [0350 Forgotten Monument](../card-operator-reading/0301-0400.md#card-0350) | LANG:SC写不能从此处获得分数，EN为不能score here，Scored流程与增分有差别 |
| [0383 Gold](../card-operator-reading/0301-0400.md#card-0383) | DATA:目录勘误缺sourceUrl和effectiveDate，按给出内容保留不补官方日期 |
| [0406 Hand Hammer](../card-operator-reading/0401-0500.md#card-0406) | DATA:SC没有printedEffectText中的宿主条件+2 |
| [0416 Heimerdinger, Inventor](../card-operator-reading/0401-0500.md#card-0416) | LANG:SC明确其他友方对象，EN/TC含自身；要保留规则层防循环及来源差异，不直接字面无限复制 |
| [0425 Hexdrinker](../card-operator-reading/0401-0500.md#card-0425) | DATA:SC缺printedEffectText的法盾 |
| [0431 Hextech Gauntlets](../card-operator-reading/0401-0500.md#card-0431) | DATA:SC缺printedEffectText的过量分配条件抽牌 |
| [0444 Hunter’s Machete](../card-operator-reading/0401-0500.md#card-0444) | DATA:SC没有printedEffectText中的狩猎 |
| [0452 Illaoi, Prophet of the Great Kraken](../card-operator-reading/0401-0500.md#card-0452) | DATA:EN及目录勘误仍含rb_energy_1图标，SC和关联模板为1战力；保留疑点不改写 |
| [0476 Jagged Cutlass](../card-operator-reading/0401-0500.md#card-0476) | DATA:SC没有printedEffectText的宿主移动限制 |
| [0512 King’s Edict](../card-operator-reading/0501-0600.md#card-0512) | LANG:TC文字互相选择他人单位，与EN/SC固定排除施法者控制并非同一个筛选 |
| [0524 Last Breath](../card-operator-reading/0501-0600.md#card-0524) | LANG:SC省略明确伤害来源主语，EN/TC明确由单位而非法术造成；映射按EN保留单位来源 |
| [0526 Last Rites](../card-operator-reading/0501-0600.md#card-0526) | DATA:SC缺printedEffectText的废牌打出能力 |
| [0527 Last Stand](../card-operator-reading/0501-0600.md#card-0527) | LANG:SC瞬息提醒写你的下回合，EN/TC按当时单位控制者开始阶段，控制变化时不同 |
| [0539 Leona, Zealot](../card-operator-reading/0501-0600.md#card-0539) | LANG:TC异画写差不到3，EN/SC/TC普通版为≤3，边界不同 |
| [0562 Maduli the Gatekeeper](../card-operator-reading/0501-0600.md#card-0562) | LANG:SC目标写敌方控制战场而EN为敌方occupied，条件谓词不同 |
| [0620 Mystic Reversal](../card-operator-reading/0601-0700.md#card-0620) | LANG:SC只明确新目标，EN/TC可重做模式等选择；不把全部选择删成targets-only |
| [0627 Nazuman Ntofo](../card-operator-reading/0601-0700.md#card-0627) | DATA:SC缺printedEffectText的坚守2 |
| [0637 Noxian Emissary](../card-operator-reading/0601-0700.md#card-0637) | DATA:SC含损坏的嵌套绝念分隔标记，保留原文并参考EN与中文括号说明 |
| [0640 Noxus Saboteur](../card-operator-reading/0601-0700.md#card-0640) | LANG:EN/TC用revealed，SC明确翻开打出，不能把技术动作Reveal和Play直接等同；需旧术语解释 |
| [0650 Order Rune](../card-operator-reading/0601-0700.md#card-0650) | DATA:一EN印刷rules只有句点，不把句点当未解释效果；基础符文能力来自明确规则而非零值推测 |
| [0650 Order Rune](../card-operator-reading/0601-0700.md#card-0650) | DATA:同一本体有非空规则文本，但这些变体printedRulesText为空：EN OGN-214, SC OGN-214, TC OGN-214 |
| [0668 Peak Guardian](../card-operator-reading/0601-0700.md#card-0668) | LANG:SC第二步含自己且条件写打出到战场，EN/TC排除自己并读当前地点；增益上限例外下可能有实际差异 |
| [0669 Pendulum Blade](../card-operator-reading/0601-0700.md#card-0669) | DATA:SC未提供printedEffectText的宿主移动加战力 |
| [0706 Production Surge](../card-operator-reading/0701-0800.md#card-0706) | LANG:SC机器人译名与英文Mech不同，以tokenCardIds绑定 |
| [0709 Promising Future](../card-operator-reading/0701-0800.md#card-0709) | LANG:英文未勘误文本没有放逐；SC选择与TC放逐不同 |
| [0711 Protector’s Shield](../card-operator-reading/0701-0800.md#card-0711) | DATA:SC缺失装备EFFECT，依据EN保留Tank |
| [0720 Rabadon’s Deathcrown](../card-operator-reading/0701-0800.md#card-0720) | DATA:SC无装备EFFECT，EN明确额外伤害3 |
| [0733 Ravenborn Tome](../card-operator-reading/0701-0800.md#card-0733) | LANG:未勘误EN和SC少本回合限制，TC有 |
| [0743 Recurve Bow](../card-operator-reading/0701-0800.md#card-0743) | DATA:SC缺少装备EFFECT |
| [0746 Reinforce](../card-operator-reading/0701-0800.md#card-0746) | LANG:EN和SC原印刷没有放逐步骤，TC及勘误有；采用勘误 |
| [0748 Rek’Sai, Swarm Queen](../card-operator-reading/0701-0800.md#card-0748) | LANG:未勘误EN/SC缺少放逐且余牌回收顺序不同；采用勘误 |
| [0751 Rell, Magnetic](../card-operator-reading/0701-0800.md#card-0751) | LANG:原印刷直接附着，勘误增加自反链项 |
| [0759 Rengar, Trophy Hunter](../card-operator-reading/0701-0800.md#card-0759) | LANG:早期文本只扩展打出地点，勘误明确扩展Ambush |
| [0763 Resonating Strike](../card-operator-reading/0701-0800.md#card-0763) | LANG:未勘误EN/SC的反应提醒误写迅捷时机，按2026-07-23勘误 |
| [0773 Riposte](../card-operator-reading/0701-0800.md#card-0773) | DATA:SC的战力图标为损坏的[s]，按EN读取 |
| [0795 Sabotage](../card-operator-reading/0701-0800.md#card-0795) | LANG:SC回收执行人为对手，其他文本非明确相同 |
| [0795 Sabotage](../card-operator-reading/0701-0800.md#card-0795) | LANG:SC指定让对手回收，EN未改主体，采用英文由本能力控制者回收；展示明确由对手执行 |
| [0797 Sacred Shears](../card-operator-reading/0701-0800.md#card-0797) | DATA:SC缺少装备EFFECT |
| [0829 Seraphine, Not Alone](../card-operator-reading/0801-0900.md#card-0829) | DATA:SC T1A-005名称与规则为空，其他印刷有完整文本 |
| [0829 Seraphine, Not Alone](../card-operator-reading/0801-0900.md#card-0829) | DATA:SC T1A-005名称与规则为空，其他三组双语卡文一致，未据此补造另一能力 |
| [0831 Serrated Dirk](../card-operator-reading/0801-0900.md#card-0831) | DATA:SC缺少装备EFFECT |
| [0836 Shadow Clone](../card-operator-reading/0801-0900.md#card-0836) | DATA:ShadowClone本体might为null；其他产生它的卡明确指定0，不能把本体缺值默认视作0 |
| [0836 Shadow Clone](../card-operator-reading/0801-0900.md#card-0836) | DATA:Shadow Clone本体might为空，产生卡若明示零仅可用于该产生模板 |
| [0845 Shady Spectacles](../card-operator-reading/0801-0900.md#card-0845) | DATA:SC缺少提醒EFFECT但非独立效果 |
| [0858 Shurelya’s Requiem](../card-operator-reading/0801-0900.md#card-0858) | DATA:SC缺少装备EFFECT |
| [0872 Skyfall of Areion](../card-operator-reading/0801-0900.md#card-0872) | DATA:SC缺少装备EFFECT |
| [0885 Sona, Harmonious](../card-operator-reading/0801-0900.md#card-0885) | LANG:旧EN/SC要求4，勘误及TC为至多4 |
| [0889 Soul Sword](../card-operator-reading/0801-0900.md#card-0889) | DATA:SC缺少装备EFFECT |
| [0909 Stalking Wolf](../card-operator-reading/0901-1000.md#card-0909) | LANG:旧印刷只扩展play位置，勘误明确Ambush |
| [0931 Strike Down](../card-operator-reading/0901-1000.md#card-0931) | LANG:SC未明确友军为伤害来源，采用EN的It deals |
| [0937 Sunken Temple](../card-operator-reading/0901-1000.md#card-0937) | LANG:EN强调征服者有Mighty单位，SC写此处留存至少一Mighty，需按事件主体而非任意敌军检查 |
| [0950 Targon’s Peak](../card-operator-reading/0901-1000.md#card-0950) | LANG:旧SC还提前选择符文，勘误为回合末至多2，不能混用 |
| [0954 Teemo, Strategist](../card-operator-reading/0901-1000.md#card-0954) | LANG:未勘误EN/SC还包含从Hidden打出触发，TC不同印刷亦冲突；按目录勘误仅防守 |
| [0962 The Boss](../card-operator-reading/0901-1000.md#card-0962) | LANG:部分EN印刷缺征服句，旧文本及TC治愈步骤不一致，按勘误 |
| [0964 The Dreaming Tree](../card-operator-reading/0901-1000.md#card-0964) | LANG:旧EN/SC以you表述，勘误与TC明确每玩家 |
| [0968 The Grand Plaza](../card-operator-reading/0901-1000.md#card-0968) | DATA:EN OGN-293a规则空，其他EN/SC/TC有胜利效果 |
| [0968 The Grand Plaza](../card-operator-reading/0901-1000.md#card-0968) | DATA:EN OGN-293a为空白规则，EN OGN-293及中繁文均有相同胜利条件，未将空文作白板 |
| [0973 The Syren](../card-operator-reading/0901-1000.md#card-0973) | LANG:早期EN为your base，勘误改its base与SC/TC相符 |
| [0975 The Zero Drive](../card-operator-reading/0901-1000.md#card-0975) | DATA:SC缺少装备EFFECT中的Deathknell放逐关联来源 |
| [0981 Tianna Crownguard](../card-operator-reading/0901-1000.md#card-0981) | LANG:原印刷score改gain，禁止范围扩大，按勘误 |
| [0983 Tideturner](../card-operator-reading/0901-1000.md#card-0983) | LANG:早期EN/SC未限定p控制和不同地点，按勘误 |
| [1002 Trinity Force](../card-operator-reading/1001-1100.md#card-1002) | DATA:SC缺少装备EFFECT |
| [1006 Tryndamere, Barbarian](../card-operator-reading/1001-1100.md#card-1006) | LANG:SC写得分+1可能误读成替代修饰，EN/TC是独立得1分 |
| [1016 Undertitan](../card-operator-reading/1001-1100.md#card-1016) | LANG:SC如果被展示的句式未明确as内联，采用EN |
| [1019 Unforgiven](../card-operator-reading/1001-1100.md#card-1019) | LANG:旧EN是your base，勘误为its base |
| [1020 Unlicensed Armory](../card-operator-reading/1001-1100.md#card-1020) | LANG:原印刷缺治愈及would，按勘误而非死后召回 |
| [1022 Unyielding Spirit](../card-operator-reading/1001-1100.md#card-1022) | LANG:TC“本回合不受”未写完整对象，按EN/SC全体法术技能伤害 |
| [1050 Void Burrower](../card-operator-reading/1001-1100.md#card-1050) | LANG:未勘误EN/SC缺放逐步骤，按2026-01-14勘误 |
| [1052 Void Gate](../card-operator-reading/1001-1100.md#card-1052) | LANG:旧SC为以此处单位作目标、EN为affecting，勘误不限选择目标 |
| [1054 Void Rush](../card-operator-reading/1001-1100.md#card-1054) | LANG:原印刷抽未打出牌；勘误改抽未放逐牌，打出失败亦不能抽被放逐者 |
| [1064 Warmog’s Armor](../card-operator-reading/1001-1100.md#card-1064) | DATA:SC缺少装备EFFECT |
| [1077 Windsinger](../card-operator-reading/1001-1100.md#card-1077) | DATA:EN Hidden未使用关键词方括号，结构化keywords为空但规则文本仍明确待命 |
| [1080 World Atlas](../card-operator-reading/1001-1100.md#card-1080) | DATA:一组EN和全部SC缺少装备EFFECT，另一EN组有 |
| [1080 World Atlas](../card-operator-reading/1001-1100.md#card-1080) | DATA:一个EN SFD-086印刷及SC装备效果为空，另一EN印刷明确两金币宿主据守效果 |
| [1081 Wraith of Echoes](../card-operator-reading/1001-1100.md#card-1081) | LANG:TC“你每回合”易误限自身回合，EN/SC为每个turn |
| [1088 XP Tracker](../card-operator-reading/1001-1100.md#card-1088) | DATA:SC栏仍是英文提醒文字，不能宣称具备实际中文译文 |
| [1092 Yone, Blademaster](../card-operator-reading/1001-1100.md#card-1092) | LANG:早期open表述改uncontrolled，按勘误检查征服前控制状态 |
| [1098 Zed, From the Shadows](../card-operator-reading/1001-1100.md#card-1098) | DATA:对应ShadowClone本体战力字段为null，但本牌明确指定0，不按null猜零 |
| [1099 Zed, Without a Sound](../card-operator-reading/1001-1100.md#card-1099) | DATA:token本体战力null，本卡明确0可用但不改源数据 |
| [1100 Zenith Blade](../card-operator-reading/1001-1100.md#card-1100) | LANG:TC多“此处的”友方限制，EN/SC无该来源限制 |
| [1103 Zhonya’s Hourglass](../card-operator-reading/1101-1106.md#card-1103) | LANG:旧EN/SC next-time与勘误If不同，旧文缺heal，按勘误 |

## 调用与阅读留档核对

- 正式函数72个；本轮2338处ops调用均可解析并匹配必需参数及关键字。该项只检验结构，不能替代上述语义复核。
- 全目录1106个原始编号无遗漏重复，5542个原文字段逐一与固定目录相等；本轮已读卡恰有一次第二轮记录。
- 已重读文本变体2771组；每张保存本轮文本组指纹，禁止把未读张数补成通过。
- 源快照含1106个本体、9039个印刷、2771组EN／SC／TC规则和装备效果文本、73个目录勘误；递归包含背面。未逐图视觉核验全部卡图，不把该项描述为已完成。
- 对照[2026-10-09官方核心规则留档](../references/riftbound/riftbound-core-rules-2026-10-09-en.pdf)。文档API无对应执行库；没有运行游戏模拟或已有项目测试套件。

| API | 本轮调用处数 |
| --- | ---: |
| `draw` | 155 |
| `look` | 16 |
| `reveal` | 29 |
| `choose` | 51 |
| `declare` | 6 |
| `predict` | 23 |
| `show_off` | 6 |
| `transfer` | 43 |
| `move` | 67 |
| `recall` | 14 |
| `discard` | 23 |
| `recycle` | 38 |
| `banish` | 45 |
| `burn` | 11 |
| `channel` | 32 |
| `reorder` | 2 |
| `hide` | 1 |
| `play` | 151 |
| `create` | 2 |
| `replace_battlefield` | 2 |
| `exhaust` | 12 |
| `ready` | 68 |
| `buff` | 41 |
| `spend_buff` | 1 |
| `stun` | 26 |
| `empower` | 51 |
| `disempower` | 5 |
| `modify_might` | 208 |
| `set_base_might` | 5 |
| `damage` | 109 |
| `prevent_damage` | 4 |
| `heal` | 10 |
| `kill` | 60 |
| `attach` | 63 |
| `detach` | 4 |
| `change_control` | 7 |
| `copy` | 4 |
| `copy_text` | 1 |
| `copy_abilities` | 1 |
| `grant_ability` | 7 |
| `suppress_ability` | 1 |
| `grant_keyword` | 109 |
| `modify_keyword` | 2 |
| `set_types` | 1 |
| `set_tags` | 2 |
| `add_resources` | 41 |
| `pay` | 319 |
| `modify_cost` | 105 |
| `change_xp` | 31 |
| `gain_points` | 17 |
| `win` | 2 |
| `modify_damage` | 8 |
| `modify_effect_value` | 1 |
| `modify_trigger_count` | 4 |
| `modify_resource_output` | 1 |
| `modify_buff_value` | 1 |
| `grant_permission` | 38 |
| `restrict_action` | 38 |
| `modify_rule` | 17 |
| `counter` | 12 |
| `redo_choices` | 2 |
| `execute_effect` | 22 |
| `skip_procedure` | 1 |
| `extra_turn` | 1 |
| `batch` | 31 |
| `on_event` | 30 |
| `replace_event` | 36 |
| `queue_effect` | 13 |
| `modify_entry` | 41 |
| `modify_equipment_bonus` | 1 |
| `modify_trigger_events` | 2 |
| `remember` | 4 |

结论以以上全量分母统计及逐卡未决项为准。

[最终结构与原文留存核对](round-2-validation.md)记录调用签名、变量绑定、文本指纹、文档链接及本轮API版本指纹。
