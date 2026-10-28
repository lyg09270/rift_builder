# TCG 卡牌评分与构筑研究

保存原始论文 PDF，不改写正文。下载来源、版本、页数、时间和 SHA-256 见 [manifest.json](manifest.json)。

建议先读 1、2、3；4、5 用于后续环境和统计验证；6、7 用于卡牌表示与数据驱动构筑。

## 1. [Learning a Resource Scale for Collectible Card Games](2019-learning-a-resource-scale.pdf)

- 年份与出处：2019；IEEE Conference on Games (CoG)
- 优先级：核心，建议第一个阅读
- 对应问题：学习属性、效果文本与资源费用之间的关系；建立身材和效果的费用参照。
- 解释边界：预测印刷费用，不直接预测入选价值或获胜贡献。
- 保存版本：conference PDF；8 页
- 原始来源：https://ieee-cog.org/2019/papers/paper_119.pdf

## 2. [Evolving Evaluation Functions for Collectible Card Game AI](2022-evolving-evaluation-functions.pdf)

- 年份与出处：2022；ICAART 2022; arXiv preprint 2021
- 优先级：核心，建议第二个阅读
- 对应问题：单卡与场面特征评分；线性和树状表示；评分参数的对局验证。
- 解释边界：LOCM 的规则与特征不同，不能直接移植评分权重。
- 保存版本：published conference PDF；8 页
- 原始来源：https://www.scitepress.org/Papers/2022/108069/108069.pdf

## 3. [Q-DeckRec: A Fast Deck Recommendation System for Collectible Card Games](2018-q-deckrec.pdf)

- 年份与出处：2018；IEEE CIG 2018; arXiv:1806.09771
- 优先级：核心，建议第三个阅读
- 对应问题：把构筑视为依赖当前套牌与对手的连续修改和搜索问题。
- 解释边界：训练与评价依赖模拟器及代理打法；不提供跨游戏通用单卡分。
- 保存版本：author preprint on arXiv；8 页
- 原始来源：https://arxiv.org/pdf/1806.09771

## 4. [Chaos Cards: Creating Novel Digital Card Games through Grammatical Content Generation and Meta-Based Card Evaluation](2020-chaos-cards-meta-based-evaluation.pdf)

- 年份与出处：2020；AAAI AIIDE 2020
- 优先级：核心，后续强度验证参考
- 对应问题：可执行卡牌效果、竞争套牌环境中的模拟评分，以及快速预测。
- 解释边界：研究使用作者自己的 Hearthstone 类游戏，需要可靠的游戏实现。
- 保存版本：published conference PDF；7 页
- 原始来源：https://cdn.aaai.org/ojs/7430/7430-52-10748-1-2-20200923.pdf

## 5. [Evolving the Hearthstone Meta](2019-evolving-the-hearthstone-meta.pdf)

- 年份与出处：2019；IEEE CoG 2019; arXiv:1907.01623
- 优先级：核心，统计指标参考
- 对应问题：打出胜率、抽到胜率和修改费用后的对局影响。
- 解释边界：观测条件胜率不等同于替换卡位产生的因果收益。
- 保存版本：conference PDF；8 页
- 原始来源：https://ieee-cog.org/2019/papers/paper_134.pdf

## 6. [Learning With Generalised Card Representations for Magic: The Gathering](2024-generalised-card-representations.pdf)

- 年份与出处：2024；IEEE CoG 2024; arXiv:2407.05879
- 优先级：补充，卡牌表示参考
- 对应问题：结合数值、类别与文本表示卡牌，支持未知卡牌的选牌预测。
- 解释边界：预测玩家选牌不等同于预测胜率或单卡真实强度。
- 保存版本：author preprint on arXiv；8 页
- 原始来源：https://arxiv.org/pdf/2407.05879

## 7. [Predicting Drafted Deck Strength for Magic: the Gathering](2026-predicting-drafted-deck-strength.pdf)

- 年份与出处：2026；arXiv:2607.04782; paper reports acceptance at CoG 2026
- 优先级：补充，结果导向的套牌模型参考
- 对应问题：从卡牌和轮抽上下文预测最终套牌对局表现。
- 解释边界：较新的数据驱动方法；依赖大量 MTG 数据，不能直接迁移到符文战场。
- 保存版本：author preprint on arXiv；4 页
- 原始来源：https://arxiv.org/pdf/2607.04782

## 未取得公开全文的相关论文

- [Deep Learning Techniques for Explainable Resource Scales in Collectible Card Games](https://doi.org/10.1109/TG.2020.3030742)（2022）：未找到可公开取得的全文 PDF；已保存同一研究路线的 2019 年会议论文。
- [Deck Building in Collectible Card Games using Genetic Algorithms: A Case Study of Legends of Code and Magic](https://web.ntnu.edu.tw/~tcchiang/publications/ssci2021a.htm)（2021）：作者页面目前仅提供 DOI；未找到开放全文，不以摘要或目录充当论文。

## 复核与重新下载

运行 `python download_papers.py`（需要 pypdf）。已有 PDF 会复核且保留，不自动覆盖。
