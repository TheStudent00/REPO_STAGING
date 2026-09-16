#!/bin/bash
# rv9 lane 3 -- THE SAMPLE for section 2: six keys of the section-2
# population, spread evenly over the blast's own gate-count order (so
# the cheap end, the middle and the expensive end are all in it), at all
# three optimization settings on c, cpp, go and rust.  It exists to say
# what the whole population will cost before it is run, and its numbers
# are pasted.  One process, no pool, no clock in the driver.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
RV=$P/Research/oracle/riscv
OP=$P/Research/op_pipeline
EMU=$P/Research/oracle/cross_construction/emulation
export HOME=/work
export GOCACHE=/work/rv9gocache GOPATH=/work/rv9gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv9_set_sample
total=6
i=1

echo "[$i/$total] the files this lane reads, by sha256"; i=$((i+1))
sha256sum "$RV/riscv_reference.py" "$OP/term.py" \
  "$G/bitblast.py" "$G/bb1_run.py" "$G/rv9_settings.py"
echo "  started $(date -u +%FT%TZ)"

for setting in ship one off; do
  echo "[$i/$total] the sample at setting '$setting'"; i=$((i+1))
  timeout 5000 python3 "$G/rv9_settings.py" run "$setting" "$OP" "$OP" \
    "$EMU" "$RV/twins.json" "$RV/model_table_rv.json" \
    "$G/rv9_set_sample_$setting" "$G/src_rv9_set_sample" \
    "/work/rv9_set_sample/$setting" "$G/bb1_all.jsonl" \
    "$G/rd1_all.jsonl,$G/rv6_all.jsonl" 6
  echo "  exit: $?  $(date -u +%FT%TZ)"
done

echo "[$i/$total] the three settings side by side"; i=$((i+1))
timeout 1200 python3 "$G/rv9_settings.py" table "$G/rv9_set_sample_ship" \
  "$G/rv9_set_sample_one" "$G/rv9_set_sample_off" "$RV/twins.json"
echo "  exit: $?"

echo "[$i/$total] the spelling guard over the json this lane wrote"
python3 "$OP/check_no_spelling_keys.py" "$G/rv9_set_sample_ship.json" \
  "$G/rv9_set_sample_one.json" "$G/rv9_set_sample_off.json"
echo "  guard rc=$?"
ls -la "$G"/rv9_set_sample_*.json*
echo "lane rv9_l3 done"
