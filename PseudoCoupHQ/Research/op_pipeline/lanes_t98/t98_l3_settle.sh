#!/usr/bin/env bash
# t98 lane 3 -- settle the three places where the recount disagreed with
# the figures the task brief carried, and measure the shapes of the
# further computed stats before any of them reaches the page.
#
# THE MEMORY BOUND: `ulimit -v 6291456` (6 GB of address space) around
# each step; an allocation past it raises MemoryError, reported BY NAME.
set -u
cd PseudoCoupHQ/Research/op_pipeline

step () {
  echo
  echo "======== [$1/4] $2 ========"
  shift 2
  ( ulimit -v 6291456 ; python3 "$@" )
  echo "-- exit $?"
}

step 1 "distinct machine code -- the two measurements, and what separates them" t98_settle.py bodies
step 2 "four spellings of 'no instructions at all'" t98_settle.py empty
step 3 "how many arch opcodes a body holds -- the definitions side by side" t98_settle.py opcodes
step 4 "the further computed stats, their shapes" t98_settle.py extras
