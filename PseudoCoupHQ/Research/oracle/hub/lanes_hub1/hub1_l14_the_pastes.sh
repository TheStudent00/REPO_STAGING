#!/usr/bin/env bash
# hub1_l14_the_pastes.sh -- task hub1, lane 14. Writes nothing.
# It runs, exactly as the log will paste them, the commands the report's
# claims rest on, so that the pasted output is the lane's own and the
# conventions verifier re-runs the same text.
set -uo pipefail
run() { echo "\$ $*"; eval "$@"; echo; }
echo "=========== BLOCK 1"
run "sed -n '5,11p' PseudoCoupHQ/Research/oracle/hub/dictionary.md"
echo "=========== BLOCK 2"
run "sed -n '13,20p' PseudoCoupHQ/Research/oracle/hub/dictionary.md"
echo "=========== BLOCK 3"
run "sed -n '/^## 3. Holes per target/,/^### rust/p' PseudoCoupHQ/Research/oracle/hub/dictionary.md"
echo "=========== BLOCK 4"
run "sed -n '/^## 1. The handful, node by node/,/^## 2/p' PseudoCoupHQ/Research/oracle/hub/oracle_test.md"
echo "=========== BLOCK 5"
run "cut -d'|' -f2,3,4,5 PseudoCoupHQ/Research/oracle/hub/oracle_test.md | sed -n '/f1_i32_add_sub | c/,/f8_i32_select | go/p'"
echo "=========== BLOCK 6"
run "sed -n '/^## 3. Body A and body B/,/^## 4/p' PseudoCoupHQ/Research/oracle/hub/oracle_test.md"
echo "=========== BLOCK 7"
run "sed -n '/^## 4. The measure over/,/^## 5/p' PseudoCoupHQ/Research/oracle/hub/oracle_test.md"
echo "=========== BLOCK 8"
run "sed -n '/^## 5. The measure, by cause/,\$p' PseudoCoupHQ/Research/oracle/hub/oracle_test.md | cut -c1-150"
echo "=========== BLOCK 9"
run "python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/hub/dictionary.json"
run "python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/hub/oracle_test.json"
run "python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py PseudoCoupHQ/Research/oracle/hub/measure.json"
echo "=========== BLOCK 10"
run "grep -c exempt PseudoCoupHQ/Research/oracle/hub/hub.py"
echo "=========== BLOCK 11"
run "cat PseudoCoupHQ/Research/oracle/hub/handful/composed_c.c | sed -n '/^int32_t/,/^}/p'"
echo "=========== BLOCK 12"
run "sed -n '/^double$/,\$p' PseudoCoupHQ/Research/oracle/hub/handful/composed_c.c | tail -8"
