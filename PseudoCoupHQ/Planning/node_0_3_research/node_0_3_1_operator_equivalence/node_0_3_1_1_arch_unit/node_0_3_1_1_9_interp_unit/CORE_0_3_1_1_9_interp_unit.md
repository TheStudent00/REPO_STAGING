---
id: hq.research.compiler_graph.arch_unit.interp_unit
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (method)
node:
    name: interp_unit
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_1_arch_unit/node_0_3_1_1_9_interp_unit/CORE_0_3_1_1_9_interp_unit.md
super_node:
    name: arch_unit
    path: ../CORE_0_3_1_1_arch_unit.md
sub_nodes: []
---

# CORE 0_3_1_1_9 — interp_unit

## metadata

- **id:** hq.research.compiler_graph.arch_unit.interp_unit
- **level:** 4
- **status:** draft
- **designation:** code (method)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [arch_unit](../CORE_0_3_1_1_arch_unit.md)

## sub_nodes

*(none yet)*

## definition

The same object as an arch-unit, built for an interpreter or JIT
handler instead of a compiled probe: the handler's own machine code,
its arrival contract and its answer home. What differs is how the
argument arrives, so each arrival carries an annotation — PLAIN (the
value itself in a register), TYPED-POINTER (a pointer to a boxed value
whose type is known), or TAGGED (a word carrying both a small value and
its type tag). Eleven such units exist: 2 java, 1 cpython, 4 ruby, 4
php. They live in the same pool as compiled units; nothing separates
them into a table of their own.

## design

```
ArchUnit.interp_unit
	attributes:
		arrival_annotation
			"""
			plain / typed-pointer / tagged, per
			argument; the interpreter's own way
			of handing a value to a handler
			"""
	methods:
		locate_handler
			"""
			interpreter build -> the handler's
			own bytes for one operation
			"""
		annotate_arrival
			"""
			handler body -> per argument, which
			of the three arrival shapes it reads
			"""
		bank
			"""
			write the handler as an ArchUnit,
			same fields as a compiled unit
			"""
```

## settled rules

- **Interpreter and JIT handlers are arch-units too**, with arrival
  annotated plain / typed-pointer / tagged. Decision: [arch_unit](../CORE_0_3_1_1_arch_unit.md)
  settled rules (AgentMemory, round 7, the universal form).
- **There is no interpreter table.** Interpreted units are members of
  the one pool; anyone needing a split filters it. Decision:
  [pool](../../node_0_3_1_7_pool/CORE_0_3_1_7_pool.md) definition
  (AgentMemory, round 9, log_134).
- **A handler with no ship body is refused by name**, not omitted.
  `ruby/rb_big_plus` and `ruby/vm_opt_plus` are the two, cause "no
  canonical text". Decision: log_146 §8.2.

## realization (what exists on disk, 2026-09-03)

Home: `PRIVATE/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| the 11 units | `interp_canon35.json` (java 2, cpython 1, ruby 4, php 4) | done for 9 |
| the two refusals | `ruby/rb_big_plus`, `ruby/vm_opt_plus` — no ship body | done, named (log_146 §8.2) |
| handler extraction | `build_op_units_php.py`, `build_op_units_ruby.py`, `add_java.py`, `probe_gen_jit.py` | done |
| arrival annotation | `arrival_modes.py` | done |
| canonical form over them | `canon38_interp.py`, `canon38_interp.json` | done |
| superseded | `interp_canon34.json`, `interp_canon_attempt.json` | superseded records |
