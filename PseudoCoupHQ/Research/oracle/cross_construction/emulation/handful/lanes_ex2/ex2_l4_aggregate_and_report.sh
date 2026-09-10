#!/usr/bin/env bash
# ex2_l4_aggregate_and_report.sh -- task ex2, step 4 (brief §3): the
# store (`expand2_runs.jsonl` + `expand2_runs_retry600.jsonl`) folded
# into `expand2.json`, then `expand2.md`, then each of the six
# deliverable commands printed on their own so the report's own
# figures are read off the aggregate, never re-counted (task ex1's
# sixth defect, §7 of log_248, is the one this order avoids).
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_EX2.
set -euo pipefail
A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
cd "$A"

echo "[1/7] the aggregate: expand2_runs.jsonl + retry600 -> expand2.json"
python3 expand2.py aggregate

echo ""
echo "[2/7] the report: expand2.md"
python3 expand2.py report

echo ""
echo "[3/7] deliverable 1 -- the per-target table"
python3 expand2.py tables

echo ""
echo "[4/7] deliverable 2 -- all seven, all twelve"
python3 expand2.py all_seven

echo ""
echo "[5/7] deliverable 3 -- every disagreement"
python3 expand2.py disagreements

echo ""
echo "[6/7] deliverable 4 -- declines by target and word"
python3 expand2.py declines

echo ""
echo "[7/7] deliverable 5 -- refusals by cause, and deliverable 6 -- the handful's seventy"
python3 expand2.py refusals
python3 expand2.py handful_check
echo "done"
