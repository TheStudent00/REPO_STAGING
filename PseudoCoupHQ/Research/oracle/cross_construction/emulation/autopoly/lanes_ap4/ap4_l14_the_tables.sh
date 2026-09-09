#!/usr/bin/env bash
# ap4_l14_the_tables.sh -- task ap4: every table the brief's last
# paragraph asks for, printed off the aggregate, and nothing in any of
# them that moves between runs.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
echo "=== the per-target table, the routes, and the all-four count ==="
python3 autopoly4.py tables
echo ""
echo "=== the by-cause table ==="
python3 autopoly4.py causes
echo ""
echo "=== the change table, task ap3 -> task ap4 ==="
python3 autopoly4.py change
echo ""
echo "=== the region list ==="
python3 autopoly4.py region
echo ""
echo "=== the identity list ==="
python3 autopoly4.py identity
echo ""
echo "=== every sat, and the one re-pose ==="
python3 autopoly4.py sat
python3 autopoly4.py repose
echo "done"
