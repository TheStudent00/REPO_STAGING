---
id: pcv6.tools.t2_ledger.progress
status: living
---

# PROGRESS — T2 ledger

- plan — **settled** (all three sub-nodes settled by the owner,
  2026-07-28).
- **phase-1 core — done** 2026-07-28: graduated to
  `PseudoCoup_v6/Tools/ledger/` (id generator
  transplanted from v0 idgen; phase-1 record; deterministic
  dump/load; `require_type` consumer gate; integrity check).
  Acceptance 7/7 on the pinned corpus (four R2-censused compiler
  files).
- open points:
  - storage strategy for generated-crate scale (assembler.rs ≈
    600k named records) — sharding / named-subset / lazy;
  - `DECLARATION_KINDS` grows with the ingestors (growth gate
    applies);
  - later slots (ui, connectivity, divergence, runtime) await
    their writers.
- next consumer: T3's ingress framework populates
  `semantic.type` for real, replacing `unresolvable` markers.
