#!/usr/bin/env bash
# ap3_l18_verify_245b.sh -- task ap3 (a lane name is used ONCE; nothing was removed): the second pass, after the ONE REFUSED of ap3_l17 was fixed in the CLAIM and never in the verifier -- a pasted command carried `sed -n ...,$p` and the verifier read the `$p` as a file path, so the same eleven lines are now cut with `grep -A 10`; and the two bare pastes were given the lane log they came from. the conventions verifier over this
# task's log, run from this task's own instance as the law requires.
# Zero DIFFERS is the obligation; a DIFFERS is fixed in the LOG or in
# the CLAIM and never in the verifier.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_245_task_ap3_autopoly_third_pass.md
echo "done"
