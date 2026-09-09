#!/usr/bin/env bash
# t83 lane 5 -- WHICH attached callee bodies can be walked at all.
# One forked child per body, each bounded at 4 GB of address space and
# 120 s, so a runaway body is named instead of killing the run.
set -u
cd PseudoCoupHQ/Research/op_pipeline
python3 probe83e_callee_bodies.py
echo "exit $?"
