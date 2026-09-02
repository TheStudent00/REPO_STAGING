---
id: pp.framework.tools
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: grouping
sub_nodes:
    - name: check_plans
      path: node_0_0_3_0_check_plans/CORE_0_0_3_0_check_plans.md
    - name: render_plan
      path: node_0_0_3_1_render_plan/CORE_0_0_3_1_render_plan.md
    - name: generate_nodes
      path: node_0_0_3_2_generate_nodes/CORE_0_0_3_2_generate_nodes.md
    - name: generate_dashboards
      path: node_0_0_3_3_generate_dashboards/CORE_0_0_3_3_generate_dashboards.md
    - name: migrate
      path: node_0_0_3_4_migrate/CORE_0_0_3_4_migrate.md
    - name: explorer
      path: node_0_0_3_5_explorer/CORE_0_0_3_5_explorer.md
node:
    name: tools
    path: Planning/node_0_0_framework/node_0_0_3_tools/CORE_0_0_3_tools.md
super_node:
    name: framework
    path: ../CORE_0_0_framework.md
---

# CORE 0_0_3 — tools

## sub_nodes

- [check_plans](node_0_0_3_0_check_plans/CORE_0_0_3_0_check_plans.md) — runs every check over one or more trees and reports by cause; exits 1 on errors.
- [render_plan](node_0_0_3_1_render_plan/CORE_0_0_3_1_render_plan.md) — writes one tree as one self-contained HTML page.
- [generate_nodes](node_0_0_3_2_generate_nodes/CORE_0_0_3_2_generate_nodes.md) — realizes the `nodes` register: creates registered-but-missing node folders with skeleton files, rebuilds `## nodes` projections (`--projections`), and writes registers into trees that predate them (`--adopt`).
- [generate_dashboards](node_0_0_3_3_generate_dashboards/CORE_0_0_3_3_generate_dashboards.md) — writes every node's `DASHBOARD.md` rollup, deterministically — two runs are byte-identical.
- [migrate](node_0_0_3_4_migrate/CORE_0_0_3_4_migrate.md) — applies one named change across every repo that uses the framework — addresses, filename grammar, section headings — as one dry-runnable operation rather than a hand pass over hundreds of files.
- [explorer](node_0_0_3_5_explorer/CORE_0_0_3_5_explorer.md) — a card explorer for one planning tree: one card per node, clicked open in place to reveal that node's files and its sub-node cards, indented.

## definition

the callable entry points. anything in this repo that is a callable
object is a tool (the owner, 2026-08-01); each is thin — the substance
lives in `planning_model` and `checks`.
