---
id: pcv6.tools.t6_slicer.progress
status: living
---

# PROGRESS — T6 slicer

- plan — **settled** 2026-07-28 (three sub-nodes:
  selection / extraction / insertion; plans ruled PERSISTED).
- **selection and extraction — removed as mis-aimed (2026-07-30).**
  Both increments (`select_slices.py`, `extract_slices.py` and its
  co-modules, the persisted plan, the emitted modules and their
  expectations, and their acceptance suites) were built pointing at
  a retired reference backend instead of the settled LLVM/rustc-LLVM
  direction. All of it — the selection acceptance numbers, the
  four-seam extraction-deepening work, the disk-exhaustion recovery,
  the later "VERIFIED GREEN" and "REVIEW STATUS" sessions that
  chased those same artifacts — is gone and none of it is carried
  forward as an accomplishment. The forward direction for both
  increments is LLVM/rustc-LLVM; they will be rebuilt against that
  target when a form declares it.
- **insertion — mount+border+cache+platform-assertion core done
  2026-07-29** (delegated to a Sonnet subagent; suites re-run and
  confirmed here). Harvested the proven PCv5 mechanism into
  `PRIVATE/PseudoCoup_v6/Tools/slicer/`, provenance-headered:
  `mount_bytes.py` (from PCv5
  `Research/rust_routing/output_ring.py` — libc mmap RW/PRIVATE|ANON
  -> memmove -> mprotect RX -> ctypes.CFUNCTYPE; `MountedCode` owns
  its page, close() munmaps, __del__ defensively closes);
  `cross_border.py` (from PCv5 `rust_cell.py` — a `BorderCell` that
  refuses every unqualified Python operator, crosses out only via
  explicit `int(x)`); `insertion_cache.py` (from the PCv5
  `pc_runtime.py`/`ledger.py` (operation,type) dispatch pattern —
  key is (intention, language, type-tuple, PLAN-IDENTITY), pages held
  for process life).
  - ADDED what PCv5 left implicit: platform assumptions (x86-64,
    System V AMD64 RDI/RSI in / RAX out, POSIX mmap/mprotect) are a
    DECLARED `MountTarget` asserted at mount time — a mismatch
    (declared `aarch64`, or `win64` cc, or `windows` os) RAISES
    `MountRefused` before any page is mmapped, so wrong code never
    executes; plus page accounting (`live_pages()`; N mounts -> N
    live, close releases to 0; leak is countable) and byte-length /
    non-empty invariants.
  - HEADLINE divergence proven against a HAND-SUPPLIED byte sequence
    written from the Intel SDM (not a PCv5 artifact): the signed
    idiv+cqto stub `48 89 F8 48 99 48 F7 FE C3`
    (MOV rax,rdi; CQO; IDIV rsi; RET), mounted and called, computes
    `-7 idiv 2 -> -3` (truncating) where Python's `-7 // 2` floors to
    `-4` — observed, recorded. A signed grid (extremes, `-1` divisors)
    and an unsigned `div` stub grid both match in-test
    truncating-division ground truth.
  - RECORDED HONEST GAP (marked, not faked): `IDIV(MIN, -1)` and any
    zero divisor raise a hardware `#DE`/SIGFPE that would crash the
    process — they are NOT executed through the mounted stub; their
    ground truth (trap) is asserted via the T4 polyfill's
    `OverflowError`. Polyfill reconciliation: DISTINGUISH the operator
    policy (this border REFUSES bare operators, opposite of
    FixedWidthInt where the operator IS the routing) but REUSE
    polyfill `I64` for the i64 range check (import, not copy). The
    `.pc` import-hook surface / CPython-fork question is carried
    forward UNCHANGED per the CORE's default (not touched here); the
    lowering/encoding byte-extraction depends on a SELECTION/
    EXTRACTION increment not currently present in this repo (see
    above).
  - Acceptance 14/14 at the time of this increment, against the
    insertion suite alone (`test_insertion.py`); it is PCv5-free and
    does not depend on selection or extraction.

## Open

- The forward direction for selection and extraction is
  LLVM/rustc-LLVM: a future increment declares an LLVM-facing seam
  (via a T5 form) and rebuilds `select_slices.py`/`extract_slices.py`
  against it.
- The assembler-scale ledger question raised by the removed
  extraction work (dumping a full ledger over a large generated
  file) remains a live concern for `node_0_0_1_3_growth` whenever a
  large generated file is sliced again, regardless of which compiler
  it comes from.
