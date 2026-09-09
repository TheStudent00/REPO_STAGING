#!/usr/bin/env bash
# h1b_l7_verify2.sh -- task h1b: the verifier again, after the two
# elided transcripts in section 5 (the tally, and the LANDED-runs
# check) were replaced with the exact untruncated command and output
# lane h1b_l3 actually produced, so those two claims stop scoring
# NOT_RERUNNABLE for carrying "...".
set -euo pipefail
echo "[1/1] the verifier over log_239, corrected"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_239_task_h1b_composition_column.md
