#!/bin/bash
# bb1 lane 3 -- the cheap half first: how many gates z3's blast gives every
# one of the 255 RISC-V cells, with nothing compiled; then the driver end to
# end on the first six cells of the population, on c, cpp, go and rust, with
# every attempt's gates, source lines, compile seconds, body size, outcome
# and check seconds printed and the carved bodies beside them.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
RV=$P/Research/oracle/riscv
OP=$P/Research/op_pipeline
EMU=$P/Research/oracle/cross_construction/emulation
export HOME=/work
export GOCACHE=/work/bb1gocache GOPATH=/work/bb1gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/bb1_first
total=4
i=1

echo "[$i/$total] the circuit size of every cell, nothing compiled"; i=$((i+1))
timeout 3000 python3 "$G/bb1_run.py" sizes "$OP" "$OP" "$EMU" \
  "$RV/twins.json" "$RV/model_table_rv.json" "$G/bb1"
echo "  exit: $?"

echo "[$i/$total] the first six cells of the population, four languages"; i=$((i+1))
timeout 1800 python3 "$G/bb1_run.py" run "$OP" "$OP" "$EMU" \
  "$RV/twins.json" "$RV/model_table_rv.json" "$G/bb1_first" \
  "$G/src_bb1_first" /work/bb1_first 24
echo "  exit: $?"

echo "[$i/$total] every attempt of that sample, and the carved bodies"; i=$((i+1))
timeout 600 python3 "$G/bb1_run.py" rows "$G/bb1_first" 400
echo "  exit: $?"

echo "[$i/$total] the spelling guard over every json this lane wrote"
python3 "$OP/check_no_spelling_keys.py" "$G/bb1_sizes.json" "$G/bb1_first.json"
echo "  guard rc=$?"
echo "lane bb1_l3 done"
