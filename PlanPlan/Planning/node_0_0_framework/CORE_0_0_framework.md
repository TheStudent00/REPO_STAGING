---
id: pp.framework
level: 1
status: draft
settled_by: the owner
supersedes: null
designation: grouping
sub_nodes:
    - name: protocol
      path: node_0_0_0_protocol/CORE_0_0_0_protocol.md
    - name: planning_model
      path: node_0_0_1_planning_model/CORE_0_0_1_planning_model.md
    - name: checks
      path: node_0_0_2_checks/CORE_0_0_2_checks.md
    - name: tools
      path: node_0_0_3_tools/CORE_0_0_3_tools.md
node:
    name: framework
    path: Planning/node_0_0_framework/CORE_0_0_framework.md
super_node:
    name: pp
    path: ../CORE_0.md
---

# CORE 0_0 — framework

## sub_nodes

- [protocol](node_0_0_0_protocol/CORE_0_0_0_protocol.md) — the rules document itself — `framework/PROTOCOL.md`: the grammar, the governance, the metadata schema, and every settled ruling with its date.
- [planning_model](node_0_0_1_planning_model/CORE_0_0_1_planning_model.md) — the shared model of a planning tree, read from disk once and used by every tool: `PlanningNode` and `PlanningTree`.
- [checks](node_0_0_2_checks/CORE_0_0_2_checks.md) — one rule, one object: `Check` sub-classes, each carrying its own name and severity, and the `Checker` that runs a list of them.
- [tools](node_0_0_3_tools/CORE_0_0_3_tools.md) — the callable entry points.

## definition

the planning framework: the protocol, the document grammar, the
metadata schema, and the tools that enforce them

*(drawn from `README.md`'s "What lives here", not settled by the owner.
`designation` deliberately absent — the judgement is made by hand
when the definition is settled.)*

## dependency direction

nothing depends on the visualization. `planning_model` depends on
nothing; `checks` depends on `planning_model`; the tools use both;
`render_plan` is imported by nobody.

the code matches since 2026-08-01: the restructure moved the grammar
checks out of `render_plan.py` into `checks.py` over the shared
`planning_model.py`, behaviour pinned before and after by the
planted-defect captures. record in this node's PROGRESS.

## notes

everything is standard library only. `install_silverbullet.sh` was
archived 2026-08-01 to
`framework/.archive/install_silverbullet_superseded_2026-07-31/`.
readiness defects are recorded with evidence in
`<WORKSPACE_DIR>/PlanPlan/DevComms/log_001_readiness_and_tree.md`.
