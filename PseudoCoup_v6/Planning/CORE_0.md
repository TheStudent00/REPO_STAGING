---
id: pcv6
level: 0
status: draft
settled_by: the owner
supersedes: pcv6.planning
nodes: [tools, research, api]
super_node:
    name: projects
    path: PseudoCoupHQ/Planning/node_0_0_projects/CORE_0_0_projects.md
    repo: PseudoCoupHQ
    remote: https://github.com/<owner>/PseudoCoupHQ.git
---

# CORE 0 — PseudoCoup

## metadata

- **id:** pcv6
- **level:** 0
- **status:** draft
- **settled_by:** the owner
- **supersedes:** pcv6.planning

## super_node

- [projects](PseudoCoupHQ/Planning/node_0_0_projects/CORE_0_0_projects.md)

## sub_nodes

- [tools](node_0_0_tools/CORE_0_0_tools.md) — the things we build and run.
- [research](node_0_1_research/CORE_0_1_research.md) — what we learn and write down.
- [api](node_0_2_api/CORE_0_2_api.md) — the callable surface.

## definition

the tool to transpile from source languages into the intention
preserving hub

## the other project

*settled above this tree.* the exchange and the cycle are stated in
`PseudoCoupHQ/Planning/node_0_1_exchange/CORE_0_1_exchange.md`.
what follows in these two sections is this project's copy, kept
because a reader here needs it — but HQ is where it is settled, and
if this copy ever disagrees with HQ's, this copy is the one that is
wrong.

the hub was constructed using PseudoIR. its plan is at
`PseudoIR/Planning`. the two projects exchange exactly
two things:

- PseudoCoup gives PseudoIR a transpiler. PseudoIR has to get a
  compiler's source into hub source before it can slice it.
- PseudoIR gives PseudoCoup the hub. that is what PseudoCoup
  transpiles into.

the hub is described in PseudoIR's plan and only there. what belongs
here is what this project's transpiler must emit against the hub's
surface — a fact about the transpiler, not a second copy of the hub.

## the cycle closes

a hub-less PseudoCoup builds the first PseudoIR. that PseudoIR builds
the hub. PseudoCoup can then use the hub, and the next PseudoIR is
built with that PseudoCoup. there the loop stops.

it stops because this project targets the hub's SURFACE. once the
surface is fixed, improving what is behind it does not change what
PseudoCoup emits, so a new PseudoIR has no new PseudoCoup to produce.

churn restarts it. different intentions, or anything that moves the
surface, runs a full cycle again.

## project goals

**intermediate**: to ingress scripts into the Hub.

**ultimate**: to ingress into the Hub and egress scripts out of the
Hub.

*(the owner's words, 2026-07-31, replacing the previous pair — "greatest
amount of automation of transpiling and slicing of languages" and
"Rust (LLVM) transpiling and slicing". Those were carried here from
the PCv5-era frame and are about transpiling AND SLICING, which is
PseudoIR's work rather than this project's. They belong to PseudoIR
more than to PseudoCoup; moving them there is the owner's call and has not
been done.)*
