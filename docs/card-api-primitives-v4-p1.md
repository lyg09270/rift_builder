# V4-P1：60项接口到35个原语的试拆

[原语参考](basic-primitives-v4-p1.md) · [V4对照](basic-operators-api-v4.md) · [卡牌模型](card-model.md) · [SES参考阅读](references/card-effect-models/README.md)

本次做接口级映射和边界卡的静态展开，不实现引擎、不执行测试套件，也不将原全库覆盖率上调。现行V4保持60个接口；P1另列35个底层原语，具名规则模板和程序节点另计。

## 1. 完整映射

同一原语可供多个模板复用，但每个模板保留原动作身份和协议。表中“流程”使用原有Choose／Pay／Batch／Register／Enqueue等结构，不暗含另一个任意效果算子。

| V4接口 | 展开原语 | 模板必须保留的规则 |
| --- | --- | --- |
| draw | zone_change | 顶牌或授权指定牌、DRAW、耗尽流程 |
| look | information_access | 私密访问者、查看范围及阶段 |
| reveal | information_access | 公开范围、逐张until、展示事件；不预读后续牌 |
| transfer | zone_change | 原区域、拥有者目的区、顶底与绑定次序，不冒充其他动作 |
| move | location_change | MOVE身份、限制、同批出发快照及获授权的过程加入 |
| recall | location_change | 当前控制者基地、RECALL身份，不套用移动限制 |
| discard | zone_change | 手牌来源、选择、实际弃牌及同批事件粒度 |
| recycle | zone_change | 各拥有者牌底、主牌随机／符文排序，直接带次序转移，不额外制造第二次重排动作 |
| banish | zone_change | 放逐身份、拥有者放逐区、链项实体及来源link |
| burn | zone_change | 顶牌／明确剩余顶牌、燃烧与耗尽，不补烧原集合外新牌 |
| channel | zone_change | 符文牌堆来源、Board初态及位置、原指令与替代追加数量归因 |
| reorder | order_change | 保持／随机／已绑定排列，不额外授予信息 |
| hide | zone_change、status_set | 合法费用、容量、战场控制、盖放区域及面朝下状态，HIDE不等于PLAY |
| play | instantiate、zone_change | 实例创建仅用于新模板；pending、最终选择、费用、优先权、入场初态及PLAY阶段由打出流程处理 |
| create | instantiate、zone_change | 新身份、拥有者／控制者、入场初态、构筑预选及创建期限，不伪造打出 |
| replace_battlefield | instantiate、battlefield_bind | 新战场才实例化；暂存／恢复原对象、继承状态，不制造普通放逐 |
| orient | orientation_set | 活跃／横置分别保留动作身份，不重复处理已有朝向 |
| buff | stack_change | BUFF数量与上限、实际新增计数物及获得事件，战力由派生规则贡献 |
| spend_buff | stack_change | 控制权、实际消耗数、SPEND_BUFF及费用完整性，不等于普通移除 |
| stun | status_set | 新眩晕合法性、STUN及解除规则，不等于横置 |
| change_empowerment | stack_change | 独立强化层数、上限、期限，EMPOWER／DISEMPOWER不混成BUFF |
| modify_might | might_contribute | 即时给予与持续贡献分开；set/swap/上下限用共同快照差值 |
| damage | damage_record | 分配、Bonus、预防、替代与真实归因先处理，致死稍后清理 |
| heal | damage_clear | 清除实际伤害，不增加战力，不作为负伤害 |
| kill | zone_change | DIE尝试、死亡替代、LKI、离场清理与真正死亡对象；普通区域迁移本身不等于摧毁 |
| attach | attachment_set | Equip费用在流程、宿主关系、有效文本及装备贡献依赖 |
| detach | attachment_set | host=None、解除贡献／文本，后续召回不冒充移动 |
| change_control | control_contribute | 独立控制修饰、拥有者不变、结束后重算 |
| end_modifier | effect_end | 仅结束已取得且获授权的具体记录，不反向恢复已发生动作 |
| copy | copy_view | 可复制特征、复制层与绑定时点，不复制伤害或任意实例状态 |
| copy_text | copy_view | rules_text/effect_text字段映射、指代及期限 |
| copy_abilities | copy_view | 动态能力筛选、原能力身份、第一人称及防派生循环 |
| grant_ability | ability_add | 完整AbilitySpec，不立即执行能力 |
| suppress_ability | ability_mask | 期限内失活遮罩，保留原定义，非永久删除 |
| grant_keyword | ability_add | 宏组只展开一次，子能力共享原关键词实例身份，保留叠加与查询 |
| set_types | trait_change | TYPE集合、有效类型视图及后续合法性重检 |
| set_tags | trait_change | TAG集合及动态依赖，不改变卡名或类型 |
| add_resources | resource_credit | 分领域批次、使用限制、来源与到期 |
| change_xp | xp_change | 获得／消耗事件与等级重算，不当作单位增益 |
| gain_points | score_credit | 来源、最后一分及替代，保持据守／征服历史 |
| win | outcome_set | 满足明确终局授权，不将分数任意设为胜利 |
| counter | chain_cancel、zone_change | 有实体卡才转移；免反制、离链目的地与Flow替代，不产生resolved |
| redo_choices | chain_choices_set | 明确改选授权、模式和目标范围，不重付费用或自动夺控 |
| skip_procedure | procedure_skip | 具体流程与次数，不发生就不产生发生触发 |
| extra_turn | turn_insert | 锚点及完整回合，不打断当前效果 |
| set_base_might | might_contribute | BASE层，不覆盖装备与增益层 |
| modify_equipment_bonus | might_contribute | EQUIPMENT_BONUS层、宿主关系及原装备贡献来源 |
| modify_buff_value | might_contribute | BUFF_VALUE层，动态包含匹配单位及其增益，不再添加计数物 |
| modify_keyword | ability_patch | 仅登记的关键词数值字段，不抹掉角色条件 |
| modify_cost | cost_rule_add | 基础／额外／替代／目标费用、使用额度与付款关联 |
| modify_damage | damage_rule_add | 只影响匹配伤害实例或总池，不额外造成伤害 |
| prevent_damage | damage_rule_add | 数值池、事件额度、逐目标／共享范围与实际预防量 |
| modify_effect_value | instruction_rule_add | 仅已登记负战力幅度参数，不修改所有文本数字 |
| modify_trigger_count | ability_patch | 指定能力额外实例数，不等于Repeat或重新打出 |
| modify_trigger_events | ability_patch | HOLD/CONQUER扩展，保留原能力，不重复登记同一实际事件 |
| modify_resource_output | output_rule_add | 只改匹配产费，不直接改变现有资源池 |
| modify_entry | entry_rule_add | 未来入场初态、来源／地点、额度，不发READY／EXHAUST |
| grant_permission | permission_rule_add | ALLOW仍受硬性禁止，不自动免费 |
| restrict_action | permission_rule_add | DENY有明确动作及例外，不等于免疫所有效果 |
| modify_rule | rule_value_add | 只登记固定RuleKey；正向位置要求保留冲突仲裁，不改成硬性禁止 |

## 2. 边界卡静态展开

以下重看本地卡面及[既有阅读记录](card-operator-reading.md)，只检查抽象是否保留关键语义；不表示真实局面执行已经通过。代码均为对应模板内部的原语调用示意，变量由同次Context与选择节点绑定。

### Stand United：增益数量与贡献分开

先对已选友军给予增益，再让本回合全部友军每枚增益额外贡献1。live_friendly_units是实时友军集合，包含后来出现的单位。

```python
# buff模板内：新增是否成功受数量上限约束。
p.stack_change([unit], "BUFF", "ADD", 1)
# modify_buff_value模板内：本回合改变每枚增益的贡献。
p.might_contribute(live_friendly_units, "BUFF_VALUE", NumericChange(add=1),
                   duration=THIS_TURN)
```

原本已有增益的单位即使未新增，也仍受第二条贡献规则影响；不能将两条指令合并为“给目标加2”。

### Lee Sin, Ascetic与Kayle, Justified：两套数量规则

Lee Sin通过BUFF_LIMIT允许自身任意数量增益，单次buff仍只增加一个。Kayle使用EMPOWER_LAYER且上限3，每层派生+2，三层时才授予Deflect 3和Ganking；内部层数不变成可被其他牌消耗的BUFF。

### Albus Ferros：按实际消耗结果继续

stack_change记录实际消耗增益及总数，随后ForEach按实际每枚增益分别执行一次channel模板。不能按请求数结算，也不能未经规则依据把多次channel合成一次批量召出。

### Gearhead：装备贡献不等于宿主普通加值

对每件当前贴附装备，在EQUIPMENT_BONUS层增加其基础武装加成，得到基础加成翻倍；不翻倍装备上其他战力效果，不持续锁定宿主最终战力。宿主关系变化由依赖重算处理。

### Hostile Takeover：结束修饰不写回旧控制者

当前结算记录控制贡献并活跃目标；合法创建的回合末延迟入口保存本次handles。到指定时点，先结束这些记录，再以重新计算的控制者决定召回基地。

```python
# 延迟能力体，control_handles来自此前control_contribute的实际登记结果。
p.effect_end(control_handles, link=takeover_link)
p.location_change([unit], unit.controller.base)
```

不删除其他来源的控制效果，来源离场不自动取消该延迟项；若创建时本回合指定结束时点已过去，不错误挪到下一回合。

### Lady of Clockwork：类型和基础战力可分别派生

trait_change给所选装备增加UNIT而保留GEAR；might_contribute在BASE层令其战力等于规则引用的Energy费用。两项效果关联同一来源实例的下一次“选择另一装备”事件，不因传奇离场就提前到期。

### Svellsongur与Heimerdinger：复制仍有结构边界

Svellsongur保留宿主规则文字到装备效果字段的映射和贴附期限；Heimerdinger保留友方横置能力集合及防派生循环。copy_view共享投影登记，具体取值方式仍由已核定模板明确绑定，不能统一猜成快照或实时。本轮核对字段与依赖表达，不新增复制时点裁定。

### Counter Strike与Ki Barrier：事件次数和数值预算分开

两者都登记PREVENT规则。Counter Strike的amount为INFINITY，limit限定下一次匹配伤害事件；Ki Barrier的amount为7，本回合从同一预算持续扣减，没有“一次事件”限制。两者不能只写成每次伤害减7。

### SES参考带来的调整

借鉴结构化操作、精确条件绑定和模板化文本；条件逻辑采用显式All/Any/Not，不靠重复指令表达OR。替代在提交前决定，不在动作发生后靠加回数值恢复。带随机或玩家选择的过程，以选择记录与随机流作为输入，不把“确定性”解释为没有选择。[阅读记录及采用边界](references/card-effect-models/README.md)

## 3. 试拆结论

- 全部60项V4接口都有对应模板和原语去向；35个原语均有用途。这里的接口映射完整度不等于全库卡牌语义覆盖率。
- 数量／层数、四类战力贡献、类型集合、宿主关系、信息授权及区域迁移形成实际共享机制，不再各维护一套独立状态更新。
- 不把费用、伤害、产费、入场、指令参数、权限和其他规则塞进通用modify；这7类登记边界独立保留。AbilityPatch和CopyView仍有有限变体，rule_value_add及特殊流程仍是待进一步评估的边界。
- 上述试拆阶段完成文档定义、映射及静态案例核对，未实现35原语执行引擎。

## 4. 后续全库复读结果（2026-10-28）

已用冻结的35原语逐张复读全部1106个卡牌本体、2771组可用EN／SC／TC规则与效果文字，并写出每张的独立入口及原语分解。确认可表达1092张，覆盖率98.73%；6张有费用最低值契约缺口，8张待核。2767处原语调用均通过名称和参数签名检查；实战语义正确率尚未测得。[完整报告、问题清单与逐卡索引](card-primitives-coverage-p1.md)

后续P1.1已在[当前原语API](basic-primitives-v4-p1.md#cost_rule_add-费用规则)加入`CostRule.energy_floor`，明确其局部折扣语义和费用求值顺序；原语仍为35项。以上数字属于冻结P1，P1.1尚未重新评估覆盖率。
