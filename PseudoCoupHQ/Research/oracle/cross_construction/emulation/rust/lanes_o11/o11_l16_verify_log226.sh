#!/bin/bash
# task o11, lane 16: re-run every command log 226 pasted, and sort each
# claim into matches / differs / unverifiable.
set -u
echo "[1/1] the verifier over log 226"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    /projects/PseudoCoupHQ/DevComms/log_226_task_o11_rust_renderer.md
echo "lane o11_l16 done"
