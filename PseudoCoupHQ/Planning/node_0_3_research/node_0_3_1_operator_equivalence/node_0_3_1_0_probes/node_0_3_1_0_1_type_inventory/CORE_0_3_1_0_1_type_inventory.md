---
id: hq.research.compiler_graph.probes.type_inventory
level: 4
status: draft
supersedes: null
settled_by: the owner
supersedes: null
designation: code (attribute)
node:
    name: type_inventory
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_0_probes/node_0_3_1_0_1_type_inventory/CORE_0_3_1_0_1_type_inventory.md
super_node:
    name: probes
    path: ../CORE_0_3_1_0_probes.md
sub_nodes: []
---

# CORE 0_3_1_0_1 — type_inventory

## metadata

- **id:** hq.research.compiler_graph.probes.type_inventory
- **level:** 4
- **status:** draft
- **designation:** code (attribute)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [probes](../CORE_0_3_1_0_probes.md)

## sub_nodes

*(none yet)*

## definition

Per language, the list of every type this target actually accepts in a
declaration — one of the two axes the probe grid is built from. Each
candidate is extracted from the compiler's own type vocabulary and then
WITNESSED: a one-line program declaring that type is compiled on this
machine, and the candidate is kept only when the compiler accepts it.
The witness step demoted 85 of 208 candidates, meaning it dropped them
from the accepted list. Nothing in the list is typed by hand.

## design

```
probes.type_inventory
	attributes:
		accepted_types
			"""
			per language, one entry per type the
			compiler accepted in a declaration:
			the spelling written into the probe
			source, and the machine facts DWARF
			reports for it (encoding + width)
			"""
		demoted_types
			"""
			candidates the witness compile
			refused, kept with the compiler's
			own refusal text
			"""
	methods:
		extract
			"""
			read the compiler's own type
			vocabulary into candidates
			"""
		witness
			"""
			compile a one-line declaration per
			candidate in an Airlock instance;
			accept or demote on the result
			"""
```

## settled rules

- **Type inventories are extracted, never hand-written.** Decision:
  [probes](../CORE_0_3_1_0_probes.md) settled rules, citing
  AgentMemory round 9 (log_137).
- **A candidate is kept only when it is witnessed declarable on this
  target with this toolchain**; 85 of 208 were demoted on that
  witness. Decision: [probes](../CORE_0_3_1_0_probes.md) realization
  table, 2026-09-03.
- **Typing is by machine fact — DWARF encoding and width — never by a
  declared type name.** The accepted spelling is what the probe source
  writes; it is not the key anything downstream joins on. Decision:
  [arch_unit](../../node_0_3_1_1_arch_unit/CORE_0_3_1_1_arch_unit.md)
  settled rules (AgentMemory, log_074 audit).

## realization (what exists on disk, 2026-09-03)

Home: `~/Programming/PseudoCoupHQ/Research/op_pipeline/`.

| part | current file | status |
|---|---|---|
| accepted_types | `type_inventory3.json` (extracted and declarable) | done |
| extract, witness | `type_inventory3.py` | done |
| earlier witness runs | `type_inventory_validate.py`, `type_inventory2_validate.py`, `type_inventory2_validation.json` | superseded records |
| earlier inventories | `type_inventory.json`, `type_inventory2.json` | superseded records |
