---
id: hq.research.interp_feeder.target
level: 4
status: draft
supersedes: null
settled_by: the owner
designation: rule
node:
    name: target
    path: Planning/node_0_3_research/node_0_3_1_operator_equivalence/node_0_3_1_11_interp_feeder/node_0_3_1_11_6_target/CORE_0_3_1_11_6_target.md
super_node:
    name: interp_feeder
    path: ../CORE_0_3_1_11_interp_feeder.md
sub_nodes: []
---

# CORE 0_3_1_11_6 — target

## metadata

- **id:** hq.research.interp_feeder.target
- **level:** 4
- **status:** draft
- **designation:** rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [interp_feeder](../CORE_0_3_1_11_interp_feeder.md)

## sub_nodes

*(none yet)*

## definition

Which build of each interpreter is read, so a unit is attributed to a
named binary and not to "php": the instrumented php builds
(`Airlock/php-{7.4.33,8.2.13,8.3.0}.tar.gz`), the
instrumented ruby 3.3.0 build, the image's cpython and openjdk 25.
The target is recorded on every unit; a body from a different build
is a different unit.
