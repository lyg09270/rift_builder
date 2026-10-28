"""Temporary document-authoring aid; no game execution or semantic matching."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / 'data/sources/openrift/catalog.json'
CAT = json.loads(SOURCE.read_text(encoding='utf-8'))
CARDS = sorted(CAT['cards'].items(), key=lambda item: (item[1]['name'].casefold(), item[0]))
FACES = defaultdict(list)

def visit(face, printing_id, path='front'):
    FACES[face['cardId']].append(dict(face, printing_id=printing_id, face_path=path))
    if isinstance(face.get('side2'), dict):
        visit(face['side2'], printing_id, path + '.side2')

for pid, face in CAT['printings'].items():
    visit(face, pid)

def variants(cid, languages=('EN', 'SC', 'TC')):
    groups = defaultdict(list)
    for face in FACES[cid]:
        if face['language'] in languages:
            groups[(face['language'], face.get('printedRulesText'), face.get('printedEffectText'))].append(face)
    return sorted(groups.items(), key=lambda kv: (languages.index(kv[0][0]), min(f.get('canonicalRank', 10**9) for f in kv[1])))

def read(start, end):
    for n in range(start, min(end, len(CARDS)) + 1):
        cid, c = CARDS[n-1]
        print(f"\n#{n:04d} {c['name']} | {c['slug']} | {','.join(c['types'])}/{','.join(c['superTypes'])} | {','.join(c['domains'])} E/P/M={c['energy']}/{c['power']}/{c['might']} | tags={','.join(c['tags'])} | keywords={','.join(c['keywords'])}")
        extras = {k:c[k] for k in ('mightBonus','maxCopiesOverride','additionalLegendCount','tokenCardIds','bans') if c.get(k) not in (None, [], {})}
        if extras: print('ATTR', json.dumps(extras, ensure_ascii=False))
        for (lang, text, effect), faces in variants(cid):
            f = min(faces, key=lambda f:f.get('canonicalRank', 10**9))
            print(f"{lang} {f['shortCode']} {f.get('printedName')!r} [{len(faces)} faces] {f['face_path']}")
            print('RULES:', text if text is not None else '<null>')
            if effect is not None: print('EFFECT:',effect)
        if c.get('errata') is not None: print('ERRATA', json.dumps(c['errata'], ensure_ascii=False))
        if not FACES[cid]: print('NO PRINTED FACE IN SNAPSHOT')

if __name__ == '__main__':
    p=argparse.ArgumentParser()
    p.add_argument('start',type=int)
    p.add_argument('end',type=int)
    a=p.parse_args()
    read(a.start,a.end)
