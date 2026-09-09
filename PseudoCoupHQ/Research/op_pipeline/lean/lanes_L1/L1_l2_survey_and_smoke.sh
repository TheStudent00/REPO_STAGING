#!/bin/bash
# L1 lane 2 — two things this lane answers, so one queue slot covers both:
#   [1/2] the smoke theorem builds, once bv_decide's import is added
#   [2/2] what t100's answered pairs look like: states, the printed layer-5
#         token vocabulary (the operator table of the printed form, read off
#         the data), the shortest PROVED texts, and the UNDECIDED shapes
set -u

LEANDIR=/projects/PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L1home
mkdir -p "$HOME"

echo "[1/2] the smoke theorem, with import Std.Tactic.BVDecide"
cat > "$LEANDIR/archproof/Archproof/Smoke.lean" <<'LEAN'
-- The smallest possible check that this toolchain proves anything:
-- one arithmetic identity over 32-bit words, discharged by bv_decide,
-- which bit-blasts the goal to a SAT solver and checks the solver's
-- certificate inside Lean's kernel.
import Std.Tactic.BVDecide

theorem smoke_add_comm (v0 v1 : BitVec 32) : v0 + v1 = v1 + v0 := by
  bv_decide
LEAN
echo "--- Archproof/Smoke.lean, LITERAL"
cat "$LEANDIR/archproof/Archproof/Smoke.lean"
echo "--- lake build"
cd "$LEANDIR/archproof" || exit 1
time lake build
echo "--- lake build exit $?"

echo "[2/2] survey of pool100_edges.json"
cd "$LEANDIR" || exit 1
python3 "$LEANDIR/edges_L1.py" survey
echo "--- survey exit $?"
