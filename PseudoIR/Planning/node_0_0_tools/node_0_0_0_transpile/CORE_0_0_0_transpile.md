---
id: pir.transpile
level: 2
status: draft
settled_by: the owner
supersedes: null
nodes: []
---

# CORE 0_0_0 — transpile

## metadata

- **id:** pir.transpile
- **level:** 2
- **status:** draft
- **settled_by:** the owner
- **supersedes:** null

## super_node

*(none — tree root)*

## sub_nodes

*(none yet)*

## definition

convert the source compiler into hub python

in: a compiler's source, in language x. out: the same compiler as hub
source. runs the transpiler, which runs the ledgerer.

nothing is selected or discarded here. this stage moves the whole
compiler across; deciding what matters is the next stage.

## notes

this is where PseudoIR borrows PseudoCoup's transpiler. settled by
the owner 2026-07-31: the transpiler it borrows is the **Frankenstein
transpiler** — composed from the best parts across the PseudoCoup
lineage — and the ledgerer it runs is the Frankenstein ledgerer.
PseudoIR does not build a transpiler of its own.

neither Frankenstein exists yet. building them is the PCv5 rebuild:
`~/Programming/PseudoCoup_v5/` is gutted and commandeered as PCv6's
precursor, and the two composed tools become version 5. the parts
list is
`~/Programming/PseudoCoup_v6/AgentMemory/03_lineage_and_harvest.md`;
the decision is in that repo's `AgentMemory/02_decisions.md` under
Direction.

still open here: what the first run transpiles INTO. there is no hub
to target on the first pass. the working theory is that the
dependency is on the hub's surface rather than its contents, so a
stub surface suffices. unproven.

what is specific to rustc lives under the rust_llvm run, not here.
