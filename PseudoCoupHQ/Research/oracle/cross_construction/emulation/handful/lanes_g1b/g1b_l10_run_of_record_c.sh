#!/usr/bin/env bash
# g1b_l10_run_of_record_c.sh -- task g1b, section 3: THE WIDENED
# LOOKUP'S OWN RUN.  The lookup under the widened rule over all forty
# pairs, then the runs of ONLY the pairs whose route it changes, then
# every UNDECIDED gate call re-posed at 300,000 ms, the composition
# column and the report -- ONE lane, so `handful3c.json` is written end
# to end by one version of the program.
#
# WHAT THE WIDENED RULE IS: section 2e of `handful.py`, in one sentence
# -- a single-opcode row is accepted for a cell when its NARROW-stripped
# body is the cell's own instruction plus zero or more ZERO-OPERAND
# setup instructions from `reference.SPREAD_SIGN` /
# `reference.ACCUMULATOR_WIDEN`, and nothing else.  `route` is recorded
# as `primitive+setup` where the accepted row carries setup and stays
# `primitive` where it carries none.
#
# WHICH PAIRS RUN: the ones `route_changes` measures, by running BOTH
# lookups for every pair and comparing the two answers.  Lane
# `g1b_l6_changes.sh` measured that set at ONE pair; this lane recomputes
# it rather than trusting that number, and prints it before running.
#
# Task g1's and task g1b's products are not written by this lane; these
# sit beside them and the rendered sources go to `src3c/`.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_G1C, checked
# after every run and every re-pose.  The heaviest read is
# `model_table_rows.json` (50 MB) in the composition step, measured at
# 257,372 kB by task g1's identical step.
set -euo pipefail
H=PseudoCoupHQ/Research/oracle/cross_construction/emulation
echo "[1/5] task g1b: handful.py primitive3c"
python3 $H/handful/handful.py primitive3c
echo "[2/5] task g1b: handful.py run3c"
python3 $H/handful/handful.py run3c
echo "[3/5] task g1b: handful.py recheck3c 300000"
python3 $H/handful/handful.py recheck3c 300000
echo "[4/5] task g1b: handful.py compose3c"
python3 $H/handful/handful.py compose3c
echo "[5/5] task g1b: handful.py report3c"
python3 $H/handful/handful.py report3c
