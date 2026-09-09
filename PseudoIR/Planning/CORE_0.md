---
id: pir
level: 0
status: draft
settled_by: the owner
supersedes: null
nodes: [tools, research, hub]
super_node:
    name: projects
    path: PseudoCoupHQ/Planning/node_0_0_projects/CORE_0_0_projects.md
    repo: PseudoCoupHQ
    remote: https://github.com/<owner>/PseudoCoupHQ.git
---

# CORE 0 — PseudoIR

## metadata

- **id:** pir
- **level:** 0
- **status:** draft
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [projects](PseudoCoupHQ/Planning/node_0_0_projects/CORE_0_0_projects.md)

## sub_nodes

- [tools](node_0_0_tools/CORE_0_0_tools.md) — the things we build and run.
- [research](node_0_1_research/CORE_0_1_research.md) — what we learn and write down.
- [hub](node_0_2_hub/CORE_0_2_hub.md) — the disciplined python center.

## definition

the system the intention preserving hub is constructed with. it
connects languages at the ir level.

## the other project

*settled above this tree.* the exchange and the cycle are stated in
`PseudoCoupHQ/Planning/node_0_1_exchange/CORE_0_1_exchange.md`.
what follows in these two sections is this project's copy, kept
because a reader here needs it — but HQ is where it is settled, and
if this copy ever disagrees with HQ's, this copy is the one that is
wrong.

PseudoCoup is the tool to transpile from source languages into the
hub. the two projects exchange exactly two things:

- PseudoCoup gives PseudoIR a transpiler. PseudoIR has to get a
  compiler's source into hub source before it can slice it.
- PseudoIR gives PseudoCoup the hub. that is what PseudoCoup
  transpiles into.

that is the whole of the coupling. each project holds one artifact it
gives and one it receives, so neither tree contains a cycle.

## the cycle closes

a hub-less PseudoCoup builds the first PseudoIR. that PseudoIR builds
the hub. PseudoCoup can then use the hub, and the next PseudoIR is
built with that PseudoCoup. there the loop stops.

it stops because PseudoCoup targets the hub's SURFACE. once the
surface is fixed, improving what is behind it does not change what
PseudoCoup emits, so a new PseudoIR has no new PseudoCoup to produce.

churn restarts it. different intentions, or anything that moves the
surface, runs a full cycle again.

## grades

every construction step carries one:

- by hand: a person does it
- mechanized: a script does it, unattended
- mechanized, called by hand: a script does it, a person starts it

the three tools are meant to be nearly entirely automated, with
intention data as the input. progress reads off the plan as the count
of steps still marked by hand.
