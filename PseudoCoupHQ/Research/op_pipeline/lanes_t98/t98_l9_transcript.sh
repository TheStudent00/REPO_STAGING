#!/usr/bin/env bash
# t98 lane 9 -- THE TRANSCRIPT (lane 8 again, with the varying lines filtered) THE LOG PASTES.
#
# Every claim log_203 makes that can be reproduced has its command here,
# run from `PseudoCoupHQ` (the working directory
# `check_conventions_log_claims.py --verify` uses), with its output
# printed underneath.  The log carries these blocks verbatim, so the
# verifier re-runs exactly what is written down.
#
# Timing lines and peak-memory lines are filtered out of the commands
# that carry them: they are true when printed and different on the next
# run, so pasting them would make an honest claim unverifiable.  The
# memory figures are claimed separately, from the lane logs that measured
# them, and those claims are attributions rather than transcripts.
set -u
cd PseudoCoupHQ

show () {
  echo
  echo "\$ $1"
  bash -c "$1"
}

echo "======== [1/9] the term store, counted ========"
show 'python3 Research/op_pipeline/t98_probe_shapes.py terms | grep -v "walk:" | grep -v "peak resident"'

echo
echo "======== [2/9] distinct machine code, the two measurements ========"
show 'python3 Research/op_pipeline/t98_settle.py bodies | grep -v "walk:" | grep -v "peak resident"'

echo
echo "======== [3/9] the definitions of an opcode count, side by side ========"
show 'python3 Research/op_pipeline/t98_settle.py opcodes | grep -v "walk:" | grep -v "peak resident"'

echo
echo "======== [4/9] every computed figure the pane draws ========"
show 'python3 Research/op_pipeline/t98_render_check.py figures | grep -v "figures:" | grep -v "peak resident"'

echo
echo "======== [5/9] the pane's rows, controls and unexplained rows ========"
show 'python3 Research/op_pipeline/t98_render_check.py now | grep -v "wall clock" | grep -v "peak resident" | grep -v "bytes of html"'

echo
echo "======== [6/9] no row key goes unexplained at any moment walked ========"
show 'python3 Research/op_pipeline/t98_render_check.py keys 14 | grep "no row key"'

echo
echo "======== [7/9] the spelling guard, unmodified, ONE process, every artifact ========"
show 'python3 Research/op_pipeline/check_no_spelling_keys.py Research/op_pipeline/the_pool5.json Research/op_pipeline/audit65.json Research/op_pipeline/name_census6.json Research/op_pipeline/canon40_wrapped_*.json Research/op_pipeline/canon40_interp.json Research/op_pipeline/canon40_regen_store/*.json Research/op_pipeline/term66_store/*.json | grep -c "^PASS"'
show 'python3 Research/op_pipeline/check_no_spelling_keys.py Research/op_pipeline/the_pool5.json Research/op_pipeline/audit65.json Research/op_pipeline/name_census6.json Research/op_pipeline/canon40_wrapped_*.json Research/op_pipeline/canon40_interp.json Research/op_pipeline/canon40_regen_store/*.json Research/op_pipeline/term66_store/*.json | grep -c exempt'

echo
echo "======== [8/9] the spelling guard over the python page code ========"
show 'python3 Research/op_pipeline/check_dashboard_py_no_spelling.py Research/op_pipeline/dashboard_ouro.py Research/op_pipeline/dashboard_stats.py | grep "^PASS"'

echo
echo "======== [9/9] the javascript route changed by 0 lines ========"
show 'git diff --stat -- Research/op_pipeline/dashboard.html Research/op_pipeline/dashboard_pane1.js Research/op_pipeline/dashboard_pane23.js Research/op_pipeline/dashboard_pane4.js Research/op_pipeline/dashboard_pane5.js Research/op_pipeline/dashboard_pane6.js Research/op_pipeline/dashboard_join.js Research/op_pipeline/dashboard_loader.js | wc -l'
show 'git diff --stat -- Research/op_pipeline/check_no_spelling_keys.py Research/op_pipeline/check_dashboard_py_no_spelling.py | wc -l'
