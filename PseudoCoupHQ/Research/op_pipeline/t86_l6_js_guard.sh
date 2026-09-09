#!/usr/bin/env bash
# t86_l6_js_guard.sh -- TASK 86, lane 6: the JavaScript-route guard, with
# its file list (lane 5 called it with no arguments and it answered its
# own usage, exit 2 -- kept as the record of that).
set -uo pipefail
cd PseudoCoupHQ/Research/op_pipeline || exit 2
python3 check_dashboard_js_no_spelling.py \
    dashboard_join.js dashboard_loader.js dashboard_pane1.js \
    dashboard_pane23.js dashboard_pane4.js dashboard_pane5.js \
    dashboard_pane6.js 2>&1 | tail -20
echo "  exit ${PIPESTATUS[0]}"
