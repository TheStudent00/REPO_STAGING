#!/bin/bash
# L2 lane 16 -- re-run of lane 14's axioms_gap after fixing axiom_line()
# (model_translate.py) to also recognise Lean's zero-axiom phrasing,
# "'NAME' does not depend on any axioms" -- lane 15's probe of
# ModelCheck_c_21.lean showed that is exactly what all 20 gap rows print
# (their `rfl` proofs use no axiom at all), and the old regex only matched
# "depends on axioms:". No theorem file changes; only the checker's own
# axiom-line parser changed.
set -u

TOTAL=1
LEANDIR=PseudoCoupHQ/Research/op_pipeline/lean
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
