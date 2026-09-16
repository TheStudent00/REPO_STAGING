---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.arch_unit
level: 6
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: arch_unit
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_3_arch_unit/CORE_0_3_2_3_1_3_3_arch_unit.md
super_node:
    name: lean_proof_path
    path: ../CORE_0_3_2_3_1_3_lean_proof_path.md
sub_nodes:
    - name: meaning
      path: node_0_3_2_3_1_3_3_0_meaning/CORE_0_3_2_3_1_3_3_0_meaning.md
    - name: decode
      path: node_0_3_2_3_1_3_3_1_decode/CORE_0_3_2_3_1_3_3_1_decode.md
    - name: compose
      path: node_0_3_2_3_1_3_3_2_compose/CORE_0_3_2_3_1_3_3_2_compose.md
    - name: branch_rule
      path: node_0_3_2_3_1_3_3_3_branch_rule/CORE_0_3_2_3_1_3_3_3_branch_rule.md
    - name: memory_and_calls
      path: node_0_3_2_3_1_3_3_4_memory_and_calls/CORE_0_3_2_3_1_3_3_4_memory_and_calls.md
---

# CORE 0_3_2_3_1_3_3 — arch_unit

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.arch_unit
- **level:** 6
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [lean_proof_path](../CORE_0_3_2_3_1_3_lean_proof_path.md)

## sub_nodes

- [meaning](node_0_3_2_3_1_3_3_0_meaning/CORE_0_3_2_3_1_3_3_0_meaning.md) — `meaning(unit, defs) -> LeanExpr`.
- [decode](node_0_3_2_3_1_3_3_1_decode/CORE_0_3_2_3_1_3_3_1_decode.md) — `decode(word) -> instruction`.
- [compose](node_0_3_2_3_1_3_3_2_compose/CORE_0_3_2_3_1_3_3_2_compose.md) — `compose(state, instruction, defs) -> state`.
- [branch_rule](node_0_3_2_3_1_3_3_3_branch_rule/CORE_0_3_2_3_1_3_3_3_branch_rule.md) — `branch_rule(state, branch, defs) -> state`.
- [memory_and_calls](node_0_3_2_3_1_3_3_4_memory_and_calls/CORE_0_3_2_3_1_3_3_4_memory_and_calls.md) — `memory_and_calls(state, instruction, defs) -> state`.

## definition

The compiled machine code of one source operator at one type pair,
cut out of the binary at its function symbol, with its meaning as a
Lean expression computed by Sail's own definitions applied in order.
This is the lifter of the earlier line, with the reference file removed:
the owner's `build_unit_lean`.

- built: `Language.compile` produces one from source; the corpus of a
  language is every unit its compiler produced for the census
  operators.
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
