---
id: pcv5.tools.ledgerer.ledger
level: 3
status: draft
settled_by: the owner
supersedes: null
designation: code (module)
node:
    name: ledger
    path: Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_1_ledger/CORE_0_0_0_1_ledger.md
super_node:
    name: ledgerer
    path: ../CORE_0_0_0_ledgerer.md
sub_nodes:
    - name: table
      designation: code (class)
      realize: false
    - name: admit
      path: node_0_0_0_1_1_admit/CORE_0_0_0_1_1_admit.md
    - name: index_by_id
      designation: code (function)
      realize: false
    - name: index_by_fqdn
      designation: code (function)
      realize: false
    - name: dump
      path: node_0_0_0_1_4_dump/CORE_0_0_0_1_4_dump.md
    - name: load
      designation: code (function)
      realize: false
    - name: merge
      path: node_0_0_0_1_6_merge/CORE_0_0_0_1_6_merge.md
---

# CORE 0_0_0_1 — ledger

## metadata

- **id:** pcv5.tools.ledgerer.ledger
- **level:** 3
- **status:** draft
- **designation:** code (module)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [ledgerer](../CORE_0_0_0_ledgerer.md)

## sub_nodes

- table — code (class) *(realize: false)*
- [admit](node_0_0_0_1_1_admit/CORE_0_0_0_1_1_admit.md) — `admit(table, node)` — the gate.
- index_by_id — code (function) *(realize: false)*
- index_by_fqdn — code (function) *(realize: false)*
- [dump](node_0_0_0_1_4_dump/CORE_0_0_0_1_4_dump.md) — `dump(table)` — the serialization of a ledger to its durable form.
- load — code (function) *(realize: false)*
- [merge](node_0_0_0_1_6_merge/CORE_0_0_0_1_6_merge.md) — `merge(tables) -> table` — joining ledgers built by independent sequencers into one reference frame.

## definition

ledger definitions — how the ledger is standardized: the record
shape, the keying, the registries, the divergence vocabulary, the
`unresolvable` posture. the abstraction of the STORED DATA
structure, as `ur` is the abstraction of the form (the owner, 2026-08-02).

**the ledger defines no second vocabulary** (settled 2026-08-04, from
the owner's "how would the UR-AST not be the ledger?"). every entry is in
`ur`'s forms; what this node owns is the MECHANICS over those forms —
keying, durability, serialization discipline, merge. one data model,
two lifecycles: UR is per-file and rebuilt by re-parsing; the ledger
is durable, id-keyed, merged across files, and extended by writers
(tracer, expansion pass) that hold no UR tree.

**the ledger is a graph of trees in a store-able data structure, and
it is the ultimate reference frame for node ids** (the owner, 2026-08-05).
per-file trees, cross-tree connectors, one id space. an origin-local
address is a proposal; canonical identity is assigned and enforced
here. the identity FORM under design is `ur`'s (see its CORE, "the
identity system"); the assignment, uniqueness, and merge mechanics
are this node's.

## design

settled 2026-08-06 (the owner: "hard to disagree with that design" /
"yes proceed"; the conversation is
`<WORKSPACE_DIR>/PseudoCoup_v5/DevComms/log_016_ledger_brainstorm.md`):
**a deliberately dumb table surrounded by three doctrine-bearing
operations.** every entry is a `ur.node` (the owner's correction:
connectors ride on their nodes, never rows of their own); the
module's machinery is module-level FUNCTIONS taking the table as an
argument — protocol §2b's ontological independence, chosen over the
welded one-class shape. the module stays `code (module)`: distinct
contents, distinct names, no stutter.

the in-file entries, designed here since they have no folder:

- **`table`** — `code (class)`, the static store-able value and
  nothing else: `frame` (this ledger instance's frame id) +
  `entries` (admission-ordered `ur.node` rows). what `dump` writes,
  what the round-trip reconstruction oracle fixes on (log_015 §2).
  `Builder.ledger` holds one.
- **`index_by_id`** — `code (function)`, table -> {Id: node}.
  DERIVED: rebuilt, never serialized — the derived-not-serialized
  rule expressed structurally.
- **`index_by_fqdn`** — `code (function)`, table -> {fqdn: Id(s)},
  resolving THROUGH the id, never around it.
- **`load`** — `code (function)`, dump's inverse. its logic is fully
  determined by dump's format (see the `dump` sub-node); someone
  holding dump's CORE writes load without inventing anything.
- open, deferred to real corpus sizes: whether hot paths cache the
  indexes on the table (fields marked derived, rebuilt on load).
  either answer keeps the serialized form identical.

the realized sub-nodes carry the doctrine: `admit` (the refusal
gate), `dump` (the serialization format), `merge` (frame
reconciliation). realization criterion applied per the owner's challenge
("are all of their definitions remarkably simple?"): an entry with
rules of its own gets a CORE where the rules live checkably; an
entry whose one rule fits a sentence stays in-file.

## harvest

which Frankenstein parts land here. part numbers are
`<WORKSPACE_DIR>/PseudoCoup_v5/DevComms/log_001_ledgerer_harvest_findings.md`
§2. placements are draft commentary, not settled. this node takes
the most parts of the four — the survey's decomposition was
store-heavy, and this is the store.

- **2.2 record shape** — the superset entry
  `{id, file, node_kind, anchor, span, ui, connectivity}` plus the
  new `semantic` slot. source: v0 `ledger_unified.build`
  (`<WORKSPACE_DIR>/StressBot/RelevantProjects/PseudoCoup_v0/tools/pseudokotlin/ledger_unified.py`,
  323 lines). the `semantic` slot is new work, not transplant.
- **2.3 semantic payload** — the eight emission-driving registries
  re-keyed onto positional-path ids, FQDN kept as secondary index.
  source: `<WORKSPACE_DIR>/PseudoCoup/pseudocoup/core/ledger.py` (289
  lines; WFL's copy byte-identical). the re-keying IS the repair of
  the recorded last-writer-wins collisions. carried detail: the
  dump/load serialization discipline (sets/tuples round-trip;
  derived overlays deliberately not serialized).
- **2.4 keying rule and refusal** — three-tier FQDN scheme and
  halt-on-unresolvable. sources: the `02_ledger` schema specs
  (`<WORKSPACE_DIR>/0_Archive/PseudoIR/DevComms/.planning/specifications/02_ledger/`,
  marked more advanced than any implementation) and the 56-line
  refusing ledger at
  `<WORKSPACE_DIR>/PseudoCoup_v5/Research/rust_routing/ledger.py` —
  **the one source inside the material the gutting removes**;
  harvest before gutting or read from version control under
  `PCv5-archived-research`.
- **2.6 divergence** — one taxonomy from three vocabularies (v0
  `classify_methods` kinds, the experimental `ledger.json` reasons,
  registry confidence ranks). the merged vocabulary is this node's;
  the LINKAGE that makes confidence evidence-backed is 2.9.
- **2.8 layout intent** — `ui_ledger._norm`'s absolute/relative
  vocabulary as a slot vocabulary, with the standing open question
  (log_001 §2.8): whether UI layout intent is in scope for a
  ledgerer serving compiler transpilation at all.
- **2.9 registry linkage** — divergence entries carrying a registry
  `op_id` and confirmation status. no existing code anywhere; design
  work. the entry FORM is this node's; the WRITING of the link is
  the `builder`'s (settled with the funnel, 2026-08-02).
- **the carrying-capacity generalization** (the owner, 2026-08-02, notes
  below) is what all six of the above sit inside: slots and
  connectors as typed entries in UR registration forms, added when
  their writer exists.

## notes

- the owner, 2026-08-02, at the node's founding: "does not strictly rely
  on tree-sitter; the UR is the abstraction of the form while ledger
  is the abstraction of the stored data structure; the ledger has
  carrying capacity beyond" — completed the same day: carrying
  capacity for runtime or any other connection (node-edge) types.
  "the UR-AST being abstract enough to formalize nodes and
  connections and the ledger being abstract enough to accept nodes
  and connections using UR-AST registration forms."
- the owner's two worked instances of that capacity, 2026-08-02:
  - a parameter whose instance type is built-in but not defined
    within the file: the ledger holds an ABSTRACT NODE representing
    the to-be wrapper, and the instance connects to it. a parameter
    defined within the file instead gets the connector between the
    parameter definition and the instance.
  - the initial ledger will not necessarily have runtime connectors;
    the tracer adds those connections and annotations later.
- precedent in the harvest, so this is buildable rather than
  speculative: slots that ship in phases and start null until their
  writer exists (the R1 refusal pattern); the to-be wrapper is the
  wrapper injection/erasure handshake of the `02_ledger` specs; the
  tracer's late connectors are the `<id>#<rank>` instance keys
  joined on id equality. what goes beyond the survey — and is this
  node's design work — is connections as first-class TYPED ENTRIES
  rather than fixed slots.
- the no-tree-sitter property is already true of the harvested
  stores and worth preserving: both surveyed store implementations
  are parser-agnostic dicts (survey addendum §1c).
