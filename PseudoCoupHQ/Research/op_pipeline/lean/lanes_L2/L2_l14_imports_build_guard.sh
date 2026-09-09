#!/bin/bash
# L2 lane 14 -- the brief's deliverable 3 and the LAW's mechanical guard, in
# one lane: (a) model_translate.py's `imports` command rewrites
# Archproof.lean to import every CLOSED check module (rfl or bv_decide),
# so the project build is a build of the proofs rather than of every
# attempt; (b) `lake build` over the whole project, exit code stated;
# (c) confirm no proof anywhere in the project can depend on `sorryAx` --
# grep for the `sorry` keyword itself, since `sorryAx` can only appear in
# `#print axioms` output if a `sorry` term or tactic exists somewhere in the
# proof or a dependency; (d) THE SPELLING BAN's mechanical guard
# (check_no_spelling_keys.py, never modified) over every json this task
# wrote.
set -u

TOTAL=4
LEANDIR=PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L2home
mkdir -p "$HOME"
cd "$LEANDIR" || exit 1

echo "[1/$TOTAL] model_translate.py imports"
python3 model_translate.py imports
echo "--- exit $?"

echo "[2/$TOTAL] lake build (whole project)"
cd archproof || exit 1
time lake build
echo "--- lake build exit $?"
cd "$LEANDIR" || exit 1

echo "[3/$TOTAL] sorry keyword, whole project (sorryAx can only exist if this"
echo "      matches)"
grep -rn "\bsorry\b" archproof/Archproof/*.lean archproof/Edges/*.lean \
    archproof/Main.lean archproof/Archproof.lean
echo "--- grep exit $? (1 = no match = no sorry anywhere = no sorryAx possible)"

echo "[4/$TOTAL] the spelling-ban guard over every json this task wrote"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    model_L2.json check_L2.json
echo "--- guard exit $?"
