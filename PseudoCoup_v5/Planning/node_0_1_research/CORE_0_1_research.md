---
id: pcv5.research
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
    name: research
    path: Planning/node_0_1_research/CORE_0_1_research.md
---

# CORE 0_1 — research

## metadata

- **id:** pcv5.research
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

what was learned, and the data it produced

this version is where the PseudoCoup research is gathered, so this
node is unusually load-bearing for a research node: the material it
covers is the parts list the tools are composed from, not a side
inquiry.

## the research that is left

the gutting happened 2026-07-31. `<WORKSPACE_DIR>/PseudoCoup_v5/`
went from 550 MB to 55 MB. what went, and why:

- **vendored upstream compiler source, ~430 MB** — rustc and
  llvm-project trees fetched under `Research/`. not this project's
  work, and not in version control: `rust_routing/.gitignore`
  excluded `sources/` outright. the four files anything actually read
  are now vendored, with their provenance recorded, into
  `<WORKSPACE_DIR>/PseudoCoup_v6/Tools/ledgerer/fixtures/upstream/` and
  `<WORKSPACE_DIR>/PseudoCoup_v6/Tools/transpiler/fixtures/upstream/`.
  PCv6's suite passes without this repo present.
- **generated tables and build artifacts, ~100 MB** — LLVM's `.inc`
  tables and a compiled Rust harness. tracked, so recoverable from
  git.
- **`Designing/` and three unreferenced research folders** (historical)
  — the intentions table generators and the basis audit. tracked;
  the artifact they produced, `pc_verdicts.json`, was copied forward
  long ago and lives in `<WORKSPACE_DIR>/PseudoIR/Tools/intentions/`.

what remains under `Research/` is about 1.5 MB: `cpp_ingress`,
`divergence_suite`, `vocab_transpiler`'s python, and `rust_routing`'s
slice scripts. it is kept because the harvest map names some of it as
a source for the very rebuild this version is undergoing, and because
it is small. deleting it after the harvest is a live option.

## the surveys

the two 2026-07-27 surveys under
`<WORKSPACE_DIR>/PseudoCoup_v5/DevComms/` carry line-cited evidence for
every harvest claim. the condensed maps elsewhere drop the citations,
so a claim being acted on is checked here.

caution recorded with them: they predate both the purge and the
project split. at least one entry is void, and one describes a repo
about to be gutted. a reading list, not current state.
