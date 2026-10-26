# TCG 构筑研究：功能模块与选牌依据

整理日期：2026-10-25。

本文件保存对公开一手资料的中文摘要、原文链接及本项目的设计推论，供离线查阅。没有收录文章全文或图片；进一步核对语境时访问原文。资料讨论的是构筑方法，历史牌表及其数量不代表当前环境，也不是 Riftbound 的规则来源。

## 使用场景

设计 `core_plan`、`deck_skeleton`、`card_selection` 的交互与数据结构，或审查模块划分是否合理时阅读。实际单卡效果、身份、领域和合法性仍以本地 Riftbound CLI 与规则快照为准。

## 高价值来源

### S1：快攻的任务一致性

- 标题：Aggro Decks
- 作者：Reid Duke
- 发布者：Wizards of the Coast
- 日期：2014-09-29
- 原文：[Aggro Decks](https://magic.wizards.com/en/news/feature/aggro-decks-2014-09-29)

原文要点摘要：快攻围绕快速威胁和资源效率组织；有限的应对牌应优先处理阻挡进攻的障碍。每张牌都应服务共同的进攻计划，不必依靠独立的大型终结牌。

对项目的启示：同是去除牌，在快攻里可能承担“突破防线”的任务。不要因为某张牌能解场，就认定它适合所有套牌。

### S2：控制先证明后期获胜能力

- 标题：Control Decks
- 作者：Reid Duke
- 发布者：Wizards of the Coast
- 日期：2014-10-06
- 原文：[Control Decks](https://magic.wizards.com/en/news/feature/control-decks-2014-10-06)

原文要点摘要：控制构筑首先要确保拖长比赛后具有足够优势，再配置早期防守。防守工具可以是去除、反制或阻挡单位；卡牌优势、长期获胜能力和防守共同构成计划。

对项目的启示：模块要覆盖完整获胜过程。“活下来”必须有后续收益；快攻的选牌顺序不应直接用于控制。

### S3：一牌多职与角色转换

- 标题：Midrange Decks
- 作者：Reid Duke
- 发布者：Wizards of the Coast
- 日期：2014-10-27
- 原文：[Midrange Decks](https://magic.wizards.com/en/news/feature/midrange-decks-2014-10-27)

原文要点摘要：中速依靠适应性，选择既能防守稳定局面、又能转入进攻的威胁。单位还可以提供资源或长期收益；套牌需要具备从防守转为主动结束比赛的能力。

对项目的启示：卡牌可有多个功能，但必须描述其适用场面。领先、均势和落后时的价值需要分别判断。

### S4：资源基础参与整个构筑过程

- 标题：Building a Mana base
- 作者：Reid Duke
- 发布者：Wizards of the Coast
- 日期：2014-11-24
- 原文：[Building a Mana base](https://magic.wizards.com/en/news/feature/building-mana-base-2014-11-24)

原文要点摘要：资源基础决定一套牌实际能完成哪些行动，应与其他卡牌共同设计，不能只在选完非地牌后补足空位。

对项目的启示：在核心机制和骨架阶段就评估资源要求。后续 `resources` 阶段负责集中确认与修正，不代表此前不检查资源。

### S5：围绕实际计划组织攻击者、引擎和支援

- 标题：Pokémon TCG Strategy: Charging Up Your Deck with Eelektrik
- 作者：Stephane Ivanoff
- 发布者：The Pokémon Company / Pokémon.com
- 日期：2025-08-14
- 原文：[Eelektrik 构筑分析](https://www.pokemon.com/us/features/pokemon-tcg-strategy-charging-up-your-deck-with-eelektrik)

原文要点摘要：文章将前期攻击、后期攻击、能量加速与回收连接为计划，再配置检索、补牌、移动及目标选择。部分卡牌兼具攻击和检索等作用，资源数量也受加速方式影响。

对项目的启示：启动、续航和获胜输出应分别检查；研究组件之间的依赖，比按卡牌类型分堆更有用。

访问情况：直接打开页面只返回 iframe；正文经官方域名的搜索索引核对。

### S6：从预期回合动作反推资源需求

- 标题：Jump Start: Understanding Card Choices and Pitch Ratios in Deck-Building
- 发布者：Legend Story Studios / Flesh and Blood 官方站
- 原文：[Card Choices and Pitch Ratios](https://legacy.fabtcg.com/en/articles/jump-start-understanding-card-choices-and-pitch-ratios-in-deck-building/)

原文要点摘要：资源配置应取决于套牌希望在一回合完成的行动。卡牌的输出和资源价值存在取舍；英雄机制也会改变所需的资源比例。

对项目的启示：比较整组行动的可支付性，而非只看平均费用；不要搬用其他游戏的比例。

访问情况：旧站直接访问返回 502；要点来自官方页面的搜索索引。作者、确切发布日期未在此次核对中确认，后续需要全文细节时重新获取。

## 如何用于本项目

由这些资料推导的功能词表、模块计数规则和选牌循环，统一维护在 [Pipeline](../deckbuilding-pipeline.md)。它们是本项目的综合设计，并非上述作者共同提出的统一标准。

数量目标需要依据；不能从其他游戏的历史案例推导 Riftbound 的固定比例、胜率、强度评分或自动选牌公式。
