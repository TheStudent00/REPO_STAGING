---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.lean_expr.once_proved_theorems
level: 7
status: draft
settled_by: the owner
supersedes: null
designation: rule
node:
    name: once_proved_theorems
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_2_lean_expr/node_0_3_2_3_1_3_2_5_once_proved_theorems/CORE_0_3_2_3_1_3_2_5_once_proved_theorems.md
super_node:
    name: lean_expr
    path: ../CORE_0_3_2_3_1_3_2_lean_expr.md
sub_nodes: []
---

# CORE 0_3_2_3_1_3_2_5 — once_proved_theorems

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.lean_expr.once_proved_theorems
- **level:** 7
- **status:** draft
- **designation:** rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [lean_expr](../CORE_0_3_2_3_1_3_2_lean_expr.md)

## sub_nodes

*(none yet)*

## definition

The closed set of theorems written once, general in width, that
`equals` may instantiate when a construction is built from narrower
pieces: the schoolbook product of half-width pieces, the shift-and-
subtract quotient and remainder, add with carry across pieces. One per
operation KIND, never per opcode; each proved in Lean and checked, so a
wrong one fails loudly.

- the schoolbook core is a polynomial identity `ring` proves for every
  width in one call (log 274 §5.4); what a person proves once is the
  carry bookkeeping between pieces, and division's loop invariant.
- the set is expected to be EMPTY for c, c++, rust, go and swift on
  rv64, because each holds a full-width product (`__int128`, `u128`,
  `bits.Mul64`, `multipliedFullWidth`); a member is added only when a
  measured `Undecided` names a kind at a width no language has.
- the ruling this leaf encodes: a theorem here is "written once" in
  the owner's sense (2026-09-13); it resists churn because it names no
  opcode, compiler or language.
