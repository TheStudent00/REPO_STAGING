#!/usr/bin/env bash
# rv2 lane 3 -- the sample again, this time with the x86 reference taken
# from ref2_originals: task ref2 is correcting op_pipeline/reference.py in
# the same hours, and the model table on disk plus every certificate in
# the bank were produced BEFORE those corrections. The lane prints the
# sha256 of the reference it actually imported, and the count of place
# rows where the re-run reproduces the table's own recorded text.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
MODEL=PseudoCoupHQ/Research/oracle/arch_opcodes/model
ORIG=PseudoCoupHQ/Research/oracle/arch_opcodes/level0/ref2_originals
export HOME=/work
total=2

echo "[1/$total] the two references, by hash"
sha256sum $OP/reference.py $OP/condition_table.py \
  $ORIG/reference.py $ORIG/condition_table.py \
  $MODEL/model_table_rows.json

echo "[2/$total] the sample against the PRE-CORRECTION reference"
python3 $RV/twins.py sample $ORIG $OP $MODEL/model_table_rows.json \
  $RV/model_table_rv.json

echo "--- lane finished"
