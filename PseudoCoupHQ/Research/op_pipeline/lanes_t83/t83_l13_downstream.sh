#!/usr/bin/env bash
# t83 lane 13 -- everything downstream of a complete term66_store, in
# order, each step under an address-space bound.
#
# THE MEMORY BOUND, stated: each step runs in a subshell with
# `ulimit -v 6291456` (6 GB of address space).  An allocation past it
# raises MemoryError, which python reports by name with a traceback --
# a named abort, not a cgroup kill.  The heaviest input any of these
# steps reads is `the_pool5.json` at 32,648,786 bytes and
# `term66_store` at 3.1 MB on disk before this round's full walk, so 6
# GB is far above what the steps need and is a ceiling, not a budget.
#
# THE ORDER, and why:
#   1 audit66.py            the four states, the movements with their
#                           causes, the consistency line, layer 5
#   2 name_census7.py       the census over term66_store
#   3 pool66_run.py         the pool, the families, the exception
#                           families, the pool5->pool6 delta and
#                           E00029's successor
#   4 pool6_prediction_check.py   task 79's prediction, separated from
#                           the member change and the ledger change
#   5 guard83_term_pool.py  the UNMODIFIED spelling guard over every
#                           JSON artifact task 83 writes, ONE process
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline

# PRECONDITION: this lane must never run on a partial store.  A
# partial store would make audit66.py overwrite audit66.json with a
# number computed over fewer records than the population it names.
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
step 5 "guard83_term_pool.py -- the unmodified guard, ONE process" guard83_term_pool.py

echo
echo "======== E00029's successor, printed ========"
cat the_pool6_entry_E00029_successor_printed.txt

echo
echo "======== the guard transcript, and its exempt count ========"
grep -c exempt guard83_term_pool_transcript.txt
tail -20 guard83_term_pool_transcript.txt
exit 0
