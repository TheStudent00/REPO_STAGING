---
id: pcv5.tools.ledgerer
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: ledgerer
    path: Planning/node_0_0_tools/node_0_0_0_ledgerer/CORE_0_0_0_ledgerer.md
super_node:
    name: tools
    path: ../CORE_0_0_tools.md
sub_nodes:
    - name: ur
      path: node_0_0_0_0_ur/CORE_0_0_0_0_ur.md
    - name: ledger
      path: node_0_0_0_1_ledger/CORE_0_0_0_1_ledger.md
    - name: ts_to_ur
      path: node_0_0_0_2_ts_to_ur/CORE_0_0_0_2_ts_to_ur.md
    - name: ur_to_ledger
      path: node_0_0_0_3_ur_to_ledger/CORE_0_0_0_3_ur_to_ledger.md
    - name: builder
      path: node_0_0_0_4_builder/CORE_0_0_0_4_builder.md
---

# CORE 0_0_0 — ledgerer

## metadata

- **id:** pcv5.tools.ledgerer
- **level:** 2
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [tools](../CORE_0_0_tools.md)

## sub_nodes

- [ur](node_0_0_0_0_ur/CORE_0_0_0_0_ur.md) — Universal Rich AST definitions — the abstraction of the FORM of a parsed source, as `ledger` is the abstraction of the stored data structure (the owner, 2026-08-02).
- [ledger](node_0_0_0_1_ledger/CORE_0_0_0_1_ledger.md) — ledger definitions — how the ledger is standardized: the record shape, the keying, the registries, the divergence vocabulary, the `unresolvable` posture.
- [ts_to_ur](node_0_0_0_2_ts_to_ur/CORE_0_0_0_2_ts_to_ur.md) — maps Tree-Sitter to UR.
- [ur_to_ledger](node_0_0_0_3_ur_to_ledger/CORE_0_0_0_3_ur_to_ledger.md) — derives ledger entries, in `ledger`'s registration forms, from a UR tree; creates the type-connected nodes.
- [builder](node_0_0_0_4_builder/CORE_0_0_0_4_builder.md) — the ledgerer's operational funnel: ledgerer calls route through the builder, which runs source → UR → ledger end to end.

## definition

records every node of a parsed source, keyed by positional-path id.

the ledger is ONE record across three axes — semantic, structural,
runtime — not separate ledgers joined afterwards (the owner, 2026-07-28).
the id is a runtime-observable signal: per-call-site positional-path
id plus a per-instance key, emitted identically into every transpiled
side, joined by id equality.

an independent tool: PseudoCoup is a module of tools, and the ledger
stands on its own. built by composition from the lineage's best
parts — the harvest is mapped in
`~/Programming/PseudoCoupHQ/DevComms/log_003_harvest_reminder.md` and
in detail in
`~/Programming/PseudoCoup_v5/DevComms/ledger_survey_2026-07-27.md`.

## support

- [SUPPORT_metaprogramming.md](SUPPORT_metaprogramming.md) — how code
  that writes code is modelled: representation always, evaluation
  separately, with Rust as the first target.
