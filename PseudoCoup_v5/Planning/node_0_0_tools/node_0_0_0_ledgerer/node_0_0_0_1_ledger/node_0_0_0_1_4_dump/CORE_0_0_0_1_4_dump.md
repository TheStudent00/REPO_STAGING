---
id: pcv5.tools.ledgerer.ledger.dump
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (function), rule
node:
    name: dump
    path: Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_1_ledger/node_0_0_0_1_4_dump/CORE_0_0_0_1_4_dump.md
super_node:
    name: ledger
    path: ../CORE_0_0_0_1_ledger.md
sub_nodes: []
---

# CORE 0_0_0_1_4 — dump

## metadata

- **id:** pcv5.tools.ledgerer.ledger.dump
- **level:** 4
- **status:** draft
- **designation:** code (function), rule
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [ledger](../CORE_0_0_0_1_ledger.md)

## sub_nodes

*(none yet)*

## definition

`dump(table)` — the serialization of a ledger to its durable form.
dual designation on purpose: the function is a serializer; the
FORMAT RULES are the point, because the dumped bytes are the durable
artifact of the whole ledgerer and the fixed point of the
reconstruction oracle.

## rules

- **deterministic, byte-identical regeneration.** two dumps of one
  table are the same bytes. no timestamps in the payload (the
  wall-clock provenance stamp is data IN a row, not metadata OF the
  dump), rows in admission order (free, from the sequencer), sets as
  sorted arrays, tuples as arrays.
- **derived values are never written.** indexes are rebuilt by
  `load`; anything recomputable per run stays out — the 289-line
  ledger's reasoned rule (`async_required` never serialized because
  it goes stale), generalized.
- **the format is versioned**, like the id recipe and the toolchain:
  a dump names its format version, or re-derivation is impossible.
- **the round-trip oracle fixes on this output** (the owner, 2026-08-05,
  log_015 §2): source -> ledger -> equivalent source -> ledger ->
  the same equivalent source. dump is where "identical after the
  first cycle" is measured, so any nondeterminism here breaks the
  oracle before it breaks anything else.
- `load` is this format read backwards; it stays in-file (see the
  ledger CORE's design section) because these rules fully determine
  it.

## harvest

- **the serialization discipline** —
  `PseudoCoup/pseudocoup/core/ledger.py` `dump`/`load`
  (set/tuple round-trip fidelity; derived overlays deliberately not
  serialized), named best-in-class by the ledger survey §2.
- **deterministic-regeneration precedent at every store in the
  line** — `pc_intentions.json` ("sorted keys, no timestamps,
  byte-identical rebuilds") and the emitted-artifact stability rule
  (log_003 §1: provenance headers, regeneration byte-identical).
