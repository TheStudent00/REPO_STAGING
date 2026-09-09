#!/bin/bash
# L2 lane 18 -- refresh `axioms` on ALL 153 proved rows with the
# lane-17-fixed `axiom_line` (joins a wrapped multi-line axiom list up to
# the closing `]` instead of returning only its opening line). Lane 17's
# probe of ModelCheck_c_9.lean showed the old single-line version silently
# dropped `Lean.ofReduceBool` and `Lean.trustCompiler` from every
# `bv_decide`-closed row whose axiom list wrapped -- those rows already
# held a (truncated, but non-empty) axioms string, so lane 16's gap-only
# pass never touched them. No theorem file changes; only the checker's
# own axiom-line parser changed, and this is a read of already-written
# files.
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

echo "[1/1] model_translate.py axioms_refresh"
python3 model_translate.py axioms_refresh
echo "--- exit $?"
