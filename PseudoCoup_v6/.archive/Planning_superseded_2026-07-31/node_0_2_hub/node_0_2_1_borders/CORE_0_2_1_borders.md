---
id: pcv6.hub.borders
level: 2
status: draft
settled_by: the owner
supersedes: null
---

# CORE 0_2_1 — Borders

How values cross between plain-Python space, PC objects, and
inserted-slice regions — the typed-cell discipline generalized.

## The rules (harvested and settled precedents)

- **Cells refuse ambiguity**: a value inside a qualified region
  is a typed cell; unqualified operators on it are refused
  (PCv5's `RustI64` precedent) OR are themselves the routing
  (T4's dunder-as-wrapper choice, recorded deviation 5). The two
  postures serve different tiers; WHICH tier uses which posture
  is this node's main open design call for the owner.
- **Outbound crossing is explicit** (`int(x)`, `.cast()`), never
  implicit coercion.
- **The border lattice is the law**: the 11 data entries
  (`border_lattice` in `pc_intentions.json`) name each divergence
  class's crossing verdict and spelling (.copy() at class-2
  borders, explicit view at class-8, freeze()/send at class-7,
  re-validate leaving dynamic-mode frames). Border code
  implements the lattice; the lattice is not re-derived.
- **Ledger records every crossing kind** at ingress so emitted
  code and inserted slices can assert their borders.

## Work items

1. A `borders` module: cell base + refusal machinery +
   crossing-spelling helpers, one per lattice entry that has a
   spelling.
2. Acceptance: per lattice entry, a fixture that crosses
   correctly (accepted) and one that crosses wrongly (refused
   with the entry named). The lattice data drives the test
   parametrization — 11 entries, 11 pairs.
3. The class-7 `send` (ownership-transfer proof) and class-J3
   re-validation entries need design detail when concurrency and
   metaprogramming intents are first exercised — recorded, not
   scheduled.
