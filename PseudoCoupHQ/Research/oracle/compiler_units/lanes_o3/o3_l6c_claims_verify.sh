#!/usr/bin/env bash
# lane 6c -- task o3b: claims-verify, re-run after fixing the one
# DIFFER o3_l6b found (the grep -c exempt paste used cd-relative
# filenames instead of the WORKDIR-relative paths a re-run produces).
set -uo pipefail
echo "[1/1] check_conventions_log_claims.py --verify over log_209 (with §8, after the grep-exempt fix)"
python3 PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py \
  --verify --timeout 20 \
  --json PseudoCoupHQ/Research/oracle/compiler_units/log_209_claims_o3b.json \
  PseudoCoupHQ/DevComms/log_209_task_o3_compiler_operators_used.md
echo "verifier exit: $?"
