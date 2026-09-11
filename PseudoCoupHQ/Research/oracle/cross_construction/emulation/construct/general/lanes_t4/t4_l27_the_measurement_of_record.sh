#!/bin/bash
# t4_l27_the_measurement_of_record.sh -- task t4, lane 27: the bank
# rebuilt with this pass in it, the three readings, the five tables the
# brief's section 2 asks for, the RISC-V count against the denominator
# task rv3 uses, and the spelling guard over every json this task wrote.
#
# THE PASS IS THE STORE AS LANES 23, 24 AND 26 LEFT IT: 970 lines.  What
# it does not hold is the flag-consumer (cell, target) runs each of
# which costs about 2,000 s -- one written place per setter cell,
# seventeen of them, each paying the native route's own compile and gate
# and then this tier's two policies -- and which are named one by one in
# `t4_general_left_behind.json` with their cause.
#
# THE BANK IS REBUILT WITH TWO PASSES REGISTERED, not one: neither the
# construct tier's pass nor this one is in `bank.PASSES`'s own file --
# each registers itself from outside, which is task t2's own rule and
# its own reason -- so a rebuild with only this one registered would
# write a bank with t2's fourteen proved places missing.
#
#   [1/8] what the store and the left-behind list hold
#   [2/8] the bank, rebuilt
#   [3/8] the three readings, beside task t2's 96 / 154 / 141 of 205
#   [4/8] the five tables of the measurement
#   [5/8] the RISC-V count, beside rv3's 117 of 255
#   [6/8] the spelling guard over every json this task wrote
#   [7/8] `grep -c exempt` over every file this task added
#   [8/8] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t4_brief.md
set -u

P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
A=$P/Research/oracle/cross_construction/emulation/autopoly
OP=$P/Research/op_pipeline
RV=$P/Research/oracle/riscv
total=8

i=1
echo "[$i/$total] what the store and the left-behind list hold"
wc -l "$A/t4_general_runs.jsonl"
echo "  the runs left behind, LITERAL:"
cat "$A/t4_general_left_behind.json" 2>/dev/null || echo "  (none)"
echo ""
ls -la "$A"/t4_general_runs.jsonl* | sed 's#.*/##'

i=2
echo ""
echo "[$i/$total] the bank, rebuilt with this pass and task t2's in it"
timeout 3600 python3 "$G/general.py" bank
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] the three readings"
timeout 3600 python3 "$G/general.py" readings
echo "  exit: $?"

i=4
echo ""
echo "[$i/$total] the five tables of the measurement"
timeout 3600 python3 "$G/general_report.py" report
echo "  exit: $?"

i=5
echo ""
echo "[$i/$total] the RISC-V count, beside rv3's 117 of 255"
timeout 900 python3 "$G/rv_general.py" count "$G/rv_general" \
  "$RV/twins.json" "$RV/certificates_riscv64_rv3.jsonl" \
  "$RV/rv_loop.jsonl"
echo "  exit: $?"

i=6
echo ""
echo "[$i/$total] the spelling guard over every json this task wrote"
FILES=""
for f in "$G/kind_census.json" "$G/construction_proofs.json" \
         "$G/general_measurement.json" \
         "$G"/constructions_*.json "$G"/lemmas_t4*.json \
         "$G"/vocabulary_*.json "$G"/rv_general*.json ; do
    if [ -f "$f" ]; then
        FILES="$FILES $f"
    fi
done
echo "  files: $(echo $FILES | wc -w)"
python3 "$OP/check_no_spelling_keys.py" $FILES
echo "  guard rc=$?"

i=7
echo ""
echo "[$i/$total] grep -c exempt over every file this task added"
grep -c exempt "$G"/*.py | sed 's#.*/##'

i=8
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
