#!/bin/bash
# L2 lane 4 — the five opcodes end to end, after the signature fix of lane 3.
set -u

TOTAL=1
LEANDIR=PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L2home
mkdir -p "$HOME"
cd "$LEANDIR" || exit 1

echo "[1/$TOTAL] the five opcodes, end to end"
python3 model_translate.py five
echo "--- exit $?"
