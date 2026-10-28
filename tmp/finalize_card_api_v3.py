"""Explicit editorial amendments after the complete R3 reading; no effect execution."""
import json
from pathlib import Path

path = Path('tmp/card-api-review-v3.jsonl')
rows = [json.loads(x) for x in path.read_text(encoding='utf-8').splitlines()]
by = {r['number']: r for r in rows}
assert len(by) == 1106

def append_review(n, text):
    by[n]['review'] += ' 终审：' + text

def gap(n, issue):
    r = by[n]
    if r['status'] == 'confirmed':
        r['status'] = 'uncovered'
    if issue not in r['gaps']:
        r['gaps'].append(issue)
    append_review(n, issue)

# Each of these entries was individually identified from its actual triggering clause.
# Unit-only play triggers can use the permanent's completed entry; spell/card triggers
# also need a post-resolution event distinct from finalization (CR 420.4.a).
spell_play = [2, 8, 52, 88, 156, 206, 236, 284, 300, 343, 349, 412,
              497, 523, 559, 588, 679, 732, 767, 803, 1044]
stage_issue = ('EVENT_STAGE:规则420.4.a的打出触发在卡牌成功结算后发生；'
               '本卡触发包含法术，PLAY.finalized会误计被反制法术，entered不足覆盖法术，'
               'V3闭合表缺PLAY.resolved/complete，不能计整卡确认覆盖。')
for n in spell_play:
    gap(n, stage_issue)
gap(196, 'EVENT_KIND:本卡明确包括使用主动能力；闭合表未定义ACTIVATE/USE_ABILITY的完成入口，不能只覆盖单位与装备打出。')
gap(292, 'EVENT_IDENTITY:替代任何非主牌堆入己废牌需要覆盖DISCARD等独立区域动作；V3未明确所有这些动作均发布带身份的ZONE_TRANSFER.before，现有枚举不能证明无遗漏。')

# In these unit-specific delayed triggers, finalization is too early; entry is
# the completed permanent play, not the pending entry replacement hook.
for n in [525, 622, 727]:
    r = by[n]
    r['bindings'] = r['bindings'].replace('PLAY.finalized', 'PLAY.entered完成入场后（不是入场替代提交前）')
    append_review(n, '仅单位打出触发改用已成功入场后的PLAY.entered，不在finalized提前触发。')

# Public trash objects are selected at finalization unless a specific exception
# defers the selection; these four ordinary play instructions have no such exception.
for n in [753, 890, 894, 969]:
    r = by[n]
    r['calls'] = r['calls'].replace('targeting=False, bind_at="resolution"',
                                   'targeting=True, bind_at="finalization"')
    append_review(n, '按规则355.9/355.10公开废牌中的被选单位/装备在本项定稿作正式目标，不能结算再重选；play执行仍重查。')

for n, name in [(66, 'v'), (164, 'top'), (210, 'unit')]:
    r = by[n]
    r['bindings'] += ';permit:PlayPermission=本条能力授权该次所选并放逐的卡从己放逐区打出，其他限制仍检查'
    r['calls'] = r['calls'].replace('cost_policy=IGNORE_BASE_COST)',
                                    'cost_policy=IGNORE_BASE_COST, permission=permit)')
    r['calls'] = r['calls'].replace('cost_policy=policy)',
                                    'cost_policy=policy, permission=permit)')
    append_review(n, '补明确该次由本能力授予的放逐区打出来源许可。')

r = by[426]
r['bindings'] = r['bindings'].replace('本回合TURN_PHASE.end',
    '当前回合TURN_PHASE.start且phase=Ending，时点已过不建立也不顺延')
append_review(426, '延迟回合末绑定当前Ending开始，不是阶段结束；已过时点不顺延。')

# Official Radiance FAQ: the Exile's chosen play location is checked at finalization,
# before Baron Nashor's entry-destination replacement.
r = by[966]
r['bindings'] = ('subjects:EntrySelection=p未来PLAY单位，原定稿步骤355.2所选打出战场由p控制；'
                 '不因入场目的地替代改到其他战场而重判该既有入场修饰;entry:EntryState=活跃')
append_review(966, '依据Radiance FAQ与Baron场景，己控打出战场按355.2原定稿地点判断，修正先前入场时重查说法。')

r = by[793]
r['bindings'] = r['bindings'].replace('until:Duration=直到p下个EndingPhase',
    'until:Duration=直到未来p下一个EndingPhase开始，若当前已在Ending则指下一己回合Ending开始')
append_review(793, '按Radiance FAQ截止于未来下一个己Ending的开始，不能延至该阶段结束。')

path.write_text(''.join(json.dumps(r, ensure_ascii=False) + '\n' for r in rows), encoding='utf-8')
print({k: sum(r['status'] == k for r in rows) for k in ['confirmed','verify','uncovered']})
