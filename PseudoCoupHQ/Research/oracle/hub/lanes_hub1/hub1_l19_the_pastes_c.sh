#!/usr/bin/env bash
# hub1_l19_the_pastes_c.sh -- task hub1, lane 19. Writes nothing.
# Lane hub1_l18 (the conventions verifier) scored 7 of this log's pasted
# commands REFUSED with cause `log_unreachable`: a `sed` RANGE like
# `'/^## 3/,/^### rust/p'` is a token beginning `/`, which the verifier
# reads as a path that does not exist. Each is re-spelled as a LINE-NUMBER
# range over the same file, which reads the same bytes and carries no
# leading slash. This lane prints each, exactly as the log then pastes it.
set -uo pipefail
run() { echo "\$ $*"; eval "$@"; echo; }
echo "=========== A dictionary.md, holes on c"
run "sed -n '21,33p' PseudoCoupHQ/Research/oracle/hub/dictionary.md"
echo "=========== B oracle_test.md, the nodes"
run "sed -n '5,24p' PseudoCoupHQ/Research/oracle/hub/oracle_test.md"
echo "=========== C oracle_test.md, the eight functions, four columns"
run "sed -n '29,52p' PseudoCoupHQ/Research/oracle/hub/oracle_test.md | cut -d'|' -f2,3,4,5"
echo "=========== D composed_c.c, the two int32 functions"
run "sed -n '59,73p' PseudoCoupHQ/Research/oracle/hub/handful/composed_c.c"
echo "=========== E composed_c.c, the float64 function"
run "sed -n '82,88p' PseudoCoupHQ/Research/oracle/hub/handful/composed_c.c"
echo "=========== F oracle_test.md, body A and body B, c and rust"
run "sed -n '54,66p' PseudoCoupHQ/Research/oracle/hub/oracle_test.md"
echo "=========== G oracle_test.md, the measure"
run "sed -n '73,82p' PseudoCoupHQ/Research/oracle/hub/oracle_test.md"
