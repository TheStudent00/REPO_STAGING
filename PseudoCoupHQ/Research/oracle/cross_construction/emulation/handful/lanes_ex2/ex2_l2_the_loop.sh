#!/usr/bin/env bash
# ex2_l2_the_loop.sh -- task ex2, step 2: THE LOOP, first pass, 60 s per
# run, over the whole outer set: 253 cells x 7 interpreted targets =
# 1,771 runs. Resumable: `expand2.py run` skips every pair already on
# `expand2_runs.jsonl`, so a lane stopped partway loses nothing and a
# re-submission of this same script finishes what is left.
#
# MEMORY: one collecting process, bound 6 GB, named abort
# ABORT_MEMORY_EX2; each runner is a separate short-lived process handed
# the whole sample at once. The smoke lane (ex2_l1) sampled the first 14
# runs' peaks; this lane prints every one of its own.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

echo "[1/1] the loop, no limit: every pair not already recorded"
python3 expand2.py run
echo "done"
