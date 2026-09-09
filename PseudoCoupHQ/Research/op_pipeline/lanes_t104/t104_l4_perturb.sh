#!/usr/bin/env bash
# t104 lane 4 -- THE OPERAND-ORDER ACCEPTANCE.
#
# The property the brief's deliverable 2 names, measured directly: the
# order of a commutative operator's operands cannot change the layer-5
# text.  Every proved unit's term is transcribed, a second term is
# built from it by permuting the operands of every commutative node
# (seed 104), and both are normalized.  The property holds for a unit
# when the two texts are the same string.
#
# MEMORY: one shard at a time, two terms per unit; hard cap 6 GB with
# the named abort ABORT_MEMORY_T104.
set -u
cd /projects/PseudoCoupHQ/Research/op_pipeline
echo "[1/1] the perturbation acceptance"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/lanes_t104/t104_perturb.py
echo "exit $?"
