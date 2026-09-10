#!/bin/bash
# ref2 lane 5 -- CORRECTION 4: `sub` and `sbb` join
# `reference.WIDTH_IS_NOT_A_SUFFIX`, so their final `b` stops being read as a
# byte-size suffix; plus the AUDIT of every arch mnemonic that rule reaches,
# measured by running each builder with the mnemonic inside and outside the
# list and comparing what it computes.
#
# Memory bound: 6 GB; named abort ABORT_MEMORY_REF2.
set -u
HQ=PseudoCoupHQ
L0=$HQ/Research/oracle/arch_opcodes/level0
OP=$HQ/Research/op_pipeline
export HOME=/work/ref2home
mkdir -p "$HOME"

echo "[1/8] the diff LITERAL -- the list, before and after"
diff -u "$L0/ref2_originals/reference.py" "$OP/reference.py" | \
    sed -n '/WIDTH_IS_NOT_A_SUFFIX = frozenset/,/^ *])/p' | head -40
echo "--- exit $?"

echo "[2/8] the reference_version AFTER correction 4 -- the FINAL pair"
sha256sum "$OP/reference.py" "$OP/condition_table.py"
echo "--- exit $?"

echo "[3/8] the rule, run on values -- the width of the memory slot"
python3 -c "
import sys
sys.path.insert(0, '$OP')
import reference as R
state = R.MachineState()
for mnem in ('add', 'sub', 'sbb', 'adc', 'xor', 'movb'):
    ops = R.Operands(state, mnem, ['%esi', '(%rax)'])
    print('destination_width of %-5s %%esi,(%%rax) is %d'
          % (mnem, ops.destination_width()))
"
echo "--- exit $?"

echo "[4/8] the audit of every size-lettered mnemonic"
python3 "$L0/ref2_suffix_audit.py" "$L0/ref2_suffix_audit.json"
echo "--- exit $?"

echo "[5/8] the level-0 check re-run -- level0_check_ref2_c4.json"
cd "$L0" || exit 1
python3 level0_check.py /sources/X86-64-semantics/semantics \
    "$L0/key_map.json" \
    "$L0/level0_check_ref2_c4.json" \
    "$L0/level0_check_ref2_c4.md" --workers=3 | tail -12
echo "--- exit $?"

echo "[6/8] before -> after, correction 3 -> correction 4"
python3 "$L0/ref2_compare.py" \
    "$L0/level0_check_ref2_c3.json" \
    "$L0/level0_check_ref2_c4.json" \
    "$L0/ref2_delta_c4.json" \
    "correction 4: sub and sbb are not size-suffixed"
echo "--- exit $?"

echo "[7/8] the whole way: the baseline against the four corrections together"
python3 "$L0/ref2_compare.py" \
    "$L0/level0_check_ref2_before.json" \
    "$L0/level0_check_ref2_c4.json" \
    "$L0/ref2_delta_whole.json" \
    "the four corrections together"
echo "  --- and whatever still disagrees, in full:"
python3 -c "
import json
d = json.load(open('$L0/level0_check_ref2_c4.json'))
for g in d['disagreements']:
    print('%4d  %-38s %s' % (g['count'], g['cause_key'],
                             ' '.join(m['mnem'] for m in g['mnems'])))
for v in d['variants']:
    for p in v['places']:
        if p['outcome'] != 'sat':
            continue
        print('')
        print('  %s (%s %s %s) at %s'
              % (v['variant'], v['mnem'], v['shape'], v['key_width'],
                 p['place']))
        print('    line   : %s' % v['line'])
        print('    ours   : %s' % p['ours'])
        print('    theirs : %s' % p['theirs'])
        print('    at the counterexample: ours %s, theirs %s'
              % (p['ours_at_the_counterexample'],
                 p['theirs_at_the_counterexample']))
        print('    counterexample: %s'
              % ', '.join('%s=%s' % (c['symbol'], c['text'])
                          for c in p['counterexample']))
"
echo "--- exit $?"

echo "[8/8] the L2 check: the sweep, then the theorems, then the tally"
cd "$OP/lean" || exit 1
python3 -c "
import os, resource, sys, time
sys.path.insert(0, '$OP/lean')
import model_translate as M
start = time.time()
M.model_command(M.HERE, os.path.join(M.HERE, 'archproof', 'Archproof'))
print('sweep wall %.1f s, peak RSS %d kB'
      % (time.time() - start, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
start = time.time()
M.check_command()
print('check wall %.1f s, peak RSS %d kB'
      % (time.time() - start, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss))
"
echo "--- sweep+check exit $?"
cd "$OP/lean/archproof" || exit 1
lake build Archproof.Model 2>&1 | tail -3
echo "--- lake build exit $?"
cd "$OP/lean" || exit 1
python3 model_translate.py run | tail -6
echo "--- run exit $?"
python3 -c "
import collections, json
d = json.load(open('$OP/lean/check_L2.json'))
rows = d['rows']
print('rows %d' % len(rows))
print('STATED %d' % sum(1 for r in rows if r['outcome'] == 'STATED'))
print('REFUSED %d' % sum(1 for r in rows if r['outcome'] == 'REFUSED'))
print('DISCREPANCY %d' % sum(1 for r in rows if r['outcome'] == 'DISCREPANCY'))
t = collections.Counter()
for r in rows:
    t[r.get('closed_by') or r.get('outcome')] += 1
for k in sorted(t, key=str):
    print('  %-16s %d' % (k, t[k]))
"
cp "$OP/lean/check_L2.json" "$L0/ref2_check_L2_c4.json"
cp "$OP/lean/model_L2.json" "$L0/ref2_model_L2_c4.json"
echo "--- exit $?"
