#!/bin/bash
# L1 lane 6 — fix the ten, and show what a printed division node actually
# looks like in this corpus.
#   [1/2] select: write L1_edges_selected.json (the ten, and any UNDECIDED
#         pair carrying a wide division node -- lane 4 says there are none,
#         so this also records that count as zero from the program itself)
#   [2/2] divsamples: the shortest printed texts that DO carry a division
#         node, with their t100 states, so the translator is written against
#         the shape on disk rather than a remembered one
set -u
LEANDIR=/projects/PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L1home
mkdir -p "$HOME"
echo '[1/2] select the ten'
python3 "$LEANDIR/edges_L1.py" select
echo "--- select exit $?"
echo '[2/2] printed division nodes in the corpus'
python3 "$LEANDIR/edges_L1.py" divsamples
echo "--- divsamples exit $?"
