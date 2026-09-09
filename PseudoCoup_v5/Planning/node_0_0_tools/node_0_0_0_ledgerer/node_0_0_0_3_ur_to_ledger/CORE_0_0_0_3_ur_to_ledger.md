---
id: pcv5.tools.ledgerer.ur_to_ledger
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: ur_to_ledger
    path: Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_3_ur_to_ledger/CORE_0_0_0_3_ur_to_ledger.md
super_node:
    name: ledgerer
    path: ../CORE_0_0_0_ledgerer.md
sub_nodes: []
---

# CORE 0_0_0_3 — ur_to_ledger

## metadata

- **id:** pcv5.tools.ledgerer.ur_to_ledger
- **level:** 3
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [ledgerer](../CORE_0_0_0_ledgerer.md)

## sub_nodes

*(none yet)*

## definition

derives ledger entries, in `ledger`'s registration forms, from a UR
tree; creates the type-connected nodes. lossless: every UR fact that
the ledger's forms can carry arrives; what cannot is recorded, never
dropped (the owner, 2026-08-02, extracted from the builder as the
counterpart of `ts_to_ur`).

a DERIVER, not a format converter: its input is language-neutral UR,
and its work is producing facts and connections that are not literal
in the parse — definition↔instance links, type connections, and
nodes for things the file never defines.

## harvest

which Frankenstein parts land here. part numbers are
`~/Programming/PseudoCoup_v5/DevComms/log_001_ledgerer_harvest_findings.md`
§2. placements are draft commentary, not settled.

- **the derivation this node performs is the survey's "re-key the
  registries onto ids" made mechanical**: the semantic facts (part
  2.3's registry content) are read off UR nodes — which carry id,
  span, and source linkage per `ur`'s strictly-richer rule — and
  written as `ledger` entries keyed by those ids. the one-moment
  problem of the survey addendum (§2.5) does not reach this node:
  its input already carries the linkage.
- **2.9 registry linkage — the writing half.** the entry form is
  `ledger`'s; putting the link INTO a divergence entry (resolving
  "why does this node diverge" to a confirmed lowering with
  evidence) is derivation work, so it moved here when this node was
  extracted from the builder (2026-08-02). no existing code; design.
- **the abstract-node cases** — the owner's worked instances of the
  ledger's carrying capacity land here as behavior: a parameter
  whose type is built-in and undefined in the file gets an ABSTRACT
  NODE for the to-be wrapper, with the instance connected to it; a
  parameter defined in the file gets the definition↔instance
  connector. this node writes both. these generated nodes are what
  give the transpiler (or any later system) something to attach new
  connector types to.
- **precedent, not transplant**: the ingress-writer pattern of
  `~/Programming/PseudoCoup/pseudocoup/ingress/kotlin.py` (semantic
  facts written to the ledger during a walk) — with the difference
  that its walk was the parse walk, while this node walks UR.

## notes

- renamed `ur_to_ledger_mapper` → `ur_to_ledger` 2026-08-04 (the owner:
  the `x_to_y` form is descriptive without a suffix). the earlier
  candidate rename was `deriver` — kept out of the NAME, kept in the
  definition: "mapper" suggested format conversion, and this node
  derives. `connector` was rejected because that word is reserved
  for the static graph object.
- extracted 2026-08-02 from the builder, with the
  definition/instance ruling: the builder holds an instance of this
  module's class as `Builder.ur_to_ledger` and sequences it after
  `ts_to_ur`; the definition lives here. symmetric boundary modules,
  one per boundary: TS → UR, UR → ledger.
- whether this node needs language-specific sub-modules the way
  `ts_to_ur` does is open — its input is already language-neutral
  UR, which argues no; language-specific typing rules (what counts
  as built-in, what the to-be wrapper is) argue some part is
  per-language. unsettled.
