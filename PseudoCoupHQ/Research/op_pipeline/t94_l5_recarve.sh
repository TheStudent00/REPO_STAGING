#!/bin/bash
set -x
echo "[1/2] re-carve the eleven interpreter units to their handler function bodies, render, gate"
cd /projects/PseudoCoupHQ/Research/op_pipeline
python3 t94_recarve.py 2>&1 | tail -120
echo "[2/2] done"
