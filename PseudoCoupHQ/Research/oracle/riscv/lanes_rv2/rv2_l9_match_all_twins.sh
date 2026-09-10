#!/usr/bin/env bash
# rv2 lane 9 -- THE MATCH again, now carrying BOTH readings: the whole
# written place, and both sides cut to the RISC-V cell's own key_width.
# The second reading exists because RISC-V's 32-bit forms sign-extend into
# the whole register where x86's zero-extend, so at the whole place a `w`
# form can never twin an x86 32-bit form and the number would read as a
# meaning difference when it is a write-rule difference.
# THIS RUN also keeps EVERY x86 cell that shares a matched term, not the
# first eight: one term is spelled by many cells, and the cells the bank
# holds certificates for were being cut off by that truncation.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
MODEL=PseudoCoupHQ/Research/oracle/arch_opcodes/model
ORIG=PseudoCoupHQ/Research/oracle/arch_opcodes/level0/ref2_originals
export HOME=/work
total=3

echo "[1/$total] the match"
python3 $RV/twins.py match $ORIG $OP $MODEL/model_table_rows.json \
  $MODEL/model_table_attest.json $RV/model_table_rv.json $RV/twins 3000

echo "[2/$total] the markdown"
python3 $RV/twins.py report $RV/twins

echo "[3/$total] the spelling guard"
python3 $OP/check_no_spelling_keys.py $RV/twins.json
echo "guard rc=$?"
echo "--- lane finished"
