#!/bin/bash
# l3 lane 14 -- the conventions checker over this task's log at its FINAL
# number.  Passes 1-3 ran while the log was numbered 250, which task ex2 had
# also taken; the file is now log_251 and this is the run of record.
set -u
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_251_task_l3_the_one_naming_and_the_trust_classes.md
echo "--- check_conventions_log_claims.py exit $?"
