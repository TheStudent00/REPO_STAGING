#!/bin/bash
# L2 lane 3 — the translator's two rule tables, and the five opcodes the
# brief names carried end to end: the reference's builder, run, translated,
# and written as a Lean definition.
set -u

TOTAL=2
LEANDIR=PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L2home
mkdir -p "$HOME"
cd "$LEANDIR" || exit 1

echo "[1/$TOTAL] the rule tables"
python3 model_translate.py table
echo "--- exit $?"

echo "[2/$TOTAL] the five opcodes, end to end"
python3 model_translate.py five
echo "--- exit $?"
