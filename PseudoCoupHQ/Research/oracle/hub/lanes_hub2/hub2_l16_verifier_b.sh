#!/usr/bin/env bash
# hub2_l16_verifier_b.sh -- task hub2, lane 16 (the second pass, after §4's pair paste had its command moved onto the fence's own first line and its output completed): the conventions verifier
# over this task's report, run FROM this task's own instance as the law
# requires.  The obligation is the DIFFERS column: zero.  A failure is
# fixed in the log or in the claim, never in the verifier.
set -uo pipefail
echo "[1/1] the verifier"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 PseudoCoupHQ/DevComms/log_254_task_hub2_the_dictionary_at_two_levels.md
