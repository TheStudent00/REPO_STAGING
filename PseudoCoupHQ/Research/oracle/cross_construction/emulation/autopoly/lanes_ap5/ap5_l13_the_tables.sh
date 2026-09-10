#!/usr/bin/env bash
# ap5_l13_the_tables.sh -- task ap5: every table the brief's last
# paragraph asks for, printed off the aggregate, and nothing in any of
# them that moves between runs.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
echo "=== the per-target table, the routes, and the all-four count ==="
python3 autopoly5.py tables
echo ""
echo "=== the by-cause table ==="
python3 autopoly5.py causes
echo ""
echo "=== the change table, task ap4 -> task ap5 ==="
python3 autopoly5.py change
echo ""
echo "=== every x87 place, with the gate's verdict in z3's own words ==="
python3 autopoly5.py x87
echo ""
echo "=== the imm_* cells, before and after, and the corpus's own immediates ==="
python3 autopoly5.py immediate
echo ""
echo "=== the region list ==="
python3 autopoly5.py region
echo ""
echo "=== the identity list ==="
python3 autopoly5.py identity
echo ""
echo "=== every sat, and the one re-pose ==="
python3 autopoly5.py sat
python3 autopoly5.py repose
echo "done"
