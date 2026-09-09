#!/bin/bash
# task o11, lane 19: the verifier over log 226, third pass.
# Lane 18 reported one DIFFERS: the three example blocks were pasted as
# shell transcripts, and each carries a fenced rust source inside it, so
# the verifier's fence reader cut the paste at the inner fence and
# compared three lines against forty-two. Those three sections are now
# inlined as attributions with the reproducing command named in prose.
set -u
echo "[1/1] the verifier over log 226"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    /projects/PseudoCoupHQ/DevComms/log_226_task_o11_rust_renderer.md
echo "lane o11_l19 done"
