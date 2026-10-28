# RiftAtlas Power 数据依据

本目录归档公开前端目录和费用显示组件，不需要账户、API 密钥或运行第三方 JavaScript。

- `card-catalog.js`：[公开卡牌目录发布文件](https://riftatlas.com/_next/static/immutable/chunks/43w1rdkmt0ytg.js)，共 1,530 条源记录。
- `cost-renderer.js`：[费用显示组件](https://riftatlas.com/_next/static/immutable/chunks/3yjnba3ykwj5_.js)。其表达式 `"number"==typeof d.powerCost?Math.max(0,Math.trunc(d.powerCost)):0` 明确规定省略的 `powerCost` 显示为 0。
- `catalog.json`：用 Python 解析数据字面量后的原始目录。解析通过词法转换和 `ast.literal_eval` 完成，没有执行下载的代码。

领域选择依据项目存档的官方核心规则 135.2.e.6：自身领域 Power，多领域可用任一自身领域，中立／无领域可用任意领域。它不是按卡牌颜色随意猜费用，而是结合源目录的数量和明确规则生成选择组。

同步只更新当前主牌库的 Power 及其来源字段。按完整编号匹配；本地 `-STAR` 与 RiftAtlas `S` 后缀的映射要求源目录同时明确声明 `isAltArt` 和 `baseCardId`，不会靠截断编号猜基础印刷。名称大小写、标点、签名牌名称布局及三条已核对的拼写差异单独处理。

同步报告为 [riftatlas-power-sync.json](../../../reports/riftatlas-power-sync.json)，记录来源哈希、费用分组、逐条原值与新值、备份和三条未修改的非 Power 属性差异。源目录固定到此次发布版本；若该发布 URL 失效，应重新核对公开发布，不能自动套用不明结构。

图文卡牌页可能展示比原始目录更新的勘误。此次归档仅作为 Power 来源，不据此认证原始文本是最新规则，也未批量覆盖本地效果文本。
