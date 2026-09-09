#!/usr/bin/env bash
# ap3_l11_run_the_loop.sh -- task ap3: THE LOOP, third pass, with task
# h2's normalise-before-render ON (the setting of record).
#
#   for arch_opcode_i in set_of_unique_arch_opcodes:   # the 253 attested cells
#       for lang_i in {c, rust, go, swift}:
#           emulated_arch_opcode = find_emulation(arch_opcode_i)
#
# 1,012 runs, the same 253 cells in the same order -- most attested
# ledger rows first.  The store is one json object per line on
# `autopoly3_runs.jsonl`, flushed as each run finishes, so a lane the
# wall clock stops loses nothing and a resumed one skips what is done.
#
# THE STORE IS STARTED AGAIN, and nothing is removed.  The 20 sample
# lines lane `ap3_l7` wrote were run before the `KeyError: 79` lane
# `ap3_l8` found was refused by cause, so they are moved aside to
# `autopoly3_runs.jsonl.before_the_x87_bits_refusal` and the loop of
# record begins on an empty store.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP3, checked
# after every run.  The sample of twenty measured the peak at 261,712
# kB -- 4% of the bound -- with both heavy reads already done; task
# ap2's own 1,012-run lane ended at 1,450,280 kB.
#
# CEILINGS: the gate of record is the pipeline's own 3,000 ms; every
# UNDECIDED is re-posed ONCE at 30,000 ms and both answers are kept.
set -euo pipefail
ART=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
mkdir -p "$ART/src3"
if [ -f "$ART/autopoly3_runs.jsonl" ]; then
  mv "$ART/autopoly3_runs.jsonl" \
     "$ART/autopoly3_runs.jsonl.before_the_x87_bits_refusal"
  echo "the earlier store moved aside: $(wc -l < "$ART/autopoly3_runs.jsonl.before_the_x87_bits_refusal") line(s)"
fi
cd "$ART"
python3 autopoly3.py run
