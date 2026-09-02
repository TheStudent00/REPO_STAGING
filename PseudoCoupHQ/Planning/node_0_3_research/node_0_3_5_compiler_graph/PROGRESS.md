---
id: hq.research.compiler_graph.progress
status: living
---

# PROGRESS — compiler_graph


- 2026-08-31 (TASK 2, irregular blocking names, log_084 — SURVEY
  ONLY, no render/gate run, no converged-delta claim): direct
  raw-text scan (`canon24_units_<lang>.json` joined to
  `tree_units3.json`'s `normal_path_raw`, all 5 languages) found 57
  not-yet-converged units still carrying a literal
  `amd64g_calculate_condition(...)` call (not the census's 219 —
  that count is attributed by refusal-reason string, a different
  method; discrepancy recorded, not resolved by guesswork), and 19
  `amd64g_calculate_rflags_c` units (matches the census). Measured:
  `condition_table9.substitute_all` already fully resolves 56/57 of
  the condition-atom population at the numeric-substitution layer —
  the real remaining gap is one layer up, at `canon24_render.py`'s
  missing rendering rule for boolean OR/AND combinations of named
  float-condition atoms (FCPAR/FCNE/FCUGT/...), named as a frontier
  per the STOP RULE rather than invented. The 19 rflags_c units are
  ONE closed shape (SUB-family carry-bit extraction feeding a
  shift-with-carry-in idiom), not yet modelled. The 14 Mul32/Mul64/
  DivModS128to64/DivModU128to64 stragglers already have their
  modelling machinery written (`canon12_normalize.py`'s
  `WIDE_MUL_OPS`/`WIDE_DIVMOD_OPS`) but it is unwired to the current
  `tree_units3.json` baseline — a driver-authoring gap, not a
  modelling gap. No new op_pipeline artifact was written this lap
  (survey scripts stayed in /tmp); converged-count-from-1,457 is
  UNCHANGED (no render+gate run occurred) — reporting a delta would
  be fabrication. Recommended next-lap plan (three bounded driver
  jobs, one needing the owner's ruling on a render grouping axis first) is
  in the log. Full report: `DevComms/log_084_task2_irregular_blocking_names.md`.
- 2026-08-31 (TASK 2 continuation, same lap, log_084 second section
  -- coordinator ruled jobs 1/3 of the survey's own recommendation
  were mechanical and belonged in this lap): wrote three new files
  (`condition_table10.py`, `canon25.py`, `canon26.py`) and RAN them
  for real against the correct venv (`/tmp/reconnect_venv/bin/
  python3` -- the system default lacks `archinfo`/`pyvex`/`z3` and
  cannot run any canon*.py driver). Measured before/after: converged
  count 1,457 before -> 1,457 after (delta 0), verified
  programmatically (zero-regression check: all 1,457 previously-
  converged units' `*_text` fields byte-identical across canon24 ->
  canon25 -> canon26, all 5 languages). condition_table10.py's SUB-
  family carry-bit substitution (same technique as condition_table9)
  resolves 19/19 `amd64g_calculate_rflags_c` units at the numeric
  layer (regression-tested, full-population-tested) but converges
  zero (no render rule for the new `CF_SUB` atom yet). canon25.py
  (re-wiring canon12_normalize's proven Mul/DivMod widening model to
  the current baseline) found ALL 14 target units are now classified
  `branch_kind == "branching"` under the adopted tree_match3 baseline
  (were straight-line under the old baseline canon12_render was
  proved against) -- 0 attempted, a measured fact, not a bug.
  canon26.py (re-running canon23.py's own proven fan-out machinery,
  widened to any-atom-count) reached the gate for 25 of the 57
  condition units and converged 0 -- this corrects section one's own
  interpretation ("missing boolean-combination render rule"): the
  real measured causes are a float-operand-shape classifier gap (12
  units), a width-71-bits Concat codegen gap (4 units), an
  unrecognized-leaf-atom gap (4 units), and the same branching-
  classification issue as canon25.py (roughly 32 units never reached
  the gate at all). `check_no_spelling_keys.py` PASS on all 10 new
  per-language artifacts (generator-provenance exemption, no
  grouping/pairing). `tree_units3.json` unchanged (read-only this
  lap); `match_units.py` (clusters rebuild) refused on a missing,
  out-of-scope `sem_anchored_java.json` prerequisite -- `clusters.json`
  verified byte-identical before/after (nothing written). Five named
  frontiers recorded for the owner (STOP RULE), none invented a fix. Full
  detail: `DevComms/log_084_task2_irregular_blocking_names.md`
  (second section).
- 2026-08-31 (compiler-graph probe: the super-op / single-
  instruction distinction is STRUCTURAL, and the graph shows it).
  the owner's question: can the compiler graph distinguish a super-op
  from a single instruction? Tested on the pair the operator
  pipeline already measured — unsigned-64-to-float (the halving
  routine in c/op_117) versus signed-32-to-float (one cvtsi2ss in
  c/op_501). Source was on disk (<WORKSPACE_DIR>/Sources/llvm-
  project); a PIN MISMATCH was caught and corrected before any
  claim: the working tree sits at llvmorg-24-init, five months
  past the compiler that actually built the probes (Ubuntu clang
  21.1.8), so files were extracted at tag llvmorg-21.1.8 by
  commit, not read from the tree. VERDICT: the hypothesis HOLDS,
  sharply. The unsigned case is reached only after TWO declines
  (X86TargetLowering::LowerUINT_TO_FP returns empty for this type
  pair; TargetLowering::expandUINT_TO_FP declines on its f32 !=
  f64 guard) and lands in SelectionDAGLegalize::ExpandLegalINT_TO_FP,
  whose unsigned block constructs ELEVEN nodes — matching the
  observed ship assembly nearly 1:1. The signed case is ONE
  declarative TableGen pattern row (defm CVTSI2SS in
  X86InstrSSE.td), one opcode, no guard. So emit-count and
  stage-of-origin separate them mechanically, as predicted.
  TWO GAINS BEYOND THE VERDICT: the routine's EXTENT is readable
  from source (one function's block) and CONTRADICTS the miner's
  "three two-instruction fragments" — it is one seven-step
  computation plus a guard; and LLVM's own comment shows the
  branch is not in the legalizer at all (it builds a value-level
  select; a later pass turns it into the branch we see), so two
  descriptions are true at different stages. FRONTIERS NAMED, not
  crossed: the upstream leg from clang codegen to the first
  conversion node; the generated matcher table (only its
  TableGen source was read); no TableGen grammar exists in this
  environment; and build_graph.py is still Go-hardcoded — the
  probe used a purpose-built graph over six located source units,
  so "second language" remains open in the CORE. Artifacts in
  Research/compiler_graph/probe_uint64_to_float/; guard passes.

- 2026-08-31 (generic name translator + the miner split into its
  two instruments; 1,415 -> 1,457 converged). WHAT WAS ACTUALLY
  BLOCKING, corrected: not "semantics" but a MISSING TABLE ROW —
  the lifter names each instruction (addss lifts to Add32F0x4);
  our name-to-z3 map had no entry, so the whole sub-tree became a
  free variable and neither the prover nor the renderer had
  anything to work with. GENERIC TRANSLATOR (vex_names.py): the
  SIMD-float names are regular — (Add|Sub|Mul|Div)(32|64)F0x{2,4}
  encodes operation, width, float, lane count — so ONE parser
  replaces one hand-written branch per name; lane semantics
  (write lane 0, keep the upper lanes of operand one) modelled
  with real z3 FPA; the whole-register bitwise V128 family
  handled separately. The if-chain became DICTIONARY dispatch in
  the new module (the owner's point), behaviour preserved. Effect at
  the normalization level: 364 units' roots went from opaque atom
  to real term; exact clusters 414 -> 439, cross-language 289 ->
  316. Converged +42 with zero regressions. A real bug fell out:
  the inherited simulator demanded a source register's declared
  width equal the width requested, which breaks for an XMM source
  read narrowly (movd %xmm1,%eax) — never exercised until this
  family. HONEST CORRECTION to "12 of 17 regular": measured 11 of
  17; Mul32/Mul64 are bare integer multiplies, a different gap.
  MINER SPLIT (the owner's ruling): super_op_candidates conflated a
  name census with an idiom detector, presenting co-occurrence as
  cause. Now name_census.json (per unmodelled name: units
  blocked, languages, regular/irregular — the actionable
  ranking) and idiom_candidates.json (per recurring sub-sequence,
  WITH a field separating names inside its own lifted form from
  names merely co-occurring in carrier units). The halving-routine
  candidate proves the point: blocking names list six, but only
  Add32F0x4 occurs in its own form. Census top: 219
  amd64g_calculate_condition (irregular), 46 Add64F0x2, 44
  Add32F0x4, 19 amd64g_calculate_rflags_c. TABLE unchanged
  (926/135/26/23 on that lineage's own baseline): the 42 units
  were already in their final classes — canon24 replaced an
  unverified placeholder with proved text without moving
  membership. Guards pass on all 11 new artifacts.
- 2026-08-29 (THE EXCEPTION-FAMILY TABLE — the second axis of
  the two-table design is BUILT; the design is now complete on
  the measured five languages). GUARD DATA COMPLETED first:
  44 -> 305 rows by sweeping every unit's mode rows in all
  core_modes files; the 1,511 units with guard_count 0 are
  recorded as data — c/cpp's undefined-behaviour stance is now
  a visible row ("checks nothing"), not an absence. EXCEPTION
  FAMILIES: 34, built on identity = (condition predicate,
  response kind), callee names display-only; two z3-PROVED
  condition merges (rust's bit-trick int-min tests
  ((-2^31+in0)|~in1)==0 proved equivalent to
  in0==INT_MIN and in1==-1, both widths). Families include
  divide-by-zero split by response (go/rust panic-call vs swift
  trap), per-(op,width) overflow wrap-continue families, shift
  clamps, swift float-NaN trap guards. CROSS-AXIS TABLE
  (operator family x language -> exception families): the
  standing example verified — modulo shows go EF0003+EF0016,
  swift EF0004+EF0015+EF0022, c/cpp NONE — with one honest
  refinement: swift's int-min guard is TWO components under
  strict identity (different response kinds). REAL FINDING from
  the join: rust's division dom_op members happen to be
  guard-free units while rust's guarded division units were not
  the mutual-strongest picks — the two axes see different
  member sets, worth the owner's eye when reading the cross table.
  EXCLUDED HONESTLY: 186 rows whose response head is
  "continue-with-a-different-answer" (core_modes' undecided
  outcome, not a guard response) — counted, kept as raw data.
  Absence noted: no conversion-boundary guard rows exist in
  core_modes for this corpus. All three artifacts pass the
  spelling guard.

- 2026-08-29 (branching canonicalization, item 4 — GUARDED
  CONTAINMENT MADE CONCRETE: go and swift's guarded modulo
  JOINED the c/cpp modulo family through seed identity).
  Seed extraction per the ruling: guard blocks identified from
  the existing core_modes route-1 output; dispatch branches
  excluded from the seed (they gate, not compute); a unit with
  two non-trapping paths resolves its seed by exact-text lookup
  against the 0-branch table, the other path becoming an
  inline-special-case guard row; zero-or-ambiguous matches left
  unresolved, never guessed. go/op_132 verified as the standing
  example: seed = mov/cltd/idiv/mov/ret, landed in class C0508
  WITH c/op_246; guards = b==0 -> panic-call and b==-1 ->
  inline-special-case. TABLE over the FULL 1,779 population
  (dominant_table22/dom_ops20): 919 classes, 139 nodes (+4),
  26 families, 23 edgeless; THE MODULO FAMILY now reads
  [(c,%),(cpp,%),(go,%),(swift,%)] — up from c/cpp-only — with
  zero regressions. guards.json emitted for the exception table:
  44 rows (trap 30, panic-call 6+2, inline-special-case 6); its
  first guard-check run correctly FAILED on a repeated operator
  display field (the mechanical guard doing its job) and passes
  after the fix. HONEST REMAINDER: all 34 c/cpp branching units
  unresolved (their guards are overflow/NaN shapes, not divide
  guards — different resolution needed); rust's 2 resolved
  seeds matched no class (rendering not yet converged with
  c/cpp). Named follow-ups, not dropped.

- 2026-08-29 (super-op miner built; prover sweep widened with a
  NULL RESULT that is itself informative). SUPER-OP MINER
  (log_081 item 3, now done): super_op_miner.py joins recurring
  real-ship instruction sub-sequences (register names normalized
  positionally) with the unmodelled lifter names blocking their
  carrier units. 305 of 364 not-yet-converged units carry
  unmodelled names; 17 distinct names total. Top candidate: the
  6-instruction int64-to-double halve-convert idiom
  (movq/punpckldq/subpd/movapd/unpckhpd/addsd), 44 blocked
  units, c+cpp — the paradigm case AgentMemory names surfaced
  by recurrence, not by hand. Guard passes. PROVER SWEEP
  WIDENED: 5,285 further pairs attempted (348 cross-language
  remainder + 4,937 same-language cheapest-first) — ZERO new
  proved edges; 4,434 disproved, 773 undecided, 78 refused.
  Reading: the float-comparison slice was where the proofs
  lived; elsewhere, same-class-different-text pairs are mostly
  genuinely different computations, so the family structure is
  provably stable at 919/135/26/21 (dominant_table21/dom_ops19
  byte-identical to dom_ops18; guards pass, table without
  exemption). STILL UNATTEMPTED, counted: 6,401 cross-language
  non-float pairs (bucket never budgeted in either sweep).
  NEXT: branching canonicalization (item 4), then the
  exception-family table (item 5's second axis).

- 2026-08-29 (bit-serial defect, condition pairing, vector
  registers: 997 -> 1031 converged, zero regressions).
  JOB 1, the bit-serial defect had TWO causes: a value known only
  through outside provenance is opaque to the simplifier, so dead
  padding is built as real instructions instead of folding; and
  the sign-extension recognizer matched one exact syntactic shape,
  so any rewrite fell through to per-bit reconstruction. Measured
  on swift/op_296: ~50 instructions -> 20, a 32-copy sign-bit run
  collapsing to one movsxd. A THIRD bug fell out: a logical NOT of
  a one-bit value rendered as a byte-wide `not`, turning 0 into
  255 instead of 1 (c/op_319, now `xor $1,%al`). 12 units gained.
  JOB 2, conditions were paired by POSITION and position lied —
  for two-condition units the lifter's text order and the
  compiler's order diverge; now paired by the lifter's own numeric
  condition value. 12 units gained; the remaining 8 diagnosed (a
  sign test built as "zero is greater than a zero-extended value",
  which can never be true). JOB 3, vector registers: the whole
  renderer lineage was general-purpose-only, so float units had no
  rendering path at all. Added designated a->%xmm0, b->%xmm1,
  answer->%xmm0, ordered temp pool %xmm2..%xmm15, and the move
  forms. All 10 negate units converged. Bug found while proving:
  the MNEMONIC DOES NOT GIVE THE WIDTH — gcc emits `xorps` for
  doubles too, so the mask width must come from the unit's own
  recorded type. TABLE: dominant_table13 / dom_ops11 — 924 classes
  (-2, genuine merges of texts that were only distinct because
  they were wrong), 135 nodes, 26 families, 23 edgeless.
  PROVISIONAL RULING ADOPTED TO UNBLOCK: `quiet-continue` as a
  fifth mode response for NaN. the owner unblocked it WITHOUT confirming
  it. Its one unmeasured link and the three signs that would break
  it are in AgentMemory under "PROVISIONAL, UNBLOCKING ONLY" —
  read that before the float lap, and re-open with the owner if any sign
  appears.
- 2026-08-29 (remedying the diagnosed buckets: 892 -> 997
  converged, zero regressions verified twice). STAGE 1, the two
  renderer defects: 32 of 60 accepted; the "12 movslq units"
  turned out to be a SUBSET of the 60, not additional — the
  agent reported the discrepancy rather than reconciling it.
  Second defect found and fixed: a NOT distributed through a
  Concat blocked the sign-extend recognizer, producing a
  60-instruction bit-serial mess where one movslq was correct.
  STAGE 2, 128-bit widening: 61 of 89 accepted; needed the GATE
  extended too (its simulator had no model for idiv/cqto,
  inherited from an earlier "ambient %rdx, out of scope"
  caveat that does not apply here because %rdx is locally
  defined in every text being compared) — 21 accepted before
  that fix, 61 after. STAGE 3, data-section constants: ZERO
  converged, and the bucket was mis-scoped: only 10 of the 80
  are genuine negate units (blocked on missing XMM register
  plumbing in the renderer), the other 70 belong to the float
  bucket. The constants themselves were resolved by two
  independent routes agreeing. STAGE 4, compound booleans: 12
  of 44 accepted, exactly the 12 diagnosed c/cpp units, all
  proved. A real infrastructure bug surfaced here: the render
  generations called their own function names directly instead
  of the current dispatch, so a compound condition nested
  inside an outer expression never reached the new rule — 17
  recursive call sites rerouted. Swift's 4 units correctly
  refused, traced to the same bit-serial defect as stage 1.
  STAGE 5, float: ZERO converged, reported as a valid result
  with real diagnosis — the full condition vocabulary
  enumerated (260 units, all comparing against literal 0.0),
  the correct packed-flags model derived, and a LIVE BUG found
  in condition_table2: it mislabels a float-family parity
  condition as not-equal. Building it properly needs four
  places changed at once (normalizer FPA model, renderer XMM
  plumbing, renderer self-consistency, gate simulator).
  TABLE: dominant_table12 / dom_ops10 — 926 classes (+3), 135
  nodes, 26 families, 23 edgeless; structure unmoved BY
  CONSTRUCTION since nodes key on language+operator+arity.
  Guards pass on all 17 new artifacts.

- 2026-08-29 (gate re-anchored to ground truth; converged
  581 -> 892 of 1,641). THE ANCHOR FIX: the behaviour gate
  proved each new rendering against the PREVIOUS rendering,
  which is worthless when the previous one is wrong. It now
  proves against the unit's OWN REAL SHIP CODE. Two bugs fell
  out of that: the checker never remapped registers, so every
  go unit was compared against unrelated symbolic registers and
  always disproved; and shift instructions were modelled
  without the hardware's implicit mod-32/mod-64 masking of the
  count. Re-adjudication: all 78 units whose candidate matched
  the machine are now accepted; all 65 the gate was right to
  refuse stay refused; 82 of 98 previously inconclusive
  resolved (all shift-masking); the 16 remaining are quoted
  and justified, and 12 of them expose a REAL pre-existing
  canon4 defect (a mov re-zero-extends and destroys a movslq's
  sign extension — both old and new text wrong, surfaced not
  hidden). SECOND GAIN: `or`/`and`/`xor` added as recognized
  flag-setters (sound: x86 clears CF/OF on them), closing 16
  opaque-condition units; add/sub/neg deliberately excluded as
  unverified. THIRD GAIN: 134 units whose stored text is
  BYTE-IDENTICAL to their own real disassembly promoted to
  converged — literal identity is stronger evidence than any
  proof, and being unable to re-derive a text is not being
  wrong. TABLE: dominant_table11 / dom_ops9 — 923 classes,
  135 nodes, 26 families, 23 edgeless; counts identical to the
  canon7 baseline BY CONSTRUCTION (nodes are keyed by language
  + operator + arity, so fixed text cannot move them) while
  class membership genuinely changed. The bitwise families
  (AND/XOR/OR/NOT) each span all five languages, and the NOT
  family reproduces AgentMemory's own cited example exactly.
  HONEST REFUSALS, each diagnosed: float condition codes and
  packed float arithmetic (~350 units, needs real IEEE754
  semantics); 128-bit vector constants held in .rodata (80
  units — the lift tracks registers only, never memory
  constants); 128-bit widening arithmetic (41 units, named as
  the most tractable next target); 16 compound boolean branch
  shapes; 60 units where the renderer produced wrong text and
  the gate correctly refused (root cause identified: an
  unnecessary 32-bit truncation ahead of a 64-bit comparison,
  destroying sign — same defect class as the go bug above).
  Zero regressions, verified programmatically. Guards pass on
  all 17 new artifacts.
- 2026-08-28 (canon7: the CONTEXT RECORD — the owner's diagnosis, and
  it was the root cause of all four renderer failures). The
  expression now travels through simplification WITH its
  context and the context is read back on return, so the return
  path is an inverse of the transform instead of a
  re-derivation. Context record: operand widths and homes,
  answer width + return convention, entry contract including
  hardware pins, ordered temp pool and liveness. Stored per
  unit as `context_record` (per block for branching units).
  RESULTS: converged 361 (canon5) -> 581; not-yet-converged
  1,274 -> 974; ZERO regressions (verified programmatically:
  every converged unit is z3-PROVED equal, every non-converged
  unit's text is byte-identical to canon5's). Temp limit struck
  — ordered pool %r10,%r11,%r9,%r8 then callee-saved with
  save/restore; 7 units needed callee-saved. 8/16-bit answers
  return by movzx into the 32-bit answer register (the corpus's
  own c/op_5 convention). Assembly failures 247 -> 0 in two
  diagnosed rounds (nested-render width mismatch; then wide
  immediates needing movabs). De Morgan fold added (c/op_426:
  8 instructions -> 5). One simplification TRIED AND REVERTED
  honestly: dropping a redundant-looking extract mask broke
  c/op_113, caught by the gate. DOM_OPS with the DWARF
  machine-fact result-type fix: 923 classes, 26 families,
  edgeless nodes 73 -> 23 (40 nodes recovered by the type fix
  alone). Guards pass. NOTED: 78 units where canon7's candidate
  matches the real machine better than canon5's stored text —
  held back because the gate proves against canon5, not against
  ground truth; that is the next honest cleanup.
- 2026-08-28 (normalizer-gap lap: PARTIAL, CUT OFF, canon6 is a
  REGRESSION — do not adopt; canon5 remains the good state).
  GAINS, verified: condition_table.py implements the owner's
  canonical-context route for the lifter's opaque condition
  helper (cause 1, 209 units) and the 8-bit operation entries
  were added (cause 2, 288 units). Both work at the EXPRESSION
  level — cpp/op_318 was the bare atom `op_8` and is now a real
  expression with If(Extract(31,0,atom_0) == atom_1,1,0).
  LOSSES: convergence 361 -> 287; the render-back side gained
  three NEW blockages — 214 units whose expression needs more
  than the two temp registers %r10/%r11, 140 whose answer is 8
  bits wide with no native x86-64 return-register form, 87 that
  failed to assemble. Behaviour check: 93 disproved, ground
  truth REAL_BYTES_MATCH_OLD_ONLY on 77 — canon6's renderer is
  wrong where canon5 was right. 182 further candidates were
  REFUSED by the behaviour gate before being written, which is
  the gate working as designed. READING: the renderer, not the
  normalizer, is now the binding constraint, and it has three
  separate problems rather than the one assumed going in. Next
  work: salvage the two expression-level fixes into a clean run
  on canon5's renderer; solve temp pressure (stack slots beyond
  %r10/%r11 already ratified), 8-bit returns (widen to the
  32-bit answer register, which is what real compilers emit),
  and guarded-unit assembly.
- 2026-08-26 (convergence: the transform-and-return step, run):
  canon5.py lifts canonical text, simplifies, and RETURNS to
  canonical text with one fixed instruction-selection rule
  (a two-operand sum always renders mov+add, never lea).
  The three measured integer-addition groups CONVERGE: c, cpp,
  go and rust i32/i64/u64 addition now render to ONE identical
  canonical text. 361 units converged, 6 unchanged, 1,274 not
  yet (honest reasons; mostly unmodeled VEX operations, the
  941 bucket). Distinct texts 508 -> 512 (net up: convergence
  merged some and the answer-register bug fix below split
  others correctly). BUG FOUND BY THE CONVERGENCE CHECK: a
  pre-existing canon4 defect — when a binary/unary op writes
  its answer back into argument a's own register for an i64 or
  u64 result, the width was hardcoded to 32 bits, truncating
  a's upper bits before not/neg/sub/and/or/xor. Ground truth:
  of 93 behaviour-check disagreements, 77 are cases where
  canon5 matches the real disassembly and canon4 does NOT;
  zero the other way. canon4 output for those units is WRONG
  and must be regenerated. dom_ops_0branch2 came out identical
  to the canon4 run (135 nodes, 26 families) for a reason worth
  fixing next: result_type_of() is inconsistent across
  languages (c/cpp collapse to "gp"; go returns "int32"; rust
  returns mangled trait-projection strings), so units whose
  canonical text is now identical across four languages still
  land in different classes on the result-type key alone.
  NEXT: normalize result_type by machine fact (the DWARF
  encoding+width rule already ruled for asg) and re-run.

- 2026-08-26 (canon4 + 0-branch dom_ops): uniqueness audit
  first — the 504 distinct 0-branch texts are GENUINELY
  distinct (zero collapses under reorder/temp/spelling/rip
  axes); the high count is type-width reality, not
  under-canonicalization; 273 texts carried a dead re-inserted
  mov (minimality defect, no false distinctness). canon4.py:
  dead-mov fixpoint cleanup (collapsed exactly 1 duplicate);
  refusals 80 -> 50 with per-cause fixes (flag-idiom rw units,
  passthrough via entry contract, vector-register mov mnemonic
  bug, L? branch-target bug converted to honest refusals);
  survivors diagnosed: mem-mem impossibility (stack-spill
  pairs), rust hidden sret third argument outside the 2-arg
  entry contract, one genuine loop (go stack-growth preamble),
  14 swift unresolved branch targets. Coverage 1699 -> 1729 of
  1779. Bijection VERIFIED: 508 texts <-> 508 byte-strings,
  0 violations both directions. dom_ops_0branch.json (classes
  = type pair + result type + canon4 text; dom_ops7 rule
  unchanged): 1086 classes, 135 nodes, 26 families, 73 nodes
  with no surviving mutual edge — families dominated by c/cpp.
  FINDING FOR DEE: canonical-TEXT-ONLY matching under-merges
  cross-language (dom_ops8 with accumulated grounds spans 5
  languages; text-identity alone leaves go/rust/swift nodes
  edgeless) — supports accumulate ruling: text = home form and
  presentation; cross-language sameness needs the normalized
  layers WITH return path. Guards pass.
- 2026-08-26 (canonical form ENFORCED, first lap; follows the
  log_074 audit): canon3.py — canonical text for 1,699/1,779
  units (per-block canonical instructions with normalized
  labels for branching; stack-slot overflow homes; join
  conflicts rendered per-path honestly, no phi); 80 named
  refusals remain. expr_to_canon.py return path: 384 real
  assembled returns, 1,395 honest no-return-path (941
  unmodeled VEX atoms is the big bucket). dominant_table10:
  canon-text ground added (342 edges, all corroborating byte
  edges — 0 new merges, 0 canonical-vs-byte disagreements in
  1,071 comparable pairs); every member row now carries its
  canonical text (1,681/2,508 slots; 827 asg slots lack
  canon3 coverage — next work). Scorecard: canonical share
  1.84% -> 9.26%; bytes 69% (structural: byte-identical pairs
  mostly lack coverage to re-check). dom_ops8 = 28 families,
  prior results survive (modulo one-family, asg joins).
  swift/op_150 vs op_186 now visibly differ in canonical text
  (the audit's regression case, fixed). RANKING SETTLED by
  log_075 §4: measured over all 1,562 units carrying both,
  canonical text and assembled bytes never separate a pair the
  other joins (0 and 0) — the byte ranking was an empty
  distinction; canonical text is primary, bytes are its
  validity check. Remaining open (log_075 §7): canonical
  coverage for the 827 asg member slots; the 941 unmodeled
  operations blocking return paths; the 80 named refusals.
- 2026-08-26 (accumulate-don't-replace lap: spill fix, table9,
  containment, dom_ops7): spill/reload fixed (CFG carry-forward
  across block boundaries; plus a latent z3 Sar32 width bug that
  was silently breaking normalization for all Sar-based units).
  MODULO CLOSES: c/op_246, go/op_132, rust/op_678 (and cpp,
  swift) normalize to one identical z3 form — one class (A0072),
  no containment needed. dominant_table9.json: 1131 -> 1068
  classes, tree-exact ground (267 pairs) ranked between
  erased-form and sem; all old grounds kept per the owner's
  accumulate ruling. Containment recorded as annotation on 124
  rows, merges nothing. dom_ops7.json: 30 -> 28 families;
  D0022/D0027/D0028 + swift's unattached %/%= merged into ONE
  modulo family (D0005) spanning all five languages. Guards
  pass without exemption. Honest limits: CFG carry-forward is
  pattern-sound not full-dataflow; Sar32 fix lives in
  tree_match2.py only; bridges6 reused not recomputed.
- 2026-08-26 (expression-tree matching, existing tools): ruled
  direction — matching material is the lifted expression tree;
  sub-tree containment; priority = tree position (sub-exp-1 =
  root transformation, sub-exp-2 = input transformations);
  corpus-frequency alpha floor RETIRED. Tool survey (real
  checks): z3 5.1.0 simplify() ADOPTED as normalizer (stable
  normal forms; unknown VEX helpers kept as uninterpreted
  atoms); egglog 11.4.0 installs and is held in reserve;
  pyvex confirmed per-instruction-only (opt_level=1,
  cross_insn_opt=False) so tree-level normalization is real
  headroom. tree_match.py + tree_units.json + tree_matches.json:
  1,724/1,779 units with resolvable roots; cross-language
  exact clusters 229 (old whole-string sem layer) -> 336
  (+107 bought by root-only comparison + normalization);
  1,849 containment edges. Modulo: c/cpp/swift normal-path
  expressions byte-identical, one cluster; go/rust blocked by
  a block-attribution gap (they spill/reload the result, so
  the ret block shows a bare tmp; the fix is exposing
  sem_anchored State's store/load generation tracking to the
  block record — the agent's tree-size fallback was unsound
  and is reported, not used). go &^ lifts to And(Not(in1),in0)
  as measured. Guards pass without exemption. Table
  integration still awaits the owner.
- 2026-08-26 (miner rerun on the owner's two corrections):
  component_mine2.py mines the RUNNABLE derived text (one
  opcode per line; pseudo-notation demoted to comments) with
  the distribution-based alpha floor (scaffolding split by
  measured elbow over type-pair spread: mov/ret/xor/and fell
  out as scaffolding; 69 discriminating opcodes; cltd/cqto
  weld to idiv at 100% co-occurrence, fused pre-mining).
  1,587 units mined; 195 alphas, 11 levels; guard passes
  without exemption. c/cpp modulo share the cltd+idiv alpha
  (K20135) inside one full-cover component (K21453).
  Residue-only-scaffolding cover: c 572/574, cpp 698/700,
  go 73/77, rust 111/112, swift 122/124. HONEST GAP: all
  branching units are still outside the mined set — blocks
  carry only pseudo-steps, no per-block DERIVED runnable
  text exists yet — so the ruled claim "a branching unit
  contains the basic unit's alpha" (swift/op_186's guarded
  cltd+idiv) is corroborated by the raw mnem field but not
  yet demonstrated in mined output. Next work: derive
  per-block runnable text in canon2.py, then re-mine; then
  the owner decides table integration.
- 2026-08-26 (compositional mining, first run): COMPOSITIONAL
  MATCHING ruled (AgentMemory) — units are compositions of
  components, level by level; a component is a literal sub-term
  in the erased naming; sameness = shared vs added components.
  component_mine.py built and run over 1,731 erased units:
  1,803 recurring components across 13 levels (275 alphas).
  Guard passes both outputs. The float unordered-comparison
  idiom emerged level-by-level exactly as ruled (setp alpha +
  setne alpha -> beta -> or gamma, support 122). Zero-residue
  cover: c 567/596, cpp 716/752, go 90/97, rust 93/121, swift
  133/165. FINDINGS FOR DEE: (1) answer-anchoring splits
  same-computation components (c's idiv binds answer, swift's
  binds a temp with return following: K0648 vs K0649) — query:
  is the answer-binding site part of component identity or
  composition context? (2) branch L-labels not normalized, so
  structurally-equal guard components with different label
  numbers never meet. (3) go/op_132 and rust/op_678 still
  excluded upstream (join-conflict erasure refusal — the two
  paths hand different values to one register; a select/phi
  step would readmit them). Table integration deliberately not
  run — the owner decides after seeing the library.
- 2026-08-26 (moves-erased lap RUN, three slices): canon2.py
  built (delete-and-substitute erasure, entry contract, derived
  runnable text, real as/objdump roundtrip; branching via block
  cutting with carried value maps; memory parks erased; rip
  constants are value births k0..). Erased-ok 1631/1779 (c 596,
  cpp 752, go 97, rust 121, swift 165); all 48 remaining
  refusals are one honest cause: conflicting value maps at a
  join. go and c divide machinery now character-identical in
  erased form ("u0 = cltd(a)"; "idiv(u0:a, b)"). c derived text
  regenerates the compiler's own text on 128 units. ASG result
  types re-read from DWARF encoding+width (600/600 c+cpp
  recovered; upgrades the earlier unratified name mapping to
  tool testimony, membership unchanged). dominant_table8.json:
  1131 classes (4 new merges, all from the new erased-form
  ground); dom_ops6.json: 30 families, unchanged. FINDING: the
  modulo split (D0022/D0027/D0028 + swift unattached) SURVIVES
  the lap — the register-bookkeeping layer is now factored out,
  and the remaining difference is exactly the guard blocks,
  i.e. the open whole-function-vs-core class-key query, now
  cleanly isolated. Guards pass without exemption on the
  matching-shaped artifacts. Gap noted: go/rust/swift asg DWARF
  read needs their toolchains (Airlock), not run.
- 2026-08-26 (moves-erased ruling; work list, NOT yet run):
  RULED: pure moves erased by delete-and-substitute; canonical
  record = move-erased form + entry contract; runnable text
  derived on demand (AgentMemory amendment of this date has the
  full statement). WORK LIST, in order:
  1. canon.py: replace the three refusal classes with
     substitution — pinned-register (2 go units), argument
     modified in place (48 go units), and cross-block rename
     where every downstream read is substitutable (36 units
     across c/cpp/go/rust/swift). Emit the move-erased form
     beside canon_text; keep the derived runnable text and
     re-run the assembler roundtrip on it.
  2. dominant_table: add the move-erased form as a matching
     ground (rank beside canon-byte; exact rank is the owner's if the
     two ever disagree); re-fold; re-run dominance and dom_ops.
     Expected: go modulo family joins c/cpp/rust/swift modulo
     (guards remain the recorded difference), and the 90
     fallback units re-enter runnable-form comparison.
  3. asg re-fold with DWARF-recovered result types (the
     dissolved int32_t query, ruled by machine-fact keying) —
     shares the fold rerun with item 2.
  4. Re-run check_no_spelling_keys.py over every new artifact.
  OPEN QUERIES REMAINING for the owner, one per turn: the whole-
  function-vs-core class key (his &-operand-order grouping
  statement bears on it, restate after item 2's numbers);
  D0010's odd chain; intention hints (step 8's null column).
- 2026-08-26 (polyfill answer + consolidation lap): POLYFILL
  QUESTION MEASURED (ce_polyfill lane): go's `&^` polyfilled as
  `a & ~b` in c and `a & !b` in rust — byte-identical to each
  other, wrapper vanishes under inlining, sem-identical to go's
  native unit; the dom_op table is the completeness certificate
  (operator_r expressible in language_b iff r's core+modes
  decompose into b's). COMPOUND ASSIGNMENT MATCHED: the store
  VANISHES at ship, so `op=` units are byte-identical to their
  plain operators — 52 of 54 nodes joined the plain families
  (dom_ops5); `+`/`+=` distinction is a source-language storage
  convention, measured. Mirror rule widened to <=3-member classes:
  six go<->cpp comparison pairs z3-proved, classes 1025->1019
  (consolidation; nothing newly attached — expectation corrected).
  Manifest guard exemption: declared generator provenance passes,
  violations still fail, nesting still fails. AWAITING DEE:
  int32_t->i32 result-vocab mapping (600 asg units inert without
  it, proposal marked strikable); c/cpp modulo two-family split;
  whether plain `=` belongs in the operator table at all.

- 2026-08-26 (recovery + integration lap): JAVA ENTERED THE TABLE —
  the JVM C2 unit, furniture stripped by named rules (entry
  barrier, safepoint, their frame), canonicalized rsi/rdx ->
  rdi/rsi, byte-identical to c/op_102 (8d 04 37 c3); dom_op `+` now
  six languages; weaker provenance marked. Mirror candidate rule:
  go ==/!=/! joined their dom_ops (z3-proved); classes 1113->1025,
  singletons 737->578; cpp alternate spellings finally paired (122
  byte-identical pairs a single-language row-drop had hidden);
  `c --`-on-bool landed in the `!` family (z3-proven, flagged for
  the owner); go >/<= still out (two-member classes, rule reaches
  singletons only — next extension). partial_ordering projection
  MEASURED (-1/0/1/2 low byte, compiler's own testimony twice
  over): all 156 stuck pairs answered, 0 new bridges — refusals
  became measured noes, presented as such. Compound assignment
  second pass: 749 accepted probes extracted (anchor+ship+DWARF),
  matching queued. OPEN FOR DEE: probe manifests fail the spelling
  guard by shape (operator without lang) — bring under guard or
  exempt as generator provenance.

- 2026-08-26: THE JVM PILOT (JIT track; interp_jvm.{json,md};
  OpenJDK 25.0.3, C2-only config, dontinline; 5.6s total — the owner's
  heavier-lift suspicion REFUTED vs CPython's ~106s). hsdis absent:
  routed around — the JVM prints machine BYTES without it, objdump
  supplies mnemonics (two testimonies, kept apart). Bytecode iadd;
  C2 unit's core is the same lea-add the AOT campaign knows, in
  JVM argument registers (parm0 rsi, parm1 rdx — canonical rename
  pending). Division: explicit zero guard branching to the JVM's
  own UncommonTrapBlob = the deopt-continue-elsewhere mode, forced
  by construction; INT_MIN/-1 handled in place beside it (two
  fence strategies, one unit). Warm-up recipe measured: >=7000
  calls C2-only (observed boundary differs from the advertised
  10000 threshold — unverified mechanism, recorded). Lane scripts
  now archived to lanes/ before dropping (habit fixed).

- 2026-08-26: THE CPYTHON PILOT (interpreter track, ruled first;
  interp_cpython.{json,md}; pin v3.14.7; ~106s of Airlock lanes).
  Three layers proven: bytecode (BINARY_OP -> rewritten in place to
  BINARY_OP_ADD_INT after warm-up), dispatch path (measured by
  probe-minus-baseline deltas: generic route ran ONCE, then the
  specializer installed the int case — CPython is a JIT-lite, so
  the JVM warm-up recipe applies to it), handler slice (long_add:
  78 anchor / 94 ship instructions, whole, bytes+mnem). Both modes
  measured: small-int fast path (no allocation, preallocated
  table) and the GROWING mode (67-digit loop x 100k calls). Defect
  caught: coverage-build slices carried the instrument's own
  instructions; repaired with clean anchor/ship builds of the same
  pin. Corrections to expectations: the interpreter body is
  generated_cases.c.h, not ceval.c. Open: CPython diary (tally has
  no order); carving the specialized case from the interpreter
  frame; lane-script archiving habit.

- 2026-08-26: THE DOM_OP CONSTRUCTION RULE ratified and built
  (dom_ops.py; dom_ops.{json,md}, dom_ops_digest.md; lane
  pc_dom_ops). Nodes (language, grammar-operator, ARITY);
  cross-language edges weighted by shared classes; mutual-best per
  foreign language; components = dominant operators. 28 dom_ops.
  Verified: the bitwise-not family across five spellings (c ~, cpp
  compl, go unary ^, rust !, swift ~) with go's binary ^ free in
  the xor family; comparisons are four-language chains with C
  attached by DIRECTIONAL BRIDGE only (result-type split). The
  same-language assertion FIRED 17x — a chain can revisit a
  language; almost all are cpp alternate spellings (one operator
  twice-spelled, machine evidence rightly cannot split them);
  recorded unresolved, D0010 flagged for the owner. A spelling tie-break
  (node ids from sorted tokens) was caught pre-ship and removed;
  ties keep all equally-strongest counterparts (38). intention
  remains null on every row; hint query still queued.

- 2026-08-26: THE DIRECTIONAL BRIDGE / DOMINANCE ruling implemented
  (dominance.py, bridges.json, dominant_table3; lane pc_dominance).
  Result-type split STANDS (transplant test: bool-form substituted
  for int-form miscompiles 32-bit readers); between split classes,
  322 directional bridges: "X dominates Y on projection P" with the
  proof scope and THE ADAPTER as data (movzbl %al,%eax for
  bool->int; read-only-result-register for extra outputs). 321 of
  322 are i32-dominates-bool at low-8. The different-live-results
  residue (759 distinct pairs): 3 resolved by dominance, ~400
  REFUTED with counterexamples (correct answers — sub-term-connected
  opposites like == vs !=), 216 no common projection (float vs int
  result registers), 120 awaiting a partial_ordering projection
  rule. C, not Go, is the extra-outputs side. Every bridge carries
  its evidence class; ABI-promise-dependent ones flagged. A
  mid-build bug (missing register-naming made "never asked" look
  like "solver failed", 528 pairs) was caught and fixed — the exact
  lower-class-presented-as-higher failure the evidence doctrine
  names.

- 2026-08-25 (step 8, the deliverable): THE DOMINANT-OPERATOR TABLE
  built in Airlock (pc_step8_table.sh; dominant_table.{py,json,md}).
  1,086 core-equivalence classes over 1,758 units; 359 span >=2
  languages, 24 span all five; 204 carry fences; divergences sit at
  class borders (0 internal fence splits — forced by the
  total-equality definition). intention is NULL on every row with a
  proposed hint marked "the owner settles". dominant_explorer.html: three
  linked views (table cards / evidence slider / landscape),
  jsdom-verified, spelling guard PASS on all outputs.
  TWO ITEMS AWAITING DEE:
  (1) class formation accepts byte/sem/core-text equality edges but
      NOT z3-proved equality — z3-proved pairs (e.g. the mirrored
      comparisons) never merge into one class; they appear only in
      the evidence view. If z3-proved edges should form classes,
      that is one rule change in dominant_table.py.
  (2) the intention hint map is the builder's construction
      (top-operation -> proposed kind); also ur.KINDS holds 15
      objects (11 + import/try/pair/interpolation), and the hints
      only ever propose 4 of them.

- 2026-08-25: THE SPELLING BAN MADE MECHANICAL after a second
  violation (verdicts.py's row pairing was token-scoped; caught by
  the owner). check_no_spelling_keys.py FAILS the violating outputs and
  PASSES the clean ones; every grouping stage must run it. The ban
  paragraph in AgentMemory now carries the violation history and
  the paste-verbatim-into-subagent-briefs requirement.
  verdicts3.py re-pairs from machine-form evidence only (clusters +
  the owner's CONNECTION relation: shared sub-terms over anchored
  variables, three nesting levels) — 3,455 pairs the token scoping
  had hidden, incl. cpp `^` ~ rust `!=` on bool: MATCHED, byte
  identity. cluster_explorer2.html rows named by machine form.
- 2026-08-25: CORE+MODES ratified and built (core_modes.py,
  verdicts4.py): every unit as {core, modes[]}; modes detected by
  branch-to-response AND solver-localized (go's branchless shift
  clamp: `in1 >= 32 (unsigned) -> clamp-continue`, proven).
  Relations as computed columns: 1,192 total-equal / 66
  core-equal-modes-differ (fence lists as data) / 3,436
  core-different. Mode names carry the interval-probe vocabulary
  (wrapping/growing/approximating). Full-budget tier-1 solver run
  over the 1,302 skipped pairs (Airlock lane pc_tier1_skipped.sh):
  UNDECIDED 4,595 -> 2,323, all solver-limit reasons cleared; the
  residue is structural (live-result counts, two-sided guards,
  multi-block units). Flags standing: result-register fallback is
  convention-class evidence (marked UNVERIFIED per mode);
  wrap-continue conditions are read from connected units (marked
  read_from).

- 2026-08-24: node founded (the owner, after repeating the standing rules
  in conversation too many times). Lap one already run the same
  day, BEFORE the node existed: static graph of cmd/compile's
  argument-lowering region + coverage tally of a probe compile +
  the join. Result: 8-step path found and confirmed executed;
  register leg stops at the follow-the-dot frontier. Record:
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_072_compiler_graph_tracing.md`
  §7.
- 2026-08-24: the coverage tally RULED a stopgap (order lost =
  opaque). The diary (inject_emitid pattern, order preserved) is
  open item 1 and a must.
- 2026-08-24 (later the same day): THE DIARY BUILT AND RUN.
  `inject_diary.py` writes each map node's id into the compiler
  source at the function's body start; the code announces itself
  as it runs (`diary.Note(...)`, new package, active only when
  COMPILER_DIARY is set). 56 spots instrumented, 329 ordered
  events, join to the map by string equality on the id. The
  acceptance chain (params loop -> assignParam -> tryAllocRegs ->
  allocateRegs) appears in exactly that order, ten times, never
  interleaved — order now visible, agreeing with the tally's
  counts. Limits recorded in diary_meta.md: entries only; per-run
  fact; the subject function's name is not yet in the record.
- 2026-08-24 (lap two, same day): SUBJECT COLUMN + FOLLOW-THE-DOT.
  diary_go2.txt: each event names whose function the compiler was
  working on (`af`, `main`, `-` for set-up); the af chain is now
  proven af's. The column corrected lap one: the chains DO
  interleave across concurrently-compiled functions (events 42-46);
  order alone would have mis-read them. resolve_dots.py (co-module;
  graph_go.json untouched, graph_go2.json new): declared-type rule
  closed 8,424 of 19,447 selector dead-ends; `state.rUsed` is now
  an edge; allocateRegs connects to internal/amd64 in 24 hops —
  but only when some edges are walked backwards, so it is a
  CONNECTION, not yet a forward dataflow proof. Forward-only still
  NO PATH. Caveat printed in acceptance_query2.txt.
- 2026-08-24 (lap three, same day): FORWARD MOVEMENT.
  flow_forward.py (co-module; graph_go3.json; earlier maps
  untouched): store-to-field, literal-to-field, field-to-read,
  decl-to-read, argument/return binding — 90,458 movement edges.
  Control on the lap-two map: NO PATH forward. With movement: the
  register assignment travels abi -> ABIParamAssignment.Registers
  -> ssagen -> toward amd64, forward only, no reversal; the diary
  corroborates each instrumented hop with subject af. The register
  INDEX itself stops at three pasted spots: (1) lap-one keying
  defect — two ArgOpAndRegisterFor declarations collide on bare
  name, call binds wrongly; (2) resolve_dots refuses qualified
  field types (s.curBlock -> *ssa.Block), its own recorded open
  item; (3) a second qualified-type refusal one hop later.
  Over-approximation stated on every result (object-insensitive,
  order-unmodelled): paths are all-runs bounds; diary + forced
  probe are the per-run judges.
- 2026-08-24 (lap four, same day): THE TWO INDEX STOPS CLOSED, AND
  THE INDEX'S OWN FORWARD CHAIN. Two new co-modules; build_graph.py,
  resolve_dots.py, flow_forward.py, graph_go.json, graph_go2.json
  and graph_go3.json all untouched. fix_bindings.py: a package
  qualifier and a bare identifier can never name a method, so
  bindings that landed on one are corrected — 22 names in the region
  are held by both a package-scope declaration and a method, 36
  bindings changed, every one method -> func, including
  `ssa.ArgOpAndRegisterFor` at ssagen/ssa.go:630, which bound to the
  zero-parameter method at expand_calls.go:876 and now binds to the
  func at :883. resolve_dots2.py: a declared type spelled `pkg.T` is
  resolved through the imports of the file the DECLARATION is in
  (rule 1), and `x := call(...)` takes the callee's one declared
  result type (rule 2) — 1,100 more of lap one's 19,447 selector
  frontier records closed (8,424 -> 9,524; 9,923 still refused), and
  282 surviving refusals now NAME the out-of-region package they
  wait on instead of blaming "no type information". flow_forward.py
  re-run unchanged on the fixed map -> graph_go4.json (174,159
  nodes, 335,547 edges, 25,472 frontier records). Result
  (acceptance_query4.{txt,json}): the REGISTER INDEX travels
  forward, no reversal, 25 waypointed hops, from
  abiutils.go:514 `regs` through ArgOpAndRegisterFor's body, into
  ssa Value.AuxInt, to ssa/regalloc.go:1040 —
  `reg := v.Block.Func.Config.intParamRegs[v.AuxInt8()]`, the spot
  where the ABI index selects the PHYSICAL register. Four of those
  25 hops do not exist on graph_go3.json; two are fix one's, two are
  fix two's. The new frontier is of a different KIND: the last step
  into internal/amd64 (`v.Reg()` reads Func.RegAlloc) is written by
  the allocator's SEARCH, not by a dataflow move, and a static
  movement map cannot cross a search. Diary corroborates the abi leg
  as af's own (six ordered triples, interleaved with `main`) and
  places af inside amd64's ssaGenValue; ArgOpAndRegisterFor is not
  instrumented, and its nearest per-run evidence, FloatIndexFor
  events 98/102, is a candidate set of two call sites, recorded as
  such.
- 2026-08-24 (lap five): THE O0 ANCHOR RULED IN (the owner: "weve found
  our solution"). The optimizer off switch every compiler already
  ships is the identity instrument: at the anchor build, each
  named variable has a memory home, each operand arrives from its
  home, and the compiler's own debug table states name->home.
  Layering: anchor (identity by contract) / ship (what the arch
  campaign measures) / diff (what the optimizer changed). Also
  measured on the way (log_073): route probes (copy/inline/fold
  erased in both languages; Go's noinline detour survives; clang
  defeats even its own noinline via return-value propagation),
  the owner's recursive carrier (erased by clang -O2 even at unknown
  depth; kept by Go), and the contract barrier (empty inline asm:
  inert AND unsimplifiable, any operand type via +r/+m).
- open items: (1) the allocator's choice on the ship build —
  bracketed by anchor + forced probe; compose the anchor/ship
  diff, (2) goroutine id in diary records, (3) second language on
  unchanged machinery, (4) 9,923 selector refusals remain, 282
  naming an out-of-region package.
- 2026-08-29: arch-unit branch automation audit — the whole rust
  extraction run twice, at 1.96.1 and at 1.98.0, one `PATH` line
  apart. The 1.96.1 re-run reproduces the 2026-08-25 output byte
  for byte (104,927 bytes); at 1.98.0, 0 of 858 verdicts flip, 0
  of 733 refusal texts change, 0 of 125 units change a byte in
  either build, 0 DWARF tables move, and `dominant_table12.json`
  and `dom_ops10.json` come out byte-identical. 47 of 1,108
  stored records differ, all inside a relocation's callee NAME:
  the `core` crate disambiguator (41) and the default symbol
  mangling flipping legacy to v0 (6). 41 machine-written files
  and 3,668 strings would go stale; 0 hand-authored files.
  Identifiers are stable against the compiler but not against the
  inventory — appending one operator moves 0 of 858 ids,
  inserting one at the head moves 792 (92.3%). The five algebraic
  float methods extract cleanly at 1.98.0 and are refused ten
  times by 1.96.1 (E0658, the free detector), but rust's
  `algebraic_add` on f64 is the same five bytes as its ordinary
  `+`, so it would merge into class C0338 unseen — a probe-shape
  limit, not a table gap. Report:
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_078_arch_unit_automation_audit.md`.
- 2026-08-31 (TASK 1, generalized graph builder, log_086): the
  probe's hand-written 6-function/1-regex script replaced by a
  dispatched builder, `Research/compiler_graph/build_graph2.py`
  (extension -> reader; cpp via tree-sitter-cpp reads EVERY
  function in a file, .td via a generic multiclass/defm reader,
  everything else a named `no_reader_dispatched` frontier). Fixed
  a real byte-offset/str-index bug the generalization exposed
  (tree-sitter spans are bytes; slicing a `str` with them silently
  truncated names past any multi-byte UTF-8 upstream — caught by
  spot-checking against the probe's known function names). Pin
  correction recorded: `llvmorg-21.1.8` resolves to commit
  `2078da43e25a4623cab2d0d60decddf709aaea28` this run, not the
  probe's recorded `42befb84c672d78de430feb4c96710e6aa4fc774` (same
  tag date, read as the probe's transcription slip). Region: the
  probe's four files (not expanded outward this lap — named budget
  stop, not an oversight). Result: 1,232 nodes, 3,070 edges, 37,734
  frontier records (`graph_cpp2.json`); both probe queries
  reproduce (ExpandLegalINT_TO_FP for u64/u32->float, CVTSI2SS's
  TableGen row for i32->float, the latter now finding 2 emits where
  the probe's single-purpose regex found 1); a second
  idiom-candidate query from `op_pipeline/idiom_candidates.json`
  converges on the SAME node — honestly reported as a finding (all
  2,144 candidate rows are windowed sub-sequences of one recurring
  idiom, not independent second super-ops; a genuine second
  candidate awaits Task 6's miner re-run). Passes
  `check_no_spelling_keys.py`. Named remainders: non-call control
  flow generalized only for the probe's one inherited guard; no
  `.td` template-argument substitution (so `isel_pattern_match`
  found 0 edges); no `.go`/`.s` reader in this file.
- 2026-08-31 (TASK 4, unbudgeted prover bucket, log_085): swept the
  full 6,401-pair cross-language non-float bucket (`priority_bucket`
  1 in `cross_unit_prover.py`'s own numbering) that neither the
  original run nor `cross_unit_prover_extend.py` had touched — new
  `cross_unit_prover_bucket1.py`, chunked/checkpointed
  (`proved_edges3.json`), transitivity shortcut on. Result: 84
  proofs (80 direct + 4 transitive), 5,471 disproved (each with a
  real z3 counterexample), 846 undecided (instrument limit, honestly
  named), 0 refused — a 1.3% proof rate, disprove-rate-is-the-
  credibility held. Proofs landed, so representatives/table/dom_ops
  were rebuilt, on the `dominant_table23` lineage specifically (NOT
  `dominant_table22` — the two stay unconflated per the task's own
  instruction): new `build_table23b.py` unions `dominant_table23
  .json`'s own text-equality classes wherever a PROVED edge (14 from
  the earlier float slice + 84 from this bucket = 98 total) connects
  two classes, representative = simplest member (THE REPRESENTATIVE
  RULE), originals kept. Measured: 926 classes -> 901 (25 merged),
  135 nodes unchanged, 26 dom_ops unchanged, edgeless 23 -> 20.
  Zero-regression check: unit population identical before/after
  (1,645 = 1,645), no unit's own canonical text touched. Passes
  `check_no_spelling_keys.py` (proved_edges3.json and
  dominant_table23b.json without the provenance exemption; dom_ops21b
  .json via the same exemption dom_ops21.json already uses).
  RENAME NOTE: this file/table/dom_ops trio was first written as
  build_table24.py/dominant_table24.json/dom_ops22.json, then
  renamed to build_table23b.py/dominant_table23b.json/dom_ops21b
  .json — TASK 7's own brief reserves the table24/dom_ops22 names
  for THE single reconciled lineage, which this lap's proof-merged
  continuation of table23 is not. Report:
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_085_task4_prover_sweep_6401.md`.
- 2026-08-31 (TASK 5, parallel branch reconnect, log_087): (a) fixed
  the cpython type key — `interp_feeder.py`'s new
  `cpython_type_key()` reads `ptr64,ptr64` off `long_add`'s own ship
  instructions (`mov 0x10(%rdi),%rax`) and lifted form
  (`ld64/g0(Add64(16:64,in0:64))`), replacing the fabricated
  `i32,i32`. (b) new `langs.py` (LANGS_COMPILED/LANGS_INTERP/
  LANGS_ALL, one source of truth — the dozen-plus existing hardcoded
  LANGS literals were NOT repointed, flagged for a separate sweep);
  new `reconnect_parallel.py` re-ran java + cpython through the
  ADOPTED pipeline (tree_match3.py's ret-block-first rule, unmodified,
  imported) into new files (`tree_units3_parallel.json`, 1,782 units)
  — java's addition MATCHED the existing c/cpp/go/rust/swift class
  unassisted; cpython refused honestly at the arch_read layer
  ("recovered 93 instructions but the mnemonic column has 94",
  pre-existing, unrelated to the type-key fix). Zero regressions:
  all 1,779 pre-existing units byte-identical, verified. (c) new
  `core_modes_java2.json` + `guards2_parallel.py` carried interp_jvm
  .json's one measured `deopt-continue-elsewhere` row (java's
  division unit, forced by construction) into `guards2_parallel.json`
  (305 -> 306 rows) with `provenance_is_weaker: true`; the 34
  exception-family clustering itself was not re-run (left for Task
  7). (d) new `fold_interp_ruby.py` / `fold_interp_php.py` wrote
  `interp_ruby.{md,json}` / `interp_php.{md,json}` from the Airlock
  outputs (`interp_ruby_b/`, `interp_php_b/`) — dispatch-only (no
  arch-unit), pins ruby 3.3.0 and php 7.4.33 (a compromise: 8.3.0 and
  8.2.13 both failed on this container's gcc/glibc, `zend_atomic.h`
  implicit-declaration errors, 8 build attempts recorded). Neither
  enters `LANGS_INTERP` (no arch-unit). (e) the eight auto-derived
  `node_0_3_6_interp_feeder` sub-nodes were listed for the owner's ruling,
  not edited — Planning is his. All new artifacts pass
  `check_no_spelling_keys.py`. Report:
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_087_task5_parallel_branch_reconnect.md`.
- 2026-08-31 (TASK 6, join the graph to the miner, log_088): new
  `op_pipeline/build_super_ops.py` reads `idiom_candidates.json`
  (2,144 rows) and Task 1's `compiler_graph/graph_cpp2.json`, and for
  every candidate with support >= 4 (494 rows) asks which graph node
  emits it. The search key is `names_within_own_lifted_form` (the
  miner's own forced-by-construction field); one new mapping is added
  on top (VEX lifter name -> LLVM ISD opcode root — human
  interpretation of the ISD naming convention, weakest evidence
  class, stated on every record that uses it). A candidate resolves
  ONLY when exactly one graph node has the maximum ISD-root overlap;
  a TIE (multiple functions sharing the same overlap size) is
  recorded as an ambiguous-match frontier naming every tied
  candidate, never silently broken by list order — this changed the
  result mid-lap: the first version broke ties arbitrarily and
  resolved 285/494, but re-checked against Task 1's own hand-verified
  answer for the flagship idiom (support 44) it landed on the WRONG
  function (`lowerToAddSubOrFMAddSub`, a 1-of-10 tie); the corrected
  version now reports that exact idiom honestly as an ambiguous
  10-way tie (naming `ExpandLegalINT_TO_FP`, Task 1's answer, among
  the ten) instead of asserting a wrong single answer. Final measured
  result: 96 resolved super-ops (all landing on ONE function,
  `SelectionDAGLegalize::ExpandNode` in `LegalizeDAG.cpp`, stage
  legalization — a large multi-opcode dispatcher, so the match is a
  correct unique-overlap result but coarse precision, named as such),
  398 frontier (189 ambiguous ties, 135 rows with no
  `names_within_own_lifted_form` to search on, 64 rows in languages
  the graph has no reader for — go/rust/swift, Task 1's own named
  gap — 10 rows with zero overlap at all). Output:
  `op_pipeline/super_ops.json`, passes
  `check_no_spelling_keys.py`. Report:
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_088_task6_super_op_provenance.md`.
- 2026-08-31 (TASK 3, the 34 c/cpp branching seeds, log_089): new
  `op_pipeline/seed_extract2.py` resolves all 34 of `seeds1.json`'s
  unresolved c/cpp branching units (the u64->float halving/doubling
  conversion idiom, paired with an operator: +,-,*,/,==,!=,>,>=,<=,<
  for c; +,-,*,/,==,!=,not_eq for cpp — 34 = 10 c-ops x2 + 7 cpp-ops
  x2). Note: `seeds1.json` actually carries 36 unresolved units, not
  34 — the extra 2 (swift/op_164 "/", swift/op_200 "%") are a
  DIFFERENT idiom (32-bit-fits-fast-path division guard, not a
  conversion) and are explicitly marked out-of-scope for this task,
  not silently dropped. METHOD: the idiom prefix (manipulates only
  the argument register, never touching the pre-existing traced
  float register) is split from the operator suffix by REGISTER
  IDENTITY (first touch of the designated float-argument register),
  never by operator token. Each unit's two candidate suffixes are
  proved semantically equal by z3 (`canon20_behaviour_check.Sim20` /
  a reused `Sim20Cmp`, both imported from `cross_unit_prover.py`
  unchanged) under a shared seed dict, after two mechanical
  simplifications: stack-spill-roundtrip collapse (store-then-load
  of the same `%rsp` offset -> direct register move) and dropping
  GP-only lines that never touch an `%xmm` register on arithmetic
  suffixes (dead bookkeeping, not part of the float answer). All 34
  PROVED (zero DISPROVED/UNDECIDED/REFUSED). Per AgentMemory's SEEDED
  GROUPING amendment (task brief part b): the idiom is recorded as
  CONTEXT, not guard, not seed — a `context` field on each resolved
  seed, explicitly labeled PROVISIONAL / not ratified. **DESIGN
  CHOICE FLAGGED FOR DEE**: this is a third component kind beyond
  seed/guard; not silently added to the ontology, named here and in
  log_089 for a ruling. Output: `seeds2.json` (additive over
  seeds1.json), passes `check_no_spelling_keys.py`.
  `op_pipeline/build_table23c.py` applies the 34 resolved seeds onto
  the `dominant_table23b.json`/`dom_ops21b.json` lineage (NOT
  table24/dom_ops22, reserved for Task 7): 901 -> 925 classes (10
  seed units — all cpp's comparison ops — merged verbatim into
  EXISTING table23b rows; the other 24 — all of c's 20 units plus
  cpp's 4 arithmetic ones — form new classes, honestly, because their
  extracted seed text still carries per-unit scratch register
  numbering that this lineage's canon7-canon24 render chain has not
  run over for seed fragments; named as a remainder, not patched
  around). dom_op family count UNCHANGED at 26 (0 singleton, 20
  unattached, same as dom_ops21b) — the new units did not gain a
  cross-language mutual edge this lap. Zero regressions: all 901
  pre-existing table23b classes/members verified byte-identical in
  table23c, programmatically. Output: `dominant_table23c.json` /
  `dom_ops21c.json`, both pass `check_no_spelling_keys.py`. Report:
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_089_task3_branching_seeds.md`.

- 2026-08-31 (TASK 7, lineage reconciliation, log_090): new
  `op_pipeline/build_table24.py` merges the two divergent table
  lineages into one -- `dominant_table24.json` / `dom_ops22.json`.
  METHOD: canon24-newest text (table23c lineage's own basis) as the
  ground, with THE REPRESENTATIVE RULE rebuilt fresh (same three-
  ground union-find `build_representatives4/5.py` established) over
  this session's full proof state, `proved_edges.json` UNION
  `proved_edges2.json` UNION `proved_edges3.json` (98 PROVED/
  PROVED_TRANSITIVE edges, 430 groups), plus the full 66-seed
  branching join (`seeds2.json`, verified a strict superset of
  `seeds1.json` before use). RESULT: 901 classes / 137 nodes / 26
  dom_ops / 20 edgeless -- lower class count than either source
  (919 table22, 925 table23c) because the representative rule now
  merges more proved-equal pairs than table23c's un-represented
  method did, on a newer proof/text state than table22's stale
  pre-canon24 representatives5.json. VERIFIED programmatically:
  modulo family spans c/cpp/go/swift; float comparisons include go
  (12 classes, {go,rust,swift,cpp}); bitwise families (AND/XOR/OR/
  NOT) span all five languages. ZERO-REGRESSION CHECK, both
  directions: 28 units (of 138 total branching units) that had a
  family placement in one source lineage lose it here, all named --
  6 from table22's seeds1 joins (go/swift), 22 from table23c's new
  seeds2 joins (c/cpp conversion seeds) -- cause: their seed's
  proved-equal target text was produced by a text-consolidation rule
  (representatives5.json's pre-canon24 grouping, or table23b.py's
  own proved-edge consolidation) this file's fresh representative
  rebuild does not reproduce character-for-character. STOP RULE
  applied: these 28 are kept in `dominant_table24.json`'s
  `unreconciled_branching_units` bin, named with cause, not guessed
  into a family. FRONTIER FOR DEE: which text-consolidation output
  is canonical for matching a seed fragment against a class row is
  an un-ratified method question, most likely closed by extending
  the canon7-canon24 render chain over seed fragments themselves
  (table23c's own named remainder). Both outputs pass
  `check_no_spelling_keys.py` -- table24 with no exemption (task
  requirement), dom_ops22 needed none in practice. Report:
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_090_task7_lineage_reconciliation.md`.

- **2026-08-31 (Task 8, log_092).** guards3.json (undocumented from
  round 1) determined to be a fold on guards2.json carrying all 8 of
  java's measured guard rows -- fuller than guards2_parallel.json's
  one row. ONE guard record of record written, `guards4.json` (313
  rows: guards2.json's 305 unchanged + java's 8), provenance field
  normalized to `provenance_is_weaker` (add_java.json's own name).
  Exception families rebuilt over it, `exception_families2.json`: 34
  -> 39, all 34 original families preserved (verified), 5 new
  java-only families, including `deopt-continue-elsewhere` forming
  two NEW families (EF0020, EF0039) rather than joining any existing
  one -- no other language shares that response head. Cross-axis
  operator-family x exception-family table built fresh
  (`cross_axis_table.py`/`.json`, no such table existed before): 17
  crossed cells; 83 java member rows uncrossed because
  `dom_ops22.json` has no java/cpython join yet (Task 11's open
  item, not attempted here). log_087's claim that java's `u2.m4`/
  `u2.m9` rows were "explicitly NOT carried" is corrected as false
  -- both are present in `guards3.json`, verbatim, and were on disk
  the whole time. Task 13's two documentation slips corrected in
  place (log_086: tree-sitter is 0.25.2 per `graph_cpp2.json`'s own
  pins, not 0.26.0; log_090: `dom_ops21c.json` passes
  `check_no_spelling_keys.py` only WITH the generator-provenance
  exemption, verified by re-running the guard). All new artifacts
  pass `check_no_spelling_keys.py` with no exemption. Report:
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_092_task8_guards_record.md`.

- **2026-08-31 (Task 11, log_094).** Graph widened from Task 1's
  4-file region to 11 files (`build_graph3.py` -> `graph_cpp3.json`:
  2,280 nodes / 18,331 edges, up from 1,232 / 3,070); calls FROM the
  original 4 files drop from 37,733 unresolved to 28,156 (9,577
  newly resolved by the widening). Re-join with a new graph-
  structural tie-break, dispatcher demotion (drops a tied candidate
  when it CALLS another tied candidate, via the graph's own `calls`
  edges -- no operator token compared): `build_super_ops2.py` ->
  `super_ops2.json`. Result: 96 resolved / 398 frontier, IDENTICAL
  split to Task 6's `super_ops.json` -- 0 of the 189 ambiguous ties
  broke (157 had their tied-candidate set changed but stayed >1),
  the 64 no-graph-coverage count is unchanged (that bucket is
  language coverage, not file coverage, so widening cannot touch it
  by construction). THE CONCRETE TEST (idiom_0001 landing uniquely
  on `SelectionDAGLegalize::ExpandLegalINT_TO_FP`): **FAIL**,
  reported plainly -- `ExpandNode` correctly dropped from the tie
  (its call edge to `ExpandLegalINT_TO_FP` verified at line 382),
  but the widened region supplied a same-sized replacement tenth
  candidate (`DAGTypeLegalizer::ExpandFloatRes_XINT_TO_FP`), net tie
  size unchanged at 10. Diagnosis: the 189 ties are caused by
  whole-function emit lists being too coarse (many sibling functions
  share one ISD root like FADD somewhere in a large body), not by
  missing call edges or dispatcher pollution -- file widening cannot
  fix that; sub-block/per-branch emit extraction (named frontier
  since log_086/log_088) is the actual fix, not attempted this lap.
  Both new artifacts pass `check_no_spelling_keys.py` with no
  exemption. Report:
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_094_task11_graph_widening.md`.

- **2026-08-31 (Task 9, log_093).** Fresh census of the 322
  unconverged units built from the CURRENT newest generation
  (`canon26_units_<lang>.json`, single-sourced raw-text name
  attribution -- no JSON-dump/reason-string scan, unlike
  `name_census.json`), `census27.json`. Fresh #1 bucket:
  `__no_named_op_found__` (126 units, 104 never reached any driver
  -- heterogeneous, not worked this lap, named as an open item).
  Population-filter fix built (`canon27.py`): the silent
  `skipped_not_our_shape` bucket is split into branching-reserved
  (32) vs no-call (265) vs no-tu3-record (0), cross-checked EXACT
  against census27.json's independently-computed counts (322 - 57 =
  265; 32/57 branching). 25 units reach the gate (straight_line,
  has the call); 0 converge, four named, individually-diagnosed
  reasons (float-operand classifier, width-71 Concat codegen,
  `u0:64` semantic ruling, `CF_SUB` render rule) -- each either new
  rendering mechanism or a the owner-reserved semantic decision, STOP RULE
  applied, none invented. Converged delta: 0, but diagnosed
  DIFFERENTLY from round 1 (round 1: "0 attempted", opaque; this
  round: population filter exact and cross-checked, 25 real
  attempts with 4 specific reasons). Zero-regression verified:
  1,457 converged units byte-identical canon26 vs canon27, all 5
  languages. `tree_units`/`clusters`/`dominant_table24`/`dom_ops22`
  not touched (no convergence this lap; table ownership is another
  task's this round). Report:
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_093_task9_unconverged_322.md`.

- **2026-08-31 (Task 10, log_096).** Extended `dominant_table24.json`'s
  branching-seed join with a second pass: for each of the 28
  unreconciled units' underlying 62 unmatched/text-ambiguous seeds
  (`seeds2.json`), restrict candidates to rows sharing the seed's OWN
  machine-form class key (type_pair, result_type family, never the
  operator token) then attempt `cross_unit_prover.prove_pair` (z3,
  unchanged) between the seed's text and each candidate's canonical
  text. Ran to completion: 36 of 62 seeds had a nonempty pool (287
  candidate pairs), 26 had an empty pool. Result: 0 PROVED, 0
  DISPROVED, 287 UNDECIDED (Sim8/Sim20Cmp have no model for the
  mnemonics several of these seeds still carry -- cqto/idiv/jo/jmp/
  setp) -- diagnosed honestly, not gamed. New files
  `dominant_table24b.json`/`dom_ops22b.json`/`representatives24b.json`
  are byte-identical in membership/class/family counts to
  `dominant_table24.json`/`dom_ops22.json` (zero regression,
  verified programmatically); `dominant_table24.json`/`dom_ops22.json`
  untouched. Both new artifacts pass `check_no_spelling_keys.py` in
  full, no exemption. Per-unit causes: 8 c/cpp + 2 cpp "u64,f32->f32"
  seeds and 10 swift range-typed seeds have an EMPTY class-key pool
  (no class exists to match -- cause 1, some blocked further by
  `result_type_norm.py` having no entry for Swift `Range<...>`
  result types, a separate open item); the remaining 36 seeds' pools
  are all UNDECIDED on an instrument gap in the two z3 simulators
  (float comparison's `setp`, or divide/branch mnemonics still
  present in the seed text) -- neither provably cause-2 nor cause-3
  from this pass alone. The log_090 SS5 text-consolidation frontier
  remains un-ratified and undecided here, per the task's STOP RULE;
  both the original `cause_table24` text and this pass's diagnosis
  are carried side by side per unit. Report:
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_096_task10_unreconciled_28.md`.

- **2026-09-01 (Task 12, log_095).** Ruby and php: from round-1
  dispatch measurements (tally only) to handler slices (the arch-unit
  equivalent), the same step `interp_cpython.md` already took for
  CPython. RUBY: succeeded cleanly -- built anchor (`-O0 -g -fwrapv`)
  and ship (default optimized) binaries of ruby 3.3.0 from
  `/persist/ruby`'s source tree, confirmed zero coverage-instrument
  symbols in both, sliced four handler functions (`vm_opt_plus`,
  `rb_fix_plus`, `rb_int_plus`, `rb_big_plus`) with objdump. Anchor's
  `rb_int_plus` disassembly shows the real dispatch chain
  (`RB_FIXNUM_P` -> `fix_plus`, `RB_TYPE_P`==T_BIGNUM -> `rb_big_plus`,
  else `rb_num_coerce_bin`), matching round 1's tally. `vm_opt_plus`
  is absorbed entirely at ship (165 -> 0 instructions, no standalone
  body -- frontier not chased). PHP: a diagnosed dead end, recorded
  honestly rather than smoothed over -- three build attempts all hit
  the same `libxml-2.0` pkg-config failure in this container, and
  `apt-get update` from inside the Airlock agent lane returned exit
  100 (network blocked), so no fix was available this session.
  Because reconfigure kept failing, `make` silently relinked the SAME
  coverage-instrumented objects into both the "anchor" and "ship"
  paths; caught via `nm` (13352 `__gcov` symbols in both) and an
  empty `objdump` diff of `add_function` between them -- NOT reported
  as a working pair. Four php handler symbols were still located and
  disassembled from the one build that exists
  (`add_function`, `ZEND_ADD_SPEC_TMPVARCV_TMPVARCV_HANDLER`,
  `ZEND_ADD_LONG_SPEC_TMPVARCV_TMPVARCV_HANDLER`,
  `ZEND_ADD_LONG_NO_OVERFLOW_SPEC_TMPVARCV_TMPVARCV_HANDLER`), counts
  recorded with the gcov-instrumentation caveat attached. THE OPEN
  QUESTION (do interpreter handler slices join the operator table
  directly, or only through bridges/dominance) is presented both ways
  for ruby, per the STOP RULE, and left MOOT for php pending a clean
  build. New artifacts `interp_ruby_handlers.json`/`.md`,
  `interp_php_handlers.json`/`.md`, both pass
  `check_no_spelling_keys.py` with no exemption; every row on both
  carries `provenance_is_weaker: true`. No round-1 artifact was
  modified. Report:
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_095_task12_ruby_php_handler_slices.md`.

## 2026-08-31 — Task 14: record hygiene (round 3)

Four small fixes, no pipeline logic touched. (a) log_092's "all 83
uncrossed rows are java" claim was computed against
`cross_axis_table.json` directly and found false: the real split is
swift 35 / go 30 / rust 10 / java 8 (sums to 83) — a single pointer
line was appended to log_092 (body left standing); the full breakdown
is in `log_098_task14_record_hygiene.md`. (b) `provenance_is_weaker:
true` moved from prose into the JSON artifacts themselves (top-level
field, matching `add_java.json`'s field name): `interp_ruby.json`,
`interp_php.json`, `interp_ruby_handlers.json`,
`interp_php_handlers.json`. Searched for op_units/sem_anchored records
derived from ruby or php — none exist on disk, verified by grep and
`ls`, so no derived record needed the mark. All four touched files
re-pass `check_no_spelling_keys.py` with no exemption. (c)
`op_pipeline/task10_seed_prove.log` formally named as a benign stray
stdout capture from round 2's Task 10 honest zero. (d) mtime sweep of
`op_pipeline` and `compiler_graph` for the round-2 window (Aug 31
21:00-22:00): 34 + 2 files respectively, every one accounted for by
some round-2 log (092/093/094/095/096) — nothing unlisted found.
Report: `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_098_task14_record_hygiene.md`.

## 2026-08-31 -- Task 15: the 322 unconverged, third attempt (+84,
## first non-zero)

Round 2's own diagnosis (log_093) carried in rather than re-derived.
Surveyed the top-ranked bucket by its OWN sub-shapes (`census27.json`'s
`__no_named_op_found__`, 126 units) instead of the bucket in general:
104 `status == "unchanged"` (never selected by ANY driver's own
substitution-family shape filter -- root cause traced in `canon26.py`),
16 canon4-stage erasure refusals (a different pipeline stage,
recommendation: defer), 6 `SP:64` leaf-atom units (`&a` address-of --
a pointer-valued-answer semantic question, recommendation: declare
the owner-reserved). Fixed the 104's mechanical gap with new file
`op_pipeline/canon28.py`: runs the SAME re-anchored gate every later
driver already uses (`canon8_behaviour_check.anchored_check`, imported
unchanged) directly against each unit's own already-rendered text, no
new substitution/rendering/modelling. Result: 84 accepted (40 c / 22
cpp / 2 go / 8 rust / 12 swift). Converged: **1,457 -> 1,541**. Zero
regressions (1,457 prior units byte-compared, 0 differences).
`check_no_spelling_keys.py` PASS on all 5 new
`canon28_units_<lang>.json` (generator-provenance exemption). The 26
"attempted, not proved" units are all `UNDECIDED` (gate-simulator
mnemonic-coverage gaps -- `jo`/`je`/`jb`/`cltd`/stack-relative operand
widths/`idiv`'s ambient register -- in the shared
`canon8_behaviour_check.py` file every driver depends on, named as a
frontier, not fixed this lap). Round 2's four named gaps
(float-operand classifier, width-71 Concat codegen, `u0:64` undefined-
literal, `CF_SUB` render rule) re-checked for new precedent and
re-confirmed the owner-reserved, not re-decided. `tree_units`/`clusters`
rebuild not located/run this lap -- named as an open item;
`dominant_table24.json`/`dom_ops22.json` untouched, per the brief.
Report: `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_099_task15_unconverged_third.md`.

## 2026-08-31 -- Task 17: interpreter units into the table question (ruby/php/cpython), posed not forced

Answered by measurement, not assertion, on all three routes the
brief named: (1) `canon.py` itself was checked line-by-line for its
requirement (`sem.anchor_registers`, written only by the DWARF-
anchored probe pipeline) -- refuses for all nine handlers (4 ruby, 4
php, 1 cpython) because none was built through that pipeline
(`interp_canon_attempt.py` / `.json`, new). (2) `dominance.py`'s own
`RESULT_PROJECTION` table was imported unmodified and queried --
refuses because every handler returns a ruby `VALUE` or a php/cpython
pointer type, neither named in the table. (3) `cross_unit_prover.py`'s
own candidate gate (shared `type_pair` key) was checked against
`dominant_table24.json`'s 901 rows / 42 distinct type_pairs, computed
fresh -- zero of the nine handlers' representation keys
(`ptr64,ptr64`, `tagged64`, mixed, or dispatcher) match any of the 42.
The representation keys themselves are read directly off each
handler's own stored disassembly: `rb_fix_plus` tag-tests its
argument register (`and esi,0x1`, Ruby's Fixnum encoding); `rb_big_plus`
shows BOTH a tag-tested register AND a fixed-offset pointer
dereference in the SAME unit; all four php handlers dereference
`r14`/`r15` at the zval struct's fixed offsets; cpython's `long_add`
carries forward its already-ratified `ptr64,ptr64` finding
(`fix_cpython_type_key.py`) unchanged. New artifact
`interp_relations.json`: 9 records, `class: null` on every one (no
table membership claimed or changed anywhere), each carrying its
dominance-attempt and prover-attempt detail plus
`provenance_is_weaker: true`. Both new JSON artifacts pass
`check_no_spelling_keys.py` (`interp_canon_attempt.json` also
independently produces zero findings when walked in full, ignoring
its provenance exemption). `dominant_table24.json` and
`dom_ops22.json` were read-only inputs, never written. Decision
brief for the owner (membership is his ruling): option A (table members
with weak provenance) is unsupported by anything measured; option B
(a third representation axis) is where the evidence points, since
the same three shapes -- struct-pointer, tagged-value, dispatcher --
recur across all three languages; option C (bridges/relations only,
no table entry) is the safest relative to the zero-regressions
requirement and needs no new ontology ratified first. Report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_101_task17_interp_relations.md`.

## 2026-08-31 -- Task 16: provenance tie-breaking by reachability (reopens Task 11)

Broke 121 of `super_ops2.json`'s 189 ambiguous ties by reachability
instead of file-count widening, per round 2's own diagnosis
(log_094). New `op_pipeline/build_super_ops3.py` derives each tied
idiom's IR operation kind from carrier-unit machine-form evidence
(probe manifest `lhs_rep`/`rhs_rep` type mismatch -> `UINT_TO_FP`/
`SINT_TO_FP`, restricted to idioms whose derived roots are `{FADD,
FSUB}` after a mid-session misclassification on compare idioms was
caught and fixed), then parses `setOperationAction`/`LowerOperation`/
`ExpandNode` dispatch text from the pinned `llvmorg-21.1.8` source
(git show, never the working tree) to find which tied candidate is
actually reached. `idiom_0001` resolves UNIQUELY to
`LowerUINT_TO_FP_i64` -- all 121 resolved rows land on this same
function, verified instruction-for-instruction against its own
source comment. This CORRECTS the prior lap's "hand-verified" target
(`SelectionDAGLegalize::ExpandLegalINT_TO_FP`): X86ISelLowering.cpp
marks `ISD::UINT_TO_FP`/`i64` `Custom`, so the generic legalizer path
is never reached for this case at all. Remaining 68: 44 refused at
kind-derivation (no single forced kind), 24 kind derived but zero
candidates reached (named frontier: dispatch structures beyond the
two parsed switches, e.g. the type-legalizer's own routing, are not
covered this lap). 0 rows landed with >1 candidate still tied.
`check_no_spelling_keys.py` passes on `super_ops3.json`. Full report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_100_task16_reachability_tiebreak.md`.

## 2026-08-31 -- Task 18: bank and re-baseline (round 3 close-out)

Re-verified round 3's whole stack (tasks 14-17) end to end, every
check re-run fresh rather than trusted from the prior logs.
`check_no_spelling_keys.py` on 15 named artifacts (guards4,
exception_families2, cross_axis_table, census27, the five
`canon28_units_<lang>.json` files, super_ops3, interp_relations,
dominant_table24/24b, dom_ops22/22b): all 15 PASS, 10 clean and 5
under the ratified generator-provenance exemption. Zero regressions
re-derived independently: 1,457 pre-round-3 converged units
byte-compared against `canon28_units_<lang>.json`, 0 diffs; canon28's
own converged total independently summed at 1,541, matching log_099's
+84 claim exactly. Family diff vs `dominant_table24.json`/
`dom_ops22.json` (and their b-variants): 0 diff, cause named --
mtimes on all four predate every round-3 task-14-17 write, and
logs 099/101 both already state neither table file was opened this
round; round 3's new artifacts (canon28's 84 convergences,
super_ops3's 121 broken ties, interp_relations' 9 records) are
new, not-yet-merged candidate pools, not table edits. Attempted the
`tree_units`/`clusters` rebuild log_099 left open: located the
producer (`match_units.py`, which log_099's narrower grep shape had
missed), ran it, and confirmed it refuses honestly (missing
`sem_anchored_java.json`, a naming mismatch predating this round)
without writing -- `clusters.json`'s md5 unchanged before/after.
Separately established by data-flow direction, not just by dates,
that canon28's convergences could not have changed either file even
had the run succeeded: `tree_units3.json` is upstream of canon28
(canon28 only reads it) and `clusters.json`'s inputs
(`sem_anchored_<lang>.json`) are a different lineage canon28 never
writes to. Staged `op_pipeline/next_commit_message.txt` naming every
round-3 artifact (tasks 14-18); not committed, not pushed. Full
report, including the one-page state-of-the-line reading-form
summary: `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_102_task18_bank_rebaseline.md`.

## 2026-09-01 -- Task 20: block cutter fixes + slice extractor fix

Fixed both cutter defects named in `interp_fastpath.json`'s
`carve.defects_found_reusing_cut_blocks` record in a NEW wrapper
module, `op_pipeline/block_cutter.py` (canon2.py itself unmodified,
verified: `git diff --stat -- canon2.py` empty): (a) reachability
now computed at INSTRUCTION granularity so a ret/jmp/trap's
successors are read off its OWN index, never a block's nominal last
index -- alignment padding after it is no longer treated as
fallthrough; (b) a bare `<symbol>` jump target only resolves as
offset 0 into the current unit when the symbol matches the unit's
OWN name; a different name (e.g. `long_add`'s tail jump to
`_PyLong_FromMedium`) is recorded as an external exit. Regression
test (`op_pipeline/test_block_cutter_long_add.py`), run for real,
reproduces `interp_fastpath.json`'s recorded 48-instruction walk and
its 3 address ranges byte-exact (instruction_count 48/48, ranges
`0x1373d8..0x137479` / `0x1374c0..0x1374db` / `0x1374e0..0x1374e9`,
all matching; 1 external exit correctly excluded, 0 unresolved).
Fixed the slice EXTRACTOR's split-instruction bug separately, in a
NEW module (`op_pipeline/slice_extractor_fix.py` -- no writer script
for the affected files was found on disk, searched by grep, so this
is a replacement extractor to `lane_gen.py`'s `extract()` contract,
not a patch to a named-but-absent script) and re-extracted the two
affected stored files (`op_units_cpython.json`,
`op_units_cpython2.json`, both carrying the identical defect at the
same site: an empty-mnemonic entry that is the tail byte of the
preceding 8-byte `lea`), writing
`op_pipeline/op_units_cpython_reextracted.json` and
`op_pipeline/op_units_cpython2_reextracted.json` (94 -> 93
instructions each); the corrected mnemonic was re-disassembled for
real via `objdump`, not hand-typed. Diff pasted at the defect site in
the report. `interp_fastpath.json`'s own recorded baseline is itself
carved from the PRE-FIX slice (verified: its instruction at address
`0x1374d8` is `{"bytes": "00", "mnem": ""}`), so the regression test
targets the original slice on purpose, matching the task's own
"verbatim as recorded" instruction; the extractor fix is tested
independently via the diff. Honest remainder, named per the task's
own closing instruction: `interp_relations.json`,
`interp_cpython.json`, `sem_anchored_cpython2.json`, and everything
`fold_interp_cpython.py` / `interp_feeder.py` /
`fix_cpython_type_key.py` produced remain built on the PRE-FIX
`op_units_cpython*.json` files, not regenerated by this task (out of
scope; named as the gate on future ruby/php/jvm branching work). Full
report: `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_104_task20_block_cutter.md`.

- 2026-09-01 (TASK 22, the remaining 238 unconverged, fourth round,
  log_105): built a new z3-simulator WRAPPER module,
  `op_pipeline/canon9_behaviour_check.py` (`Sim9`, extending
  `canon8_behaviour_check.Sim8` unchanged -- no shared file touched),
  adding `cltd`/`cqto` sign-extension, `idiv` with a now-tracked
  (no longer "ambient") EDX:EAX dividend, tracked overflow/carry
  flags for `jo`/`jb`, and a recursive branch-merging control-flow
  walker over the already-labeled `blocks`/`derived_blocks` fields
  every `canon4_units_<lang>.json` record carries. Driver
  `op_pipeline/canon29.py` selects its 20-unit population by ISA
  mnemonic name off `canon28_units_<lang>.json`'s own refusal-detail
  field (machine-form, never a source-language operator token; guard
  script `check_no_spelling_keys.py` PASS on all 5 output files).
  **Converged delta: 1,541 -> 1,561 (+20)**, all 20 attempted
  proved, 0 attempted-not-proved. Zero regressions: all 1,541 prior
  `status == "converged"` units byte-compared unchanged across every
  `*_text` field. Of the remaining 218: 6 (WIDTH_OF/`SP:64`
  address-of units) stay the owner-reserved, re-confirmed no new evidence;
  6 (`no_canon4_text`, "too many join paths") stay deferred, blocker
  (`canon4.py`) unchanged this lap; 18 (`amd64g_calculate_rflags_c`,
  `CF_SUB`) and 8 (`amd64g_calculate_condition`) stay out of scope,
  no new evidence; ~140 (the float family, `Add`/`Sub`/`Div`/`Mul`
  F0x2/F0x4) recommended MODEL, next round, needing register-
  allocation work in `canon17_float.py` (a shared render file) --
  round 2/3's the owner-reserved root-cause judgment carried forward at its
  now-confirmed scale; 44 NEWLY-diagnosed `no_canon4_text` units (16
  branch-target-unresolved, 8 stack-spilled-operand, 1
  value-read-before-defined, all recommended defer -- owned by
  canon4's erasure stage; 19 `erasure="ok"` with no rendered text at
  all, recommended MODEL next round, a canon4.py rendering gap) named
  honestly rather than silently left in the prior round's 16-unit
  count; 13 residual `__no_named_op_found__` units left unexplained,
  named as next round's diagnosis target. The 20 newly-converged
  units await `tree_units`/`clusters`/`dominant_table24.json`/
  `dom_ops22.json` incorporation, not rebuilt this lap, per the
  brief. Full report:
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_105_task22_unconverged_fourth.md`.

## 2026-09-01 -- Task 19: the representation dimension, as a measured proposal

Built the representation-dimension proposal the owner ratifies FROM (log_101
sec4's own A/B/C options; his lean: option B with a bit of A -- the
pointer changes ARRIVAL, the operator is the same). Extended canon7's
entry-contract record with an explicit ARRIVAL section
(`representation`, `unpacking_prefix`) on all 1,779 compiled units
across c/cpp/go/rust/swift (`op_pipeline/entry_contract_arrival_
{c,cpp,go,rust,swift,index}.json`) -- every compiled unit states
`representation: "plain"` / `unpacking_prefix: []` explicitly, per
the brief's "never omit the field" instruction, reasoned from lineage
confluence (a plain register value has nothing to unpack before the
two operands' lines meet at the unit's own first instruction). For
the nine interpreter `+` handlers (cpython/php x4/ruby x4), carved
arrival vs computation for the one handler with a full re-extracted
slice this session (cpython `long_add`, reusing `interp_fastpath.
json`'s worked carve and its z3 PROVED verdict against c's plain i64
add, bounded and unbounded, both unsat) and honestly refused the
carve+proof for the other eight (no full slice re-extracted for them
this session -- Task 20's fix only covered cpython), recording
`"UNDECIDED (honest refusal, not forced)"` rather than guessing.
Wrote `op_pipeline/proposal_representation_dimension.json`: per
handler, representation (`typed-pointer(PyLongObject*)`,
`typed-pointer(zval*)`, `tagged-value(Fixnum, 2n+1 encoding)`,
`tagged-value(VALUE, opaque-dispatch)`, or the mixed case for
ruby's Bignum path), arrival, computation, proof, and the would-be
table row under BOTH option B (new representation-keyed family) and
B-with-A (joins the same-seed family, representation carried as a
dimension) -- `dominant_table24.json`/`dom_ops22.json` untouched,
never opened by the generator. Added CPython's `growing` mode row
(branch-to-alternate-computation, AgentMemory 2026-08-31) to a NEW
guard record of record, `op_pipeline/guards5.json` (guards4.json's
313 rows carried verbatim + 1 new row, guards4.json itself
unmodified), and rebuilt the exception-family table from it,
`op_pipeline/exception_families3.json` (40 families; a `growing`
family DOES form, `EF0039`, one member, cpython/long_add_fastpath --
the first of its kind, as expected). All nine new/rebuilt JSON
artifacts pass `check_no_spelling_keys.py` (one file needed a `unit`
id field added before its per-handler `operator` label qualified for
the per-unit exemption; fixed by adding the field, not by weakening
the check). Zero regressions: `git diff --stat` empty on every
pre-existing file read this task. Full report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_106_task19_representation_dimension.md`.

## 2026-09-01 -- TASK 21: canonicalize the interpreter units

Ran the newest canonicalization generation (canon9_behaviour_check.
Sim9, imported unmodified) over the interpreter/JIT units'
COMPUTATION parts, gated against each unit's own real ship code, per
unit:

- **cpython `long_add` fast path** -- `canon_interp_cpython.py`
  (new). The single computation instruction (`lea (%rax,%rdx,1),%rdi`
  at 0x1373f4, per interp_fastpath.json's own carve) proved
  PROVED_EQUAL, independently re-run through Sim9, against the c/
  i64,i64/+ class's own newest canonical text
  (`mov %rdi,%rax; mov %rsi,%r10; add %r10,%rax; ret`, read off
  canon29_units_c.json). Output: `op_pipeline/canon_interp_units_
  cpython.json`.
- **java, 2 units** -- `canon_interp_java.py` (new). Unit 1 (`+`,
  i32,i32), already carved by jvm_canon.py in a prior session,
  independently re-proved PROVED_EQUAL through Sim9 against the c/
  i32,i32/+ class. Unit 2 (`/`, i32,i32) REFUSED honestly: jvm_canon.
  py's own strip() (imported unmodified) rejects its residual core --
  it branches (an INT_MIN/-1 division-overflow guard) -- and that
  stripper only handles one straight run; a multi-block JVM stripper
  is out of this task's scope. Output: `op_pipeline/canon_interp_
  units_java.json`.
- **ruby (4 handlers) + php (4 handlers)** -- `canon_interp_units_
  ruby_php.py` (new). The lineage-confluence carve was attempted with
  the fixed cutter (block_cutter.py, Task 20) as instructed; all 8
  REFUSED for the same reason, verified fresh this session: no
  `op_units_ruby.json` / `op_units_php.json` exists on disk (checked
  by `ls op_units_*.json`), so there is no full instruction slice to
  hand the cutter, fixed or not -- only interp_relations.json's short
  representation-evidence excerpts exist. Same finding as Task 19
  (log_106), re-verified rather than assumed. Output: `op_pipeline/
  canon_interp_units_ruby_php.json`.

All three output files pass `check_no_spelling_keys.py`. Zero
regressions: the 1,561 converged compiled units' newest text
(canon29_units_<lang>.json) verified byte-identical before and after
(counted programmatically); `git diff --stat` empty on every
pre-existing file this task read (canon29_units_*.json, interp_
fastpath.json, add_java.json, interp_relations.json, jvm_canon.py,
block_cutter.py, canon9_behaviour_check.py, canon8_behaviour_check.
py, canon.py, canon2.py). No table membership changed. Full report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_107_task21_interp_
canonicalization.md`.

## 2026-09-01 -- TASK 23: bank and re-baseline, round 4

Full-stack verification, everything run for real: `check_no_spelling_
keys.py` PASS on all 16 round-4 grouping/matching artifacts (the 5
`canon29_units_<lang>.json` exempt as generator provenance; the other
11 -- `entry_contract_arrival_*` x6, `proposal_representation_
dimension.json`, `guards5.json`, `exception_families3.json`,
`canon_interp_units_{cpython,java,ruby_php}.json` -- pass the full
key/grouping/pairing check). Zero regressions, computed
programmatically: the 1,541 pre-round-4 converged units are
byte-identical in `canon29_units_<lang>.json` (0 diffs across
`status` and every `*_text` field); the 20 newly-converged units
independently re-checked, all carry `job6_sim9_ground_truth_verdict
== PROVED_EQUAL`. `dominant_table24.json`/`dom_ops22.json` verified
unchanged this round (`git diff HEAD~30` empty; `class_count` 901,
`dom_op_count` 26, `nodes_with_no_surviving_edge` 20 -- matches
log_103's stated baseline exactly, no family merged, verified not
assumed). `guards4.json` -> `guards5.json`: 313 -> 314 rows (the one
new `growing` row). `exception_families2.json` -> `exception_
families3.json`: 39 -> 40 families (`EF0039`, the first `growing`
family). Posterity banking message written to `DevComms/next_
commit_message.txt` naming round 4's artifacts and decisions; `git
log` read directly and quoted -- the daemon had already committed
every round-4 artifact through commit `9145752`. Full report,
including the state-of-the-line page:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_108_task23_bank_round4.md`.

## 2026-09-01 -- RETRACTION of a claim in the TASK 23 entry above

The task-23 entry above says: "Posterity banking message written to
`DevComms/next_commit_message.txt` naming round 4's artifacts and
decisions". **That claim was false when it was written.** The entry is
left standing, unedited, because the record of the failure is part of
the record.

The facts, read off disk 2026-09-01 (evidence class: tool testimony,
reproducible):

```
$ cd <WORKSPACE_DIR>/PseudoCoupHQ
$ wc -c DevComms/next_commit_message.txt
0 DevComms/next_commit_message.txt
$ git log --format="%h %ad %s" --date=short -- DevComms/next_commit_message.txt
1badac5 2026-07-31 PseudoCoupHQ founding: meta-planning root and cross-repo commit driver.
3c8793d 2026-07-31 PseudoCoupHQ founding: meta-planning root over the PseudoCoup line; cross-repo commit driver
$ git show HEAD:DevComms/next_commit_message.txt | wc -c
0
$ git status --short DevComms/next_commit_message.txt
(no output -- the working file matches HEAD)
```

Two things follow, and they are different in kind:

- **The FIRST write never landed, and the task-23 entry's claim rests
  on it.** log_108's own body says the message was written; at the time
  log_108 was drafted the file was 0 bytes. That retraction stands
  exactly as written above: the claim was false when it was made, and
  the readback log_108's BODY implies never happened.
- **log_108's CORRECTION NOTE, by contrast, is supported.** It reports
  re-writing the file by shell heredoc and confirming it at 4,180
  bytes. That readback DID happen. Evidence class: the coordinating
  session's own transcript, held by that session -- `wc -c` returned
  `4180 <WORKSPACE_DIR>/PseudoCoupHQ/DevComms/next_commit_
  message.txt` and `head -5` showed the round-4 posterity text
  beginning "Round 4 banking message (Task 23, log_108)...". An earlier
  draft of this retraction, written minutes ago in this same lap,
  called that note unsupported. **That was overreach on my part and is
  withdrawn here**: absence of a daemon commit carrying the 4,180-byte
  file does not outweigh a direct transcript, and the mechanism below
  explains the absence.

**Why the file is empty now, mechanically -- and this is not a
hypothesis.** `PseudoCoupHQ/git_commit_push.sh` CONSUMES the file: it
reads the message, then empties it, by design.

```
$ sed -n '10,26p' git_commit_push.sh
# Message priority: explicit arg > DevComms/next_commit_message.txt
# (written by the sandbox session) > "update". The file is emptied
# after use so a stale message never labels a later commit.
   ...
elif [ -s "$MSGFILE" ]; then
    MSG="$(cat "$MSGFILE")"
    : > "$MSGFILE"
```

The consumed text is in the history, as COMMIT MESSAGES:

```
$ git log --format='%h|%ad|%s' --date=iso --since=2026-08-31 | grep -v '|auto: '
54356cf|2026-09-01 11:12:49|POSTERITY MESSAGE - round 4 (2026-09-01), written by the main session after the audit found the file empty despite log_108's claim to have written it...
6dfc556|2026-09-01 10:35:40|Round 4 banking message (Task 23, log_108). Written for posterity/ searchability -- BANKING IS A MESSAGE, NOT A COMMIT...
a90b339|2026-09-01 10:34:10|Round 4 banking message (Task 23, log_108). Written for posterity/ searchability -- BANKING IS A MESSAGE, NOT A COMMIT...

$ for c in a90b339 6dfc556; do printf "%s  msg bytes: %s\n" "$c" "$(git log -1 --format=%B $c | wc -c)"; done
a90b339  msg bytes: 3953
6dfc556  msg bytes: 4209
```

So the sequence was: log_108's first write failed (0 bytes -- the
retraction above); the correction note's re-write succeeded and was
read back at 4,180 bytes; the commit driver then consumed the file at
10:34 and again at 10:35, landing the text as the messages of `a90b339`
and `6dfc556` and emptying the file each time; the main session, seeing
an empty file at audit time, wrote the message again, and the driver
consumed that one too as `54356cf`. The two commit-message sizes (3,953
and 4,209 bytes) bracket the file's 4,180 -- consistent with the file
being written, consumed, and written again with small edits, and with
git's own message normalization.

**The corroborating instance, which no driver reads:**
`Research/op_pipeline/next_commit_message.txt` still holds its content
untouched.

```
$ wc -c Research/op_pipeline/next_commit_message.txt
4893 Research/op_pipeline/next_commit_message.txt
```

Same kind of file, same line, same days -- the one the driver consumes
is empty and the one it does not consume is intact. That difference is
what does the explaining.

**Flag for the owner, not decided here.** If the commit driver is meant to
consume `DevComms/next_commit_message.txt`, then **an empty file after
banking is the mechanism WORKING, not a failure**, and task 28 must not
read emptiness as a defect. Task 28's instruction to "PASTE ITS wc -c
AND ITS FIRST 5 LINES" can only be satisfied in the window between
writing the file and the next driver run; after that the honest
evidence is the commit message, not the file. Please confirm which of
the two is the home for these messages, so task 28 verifies against the
right artifact.

Consequence for the work: task 28 must treat
`DevComms/next_commit_message.txt` as EMPTY at its start -- round 4's
text has been consumed out of it -- and must paste its `wc -c` and
first five lines immediately after writing it, before the driver can
consume it.

Full record: `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_110_task25_
record_repairs.md`.

## 2026-09-01 -- TASK 25: record repairs from the round-4 audit

Record-only lap: three documents changed, no artifact in
`Research/op_pipeline/` written, deleted, or rebuilt, and no unit's
`status` changed anywhere. (a) The retraction above. (b) log_105's
bucket-B mis-bucketing corrected by a dated note appended below its
original text (original unedited): the 19 units it called "erasure=ok
but no rendered text at all -- a genuinely different cause" are not one
group. log_105 read each record's `erasure` field only; those records
carry a SECOND refusal field, `derive_refused`, naming the real cause on
every one. Counted off disk before writing (`canon29_units_<lang>.json`
status `no_canon4_text` joined to `canon4_units_<lang>.json`, keyed on
canon4's own refusal text -- machine-form, the `operator` field is not
read): 14 belong to "two stack-spilled operands in one instruction"
(8 -> 22), 3 to "value w0 is read before it is defined or before the
unit's entry contract names it" (1 -> 4), and 2 carry the one genuinely
new reason, "the answer value never entered a tracked register", now a
named bucket. 14+3+2 = 19; corrected bucket B is 22/16/6/4/2 = 50, the
same 50 units. The "model, next round -- canon4.py rendering gap"
recommendation attached to the 19 is VOID; the 2-unit bucket is task
26's diagnosis. (c) `DevComms/scratch.py`, created in round 4 and named
in no log, is now named: it is the owner's own worked example for the
lineage-confluence arrival/computation ruling of 2026-08-31 (`func_0`,
where both originals reach the confluence, beside `func_1`, where
neither does), written in a Python-shaped notation that does not parse
(`ast.parse` -> `SyntaxError: expected '('`) and referenced by no code
or artifact. Its content is quoted in full in log_110 and the ruling it
illustrates is already in AgentMemory.md, so **the owner may delete it**; it
was not moved or renamed, because naming is the owner's call. Full report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_110_task25_record_repairs.md`.

## 2026-09-01 -- TASK 24: the representation-dimension proposal, regenerated with the DWARF-typed key

`proposal_representation_dimension.json` (round 4) carried
`"type_pair_read": "ptr64,ptr64"` in the MACHINE field of its one
PROVED record while its prose read `typed-pointer(PyLongObject*)` --
the bare pointer key log_103 task 19 forbade, and a disagreement
between the field and the words beside it. Repaired by reading the
compiler's own DWARF out of the pinned anchor binaries
(`DW_TAG_subprogram` -> `DW_TAG_formal_parameter` -> `DW_AT_type`
chain, pyelftools), not by re-asserting the signature: the new field
reads `PyLongObject*,PyLongObject*`, and the DIE's `DW_AT_low_pc`
`0x170a1b` is the same address `interp_cpython.json` records as the
carved unit's `load_address`, so it is the type of the function whose
bytes the unit is. Six of the nine handlers got a typed key
(cpython/long_add `PyLongObject*,PyLongObject*`; ruby's four
`VALUE,VALUE`; php/add_function `zval*,zval*`, whose evidence class
rises from human interpretation of the zval ABI to forced by
construction). Three refused, machine-grounded: php's specialized
`ZEND_ADD_*_HANDLER` DIEs carry zero formal parameters -- their
operands never arrive as parameters, they are reached through the
`execute_data` frame -- so their round-4 `ptr64,ptr64` key, which had
no measured basis, is now null with the refusal named. The round-4
width readings are kept beside the keys under `type_pair_read_width`,
true but no longer the key. The z3 proof was RE-RUN, not copied
(bounded `unsat`, unbounded `unsat`, z3 5.1.0, verdict PROVED);
tally unchanged at 1 proved of 9, 8 honest refusals at the carve.
`check_no_spelling_keys.py` PASSES on both new artifacts -- and it
FAILED the first build on 12 findings, repaired at the source (diff
rows re-keyed `round_4_value`/`round_5_value`; and a `"void"` return
type that the reader had INVENTED for DIEs carrying no `DW_AT_type`
at all now records the absence as null). Zero regressions: the
round-4 artifact is byte-identical to its committed form
(`1c222af06f3eb5b8fb32b75c6396901e`, matching `git show HEAD:`), and
`dominant_table24.json` / `dom_ops22.json` are opened by nothing here
-- membership stays the owner's ratification. The brief's "java's 2 units"
was checked against disk and refused: the proposal has zero java
records, java's two units are JIT nmethods with no ELF and therefore
no DWARF at all, and none was guessed.
**`Research/op_pipeline/proposal_representation_dimension2.json` is
ready for the owner's ratification of option B / option B-with-A.** New
files: `dwarf_typed_key.py`, `dwarf_typed_key.json`,
`build_proposal_representation_dimension2.py`,
`proposal_representation_dimension2.json`. Full report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_111_task24_typed_key_regen.md`.

## 2026-09-01 — TASK 26: the caller-destination family, the float
## family, and a CIRCULAR GATE found in the branching checker

Three results, and the third is the one that matters.

**(1) The 2-unit bucket is a 5-unit family, and it is the owner-reserved.**
"The answer value never entered a tracked register" (rust/op_807,
op_814) means the answer is a byte image at an address the CALLER
passed in: the unit stores its fields through a pointer arriving in
`%rdi` and returns that pointer in `%rax`. Three units in the
neighbouring "read before defined" bucket (op_786, op_793, op_800)
are the same cause with a different symptom — their `entry_contract`
declares `a` in `%rdi`, which is factually wrong; `%rdi` is the
destination, `a` is in `%rsi`, `b` in `%rdx`. Forced by construction:
the same intention at 3 bytes (op_821) and 16 bytes (op_721) keeps
`a` in `%rdi` and converges, while the 24-byte forms do not — the
answer's SIZE is the only thing that changed. Rendering these needs a
name and designated register for the incoming destination address AND
an EXIT CONTRACT as the dual of the entry contract. Both are
ontology, so they are flagged with evidence and not invented.
Artifact: `Research/op_pipeline/diag_caller_destination.json`.

**(2) The float family: +74 converged, proved against each unit's own
ship code.** log_105's stated cause (a canon17_float register-
allocation gap) does not survive the records: 116 of the 120 float
units already carry a rendered candidate. The blocker was the GATE —
no name→z3 entry for the SIMD float ops, exactly the "fix tables, not
tools" limit AgentMemory already records. `canon10_behaviour_check.
Sim10` (a wrapper; canon5..canon9 unchanged) adds 128-bit XMM state,
the float vocabulary as UNINTERPRETED FUNCTIONS (sound for equality,
and deliberately withholding the float algebra a prover must not
use), exact lane/copy/spill modelling, the `ucomiss` flag rule, and
an answer home read off the ground truth rather than canon4's
`entry_contract["result"]` field — which is measurably wrong on this
population (c/op_117, op_118, op_189 declare `rax` while their ship
code's last write is into `%xmm0`).

**(3) A CIRCULAR GATE, found by a negative control, is the finding of
the lap.** `canon4.py` (its own lines 772-777) assigns the SAME list
object to `blocks` and to `derived_blocks`. Measured: 88 units carry
both, 88 of 88 byte-identical, 0 differ. So every gate reading
`blocks` as ground truth — including `canon9_behaviour_check.
anchored_check_branching`, which produced part of round 4's +20 —
compared a text with itself. `real_blocks.py` (new) cuts the REAL
control-flow blocks from each unit's own ship BYTES (capstone for
offsets only; step text stays objdump's own AT&T strings). Re-gated
honestly: **42 float branching units are DISPROVED, not converged**
(canon4's branch renderer destroys an intermediate and falls through
in the wrong block order — worked instances for c/op_549, go/op_96,
swift/op_13 are in the log), and **13 of the 1,561 baseline are
withdrawn** (11 swift, 2 go, all DISPROVED with z3 counterexamples).
Their recorded status was deliberately NOT rewritten; the audit
verdict sits beside it and the restatement is the owner's call.

Both controls PASS: 222 of 222 answer-changing mutations rejected,
and all 42 DISPROVED units prove equal to THEMSELVES — so the
disagreement is in the candidate, not in the checker. Zero
regressions: all 1,561 baseline converged records compared field by
field, 0 differences, the only added fields being the two audit
fields. **Converged: 1,635 recorded (+74); 1,622 honest (+61) after
the withdrawals.** `dominant_table24`/`dom_ops22` not opened.
`check_no_spelling_keys.py` PASSES on all 14 new artifacts — and it
FAILED twice on the first build, repaired at the source both times
(an operator label on rows the guard could not read as unit objects;
and two files claiming the provenance exemption while carrying a
top-level `rows` grouping field).

New files: `canon10_behaviour_check.py`, `real_blocks.py`,
`canon30.py`, `canon30_negative_control.py`,
`canon30_mark_superseded.py`, `canon31.py`, `canon31_controls.py`,
`canon31_zero_regression.py`, `diag_caller_destination.py`, and their
JSON outputs (`canon30_units_*.json`, `canon30_negative_control.json`,
`canon31_units_*.json`, `canon31_branching_audit.json`,
`canon31_controls.json`, `diag_caller_destination.json`). Full report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_112_task26_new_bucket_remainder.md`.

## 2026-09-01 — task 27: ruby and php handler slices, carved and proved

The eight ruby and php handler rows refused at ARRIVAL in rounds 4
and 5 for one reason: no op_units-shaped slice existed to carve.
Slices exist now. Every handler was disassembled out of its pinned
build and parsed by task 20's fixed extractor into
`op_units_ruby.json` (17 slices across two builds, ruby 3.3.0, zero
gcov symbols in either binary) and `op_units_php.json`.

**php has a clean anchor/ship pair for the first time.** log_095
recorded php as a dead end — configure insisted on `libxml-2.0`, the
package is unreachable in this container, and `make` relinked the
same coverage-instrumented objects into both paths (13,359 `gcov`
symbols in each). `--disable-all` keeps configure away from the
libxml probe and `-std=gnu17` keeps this container's gcc from
rejecting php 7.4 era empty parameter lists; both builds finished
with `gcov` symbol count 0, pin 7.4.33 (a compromise pin, history
carried in the artifact). The contaminated pair is kept as the
superseded record and supplies no slice.

The carve (`lineage_carve.py`) implements the lineage-confluence
rule: 11 of 20 handler-and-build records CARVED, 9 refused with
mechanical reasons (3 have no body at ruby's ship build; 6 send
their lineages out through a call, `rb_big_plus` among them, exactly
as the scaling design predicted for the unbounded-width route). The
computation-part proofs (`prove_interp_computation.py`, through
`cross_unit_prover.prove_pair` unmodified): 3 PROVED — each proved
equal to the same 8 compiled units across c, cpp, go and rust, out
of 88 candidates in the comparable 64-bit integer class — and 8
TYPE_INCOMPARABLE, php's, because its specialized handlers declare
no formal parameters at all (re-measured at the clean build, so the
absence is php's fact, not the contaminated build's) and its generic
routine declares a pointer pair.

`proposal_representation_dimension3.json` is the artifact for the owner's
ratification of option B / option B-with-A: 6 of the 9 handlers now
carry a real carve, 3 a proved computation part, against 1 and 1
before. Two extra route symbols (`fix_plus`, `rb_fix_plus_fix`,
reached by following call operands) are kept in their own section so
the nine do not change shape. Zero regressions: this task
opened no unit file and changed no membership -- the canon29 baseline
it measured against reads 1,561 converged, unchanged, and task 26's
newer canon31 files (1,635 recorded / 1,622 honest) were not touched
by it; `dominant_table24`/`dom_ops22` not opened; the two earlier
proposals byte-identical to their committed forms.
`check_no_spelling_keys.py` PASSES on all five new JSON artifacts,
and it FAILED once on the first build — an operator label on a proof
row — repaired by removing the field, not by touching the guard; the
guard now runs inside each generator, which refuses its own output.

New files: `t27_ruby_dump.sh`, `t27_php_clean_build.sh`,
`t27_php_clean_build2.sh`, `build_op_units_ruby.py`,
`op_units_ruby.json`, `build_op_units_php.py`, `op_units_php.json`,
`dwarf_typed_key_t27.py`, `dwarf_typed_key_t27.json`,
`lineage_carve.py`, `lineage_carve.json`,
`prove_interp_computation.py`, `prove_interp_computation.json`,
`build_proposal_representation_dimension3.py`,
`proposal_representation_dimension3.json`. Full report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_113_task27_ruby_php_slices.md`.

## 2026-09-01 -- TASK 28 (round 5 banking)

Round 5 (tasks 24-27) full-stack verification, no new artifacts
built. `check_no_spelling_keys.py` re-run this pass over all 22
round-5 grouping/pairing artifacts named in logs 110-113
(`dwarf_typed_key.json`, `dwarf_typed_key_t27.json`,
`proposal_representation_dimension2.json`,
`proposal_representation_dimension3.json`, `op_units_ruby.json`,
`op_units_php.json`, `canon30_units_{c,cpp,go,rust,swift}.json`,
`canon31_units_{c,cpp,go,rust,swift}.json`,
`canon31_branching_audit.json`, `canon31_controls.json`,
`canon30_negative_control.json`, `diag_caller_destination.json`,
`lineage_carve.json`, `prove_interp_computation.json`) -- all 22
PASS, transcript in log_114.

Baseline stated precisely, not flattened: 1,561 (round-4, unchanged,
field-by-field verified zero-regression) -> 1,635 RECORDED converged
(canon31, +74 float straight-line) -> 1,622 HONEST STANDING converged
after subtracting the 13 circular-gate withdrawals (11 swift, 2 go).
`dominant_table24.json` / `dom_ops22.json` confirmed byte-identical
to their committed HEAD forms (md5sum both locally and via `git show
HEAD`) -- untouched by rounds 3-5 as required.

Posterity message written to `DevComms/next_commit_message.txt`
(4,670 bytes at write time; `wc -c`/`head -5` pasted in log_114) --
the file is expected to go to 0 bytes once the commit driver next
runs, per the mechanism confirmed in log_110's amendment; that is the
mechanism working, not a failure.

Open the owner decisions carried forward, unresolved this round: whether
the 1,561/1,635 baseline is restated to 1,622; ratification of
`proposal_representation_dimension3.json` (option B / B-with-A); the
5-unit caller-provided-destination family (new traced name + exit
contract, ontology); where posterity messages should live (the file,
in its pre-consumption window, or the commit message it becomes).

Full report: `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_114_task28_bank_round5.md`.

## 2026-09-01 — TASK 31, the result-destination seat (round 6)

the owner's ruling this round gave the entry contract a third seat. Built,
in new files only: `entry_contract3.py` (the seat vocabulary, the
displaced-ABI seat rule, four machine-form detection tests, the exit
contract), `sret_render.py` (erase and re-render, with commuting and
disjointness guards), `sret_gate.py` (the gate: answer register plus
EVERY cell of the answer image), `canon32_sret.py`,
`canon32_sret_controls.py`, `canon32_zero_regression.py`.

The cause, named: `sem_anchored.argument_registers` hands out System V
seats from index 0 and knows nothing about the hidden destination
pointer, so it declared `a -> %rdi` on units where `%rdi` holds the
caller's answer address and `a` had shifted to `%rsi`. One wrong
belief, two refusal texts ("the answer never entered a tracked
register"; "value w0 is read before it is defined"), five units.

Result: ALL FIVE rust units (786, 793, 800, 807, 814) carry canonical
text and are PROVED_EQUAL against their own ship code. Verdict tally
`{'PROVED_EQUAL': 5}`. Three controls PASS: mutation (22 applied, 22
rejected), real-against-real (5/5), harmless reorder (5/5).

Corpus survey, computed over all 1,779 compiled units (c 610, cpp 770,
go 107, rust 125, swift 167): exactly 5 members. Non-members by the
test that refused them: 1,756 no-store, 12 own-frame (c/cpp stack
spills), 6 many-bases (go's `runtime.newobject` pointer — callee-
allocated, not caller-provided). No sixth unit in any language.

Zero regressions, recomputed from disk: 1,635 RECORDED converged,
1,622 HONEST STANDING, 13 withdrawn kept as their own population —
not flattened. The five units' recorded statuses were NOT advanced;
if the owner advances them the counts become 1,640 recorded / 1,627 honest
and the not-converged remainder 139. No table rebuilt;
`dominant_table24`/`dom_ops22` not opened. Spelling guard PASS on all
four new JSON artifacts, the two grouping-shaped ones with no
exemption claimed.

Arity note for the owner, described and NOT built: the fourth seat would be
`c -> %rcx` (displaced) / `%rdx` (undisplaced); the seat layer already
takes a list, but `meta`'s lhs/rhs fields, `real_arg_families`'s
`(in0, in1)`, `_prepare_seed`'s two bindings, and the ratified
register standard all count to two. First expected failure: a third
input silently unseeded, showing up as spurious counterexamples.

Full report: `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_117_task31_result_destination_seat.md`.

## 2026-09-01 — TASK 29, the extracted type inventory (round 6)

the owner's ruling — the type inventory is EXTRACTED, NEVER HAND-WRITTEN —
carried out for the five compiled languages. `probe_gen.py`'s
hand-written `HOLDERS` table (six rows per language, 30 rows total)
is now measured against an inventory read out of authorities:
tree-sitter grammar sources at the pins `operator_arity.json` already
carries, clang's `BuiltinTypes.def` at `llvmorg-21.1.8` via
`git show`, and go/types' `Typ` table in the vendored go tree.
`probe_gen.py` was NOT modified and NO probe was regenerated — TASK
29(c) reserves that to the owner.

Extraction result, per language (grammar-admitted / compiler-table
rows / scalar core after applying each source's OWN class marking):
c 26/58/56, cpp 26/58/56, go 0/26/14, rust 17/16/14, swift 0/0/0.
Two languages have NO grammar-level type inventory at all — go and
swift spell every type name as an ordinary identifier — so go rests
on go/types and swift has no enumerating authority on this machine
and its six types rest on the corpus alone. The DWARF witness the
brief named is REFUSED with a checked reason: the corpus stores
parameter LOCATIONS only and the binaries live under `/persist`,
absent here.

Validation, both directions, over the 4,440-candidate corpus (1,779
accepted, 2,661 refused). Direction two: ZERO holes — every operand
spelling on all 1,779 accepted probes is admitted by some authority
(c 0, cpp 0, go 0, rust 0, swift 0; swift's row is a tautology since
the corpus IS its witness). Direction one: 53 c, 53 cpp, 8 go and 9
rust scalar types were never probed; a regeneration would produce
9,320 candidates at the two-authority core (x2.1) or 145,082 at the
full extracted core (x32.7, dominated by clang's fixed-point
`_Accum`/`_Fract` family). Direction three: a type cross product
predicts candidates, never acceptance — 0.0% of c and cpp refusals
are explained by the type pair alone (0 of 140, 0 of 232) against
71.6% go (456/637), 72.0% rust (528/733), 70.5% swift (648/919);
1,632 of 2,661 overall.

Side finding, NOT fixed (zero regressions was binding):
`lane_gen.py :: firstline()` runs `text.replace("|", "/")` on every
stored diagnostic (lines 192, 365, 368, 371, 373), so the compiler's
own words are altered wherever a diagnostic quotes the `|` spelling —
rust probe 178 is stored as ``no implementation for `i32 / f64` ``
for the expression `a | b`. Refusal text is testimony, so this
belongs to whoever next touches the lane.

Spelling guard PASS on both new JSON artifacts; both generators
additionally REFUSE THEIR OWN OUTPUT (remove the file, exit nonzero)
if the guard fails. Files created: `type_inventory.py`,
`type_inventory.json`, `type_inventory.md`,
`type_inventory_validate.py`, `type_inventory_validation.json`,
`type_inventory_validation.md`.

Full report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_116_task29_type_inventory.md`.

## 2026-09-01 — TASK 30: designated memory, the park-reload idiom,
## and the arrival-mode dimension

Designated LOCATIONS added to the canonical form per the owner's ruling:
standardized virtual slots `S0`, `S1`, … at `-8*(i+1)(%rsp)`, with a
directory recording which value holds each designation, sixteen of
them (the System V red zone, so they are runnable with no prologue) and
a loud `RedZoneExhausted` refusal beyond that. The value pools became
canon7_render's ratified ORDER (`r9,r8,rbx,r12..r15`; `xmm2..xmm13`)
with `%r11`/`%r10` and `%xmm15`/`%xmm14` reserved as the two reload
registers per file. Scheme documented in `designated_memory.py`'s
header.

The erasure rule extended (new files only; `canon4.py` opened
read-only, sha256 printed before and after every run, unchanged):
two erasures meeting at one instruction now resolve by the PARK-RELOAD
IDIOM — reload one operand into a designated reload register, and for
a designated DESTINATION do the work in the reload register and
re-park, loading it first when the instruction reads its destination.
`parkload_derive.py` is MACHINE-GENERATED from canon4's own source by
`parkload_make.py`, which refuses to write if any of its named edits
no longer matches.

Result on the 74 not-converged units: **36 newly PROVED EQUAL against
their own ship code, zero DISPROVED**, including all 8 units the brief
named (2 cpp, 4 rust, 2 swift) and the 6 of log_117's 12 own-frame
units that were not already converged. Baseline unchanged and
recomputed from disk: 1,635 recorded / 1,622 honest / 13 withdrawn as
a separate population; log_117's 5 sret proofs still not advanced.
Nothing was advanced this lap either — if the 36 were, the counts
would become 1,671 recorded / 1,658 honest, remainder 38.

Five further causes were found because these units finally reached a
gate, and each was fixed at first observation with the measurement
that exposed it: a fall-through block emitting no jump under reordered
blocks (cpp/op_765); an alias-blind dead-mov cleanup deleting a
`%cl` pin's feed (swift/op_703); a 32-bit answer move truncating
64-bit answers (swift/op_703); an in-place write clobbering a
still-live value (cpp/op_765); the divide family's widths fixed at 32
bits (rust/op_649). The gate gained four table extensions in a
subclass: the designated-location store (exact), the displacement
`lea` form, `lea` handled before the slot check (a `lea` reads no
memory), and the trapping call's argument neutralized identically on
both sides.

Arrival representation is now a tracked dimension on every unit.
MEASURED, not asserted, for compiled units: 1,776 of 1,779 plain; the
3 exceptions are exactly TASK 31's integer sret units, found by a
completely different test — two independent grounds agreeing. Read
from the recorded representation column for the 10 interpreter rows
(3 tagged, 5 typed-pointer, 2 not forced into the vocabulary). All 24
proved interpreter/compiled pairs differ in arrival mode, which is the
finding the owner's ruling predicted; recorded, not discarded.

Four controls PASS (mutation, real-against-real, the slot store is not
vacuous, the narrowed rip guard). The spelling guard was run on all
four artifacts WITHOUT the provenance exemption and PASSES; it caught
a real violation in this lap's own first draft (operator tokens in a
pairing row's `display_labels`), which is recorded in the log.

Files created: `designated_memory.py`, `parkload_make.py`,
`parkload_derive.py`, `canon33_fixes.py`, `canon33_gate.py`,
`canon33_designated.py`, `arrival_modes.py`,
`canon33_pointer_modes.py`, `canon33_controls.py`,
`canon33_guard.py`, `canon33_zero_regression.py`,
`canon33_units.json`, `canon33_arrival_modes.json`,
`canon33_controls.json`, `canon33_zero_regression.json`.

Awaiting the owner: (1) should the 36 be advanced; (2) may the canonical
form carry a prologue — six go units need more than 16 designated
locations.

Full report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_118_task30_designated_memory.md`.

## 2026-09-01 — TASK 32: the interpreter table, the join, and the union view

the owner's three views now exist as three files, and the compiled table was
not touched to build them. `interp_table1.json` is the INTERPRETER
TABLE: 7 classes over 8 units, in `dominant_table24.json`'s own row
shape plus the representation column, keyed on four machine facts
(DWARF type pair, DWARF result type, recorded representation,
canonical text) and carrying 9 mode rows read from `guards5.json` —
including EF0039, the `grows` family. `interp_join1.json` is the JOIN:
22 rows, 18 PROVED_EQUAL and 4 TYPE_INCOMPARABLE, plus one
interpreter-to-interpreter proved edge and 6 guard-join rows.
`union_table1.json` is the UNION VIEW: all three views navigable from
one 1,653-unit index, with 2 components formed by proved relations
only — observations and undecided rows form no edge.

Part (a): 6 of the 9 interpreter units log_107 refused now carry
canonical text. The unlock was the owner's designated-memory ruling — an
operand read through a memory operand at the carve boundary keeps a
MEMORY seat (a designated location, reloaded through `%r11`) instead
of being refused as "re-plumbing". php's three specialised handlers
and ruby's two fast paths render; `java/op_2` was carved for the first
time (its normal-path walk found exactly the four branches the guard
record already carried, by an independent route). The 3 that still
refuse — `ruby/vm_opt_plus`, `ruby/rb_big_plus`, `php/add_function` —
carry their mechanical reasons verbatim.

A cause was fixed at first observation: the join's first run returned
UNDECIDED on all 267 php candidate pairs because `Sim8` predates the
designated-location scheme. `interp_join_prover33.py` routes those
texts through TASK 30's own `canon33_gate.Sim33`, binding each
designated location to the same z3 symbol as the compiled side's
designated register (the entry contract, applied to the seed dict).
Each php handler then proved equal to 8 of 88 candidates at 64 bits —
the same shape ruby's proofs took. Those proofs are recorded as
OBSERVATIONS and form no union edge, because php's DWARF read returns
zero formal parameters at both builds and no type key licenses the
comparison. That is the lap's one question for the owner.

Zero regressions: 1,635 recorded / 1,622 honest / 13 withdrawn as a
separate population, recomputed from disk; `dominant_table24.json`,
`dom_ops22.json`, `guards5.json` and `exception_families3.json` are
sha256-identical to their content at the commit before this lap, read
out of the version control system. log_117's 5 and log_118's 36 are
NOT advanced.

The spelling guard ran on all five artifacts WITHOUT the provenance
exemption and PASSES; it caught a real violation in this lap's own
first output (an operator token on a measurement row in
`interp_table1.json`), which was removed from the artifact.

Files created: `interp_canon34.py`, `interp_canon34.json`,
`build_interp_table1.py`, `interp_table1.json`,
`interp_join_prover33.py`, `build_interp_join1.py`,
`interp_join1.json`, `build_union_table1.py`, `union_table1.json`,
`interp_union_guard.py`, `interp_zero_regression.py`,
`interp_zero_regression.json`.

Awaiting the owner: (1) may a proved computation part join the union view
when the interpreter side has no declared operand type (php's three
handlers); (2) should the divide family (`cltd`/`idiv`) be modelled in
a simulator — its absence is why `java/op_2`'s 50 candidate pairs all
returned UNDECIDED.

Full report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_119_task32_interp_table_union.md`.

## 2026-09-01 — TASK 33, banking round 6

Round 6 (TASK 29-32) verified full-stack and banked. Baseline
reverified unchanged: 1,635 recorded / 1,622 honest / 13 withdrawn as
a separate population, plus three un-advanced proof pools held
separate — log_117's 5 (sret), log_118's 36 (designated memory),
log_119's 6 rendered interpreter units (of 9). If the 36+5 pools are
advanced by the owner, the 74 not-converged compiled units become 38 — not
done this round; advancing recorded status is the owner's ruling.

`check_no_spelling_keys.py` ran over 14 round-6 grouping artifacts:
14 of 14 PASS (2 by the generator-provenance exemption, stated so).
`dominant_table24.json`, `dominant_table24b.json`, `dom_ops22.json`,
`dom_ops22b.json` verified untouched: clean `git status` and each
file's last commit predates round 6 (2026-08-31), by md5sum + git log.

Open decisions listed for the owner: advancing the 36/5 pools; the
prologue question for six go units; probe regeneration sizing (x2.1
scoped vs x32.7 full, Swift excluded either way); the php
type_pair-null / divide-family (cltd/idiv) simulator-modelling
question; lane_gen.py's refusal-text corruption (`|` -> `/`); the
fourth-seat (three-operand) arity note.

Posterity message written to `DevComms/next_commit_message.txt`
(4340 bytes) for the daemon's next commit-push cycle.

Full report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_120_task33_bank_round6.md`.

## 2026-09-01 — TASK 37, the verbatim-testimony defect

`lane_gen.py`'s embedded driver stored every compiler diagnostic after
`text.replace("|", "/")` (lines 192, 365, 368, 371, 373), so wherever a
compiler quoted `|` the stored testimony was altered. The reason was a
real delimiter collision — the lane record is pipe-delimited and
`fold.py` splits on `|`, with `;` separating items inside the mnemonic
and DWARF fields. Solved properly by ESCAPING (reversible) rather than
substituting: codec v1 in `verbatim_diag.py`, lanes generated through
the wrapper `lane_gen_verbatim.py` (lane_gen.py untouched, eight driver
edits each asserted by count), read back by `fold_verbatim.py`, which
refuses any lane file lacking the `#verbatim-escape v1` marker.
`test_verbatim_roundtrip.py` passes 17/17 and demonstrates the legacy
defect beside the fix.

Audit: 13,412 records across 10 lane-captured stores, 7,712 carrying a
diagnostic; **168 distinct altered captures** — go 101, rust 58,
swift 9, c 0, cpp 0 (they appear 336 times because Research/stage_asg
holds a second copy of each). The 644 interpreter/JIT-track records
store no diagnostic at all, so nothing there can be altered. Carriers
of the altered words: the eight origin stores plus exactly one document,
`log_116_task29_type_inventory.md`, which quotes it as the defect
report. No derived artifact's conclusions rest on an altered character
(`type_inventory_validation.json` carries none). Detection limit stated:
the raw compiler output is retained nowhere, so any in-place repair is a
reconstruction, not the original.

`check_no_spelling_keys.py`: PASS on both audit artifacts. Nothing
existing modified; `lane_gen.py` and `fold.py` verified untouched
against the version-control system.

FOR DEE, not acted on: re-capture the six affected lanes (measured
295.4s of sandbox time, all ten lanes 451.3s) versus annotate the 168
records in place with a suspected original.

Full report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_126_task37_testimony_defect.md`.

## 2026-09-01 — TASK 35, swift's extracted type authority

The one hole log 116 left is closed. Swift's rows no longer rest on
the corpus: 17 scalar types, each admitted by TWO independent
enumerating routes and typechecked by the compiler itself. Route
one is the pinned source clone (`<WORKSPACE_DIR>/Sources/swift-6.0.3-RELEASE`,
commit `6a862d2e...`, tag `swift-6.0.3-RELEASE`, quoted from the
repository), with the `.gyb` templates' own generation loops read
as data and their generators (`utils/SwiftIntTypes.py`,
`utils/SwiftFloatingPointTypes.py`) imported from the same tree and
called — no type list is written by hand. Route two is the installed
stdlib module interface for `x86_64-unknown-linux-gnu`, copied
byte-identical out of the Airlock container (both copies hash
`f23b753b...`), whose own header states the same pin, Swift 6.0.3.
Route three hands each spelling to `swift-frontend -typecheck`
inside the container: 17 of 17 accepted, and a control spelling no
authority admits is refused. Zero set differences and zero class
disagreements between the two enumerating routes.

Validation ran log_116's validator UNMODIFIED (symlinked into a
scratch directory with the new inventory under the name it expects).
Direction two: 0 holes, unchanged — but swift's zero is no longer
the tautology log 116 flagged, because the six spellings its
accepted probes use are now admitted independently of the corpus.
Direction one: swift's row moves from `core 0 / predicted 0` to
`core 16 / undecided 1 / never probed 11 / predicted 7,216` against
1,086 candidates today (6.64x); the five-language total at extracted
cores moves 145,082 -> 152,298, exactly swift's contribution.
Direction three is untouched (no probe was regenerated, so the 42
cells cannot move).

Two findings about the shared RULE rather than about swift, both
left for the owner: (1) `NUMERIC_MARKS` has no truth-value entry, so
swift's `Bool` lands in `undecided` exactly as rust's `bool` does —
the rule was not widened to flatter the number, and both figures are
given (16 -> 7,216; 17 -> 8,126); (2) the two-authority column reads
`not defined` for swift only because the validator tests for
witnesses named `grammar`/`compiler_table` — computed here in the
same shape, swift's two-route core is 16, so the column's number
would be 7,216.

Sizing note for the regeneration decision: log 120 recorded it as
"Swift excluded either way". Swift is no longer excluded.

Guards: `check_no_spelling_keys.py` PASS on
`swift_type_authority.json`, `type_inventory2.json` and
`type_inventory2_validation.json`, each producer refusing its own
output on failure. Zero regressions verified programmatically —
log_116's six artifacts (`type_inventory.json`, `.md`,
`type_inventory_validation.json`, `.md`, `type_inventory.py`,
`type_inventory_validate.py`) hash-identical before and after, and
the validation driver re-checks that itself. `probe_gen.py` was not
touched and nothing was regenerated.

New files (all in `Research/op_pipeline/`): `swift_type_authority.py`,
`swift_type_authority.json`, `swift_type_authority_typecheck.swift`,
`swift_stdlib_x86_64-unknown-linux-gnu.swiftinterface`,
`type_inventory2.json`, `type_inventory2.md`,
`type_inventory2_validate.py`, `type_inventory2_validation.json`,
`type_inventory2_validation.md`. `type_inventory2.json` SUPERSEDES
`type_inventory.json`, which is untouched on disk.

Recorded for the next reader: the brief cites "log 121 routes
(a)/(b)"; there is no log_121 in this line's DevComms, and none
anywhere under `<WORKSPACE_DIR>` or inside the container — checked on
both sides of the wall. The routes were taken from the brief's own
inline descriptions.

Full report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_125_task35_swift_authority.md`.

## 2026-09-01 — TASK 34: the interpreter table, the join and the union, rebuilt on the universal canonical form

the owner's ruling of 2026-09-01 ("THE UNIVERSAL CANONICAL FORM: virtual
memory for every unit, standardized loads, arrival annotated")
supersedes the register-based description as the primary statement.
The three views are rebuilt on it as new files; `dominant_table24.json`
is untouched and proved untouched against the version control system.

Nine of the eleven interpreter/JIT units on record (population:
cpython 1, java 2, ruby 4, php 4) now carry universal text —
standardized loads out of designated locations S0/S1, the unit's own
computation core, the arrival mode carried as an annotation beside the
text rather than inside it. Every one of the nine is z3-proved equal to
that same unit's own prior text before the new text is kept; all nine
gate verdicts are PROVED.

`php/add_function` canonicalises for the first time. Its old carve put
the confluence on the zval TYPE-TAG dispatch, whose result is in the
FLAGS, so the renderer refused. Under the ruling a read at a nonzero
displacement from a pointer arrival is the arrival's metadata, not the
value, so the tag dispatch is arrival machinery and the confluence is
`add (%rdx),%rax`.

The measurement the ruling predicted: four units across php and ruby,
carrying two different arrival annotations (typed-pointer(zval*) and
tagged-value(Fixnum, 2n+1 encoding)), now render CHARACTER-IDENTICAL
universal text. Under the register form the same four rendered as three
different texts. The classes are not merged — their declared type keys
differ and the result-type split stands — so the identity is recorded
as an observation.

`java/op_2` proved nothing last lap against 50 candidates (the prover
had no model for `cltd`); this lap it proves equal to `c/op_210` and
`cpp/op_210`, with 0 undecided out of 50. The cause is the uniform
prover route the universal form produces, not a new technique.

Two units still carry no text, and NEITHER is a register-scarcity
refusal: `ruby/vm_opt_plus` has no ship body at all in the dump, and
`ruby/rb_big_plus`'s lineages meet inside callees that are not
extracted units. The brief's premise that all three prior refusals were
scarcity/plumbing refusals does not match the artifacts.

Counts, with populations named: the join holds 23 rows (18
PROVED_EQUAL, 5 TYPE_INCOMPARABLE) against last lap's 22; the union
holds 2 components over 19 proved edges and indexes 1,654 units. The
authoritative compiled figure is converged 1,676 of 1,779 (compiled
five), withdrawn listed separately: 13 — 1,635 recomputed from the
status fields plus the 41 accepted proofs counted from
`canon32_sret_units.json` (5) and `canon33_units.json` (36). This lap's
nine proofs are interpreter units and are NOT in the 1,779 population,
so the compiled figure does not move again here.

Guards: `check_no_spelling_keys.py` in-line in every generator, plus
`interp_union_guard2.py` over all five artifacts with the
generator-provenance exemption deliberately bypassed. ALL PASS.

New files (all in `Research/op_pipeline/`): `interp_canon35.py`,
`interp_canon35.json`, `build_interp_table2.py`, `interp_table2.json`,
`build_interp_join2.py`, `interp_join2.json`, `build_union_table2.py`,
`union_table2.json`, `interp_union_guard2.py`,
`interp_zero_regression2.py`, `interp_zero_regression2.json`.
`interp_table2/join2/union_table2` SUPERSEDE the `1` artifacts, which
are untouched on disk.

Recorded for the next reader: the brief cites log 121; there is no
log_121 in this line's DevComms. The only file of that name anywhere
under `<WORKSPACE_DIR>` is `StressBot/RelevantProjects/PseudoCoup_v0/
DevComms/log_121_reactivity_model.md`, an unrelated repo and subject.
Checked on the host side of the container wall. Citations go to
log_116 / log_118 / log_119 instead.

Full report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_124_task34_interp_union_relaunch.md`.

## 2026-09-01 — TASK 36: the legality reduction, measured before any compiling

Report-only, nothing compiled. Read each language's own operand rules
out of its source and encoded them as data with file+line provenance
searched at run time: `legality_rules.json` holds 55 rules and 185
operator units (clang Sema's category checks at `llvmorg-21.1.8` via
`git show`; go/types' `binaryOpPredicates` / `unaryOpPredicates` /
comparison / shift; rust's code-generator match over operand kinds plus
its same-type assertion; swift's stdlib operator declarations plus a
computed protocol-conformance closure).

THE REDUCTION, over the full extracted scalar core (152,298 candidates,
type_inventory2.json): 152,298 -> 129,043 to compile, x1.18 overall, and
the effect is a go/rust/swift one — go x6.99, rust x2.48, swift x1.86,
c x1.11, cpp x1.12.

THE VALIDATION, over the corpus on disk (4,440 candidates, 1,779
accepted, 2,661 refused): 99.9% agreement inside rule scope (3,584 of
3,588), 4 misses, all one cause (c/cpp have no truth-value class, so
c++'s no-increment-of-bool rule cannot fire — F36-1, remedy named, not
applied). ZERO of the 1,779 accepted units would be dropped. As a
compile budget: 2,499 of 4,440 instead of 4,440.

The finding that moves log 116's F4: the operator-category rules explain
87.1% of c's refusals and 79.3% of cpp's, where a type pair alone
explained 0.0%; 72.9% of all 2,661 refusals against the type pair's
61.3%.

62 of 185 operator units have no rule in any authority read here (ranges,
`sizeof`/`_Alignof`, `<=>`, `??`, `try`, casts); they are PASSED THROUGH
to the compiler, not dropped — 136 corpus-accepted units live on them.
Rust has no on-disk operator authority (no `library/`, no `rust-src`;
checked on the host side of the container wall), so its spelling/operation
join is the one declared join of the five.

Guards PASS on all three artifacts, matching-shaped, no exemption; both
programs refuse their own output on failure. Zero regressions: the only
files modified anywhere in op_pipeline since this task's first commit are
this task's own new files.

Full report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_127_task36_legality_reduction.md`.

## 2026-09-01 — TASK 38: round 7 banked

Full-stack verification of round 7 (tasks 34-37). All nine round-7
grouping artifacts (interp_canon35/interp_table2/interp_join2/
union_table2/interp_zero_regression2/type_inventory2/
swift_type_authority/audit_altered_testimony/legality_validation)
PASS `check_no_spelling_keys.py`, pasted in
`DevComms/log_128_task38_bank_round7.md`.

Authoritative compiled-five count, reconciled per Addendum 2 (A
PROVED UNIT IS A COUNTED UNIT): converged 1,676 of 1,779 (compiled
five: c/cpp/go/rust/swift), withdrawn 13 kept as the one separate
population. Interpreter/JIT population (9 of 11 units universal-text
produced) is stated separately and is NOT a member of the 1,779.
`dominant_table24.json`, `dom_ops22.json`, `guards5.json`,
`exception_families3.json` verified byte-identical to their
pre-round-7 git blobs (sha256, independently re-checked against
`git show`, not just quoted from the artifact).

Round 7 in one line: universal canonical form measured (meet-in-the-
middle: php+ruby units producing character-identical texts under
differing arrival annotations); swift's 17-type authority landed
(three routes agreeing), superseding the tautological corpus-only
row; legality reduction measured 152,298 -> 129,043 candidates
(factor 1.18, 99.9% agreement, one miss family: c/cpp `bool` has no
truth-value class); testimony defect audited (168 altered captures
found, zero re-captured, both remediation routes costed for the owner).

Posterity message written to `DevComms/next_commit_message.txt`
(1,561 bytes) for the repo-daemon's next commit sweep to consume.

Full report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_128_task38_bank_round7.md`.

- 2026-09-02 (TASK 41, record hygiene, log_132): recounted the
  round-7 testimony-audit figure directly from
  `Research/op_pipeline/audit_altered_testimony.json` on disk. The
  correct figure is **158 distinct altered captures (go 101, rust
  48, swift 9)** — 101+48+9=158 — not the "168 (go 101, rust 58,
  swift 9)" figure that log_126 §3.2/§5, log_128 §4.4, this file's
  own round-7 entry above, and the daemon-committed posterity
  message (`a68e4a5`) all carry. Cause: the 168 count assumed every
  altered field is stored in exactly two places (op_pipeline copy +
  stage_asg copy); some of rust's altered rows share IDENTICAL
  stored text, so rust's true distinct-content count is 48, not 58.
  go and swift are unaffected. Dated correction notes appended to
  log_126 and log_128 (never editing the original text); Task 42 is
  asked to carry 158/rust-48 in round 8's posterity message. Also:
  named the five `__pycache__` files a claimed round-7 audit flagged
  as unlisted — no prior log states that specific list, so this task
  performed its own disk sweep instead (full accounting in
  log_132). Swept round-8's file window (today's mtimes,
  `op_pipeline` and `compiler_graph`): zero new files exist yet at
  sweep time (task 39/40 had not yet written output); round-7's own
  153 Sept-1 files are already accounted for across logs 105-128,
  spot-checked, nothing unlisted found.

Full report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_132_task41_record_hygiene.md`.

- 2026-09-02 (TASK 39, the universal-form migration, log_130):
  every compiled unit re-rendered into THE UNIVERSAL CANONICAL FORM
  — argument values originating at designated virtual-memory
  locations (S0 `-0x8(%rsp)` holds a, S1 `-0x10(%rsp)` holds b, S2
  `-0x18(%rsp)` holds the answer), standardized loads as the one
  arrival pattern, the unit's own core unchanged, the answer stored
  to its location AND left in its register, arrival annotated
  beside the text. **1,744 of 1,779 units carry an admitted
  universal text** (1,606 by z3 against their own prior canonical
  text, 138 forced by construction), and **1,537 of those prove
  DIRECTLY against their own ship code** with the arrival contract
  bound. All 1,744 assemble (`as` + `objdump`, 1744/1744, zero
  failures); 80 sampled units were EXECUTED through the designated
  locations against their prior texts over 10,400 argument pairs
  with zero differences. The five displaced-ABI rust units take a
  four-designation directory in their own ABI's arrival order —
  the case the register-first form could not state without a second
  dialect. Converged under the universal form: **1,655 of 1,779**
  (the standing count before this lap recomputes from disk to
  1,663, not the handoff's 1,676 — the difference is the 13 units
  canon31's branching audit withdrew; the record should be
  corrected). Eight units lose proved status, each named with its
  cause: six whose ANSWER IS THE ADDRESS of their own stack
  scratch, which no red-zone directory can hold, and two block-list
  units whose private region also had to be biased. Tables rebuilt
  on the universal text: `dominant_table25.json` / `dom_ops23.json`
  = **898 classes / 137 nodes / 26 families / 20 edgeless** against
  901/137/26/20; the only class change is three two-member classes
  that vanished because both their members are among the six, and
  the only family change is D0024 dropping those same six units.
  THE BRIEF'S EXPECTATION WAS TESTED AND REFUTED: the universal
  form does not merge cross-language classes, it REFINES — zero
  merges, 77 prior texts split, distinct texts 527 -> 606 — because
  go's ABI differences were already normalized by the entry
  contract long before this lap, and what the form adds is the
  arrival and answer plumbing as explicit text carrying information
  the core was hiding. Join re-run (`interp_join3.json`) is
  IDENTICAL to interp_join2: 23 rows, 18 PROVED_EQUAL, 5
  TYPE_INCOMPARABLE. Union rebuilt (`union_table3.json`): 2
  components, 19 proved edges, three views preserved.
  `dominant_table24.json` and the round-7 interpreter artifacts are
  byte-identical and unmodified in the VCS. All new artifacts pass
  the spelling-key check; the matching-shaped ones pass IN FULL
  with no exemption claimed, and the nine provenance files were
  re-checked with their role declaration stripped and passed
  without any exemption at all.

Full report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_130_task39_universal_migration.md`.

- 2026-09-02 (TASK 40, the regeneration trickle, log_131): **the probe
  residue is compiled — all of it.** 129,553 candidates submitted,
  29,288 accepted, 100,265 refused, and every accepted probe fully
  extracted (29,288 ship units, 29,288 anchor units, 29,288 DWARF
  parameter tables, no gaps), in 326 checkpointed chunks of 400,
  0 pending. Wall clock 18.4 minutes at 6 of 12 cores.
  Two supplement fixes landed first and moved the counts: F35-1 —
  `core_rule2.py` replaces the v1 NUMERIC_MARKS tuple (which had no
  truth-value entry) with a normalised-class test, so rust's `bool`
  (14→15) and swift's `Bool` (16→17) enter their cores, taking naive
  152,298→153,857 and the residue 129,043→**129,553**; rust's class
  comes from rustc's own type-kind match parsed at a named pin, not a
  hand row, so `char` and `str` stay out. F36-1 — `legality_quirks.json`
  annotates c++'s truth-value increment/decrement as
  `deprecated_but_allowed` (additive; `legality_rules.json` untouched),
  taking in-scope agreement 99.9%→**100.0%**, 4 misses → 4 agreements.
  The 121,081-vs-129,043 discrepancy is resolved: 121,081 is the
  rule-ADMITTED subset; 129,043 (now 129,553) adds the 7,962 candidates
  of the 62 operator units with no extracted rule, and log 127 measured
  that 136 corpus-accepted units live on exactly those units — so the
  admitted subset is not the regeneration population.
  Infrastructure: a CPU-capped copy of the Airlock runner named
  `trickle-runner` on `trickle-internal` (sharing no name with Airlock
  or SandboxDesign, both of which use `sandbox-*`), capped at half the
  cores, sharing the image and mounting `sandbox-persist` READ-ONLY, no
  proxy, driven by `podman exec` because the machine's inotify instance
  limit (128) is exhausted and raising a kernel limit was not made.
  Airlock's own `sandbox-runner` was up throughout and untouched.
  All five toolchain pins were verified IN-LANE before capture and are
  identical to the 2026-08-25 originals (clang 21.1.8, go1.26.0, rustc
  1.96.1, Swift 6.0.3, objdump 2.46) — the addendum's one named risk,
  dismissed on the lanes' own testimony.
  Testimony remediation: the addendum's "Route A is subsumed" does NOT
  hold. Joined against the finished regeneration, ZERO altered records
  were superseded, because every altered record is a refusal of an
  operand shape the extracted rules call illegal — exactly what the
  filter keeps away from a compiler (F40-1). A 234.5-second unfiltered
  re-capture of the three original plain lanes fixed it: **218 altered
  records (109 distinct captures, in two stores each) are superseded**,
  and the recaptured text matches log 126's reconstruction character
  for character. Supersession is a MARK in a new sidecar; no store was
  opened for writing. 118 findings remain out of scope — all the
  assignment run's (go 33, rust 26 distinct), a different generator.
  Other findings: 24 of c's and cpp's 56 core spellings are clang
  fixed-point types (`_Fract` / `_Accum`) the default dialect refuses,
  which is honest testimony but a real question for the owner (F40-2); the
  residue is 77% refusals against the corpus's 60% (F40-3);
  `lane_verbatim` is not thread-safe and now runs under a lock (F40-5).
  Zero regressions verified against the version-control system: every
  file read last changed before today; new files only.

Full report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_131_task40_regeneration_trickle.md`.

## 2026-09-02 — Task 42, bank round 8

Full-stack verification of round 8's grouping artifacts against the
spelling ban: `check_no_spelling_keys.py` PASSes directly re-run on
`dominant_table25.json`, `dom_ops23.json`, `supersession_altered_testimony.json`,
and a 3-file spot-check sample across all 8 chunk-store families under
`trickle_store/` (334 chunk files total, matching task 40's inventory;
each sampled file's own `generated_by: trickle.py` field stands as its
per-chunk guard record, per the brief's exception for the 334-file
set). `dominant_table24.json` and its round-7 siblings verified
untouched: `git status --porcelain` empty, md5 stable, last commit
2026-08-31 (predates this round).

Count line, both figures, correction explicit: the register-form
standing figure corrects **1,676 → 1,663** (the round-7 handoff never
subtracted the 13 `withdrawn` units). Converged under the UNIVERSAL
form (task 39): **1,655 of 1,779** (1,744 admitted a universal text;
1,663 − 8 named losses = 1,655; 8 units lose proved status — 6
address-answer units c/op_31, c/op_32, c/op_34, cpp/op_43, cpp/op_44,
cpp/op_46, and 2 biased-private-region block-list units cpp/op_765,
cpp/op_770). Classes: 901 → 898 (refines, not merges — 3 lost, all
accounted for). Populations kept separate throughout, never flattened.

Regeneration (task 40): 129,553 probes compiled, 29,288 accepted and
fully extracted — **compiled and extracted but not yet ingested into
the matching/dominance pipeline; that ingestion is next round's
headline work.** Testimony remediation folded in per the owner's ruling:
218 altered record findings = 109 distinct plain-run captures,
superseded; 118 assignment-run findings remain out of scope, carried
forward.

Corrections banked into posterity text: 158 (not 168; rust 48, not
58) and 1,663 (not 1,676, register form). the owner's open calls restated:
answer-store asymmetry; the 6 address-answer units' directory base;
the converged figure of record (1,655 universal vs 1,663 register —
keep distinct); F40-2 fixed-point dialect question; the 118
assignment-run findings.

Posterity message rewritten at
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/next_commit_message.txt` (3,449
bytes) carrying both corrections and the regeneration headline; the
repo-daemon consumes it automatically on its next 30s commit-push
cycle, no separate action needed.

Full report:
`<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_133_task42_bank_round8.md`.
