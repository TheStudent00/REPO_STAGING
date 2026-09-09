#!/bin/bash
# L1 lane 7 — the ten certified edges.
#   [1/3] re-select, so L1_edges_selected.json also carries the three pairs
#         t100 left UNDECIDED (one per UNDECIDED machine type key)
#   [2/3] the operator table this task translates by, printed LITERAL
#   [3/3] one Lean theorem per pair, each in its own `lean` process, with that
#         process's wall clock and peak RSS
set -u
LEANDIR=/projects/PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L1home
mkdir -p "$HOME"
echo '[1/3] re-select'
python3 "$LEANDIR/edges_L1.py" select
echo '[2/3] the operator table, printed layer-5 form to Lean 4.24'
python3 "$LEANDIR/term_to_lean.py" table
echo '[3/3] the ten theorems'
python3 "$LEANDIR/run_edges_L1.py" ten
echo "--- ten exit $?"
