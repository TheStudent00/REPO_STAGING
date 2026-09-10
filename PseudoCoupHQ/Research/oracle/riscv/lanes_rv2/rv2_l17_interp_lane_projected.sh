#!/usr/bin/env bash
# rv2 lane 17 -- the interpreter's handful again. Lane 15 could not find
# the sources: the bank records a compiled target's source relative to
# `autopoly/` and an interpreted target's relative to `emulation/` above
# it, and only the first root was tried.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
MODEL=PseudoCoupHQ/Research/oracle/arch_opcodes/model
ORIG=PseudoCoupHQ/Research/oracle/arch_opcodes/level0/ref2_originals
EMU=PseudoCoupHQ/Research/oracle/cross_construction/emulation
BANK=$EMU/autopoly
export HOME=/work
total=2

echo "[1/$total] one interpreter's handful, re-run"
python3 $RV/interp_recheck.py run $ORIG $OP $MODEL/model_table_rows.json \
  $RV/twins.json $BANK/certificates.jsonl $BANK $RV/interp_recheck 6

echo "[2/$total] the spelling guard"
python3 $OP/check_no_spelling_keys.py $RV/interp_recheck.json
echo "guard rc=$?"
echo "--- lane finished"
