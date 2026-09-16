---
id: hq.research.lean_proof_path_resistant_to_churn.arch_unit
level: 3
status: draft
settled_by: the owner
supersedes: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.arch_unit
designation: code (class)
node:
    name: arch_unit
    path: Planning/node_0_3_research/node_0_3_3_lean_proof_path_resistant_to_churn/node_0_3_3_3_arch_unit/CORE_0_3_3_3_arch_unit.md
super_node:
    name: lean_proof_path_resistant_to_churn
    path: ../CORE_0_3_3_lean_proof_path_resistant_to_churn.md
sub_nodes:
    - name: meaning
      path: node_0_3_3_3_0_meaning/CORE_0_3_3_3_0_meaning.md
    - name: decode
      path: node_0_3_3_3_1_decode/CORE_0_3_3_3_1_decode.md
    - name: compose
      path: node_0_3_3_3_2_compose/CORE_0_3_3_3_2_compose.md
    - name: branch_rule
      path: node_0_3_3_3_3_branch_rule/CORE_0_3_3_3_3_branch_rule.md
    - name: memory_and_calls
      path: node_0_3_3_3_4_memory_and_calls/CORE_0_3_3_3_4_memory_and_calls.md
---

# CORE 0_3_3_3 — arch_unit

## metadata

- **id:** hq.research.lean_proof_path_resistant_to_churn.arch_unit
- **level:** 3
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.arch_unit

## super_node

- [lean_proof_path_resistant_to_churn](../CORE_0_3_3_lean_proof_path_resistant_to_churn.md)

## sub_nodes

- [meaning](node_0_3_3_3_0_meaning/CORE_0_3_3_3_0_meaning.md) — `meaning(unit, defs) -> LeanExpr`.
- [decode](node_0_3_3_3_1_decode/CORE_0_3_3_3_1_decode.md) — `decode(word) -> instruction`.
- [compose](node_0_3_3_3_2_compose/CORE_0_3_3_3_2_compose.md) — `compose(state, instruction, defs) -> state`.
- [branch_rule](node_0_3_3_3_3_branch_rule/CORE_0_3_3_3_3_branch_rule.md) — `branch_rule(state, branch, defs) -> state`.
- [memory_and_calls](node_0_3_3_3_4_memory_and_calls/CORE_0_3_3_3_4_memory_and_calls.md) — `memory_and_calls(state, instruction, defs) -> state`.

## definition

The compiled machine code of one source operator at one type pair,
cut out of the binary at its function symbol, with its meaning as a
Lean expression computed by Sail's own definitions applied in order.
This is the lifter of the earlier line, with the reference file removed:
the owner's `build_unit_lean`.

- built: `Language.compile` produces one from source;
  `Language.compiler_corpus` is EVERY compiler-operator of the language,
  function-wrapped and lowered: one unit per (operator, operand types),
  the probe set of the operator pipeline, generated from the grammar,
  never typed.
- `meaning` knows Sail's decoder and `execute` and the shape of a
  straight-line body with branches, loads, stores and calls; it knows
  no instruction.

## design

```
class ArchUnit
	attributes:
		language
		source
		symbol
		instructions       # list of encoded words, in address order
		lean               # LeanExpr, set by meaning
	methods:
		meaning
		decode
		compose
		branch_rule
		memory_and_calls
```
