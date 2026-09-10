#!/usr/bin/env bash
# hub2_l14_the_pastes.sh -- task hub2, lane 14: every command the report
# quotes, run here so the report's fenced blocks are captured output and
# never hand-tidied.  It writes nothing.
set -uo pipefail
D=PseudoCoupHQ/Research/oracle/hub
run() { echo "\$ $*"; "$@"; echo; }
echo "=== 1 dictionary2.md, entries and holes per target per level"
run sed -n '5,17p' $D/dictionary2.md
echo "=== 2 dictionary2.md, routes and kinds"
run sed -n '19,26p' $D/dictionary2.md
echo "=== 3 dictionary2.md, the c cell holes by cause"
run sed -n '27,38p' $D/dictionary2.md
echo "=== 4 dictionary2.md, the go side at three levels"
run sed -n '466,473p' $D/dictionary2.md
echo "=== 5 dictionary2.md, the pairs go's corpus attests, the ones with an entry"
echo "\$ grep -n 'cmp gpr_gpr 8 +' $D/dictionary2.md | head -12"
grep -n 'cmp gpr_gpr 8 +' $D/dictionary2.md | head -12
echo
echo "=== 6 oracle_test2.md, the handful hub1 then hub2"
run sed -n '25,52p' $D/oracle_test2.md
echo "=== 7 oracle_test2.md, the measure over task hub1's own population"
run sed -n '88,99p' $D/oracle_test2.md
echo "=== 8 oracle_test2.md, the measure over every corpus go unit"
run sed -n '101,107p' $D/oracle_test2.md
echo "=== 9 oracle_test2.md, the measure by level"
run sed -n '109,121p' $D/oracle_test2.md
echo "=== 10 the composed f5 on c, LITERAL"
run sed -n '100,106p' $D/handful/composed2_c.c
echo "=== 11 one pair composition and its two bodies"
echo "\$ python3 $D/hub2_paste_a_pair.py"
python3 $D/hub2_paste_a_pair.py
echo
echo "=== 12 the tally"
run wc -l $D/hub2.py $D/dictionary2.json $D/dictionary2.md $D/oracle_test2.json $D/oracle_test2.md $D/measure2.json
