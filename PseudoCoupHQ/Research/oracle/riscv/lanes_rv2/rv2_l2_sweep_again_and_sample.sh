#!/usr/bin/env bash
# rv2 lane 2 -- the sweep again, after the symbolic-immediate shape was
# restricted to the builders that actually read an immediate (a spelling
# that is not a second spelling is not a second cell); then the memory
# SAMPLE the law asks for: 20 x86 cells re-run from the model table's own
# recorded line, with the peak resident printed at every stage.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
MODEL=PseudoCoupHQ/Research/oracle/arch_opcodes/model
export HOME=/work
total=3

echo "[1/$total] the sweep again"
python3 $RV/model_table_rv.py sweep $OP $RV/model_table_rv

echo "[2/$total] the markdown"
python3 $RV/model_table_rv.py report $RV/model_table_rv

echo "[3/$total] the sample: 20 x86 cells re-run, peak resident printed"
python3 $RV/twins.py sample $OP $MODEL/model_table_rows.json \
  $RV/model_table_rv.json

echo "--- lane finished"
