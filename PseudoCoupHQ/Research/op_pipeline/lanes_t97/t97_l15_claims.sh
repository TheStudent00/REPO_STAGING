#!/usr/bin/env bash
# t97 lane 12 -- this task's own report held to the rule it is written
# under: `check_conventions_log_claims.py --verify` re-runs every
# command log_202 pasted and sorts each claim into matches / differs /
# unverifiable.  Task 94 scored 19 matched of 32, with 28%
# unverifiable; the gate for this round is to beat that.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
python3 check_conventions_log_claims.py --verify \
  --json /projects/PseudoCoupHQ/Research/op_pipeline/claims97c.json \
  /projects/PseudoCoupHQ/DevComms/log_202_task97_term_pool_canon40.md
echo "exit $?"
