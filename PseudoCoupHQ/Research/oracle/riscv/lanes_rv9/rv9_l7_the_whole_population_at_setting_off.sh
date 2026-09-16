#!/bin/bash
# rv9 lane 7 -- SECTION 2, THE WHOLE POPULATION at setting 'off':
# every optimization level moved to 0, go with the local optimizations and inlining off.
# The population is every (cell, place) the blast route left undecided
# or refused, together with every key no store proves at all -- read off
# the verdicts, never off a name.  One process, no pool, no clock in the
# driver.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
RV=$P/Research/oracle/riscv
OP=$P/Research/op_pipeline
EMU=$P/Research/oracle/cross_construction/emulation
export HOME=/work
export GOCACHE=/work/rv9gocache GOPATH=/work/rv9gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv9_set_off
total=3
i=1

echo "[$i/$total] the files this lane reads, by sha256"; i=$((i+1))
sha256sum "$RV/riscv_reference.py" "$OP/term.py" "$G/bitblast.py" \
  "$G/bb1_run.py" "$G/rv9_settings.py"
echo "  started $(date -u +%FT%TZ)"

echo "[$i/$total] the whole population at setting 'off'"; i=$((i+1))
timeout 20000 python3 "$G/rv9_settings.py" run off "$OP" "$OP" \
  "$EMU" "$RV/twins.json" "$RV/model_table_rv.json" \
  "$G/rv9_set_off" "$G/src_rv9_set_off" "/work/rv9_set_off" \
  "$G/bb1_all.jsonl" "$G/rd1_all.jsonl,$G/rv6_all.jsonl"
echo "  exit: $?  finished $(date -u +%FT%TZ)"

echo "[$i/$total] the spelling guard over the json this lane wrote"
python3 "$OP/check_no_spelling_keys.py" "$G/rv9_set_off.json"
echo "  guard rc=$?"
ls -la "$G"/rv9_set_off.jsonl "$G"/rv9_set_off.json
echo "lane rv9_l7 done"
