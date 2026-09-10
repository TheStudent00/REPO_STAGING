#!/usr/bin/env bash
# ex1_l17_verify_248.sh -- task ex1: the conventions verifier over this
# task's log, from this task's own instance, as the law requires.  Zero
# DIFFERS is the obligation; a DIFFERS is fixed in the CLAIM or in the
# object, never in the verifier.
set -euo pipefail
cd PseudoCoupHQ
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_248_task_ex1_cpp_and_the_interpreted_check.md
echo "done"
