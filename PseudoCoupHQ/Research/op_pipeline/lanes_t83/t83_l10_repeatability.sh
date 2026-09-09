#!/usr/bin/env bash
# t83 lane 10 -- IS THE BOUND THE CAUSE, or is the gate simply not
# repeatable?  Lane 9's bounded re-transcription of three stored
# shards differed from the store on four go units: three kept the same
# verdict with a different witness, and one moved DISPROVED ->
# UNDECIDED on the solver's 3000 ms limit.  None of that smells of
# memory.  So the SAME bounded check is run TWICE here, with nothing
# changed between the runs.  If the two runs disagree with the store
# in different places, the variation is the solver's and not the
# bound's.
set -u
cd PseudoCoupHQ/Research/op_pipeline
for pass in 1 2; do
  echo "======== [$pass/2] the same bounded check, run again ========"
  rm -rf /work/t83_check_store /work/t83_check_state.json
  python3 term66_bounded.py 6144 100000 --check \
    canon40_wrapped_go.json \
    canon40_interp.json \
    canon40_regen_store/op_units2_c_c0001.json
  echo "pass $pass exit $?"
done
