#!/usr/bin/env bash
# g1_l8_compose_report.sh -- task g1: the composition column over the
# forty runs' own carved bodies, the report, and the tally.
#
# WHY BEFORE THE RE-POSE: the re-pose of every UNDECIDED gate call at
# 300,000 ms is the one slow step of this task (task h2's four took
# 1,218 s), and reading the forty runs first is what says how many
# obligations there are to re-pose and whether anything else needs
# fixing before that time is spent.  The report is written again after
# the re-pose, so nothing here is the report of record.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_G1.  The
# composition step reads `model_table_rows.json` (50 MB), measured at
# 253,716 kB by task h1b.
set -euo pipefail
H=PseudoCoupHQ/Research/oracle/cross_construction/emulation
echo "[1/4] task g1: handful.py compose3"
python3 $H/handful/handful.py compose3
echo "[2/4] task g1: handful.py report3"
python3 $H/handful/handful.py report3
echo "[3/4] task g1: handful.py tally3"
python3 $H/handful/handful.py tally3
echo "[4/4] task g1: the forty-row table as the report wrote it"
sed -n '\%^| cell . lang . route%,\%^$%p' $H/handful/handful3.md
