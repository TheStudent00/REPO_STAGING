---
id: pcv6.tools.t6_slicer.insertion
level: 3
status: draft
settled_by: the owner
supersedes: null
---

# CORE 0_0_5_2 — Insertion

Mount extracted slices so hub code executes them. The mechanism is
proven in PCv5 and is harvested, not invented.

## Mechanism (as it works today, from the R5 survey)

- **Mounting** — `output_ring.py` (67 lines): libc `mmap`
  (READ|WRITE, PRIVATE|ANONYMOUS) via ctypes, `memmove` the bytes,
  `mprotect` to READ|EXEC, cast through `ctypes.CFUNCTYPE` to get
  a callable. The `MountedCode` object owns its page; `close()`
  munmaps, `__del__` calls `close()` defensively.
- **Border** — `rust_cell.py` (61 lines): results return as plain
  ints and are wrapped in a typed cell that validates range and
  REFUSES every unqualified Python operator; crossing outward is
  an explicit `int(x)`.
- **Type context** — the ledger answers the operand-type question
  between border crossing and dispatch, producing the
  `(operation, type)` cache key.
- **Surface** — `pc_import.py` (80 lines): a meta-path finder for
  `.pc` modules, rewriting qualified operator spellings to an
  infix trick before compilation.

## Platform assumptions to make explicit (currently implicit)

x86-64, System V AMD64 calling convention (RDI/RSI in, RAX out),
POSIX `mmap`/`mprotect`. These are hard-coded today. In PCv6 they
become DECLARED properties of a mount target, asserted at mount
time, so a mismatch fails loudly instead of executing wrong code.

## Work items

1. Harvest mounting and the typed-cell border into
   `PRIVATE/PseudoCoup_v6/Tools/slicer/`, with the platform
   assumptions asserted rather than assumed.
2. Cache keyed by (intention, language, type-tuple) with the
   plan's identity in the key, so a plan change invalidates
   mounted code.
3. Lifetime: PCv5 held pages for process lifetime via a cache.
   Keep that, but make it explicit and measurable (count mounted
   pages; a leak is then visible).

## Acceptance (delegation-ready)

- A hub expression using an extracted slice executes and returns
  the target language's semantics — the recorded divergence case
  is the test: truncating division where Python floors
  (`-7 / 2` → `-3`, not `-4`).
- The full recorded grid passes (signed, unsigned, extremes, `-1`
  divisors), matching the PCv5 ground truth.
- A deliberately wrong platform assertion REFUSES to mount.
- The typed cell still refuses unqualified operators.
- Page accounting: mounted pages are counted; closing releases.

## Open (the owner)

- Whether PCv6 keeps the `.pc` import-hook surface at all, given
  the settled decision that parser-level qualifiers via a forked
  CPython are the real answer (pencilled at PCv6). If the fork is
  in scope now, this node's surface half changes shape; if not,
  the hook is carried forward unchanged.
