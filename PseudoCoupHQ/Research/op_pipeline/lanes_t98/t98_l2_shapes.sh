#!/usr/bin/env bash
# t98 lane 2 -- lane 1 again, without `/usr/bin/time`, which is not in
# the image (lane 1's log: "/usr/bin/time: No such file or directory",
# four times).  The program prints its own wall clock and its own peak
# resident size through `resource.getrusage`, so nothing is lost.
#
# What this settles: what a render-time walk of each artifact family
# COSTS, and which definition of "how many arch opcodes a body holds"
# reproduces the figures the task brief measured.
#
# THE MEMORY BOUND: `ulimit -v 6291456` (6 GB of address space) around
# each step, so an allocation past it raises MemoryError, reported BY
# NAME, rather than the operating system stopping the process.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline

step () {
  echo
  echo "======== [$1/4] $2 ========"
  shift 2
  ( ulimit -v 6291456 ; python3 "$@" )
  echo "-- exit $?"
}

step 1 "the canonical-form corpus (canon39): cost, and the three candidate definitions" t98_probe_shapes.py corpus
step 2 "canon40: the proved population" t98_probe_shapes.py canon40
step 3 "term66_store: the term states" t98_probe_shapes.py terms
step 4 "all three in ONE process -- the cost the pane would actually pay" t98_probe_shapes.py all
