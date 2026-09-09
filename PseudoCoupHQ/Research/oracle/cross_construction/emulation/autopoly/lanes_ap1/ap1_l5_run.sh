#!/usr/bin/env bash
# ap1_l5_run.sh -- task ap1: THE LOOP. the owner's loop over every attested
# cell of the arch-opcode model table, on the four compiled targets,
# primitive-first.
#
#   for arch_opcode_i in set_of_unique_arch_opcodes:   # the 253 attested cells
#       for lang_i in {c, rust, go, swift}:
#           emulated_arch_opcode = find_emulation(arch_opcode_i)
#
# 1,012 runs. The route is `handful.py` as task g1b left it; this lane
# runs the loop around it and nothing else. The twenty runs lane
# `ap1_l2_preflight_sample.sh` already recorded are skipped, and so is
# every run any earlier pass of this lane recorded -- the store is one
# json object per line on `autopoly_runs.jsonl`, flushed as each run
# finishes, so a lane the wall clock stops loses nothing and the next
# pass resumes where it stopped.
#
# MEMORY BOUND: 6 GB resident on the one collecting process, named
# abort ABORT_MEMORY_AP1, checked after every run. The sample measured
# the peak at 260,016 kB -- 4% of the bound -- with the whole of
# `model_table_rows.json` already read.
#
# CEILINGS: the gate of record is the pipeline's own 3,000 ms; every
# UNDECIDED is re-posed ONCE at 30,000 ms and both answers are kept.
set -euo pipefail
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 autopoly.py run
