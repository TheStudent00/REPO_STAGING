#!/usr/bin/env bash
# ex2_l7_verify_250.sh -- task ex2: the conventions verifier over this
# task's log, from this task's own instance, as the law requires. Zero
# DIFFERS is the obligation; a DIFFERS is fixed in the CLAIM or in the
# object, never in the verifier.
set -euo pipefail
cd PseudoCoupHQ
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_250_task_ex2_the_interpreted_loop.md
echo "done"
