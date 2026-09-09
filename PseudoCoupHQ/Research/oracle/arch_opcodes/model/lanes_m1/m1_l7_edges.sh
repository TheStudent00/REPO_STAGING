#!/usr/bin/env bash
# m1_l7_edges.sh -- task m1: the whole equivalence pass. The
# identical_text classes over every TRANSLATED row, then z3's two
# verdicts (destination, flags) at a 3,000 ms ceiling for every
# (same-builder pair, shape, width) cell, then the same for the one pair
# the brief names. Writes model_table_edges.json.
# MEMORY BOUND: 16g resident, named abort ABORT_MEMORY_M1, checked every
# 200 cells; the rebuilt z3 terms are held in a 400-row cache
# (TERM_CACHE_CEILING) rather than all at once, because the 400-cell
# sample lane measured about 0.7 MB resident per row held.
# TIME: the 400-cell sample ran 400 cells in 59 s (0.15 s/cell).
set -euo pipefail
echo "[1/1] task m1: model_table.py edges"
cd /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 model_table.py edges
echo "[1/1] done"
