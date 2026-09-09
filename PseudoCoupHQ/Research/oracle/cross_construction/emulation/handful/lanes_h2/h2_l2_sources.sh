#!/usr/bin/env bash
# h2_l2_sources.sh -- task h2, fix 1's own regression guard: every place
# of the ten cells rendered BOTH ways -- the term task h1 handed the
# renderer, and the normalised term task h2 hands it -- with the two
# sources compared character for character, the h1-way source compared
# against the file task h1's own run wrote under `src/`, and, where the
# two sources differ, the two terms put to the gate.
#
# THE BRIEF'S OWN WORDING is "the other eight cells' rendered sources
# must be unchanged or provably equal (z3, both terms)"; this lane is
# that measurement, over every cell and every place rather than only the
# eight, so nothing is chosen after the fact.  Nothing is rendered into
# `src2/` here.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_H2, checked
# after every cell.
set -euo pipefail
echo "[1/2] task h2: handful.py sources2"
python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py sources2
echo "[2/2] done"
