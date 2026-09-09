#!/usr/bin/env bash
# m1b_l19_guard.sh -- task m1b: the spelling guard, unmodified, over
# every json this task wrote, and the companion count over every file
# it added.
set -euo pipefail
echo "[1/2] task m1b: check_no_spelling_keys.py over the four json"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json \
  PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table_rows.json \
  PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table_attest.json \
  PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table_edges.json
echo "[2/2] task m1b: grep -c exempt over the files this task added"
for f in PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.py \
         PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.md \
         PseudoCoupHQ/Research/oracle/arch_opcodes/model/lanes_m1b/*.sh; do
  echo "   $(grep -c exempt "$f") $f"
done
echo "[2/2] done"
