---
id: pcv6.ledgerer.support.validation
status: projected
---

# SUPPORT — validation

projected 2026-07-30 from the previous plan, now archived at
`PseudoCoup_v6/.archive/Planning_superseded_2026-07-31/`.
the `source:` paths below are relative to that folder.

source: node_0_0_tools/node_0_0_1_ledger/node_0_0_1_2_integrity/CORE_0_0_1_2_integrity.md  (229 words)
verdict: clean
changed: nothing

---

# CORE 0_0_1_2 — Ledger Integrity and Refusal

The check harness (harvest: v0 `ledger_unified.check()`, extended).

- **Build invariants** (`--check`, nonzero exit on any failure):
  - every id globally unique; every id appears exactly once;
  - `entry_count == idgen node_count` over the same root;
  - `missing_from_ledger` and `extra_in_ledger` both empty;
  - every declaration-kind node has `semantic.type` or the
    explicit `unresolvable` marker (no silent omission);
  - phase discipline: no record claims a slot its phase doesn't
    define.
- **Coverage invariant** (added over the harvest): every node in
  EMITTED output traces back to a ledger id — the emission
  contract is checkable, not aspirational.
- **Refusal semantics** (settled: refusal at consumption):
  - ingest NEVER guesses — it writes `unresolvable` and continues;
  - `--check` reports the unresolvable count as a first-class
    number;
  - consumers (emitter, slicer) HALT on an unresolvable entry with
    the id and span in the error. Strictness where wrong output
    would be produced; tolerance while still reading.
- **Growth gate**: adding a slot to the schema requires, in the
  same change — the writer that populates it, the `--check`
  extension that validates it, and the consumer rule for its
  absence. (One cause, one fix, moving the whole group — a slot
  without its check is the mixed-depth failure in new clothes.)
- **Acceptance tests** (tool-level, restated from the T2 CORE):
  pinned-corpus `--check` green; dump/load byte-fidelity;
  consumer-halt test; id-emission recoverability test.
