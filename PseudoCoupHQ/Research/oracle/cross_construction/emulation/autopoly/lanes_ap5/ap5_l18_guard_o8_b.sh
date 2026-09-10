#!/usr/bin/env bash
# ap5_l18_guard_o8_b.sh -- task ap5: the third of the four guards the
# brief names.
#
# Task o8's own program re-run over its own 243 rows through
# `o8_regression.py`, whose whole purpose is that: task o8's four
# totals -- rows, LANDED, byte-identical to the row's own body, proved
# -- are 243 / 197 / 155 / 216 (log 220).  If they come back the same,
# nothing this task changed in `reference.answer_of`, in
# `pool100_entry_equivalence.align_by_row`, in
# `model_translate.shapes_for` or in the driver moved what the
# renderers write for the same 243 terms.
#
# Every product goes into `handful/o8_regression/`, which is that
# program's own scratch; nothing under `per_opcode/` is written.
#
# MEMORY BOUND: task o8's own, ABORT_MEMORY_O8, 2 GB resident, checked
# by its own collector after every row.
# THE SECOND PASS.  The guards are re-run over the code as this task
# FINALLY leaves it -- lane ap5_l15's fix to `align_by_row`'s new
# branch landed after the first pass of them -- so the tally of
# record is this one.  A lane name is used ONCE, so this is a new
# name and the first pass stays on the record.
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
