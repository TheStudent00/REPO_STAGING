#!/usr/bin/env bash
# ref1 lane 7 -- build key_map.json: their variant names against our model
# table's (mnem, shape, key_width) keys, with every unmatched name on either
# side listed by cause.
set -euo pipefail
S=/sources/X86-64-semantics/semantics
L0=PseudoCoupHQ/Research/oracle/arch_opcodes/level0
M=PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json
total=3

echo "[1/$total] the map"
python3 $L0/key_map.py $S $M $L0/key_map.json

echo "[2/$total] the matched cells, by our shape and our mnemonic"
python3 -c "
import json
d = json.load(open('$L0/key_map.json'))
by_shape = {}
by_mnem = {}
for variant, r in d['matched'].items():
    by_shape[r['shape']] = by_shape.get(r['shape'], 0) + 1
    by_mnem[r['mnem']] = by_mnem.get(r['mnem'], 0) + 1
print('matched variants by our shape:')
for s in sorted(by_shape, key=lambda s: -by_shape[s]):
    print('%6d  %s' % (by_shape[s], s))
print('distinct mnemonics matched:', len(by_mnem))
print('the twenty with the most matched variants:')
for m in sorted(by_mnem, key=lambda m: -by_mnem[m])[:20]:
    print('%6d  %s' % (by_mnem[m], m))
"

echo "[3/$total] our triples with no counterpart, the first forty"
python3 -c "
import json
d = json.load(open('$L0/key_map.json'))
rows = d['unmatched_ours']
print('unmatched on our side:', len(rows))
by_shape = {}
for r in rows:
    by_shape[r['shape']] = by_shape.get(r['shape'], 0) + 1
for s in sorted(by_shape, key=lambda s: -by_shape[s]):
    print('%6d  %s' % (by_shape[s], s))
"
python3 -c "
import resource
print('peak RSS: %.1f MB' % (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024.0))
"
