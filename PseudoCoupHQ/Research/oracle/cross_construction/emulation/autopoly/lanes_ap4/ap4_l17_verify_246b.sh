#!/usr/bin/env bash
# ap4_l17_verify_246b.sh -- task ap4: the conventions verifier over this
# task's log, run FROM THIS INSTANCE as the law requires.  The obligation
# is the DIFFERS column: zero, and a difference is fixed in the log or in
# the claim, never in the verifier.
set -euo pipefail
cd PseudoCoupHQ/Research/op_pipeline
python3 check_conventions_log_claims.py --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_246_task_ap4_autopoly_fourth_pass.md
echo "done"
