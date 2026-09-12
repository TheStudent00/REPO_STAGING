#!/bin/bash
# rv4_l2_the_round.sh -- task rv4, lane 2: THE ROUND OF RECORD, the one the owner
# timed.  Every RISC-V cell whose term the lifter states, on each of the
# three compiled targets that has no proved certificate for it, rendered by
# the general tier, compiled for riscv64 WITH OPTIMIZATION OFF, carved,
# walked through the RISC-V reference and gated -- eight worker processes,
# the driver's own wall clock hard at nine minutes, and a
# NOT_REACHED_IN_BUDGET row for every pair the clock did not reach.
#
# THE LANE HOLDS NOTHING ELSE.  The count, the guard and the tables are
# lane 3, because this lane's submit-to-done must be inside ten minutes and
# nothing that is not the round is allowed to sit inside that window.
#
#   [1/2] the round: eight workers, nine minutes hard
#   [2/2] peak resident
#
# MEMORY: bound 6 GB resident per worker, named abort ABORT_MEMORY_RV4.
# The instance's own ceiling is 20g for the eight together (rv4.conf).
#
# Node: hq.research.arch_unit_oracle.architectures.riscv64
# Brief: Research/briefs/task_rv4_brief.md
set -u

P=PseudoCoupHQ
RV=$P/Research/oracle/riscv
export HOME=/work
export GOCACHE=/work/rv4gocache GOPATH=/work/rv4gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv4round
total=2

i=1
echo "[$i/$total] the round: eight workers, nine minutes hard"
date -u +"  the driver starts at %Y-%m-%dT%H:%M:%SZ"
timeout 700 python3 "$RV/rv4_off.py" round "$P" \
  "$RV/rv4_population.json" 8 540 "$RV/rv4_round" "$RV/src_rv4" \
  /work/rv4round
echo "  exit: $?"
date -u +"  the driver ended at %Y-%m-%dT%H:%M:%SZ"

i=2
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
