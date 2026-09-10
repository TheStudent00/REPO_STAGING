#!/usr/bin/env bash
# ex2_l4_the_loop_after_the_label_fix.sh -- task ex2, step 4: THE LOOP,
# RESUMED, after `interp_check.one_run`'s label gained the same dot
# sanitisation `handful.one_place` (the compiled route) already carries.
# The first pass's 196 (cell, target) pairs whose destination place name
# carried a dot -- `flags.low`, `reg_xmm0.low` -- were purged from
# `expand2_runs.jsonl` (kept beside as
# `expand2_runs.jsonl.before_the_dotted_label_fix`) because their
# records were wrong: a compile error on six targets, and on csharp a
# STALE dll from an earlier successful build in the same reused project
# folder, silently executed in its place. This lane re-runs exactly
# those 196, resuming by skipping the 1,575 the first pass already got
# right.
#
# MEMORY: one collecting process, bound 6 GB, named abort
# ABORT_MEMORY_EX2.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

echo "[1/1] the loop, resumed: every pair not already recorded"
python3 expand2.py run
echo "done"
