#!/usr/bin/env bash
# ap3_l10_measure_fix2_again.sh -- task ap3: FIX 2 measured again on its
# 128 pairs, after the ONE defect lane `ap3_l8` found in this task's own
# new code.
#
# WHAT `ap3_l8` FOUND, and it was in the measurement's own code path and
# not in the fix's idea: two of the 128 pairs -- `fucomi` and `fucomip`
# on c -- raised `KeyError: 79` out of the driver.  An x87 COMPARE's
# flags place is the two operands' BITS concatenated, so the term
# reaches `fp.to_ieee_bv` on an x87 value inside itself, and
# `Renderer.helper_text` went looking for an unsigned holder 79 bits
# wide to memcpy into.  There is none, and there must not be one: c's
# `long double` and z3's `FPSort(15, 64)` differ by the explicit
# integer bit.  The node is now REFUSED BY CAUSE at that width.
#
# WHAT `ap3_l9` FOUND, and it is not this task's to fix: the c body of
# an x87 cell renders, compiles and carves to the x87 opcode -- and the
# CANONICAL FORM then refuses it, `no answer home`: "this unit's own
# code names no register the answer is left in".  A `long double`
# answer is left in st(0) and its arguments arrive on the stack, and
# neither is a register family, which is the arrival-contract question
# already awaiting the owner.  Flagged, not worked around.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 autopoly3.py measure 'no setter row to compose'
echo "done"
