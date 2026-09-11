#!/bin/bash
# t4_l18_the_bank_the_readings_and_the_report.sh -- task t4, lane 18: the
# bank rebuilt with this pass in it, the three readings, the five tables
# the brief's section 2 asks for, and the spelling guard over every json
# this task wrote.
#
# THE BANK IS REBUILT FROM HERE WITH TWO PASSES REGISTERED, not one:
# neither the construct tier's pass nor this one is in `bank.PASSES`'s
# own file -- each registers itself from outside, which is task t2's own
# rule and its own reason -- so a rebuild with only this one registered
# would write a bank with t2's fourteen proved places missing.
#
#   [1/6] the bank, rebuilt
#   [2/6] the three readings, beside task t2's 96 / 154 / 141 of 205
#   [3/6] the five tables of the measurement
#   [4/6] the spelling guard over every json this task wrote
#   [5/6] `grep -c exempt` over every file this task added
#   [6/6] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t4_brief.md
set -u

P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
OP=$P/Research/op_pipeline
total=6

i=1
echo "[$i/$total] the bank, rebuilt with this pass and task t2's in it"
timeout 3600 python3 "$G/general.py" bank
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] the three readings"
timeout 3600 python3 "$G/general.py" readings
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] the five tables of the measurement"
timeout 3600 python3 "$G/general_report.py" report
echo "  exit: $?"

i=4
echo ""
echo "[$i/$total] the spelling guard over every json this task wrote"
python3 "$OP/check_no_spelling_keys.py" \
  "$G/kind_census.json" \
  "$G/construction_proofs.json" \
  "$G/general.json" \
  "$G/general_measurement.json" \
  "$G"/constructions_*.json \
  "$G"/lemmas_t4*.json \
  "$G"/vocabulary_*.json \
  "$G"/rv_general*.json
echo "  guard rc=$?"

i=5
echo ""
echo "[$i/$total] grep -c exempt over every file this task added"
for f in "$G"/*.py "$G"/*.json; do
    n=$(grep -c exempt "$f" || true)
    if [ "$n" != "0" ]; then
        echo "  $n  $f"
    fi
done
echo "  (nothing above means every added file has 0)"
grep -c exempt "$G"/*.py | sed 's#.*/##'

i=6
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
