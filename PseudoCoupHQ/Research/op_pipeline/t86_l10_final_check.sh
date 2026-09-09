#!/usr/bin/env bash
# t86_l10_final_check.sh -- TASK 86, lane 10: the last check over every
# python file this task edited, including the superseded builder, and a
# compile of each.
set -uo pipefail
cd /projects/PseudoCoupHQ/Research/op_pipeline || exit 2
echo "[1/2] every edited python file compiles"
for f in dashboard_ouro.py chronology_build.py t86_ouro_shots.py; do
    python3 -c "import ast,sys; ast.parse(open(sys.argv[1]).read()); print('  parses:', sys.argv[1])" "$f" || exit 3
done
echo
echo "[2/2] check_dashboard_py_no_spelling.py over all three"
python3 check_dashboard_py_no_spelling.py dashboard_ouro.py \
    chronology_build.py viewer_build.py 2>&1 | grep -E "^(PASS|FAIL|operator inventory)"
echo "  exit ${PIPESTATUS[0]}"
