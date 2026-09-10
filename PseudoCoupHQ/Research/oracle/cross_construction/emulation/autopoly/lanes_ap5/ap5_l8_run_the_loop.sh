#!/usr/bin/env bash
# ap5_l8_run_the_loop.sh -- task ap5: THE LOOP, fifth pass.  253 cells
# times four targets, 1,012 runs, exactly task ap4's loop over exactly
# task ap4's outer set, with the two changes of this task in the layers
# that own them.  One line on `autopoly5_runs.jsonl` per finished run,
# flushed as it finishes, so a stopped lane loses nothing and a re-run
# resumes.
#
# MEMORY BOUND: 6 GB resident on the one collecting process, named
# abort ABORT_MEMORY_AP5, checked after every run.  Task ap4's own loop
# over the same 1,012 runs peaked at 2,427,092 kB.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 autopoly5.py run
echo "done"
