#!/usr/bin/env bash
# h2_l9_evidence.sh -- task h2: the read-only commands log 240 pastes,
# run once so every transcript in it is the output of the command
# printed above it. Nothing here writes anything.
#
# THE SHAPE IS TASK h1's OWN (`lanes_h1/h1_l9_evidence2.sh`), copied
# rather than reinvented, including its two hard-won details:
#   * the `$` lines are printed with `printf %q`, not through "$*",
#     because "$*" drops the quoting and the printed command is then not
#     the one that ran (task o11's lane o11_l12);
#   * the `sed` addresses use the `\%...%` form and spell `.` where the
#     table's own `|` sits, because the verifier reads a token starting
#     with `/` as a path and splits a pasted command on `|` to check
#     each stage's head (task h1's own log 238 ADDENDUM).
# `|| true` sits on the two steps whose own exit is a result rather than
# a failure: the guard over task o8's inherited artifact, and `grep -c`,
# which answers 1 when a count it prints is zero.
#
# MEMORY: reads json files of a few hundred kB; the task's bound is
# 4 GB with the named abort ABORT_MEMORY_H2.
set -euo pipefail
H=PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
P=PseudoCoupHQ/Research/oracle/cross_construction/emulation/per_opcode
run () { echo; printf '$'; printf ' %q' "$@"; echo; "$@"; }

echo "[1/10] change 3: what the zero-operand width rule reads and answers"
run python3 $H/classifier_probe.py

echo "[2/10] change 3: task h1b's composition re-derived over task h1's own twenty bodies"
run python3 $H/handful.py reclassify

echo "[3/10] fix 1: handful2_sources.json, counted"
run python3 $H/handful.py sources_counts

echo "[4/10] fix 1: the idiv destination place, both ways"
run python3 $H/handful.py sources_idiv idiv c reg_rax

echo "[5/10] the twenty-row table"
run sed -n '\%^. cell . lang . h1 verdict%,\%^$%p' $H/handful2.md

echo "[6/10] what did not work, by cause"
run sed -n '\%^### 3.1 Refusals%,\%^### 3.2%p' $H/handful2.md

echo "[7/10] the two targets' bytes, the verdict tally, the composition tally"
run python3 $H/handful.py tally2

echo "[8/10] the regression: task o8's four totals off the scratch copy"
run python3 $H/o8_regression.py totals

echo "[9/10] the spelling guard, unmodified: this task's own three json, then task o8's inherited pair"
run python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    $H/handful2.json $H/handful2_sources.json $H/handful2_classifier.json
run python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    $P/per_opcode_results.json $H/o8_regression/per_opcode_results.json || true

echo "[10/10] grep -c exempt over every file this task added"
run grep -c exempt \
    $H/handful.py \
    $H/o8_regression.py \
    $H/classifier_probe.py \
    $H/handful2.md \
    $H/lanes_h2/h2_l1_classifier.sh \
    $H/lanes_h2/h2_l2_sources.sh \
    $H/lanes_h2/h2_l3_run.sh \
    $H/lanes_h2/h2_l4_o8_regression.sh \
    PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.py || true
