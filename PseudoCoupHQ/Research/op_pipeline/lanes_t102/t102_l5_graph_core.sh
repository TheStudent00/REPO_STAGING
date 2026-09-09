#!/usr/bin/env bash
set -u
cd PseudoCoupHQ
echo "[1/1] graph core check"
echo "=== full grep task93/graph_compact/graphs_home/PseudoCoupGraphs in graph CORE ==="
grep -n -i "task 93\|graph_compact\|graphs_home\|PseudoCoupGraphs\|compact" \
  Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_9_graph/CORE_0_3_1_9_graph.md
echo "=== realization table section of graph CORE ==="
sed -n '/## realization/,/## /p' Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_9_graph/CORE_0_3_1_9_graph.md | head -100
echo "=== does graph PROGRESS mention 'moved' or 'PseudoCoupGraphs' at all? ==="
grep -n -i "PseudoCoupGraphs\|moved\|compact" Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_9_graph/PROGRESS.md
echo "[1/1] done"
