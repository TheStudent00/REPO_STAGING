---
id: pp.framework.tools.generate_dashboards
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
nodes: []
node:
    name: generate_dashboards
    path: Planning/node_0_0_framework/node_0_0_3_tools/node_0_0_3_3_generate_dashboards/CORE_0_0_3_3_generate_dashboards.md
super_node:
    name: tools
    path: ../CORE_0_0_3_tools.md
sub_nodes: []
---

# CORE 0_0_3_3 — generate_dashboards

## sub_nodes

*(none yet)*

## definition

writes every node's `DASHBOARD.md` rollup, deterministically —
two runs are byte-identical. `--check` writes nothing and exits 1 if
any dashboard is stale.
