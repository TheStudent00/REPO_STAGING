#!/usr/bin/env bash
# ex1_l14_the_tables_of_record.sh -- task ex1: THE TABLES OF RECORD.
#
# Table 1's figures are read off the two AGGREGATES rather than
# re-counted: cpp's from this task's `expand1.json`, the other four
# from task ap4's `autopoly4.json`, both written by the same function.
# The first pass of lane ex1_l13 re-counted them here instead and got a
# different c column and a different all-four line (142 against task
# ap4's own 162), which is why the rule is now CALLED
# (`autopoly4.outcome_of`) and not restated.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
echo "[1/5] the tables"
python3 expand1.py tables
echo ""
echo "[2/5] the handful's ten cells on cpp beside c"
python3 expand1.py handful
echo ""
echo "[3/5] what did not work on cpp, by cause"
python3 expand1.py causes
echo ""
echo "[4/5] the cpp spelling table"
python3 - <<'PYEOF'
import sys
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/"
                   "cross_construction/emulation/cpp")
import cpp_render as CPR
print("| what | the spelling | the probe that measured it |")
print("|---|---|---|")
for row in CPR.spelling_rows():
    print("| %s | `%s` | %s |"
          % (row["what"], row["spelling"].replace("|", "/"),
             row["probe"].replace("|", "/")))
PYEOF
echo ""
echo "[5/5] the report"
python3 expand1.py report
echo "done"
