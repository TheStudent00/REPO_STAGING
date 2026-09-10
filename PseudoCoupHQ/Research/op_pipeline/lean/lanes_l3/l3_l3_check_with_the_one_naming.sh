#!/bin/bash
# l3 lane 3 -- `model_translate.py check` with the composer's naming corrected:
# both sides of every theorem now carry the names the STORED layer-5 line gave
# the unit's arrivals, and the naming is proved against that line per row.
# This REWRITES Model.lean, every ModelCheck_*.lean and check_L2.json; the
# theorems themselves are run by the next lane.
#
# Memory bound: 6 GB, named abort ABORT_MEMORY_L3 (model_translate's own
# MEMORY_CEILING_KB guards the streaming; this lane prints its peak RSS too).
set -u
TOTAL=3
LEANDIR=PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/l3home
mkdir -p "$HOME"
cd "$LEANDIR" || exit 1

echo "[1/$TOTAL] the tally BEFORE, off check_L2.json as it stands"
python3 -c "
import collections, json
d = json.load(open('$LEANDIR/check_L2.json'))
t = collections.Counter()
for r in d['rows']:
    t[r.get('closed_by') or r.get('outcome')] += 1
print('   rows %d' % len(d['rows']))
for k in sorted(t, key=str):
    print('   %-14s %d' % (k, t[k]))
print('   STATED total %d' % sum(v for k, v in t.items() if k != 'REFUSED'))
"

echo "[2/$TOTAL] model_translate.py check"
python3 -c "
import resource, sys, time
sys.path.insert(0, '$LEANDIR')
import model_translate as M
start = time.time()
M.check_command()
print('check wall %.1f s' % (time.time() - start))
print('check peak RSS %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
"

echo "[3/$TOTAL] the nineteen, one line each, as the check now states them"
python3 -c "
import json
NINETEEN = ['c/op_113','c/op_133','c/regen_8997','c/regen_9822','c/op_138',
            'c/op_145','c/op_149','cpp/op_113','cpp/op_133','cpp/regen_8581',
            'cpp/regen_8966','cpp/op_138','cpp/op_145','cpp/op_149',
            'go/op_348','go/op_355','rust/op_570','rust/op_577',
            'rust/regen_1043']
d = json.load(open('$LEANDIR/check_L2.json'))
by = dict((r['unit'], r) for r in d['rows'])
for unit in NINETEEN:
    r = by[unit]
    print('   %-18s %-12s %s' % (unit, r['outcome'], r.get('theorem_name','')))
    print('      left  : %s' % r.get('left'))
    print('      right : %s' % r.get('right'))
"
echo "--- exit $?"
