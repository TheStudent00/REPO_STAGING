---
id: pcv6.tools.t4_polyfill.progress
status: living
---

# PROGRESS — T4 polyfill

- plan — **settled** 2026-07-28.
- build — **done** 2026-07-28 (delegated to a Sonnet subagent,
  reviewed here): `PRIVATE/PseudoCoup_v6/Tools/polyfill/`
  — `wrap_fixed_width.py` (u8..u64 / i8..i64, operators routed
  through the wrappers: wrapping arithmetic, bitwise, shifts
  logical-vs-arithmetic by signedness, truncating div/rem,
  comparisons), `check_uniformity.py` (AST check that no bare
  operator touches a polyfilled value — the uniform law made
  checkable), `test_polyfill.py` (differential grid against an
  independently computed mask/sign-extend oracle, incl. type
  max/min, -1, zero and width-1 shifts, unsigned wraparound).
- provenance: u8/u32 masking and i8 sign-extend from a retired
  reference backend's Rust support-layer transpile (since removed as
  mis-aimed); generalized
  `_wrap(v, bits, signed)` from v0's `runtime/numbers.py`;
  truncating div/rem from v0 and PCv5's divergence suite; the
  shift-by-signedness rule from
  `PRIVATE/PseudoIR/DevComms/compiler_transpilation_experiment.md`
  (no harvested source implemented it).

## Recorded deviations (pinned by tests, not papered over)

1. **RULED (the owner, 2026-07-28): TRAP — IMPLEMENTED same day.**
   `MIN / -1` AND `MIN % -1` raise `OverflowError` (real Rust
   panics on both; the earlier silent wrap is closed). Neighboring
   inputs asserted non-trapping (MIN/1, MIN%1, (MIN+1)/-1,
   MAX/-1). Note on record: PCv5's srem(MIN,-1)=0 was a retired
   reference backend's MACHINE-level guard; this module models Rust SURFACE semantics
   — remainder traps too (agent's mechanical extension of the
   ruling, reasoning in `wrap_fixed_width.py`'s header).
   Verified: polyfill 68/68; full four-tool stack 104 passed
   (tree_sitter_base + ledger + polyfill 87, transpiler 17).
2. Division by zero raises Python's `ZeroDivisionError`.
3. Cross-type mixing (U8 + U16) raises `TypeError`; explicit
   `.cast()` required.
4. Unary `-` on unsigned raises `TypeError` (Rust has no `Neg`
   for `u*`).
5. Operator dunders ARE the wrapper here, where `rust_cell.py`
   refused bare Python operators outright — a design choice,
   recorded.

## Open

- u16/u64/i16/i32/i64 are generalized-formula ports (only
  u8/u32/i8 exist literally in harvested sources) and no live
  ingestor exercises them yet.
- `check_uniformity.py` is not yet wired into any ingestor's build
  path — no egress renderer emits wrapper-style code yet.
