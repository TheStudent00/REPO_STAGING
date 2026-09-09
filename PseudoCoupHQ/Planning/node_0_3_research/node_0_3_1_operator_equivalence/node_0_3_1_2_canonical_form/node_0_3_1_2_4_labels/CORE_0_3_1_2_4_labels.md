---
id: hq.research.compiler_graph.canonical_form.labels
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (method), rule
node:
    name: labels
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_2_canonical_form/node_0_3_1_2_4_labels/CORE_0_3_1_2_4_labels.md
super_node:
    name: canonical_form
    path: ../CORE_0_3_1_2_canonical_form.md
sub_nodes: []
---

# CORE 0_3_1_2_4 — labels

## metadata

- **id:** hq.research.compiler_graph.canonical_form.labels
- **level:** 4
- **status:** draft
- **designation:** code (method), rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [canonical_form](../CORE_0_3_1_2_canonical_form.md)

## sub_nodes

*(none yet)*

## definition

The rewrite that replaces every branch target inside a unit with a
positional name — `L0`, `L1`, … in address order — so that two units
with the same shape of jumps get the same text instead of two texts
differing only by their own addresses and their own function names.
The targets are located by reading the unit's OWN bytes with capstone,
a disassembler library, so the mapping is forced by the bytes rather
than guessed from the printed text. A transfer OUT of the unit is
treated differently: it drops its address and its angle-bracket symbol
comment but KEEPS the callee as its operand.

## design

The rule, as numbered statements:

1. A transfer whose target is an instruction inside this unit becomes
   `L0`, `L1`, … numbered in ADDRESS order, and the label is defined
   on the instruction it names.
2. Targets are located by disassembling the unit's own bytes with
   capstone, so the target mapping comes from the bytes.
3. A transfer OUT of the unit keeps its callee as the operand and
   drops the address and the angle-bracket comment:
   `call 43f300 <runtime.panicshift>` becomes
   `call x_runtime_panicshift`.
4. The callee is kept because the ruling's purpose is that a unit's
   own name must not sit in its own text — and two units calling
   DIFFERENT routines must not collapse into one text.
5. Nothing else on any line changes. That is structural check C6.

```
CanonicalForm.labels
	methods:
		locate_targets
			"""
			body_bytes -> per transfer, whether
			its target is inside the unit, and
			at which offset (capstone)
			"""
		rewrite
			"""
			body_text + targets -> the same text
			with L0.. labels defined and named
			"""
		rewrite_external
			"""
			an out-of-unit transfer -> callee
			kept as operand, address and comment
			dropped
			"""
```

## settled rules

- **Branch labels are positional, `L0..` in address order.**
  Decision: AgentMemory "ROUND 10 RULINGS" (4); log_152 §4.1.
- **An out-of-unit transfer keeps its callee as the operand.**
  Decision: log_152 §4.1 and §9.1 item 1 — recorded as a declared
  departure from the ruling's literal words, for the stated reason.
- **The targets are read off the bytes with capstone**, not guessed
  from the text. Decision: log_152 §4.1.
- **C6 verifies that nothing else on any line changed**, and it is a
  new check rather than a reuse of canon37's character-for-character
  claim, which this rewrite makes false as written. Decision:
  log_152 §9.1 item 3.

## realization (what exists on disk, 2026-09-03)

Home: `PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| locate_targets, rewrite | `ledger48.py`, driven by `canon38_wrapped.py` | done |
| locate_targets, rewrite, rewrite_external (the node's shape over `ledger.py`'s one text) | `canonical_form.Labels` | done, 2026-09-03 (log_162) |
| C6 | `canon38_gate.check_six` (in `canon38_gate.py`) | done |
| acceptance instance | `go/op_174` and `go/op_180`; assembled read-back in `canon38_assemble_go_op_174.txt` | done (log_152 §4.2, §4.4) |
| the collapse measured | over the 30,436 texts (log_152 §4.3) | done |
| superseded | `canon37_wrapped.py`, which carried unit-own addresses | superseded record |
