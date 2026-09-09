#!/usr/bin/env bash
# lane 10 -- task o3b, correction: claims-verify over log_209 with
# §9 appended, --timeout 20 as §8's own l6b/l6c used.
set -uo pipefail
echo "[1/1] check_conventions_log_claims.py --verify over log_209 (with §9 appended)"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
  --verify --timeout 20 \
  --json PseudoCoupHQ/Research/oracle/compiler_units/log_209_claims_o3b_correction.json \
  PseudoCoupHQ/DevComms/log_209_task_o3_compiler_operators_used.md
echo "verifier exit: $?"
