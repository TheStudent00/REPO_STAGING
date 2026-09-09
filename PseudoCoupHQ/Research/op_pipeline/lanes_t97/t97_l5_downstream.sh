#!/usr/bin/env bash
# t97 lane 5 -- everything downstream of a COMPLETE term66_store, in
# order, each step under an address-space bound.
#
# PRECONDITION, mechanical: this lane refuses on a partial store, so no
# artifact is ever overwritten with a number computed over fewer
# records than the population it names.
#
# THE MEMORY BOUND, stated: each step runs in a subshell with
# `ulimit -v 6291456` (6 GB of address space).  An allocation past it
# raises MemoryError, which python reports BY NAME with a traceback --
# a named abort, not a cgroup ABORT.
set -u
cd PseudoCoupHQ/Research/op_pipeline

total=$(( $(ls canon40_regen_store/*.json | wc -l) + 6 ))
done_now=$(python3 -c "import json;print(len(json.load(open('term66_state.json'))['done']))")
echo "resume state: $done_now of $total inputs transcribed"
if [ "$done_now" -lt "$total" ]; then
  echo "REFUSED: term66_store is incomplete ($done_now of $total inputs)."
  echo "Nothing downstream is run and no artifact is overwritten."
  exit 4
fi

step () {
  echo
  echo "======== [$1/5] $2 ========"
  ( ulimit -v 6291456 ; shift 2 ; python3 "$@" )
  echo "-- exit $?"
}

step 1 "audit66.py -- the four states, the movements, the consistency line" audit66.py
step 2 "name_census7.py -- the census over term66_store" name_census7.py
step 3 "pool66_run.py -- the pool, the families, the exception families" pool66_run.py
step 4 "pool6_prediction_check.py -- task 79's prediction, checked" pool6_prediction_check.py
step 5 "guard97_term_pool.py -- the unmodified guard, ONE process" guard97_term_pool.py

echo
echo "======== E00029's successor, printed ========"
cat the_pool6_entry_E00029_successor_printed.txt

echo
echo "======== THE CONSISTENCY LINE, pasted off audit66_printed.txt ========"
grep -n -A 6 -i "consistency" audit66_printed.txt | head -40

echo
echo "======== the guard transcript, and its exempt count ========"
echo "grep -c exempt over the guard's own output:"
grep -c exempt guard97_term_pool_transcript.txt
tail -20 guard97_term_pool_transcript.txt
exit 0
