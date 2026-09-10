#!/usr/bin/env bash
# rv2 lane 15 -- THE LOOP ON THE DELTA and the interpreter's handful.
# The loop: find_emulation over the RISC-V cells no x86 cell twins under
# either reading, on c and go, both routes -- the term rendered by
# handful's own renderer, and where the corpus attests a riscv64 SINGLETON
# for the cell, that probe's own source. Then a handful of cpython
# emulations re-run at 200 points each, which is the evidence behind
# "an agreed certificate transfers as it is".
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
MODEL=PseudoCoupHQ/Research/oracle/arch_opcodes/model
ORIG=PseudoCoupHQ/Research/oracle/arch_opcodes/level0/ref2_originals
EMU=PseudoCoupHQ/Research/oracle/cross_construction/emulation
BANK=$EMU/autopoly
export HOME=/work
export GOCACHE=/work/rv2gocache GOPATH=/work/rv2gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv2loop
total=3

echo "[1/$total] the loop on the delta"
python3 $RV/rv_loop.py run $ORIG $OP $EMU $RV/twins.json \
  $RV/attest_rv.json $RV/model_table_rv.json $RV/rv_loop \
  $RV/src_rv2 /work/rv2loop

echo "[2/$total] one interpreter's handful, re-run"
python3 $RV/interp_recheck.py run $ORIG $OP $MODEL/model_table_rows.json \
  $RV/twins.json $BANK/certificates.jsonl $BANK $RV/interp_recheck 6

echo "[3/$total] the spelling guard"
python3 $OP/check_no_spelling_keys.py $RV/rv_loop.json \
  $RV/interp_recheck.json
echo "guard rc=$?"
echo "--- lane finished"
