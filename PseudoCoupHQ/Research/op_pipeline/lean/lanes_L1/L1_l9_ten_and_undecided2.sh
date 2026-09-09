#!/bin/bash
# L1 lane 9 — the ten and the three, after two fixes lane 8 forced:
#   the z3 rebuild tried to give a bit POSITION a width and stopped;
#   a pool5 entry's field is `layer5_normalized_texts`, a LIST of the distinct
#   printed texts among its members, not a single `layer5_normalized_text`.
set -u
LEANDIR=/projects/PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L1home
mkdir -p "$HOME"
echo '[1/2] the ten theorems'
python3 "$LEANDIR/run_edges_L1.py" ten
echo "--- ten exit $?"
echo '[2/2] the three pairs t100 left UNDECIDED'
python3 "$LEANDIR/run_edges_L1.py" undecided
echo "--- undecided exit $?"
