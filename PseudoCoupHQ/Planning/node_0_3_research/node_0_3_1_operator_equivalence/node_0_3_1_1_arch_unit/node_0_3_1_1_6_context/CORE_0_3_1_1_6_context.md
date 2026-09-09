---
id: hq.research.compiler_graph.arch_unit.context
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (attribute)
node:
    name: context
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_1_arch_unit/node_0_3_1_1_6_context/CORE_0_3_1_1_6_context.md
super_node:
    name: arch_unit
    path: ../CORE_0_3_1_1_arch_unit.md
sub_nodes: []
---

# CORE 0_3_1_1_6 — context

## metadata

- **id:** hq.research.compiler_graph.arch_unit.context
- **level:** 4
- **status:** draft
- **designation:** code (attribute)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [arch_unit](../CORE_0_3_1_1_arch_unit.md)

## sub_nodes

*(none yet)*

## definition

Everything OUTSIDE a unit's body that the body needs in order to run:
the constants it reaches rip-relative (addressed as an offset from the
instruction pointer), the stack frame it addresses as its own, and the
routines it transfers to. Context is kept as part of the unit's record,
because a body that cannot run without it is not fully recorded without
it. It is a record of what the body reaches for, not a rewrite of the
body: nothing in the body changes to accommodate it.

## design

```
ArchUnit.context
	attributes:
		rip_constants
			"""
			each constant the body reads at an
			offset from the instruction pointer,
			with its bytes; they become
			ripconst_<n> symbols in the
			reference's memory
			"""
		own_frame
			"""
			the stack addresses the body treats
			as its own frame: the offsets it
			writes and reads back
			"""
		callees
			"""
			each routine the body transfers to,
			by name; a routine of the compiler's
			own runtime is followed further —
			see runtime_callee
			"""
	methods:
		collect
			"""
			body_bytes + body_text + the object
			file -> the three records above
			"""
```

## settled rules

- **Context code is kept.** the owner, 2026-08-30: "if the system requires
  context code to function, that context code needs to be kept."
  Decision: [arch_unit](../CORE_0_3_1_1_arch_unit.md) settled rules.
- **The body is never changed to remove a context need.** The record
  grows; the body stays verbatim. Decision:
  [canonical_form](../../node_0_3_1_2_canonical_form/CORE_0_3_1_2_canonical_form.md)
  settled rules (AgentMemory "THE MEMORY-WRAPPED FORM").
- **A rip-relative constant enters the reference as a named symbol**
  `ripconst_<n>`, so a proof can talk about it. Decision:
  [machine_state](../../node_0_3_1_4_reference/node_0_3_1_4_1_machine_state/CORE_0_3_1_4_1_machine_state.md);
  carried in
  [reference](../../node_0_3_1_4_reference/CORE_0_3_1_4_reference.md).
- **A callee into the compiler's own runtime is followed, not treated
  as an outside library.** Decision: the owner, 2026-09-03; see
  [runtime_callee](../node_0_3_1_1_8_runtime_callee/CORE_0_3_1_1_8_runtime_callee.md).

## realization (what exists on disk, 2026-09-03)

| part | current file | status |
|---|---|---|
| context record per unit | the round-6 context record, carried on the unit | done |
| rip_constants in proofs | `ripconst_<n>` symbols in the reference's memory array | done |
| callees named in canonical text | `call x_runtime_panicshift` form (log_152 §4.1) | done |
| callees followed into the runtime | see [runtime_callee](../node_0_3_1_1_8_runtime_callee/CORE_0_3_1_1_8_runtime_callee.md) — attached bodies (task 59/63), their answer registers read off the body rather than asserted (task 78) | **done** — STALE ROW CORRECTED 2026-09-04 (round-15 bank): runtime_callee's own realization has carried this as done since task 63/78 |
