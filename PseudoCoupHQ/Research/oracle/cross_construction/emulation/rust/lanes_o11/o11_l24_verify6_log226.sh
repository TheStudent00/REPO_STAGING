#!/bin/bash
# task o11, lane 24: the verifier over log 226, after section 11 gained
# the `grep -c exempt` transcript.
set -u
echo "[1/1] the verifier over log 226"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_226_task_o11_rust_renderer.md
echo "lane o11_l24 done"
