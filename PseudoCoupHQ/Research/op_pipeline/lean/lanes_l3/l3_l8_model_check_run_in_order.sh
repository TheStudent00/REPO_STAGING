#!/bin/bash
# l3 lane 8 -- the three commands in the order that leaves the artifact folder
# self-consistent: `model` (the sweep, which writes model_L2.json AND
# Model.lean), then `check` (which re-runs the sweep, adds any definition a
# unit's own body line needs, and rewrites Model.lean and every
# ModelCheck_*.lean), then `run` (one lean process per stated theorem).
#
# WHY THE SWEEP IS RE-RUN HERE.  Task ap5 (log 249) widened
# `model_translate.shapes_for` with four symbolic-immediate shapes on
# 2026-09-09 but restored every file it touched, so model_L2.json on disk is
# the census of the sweep BEFORE that widening while `check` writes a
# Model.lean from the sweep AFTER it.  Running `model` first makes the census
# describe the file that is actually on disk.
#
# Memory bound: 6 GB, named abort ABORT_MEMORY_L3.
set -u
LEANDIR=PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/l3home
mkdir -p "$HOME"
cd "$LEANDIR" || exit 1

echo "[1/5] model_translate.py model -- the sweep"
python3 -c "
import resource, sys, time
sys.path.insert(0, '$LEANDIR')
import model_translate as M, os
start = time.time()
M.model_command(M.HERE, os.path.join(M.HERE, 'archproof', 'Archproof'))
print('sweep wall %.1f s' % (time.time() - start))
print('sweep peak RSS %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
"
echo "--- exit $?"

echo "[2/5] model_translate.py check"
python3 -c "
import resource, sys, time
sys.path.insert(0, '$LEANDIR')
import model_translate as M
start = time.time()
M.check_command()
print('check wall %.1f s' % (time.time() - start))
print('check peak RSS %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
"
echo "--- exit $?"

echo "[3/5] lake build Archproof.Model, then model_translate.py run"
cd archproof || exit 1
time lake build Archproof.Model
echo "--- lake build exit $?"
cd "$LEANDIR" || exit 1
python3 model_translate.py run | tail -8
echo "--- run exit $?"

echo "[4/5] the census and the tally, off the two json files as they now stand"
python3 -c "
import collections, json
m = json.load(open('$LEANDIR/model_L2.json'))
per = m['per_mnemonic']
print('   mnemonics in the reference table : %d' % m['mnemonics_in_the_table'])
print('   definitions in model_L2.json     : %d' % m['definitions'])
print('   opaque float primitives          : %d' % len(m['opaque_float_primitives']))
print('   a census row, no builder         : %d' % sum(1 for x in per.values() if x['no_builder']))
print('   at least one shape translated    : %d' % sum(1 for x in per.values() if x['translated']))
print('   builder, no shape this sweep spells: %d' % sum(1 for x in per.values() if not x['translated'] and not x['no_builder']))
d = json.load(open('$LEANDIR/check_L2.json'))
t = collections.Counter()
for r in d['rows']:
    t[r.get('closed_by') or r.get('outcome')] += 1
print('   check rows %d' % len(d['rows']))
for k in sorted(t, key=str):
    print('   %-14s %d' % (k, t[k]))
print('   STATED %d   REFUSED %d   DISCREPANCY %d'
      % (sum(1 for r in d['rows'] if r['outcome'] == 'STATED'),
         sum(1 for r in d['rows'] if r['outcome'] == 'REFUSED'),
         sum(1 for r in d['rows'] if r['outcome'] == 'DISCREPANCY')))
"

echo "[5/5] the definition count in Model.lean itself"
grep -c '^def \|^opaque ' archproof/Archproof/Model.lean
wc -l archproof/Archproof/Model.lean
echo "--- exit $?"
