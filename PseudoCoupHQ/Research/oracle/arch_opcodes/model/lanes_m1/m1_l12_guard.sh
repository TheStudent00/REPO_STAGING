#!/usr/bin/env bash
# m1_l12_guard.sh -- task m1: the spelling-ban guard, UNMODIFIED, over
# every json this task wrote. `|| true` so the lane prints the guard's
# own verdict for every file rather than stopping at the first failure;
# the verdict lines are the record.
set -euo pipefail
cd /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model
echo "[1/2] task m1: check_no_spelling_keys.py over the four json"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
  model_table.json model_table_rows.json model_table_attest.json \
  model_table_edges.json || true
echo "[2/2] task m1: grep -c exempt over the files this task added"
grep -c exempt model_table.py || true
grep -c exempt model_table.md || true
echo "[2/2] done"
