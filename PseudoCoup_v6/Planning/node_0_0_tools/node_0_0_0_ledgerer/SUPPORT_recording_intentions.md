---
id: pcv6.ledgerer.support.recording_intentions
status: projected
---

# SUPPORT — recording intentions

projected 2026-07-30 from the previous plan, now archived at
`PseudoCoup_v6/.archive/Planning_superseded_2026-07-31/`.
the `source:` paths below are relative to that folder.

source: node_0_4_application_ingress/node_0_4_1_intent_capture/CORE_0_4_1_intent_capture.md  (244 words)
verdict: clean
changed: nothing

---

# CORE 0_4_1 — Intent Capture

Recording, in the ledger, which intention each construct of an
ingressed program selects — including its complexity class, which
IS part of the intention (the `d[key]` = associate-with-fast-
retrieval principle).

## What gets recorded (extends the T2 ledger's semantic slot)

- per construct node: the intention object it maps to, the
  complexity class it commits to (O(1) map lookup vs O(n) list
  scan), and the source construct that carried it.
- This is the ledger's `semantic` slot growing a real payload
  where today it holds `unresolvable` markers — the T2 growth
  gate applies (writer + check + consumer rule together).

## Why it matters downstream

- Egress (emit hub → the 12) reads this to preserve complexity
  class: a PC.map rendered into a language without fast retrieval
  is a RECORDED SHORTFALL of that destination, and intent capture
  is what makes the shortfall visible rather than silent.
- The behavioral oracle (node_0_4_2) checks that captured intent
  actually holds at runtime.

## Acceptance

- Every mapped construct in a program has a captured intention
  (ledger `--check` extended: no construct maps to an object
  without recording which and at what complexity class).
- A construct whose complexity class is ambiguous is REFUSED
  (never guessed) — the refusal-at-consumption posture at ingress.

## Open (the owner)

- The complexity-class vocabulary: how finely to record it (O(1)
  / O(n) / O(log n) buckets vs a richer scheme). Recorded;
  priced when the first ingestor needs it.
