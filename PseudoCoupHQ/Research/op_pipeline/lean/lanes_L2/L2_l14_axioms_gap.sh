#!/bin/bash
# L2 lane 14 -- 20 of the 153 proved theorems (all closed by `rfl`) came out
# of lane 13's `run` with row["closed_by"] set but row["axioms"] None: the
# `#print axioms` info trace that a successful `lean_once` should carry
# was not found in the captured output by `axiom_line`. The brief's
# deliverable 3 is "`#print axioms` on every proved theorem (no sorryAx)",
# so this gap has to close before that claim can be made over all 153.
# `axioms_gap_command` (added to model_translate.py this lane) re-runs
# `lake env lean` on exactly those 20 already-written files -- nothing here
# writes a new theorem or edits an existing one's statement or tactic --
# and records what the trace actually says.
set -u

TOTAL=1
LEANDIR=/projects/PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L2home
mkdir -p "$HOME"
cd "$LEANDIR" || exit 1

echo "[pre] lake build Archproof.Model (cache hit expected)"
cd archproof || exit 1
time lake build Archproof.Model
echo "--- lake build exit $?"
cd "$LEANDIR" || exit 1

echo "[1/1] model_translate.py axioms_gap"
python3 model_translate.py axioms_gap
echo "--- exit $?"
