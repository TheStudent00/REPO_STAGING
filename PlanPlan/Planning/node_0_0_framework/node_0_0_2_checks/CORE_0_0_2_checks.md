---
id: pp.framework.checks
level: 2
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
sub_nodes: []
node:
    name: checks
    path: Planning/node_0_0_framework/node_0_0_2_checks/CORE_0_0_2_checks.md
super_node:
    name: framework
    path: ../CORE_0_0_framework.md
---

# CORE 0_0_2 — checks

## sub_nodes

*(none yet)*

## definition

one rule, one object: `Check` sub-classes, each carrying its own name
and severity, and the `Checker` that runs a list of them. depends on
`planning_model` only.

built 2026-08-01 as `framework/checks.py`, in the restructure that
ended the checker's import from the viewer. one class per rule:
GrammarCheck, DanglingPathCheck, DuplicateProseCheck,
IdCollisionCheck, RequiredFilesCheck, NodesRegisterCheck,
ProjectionCheck, DesignationCheck, CompletenessCheck.
