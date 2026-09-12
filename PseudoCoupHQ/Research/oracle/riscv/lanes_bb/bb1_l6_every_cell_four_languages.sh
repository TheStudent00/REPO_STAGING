#!/bin/bash
# bb1 lane 6 -- THE RUN: every one of the 255 RISC-V cells of twins.json
# through z3's own bit-blast, the circuit written as one named local per gate
# in c, cpp, go and rust, compiled for riscv64 at the corpus's ship flags,
# carved, walked and gated. One process, no pool, no clock in the driver.
# Then every attempt printed, the three routes in one table, and the guard.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
RV=$P/Research/oracle/riscv
OP=$P/Research/op_pipeline
EMU=$P/Research/oracle/cross_construction/emulation
export HOME=/work
export GOCACHE=/work/bb1gocache GOPATH=/work/bb1gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/bb1_all
total=4
i=1

echo "[$i/$total] every cell, four languages: started $(date -u +%FT%TZ)"; i=$((i+1))
timeout 16000 python3 "$G/bb1_run.py" run "$OP" "$OP" "$EMU" \
  "$RV/twins.json" "$RV/model_table_rv.json" "$G/bb1_all" \
  "$G/src_bb1_all" /work/bb1_all
echo "  exit: $?  finished $(date -u +%FT%TZ)"

echo "[$i/$total] every attempt, its gates, source lines, compile seconds, body size, outcome and check seconds"; i=$((i+1))
timeout 1200 python3 "$G/bb1_run.py" rows "$G/bb1_all" 0
echo "  exit: $?"

echo "[$i/$total] the three routes in one table, beside rv6"; i=$((i+1))
timeout 1200 python3 "$G/bb1_run.py" table "$G/bb1_all" "$G/rv6_all" \
  "$RV/twins.json"
echo "  exit: $?"

echo "[$i/$total] the spelling guard over every json this task wrote"
python3 "$OP/check_no_spelling_keys.py" "$G/bb1_all.json" \
  "$G/bb1_sizes.json" "$G/bb1_first.json" "$G/bb1_largest.json"
echo "  guard rc=$?"
ls -la "$G"/bb1_all.jsonl "$G"/bb1_all.json
echo "lane bb1_l6 done"
