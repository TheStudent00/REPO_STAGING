#!/usr/bin/env bash
# t98 lane 4 -- pane 5 rendered off the page and checked: every row's
# explanation present or the row visibly marked unexplained, no
# javascript in what the pane emits, every computed figure printed, the
# cost, and the pane drawn at a run of past moments.
#
# THE MEMORY BOUND: `ulimit -v 6291456` (6 GB of address space); an
# allocation past it raises MemoryError, reported BY NAME.
set -u
cd PseudoCoupHQ/Research/op_pipeline

step () {
  echo
  echo "======== [$1/3] $2 ========"
  shift 2
  ( ulimit -v 6291456 ; python3 "$@" )
  echo "-- exit $?"
}

step 1 "the present moment: rows, controls, unexplained rows, script count, cost" t98_render_check.py now
step 2 "every computed figure, to be set against the brief's own" t98_render_check.py figures
step 3 "the pane at past moments: numbers or refusal" t98_render_check.py past 14
