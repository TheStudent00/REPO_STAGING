#!/bin/bash
set -x
echo "[1/2] read the handler function bounds from symbol table + DWARF"
cd /projects/PseudoCoupHQ/Research/op_pipeline
python3 t94_read_bounds.py 2>&1 | tail -80
echo "[2/2] done"
