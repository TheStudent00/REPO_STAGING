#!/bin/bash
# ref2 lane 3 -- CORRECTION 2: `adc` and `sbb` leave the carry they read IN
# THE FLAG STATE, and `carry_bit` and `overflow_bit` read the same sum the
# destination was computed from.
#
# The flag state becomes `reference.FlagState`, which IS the (setter, L, R)
# triple every reader already unpacks and carries the incoming carry beside
# it, so no other file's unpacking changes.
#
# Also in this lane: the count of (variant, place) keys the level-0 check
# writes more than once, because lane 2's before/after table read 411 refused
# places where the check's own tally reads 439 and the gap must be named.
#
# Memory bound: 6 GB; named abort ABORT_MEMORY_REF2.
set -u
HQ=PseudoCoupHQ
L0=$HQ/Research/oracle/arch_opcodes/level0
OP=$HQ/Research/op_pipeline
export HOME=/work/ref2home
mkdir -p "$HOME"

echo "[1/7] the diff LITERAL -- correction 2 against correction 1"
diff -u "$L0/ref2_originals/reference.py" "$OP/reference.py" | \
    sed -n '/FlagState/,$p' | head -160
echo "--- exit $?"

echo "[2/7] the reference_version AFTER correction 2"
sha256sum "$OP/reference.py" "$OP/condition_table.py"
echo "--- exit $?"

echo "[3/7] the rule, run on values -- sbb at L == R with the carry set"
python3 -c "
import sys
sys.path.insert(0, '$OP')
import z3, reference as R

def run(seed_line, line, l_value, r_value):
    state = R.MachineState()
    state.set_family('r10', z3.BitVecVal(l_value, 64))
    state.set_family('r11', z3.BitVecVal(r_value, 64))
    R.REFERENCE.step(state, seed_line)
    state.set_family('rdi', z3.BitVecVal(0x08, 64))
    state.set_family('rsi', z3.BitVecVal(0x08, 64))
    R.REFERENCE.step(state, line)
    return state

for l_value, r_value, carry in ((1, 0, 'carry in 0'), (0, 1, 'carry in 1')):
    state = run('cmp %r10d,%r11d', 'sbb %sil,%dil', l_value, r_value)
    print('%-12s  sbb %%sil,%%dil with 0x08 - 0x08 : destination 0x%x, CF %s'
          % (carry,
             z3.simplify(z3.Extract(7, 0, state.registers['rdi'])).as_long(),
             z3.simplify(z3.If(R.carry_bit(state.flags), 1, 0)).as_long()))
for l_value, r_value, carry in ((1, 0, 'carry in 0'), (0, 1, 'carry in 1')):
    state = run('cmp %r10d,%r11d', 'adc %sil,%dil', l_value, r_value)
    print('%-12s  adc %%sil,%%dil with 0x08 + 0x08 : destination 0x%x, CF %s'
          % (carry,
             z3.simplify(z3.Extract(7, 0, state.registers['rdi'])).as_long(),
             z3.simplify(z3.If(R.carry_bit(state.flags), 1, 0)).as_long()))
"
echo "--- exit $?"

echo "[4/7] the (variant, place) keys the check writes more than once"
python3 -c "
import collections, json
d = json.load(open('$L0/level0_check_ref2_c1.json'))
seen = collections.Counter()
for v in d['variants']:
    for p in v['places']:
        seen[(v['variant'], p['place'])] += 1
extra = {k: n for k, n in seen.items() if n > 1}
print('distinct (variant, place) keys %d, rows %d, keys written twice or more %d'
      % (len(seen), sum(seen.values()), len(extra)))
by_place = collections.Counter()
for k in extra:
    by_place[k[1]] += 1
for k in sorted(by_place, key=str):
    print('  place %-12s %d keys' % (k, by_place[k]))
for k in sorted(extra, key=str)[:5]:
    rows = [p for v in d['variants'] if v['variant'] == k[0]
            for p in v['places'] if p['place'] == k[1]]
    print('  %s at %s: %s' % (k[0], k[1], [r['outcome'] for r in rows]))
    for r in rows:
        print('      cause: %s' % (r.get('cause') or '(none)'))
"
echo "--- exit $?"

echo "[5/7] the level-0 check re-run -- level0_check_ref2_c2.json"
cd "$L0" || exit 1
python3 level0_check.py /sources/X86-64-semantics/semantics \
    "$L0/key_map.json" \
    "$L0/level0_check_ref2_c2.json" \
    "$L0/level0_check_ref2_c2.md" --workers=3 | tail -12
echo "--- exit $?"

echo "[6/7] before -> after, correction 1 -> correction 2"
python3 "$L0/ref2_compare.py" \
    "$L0/level0_check_ref2_c1.json" \
    "$L0/level0_check_ref2_c2.json" \
    "$L0/ref2_delta_c2.json" \
    "correction 2: adc and sbb leave the carry in the flag state"
echo "--- exit $?"

echo "[7/7] the L2 check: the sweep, then the theorems, then the tally"
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
cp "$OP/lean/check_L2.json" "$L0/ref2_check_L2_c2.json"
cp "$OP/lean/model_L2.json" "$L0/ref2_model_L2_c2.json"
echo "--- exit $?"
