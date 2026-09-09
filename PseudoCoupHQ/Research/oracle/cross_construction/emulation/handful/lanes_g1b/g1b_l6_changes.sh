#!/usr/bin/env bash
# g1b_l6_changes.sh -- task g1b, section 3, first step: WHICH (cell,
# target) pairs the widened primitive lookup changes, and what row each
# becomes.  Nothing is rendered, compiled or proved here; this is the
# set `run3c` will run, printed before it runs.
#
# WHAT THE WIDENED RULE IS, in one sentence: a single-opcode row is
# accepted for a cell when its NARROW-stripped body is the cell's own
# instruction plus zero or more ZERO-OPERAND setup instructions from
# `reference.SPREAD_SIGN` / `reference.ACCUMULATOR_WIDEN`, and nothing
# else -- which is what a divide looks like in every one of the four
# targets (`cltd; idiv`, `cqto; idiv`).  Section 2e of `handful.py`
# states it in full and states its reason from what task g1 measured.
#
# BOTH LOOKUPS RUN FOR EVERY PAIR and the two answers are compared, so
# "which pairs change" is a measurement and not an assertion.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_G1C.  The one
# read is `single_opcode_units.json` (1.6 MB), now read under both of
# task o2's rule lists, plus one `probe_manifest_<lang>.json` per
# target; task g1's own lookup step peaked at 82,744 kB.
set -euo pipefail
H=PseudoCoupHQ/Research/oracle/cross_construction/emulation
echo "[1/1] task g1b: handful.py changes3c"
python3 $H/handful/handful.py changes3c
