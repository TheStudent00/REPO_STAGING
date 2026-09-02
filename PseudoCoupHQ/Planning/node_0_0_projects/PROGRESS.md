---
id: hq.projects.progress
status: living
---

# PROGRESS — projects

- 2026-07-31: roster written from the state of the four repos as read
  that day.
- **blocked, and naming what is not**: PseudoCoup_v5's rebuild cannot
  start cleanly while PseudoCoup_v6's suite depends on PCv5 being on
  disk. measured 2026-07-31 — `python3 -m pytest Tools -q` in
  PseudoCoup_v6 gives 6 errors resolving
  `PseudoCoup_v5/Research/rust_routing/sources/rust/compiler/rustc_codegen_llvm/src/declare.rs`
  through `PCV5_ROOT`, and 95 passed once it is set. NOT blocked by
  this: everything in PseudoIR, and every part of PCv6 that does not
  read `PCV5_ROOT`. the unblocking step is vendoring the upstream
  rustc sources into PCv6, which needs no decision from the owner beyond
  where they land.
- planned: keep this roster current as the rebuild proceeds. it is
  the file most likely to go stale, because it summarises four repos
  that each move on their own.
