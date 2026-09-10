#!/usr/bin/env bash
# ref1 lane 17 -- the whole check: key_map.json rebuilt, then every matched
# variant compared place by place, at most three solver processes, the 3,000
# ms ceiling with one re-pose at 30,000 ms for the wide multiply and the
# divisions.  Memory bound 6 GB with the named abort ABORT_MEMORY_REF1.
set -euo pipefail
S=/sources/X86-64-semantics/semantics
L0=PseudoCoupHQ/Research/oracle/arch_opcodes/level0
total=4

echo "[1/$total] the key map"
python3 $L0/key_map.py $S PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json $L0/key_map.json

echo "[2/$total] the check over every matched variant"
cd $L0
python3 level0_check.py $S $L0/key_map.json $L0/level0_check.json $L0/level0_check.md --workers=3

echo "[3/$total] the headline and the per-mnemonic totals"
python3 -c "
import json
d = json.load(open('$L0/level0_check.json'))
print('totals:', json.dumps(d['totals']))
print('variants all-agree', d['variants_agreeing_on_every_place'],
      'with a disagreement', d['variants_with_a_disagreement'])
print()
print('disagreement groups:')
for g in d['disagreements']:
    print('%6d  %s   %s' % (g['count'], g['cause_key'],
          ' '.join(m['mnem'] for m in g['mnems'][:14])))
print()
print('refusal causes:')
for r in d['refusals']:
    print('%6d  %s' % (r['count'], r['reason'][:110]))
"

echo "[4/$total] the guard, unmodified, over every json this task wrote"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    $L0/key_map.json $L0/level0_check.json
