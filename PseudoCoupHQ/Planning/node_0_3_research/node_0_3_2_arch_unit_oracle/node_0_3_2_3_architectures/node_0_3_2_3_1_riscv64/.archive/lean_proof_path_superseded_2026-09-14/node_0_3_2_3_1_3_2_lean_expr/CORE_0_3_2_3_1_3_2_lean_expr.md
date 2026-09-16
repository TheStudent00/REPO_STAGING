---
id: hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.lean_expr
level: 6
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: lean_expr
    path: Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_3_architectures/node_0_3_2_3_1_riscv64/node_0_3_2_3_1_3_lean_proof_path/node_0_3_2_3_1_3_2_lean_expr/CORE_0_3_2_3_1_3_2_lean_expr.md
super_node:
    name: lean_proof_path
    path: ../CORE_0_3_2_3_1_3_lean_proof_path.md
sub_nodes:
    - name: equals
      path: node_0_3_2_3_1_3_2_0_equals/CORE_0_3_2_3_1_3_2_0_equals.md
    - name: widen
      path: node_0_3_2_3_1_3_2_1_widen/CORE_0_3_2_3_1_3_2_1_widen.md
    - name: normalize_integer_level
      path: node_0_3_2_3_1_3_2_2_normalize_integer_level/CORE_0_3_2_3_1_3_2_2_normalize_integer_level.md
    - name: decide_fixed_width
      path: node_0_3_2_3_1_3_2_3_decide_fixed_width/CORE_0_3_2_3_1_3_2_3_decide_fixed_width.md
    - name: primitives
      path: node_0_3_2_3_1_3_2_4_primitives/CORE_0_3_2_3_1_3_2_4_primitives.md
    - name: once_proved_theorems
      path: node_0_3_2_3_1_3_2_5_once_proved_theorems/CORE_0_3_2_3_1_3_2_5_once_proved_theorems.md
---

# CORE 0_3_2_3_1_3_2 — lean_expr

## metadata

- **id:** hq.research.arch_unit_oracle.architectures.riscv64.lean_proof_path.lean_expr
- **level:** 6
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [lean_proof_path](../CORE_0_3_2_3_1_3_lean_proof_path.md)

## sub_nodes

- [equals](node_0_3_2_3_1_3_2_0_equals/CORE_0_3_2_3_1_3_2_0_equals.md) — `equals(left, right, budget) -> Proof | Differ | Undecided`.
- [widen](node_0_3_2_3_1_3_2_1_widen/CORE_0_3_2_3_1_3_2_1_widen.md) — `widen(expr) -> LeanExpr`.
- [normalize_integer_level](node_0_3_2_3_1_3_2_2_normalize_integer_level/CORE_0_3_2_3_1_3_2_2_normalize_integer_level.md) — `normalize_integer_level(expr) -> LeanExpr`.
- [decide_fixed_width](node_0_3_2_3_1_3_2_3_decide_fixed_width/CORE_0_3_2_3_1_3_2_3_decide_fixed_width.md) — `decide_fixed_width(equation, budget) -> Proof | Differ | Undecided`.
- [primitives](node_0_3_2_3_1_3_2_4_primitives/CORE_0_3_2_3_1_3_2_4_primitives.md) — `primitives(expr) -> set[SailPrimitive]`.
- [once_proved_theorems](node_0_3_2_3_1_3_2_5_once_proved_theorems/CORE_0_3_2_3_1_3_2_5_once_proved_theorems.md) — The closed set of theorems written once, general in width, that `equals` may instantiate when a construction is built from narrower pieces: the schoolbook product of half-width pieces, the shift-and- subtract quotient and remainder, add with carry across pieces.

## definition

An expression in Lean over unknowns of fixed width, with one question
answerable of any two: are they the same function of their unknowns.
Every definition, every unit's meaning and every primitive is one of
these, so the prover has one input type.

- built: from the Lean text the sail compiler emitted, or from
  `ArchUnit.meaning` composing such texts.
- the answer to `equals` is a Lean theorem file, checked by Lean's
  kernel; that file is the certificate the dictionary stores.

## design

```
class LeanExpr
	attributes:
		text               # the Lean expression
		unknowns           # name -> width
	methods:
		equals
		widen
		normalize_integer_level
		decide_fixed_width
		primitives
```
