#!/usr/bin/env bash
# t104 lane 15 -- the conventions-log verifier, over this closer's own
# DevComms log, from the t104 instance, per LAW's final-lane
# requirement: zero DIFFERS before this task is called closed.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
python3 check_conventions_log_claims.py --verify --timeout 20 /projects/PseudoCoupHQ/DevComms/log_233_task_t104_normalize_commutative_order_close.md
echo "verifier exit $?"
