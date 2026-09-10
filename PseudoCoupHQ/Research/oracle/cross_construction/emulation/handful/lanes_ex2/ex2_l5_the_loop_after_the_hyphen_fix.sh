#!/usr/bin/env bash
# ex2_l5_the_loop_after_the_hyphen_fix.sh -- task ex2, step 5: THE LOOP,
# RESUMED, after `interp_check.one_run`'s label sanitisation gained the
# hyphen alongside the dot. The one cell whose destination place name
# carries a hyphen (`push` gpr_one 64, writes `stack_-8`) produced a
# syntax error on six targets and, on csharp, the same reused-project-
# folder stale-binary masking task ex2's earlier dotted-label fix (lane
# ex2_l4) already found and fixed for a different character. The seven
# (cell, target) records this bug produced were purged from
# `expand2_runs.jsonl` (kept beside as
# `expand2_runs.jsonl.before_the_hyphen_label_fix`); this lane re-runs
# exactly those seven, resuming by skipping the rest.
#
# MEMORY: one collecting process, bound 6 GB, named abort
# ABORT_MEMORY_EX2.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

echo "[1/1] the loop, resumed: every pair not already recorded"
python3 expand2.py run
echo "done"
