#!/usr/bin/env bash
# h1_l3_run.sh -- task h1: the twenty runs. Ten cells of the arch-opcode
# model table, two targets; per written place of each cell, one render
# by the existing renderer, one compile at that corpus's own ship flags,
# one carve, and one gate call at the 3,000 ms ceiling.
# MEMORY BOUND: 4 GB resident on the one collecting process, named abort
# ABORT_MEMORY_H1, checked after every run; there are no forked workers.
# The probe lane (h1_l2) measured the same program's step 1 at 69,544 kB.
set -euo pipefail
echo "[1/2] task h1: handful.py run"
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
python3 handful.py run
echo "[2/2] done"
