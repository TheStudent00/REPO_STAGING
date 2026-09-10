#!/usr/bin/env bash
# ex1_l15_guard_report_and_the_tally.sh -- task ex1: the spelling guard
# over every json this task wrote, the two sources side by side, the
# report, and the tally.
#
# The guard is `Research/op_pipeline/check_no_spelling_keys.py`, which
# is never modified and is run here over every file this task added.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly

echo "[1/6] the tables of record"
python3 expand1.py tables
echo ""
echo "[2/6] the handful's ten cells on cpp beside c"
python3 expand1.py handful
echo ""
echo "[3/6] what did not work on cpp, by cause"
python3 expand1.py causes

echo ""
echo "[4/6] two cpp sources beside c's, LITERAL"
python3 expand1.py sources 2>&1 | sed -n '1,60p'

echo ""
echo "[5/6] the spelling guard, over every json this task wrote"
for f in expand1_cells.json expand1.json expand1_interp.json; do
    if [ -f "$f" ]; then
        python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py "$f"
    fi
done
echo ""
echo "   grep -c exempt over the files this task added:"
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation
for f in cpp/cpp_render.py interp/dialects.py interp/interp_render.py \
         interp/interp_check.py autopoly/expand1.py; do
    echo "      $f: $(grep -c exempt "$f" || true)"
done

echo ""
echo "[6/6] the report, and the tally"
cd autopoly
python3 expand1.py report
python3 expand1.py tally
echo ""
echo "   the interpreted table's totals"
python3 expand1.py interp_table 2>&1 | sed -n '/target . runs . rendered/,$p'
echo "done"
