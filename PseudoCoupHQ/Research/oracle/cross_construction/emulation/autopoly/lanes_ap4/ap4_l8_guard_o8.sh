#!/usr/bin/env bash
# ap4_l8_guard_o8.sh -- task ap4: the third guard the brief names.
#
# Task o8's own program re-run over its own 243 rows through
# `o8_regression.py`, whose whole purpose is that: task o8's four
# totals -- rows, LANDED, byte-identical to the row's own body, proved
# -- are 243 / 197 / 155 / 216 (log 220).  If they come back the same,
# nothing this task changed in the ledger or the driver moved what the
# renderers write for the same 243 terms.
#
# Every product goes into `handful/o8_regression/`, which is that
# program's own scratch; nothing under `per_opcode/` is written.
#
# MEMORY BOUND: task o8's own, ABORT_MEMORY_O8, 2 GB resident, checked
# by its own collector after every row.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
echo "[1/3] the population"
python3 o8_regression.py population 2>&1 | tail -6
echo ""
echo "[2/3] the 243 rows"
python3 o8_regression.py run 2>&1 | tail -8
echo ""
echo "[3/3] the four totals"
python3 o8_regression.py totals 2>&1 | tail -20
echo "done"
