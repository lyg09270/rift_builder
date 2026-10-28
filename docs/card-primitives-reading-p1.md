# P1逐卡复读与编写约定

[本轮覆盖报告](card-primitives-coverage-p1.md) · [冻结原语参考](basic-primitives-v4-p1-frozen.md) · [35原语草案](basic-primitives-v4-p1.md)

本轮固定分母为本地OpenRift目录的1106个卡牌本体。逐卡重新读取全部可用EN/SC/TC规则、装备效果、属性、背面与目录勘误，再独立记录入口、绑定、P1展开和结论。旧R3程序只作候选输入，不能自动继承通过状态。

## 阅读与覆盖口径

- covered：该卡所有能力与固有关键词均能在现有卡牌模型、明确规则模板和冻结35原语中表达，没有本轮已知缺口或待裁定语义。
- verify：已读，但规则解释、数据、复制取值或费用政策等尚不足以确认完整分解。
- uncovered：已读，但冻结契约缺少必需结构／字段，不能以未登记参数或自然语言占位补过。
- 目录检索keywords不是固有能力清单；被授予、衍生物提醒、状态描述与动作名按实际文字归属。DATA/LANG来源问题独立保留，不擅自修改原文。

确认表达覆盖率按covered/1106计算；未读及待核不进分子。程序调用检查只检验名称、签名与结构，不代表独立测得的游戏执行正确率。卡面文本完整复读也不等于所有印刷图片逐图视觉核验。

## 展开代码如何阅读

代码是静态符号程序，不是Python游戏引擎。`p`只调用冻结API的35个原语；`flow`表示V4程序节点；`action_frame`和`phase`是描述模板作用域及阶段的编写记法，不新增基本算子，也不提供任意文本执行功能。

```text
完整的卡牌入口和参数绑定
→ action_frame(已登记模板名, 原始实参)
→ 该模板固定协议处理选择、费用、替代与事件阶段
→ p原语按真实阶段提交实际状态
→ frame.result按原动作身份返回实际结果
```

同一张卡的独立能力／延迟体分片列出，只在各自入口执行，不能把整页所有片段串行运行。共享上下文、link或回执须显式绑定。暂未补齐的模板实现与未决规则不能因此获得运行认证。

## ActionFrame的派生字段

原始实参保存在每个frame头，卡牌具体数值不会丢进抽象模板名。以下字段由具名协议确定，不能任意填值：

| 字段 | 来源与类型 |
| --- | --- |
| objects、origin、destination | 原动作实际选择的集合及源／目的区域映射；draw/discard/kill等各自规则独立 |
| owner_decks、owner_trash、owner_banishment | 每张真实对象拥有者的对应区域；不是当前控制者区域 |
| board、entry、entry_locations | 合法Board入场区域、经过费用与替代后的初态和地点；与原选择位置分开 |
| chain_zone、leave_destination | 对应item的真实链区域及离链目的地，仍处理Flow等替代 |
| new_template、template、count、owner、controller | 新模板实例化信息；现有卡不再实例化，出生仅绑定待提交实例 |
| snapshot_change | set/swap/上下限按本次共同快照算出的数值差，不持续设定最终战力 |
| actual_damage_map | 伤害分配、Bonus、预防和替代后的实际数值与因果记录，不能直接等于请求量 |
| count_map、stack_operation | 实际请求的逐对象数量及闭集增益／强化操作；真实消耗另记收据 |
| ability、keyword_definitions、patch、copy_view | 结构化能力／关键词展开／受限元数据补丁／复制投影；不接受原文代执行 |
| rule、scope、change、limit、link | 对应分域规则的类型化记录与作用域；字段必须属于该API闭集 |
| result | 保留具名动作实际回执类型；kill返回真实死亡者，不能把任何区域迁移都算死亡；PaymentReceipt独立 |

这些字段表示依V4具名协议和本轮具体绑定进行的符号求值，不代表已有可调用的Frame实现。缺少契约字段时明确判未覆盖；无法确认求值方式时判待核。

`play`按start、enter_permanent、spell_leave_chain分阶段列出；后两个阶段只有在统一打出／链流程真正到达时执行。关键词Predict与ShowOff按其既有V4结构宏展开信息授权、选择、回收／排序或展示，不增加P1原语。

## 固有关键词参数绑定

每张的native列表由本轮读卡后记录，不从目录索引整批复制。`:body`表示该关键词已在正文分片完整展开，`:condition`／`:entry`表示已绑定对应条件或入口；其余关键词另列原语分片。重复授予关键词时沿用同一KeywordSpec来源身份，不把子能力当成多个关键词。

| KW字段 | 对应的固定结构 |
| --- | --- |
| KW_ATTACKING／KW_DEFENDING | 本实例在场且有对应战斗角色的Duration，数值取该卡已记录Assault／Shield参数 |
| KW_TARGET_CHOICES／KW_DEFLECT_COST | 对手法术／能力每次选择本实例的CostSelection与本卡Deflect参数形成的AnyPower附加费 |
| KW_ASSIGNMENT_SCOPE／KW_FIRST／KW_LAST | 本实例战斗伤害分配范围及Tank／Backline顺序，限定分配玩家，不删除关键词 |
| KW_OWN_PLAY／KW_ACCEL_EXTRA／KW_ACCEL_ENTRIES | 仅本次选急速分支的费用与入场，附加Energy1及规则定义的自身领域Power1；必须与付款回执一致 |
| KW_SELECTED_EQUIPMENT／KW_DISCOUNTED_EQUIP_COST | 百炼所选己控武装与按Equip成本规则计算的可适用折扣，未有Equip成本不能虚构为0；付款角色为结算内指令，不真激活Equip |
| KW_HIDE_PERMISSION／KW_HIDDEN_BATTLEFIELD | 本卡Hidden参数、合法来源、战场容量及控制检查；选择和付款由盖放流程处理 |
| KW_HIDDEN_PLAY_PERMISSION／KW_HIDDEN_PLAY_COSTS／KW_IGNORE_BASE | 盖放后规则允许的未来回合、来源／目的地／Reaction权限及独立忽略基础费政策，不免除额外费 |
| KW_BATTLEFIELD_ONLY／KW_DEPLOY_RECALL_EXCEPTION | Deploy合法地点限制、非单位装备召回例外；对手据守本地点后的摧毁体另有入口 |
| KW_FLOW_PERMISSION／KW_FLOW_BASE_REPLACEMENT／KW_THIS_ITEM_LEAVE_CHAIN | 本卡明确Flow参数、替代基础费、仅此item定稿后的离链替代，排除自身指令离链；不使用猜测费用 |

Temporary的摧毁分片在规则清理任务的指定时点执行，不伪装成可等待普通反应的触发；Reaction／Action等纯时机关键词进入能力约束，不需要伪造一次状态动作。其余KW常量同样须由该卡原文、既有正式关键词定义及具体实例绑定，不是任意自然语言占位。

本轮来源SHA-256：`ad521068ff70def757a00ff18f049583e1e5dffdc3e0152515eb90007b54ca05`。

冻结API SHA-256：`f76a76027f24165662f8e010d69a5ddad34b31ea132cda8fe6448878422462a6`。遇到缺口先记账，不在全读途中静默修改该版本。
