#!/bin/bash
# t4_l21_the_constructions_one_process_each_again.sh -- task t4, lane 21:
# the z3 fallback again, with each obligation posed in a PROCESS OF ITS
# OWN.
#
# LANE 19 IS THIS LANE WITHOUT ITS IMPORT: every part ended on
# `NameError: name 'subprocess' is not defined` in 0.7 s, which is the
# one line the edit that wrote `one_in_a_child` did not land.
#
# LANE 15's FINDING, which is why this lane exists.  z3's
# `memory_max_size` raises once and then refuses everything after it in
# the same process.  Lane 15 posed a whole part in one process, so after
# the divider at 32 bits exhausted the bound every later row in that
# part came back UNDECIDED in about zero seconds -- `fp_neg` at 79 bits
# among them, and that same obligation at the tiny formats is PROVED in
# lane 5.  Those rows say the solver could not decide when what happened
# is that the solver was already out of memory.  Lane 15's four part
# files are kept on disk and named in `collect_proofs.SET_ASIDE` with
# that reason; this lane's are what the proof table reads.
#
# THE CEILING IS THE BRIEF'S HARD 30 SECONDS and is never raised.  It is
# SOFT in z3 -- checked between propagations, not during bit-blasting --
# so a wide multiply overshoots it and what the row records is the
# seconds ACTUALLY TAKEN.
#
#   [1/6] part 1 of 5
#   [2/6] part 2 of 5
#   [3/6] part 3 of 5
#   [4/6] part 4 of 5
#   [5/6] part 5 of 5
#   [6/6] the proof table, rebuilt
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_T4; the solver's
# own bound is 4 GB and it now stops one child rather than a whole part.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_t4_brief.md
set -u

G=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general
total=6

for p in 1 2 3 4 5; do
    echo ""
    echo "[$p/$total] part $p of 5"
    timeout 3600 python3 "$G/check_constructions.py" store_rest "$p" 5
    echo "  exit: $?"
done

echo ""
echo "[6/$total] the proof table, rebuilt"
timeout 900 python3 "$G/collect_proofs.py" build
echo "  exit: $?"

echo ""
echo "peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
