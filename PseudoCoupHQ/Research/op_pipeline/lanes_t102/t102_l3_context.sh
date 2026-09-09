#!/usr/bin/env bash
set -u
cd /projects/PseudoCoupHQ
echo "=== A: node_0_3_1_10_dashboard/PROGRESS.md tail ==="
tail -40 Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_10_dashboard/PROGRESS.md
echo "=== B: node_0_3_1_9_graph/PROGRESS.md tail ==="
tail -60 Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_9_graph/PROGRESS.md
echo "=== C: node_0_3_1_1_arch_unit/PROGRESS.md tail ==="
tail -40 Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_1_arch_unit/PROGRESS.md
echo "=== D: node_0_3_1_1_6_context/PROGRESS.md full ==="
cat Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_1_arch_unit/node_0_3_1_1_6_context/PROGRESS.md
echo "=== E: node_0_3_1_1_8_runtime_callee/PROGRESS.md tail ==="
tail -40 Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_1_arch_unit/node_0_3_1_1_8_runtime_callee/PROGRESS.md
echo "=== F: node_0_3_1_6_term/PROGRESS.md around line 3535-3660 ==="
sed -n '3520,3660p' Planning/node_0_3_research/node_0_3_1_operator_equivalence/PROGRESS.md
echo "=== G: node_0_3_1_6_2_transcribe/PROGRESS.md tail ==="
tail -40 Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_6_term/node_0_3_1_6_2_transcribe/PROGRESS.md
echo "=== H: node_0_3_1_6_3_normalize/PROGRESS.md tail ==="
tail -40 Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_6_term/node_0_3_1_6_3_normalize/PROGRESS.md
echo "=== I: node_0_3_1_6_4_census/PROGRESS.md tail ==="
tail -30 Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_6_term/node_0_3_1_6_4_census/PROGRESS.md
echo "=== J: node_0_3_1_7_pool/PROGRESS.md tail ==="
tail -40 Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_7_pool/PROGRESS.md
echo "=== K: node_0_3_1_7_6_exception_families/PROGRESS.md tail ==="
tail -30 Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_7_pool/node_0_3_1_7_6_exception_families/PROGRESS.md
echo "=== L: node_0_3_1_5_gate/PROGRESS.md tail ==="
tail -30 Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/PROGRESS.md
echo "=== M: node_0_3_1_5_0_verdict/PROGRESS.md tail ==="
tail -30 Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_0_verdict/PROGRESS.md
echo "=== N: node_0_3_1_5_5_zero_regression/PROGRESS.md tail ==="
tail -30 Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_5_gate/node_0_3_1_5_5_zero_regression/PROGRESS.md
echo "=== O: node_0_3_1_2_canonical_form/PROGRESS.md tail ==="
tail -40 Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_2_canonical_form/PROGRESS.md
echo "=== P: node_0_3_1_2_2_prelude/PROGRESS.md tail ==="
tail -30 Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_2_canonical_form/node_0_3_1_2_2_prelude/PROGRESS.md
echo "=== Q: node_0_3_1_4_reference/PROGRESS.md tail ==="
tail -40 Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_4_reference/PROGRESS.md
echo "=== R: node_0_3_1_4_0_opcode_table/PROGRESS.md tail ==="
tail -40 Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_4_reference/node_0_3_1_4_0_opcode_table/PROGRESS.md
echo "=== S: node_0_3_1_4_1_machine_state/PROGRESS.md tail ==="
tail -30 Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_4_reference/node_0_3_1_4_1_machine_state/PROGRESS.md
echo "=== T: node_0_3_2_arch_unit_oracle/PROGRESS.md full ==="
cat Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/PROGRESS.md
