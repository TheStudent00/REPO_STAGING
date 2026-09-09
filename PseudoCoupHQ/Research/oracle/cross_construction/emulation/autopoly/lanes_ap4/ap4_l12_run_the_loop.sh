#!/usr/bin/env bash
# ap4_l12_run_the_loop.sh -- task ap4: THE LOOP, fourth pass.
#
# The same 1,012 (cell, target) pairs task ap3 ran, in the same order --
# most attested ledger rows first -- through the driver as task ap4
# leaves it.  One line of `autopoly4_runs.jsonl` per finished run,
# flushed before the next begins, so a lane the wall clock stops loses
# nothing and a re-submitted lane resumes.
#
# MEMORY BOUND: 6 GB resident on the one collecting process, named
# abort ABORT_MEMORY_AP4, checked after every run.  Task ap3's own loop
# peaked at 2,419,276 kB over the same run count.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 autopoly4.py run
echo "done"
