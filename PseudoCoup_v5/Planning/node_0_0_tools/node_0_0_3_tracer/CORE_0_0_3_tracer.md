---
id: pcv5.tools.tracer
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (object)
sub_nodes: []
super_node:
    name: tools
    path: ../CORE_0_0_tools.md
node:
    name: tracer
    path: Planning/node_0_0_tools/node_0_0_3_tracer/CORE_0_0_3_tracer.md
---

# CORE 0_0_3 — tracer

## metadata

- **id:** pcv5.tools.tracer
- **level:** 2
- **status:** draft
- **designation:** code (object)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [tools](../CORE_0_0_tools.md)

## sub_nodes

*(none yet)*

## definition

the runtime tracer: instruments transpiled code so execution reports
itself in ledger ids.

two parts, both found in the lineage (the owner, 2026-07-31):

- a **global tracer** called from inside instrumented nodes with that
  node's id.
- the tree-sitter driven **injector** that places those calls — what
  makes instrumentation mechanical rather than hand-written, and the
  larger of the two.

a sibling of the ledgerer, not a part of it (the owner, 2026-08-01), keyed
on the same positional-path ids — it is how the ledger's runtime axis
gets its data. detail and inherited hazards in
`PseudoIR/Planning/node_0_0_tools/node_0_0_1_slice/SUPPORT_brainstorm.md`.
