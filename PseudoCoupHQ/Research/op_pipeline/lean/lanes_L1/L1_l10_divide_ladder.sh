#!/bin/bash
# L1 lane 10 — two questions the brief's third item asks, answered separately
# because the corpus does not hold the shape the brief expected:
#   [1/2] the three pairs t100 left UNDECIDED, again, now saying for each
#         entry text that exists whether Lean can state it at all and by what
#         cause not
#   [2/2] the cost of bit-blasting a divider, measured directly at 8, 16, 32
#         and 64 bits on the division identity. NOT corpus pairs: none of
#         t100's 1,099 UNDECIDED pairs carries a division node.
set -u
LEANDIR=PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L1home
mkdir -p "$HOME"
echo '[1/2] the three UNDECIDED pairs, with a translation probe per text'
python3 "$LEANDIR/run_edges_L1.py" undecided
echo "--- undecided exit $?"
echo '[2/2] the division cost ladder'
python3 "$LEANDIR/run_edges_L1.py" divide
echo "--- divide exit $?"
