---
id: pcv6.hub.surface
level: 2
status: draft
settled_by: the owner
supersedes: null
---

# CORE 0_2_2 — Surface Spelling

How hub source spells qualified semantics: `a r./ b` meaning
"divide with Rust's exact semantics".

## The two mechanisms (decision long since made; scheduling open)

- **Import-hook rewrite (now)**: a meta-path finder intercepts
  `.pc` modules and rewrites qualified spellings into method
  calls before Python parses (PCv5's `pc_import.py`, proven).
  Its three recorded costs: wrong precedence (`|`-trick binds
  low), error messages point at rewritten text, qualifiers
  restricted to positions where the infix trick parses.
- **Parser-level fork (the end state)**: `r./` as a real token
  with real precedence in a forked CPython. DECIDED in PCv5
  (the fork was always the plan; the hook was the stepping stone
  that measured everything except the fork), pencilled "at
  PCv6". SCHEDULING REMAINS DEE'S CALL — the fork's cost is a
  forked interpreter rebuilt per Python release; nothing blocks
  on it today.

## Work items

1. Transplant the import-hook mechanism as a PCv6 tool when the
   Hub assembly starts (T6 insertion's demo needs it): harvest
   `PRIVATE/PseudoCoup_v5/Research/rust_routing/pc_import.py`
   + `pc_runtime.py`, re-keyed to the T2 ledger.
2. Qualifier grammar as data: which spellings exist (`r./`,
   `r.%`, future `go.<op>`, …) derives from the intentions
   artifact (language × operator), not from hand-kept lists.
3. The fork, when the owner schedules it: its own depth node; the ABI
   and maintenance analysis from the PCv5 record carries forward
   as its starting material.

## Acceptance shape

A `.pc` module using every spelling the grammar-data declares
runs end to end; a spelling NOT declared is refused at import
with the missing declaration named (the T5 refusal posture at
the surface).
