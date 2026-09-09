#!/bin/bash
# L1 lane 4 — what an UNDECIDED pair record carries. Lane 3 found that none of
# t100's 1,099 UNDECIDED pairs carries a printed layer-5 text on both sides, so
# the three wide-division shapes the brief asks for cannot be read off the pair
# record alone; this lane says what IS on the record, so the next lane knows
# where to go for the terms.
set -u
LEANDIR=PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L1home
mkdir -p "$HOME"
echo '[1/1] the shape of an UNDECIDED pair record'
python3 "$LEANDIR/edges_L1.py" undecided
echo "--- exit $?"
