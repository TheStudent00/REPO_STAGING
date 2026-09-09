#!/usr/bin/env bash
# t97 lane 10 -- the downstream steps that CAN run over the store as
# the two passes left it, and the one that mechanically cannot, with
# its refusal pasted rather than worked around.
#
# THE POPULATION, stated once and carried by every artifact:
# canon40 proves 30,324 wrapped texts; term66_store holds 30,280 of
# them.  The 44 short are the units whose LAYER-5 normalization does
# not converge -- measured invariant at 1536, 4096 and 18432 MB, the
# peak pinned against every ceiling (log_202 section 4).  Their layer-4
# term is built and PROVED; it is the comparison key that is missing.
#
# `pool66_run.py` refuses a member set short of the population.  That
# refusal is CORRECT and is NOT circumvented: it is run, and its own
# words are the evidence.
#
# THE MEMORY BOUND: each step in a subshell with `ulimit -v 6291456`
# (6 GB of address space); an allocation past it raises MemoryError,
# which python reports BY NAME.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline

echo "======== the store this lane reads ========"
python3 report97_numbers.py walk

step () {
  echo
  echo "======== [$1/4] $2 ========"
  ( ulimit -v 6291456 ; shift 2 ; python3 "$@" )
  echo "-- exit $?"
}

step 1 "audit66.py -- the four states, the movements, the consistency line" audit66.py
step 2 "name_census7.py -- the census over term66_store" name_census7.py
step 3 "pool66_run.py -- the pool; its own refusal is the evidence" pool66_run.py
step 4 "guard97_term_pool.py -- the unmodified guard, ONE process" guard97_term_pool.py

echo
echo "======== the guard transcript, and its exempt count ========"
echo "grep -c exempt over the guard's own output:"
grep -c exempt guard97_term_pool_transcript.txt
tail -12 guard97_term_pool_transcript.txt
exit 0
