#!/usr/bin/env bash
# h2_l1_classifier.sh -- task h2, change 3: the zero-operand width rule
# in `model_table.classify_line`, and what it moves.
#
# WHAT THIS LANE MEASURES.  Step 1 prints the two reference tables the
# width is read from, the map the rule builds from them, the
# classifier's own answer for each zero-operand mnemonic and for three
# control lines, and whether each resulting (mnem, shape, key_width)
# triple is a TRANSLATED row of the model table.  Step 2 re-derives task
# h1b's own composition over task h1's OWN twenty carved bodies with the
# rule in place, entry by entry against what h1b recorded, and prints
# every entry that moved.  Task h1's `handful.json` is READ and never
# written.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_H2, checked
# after the one heavy read (`model_table_rows.json`, 50 MB, which task
# h1b measured at 253,716 kB).
set -euo pipefail
echo "[1/3] task h2: the rule's own tables, the classifier's answers"
python3 /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/classifier_probe.py
echo "[2/3] task h2: task h1b's composition re-derived over task h1's own twenty bodies"
python3 /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.py reclassify
echo "[3/3] done"
