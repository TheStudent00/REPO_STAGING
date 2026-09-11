#!/bin/bash
# t4_l17_the_tier_on_riscv64.sh -- task t4, lane 17: the general tier on
# the SECOND architecture -- every RISC-V cell with no x86 twin,
# rendered again under both policies, compiled for riscv64 at the
# corpus's ship flags, carved, walked through the RISC-V reference and
# gated.
#
# The count this produces stands beside task rv3's 117 of 255
# (`DevComms/log_260` section 5.4): the inheritance's 35 cells, task
# rv2's loop's 82, and their union.  The population is the same -- the
# cells `twins.json` leaves untwinned -- so the two numbers are about
# the same thing.
#
# THE X86 REFERENCE IS THE CORRECTED ONE, `Research/op_pipeline`, which
# task ref2 closed on 2026-09-10 (`DevComms/log_261`): level 0 now
# disagrees with the independent reading at NONE of 1,779 places.  Task
# rv2's own lane read the PRE-correction reference out of
# `level0/ref2_originals`, so the two runs are not read as one.
#
#   [1/4] the smoke: eight runs, so the machinery is known to work
#   [2/4] the whole population
#   [3/4] the count, beside rv3's 117 of 255
#   [4/4] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4.
#
# Node: hq.research.arch_unit_oracle.cross_construction.riscv
# Brief: Research/briefs/task_t4_brief.md
set -u

P=PseudoCoupHQ
G=$P/Research/oracle/cross_construction/emulation/construct/general
RV=$P/Research/oracle/riscv
OP=$P/Research/op_pipeline
EMU=$P/Research/oracle/cross_construction/emulation
export HOME=/work
export GOCACHE=/work/t4gocache GOPATH=/work/t4gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/t4rv
total=4

i=1
echo "[$i/$total] the smoke: eight runs"
timeout 1800 python3 "$G/rv_general.py" run "$OP" "$OP" "$EMU" \
  "$RV/twins.json" "$RV/model_table_rv.json" \
  "$G/rv_general_smoke" "$G/src_t4_rv_smoke" /work/t4rv 8
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] the whole population"
timeout 14000 python3 "$G/rv_general.py" run "$OP" "$OP" "$EMU" \
  "$RV/twins.json" "$RV/model_table_rv.json" \
  "$G/rv_general" "$G/src_t4_rv" /work/t4rv
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] the count, beside rv3's 117 of 255"
timeout 900 python3 "$G/rv_general.py" count "$G/rv_general" \
  "$RV/twins.json" "$RV/certificates_riscv64_rv3.jsonl" \
  "$RV/rv_loop.jsonl"
echo "  exit: $?"

i=4
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
