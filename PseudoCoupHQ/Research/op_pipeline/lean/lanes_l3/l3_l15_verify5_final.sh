#!/bin/bash
# l3 lane 15 -- the conventions checker over the log as this task finally
# leaves it: renumbered to 251, every attribution carrying its host lane log
# path.  This is the pass whose numbers section 10's tally line states.
set -u
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_251_task_l3_the_one_naming_and_the_trust_classes.md
echo "--- check_conventions_log_claims.py exit $?"
