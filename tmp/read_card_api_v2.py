"""R2 full-text reader: always print every EN/SC/TC variant plus errata and migrated call body."""
import sys,json,re,ast
from pathlib import Path
from read_card_operators import CARDS,variants,read,ROOT
sys.stdout.reconfigure(encoding='utf-8')
BASE={r['number']:r for r in map(json.loads,(ROOT/'tmp/card-api-review-v1.jsonl').read_text(encoding='utf-8').splitlines())}
def migrate(row):
 row=dict(row);text=row['calls']
 text=text.replace('ops.gain_xp(', 'ops.change_xp(').replace('ops.spend_xp(', 'ops.change_xp(')
 text=re.sub(r'ops\.set_might\((.*?), ([^\n,]+), direction="([a-z_]+)", duration=([^\n]+)\)',r'ops.modify_might(\1, change=MightChange.set(\2, direction="\3"), duration=\4)',text)
 text=re.sub(r'ops\.swap_might\((.*?), (.*?), duration=([^\n]+)\)',r'ops.modify_might([\1], change=MightChange.swap(\2), duration=\3)',text)
 text=re.sub(r'ops\.restore_battlefield\((.*?), link=([^\n]+)\)',r'ops.replace_battlefield(\1, mode="restore", link=\2)',text)
 row['calls']=text
 return row
if __name__=='__main__':
 for n in range(int(sys.argv[1]),int(sys.argv[2])+1):
  read(n,n)
  r=migrate(BASE[n]);print('V1待复核入口:',r['window']);print('V1参数:',r['bindings']);print('迁移草稿，未经第二轮认可:');print(r['calls'])
  for g in r['gaps']:
   if not g.startswith(('DATA:','LANG:')):print('V1待解决:',g)
