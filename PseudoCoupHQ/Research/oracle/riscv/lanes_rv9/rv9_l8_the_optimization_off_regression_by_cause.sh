#!/bin/bash
# rv9 lane 8 -- WHY OPTIMIZATION OFF MADE THE CHECK WORSE (task rv4,
# log_263, whose written cause was retracted in it).  The same
# population, the same render, the same lifter and the same gate, run
# TWICE -- at the corpus's ship flags and with optimization off -- with
# three measured properties read off every carved body: instructions
# naming a memory address, branches inside the unit, and the walk's own
# refusal.  The transitions are crossed against the three, and the body
# that grew most is pasted at both settings.  One process, no pool, no
# clock in the driver.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
RV=$P/Research/oracle/riscv
OP=$P/Research/op_pipeline
EMU=$P/Research/oracle/cross_construction/emulation
export HOME=/work
export GOCACHE=/work/rv9gocache GOPATH=/work/rv9gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv9_offcause
total=3
i=1

echo "[$i/$total] the files this lane reads, by sha256"; i=$((i+1))
sha256sum "$RV/riscv_reference.py" "$OP/term.py" "$G/rv_general.py" \
  "$G/rv9_native.py" "$G/rv9_offcause.py" "$G/rv4_o0.py"
echo "  started $(date -u +%FT%TZ)"

echo "[$i/$total] both settings over rv4's own population"; i=$((i+1))
timeout 16000 python3 "$G/rv9_offcause.py" run "$OP" "$OP" "$EMU" \
  "$RV/twins.json" "$RV/model_table_rv.json" "$G/rv9_offcause" \
  "$G/src_rv9_offcause" /work/rv9_offcause
echo "  exit: $?  finished $(date -u +%FT%TZ)"

echo "[$i/$total] the spelling guard over the json this lane wrote"
python3 "$OP/check_no_spelling_keys.py" "$G/rv9_offcause.json"
echo "  guard rc=$?"
ls -la "$G"/rv9_offcause.jsonl "$G"/rv9_offcause.json
echo "lane rv9_l8 done"
