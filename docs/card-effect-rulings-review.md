# 12张未覆盖／待核卡：真实效果与API专项修订

核验日期：2026-10-28。先核对本地目录的全部EN／SC／TC文本与勘误，再逐张查看这12张的普通英文卡图，检索官方规则、勘误及FAQ，最后决定接口变更。[本次专项采用V2.1，73个函数](basic-operators-api-v2.1.md)。此文保留专项历史；后续1106张完整复读与当前结论见[第三轮报告](card-api-coverage.md)。

## 依据与证据等级

- **A：官方直接说明**，包括规则明确例子、官方勘误、FAQ及卡牌文字。
- **B：按官方通则分解**，列出推导依据；不是声称找到该卡的专门FAQ。
- **待核**：已确认普通作用，但某个影响精确调用的边界尚无充分依据，不计语义通过。

规则以[2026-10-09核心规则](references/riftbound/riftbound-core-rules-2026-10-09-en.pdf)为基础，另核查[官方规则入口](https://playriftbound.com/en-us/rules-hub/)、[2026-10-26 Radiance FAQ](https://playriftbound.com/en-us/news/organizedplay/radiance-rules-faq-and-clarifications/)。新FAQ明确优先于与之冲突的旧核心规则；本次没有据此冒充完成全库版本迁移。

补充来源：[Unleashed FAQ](https://playriftbound.com/en-us/news/rules-and-releases/unleashed-rules-faq-and-clarifications/)、[Vendetta FAQ](https://playriftbound.com/en-us/news/rules-and-releases/vendetta-rules-faq-and-clarifications/)、[Vendetta勘误](https://playriftbound.com/en-us/news/announcements/vendetta-errata-updates/)、[Spiritforged FAQ](https://playriftbound.com/en-us/news/rules-and-releases/riftbound-spiritforged-faq/)。检索到的自动生成规则问答不作为裁定依据；社区裁定线索不能替代官方结论。

## 本次结果

| 编号 | 卡牌 | 真实作用及核验结论 | 对API的决定 |
| --- | --- | --- | --- |
| 0201 | 曼舞手雷 | 伤害后由受伤单位控制者选择付任意Power1重打同一牌；跨重打计数、Bonus继承及适用时点仍待核 | 现有play／modify_damage能容纳相关行为，暂不为未知裁定新增接口 |
| 0286 | 沙漠皇帝 | 沙兵百炼；本回合打过Equipment后，可付Energy1并横置传奇，打2战力沙兵到自己基地；两个英文版本的授权范围仍待核 | 不增加算子，不把两种印刷文字强行归为完全等价 |
| 0338 | 嚼火者手雷 | 弃置后出现可选触发，Fury1属于首部触发费用；后续打出的印刷费用如何被该句处理尚缺足够官方依据 | 明确pay的费用角色，不凭推测把后续play设免费或再收印刷费 |
| 0367 | 普朗克，海上霸主 | 强化后，仅替代选择自己的法术／技能产生的实际眩晕、给予负战力或回手；结果为本回合+3 | 补STUN、MIGHT_CHANGE事件及替代契约；确认 |
| 0440 | 恶意收购 | 夺控并活跃；指定回合末能力结算时先结束关联控制修饰，再召回。结束阶段中打出不会补触发该回合末能力 | 新增end_modifier；补精确回合末契约；确认 |
| 0453 | 不朽凤凰 | 自带强攻2；法术击杀满足归属条件且它已在废牌时出现可选触发。Energy1/Fury1是首部触发费用；后续印刷费处理仍待核 | 明确费用角色；不能将该费用直接标为替代单位打出费用；仍待核 |
| 0504 | 持卫的裁决 | 选择战场敌军，由其拥有者选择并执行放到自己主牌堆顶或底 | transfer增加position；一次区域放置；确认 |
| 0541 | 奥义！雷铠 | 私密看顶3，可选其中一张并抽取，指定余牌入废；Flow为Energy2/任意Power1。抽取被替代时rest集合与燃烧授权边界仍待核 | 保留指定对象，不改成烧当前顶部若干张；暂不扩展burn契约冒充已裁定 |
| 0656 | 章獭 | 每名玩家自己的首二回合，将其征服／据守将获得的1分替代为抽1；不会撤销征服／据守过程 | 补GAIN_POINTS事件及替代契约；确认 |
| 0836 | 影分身 | 零战力；进攻触发可在结算时放逐自己废牌堆单位，实际放逐后本回合获强攻4。放逐不是发动费用 | 修正pay为banish→实际结果判断→grant_keyword；无新算子；确认 |
| 0922 | 隐秘追踪者 | 友军从自身位置移动引发可选触发，再执行跟随移动；不是修改已完成的原批次 | 取消强制join，以触发事件目的地快照调用普通move；通则推导确认 |
| 1025 | 偶像谷 | 打出单位的玩家作选择并控制本触发，付Energy1后给该单位增益 | 修正Ability.controller，保留pay→buff；无新算子；确认 |

本次12张中，**7张的本次分解确认，5张仍有影响正确性的待核项**。这7张包括按官方通则推导的隐秘追踪者，不是7份独立的官方逐卡FAQ。所有12张均已查找资料、重读文字和查看一张普通英文卡图；5张待核不因检索无结果而算通过。

## 0201 曼舞手雷：待核

[逐卡文字与调用](card-operator-reading/0201-0300.md#card-0201) · [核验卡图](../tmp/ruling-card-faces/0201.webp)

卡面确实授权受伤单位的控制者付任意Power1再次打出这张牌，需要新的选择和定稿记录；不是复制一张新法术。规则356.1.a可确定“for [Cost]”替代基础费用。不能把首次打出的Energy2/Fury1再完整收取一次。

未解决的是：这张正在链上执行的实体，重打后如何精确保留本回合伤害次数，以及后句授予的Bonus在新项哪一时点适用。规则124、359.3.e.15、712–715提供一般约束，尚不足以在本次资料中给出无歧义的跨重打序列。因此不写死2→3→4或2→3→5。旧modify_damage草稿保留为待核候选，不能充当已确认实现。

## 0286 沙漠皇帝：待核授权范围

[逐卡文字与调用](card-operator-reading/0201-0300.md#card-0286) · [核验卡图](../tmp/ruling-card-faces/0286.webp)

普通英文卡图写的是“你的沙兵拥有百炼”；目录另一个金属奖品印刷写的是“你打出的沙兵拥有百炼”。目录无针对两者的勘误。规则821确认百炼为打出触发，支付实际装配费用减任意Power1，而非免费贴附；其在场上没有主动功能，但是否拥有关键词仍可被读取。

两个版本在通常的己方打出沙兵场景下可作相同处理；不能由此证明换控制、区域范围及特征引用始终等价。保留版本来源，不把数据库文字差异当作新增算子的理由。

## 0338 嚼火者手雷、0453 不朽凤凰：已查清费用阶段，未强行消除收费疑点

[手雷逐卡记录](card-operator-reading/0301-0400.md#card-0338) · [凤凰逐卡记录](card-operator-reading/0401-0500.md#card-0453) · [手雷卡图](../tmp/ruling-card-faces/0338.webp) · [凤凰卡图](../tmp/ruling-card-faces/0453.webp)

规则204.1.c、383.3.b、404.1.b.1说明首部“支付X以……”是触发能力的基础费用，定稿时付，不是先让能力免费上链、等结算再决定支付。凤凰的Energy1/Fury1、手雷的Fury1都应记录在相应触发能力上。限制“只能用于打出单位”的资源不能未经裁定自动用于能力费用。

本次找到[裁判问答转录及原作者链接](https://www.joutes.app/de/games/riftbound/cards/OGN037)，其中明确区分这两张与Meticulous Restorationist；这是社区裁定线索，不提升为Riot官方裁定。最新[官方Radiance FAQ](https://playriftbound.com/en-us/news/organizedplay/radiance-rules-faq-and-clarifications/)仅直接回答Restorationist的“play for”替代基础费，不能套到这两张不同模板上。

仍需权威澄清的是：触发费用与能力随后指令打出该单位之间，印刷基础费被什么规则明确替代／免除。普通对局中常见的“仅付触发所写费用”说法与其准确费用角色应分开。本次不写入“费用相同所以都是替代费”，也不宣布需要追加印刷费。API已能区分pay和play，暂不为此增加猜测性政策。

凤凰另依规则383.2.c.1可在自身被法术杀死后触发；击杀来源归属按429.5及[Vendetta FAQ](https://playriftbound.com/en-us/news/rules-and-releases/vendetta-rules-faq-and-clarifications/)处理。实际死亡被替代时不能按已击杀计算；来源于法术的能力可按当前归属规则同时归给原法术。

## 0367 普朗克：按专门FAQ补事件

[逐卡文字与调用](card-operator-reading/0301-0400.md#card-0367) · [核验卡图](../tmp/ruling-card-faces/0367.webp)

[Vendetta勘误](https://playriftbound.com/en-us/news/announcements/vendetta-errata-updates/)确认+3仅本回合。[Vendetta FAQ](https://playriftbound.com/en-us/news/rules-and-releases/vendetta-rules-faq-and-clarifications/)明确三个边界：

- 交换战力先算双方差值；6战力普朗克与2战力单位交换时，自己的-4改为+3，另一名仍得到+4，最终分别9与6。
- 不选择普朗克的眩晕不会被其能力替代。已经眩晕时再次眩晕没有实际动作可替代，因此不白得+3。
- 减战力经局部下限计算后为零，也没有负战力事件可替代。

因此补STUN与MIGHT_CHANGE的before阶段，并在set／swap快照之后、提交之前应用替代。MIGHT_CHANGE不是监控所有最终战力下降，装备离开或强化失效不能无条件变成“给予负战力”。已有modify_might足够执行+3，不能另造一个“普朗克专用”算子。

## 0440 恶意收购：先结束关联控制，再召回

[逐卡文字与调用](card-operator-reading/0401-0500.md#card-0440) · [核验卡图](../tmp/ruling-card-faces/0440.webp)

规则359.3.e.16直接举本卡为例：结束阶段中打出不触发本回合已过时点的延迟能力，也不顺延下回合。故夺控不是一律THIS_TURN自动到期。正常流程是先夺控、活跃，再生成指定当前回合末的延迟能力；其结算体结束本次关联控制修饰，再召回该实例。

新增end_modifier用于精确结束取得的Modifier。不能用change_control(unit, owner)冒充“结束这个控制效果”，也不能把recall改为move。若单位离开原区域后成为新对象，旧引用不自动追踪新实例。控制变化造成的争夺／对决仍由正常规则任务处理，不在法术文字中直接凭提醒文字加分。

## 0504 持卫的裁决：一次顶／底放置

[逐卡文字与调用](card-operator-reading/0501-0600.md#card-0504) · [核验卡图](../tmp/ruling-card-faces/0504.webp)

卡文明确区分施法者选择战场敌军，与单位拥有者选择／执行顶底放置；拥有者不等于当时控制者。先用declare取得拥有者在结算时的top／bottom决定，再用transfer(position=..., actor=owner)完成一次区域转移。该动作不是回收，也不洗牌；不再拆成无位置的transfer加reorder。

## 0541 奥义！雷铠：普通效果明确，替代交互仍待核

[逐卡文字与调用](card-operator-reading/0501-0600.md#card-0541) · [核验卡图](../tmp/ruling-card-faces/0541.webp)

确认私密look与draw不是公开reveal／普通transfer；余牌指向本次看见的集合，不能任意烧当前新顶部牌。Flow提供废牌来源权限与替代基础费用，并对关联链项按流转规则处理离链放逐，不能只在成功结算尾部放逐。

若选择的牌未实际抽走，例如抽牌被替代，而牌仍留在原顶部，本次未找到专门说明可确定rest排除的是所选牌还是实际完成抽取的牌、以及指定余牌的BURN授权边界。旧绑定“实际未抽取剩余牌”不能不加说明就作为裁定。保留VERIFY，不把transfer(identity=BURN)或更宽的burn参数当成解决规则歧义。

## 0656 章獭：替代获得分数，不替代征服／据守

[逐卡文字与调用](card-operator-reading/0601-0700.md#card-0656) · [核验卡图](../tmp/ruling-card-faces/0656.webp)

按卡文及规则470–473，匹配玩家自己第1／2回合、cause为HOLD／CONQUER、即将获得的1分，取消该增分并由该玩家draw(1)。其他效果给分不在本卡范围内；不能得分后再加一次抽牌，也不能取消整个得分战场的过程使其重复征服。因而补GAIN_POINTS.before，保留来源与回合归属。

## 0836 影分身：撤销错误待核，修正放逐时点

[逐卡文字与调用](card-operator-reading/0801-0900.md#card-0836) · [核验卡图](../tmp/ruling-card-faces/0836.webp)

规则187.11直接定义0战力影分身；卡图右上也明确为0。数据库might=null是来源字段缺失，不是规则未定义。笔记使用注明来源的TokenTemplate，不修改原始目录快照，也不建立“所有null都等于0”的规则。

更关键的是，卡文为“可以放逐……若如此做”，没有“放逐……以……”的费用连接。按规则204–205、383.3，选择是否执行首部可选触发在定稿时，放逐动作在能力结算时发生；原pay(banish-cost)分解错误。应banish指定废牌单位，实际放逐后grant_keyword(ASSAULT,4,THIS_TURN)。该触发被counter时不会先失去废牌单位；放逐没有实际发生时也不获得强攻。

## 0922 隐秘追踪者：改映射，不增跟随算子

[逐卡文字与调用](card-operator-reading/0901-1000.md#card-0922) · [核验卡图](../tmp/ruling-card-faces/0922.webp)

[官方赛事规则说明](https://playriftbound.com/en-us/news/announcements/tournament-rules-january-update/)把本卡列为触发能力造成移动的例子。结合当前规则383.2.c、359.3.f.3、448–455，原移动先完成，触发信息保存该次移动的地点，随后能力结算执行新的move。这里的目的地按触发事件保存，不因被跟随单位再次移动而自动改成其最新位置。这是通则推导，不是假称找到逐卡专门FAQ。

无需付普通移动横置费用；不能加入已提交批次。跟随时仍重检自身对象和目的地合法性、正常生成移动事件／任务。旧join=pending_move要求取得不存在的未提交窗口，予以撤销。

## 1025 偶像谷：改能力控制者，不增buff参数

[逐卡文字与调用](card-operator-reading/1001-1100.md#card-1025) · [核验卡图](../tmp/ruling-card-faces/1025.webp)

规则190.6.c与[Unleashed FAQ](https://playriftbound.com/en-us/news/rules-and-releases/unleashed-rules-faq-and-clarifications/)明确，战场能力指定某玩家作选择时，该玩家控制该能力。因此p绑定打出单位的玩家，而非把战场控制者当p、再额外传一个不同actor。Energy1为首部触发费用；增益在结算时给予，已有增益时受正常上限限制。现有pay与buff能完整表达。

## API变更与冗余决定

| 契约变更 | 依据 | 函数数量变化 |
| --- | --- | ---: |
| 新增end_modifier | 恶意收购精确结束关联控制效果 | +1 |
| transfer增加position=None/top/bottom | 持卫的裁决的一次顶底放置 | 0 |
| 补STUN、MIGHT_CHANGE、GAIN_POINTS的事件／替代定义 | 普朗克官方交互及章獭卡文 | 0 |
| 澄清move、on_event与触发信息绑定 | 隐秘追踪者；偶像谷控制者；恶意收购时点 | 0 |
| 明确pay不自动替后续play减免基础费用 | 费用规则；仍待核的两张不借接口修订虚报通过 | 0 |

72→73个正式函数。没有增加普朗克、章獭、随行、顶底放置等卡牌专用函数。end_modifier与change_control分别是结束既有修饰和建立新修饰，不是同义入口。其他接口重叠结论见[冗余检查](card-api-overlap.md)。

## 留存与统计限制

[原第二轮报告](operator-audits/round-2-coverage.md)与[V2 API](basic-operators-api-v2.md)保留。本次12张的当前分解写回原逐卡笔记，历史第二轮段落另标明。其余1094张没有再次完整阅读，不能把其既有判定重新标成V2.1完整阅读通过。当前[总报告](card-api-coverage.md)分开呈现第二轮原结果与本次专项结果。

五张待核：0201、0286、0338、0453、0541。后续只有找到足以决定调用的规则依据，才能解除相应VERIFY；改变API签名本身不构成规则证明。

本次文档结构核对：73个函数定义；原第二轮2338处调用与本次38处调用均能匹配当前签名；本次无未绑定小写变量。12张专项段落已写入；1106张笔记的5542个原文规则／装备字段仍与固定目录逐字段相同，目录快照及V2 API存档未改动。排除代码块后的4795条本地文档链接无缺失目标。本项只核对文档结构和原文留存，不执行游戏效果、不运行项目测试套件，五张候选程序不因此获得语义通过。

V2.1 API SHA-256：`e71df1d2bc6035fe20e24f8b2a16f8daf3062e26bc267d4687657bda99155250`。
