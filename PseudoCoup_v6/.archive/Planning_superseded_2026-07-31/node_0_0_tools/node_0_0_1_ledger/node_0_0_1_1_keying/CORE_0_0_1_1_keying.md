---
id: pcv6.tools.t2_ledger.keying
level: 3
status: settled
settled_by: the owner
supersedes: null
decision: ../../../../AgentMemory/02_decisions.md
---

# CORE 0_0_1_1 — Ledger Keying: the id as a runtime-observable signal

Spec taken from direction (b) of
`PseudoCoup_v0/DevComms/walk_node_identity_decision.md` (the
written, previously-unmade decision — see
[R4](../../../../Research/r4_runtime_ledger_survey/REPORT.md)).

- **Primary key: the call-site id** — idgen positional path over
  T1's tree-sitter tree: `"<childIndex>:<nodeKind>"` segments
  (idgen's own format string, quoted as theirs) joined by `/` from
  the source root — the sub-node index recorded unconditionally at
  EVERY node. Anchors (names, labels, text) are metadata only,
  never keys. Files and directories are themselves positioned
  nodes. Uniqueness is asserted at build (`--check`), not assumed.
- **Instance key at fire time**: a per-instance ordinal appended
  when the same call site executes multiply (`<id>#<rank>` — the
  walk_id form already present in the recorded walk JSONs).
- **The emission contract** (what makes it a signal, not just a
  key): every transpiled side EMITS the id identically into its
  output at the call site (the `inject_emitid.py` precedent), so
  any runtime observation joins the ledger by id equality —
  "never ambiguous: id is unique by construction."
- **Rejected keyings, on recorded evidence**: source coordinates
  (list-valued oracle registry — one Kotlin line hosts three
  composables) and content anchors (identical co-node collisions;
  the 5-shared-states walk diff). Both failures are documented in
  the R4 sources.
- **Secondary index: FQDN** (`scope.identifier`, three tiers per
  the 02_ledger spec — global / class / parameter) for call sites
  that only know a name; always resolves THROUGH the id, never
  around it.
- Address-vs-identity note (mirrors the planning framework):
  positional ids are addresses of the parse tree as vendored —
  re-ingesting changed source changes ids. Cross-version node
  tracking is an analysis problem (diff-based), not a keying
  problem; the ledger never pretends ids are stable across source
  edits.
