---
id: pir.hub
level: 1
status: draft
settled_by: the owner
supersedes: null
nodes: [construction, assembly]
---

# CORE 0_2 — hub

## metadata

- **id:** pir.hub
- **level:** 1
- **status:** draft
- **settled_by:** the owner
- **supersedes:** null

## super_node

*(none — tree root)*

## sub_nodes

- [construction](node_0_2_0_construction/CORE_0_2_0_construction.md) — getting a language's semantics into the hub, one language at a time.
- [assembly](node_0_2_1_assembly/CORE_0_2_1_assembly.md) — the hub's own machinery.

## definition

the disciplined python center. all 12 languages (and potentially
more) convert into it without violating the intentions of the source
scripts, and it satisfies those intentions.

## notes

what this project produces. PseudoCoup transpiles into it.

the hub is the contract between the two projects, so it is described
here and only here. PseudoCoup does not carry a second description of
it; what PseudoCoup carries is what its transpiler must emit, which
is a fact about the transpiler.

the surface is the part that ends the bootstrap cycle. once it is
fixed, PseudoCoup stops needing new versions.

## support

- [SUPPORT_hub.md](SUPPORT_hub.md) — standing constraints and
  sequencing, from the previous plan
