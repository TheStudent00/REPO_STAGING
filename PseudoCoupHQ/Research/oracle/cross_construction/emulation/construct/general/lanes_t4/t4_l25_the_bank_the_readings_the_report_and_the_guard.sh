#!/bin/bash
# t4_l25_the_bank_the_readings_the_report_and_the_guard.sh -- task t4,
# lane 25: the bank rebuilt with this pass in it, the three readings,
# the five tables the brief's section 2 asks for, the RISC-V count with
# its denominator corrected, and the spelling guard over every json this
# task wrote.
#
# THE BANK IS REBUILT FROM HERE WITH TWO PASSES REGISTERED, not one:
# neither the construct tier's pass nor this one is in `bank.PASSES`'s
# own file -- each registers itself from outside, which is task t2's own
# rule and its own reason -- so a rebuild with only this one registered
# would write a bank with t2's fourteen proved places missing.
#
# THE RISC-V COUNT IS RE-RUN because lane 17 printed its shares against
# 1,512, which is the number of ROWS in `model_table_rv.json` -- one per
# (mnemonic, operand shape, key width, written place) -- and a CELL is
# the triple without the place.  The counts were right and the shares
# were not; the denominator is now the cell count, which is what task
# rv3's own 117 of 255 is against.
#
#   [1/7] the bank, rebuilt
#   [2/7] the three readings, beside task t2's 96 / 154 / 141 of 205
#   [3/7] the five tables of the measurement
#   [4/7] the RISC-V count, beside rv3's 117 of 255
#   [5/7] the spelling guard over every json this task wrote
#   [6/7] `grep -c exempt` over every file this task added
#   [7/7] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t4_brief.md
set -u

P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
OP=$P/Research/op_pipeline
RV=$P/Research/oracle/riscv
total=7

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
echo "[$i/$total] the RISC-V count, beside rv3's 117 of 255"
timeout 900 python3 "$G/rv_general.py" count "$G/rv_general" \
  "$RV/twins.json" "$RV/certificates_riscv64_rv3.jsonl" \
  "$RV/rv_loop.jsonl"
echo "  exit: $?"

i=5
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

i=6
echo ""
echo "[$i/$total] grep -c exempt over every file this task added"
grep -c exempt "$G"/*.py | sed 's#.*/##'

i=7
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
