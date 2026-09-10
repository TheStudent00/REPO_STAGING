#!/usr/bin/env bash
# ex2_l6_aggregate_and_report_b.sh -- task ex2: THE SECOND PASS of the
# aggregate and report, over the run of record AFTER the label-dot
# sanitization fix (`interp_check.one_run`, found by this task's own
# loop over the full outer set -- the handful's ten cells never hit a
# place name carrying a dot) and its verifying re-run
# (`ex2_l4_the_loop_after_the_label_fix.sh`, 196 of the 1,771 pairs
# re-rendered and re-run). `ex2_l4_aggregate_and_report.sh`'s own
# output stays on the record as the FIRST pass (11 disagreements, all
# on csharp); this lane's own output, with zero disagreements, is the
# one the report of record reads from -- a lane name is used once, so
# this is a new name and the first pass's log is not overwritten.
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
