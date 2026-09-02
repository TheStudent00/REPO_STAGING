---
id: pp.framework.tools.generate_nodes
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
nodes: []
node:
    name: generate_nodes
    path: Planning/node_0_0_framework/node_0_0_3_tools/node_0_0_3_2_generate_nodes/CORE_0_0_3_2_generate_nodes.md
super_node:
    name: tools
    path: ../CORE_0_0_3_tools.md
sub_nodes: []
---

# CORE 0_0_3_2 — generate_nodes

## sub_nodes

*(none yet)*

## definition

realizes the `nodes` register: creates registered-but-missing node
folders with skeleton files, rebuilds `## nodes` projections
(`--projections`), and writes registers into trees that predate them
(`--adopt`). dry run unless `--apply`.
