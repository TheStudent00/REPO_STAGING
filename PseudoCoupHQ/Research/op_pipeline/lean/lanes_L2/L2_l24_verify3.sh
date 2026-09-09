#!/bin/bash
# L2 lane 24 -- third and final verifier pass, after removing the
# self-referential `$ ` line from section 11 (pass 2's own summary, pasted
# as output, would otherwise be re-run and compared against itself with a
# truncated paste -- see section 11's note).
set -u
TOTAL=1
echo "[1/$TOTAL] check_conventions_log_claims.py --verify over log_232, pass 3 (final)"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
    --verify --timeout 20 \
    PseudoCoupHQ/DevComms/log_232_task_L2_model_translator.md
echo "--- exit $?"
