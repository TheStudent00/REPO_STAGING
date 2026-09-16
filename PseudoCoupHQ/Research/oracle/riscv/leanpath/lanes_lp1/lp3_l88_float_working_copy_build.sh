#!/bin/bash
# lp3_l88_float_working_copy_build.sh -- THE WORKING COPY of the emit, built as
# its own proof project, with Sail's float axioms given bodies from Kinds.lean.
#
# Its small check ran first (make_working_copy.sh check, by podman exec): the copy,
# the rewrite of 27 axioms, the kinds modules built, and the rewritten
# RiscvExtras.lean checked as one file with no error. This lane builds the WHOLE
# copy: every module that imports RiscvExtras is rebuilt against the bodies.
#
# Never the cache and never /work/proof (another agent's lanes use it): the copy is
# /work/proof_float; /work/proof is only read (its built lean-sail package and its
# built emit are copied after the emit is checked byte-identical to the cache's).
# The set of axioms rewritten is the intersection of two texts (Kinds.Axioms'
# definitions and the emit's axioms of the same name and type), nothing named.
# Fetches nothing. The previous build of this emit took 489 s (lane lp1_l17).
set -uo pipefail
total=1
echo "[1/$total] the working copy, the rewrite, the whole build, and what Lean says the rewritten constants are (make_working_copy.sh prints its own five steps)"
bash PseudoCoupHQ/Research/oracle/riscv/leanpath/float_emit/make_working_copy.sh build
echo done
