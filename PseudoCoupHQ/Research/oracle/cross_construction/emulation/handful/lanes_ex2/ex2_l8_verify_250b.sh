#!/usr/bin/env bash
# ex2_l8_verify_250b.sh -- task ex2: the conventions verifier, second
# pass, after log_250 gained proper `$ ` shell-transcript blocks for its
# six deliverable tables so they are re-run and matched rather than
# left UNVERIFIABLE. Zero DIFFERS is the obligation.
set -euo pipefail
cd PseudoCoupHQ
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_250_task_ex2_the_interpreted_loop.md
echo "done"
