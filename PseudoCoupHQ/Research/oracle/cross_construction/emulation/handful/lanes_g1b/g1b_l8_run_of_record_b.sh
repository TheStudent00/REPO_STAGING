#!/usr/bin/env bash
# g1b_l8_run_of_record_b.sh -- task g1b, section 2: THE SECOND RUN OF
# RECORD.  The same forty runs task g1 ran, on the rebuilt image and
# with `sandbox-persist` mounted read-only, so a swift compiler is
# reachable at last; then every UNDECIDED gate call re-posed at
# 300,000 ms, then the composition column, the report and the spelling
# tables -- ONE lane, so `handful3b.json` is written end to end by one
# version of the program (task h1's own section 7.1 lesson, kept).
#
# WHY ALL FORTY AND NOT THE TEN SWIFT ROWS ALONE.  The brief asks for
# the ten swift rows and for the answer "in the same 40-row shape beside
# g1's".  Running all forty gives that shape from ONE run rather than by
# stitching thirty of task g1's rows to ten of this task's, and it makes
# the thirty non-swift rows a CHECK: the machine changed under them, and
# `handful3b.md`'s section 4 puts task g1's verdict for every pair beside
# this run's, so a row that moved and a row that did not are both on the
# page.  Task g1's own `handful3.json` / `handful3.md` are not written
# by this lane; these products sit beside them and the rendered sources
# go to `src3b/` beside `src3/`.
#
# NOT ONE THING ABOUT THE ROUTE IS DIFFERENT.  `use_task_g1b` changes
# the product paths and the named abort and nothing else; the lookup is
# still task o2's narrow rows, the renderers are unchanged, task h2's
# two printing fixes are still on, and the solver ceiling is still the
# pipeline's own 3,000 ms with the re-pose at 300,000 ms as the law's
# time-limit-is-a-flag rule requires.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_G1B, checked
# after every run and every re-pose.  Task g1's identical run peaked at
# 466,868 kB on the forty runs, 439,916 kB on the re-poses and
# 257,372 kB on the composition step.
set -euo pipefail
H=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation
echo "[1/6] task g1b: handful.py primitive3b"
python3 $H/handful/handful.py primitive3b
echo "[2/6] task g1b: handful.py run3b"
python3 $H/handful/handful.py run3b
echo "[3/6] task g1b: handful.py recheck3b 300000"
python3 $H/handful/handful.py recheck3b 300000
echo "[4/6] task g1b: handful.py compose3b"
python3 $H/handful/handful.py compose3b
echo "[5/6] task g1b: handful.py report3b"
python3 $H/handful/handful.py report3b
echo "[6/6] task g1b: handful.py spellings3b"
python3 $H/handful/handful.py spellings3b
