#!/usr/bin/env bash
# g1b_l7_whynot.sh -- task g1b, section 3: why the widened lookup reaches
# `idiv gpr_one 32` in c and in NO other target.
#
# WHY THIS LANE EXISTS.  Task g1b's brief expects the widened rule to
# move `idiv` on c, rust and go.  Lane `g1b_l6_changes.sh` measured that
# it moves ONE pair, c's, and the honest next step is to print the
# language's own rows rather than to guess at rust's and go's silence.
# `whynot3c` walks every single-opcode row of task o2's TWO lists whose
# body carries the cell's own arch mnemonic at all, and prints for each:
# the body, the narrow strip, the setup split section 2e makes, and what
# task m1b's classifier says the non-setup part is -- so a row that is
# not accepted carries the reason it is not.
#
# THE MNEMONIC IS MACHINE FORM: it is the cell's own `mnem`, the key the
# ruling of 2026-09-08 states.  No operator token enters the walk.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_G1C.  One read
# of `single_opcode_units.json` (1.6 MB) per rule list, cached.
set -euo pipefail
H=PseudoCoupHQ/Research/oracle/cross_construction/emulation
echo "[1/1] task g1b: handful.py whynot3c idiv gpr_one 32"
python3 $H/handful/handful.py whynot3c idiv gpr_one 32
