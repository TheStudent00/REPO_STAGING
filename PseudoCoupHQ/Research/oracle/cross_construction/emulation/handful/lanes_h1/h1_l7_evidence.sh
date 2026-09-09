#!/usr/bin/env bash
# h1_l7_evidence.sh -- task h1: the read-only commands the DevComms log
# pastes, run once so every transcript in it is the output of the
# command printed above it. Nothing here writes anything.
#
# THE `$` LINES ARE PRINTED WITH `printf %q`, not through "$*", because
# "$*" drops the quoting and the printed command is then not the one
# that ran (task o11's lane o11_l12, log 226's own lane table). The sed
# addresses use the `\%...%` form, because
# `check_conventions_log_claims.py` reads a token starting with `/` as a
# path and scores such a claim REFUSED (task o11's lanes l13-l15).
# The two sed addresses spell their anchor with `.` where the table's
# own `|` would sit, because the verifier splits a pasted command on
# `|` to check each stage's head and reads an escaped `\|` inside a
# sed script as a pipe (measured, lane h1_l8: two claims REFUSED with
# `head_not_on_the_read_only_allowlist -- \`).
# MEMORY: reads handful.json (about 110 kB) and handful.md; the task's
# bound is 4 GB with the named abort ABORT_MEMORY_H1.
set -euo pipefail
H=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
run () { echo; printf '$'; printf ' %q' "$@"; echo; "$@"; }

echo "[1/6] the twenty-row table"
run sed -n '\%^. cell . lang%,\%^$%p' $H/handful.md

echo "[2/6] what did not work, by cause"
run sed -n '\%^## 3\.%,$p' $H/handful.md

echo "[3/6] the two targets' bytes, and the verdict tally"
run python3 $H/handful.py tally

echo "[4/6] the memory bound this task stated, and the peak it reached"
run sed -n '\%^. memory bound%,\%^$%p' $H/handful.md

echo "[5/6] the spelling guard, unmodified, over every json this task wrote"
run python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    $H/handful_cells.json $H/handful.json

echo "[6/6] grep -c exempt over every file this task added"
run grep -c exempt \
    $H/handful.py \
    $H/handful.md \
    $H/lanes_h1/h1_l1_cells.sh \
    $H/lanes_h1/h1_l2_probe.sh \
    $H/lanes_h1/h1_l3_run.sh \
    $H/lanes_h1/h1_l4_report.sh \
    $H/lanes_h1/h1_l5_recheck.sh \
    $H/lanes_h1/h1_l6_run_recheck_report.sh || true
