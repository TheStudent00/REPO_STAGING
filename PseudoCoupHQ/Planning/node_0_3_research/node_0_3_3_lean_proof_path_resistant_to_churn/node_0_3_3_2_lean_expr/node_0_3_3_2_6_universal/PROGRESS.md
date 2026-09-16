---
id: hq.research.lean_proof_path_resistant_to_churn.lean_expr.universal.progress
status: living
---

# PROGRESS — universal

- 2026-09-15: node created on the owner's decision of the day: one universal
  numeric type, every primitive kind a constraint on it plus a
  projection, written once by hand (status: done).
- 2026-09-15: `Universal.lean` written and built on the tower (lp3,
  `podman exec`, no lane), exit 0; the theorem
  `sailToBitsTruncate_eq_ofInt` (Sail's `to_bits_truncate` is
  `BitVec.ofInt`, every width) proved (status: done).
- 2026-09-15: `Kinds.lean` written and built against it, exit 0, in
  2.3 s. Its `#eval` checks: 157 of 157 ok over 10 groups. binary64
  add/sub 6, subnormals and underflow 7, special classes 9,
  mul/div/compare 10, binary32/16 6, integer kinds against
  `to_bits_truncate` 72, `divT`/`remT` against `Int.tdiv`/`Int.tmod`
  with zero divisors 22, constraint sets 10, fixed-point 6, exact
  operations 9. The first run had 1 failure; the check's input was wrong
  (it built an integer where it meant a third), not the kind. The input
  was corrected and the whole file run again (status: done).
- 2026-09-15: bodies exist for 27 of the 67 float axioms (12
  add/sub/mul/div, 15 compare) as definitions in `Kinds.Axioms` of the
  axioms' exact types. The reversible substitution into a working copy is
  not run (status: planned).
- 2026-09-15: MulAdd (3), Sqrt (3), roundToInt (3) and the 31
  conversions have no body yet (status: planned).
- 2026-09-15: the IEEE values checked against the host's doubles and
  known constants, not against Sail's softfloat; no theorem about the
  IEEE part yet (status: planned).
- 2026-09-15: registering `Universal` and `Kinds` in the proof
  project's `Leanpath` roots is held back while lanes l80 and l81 use
  that project (status: deferred, on the lanes finishing).
- 2026-09-15, evening: level 0 against Sail's OWN softfloat, the gate
  (`podman exec` on lp3, no lane; `Research/oracle/riscv/leanpath/softfloat_level0/run_level0.sh gate`).
  The 27 bodies beside Sail's compiled `riscv_softfloat.cpp.o` over
  Berkeley SoftFloat 3, RISCV specialization (the objects the simulator
  links; their sources byte-identical to the emit's model commit
  6266b40c), result bits and the five flag bits. The operations, the C++
  functions and the argument order are read from the three texts
  (`RiscvExtras.lean`, `Kinds.lean`, `softfloat_interface.sail`), none
  typed. 16,875 points (every ordered edge pair, all five modes): 16,833
  agree, 42 disagree, in two causes, both OURS: (1) ∞ / ±0 raised DZ,
  softfloat raises nothing (IEEE 754 §7.3), 30 points; (2) tininess was
  decided at the subnormal quantum instead of at the format's precision
  with the exponent unbounded (IEEE 754 §7.5, after rounding), so a
  product just below the smallest normal with its first m+1 bits all
  ones lacked UF in RNE and RMM, 12 points. Result bits agreed at every
  point (status: done).
- 2026-09-15, evening: both fixed in `Kinds.lean` by rule: `tinyAfter`
  (rounding at m+1 bits, exponent unbounded) feeds `assemble` from
  `roundUni` and `divRaw`; the ∞-dividend line moved above the zero
  divisor's; four checks added from the level-0 rows. The gate is re-run
  before the full comparison is submitted (status: done).
- 2026-09-15, evening: the gate re-run over the fixed `Kinds.lean`:
  16,875 of 16,875 agree, 0 disagree; `Kinds.lean`'s own checks 161 of
  161 (157 and the four new) (status: done).
- 2026-09-15, evening: the full comparison, about 183,000 points (every
  ordered pair over 38 edge values per format, then 1,000 random pairs per
  operation and mode), submitted as lane
  `lanes_lp1/lp3_l87_softfloat_level0_full.sh` on lp3, queued behind
  l83 to l86 (status: done).
- 2026-09-15, 21:47 UTC: lane l87, the full comparison, exit 0 in 8.3 s:
  183,300 points, 183,300 agree, 0 disagree, 0 misaligned, 0 unknown;
  every one of the 27 operations agrees in every mode, result bits and
  the five flag bits (the four arithmetic operations of each width
  12,220 points each, 7,220 edge and 5,000 random; the five comparisons
  2,444 each, 1,444 edge and 1,000 random). The sources again
  byte-identical to 6266b40c; `Kinds.lean`'s own checks 161 of 161;
  the spelling guard passes on the record
  (`softfloat_level0/level0_softfloat.{json,md}`). Points, not a proof:
  no theorem about the IEEE part yet (status: done).
- 2026-09-15, evening: the reversible rewrite, checked small first
  (`podman exec`, `Research/oracle/riscv/leanpath/float_emit/make_working_copy.sh check`):
  a working copy at `/work/proof_float` (the cache's `LeanIM`, and the
  built lean-sail package and emit copied from `/work/proof`, read only,
  after `/work/proof/LeanIM` was checked byte-identical to the cache's);
  `float_emit/rewrite_axioms.py` gave 27 axioms their `Kinds.Axioms`
  bodies (the intersection of the two texts, type kept), 48 axioms left;
  `Universal` and `Kinds` built in the copy (161 of 161 checks); the
  rewritten `RiscvExtras.lean` checked as one file, rc 0, no error. The
  cache's file untouched; the diff kept as
  `float_emit/RiscvExtras_working_copy.diff` (status: done).
- 2026-09-15, evening: the whole working copy built, submitted as lane
  `lanes_lp1/lp3_l88_float_working_copy_build.sh`, queued after l87
  (status: in-progress).
