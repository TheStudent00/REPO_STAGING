---
id: pir.surface
level: 3
status: draft
settled_by: the owner
supersedes: null
nodes: []
---

# CORE 0_2_1_2 — surface

## metadata

- **id:** pir.surface
- **level:** 3
- **status:** draft
- **settled_by:** the owner
- **supersedes:** null

## super_node

*(none — tree root)*

## sub_nodes

*(none yet)*

## definition

how hub source spells a qualified operation

`a r./ b` means divide with rust's exact semantics. the mechanism is
a parser-level fork of cpython where `r./` is a real token with real
precedence. the interim import-hook rewrite was dropped 2026-07-31.

this is the node the bootstrap cycle ends on. PseudoCoup emits
against this surface; when it stops moving, PseudoCoup stops needing
new versions.

## support

- [SUPPORT_surface.md](SUPPORT_surface.md)
