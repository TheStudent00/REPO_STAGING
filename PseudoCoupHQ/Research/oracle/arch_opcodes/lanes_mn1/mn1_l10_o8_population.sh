#!/usr/bin/env bash
set -euo pipefail
echo "[1/1] task mn1: per_opcode.py population (reads single_opcode_units.json's mnem field)"
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/per_opcode
python3 per_opcode.py population
echo "[1/1] done"
