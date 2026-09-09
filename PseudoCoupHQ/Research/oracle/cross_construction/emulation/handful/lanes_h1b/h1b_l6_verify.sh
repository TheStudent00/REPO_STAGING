#!/usr/bin/env bash
# h1b_l6_verify.sh -- task h1b: the conventions-log-claims verifier
# over this task's own DevComms log, from the instance, as the law
# requires.
set -euo pipefail
echo "[1/1] the verifier over log_239"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    /projects/PseudoCoupHQ/DevComms/log_239_task_h1b_composition_column.md
