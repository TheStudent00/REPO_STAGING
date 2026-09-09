#!/usr/bin/env bash
# h1b_l9_verify3.sh -- task h1b: the verifier, final pass, after the
# REFUSED claim from `h1b_l7` was cleared by lane `h1b_l8`'s
# `->`-free re-run.
set -euo pipefail
echo "[1/1] the verifier over log_239, final"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    /projects/PseudoCoupHQ/DevComms/log_239_task_h1b_composition_column.md
