---
id: pcv5
level: 0
status: draft
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: pcv5
    path: Planning/CORE_0.md
    repo: PseudoCoup_v5
    remote: https://github.com/<owner>/PseudoCoup_v5.git
super_node:
    name: projects
    path: PseudoCoupHQ/Planning/node_0_0_projects/CORE_0_0_projects.md
    repo: PseudoCoupHQ
    remote: https://github.com/<owner>/PseudoCoupHQ.git
sub_nodes:
    - name: tools
      path: node_0_0_tools/CORE_0_0_tools.md
    - name: research
      path: node_0_1_research/CORE_0_1_research.md
    - name: api
      path: node_0_2_api/CORE_0_2_api.md
---

# CORE 0 — PseudoCoup version 5

## metadata

- **id:** pcv5
- **level:** 0
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [projects](PseudoCoupHQ/Planning/node_0_0_projects/CORE_0_0_projects.md)

## sub_nodes

- [tools](node_0_0_tools/CORE_0_0_tools.md) — the four tools this version is built from, each composed from the best parts across the lineage rather than written fresh or ported whole.
- [research](node_0_1_research/CORE_0_1_research.md) — what was learned, and the data it produced.
- [api](node_0_2_api/CORE_0_2_api.md) — the callable things — what someone outside this repo invokes to get a source converted.

## definition

the turn of the cycle where the hub is still empty

*(confirmed by the owner, 2026-07-31.)*

## project goal

**to support the transpilation of compilers**, with respect to
constructing and upgrading a hub.

a PCv{N} is capable of transpiling code in general. this version's
work is in service of PseudoIR — that is a statement about what it is
FOR right now, not about what it can do.

*(the owner's words, 2026-07-31.)*

## what makes a version

versions of PseudoCoup are turns of the bootstrap cycle, not different
products. the cycle is settled at
`PseudoCoupHQ/Planning/node_0_1_exchange/CORE_0_1_exchange.md`
and that is where it is stated; what belongs here is only which turn
this is.

the discriminator is the hub. version 5's `hub/` is inert. the next
version's is the hub PseudoIR built.

## the hub is not described here

`hub/` in this repo holds the artifact. the hub is DESCRIBED in
PseudoIR's plan and only there. a description of it must not grow in
this tree — that is the duplication the split exists to prevent.
