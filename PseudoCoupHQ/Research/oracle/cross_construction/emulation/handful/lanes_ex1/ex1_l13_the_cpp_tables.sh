#!/usr/bin/env bash
# ex1_l13_the_cpp_tables.sh -- task ex1: the cpp column, the all-four
# and all-five lines, the handful's ten cells on cpp beside c, and what
# did not work on cpp by cause.  Printed and nothing that moves between
# runs, so a claim about any of it in a DevComms log carries a command
# that re-runs.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
echo "[1/4] the tables"
python3 expand1.py tables
echo ""
echo "[2/4] the handful's ten cells on cpp beside c"
python3 expand1.py handful
echo ""
echo "[3/4] what did not work on cpp, by cause"
python3 expand1.py causes
echo ""
echo "[4/4] the cpp spelling table"
python3 - <<'PYEOF'
import os
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
echo "done"
