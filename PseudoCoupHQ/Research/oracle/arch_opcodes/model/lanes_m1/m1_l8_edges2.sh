#!/usr/bin/env bash
# m1_l8_edges2.sh -- task m1: the whole equivalence pass, re-run after
# the cell key was corrected.
#
# WHAT CHANGED AND WHY. Lane m1_l7_edges.sh keyed a same-builder cell by
# (pair, shape, width, whether the sweep's second pass seeded the state,
# which flag-setting mnemonic it seeded it with) and reached 196,190
# cells, which at the sample lane's measured 0.15 s/cell is about 8.2 h
# -- past this instance's 21,600 s script_timeout. The seed is a probe
# choice of the sweep's second pass, not part of the machine form: the
# ruling of 2026-09-08 keys a mapping by (mnemonic, operand form,
# width). So the cell is now keyed by that triple, one attempt per
# triple, first in sweep order; both counts are recorded in
# model_table_edges.json's meta. Lane l7 was stopped (down.sh --force)
# and wrote nothing.
#
# MEMORY BOUND: 16g resident, named abort ABORT_MEMORY_M1, checked every
# 200 cells; rebuilt z3 terms held in a 400-row cache.
set -euo pipefail
echo "[1/1] task m1: model_table.py edges (triple-keyed cells)"
cd PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 model_table.py edges
echo "[1/1] done"
