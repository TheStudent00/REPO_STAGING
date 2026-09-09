#!/bin/bash
# task o11, lane 20: the verifier over log 226 WITH its own tally
# section appended, so the pasted tally is not the only pass on record.
set -u
echo "[1/1] the verifier over log 226"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    /projects/PseudoCoupHQ/DevComms/log_226_task_o11_rust_renderer.md
echo "lane o11_l20 done"
