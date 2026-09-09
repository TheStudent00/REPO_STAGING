#!/usr/bin/env bash
set -u
cd /projects/PseudoCoupHQ
echo "======== [1/3] PROGRESS.md files under the two subtrees ========"
find Planning/node_0_3_research/node_0_3_1_operator_equivalence Planning/node_0_3_research/node_0_3_2_arch_unit_oracle -name PROGRESS.md | sort | wc -l
echo "======== [2/3] rows with planned/in-progress (case-insensitive) ========"
grep -n -i "planned\|in-progress\|in progress" \
  $(find Planning/node_0_3_research/node_0_3_1_operator_equivalence Planning/node_0_3_research/node_0_3_2_arch_unit_oracle -name PROGRESS.md) \
  2>/dev/null
echo "======== [3/3] rows with done (case-insensitive), for absence spot-check ========"
grep -n -i "\bdone\b" \
  $(find Planning/node_0_3_research/node_0_3_1_operator_equivalence Planning/node_0_3_research/node_0_3_2_arch_unit_oracle -name PROGRESS.md) \
  2>/dev/null
