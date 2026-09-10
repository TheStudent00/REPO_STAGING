#!/usr/bin/env bash
# hub1_l16_tables_c.sh -- task hub1, lane 16: the tables a third time. The
# three population figures of table 4 are now read from dictionary.json as
# it stands rather than from the counts the measure lane stored, so the
# sentence naming them is correct without re-running the measure. Nothing
# measured changed; only the naming of the population did.
set -uo pipefail
echo "[1/2] the tables"
cd PseudoCoupHQ/Research/oracle/hub
python3 hub.py tables
echo "[2/2] table 4, as it now reads"
sed -n '/^## 4. The measure over/,/^## 5/p' PseudoCoupHQ/Research/oracle/hub/oracle_test.md
