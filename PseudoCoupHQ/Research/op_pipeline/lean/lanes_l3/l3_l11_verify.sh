#!/bin/bash
# l3 lane 11 -- the conventions checker over this task's log, run FROM the l3
# instance, unmodified.
set -u
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_250_task_l3_the_one_naming_and_the_trust_classes.md
echo "--- check_conventions_log_claims.py exit $?"
