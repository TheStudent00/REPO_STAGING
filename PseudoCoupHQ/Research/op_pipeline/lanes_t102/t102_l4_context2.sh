#!/usr/bin/env bash
set -u
cd PseudoCoupHQ
echo "[1/1] more context"
echo "=== dashboard PROGRESS lines 1-30 ==="
sed -n '1,30p' Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_10_dashboard/PROGRESS.md
echo "=== dashboard PROGRESS lines 255-390 ==="
sed -n '255,390p' Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_10_dashboard/PROGRESS.md
echo "=== graph PROGRESS lines 1-30 ==="
sed -n '1,30p' Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_9_graph/PROGRESS.md
echo "=== graph PROGRESS lines 240-320 ==="
sed -n '240,320p' Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_9_graph/PROGRESS.md
echo "=== does dashboard PROGRESS mention task 93? ==="
grep -n "task 93\|TASK 93" Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_10_dashboard/PROGRESS.md
echo "=== does graph PROGRESS mention task 93? ==="
grep -n "task 93\|TASK 93" Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_9_graph/PROGRESS.md
echo "[1/1] done"
