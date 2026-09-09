#!/usr/bin/env bash
# h2_l5_report_evidence.sh -- task h2: `handful.py report2` re-run after
# one rendering fix in the report writer, then every transcript log 240
# pastes, the unmodified spelling guard over every json this task wrote,
# and `grep -c exempt` over every file it added.
#
# WHY THE REPORT IS RE-RUN HERE: task h1's four refused runs have no
# gate verdict, so the `h1 verdict` column of the twenty-row table read
# as an empty cell rather than as their own cause word. The fix is in
# `handful.table_row`'s h2 branch (the report WRITER), not in the data:
# `handful2.json` is not re-run and is not rewritten by this lane.
#
# THE `sed` ADDRESSES SPELL `.` WHERE THE TABLE'S `|` SITS: the
# conventions verifier splits a pasted command on `|` to check each
# stage's head, and an escaped `\|` inside a sed script reads to it as a
# pipe (task h1's own log 238 ADDENDUM, same fix).
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_H2; every step
# here reads json files of a few hundred kB.
set -euo pipefail
H=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
echo "[1/7] task h2: handful.py report2, after the report writer's fix"
python3 $H/handful.py report2
echo "[2/7] task h2: the twenty-row table"
sed -n '\%^. cell . lang . h1 verdict%,\%^$%p' $H/handful2.md
echo "[3/7] task h2: what the two fixes changed, run by run"
sed -n '\%^### 4.1 Fix 1%,\%^### 4.2%p' $H/handful2.md
echo "[4/7] task h2: the tally over handful2.json"
python3 $H/handful.py tally2
echo "[5/7] task h2: task o8's four totals, off the scratch copy"
python3 $H/o8_regression.py totals
echo "[6/7] task h2: the unmodified spelling guard over every json this task wrote"
python3 /projects/PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    $H/handful2.json $H/handful2_sources.json $H/handful2_classifier.json \
    $H/o8_regression/per_opcode_results.json \
    $H/o8_regression/per_opcode_population.json
echo "[7/7] task h2: grep -c exempt over every file this task added"
grep -c exempt $H/o8_regression.py $H/classifier_probe.py $H/handful.py \
    $H/handful2.md $H/lanes_h2/h2_l1_classifier.sh \
    $H/lanes_h2/h2_l2_sources.sh $H/lanes_h2/h2_l3_run.sh \
    $H/lanes_h2/h2_l4_o8_regression.sh \
    /projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.py
echo "done"
