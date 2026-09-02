---
id: pcv5.tools.transpiler
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
    name: transpiler
    path: Planning/node_0_0_tools/node_0_0_1_transpiler/CORE_0_0_1_transpiler.md
---

# CORE 0_0_1 — transpiler

## metadata

- **id:** pcv5.tools.transpiler
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

turns a compiler's source into hub source. runs the ledgerer.

tree-sitter is the parsing foundation, no exceptions without
extraordinary proof. generalize then specialize: tree-sitter
handling, the ledger, and most transpiler machinery overlap massively
across languages — generalize what overlaps, specialize only where a
language demands it (the owner).

ingest never guesses: it records `unresolvable` honestly, and the
consumers halt on it. built by composition from the lineage's best
parts — the harvest is mapped in
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_003_harvest_reminder.md` and
in detail in
`<WORKSPACE_DIR>/PseudoCoup_v5/DevComms/transpiler_survey_2026-07-27.md`.
