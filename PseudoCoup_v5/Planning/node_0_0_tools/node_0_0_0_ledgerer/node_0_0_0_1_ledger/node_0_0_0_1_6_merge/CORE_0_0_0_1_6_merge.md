---
id: pcv5.tools.ledgerer.ledger.merge
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (function)
node:
    name: merge
    path: Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_1_ledger/node_0_0_0_1_6_merge/CORE_0_0_0_1_6_merge.md
super_node:
    name: ledger
    path: ../CORE_0_0_0_1_ledger.md
sub_nodes: []
---

# CORE 0_0_0_1_6 — merge

## metadata

- **id:** pcv5.tools.ledgerer.ledger.merge
- **level:** 4
- **status:** draft
- **designation:** code (function)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [ledger](../CORE_0_0_0_1_ledger.md)

## sub_nodes

*(none yet)*

## definition

`merge(tables) -> table` — joining ledgers built by independent
sequencers into one reference frame. the MECHANICS live here because
they touch the table's own state (`frame`, `entries`); the `builder`
CALLS it (build-from-many) — the resolution of the placement both
records half-claimed.

## rules

- **merge is coordinate-frame reconciliation, not content
  comparison** (settled with the spacetime id, 2026-08-05): each
  input table's `frame` id joins its rows' identity tuple; rows are
  re-addressed by frame, never re-derived.
- **same-source discovery uses the three-layer triage** (log_015):
  a shared file name in the origins raises the flag; the
  fingerprint attribute says redundant vs updated; redundant rows
  alias, updated ones both stand joined by a supersedes-style
  connector (candidate connector kind, unruled).
- **open edge, flagged not settled:** what merge does when two
  frames both admitted the same file AND the fingerprints disagree
  with neither superseding the other (true fork). leaning: keep
  both, refuse to pick — refusal posture applied to merge — but
  unruled.

## harvest

- **no surveyed part corresponds** — nothing in the lineage ever
  merged two ledgers (recorded at the builder's founding). the
  nearest prior art is external: GitHub's stack-graphs
  (per-file artifacts that compose; log_002 §6.5), a composition
  SHAPE reference only, not code to transplant.
