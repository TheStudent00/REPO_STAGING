#!/bin/bash
# rv9 lane 9 -- SECTION 3: the table "of 255" per language for the union
# of every route after this task, beside the same table computed from
# the stores that existed before it BY THE SAME READER IN THE SAME RUN;
# then the three optimization settings side by side over the whole
# section-2 population; then the spelling guard over every json this
# task wrote, and the exempt count over every file it added.
set -u
P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
RV=$P/Research/oracle/riscv
OP=$P/Research/op_pipeline
export HOME=/work
total=5
i=1

echo "[$i/$total] the files this lane reads, by sha256"; i=$((i+1))
sha256sum "$RV/riscv_reference.py" "$OP/term.py" \
  "$OP/check_no_spelling_keys.py" "$G/rv9_union.py" \
  "$G/rv9_settings.py"
echo "  started $(date -u +%FT%TZ)"

echo "[$i/$total] the union of every route, before and after"; i=$((i+1))
timeout 1800 python3 "$G/rv9_union.py" table "$RV/twins.json" \
  "rd1=$G/rd1_all,bb1=$G/bb1_all" \
  "rd1=$G/rd1_all,bb1=$G/bb1_all,rv9_native=$G/rv9_native,rv9_ship=$G/rv9_set_ship,rv9_one=$G/rv9_set_one,rv9_off=$G/rv9_set_off"
echo "  exit: $?"

echo "[$i/$total] the three settings side by side, the whole population"; i=$((i+1))
timeout 1800 python3 "$G/rv9_settings.py" table "$G/rv9_set_ship" \
  "$G/rv9_set_one" "$G/rv9_set_off" "$RV/twins.json"
echo "  exit: $?"

echo "[$i/$total] the spelling guard over every json this task wrote"; i=$((i+1))
python3 "$OP/check_no_spelling_keys.py" "$G/rv9_native.json" \
  "$G/rv9_native_sample.json" "$G/rv9_set_ship.json" \
  "$G/rv9_set_one.json" "$G/rv9_set_off.json" \
  "$G/rv9_set_sample_ship.json" "$G/rv9_set_sample_one.json" \
  "$G/rv9_set_sample_off.json" "$G/rv9_offcause.json"
echo "  guard rc=$?"

echo "[$i/$total] grep -c exempt over every file this task added"
grep -c exempt "$G"/rv9_native.py "$G"/rv9_settings.py \
  "$G"/rv9_offcause.py "$G"/rv9_union.py "$RV"/lanes_rv9/*.sh
echo "  grep rc=$?"
echo "lane rv9_l9 done"
