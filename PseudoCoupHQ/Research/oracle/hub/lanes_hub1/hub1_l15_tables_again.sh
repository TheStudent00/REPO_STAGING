#!/usr/bin/env bash
# hub1_l15_tables_again.sh -- task hub1, lane 15: the tables again, after a
# correction to ONE sentence and one count. Lane hub1_l13's table 4 said
# "the corpus holds 138 go units"; 138 is the size of task o2's NARROW rule
# population for go, and the corpus holds 590. The count and the sentence
# now say both, and nothing measured changed.
set -uo pipefail
echo "[1/2] the tables"
cd PseudoCoupHQ/Research/oracle/hub
python3 hub.py tables
echo "[2/2] table 4, as it now reads"
sed -n '/^## 4. The measure over/,/^## 5/p' PseudoCoupHQ/Research/oracle/hub/oracle_test.md
