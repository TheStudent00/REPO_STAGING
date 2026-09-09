#!/usr/bin/env bash
# o2 lane 3 -- THE SPELLING BAN mechanical guard, run over both json
# files this task wrote (single_opcode_units.json, unique_opcodes.json).
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
total=2
i=0
rc_total=0
for f in /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/single_opcode_units.json \
         /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/unique_opcodes.json; do
  i=$((i+1))
  echo "======== [$i/$total] check_no_spelling_keys.py $f ========"
  python3 check_no_spelling_keys.py "$f"
  rc=$?
  echo "exit ${rc} for $f"
  if [ "$rc" -ne 0 ]; then rc_total=1; fi
done
exit ${rc_total}
