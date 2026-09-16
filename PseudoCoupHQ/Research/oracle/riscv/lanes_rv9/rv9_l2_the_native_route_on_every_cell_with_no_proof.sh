#!/bin/bash
# rv9 lane 2 -- SECTION 1 OF THE BRIEF, WHOLE: every (cell, place) for
# which no store records a proof -- on any language, by any route --
# taken through the native route on c, cpp, go and rust, with the
# rendered source, the compiled body, the references the body makes
# outside itself, the lifted formula beside the definition's, whether
# the canonical form makes them identical, and the first node at which
# they differ.  Where the gate's own 3,000 ms ran out the same question
# is asked again with ten times the room and through z3's own bit-blast
# tactic, and both answers are reported beside it.  One process, no
# pool, no clock in the driver.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
RV=$P/Research/oracle/riscv
OP=$P/Research/op_pipeline
EMU=$P/Research/oracle/cross_construction/emulation
export HOME=/work
export GOCACHE=/work/rv9gocache GOPATH=/work/rv9gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv9_native
total=3
i=1

echo "[$i/$total] the files this lane reads, by sha256"; i=$((i+1))
sha256sum "$RV/riscv_reference.py" "$OP/term.py" \
  "$OP/check_no_spelling_keys.py" "$G/render_general.py" \
  "$G/rv_general.py" "$G/rv9_native.py"
echo "  started $(date -u +%FT%TZ)"

echo "[$i/$total] the native route on every key with no proof anywhere"; i=$((i+1))
timeout 9000 python3 "$G/rv9_native.py" run "$OP" "$OP" "$EMU" \
  "$RV/twins.json" "$RV/model_table_rv.json" "$G/rv9_native" \
  "$G/src_rv9_native" /work/rv9_native \
  "$G/rd1_all.jsonl,$G/rv6_all.jsonl,$G/bb1_all.jsonl"
echo "  exit: $?  finished $(date -u +%FT%TZ)"

echo "[$i/$total] the spelling guard over the json this lane wrote"
python3 "$OP/check_no_spelling_keys.py" "$G/rv9_native.json"
echo "  guard rc=$?"
ls -la "$G"/rv9_native.jsonl "$G"/rv9_native.json
echo "lane rv9_l2 done"
