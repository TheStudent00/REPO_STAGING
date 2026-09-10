#!/usr/bin/env bash
# ref1 lane 19 -- one level deeper than each disagreement's cause: the set of
# mnemonics at risk from the AT&T-suffix width rule, the corpus's own rows
# behind the affected cells, the undefined-region table, and two spot checks
# that an `unsat` is a real agreement and not a term compared with itself.
set -euo pipefail
L0=PseudoCoupHQ/Research/oracle/arch_opcodes/level0
P=PseudoCoupHQ/Research/op_pipeline
total=5

echo "[1/$total] every table mnemonic whose last letter is an AT&T size letter and which the exempt list does not hold"
python3 -c "
import sys; sys.path.insert(0, '$P')
import reference as R
at_risk = []
for mnem in sorted(R.REFERENCE.opcode_table.entries):
    if mnem[-1:] in R.SIZE_LETTER and mnem not in R.WIDTH_IS_NOT_A_SUFFIX:
        at_risk.append({'mnem': mnem, 'read_as': R.SIZE_LETTER[mnem[-1:]]})
print('at risk:', len(at_risk))
for r in at_risk:
    print('  %-10s its last letter would be read as width %d' % (r['mnem'], r['read_as']))
"

echo "[2/$total] the width our reference gives a memory destination for those, one line each"
python3 -c "
import sys; sys.path.insert(0, '$P')
import reference as R
s = R.MachineState()
for mnem in ('sub', 'add', 'xor', 'mov', 'shl', 'sar', 'adc', 'sbb'):
    ops = R.Operands(s, mnem, ['%esi', '(%rax)'])
    try:
        print('%-6s %s -> width %d' % (mnem, '%esi,(%rax)', ops.destination_width()))
    except Exception as e:
        print('%-6s refused: %s' % (mnem, e))
"

echo "[3/$total] the corpus's own ledger rows behind the cells this check found disagreeing"
python3 -c "
import json
key = json.load(open('$L0/key_map.json'))
chk = json.load(open('$L0/level0_check.json'))
bad = {}
for v in chk['variants']:
    n = sum(1 for p in v['places'] if p['outcome'] == 'sat')
    if not n:
        continue
    k = (v['mnem'], v['shape'], v['key_width'])
    bad[k] = max(bad.get(k, 0), v['attestation_ledger_rows'])
print('distinct (mnem, shape, key_width) cells with at least one disagreement:', len(bad))
print('their corpus ledger rows, summed:', sum(bad.values()))
top = sorted(bad.items(), key=lambda kv: -kv[1])[:20]
for (m, sh, w), n in top:
    print('  %-8s %-16s width %-4s %6d ledger rows' % (m, sh, w, n))
"

echo "[4/$total] the undefined-region table"
python3 -c "
import json
d = json.load(open('$L0/level0_check.json'))
print('mnemonics with an undefined region:', len(d['undefined_regions']))
for r in d['undefined_regions']:
    print('  %-10s whole: %-16s partial: %s' % (r['mnem'],
          ' '.join(r['whole']) or '--', ' '.join(r['partial']) or '--'))
"

echo "[5/$total] two spot checks that an unsat is a real agreement"
python3 -c "
import json
d = json.load(open('$L0/level0_check.json'))
for want in ('movl_r32_r32', 'notl_r32', 'xorl_r32_r32', 'shll_r32_cl'):
    for v in d['variants']:
        if v['variant'] != want:
            continue
        print('==', v['variant'], v.get('line'))
        for p in v['places']:
            print('   %-12s %-10s %s' % (p['place'], p['outcome'], (p.get('reason') or '')[:70]))
"
