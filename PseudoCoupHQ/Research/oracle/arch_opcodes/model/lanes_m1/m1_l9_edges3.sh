#!/usr/bin/env bash
# m1_l9_edges3.sh -- task m1: the whole equivalence pass, third run.
#
# WHAT CHANGED AND WHY, in order.
#  * m1_l7_edges.sh keyed a cell by (pair, shape, width, seeded?, which
#    flag-setting mnemonic seeded it) and reached 196,190 cells. The seed
#    is a probe choice of the sweep's second pass, not part of the
#    machine form the ruling of 2026-09-08 names, so the key was
#    corrected to (pair, shape, width): 51,730 cells. Lane l7 was stopped
#    (down.sh --force) at cell 1,600 and wrote nothing.
#  * m1_l8_edges2.sh ran that corrected key and measured 8,400 cells in
#    1,635 s: fast at first (0.02 s/cell) and then about 2 s/cell once it
#    reached the x87 group, whose terms are 80-bit floating point and
#    which therefore reach the 3,000 ms ceiling and answer `unknown`. At
#    that rate the pass is about 24 h, past the 21,600 s script_timeout.
#    It was stopped at cell 8,400 and wrote nothing.
#  * This run adds a MEMO on the question itself: the pair of the two
#    terms' s-expressions. z3's answer is a function of the terms, so an
#    identical question is answered once and re-used; nothing is compared
#    less, and meta.solver_calls / meta.solver_memo_hits record both
#    numbers. The 3,000 ms ceiling is unchanged.
#
# MEMORY BOUND: 16g resident, named abort ABORT_MEMORY_M1, checked every
# 200 cells; rebuilt z3 terms held in a 400-row cache.
set -euo pipefail
echo "[1/1] task m1: model_table.py edges (memoized questions)"
cd PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 model_table.py edges
echo "[1/1] done"
