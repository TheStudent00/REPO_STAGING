#!/usr/bin/env bash
# ap2_l12_run.sh -- task ap2: THE LOOP, second pass.  the owner's loop over
# every attested cell of the arch-opcode model table, on the four
# compiled targets, primitive-first, with the six mechanical causes
# task ap1 counted fixed.
#
#   for arch_opcode_i in set_of_unique_arch_opcodes:   # the 253 attested cells
#       for lang_i in {c, rust, go, swift}:
#           emulated_arch_opcode = find_emulation(arch_opcode_i)
#
# 1,012 runs, the same 253 cells in the same order -- most attested
# ledger rows first -- so a lane the wall clock stops has already
# finished the cells that carry most of the corpus.  The twenty runs
# lane `ap2_l11_guards_and_sample.sh` recorded are skipped, and so is
# every run any earlier pass of this lane recorded: the store is one
# json object per line on `autopoly2_runs.jsonl`, flushed as each run
# finishes.
#
# MEMORY BOUND: 6 GB resident on the one collecting process, named
# abort ABORT_MEMORY_AP2, checked after every run.  The sample of
# twenty measured the peak at 261,272 kB -- 4% of the bound -- with
# both heavy reads already done.  Task ap1's own 1,012-run lane ended
# at 2,414,988 kB, and it grows with the run count because the z3
# context accumulates terms; a lane stopped on the bound loses nothing
# and a resumed one starts again at 261 MB.
#
# CEILINGS: the gate of record is the pipeline's own 3,000 ms; every
# UNDECIDED is re-posed ONCE at 30,000 ms and both answers are kept.
set -euo pipefail
mkdir -p /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/src2
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 autopoly2.py run
