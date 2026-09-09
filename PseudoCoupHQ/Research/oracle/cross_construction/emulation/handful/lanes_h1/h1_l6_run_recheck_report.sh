#!/usr/bin/env bash
# h1_l6_run_recheck_report.sh -- task h1: the twenty runs, the re-pose
# of every gate call the 3,000 ms ceiling left UNDECIDED, and the
# report, in ONE lane so handful.json is written end to end by one
# version of the program.
#
# WHY THIS LANE EXISTS AT ALL: lanes h1_l3 and h1_l5 already ran the
# same two commands and their logs stand. `handful.landing_of` then
# gained two fields -- the arch opcodes that remain after the chaff
# strip, and whether the cell's own opcode is among them -- so that
# section 3.2 of the report can key its causes on a fact rather than on
# a reading. Nothing about what is measured changed: the same ten
# cells, the same two renderers, the same ship flags, the same gate.
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_H1, checked
# after every run and every re-pose. h1_l3 peaked at 445,684 kB and
# h1_l5 at 437,560 kB.
set -euo pipefail
echo "[1/4] task h1: handful.py run"
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
python3 handful.py run
echo "[2/4] task h1: handful.py recheck 300000"
python3 handful.py recheck 300000
echo "[3/4] task h1: handful.py report, and the unmodified spelling guard"
python3 handful.py report
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful_cells.json \
    PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.json
echo "[4/4] done"
