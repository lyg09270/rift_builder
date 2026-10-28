# 卡牌算子：逐卡阅读索引
当前API参考已进入[V4](basic-operators-api.md)，见[V4迁移表](card-api-changes-v4.md)与[程序流程契约](card-resolution-v4.md)。以下逐卡记录仍绑定[冻结V3](basic-operators-api-v3.md)，未自动迁移或上调覆盖率。

<!-- R3-INDEX-START -->
当前第三轮V3（71函数）：已完整复读1106/1106，确认1059（95.75%），待核7，未覆盖40。[报告](card-api-coverage.md) · [修订与简化](card-api-changes-v3.md) · [终审核对](operator-audits/round-3-validation.md) · [冗余审查](operator-audits/round-3-redundancy.md)。以下旧轮次数值仅供历史追溯。
<!-- R3-INDEX-END -->

历史专项：[12张真实效果核验](card-effect-rulings-review.md)采用[API V2.1](basic-operators-api-v2.1.md)，共73函数。当时专项确认7张、待核5张；当前以页首第三轮结果为准。

<!-- API-INDEX-START -->
第二轮72算子API历史：已完整重读1106/1106本体。[第二轮原报告](operator-audits/round-2-coverage.md) · [修订依据](card-api-changes-v2.md)。第一轮已[单独存档](operator-audits/round-1-reading.md)。
<!-- API-INDEX-END -->

[返回算子定义](card-operators.md)

范围为本地 OpenRift 快照的全部1,106个卡牌本体。按英文名排序编号，每张保留人工阅读笔记、玩法属性、EN／SC／TC完整规则及装备效果文本和目录勘误。同玩法文本的印刷合组；不同文本不互相覆盖，递归包含背面。

源 SHA-256：`ad521068ff70def757a00ff18f049583e1e5dffdc3e0152515eb90007b54ca05`。

阅读整理日期：2026-10-27至2026-10-28。只生成文档；没有执行游戏转换或测试套件。

| 语言 | 有卡面本体 | 文本组 | 规则字段为null的组 |
| --- | ---: | ---: | ---: |
| EN | 1106 | 1222 | 18 |
| SC | 1105 | 1217 | 16 |
| TC | 321 | 332 | 12 |

null可能表示纯属性卡，也可能表示该印刷缺文，须结合本体、其他印刷和笔记判断。未把缺中文、缺战力或损坏文本填成推测值。缺SC卡面：Bomb。

## 分批记录

| 批次 | 张数 |
| --- | ---: |
| [0001–0100](card-operator-reading/0001-0100.md) | 100 |
| [0101–0200](card-operator-reading/0101-0200.md) | 100 |
| [0201–0300](card-operator-reading/0201-0300.md) | 100 |
| [0301–0400](card-operator-reading/0301-0400.md) | 100 |
| [0401–0500](card-operator-reading/0401-0500.md) | 100 |
| [0501–0600](card-operator-reading/0501-0600.md) | 100 |
| [0601–0700](card-operator-reading/0601-0700.md) | 100 |
| [0701–0800](card-operator-reading/0701-0800.md) | 100 |
| [0801–0900](card-operator-reading/0801-0900.md) | 100 |
| [0901–1000](card-operator-reading/0901-1000.md) | 100 |
| [1001–1100](card-operator-reading/1001-1100.md) | 100 |
| [1101–1106](card-operator-reading/1101-1106.md) | 6 |

## 全卡目录

词汇是语义阅读索引，不能仅凭有标签就宣称所有句段均已完成可执行映射。费用、数值、目标、期限等以分批附录原文及其来源为据。

| 编号 | 英文名 | 简中印刷名 | 类型 | 语义词汇 |
| --- | --- | --- | --- | --- |
| 0001 | [Abandon](card-operator-reading/0001-0100.md#card-0001) | 遗弃 | spell | COUNTER, TRANSFER, PREDICT, REPLACE |
| 0002 | [Abandoned Hall](card-operator-reading/0001-0100.md#card-0002) | 废弃大厅 | battlefield | MOD_MIGHT |
| 0003 | [Acceleration Gate](card-operator-reading/0001-0100.md#card-0003) | 加速之门 | spell | READY |
| 0004 | [Acceptable Losses](card-operator-reading/0001-0100.md#card-0004) | 折戟再战 | spell | KILL, CHOOSE |
| 0005 | [Adaptatron](card-operator-reading/0001-0100.md#card-0005) | 自适应机器人 | unit | KILL, BUFF, IF_DO |
| 0006 | [Affectionate Poro](card-operator-reading/0001-0100.md#card-0006) | 贴贴魄罗 | unit | DRAW |
| 0007 | [Against the Odds](card-operator-reading/0001-0100.md#card-0007) | 矢志不退 | spell | MOD_MIGHT |
| 0008 | [Agony’s Embrace](card-operator-reading/0001-0100.md#card-0008) | 痛苦之拥 | legend | DRAW, DISCARD |
| 0009 | [Ahri, Alluring](card-operator-reading/0001-0100.md#card-0009) | 阿狸, 嫣然狐媚 | unit | SCORE |
| 0010 | [Ahri, Confident](card-operator-reading/0001-0100.md#card-0010) | 阿狸, 自信闪耀 | unit | MOD_MIGHT |
| 0011 | [Ahri, Inquisitive](card-operator-reading/0001-0100.md#card-0011) | 阿狸, 天真绮梦 | unit | MOD_MIGHT |
| 0012 | [Akali, Brash](card-operator-reading/0001-0100.md#card-0012) | 阿卡丽, 狂傲不羁 | unit | ADD_RESOURCE, BANISH, PERMIT, DELAY |
| 0013 | [Akali, Deadly Weapon](card-operator-reading/0001-0100.md#card-0013) | 阿卡丽, 游离之刃 | unit | DAMAGE, MOD_MIGHT, REPLACE |
| 0014 | [Akali, Silent](card-operator-reading/0001-0100.md#card-0014) | 阿卡丽, 无形致命 | unit | RESTRICT, MOD_MIGHT |
| 0015 | [Akshan, Mischievous](card-operator-reading/0001-0100.md#card-0015) | 阿克尚, 放浪不羁 | unit | PAY, MOVE, CONTROL, ATTACH, DELAY |
| 0016 | [Albus Ferros](card-operator-reading/0001-0100.md#card-0016) | 阿不思·菲罗斯 | unit | SPEND_BUFF, CHANNEL |
| 0017 | [Allay, Eager Admirer](card-operator-reading/0001-0100.md#card-0017) | 艾蕾，头号拥趸 | unit | GRANT_KEYWORD |
| 0018 | [Alpha Strike](card-operator-reading/0001-0100.md#card-0018) | 阿尔法突袭 | spell | DAMAGE, XP, REPEAT |
| 0019 | [Alpha Wildclaw](card-operator-reading/0001-0100.md#card-0019) | 野爪兽王 | unit | RESTRICT |
| 0020 | [Altar of Blood](card-operator-reading/0001-0100.md#card-0020) | 鲜血祭坛 | battlefield | REPLACE, PAY, HEAL, EXHAUST, RECALL |
| 0021 | [Altar of Memories](card-operator-reading/0001-0100.md#card-0021) | 追忆祭坛 | gear | PAY, EXHAUST, DRAW, TRANSFER, CHOOSE |
| 0022 | [Altar to Unity](card-operator-reading/0001-0100.md#card-0022) | 团结圣坛 | battlefield | CREATE, PLAY |
| 0023 | [Amateur Demolitionist](card-operator-reading/0001-0100.md#card-0023) | 业余爆破狂 | unit | CREATE, PLAY |
| 0024 | [Amateur Recital](card-operator-reading/0001-0100.md#card-0024) | 业余排练厅 | battlefield | MOVE, RECALL |
| 0025 | [Ambessa, Respected and Feared](card-operator-reading/0001-0100.md#card-0025) | 安蓓萨, 战狼尊母 | unit | GRANT_KEYWORD, KILL |
| 0026 | [Ambessa, The Wolf](card-operator-reading/0001-0100.md#card-0026) | 安蓓萨, 恶狼意志 | unit | MOD_MIGHT, RESTRICT |
| 0027 | [An Offer You Can’t Refuse](card-operator-reading/0001-0100.md#card-0027) | 无法拒绝的提议 | spell | KILL, CREATE, PLAY |
| 0028 | [Ancient Henge](card-operator-reading/0001-0100.md#card-0028) | 远古簇碑 | gear | EXHAUST, PAY, ADD_RESOURCE |
| 0029 | [Ancient Warmonger](card-operator-reading/0001-0100.md#card-0029) | 远古战狂 | unit | GRANT_KEYWORD |
| 0030 | [Angle Shot](card-operator-reading/0001-0100.md#card-0030) | 取放自如 | spell | CHOOSE, ATTACH, DETACH, DRAW |
| 0031 | [Angler Beast](card-operator-reading/0001-0100.md#card-0031) | 提灯海煞 | unit | TRANSFER |
| 0032 | [Angler Wyrm](card-operator-reading/0001-0100.md#card-0032) | 提灯亚龙 | unit | EXHAUST, CHOOSE, MOVE |
| 0033 | [Anivia, Primal](card-operator-reading/0001-0100.md#card-0033) | 艾尼维亚, 初始啼鸣 | unit | DAMAGE |
| 0034 | [Annie, Fiery](card-operator-reading/0001-0100.md#card-0034) | 安妮, 汹涌烈焰 | unit | MOD_DAMAGE |
| 0035 | [Annie, Stubborn](card-operator-reading/0001-0100.md#card-0035) | 安妮, 野火丛生 | unit | TRANSFER |
| 0036 | [Antagonistic Apparatus](card-operator-reading/0001-0100.md#card-0036) | 分裂强袭机 | unit | ENTRY, CREATE, PLAY |
| 0037 | [Aphelios, Exalted](card-operator-reading/0001-0100.md#card-0037) | 厄斐琉斯, 出尘 | unit | CHOOSE, READY, CHANNEL, BUFF |
| 0038 | [Applied Researchers](card-operator-reading/0001-0100.md#card-0038) | 实干研究员 | unit | MOD_COST |
| 0039 | [Apprentice Mage](card-operator-reading/0001-0100.md#card-0039) | 见习法师 | unit | PREDICT, MOD_MIGHT |
| 0040 | [Apprentice Smith](card-operator-reading/0001-0100.md#card-0040) | 学徒铁匠 | unit | REVEAL, DRAW, RECYCLE |
| 0041 | [Arachnoid Horror](card-operator-reading/0001-0100.md#card-0041) | 恐怖蛛怪 | unit | PERMIT |
| 0042 | [Arcane Shift](card-operator-reading/0001-0100.md#card-0042) | 奥术跃迁 | spell | BANISH, PLAY, DAMAGE |
| 0043 | [Arena Bar](card-operator-reading/0001-0100.md#card-0043) | 竞技场酒吧 | gear | EXHAUST, BUFF |
| 0044 | [Arena Kingpin](card-operator-reading/0001-0100.md#card-0044) | 竞技场理事 | unit | ENTRY, EXHAUST, MOD_MIGHT |
| 0045 | [Arise!](card-operator-reading/0001-0100.md#card-0045) | 沙兵现身 | spell | CREATE, PLAY, READY |
| 0046 | [Armed Assailant](card-operator-reading/0001-0100.md#card-0046) | 武装强袭者 | unit | PAY, ENTRY, ATTACH, MOD_COST |
| 0047 | [Armored Tusker](card-operator-reading/0001-0100.md#card-0047) | 重甲象骑 | unit | DAMAGE |
| 0048 | [Ashe, Focused](card-operator-reading/0001-0100.md#card-0048) | 艾希, 凛如寒芒 | unit | REVEAL, CHOOSE, BANISH, DELAY, TRANSFER |
| 0049 | [Aspirant’s Climb](card-operator-reading/0001-0100.md#card-0049) | 攀圣长阶 | battlefield | SET_RULE |
| 0050 | [Aspiring Engineer](card-operator-reading/0001-0100.md#card-0050) | 见习工程师 | unit | TRANSFER |
| 0051 | [Assembly Rig](card-operator-reading/0001-0100.md#card-0051) | 装配架 | gear | PAY, RECYCLE, EXHAUST, CREATE, PLAY |
| 0052 | [Astral Heron](card-operator-reading/0001-0100.md#card-0052) | 星界灵鹭 | unit | MOD_COST, DELAY |
| 0053 | [Atakhan](card-operator-reading/0001-0100.md#card-0053) | 厄塔汗 | unit | PAY, KILL, MOD_COST, CHOOSE |
| 0054 | [Aurok General](card-operator-reading/0001-0100.md#card-0054) | 奥洛克将军 | unit | MOD_MIGHT |
| 0055 | [Ava Achiever](card-operator-reading/0001-0100.md#card-0055) | 斥候标兵 艾娃 | unit | PAY, PLAY |
| 0056 | [Avalanche](card-operator-reading/0001-0100.md#card-0056) | 雪崩 | spell | DAMAGE |
| 0057 | [Azir, Ascendant](card-operator-reading/0001-0100.md#card-0057) | 阿兹尔, 飞升者 | unit | PAY, MOVE, ATTACH |
| 0058 | [Azir, Sovereign](card-operator-reading/0001-0100.md#card-0058) | 阿兹尔, 帝君 | unit | MOVE |
| 0059 | [B.F. Sword](card-operator-reading/0001-0100.md#card-0059) | 暴风大剑 | gear | ATTACH, MOD_MIGHT |
| 0060 | [Baccai Reaper](card-operator-reading/0001-0100.md#card-0060) | 巴凯收割者 | unit | PAY, GRANT_KEYWORD |
| 0061 | [Baccai Sandspinner](card-operator-reading/0001-0100.md#card-0061) | 巴凯旋沙者 | unit | MOD_COST, GRANT_KEYWORD |
| 0062 | [Baccai Witherclaw](card-operator-reading/0001-0100.md#card-0062) | 枯爪巴凯 | unit | MOD_MIGHT, CHANNEL |
| 0063 | [Back Off](card-operator-reading/0001-0100.md#card-0063) | 走开 | spell | STUN, DRAW |
| 0064 | [Back to Back](card-operator-reading/0001-0100.md#card-0064) | 背靠背 | spell | MOD_MIGHT |
| 0065 | [Back-Alley Bar](card-operator-reading/0001-0100.md#card-0065) | 后巷酒吧 | battlefield | MOD_MIGHT |
| 0066 | [Baited Hook](card-operator-reading/0001-0100.md#card-0066) | 海兽钓钩 | gear | EXHAUST, PAY, KILL, LOOK, BANISH, PLAY, RECYCLE |
| 0067 | [Bandle Scouts’ Academy](card-operator-reading/0001-0100.md#card-0067) | 班德尔斥候学院 | battlefield | CREATE, PLAY |
| 0068 | [Bandle Soldier](card-operator-reading/0001-0100.md#card-0068) | 班德尔士兵 | unit | ENTRY |
| 0069 | [Bandle Tree](card-operator-reading/0001-0100.md#card-0069) | 班德尔树 | battlefield | SET_RULE |
| 0070 | [Banner of Conquest](card-operator-reading/0001-0100.md#card-0070) | 征服之旗 | gear | GRANT_KEYWORD |
| 0071 | [Bard, Mercurial](card-operator-reading/0001-0100.md#card-0071) | 巴德, 幻神 | unit | PAY, EXHAUST, MOVE |
| 0072 | [Baron Nashor](card-operator-reading/0001-0100.md#card-0072) | 纳什男爵 | unit | CREATE, ENTRY, RESTRICT, MOD_MIGHT |
| 0073 | [Baron Pit](card-operator-reading/0001-0100.md#card-0073) | 男爵巢穴 | battlefield | PERMIT, SET_RULE |
| 0074 | [Bashful Bloom](card-operator-reading/0001-0100.md#card-0074) | 含羞蓓蕾 | legend | PAY, EXHAUST, MOD_COST, CREATE, PLAY |
| 0075 | [Battering Ram](card-operator-reading/0001-0100.md#card-0075) | 攻城锤 | unit | MOD_COST |
| 0076 | [Battle Mistress](card-operator-reading/0001-0100.md#card-0076) | 战争女神 | legend | EXHAUST, CREATE, PLAY, READY |
| 0077 | [Battle Preparations](card-operator-reading/0001-0100.md#card-0077) | 战前仪式 | spell | SHOW_OFF, MOD_MIGHT, READY |
| 0078 | [Battlefield Armorer](card-operator-reading/0001-0100.md#card-0078) | 战地甲胄师 | unit | PAY, TRANSFER |
| 0079 | [Beast Below](card-operator-reading/0001-0100.md#card-0079) | 海渊巨兽 | unit | TRANSFER |
| 0080 | [Bedeviling Stranger](card-operator-reading/0001-0100.md#card-0080) | 祸心陌客 | unit | CHOOSE, TRANSFER |
| 0081 | [Bellows Breath](card-operator-reading/0001-0100.md#card-0081) | 风箱炎息 | spell | DAMAGE, REPEAT |
| 0082 | [Bewitching Spirit](card-operator-reading/0001-0100.md#card-0082) | 魅惑之灵 | unit | CHOOSE, DISCARD |
| 0083 | [Bilgewater Bully](card-operator-reading/0001-0100.md#card-0083) | 比尔吉沃特恶霸 | unit | GRANT_KEYWORD |
| 0084 | [Bilgewater Tracker](card-operator-reading/0001-0100.md#card-0084) | 比港追捕者 | unit | DAMAGE |
| 0085 | [Bird](card-operator-reading/0001-0100.md#card-0085) | 战鹰 | unit | RESTRICT |
| 0086 | [Black Flame Altar](card-operator-reading/0001-0100.md#card-0086) | 黑焰祭坛 | battlefield | GRANT_KEYWORD |
| 0087 | [Black Market](card-operator-reading/0001-0100.md#card-0087) | 黑市 | battlefield | PAY, DRAW, PERMIT |
| 0088 | [Black Market Broker](card-operator-reading/0001-0100.md#card-0088) | 黑市掮客 | unit | CREATE, PLAY |
| 0089 | [Black Rose Dignitary](card-operator-reading/0001-0100.md#card-0089) | 黑色玫瑰要员 | unit | CHANNEL |
| 0090 | [Black Rose Sanctum](card-operator-reading/0001-0100.md#card-0090) | 黑色玫瑰圣所 | battlefield | CREATE, PLAY |
| 0091 | [Blade Dancer](card-operator-reading/0001-0100.md#card-0091) | 刀锋舞者 | legend | PAY, EXHAUST, READY |
| 0092 | [Blade of the Exile](card-operator-reading/0001-0100.md#card-0092) | 放逐之锋 | gear | PAY, ATTACH, MOD_MIGHT, GRANT_KEYWORD |
| 0093 | [Blade of the Ruined King](card-operator-reading/0001-0100.md#card-0093) | 破败王者之刃 | gear | PAY, KILL, ATTACH, MOD_MIGHT |
| 0094 | [Blade Twirler](card-operator-reading/0001-0100.md#card-0094) | 旋风剑客 | unit | BURN, CHOOSE |
| 0095 | [Blast Cone](card-operator-reading/0001-0100.md#card-0095) | 喷射球果 | gear | MOVE, EXHAUST, STUN |
| 0096 | [Blast Corps Cadet](card-operator-reading/0001-0100.md#card-0096) | 爆破队学员 | unit | PAY, DAMAGE |
| 0097 | [Blast of Power](card-operator-reading/0001-0100.md#card-0097) | 爆能术 | spell | KILL |
| 0098 | [Blastcone Fae](card-operator-reading/0001-0100.md#card-0098) | 爆裂球果仙灵 | unit | MOD_MIGHT |
| 0099 | [Blazing Scorcher](card-operator-reading/0001-0100.md#card-0099) | 灼焰飞龙 | unit | PAY, ENTRY |
| 0100 | [Blighted Battleaxe](card-operator-reading/0001-0100.md#card-0100) | 枯萎战斧 | gear | PAY, ATTACH, MOD_MIGHT, DETACH, DAMAGE |
| 0101 | [Blind Fury](card-operator-reading/0101-0200.md#card-0101) | 暴怒冲动 | spell | REVEAL, CHOOSE, BANISH, PLAY, RECYCLE |
| 0102 | [Blind Monk](card-operator-reading/0101-0200.md#card-0102) | 盲僧 | legend | PAY, EXHAUST, BUFF |
| 0103 | [Blitzcrank, Impassive](card-operator-reading/0101-0200.md#card-0103) | 布里茨, 钢铁意志 | unit | MOVE, TRANSFER |
| 0104 | [Block](card-operator-reading/0101-0200.md#card-0104) | 格挡 | spell | GRANT_KEYWORD |
| 0105 | [Blood Money](card-operator-reading/0101-0200.md#card-0105) | 血钱 | spell | KILL, CREATE, PLAY |
| 0106 | [Blood Rose](card-operator-reading/0101-0200.md#card-0106) | 猩红玫瑰 | gear | PAY, XP, EXHAUST, READY |
| 0107 | [Blood Rush](card-operator-reading/0101-0200.md#card-0107) | 血性冲刺 | spell | GRANT_KEYWORD, REPEAT |
| 0108 | [Bloodharbor Ripper](card-operator-reading/0101-0200.md#card-0108) | 血港鬼影 | legend | PAY, EXHAUST, TRANSFER, CREATE, PLAY |
| 0109 | [Bloodscent Swarm](card-operator-reading/0101-0200.md#card-0109) | 觅血虫群 | unit | MOD_COST |
| 0110 | [Blossoming Dreamroot](card-operator-reading/0101-0200.md#card-0110) | 幻梦之根 | gear | DRAW |
| 0111 | [Blue Sentinel](card-operator-reading/0101-0200.md#card-0111) | 苍蓝雕纹魔像 | unit | MOD_TRIGGER, DELAY, ADD_RESOURCE |
| 0112 | [Body Rune](card-operator-reading/0101-0200.md#card-0112) | 摧破符文 | rune | ADD_RESOURCE, PAY, RECYCLE, EXHAUST |
| 0113 | [Bomb](card-operator-reading/0101-0200.md#card-0113) | 缺失 | gear | DAMAGE, KILL |
| 0114 | [Bonds of Strength](card-operator-reading/0101-0200.md#card-0114) | 力量之缚 | spell | MOD_MIGHT, REPEAT |
| 0115 | [Bone Skewer](card-operator-reading/0101-0200.md#card-0115) | 透骨尖钉 | spell | CHOOSE, REVEAL, PLAY, STUN, IF_DO |
| 0116 | [Boneshiver](card-operator-reading/0101-0200.md#card-0116) | 碎骨棒 | gear | ATTACH, MOD_MIGHT, CHANNEL |
| 0117 | [Boots of Swiftness](card-operator-reading/0101-0200.md#card-0117) | 轻灵之靴 | gear | ATTACH, MOD_MIGHT, GRANT_KEYWORD |
| 0118 | [Bottled Constellation](card-operator-reading/0101-0200.md#card-0118) | 瓶中星海 | gear | KILL, SCORE, IF_DO |
| 0119 | [Bounty Hunter](card-operator-reading/0101-0200.md#card-0119) | 赏金猎人 | legend | EXHAUST, GRANT_KEYWORD |
| 0120 | [Boy Who Shattered Time](card-operator-reading/0101-0200.md#card-0120) | 时间刺客 | legend | DISEMPOWER, EXHAUST, MOD_COST, GRANT_ABILITY, DELAY, KILL |
| 0121 | [Brawl](card-operator-reading/0101-0200.md#card-0121) | 乱殴 | spell | GRANT_KEYWORD |
| 0122 | [Brazen Buccaneer](card-operator-reading/0101-0200.md#card-0122) | 粗鲁的海盗 | unit | DISCARD, MOD_COST |
| 0123 | [Breakneck Mech](card-operator-reading/0101-0200.md#card-0123) | 疾驰机械 | unit | GRANT_KEYWORD, ENTRY |
| 0124 | [Brittle Steel](card-operator-reading/0101-0200.md#card-0124) | 极寒脆化 | spell | KILL, PLAY, BANISH |
| 0125 | [Brush](card-operator-reading/0101-0200.md#card-0125) | 草丛 | battlefield | MOD_MIGHT, REPLACE_BATTLEFIELD |
| 0126 | [Brutal Hunter](card-operator-reading/0101-0200.md#card-0126) | 残暴猎手 | unit | MOD_MIGHT, GRANT_KEYWORD |
| 0127 | [Brutalizer](card-operator-reading/0101-0200.md#card-0127) | 残暴之力 | gear | ATTACH, MOD_MIGHT |
| 0128 | [Brynhir Thundersong](card-operator-reading/0101-0200.md#card-0128) | 颂雷者 布林希尔 | unit | RESTRICT |
| 0129 | [Bubble Bot](card-operator-reading/0101-0200.md#card-0129) | 泡泡机 | unit | READY |
| 0130 | [Buff](card-operator-reading/0101-0200.md#card-0130) | 增益 | other | SET_RULE, MOD_MIGHT |
| 0131 | [Buhru Captain](card-operator-reading/0101-0200.md#card-0131) | 芭茹队长 | unit | CHOOSE, DRAW, BUFF |
| 0132 | [Bullet Time](card-operator-reading/0101-0200.md#card-0132) | 弹幕时间 | spell | PAY, DAMAGE |
| 0133 | [Burn Away](card-operator-reading/0101-0200.md#card-0133) | 冥火销魂 | spell | BANISH, BURN |
| 0134 | [Bushwhack](card-operator-reading/0101-0200.md#card-0134) | 丛林伏击 | spell | ENTRY, CREATE, PLAY |
| 0135 | [Bushwhack Trap](card-operator-reading/0101-0200.md#card-0135) | 伏击陷阱 | gear | SET_RULE |
| 0136 | [Butcher of the Sands](card-operator-reading/0101-0200.md#card-0136) | 荒漠屠夫 | legend | PAY, EXHAUST, ADD_RESOURCE, RESTRICT_RESOURCE |
| 0137 | [Caitlyn, Patrolling](card-operator-reading/0101-0200.md#card-0137) | 凯特琳, 守望者 | unit | SET_RULE, EXHAUST, DAMAGE |
| 0138 | [Call to Battle](card-operator-reading/0101-0200.md#card-0138) | 战斗号令 | spell | MOVE, CHOOSE |
| 0139 | [Call to Glory](card-operator-reading/0101-0200.md#card-0139) | 荣耀召唤 | spell | SPEND_BUFF, MOD_COST, MOD_MIGHT |
| 0140 | [Called Shot](card-operator-reading/0101-0200.md#card-0140) | 预判攻势 | spell | LOOK, CHOOSE, DRAW, RECYCLE, REPEAT |
| 0141 | [Calm Rune](card-operator-reading/0101-0200.md#card-0141) | 翠意符文 | rune | ADD_RESOURCE, PAY, RECYCLE, EXHAUST |
| 0142 | [Cannon Barrage](card-operator-reading/0101-0200.md#card-0142) | 加农炮幕 | spell | DAMAGE |
| 0143 | [Captain Farron](card-operator-reading/0101-0200.md#card-0143) | 法荣队长 | unit | GRANT_KEYWORD |
| 0144 | [Card Sharp](card-operator-reading/0101-0200.md#card-0144) | 大老千 | unit | CREATE, PLAY, CHOOSE, REPEAT |
| 0145 | [Carnivorous Snapvine](card-operator-reading/0101-0200.md#card-0145) | 食肉蛇藤 | unit | DAMAGE |
| 0146 | [Carrion Dredger](card-operator-reading/0101-0200.md#card-0146) | 腐泥疏浚工 | unit | CREATE, PLAY |
| 0147 | [Cataclysm](card-operator-reading/0101-0200.md#card-0147) | 天崩地裂 | spell | RESTRICT, MOVE |
| 0148 | [Cataclysmic Duel](card-operator-reading/0101-0200.md#card-0148) | 末日决斗 | spell | CHOOSE, KILL |
| 0149 | [Catalyst of Aeons](card-operator-reading/0101-0200.md#card-0149) | 万世催化石 | spell | CHANNEL, DRAW, IF_DO |
| 0150 | [Cemetery Attendant](card-operator-reading/0101-0200.md#card-0150) | 牧灵犬 | unit | TRANSFER |
| 0151 | [Chakram Dancer](card-operator-reading/0101-0200.md#card-0151) | 环刃舞者 | unit | GRANT_KEYWORD |
| 0152 | [Challenge](card-operator-reading/0101-0200.md#card-0152) | 决斗 | spell | DAMAGE |
| 0153 | [Chaos Rune](card-operator-reading/0101-0200.md#card-0153) | 混沌符文 | rune | ADD_RESOURCE, PAY, RECYCLE, EXHAUST |
| 0154 | [Charm](card-operator-reading/0101-0200.md#card-0154) | 魅惑妖术 | spell | MOVE |
| 0155 | [Chem-Baroness](card-operator-reading/0101-0200.md#card-0155) | 炼金男爵 | legend | EXHAUST, CREATE, PLAY, MOD_RESOURCE |
| 0156 | [Chemtech Cask](card-operator-reading/0101-0200.md#card-0156) | 炼金科技桶 | gear | EXHAUST, CREATE, PLAY |
| 0157 | [Chemtech Enforcer](card-operator-reading/0101-0200.md#card-0157) | 炼金太保 | unit | DISCARD |
| 0158 | [Chronobreak](card-operator-reading/0101-0200.md#card-0158) | 时空断裂 | spell | PAY, BANISH, PLAY, ORDER |
| 0159 | [Cithria of Cloudfield](card-operator-reading/0101-0200.md#card-0159) | 云丛的希思莉亚 | unit | BUFF |
| 0160 | [Clairvoyance](card-operator-reading/0101-0200.md#card-0160) | 千里眼 | spell | PREDICT, DRAW |
| 0161 | [Clanging Sentry](card-operator-reading/0101-0200.md#card-0161) | 叮响巡警 | unit | GRANT_KEYWORD |
| 0162 | [Clash of Giants](card-operator-reading/0101-0200.md#card-0162) | 巨人之战 | spell | DAMAGE |
| 0163 | [Cleave](card-operator-reading/0101-0200.md#card-0163) | 顺劈 | spell | GRANT_KEYWORD |
| 0164 | [Clocktower Guardian](card-operator-reading/0101-0200.md#card-0164) | 钟塔守护者 | unit | PREDICT, BANISH, PLAY |
| 0165 | [Clockwork Keeper](card-operator-reading/0101-0200.md#card-0165) | 小小守护者 | unit | PAY, DRAW |
| 0166 | [Cloth Armor](card-operator-reading/0101-0200.md#card-0166) | 布甲 | gear | ATTACH, GRANT_KEYWORD |
| 0167 | [Cloud Drake](card-operator-reading/0101-0200.md#card-0167) | 云端亚龙 | unit | DRAW |
| 0168 | [Coalesced Energy](card-operator-reading/0101-0200.md#card-0168) | 能量聚合体 | unit | RECYCLE, CHANNEL |
| 0169 | [Combat Chef](card-operator-reading/0101-0200.md#card-0169) | 战斗厨神 | unit | PAY, ATTACH, MOD_COST |
| 0170 | [Combat Experience](card-operator-reading/0101-0200.md#card-0170) | 实战经验 | spell | MOD_MIGHT, REPLACE |
| 0171 | [Command: Attack](card-operator-reading/0101-0200.md#card-0171) | 指令：攻击 | spell | CHOOSE, MOVE, LOOK, REVEAL, DRAW, RECYCLE |
| 0172 | [Commander Ledros](card-operator-reading/0101-0200.md#card-0172) | 莱卓斯指挥官 | unit | KILL, MOD_COST |
| 0173 | [Concentrate](card-operator-reading/0101-0200.md#card-0173) | 聚心凝神 | spell | DRAW, MOD_COST, REPLACE |
| 0174 | [Concert Poster](card-operator-reading/0101-0200.md#card-0174) | 演出海报 | gear | PAY, CREATE, PLAY |
| 0175 | [Confront](card-operator-reading/0101-0200.md#card-0175) | 迎敌号令 | spell | ENTRY, DRAW |
| 0176 | [Conscription](card-operator-reading/0101-0200.md#card-0176) | 强制征召 | spell | XP, CONTROL, EXHAUST, RECALL |
| 0177 | [Consult the Heavens](card-operator-reading/0101-0200.md#card-0177) | 聆听天意 | spell | GRANT_KEYWORD, PREDICT |
| 0178 | [Consult the Past](card-operator-reading/0101-0200.md#card-0178) | 借鉴历史 | spell | DRAW |
| 0179 | [Consuming Curse](card-operator-reading/0101-0200.md#card-0179) | 蚀骨诅咒 | spell | DAMAGE, MOD_DAMAGE |
| 0180 | [Convergent Mutation](card-operator-reading/0101-0200.md#card-0180) | 聚合变异 | spell | SET_MIGHT |
| 0181 | [Corina Veraza](card-operator-reading/0101-0200.md#card-0181) | 卡银娜·薇蕊泽 | unit | CREATE, PLAY |
| 0182 | [Corrupt Enforcer](card-operator-reading/0101-0200.md#card-0182) | 腐化执法官 | unit | DISCARD, DRAW |
| 0183 | [Corrupted Dragon](card-operator-reading/0101-0200.md#card-0183) | 腐化巨龙 | unit | ENTRY, MOVE |
| 0184 | [Cosmic Vista](card-operator-reading/0101-0200.md#card-0184) | 星界绝景 | battlefield | SCORE |
| 0185 | [Counter Strike](card-operator-reading/0101-0200.md#card-0185) | 反击风暴 | spell | PREVENT_DAMAGE, DRAW |
| 0186 | [Covert Informant](card-operator-reading/0101-0200.md#card-0186) | 秘密线人 | unit | DRAW |
| 0187 | [Crackshot Corsair](card-operator-reading/0101-0200.md#card-0187) | 神射海盗 | unit | DAMAGE |
| 0188 | [Crescent Guardian](card-operator-reading/0101-0200.md#card-0188) | 新月禁卫 | unit | PAY, ENTRY |
| 0189 | [Crescent Strike](card-operator-reading/0101-0200.md#card-0189) | 新月打击 | spell | DAMAGE |
| 0190 | [Crimson Pigeons](card-operator-reading/0101-0200.md#card-0190) | 猩红飞鸽 | unit | MOD_MIGHT |
| 0191 | [Crowd Favorite](card-operator-reading/0101-0200.md#card-0191) | 竞技场人气王 | unit | XP, BUFF |
| 0192 | [Cruel Patron](card-operator-reading/0101-0200.md#card-0192) | 冷血贵族 | unit | KILL, PAY |
| 0193 | [Crumbling Sands](card-operator-reading/0101-0200.md#card-0193) | 崩解之沙 | spell | COUNTER |
| 0194 | [Cull](card-operator-reading/0101-0200.md#card-0194) | 萃取 | gear | ATTACH, MOD_MIGHT, CREATE, PLAY |
| 0195 | [Cull the Weak](card-operator-reading/0101-0200.md#card-0195) | 清理门户 | spell | CHOOSE, KILL |
| 0196 | [Curator of the Sands](card-operator-reading/0101-0200.md#card-0196) | 沙漠死神 | legend | EXHAUST, READY |
| 0197 | [Cursed Sarcophagus](card-operator-reading/0101-0200.md#card-0197) | 受诅咒的石棺 | gear | BANISH, EXHAUST, PLAY, LINK |
| 0198 | [Curtain Call](card-operator-reading/0101-0200.md#card-0198) | 完美谢幕 | spell | CHOOSE, DRAW, DAMAGE, MOD_MIGHT, REPEAT |
| 0199 | [Daisy!](card-operator-reading/0101-0200.md#card-0199) | 小菊！ | unit | ENTRY, MOD_COST, STUN |
| 0200 | [Dame the Despoiler](card-operator-reading/0101-0200.md#card-0200) | 夺魂钩 妲姆 | unit | SET_MIGHT, MOD_MIGHT |
| 0201 | [Dancing Grenade](card-operator-reading/0201-0300.md#card-0201) | 曼舞手雷 | spell | DAMAGE, PLAY, MOD_DAMAGE, LINK |
| 0202 | [Danger Zone](card-operator-reading/0201-0300.md#card-0202) | 危险温度 | spell | MOD_MIGHT, REPEAT |
| 0203 | [Dangerous Duo](card-operator-reading/0201-0300.md#card-0203) | 危险二人组 | unit | MOD_MIGHT |
| 0204 | [Daring Poro](card-operator-reading/0201-0300.md#card-0204) | 莽莽魄罗 | unit | MOD_MIGHT |
| 0205 | [Darius, Executioner](card-operator-reading/0201-0300.md#card-0205) | 德莱厄斯, 处刑官 | unit | READY, MOD_MIGHT |
| 0206 | [Darius, Trifarian](card-operator-reading/0201-0300.md#card-0206) | 德莱厄斯, 崔法利 | unit | READY, MOD_MIGHT |
| 0207 | [Dark Child, Starter](card-operator-reading/0201-0300.md#card-0207) | 黑暗之女, 入门 | legend | READY |
| 0208 | [Daughter of the Void](card-operator-reading/0201-0300.md#card-0208) | 虚空之女 | legend | EXHAUST, ADD_RESOURCE, RESTRICT_RESOURCE |
| 0209 | [Dauntless Vanguard](card-operator-reading/0201-0300.md#card-0209) | 无畏先锋 | unit | PERMIT |
| 0210 | [Dazzling Aurora](card-operator-reading/0201-0300.md#card-0210) | 闪耀极光 | gear | REVEAL, BANISH, PLAY, RECYCLE, REPEAT |
| 0211 | [Deadbloom Predator](card-operator-reading/0201-0300.md#card-0211) | 亡花掠食者 | unit | PERMIT |
| 0212 | [Deadly Flourish](card-operator-reading/0201-0300.md#card-0212) | 致命华彩 | spell | DAMAGE, DELAY, CREATE, PLAY |
| 0213 | [Death from Below](card-operator-reading/0201-0300.md#card-0213) | 涌泉之恨 | spell | KILL, PLAY, DELAY |
| 0214 | [Death Mark](card-operator-reading/0201-0300.md#card-0214) | 禁奥义！瞬狱影杀阵 | spell | BURN, CREATE, PLAY |
| 0215 | [Deathgrip](card-operator-reading/0201-0300.md#card-0215) | 断魂一扼 | spell | KILL, MOD_MIGHT, DRAW, IF_DO |
| 0216 | [Deceiver](card-operator-reading/0201-0300.md#card-0216) | 诡术妖姬 | legend | DISCARD, EXHAUST, CREATE, PLAY, COPY, GRANT_KEYWORD |
| 0217 | [Decisive Strike](card-operator-reading/0201-0300.md#card-0217) | 致命打击 | spell | MOD_MIGHT |
| 0218 | [Decree of Discord](card-operator-reading/0201-0300.md#card-0218) | 不和箴言 | spell | TRANSFER, CHOOSE |
| 0219 | [Decree of Focus](card-operator-reading/0201-0300.md#card-0219) | 专注箴言 | spell | MOD_MIGHT |
| 0220 | [Decree of Insight](card-operator-reading/0201-0300.md#card-0220) | 洞察箴言 | spell | IGNORE_ABILITY, MOD_MIGHT |
| 0221 | [Decree of Rage](card-operator-reading/0201-0300.md#card-0221) | 暴怒箴言 | spell | RESTRICT, DAMAGE |
| 0222 | [Decree of Strength](card-operator-reading/0201-0300.md#card-0222) | 力量箴言 | spell | REVEAL, CHOOSE, RECYCLE |
| 0223 | [Decree of Unity](card-operator-reading/0201-0300.md#card-0223) | 团结箴言 | spell | KILL |
| 0224 | [Defender of Tomorrow](card-operator-reading/0201-0300.md#card-0224) | 未来守护者 | legend | PAY, EXHAUST, READY |
| 0225 | [Defiant Dance](card-operator-reading/0201-0300.md#card-0225) | 距破之舞 | spell | MOD_MIGHT |
| 0226 | [Defy](card-operator-reading/0201-0300.md#card-0226) | 蔑视 | spell | COUNTER |
| 0227 | [Demacian Diplomat](card-operator-reading/0201-0300.md#card-0227) | 德玛西亚使节 | unit | XP |
| 0228 | [Demacian Illuminators](card-operator-reading/0201-0300.md#card-0228) | 光照者教团 | unit | BUFF |
| 0229 | [Demacian Standard](card-operator-reading/0201-0300.md#card-0229) | 德邦军旗 | gear | MOD_MIGHT, TRANSFER |
| 0230 | [Demon Shade](card-operator-reading/0201-0300.md#card-0230) | 恶魔魅影 | spell | CHOOSE, MOVE, GRANT_KEYWORD |
| 0231 | [Desert’s Call](card-operator-reading/0201-0300.md#card-0231) | 点沙成兵 | spell | CREATE, PLAY, REPEAT |
| 0232 | [Determined Sentry](card-operator-reading/0201-0300.md#card-0232) | 坚定的哨兵 | unit | RESTRICT |
| 0233 | [Detonate](card-operator-reading/0201-0300.md#card-0233) | 印爆术 | spell | KILL, DRAW |
| 0234 | [Detonation Amplifier](card-operator-reading/0201-0300.md#card-0234) | 爆破增幅器 | gear | KILL, DRAW, MOD_TRIGGER |
| 0235 | [Diana, Lunari](card-operator-reading/0201-0300.md#card-0235) | 黛安娜, 皎月化身 | unit | PAY, PREDICT, REVEAL, DRAW |
| 0236 | [Diana, No Longer Human](card-operator-reading/0201-0300.md#card-0236) | 黛安娜, 超脱凡界 | unit | MOD_MIGHT |
| 0237 | [Direwing](card-operator-reading/0201-0300.md#card-0237) | 凶翼 | unit | ENTRY |
| 0238 | [Disarming Rake](card-operator-reading/0201-0300.md#card-0238) | 斩剑浪客 | unit | KILL |
| 0239 | [Disciple of Shen](card-operator-reading/0201-0300.md#card-0239) | 慎的弟子 | unit | GRANT_KEYWORD |
| 0240 | [Discipline](card-operator-reading/0201-0300.md#card-0240) | 训练有素 | spell | MOD_MIGHT, DRAW |
| 0241 | [Disintegrate](card-operator-reading/0201-0300.md#card-0241) | 碎裂之火 | spell | DAMAGE, DRAW, DELAY |
| 0242 | [Disposal Expert](card-operator-reading/0201-0300.md#card-0242) | 处置专家 | unit | ENTRY |
| 0243 | [Disposal Order](card-operator-reading/0201-0300.md#card-0243) | 处置命令 | spell | CHOOSE, RECYCLE, DRAW |
| 0244 | [Divine Judgment](card-operator-reading/0201-0300.md#card-0244) | 圣裁之刻 | spell | CHOOSE, RECYCLE |
| 0245 | [Divining Shells](card-operator-reading/0201-0300.md#card-0245) | 占卜贝壳 | gear | KILL, EXHAUST, MOD_MIGHT |
| 0246 | [Dockside Lock-Up](card-operator-reading/0201-0300.md#card-0246) | 码头囚笼 | gear | BANISH, KILL, PLAY, LINK |
| 0247 | [Dominus](card-operator-reading/0201-0300.md#card-0247) | 终极统治 | spell | SET_MIGHT, GRANT_ABILITY |
| 0248 | [Doran’s Blade](card-operator-reading/0201-0300.md#card-0248) | 多兰之刃 | gear | ATTACH, MOD_MIGHT |
| 0249 | [Doran’s Ring](card-operator-reading/0201-0300.md#card-0249) | 多兰之戒 | gear | ATTACH, MOD_MIGHT, DISCARD, DRAW |
| 0250 | [Doran’s Shield](card-operator-reading/0201-0300.md#card-0250) | 多兰之盾 | gear | ATTACH, MOD_MIGHT, GRANT_KEYWORD |
| 0251 | [Double Trouble](card-operator-reading/0201-0300.md#card-0251) | 龙虎双雄 | spell | LOOK, REVEAL, DRAW, RECYCLE, REPEAT |
| 0252 | [Downstage Dramatics](card-operator-reading/0201-0300.md#card-0252) | 台前作秀 | spell | DRAW, REPEAT |
| 0253 | [Downwell](card-operator-reading/0201-0300.md#card-0253) | 坠渊之流 | spell | TRANSFER |
| 0254 | [Dr. Mundo, Expert](card-operator-reading/0201-0300.md#card-0254) | 蒙多医生, 主治大夫 | unit | MOD_MIGHT, RECYCLE |
| 0255 | [Drag Under](card-operator-reading/0201-0300.md#card-0255) | 流沙陷坑 | spell | MOD_COST, KILL |
| 0256 | [Dragon Form](card-operator-reading/0201-0300.md#card-0256) | 龙之形 | spell | SET_BASE_MIGHT |
| 0257 | [Dragon Roost](card-operator-reading/0201-0300.md#card-0257) | 龙栖峰 | battlefield | PAY, PERMIT, ENTRY |
| 0258 | [Dragonsoul Sage](card-operator-reading/0201-0300.md#card-0258) | 龙魂贤者 | unit | EXHAUST, ADD_RESOURCE |
| 0259 | [Dragon’s Rage](card-operator-reading/0201-0300.md#card-0259) | 猛龙摆尾 | spell | MOVE, DAMAGE, DELAY |
| 0260 | [Drakehound Packmaster](card-operator-reading/0201-0300.md#card-0260) | 龙犬驯兽师 | unit | REVEAL, CHOOSE, BANISH, PLAY, RECYCLE |
| 0261 | [Dramatic Visionary](card-operator-reading/0201-0300.md#card-0261) | 戏精远见家 | unit | PREDICT |
| 0262 | [Draven, Audacious](card-operator-reading/0201-0300.md#card-0262) | 德莱文, 艺高胆大 | unit | SCORE, CHOOSE |
| 0263 | [Draven, Showboat](card-operator-reading/0201-0300.md#card-0263) | 德莱文, 夸耀角斗士 | unit | MOD_MIGHT |
| 0264 | [Draven, Vanquisher](card-operator-reading/0201-0300.md#card-0264) | 德莱文, 血斧飞旋 | unit | CREATE, PLAY, PAY, MOD_MIGHT |
| 0265 | [Dredge Up](card-operator-reading/0201-0300.md#card-0265) | 深水打捞 | spell | DRAW |
| 0266 | [Dropboarder](card-operator-reading/0201-0300.md#card-0266) | 滑板高手 | unit | READY |
| 0267 | [Dune Devourer](card-operator-reading/0201-0300.md#card-0267) | 沙丘吞噬者 | unit | KILL, MOD_COST |
| 0268 | [Dune Drake](card-operator-reading/0201-0300.md#card-0268) | 沙丘亚龙 | unit | MOD_MIGHT |
| 0269 | [Dune Surfer](card-operator-reading/0201-0300.md#card-0269) | 沙丘冲浪者 | unit | IGNORE_ABILITY |
| 0270 | [Dunebreaker](card-operator-reading/0201-0300.md#card-0270) | 穿沙角兽 | unit | ENTRY, DRAW |
| 0271 | [Durand Memorial](card-operator-reading/0201-0300.md#card-0271) | 杜朗纪念碑 | battlefield | GRANT_KEYWORD |
| 0272 | [Dusk Rose Lab](card-operator-reading/0201-0300.md#card-0272) | 暮色玫瑰实验室 | battlefield | KILL, DRAW, IF_DO |
| 0273 | [Eager Apprentice](card-operator-reading/0201-0300.md#card-0273) | 踊跃的学徒 | unit | MOD_COST |
| 0274 | [Eager Drakehound](card-operator-reading/0201-0300.md#card-0274) | 好斗的龙犬 | unit | ENTRY |
| 0275 | [Eclipse](card-operator-reading/0201-0300.md#card-0275) | 月蚀 | spell | MOD_MIGHT, PREDICT |
| 0276 | [Eclipse Dragon](card-operator-reading/0201-0300.md#card-0276) | 蚀影巨龙 | unit | DRAW |
| 0277 | [Eclipse Herald](card-operator-reading/0201-0300.md#card-0277) | 星蚀先锋 | unit | READY, MOD_MIGHT |
| 0278 | [Edge of Night](card-operator-reading/0201-0300.md#card-0278) | 夜之锋刃 | gear | ATTACH, MOD_MIGHT |
| 0279 | [Ekko, Ingenious](card-operator-reading/0201-0300.md#card-0279) | 艾克, 灵光一现 | unit | TRANSFER, PAY |
| 0280 | [Ekko, Recurrent](card-operator-reading/0201-0300.md#card-0280) | 艾克, 溯时洄光 | unit | RECYCLE, READY, IF_DO |
| 0281 | [Ekko, Revolutionary](card-operator-reading/0201-0300.md#card-0281) | 艾克, 逆时而行 | unit | ENTRY, DISCARD, PAY, BANISH, PLAY |
| 0282 | [Elder Dragon](card-operator-reading/0201-0300.md#card-0282) | 远古巨龙 | unit | SET_RULE, DAMAGE |
| 0283 | [Elnuk Herd](card-operator-reading/0201-0300.md#card-0283) | 厄努克牛群 | unit | MOD_MIGHT, RECYCLE |
| 0284 | [Ember Monk](card-operator-reading/0201-0300.md#card-0284) | 余火修士 | unit | MOD_MIGHT |
| 0285 | [Eminent Benefactor](card-operator-reading/0201-0300.md#card-0285) | 显赫金主 | unit | CREATE, PLAY |
| 0286 | [Emperor of the Sands](card-operator-reading/0201-0300.md#card-0286) | 沙漠皇帝 | legend | GRANT_KEYWORD, PAY, EXHAUST, CREATE, PLAY |
| 0287 | [Emperor’s Dais](card-operator-reading/0201-0300.md#card-0287) | 帝王神坛 | battlefield | PAY, TRANSFER, CREATE, PLAY, IF_DO |
| 0288 | [Emperor’s Divide](card-operator-reading/0201-0300.md#card-0288) | 禁军之墙 | spell | MOVE |
| 0289 | [Empowered](card-operator-reading/0201-0300.md#card-0289) | Empowered | other | SET_RULE |
| 0290 | [En Garde](card-operator-reading/0201-0300.md#card-0290) | 决斗架势 | spell | MOD_MIGHT |
| 0291 | [Encore](card-operator-reading/0201-0300.md#card-0291) | 炫音返场 | spell | CHOOSE, DAMAGE, CREATE, PLAY, MOD_MIGHT, LOOK, DRAW, RECYCLE |
| 0292 | [Endless Riches](card-operator-reading/0201-0300.md#card-0292) | 无尽秘藏 | gear | BANISH, BURN, SKIP_PHASE, PERMIT, REPLACE |
| 0293 | [Energy Conduit](card-operator-reading/0201-0300.md#card-0293) | 能量通道 | gear | EXHAUST, ADD_RESOURCE |
| 0294 | [Enthralling Protector](card-operator-reading/0201-0300.md#card-0294) | 惊艳守护者 | unit | XP, BUFF |
| 0295 | [Enthusiastic Promoter](card-operator-reading/0201-0300.md#card-0295) | 热情的播报员 | unit | BUFF |
| 0296 | [Entrenched Boar](card-operator-reading/0201-0300.md#card-0296) | 盘踞野猪 | unit | ENTRY, RESTRICT |
| 0297 | [Ephemeral Ward](card-operator-reading/0201-0300.md#card-0297) | 除灵结界 | gear | MOD_MIGHT, KILL |
| 0298 | [Escaped Grayback](card-operator-reading/0201-0300.md#card-0298) | 脱逃的灰背 | unit | KILL, MOD_MIGHT |
| 0299 | [Esteemed Hierophant](card-operator-reading/0201-0300.md#card-0299) | 圣职尊者 | unit | PREVENT_DAMAGE |
| 0300 | [Evelynn, Consuming](card-operator-reading/0201-0300.md#card-0300) | 伊芙琳, 噬魂蚀骨 | unit | READY, MOD_MIGHT |
| 0301 | [Evelynn, Entrancing](card-operator-reading/0301-0400.md#card-0301) | 伊芙琳, 摄人心魄 | unit | MOVE |
| 0302 | [Evelynn, In Control](card-operator-reading/0301-0400.md#card-0302) | 伊芙琳, 掌握全场 | unit | SCORE |
| 0303 | [Evershade Stalker](card-operator-reading/0301-0400.md#card-0303) | 永黯潜伏者 | unit | DISCARD, DRAW |
| 0304 | [Exemplar of Demacia](card-operator-reading/0301-0400.md#card-0304) | 德玛西亚皇子 | legend | EXHAUST, PAY, MOVE |
| 0305 | [Existential Dread](card-operator-reading/0301-0400.md#card-0305) | 存在焦虑 | spell | STUN, TRANSFER, REPLACE, REPEAT |
| 0306 | [Experimental Hexplate](card-operator-reading/0301-0400.md#card-0306) | 海克斯注力刚壁 | gear | ATTACH, MOD_MIGHT, SET_TAG |
| 0307 | [Explosimian](card-operator-reading/0301-0400.md#card-0307) | 爆破猿 | unit | CREATE, PLAY |
| 0308 | [Eye of the Herald](card-operator-reading/0301-0400.md#card-0308) | 先锋之眼 | gear | ATTACH, CREATE, PLAY |
| 0309 | [Eye of Twilight](card-operator-reading/0301-0400.md#card-0309) | 暮光之眼 | legend | EXHAUST, GRANT_KEYWORD |
| 0310 | [Ezreal, Dashing](card-operator-reading/0301-0400.md#card-0310) | 伊泽瑞尔, 翩然俊朗 | unit | DAMAGE, RESTRICT, PAY, MOVE |
| 0311 | [Ezreal, Prodigy](card-operator-reading/0301-0400.md#card-0311) | 伊泽瑞尔, 奥法逸才 | unit | DISCARD, DRAW, MOD_COST |
| 0312 | [Facebreaker](card-operator-reading/0301-0400.md#card-0312) | 强手裂颅 | spell | STUN |
| 0313 | [Factory Recall](card-operator-reading/0301-0400.md#card-0313) | 紧急召回 | spell | TRANSFER |
| 0314 | [Fading Memories](card-operator-reading/0301-0400.md#card-0314) | 逝水如镜 | spell | GRANT_KEYWORD |
| 0315 | [Fae Dragon](card-operator-reading/0301-0400.md#card-0315) | 仙灵龙 | unit | BUFF, CREATE, PLAY |
| 0316 | [Fae Porter](card-operator-reading/0301-0400.md#card-0316) | 大力仙灵 | unit | PAY, MOVE |
| 0317 | [Faithful Manufactor](card-operator-reading/0301-0400.md#card-0317) | 忠实的工坊主 | unit | CREATE, PLAY |
| 0318 | [Fallen Feline](card-operator-reading/0301-0400.md#card-0318) | 坠落猫咪 | unit | NAME, RESTRICT, LINK |
| 0319 | [Falling Comet](card-operator-reading/0301-0400.md#card-0319) | 彗星坠击 | spell | DAMAGE |
| 0320 | [Falling Star](card-operator-reading/0301-0400.md#card-0320) | 星落 | spell | DAMAGE, REPEAT |
| 0321 | [Fanfare](card-operator-reading/0301-0400.md#card-0321) | 大喇叭 | spell | DELAY, DRAW |
| 0322 | [Fate Weaver](card-operator-reading/0301-0400.md#card-0322) | 命运编织者 | unit | LOOK, REVEAL, DRAW, RECYCLE |
| 0323 | [Feral Strength](card-operator-reading/0301-0400.md#card-0323) | 蛮荒之力 | spell | MOD_MIGHT, REPEAT |
| 0324 | [Ferrous Forerunner](card-operator-reading/0301-0400.md#card-0324) | 铁甲先锋 | unit | CREATE, PLAY |
| 0325 | [Field Musicians](card-operator-reading/0301-0400.md#card-0325) | 战地乐团 | unit | MOD_MIGHT |
| 0326 | [Fight or Flight](card-operator-reading/0301-0400.md#card-0326) | 战或逃 | spell | MOVE |
| 0327 | [Final Spark](card-operator-reading/0301-0400.md#card-0327) | 终极闪光 | spell | DAMAGE |
| 0328 | [Find Your Center](card-operator-reading/0301-0400.md#card-0328) | 御衡守念 | spell | MOD_COST, DRAW, CHANNEL |
| 0329 | [Fiora, Peerless](card-operator-reading/0301-0400.md#card-0329) | 菲奥娜, 苦心孤诣 | unit | SET_MIGHT |
| 0330 | [Fiora, Victorious](card-operator-reading/0301-0400.md#card-0330) | 菲奥娜, 所向披靡 | unit | GRANT_KEYWORD |
| 0331 | [Fiora, Worthy](card-operator-reading/0301-0400.md#card-0331) | 菲奥娜, 无上统御 | unit | PAY, READY |
| 0332 | [Fire Below the Mountain](card-operator-reading/0301-0400.md#card-0332) | 山隐之焰 | legend | EXHAUST, ADD_RESOURCE, RESTRICT_RESOURCE |
| 0333 | [Firebrand Raider](card-operator-reading/0301-0400.md#card-0333) | 焰烙劫掠者 | unit | ENTRY, READY, RESTRICT |
| 0334 | [Firelights’ Hideout](card-operator-reading/0301-0400.md#card-0334) | 野火帮秘密基地 | battlefield | DELAY, GRANT_KEYWORD |
| 0335 | [Firestorm](card-operator-reading/0301-0400.md#card-0335) | 烈火风暴 | spell | DAMAGE |
| 0336 | [First Mate](card-operator-reading/0301-0400.md#card-0336) | 大副 | unit | READY |
| 0337 | [Fizz, Trickster](card-operator-reading/0301-0400.md#card-0337) | 菲兹, 捣蛋鬼 | unit | PLAY, RECYCLE |
| 0338 | [Flame Chompers](card-operator-reading/0301-0400.md#card-0338) | 嚼火者手雷 | unit | PAY, PLAY |
| 0339 | [Flash](card-operator-reading/0301-0400.md#card-0339) | 闪现 | spell | MOVE |
| 0340 | [Flurry of Blades](card-operator-reading/0301-0400.md#card-0340) | 剑刃飓风 | spell | DAMAGE |
| 0341 | [Flurry of Feathers](card-operator-reading/0301-0400.md#card-0341) | 羽毛旋风 | spell | CHOOSE, COUNTER, CREATE, PLAY |
| 0342 | [For Demacia!](card-operator-reading/0301-0400.md#card-0342) | 为了德玛西亚！ | spell | GRANT_KEYWORD |
| 0343 | [Forbidden Technique](card-operator-reading/0301-0400.md#card-0343) | 禁忌秘术 | spell | READY, PLAY, BANISH |
| 0344 | [Forbidding Waste](card-operator-reading/0301-0400.md#card-0344) | 禁忌荒原 | battlefield | MOD_MIGHT |
| 0345 | [Forecaster](card-operator-reading/0301-0400.md#card-0345) | 先见机甲 | unit | GRANT_KEYWORD |
| 0346 | [Forge of the Fluft](card-operator-reading/0301-0400.md#card-0346) | 魄罗熔炉 | battlefield | GRANT_ABILITY, ATTACH |
| 0347 | [Forge of the Future](card-operator-reading/0301-0400.md#card-0347) | 未来熔炉 | gear | CREATE, PLAY, KILL, RECYCLE |
| 0348 | [Forgefire Cape](card-operator-reading/0301-0400.md#card-0348) | 炉火斗篷 | gear | ATTACH, MOD_MIGHT, DAMAGE |
| 0349 | [Forgotten Library](card-operator-reading/0301-0400.md#card-0349) | 失落书库 | battlefield | PREDICT |
| 0350 | [Forgotten Monument](card-operator-reading/0301-0400.md#card-0350) | 遗忘丰碑 | battlefield | RESTRICT |
| 0351 | [Forgotten Relic](card-operator-reading/0301-0400.md#card-0351) | 遗落圣物 | gear | BURN, MOD_MIGHT, DELAY |
| 0352 | [Forgotten Signpost](card-operator-reading/0301-0400.md#card-0352) | 被遗忘的路标 | gear | EXHAUST, MOVE, LINK |
| 0353 | [Forsaken Baccai](card-operator-reading/0301-0400.md#card-0353) | 巴凯遗民 | unit | MOD_MIGHT |
| 0354 | [Fortified Position](card-operator-reading/0301-0400.md#card-0354) | 强化阵地 | battlefield | GRANT_KEYWORD |
| 0355 | [Fox-Fire](card-operator-reading/0301-0400.md#card-0355) | 妖异狐火 | spell | KILL, CHOOSE |
| 0356 | [Fresh Beans](card-operator-reading/0301-0400.md#card-0356) | 魔法鲜豆 | gear | EXHAUST, DRAW |
| 0357 | [Fretful Feline](card-operator-reading/0301-0400.md#card-0357) | 焦躁的猫咪 | unit | MOD_MIGHT |
| 0358 | [Friendship](card-operator-reading/0301-0400.md#card-0358) | 动物之友 | spell | MOD_MIGHT |
| 0359 | [Frigid Jewel](card-operator-reading/0301-0400.md#card-0359) | 冰封宝石 | gear | MOD_MIGHT |
| 0360 | [Frigid Touch](card-operator-reading/0301-0400.md#card-0360) | 封冻 | spell | MOD_MIGHT, REPEAT |
| 0361 | [Frisky Hunter](card-operator-reading/0301-0400.md#card-0361) | 调皮猎手 | unit | CREATE, PLAY |
| 0362 | [Frostcoat Cub](card-operator-reading/0301-0400.md#card-0362) | 霜衣幼崽 | unit | PAY, MOD_MIGHT |
| 0363 | [Frostcoat Mother](card-operator-reading/0301-0400.md#card-0363) | 霜衣狼母 | unit | MOD_COST, MOD_MIGHT |
| 0364 | [Frozen Fortress](card-operator-reading/0301-0400.md#card-0364) | 冰霜要塞 | battlefield | DAMAGE |
| 0365 | [Fury Rune](card-operator-reading/0301-0400.md#card-0365) | 炽烈符文 | rune | ADD_RESOURCE, PAY, EXHAUST, RECYCLE |
| 0366 | [Galio, Indefatigable](card-operator-reading/0301-0400.md#card-0366) | 加里奥, 不屈卫士 | unit | RESTRICT |
| 0367 | [Gangplank, Naval](card-operator-reading/0301-0400.md#card-0367) | 普朗克, 海上霸主 | unit | REPLACE, MOD_MIGHT |
| 0368 | [Garbage Grabber](card-operator-reading/0301-0400.md#card-0368) | 拾荒小能手 | gear | RECYCLE, PAY, EXHAUST, DRAW |
| 0369 | [Gardens of Becoming](card-operator-reading/0301-0400.md#card-0369) | 蜕变花园 | battlefield | GRANT_ABILITY, EXHAUST, XP |
| 0370 | [Garen, Commander](card-operator-reading/0301-0400.md#card-0370) | 盖伦, 剑尉长 | unit | MOD_MIGHT |
| 0371 | [Garen, Rugged](card-operator-reading/0301-0400.md#card-0371) | 盖伦, 身经百战 | unit | MOD_MIGHT |
| 0372 | [Gearhead](card-operator-reading/0301-0400.md#card-0372) | 机械迷 | unit | MOD_MIGHT |
| 0373 | [Gem Jammer](card-operator-reading/0301-0400.md#card-0373) | 晶能阻断器 | unit | GRANT_KEYWORD |
| 0374 | [Gemcraft Seer](card-operator-reading/0301-0400.md#card-0374) | 宝石真知者 | unit | GRANT_KEYWORD |
| 0375 | [Gemhand Hunter](card-operator-reading/0301-0400.md#card-0375) | 晶手猎人 | unit | MOD_MIGHT |
| 0376 | [Gentle Gemdragon](card-operator-reading/0301-0400.md#card-0376) | 温驯的宝石龙 | unit | READY |
| 0377 | [Gentlemen’s Duel](card-operator-reading/0301-0400.md#card-0377) | 绅士决斗 | spell | MOD_MIGHT, DAMAGE |
| 0378 | [Get Excited!](card-operator-reading/0301-0400.md#card-0378) | 罪恶快感 | spell | DISCARD, DAMAGE, LINK |
| 0379 | [Glasc Mixologist](card-operator-reading/0301-0400.md#card-0379) | 戈拉斯克调酒师 | unit | PLAY |
| 0380 | [Gloomist](card-operator-reading/0301-0400.md#card-0380) | 愁云使者 | legend | EXHAUST, DRAW |
| 0381 | [Glorious Executioner](card-operator-reading/0301-0400.md#card-0381) | 荣耀行刑官 | legend | DRAW |
| 0382 | [Glowstone](card-operator-reading/0301-0400.md#card-0382) | 发光石 | gear | DISEMPOWER, EXHAUST, CONTROL, RECALL, KILL, DAMAGE |
| 0383 | [Gold](card-operator-reading/0301-0400.md#card-0383) | 金币 | gear | KILL, EXHAUST, ADD_RESOURCE |
| 0384 | [Grand Duelist](card-operator-reading/0301-0400.md#card-0384) | 无双剑姬 | legend | EXHAUST, CHANNEL |
| 0385 | [Grand Strategem](card-operator-reading/0301-0400.md#card-0385) | 宏伟战略 | spell | MOD_MIGHT |
| 0386 | [Grandmaster at Arms](card-operator-reading/0301-0400.md#card-0386) | 武器大师 | legend | PAY, EXHAUST, ATTACH |
| 0387 | [Graves, Blasting Through](card-operator-reading/0301-0400.md#card-0387) | 格雷福斯, 强行突破 | unit | DAMAGE, RESTRICT |
| 0388 | [Gravity Field](card-operator-reading/0301-0400.md#card-0388) | 重力场 | gear | MOD_COST, DRAW |
| 0389 | [Green Father](card-operator-reading/0301-0400.md#card-0389) | 翠神 | legend | EXHAUST, REPLACE_BATTLEFIELD |
| 0390 | [Grim Apothecary](card-operator-reading/0301-0400.md#card-0390) | 阴森药剂师 | unit | TRANSFER |
| 0391 | [Grim Resolve](card-operator-reading/0301-0400.md#card-0391) | 视死如归 | spell | MOD_MIGHT, DELAY, XP |
| 0392 | [Grove of the God-Willow](card-operator-reading/0301-0400.md#card-0392) | 帝柳之林 | battlefield | DRAW |
| 0393 | [Grumpy Rockbear](card-operator-reading/0301-0400.md#card-0393) | 凶暴的岩熊 | unit | MOD_COST, GRANT_KEYWORD |
| 0394 | [Guardian Angel](card-operator-reading/0301-0400.md#card-0394) | 守护天使 | gear | ATTACH, MOD_MIGHT, REPLACE, KILL, HEAL, EXHAUST, RECALL |
| 0395 | [Guardian of the Passage](card-operator-reading/0301-0400.md#card-0395) | 幽径守卫 | unit | TRANSFER |
| 0396 | [Guards!](card-operator-reading/0301-0400.md#card-0396) | 护驾！ | spell | CREATE, PLAY, DELAY, PAY, READY |
| 0397 | [Guerilla Warfare](card-operator-reading/0301-0400.md#card-0397) | 游击战 | spell | TRANSFER, MOD_COST |
| 0398 | [Gust](card-operator-reading/0301-0400.md#card-0398) | 罡风 | spell | TRANSFER |
| 0399 | [Gust Monk](card-operator-reading/0301-0400.md#card-0399) | 劲风修士 | unit | PAY, BANISH, GRANT_KEYWORD |
| 0400 | [Gustwalker](card-operator-reading/0301-0400.md#card-0400) | 风行狐 | unit | MOD_MIGHT, GRANT_KEYWORD |
| 0401 | [Gutter Guardian](card-operator-reading/0401-0500.md#card-0401) | 暗巷守护者 | unit | SHOW_OFF, ADD_RESOURCE |
| 0402 | [Gutter Palace](card-operator-reading/0401-0500.md#card-0402) | 倾颓宫殿 | gear | WIN, DISCARD, EXHAUST, CREATE, PLAY |
| 0403 | [Guttural Roar](card-operator-reading/0401-0500.md#card-0403) | 深沉咆哮 | spell | MOD_MIGHT, REPLACE |
| 0404 | [Hall of Legends](card-operator-reading/0401-0500.md#card-0404) | 传奇殿堂 | battlefield | PAY, READY |
| 0405 | [Hallowed Tomb](card-operator-reading/0401-0500.md#card-0405) | 圣化之墓 | battlefield | TRANSFER |
| 0406 | [Hand Hammer](card-operator-reading/0401-0500.md#card-0406) | 杠锤 | gear | ATTACH, MOD_MIGHT |
| 0407 | [Hand of Noxus](card-operator-reading/0401-0500.md#card-0407) | 诺克萨斯之手 | legend | EXHAUST, ADD_RESOURCE |
| 0408 | [Hard Bargain](card-operator-reading/0401-0500.md#card-0408) | 强买强卖 | spell | COUNTER, PAY, CHOOSE, REPEAT |
| 0409 | [Harnessed Dragon](card-operator-reading/0401-0500.md#card-0409) | 龙骑兵 | unit | KILL |
| 0410 | [Harpoon Squad](card-operator-reading/0401-0500.md#card-0410) | 猎海小队 | unit | MOD_MIGHT |
| 0411 | [Heart of Dark Ice](card-operator-reading/0401-0500.md#card-0411) | 玄冰之心 | gear | EXHAUST, MOD_MIGHT |
| 0412 | [Heart of the Tempest](card-operator-reading/0401-0500.md#card-0412) | 狂暴之心 | legend | EMPOWER, DISEMPOWER, EXHAUST, GRANT_KEYWORD |
| 0413 | [Heartening Soul](card-operator-reading/0401-0500.md#card-0413) | 鼓舞之魂 | unit | READY, GRANT_ABILITY |
| 0414 | [Heedless Resurrection](card-operator-reading/0401-0500.md#card-0414) | 残酷复活 | spell | KILL, PAY, PLAY |
| 0415 | [Heimerdinger, Academy Instructor](card-operator-reading/0401-0500.md#card-0415) | 黑默丁格, 学院导师 | unit | REPLACE, CREATE, PLAY |
| 0416 | [Heimerdinger, Inventor](card-operator-reading/0401-0500.md#card-0416) | 黑默丁格, 博学家 | unit | COPY_ABILITY |
| 0417 | [Heisho, Shell of the World](card-operator-reading/0401-0500.md#card-0417) | 世界之壳 亥宿 | battlefield | IGNORE_ABILITY |
| 0418 | [Helm of Suppression](card-operator-reading/0401-0500.md#card-0418) | 抑制之盔 | gear | MOD_COST, REPLACE |
| 0419 | [Herald of Scales](card-operator-reading/0401-0500.md#card-0419) | 唤龙使者 | unit | MOD_COST |
| 0420 | [Herald of Spring](card-operator-reading/0401-0500.md#card-0420) | 暖春之使 | unit | XP |
| 0421 | [Herald of the Arcane](card-operator-reading/0401-0500.md#card-0421) | 奥术先驱 | legend | PAY, EXHAUST, CREATE, PLAY |
| 0422 | [Herald of the Emperor](card-operator-reading/0401-0500.md#card-0422) | 帝皇令使 | unit | SET_BASE_MIGHT |
| 0423 | [Here to Help](card-operator-reading/0401-0500.md#card-0423) | 前来相助 | spell | PLAY, MOD_COST |
| 0424 | [Heroic Charge](card-operator-reading/0401-0500.md#card-0424) | 英勇冲锋 | spell | MOD_MIGHT, STUN |
| 0425 | [Hexdrinker](card-operator-reading/0401-0500.md#card-0425) | 海克斯饮魔刀 | gear | ATTACH, MOD_MIGHT, GRANT_KEYWORD |
| 0426 | [Hexplosive Minefield](card-operator-reading/0401-0500.md#card-0426) | 海克斯爆破雷区 | spell | KILL, DELAY, CREATE, PLAY |
| 0427 | [Hexplosives Expert](card-operator-reading/0401-0500.md#card-0427) | 爆破鬼才 | legend | PAY, EXHAUST, CREATE, PLAY |
| 0428 | [Hextech Anomaly](card-operator-reading/0401-0500.md#card-0428) | 海克斯异常体 | gear | PAY, EXHAUST, ADD_RESOURCE |
| 0429 | [Hextech Disc](card-operator-reading/0401-0500.md#card-0429) | 海克斯圆盘 | gear | DISEMPOWER, PAY, EXHAUST, CREATE, PLAY |
| 0430 | [Hextech Formula](card-operator-reading/0401-0500.md#card-0430) | 海克斯方程式 | gear | ENTRY, EXHAUST, EMPOWER |
| 0431 | [Hextech Gauntlets](card-operator-reading/0401-0500.md#card-0431) | 海克斯科技护手 | gear | ATTACH, MOD_COST, MOD_MIGHT, DRAW |
| 0432 | [Hextech Ray](card-operator-reading/0401-0500.md#card-0432) | 海克斯射线 | spell | DAMAGE |
| 0433 | [Hidden Blade](card-operator-reading/0401-0500.md#card-0433) | 暗刃 | spell | KILL, DRAW |
| 0434 | [High Note](card-operator-reading/0401-0500.md#card-0434) | 清籁穿云 | spell | MOD_MIGHT |
| 0435 | [Highlander](card-operator-reading/0401-0500.md#card-0435) | 高原血统 | spell | REPLACE, HEAL, EXHAUST, RECALL |
| 0436 | [Hold ’Em](card-operator-reading/0401-0500.md#card-0436) | 先打再跟 | spell | MOD_COST, MOD_MIGHT |
| 0437 | [Honest Broker](card-operator-reading/0401-0500.md#card-0437) | 诚实掮客 | unit | CREATE, PLAY |
| 0438 | [Honeyfruit](card-operator-reading/0401-0500.md#card-0438) | 蜜糖果实 | gear | ENTRY, EXHAUST, ADD_RESOURCE |
| 0439 | [Horns of the Dragon](card-operator-reading/0401-0500.md#card-0439) | 龙角勇士 | unit | SET_RULE |
| 0440 | [Hostile Takeover](card-operator-reading/0401-0500.md#card-0440) | 恶意收购 | spell | CONTROL, READY, DELAY, RECALL |
| 0441 | [Hungry Wolf](card-operator-reading/0401-0500.md#card-0441) | 冰原饿狼 | unit | PAY, READY, MOD_MIGHT |
| 0442 | [Hunker Down](card-operator-reading/0401-0500.md#card-0442) | 气敛神聚 | spell | READY, RESTRICT, DRAW |
| 0443 | [Hunters’ Circle](card-operator-reading/0401-0500.md#card-0443) | 猎风广场 | battlefield | MOD_COST |
| 0444 | [Hunter’s Machete](card-operator-reading/0401-0500.md#card-0444) | 猎人的宽刃刀 | gear | ATTACH, MOD_MIGHT, GRANT_KEYWORD |
| 0445 | [Hunting Blind](card-operator-reading/0401-0500.md#card-0445) | 狩猎掩体 | gear | MOVE, GRANT_KEYWORD |
| 0446 | [Hunting Dog](card-operator-reading/0401-0500.md#card-0446) | 狩猎犬 | unit | CREATE, PLAY |
| 0447 | [Hush](card-operator-reading/0401-0500.md#card-0447) | 缄默术 | spell | COUNTER |
| 0448 | [Hwei, Brooding Painter](card-operator-reading/0401-0500.md#card-0448) | 彗, 焚心绘华 | unit | DRAW, DISCARD, READY, MOD_MIGHT |
| 0449 | [Iascylla](card-operator-reading/0401-0500.md#card-0449) | 娅希拉 | unit | DELAY, MOVE |
| 0450 | [Icathian Rain](card-operator-reading/0401-0500.md#card-0450) | 艾卡西亚暴雨 | spell | DAMAGE, REPEAT |
| 0451 | [Icevale Archer](card-operator-reading/0401-0500.md#card-0451) | 冰谷弓箭手 | unit | PAY, MOD_MIGHT |
| 0452 | [Illaoi, Prophet of the Great Kraken](card-operator-reading/0401-0500.md#card-0452) | 俄洛伊, 大海兽先知 | unit | CREATE, PLAY, MOD_MIGHT |
| 0453 | [Immortal Phoenix](card-operator-reading/0401-0500.md#card-0453) | 不朽凤凰 | unit | PLAY |
| 0454 | [Imperial Decree](card-operator-reading/0401-0500.md#card-0454) | 帝国谕令 | spell | DELAY, KILL |
| 0455 | [Imposing Challenger](card-operator-reading/0401-0500.md#card-0455) | 气势逼人的挑战者 | unit | MOVE |
| 0456 | [Improvised Projectile](card-operator-reading/0401-0500.md#card-0456) | 随手投掷 | spell | DAMAGE |
| 0457 | [Incinerate](card-operator-reading/0401-0500.md#card-0457) | 焚烧 | spell | DAMAGE |
| 0458 | [Incorrigible Construct](card-operator-reading/0401-0500.md#card-0458) | 冥顽构装体 | unit | SHOW_OFF, ENTRY |
| 0459 | [Industrious Mechsmith](card-operator-reading/0401-0500.md#card-0459) | 勤勉的机械匠 | unit | CREATE, PLAY |
| 0460 | [Inferna](card-operator-reading/0401-0500.md#card-0460) | 伊焚娜 | unit | PERMIT, MOD_MIGHT |
| 0461 | [Insightful Investigator](card-operator-reading/0401-0500.md#card-0461) | 缜密的调查员 | unit | REVEAL, XP, CHOOSE, DISCARD, DRAW |
| 0462 | [Invert Timelines](card-operator-reading/0401-0500.md#card-0462) | 反转时间线 | spell | DISCARD, DRAW |
| 0463 | [Invigorating Bloom](card-operator-reading/0401-0500.md#card-0463) | 醒神花 | gear | MOD_MIGHT, EXHAUST, DRAW |
| 0464 | [Inviolus Vox](card-operator-reading/0401-0500.md#card-0464) | 天声玄龙 | unit | MOD_MIGHT |
| 0465 | [Irelia, Fervent](card-operator-reading/0401-0500.md#card-0465) | 艾瑞莉娅, 虔心承志 | unit | MOD_MIGHT |
| 0466 | [Irelia, Graceful](card-operator-reading/0401-0500.md#card-0466) | 艾瑞莉娅, 绝世风华 | unit | MOD_COST |
| 0467 | [Iridescent Avian](card-operator-reading/0401-0500.md#card-0467) | 幻彩飞禽 | unit | EXHAUST, BUFF, MOD_MIGHT, REPLACE |
| 0468 | [Iron Ballista](card-operator-reading/0401-0500.md#card-0468) | 钢铁弩炮 | gear | ENTRY, EXHAUST, DAMAGE |
| 0469 | [Iron Revenant](card-operator-reading/0401-0500.md#card-0469) | 铁铠冥魂 | legend | BANISH, EXHAUST, ADD_RESOURCE, RESTRICT_RESOURCE |
| 0470 | [Irresistible Faefolk](card-operator-reading/0401-0500.md#card-0470) | 诱人仙灵 | unit | MOVE |
| 0471 | [Isolate](card-operator-reading/0401-0500.md#card-0471) | 隔绝 | spell | MOVE, DRAW |
| 0472 | [Iterative Design](card-operator-reading/0401-0500.md#card-0472) | 迭代式设计 | spell | CREATE, PLAY |
| 0473 | [Ivern, Friend to All](card-operator-reading/0401-0500.md#card-0473) | 艾翁, 万物之友 | unit | NAME, SET_TAG, SCORE |
| 0474 | [Ivern, Nurturer](card-operator-reading/0401-0500.md#card-0474) | 艾翁, 自然恩赐 | unit | LOOK, REVEAL, DRAW, RECYCLE, BUFF, DELAY |
| 0475 | [Jae Medarda](card-operator-reading/0401-0500.md#card-0475) | 贾尔·米达尔达 | unit | DRAW |
| 0476 | [Jagged Cutlass](card-operator-reading/0401-0500.md#card-0476) | 锯齿弯刀 | gear | ATTACH, MOD_MIGHT, RESTRICT |
| 0477 | [Janna, Savior](card-operator-reading/0401-0500.md#card-0477) | 迦娜, 救世之灵 | unit | HEAL, MOVE |
| 0478 | [Jarvan IV, Martial Paragon](card-operator-reading/0401-0500.md#card-0478) | 嘉文四世, 天赋将才 | unit | GRANT_KEYWORD, CHANNEL |
| 0479 | [Jarvan IV, Royal Heir](card-operator-reading/0401-0500.md#card-0479) | 嘉文四世, 冕武天骄 | unit | MOVE |
| 0480 | [Jaull-Fish](card-operator-reading/0401-0500.md#card-0480) | 琢珥鱼 | unit | MOD_COST |
| 0481 | [Jax, Unmatched](card-operator-reading/0401-0500.md#card-0481) | 贾克斯, 万般皆武 | unit | GRANT_KEYWORD |
| 0482 | [Jax, Unrelenting](card-operator-reading/0401-0500.md#card-0482) | 贾克斯, 无情攻势 | unit | PAY, DRAW |
| 0483 | [Jayce, Brilliant Inventor](card-operator-reading/0401-0500.md#card-0483) | 杰斯, 进步先锋 | unit | READY |
| 0484 | [Jayce, Hammer in Hand](card-operator-reading/0401-0500.md#card-0484) | 杰斯, 举锤待发 | unit | CHOOSE, GRANT_KEYWORD |
| 0485 | [Jayce, Man of Progress](card-operator-reading/0401-0500.md#card-0485) | 杰斯, 推陈出新 | unit | KILL, PERMIT, PLAY, MOD_COST |
| 0486 | [Jeweled Colossus](card-operator-reading/0401-0500.md#card-0486) | 宝石巨像 | unit | PREDICT, MOD_MIGHT |
| 0487 | [Jhin, Meticulous Killer](card-operator-reading/0401-0500.md#card-0487) | 烬, 匠心索命 | unit | MOD_COST |
| 0488 | [Jhin, Murderous Artist](card-operator-reading/0401-0500.md#card-0488) | 烬, 致命艺术 | unit | ADD_RESOURCE |
| 0489 | [Jinx, Demolitionist](card-operator-reading/0401-0500.md#card-0489) | 金克丝, 爆破狂人 | unit | DISCARD |
| 0490 | [Jinx, Rebel](card-operator-reading/0401-0500.md#card-0490) | 金克丝, 反抗者 | unit | READY, MOD_MIGHT |
| 0491 | [Kadregrin the Infernal](card-operator-reading/0401-0500.md#card-0491) | 邪焰巨龙 卡德雷格林 | unit | DRAW |
| 0492 | [Kai’Sa, Evolutionary](card-operator-reading/0401-0500.md#card-0492) | 卡莎, 蜕变者 | unit | PLAY, RECYCLE |
| 0493 | [Kai’Sa, Rebel](card-operator-reading/0401-0500.md#card-0493) | 卡莎, 逆天改命 | unit | GRANT_KEYWORD |
| 0494 | [Kai’Sa, Survivor](card-operator-reading/0401-0500.md#card-0494) | 卡莎, 九死一生 | unit | DRAW |
| 0495 | [Karma, Channeler](card-operator-reading/0401-0500.md#card-0495) | 卡尔玛, 圣灵之媒 | unit | BUFF |
| 0496 | [Karthus, Eternal](card-operator-reading/0401-0500.md#card-0496) | 卡尔萨斯, 永恒颂葬 | unit | MOD_TRIGGER |
| 0497 | [Katarina, Reckless](card-operator-reading/0401-0500.md#card-0497) | 卡特琳娜, 暗里藏刀 | unit | READY, DAMAGE |
| 0498 | [Kato the Arm](card-operator-reading/0401-0500.md#card-0498) | 巨腕加藤 | unit | GRANT_KEYWORD, MOD_MIGHT |
| 0499 | [Kayle, Justified](card-operator-reading/0401-0500.md#card-0499) | 凯尔, 正义天降 | unit | SET_RULE, MOD_MIGHT, GRANT_KEYWORD |
| 0500 | [Kayn, Unleashed](card-operator-reading/0401-0500.md#card-0500) | 凯隐, 巨镰奔扬 | unit | PREVENT_DAMAGE |
| 0501 | [Keeper of Law](card-operator-reading/0501-0600.md#card-0501) | 律法守护者 | unit | MOD_COST |
| 0502 | [Keeper of Masks](card-operator-reading/0501-0600.md#card-0502) | 赐面守侍 | unit | CREATE, PLAY, COPY, DELAY |
| 0503 | [Keeper of the Hammer](card-operator-reading/0501-0600.md#card-0503) | 圣锤之毅 | legend | XP, EXHAUST, DRAW |
| 0504 | [Keeper’s Verdict](card-operator-reading/0501-0600.md#card-0504) | 持卫的裁决 | spell | TRANSFER, CHOOSE |
| 0505 | [Kennen, Keeper of Balance](card-operator-reading/0501-0600.md#card-0505) | 凯南, 御衡之心 | unit | PAY, STUN, MOD_MIGHT |
| 0506 | [Kennen, Storm of Shuriken](card-operator-reading/0501-0600.md#card-0506) | 凯南, 万雷倾泻 | unit | BURN, GRANT_KEYWORD |
| 0507 | [Kharox](card-operator-reading/0501-0600.md#card-0507) | 卡洛克斯 | unit | CHOOSE, BURN, PLAY, DELAY |
| 0508 | [Kha’Zix, Evolving Hunter](card-operator-reading/0501-0600.md#card-0508) | 卡兹克, 进化猎手 | unit | XP, DAMAGE |
| 0509 | [Kha’Zix, Mutating Horror](card-operator-reading/0501-0600.md#card-0509) | 卡兹克, 恐怖畸变 | unit | MOD_MIGHT, XP |
| 0510 | [Ki Barrier](card-operator-reading/0501-0600.md#card-0510) | 忍法！气合盾 | spell | PREVENT_DAMAGE |
| 0511 | [Ki Burst](card-operator-reading/0501-0600.md#card-0511) | 震魂怒吼 | spell | EXHAUST, PAY, STUN |
| 0512 | [King’s Edict](card-operator-reading/0501-0600.md#card-0512) | 国王诏令 | spell | CHOOSE, ORDER, KILL |
| 0513 | [Kinkou Initiate](card-operator-reading/0501-0600.md#card-0513) | 均衡门徒 | unit | DRAW |
| 0514 | [Kinkou Lifeblade](card-operator-reading/0501-0600.md#card-0514) | 均衡渡命人 | unit | MOD_MIGHT, GRANT_KEYWORD |
| 0515 | [Kinkou Monk](card-operator-reading/0501-0600.md#card-0515) | 均衡僧侣 | unit | BUFF |
| 0516 | [Kinkou Temple](card-operator-reading/0501-0600.md#card-0516) | 均衡寺院 | battlefield | MOD_MIGHT |
| 0517 | [Kog’Maw, Caustic](card-operator-reading/0501-0600.md#card-0517) | 克格莫, 腐蚀巨口 | unit | DAMAGE |
| 0518 | [Kraken Hunter](card-operator-reading/0501-0600.md#card-0518) | 海妖猎手 | unit | SPEND_BUFF, MOD_COST |
| 0519 | [K’Sante, Courageous](card-operator-reading/0501-0600.md#card-0519) | 奎桑提, 骄勇无敌 | unit | CHANNEL |
| 0520 | [K’Sante, Dauntless](card-operator-reading/0501-0600.md#card-0520) | 奎桑提, 傲然无畏 | unit | MOD_KEYWORD |
| 0521 | [Lacerate](card-operator-reading/0501-0600.md#card-0521) | 血戮 | spell | DISEMPOWER, KILL |
| 0522 | [Lady of Clockwork](card-operator-reading/0501-0600.md#card-0522) | 发条魔灵 | legend | PAY, SET_TYPE, SET_BASE_MIGHT, LINK |
| 0523 | [Lady of Luminosity, Starter](card-operator-reading/0501-0600.md#card-0523) | 光辉女郎, 入门 | legend | DRAW |
| 0524 | [Last Breath](card-operator-reading/0501-0600.md#card-0524) | 狂风绝息斩 | spell | READY, DAMAGE |
| 0525 | [Last Caress](card-operator-reading/0501-0600.md#card-0525) | 最终抚慰 | spell | PERMIT, DELAY, BUFF |
| 0526 | [Last Rites](card-operator-reading/0501-0600.md#card-0526) | 临终仪式 | gear | ATTACH, MOD_MIGHT, RECYCLE, PLAY |
| 0527 | [Last Stand](card-operator-reading/0501-0600.md#card-0527) | 背水一战 | spell | SET_MIGHT, GRANT_KEYWORD |
| 0528 | [Laurent Bladekeeper](card-operator-reading/0501-0600.md#card-0528) | 劳伦特护刃者 | unit | PERMIT |
| 0529 | [Laurent Duelist](card-operator-reading/0501-0600.md#card-0529) | 劳伦特剑使 | unit | MOD_MIGHT |
| 0530 | [LeBlanc, Everywhere at Once](card-operator-reading/0501-0600.md#card-0530) | 乐芙兰, 万象归宗 | unit | MOD_TRIGGER |
| 0531 | [LeBlanc, Fragmented](card-operator-reading/0501-0600.md#card-0531) | 乐芙兰, 残影之殇 | unit | DRAW, REPLACE |
| 0532 | [Lecturing Yordle](card-operator-reading/0501-0600.md#card-0532) | 约德尔教官 | unit | DRAW |
| 0533 | [Lee Sin, Ascetic](card-operator-reading/0501-0600.md#card-0533) | 李青, 苦修者 | unit | EXHAUST, BUFF, SET_RULE |
| 0534 | [Lee Sin, Centered](card-operator-reading/0501-0600.md#card-0534) | 李青, 不怒自威 | unit | MOD_MIGHT |
| 0535 | [Legion Marauder](card-operator-reading/0501-0600.md#card-0535) | 军团掠阵兵 | unit | PAY, MOD_MIGHT |
| 0536 | [Legion Quartermaster](card-operator-reading/0501-0600.md#card-0536) | 军团军需官 | unit | TRANSFER, PAY |
| 0537 | [Legion Rearguard](card-operator-reading/0501-0600.md#card-0537) | 军团后卫 | unit | PAY, ENTRY |
| 0538 | [Leona, Determined](card-operator-reading/0501-0600.md#card-0538) | 蕾欧娜, 炽诚者 | unit | STUN |
| 0539 | [Leona, Zealot](card-operator-reading/0501-0600.md#card-0539) | 蕾欧娜, 献身者 | unit | ENTRY, MOD_MIGHT |
| 0540 | [Life from Stone](card-operator-reading/0501-0600.md#card-0540) | 破厄新生 | spell | EXHAUST, PAY, DRAW, CHANNEL |
| 0541 | [Lightning Rush](card-operator-reading/0501-0600.md#card-0541) | 奥义！雷铠 | spell | LOOK, DRAW, TRANSFER |
| 0542 | [Lillia, Fae Fawn](card-operator-reading/0501-0600.md#card-0542) | 莉莉娅, 仙灵小鹿 | unit | CREATE, PLAY |
| 0543 | [Lillia, Protector of Dreams](card-operator-reading/0501-0600.md#card-0543) | 莉莉娅, 梦境守护者 | unit | MOD_MIGHT, GRANT_KEYWORD |
| 0544 | [Lilting Lullaby](card-operator-reading/0501-0600.md#card-0544) | 夜阑谣 | spell | COUNTER, RESTRICT |
| 0545 | [Lingering Animus](card-operator-reading/0501-0600.md#card-0545) | 弥留之灵 | unit | ENTRY |
| 0546 | [Lonely Poro](card-operator-reading/0501-0600.md#card-0546) | 哀哀魄罗 | unit | DRAW |
| 0547 | [Long Sword](card-operator-reading/0501-0600.md#card-0547) | 长剑 | gear | ATTACH, MOD_MIGHT |
| 0548 | [Loose Cannon](card-operator-reading/0501-0600.md#card-0548) | 暴走萝莉 | legend | DRAW |
| 0549 | [Lord Broadmane](card-operator-reading/0501-0600.md#card-0549) | 布罗梅因领主 | unit | GRANT_KEYWORD |
| 0550 | [Lost to the Sands](card-operator-reading/0501-0600.md#card-0550) | 葬身沙海 | spell | CHOOSE, DAMAGE, KILL |
| 0551 | [Lotus Trap](card-operator-reading/0501-0600.md#card-0551) | 莲花陷阱 | spell | MOD_DAMAGE |
| 0552 | [Loyal Poro](card-operator-reading/0501-0600.md#card-0552) | 忠忠魄罗 | unit | DRAW |
| 0553 | [Loyal Pup](card-operator-reading/0501-0600.md#card-0553) | 忠诚的猎犬 | unit | MOVE |
| 0554 | [Lucian, Gunslinger](card-operator-reading/0501-0600.md#card-0554) | 卢锡安, 孤绝枪火 | unit | DAMAGE |
| 0555 | [Lucian, Merciless](card-operator-reading/0501-0600.md#card-0555) | 卢锡安, 冷面枪手 | unit | READY |
| 0556 | [Lulu, Whimsical](card-operator-reading/0501-0600.md#card-0556) | 璐璐, 古灵精怪 | unit | SET_BASE_MIGHT |
| 0557 | [Lunar Boon](card-operator-reading/0501-0600.md#card-0557) | 月神恩赐 | spell | DISCARD, DRAW |
| 0558 | [Lux, Crownguard](card-operator-reading/0501-0600.md#card-0558) | 拉克丝, 冕卫之光 | unit | EXHAUST, ADD_RESOURCE, RESTRICT_RESOURCE |
| 0559 | [Lux, Illuminated](card-operator-reading/0501-0600.md#card-0559) | 拉克丝, 明丽光华 | unit | MOD_MIGHT |
| 0560 | [Machine Evangel](card-operator-reading/0501-0600.md#card-0560) | 机械戏法师 | unit | CREATE, PLAY |
| 0561 | [Maddened Marauder](card-operator-reading/0501-0600.md#card-0561) | 疯狂海寇 | unit | MOVE |
| 0562 | [Maduli the Gatekeeper](card-operator-reading/0501-0600.md#card-0562) | 守门者马杜里 | unit | RESTRICT, PAY, MOVE |
| 0563 | [Mageseeker Investigator](card-operator-reading/0501-0600.md#card-0563) | 搜魔人巡管 | unit | MOD_COST |
| 0564 | [Mageseeker Warden](card-operator-reading/0501-0600.md#card-0564) | 搜魔人典狱长 | unit | RESTRICT |
| 0565 | [Magma Wurm](card-operator-reading/0501-0600.md#card-0565) | 熔浆巨龙 | unit | ENTRY |
| 0566 | [Malzahar, Fanatic](card-operator-reading/0501-0600.md#card-0566) | 玛尔扎哈, 狂热信徒 | unit | KILL, EXHAUST, ADD_RESOURCE |
| 0567 | [Marai Spire](card-operator-reading/0501-0600.md#card-0567) | 玛莱尖塔 | battlefield | MOD_COST |
| 0568 | [Marching Orders](card-operator-reading/0501-0600.md#card-0568) | 行军号令 | spell | DAMAGE, REPEAT |
| 0569 | [Masa, Crashing Thunder](card-operator-reading/0501-0600.md#card-0569) | 雷霆之怒 玛萨 | unit | PAY, STUN |
| 0570 | [Mask Mother](card-operator-reading/0501-0600.md#card-0570) | 面具之母 | unit | PAY, MOD_MIGHT |
| 0571 | [Mask of Foresight](card-operator-reading/0501-0600.md#card-0571) | 远见面具 | gear | MOD_MIGHT |
| 0572 | [Master Bingwen](card-operator-reading/0501-0600.md#card-0572) | 炳文大师 | unit | PAY, ATTACH, MOD_COST |
| 0573 | [Master of Shadows](card-operator-reading/0501-0600.md#card-0573) | 影流之主 | legend | EMPOWER, DISEMPOWER, EXHAUST, DISCARD, DRAW |
| 0574 | [Master Yi, Honed](card-operator-reading/0501-0600.md#card-0574) | 易, 锋芒毕现 | unit | ENTRY, PERMIT |
| 0575 | [Master Yi, Meditative](card-operator-reading/0501-0600.md#card-0575) | 易, 禅心大道 | unit | MOD_MIGHT |
| 0576 | [Master Yi, Tempered](card-operator-reading/0501-0600.md#card-0576) | 易, 臻入化境 | unit | GRANT_KEYWORD |
| 0577 | [Master Yi, Unstoppable](card-operator-reading/0501-0600.md#card-0577) | 易, 人剑合一 | unit | MOD_COST, REPLACE, RESTRICT |
| 0578 | [Matriarch of War](card-operator-reading/0501-0600.md#card-0578) | 铁血狼母 | legend | EMPOWER, DISEMPOWER, PAY, EXHAUST, READY |
| 0579 | [Mech](card-operator-reading/0501-0600.md#card-0579) | 机器人 | unit | NONE |
| 0580 | [Mechanical Bandit](card-operator-reading/0501-0600.md#card-0580) | 自走角子机 | gear | REVEAL, DRAW, RECYCLE |
| 0581 | [Mechanized Menace](card-operator-reading/0501-0600.md#card-0581) | 机械公敌 | legend | GRANT_KEYWORD |
| 0582 | [Meditation](card-operator-reading/0501-0600.md#card-0582) | 冥想 | spell | EXHAUST, PAY, DRAW, REPLACE |
| 0583 | [Mega-Mech](card-operator-reading/0501-0600.md#card-0583) | 超能机甲 | unit | NONE |
| 0584 | [Megatusk](card-operator-reading/0501-0600.md#card-0584) | 巨牙海兽 | unit | XP, GRANT_KEYWORD |
| 0585 | [Mel, Defiant Soul](card-operator-reading/0501-0600.md#card-0585) | 梅尔, 镜转乾坤 | unit | DISCARD, BANISH |
| 0586 | [Mel, Newly Awakened](card-operator-reading/0501-0600.md#card-0586) | 梅尔, 奥法觉醒 | unit | DRAW, RESTRICT, MOD_EFFECT |
| 0587 | [Mesmerize](card-operator-reading/0501-0600.md#card-0587) | 惑心转意 | spell | CHOOSE, TRANSFER, MOD_MIGHT |
| 0588 | [Meticulous Restorationist](card-operator-reading/0501-0600.md#card-0588) | 细心的修复师 | unit | PLAY |
| 0589 | [Might of Demacia, Starter](card-operator-reading/0501-0600.md#card-0589) | 德玛西亚之力, 入门 | legend | DRAW |
| 0590 | [Minah Swiftfoot](card-operator-reading/0501-0600.md#card-0590) | 米娜·捷足 | unit | CHOOSE, DISCARD, DRAW |
| 0591 | [Mind Rune](card-operator-reading/0501-0600.md#card-0591) | 灵光符文 | rune | ADD_RESOURCE, PAY, EXHAUST, RECYCLE |
| 0592 | [Mindsplitter](card-operator-reading/0501-0600.md#card-0592) | 辟心玄龙 | unit | REVEAL, CHOOSE, DISCARD |
| 0593 | [Minefield](card-operator-reading/0501-0600.md#card-0593) | 雷区 | battlefield | TRANSFER |
| 0594 | [Minotaur Reckoner](card-operator-reading/0501-0600.md#card-0594) | 牛头人清算者 | unit | RESTRICT |
| 0595 | [Mirror Image](card-operator-reading/0501-0600.md#card-0595) | 镜花水月 | spell | CREATE, PLAY, COPY, GRANT_KEYWORD, DELAY |
| 0596 | [Mischievous Marai](card-operator-reading/0501-0600.md#card-0596) | 鲛人滋事者 | unit | DAMAGE |
| 0597 | [Miss Fortune, Buccaneer](card-operator-reading/0501-0600.md#card-0597) | 厄运小姐, 海盗 | unit | PERMIT |
| 0598 | [Miss Fortune, Captain](card-operator-reading/0501-0600.md#card-0598) | 厄运小姐, 船长 | unit | READY |
| 0599 | [Mister Root](card-operator-reading/0501-0600.md#card-0599) | 树根先生 | unit | XP |
| 0600 | [Mistfall](card-operator-reading/0501-0600.md#card-0600) | 雾临剑冢 | gear | PAY, EXHAUST, READY |
| 0601 | [Mobilize](card-operator-reading/0601-0700.md#card-0601) | 动员 | spell | CHANNEL, DRAW |
| 0602 | [Momentary Companion](card-operator-reading/0601-0700.md#card-0602) | 临时舞伴 | unit | GRANT_KEYWORD |
| 0603 | [Monastery of Hirana](card-operator-reading/0601-0700.md#card-0603) | 希拉娜修道院 | battlefield | SPEND_BUFF, DRAW |
| 0604 | [Monch](card-operator-reading/0601-0700.md#card-0604) | 啃啃 | unit | MOD_COST, ENTRY |
| 0605 | [Monster Harpoon](card-operator-reading/0601-0700.md#card-0605) | 渊海狩咒 | spell | DAMAGE, REPLACE |
| 0606 | [Moonfall](card-operator-reading/0601-0700.md#card-0606) | 月之降临 | spell | MOVE, MOD_MIGHT |
| 0607 | [Moonlight Affliction](card-operator-reading/0601-0700.md#card-0607) | 月光之殇 | spell | MOD_MIGHT |
| 0608 | [Morbid Return](card-operator-reading/0601-0700.md#card-0608) | 亡者复生 | spell | TRANSFER |
| 0609 | [Mordekaiser, Dominating](card-operator-reading/0601-0700.md#card-0609) | 莫德凯撒, 冥王进军 | unit | DISCARD, KILL, IF_DO |
| 0610 | [Mordekaiser, Twice Slain](card-operator-reading/0601-0700.md#card-0610) | 莫德凯撒, 冥途二渡 | unit | REPLACE, KILL, HEAL, EXHAUST, RECALL |
| 0611 | [Morgana, Vindictive](card-operator-reading/0601-0700.md#card-0611) | 莫甘娜, 复仇天使 | unit | DAMAGE |
| 0612 | [Mosstomper](card-operator-reading/0601-0700.md#card-0612) | 踏苔蜥 | unit | MOD_MIGHT, GRANT_KEYWORD |
| 0613 | [Mountain Drake](card-operator-reading/0601-0700.md#card-0613) | 山脉亚龙 | unit | NONE |
| 0614 | [Mournful Spirit](card-operator-reading/0601-0700.md#card-0614) | 哀戚悲灵 | unit | KILL |
| 0615 | [Mournful Witness](card-operator-reading/0601-0700.md#card-0615) | 悲悯见证者 | unit | EMPOWER, MOD_MIGHT |
| 0616 | [Mushroom Pouch](card-operator-reading/0601-0700.md#card-0616) | 蘑菇袋 | gear | DRAW |
| 0617 | [Mutated Mouser](card-operator-reading/0601-0700.md#card-0617) | 变异猫咪 | unit | SET_RULE, MOD_MIGHT |
| 0618 | [Mysterious Chronomancer](card-operator-reading/0601-0700.md#card-0618) | 神秘的时间法师 | unit | PREDICT |
| 0619 | [Mystic Poro](card-operator-reading/0601-0700.md#card-0619) | 叨叨魄罗 | unit | PREDICT |
| 0620 | [Mystic Reversal](card-operator-reading/0601-0700.md#card-0620) | 倒转神通 | spell | CONTROL, RECHOOSE |
| 0621 | [Mystic Vortex](card-operator-reading/0601-0700.md#card-0621) | 神秘星旋 | battlefield | MOD_COST |
| 0622 | [Nami, Headstrong](card-operator-reading/0601-0700.md#card-0622) | 娜美, 移海之志 | unit | PAY, STUN, DELAY, READY, BUFF |
| 0623 | [Nasus, Ascended](card-operator-reading/0601-0700.md#card-0623) | 内瑟斯, 飞升者 | unit | SCORE |
| 0624 | [Nasus, Guardian of Knowledge](card-operator-reading/0601-0700.md#card-0624) | 内瑟斯, 亘古守知 | unit | CHANNEL |
| 0625 | [Navori Fighting Pit](card-operator-reading/0601-0700.md#card-0625) | 纳沃利角斗场 | battlefield | BUFF |
| 0626 | [Navori Scout](card-operator-reading/0601-0700.md#card-0626) | 纳沃利侦察兵 | unit | RESTRICT |
| 0627 | [Nazuman Ntofo](card-operator-reading/0601-0700.md#card-0627) | 纳祖芒陀斧 | gear | ATTACH, GRANT_KEYWORD |
| 0628 | [Needlessly Large Yordle](card-operator-reading/0601-0700.md#card-0628) | 超大型约德尔人 | unit | MOD_COST |
| 0629 | [Neeko, Blending In](card-operator-reading/0601-0700.md#card-0629) | 妮蔻, 完美伪装 | unit | SETUP_CHOICE, ADD_LEGEND, LINK, DELAY |
| 0630 | [Nidalee, Cat Form](card-operator-reading/0601-0700.md#card-0630) | 奈德丽, 灵猫形态 | unit | DRAW |
| 0631 | [Nilah, Joyful Ascetic](card-operator-reading/0601-0700.md#card-0631) | 尼菈, 欢歌破浪 | unit | XP |
| 0632 | [Nine-Tailed Fox](card-operator-reading/0601-0700.md#card-0632) | 九尾妖狐 | legend | MOD_MIGHT |
| 0633 | [Nocturne, Horrifying](card-operator-reading/0601-0700.md#card-0633) | 魔腾, 惊魂夜 | unit | BANISH, PLAY, REPLACE |
| 0634 | [Not So Fast](card-operator-reading/0601-0700.md#card-0634) | 极速反制 | spell | COUNTER |
| 0635 | [Noxian Demolitionist](card-operator-reading/0601-0700.md#card-0635) | 诺克萨斯爆破手 | unit | KILL |
| 0636 | [Noxian Drummer](card-operator-reading/0601-0700.md#card-0636) | 诺克萨斯鼓手 | unit | CREATE, PLAY |
| 0637 | [Noxian Emissary](card-operator-reading/0601-0700.md#card-0637) | 诺克萨斯使节 | unit | CREATE, PLAY |
| 0638 | [Noxian Guillotine](card-operator-reading/0601-0700.md#card-0638) | 诺克萨斯断头台 | spell | DELAY, KILL, REPLACE |
| 0639 | [Noxus Hopeful](card-operator-reading/0601-0700.md#card-0639) | 诺克萨斯新兵 | unit | MOD_COST |
| 0640 | [Noxus Saboteur](card-operator-reading/0601-0700.md#card-0640) | 诺克萨斯破坏者 | unit | RESTRICT |
| 0641 | [Ntofo Strikes](card-operator-reading/0601-0700.md#card-0641) | 陀斧打击 | spell | GRANT_KEYWORD, DAMAGE |
| 0642 | [Oasis Raider](card-operator-reading/0601-0700.md#card-0642) | 绿洲劫掠者 | unit | MOD_MIGHT, GRANT_KEYWORD |
| 0643 | [Obelisk of Power](card-operator-reading/0601-0700.md#card-0643) | 力量方尖碑 | battlefield | CHANNEL |
| 0644 | [Ocean Drake](card-operator-reading/0601-0700.md#card-0644) | 海洋亚龙 | unit | PERMIT, TRANSFER |
| 0645 | [Ol’ Poro](card-operator-reading/0601-0700.md#card-0645) | 老老魄罗 | unit | RESTRICT |
| 0646 | [On the Hunt](card-operator-reading/0601-0700.md#card-0646) | 狩猎 | spell | READY |
| 0647 | [One-Two Punch](card-operator-reading/0601-0700.md#card-0647) | 组合拳 | spell | BUFF, STUN |
| 0648 | [Onslaught](card-operator-reading/0601-0700.md#card-0648) | 狂袭 | spell | MOD_MIGHT |
| 0649 | [Orb of Regret](card-operator-reading/0601-0700.md#card-0649) | 懊悔法球 | gear | EXHAUST, MOD_MIGHT |
| 0650 | [Order Rune](card-operator-reading/0601-0700.md#card-0650) | 序理符文 | rune | ADD_RESOURCE, PAY, EXHAUST, RECYCLE |
| 0651 | [Orianna, Exquisite](card-operator-reading/0601-0700.md#card-0651) | 奥莉安娜, 精密优雅 | unit | RESTRICT |
| 0652 | [Orianna, Mechanical Marvel](card-operator-reading/0601-0700.md#card-0652) | 奥莉安娜, 机械奇迹 | unit | MOD_COST |
| 0653 | [Ornn, Blacksmith](card-operator-reading/0601-0700.md#card-0653) | 奥恩, 铁匠 | unit | LOOK, REVEAL, DRAW, RECYCLE |
| 0654 | [Ornn, Forge God](card-operator-reading/0601-0700.md#card-0654) | 奥恩, 熔铸之神 | unit | MOD_MIGHT |
| 0655 | [Ornn’s Forge](card-operator-reading/0601-0700.md#card-0655) | 奥恩的锻炉 | battlefield | MOD_COST |
| 0656 | [Otterpus](card-operator-reading/0601-0700.md#card-0656) | 章獭 | unit | REPLACE, DRAW |
| 0657 | [Overloaded Traveler](card-operator-reading/0601-0700.md#card-0657) | 满载的旅人 | unit | MOD_MIGHT |
| 0658 | [Overt Operation](card-operator-reading/0601-0700.md#card-0658) | 公开行动 | spell | SPEND_BUFF, READY, BUFF |
| 0659 | [Overzealous Fan](card-operator-reading/0601-0700.md#card-0659) | 狂热粉丝 | unit | KILL, MOVE |
| 0660 | [Pack of Wonders](card-operator-reading/0601-0700.md#card-0660) | 奇妙行囊 | gear | EXHAUST, TRANSFER |
| 0661 | [Packed Amphitheater](card-operator-reading/0601-0700.md#card-0661) | 星耀殿堂 | battlefield | MOD_MIGHT |
| 0662 | [Pakaa Cub](card-operator-reading/0601-0700.md#card-0662) | 帕卡幼崽 | unit | HIDE, PERMIT |
| 0663 | [Pakaa Protector](card-operator-reading/0601-0700.md#card-0663) | 帕卡监护者 | unit | REVEAL, DRAW, TRANSFER, MOD_MIGHT |
| 0664 | [Parallel Convergence](card-operator-reading/0601-0700.md#card-0664) | 时光交错 | spell | TRANSFER, PAY, DAMAGE |
| 0665 | [Party Crasher](card-operator-reading/0601-0700.md#card-0665) | 不速之客 | unit | MOD_COST |
| 0666 | [Party Favors](card-operator-reading/0601-0700.md#card-0666) | 次元门狂欢 | spell | CHOOSE, DRAW, CHANNEL |
| 0667 | [Patched Porobot](card-operator-reading/0601-0700.md#card-0667) | 散装机械魄罗 | unit+gear | ENTRY, DRAW |
| 0668 | [Peak Guardian](card-operator-reading/0601-0700.md#card-0668) | 巅峰守护者 | unit | BUFF |
| 0669 | [Pendulum Blade](card-operator-reading/0601-0700.md#card-0669) | 悬摆之刃 | gear | ATTACH, MOD_MIGHT |
| 0670 | [Perched Grimwyrm](card-operator-reading/0601-0700.md#card-0670) | 栖息的冥龙 | unit | RESTRICT, PERMIT |
| 0671 | [Perfect Execution](card-operator-reading/0601-0700.md#card-0671) | 表里杀缭乱 | spell | READY, GRANT_KEYWORD |
| 0672 | [Petal Pixie](card-operator-reading/0601-0700.md#card-0672) | 花瓣仙子 | unit | MOD_MIGHT |
| 0673 | [Petricite Monument](card-operator-reading/0601-0700.md#card-0673) | 禁魔石丰碑 | gear | GRANT_KEYWORD |
| 0674 | [Petty Officer](card-operator-reading/0601-0700.md#card-0674) | 躁烈的副官 | unit | MOD_MIGHT |
| 0675 | [Pickpocket](card-operator-reading/0601-0700.md#card-0675) | 暗巷神偷 | unit | KILL, CREATE, PLAY, IF_DO |
| 0676 | [Piercing Light](card-operator-reading/0601-0700.md#card-0676) | 透体圣光 | spell | DAMAGE, REPEAT |
| 0677 | [Pillaged Armory](card-operator-reading/0601-0700.md#card-0677) | 搜刮来的武器堆 | gear | BUFF |
| 0678 | [Piltovan Forge](card-operator-reading/0601-0700.md#card-0678) | 皮城锻炉 | battlefield | MOD_COST |
| 0679 | [Piltovan Guidebot](card-operator-reading/0601-0700.md#card-0679) | 皮城向导机器人 | unit | SET_BASE_MIGHT |
| 0680 | [Piltover Enforcer](card-operator-reading/0601-0700.md#card-0680) | 皮城执法官 | legend | EXHAUST, READY |
| 0681 | [Pirate’s Haven](card-operator-reading/0601-0700.md#card-0681) | 海盗避风港 | gear | MOD_MIGHT |
| 0682 | [Pit Crew](card-operator-reading/0601-0700.md#card-0682) | 竞技场勤务小队 | unit | READY |
| 0683 | [Pit Rookie](card-operator-reading/0601-0700.md#card-0683) | 竞技场新人 | unit | BUFF |
| 0684 | [Pitiless Stalker](card-operator-reading/0601-0700.md#card-0684) | 无情潜伏者 | unit | EXHAUST, STUN |
| 0685 | [Platewyrm Egg](card-operator-reading/0601-0700.md#card-0685) | 剑头蛟的卵 | gear | ENTRY, EXHAUST, ADD_RESOURCE, REPLACE |
| 0686 | [Playful Phantom](card-operator-reading/0601-0700.md#card-0686) | 贪玩的小鬼 | unit | NONE |
| 0687 | [Plaza Guardian](card-operator-reading/0601-0700.md#card-0687) | 广场守卫 | unit | MOD_COST |
| 0688 | [Plundering Poro](card-operator-reading/0601-0700.md#card-0688) | 坏坏魄罗 | unit | CREATE, PLAY |
| 0689 | [Poppy, Defender of the Meek](card-operator-reading/0601-0700.md#card-0689) | 波比, 扶弱使者 | unit | XP, MOD_COST |
| 0690 | [Poppy, Paragon](card-operator-reading/0601-0700.md#card-0690) | 波比, 刚毅典范 | unit | READY, XP |
| 0691 | [Poro Herder](card-operator-reading/0601-0700.md#card-0691) | 魄罗牧者 | unit | BUFF, DRAW |
| 0692 | [Poro Snax](card-operator-reading/0601-0700.md#card-0692) | 魄罗佳肴 | gear | DRAW, PAY, EXHAUST, KILL |
| 0693 | [Portable Portal](card-operator-reading/0601-0700.md#card-0693) | 便携传送门 | gear | PAY, READY, GRANT_KEYWORD |
| 0694 | [Portal Rescue](card-operator-reading/0601-0700.md#card-0694) | 传送门大营救 | spell | BANISH, PLAY |
| 0695 | [Possession](card-operator-reading/0601-0700.md#card-0695) | 据为己有 | spell | CONTROL, RECALL |
| 0696 | [Pouty Poro](card-operator-reading/0601-0700.md#card-0696) | 呸呸魄罗 | unit | RESTRICT |
| 0697 | [Power Nexus](card-operator-reading/0601-0700.md#card-0697) | 能量枢纽 | battlefield | PAY, SCORE |
| 0698 | [Premonition](card-operator-reading/0601-0700.md#card-0698) | 先知之兆 | spell | DRAW |
| 0699 | [Prepared Neophyte](card-operator-reading/0601-0700.md#card-0699) | 晋升信徒 | unit | MOD_MIGHT |
| 0700 | [Pride of Nazumah](card-operator-reading/0601-0700.md#card-0700) | 纳祖芒荣耀 | legend | GRANT_ABILITY, MOD_KEYWORD |
| 0701 | [Pridestalker](card-operator-reading/0701-0800.md#card-0701) | 傲之追猎者 | legend | MOD_MIGHT |
| 0702 | [Primal Strength](card-operator-reading/0701-0800.md#card-0702) | 洪荒巨力 | spell | MOD_MIGHT |
| 0703 | [Primordial Roar](card-operator-reading/0701-0800.md#card-0703) | 洪荒咆哮 | spell | SHOW_OFF, DAMAGE |
| 0704 | [Prize of Progress](card-operator-reading/0701-0800.md#card-0704) | 进步荣光 | unit | MOD_MIGHT |
| 0705 | [Prodigal Explorer](card-operator-reading/0701-0800.md#card-0705) | 探险家 | legend | EXHAUST, DRAW |
| 0706 | [Production Surge](card-operator-reading/0701-0800.md#card-0706) | 产量激增 | spell | MOD_COST, CREATE, PLAY, DRAW |
| 0707 | [Profiteer](card-operator-reading/0701-0800.md#card-0707) | 黑心商人 | unit | DISEMPOWER, EMPOWER, IF_DO |
| 0708 | [Progress Day](card-operator-reading/0701-0800.md#card-0708) | 进化日 | spell | DRAW |
| 0709 | [Promising Future](card-operator-reading/0701-0800.md#card-0709) | 光明未来 | spell | LOOK, BANISH, RECYCLE, ORDER, PLAY |
| 0710 | [Protective Sands](card-operator-reading/0701-0800.md#card-0710) | 藏古之漠 | battlefield | PAY, DRAW |
| 0711 | [Protector’s Shield](card-operator-reading/0701-0800.md#card-0711) | 守护者之盾 | gear | ATTACH, MOD_MIGHT, GRANT_KEYWORD |
| 0712 | [Public Execution](card-operator-reading/0701-0800.md#card-0712) | 公开处刑 | spell | KILL |
| 0713 | [Punch First](card-operator-reading/0701-0800.md#card-0713) | 先打再问 | spell | MOD_MIGHT |
| 0714 | [Punching Poro](card-operator-reading/0701-0800.md#card-0714) | 拳拳魄罗 | unit | DISCARD, MOD_MIGHT |
| 0715 | [Purifier](card-operator-reading/0701-0800.md#card-0715) | 圣枪游侠 | legend | GRANT_KEYWORD |
| 0716 | [Pyke, Dockside Butcher](card-operator-reading/0701-0800.md#card-0716) | 派克, 码头屠夫 | unit | PAY, READY, MOD_MIGHT |
| 0717 | [Pyke, Returned](card-operator-reading/0701-0800.md#card-0717) | 派克, 深渊再临 | unit | CREATE, PLAY |
| 0718 | [Qiyana, Victorious](card-operator-reading/0701-0800.md#card-0718) | 奇亚娜, 所向披靡 | unit | CHOOSE, DRAW, CHANNEL |
| 0719 | [Questionable Tome](card-operator-reading/0701-0800.md#card-0719) | 可疑之书 | gear | DISEMPOWER, PAY, EXHAUST, DRAW |
| 0720 | [Rabadon’s Deathcrown](card-operator-reading/0701-0800.md#card-0720) | 灭世者的死亡之冠 | gear | ATTACH, MOD_MIGHT, MOD_DAMAGE |
| 0721 | [Radiant Dawn](card-operator-reading/0701-0800.md#card-0721) | 曙光女神 | legend | BUFF |
| 0722 | [Rage Amplifier](card-operator-reading/0701-0800.md#card-0722) | 怒火放大器 | gear | MOD_MIGHT, REPLACE |
| 0723 | [Raging Firebrand](card-operator-reading/0701-0800.md#card-0723) | 狂暴龙怪 | unit | DELAY, MOD_COST |
| 0724 | [Raging Soul](card-operator-reading/0701-0800.md#card-0724) | 肆虐狂魂 | unit | GRANT_KEYWORD |
| 0725 | [Rakelstake](card-operator-reading/0701-0800.md#card-0725) | 拉克斯塔克 | battlefield | PREDICT |
| 0726 | [Rally for War](card-operator-reading/0701-0800.md#card-0726) | 战争集结 | spell | CREATE, PLAY |
| 0727 | [Rally the Troops](card-operator-reading/0701-0800.md#card-0727) | 集结部队 | spell | DELAY, BUFF, DRAW |
| 0728 | [Rampage](card-operator-reading/0701-0800.md#card-0728) | 暴走 | spell | PAY, MOD_MIGHT, DAMAGE |
| 0729 | [Raucous Anthem](card-operator-reading/0701-0800.md#card-0729) | 炸裂神曲 | spell | READY, MOD_MIGHT |
| 0730 | [Ravenbloom Conservatory](card-operator-reading/0701-0800.md#card-0730) | 拉文布鲁姆学院 | battlefield | REVEAL, TRANSFER, RECYCLE |
| 0731 | [Ravenbloom Prefect](card-operator-reading/0701-0800.md#card-0731) | 拉文布鲁姆级长 | unit | BANISH, IF_DO |
| 0732 | [Ravenbloom Student](card-operator-reading/0701-0800.md#card-0732) | 拉文布鲁姆学生 | unit | MOD_MIGHT |
| 0733 | [Ravenborn Tome](card-operator-reading/0701-0800.md#card-0733) | 邪鸦魔典 | gear | EXHAUST, DELAY, MOD_DAMAGE |
| 0734 | [Raving Witness](card-operator-reading/0701-0800.md#card-0734) | 狂热目击者 | unit | REVEAL, DRAW, RECYCLE |
| 0735 | [Realm of Death](card-operator-reading/0701-0800.md#card-0735) | 轮回绝境 | spell | MOD_MIGHT, DAMAGE |
| 0736 | [Reaver’s Row](card-operator-reading/0701-0800.md#card-0736) | 劫掠船巷 | battlefield | MOVE |
| 0737 | [Rebuke](card-operator-reading/0701-0800.md#card-0737) | 责退 | spell | TRANSFER |
| 0738 | [Rebuttal](card-operator-reading/0701-0800.md#card-0738) | 灵魂折镜 | spell | PAY, CONTROL, RECHOOSE, COUNTER |
| 0739 | [Reckless Innovator](card-operator-reading/0701-0800.md#card-0739) | 鲁莽的发明家 | unit | CHOOSE, CREATE, PLAY, PAY, DRAW |
| 0740 | [Reckoner’s Arena](card-operator-reading/0701-0800.md#card-0740) | 清算人竞技场 | battlefield | EXECUTE_TRIGGER |
| 0741 | [Recruit](card-operator-reading/0701-0800.md#card-0741) | 随从 | unit | NONE |
| 0742 | [Recruit the Vanguard](card-operator-reading/0701-0800.md#card-0742) | 共同献身 | spell | CREATE, PLAY |
| 0743 | [Recurve Bow](card-operator-reading/0701-0800.md#card-0743) | 反曲之弓 | gear | ATTACH, DAMAGE |
| 0744 | [Red Brambleback](card-operator-reading/0701-0800.md#card-0744) | 绯红印记树怪 | unit | MOD_TRIGGER, BUFF |
| 0745 | [Reflection](card-operator-reading/0701-0800.md#card-0745) | 映像 | unit | COPY |
| 0746 | [Reinforce](card-operator-reading/0701-0800.md#card-0746) | 增援 | spell | LOOK, BANISH, PLAY, MOD_COST, RECYCLE |
| 0747 | [Rek’Sai, Breacher](card-operator-reading/0701-0800.md#card-0747) | 雷克塞, 黄沙噬猎 | unit | GRANT_KEYWORD |
| 0748 | [Rek’Sai, Swarm Queen](card-operator-reading/0701-0800.md#card-0748) | 雷克塞, 万类女皇 | unit | REVEAL, BANISH, PLAY, RECYCLE |
| 0749 | [Relentless Pursuit](card-operator-reading/0701-0800.md#card-0749) | 冷酷追击 | spell | MOVE, ATTACH, GRANT_ABILITY |
| 0750 | [Relentless Storm](card-operator-reading/0701-0800.md#card-0750) | 不灭狂雷 | legend | EXHAUST, CHANNEL |
| 0751 | [Rell, Magnetic](card-operator-reading/0701-0800.md#card-0751) | 芮尔, 唯心铁意 | unit | PLAY, ATTACH, DELAY |
| 0752 | [Reluctant Leader](card-operator-reading/0701-0800.md#card-0752) | 草包队长 | unit | MOD_MIGHT |
| 0753 | [Remember the Fallen](card-operator-reading/0701-0800.md#card-0753) | 不朽铭记 | spell | PLAY |
| 0754 | [Renata Glasc, Industrialist](card-operator-reading/0701-0800.md#card-0754) | 烈娜塔·戈拉斯克, 实业家 | unit | ENTRY |
| 0755 | [Renata Glasc, Mastermind](card-operator-reading/0701-0800.md#card-0755) | 烈娜塔·戈拉斯克, 幕后主脑 | unit | PAY, DRAW, EXHAUST, SCORE, RESTRICT |
| 0756 | [Renekton, Brute](card-operator-reading/0701-0800.md#card-0756) | 雷克顿, 蛮荒巨兽 | unit | PAY, MOD_MIGHT, EMPOWER, GRANT_KEYWORD |
| 0757 | [Renekton, Rage Fueled](card-operator-reading/0701-0800.md#card-0757) | 雷克顿, 杀意骤起 | unit | DAMAGE |
| 0758 | [Rengar, Pouncing](card-operator-reading/0701-0800.md#card-0758) | 雷恩加尔, 暴起 | unit | PERMIT |
| 0759 | [Rengar, Trophy Hunter](card-operator-reading/0701-0800.md#card-0759) | 雷恩加尔, 异兽猎手 | unit | PERMIT |
| 0760 | [Rengar, Unseen](card-operator-reading/0701-0800.md#card-0760) | 雷恩加尔, 隐匿杀机 | unit | PAY, ENTRY, MOD_MIGHT, RESTRICT, PERMIT |
| 0761 | [Repair Specialist](card-operator-reading/0701-0800.md#card-0761) | 维修专家 | unit | MOD_KEYWORD |
| 0762 | [Repulse](card-operator-reading/0701-0800.md#card-0762) | 击退 | spell | COUNTER |
| 0763 | [Resonating Strike](card-operator-reading/0701-0800.md#card-0763) | 回音击 | spell | MOVE, MOD_MIGHT |
| 0764 | [Resource Extractor](card-operator-reading/0701-0800.md#card-0764) | 资源开采器 | gear | CREATE, PLAY |
| 0765 | [Resplendent Rostrum](card-operator-reading/0701-0800.md#card-0765) | 辉映圣坛 | gear | EXHAUST, DRAW, CHANNEL, MOD_MIGHT |
| 0766 | [Retreat](card-operator-reading/0701-0800.md#card-0766) | 择日再战 | spell | TRANSFER, CHANNEL |
| 0767 | [Revna the Lorekeeper](card-operator-reading/0701-0800.md#card-0767) | 传承者雷芙纳 | unit | READY |
| 0768 | [Rhasa the Sunderer](card-operator-reading/0701-0800.md#card-0768) | 裂魂者喇煞 | unit | MOD_COST |
| 0769 | [Ribbon Dancer](card-operator-reading/0701-0800.md#card-0769) | 绸舞士 | unit | MOD_MIGHT |
| 0770 | [Ride the Wind](card-operator-reading/0701-0800.md#card-0770) | 驭风而行 | spell | MOVE, READY |
| 0771 | [Rift Herald](card-operator-reading/0701-0800.md#card-0771) | 峡谷先锋 | unit | LOOK, REVEAL, DRAW, RECYCLE, PLAY |
| 0772 | [Right of Conquest](card-operator-reading/0701-0800.md#card-0772) | 占山为王 | spell | DRAW |
| 0773 | [Riposte](card-operator-reading/0701-0800.md#card-0773) | 劳伦特心眼刀 | spell | COUNTER, MOD_MIGHT |
| 0774 | [Ripper’s Bay](card-operator-reading/0701-0800.md#card-0774) | 鬼影湾 | battlefield | PAY, CHANNEL |
| 0775 | [Riptide Mage](card-operator-reading/0701-0800.md#card-0775) | 怒海法师 | unit | MOD_MIGHT |
| 0776 | [Riptide Rex](card-operator-reading/0701-0800.md#card-0776) | 怒海大鲨炮 | unit | DAMAGE |
| 0777 | [Risen Altar](card-operator-reading/0701-0800.md#card-0777) | 升格圣坛 | battlefield | MOD_COST |
| 0778 | [Riven, Broken Blade](card-operator-reading/0701-0800.md#card-0778) | 锐雯, 断剑之誓 | unit | CHOOSE, BUFF, SPEND_BUFF, STUN, READY |
| 0779 | [Riven, Deserter](card-operator-reading/0701-0800.md#card-0779) | 锐雯, 弃暗投明 | unit | MOD_MIGHT, EXHAUST, READY |
| 0780 | [Riven, Shattered](card-operator-reading/0701-0800.md#card-0780) | 锐雯, 重铸而归 | unit | DAMAGE |
| 0781 | [Rocket Barrage](card-operator-reading/0701-0800.md#card-0781) | 火箭轰击 | spell | CHOOSE, DAMAGE, KILL, REPEAT |
| 0782 | [Rockfall Path](card-operator-reading/0701-0800.md#card-0782) | 落岩之径 | battlefield | RESTRICT |
| 0783 | [Rogue Assassin](card-operator-reading/0701-0800.md#card-0783) | 离群之刺 | legend | EXHAUST, MOVE, READY |
| 0784 | [Rousing Display](card-operator-reading/0701-0800.md#card-0784) | 辉映同心 | spell | SHOW_OFF, CREATE, PLAY, REPLACE |
| 0785 | [Royal Entourage](card-operator-reading/0701-0800.md#card-0785) | 皇家随从 | unit | CHOOSE, READY, EXHAUST |
| 0786 | [Royal Guard](card-operator-reading/0701-0800.md#card-0786) | 皇家守卫 | unit | CREATE, PLAY |
| 0787 | [Ruin Runner](card-operator-reading/0701-0800.md#card-0787) | 沙墟啸匪 | unit | RESTRICT |
| 0788 | [Ruined Monastery](card-operator-reading/0701-0800.md#card-0788) | 破败修道院 | battlefield | DISCARD, CHANNEL |
| 0789 | [Ruined Rex](card-operator-reading/0701-0800.md#card-0789) | 破败大鲨炮 | unit | DAMAGE |
| 0790 | [Rumble, Hotheaded](card-operator-reading/0701-0800.md#card-0790) | 兰博, 热力全开 | unit | GRANT_KEYWORD, RECYCLE, PLAY, MOD_COST |
| 0791 | [Rumble, Scrapper](card-operator-reading/0701-0800.md#card-0791) | 兰博, 机械师 | unit | MOD_MIGHT, CREATE, PLAY |
| 0792 | [Rune Prison](card-operator-reading/0701-0800.md#card-0792) | 符文禁锢 | spell | STUN |
| 0793 | [Runeblade Anvil](card-operator-reading/0701-0800.md#card-0793) | 符刃铁砧 | gear | BANISH, PERMIT, DELAY, PAY, EXHAUST, KILL |
| 0794 | [Ruthless Strike](card-operator-reading/0701-0800.md#card-0794) | 无情打击 | spell | DISCARD, PAY, DAMAGE, REPLACE |
| 0795 | [Sabotage](card-operator-reading/0701-0800.md#card-0795) | 暗中破坏 | spell | REVEAL, CHOOSE, RECYCLE |
| 0796 | [Sacred Protector](card-operator-reading/0701-0800.md#card-0796) | 神圣守护者 | unit | RESTRICT |
| 0797 | [Sacred Shears](card-operator-reading/0701-0800.md#card-0797) | 神圣剪刀 | gear | ATTACH, MOD_MIGHT, DRAW |
| 0798 | [Sacrifice](card-operator-reading/0701-0800.md#card-0798) | 牺牲 | spell | KILL, PAY, DRAW, CHANNEL |
| 0799 | [Safety Inspector](card-operator-reading/0701-0800.md#card-0799) | 安全检查员 | unit | XP, PAY, CHOOSE, KILL |
| 0800 | [Sai Scout](card-operator-reading/0701-0800.md#card-0800) | 大塞斥候 | unit | PERMIT, PREDICT |
| 0801 | [Salvage](card-operator-reading/0801-0900.md#card-0801) | 废物利用 | spell | KILL, DRAW |
| 0802 | [Sanction](card-operator-reading/0801-0900.md#card-0802) | 念化盈虚 | spell | CHOOSE, EMPOWER, DISEMPOWER, DELAY |
| 0803 | [Sanctum Conservator](card-operator-reading/0801-0900.md#card-0803) | 圣所保管员 | unit | READY |
| 0804 | [Sand Soldier](card-operator-reading/0801-0900.md#card-0804) | 黄沙士兵 | unit | NONE |
| 0805 | [Sandshifter](card-operator-reading/0801-0900.md#card-0805) | 流沙术士 | unit | KILL |
| 0806 | [Sandstone Chimera](card-operator-reading/0801-0900.md#card-0806) | 砂岩奇美拉 | unit | SET_RULE |
| 0807 | [Sandswept Tomb](card-operator-reading/0801-0900.md#card-0807) | 沙蚀墓穴 | battlefield | MOD_COST |
| 0808 | [Satchel Charge](card-operator-reading/0801-0900.md#card-0808) | 定点爆破 | spell | MOVE, CREATE, PLAY |
| 0809 | [Scorchclaw](card-operator-reading/0801-0900.md#card-0809) | 焰爪 | unit | MOD_MIGHT, ENTRY |
| 0810 | [Scorched Earth](card-operator-reading/0801-0900.md#card-0810) | 灼热焦土 | spell | DAMAGE |
| 0811 | [Scorn of the Moon](card-operator-reading/0801-0900.md#card-0811) | 皎月女神 | legend | EXHAUST, ADD_RESOURCE, RESTRICT_RESOURCE |
| 0812 | [Scrapheap](card-operator-reading/0801-0900.md#card-0812) | 废料堆 | gear | DRAW |
| 0813 | [Scrapyard Champion](card-operator-reading/0801-0900.md#card-0813) | 垃圾场小霸王 | unit | DISCARD, DRAW |
| 0814 | [Scrutinizing Scope](card-operator-reading/0801-0900.md#card-0814) | 严审透镜 | gear | PAY, EXHAUST, NAME, REVEAL, RECYCLE, DRAW |
| 0815 | [Scrutinizing Sergeant](card-operator-reading/0801-0900.md#card-0815) | 严厉军士 | unit | XP |
| 0816 | [Scryer’s Bloom](card-operator-reading/0801-0900.md#card-0816) | 占卜花朵 | gear | ENTRY, KILL, PAY, EXHAUST, PREDICT, DRAW, XP |
| 0817 | [Scuttle Crab](card-operator-reading/0801-0900.md#card-0817) | 迅捷蟹 | unit | DRAW, CHOOSE, REVEAL, PERMIT, XP |
| 0818 | [Sea Monkey](card-operator-reading/0801-0900.md#card-0818) | 船猿 | unit | PAY, BUFF |
| 0819 | [Seal of Discord](card-operator-reading/0801-0900.md#card-0819) | 不和之印 | gear | EXHAUST, ADD_RESOURCE |
| 0820 | [Seal of Focus](card-operator-reading/0801-0900.md#card-0820) | 专注之印 | gear | EXHAUST, ADD_RESOURCE |
| 0821 | [Seal of Insight](card-operator-reading/0801-0900.md#card-0821) | 洞察之印 | gear | EXHAUST, ADD_RESOURCE |
| 0822 | [Seal of Rage](card-operator-reading/0801-0900.md#card-0822) | 暴怒之印 | gear | EXHAUST, ADD_RESOURCE |
| 0823 | [Seal of Strength](card-operator-reading/0801-0900.md#card-0823) | 力量之印 | gear | EXHAUST, ADD_RESOURCE |
| 0824 | [Seal of Unity](card-operator-reading/0801-0900.md#card-0824) | 团结之印 | gear | EXHAUST, ADD_RESOURCE |
| 0825 | [Seat of Power](card-operator-reading/0801-0900.md#card-0825) | 权能之座 | battlefield | DRAW |
| 0826 | [Sentinel Adept](card-operator-reading/0801-0900.md#card-0826) | 哨兵好手 | unit | PAY, ATTACH, MOD_COST |
| 0827 | [Seraphic Wyvern](card-operator-reading/0801-0900.md#card-0827) | 天界双足龙 | unit | REPLACE, CHANNEL |
| 0828 | [Seraphine, Inspiring](card-operator-reading/0801-0900.md#card-0828) | 萨勒芬妮, 声愈人心 | unit | DRAW |
| 0829 | [Seraphine, Not Alone](card-operator-reading/0801-0900.md#card-0829) | 萨勒芬妮, 星火相随 | unit | CREATE, PLAY, MOD_MIGHT |
| 0830 | [Serene Ascetic](card-operator-reading/0801-0900.md#card-0830) | 无情苦修者 | unit | GRANT_KEYWORD |
| 0831 | [Serrated Dirk](card-operator-reading/0801-0900.md#card-0831) | 锯齿短匕 | gear | ATTACH, GRANT_KEYWORD |
| 0832 | [Sett, Brawler](card-operator-reading/0801-0900.md#card-0832) | 瑟提, 铁拳 | unit | BUFF, SPEND_BUFF, MOD_MIGHT |
| 0833 | [Sett, Kingpin](card-operator-reading/0801-0900.md#card-0833) | 瑟提, 魁首 | unit | MOD_MIGHT |
| 0834 | [Shadow](card-operator-reading/0801-0900.md#card-0834) | 黑影 | unit | ENTRY, PAY, EXHAUST, STUN |
| 0835 | [Shadow Assassin](card-operator-reading/0801-0900.md#card-0835) | 暗影刺客 | unit | ENTRY |
| 0836 | [Shadow Clone](card-operator-reading/0801-0900.md#card-0836) | 影分身 | unit | BANISH, GRANT_KEYWORD, IF_DO |
| 0837 | [Shadow Dash](card-operator-reading/0801-0900.md#card-0837) | 奥义！影缚 | spell | MOVE, MOD_MIGHT |
| 0838 | [Shadow Fiend](card-operator-reading/0801-0900.md#card-0838) | 暗影之魔 | unit | GRANT_KEYWORD |
| 0839 | [Shadow Order Disciple](card-operator-reading/0801-0900.md#card-0839) | 影流弟子 | unit | BURN, MOD_MIGHT, IF_DO |
| 0840 | [Shadow Temple](card-operator-reading/0801-0900.md#card-0840) | 影流寺院 | battlefield | BURN |
| 0841 | [Shadow Watcher](card-operator-reading/0801-0900.md#card-0841) | 影卫 | unit | ENTRY |
| 0842 | [Shadowblade Lurker](card-operator-reading/0801-0900.md#card-0842) | 影刃潜伏者 | unit | MOD_COST |
| 0843 | [Shadows of the Past](card-operator-reading/0801-0900.md#card-0843) | 往日阴影 | spell | TRANSFER |
| 0844 | [Shadow’s Call](card-operator-reading/0801-0900.md#card-0844) | 暗影的召唤 | spell | GRANT_KEYWORD, DRAW |
| 0845 | [Shady Spectacles](card-operator-reading/0801-0900.md#card-0845) | 可疑的眼镜 | gear | ATTACH, COPY, LINK |
| 0846 | [Shakedown](card-operator-reading/0801-0900.md#card-0846) | 巧取豪夺 | spell | CHOOSE, DRAW, DAMAGE |
| 0847 | [Shard of Undoing](card-operator-reading/0801-0900.md#card-0847) | 逆转碎片 | gear | CHOOSE, KILL |
| 0848 | [Sharkling](card-operator-reading/0801-0900.md#card-0848) | 小鲨鱼 | unit | PAY, ENTRY, MOD_MIGHT |
| 0849 | [Shen, Kinkou](card-operator-reading/0801-0900.md#card-0849) | 慎, 均衡守中 | unit | PERMIT, MOD_MIGHT, SET_RULE |
| 0850 | [Shen, Leader of the Kinkou Order](card-operator-reading/0801-0900.md#card-0850) | 慎, 均衡领袖 | unit | SCORE |
| 0851 | [Shen, Scourge of Shadows](card-operator-reading/0801-0900.md#card-0851) | 慎, 破影之光 | unit | DRAW |
| 0852 | [Shepherd’s Heirloom](card-operator-reading/0801-0900.md#card-0852) | 牧人的传家宝 | gear | XP, ATTACH, MOD_MIGHT |
| 0853 | [Shimmering Swimmer](card-operator-reading/0801-0900.md#card-0853) | 微光泳者 | unit | KILL, PAY, DAMAGE |
| 0854 | [Shipyard Skulker](card-operator-reading/0801-0900.md#card-0854) | 船坞潜伏者 | unit | NONE |
| 0855 | [Shock Blast](card-operator-reading/0801-0900.md#card-0855) | 电能震荡 | spell | MOD_COST, DAMAGE |
| 0856 | [Show of Strength](card-operator-reading/0801-0900.md#card-0856) | 实力至上 | spell | DRAW |
| 0857 | [Showstopper](card-operator-reading/0801-0900.md#card-0857) | 叹为观止 | spell | BUFF, MOVE |
| 0858 | [Shurelya’s Requiem](card-operator-reading/0801-0900.md#card-0858) | 舒瑞娅的安魂曲 | gear | ATTACH, MOD_MIGHT, READY, GRANT_KEYWORD |
| 0859 | [Shuriken Flip](card-operator-reading/0801-0900.md#card-0859) | 我流奥义！隼舞 | spell | DAMAGE, MOVE |
| 0860 | [Sigil of the Storm](card-operator-reading/0801-0900.md#card-0860) | 雷霆之纹 | battlefield | RECYCLE |
| 0861 | [Simian Ancestor](card-operator-reading/0801-0900.md#card-0861) | 山猿老祖 | unit | READY |
| 0862 | [Singularity](card-operator-reading/0801-0900.md#card-0862) | 星芒凝汇 | spell | DAMAGE |
| 0863 | [Sinister Poro](card-operator-reading/0801-0900.md#card-0863) | 悚悚魄罗 | unit | PAY, MOVE |
| 0864 | [Siphon Power](card-operator-reading/0801-0900.md#card-0864) | 虹吸能量 | spell | MOD_MIGHT |
| 0865 | [Siphoning Strike](card-operator-reading/0801-0900.md#card-0865) | 汲魂痛击 | spell | DAMAGE, REPLACE, DELAY, CHANNEL |
| 0866 | [Siren of the Shallows](card-operator-reading/0801-0900.md#card-0866) | 浅滩海妖 | unit | MOD_MIGHT, MOVE |
| 0867 | [Siren’s Song](card-operator-reading/0801-0900.md#card-0867) | 海妖之歌 | spell | MOVE |
| 0868 | [Sivir, Ambitious](card-operator-reading/0801-0900.md#card-0868) | 希维尔, 远大野心 | unit | DAMAGE |
| 0869 | [Sivir, Mercenary](card-operator-reading/0801-0900.md#card-0869) | 希维尔, 险中求贵 | unit | MOD_MIGHT, GRANT_KEYWORD |
| 0870 | [Sky Cruiser](card-operator-reading/0801-0900.md#card-0870) | 天际漫游者 | unit | DISCARD, PAY, EXHAUST, DAMAGE |
| 0871 | [Sky Splitter](card-operator-reading/0801-0900.md#card-0871) | 霹天雳地 | spell | MOD_COST, DAMAGE |
| 0872 | [Skyfall of Areion](card-operator-reading/0801-0900.md#card-0872) | 阿瑞昂的陨落 | gear | ATTACH, MOD_MIGHT, MOD_TRIGGER |
| 0873 | [Skystrike Squadron](card-operator-reading/0801-0900.md#card-0873) | 鹰翼中队 | unit | TRANSFER, PAY, MOD_COST |
| 0874 | [Skyward Strike](card-operator-reading/0801-0900.md#card-0874) | 升龙踢 | spell | MOVE, STUN |
| 0875 | [Smite](card-operator-reading/0801-0900.md#card-0875) | 惩戒 | spell | DAMAGE, REPLACE, BANISH |
| 0876 | [Smoke and Mirrors](card-operator-reading/0801-0900.md#card-0876) | 镜中幻影 | spell | MOVE, DRAW |
| 0877 | [Smoke Screen](card-operator-reading/0801-0900.md#card-0877) | 烟幕弹 | spell | MOD_MIGHT |
| 0878 | [Sneaky Deckhand](card-operator-reading/0801-0900.md#card-0878) | 鬼祟的水手 | unit | PERMIT |
| 0879 | [Sneaky Zeebles](card-operator-reading/0801-0900.md#card-0879) | 古灵翼兽 | unit | ADD_RESOURCE |
| 0880 | [Soaring Scout](card-operator-reading/0801-0900.md#card-0880) | 侦察飞鹰 | unit | CHANNEL |
| 0881 | [Solari Chief](card-operator-reading/0801-0900.md#card-0881) | 烈阳首领 | unit | KILL, STUN, REPLACE |
| 0882 | [Solari Shieldbearer](card-operator-reading/0801-0900.md#card-0882) | 烈阳盾卫 | unit | STUN |
| 0883 | [Solari Shrine](card-operator-reading/0801-0900.md#card-0883) | 烈阳圣坛 | gear | EXHAUST, DRAW |
| 0884 | [Solari Sunhawk](card-operator-reading/0801-0900.md#card-0884) | 烈阳之鹰 | unit | MOD_MIGHT, GRANT_KEYWORD |
| 0885 | [Sona, Harmonious](card-operator-reading/0801-0900.md#card-0885) | 娑娜, 清心谐律 | unit | READY |
| 0886 | [Soraka, Wanderer](card-operator-reading/0801-0900.md#card-0886) | 索拉卡, 星尘逆旅 | unit | SET_RULE, REPLACE, HEAL, EXHAUST, RECALL |
| 0887 | [Soul Harvest](card-operator-reading/0801-0900.md#card-0887) | 狩魂 | spell | KILL |
| 0888 | [Soul Shepherd](card-operator-reading/0801-0900.md#card-0888) | 牧魂人 | unit | MOD_MIGHT |
| 0889 | [Soul Sword](card-operator-reading/0801-0900.md#card-0889) | 灵魂之剑 | gear | ATTACH, MOD_MIGHT |
| 0890 | [Soulgorger](card-operator-reading/0801-0900.md#card-0890) | 咂魂者 | unit | PLAY |
| 0891 | [Soulspinner](card-operator-reading/0801-0900.md#card-0891) | 织魂者 | unit | PERMIT |
| 0892 | [Soul’s Reflection](card-operator-reading/0801-0900.md#card-0892) | 流光镜影 | legend | EMPOWER, DISEMPOWER, EXHAUST, MOD_MIGHT |
| 0893 | [Spectral Centaur](card-operator-reading/0801-0900.md#card-0893) | 幽魂半人马 | unit | MOD_MIGHT |
| 0894 | [Spectral Matron](card-operator-reading/0801-0900.md#card-0894) | 幽灵主母 | unit | PLAY |
| 0895 | [Spiderling](card-operator-reading/0801-0900.md#card-0895) | 小蜘蛛 | unit | MOD_MIGHT, SET_RULE |
| 0896 | [Spinning Axe](card-operator-reading/0801-0900.md#card-0896) | 旋转飞斧 | gear | ATTACH, MOD_MIGHT |
| 0897 | [Spirit of the Forge](card-operator-reading/0801-0900.md#card-0897) | 熔炉之灵 | unit | TRANSFER, PAY, READY, MOD_MIGHT |
| 0898 | [Spirit Wheel](card-operator-reading/0801-0900.md#card-0898) | 灵魂之轮 | gear | PAY, EXHAUST, DRAW |
| 0899 | [Spirit’s Refuge](card-operator-reading/0801-0900.md#card-0899) | 奥义！魂佑 | gear | BUFF, GRANT_KEYWORD |
| 0900 | [Spoils of War](card-operator-reading/0801-0900.md#card-0900) | 以战养战 | spell | MOD_COST, DRAW |
| 0901 | [Sprite](card-operator-reading/0901-1000.md#card-0901) | 精灵 | unit | DELAY, KILL |
| 0902 | [Sprite Burst](card-operator-reading/0901-1000.md#card-0902) | 精灵迸发 | spell | CREATE, PLAY |
| 0903 | [Sprite Call](card-operator-reading/0901-1000.md#card-0903) | 精灵召唤 | spell | CREATE, PLAY |
| 0904 | [Sprite Fountain](card-operator-reading/0901-1000.md#card-0904) | 精灵提灯 | gear | CREATE, PLAY, EXECUTE_TRIGGER |
| 0905 | [Sprite Mother](card-operator-reading/0901-1000.md#card-0905) | 精灵之母 | unit | CREATE, PLAY |
| 0906 | [Sprite Queen](card-operator-reading/0901-1000.md#card-0906) | 精灵女王 | unit | CREATE, PLAY |
| 0907 | [Square Up](card-operator-reading/0901-1000.md#card-0907) | 怒吼清算 | spell | GRANT_KEYWORD, DISCARD, REPEAT |
| 0908 | [Stacked Deck](card-operator-reading/0901-1000.md#card-0908) | 卡牌骗术 | spell | LOOK, TRANSFER, RECYCLE |
| 0909 | [Stalking Wolf](card-operator-reading/0901-1000.md#card-0909) | 追猎雪狼 | unit | KILL, PAY, PERMIT |
| 0910 | [Stalwart Goatherd](card-operator-reading/0901-1000.md#card-0910) | 坚毅牧羊人 | unit | KILL |
| 0911 | [Stalwart Poro](card-operator-reading/0901-1000.md#card-0911) | 强强魄罗 | unit | MOD_MIGHT |
| 0912 | [Stand United](card-operator-reading/0901-1000.md#card-0912) | 秘奥义！慈悲度魂落 | spell | BUFF, MOD_BUFF |
| 0913 | [Star Spring](card-operator-reading/0901-1000.md#card-0913) | 流星疗泉 | battlefield | MOVE |
| 0914 | [Star-Crossed](card-operator-reading/0901-1000.md#card-0914) | 造化弄人 | spell | TRANSFER |
| 0915 | [Stare Down](card-operator-reading/0901-1000.md#card-0915) | 对峙 | spell | MOVE, XP |
| 0916 | [Stargazer](card-operator-reading/0901-1000.md#card-0916) | 观星者 | unit | MOD_COST |
| 0917 | [Starhound](card-operator-reading/0901-1000.md#card-0917) | 星獒 | unit | TRANSFER |
| 0918 | [Starry-Eyed Songstress](card-operator-reading/0901-1000.md#card-0918) | 星籁歌姬 | legend | EXHAUST, PAY, MOD_COST |
| 0919 | [Startipped Peak](card-operator-reading/0901-1000.md#card-0919) | 星尖峰 | battlefield | CHANNEL |
| 0920 | [Staunch Survivor](card-operator-reading/0901-1000.md#card-0920) | 坚毅生还者 | unit | MOD_MIGHT |
| 0921 | [Steadfast Outrider](card-operator-reading/0901-1000.md#card-0921) | 坚定游骑 | unit | MOD_MIGHT |
| 0922 | [Stealthy Pursuer](card-operator-reading/0901-1000.md#card-0922) | 隐秘追踪者 | unit | MOVE, REPLACE |
| 0923 | [Steel Paws](card-operator-reading/0901-1000.md#card-0923) | 钢爪 | unit | MOD_MIGHT |
| 0924 | [Stellacorn Herder](card-operator-reading/0901-1000.md#card-0924) | 天角牧者 | unit | DRAW |
| 0925 | [Sterak’s Gage](card-operator-reading/0901-1000.md#card-0925) | 斯特拉克的挑战护手 | gear | ATTACH, MOD_MIGHT |
| 0926 | [Stoic Ferryman](card-operator-reading/0901-1000.md#card-0926) | 冷面摆渡人 | unit | MOVE |
| 0927 | [Storm Raptor](card-operator-reading/0901-1000.md#card-0927) | 风暴锋喙鸟 | unit | DRAW |
| 0928 | [Stormbringer](card-operator-reading/0901-1000.md#card-0928) | 天声震落 | spell | DAMAGE, MOVE |
| 0929 | [Stormclaw Ursine](card-operator-reading/0901-1000.md#card-0929) | 雷爪氏族熊人 | unit | CHANNEL |
| 0930 | [Strigian Oracle](card-operator-reading/0901-1000.md#card-0930) | 翼之神谕者 | unit | PREDICT |
| 0931 | [Strike Down](card-operator-reading/0901-1000.md#card-0931) | 击倒 | spell | DAMAGE, DETACH |
| 0932 | [Stupefy](card-operator-reading/0901-1000.md#card-0932) | “敲”诈 | spell | MOD_MIGHT, DRAW |
| 0933 | [Suave Negotiator](card-operator-reading/0901-1000.md#card-0933) | 巧言说客 | unit | CHOOSE, DRAW |
| 0934 | [Sudden Storm](card-operator-reading/0901-1000.md#card-0934) | 雷霆突降 | spell | DAMAGE, REPLACE |
| 0935 | [Sumpworks Map](card-operator-reading/0901-1000.md#card-0935) | 地沟区地图 | gear | DRAW |
| 0936 | [Sun Disc](card-operator-reading/0901-1000.md#card-0936) | 太阳圆盘 | gear | EXHAUST, DELAY, ENTRY |
| 0937 | [Sunken Temple](card-operator-reading/0901-1000.md#card-0937) | 沉没神庙 | battlefield | PAY, DRAW |
| 0938 | [Sunlit Guardian](card-operator-reading/0901-1000.md#card-0938) | 日耀卫队 | unit | MOD_MIGHT, SET_RULE |
| 0939 | [Super Mega Death Rocket!](card-operator-reading/0901-1000.md#card-0939) | 超究极死神飞弹！ | spell | DAMAGE, DISCARD, TRANSFER |
| 0940 | [Supernova](card-operator-reading/0901-1000.md#card-0940) | 超新星 | spell | DAMAGE, DRAW |
| 0941 | [Svellsongur](card-operator-reading/0901-1000.md#card-0941) | 斯弗尔尚歌 | gear | ATTACH, COPY_TEXT, LINK |
| 0942 | [Swain, Visionary](card-operator-reading/0901-1000.md#card-0942) | 斯维因, 远谋卓识 | unit | SCORE |
| 0943 | [Swift Scout](card-operator-reading/0901-1000.md#card-0943) | 迅捷斥候 | legend | MOD_COST, PAY, EXHAUST, TRANSFER |
| 0944 | [Switcheroo](card-operator-reading/0901-1000.md#card-0944) | 换换乐 | spell | SWAP_MIGHT |
| 0945 | [Symbol of the Solari](card-operator-reading/0901-1000.md#card-0945) | 烈阳徽记 | gear | REPLACE, RECALL |
| 0946 | [Syndra, Transcendent](card-operator-reading/0901-1000.md#card-0946) | 辛德拉, 卓尔不凡 | unit | GRANT_KEYWORD |
| 0947 | [Tactical Retreat](card-operator-reading/0901-1000.md#card-0947) | 战术撤退 | spell | REPLACE, HEAL, EXHAUST, RECALL |
| 0948 | [Tail-Cloaked Matriarch](card-operator-reading/0901-1000.md#card-0948) | 披尾女族长 | unit | PLAY |
| 0949 | [Targonian Visionary](card-operator-reading/0901-1000.md#card-0949) | 巨神峰先知 | unit | MOD_MIGHT |
| 0950 | [Targon’s Peak](card-operator-reading/0901-1000.md#card-0950) | 巨神峰之巅 | battlefield | DELAY, READY |
| 0951 | [Taric, Protector](card-operator-reading/0901-1000.md#card-0951) | 塔里克, 坚盾 | unit | GRANT_KEYWORD |
| 0952 | [Tasty Faefolk](card-operator-reading/0901-1000.md#card-0952) | 美味仙灵 | unit | CHANNEL, DRAW |
| 0953 | [Teemo, Scout](card-operator-reading/0901-1000.md#card-0953) | 提莫, 斥候 | unit | MOD_MIGHT |
| 0954 | [Teemo, Strategist](card-operator-reading/0901-1000.md#card-0954) | 提莫, 军事家 | unit | CHOOSE, REVEAL, DAMAGE, RECYCLE |
| 0955 | [Temporal Breach](card-operator-reading/0901-1000.md#card-0955) | 时空裂隙 | spell | BANISH, PLAY |
| 0956 | [Temporal Portal](card-operator-reading/0901-1000.md#card-0956) | 预时之门 | gear | PAY, EXHAUST, DELAY, GRANT_KEYWORD |
| 0957 | [Temptation](card-operator-reading/0901-1000.md#card-0957) | 诱饵 | spell | MOVE, REPEAT |
| 0958 | [Tentacle](card-operator-reading/0901-1000.md#card-0958) | 触手 | unit | NONE |
| 0959 | [The Academy](card-operator-reading/0901-1000.md#card-0959) | 皮城学院 | battlefield | DELAY, GRANT_KEYWORD |
| 0960 | [The Arena’s Greatest](card-operator-reading/0901-1000.md#card-0960) | 荣耀竞技场 | battlefield | SCORE |
| 0961 | [The Ball](card-operator-reading/0901-1000.md#card-0961) | 魔偶 | gear | CHOOSE, DRAW, DAMAGE |
| 0962 | [The Boss](card-operator-reading/0901-1000.md#card-0962) | 腕豪 | legend | REPLACE, PAY, EXHAUST, SPEND_BUFF, HEAL, RECALL, READY |
| 0963 | [The Candlelit Sanctum](card-operator-reading/0901-1000.md#card-0963) | 烛光圣殿 | battlefield | LOOK, RECYCLE, ORDER |
| 0964 | [The Dreaming Tree](card-operator-reading/0901-1000.md#card-0964) | 幻梦之树 | battlefield | DRAW |
| 0965 | [The Empyrean](card-operator-reading/0901-1000.md#card-0965) | 苍穹腾蛟 | unit | SHOW_OFF, PREDICT, DRAW |
| 0966 | [The Exile](card-operator-reading/0901-1000.md#card-0966) | 放逐之刃 | legend | ENTRY |
| 0967 | [The Good Stuff](card-operator-reading/0901-1000.md#card-0967) | 好东西 | gear | DISCARD, DRAW, TRANSFER |
| 0968 | [The Grand Plaza](card-operator-reading/0901-1000.md#card-0968) | 宏伟广场 | battlefield | WIN |
| 0969 | [The Harrowing](card-operator-reading/0901-1000.md#card-0969) | 蚀魂夜 | spell | PLAY |
| 0970 | [The List](card-operator-reading/0901-1000.md#card-0970) | 夺命名单 | gear | NAME, EXHAUST, MOD_MIGHT |
| 0971 | [The Papertree](card-operator-reading/0901-1000.md#card-0971) | 彩纸灵树 | battlefield | CHANNEL |
| 0972 | [The Ruination](card-operator-reading/0901-1000.md#card-0972) | 破败之咒 | spell | KILL |
| 0973 | [The Syren](card-operator-reading/0901-1000.md#card-0973) | 塞壬号 | gear | PAY, EXHAUST, MOVE |
| 0974 | [The Waters’ Wage](card-operator-reading/0901-1000.md#card-0974) | 过海费 | spell | CREATE, PLAY, REPLACE |
| 0975 | [The Zero Drive](card-operator-reading/0901-1000.md#card-0975) | Z型驱动 | gear | ATTACH, MOD_MIGHT, BANISH, PLAY, LINK |
| 0976 | [Thermo Beam](card-operator-reading/0901-1000.md#card-0976) | 热电光束 | spell | KILL |
| 0977 | [Thousand-Tailed Watcher](card-operator-reading/0901-1000.md#card-0977) | 千尾监视者 | unit | MOD_MIGHT |
| 0978 | [Threshold of the Gray](card-operator-reading/0901-1000.md#card-0978) | 灰亡阈门 | battlefield | ADD_RESOURCE |
| 0979 | [Thrill of the Hunt](card-operator-reading/0901-1000.md#card-0979) | 狩猎律动 | spell | BANISH, PLAY |
| 0980 | [Thwonk!](card-operator-reading/0901-1000.md#card-0980) | 扑咚！ | spell | STUN, REPEAT |
| 0981 | [Tianna Crownguard](card-operator-reading/0901-1000.md#card-0981) | 缇亚娜·冕卫 | unit | RESTRICT |
| 0982 | [Tibbers](card-operator-reading/0901-1000.md#card-0982) | 提伯斯 | unit | DAMAGE |
| 0983 | [Tideturner](card-operator-reading/0901-1000.md#card-0983) | 控潮者 | unit | MOVE |
| 0984 | [Time Warp](card-operator-reading/0901-1000.md#card-0984) | 时间扭曲 | spell | EXTRA_TURN, BANISH |
| 0985 | [Titanic Shrine](card-operator-reading/0901-1000.md#card-0985) | 泰坦圣祠 | gear | EXHAUST, DRAW |
| 0986 | [Tomb-Raider Barbara](card-operator-reading/0901-1000.md#card-0986) | 盗墓贼芭芭拉 | unit | DISEMPOWER, KILL, REPLACE |
| 0987 | [Tools of Empire](card-operator-reading/0901-1000.md#card-0987) | 帝国工具 | gear | EXHAUST, MOD_MIGHT, REPLACE |
| 0988 | [Tornado Warrior](card-operator-reading/0901-1000.md#card-0988) | 旋风武者 | unit | EMPOWER, DELAY, DISEMPOWER |
| 0989 | [Towering Combatant](card-operator-reading/0901-1000.md#card-0989) | 魁梧斗士 | unit | MOD_MIGHT, SET_RULE |
| 0990 | [Towering Pairofant](card-operator-reading/0901-1000.md#card-0990) | 莽林巨象 | unit | ENTRY |
| 0991 | [Transpositionist](card-operator-reading/0901-1000.md#card-0991) | 易位法师 | unit | PAY, EXHAUST, TRANSFER, PLAY |
| 0992 | [Trapping Grounds](card-operator-reading/0901-1000.md#card-0992) | 捕猎场 | battlefield | CREATE, PLAY |
| 0993 | [Traveling Merchant](card-operator-reading/0901-1000.md#card-0993) | 旅行商人 | unit | DISCARD, DRAW |
| 0994 | [Treasure Hoard](card-operator-reading/0901-1000.md#card-0994) | 珍宝堆 | battlefield | PAY, CREATE, PLAY |
| 0995 | [Treasure Hunter](card-operator-reading/0901-1000.md#card-0995) | 寻宝猎人 | unit | CREATE, PLAY |
| 0996 | [Treasure Trove](card-operator-reading/0901-1000.md#card-0996) | 无主宝藏 | gear | DRAW, CHANNEL, PAY, EXHAUST, KILL |
| 0997 | [Trevor Snoozebottom](card-operator-reading/0901-1000.md#card-0997) | 特雷弗·达顿尔 | unit | CREATE, PLAY |
| 0998 | [Tricksy Tentacles](card-operator-reading/0901-1000.md#card-0998) | 顽皮触手 | spell | MOVE |
| 0999 | [Trifarian Captain](card-operator-reading/0901-1000.md#card-0999) | 崔法利队长 | unit | LOOK, REVEAL, DRAW, RECYCLE |
| 1000 | [Trifarian Gloryseeker](card-operator-reading/0901-1000.md#card-1000) | 崔法利求战者 | unit | BUFF |
| 1001 | [Trifarian War Camp](card-operator-reading/1001-1100.md#card-1001) | 崔法利兵营 | battlefield | MOD_MIGHT |
| 1002 | [Trinity Force](card-operator-reading/1001-1100.md#card-1002) | 三相之力 | gear | ATTACH, MOD_MIGHT, SCORE |
| 1003 | [Trinket Peddler](card-operator-reading/1001-1100.md#card-1003) | 饰品商贩 | unit | MOD_MIGHT |
| 1004 | [Trove Golem](card-operator-reading/1001-1100.md#card-1004) | 宝藏魔像 | unit | CREATE, PLAY |
| 1005 | [Trusty Ramhound](card-operator-reading/1001-1100.md#card-1005) | 可靠攻城犬 | unit | MOD_MIGHT |
| 1006 | [Tryndamere, Barbarian](card-operator-reading/1001-1100.md#card-1006) | 泰达米尔, 凛冽凶蛮 | unit | SCORE |
| 1007 | [Turn to Dust](card-operator-reading/1001-1100.md#card-1007) | 化为灰烬 | spell | GRANT_KEYWORD |
| 1008 | [Twilight Reveler](card-operator-reading/1001-1100.md#card-1008) | 暮光狂舞者 | unit | READY |
| 1009 | [Twilight Shroud](card-operator-reading/1001-1100.md#card-1009) | 我流奥义！霞阵 | spell | MOD_MIGHT, RESTRICT |
| 1010 | [Twilight Step](card-operator-reading/1001-1100.md#card-1010) | 奥义！幽步 | spell | MOVE |
| 1011 | [Twisted Fate, Gambler](card-operator-reading/1001-1100.md#card-1011) | 崔斯特, 赌徒 | unit | REVEAL, RECYCLE, DAMAGE, DRAW, STUN |
| 1012 | [Udyr, Wildman](card-operator-reading/1001-1100.md#card-1012) | 乌迪尔, 荒野化身 | unit | SPEND_BUFF, CHOOSE, DAMAGE, STUN, READY, GRANT_KEYWORD |
| 1013 | [Ultrasoft Poro](card-operator-reading/1001-1100.md#card-1013) | 绵绵魄罗 | unit | EXHAUST, CREATE, PLAY |
| 1014 | [Unchecked Power](card-operator-reading/1001-1100.md#card-1014) | 过载能量 | spell | EXHAUST, DAMAGE |
| 1015 | [Undercover Agent](card-operator-reading/1001-1100.md#card-1015) | 卧底特工 | unit | DISCARD, DRAW |
| 1016 | [Undertitan](card-operator-reading/1001-1100.md#card-1016) | 垓兽 | unit | MOD_MIGHT, ADD_RESOURCE, REPLACE |
| 1017 | [Undying Legion](card-operator-reading/1001-1100.md#card-1017) | 不死军团 | unit | PERMIT, MOD_COST |
| 1018 | [Undying Loyalty](card-operator-reading/1001-1100.md#card-1018) | 忠诚不渝 | spell | MOD_COST, PLAY |
| 1019 | [Unforgiven](card-operator-reading/1001-1100.md#card-1019) | 疾风剑豪 | legend | PAY, EXHAUST, MOVE |
| 1020 | [Unlicensed Armory](card-operator-reading/1001-1100.md#card-1020) | 来路不明的武器 | gear | DISCARD, EXHAUST, DELAY, REPLACE, PAY, HEAL, RECALL |
| 1021 | [Unsung Hero](card-operator-reading/1001-1100.md#card-1021) | 无名英雄 | unit | DRAW |
| 1022 | [Unyielding Spirit](card-operator-reading/1001-1100.md#card-1022) | 坚毅不倒 | spell | PREVENT_DAMAGE |
| 1023 | [Up from the Deep](card-operator-reading/1001-1100.md#card-1023) | 深渊之触 | spell | CREATE, PLAY |
| 1024 | [Upstage Comedy](card-operator-reading/1001-1100.md#card-1024) | 大幕渐起 | spell | READY, REPEAT |
| 1025 | [Valley of Idols](card-operator-reading/1001-1100.md#card-1025) | 偶像谷 | battlefield | PAY, BUFF |
| 1026 | [Vanguard Armory](card-operator-reading/1001-1100.md#card-1026) | 先锋军备 | gear | EXHAUST, CREATE, PLAY |
| 1027 | [Vanguard Attendant](card-operator-reading/1001-1100.md#card-1027) | 先锋扈从 | unit | ENTRY |
| 1028 | [Vanguard Captain](card-operator-reading/1001-1100.md#card-1028) | 先锋队长 | unit | CREATE, PLAY |
| 1029 | [Vanguard Helm](card-operator-reading/1001-1100.md#card-1029) | 先锋之盔 | gear | BUFF |
| 1030 | [Vanguard Sergeant](card-operator-reading/1001-1100.md#card-1030) | 先锋中士 | unit | NONE |
| 1031 | [Vault Breaker](card-operator-reading/1001-1100.md#card-1031) | 强能冲拳 | spell | GRANT_KEYWORD |
| 1032 | [Vaults of Helia](card-operator-reading/1001-1100.md#card-1032) | 海力亚秘库 | battlefield | MOD_COST, DELAY |
| 1033 | [Vayne, Hunter](card-operator-reading/1001-1100.md#card-1033) | 薇恩, 追猎者 | unit | ENTRY, PAY, TRANSFER |
| 1034 | [Veiled Temple](card-operator-reading/1001-1100.md#card-1034) | 月帷祭坛 | battlefield | READY, DETACH |
| 1035 | [Vengeance](card-operator-reading/1001-1100.md#card-1035) | 复仇 | spell | KILL |
| 1036 | [Veteran Poro](card-operator-reading/1001-1100.md#card-1036) | 壮壮魄罗 | unit | ATTACH, MOD_COST, PAY |
| 1037 | [Vex, Apathetic](card-operator-reading/1001-1100.md#card-1037) | 薇古丝, 冷眼旁观 | unit | STUN, RESTRICT |
| 1038 | [Vex, Cheerless](card-operator-reading/1001-1100.md#card-1038) | 薇古丝, 郁郁 | unit | MOD_COST |
| 1039 | [Vex, Mocking](card-operator-reading/1001-1100.md#card-1039) | 薇古丝, 玩世不恭 | unit | MOVE |
| 1040 | [Vi, Destructive](card-operator-reading/1001-1100.md#card-1040) | 蔚, 铲除者 | unit | RECYCLE, MOD_MIGHT |
| 1041 | [Vi, Hotheaded](card-operator-reading/1001-1100.md#card-1041) | 蔚, 火爆铁拳 | unit | PAY, SET_MIGHT |
| 1042 | [Vi, Peacekeeper](card-operator-reading/1001-1100.md#card-1042) | 蔚, 和平卫士 | unit | STUN |
| 1043 | [Vicious Snapjaws](card-operator-reading/1001-1100.md#card-1043) | 凶残颚鱼 | unit | XP |
| 1044 | [Viktor, Innovator](card-operator-reading/1001-1100.md#card-1044) | 维克托, 创见先驱 | unit | CREATE, PLAY |
| 1045 | [Viktor, Leader](card-operator-reading/1001-1100.md#card-1045) | 维克托, 领袖 | unit | CREATE, PLAY |
| 1046 | [Vilemaw](card-operator-reading/1001-1100.md#card-1046) | 卑鄙之喉 | unit | RESTRICT, DRAW |
| 1047 | [Vilemaw’s Lair](card-operator-reading/1001-1100.md#card-1047) | 卑鄙之喉的巢穴 | battlefield | RESTRICT |
| 1048 | [Virtuoso](card-operator-reading/1001-1100.md#card-1048) | 戏命师 | legend | BANISH, LINK, TRANSFER, CHANNEL, DRAW |
| 1049 | [Void Assault](card-operator-reading/1001-1100.md#card-1049) | 虚空来袭 | spell | MOVE |
| 1050 | [Void Burrower](card-operator-reading/1001-1100.md#card-1050) | 虚空遁地兽 | legend | EXHAUST, REVEAL, BANISH, PLAY, RECYCLE |
| 1051 | [Void Drone](card-operator-reading/1001-1100.md#card-1051) | 虚空蜢 | unit | MOD_COST |
| 1052 | [Void Gate](card-operator-reading/1001-1100.md#card-1052) | 虚空之门 | battlefield | MOD_DAMAGE |
| 1053 | [Void Hatchling](card-operator-reading/1001-1100.md#card-1053) | 虚空兽苗 | unit | REPLACE, LOOK, RECYCLE, REVEAL |
| 1054 | [Void Rush](card-operator-reading/1001-1100.md#card-1054) | 虚空猛冲 | spell | REVEAL, BANISH, PLAY, MOD_COST, DRAW |
| 1055 | [Void Seeker](card-operator-reading/1001-1100.md#card-1055) | 虚空索敌 | spell | DAMAGE, DRAW |
| 1056 | [Voidreaver](card-operator-reading/1001-1100.md#card-1056) | 虚空掠夺者 | legend | XP, EXHAUST, BUFF, MOVE |
| 1057 | [Volibear, Furious](card-operator-reading/1001-1100.md#card-1057) | 沃利贝尔, 震怒天声 | unit | DAMAGE |
| 1058 | [Volibear, Imposing](card-operator-reading/1001-1100.md#card-1058) | 沃利贝尔, 雄浑巨力 | unit | DRAW |
| 1059 | [Voracious Gromp](card-operator-reading/1001-1100.md#card-1059) | 贪食魔沼蛙 | unit | XP |
| 1060 | [Wages of Pain](card-operator-reading/1001-1100.md#card-1060) | 痛苦之酬 | spell | DAMAGE, CREATE, PLAY |
| 1061 | [Walking Roost](card-operator-reading/1001-1100.md#card-1061) | 移动栖木 | unit | CHOOSE, CREATE, PLAY |
| 1062 | [Wallop](card-operator-reading/1001-1100.md#card-1062) | 痛殴 | spell | SPEND_BUFF, PAY, MOD_COST, READY |
| 1063 | [War Scout](card-operator-reading/1001-1100.md#card-1063) | 战争斥候 | unit | MOD_MIGHT |
| 1064 | [Warmog’s Armor](card-operator-reading/1001-1100.md#card-1064) | 狂徒铠甲 | gear | ATTACH, MOD_MIGHT, BUFF |
| 1065 | [Warwick, Hunter](card-operator-reading/1001-1100.md#card-1065) | 沃里克, 追猎者 | unit | ENTRY, KILL |
| 1066 | [Watchful Curator](card-operator-reading/1001-1100.md#card-1066) | 警觉的收藏家 | unit | GRANT_KEYWORD |
| 1067 | [Watchful Sentry](card-operator-reading/1001-1100.md#card-1067) | 警觉的哨兵 | unit | DRAW |
| 1068 | [Whirling Twirligig](card-operator-reading/1001-1100.md#card-1068) | 旋转陀螺机 | gear | EXHAUST, KILL, CREATE, PLAY |
| 1069 | [Whirlwind](card-operator-reading/1001-1100.md#card-1069) | 飓风席卷 | spell | ORDER, TRANSFER |
| 1070 | [Whiteflame Protector](card-operator-reading/1001-1100.md#card-1070) | 苍炎守护者 | unit | MOD_MIGHT |
| 1071 | [Wielder of Water](card-operator-reading/1001-1100.md#card-1071) | 驭水者 | unit | MOD_MIGHT |
| 1072 | [Wild Claw](card-operator-reading/1001-1100.md#card-1072) | 狂野钩爪 | spell | LOOK, BANISH, PLAY, MOD_COST, RECYCLE, EMPOWER, DELAY |
| 1073 | [Wildclaw Shaman](card-operator-reading/1001-1100.md#card-1073) | 野爪萨满 | unit | SPEND_BUFF, BUFF, READY |
| 1074 | [Wily Newtfish](card-operator-reading/1001-1100.md#card-1074) | 狡猾的蝾螈 | unit | MOD_MIGHT, GRANT_KEYWORD |
| 1075 | [Wind and Ghosts](card-operator-reading/1001-1100.md#card-1075) | 风灵瞬转 | spell | CHOOSE, BANISH, TRANSFER |
| 1076 | [Wind Wall](card-operator-reading/1001-1100.md#card-1076) | 风之障壁 | spell | COUNTER |
| 1077 | [Windsinger](card-operator-reading/1001-1100.md#card-1077) | 吟风翼 | unit | TRANSFER |
| 1078 | [Windswept Hillock](card-operator-reading/1001-1100.md#card-1078) | 疾风山丘 | battlefield | GRANT_KEYWORD |
| 1079 | [Wizened Elder](card-operator-reading/1001-1100.md#card-1079) | 睿智长者 | unit | MOD_MIGHT |
| 1080 | [World Atlas](card-operator-reading/1001-1100.md#card-1080) | 云游图鉴 | gear | ATTACH, MOD_MIGHT, CREATE, PLAY |
| 1081 | [Wraith of Echoes](card-operator-reading/1001-1100.md#card-1081) | 残响之魂 | unit | DRAW |
| 1082 | [Wrath of the Freljord](card-operator-reading/1001-1100.md#card-1082) | 弗雷尔卓德之怒 | unit | ENTRY, MOD_MIGHT |
| 1083 | [Wuju Apprentice](card-operator-reading/1001-1100.md#card-1083) | 无极学徒 | unit | DRAW |
| 1084 | [Wuju Bladesman, Starter](card-operator-reading/1001-1100.md#card-1084) | 无极剑圣, 入门 | legend | MOD_MIGHT |
| 1085 | [Wuju Master](card-operator-reading/1001-1100.md#card-1085) | 无极宗师 | legend | MOD_MIGHT, ENTRY |
| 1086 | [Xerath, Freed](card-operator-reading/1001-1100.md#card-1086) | 泽拉斯, 无边能量 | unit | PAY, EXHAUST, DAMAGE, RESTRICT |
| 1087 | [Xin Zhao, Vigilant](card-operator-reading/1001-1100.md#card-1087) | 赵信, 千夫所向 | unit | ENTRY |
| 1088 | [XP Tracker](card-operator-reading/1001-1100.md#card-1088) | XP Tracker | other | XP, SET_RULE |
| 1089 | [Yasuo, Remorseful](card-operator-reading/1001-1100.md#card-1089) | 亚索, 迷途怅惘 | unit | DAMAGE |
| 1090 | [Yasuo, Windrider](card-operator-reading/1001-1100.md#card-1090) | 亚索, 乘风归 | unit | SCORE |
| 1091 | [Yeti Brawler](card-operator-reading/1001-1100.md#card-1091) | 雪人斗士 | unit | CREATE, PLAY |
| 1092 | [Yone, Blademaster](card-operator-reading/1001-1100.md#card-1092) | 永恩, 一剑封尘 | unit | DAMAGE |
| 1093 | [Yordle Explorer](card-operator-reading/1001-1100.md#card-1093) | 约德尔探险家 | unit | DRAW |
| 1094 | [Yuumi, Magical Cat](card-operator-reading/1001-1100.md#card-1094) | 悠米, 魔法猫咪 | unit | MOD_MIGHT, GRANT_KEYWORD |
| 1095 | [Zaun Punk](card-operator-reading/1001-1100.md#card-1095) | 祖安混混 | unit | KILL, PAY |
| 1096 | [Zaun Warrens](card-operator-reading/1001-1100.md#card-1096) | 祖安地沟 | battlefield | DISCARD, DRAW |
| 1097 | [Zaunite Bouncer](card-operator-reading/1001-1100.md#card-1097) | 祖安保镖 | unit | TRANSFER |
| 1098 | [Zed, From the Shadows](card-operator-reading/1001-1100.md#card-1098) | 劫, 禁忌之影 | unit | DISCARD, PAY, CREATE, PLAY |
| 1099 | [Zed, Without a Sound](card-operator-reading/1001-1100.md#card-1099) | 劫, 落影无声 | unit | CREATE, PLAY, PAY, MOVE |
| 1100 | [Zenith Blade](card-operator-reading/1001-1100.md#card-1100) | 天顶之刃 | spell | STUN, MOVE |
| 1101 | [Zephyr Sage](card-operator-reading/1101-1106.md#card-1101) | 和风贤者 | unit | MOD_MIGHT |
| 1102 | [Zero Point Inflection](card-operator-reading/1101-1106.md#card-1102) | 临界零点 | gear | DRAW, DISCARD, KILL, SCORE |
| 1103 | [Zhonya’s Hourglass](card-operator-reading/1101-1106.md#card-1103) | 中娅沙漏 | gear | REPLACE, KILL, HEAL, EXHAUST, RECALL |
| 1104 | [Ziggs, Explosive](card-operator-reading/1101-1106.md#card-1104) | 吉格斯, 狂轰滥炸 | unit | PAY, EXHAUST, CREATE, PLAY, KILL, MOD_MIGHT |
| 1105 | [Ziggs, Short-Fused](card-operator-reading/1101-1106.md#card-1105) | 吉格斯, 炸欢天 | unit | CREATE, PLAY, MOD_DAMAGE |
| 1106 | [Zilean, Time Mage](card-operator-reading/1101-1106.md#card-1106) | 基兰, 时间法师 | unit | REPLACE, CREATE, PLAY, COPY |

## 词汇使用计数

这是人工笔记显式列出的词汇次数；关键词内部展开未一律重复计入，不能解释为各类效果的统计总量。

| ID | 涉及笔记数 |
| --- | ---: |
| `ADD_LEGEND` | 1 |
| `ADD_RESOURCE` | 34 |
| `ATTACH` | 55 |
| `BANISH` | 37 |
| `BUFF` | 40 |
| `BURN` | 9 |
| `CHANNEL` | 32 |
| `CHOOSE` | 58 |
| `CONTROL` | 7 |
| `COPY` | 6 |
| `COPY_ABILITY` | 1 |
| `COPY_TEXT` | 1 |
| `COUNTER` | 12 |
| `CREATE` | 97 |
| `DAMAGE` | 96 |
| `DELAY` | 43 |
| `DETACH` | 4 |
| `DISCARD` | 36 |
| `DISEMPOWER` | 13 |
| `DRAW` | 151 |
| `EMPOWER` | 11 |
| `ENTRY` | 49 |
| `EXECUTE_TRIGGER` | 2 |
| `EXHAUST` | 132 |
| `EXTRA_TURN` | 1 |
| `GRANT_ABILITY` | 7 |
| `GRANT_KEYWORD` | 94 |
| `HEAL` | 10 |
| `HIDE` | 1 |
| `IF_DO` | 14 |
| `IGNORE_ABILITY` | 3 |
| `KILL` | 79 |
| `LINK` | 12 |
| `LOOK` | 17 |
| `MOD_BUFF` | 1 |
| `MOD_COST` | 75 |
| `MOD_DAMAGE` | 8 |
| `MOD_EFFECT` | 1 |
| `MOD_KEYWORD` | 3 |
| `MOD_MIGHT` | 226 |
| `MOD_RESOURCE` | 1 |
| `MOD_TRIGGER` | 6 |
| `MOVE` | 65 |
| `NAME` | 4 |
| `NONE` | 9 |
| `ORDER` | 5 |
| `PAY` | 133 |
| `PERMIT` | 28 |
| `PLAY` | 144 |
| `PREDICT` | 17 |
| `PREVENT_DAMAGE` | 5 |
| `READY` | 66 |
| `RECALL` | 15 |
| `RECHOOSE` | 2 |
| `RECYCLE` | 51 |
| `REPEAT` | 25 |
| `REPLACE` | 44 |
| `REPLACE_BATTLEFIELD` | 2 |
| `RESTRICT` | 41 |
| `RESTRICT_RESOURCE` | 6 |
| `REVEAL` | 30 |
| `SCORE` | 16 |
| `SETUP_CHOICE` | 1 |
| `SET_BASE_MIGHT` | 5 |
| `SET_MIGHT` | 6 |
| `SET_RULE` | 19 |
| `SET_TAG` | 2 |
| `SET_TYPE` | 1 |
| `SHOW_OFF` | 6 |
| `SKIP_PHASE` | 1 |
| `SPEND_BUFF` | 11 |
| `STUN` | 26 |
| `SWAP_MIGHT` | 1 |
| `TRANSFER` | 53 |
| `WIN` | 2 |
| `XP` | 28 |
