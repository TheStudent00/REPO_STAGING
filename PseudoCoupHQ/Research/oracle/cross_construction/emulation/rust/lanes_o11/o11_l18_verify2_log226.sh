#!/bin/bash
# task o11, lane 18: the verifier over log 226 again, after its
# transcripts were regenerated from lane o11_l17 in a form the verifier
# can re-run.
set -u
echo "[1/1] the verifier over log 226"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_226_task_o11_rust_renderer.md
echo "lane o11_l18 done"
