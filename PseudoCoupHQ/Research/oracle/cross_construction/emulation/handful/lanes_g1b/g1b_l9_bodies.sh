#!/usr/bin/env bash
# g1b_l9_bodies.sh -- task g1b, section 3: what the CORPUS holds at the
# arch mnemonic the widened lookup reaches in c and in no other target.
#
# WHY THIS LANE EXISTS.  Lane `g1b_l7_whynot.sh` answered "no row of
# task o2's single-opcode lists carries this mnemonic" for rust, go and
# swift -- a fact about the LISTS.  The question underneath it is
# whether those languages' corpora carry the instruction at all, and in
# what shape.  `bodies3c` answers that from `canon40_wrapped_<lang>.json`,
# the corpus itself: how many units carry the mnemonic, and the shortest
# and longest such body printed instruction by instruction.
#
# THE SELECTION IS MACHINE FORM: a unit is taken when an instruction of
# its body carries this arch mnemonic, which is the cell's own `mnem`.
# The operator each unit displays is printed beside its body as the
# display label it is, and selects nothing.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_G1C, checked
# after every language.  The four files are 4.9 MB (c), 0.9 MB (go),
# 0.8 MB (rust) and 1.2 MB (swift), read ONE AT A TIME and dropped.
set -euo pipefail
H=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation
echo "[1/1] task g1b: handful.py bodies3c idiv"
python3 $H/handful/handful.py bodies3c idiv
