#!/usr/bin/env bash
# t101 lane 4 -- the two source quotations lane 3 could not read, re-run
# with the container's own path for the repo. The DevComms log writes the
# same two commands with the host path `PseudoCoupHQ/...`,
# which is what check_conventions_log_claims.py remaps to `
# PseudoCoupHQ/...` before it re-runs them.
set -u
cd PseudoCoupHQ

run() {
  echo "\$ $1"
  eval "$1"
  echo "--------8<--------"
}

echo "======== [1/2] fold.py :: dwarf_rows, the shared reader ========"
run "sed -n '80,91p' PseudoCoupHQ/Research/op_pipeline/fold.py"

echo "======== [2/2] the lane that read DWARF off the anchor object ========"
run "sed -n '255,262p' PseudoCoupHQ/Research/op_pipeline/trickle_lanes/asgrecap_asgrecap_go_c0001.sh"

exit 0
