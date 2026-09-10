#!/bin/bash
# ref2 lane 4 -- CORRECTION 3: a condition is a reading of THE FLAGS the
# setter wrote, not a re-derivation from the setter's two operands.
#
# `reference.flag_result` states the value each builder produced,
# `reference.FlagReading.bit` computes CF/ZF/SF/OF/PF from it, and
# `condition_table.cond_from_flags` is Intel's own condition table over those
# five.  `condition_table.cond_to_z3` keeps its body and its 112-row proof
# against angr, and keeps the callers it is right for.
#
# The acceptance criterion the brief names is measured in step [3/8]: the
# `sub` and `cmp` rows must not move and the `add` and `neg` rows must.
#
# Memory bound: 6 GB; named abort ABORT_MEMORY_REF2.
set -u
HQ=PseudoCoupHQ
L0=$HQ/Research/oracle/arch_opcodes/level0
OP=$HQ/Research/op_pipeline
export HOME=/work/ref2home
mkdir -p "$HOME"

echo "[1/8] the diff LITERAL -- condition_table.py, whole"
diff -u "$L0/ref2_originals/condition_table.py" "$OP/condition_table.py"
echo "--- exit $?"

echo "[2/8] the reference_version AFTER correction 3"
sha256sum "$OP/reference.py" "$OP/condition_table.py"
echo "--- exit $?"

echo "[3/8] every condition after every setter, before -> after, z3's verdict"
python3 "$L0/ref2_condition_proof.py" "$L0/ref2_condition_proof.json"
echo "--- exit $?"

echo "[4/8] the rule, run on values -- the zero flag after an addition"
python3 -c "
import sys
sys.path.insert(0, '$OP')
import z3, reference as R
for line, mnem in (('add %sil,%dil', 'add'), ('sub %sil,%dil', 'sub')):
    for a, b in ((8, 8), (8, 0xf8)):
        state = R.MachineState()
        state.set_family('rdi', z3.BitVecVal(a, 64))
        state.set_family('rsi', z3.BitVecVal(b, 64))
        R.REFERENCE.step(state, line)
        zero = z3.simplify(z3.If(R.predicate_of(state, 'e'), 1, 0)).as_long()
        sign = z3.simplify(z3.If(R.predicate_of(state, 's'), 1, 0)).as_long()
        result = z3.simplify(z3.Extract(7, 0, state.registers['rdi'])).as_long()
        print('%-14s %%dil=0x%02x %%sil=0x%02x -> result 0x%02x  ZF %d  SF %d'
              % (line, a, b, result, zero, sign))
state = R.MachineState()
state.set_family('rdi', z3.BitVecVal(0x40000000, 64))
R.REFERENCE.step(state, 'neg %edi')
print('neg %%edi        %%edi=0x40000000 -> result 0x%08x  SF %d'
      % (z3.simplify(z3.Extract(31, 0, state.registers['rdi'])).as_long(),
         z3.simplify(z3.If(R.predicate_of(state, 's'), 1, 0)).as_long()))
"
echo "--- exit $?"

echo "[5/8] the level-0 check re-run -- level0_check_ref2_c3.json"
cd "$L0" || exit 1
python3 level0_check.py /sources/X86-64-semantics/semantics \
    "$L0/key_map.json" \
    "$L0/level0_check_ref2_c3.json" \
    "$L0/level0_check_ref2_c3.md" --workers=3 | tail -12
echo "--- exit $?"

echo "[6/8] before -> after, correction 2 -> correction 3"
python3 "$L0/ref2_compare.py" \
    "$L0/level0_check_ref2_c2.json" \
    "$L0/level0_check_ref2_c3.json" \
    "$L0/ref2_delta_c3.json" \
    "correction 3: a condition reads the flags the setter wrote"
echo "--- exit $?"

echo "[7/8] the places that still disagree, by cause"
python3 -c "
import collections, json
d = json.load(open('$L0/level0_check_ref2_c3.json'))
for g in d['disagreements']:
    print('%4d  %-38s %s' % (g['count'], g['cause_key'],
                             ' '.join(m['mnem'] for m in g['mnems'])))
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
cp "$OP/lean/check_L2.json" "$L0/ref2_check_L2_c3.json"
cp "$OP/lean/model_L2.json" "$L0/ref2_model_L2_c3.json"
echo "--- exit $?"
