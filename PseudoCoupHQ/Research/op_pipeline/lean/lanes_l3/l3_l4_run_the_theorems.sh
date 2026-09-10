#!/bin/bash
# l3 lane 4 -- run every STATED theorem the corrected composer wrote: `rfl`
# first, then the model definitions unfolded and the goal bit-blasted with the
# SAT certificate checked in Lean.  One `lake env lean` process per theorem,
# each carrying its own wall clock and peak RSS from `os.wait4`.  This mutates
# check_L2.json in place, adding the outcome fields.
#
# Memory bound: 6 GB, named abort ABORT_MEMORY_L3.  L1 measured bv_decide on
# these widths under 500 MB; the one 16-bit division that took 12 GB is not
# posed here.
set -u
LEANDIR=PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/l3home
mkdir -p "$HOME"
cd "$LEANDIR/archproof" || exit 1

echo "[1/3] lake build Archproof.Model -- one elaboration of the model, not 172"
time lake build Archproof.Model
echo "--- lake build exit $?"

cd "$LEANDIR" || exit 1
echo "[2/3] model_translate.py run"
python3 model_translate.py run
echo "--- run exit $?"

echo "[3/3] the nineteen, their outcome after the run"
python3 -c "
import json
NINETEEN = ['c/op_113','c/op_133','c/regen_8997','c/regen_9822','c/op_138',
            'c/op_145','c/op_149','cpp/op_113','cpp/op_133','cpp/regen_8581',
            'cpp/regen_8966','cpp/op_138','cpp/op_145','cpp/op_149',
            'go/op_348','go/op_355','rust/op_570','rust/op_577',
            'rust/regen_1043']
d = json.load(open('$LEANDIR/check_L2.json'))
by = dict((r['unit'], r) for r in d['rows'])
print('| unit | theorem | outcome | closed by | wall s | peak kB |')
print('|---|---|---|---|---|---|')
for unit in NINETEEN:
    r = by[unit]
    print('| %s | %s | %s | %s | %s | %s |'
          % (unit, r.get('theorem_name'), r['outcome'],
             r.get('closed_by'), r.get('wall_seconds'), r.get('peak_kb')))
    if r['outcome'] != 'STATED' or not r.get('closed_by'):
        print('   cause: %s' % r.get('cause'))
"
echo "--- exit $?"
