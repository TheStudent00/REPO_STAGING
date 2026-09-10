# Progress

Initialized.

- 2026-09-10: task ex2 — THE SAME CHECK task ex1 DEFINED, RUN OVER EVERY
  ATTESTED CELL RATHER THAN THE HANDFUL: 253 cells x the seven targets
  (cpython, php, ruby, java, javascript, dart, csharp) = 1,771 runs, all
  recorded, ZERO disagreements, ZERO timeouts. cpython/ruby/javascript
  render 193 of 253 cells (90.52% of attested ledger rows); php/java/
  dart/csharp render 184 (87.23%) — every rendered cell's whole sample
  agrees, on every target, with no exception; the ten-cell handful
  reproduces inside this loop, 63 of 63 compared. Refusals scale the same
  way task ex1 already measured (the x87 register, vector-lane gaps) plus
  ONE NEW HARNESS-LEVEL FINDING the handful was too small to meet: six
  NULLARY cells (self-XOR and the like) cannot be checked by ANY of the
  seven interpreted targets, because a zero-arrival sample point renders
  as a blank input line and every dialect's own `main` skips blank lines
  by convention — symmetric across languages, not a language difference,
  flagged rather than worked around. This task's OWN runs also found and
  fixed two defects in `interp/interp_check.py` (an unsanitised `.` or `-`
  in a rendered function name, masked on csharp alone by a reused build
  folder's stale binary) — see the autopoly node's PROGRESS.md and
  `PseudoCoupHQ/DevComms/log_250_task_ex2_the_interpreted_loop.md`
  for the full account; nothing here duplicates it.

- 2026-09-09: task ex1 — THE FIRST TIME THIS NODE'S LANGUAGES ARE RUN
  AS EMULATION TARGETS, on the handful of ten arch-opcode cells. The
  route is not this node's interpreter/JIT shape and does not replace
  it: for an emulation target there is no carve at all, so the
  emulation is SOURCE in the language over the language's own value
  model and the check is the fuzz census's method (the reference's own
  z3 term evaluated at each point of a stated sample against what the
  runner prints; declines never scored). Seven targets ran — cpython,
  php, ruby, java, javascript, dart, csharp — every one of their
  runners being in the image (python3 3.13.15, php 8.5.4, ruby 3.3.8,
  openjdk 25.0.4, node v22.22.1) or the persist volume (Dart SDK
  3.13.0 at `/persist/dart-sdk`, .NET 10.0.400 at `/persist/dotnet`);
  kotlinc 2.3.21 is at `/persist/kotlinc` and was not used. 70 runs,
  all 70 rendered, 39,062 sample points per target, ZERO
  DISAGREEMENTS, 819 or 820 declines each carrying the target's own
  word for it. Each language's value model was MEASURED before a
  spelling was written and four of the measurements corrected a wrong
  first spelling: php's integer leaves the integers for a double at
  the width boundary (so its 64-bit arithmetic is in 16-bit limbs) and
  neither gmp nor bcmath is loaded; java's and c#'s shift counts are
  masked while dart's and php's saturate; python's and ruby's division
  floors where z3's `bvsdiv` truncates. THE JIT HALF IS A FLAG, not a
  result: `Research/op_pipeline/jit_out_{javascript,dart,csharp}` holds
  each JIT's own dump text in three different formats, none of them
  objdump's, and `single_opcode_units.json` holds no entry for those
  three languages at all — which agrees with this node's own table
  ("arch-units on disk: 0", "route status: designed only"). Building a
  reader for those formats is a new instrument and is the
  coordinator's. Report:
  `PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/expand1.md`
  §4 and §5. Log:
  `PseudoCoupHQ/DevComms/log_248_task_ex1_cpp_and_the_interpreted_check.md`.
  Status: closed.
