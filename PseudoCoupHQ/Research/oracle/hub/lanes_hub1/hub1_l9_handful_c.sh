#!/usr/bin/env bash
# hub1_l9_handful_c.sh -- task hub1, lane 9: the handful, third pass.
# Three corrections since lane hub1_l8, each named on its own: go's own
# brace placement in a composed declaration (`go build` refuses a `{` on a
# line of its own); the DEFAULT TYPE of an untyped boolean value, which is
# how go/types' `untyped bool` and the corpus's own `bool` are joined; and
# the second operator label the node record carried, which the spelling
# guard refused and which said nothing the record's own `operator` field
# did not. Memory bound 6 GB, named abort ABORT_MEMORY_HUB1.
set -uo pipefail
echo "[1/2] the handful"
cd PseudoCoupHQ/Research/oracle/hub
python3 hub.py handful
echo "[2/2] the spelling guard over what this lane wrote"
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py \
    PseudoCoupHQ/Research/oracle/hub/oracle_test.json
