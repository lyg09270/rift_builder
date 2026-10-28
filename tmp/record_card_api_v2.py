"""Persist an explicit, manually reread R2 decision for each card. No semantic classifier."""
import sys,json,hashlib
from pathlib import Path
from read_card_api_v2 import BASE,migrate
from read_card_operators import ROOT,CARDS,variants
sys.stdin.reconfigure(encoding='utf-8');sys.stdout.reconfigure(encoding='utf-8')
path=ROOT/'tmp/card-api-review-v2.jsonl'
rows={r['number']:r for r in map(json.loads,path.read_text(encoding='utf-8').splitlines())} if path.exists() else {}
for line in sys.stdin.read().splitlines():
 if not line.strip():continue
 if line.count('|')!=4:raise ValueError('expected number|new review|bindings (= retains checked draft)|calls (= retains checked draft)|gaps (- clears semantic gaps, = retains)')
 number,review,bindings,calls,gaps=line.split('|');n=int(number)
 if n in rows:raise ValueError(f'already reread {n}')
 if len(review)<12:raise ValueError('need a card-specific semantic review')
 r=migrate(BASE[n]);r['review']=review
 if bindings!='=':r['bindings']=bindings
 if calls!='=':r['calls']=calls.replace('\\n','\n')
 if gaps!='=':r['gaps']=[g for g in r['gaps'] if g.startswith(('DATA:','LANG:'))]+([] if gaps=='-' else gaps.split(';'))
 r['round']=2;r['api_sha256']=hashlib.sha256((ROOT/'docs/basic-operators-api.md').read_bytes()).hexdigest()
 r['text_groups']=[hashlib.sha256(json.dumps(key,ensure_ascii=False).encode()).hexdigest() for key,faces in variants(CARDS[n-1][0])]
 rows[n]=r
path.write_text(''.join(json.dumps(rows[n],ensure_ascii=False)+'\n' for n in sorted(rows)),encoding='utf-8')
print('R2 manual full readings:',len(rows),'/',len(CARDS))
