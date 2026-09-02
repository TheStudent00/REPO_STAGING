---
id: pir.borders
level: 3
status: draft
settled_by: the owner
supersedes: null
nodes: []
---

# CORE 0_2_1_1 — borders

## metadata

- **id:** pir.borders
- **level:** 3
- **status:** draft
- **settled_by:** the owner
- **supersedes:** null

## super_node

*(none — tree root)*

## sub_nodes

*(none yet)*

## definition

how a value crosses into and out of a sliced region

a value inside a qualified region is a typed cell. unqualified
operators on it are refused. crossing outward is explicit, never
implicit coercion. the border lattice is the law; border code
implements it rather than re-deriving it.

faces both projects: emitted code and inserted slices assert the
same borders.

## support

- [SUPPORT_borders.md](SUPPORT_borders.md)
