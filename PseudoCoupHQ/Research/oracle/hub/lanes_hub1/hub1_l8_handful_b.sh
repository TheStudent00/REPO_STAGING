#!/usr/bin/env bash
# hub1_l8_handful_b.sh -- task hub1, lane 8: the handful, second pass.
# Lane hub1_l5's own log is the first pass and is kept; this one runs the
# same command after three corrections lane hub1_l6 made possible -- the
# grammar's real nesting (`block -> statement_list -> return_statement ->
# expression_list`), a node key on the whole SPAN (because `a + b - c`
# gives the outer node and its own left sub-node the same start), and the
# hole causes read off go's own build of the same construct.
# Memory bound 6 GB, named abort ABORT_MEMORY_HUB1.
set -uo pipefail
echo "[1/2] the handful"
cd PseudoCoupHQ/Research/oracle/hub
python3 hub.py handful
echo "[2/2] the spelling guard over what this lane wrote"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    PseudoCoupHQ/Research/oracle/hub/oracle_test.json
