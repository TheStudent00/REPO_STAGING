---
id: hq.exchange
level: 1
status: draft
settled_by: the owner
supersedes: null
designation: rule
sub_nodes: []
super_node:
    name: hq
    path: ../CORE_0.md
node:
    name: exchange
    path: Planning/node_0_1_exchange/CORE_0_1_exchange.md
---

# CORE 0_1 — exchange

## metadata

- **id:** hq.exchange
- **level:** 1
- **status:** draft
- **designation:** rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [hq](../CORE_0.md)

## sub_nodes

*(none yet)*

## definition

what crosses between PseudoCoup and PseudoIR, and why the bootstrap
cycle stops. this is the settled statement; the project plans state
it too, as dependents of this one.

## exactly two things cross

- PseudoCoup gives PseudoIR a **transpiler**. PseudoIR has to get a
  compiler's source into hub source before it can slice it.
- PseudoIR gives PseudoCoup the **hub**. that is what PseudoCoup
  transpiles into.

that is the whole of the coupling. each project holds one artifact
it gives and one it receives, so neither tree contains a cycle.

wanting a third thing to cross is the signal that the split is being
violated. it is raised with the owner, not reached across.

settled 2026-07-31: the transpiler that crosses is the **Frankenstein
transpiler**, and the ledgerer it runs is the **Frankenstein
ledgerer**. PseudoIR builds neither of its own.

## the cycle closes

a hub-less PseudoCoup builds the first PseudoIR. that PseudoIR
builds the hub. PseudoCoup can then use the hub, and the next
PseudoIR is built with that PseudoCoup. there the loop stops.

it stops because PseudoCoup targets the hub's SURFACE. once the
surface is fixed, improving what is behind it does not change what
PseudoCoup emits, so a new PseudoIR has no new PseudoCoup to
produce.

churn restarts it. different intentions, or anything that moves the
surface, runs a full cycle again.

## where the hub is described

in PseudoIR's plan and only there. PseudoCoup deliberately carries no
second description of it, and HQ does not either — what is above is
the COUPLING, not the hub. a description of the hub growing in this
file would be the same duplication this node was made to end.

## the dependency rule

the project plans may state the two sections above (the owner,
2026-07-31). when they do, they state them as dependents: this node
is where they are settled, and a project copy that disagrees with
this one is the project's error to correct. that follows the
framework's governance rule — a sub-document may refine its
super-document, never contradict it.
