#!/usr/bin/env bash
set -uo pipefail
echo "[1/1] check_conventions_log_claims.py --verify over log_209 (final, after relocating lane logs / paths)"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
  --verify --timeout 120 \
  --json PseudoCoupHQ/Research/oracle/compiler_units/log_209_claims_final.json \
  PseudoCoupHQ/DevComms/log_209_task_o3_compiler_operators_used.md
echo "verifier exit: $?"
