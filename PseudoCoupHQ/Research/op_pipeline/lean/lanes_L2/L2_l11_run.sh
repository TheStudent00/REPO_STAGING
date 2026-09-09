#!/bin/bash
# L2 lane 11 -- the brief's deliverable 2, step 2: build each STATED theorem
# through `lake env lean`, one process per theorem (model_translate.py's own
# `run` command).  `rfl` is tried first (definitional agreement); a goal it
# does not close is rewritten with the model definitions unfolded and
# `bv_decide` is tried; a `bv_decide` counterexample is classified as a
# DISCREPANCY (the two readings of the hardware disagree), any other failure
# as LEAN_REFUSED by cause.  Wall clock and peak RSS are `os.wait4`'s own
# reading of that one child process (per theorem, not a running maximum), and
# every proved theorem's file already carries `#print axioms` so lane 12 can
# check none is sorryAx.  This mutates check_L2.json (lane 10's output) in
# place, adding the outcome fields.
set -u

TOTAL=1
LEANDIR=PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L2home
mkdir -p "$HOME"
cd "$LEANDIR" || exit 1

echo "[pre] lake build Archproof.Model, so each theorem's own \`lake env"
echo "      lean\` finds an up-to-date olean rather than elaborating the"
echo "      15809-line model 172 times over"
cd archproof || exit 1
time lake build Archproof.Model
echo "--- lake build exit $?"
cd "$LEANDIR" || exit 1

echo "[pre] model_translate.py run"
python3 model_translate.py run
echo "--- exit $?"
