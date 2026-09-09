#!/usr/bin/env bash
# o2 lane 10 (final, after fixing five pasted outputs that had drifted from real re-run output, caught by lane 9) --
# --verify over log_208 itself, per the standing report rule.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "======== [1/1] check_conventions_log_claims.py --verify log_208 ========"
python3 check_conventions_log_claims.py --verify \
  --timeout 120 \
  --json /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/log_208_claims_l10.json \
  /projects/PseudoCoupHQ/DevComms/log_208_task_o2_single_opcode_units.md
rc=$?
echo "verifier exit ${rc}"
exit ${rc}
