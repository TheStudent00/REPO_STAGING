#!/usr/bin/env bash
# hub1_l17_the_pastes_b.sh -- task hub1, lane 17. Writes nothing.
# Lane hub1_l14's own pastes, corrected: the two composed c functions the
# range prints (not one), the float function with the blank line the range
# begins on, the body table cut at the last rust row, and the no-exemption
# count after the one word `exempt` was taken out of hub.py's docstring.
set -uo pipefail
run() { echo "\$ $*"; eval "$@"; echo; }
echo "=========== A"
run "cat PseudoCoupHQ/Research/oracle/hub/handful/composed_c.c | sed -n '/^int32_t/,/^}/p'"
echo "=========== B"
run "sed -n '/^double\$/,\$p' PseudoCoupHQ/Research/oracle/hub/handful/composed_c.c | tail -7"
echo "=========== C"
run "sed -n '/^## 3. Body A and body B/,/f7_f64_add_mul | rust/p' PseudoCoupHQ/Research/oracle/hub/oracle_test.md"
echo "=========== D"
run "grep -c exempt PseudoCoupHQ/Research/oracle/hub/hub.py"
