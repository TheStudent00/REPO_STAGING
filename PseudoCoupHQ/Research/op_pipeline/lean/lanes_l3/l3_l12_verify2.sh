#!/bin/bash
# l3 lane 12 -- the conventions checker again, after the two bare pastes of
# section 6 were given their attribution lead-ins.
set -u
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_250_task_l3_the_one_naming_and_the_trust_classes.md
echo "--- check_conventions_log_claims.py exit $?"
