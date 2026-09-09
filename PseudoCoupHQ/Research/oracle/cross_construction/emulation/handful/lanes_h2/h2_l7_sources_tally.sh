#!/usr/bin/env bash
# h2_l7_sources_tally.sh -- task h2: `handful2_sources.json` counted,
# and the one place the brief asks about by name.
#
# WHAT IT MEASURES.  Step 1: over every place of the ten cells, how many
# came back with the same rendered source both ways, how many were not
# rendered at all, and how many of the rendered ones are character for
# character the file task h1's own run left under `src/`.  Step 2: the
# `idiv` destination place, both ways side by side -- the length of each
# term text, whether the two texts are identical, and whether the two
# sources are.  Both read the json lane h2_l2 wrote; nothing is
# re-rendered and nothing is written.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_H2; both steps
# read one 74 kB json file.
set -euo pipefail
H=PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
echo "[1/3] task h2: handful2_sources.json, counted"
python3 $H/handful.py sources_counts
echo "[2/3] task h2: the idiv destination place, both ways"
python3 $H/handful.py sources_idiv idiv c reg_rax
echo "[3/3] done"
