---
id: pir.slice
level: 2
status: draft
settled_by: the owner
supersedes: null
nodes: []
---

# CORE 0_0_1 — slice

## metadata

- **id:** pir.slice
- **level:** 2
- **status:** draft
- **settled_by:** the owner
- **supersedes:** null

## super_node

*(none — tree root)*

## sub_nodes

*(none yet)*

## definition

extract the intention-bearing logic out of the transpiled compiler

in: the transpiled compiler, plus the intentions data. out: the slice
— the part of that compiler that decides the language's semantics.
runs the slicer.

the intentions data is what steers it. this is the stage that the
automation goal is really about: given intention data as input, the
selection should not need a person.

## support

- [SUPPORT_selection_and_extraction.md](SUPPORT_selection_and_extraction.md)
  — deciding what to cut, and executing the cut. the machinery; what
  is specific to a language lives under that language's run
- [SUPPORT_brainstorm.md](SUPPORT_brainstorm.md) — the owner's 2026-07-31
  idea for automating the selection by MEASURING it instead of
  judging it: detectors mapped into UR-AST nodes by the ledgerer, a
  compiler's own test suite as the driver, and the nodes that
  activate as the slice. unsettled; captured with its open questions,
  chief of which is whether an activation-derived slice closes
