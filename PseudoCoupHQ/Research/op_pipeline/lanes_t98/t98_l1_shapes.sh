#!/usr/bin/env bash
# t98 lane 1 -- what a render-time walk of each artifact family COSTS,
# and which definition of "how many arch opcodes a body holds"
# reproduces the figures the task brief measured.
#
# Nothing is written.  Every family is read once, reduced to counters,
# and the parsed document dropped -- so the peak resident size printed
# here is the honest cost of the same walk inside the dashboard.
#
# THE MEMORY BOUND: `ulimit -v 6291456` (6 GB of address space) around
# each step, so an allocation past it raises MemoryError, which python
# reports BY NAME rather than the operating system stopping the process
# without a language-level error.
set -u
cd PseudoCoupHQ/Research/op_pipeline

step () {
  echo
  echo "======== [$1/4] $2 ========"
  shift 2
  ( ulimit -v 6291456 ; /usr/bin/time -v python3 "$@" ) 2>&1 \
    | grep -v '^\s*$'
  echo "-- step done"
}

step 1 "the canonical-form corpus (canon39): cost, and the three candidate definitions" t98_probe_shapes.py corpus
step 2 "canon40: the proved population" t98_probe_shapes.py canon40
step 3 "term66_store: the term states" t98_probe_shapes.py terms
step 4 "all three in ONE process -- the cost the pane would actually pay" t98_probe_shapes.py all

echo
echo "======== the artifacts this lane read ========"
ls -la canon39_wrapped_*.json canon39_interp.json
du -sh canon39_regen_store canon40_regen_store term66_store
echo "shard counts:"
ls canon39_regen_store/*.json | wc -l
ls canon40_regen_store/*.json | wc -l
ls term66_store/*.json | wc -l
