#!/usr/bin/env bash
# ap5_l16_run_the_loop_b.sh -- task ap5: THE LOOP OF RECORD, fifth
# pass, run again after the defect lane `ap5_l15` found in this task's
# own first pass.
#
# WHY THERE IS A SECOND PASS.  Lane `ap5_l8` ran the 1,012 and the
# change table then said `runs task ap4 proved and task ap5 does not:
# 31`, which is the brief's own STOP condition.  Thirty of the 31 were
# `mem_one` 80 cells on c and the counterexamples named the cause
# themselves: `seed_x87__rsi_` free on the cell side beside `IN_0` and
# `IN_1`.  An x87 arrival reaches a row under TWO names -- `X87_<k>`,
# a stack position the model table preseeded, and `x87_<mangled
# operand>`, a literal memory operand read at the x87 sort -- and
# `emulate.X87_ARRIVAL` holds both; the first draft of
# `align_by_row`'s new branch tested only the first, so the second
# arrival of those thirty cells was never put on a row.  The branch
# now tests both (lane `ap5_l15` ran four of the thirty and all four
# prove).
#
# THE FIRST PASS'S STORE IS KEPT.  Nothing under the artifact folder
# is deleted: `autopoly5_runs.jsonl` is RENAMED to
# `autopoly5_runs.jsonl.before_the_x87_memory_arrival_fix` and the
# loop starts from an empty store, so both passes are on disk.
#
# MEMORY BOUND: 6 GB resident on the one collecting process, named
# abort ABORT_MEMORY_AP5, checked after every run.  The first pass
# peaked at 2,909,168 kB over the same 1,012 runs.
set -euo pipefail
A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
cd "$A"
KEPT="$A/autopoly5_runs.jsonl.before_the_x87_memory_arrival_fix"
if [ -f "$A/autopoly5_runs.jsonl" ]; then
  if [ -f "$KEPT" ]; then
    echo "the kept store already exists; nothing is overwritten"
    exit 1
  fi
  mv "$A/autopoly5_runs.jsonl" "$KEPT"
  echo "the first pass's store kept as $(basename "$KEPT"): $(wc -l < "$KEPT") lines"
fi
python3 autopoly5.py run
echo "done"
