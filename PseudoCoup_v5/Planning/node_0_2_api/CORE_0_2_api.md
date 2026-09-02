---
id: pcv5.api
level: 1
status: draft
settled_by: the owner
supersedes: null
designation: grouping
sub_nodes: []
super_node:
    name: pcv5
    path: ../CORE_0.md
node:
    name: api
    path: Planning/node_0_2_api/CORE_0_2_api.md
---

# CORE 0_2 — api

## metadata

- **id:** pcv5.api
- **level:** 1
- **status:** draft
- **designation:** grouping
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [pcv5](../CORE_0.md)

## sub_nodes

*(none yet)*

## definition

the callable things — what someone outside this repo invokes to get a
source converted

this version has exactly one caller: PseudoIR, which needs a
compiler's source turned into hub source before it can slice it. so
the surface here is narrower than a later version's, which also has
to serve people converting ordinary programs.

## what this version's api is NOT

it does not offer application-program conversion. not because it is
unbuilt, but because there is nothing to convert INTO — this
version's `hub/` is inert. that capability arrives with the hub, in
the next turn of the cycle, and belongs to that version's api node.
