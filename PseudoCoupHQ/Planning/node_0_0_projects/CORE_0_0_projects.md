---
id: hq.projects
level: 1
status: draft
settled_by: the owner
supersedes: null
designation: grouping
node:
    name: projects
    path: Planning/node_0_0_projects/CORE_0_0_projects.md
super_node:
    name: hq
    path: ../CORE_0.md
sub_nodes:
    - name: pcv5
      path: PseudoCoup_v5/Planning/CORE_0.md
      repo: PseudoCoup_v5
      remote: https://github.com/<owner>/PseudoCoup_v5.git
    - name: pcv6
      path: PseudoCoup_v6/Planning/CORE_0.md
      repo: PseudoCoup_v6
      remote: https://github.com/<owner>/PseudoCoup_v6.git
    - name: pseudoir
      path: PseudoIR/Planning/CORE_0.md
      repo: PseudoIR
      remote: https://github.com/<owner>/PseudoIR.git
---

# CORE 0_0 — projects

## metadata

- **id:** hq.projects
- **level:** 1
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [hq](../CORE_0.md)

## sub_nodes

*(none yet)*

## definition

what each repo in the line is, and what stage it is at. one entry
per repo, short enough that the roster stays current.

detail lives in each project's own plan; this node exists so that a
reader arriving at the line for the first time knows which repos
exist and which are live before opening any of them.

## PseudoCoup, version 5 — `PseudoCoup_v5`

being gutted and rebuilt (the owner, 2026-07-31). the PseudoCoup research
is gathered and composed into **Frankenstein tools** — built from the
best parts already scattered across the lineage rather than written
fresh — and those become version 5. PseudoIR then uses them.

its tools node names four: ledgerer, transpiler, polyfill, tracer
(the owner, 2026-08-01, when the tracer was settled as a sibling of the
ledgerer). *(this entry said "those two become version 5", naming
only the transpiler and ledgerer, which was the state before that
ruling.)* the detail is
`PseudoCoup_v5/Planning/node_0_0_tools/CORE_0_0_tools.md`;
this roster stays a pointer, so the count lives there.

gutting is safe because the VCS tracks the research. references to
material from before the gutting are annotated
`PCv5-archived-research`, meaning: exists in version control, not in
the current tree.

recorded in
`PseudoCoup_v6/AgentMemory/02_decisions.md` under
Direction, superseding the 2026-07-28 decision that PCv5 was
archived research.

**Version 5 is the basis for version 6, and version 6's decisions
wait on it** (the owner, 2026-07-31): "we can hold off on PCv6 decisions
until weve completed PCv5 — unless something comes up in brainstorming
or whatever and we want to update it." So a question of the form "does
this move to PCv5 / how does PCv6 change" is not an open item; it is
work that happens after.

## PseudoCoup, version 6 — `PseudoCoup_v6`

the tool to transpile from source languages into the hub. plan at
`PseudoCoup_v6/Planning/CORE_0.md`. holds three tools
today: ledgerer, transpiler, polyfill.

## PseudoIR — `PseudoIR`

the system the hub is constructed with; connects languages at the ir
level. plan at `PseudoIR/Planning/CORE_0.md`. holds
three tools today: transpile, slice, insert — one per stage.

*(corrected 2026-08-01: this entry read "two tools today: insert,
intentions". both halves were wrong from the day it was written —
PseudoIR's tools node has named three tools since 2026-07-31, and
`intentions` is a sub-node of its research node, not a tool.)*

## the open cross-cutting fact

PseudoCoup_v6's test suite does not pass without PseudoCoup_v5 on
disk: six tests resolve vendored upstream rustc source through
`PCV5_ROOT`. that source is upstream rustc, not a PCv5 artifact, and
it happens to live under PCv5's tree. the gutting turns "vendor
those sources into PCv6" from cleanup into a precondition. tracked
in this node's PROGRESS.
