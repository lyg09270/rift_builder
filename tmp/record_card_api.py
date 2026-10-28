"""Documentation authoring: persist manually reviewed API call blocks."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding='utf-8')
sys.stdin.reconfigure(encoding='utf-8')
root = Path(__file__).resolve().parents[1]
path = root / 'tmp/card-api-review.jsonl'
records = {}
if path.exists():
    for line in path.read_text(encoding='utf-8').splitlines():
        row = json.loads(line)
        records[row['number']] = row
for line in sys.stdin.read().splitlines():
    if not line.strip():
        continue
    if line.count('|') != 4:
        raise ValueError('A manual row must contain exactly four field delimiters')
    number, window, bindings, calls, gaps = line.split('|', 4)
    number = int(number)
    if number in records:
        raise ValueError(f'Already recorded: {number}')
    records[number] = dict(number=number, window=window, bindings=bindings,
                           calls=calls.replace('\\n', '\n'),
                           gaps=[] if gaps == '-' else gaps.split(';'))
path.write_text(''.join(json.dumps(records[k], ensure_ascii=False) + '\n'
                        for k in sorted(records)), encoding='utf-8')
print(f'Manually reviewed API records: {len(records)}, last={max(records, default=0)}')
