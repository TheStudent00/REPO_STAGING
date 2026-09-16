#!/bin/bash
# rv9 lane 1 -- THE SAMPLE: the first two (cell, place) keys of the
# population (every key no store records a proof for, on any language, by
# any route) taken through the native route on c, cpp, go and rust, with
# every object section 1 of the brief asks for printed: the rendered
# source, the compiled body, the references the body makes outside
# itself, the two canonical texts, whether they are identical, and the
# first node at which they differ.  One process, no pool, no clock in the
# driver.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
RV=$P/Research/oracle/riscv
OP=$P/Research/op_pipeline
EMU=$P/Research/oracle/cross_construction/emulation
export HOME=/work
export GOCACHE=/work/rv9gocache GOPATH=/work/rv9gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv9_native_sample
total=3
i=1

echo "[$i/$total] the files this lane reads, by sha256"; i=$((i+1))
sha256sum "$RV/riscv_reference.py" "$OP/term.py" \
  "$OP/check_no_spelling_keys.py" "$G/render_general.py" \
  "$G/rv_general.py" "$G/rv9_native.py"
echo "  started $(date -u +%FT%TZ)"

echo "[$i/$total] the native route on the first two keys of the population"; i=$((i+1))
timeout 3000 python3 "$G/rv9_native.py" run "$OP" "$OP" "$EMU" \
  "$RV/twins.json" "$RV/model_table_rv.json" "$G/rv9_native_sample" \
  "$G/src_rv9_native_sample" /work/rv9_native_sample \
  "$G/rd1_all.jsonl,$G/rv6_all.jsonl,$G/bb1_all.jsonl" 8
echo "  exit: $?  finished $(date -u +%FT%TZ)"

echo "[$i/$total] the spelling guard over the json this lane wrote"
python3 "$OP/check_no_spelling_keys.py" "$G/rv9_native_sample.json"
echo "  guard rc=$?"
ls -la "$G"/rv9_native_sample.jsonl "$G"/rv9_native_sample.json
echo "lane rv9_l1 done"
