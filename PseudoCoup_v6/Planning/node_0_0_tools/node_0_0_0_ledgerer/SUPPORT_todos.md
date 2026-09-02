---
id: pcv6.ledgerer.support.todos
status: projected
---

# SUPPORT — todos

projected 2026-07-30 from the previous plan, now archived at
`<WORKSPACE_DIR>/PseudoCoup_v6/.archive/Planning_superseded_2026-07-31/`.
the `source:` paths below are relative to that folder.

source: node_0_0_tools/node_0_0_1_ledger/node_0_0_1_3_growth/CORE_0_0_1_3_growth.md  (392 words)
verdict: substitute
changed: replaced the two literal filenames of the retired backend's
  generated files with generic phrasing (one of the two names is
  disallowed verbatim, regardless of case); reorganized the old
  "Slot growth" and "Scale" sections under the required `## slot
  growth` / `## [UNRESOLVED] scale` headings; appended the required
  unresolved-scale note.

---

# CORE 0_0_1_3 — Ledger Growth (slots and scale)

The phase-1 ledger ships a minimal core (id/span/type + integrity).
This node plans the DEEPENING recorded as open on the T2 PROGRESS:
the later slots, and the storage strategy for generated-crate
scale.

## slot growth

(each under the growth gate: writer + check + consumer rule,
together, never a slot without its check)

- **`semantic` real payload** — types populated by ingestors
  (application: intent + complexity class per node_0_4_1; compiler:
  the sliced region's role). Replaces `unresolvable` markers.
- **`connectivity`** — 1-degree wiring per node (v0 ledger.py's
  Kotlin-side extraction), for structural verification.
- **`ui`** — layout intent, only when a UI-bearing language is
  ingressed (v0 ui_ledger vocabulary); dormant until then.
- **`divergence`** — the merged taxonomy with registry-style
  confidence, populated where a construct crosses a divergence
  class.
- **`runtime`** — walker-suite observations (states, mounts,
  edges), joined by the emitted id; the reason keying is fixed now.

### Acceptance (per slot added)

The growth-gate triple lands together, `--check` extends to cover
the new slot, and a consumer-absence test proves the refusal
posture holds for the new slot.

## [UNRESOLVED] scale

*(the recorded open point)*

The generated file of the retired backend [SUBSTITUTED] is 1.27M
nodes → ~600k named records; materializing the whole ledger is
impractical. Options, to price when a consumer actually needs
file-scale ids: [SUBSTITUTED]

| option | what it is |
|---|---|
| named-subset | ledger only the record kinds a consumer queries (the T6 selection already works region-by-region, not whole-file) |
| sharded | one ledger file per source file, id prefixes keep global uniqueness |
| lazy | build ids on demand for a queried region, never materialize the full set |

Recommendation (agent): named-subset first — it matches how T6
already consumes (per-region), and nothing yet needs every node of
a 1.27M-node file.

**NO LONGER HYPOTHETICAL (2026-07-29)**: a T6 extraction-deepening
run that dumped full ledgers over two generated files of the
retired backend (~226k and ~720k records) EXHAUSTED the sandbox
disk and wedged the session. [SUBSTITUTED] The named-subset/lazy
strategy is now a REQUIRED precondition for extraction over
generated files, not a future nicety. Priority raised from "price
when a consumer needs it" to "needed before the next
generated-file extraction run." The extraction tool already has a
partial mitigation (`extract_slices._ledger_for_dump`: full
in-memory ledger for the `--check` guarantee, only traced records
persisted) — validate it, then decide whether named-subset must be
formalized here.

the scale problem is real and will recur. the files it was measured
on are gone with the retired backend, so the equivalent LLVM-side
file to re-measure against is not yet identified. unresolved.
