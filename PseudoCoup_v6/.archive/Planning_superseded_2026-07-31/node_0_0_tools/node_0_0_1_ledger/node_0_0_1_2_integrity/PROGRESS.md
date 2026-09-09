---
id: pcv6.tools.t2_ledger.integrity.progress
status: living
---

# PROGRESS — T2 integrity

- plan — **settled** 2026-07-28.
- `--check` harness — **done** 2026-07-28
  (`PseudoCoup_v6/Tools/ledger/check_ledger.py`:
  uniqueness, independent-recount equality, missing/extra,
  declaration typing, unresolvable count first-class).
- refusal-at-consumption test — **done** (in the acceptance
  suite: `require_type` halts on `unresolvable`).
- coverage invariant (emitted output traces to ledger ids) —
  **planned**; testable once any emitter exists.
