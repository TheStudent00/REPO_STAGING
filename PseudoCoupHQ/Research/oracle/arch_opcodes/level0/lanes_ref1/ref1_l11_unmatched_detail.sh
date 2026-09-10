#!/usr/bin/env bash
# ref1 lane 11 -- the unmatched variants of theirs, one level deeper than the
# cause: which (mnem, shape, width) our table lacks, and what the grammar's
# own refusals actually say, so each is either covered or reported as itself.
set -euo pipefail
L0=PseudoCoupHQ/Research/oracle/arch_opcodes/level0
total=4

echo "[1/$total] 'our model table has no translated row', by (shape, width)"
python3 -c "
import json, collections
d = json.load(open('$L0/key_map.json'))
want = 'our model table has no translated row at that operand form and width'
rows = [r for r in d['unmatched_theirs'] if r['reason'] == want]
c = collections.Counter((r.get('shape'), r.get('width')) for r in rows)
for k in sorted(c, key=str):
    print('%6d  shape %-20s width %s' % (c[k], k[0], k[1]))
print()
bym = collections.Counter(r['mnem'] for r in rows)
print('by their mnemonic, the twenty largest:')
for m in sorted(bym, key=lambda m: -bym[m])[:20]:
    print('%6d  %s' % (bym[m], m))
"

echo "[2/$total] the grammar's own refusals, with one example detail each"
python3 -c "
import json, collections
d = json.load(open('$L0/key_map.json'))
rows = [r for r in d['unmatched_theirs'] if r['reason'].startswith('their rule:')]
c = collections.Counter(r['reason'] for r in rows)
seen = {}
for r in rows:
    seen.setdefault(r['reason'], (r['variant'], r.get('detail')))
for k in sorted(c, key=lambda k: -c[k]):
    print('%6d  %s' % (c[k], k))
    print('        e.g. %s -- %s' % seen[k])
"

echo "[3/$total] our shapes' translated rows, so the join's denominator is visible"
python3 -c "
import json, collections
d = json.load(open('PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json'))
c = collections.Counter(str(r['shape']) for r in d['rows'] if r['outcome']=='TRANSLATED')
print('imm_symbolic_gpr translated rows:', c.get('imm_symbolic_gpr', 0))
print('mem_one translated rows:', c.get('mem_one', 0))
mn = set(r['mnem'] for r in d['rows'] if r['outcome']=='TRANSLATED' and r['shape']=='mem_one')
print('mnemonics with a translated mem_one row:', len(mn))
"

echo "[4/$total] which of their one-memory-operand variants exist"
python3 -c "
import json, collections
d = json.load(open('$L0/key_map.json'))
rows = [r for r in d['unmatched_theirs']]
c = collections.Counter(r['reason'] for r in rows if r['mnem'] in ('negl','notl','idivl','imull','divl','mull','incl','decl'))
for k in sorted(c, key=lambda k: -c[k]):
    print('%6d  %s' % (c[k], k))
"
