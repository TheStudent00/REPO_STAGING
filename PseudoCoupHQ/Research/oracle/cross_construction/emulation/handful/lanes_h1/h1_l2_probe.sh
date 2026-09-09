#!/usr/bin/env bash
# h1_l2_probe.sh -- task h1, step 1 for all ten cells and nothing else:
# the row chosen, the z3 term of every place the cell's opcode writes,
# that term's width, and the arrival families it reads. Nothing is
# rendered, compiled or proved here; this lane exists so the input
# object of every run is on the record before any of it is acted on.
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_H1, checked at
# the end; this lane reads only the ten-row handful_cells.json.
set -euo pipefail
echo "[1/2] task h1: handful.py probe"
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
python3 handful.py probe
echo "[2/2] done"
