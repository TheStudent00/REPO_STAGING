#!/bin/bash
# L1 lane 8 — the ten certified edges again, after the width-inference fix
# (lane 7 refused six of them because it asked what width the literal 31 in
# `Extract(31, 0, v0)` has; a bit POSITION has no width), and then the three
# pairs t100 left UNDECIDED, whose terms are read from the_pool5.json because
# the pair record carries none.
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
