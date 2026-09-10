#!/usr/bin/env bash
# ex2_l6_reaggregate_after_label_fix.sh -- task ex2, step 6 (brief §3),
# RE-RUN. `ex2_l4_aggregate_and_report.sh` folded the store while it
# still carried the 196 (cell, target) pairs whose destination place
# name held a dot (`flags.low`, `reg_xmm0.low`); those records were
# wrong (a compile error on six targets, and on csharp a STALE dll from
# an earlier build silently executed in its place -- see
# `ex2_l3_csharp_disagreement_diagnosis.sh`'s log). The dot-sanitisation
# fix in `interp_check.one_run` (git a24c3042) and the resume lane
# `ex2_l4_the_loop_after_the_label_fix.sh` purged and re-ran exactly
# those 196; this lane repeats l4's aggregate + report + six deliverable
# commands over the now-corrected `expand2_runs.jsonl`, under a new name
# because `ex2_l4_aggregate_and_report.sh` already ran once (LAW: a
# collided name gets a new name, nothing removed to make room). Same
# content as l4, unchanged, only the name and this note are new.
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
