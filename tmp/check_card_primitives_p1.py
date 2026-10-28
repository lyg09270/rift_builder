"""One-off document audit requested by the user; no game engine or test suite."""
import ast
import collections
import hashlib
import inspect
import json
import re
import sys
from pathlib import Path
from card_primitives_review_p1 import ROOT, OUT, META, CARDS, groups

sys.stdout.reconfigure(encoding='utf-8')
rows = [json.loads(s) for s in OUT.read_text(encoding='utf-8').splitlines()]
errors = []
assert [r['number'] for r in rows] == list(range(1, len(CARDS) + 1))
assert len({r['card_id'] for r in rows}) == len(CARDS)
assert len({r['review'] for r in rows}) == len(CARDS)
for path, digest in META.items():
    assert hashlib.sha256((ROOT/path).read_bytes()).hexdigest() == digest, path

signatures = {}
api = (ROOT/'docs/basic-primitives-v4-p1-frozen.md').read_text(encoding='utf-8')
for snippet in re.findall(r'```python\n(.*?)\n```', api, re.S):
    declaration = ast.parse('def ' + snippet.strip() + ':\n    pass').body[0]
    args = declaration.args
    parameters = []
    for i, arg in enumerate(args.args):
        required = i < len(args.args) - len(args.defaults)
        parameters.append(inspect.Parameter(arg.arg, inspect.Parameter.POSITIONAL_OR_KEYWORD,
                          default=inspect.Parameter.empty if required else None))
    for arg, default in zip(args.kwonlyargs, args.kw_defaults):
        parameters.append(inspect.Parameter(arg.arg, inspect.Parameter.KEYWORD_ONLY,
                          default=inspect.Parameter.empty if default is None else None))
    signatures[declaration.name] = inspect.Signature(parameters)
assert len(signatures) == 35

usage = collections.Counter()
frames = collections.Counter()
flow_nodes = collections.Counter()
calls = 0
checked = 0
literal_checks = 0
literal_values = {
    ('orientation_set', 1, 'state'): {'ready', 'exhausted'},
    ('status_set', 1, 'status'): {'STUNNED', 'FACE_DOWN'},
    ('stack_change', 1, 'quantity'): {'BUFF', 'EMPOWER_LAYER'},
    ('stack_change', 2, 'operation'): {'ADD', 'SPEND', 'REMOVE'},
    ('might_contribute', 1, 'layer'): {'BASE', 'ARITHMETIC', 'EQUIPMENT_BONUS', 'BUFF_VALUE'},
    ('trait_change', 1, 'trait'): {'TYPE', 'TAG'},
    ('trait_change', 2, 'operation'): {'ADD', 'REMOVE', 'REPLACE'},
    ('information_access', None, 'mode'): {'LOOK', 'REVEAL'},
    ('battlefield_bind', None, 'mode'): {'replace', 'restore'},
    ('xp_change', None, 'operation'): {'GAIN', 'SPEND'},
    ('procedure_skip', None, 'occurrence'): {'next', 'all_matching'},
}
direct_exceptions = []
keywords = ['Hidden', 'Accelerate', 'Assault', 'Shield', 'Deflect', 'Tank', 'Backline',
            'Ganking', 'Weaponmaster', 'Vision', 'Unique', 'Temporary', 'Ambush',
            'Quick-Draw', 'Equip', 'Empower', 'Action', 'Reaction']
for r in rows:
    number = r['number']
    assert r['card_id'] == CARDS[number-1][0]
    assert r['text_groups'] == groups(number), number
    assert r['api_sha256'] == META['docs/basic-primitives-v4-p1.md']
    assert r['source_sha256'] == META['data/sources/openrift/catalog.json']
    parts = r['primitive_sections'] + r['native_sections']
    for part in parts:
        tree = ast.parse(part['program'])
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            fun = node.func
            if isinstance(fun, ast.Name) and fun.id == 'action_frame':
                frames[node.args[0].value] += 1
            if not isinstance(fun, ast.Attribute) or not isinstance(fun.value, ast.Name):
                continue
            namespace = fun.value.id
            if namespace == 'ops':
                errors.append([number, 'unexpanded operator', fun.attr])
            if namespace == 'flow':
                flow_nodes[fun.attr] += 1
            if namespace != 'p':
                continue
            calls += 1
            usage[fun.attr] += 1
            if fun.attr not in signatures:
                errors.append([number, 'unknown primitive', fun.attr])
                continue
            try:
                signatures[fun.attr].bind(*[object() for _ in node.args],
                                         **{kw.arg: object() for kw in node.keywords})
                checked += 1
            except TypeError as exc:
                errors.append([number, fun.attr, str(exc)])
            for (name, pos, field), allowed in literal_values.items():
                if name != fun.attr:
                    continue
                value = next((kw.value for kw in node.keywords if kw.arg == field), None)
                if value is None and pos is not None and pos < len(node.args):
                    value = node.args[pos]
                if isinstance(value, ast.Constant) and isinstance(value.value, str):
                    literal_checks += 1
                    if value.value not in allowed:
                        errors.append([number, name, field, value.value])
    card = CARDS[number-1][1]
    errata = card.get('errata') or {}
    texts = [errata['correctedRulesText']] if errata.get('correctedRulesText') else [
        g['text'] or '' for g in r['text_groups'] if g['language'] == 'EN']
    declared = {x.split(':')[0].split('=')[0] for x in r['native']}
    for keyword in keywords:
        if any(re.search(r'^\[' + re.escape(keyword) + r'(?:\]|[ :—])', t, re.M) for t in texts):
            if keyword not in declared:
                direct_exceptions.append([number, keyword])

counts = collections.Counter(r['status'] for r in rows)
result = dict(cards=len(rows), total=len(CARDS), source_groups=sum(len(r['text_groups']) for r in rows),
              review_unique=len({r['review'] for r in rows}), counts=dict(counts),
              coverage=counts['covered']/len(CARDS), primitive_signatures=len(signatures),
              primitive_call_sites=calls, signatures_passed=checked,
              literal_checks=literal_checks, usage=dict(sorted(usage.items())),
              unused_primitives=sorted(set(signatures)-set(usage)),
              frames=dict(sorted(frames.items())), flow_nodes=dict(flow_nodes),
              source_issue_cards=sum(bool(r['source_issues']) for r in rows),
              direct_keyword_exceptions=direct_exceptions, errors=errors,
              semantic_execution_accuracy=None, frozen_inputs=META)
(ROOT/'tmp/card-primitives-p1-audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
print(json.dumps({k: v for k, v in result.items() if k not in ('usage', 'frames', 'flow_nodes', 'frozen_inputs')}, ensure_ascii=False, indent=2))
