---
id: hq.research.compiler_graph.arch_unit.arrival_contract
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (attribute), rule
node:
    name: arrival_contract
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_1_arch_unit/node_0_3_1_1_5_arrival_contract/CORE_0_3_1_1_5_arrival_contract.md
super_node:
    name: arch_unit
    path: ../CORE_0_3_1_1_arch_unit.md
sub_nodes: []
---

# CORE 0_3_1_1_5 — arrival_contract

## metadata

- **id:** hq.research.compiler_graph.arch_unit.arrival_contract
- **level:** 4
- **status:** draft
- **designation:** code (attribute), rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [arch_unit](../CORE_0_3_1_1_arch_unit.md)

## sub_nodes

*(none yet)*

## definition

Per argument of a unit, the register family the body READS before it
ever writes that family — a register family being one register and its
narrower spellings taken as one thing, so `%rdi`, `%edi` and `%dil` are
one family. The contract is read off the body's own instruction text,
never assumed from a calling convention, and the arguments are taken in
the language's own register order: System V's `%rdi, %rsi, %rdx, …` for
c, cpp, rust and swift, and go's `%rax, %rbx, %rcx, …` since go 1.17. A
register appearing inside a memory operand counts as a read.

## design

The rule, as numbered statements:

1. A register family is a read when the body uses its value before any
   instruction in the body writes that family.
2. A register named inside a memory operand — the base or the index of
   an address — is a read of that family, not an address decoration.
3. The families that are reads, listed in the language's own argument
   register order, are the arrival contract; position i in that list is
   argument i.
4. The order is the language's, not System V's for every language. go
   uses `%rax, %rbx, %rcx, …`; c, cpp, rust and swift use System V.
5. The contract is read off the body. A convention document is not
   evidence about a particular body.
6. The boundary between arrival and computation is lineage confluence
   — the first instruction whose result depends on more than one input
   lineage — never "where the arguments meet".

The stored shape:

```
ArchUnit.arrival_contract
	attributes:
		arrival_families
			"""
			ordered list of register families,
			argument i at position i
			"""
		arrival_annotation
			"""
			plain / typed-pointer / tagged —
			how the value arrives, which matters
			for interpreter handlers
			"""
```

## settled rules

- **The arrival contract is read off the body, in the language's own
  register order**, and a register inside a memory operand is a read.
  Decision: log_146 §5.4, fixed at first observation; carried in
  [arch_unit](../CORE_0_3_1_1_arch_unit.md) settled rules.
- **The arrival/computation boundary is lineage confluence.**
  Decision: AgentMemory "ARRIVAL/COMPUTATION BOUNDARY IS LINEAGE
  CONFLUENCE"; carried in [arch_unit](../CORE_0_3_1_1_arch_unit.md).
- **IN rows are numbered in arrival_contract order.** The prelude that
  emits vector arrivals first (log_153 §9) is a defect against this
  node, not a second reading of it. Decision:
  [canonical_form](../../node_0_3_1_2_canonical_form/CORE_0_3_1_2_canonical_form.md),
  this CORE's co-node ruling of 2026-09-03.
- **Argument identity rests on three grounds**: DWARF at the anchor
  build, the forced probe (`a-b` against `b-a`), and the route detour.
  Decision: `../../CORE_0_3_1_operator_equivalence.md` steps 2-4.

## realization (what exists on disk, 2026-09-03)

Home: `~/Programming/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| arrival_families per unit | `canon37_wrapped_<lang>.json`, `canon38_wrapped_<lang>.json` | done |
| go's register order corrected | recorded in log_146 §5.4 | done |
| arrival_annotation | `arrival_modes.py`, `build_entry_contract_arrival.py` | done |
| IN-i ordering against the prelude | disagreement stands, `c/op_105` the instance | **blocked** on the canonical_form fix (log_153 §9) |
