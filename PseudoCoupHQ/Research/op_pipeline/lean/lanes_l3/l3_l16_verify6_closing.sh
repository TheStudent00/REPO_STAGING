#!/bin/bash
# l3 lane 16 -- the closing pass: section 10 now names pass 5, so the checker
# runs once more to confirm the tally that section states is still what the
# file gives.
set -u
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_251_task_l3_the_one_naming_and_the_trust_classes.md
echo "--- check_conventions_log_claims.py exit $?"
