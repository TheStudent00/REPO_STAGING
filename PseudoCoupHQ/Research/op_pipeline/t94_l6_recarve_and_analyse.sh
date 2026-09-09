#!/bin/bash
set -x
echo "[1/4] re-read the handler bounds (label field renamed to the spelling-guard's own name)"
cd /projects/PseudoCoupHQ/Research/op_pipeline
python3 t94_read_bounds.py 2>&1 | tail -20
echo "[2/4] re-carve, render through the universal form, gate against own ship code"
python3 t94_recarve.py 2>&1 | tail -60
echo "[3/4] causes, recurring paths, super-op route"
python3 t94_analysis.py 2>&1 | tail -40
echo "[4/4] done"
