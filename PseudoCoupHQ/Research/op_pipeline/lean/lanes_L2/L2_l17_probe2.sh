#!/bin/bash
set -u
LEANDIR=/projects/PseudoCoupHQ/Research/op_pipeline/lean
export HOME=/work/L2home
mkdir -p "$HOME"
cd "$LEANDIR/archproof" || exit 1
echo "[1/1] raw lake env lean output for ModelCheck_c_9.lean (a truncated-axioms row)"
lake env lean Archproof/ModelCheck_c_9.lean
echo "--- exit $?"
