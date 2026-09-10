#!/usr/bin/env bash
# rv2 lane 4 -- THE MATCH, BY TERM. Every RISC-V cell's place term against
# every x86 cell's place term: identical after Term.normalize is a text
# twin, else z3 at 3,000 ms over the pairs of the same term width and the
# same free-symbol widths that also agree at every sample point. The x86
# reference is the PRE-CORRECTION one ref2 kept, because the model table
# on disk and the bank were produced under it.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
MODEL=PseudoCoupHQ/Research/oracle/arch_opcodes/model
ORIG=PseudoCoupHQ/Research/oracle/arch_opcodes/level0/ref2_originals
export HOME=/work
total=2

echo "[1/$total] the match"
python3 $RV/twins.py match $ORIG $OP $MODEL/model_table_rows.json \
  $MODEL/model_table_attest.json $RV/model_table_rv.json $RV/twins 3000

echo "[2/$total] the spelling guard"
python3 $OP/check_no_spelling_keys.py $RV/twins.json
echo "guard rc=$?"

echo "--- lane finished"
