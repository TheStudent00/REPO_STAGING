#!/bin/bash
set -u
LEANDIR=PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L2home
mkdir -p "$HOME"
cd "$LEANDIR/archproof" || exit 1
echo "[1/1] raw lake env lean output for ModelCheck_c_21.lean"
lake env lean Archproof/ModelCheck_c_21.lean
echo "--- exit $?"
echo "=== file contents ==="
cat -A Archproof/ModelCheck_c_21.lean | tail -10
