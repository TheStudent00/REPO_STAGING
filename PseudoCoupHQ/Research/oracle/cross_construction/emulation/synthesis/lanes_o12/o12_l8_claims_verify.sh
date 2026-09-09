#!/usr/bin/env bash
# o12 lane 8 -- closing pass: the conventions checker over log_230
# (the closing report for this task, written after the compute of
# lanes 1-7 was found complete and past the sort-filter correction).
# It re-runs every command the log pastes and says which claims
# reproduce.  The checker is never modified; the log is fixed if a
# claim differs.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "[1/1] claims verify"
python3 check_conventions_log_claims.py --verify --timeout 20 \
  /projects/PseudoCoupHQ/DevComms/log_230_task_o12_synthesis_route.md
echo "-- exit $?"
