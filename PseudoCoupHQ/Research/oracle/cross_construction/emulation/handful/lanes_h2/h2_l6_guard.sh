#!/usr/bin/env bash
# h2_l6_guard.sh -- task h2: the unmodified spelling guard, in two
# steps, and `grep -c exempt` over every file this task added.
#
# WHY TWO STEPS, and why lane h2_l5 exited 1.  Lane h2_l5 ran the guard
# over five json files at once, and one of them is not this task's own:
# `o8_regression/per_opcode_results.json` is written by task o8's own
# program, unchanged, and it carries `landed_mnem` -- an arch-opcode
# mnemonic, four of which (`and`, `or`, `xor`, `not`) are also banned
# operator spellings.  Task o8 found this on its own artifact and left
# it OPEN, awaiting the owner (log 208, log 220, and `per_opcode.py`'s own
# docstring); this task inherits that open question and does not
# re-litigate it, so the two populations are guarded apart:
#   step 1: the three json THIS task's own programs write -- expected
#           to PASS on their first run, as task h1's and h1b's did.
#   step 2: task o8's OWN artifact beside this task's scratch copy of
#           it, so the two are seen to fail identically and the scratch
#           copy is seen to introduce nothing.  `|| true` keeps the
#           lane's own exit about the lane, not about that inherited
#           question.
# The guard itself is never modified and no exemption is claimed.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_H2; the guard
# reads json files of a few hundred kB and reports its own peak.
set -euo pipefail
H=PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
P=PseudoCoupHQ/Research/oracle/cross_construction/emulation/per_opcode
echo "[1/3] task h2: the guard over the three json this task's own programs write"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    $H/handful2.json $H/handful2_sources.json $H/handful2_classifier.json
echo "[2/3] task h2: the guard over task o8's own results beside this task's scratch copy"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    $P/per_opcode_results.json $H/o8_regression/per_opcode_results.json \
    2>&1 | grep -E "^(operator inventory|PASS|FAIL)" || true
echo "[3/3] task h2: grep -c exempt over every file this task added"
grep -c exempt $H/o8_regression.py $H/classifier_probe.py $H/handful.py \
    $H/handful2.md $H/lanes_h2/h2_l1_classifier.sh \
    $H/lanes_h2/h2_l2_sources.sh $H/lanes_h2/h2_l3_run.sh \
    $H/lanes_h2/h2_l4_o8_regression.sh \
    PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.py
echo "done"
