---
id: hq.research.interp_feeder.run_pipeline
level: 4
status: draft
supersedes: null
settled_by: the owner
designation: work
node:
    name: run_pipeline
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_11_interp_feeder/node_0_3_1_11_4_run_pipeline/CORE_0_3_1_11_4_run_pipeline.md
super_node:
    name: interp_feeder
    path: ../CORE_0_3_1_11_interp_feeder.md
sub_nodes: []
---

# CORE 0_3_1_11_4 — run_pipeline

## metadata

- **id:** hq.research.interp_feeder.run_pipeline
- **level:** 4
- **status:** draft
- **designation:** work
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [interp_feeder](../CORE_0_3_1_11_interp_feeder.md)

## sub_nodes

*(none yet)*

## definition

The lane that runs one interpreted language end to end: parse the
pilot's dump, format it to op_units, invoke the normalizer, and
leave the canonical records where the gate reads them. Runs as an
Airlock lane like every other step. As of 2026-09-06 it has been run
for java, cpython, php and ruby, producing the eleven units in
`canon40_interp.json`.
