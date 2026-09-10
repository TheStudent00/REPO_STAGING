#!/usr/bin/env bash
# ex2_l8_reaggregate_after_hyphen_fix.sh -- task ex2, FINAL re-run of the
# aggregate + report + six deliverable commands, after
# `ex2_l5_the_loop_after_the_hyphen_fix.sh` purged and re-ran the seven
# (cell, target) records the hyphen in `push gpr_one 64`'s destination
# (`stack_-8`) broke the same way the dot did (lane ex2_l6's note).
# `ex2_l6_reaggregate_after_label_fix.sh` ran BEFORE the hyphen fix and
# is therefore stale (its one reported disagreement, `push` gpr_one 64
# -> csharp, IS the hyphen bug, not a real value-model difference). This
# lane repeats l4/l6's content once more, under a new name for the same
# LAW reason, over the now fully-corrected store. `interp_check.py`'s
# comment (git c89e4f79) states both bad characters (dot, hyphen) were
# found by scanning every `writes` string this loop met, character by
# character, over the whole 253-cell outer set -- so this is expected to
# be the last such fix.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_EX2.
set -euo pipefail
A=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
cd "$A"

echo "[1/7] the aggregate: expand2_runs.jsonl + retry600 -> expand2.json"
python3 expand2.py aggregate

echo ""
echo "[2/7] the report: expand2.md"
python3 expand2.py report

echo ""
echo "[3/7] deliverable 1 -- the per-target table"
python3 expand2.py tables

echo ""
echo "[4/7] deliverable 2 -- all seven, all twelve"
python3 expand2.py all_seven

echo ""
echo "[5/7] deliverable 3 -- every disagreement"
python3 expand2.py disagreements

echo ""
echo "[6/7] deliverable 4 -- declines by target and word"
python3 expand2.py declines

echo ""
echo "[7/7] deliverable 5 -- refusals by cause, and deliverable 6 -- the handful's seventy"
python3 expand2.py refusals
python3 expand2.py handful_check
echo "done"
