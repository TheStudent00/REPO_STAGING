#!/usr/bin/env bash
# h2_l4_o8_regression.sh -- task h2: task o8's per-opcode check re-run
# UNCHANGED over its own 243 rows, into a scratch copy.
#
# WHY: task h2 changed the driver and one width rule; it changed neither
# renderer.  Task o8's four totals -- rows, LANDED, byte-identical to
# the row's own body, proved -- are 243 / 197 / 155 / 216 (log 220 and
# `per_opcode_report.md` section 2, row `all`).  The same four totals
# coming back is the proof that the renderers write the same c for the
# same 243 terms.
#
# HOW TASK o8's OWN ARTIFACT STAYS UNTOUCHED: `o8_regression.py` imports
# `per_opcode.py` from its own folder, unmodified and unforked, and
# points the five paths it WRITES at `o8_regression/` under this task's
# artifact folder before calling its `main`.
#
# MEMORY BOUND: task o8's own, unchanged -- ABORT_MEMORY_O8, 2 GB
# resident, checked by its own collector after every row; it measured
# 83,096 kB when task o8 ran it.
set -euo pipefail
echo "[1/5] task h2: task o8's population, into the scratch copy"
python3 /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/o8_regression.py population
echo "[2/5] task h2: task o8's 243 rows, into the scratch copy"
python3 /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/o8_regression.py run
echo "[3/5] task h2: task o8's report, into the scratch copy"
python3 /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/o8_regression.py report
echo "[4/5] task h2: the four totals, counted off the scratch results"
python3 /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/o8_regression.py totals
echo "[5/5] done"
