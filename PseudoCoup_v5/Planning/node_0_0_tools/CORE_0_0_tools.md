---
id: pcv5.tools
level: 1
status: draft
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: tools
    path: Planning/node_0_0_tools/CORE_0_0_tools.md
super_node:
    name: pcv5
    path: ../CORE_0.md
sub_nodes:
    - name: ledgerer
      path: node_0_0_0_ledgerer/CORE_0_0_0_ledgerer.md
    - name: transpiler
      path: node_0_0_1_transpiler/CORE_0_0_1_transpiler.md
    - name: polyfill
      path: node_0_0_2_polyfill/CORE_0_0_2_polyfill.md
    - name: tracer
      path: node_0_0_3_tracer/CORE_0_0_3_tracer.md
---

# CORE 0_0 — tools

## metadata

- **id:** pcv5.tools
- **level:** 1
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [pcv5](../CORE_0.md)

## sub_nodes

- [ledgerer](node_0_0_0_ledgerer/CORE_0_0_0_ledgerer.md) — records every node of a parsed source, keyed by positional-path id.
- [transpiler](node_0_0_1_transpiler/CORE_0_0_1_transpiler.md) — turns a compiler's source into hub source.
- [polyfill](node_0_0_2_polyfill/CORE_0_0_2_polyfill.md) — wrappers that make the hub match the source language's behaviour.
- [tracer](node_0_0_3_tracer/CORE_0_0_3_tracer.md) — the runtime tracer: instruments transpiled code so execution reports itself in ledger ids.

## definition

the four tools this version is built from, each composed from the
best parts across the lineage rather than written fresh or ported
whole

## the harvest

what each tool is made of is the harvest, mapped in
`PseudoCoupHQ/DevComms/log_003_harvest_reminder.md`
and in detail in the two 2026-07-27 surveys under
`PseudoCoup_v5/DevComms/`.
