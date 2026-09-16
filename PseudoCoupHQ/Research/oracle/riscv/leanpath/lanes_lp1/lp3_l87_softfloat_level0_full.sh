#!/bin/bash
# lp3_l87_softfloat_level0_full.sh -- LEVEL 0 for the 27 bodies Kinds.lean gives
# Sail's float axioms: the full comparison, after its gate was read twice (first
# 42 disagreements in two causes, both ours, fixed in Kinds.lean; then 16,875 of
# 16,875 agree). Every operation with a body, every rounding mode, result bits
# AND the five flag bits, against Sail's own softfloat: the compiled
# riscv_softfloat object the model's simulator links, over Berkeley SoftFloat 3
# with the RISCV specialization, its sources byte-identical to the emit's model
# commit 6266b40c (checked again in step 1 of run_level0.sh).
#
# The points: every ordered pair over 38 edge values per format (both zeros, both
# infinities, quiet and signalling NaNs with payloads, the extreme subnormals and
# normals, 1 and its neighbours, the halfway cases of the sum, the product, the
# subnormal quantum and overflow, and the tininess boundary), then 1,000 random
# pairs per operation and mode (uniform bits, close exponents, subnormals,
# exponents at overflow and underflow, sums built to tie). About 183,000 points.
#
# Nothing is selected by an operator token: the operations are the definitions of
# Kinds.Axioms whose type is their Sail axiom's type and which Sail's own
# softfloat_interface.sail binds to a C++ function. Writes /work/sf_level0_full
# and softfloat_level0/level0_softfloat.{json,md}. Fetches nothing.
set -uo pipefail
total=1
echo "[1/$total] the full comparison (run_level0.sh prints its own seven steps)"
bash PseudoCoupHQ/Research/oracle/riscv/leanpath/softfloat_level0/run_level0.sh full /work/sf_level0_full level0_softfloat
echo done
