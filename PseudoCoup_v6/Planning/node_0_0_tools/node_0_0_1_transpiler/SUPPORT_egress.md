---
id: pcv6.transpiler.support.egress
status: projected
---

# SUPPORT — egress

projected 2026-07-30 from the previous plan, now archived at
`PRIVATE/PseudoCoup_v6/.archive/Planning_superseded_2026-07-31/`.
the `source:` paths below are relative to that folder.

source: node_0_0_tools/node_0_0_2_transpiler/node_0_0_2_2_emission/CORE_0_0_2_2_emission.md  (228 words)
verdict: clean
changed: nothing

---

# CORE 0_0_2_2 — Emission (deferred)

Held until ingress stands (settled: ingress-first). What is already
settled FOR it, so it isn't re-litigated:

- **Gate-before-emit**: no construct emits without a confirmed
  lowering (the pseudoir `gate.py` discipline as a framework
  feature). Refusal carries the ledger id and the missing registry
  cell — the refusal-at-consumption posture at the emit boundary.
- **Byte-snapshot regression net from the first emitter** (v4
  `test_snapshot.py` pattern): every (example × target) pair
  frozen; a deliberate change updates its snapshot in the same
  commit.
- **Deep-emitter mechanisms worth generalizing at framework
  level** (from the WFL harvest): bounded type resolution that
  never guesses; transitive async-requirement fixpoints as derived
  (non-serialized) overlays; ledger-driven import-collision repair.
- **Id emission is mandatory, not decoration**: every emitter
  stamps the ledger id per T2's emission contract — it is the
  runtime join signal (the walker suite's precedent).

## When it activates

Emission is the EGRESS direction (hub → the 12), which the
project reaches only after application ingress (node_0_4) gives it
programs to emit AND the intention objects (node_0_2) exist to
emit from. Two live consumers pull it forward: the Rust/LLVM
application does not need it (that is slicing, not egress), but
the moment a hub program must render back to a target language,
this node builds. Recorded so the sequencing is explicit: emission
is downstream of node_0_2 and node_0_4, not of the tools line.
