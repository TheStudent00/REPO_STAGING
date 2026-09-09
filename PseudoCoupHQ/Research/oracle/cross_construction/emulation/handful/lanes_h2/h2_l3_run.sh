#!/usr/bin/env bash
# h2_l3_run.sh -- task h2: the twenty runs after the two printing fixes,
# the re-pose of every gate call the 3,000 ms ceiling leaves UNDECIDED,
# the composition column over this task's own carved bodies, and the
# report -- in ONE lane, so `handful2.json` is written end to end by one
# version of the program (task h1's own section 7.1 lesson).
#
# WHAT IS DIFFERENT FROM TASK h1's OWN RUN, and nothing else is: the
# term the renderer is handed is the one the pipeline's own normaliser
# leaves (fix 1), and a vector cell's place is projected to the lane the
# cell's own key_width names before it is rendered (fix 2).  The same
# ten cells, the same two renderers unchanged, the same ship flags, the
# same gate and the same 3,000 ms ceiling.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_H2, checked
# after every run and every re-pose.  Task h1's own run of the same
# twenty peaked at 405,812 kB.
set -euo pipefail
echo "[1/5] task h2: handful.py run2"
python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py run2
echo "[2/5] task h2: handful.py recheck2 300000"
python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py recheck2 300000
echo "[3/5] task h2: handful.py compose2"
python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py compose2
echo "[4/5] task h2: handful.py report2"
python3 PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py report2
echo "[5/5] done"
