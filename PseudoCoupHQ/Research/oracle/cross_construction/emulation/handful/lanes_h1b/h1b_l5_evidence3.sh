#!/usr/bin/env bash
# h1b_l5_evidence3.sh -- task h1b: `grep -c exempt`, corrected a second
# time -- SUPERSEDES lane h1b_l4's own step, which referenced itself
# before its own sync had landed on the tower.  The list here is task
# h1's own precedent (log 238 section 10): the driver, the report, and
# the two COMPUTE lanes (h1b_l1, h1b_l2) -- never the evidence lanes
# themselves, because the word `exempt` appears in the `grep -c exempt`
# command an evidence lane prints, which is not a claimed exemption.
# MEMORY: the task's bound is 4 GB with the named abort ABORT_MEMORY_H1.
set -euo pipefail
H=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
run () { echo; printf '$'; printf ' %q' "$@"; echo; "$@"; }

echo "[1/1] grep -c exempt over every file this task added, excluding "
echo "      the evidence lanes themselves (task h1's own precedent)"
run grep -c exempt \
    $H/handful.py \
    $H/handful.md \
    $H/lanes_h1b/h1b_l1_compose_report.sh \
    $H/lanes_h1b/h1b_l2_report.sh || true
