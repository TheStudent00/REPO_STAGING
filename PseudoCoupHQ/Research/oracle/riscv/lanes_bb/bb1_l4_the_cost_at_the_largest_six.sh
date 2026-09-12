#!/bin/bash
# bb1 lane 4 -- the cost sample at the EXPENSIVE end. The driver's own `limit`
# takes the first n attempts, and the first rows of twins.json are the cheap
# end, so the population is ordered by the number of GATES z3's blast gave it
# (lane bb1_l3's own sizes file, machine-form evidence) and the six largest
# cells are taken. This is what says what the whole run will cost.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
RV=$P/Research/oracle/riscv
OP=$P/Research/op_pipeline
EMU=$P/Research/oracle/cross_construction/emulation
export HOME=/work
export GOCACHE=/work/bb1gocache GOPATH=/work/bb1gopath
export BB1_SIZES="$G/bb1_sizes.json"
mkdir -p "$GOCACHE" "$GOPATH" /work/bb1_largest
total=3
i=1

echo "[$i/$total] the six largest circuits, four languages: started $(date -u +%FT%TZ)"; i=$((i+1))
timeout 5400 python3 "$G/bb1_run.py" run "$OP" "$OP" "$EMU" \
  "$RV/twins.json" "$RV/model_table_rv.json" "$G/bb1_largest" \
  "$G/src_bb1_largest" /work/bb1_largest 24
echo "  exit: $?  finished $(date -u +%FT%TZ)"

echo "[$i/$total] every attempt of that sample"; i=$((i+1))
timeout 900 python3 "$G/bb1_run.py" rows "$G/bb1_largest" 0
echo "  exit: $?"

echo "[$i/$total] the spelling guard over the json this lane wrote"
python3 "$OP/check_no_spelling_keys.py" "$G/bb1_largest.json"
echo "  guard rc=$?"
echo "lane bb1_l4 done"
