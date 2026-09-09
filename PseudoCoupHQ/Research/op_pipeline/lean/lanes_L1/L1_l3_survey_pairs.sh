#!/bin/bash
# L1 lane 3 — survey the ANSWERED PAIRS of pool100_edges.json, not only the 12
# applied edges. Lane 2 read `edges` (12 records) and found no UNDECIDED there;
# the file's `pairs` list carries all 21,502 answered pairs with their states,
# which is where the 226 PROVED and the 1,099 UNDECIDED live.
set -u

LEANDIR=PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L1home
mkdir -p "$HOME"

echo '[1/1] survey of pool100_edges.json over the union of its edges and pairs lists'
cd "$LEANDIR" || exit 1
python3 "$LEANDIR/edges_L1.py" survey
echo "--- survey exit $?"
