#!/usr/bin/env bash
# o2 lane 8 -- final verifier pass: check_conventions_log_claims.py
# --verify over log_208 itself, per the standing report rule.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "======== [1/1] check_conventions_log_claims.py --verify log_208 ========"
python3 check_conventions_log_claims.py --verify \
  --timeout 120 \
  --json /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/log_208_claims.json \
  /projects/PseudoCoupHQ/DevComms/log_208_task_o2_single_opcode_units.md
rc=$?
echo "verifier exit ${rc}"
exit ${rc}
