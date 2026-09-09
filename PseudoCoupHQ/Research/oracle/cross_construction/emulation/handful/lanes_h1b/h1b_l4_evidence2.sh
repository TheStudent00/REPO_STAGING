#!/usr/bin/env bash
# h1b_l4_evidence2.sh -- task h1b: lane h1b_l3's own `grep -c exempt`
# step named `lanes_h1b/h1b_l2_report.sh` before the whole `handful/`
# folder (lanes_h1b/ included) had been synced to the tower, so grep
# could not find it -- SUPERSEDED for that one step only; every other
# transcript in h1b_l3_evidence.sh's log stands and is not re-run here.
# MEMORY: the task's bound is 4 GB with the named abort ABORT_MEMORY_H1.
set -euo pipefail
H=PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
run () { echo; printf '$'; printf ' %q' "$@"; echo; "$@"; }

echo "[1/1] grep -c exempt over every file this task added"
run grep -c exempt \
    $H/handful.py \
    $H/handful.md \
    $H/lanes_h1b/h1b_l1_compose_report.sh \
    $H/lanes_h1b/h1b_l2_report.sh \
    $H/lanes_h1b/h1b_l3_evidence.sh \
    $H/lanes_h1b/h1b_l4_evidence2.sh || true
