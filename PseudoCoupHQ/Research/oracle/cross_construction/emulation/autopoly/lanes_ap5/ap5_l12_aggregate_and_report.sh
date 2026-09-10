#!/usr/bin/env bash
# ap5_l12_aggregate_and_report.sh -- task ap5: the store -> the
# aggregate -> the report, then the store and the aggregate compared
# run for run, the spelling guard over every json this task wrote, and
# the tally.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP5.
set -euo pipefail
A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
cd "$A"
echo "[1/6] the aggregate"
python3 autopoly5.py aggregate
echo ""
echo "[2/6] the report"
python3 autopoly5.py report
echo ""
echo "[3/6] the store and the aggregate compared run for run"
python3 autopoly5.py store
echo ""
echo "[4/6] the spelling guard, over every json this task wrote"
cd PseudoCoupHQ/Research/op_pipeline
for F in autopoly5_cells.json autopoly5.json autopoly5_check_L2_rerun.json; do
  python3 check_no_spelling_keys.py "$A/$F"
done
echo ""
echo "[5/6] no exemption anywhere in what this task wrote"
grep -c exempt "$A/autopoly5.py" "$A/lanes_ap5/"*.sh || true
echo ""
echo "[6/6] the tally"
cd "$A"
python3 autopoly5.py tally
echo "done"
