---
id: pcv5.tools.ledgerer.ur.id
level: 4
status: draft
settled_by: the owner
supersedes: null
designation: code (class)
node:
    name: id
    path: Planning/node_0_0_tools/node_0_0_0_ledgerer/node_0_0_0_0_ur/node_0_0_0_0_2_id/CORE_0_0_0_0_2_id.md
super_node:
    name: ur
    path: ../CORE_0_0_0_0_ur.md
sub_nodes: []
---

# CORE 0_0_0_0_2 — id

## metadata

- **id:** pcv5.tools.ledgerer.ur.id
- **level:** 4
- **status:** draft
- **designation:** code (class)
- **settled_by:** the owner
- **supersedes:** null

## super_node

- [ur](../CORE_0_0_0_0_ur.md)

## sub_nodes

*(none yet)*

## definition

the identity value — the third form beside `node` and `connector`
(registered 2026-08-05, the owner: "we are aligned. lets proceed"). a
static datum: it travels in every node and connector and serializes
in the ledger's records, which is why its class lives in the
vocabulary and not in the operator (`builder`) that assigns it.

the ledger is the ultimate reference frame for node ids (the owner,
2026-08-05): an origin-local address — positional path for parsed
nodes, sub-address under the producing invocation for generated
ones, the abstract scheme for declared nodes — is a PROPOSAL; an id
becomes canonical at admission.

## design

**the spacetime id** (the owner, 2026-08-05): uniqueness by exclusion
principle — no two admissions occupy the same cell, so the id is
unique by EVENT rather than by description, and the connector
circularity vanishes (the id derives from the admission, not from
the graph). "degree one would be unique."

- **coordinates are LOGICAL, ruled** (the owner: "yeah logical space makes
  sense") — the ledger's own bookkeeping, not wall clock, thread, or
  memory position, which are re-used or skew and break the
  exclusion. the Lamport-clock shape.
- **a two-level clock, per the owner's own correction**: batch ordinal and
  in-batch sequential index are BOTH admission-order quantities —
  the batch number is a second temporal dimension, not space. within
  one ledger, `id = (batch, ordinal)`, both assigned by one
  sequencer; the single bookkeeper is what "the safest" resolves to.
- **the spatial axis exists only across sequencers**: independent
  ledger instances share no clock, so the FRAME id joins the tuple
  at merge, and merge stays coordinate-frame reconciliation
  (bookkeeping, not content comparison).
- **reproducibility** rides on the standing determinism rule: a
  deterministic build admits in deterministic order, so identical
  input + recipe yields identical ids.
- **the recipe is load-bearing data**: it needs a version recorded
  in the ledger, like the toolchain version, or re-derivation is
  impossible.

**what sits beside the id, deliberately outside it:**

- **the node+connector fingerprint — an attribute, never the key.**
  content-derived identity was rejected as a KEY on recorded
  evidence (identical co-nodes collide; survey, log_001 §2.1); as a
  derived field it does what content does well — integrity checking,
  duplicate detection, cross-version matching — with its collision
  risk harmless. the key never encodes content, so cross-version
  tracking stays an analysis problem, per the standing ruling.
- **one wall-clock stamp per file admission — provenance, ruled**
  (the owner: "id like to have it nonetheless"; placement as
  metadata-not-coordinate per Claude's accepted correction: clocks
  can read equal at resolution or skew, so a wall-clock tie-breaker
  can itself tie — the frame coordinate is what excludes ties
  between independent batch streams). the stamp answers human
  questions: when did this ingest happen, which update is recent,
  what surrounded a strange merge.
- **re-running and redundant/conflicting objects** (the owner): two
  ingests of one file name get different ids — correctly, different
  admission events — and the shared file name in the origin is the
  "easy flag to raise." the fingerprint triages: identical =
  redundant re-admission (alias or supersede); differing = the file
  was updated (both stand, joined by a supersedes-style connector —
  candidate connector kind, unruled). three layers, one job each:
  the id says WHICH ADMISSION, the origin says FROM WHAT SOURCE, the
  fingerprint says SAME OR CHANGED.

**the assigner is not this class.** the SEQUENCER — the counter that
hands out coordinates at admission — is the builder's held state,
beside the ledger-under-construction (see
`../../node_0_0_0_4_builder/CORE_0_0_0_4_builder.md`). the owner's
"builder is nearly stateless" is corrected by exactly this: the
clock IS the state the builder holds. this class is the value the
sequencer produces.

## notes

- named `id` following the module's brevity pattern (`ur.node`,
  `ur.connector`, `ur.id`); `identity` is the standing alternative
  if the builtin-shadowing in code ever annoys.
- graduated 2026-08-05 from the identity-system section of `ur`'s
  CORE, which now points here; the discussion history (including the
  superseded subtree-fingerprint-as-key candidate) is preserved in
  that CORE's git history and the chat-derived quotes above.
