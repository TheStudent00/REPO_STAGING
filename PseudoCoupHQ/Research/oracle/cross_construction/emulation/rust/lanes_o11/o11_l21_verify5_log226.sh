#!/bin/bash
# task o11, lane 21: the verifier over log 226, final pass, after one
# prose correction in section 12 (an earlier draft said log 220 records
# a PASS for the guard; log 220 in fact records the FAIL and flags it,
# and section 12 now quotes log 220's own words).
set -u
echo "[1/1] the verifier over log 226"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    /projects/PseudoCoupHQ/DevComms/log_226_task_o11_rust_renderer.md
echo "lane o11_l21 done"
