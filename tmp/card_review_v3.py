"""R3 reading/authoring aid. Records require an explicit per-card human-authored review."""
import ast,hashlib,json,re,sys
from pathlib import Path
from read_card_operators import ROOT,CARDS,variants,read,SOURCE
sys.stdout.reconfigure(encoding='utf-8')
API=ROOT/'docs/basic-operators-api.md'
FROZEN='2530366c3f814b7f77f992ffe36c7c5bf3a0ad5fa23812de34119a6ea4dd03a3'
assert hashlib.sha256(API.read_bytes()).hexdigest()==FROZEN,'Frozen API changed'
BASE={r['number']:r for r in map(json.loads,(ROOT/'tmp/card-api-review-v2.jsonl').read_text(encoding='utf-8').splitlines())}
for r in map(json.loads,(ROOT/'tmp/card-api-rulings-v2.1.jsonl').read_text(encoding='utf-8').splitlines()):BASE[r['number']]=r
OUT=ROOT/'tmp/card-api-review-v3.jsonl'

def groups(n):
 return [dict(language=l,text=a,effect=b,hash=hashlib.sha256(json.dumps([l,a,b],ensure_ascii=False).encode()).hexdigest()) for (l,a,b),fs in variants(CARDS[n-1][0])]

def migrate(text):
 # Rename only registered calls; this produces a draft, never a semantic approval.
 for old,new,mode in [('ready','orient','ready'),('exhaust','orient','exhausted'),('empower','change_empowerment','empower'),('disempower','change_empowerment','disempower')]:
  tree=ast.parse(text);changes=[]
  lines=text.splitlines(keepends=True);offsets=[0]
  for line in lines:offsets.append(offsets[-1]+len(line))
  for node in ast.walk(tree):
   if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and isinstance(node.func.value,ast.Name) and node.func.value.id=='ops' and node.func.attr==old:
    src=ast.get_source_segment(text,node);src=src.replace('ops.'+old+'(','ops.'+new+'(',1)
    first=node.args[0];end=offsets[first.end_lineno-1]+first.end_col_offset;relative=end-(offsets[node.lineno-1]+node.col_offset)
    relative+=len(new)-len(old)
    src=src[:relative]+', "'+mode+'"'+src[relative:]
    changes.append((offsets[node.lineno-1]+node.col_offset,offsets[node.end_lineno-1]+node.end_col_offset,src))
  for a,b,src in sorted(changes,reverse=True):text=text[:a]+src+text[b:]
 return text

def draft(n):
 r=dict(BASE[n]);r['calls']=migrate(r['calls']);return r

def show(a,b):
 for n in range(a,b+1):
  read(n,n);r=draft(n)
  print('ENTRY',r['window']);print('BIND',r['bindings']);print('DRAFT\n'+r['calls'])
  for gap in r['gaps']:print('ISSUE',gap)

def record(data):
 existing=[json.loads(x) for x in OUT.read_text(encoding='utf-8').splitlines()] if OUT.exists() else []
 by={r['number']:r for r in existing}
 for item in data:
  n=item['number'];assert n not in by,('already reviewed',n)
  assert item['status'] in ['confirmed','verify','uncovered'] and len(item['review'])>=12
  r=draft(n);r.update(round=3,api_version='3',api_sha256=FROZEN,text_groups=groups(n))
  r.pop('scope',None);r.pop('verdict',None)
  r.update(item)
  # Previous source discrepancies survive unless explicitly superseded with evidence.
  source_gaps=[g for g in r.get('gaps',[]) if g.startswith(('DATA:','LANG:'))]
  r['gaps']=source_gaps+item.get('issues',[])
  if r['status']!='confirmed':assert item.get('issues'),n
  ast.parse(r['calls']);by[n]=r
 OUT.write_text(''.join(json.dumps(by[n],ensure_ascii=False)+'\n' for n in sorted(by)),encoding='utf-8')
 print(json.dumps(dict(read=len(by),confirmed=sum(r['status']=='confirmed' for r in by.values()),verify=sum(r['status']=='verify' for r in by.values()),uncovered=sum(r['status']=='uncovered' for r in by.values())),ensure_ascii=False))

if __name__=='__main__':
 if sys.argv[1]=='read':show(int(sys.argv[2]),int(sys.argv[3]))
 elif sys.argv[1]=='record':record(json.load(sys.stdin))
 elif sys.argv[1]=='status':
  rows=[json.loads(x) for x in OUT.read_text(encoding='utf-8').splitlines()] if OUT.exists() else []
  print(len(rows),[r['number'] for r in rows if r['status']!='confirmed'])
