"""Document authoring for the explicitly requested P1 complete-card reading.

This lowers prior drafts to symbolic ActionFrame programs. It does not execute games,
infer semantic approval, or modify the catalog. Every recorded card needs a fresh review.
"""
import ast
import hashlib
import json
import re
import sys
from pathlib import Path
from read_card_operators import ROOT, CARDS, variants, read

sys.stdout.reconfigure(encoding='utf-8')
META = json.loads((ROOT/'tmp/card-primitives-p1-frozen.json').read_text(encoding='utf-8'))
for rel, fingerprint in META.items():
    assert hashlib.sha256((ROOT/rel).read_bytes()).hexdigest() == fingerprint, rel
OUT = ROOT/'tmp/card-primitives-review-p1.jsonl'
OLD = {r['number']:r for r in map(json.loads,(ROOT/'tmp/card-api-review-v3.jsonl').read_text(encoding='utf-8').splitlines())}

# Closed lowering recipes. f.* is supplied by the named action protocol, not a raw
# natural-language evaluator. Original inputs remain printed in each frame header.
RECIPES = {
 'draw': 'p.zone_change(f.objects, f.origin, f.destination)',
 'look': 'p.information_access(f.objects, [f.player], mode="LOOK", duration=UNTIL_EFFECT_END)',
 'reveal': 'p.information_access(f.objects, f.viewers, mode="REVEAL", duration=f.duration)',
 'transfer': 'p.zone_change(f.objects, f.origin, f.destination, position=f.position, order=f.order)',
 'move': 'p.location_change(f.objects, f.destination, origin=f.origin)',
 'recall': 'p.location_change(f.objects, f.controller_bases)',
 'discard': 'p.zone_change(f.objects, f.origin, f.destination)',
 'recycle': '''with flow.Batch(policy=SIMULTANEOUS):
    for group in f.recycle_groups:
        if group.same_zone:
            p.order_change(group.objects, group.deck, position="bottom", order=group.order)
        else:
            p.zone_change(group.objects, group.origin, group.deck, position="bottom", order=group.order)''',
 'banish': 'p.zone_change(f.objects, f.origin, f.owner_banishment)',
 'burn': 'p.zone_change(f.objects, f.origin, f.destination)',
 'channel': 'p.zone_change(f.objects, f.origin, f.board, entry=f.entry, entry_location=f.entry_locations)',
 'reorder': 'p.order_change(f.objects, f.zone, position=f.position, order=f.order)',
 'hide': 'p.zone_change(f.objects, f.origin, f.hidden_zone)\np.status_set(f.objects, "FACE_DOWN", True)',
 'play': '''with phase("start"):
    if f.new_template:
        born = p.instantiate(f.template, f.count, owner=f.owner, controller=f.controller, initial=f.entry)
        f.bind_newborn(born.value)
    p.zone_change(f.objects, f.origin, f.chain_zone)
with phase("enter_permanent"):
    p.zone_change(f.objects, f.chain_zone, f.board, entry=f.entry, entry_location=f.entry_locations)
with phase("spell_leave_chain"):
    p.zone_change(f.objects, f.chain_zone, f.leave_destination)''',
 'create': 'born = p.instantiate(f.template, f.count, owner=f.owner, controller=f.controller, initial=f.entry)\np.zone_change(born.value, None, f.destination, entry=f.entry, entry_location=f.entry_locations)',
 'replace_battlefield': '''if f.mode == "replace":
    born = p.instantiate(f.template, 1, owner=f.owner, controller=None)
    p.battlefield_bind(f.slot, born.value[0], mode="replace", link=f.link)
else:
    p.battlefield_bind(f.slot, None, mode="restore", link=f.link)''',
 'orient': 'p.orientation_set(f.objects, f.state)',
 'buff': 'p.stack_change(f.objects, "BUFF", "ADD", 1)',
 'spend_buff': 'p.stack_change(f.objects, "BUFF", "SPEND", f.count_map)',
 'stun': 'p.status_set(f.objects, "STUNNED", True)',
 'change_empowerment': 'p.stack_change(f.objects, "EMPOWER_LAYER", f.stack_operation, 1)',
 'modify_might': 'p.might_contribute(f.objects, "ARITHMETIC", f.snapshot_change, duration=f.duration)',
 'damage': 'p.damage_record(f.objects, f.actual_damage_map, source=f.source, actor=f.actor)',
 'heal': 'p.damage_clear(f.objects)',
 'kill': 'p.zone_change(f.objects, f.origin, f.owner_trash)',
 'attach': 'p.attachment_set(f.gear, f.host)',
 'detach': 'p.attachment_set(f.gear, None)',
 'change_control': 'p.control_contribute(f.objects, f.player, duration=f.duration, link=f.link)',
 'end_modifier': 'p.effect_end(f.handles, link=f.link)',
 'copy': 'p.copy_view(f.target, f.copy_view, duration=f.duration, link=f.link)',
 'copy_text': 'p.copy_view(f.target, f.copy_view, duration=f.duration, link=f.link)',
 'copy_abilities': 'p.copy_view(f.target, f.copy_view, duration=f.duration, link=f.link)',
 'grant_ability': 'p.ability_add(f.objects, f.ability, duration=f.duration, link=f.link)',
 'suppress_ability': 'p.ability_mask(f.objects, f.ability_filter, duration=f.duration)',
 'grant_keyword': 'for definition in f.keyword_definitions:\n    p.ability_add(f.objects, definition, duration=f.duration, link=f.keyword_link)',
 'set_types': 'p.trait_change(f.objects, "TYPE", f.operation, f.values, duration=f.duration)',
 'set_tags': 'p.trait_change(f.objects, "TAG", f.operation, f.values, duration=f.duration)',
 'add_resources': 'p.resource_credit(f.player, f.resources, restriction=f.restriction, expires=f.expires)',
 'change_xp': 'p.xp_change(f.player, f.amount, operation=f.operation)',
 'gain_points': 'p.score_credit(f.player, f.actual_amount, cause=f.cause, source=f.source)',
 'win': 'p.outcome_set(f.player, authorization=f.authorization)',
 'counter': 'p.chain_cancel(f.item)\nif f.has_card:\n    p.zone_change([f.card], f.chain_zone, f.leave_destination)',
 'redo_choices': 'p.chain_choices_set(f.item, f.rebound_choices, authorization=f.authorization)',
 'skip_procedure': 'p.procedure_skip(f.player, f.procedure, occurrence=f.occurrence, duration=f.duration)',
 'extra_turn': 'p.turn_insert(f.player, f.count, after=f.after)',
 'set_base_might': 'p.might_contribute(f.objects, "BASE", f.change, duration=f.duration)',
 'modify_equipment_bonus': 'p.might_contribute(f.objects, "EQUIPMENT_BONUS", f.change, duration=f.duration)',
 'modify_buff_value': 'p.might_contribute(f.objects, "BUFF_VALUE", f.change, duration=f.duration)',
 'modify_keyword': 'p.ability_patch(f.abilities, f.patch, duration=f.duration)',
 'modify_cost': 'p.cost_rule_add(f.subjects, f.rule, duration=f.duration, limit=f.limit, link=f.link)',
 'modify_damage': 'p.damage_rule_add(f.subjects, f.rule, duration=f.duration, limit=f.limit)',
 'prevent_damage': 'p.damage_rule_add(f.subjects, f.rule, duration=f.duration, limit=f.limit)',
 'modify_effect_value': 'p.instruction_rule_add(f.effects, f.parameter, f.change, duration=f.duration)',
 'modify_trigger_count': 'p.ability_patch(f.abilities, f.patch, duration=f.duration)',
 'modify_trigger_events': 'p.ability_patch(f.abilities, f.patch, duration=f.duration)',
 'modify_resource_output': 'p.output_rule_add(f.actions, f.change, duration=f.duration)',
 'modify_entry': 'p.entry_rule_add(f.subjects, f.entry, duration=f.duration, limit=f.limit, link=f.link)',
 'grant_permission': 'p.permission_rule_add(f.subjects, f.rule, duration=f.duration, limit=f.limit)',
 'restrict_action': 'p.permission_rule_add(f.subjects, f.rule, duration=f.duration)',
 'modify_rule': 'p.rule_value_add(f.key, f.scope, f.change, duration=f.duration)',
}
FLOW = {'choose':'Choose','declare':'Choose','pay':'Pay','batch':'Batch','on_event':'Register',
        'replace_event':'Register','queue_effect':'Enqueue','execute_effect':'Enqueue','remember':'Bind',
        'predict':'Keyword','show_off':'Keyword'}

def symbolic(name, *args, **kwargs):
    return ast.Call(ast.Name(name,ast.Load()),list(args),[ast.keyword(k,v) for k,v in kwargs.items()])

def flow_call(call):
    name=call.func.attr;args=call.args;kw={k.arg:k.value for k in call.keywords}
    def val(key,pos,default=None):
        return kw.get(key,args[pos] if len(args)>pos else ast.Constant(default))
    def node(node_type,**fields):
        return ast.Call(ast.Attribute(ast.Name('flow',ast.Load()),node_type,ast.Load()),[],[ast.keyword(k,v) for k,v in fields.items()])
    if name=='pay':return node('Pay',player=val('player',0),cost=val('cost',1),binding=kw['binding'])
    if name in ('choose','declare'):
        fields=dict(player=val('player',0),kind=ast.Constant('object') if name=='choose' else kw.get('kind',ast.Constant('value')),
                    candidates=val('candidates' if name=='choose' else 'options',1),minimum=kw.get('minimum',ast.Constant(1)),maximum=kw.get('maximum',ast.Constant(1)),
                    stage=kw.get('bind_at',ast.Constant('finalization' if name=='choose' else 'resolution')))
        if name=='choose':fields.update(targeting=kw.get('targeting',ast.Constant(True)),shortage=kw.get('shortage',ast.Constant('as_many_as_possible')))
        return node('Choose',**fields)
    if name=='on_event':
        entry=symbolic('EventEntry',events=val('events',0),delivery=kw.get('timing',ast.Constant('triggered')))
        bound=symbolic('AbilityBinding',definition=val('ability',1),entry=entry)
        return node('Register',ability=bound,**{k:v for k,v in kw.items() if k!='timing'})
    if name=='replace_event':
        bound=symbolic('ReplacementAbility',events=val('events',0),rewrite=val('rewrite',1),optional=kw.get('optional',ast.Constant(False)))
        return node('Register',ability=bound,**{k:v for k,v in kw.items() if k!='optional'})
    if name=='queue_effect':return node('Enqueue',source=val('source',0),ability=val('ability',1),**{('bindings' if k=='choices' else k):v for k,v in kw.items()})
    if name=='execute_effect':
        count=kw.get('count',ast.Constant(1));mode=kw.get('mode',ast.Constant('pending'))
        ref=symbolic('EffectRef',source=val('source',0),ability=val('ability',1))
        if isinstance(mode,ast.Constant) and mode.value=='repeat_inline':return node('Repeat',count=count,body=ref,bindings=kw.get('choices',ast.Constant(None)))
        pending=node('Enqueue',source=val('source',0),ability=val('ability',1),**{('bindings' if k=='choices' else k):v for k,v in kw.items() if k not in ('count','mode')})
        return pending if isinstance(count,ast.Constant) and count.value==1 else node('Repeat',count=count,body=pending)
    if name=='remember':return node('Bind',key=symbolic('ScopedKey',source=val('source',0),key=val('key',1)),value=val('value',2),scope=ast.Attribute(val('key',1),'scope',ast.Load()),**kw)
    if name=='batch':return node('Batch',**kw)
    raise ValueError(name)

class LowerFlow(ast.NodeTransformer):
    def visit_Call(self,node):
        self.generic_visit(node)
        if is_op(node) and node.func.attr in FLOW and node.func.attr not in ('predict','show_off'):
            return flow_call(node)
        return node

RECIPES['predict']='''p.information_access(f.looked, [f.player], mode="LOOK", duration=UNTIL_EFFECT_END)
f.bind_recycle_choice(flow.Choose(player=f.player, kind="object", candidates=f.looked, minimum=0, maximum=f.count, targeting=False, stage="resolution", shortage="as_many_as_possible"))
if f.to_recycle:
    with action_frame("recycle", {"positional": (f.to_recycle,), "keywords": {}}) as recycled:
        p.order_change(f.to_recycle, f.main_deck, position="bottom", order=f.recycle_order)
if f.kept_on_top:
    p.order_change(f.kept_on_top, f.main_deck, position="top", order=f.chosen_top_order)'''
RECIPES['show_off']='''f.bind_show_off_choice(flow.Choose(player=f.player, kind="object", candidates=f.candidates, minimum=f.count, maximum=f.count, targeting=False, stage="finalization", shortage="fail"))
if f.hand_shown:
    p.information_access(f.hand_shown, f.viewers, mode="REVEAL", duration=UNTIL_EFFECT_END)
f.capture_show_off_snapshot()'''

class RenamePlayer(ast.NodeTransformer):
    def visit_Name(self,node):
        if node.id=='p': node.id='player'
        return node

def is_op(expr):
    return isinstance(expr,ast.Call) and isinstance(expr.func,ast.Attribute) and isinstance(expr.func.value,ast.Name) and expr.func.value.id=='ops'

def lower(code):
    tree=LowerFlow().visit(RenamePlayer().visit(ast.parse(code))); frame_no=0
    def statements(items):
        nonlocal frame_no
        output=[]
        for node in items:
            expr=node.value if isinstance(node,(ast.Expr,ast.Assign,ast.AnnAssign)) else None
            attr=None
            if isinstance(expr,ast.Attribute) and is_op(expr.value):attr=expr.attr;expr=expr.value
            if is_op(expr):
                name=expr.func.attr
                assert name in RECIPES,name
                frame_no+=1;var='f'+str(frame_no)
                inp=ast.Dict([ast.Constant('positional'),ast.Constant('keywords')],
                             [ast.Tuple(expr.args,ast.Load()),ast.Dict([ast.Constant(k.arg) for k in expr.keywords],[k.value for k in expr.keywords])])
                context=ast.Call(ast.Name('action_frame',ast.Load()),[ast.Constant(name),inp],[])
                body=ast.parse(RECIPES[name]).body
                class FrameName(ast.NodeTransformer):
                    def visit_Name(self,x):
                        if x.id=='f':x.id=var
                        return x
                body=[FrameName().visit(x) for x in body]
                output.append(ast.With([ast.withitem(context,ast.Name(var,ast.Store()))],body))
                if isinstance(node,(ast.Assign,ast.AnnAssign)):
                    result=ast.Attribute(ast.Name(var,ast.Load()),'result',ast.Load())
                    node.value=ast.Attribute(result,attr,ast.Load()) if attr else result;output.append(node)
                continue
            for field in ('body','orelse','finalbody'):
                if hasattr(node,field):setattr(node,field,statements(getattr(node,field)))
            if isinstance(node,ast.With):
                for item in node.items:
                    if is_op(item.context_expr):
                        item.context_expr.func=ast.Attribute(ast.Name('flow',ast.Load()),'Batch',ast.Load())
            output.append(node)
        return output
    tree.body=statements(tree.body)
    return ast.unparse(ast.fix_missing_locations(tree))

def sections(code, window):
    parts=[];label=window;buf=[]
    for line in code.splitlines():
        if line.startswith('#'):
            if any(x.strip() for x in buf):parts.append((label,'\n'.join(buf)))
            label=line.lstrip('# ').strip();buf=[]
        else:buf.append(line)
    if any(x.strip() for x in buf):parts.append((label,'\n'.join(buf)))
    try:return [dict(entry=label,program=lower(body)) for label,body in parts]
    except SyntaxError:return [dict(entry=window,program=lower(code))]

def native_sections(specs):
    result=[]
    for spec in specs:
        if ':body' in spec or ':condition' in spec or ':entry' in spec:continue
        base=spec.split(':')[0];name,_,raw_value=base.partition('=');value=int(raw_value) if raw_value else 1
        if name in ('Action','Reaction','Empowered','Level','Mighty','Legion','Repeat'):
            result.append(dict(entry='固有'+spec+'：权限／条件／定稿结构',program='# '+spec+'由本卡入口、选择、费用与历史约束明确绑定；不制造一次即时动作。'))
            continue
        programs={
          'Assault':f'ops.modify_might([me], {value}, duration=KW_ATTACKING)',
          'Shield':f'ops.modify_might([me], {value}, duration=KW_DEFENDING)',
          'Deflect':'ops.modify_cost(KW_TARGET_CHOICES, KW_DEFLECT_COST, duration=KW_ACTIVE)',
          'Tank':'ops.modify_rule(COMBAT_DAMAGE_ORDER, KW_ASSIGNMENT_SCOPE, KW_FIRST, duration=KW_ACTIVE)',
          'Backline':'ops.modify_rule(COMBAT_DAMAGE_ORDER, KW_ASSIGNMENT_SCOPE, KW_LAST, duration=KW_ACTIVE)',
          'Ganking':'ops.grant_permission([me], KW_BATTLEFIELD_MOVE, duration=KW_ACTIVE)',
          'Accelerate':'ops.modify_cost(KW_OWN_PLAY, KW_ACCEL_EXTRA, duration=KW_THIS_PLAY)\nops.modify_entry(KW_ACCEL_ENTRIES, KW_READY_ENTRY, duration=KW_THIS_PLAY)',
          'Weaponmaster':'wm_paid = ops.pay(player, KW_DISCOUNTED_EQUIP_COST, binding=KW_INSTRUCTION_PAYMENT)\nif wm_paid.value is not None:\n    ops.attach(KW_SELECTED_EQUIPMENT, me)',
          'Vision':f'ops.predict(player, {value})',
          'Hunt':f'ops.change_xp(player, {value})',
          'Hidden':'# 盖放请求入口，费用由hide协议完整处理\nops.hide(me, KW_HIDDEN_BATTLEFIELD, permission=KW_HIDE_PERMISSION)\n# 盖放后未来合法打出权限与基础费政策\nops.grant_permission([me], KW_HIDDEN_PLAY_PERMISSION, duration=KW_HIDDEN_WINDOW)\nops.modify_cost(KW_HIDDEN_PLAY_COSTS, KW_IGNORE_BASE, duration=KW_HIDDEN_WINDOW)',
          'Deploy':'# 固有部署位置限制与清理召回例外\nops.restrict_action([me], KW_BATTLEFIELD_ONLY, duration=KW_PLAYABLE)\nops.modify_rule(GEAR_RECALL_POLICY, KW_RECALL_SCOPE, KW_DEPLOY_RECALL_EXCEPTION, duration=KW_ACTIVE)\n# 对手据守此处后\nops.kill([me])',
          'Temporary':'# 下一控制者Beginning得分前的规则清理入口，不是普通待处理触发\nops.kill([me])',
          'Quick-Draw':'# 固有Reaction权限，独立PLAY.resolved贴附入口\nops.attach(me, KW_FRIENDLY_UNIT)',
          'Disarm':'ops.modify_might([KW_ENEMY_HERE], -1, duration=THIS_TURN)',
          'Unique':'ops.modify_rule(DECK_NAME_LIMIT, KW_DECK_SCOPE, KW_UNIQUE_LIMIT, duration=KW_CONSTRUCTION)',
          'Flow':'# 废牌来源许可、替代基础费用、仅该item离链替代\nops.grant_permission([me], KW_FLOW_PERMISSION, duration=KW_FLOW_WINDOW)\nops.modify_cost(KW_FLOW_COSTS, KW_FLOW_BASE_REPLACEMENT, duration=KW_THIS_PLAY)\nops.replace_event(KW_THIS_ITEM_LEAVE_CHAIN, KW_FLOW_REWRITE, duration=KW_THIS_ITEM)\n# 替代体排除自身执行指令离链\nops.banish([KW_ITEM_CARD])',
          'Empower':'paid = ops.pay(player, KW_EMPOWER_COST, binding=KW_ACTIVE_PAYMENT)\nif paid.value is not None:\n    ops.change_empowerment([me], "empower")',
          'Equip':'paid = ops.pay(player, KW_EQUIP_COST, binding=KW_ACTIVE_PAYMENT)\nif paid.value is not None:\n    ops.attach(me, KW_FRIENDLY_UNIT)',
          'Ambush':'ops.grant_permission([me], KW_AMBUSH_PERMISSION, duration=KW_PLAYABLE)',
        }
        assert name in programs,('undeclared native keyword',spec)
        for part in sections(programs[name], '固有'+spec+'的正式规则展开'):
            part['entry']='固有'+spec+' / '+part['entry'];result.append(part)
    return result

def groups(n):
    return [dict(language=l,text=a,effect=b,hash=hashlib.sha256(json.dumps([l,a,b],ensure_ascii=False).encode()).hexdigest())
            for (l,a,b),faces in variants(CARDS[n-1][0])]

def show(a,b):
    for n in range(a,b+1):
        read(n,n);r=OLD[n]
        print('R3_ENTRY:',r['window']);print('R3_BIND:',r['bindings']);print('R3_BODY:\n'+r['calls'])
        for g in r['gaps']:print('OLD_ISSUE',g)

def record(items):
    existing=[json.loads(x) for x in OUT.read_text(encoding='utf-8').splitlines()] if OUT.exists() else []
    by={r['number']:r for r in existing}
    for item in items:
        n=item['number'];assert n not in by,n
        assert item['status'] in ('covered','verify','uncovered')
        assert len(item['review'])>=16
        r=OLD[n];body=item.get('source_program',r['calls'])
        compiled=lower(body);ast.parse(compiled)
        issues=item.get('issues',[])
        assert item['status']=='covered' or issues,n
        row=dict(number=n,card_id=CARDS[n-1][0],name=CARDS[n-1][1]['name'],round='P1-R1',
                 api_sha256=META['docs/basic-primitives-v4-p1.md'],source_sha256=META['data/sources/openrift/catalog.json'],
                 text_groups=groups(n),window=item.get('window',r['window']),bindings=item.get('bindings',r['bindings']),
                 source_program=body,primitive_program=compiled,primitive_sections=sections(body,item.get('window',r['window'])),native_sections=native_sections(item.get('native',[])),native=item.get('native',[]),review=item['review'],
                 status=item['status'],issues=issues,source_issues=[g for g in r['gaps'] if g.startswith(('DATA:','LANG:'))])
        by[n]=row
    OUT.write_text(''.join(json.dumps(by[n],ensure_ascii=False)+'\n' for n in sorted(by)),encoding='utf-8')
    status()

def status():
    rows=[json.loads(x) for x in OUT.read_text(encoding='utf-8').splitlines()] if OUT.exists() else []
    print(json.dumps(dict(read=len(rows),covered=sum(r['status']=='covered' for r in rows),verify=sum(r['status']=='verify' for r in rows),
                         uncovered=sum(r['status']=='uncovered' for r in rows),last=max([r['number'] for r in rows],default=0)),ensure_ascii=False))

if __name__=='__main__':
    cmd=sys.argv[1]
    if cmd=='read':show(int(sys.argv[2]),int(sys.argv[3]))
    elif cmd=='record':record(json.load(sys.stdin))
    elif cmd=='status':status()
