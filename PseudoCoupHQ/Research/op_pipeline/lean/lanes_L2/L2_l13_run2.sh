#!/bin/bash
# L2 lane 13 -- the fixed re-run of lane 11's `run` command, over the fresh
# check_L2.json lane 12 wrote.  Every theorem file now carries `import
# Std.Tactic.BVDecide` (see lane 12's header).  Same protocol as lane 11:
# `rfl` first, `bv_decide` on what does not close definitionally, wall clock
# and peak RSS from `os.wait4` per theorem, DISCREPANCY on a bv_decide
# counterexample, LEAN_REFUSED by cause on any other failure.
set -u

TOTAL=1
LEANDIR=PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L2home
mkdir -p "$HOME"
cd "$LEANDIR" || exit 1

echo "[pre] lake build Archproof.Model (should be a cache hit; Model.lean is"
echo "      unchanged by the check re-run, which is deterministic)"
cd archproof || exit 1
time lake build Archproof.Model
echo "--- lake build exit $?"
cd "$LEANDIR" || exit 1

echo "[pre] model_translate.py run"
python3 model_translate.py run
echo "--- exit $?"
