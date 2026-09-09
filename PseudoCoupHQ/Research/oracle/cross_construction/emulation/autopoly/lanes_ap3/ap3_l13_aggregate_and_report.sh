#!/usr/bin/env bash
# ap3_l13_aggregate_and_report.sh -- task ap3: the 1,012-run store read
# once, every table computed off it, the report written, and the
# spelling guard over every json this task wrote.
#
# THE GUARD IS `Research/op_pipeline/check_no_spelling_keys.py`, the
# standing one, run over this task's own output and never modified.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP3.  Task
# ap2's aggregate lane peaked at 86,520 kB over the same-sized store.
set -euo pipefail
A=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
cd "$A"

echo "[1/6] the aggregate"
python3 autopoly3.py aggregate

echo "[2/6] the report"
python3 autopoly3.py report

echo "[3/6] the store and the aggregate compared run for run"
python3 autopoly3.py store

echo "[4/6] the spelling guard, over every json this task wrote"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    "$A/autopoly3_cells.json" "$A/autopoly3.json" \
    "$A/autopoly3_check_L2_rerun.json"

echo "[5/6] no exemption anywhere in what this task wrote"
grep -c exempt "$A/autopoly3.py" "$A/lanes_ap3/"*.sh || true

echo "[6/6] the tally"
python3 autopoly3.py tally
echo "done"
