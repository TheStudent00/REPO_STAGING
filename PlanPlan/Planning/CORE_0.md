---
id: pp
level: 0
status: draft
settled_by: the owner
supersedes: null
designation: grouping
sub_nodes:
    - name: framework
      path: node_0_0_framework/CORE_0_0_framework.md
    - name: analysis
      path: node_0_1_analysis/CORE_0_1_analysis.md
    - name: instances
      path: node_0_2_instances/CORE_0_2_instances.md
super_node: null
node:
    name: pp
    path: Planning/CORE_0.md
    repo: PlanPlan
    remote: https://github.com/<owner>/PlanPlan.git
---

# CORE 0 — PlanPlan

## sub_nodes

- [framework](node_0_0_framework/CORE_0_0_framework.md) — the planning framework: the protocol, the document grammar, the metadata schema, and the tools that enforce them.
- [analysis](node_0_1_analysis/CORE_0_1_analysis.md) — tools for analysing the version-control histories and file structures of conforming projects, and for extracting planning instances into the dataset.
- [instances](node_0_2_instances/CORE_0_2_instances.md) — extracted planning snapshots from conforming projects, the raw material of the ontology-evolution study.

## definition

the study of ontology evolution in research project development, and
the home of the planning framework projects conform to

*(definition drawn from this repo's `README.md`, not settled by the owner.
the wording, the node names and the count are all his to keep or
cut.)*

## why this tree exists

it was missing until 2026-08-01. the owner, that day:

> and why doesnt PlanPlan use its own framework? there are tools
> and research and whatever the fuck. idk why its completely missing
> it.

no exemption was ever recorded — `PROTOCOL.md` and `README.md` were
both searched and neither says the framework does not apply here.
the closest thing to a cause is §6's wording, which puts PlanPlan
on one side and "conforming projects" on the other:

> The framework is a template, not a dependency: conforming
> projects copy the conventions; PlanPlan later EXTRACTS
> instances from their VCS histories for the ontology-evolution
> dataset.

that sentence never says PlanPlan is exempt. it just never counts
it as a candidate.

## the node names come from the README

the three nodes above are this repo's own three areas, quoted from
`README.md` under "What lives here". two of them do not exist on
disk: there is no `analysis/` and no `instances/` folder today.

that is the point of the tree. unbuilt work with no plan is the
condition the framework exists to prevent, and it was sitting in the
framework's own repo.
