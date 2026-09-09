#!/usr/bin/env bash
# m1b_l10_edges.sh -- task m1b: model_table.py edges, re-run because
# every row_id moved when the sweep grew. The population of
# same-builder cells is EXACTLY the one task m1 decided: the three
# added x87 shapes are left out of it (model_table.cells_of_pair says
# so and why), because the x87 group's terms are 80-bit floating point
# and every solver call on them reaches the 3,000 ms ceiling -- task
# m1 measured that pass at about 24 hours. Nothing else is skipped.
# MEMORY BOUND: 16 GB resident, named abort ABORT_MEMORY_M1B, checked
# every 200 cells; m1's own run of this command peaked at 1,088 MB.
# Peak RSS printed by the script.
set -euo pipefail
echo "[1/1] task m1b: model_table.py edges"
cd PseudoCoupHQ/Research/oracle/arch_opcodes/model
python3 model_table.py edges
echo "[1/1] done"
