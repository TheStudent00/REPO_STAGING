#!/usr/bin/env bash
# ex2_l6_report_and_guard.sh -- task ex2, step 6: aggregate, the report
# (the six deliverables), the spelling guard over every json this task
# wrote, and the tally.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

echo "[1/6] aggregate"
python3 expand2.py aggregate

echo ""
echo "[2/6] deliverable 1: the per-target table"
python3 expand2.py tables

echo ""
echo "[3/6] deliverable 2: all seven, all twelve"
python3 expand2.py all_seven

echo ""
echo "[4/6] deliverable 3: every disagreement"
python3 expand2.py disagreements

echo ""
echo "[5/6] deliverable 6: the handful's seventy, reproduced"
python3 expand2.py handful_check

echo ""
echo "[6/6] the report"
python3 expand2.py report

echo ""
echo "the spelling guard, over every json this task wrote"
for f in expand2_cells.json expand2.json; do
    python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py "$f"
done

echo ""
echo "grep -c exempt over the files this task added:"
echo -n "   interp/interp_check.py (modified): "
grep -c exempt PseudoCoupHQ/Research/oracle/cross_construction/emulation/interp/interp_check.py || true
echo -n "   autopoly/expand2.py: "
grep -c exempt expand2.py || true

echo ""
echo "the tally"
wc -l expand2_runs.jsonl
echo "done"
