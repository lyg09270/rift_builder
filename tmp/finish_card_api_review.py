"""Editorial corrections after full catalog rereading; does not execute card effects."""
import ast,json,re,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from read_card_operators import CARDS,variants
p=Path('tmp/card-api-review.jsonl')
rows=[json.loads(x) for x in p.read_text(encoding='utf-8').splitlines()]
by={r['number']:r for r in rows}
def replace(n,window,bindings,calls,gaps=None):
 r=by[n];r.update(window=window,bindings=bindings,calls=calls)
 r['gaps']=[g for g in r['gaps'] if not g.startswith('DELEGATED:')] if gaps is None else gaps
# Explicit native-keyword expansions; replace these macro bodies, never run them twice.
for n in (169,572):
 replace(n,'百炼打出触发：可装配p武装，装配费减任意Power1，允许已贴附武装','g:Gear=p控制的一件武装;cost:Cost=g的Equip费用减任意Power1最低0;binding:CostBinding=百炼可选触发费用','paid = ops.pay(p, cost, binding=binding)\nif paid.value is not None:\n    ops.attach(g, me)')
for n,k in ((204,1),(529,2),(674,1)):
 replace(n,f'固有Assault{k}的内部持续效果：me进攻时战力加{k}','attacking:bool=me是进攻方',f'if attacking:\n    ops.modify_might([me], {k}, duration=WHILE_CONDITION)')
replace(371,'强攻2与坚守2的内部展开','fighting:bool=me进攻或防守','if fighting:\n    ops.modify_might([me], 2, duration=WHILE_CONDITION)')
replace(439,'固有壁垒内部展开','scope:RuleScope=me在同控制者参战单位中的承伤次序;change:RuleChange=先承担致死伤害','ops.modify_rule(COMBAT_DAMAGE_ORDER, scope, change, duration=WHILE_SOURCE_PRESENT)')
for n in (617,849):
 replace(n,'固有坚守2及壁垒内部展开'+('；反应打出权限' if n==849 else ''),'defending:bool=me为防守方;scope:RuleScope=me同控制者参战单位承伤顺序;change:RuleChange=先承担致死伤害'+(';permission:PermissionSpec=具有Reaction时机且仍检查优先权和合法地点，可到p控制战场' if n==849 else ''),'if defending:\n    ops.modify_might([me], 2, duration=WHILE_CONDITION)\nops.modify_rule(COMBAT_DAMAGE_ORDER, scope, change, duration=WHILE_SOURCE_PRESENT)'+('\nops.grant_permission([me], permission, duration=WHILE_SOURCE_PRESENT)' if n==849 else ''))
for n in (85,626,696):
 replace(n,'固有法盾1：对手以法术或技能选择本实例时附加任意Power1','subjects:CostSelection=对手法术/技能为选择me须付的目标附加费用，同一能力选择me不重复收取;change:CostChange=额外任意Power1','ops.modify_cost(subjects, change, duration=WHILE_SOURCE_PRESENT)')
replace(528,'固有游走扩展普通移动路径','permission:PermissionSpec=me可从当前战场移动到其他战场，普通移动费用与其他限制仍适用','ops.grant_permission([me], permission, duration=WHILE_SOURCE_PRESENT)')
for n in (460,891):
 replace(n,'伏击允许以反应打出到p有单位战场'+('；固有强攻2' if n==460 else ''),'permission:PermissionSpec=以Reaction时机将me打出到p有单位战场；不忽略其他费用与限制'+(';attacking:bool=me为进攻方' if n==460 else ''),'ops.grant_permission([me], permission, duration=WHILE_SOURCE_PRESENT)'+('\nif attacking:\n    ops.modify_might([me], 2, duration=WHILE_CONDITION)' if n==460 else ''))
# Accelerate choices are bound before play and then checked by normal complete cost payment.
for n in (46,99,537,760,848):
 binds='dest:Location/Zone=本次合法打出位置;choices:ChoiceBinding=定稿选择是否支付急速附加费Energy1Fury1;subjects:CostSelection=本次打出me;extra:CostChange=该次所选急速附加费Energy1Fury1，不改印刷基础费;entry:EntryState=choices选择急速则ready否则默认，必须与完整费用支付一致'
 calls='# 急速内部费用与入场展开\nops.modify_cost(subjects, extra, duration=THIS_PLAY)\nops.play(me, p, origin=p.hand, destination=dest, choices=choices, entry=entry)'
 if n==46:
  binds+=';g:Gear=p控制武装;cost:Cost=g装配费用减任意Power1最低0;binding:CostBinding=可选百炼触发费用'
  calls+='\n# 百炼打出触发\npaid = ops.pay(p, cost, binding=binding)\nif paid.value is not None:\n    ops.attach(g, me)'
 if n in (760,848):
  binds+=';attacking:bool=me为进攻方';calls+=f'\n# 强攻持续\nif attacking:\n    ops.modify_might([me], {2 if n==760 else 4}, duration=WHILE_CONDITION)'
 if n==760:
  binds+=';target_costs:CostSelection=对手法术技能选择me时的目标附加费;deflect_cost:CostChange=额外任意Power1;ganking:PermissionSpec=me可从战场普通移动到其他战场'
  calls+='\n# 法盾与游走持续\nops.modify_cost(target_costs, deflect_cost, duration=WHILE_SOURCE_PRESENT)\nops.grant_permission([me], ganking, duration=WHILE_SOURCE_PRESENT)'
 replace(n,'固有关键词内部展开；不同注释为独立入口',binds,calls)
# Discard already performs mandatory selection and does as much as possible.
for n in (813,1015):
 by[n]['calls']='ops.discard(p, 2)\nops.draw(p, 2)';by[n]['bindings']=' '
 by[n]['gaps']=[g for g in by[n]['gaps'] if not g.startswith('CHOICE_SHORTAGE:')]
for n,draw in ((967,3),(993,1),(1096,1)):
 r=by[n];r['calls']=re.sub(r'c(?:ard)? = ops.choose.*?\nops.discard\(p, (?:c|card)\)', 'ops.discard(p, 1)',r['calls'],flags=re.S)
by[1102]['bindings']=by[1102]['bindings'].replace('hand:Selection[Card]','hand:list[Card]')
by[1102]['calls']=by[1102]['calls'].replace('ops.discard(p, hand)','ops.discard(p, len(hand), cards=hand)')
by[744]['bindings']=by[744]['bindings'].replace('extra:NumericChange=add1','extra:IntExpr=1')
# Never execute play after a failed trigger-cost payment. Cost-role uncertainty stays explicit.
by[453]['calls']='# 仅记录支持的付款片段；后续打出成本角色待核\nops.pay(p, cost, binding=binding)'
by[338]['calls']='# 仅记录支持的付款片段；不错误重复收取印刷基础费用\nops.pay(p, cost, binding=binding)'
# Burn identity: definite top-to-trash is Burn per 441.1. Retain exact chosen remainder gap.
by[663].update(bindings='top:list[Card]=主牌堆顶部至多1张',calls='ops.reveal(top)\nif top and "unit" in top[0].types:\n    ops.draw(p, 1, cards=top)\nelse:\n    if top:\n        ops.burn(p, 1)\n    ops.modify_might([me], 2, duration=THIS_TURN)',gaps=[])
by[541]['window']='看3可选一牌抽取，其余指定牌置废；流转Energy2任意Power1'
by[541]['gaps'].append('ACTION_ID:剩余指定牌通常仍在牌堆顶部，441.1将顶牌入废定义为Burn；但burn没有cards参数，不能保证先前抽取遭替代后仍准确处理原rest且保留Burn身份，现transfer片段不作完整证明')
by[836]['gaps'].append('DATA:ShadowClone本体might为null；其他产生它的卡明确指定0，不能把本体缺值默认视作0')
# Normalise annotation names to exact published API types, without editing that reference.
for r in rows:
 r['bindings']=r['bindings'].replace(':EntrySpec=',':EntryState=').replace(':DamageAllocation=',':dict[Unit,int]=').replace(':SourceFilter=',':Predicate=').replace(':RuneSelection=',':Selection[Rune]=')
 # Keyword/RuleKey/TextField enum identifiers, rather than strings masquerading as typed enums.
 r['calls']=re.sub(r'(ops\.grant_keyword\([^\n]*?, )"([A-Za-z]+)"',lambda m:m[1]+re.sub(r'(?<!^)(?=[A-Z])','_',m[2]).upper(),r['calls'])
 r['calls']=re.sub(r'ops\.modify_rule\("([A-Z_]+)"',r'ops.modify_rule(\1',r['calls'])
 r['calls']=r['calls'].replace('from_field="rules_text"','from_field=RULES_TEXT').replace('to_field="effect_text"','to_field=EFFECT_TEXT')
 # Entry arguments use EntryState; a play-specific permission is a PlayPermission.
 tree=ast.parse(r['calls'])
 for c in ast.walk(tree):
  if isinstance(c,ast.Call) and isinstance(c.func,ast.Attribute) and c.func.attr=='play':
   for k in c.keywords:
    if k.arg=='permission' and isinstance(k.value,ast.Name):r['bindings']=r['bindings'].replace(k.value.id+':PermissionSpec=',k.value.id+':PlayPermission=')
 # Spell modes are prebound finalization choices, not name/type/tag declarations.
 for line in r['calls'].splitlines():
  if 'mode = ops.declare' in line:
   r['calls']=r['calls'].replace(line,'# mode由本入口明确的合法模式选择绑定；不是标签宣告')
   r['bindings']+=';mode:list[str]=本入口合法模式选择结果单元素列表；普通法术/主动在定稿绑定，后续可选模式按指定结算时点绑定'
 # Explicit, per-card aliases for Duration values used by documentary call blocks.
 for alias,meaning in {'WHILE_CONDITION':'WHILE(该段入口中明确的持续条件)，依赖变化时重算','WHILE_ATTACHED':'WHILE(本装备仍贴附于该宿主)，宿主/装备关联按本实例保存','THIS_PLAY':'UNTIL(本次打出完成费用定稿)，只用于此打出流程修饰','DECK_CONSTRUCTION':'PERMANENT，适用范围仅构筑检查'}.items():
  if re.search(r'\b'+alias+r'\b',r['calls']) and alias+':Duration=' not in r['bindings']:r['bindings']+=';'+alias+':Duration='+meaning
 # Different language/printing omissions are source findings, not new semantic guesses.
 cid,_=CARDS[r['number']-1];groups=variants(cid)
 missing_rules=[f'{lang} {faces[0]["shortCode"]}' for (lang,text,effect),faces in groups if not text and any(t for (l,t,e),fs in groups)]
 missing_effect=[f'{lang} {faces[0]["shortCode"]}' for (lang,text,effect),faces in groups if not effect and any(e for (l,t,e),fs in groups)]
 if missing_rules and not any('规则空' in g or '规则为空' in g or '规则和' in g for g in r['gaps']):r['gaps'].append('DATA:同一本体有非空规则文本，但这些变体printedRulesText为空：'+', '.join(missing_rules))
 if missing_effect and not any(('EFFECT' in g or 'effect' in g or '装备效果' in g) and g.startswith('DATA:') for g in r['gaps']):r['gaps'].append('DATA:同一本体有非空装备效果，但这些变体printedEffectText为空：'+', '.join(missing_effect))
p.write_text(''.join(json.dumps(r,ensure_ascii=False)+'\n' for r in rows),encoding='utf-8')
print('Editorial corrections saved for',len(rows),'cards')
