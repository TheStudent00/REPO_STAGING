#!/bin/bash
# ref2 lane 2 -- CORRECTION 1: `reference.full64` keeps the register's other
# bits at write widths 8 and 16 and zero-extends at 32, which is Intel SDM
# Vol. 1 section 3.4.1.1's own rule and the rule `reference.place_bits`
# already stated in its docstring.
#
# It re-runs task ref1's level-0 check into a NEW pair of files beside every
# earlier pair, compares it place by place with the baseline, and re-runs the
# L2 check (the sweep, the Lean theorems, the tally 259 / 172 / 87).
#
# Memory bound: 6 GB; named abort ABORT_MEMORY_REF2.
set -u
HQ=PseudoCoupHQ
L0=$HQ/Research/oracle/arch_opcodes/level0
OP=$HQ/Research/op_pipeline
export HOME=/work/ref2home
mkdir -p "$HOME"

echo "[1/6] the diff LITERAL -- what changed in reference.py"
diff -u "$L0/ref2_originals/reference.py" "$OP/reference.py"
echo "--- diff exit $? (1 means there is a difference, which is the point)"

echo "[2/6] the reference_version AFTER correction 1"
sha256sum "$OP/reference.py" "$OP/condition_table.py"
echo "--- exit $?"

echo "[3/6] the rule, run on values -- a one-byte, two-byte, four-byte and eight-byte write into a register holding all ones"
python3 -c "
import sys
sys.path.insert(0, '$OP')
import z3, reference as R
state = R.MachineState()
state.set_family('rax', z3.BitVecVal(0xffffffffffffffff, 64))
R.REFERENCE.step(state, 'mov \$0x1,%al')
print('after  mov \$0x1,%%al   into 0xffffffffffffffff : 0x%x'
      % z3.simplify(state.registers['rax']).as_long())
state = R.MachineState()
state.set_family('rax', z3.BitVecVal(0xffffffffffffffff, 64))
R.REFERENCE.step(state, 'mov \$0x1,%ax')
print('after  mov \$0x1,%%ax   into 0xffffffffffffffff : 0x%x'
      % z3.simplify(state.registers['rax']).as_long())
state = R.MachineState()
state.set_family('rax', z3.BitVecVal(0xffffffffffffffff, 64))
R.REFERENCE.step(state, 'mov \$0x1,%eax')
print('after  mov \$0x1,%%eax  into 0xffffffffffffffff : 0x%x'
      % z3.simplify(state.registers['rax']).as_long())
state = R.MachineState()
state.set_family('rax', z3.BitVecVal(0xffffffffffffffff, 64))
R.REFERENCE.step(state, 'mov \$0x1,%rax')
print('after  mov \$0x1,%%rax  into 0xffffffffffffffff : 0x%x'
      % z3.simplify(state.registers['rax']).as_long())
"
echo "--- exit $?"

echo "[4/6] the level-0 check re-run -- level0_check_ref2_c1.json"
cd "$L0" || exit 1
python3 level0_check.py /sources/X86-64-semantics/semantics \
    "$L0/key_map.json" \
    "$L0/level0_check_ref2_c1.json" \
    "$L0/level0_check_ref2_c1.md" --workers=3 | tail -12
echo "--- exit $?"

echo "[5/6] before -> after, per written place"
python3 "$L0/ref2_compare.py" \
    "$L0/level0_check_ref2_before.json" \
    "$L0/level0_check_ref2_c1.json" \
    "$L0/ref2_delta_c1.json" \
    "correction 1: full64 keeps the upper bits at 8 and 16"
echo "--- exit $?"

echo "[6/6] the L2 check: the sweep, then the theorems, then the tally"
cd "$OP/lean" || exit 1
if [ ! -f "$OP/lean/check_L2.json.before_ref2" ]; then
    cp "$OP/lean/check_L2.json" "$OP/lean/check_L2.json.before_ref2"
    cp "$OP/lean/model_L2.json" "$OP/lean/model_L2.json.before_ref2"
    echo "  kept the pre-ref2 pair as check_L2.json.before_ref2 / model_L2.json.before_ref2"
fi
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
lake build Archproof.Model 2>&1 | tail -5
echo "--- lake build exit $?"
cd "$OP/lean" || exit 1
python3 model_translate.py run | tail -8
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
cp "$OP/lean/check_L2.json" "$L0/ref2_check_L2_c1.json"
cp "$OP/lean/model_L2.json" "$L0/ref2_model_L2_c1.json"
echo "--- exit $?"
