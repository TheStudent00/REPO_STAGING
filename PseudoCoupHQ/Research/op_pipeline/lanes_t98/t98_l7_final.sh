#!/usr/bin/env bash
# t98 lane 7 -- the final pass, after the nine earlier-generation pool
# records were added: pane 5 at the present moment and at 14 moments of
# the repository's own history, with the row keys that go unexplained
# named at each.  Lane 5 found nine at two commits of 2026-09-03; this
# says whether any is left.
set -u
cd PseudoCoupHQ/Research/op_pipeline

step () {
  echo
  echo "======== [$1/3] $2 ========"
  shift 2
  ( ulimit -v 6291456 ; python3 "$@" )
  echo "-- exit $?"
}

step 1 "the present moment" t98_render_check.py now
step 2 "every unexplained row key, over 14 moments" t98_render_check.py keys 14
step 3 "the pane at those moments: numbers or refusal" t98_render_check.py past 14
