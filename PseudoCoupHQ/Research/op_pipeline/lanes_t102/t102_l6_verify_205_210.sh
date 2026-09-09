#!/usr/bin/env bash
set -u
cd /projects/PseudoCoupHQ
total=6
i=0
for log in DevComms/log_205_task_99_recording_gaps.md \
           DevComms/log_206_arch_unit_oracle_founding.md \
           DevComms/log_207_task_o1_cross_construction_map.md \
           DevComms/log_208_task_o2_single_opcode_units.md \
           DevComms/log_209_task_o3_compiler_operators_used.md \
           DevComms/log_210_task_o4_operator_variants_by_search.md; do
  i=$((i+1))
  echo "======== [$i/$total] $log ========"
  python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_conventions_log_claims.py --verify --timeout 20 "$log"
  echo "---- exit $? ----"
done
