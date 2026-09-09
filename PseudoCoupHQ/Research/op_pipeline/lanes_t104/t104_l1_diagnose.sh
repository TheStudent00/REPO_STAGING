#!/usr/bin/env bash
# t104 lane 1 -- DIAGNOSIS, no change to anything.
#
# The brief's gap: log_224 section 4 shows two pool5 entries whose
# layer-5 texts differ only in which side of an `==` the bare symbol
# sits on, and the CORE of the normalize node already rules that the
# arguments of every commutative operator are put in a fixed order.
# So either the ordering step is not reached for these units, or its
# key ties.  This lane answers WHICH, by printing, for the six units
# log_224 names, the layer-4 term, the ordering key of each argument of
# every commutative node, and the text the normalizer prints today.
#
# It also prints the table of commutative declaration kinds FROM z3's
# own opcode enumeration, so the report's list is read off the table
# and not off memory.
#
# Reads only; writes t104_diagnose.json under the artifact folder.
set -u
cd PseudoCoupHQ/Research/op_pipeline
echo "[1/3] the opcode table, from z3's own enumeration"
python3 PseudoCoupHQ/Research/op_pipeline/lanes_t104/t104_diagnose.py table
echo "[2/3] the six units log_224 names"
python3 PseudoCoupHQ/Research/op_pipeline/lanes_t104/t104_diagnose.py units
echo "[3/3] done"
ls -la t104_diagnose.json
