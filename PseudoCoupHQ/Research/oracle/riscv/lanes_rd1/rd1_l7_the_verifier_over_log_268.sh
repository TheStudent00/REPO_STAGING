#!/bin/bash
# rd1 lane 7 -- the law's final lane: re-run this task's log's own claims from
# this task's instance, and print the tally.
set -u
P=PseudoCoupHQ
echo "[1/1] check_conventions_log_claims.py --verify over log 268"
timeout 3000 python3 "$P/Research/op_pipeline/check_conventions_log_claims.py" \
  --verify --timeout 20 \
  "$P/DevComms/log_268_rd1_the_guard_dominates_the_operation.md"
echo "  exit: $?"
