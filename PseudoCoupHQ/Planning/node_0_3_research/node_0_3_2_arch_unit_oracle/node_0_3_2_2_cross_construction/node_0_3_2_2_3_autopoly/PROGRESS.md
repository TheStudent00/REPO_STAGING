---
id: hq.research.arch_unit_oracle.cross_construction.autopoly.progress
status: living
---

# PROGRESS — autopoly

- 2026-09-10: task bank1 closed — THE POLYFILL LIBRARY AS BANKED
  CERTIFICATES, AND THE LOOP RESHAPED TO DELTA PLUS AUDIT. A CERTIFICATE
  is a record about ONE ARTIFACT: one (cell, target, written place) with
  the term text it was posed on, the rendered source and its sha256, the
  compiler and its flags LITERAL, the carved body's bytes and text, and
  the gate's verdict in z3's own words with the region sentence where one
  applied. `bank.py` read every run of every pass on disk — `ap1`..`ap5`,
  task ap3's normalise-off ablation, task ex1's cpp pass, task ex1's
  interpreted handful, task ex2's interpreted loop, and this task's own
  delta pass — and wrote 12,593 certificates over 4,117 distinct keys onto
  `certificates.jsonl`, the strongest of each key marked `preferred` (ties
  by the earliest pass) and every weaker or later entry kept beside it and
  marked `superseded_by`. PER KIND, preferred in brackets: `proved` 5,806
  (1,227), `proved_under_caller_extension` 677 (122), `agreed` 1,385
  (1,322), `sat` 483 (91), `undecided` 583 (72), `refused` 3,659 (1,283).
  THE HEADLINE IN THREE READINGS, stated as three from now on — STRICT
  (every written place proved), DESTINATION-ONLY (every place of the
  destination register proved, the flags not read; the reading tasks ap1
  to ap5 published) and CORPUS-NEEDED (the destination proved AND the
  flags proved wherever the corpus's flag-pair attestation records a
  consumer of a cell of this `mnem`'s flags): over the bank, 1,999 /
  2,241 / 2,203 proved (cell, target) pairs, and at the cell width all
  four 93 / 144 / 134 cells (60,534 / 84,633 / 73,425 attested ledger
  rows, 45.5% / 63.61% / 55.19%), all five 92 / 140 / 132, all twelve 87 /
  135 / 127. The five passes' own STRICT figures reproduce the
  coordinator's object for object — 330 / 434 / 465 / 521 / 504, union
  523 — and the 19 pairs proved by some pass and not by the last are
  restored, every one an `imm_gpr` cell (`and` 8; `cmp` 8 and 16; `mov` 8
  and 16; `or` 8; `sbb` 8) on c, rust or swift, all 19 preferred from
  `ap1`. The passes' own published count is reconciled rather than left as
  a discrepancy: they counted `proved` OR `proved_under_caller_extension`,
  which recomputes to ap5's 165 cells on all four exactly. THE TEN
  WITHIN-PASS BACKUP STORES were deliberately not banked and each was read
  anyway: none holds a certified key the bank lacks. THE LOOP, RESHAPED:
  `autopoly.py --bank` attempts (a) every (cell, target, written place)
  with no certificate of kind `proved`/`agreed` and (b) a 5% audit sample
  of the certified, chosen by `random.Random("2026-09-10")` and re-derived
  from the term; an audited triple whose verdict differs on IDENTICAL
  inputs is an ALARM that stops the pass. One pass on the five compiled
  targets: certified before 1,225 / attempted 954 / newly certified 2 /
  audited 58 / alarms 0, over 707 runs. A FULL pass over the same five was
  run in the same instance and the same hour for the comparison: 1,265
  runs, so the delta ran 55.9% of the runs and cost 81.9% of the seconds —
  the saving is in RUNS, not proportionally in seconds, because the runs
  the delta drops are the fast already-proved ones. The audit's 58: 51
  reproduced identically, 7 came back on a DIFFERENT artifact (six
  `imm_*`, the certificate's source saying `3` where the re-derivation's
  says `v0` — task ap5's symbolic immediate, the same mechanism as the 19;
  the seventh, `or` gpr_gpr 64 on c at `flags.high`, was proved by ap2
  through the primitive route which the current driver refuses outright,
  so it is a proof the machinery can no longer reach and the certificate
  keeps it). Task ap1's driver was copied unchanged to `autopoly1.py` and
  every unflagged command of `autopoly.py` delegates to it, so log 243's
  seven reproducing commands and `lanes_ap1/ap1_l5_run.sh` still answer.
  No shared file changed. Report:
  `PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/bank1.md`.
  Log: `PseudoCoupHQ/DevComms/log_253_task_bank1_the_bank.md`.
  Status: closed, guard PASS on both json and both jsonl products,
  verifier 20 claims / 0 DIFFERS, instance `bank1` down.

- 2026-09-10: task ex2 closed — THE INTERPRETED LOOP: task ex1's check
  (the cell's mapping rendered as source in the target's own operators,
  compared against the reference's own term over a stated sample) run
  over the whole 253-cell outer set instead of the handful's ten, on all
  seven of task ex1's interpreted targets. 1,771 of 1,771 runs recorded:
  ZERO disagreements, ZERO timeouts. cpython, ruby and javascript render
  193 of 253 cells (120,433 ledger rows, 90.52%); php, java, dart and
  csharp render 184 (116,057 rows, 87.23%) — every rendered cell's whole
  sample agrees, on every target, with no exception. Beside the compiled
  side at neither width redefining the other: all four is 165 cells /
  106,773 rows / 80.25%, all five is 163 / 105,877 / 79.58% (a LOWER
  BOUND — cpp's own store predates task ap5's imm_symbolic gain and was
  not re-run, out of this task's scope; flagged for the owner); all seven
  interpreted is 184 / 116,057 / 87.23%; all twelve (the five compiled
  proved AND the seven agreeing) is 158 / 100,023 / 75.18%. TWO DEFECTS
  OF THIS TASK'S OWN were found by its own runs and fixed in the ONE file
  the brief authorises — `interp/interp_check.py`, the interpreted route,
  nothing else touched: a destination place name carrying a dot
  (`flags.low`, a halved place) or a hyphen (`stack_-8`, `push`'s own
  write) was never sanitised before becoming a rendered FUNCTION NAME,
  which every target refuses to parse — six refuse cleanly, and csharp's
  REUSED project folder silently ran a STALE dll from an earlier
  successful build instead, producing what looked like eleven then one
  genuine disagreement. Both fixed (the same sanitisation
  `handful.one_place`, the compiled route, already applies to the dot,
  extended to the hyphen); every apparent disagreement traced to one of
  the two and re-run to zero before any deliverable was written. The
  handful's ten cells reproduce inside this loop, 63 of 63 compared
  (`sub` imm_gpr 64 is not in this outer set, as tasks ap4 and ex1 both
  already found). Declines (division by zero, the NaN region of `addss`)
  and refusals (the x87 register, vector-lane gaps, six nullary cells
  whose zero-arrival sample point every dialect's own blank-line
  convention skips) are counted by cause, never scored, never worked
  around. Report:
  `PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/expand2.md`.
  Log:
  `PseudoCoupHQ/DevComms/log_250_task_ex2_the_interpreted_loop.md`.
  Status: closed, guard PASS on both json products, verifier zero DIFFERS,
  instance `ex2` down.

- 2026-09-09: task ap5 closed with a STOP — the two mechanical remainders
  of the four languages, each closed IN THE LAYER THAT OWNS IT, and
  AutoPoly's loop, fifth pass. (1) THE x87 STACK, READ END TO END:
  `reference.answer_of` now reads an answer home spelled `X87_<k>` off the
  reference's own `MachineState.x87`, `pool100_entry_equivalence.align_by_row`
  now aligns an x87 arrival by its IN row at `reference.X87_SORT`, and task
  ap4's driver-side stand-in `emulate.x87_answer_for_unit` is REMOVED. The
  branch must test BOTH spellings the pipeline already names in
  `emulate.X87_ARRIVAL` — `X87_<k>`, a preseeded stack position, and
  `x87_<operand>`, a memory operand read at the x87 sort — and the first
  draft tested one, which the loop's own change table caught as 30
  regressions; the branch was widened and the whole 1,012 re-run, the first
  pass's store kept beside the second. THE x87 POPULATION DID NOT MOVE, and
  that is the point: 36 x87 places PROVED on c, 0 disproved, 0 sat, 0
  undecided, rust/go/swift refused by nature (41 places each), and the
  standing cause "answer home or arrival on the x87 stack" still carries 114
  runs, exactly task ap4's count. No `sat` and no counterexample on any x87
  place, so the 80-bit explicit-integer-bit finding the brief asked to be
  stated if it appeared does NOT appear. (2) THE IMMEDIATE AS AN INPUT OF THE
  MAPPING: `model_translate.shapes_for` spells each `imm_*` shape a second
  time with a register of the operand's own width in the immediate's slot,
  marked `imm_symbolic`; the driver takes that immediate as one more
  parameter and does not ask the primitive route, whose key carries no
  immediate. 20 symbolic rows added, 0 existing rows changed, and the CELL
  COUNT DID NOT RISE — 253 before and after, 133,044 ledger rows both. Six
  runs task ap4 answered `sat` are proved (`mov` imm_gpr 32/8 on c, `xor`
  imm_gpr 8 on c/rust/swift, `xor` imm_gpr 32 on go), every one a primitive
  match against a corpus body with a foreign baked-in immediate. THE ALL-FOUR
  LINE: 165 cells, 106,773 attested ledger rows, 80.25%, up from ap4's 162 /
  106,032 / 79.7% (ap3 151, ap2 144, ap1 120). Runs carrying a cause 232 of
  1,012, down from 237. THE FOUR GUARDS PASS: `model_translate check` 259 /
  172 STATED / 87 REFUSED, task o8's totals 243 / 197 / 155 / 216, the h2
  handful 24 of 24, and task t100's proved edges 12 of 12 with the new branch
  measured UNREACHABLE for the whole pool (no x87 family on any edge) and the
  aligner's substitution identical edge for edge. THE STOP: runs task ap4
  proved that task ap5 does not is ONE, not zero — `sbb` imm_gpr 8 on swift,
  whose four-parameter symbolic rendering compiled its `@_cdecl` entry to a
  five-byte tail-call thunk (`e9 00 00 00 00`, `R_X86_64_PLT32` to the
  mangled swift symbol), so the carve holds a `jmp` and the reference says the
  unit record carries no body. The brief's rule is "zero regressions or STOP",
  so no sixth pass was run and the cell is reported, not patched; whether the
  symbolic row should be preferred where the target's compiler answers with a
  thunk is left for the owner. Report:
  `PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly5.md`.
  Log:
  `PseudoCoupHQ/DevComms/log_249_task_ap5_autopoly_fifth_pass.md`.
  Status: closed with one regression standing, spelling guard PASS on all
  three json products, conventions verifier 0 DIFFERS over three passes,
  instance `ap5` down.

- 2026-09-09: task ex1 closed — BEYOND THE FOUR, each expansion on the
  handful first, per the owner's standing rule. TWO EXPANSIONS. (1) cpp as a
  FIFTH COMPILED TARGET: `cpp/cpp_render.py`'s `CppRenderer` is c's
  renderer with the two things measured to differ and nothing else —
  the `extern "C"` linkage (without it the symbol is mangled and the
  carve cannot ask objdump for it) and the `<cstdint>` / `<cstring>`
  header names — on the evidence that 305 of the 309 c sources task
  ap4's loop rendered compile under clang++ at the corpus's own cpp
  ship flags VERBATIM, the four that do not being c primitive rows
  (`bool` increment) and not term-route text. cpp's `long double`
  carves to the same x87 body task ap3 measured for c's, so cpp joins
  `TARGETS_WITH_AN_80_BIT_HOLDER`. The loop's 253 cells ran on cpp
  alone (253 runs, 63 s): 245 rendered, 245 compiled, 202 proved plus
  23 under the caller extension, 8 refused — the same eight as c. THE
  ALL-FIVE LINE IS THE ALL-FOUR LINE: 162 cells, 106,032 attested
  ledger rows, 79.7% on both widths, and the list of cells proved on
  all four and NOT on cpp is empty; both widths are reported until the owner
  says which counts. cpp's own proved set is 225 cells, 63 of them
  outside the all-four set (the x87 arithmetic among them), which is a
  reading about how much of the four-way intersection rust, go and
  swift are setting. (2) THE INTERPRETED CHECK, defined and stated
  LITERAL before it ran: there is no carve for an interpreted target,
  so the emulation is SOURCE in that language over that language's own
  value model (one measured prelude per language in
  `interp/dialects.py`) and the check is the fuzz census's method — the
  reference's own term evaluated at each point of a stated sample
  against what the runner prints, one process for the whole sample,
  declines never scored. Seven targets (cpython, php, ruby, java,
  javascript, dart, csharp — every runner named by the brief is in the
  image or the persist volume), ten cells each, 70 runs, ALL 70
  RENDERED: 39,062 sample points per target, zero disagreements on any
  target, 819 or 820 declines each with the target's own word for it
  (division by zero on six spellings; the NaN region where
  `fp.to_ieee_bv` is underspecified; php's and c#'s refusal of
  MIN / −1). An agreement is evidence, not a proof, and no interpreted
  run carries a gate verdict. FIVE DEFECTS OF THIS TASK'S OWN were
  found by its own runs and each fixed in the layer that owns it, with
  the run that caught it quoted; the fifth is the one worth reading —
  the interpreted route was SKIPPING task h2's `projected_lane`, which
  the compiled route runs, and that is why the two float cells refused
  on all seven while proving on cpp. ONE THING FLAGGED: the brief's
  "ALSO carve and gate the JIT output" has no object — `jit_out_*`
  holds three different JIT dump formats, none of them objdump's, and
  the corpus holds zero arch-units for javascript, dart and csharp.
  Report:
  `PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/expand1.md`.
  Log:
  `PseudoCoupHQ/DevComms/log_248_task_ex1_cpp_and_the_interpreted_check.md`.
  Status: closed, guard PASS on all three json products, verifier zero
  DIFFERS, instance `ex1` down.
- 2026-09-06: node folder generated by
  `PlanPlan/framework/generate_nodes.py` from the
  `nodes` register of `PseudoCoupHQ/Planning/node_0_3_research/node_0_3_2_arch_unit_oracle/node_0_3_2_2_cross_construction/CORE_0_3_2_2_cross_construction.md`. Skeleton only — definition,
  designation, and content pending.
- 2026-09-07: task o13 closed ("what is next, in order" item 1 —
  render the mode). The guard read off the ledger's GUARD-block rows
  is now rendered into the emulation before the operation, per guard
  kind (`test je on IN IN` / `cmp je on CONST IN` / `cmp jne on CONST
  IN` / `cmp jl on IN IN`, each with the outcome — trap or a call that
  does not return — read off the x unit's own departing path). Re-run
  of the 95 emulations task o7 (log 218) and task o11 (log 226)
  recorded DISPROVED: 27/36 c and 42/59 rust now PROVED_ON_SHIP at the
  gate's 3,000 ms (kept as the verdict of record); a 30,000 ms re-run
  moves 3 more (2 c, 1 rust); 5 emulations (4 c, 1 rust) still
  disagree with a mode rendered, diagnosed by cause (both sides' guard
  fires correctly; the guarded BODY still differs); 85 of 95 carry no
  ledger guard row at all and are unaffected by this task. Report:
  `PseudoCoupHQ/Research/oracle/cross_construction/emulation/mode/mode_report.md`.
  Log: `PseudoCoupHQ/DevComms/log_231_task_o13_mode_rendered_guard.md`.
  Status: closed, verifier zero DIFFERS, instance `o13` down.
- 2026-09-07: task o12 closed ("what is next, in order" item 2 — the
  synthesis route). Compose y's arch-units directly from a
  counterexample-guided search (CEGIS, k = 1, 2, 3) over c-bearing pool
  entries in the target's machine-type-key bucket, no compiler in the
  loop. All 206 targets of task o7's population P3 run inside the
  brief's 4-hour budget (actual: 466 s): 4 PROVED (`E01614`, `E01617`
  at depth 3; `E01654`, `E01664` at depth 1), 135 `NONE_AT_DEPTH_3` (78
  from buckets with zero c-bearing components at all), 16 `UNDECIDED`
  at the round limit, 51 excluded as `term_to_lean.py` parser
  refusals. The oracle against task o7's compiled-emulation route: of
  155 targets both routes answered, both proved the same 4, and on
  every one the compiler route's own emulation term lands in a
  DIFFERENT pool entry than every component this route's composition
  used. The compute was already complete when this closing session
  began (an earlier session's usage limit cut it off before the
  report); this session confirmed the full run post-dates the
  sort-filter correction (commit `b7abda67`, 00:14:35 -0400, which
  made the machine-type-key bucket itself the sort filter, holder
  class/width no longer excluding admissible wires) rather than
  re-running, then wrote the report and this entry. Report:
  `PseudoCoupHQ/Research/oracle/cross_construction/emulation/synthesis/synthesis_report.md`.
  Log: `PseudoCoupHQ/DevComms/log_230_task_o12_synthesis_route.md`.
  Status: closed, verifier zero DIFFERS (10 MATCHES, 11 UNVERIFIABLE, 3
  NOT_RERUNNABLE), instance `o12` down.
- 2026-09-09: task h1 closed — a handful of `find_emulation` runs from
  the arch-opcode model table, run on the TOWER. Ten cells of
  `PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json`
  (`add` gpr_gpr 32, `sub` imm_gpr 64, `imul` gpr_gpr 32, `sar` cl_gpr
  32, `shr` cl_gpr 64, `idiv` gpr_one 32, `cmovne` gpr_gpr 32, `setne`
  gpr_one 8, `addss` xmm_xmm 32, `cvtsi2sd` gpr_xmm 64), all present at
  exactly that key, each run against c and rust — twenty runs, every
  intermediate object on the record. Unlike task o8, a cell has no unit
  behind it, so the gate's other side is the CELL'S OWN TERM. Result:
  16 of 20 runs reached a compiled body; 24 places compiled and carved;
  landing 6 LANDED / 6 LANDED_ELSEWHERE (all `lea` for a two-register
  sum and a subtract-a-constant, the same substitution logs 220 and 226
  found) / 12 NOT_COLLAPSED; gate 18 PROVED_ON_SHIP at 3,000 ms plus 2
  more under the caller-extension re-pose, and 4 UNDECIDED — `idiv`'s
  two places in each target, still UNDECIDED when re-posed at 300,000
  ms. The 4 runs that never compiled are the two float cells in both
  targets, refused by the existing renderers' own cause
  (`emulate.CAUSE_LANE`): the table's term for a vector place keeps the
  whole 128-bit register and neither renderer has a holder for a vector
  arrival read above bit 63. Unasked-for finding: clang at `-O1` and
  rustc at `opt-level=1` emitted byte-identical bodies in all 12 places
  both compiled. Report:
  `PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.md`.
  Log:
  `PseudoCoupHQ/DevComms/log_238_task_h1_handful_of_find_emulation_runs.md`.
  Status: closed, instance `h1` down.
- 2026-09-09: task h1b closed — the composition column, closing task
  h1's brief §5 (added after h1 ran). For every one of the twenty
  runs, `composition` (a new field on `handful.json`, nothing else
  changed) walks the RAW carved body of the run's own destination
  place instruction by instruction and classifies each one by task
  m1b's own classifier (`model_table.classify_line` /
  `.SHAPE_OF_CLASSES` / `.key_width`, imported, not re-implemented)
  against the model table's 6,218 distinct TRANSLATED (`mnem`, shape,
  `key_width`) triples; `ret` and calling-convention moves are marked
  as chaff (task o2's own narrow rule) rather than reported as
  unmapped. Sixteen runs have a compiled destination place, 198 raw
  instructions between them: 120 table cells, 76 chaff, 2 map to no
  table cell (`cqto`, both `idiv` targets — no operand, so the
  classifier has no width to read). Every one of the six LANDED runs'
  composition is exactly one cell, the run's own target, checked
  rather than asserted. `handful.md`'s twenty-row table gained the
  `composition` column. Report:
  `PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful.md`.
  Log:
  `PseudoCoupHQ/DevComms/log_239_task_h1b_composition_column.md`.
  Status: closed, instance `h1b` down.
- 2026-09-09: task h2 closed — the same ten cells and two targets task
  h1 ran, re-run after two printing fixes in the DRIVER (neither
  renderer touched) plus one additive width rule in the shared
  `model_table.classify_line`. FIX 2, the one that moved the answer: a
  vector cell's place is the whole 128-bit register, so the driver
  projects `Extract(key_width - 1, 0, place)`, renders that lane, and
  puts the bits above it to the gate against the same bits of the
  arrival — proved pass-through in all four cases. The four runs task h1
  refused (`addss`, `cvtsi2sd`, in c and rust) now render, LAND on their
  own arch opcode and are PROVED_ON_SHIP; 20 of 20 runs reach a compiled
  body, LANDED 6 → 10, proved 18 → 22. FIX 1, the cell's term put
  through the pipeline's own normaliser before the renderer sees it, is
  a NO-OP on this population, measured: all 24 rendered places produce a
  source character for character identical both ways and identical to
  the file h1 wrote, so `idiv` is still 76 instructions (51 stripped)
  and still UNDECIDED at 3,000 ms and at 300,000 ms — the 32-copy sign
  extension is in the table's own term, which belongs to m1/m1b. THE
  ZERO-OPERAND RULE (`cqto`, `cltq`, `cltd`, `cwtd`, `cqo` take their
  width from `reference.SPREAD_SIGN` / `ACCUMULATOR_WIDEN`) moves
  exactly 2 of task h1b's own 198 composition records, both `cqto`, and
  nothing else. Regression: task o8's per-opcode check re-run unchanged
  over its 243 rows into a scratch copy returns 243 / 197 / 155 / 216,
  the proof that the renderers were not changed. Reports:
  `PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful2.md`.
  Log:
  `PseudoCoupHQ/DevComms/log_240_task_h2_two_printing_fixes.md`.
  Status: closed, instance `h2` down.
- 2026-09-09: task g1 closed by task g1b — the same ten cells tasks h1
  and h2 ran, now on FOUR targets (c, rust, go, swift) and by a route
  tried BEFORE the term route. THE PRIMITIVE ROUTE asks whether the
  target has an operator whose whole lowered body IS the cell: task o2's
  own single-opcode rows for that language, each stripped again by task
  o2's narrow rule and its one instruction classified by task m1b's own
  classifier to a (`mnem`, shape, `key_width`) triple, matched against
  the cell's. 8 of the 40 pairs have one; 32 do not and took the term
  route. Where it ran, what is compiled is the chosen member's OWN probe
  source — `a + b`, `a * b`, `a >> b` — and four cells moved from term to
  primitive in c and rust (`imul`, `sar`, `shr`) with NOT ONE verdict
  changing. Of 40 runs: 37 places compiled and were carved, 12 LANDED,
  7 LANDED_ELSEWHERE, 18 NOT_COLLAPSED, 29 PROVED_ON_SHIP, 2 more under
  caller extension, 6 neither. TWO NEW RENDERERS: `go/go_render.py`,
  whose 26 spellings were every one measured by `go/go_facts.py` first,
  and `swift/swift_render.py`, whose 17 are all UNMEASURED. SWIFT DID
  NOT RUN: `/persist` is an empty directory inside the `g1` instance, so
  `/persist/swift/usr/bin/swiftc` does not exist and all 13 swift places
  that reached the compile step were refused there with that literal
  answer; no workaround was attempted. `idiv` did NOT reach the
  primitive route in any of the four, because division everywhere lowers
  to the accumulator setup plus the divide (`cltd; idiv`), which is two
  instructions under the narrow rule — so it went by the term route, 51
  instructions after the strip in c and rust and 85 in go, UNDECIDED at
  3,000 ms and again at 300,000 ms on all six of its places. Report:
  `PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3.md`.
  Log:
  `PseudoCoupHQ/DevComms/log_241_task_g1_find_emulation_go_and_swift.md`
  (9 MATCHES, 0 DIFFERS, 0 REFUSED, 0 NOT_RERUNNABLE). Status: closed;
  the instance stays up for task g1b, which re-runs swift on the rebuilt
  image and widens the lookup.
- 2026-09-09: task g1b closed — task g1's closer, in two pieces. SWIFT
  RUNS AT LAST, and the obstacle was two obstacles: the coordinator's
  rebuilt image carries `libncurses6`, which the swift driver loads, AND
  `g1.conf` named no persist volume, so Airlock's own default gave the
  container an EMPTY `g1-persist` over `/persist` — while the swift
  toolchain lives at `/persist/swift` on `sandbox-persist`. `g1.conf`
  now mounts that volume read-only, as `t101b.conf` and `t103.conf`
  already do for the same toolchain; the container was re-created;
  `swiftc --version` answers `Swift version 6.0.3
  (swift-6.0.3-RELEASE)`. THE SECOND RUN OF RECORD (`handful3b.json` /
  `.md`) re-ran all forty pairs, not the ten swift ones, so the 40-row
  table comes from one run and the thirty non-swift rows are a check:
  every one returns exactly what task g1 got for it, and the ten swift
  rows are the ten that moved. 40 of 40 runs reach a compiled body (was
  30); 50 places carved (was 37); LANDED 12 → 17; PROVED_ON_SHIP 29 →
  39, plus 3 under caller extension (was 2). Eight of swift's ten cells
  are proved for every input, a ninth once its narrow holder is
  zero-extended, and the tenth is the divide. THE LOOKUP WIDENED BY ONE
  STEP (section 2e of `handful.py`): a single-opcode row is accepted for
  a cell when its NARROW-stripped body is the cell's own instruction
  plus zero or more ZERO-OPERAND setup instructions from
  `reference.SPREAD_SIGN` / `ACCUMULATOR_WIDEN` and nothing else; the
  route is then `primitive+setup`. It changes ONE of the forty pairs,
  the divide in c, and not three: rust, go and swift hold ZERO
  single-opcode rows carrying the divide instruction at all, because
  their divide bodies carry the GUARD (rust's shortest is 17
  instructions ending in two `core::panicking` calls; go's branches into
  `runtime.panicdivide`; swift's carries two `ud2`), where c's is four
  instructions and no guard. **The primitive route reaches an operator
  exactly when the target leaves the edge region undefined** — the owner's
  primitive-plus-edge-regions model, measured. On c the emulation drops
  from 76 instructions to 5 (the cell's own opcode plus `cltd`), and the
  gate still cannot answer — but for a new reason, and this is the flag:
  the emulation reads TWO inputs where the cell reads THREE, the third
  being the one `cltd` derives, so the IN-row alignment declines rather
  than the solver timing out. No `sat`, so no counterexample and no
  region. One defect was found and fixed on the way: `one_recheck`
  rebuilt the term-route parameter plan (which IS the arrival contract)
  even for a primitive-route place, aligning the wrong rows and
  returning a DISPROVED about a comparison nobody posed; measured per
  place, the fix moves 0 of `handful3b.json`'s 8 re-posed places and
  both of `handful3c.json`'s. Reports:
  `PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful/handful3b.md`
  and `.../handful3c.md`. Log:
  `PseudoCoupHQ/DevComms/log_242_task_g1b_swift_and_the_widened_lookup.md`
  (26 claims: 13 MATCHES, 0 DIFFERS, 9 UNVERIFIABLE, 1 REFUSED, 3
  NOT_RERUNNABLE, each non-matching outcome named with its cause in its
  section 11). Status: closed, instance `g1` down.
- 2026-09-09: task ap4 closed — CLOSING THE FOUR LANGUAGES: the contract
  for a value that is not in a register, and AutoPoly's loop, FOURTH
  PASS. the owner's ruling of 2026-09-09 — "the contract may state a place by a
  CONSTRAINT, not only by a register name; one extension, in the layer
  that owns each half" — carried out as three changes. CHANGE 1, in the
  DRIVER: where the cell reads a different NUMBER of arrivals from the
  emulation the two sides are no longer aligned row by row; the cell's
  arrivals are SUBSTITUTED by what the reference simulator leaves in them
  when it steps the emulation's own attested body up to the cell's
  instruction, and the REGION that names is recorded as a sentence and
  printed only where z3 proved it. CHANGE 2, in the LEDGER
  (`build_epilogue`: `fstpt OUT-0`; `build_prelude`: `fldt IN-k`) and in
  the driver: an answer left on the x87 register stack is now an answer,
  and because `reference.answer_of` cannot read one and
  `pool100_entry_equivalence.align_by_row` cannot align an FP arrival —
  neither file named by the brief — both readings are done in the driver
  over the reference's own state. CHANGE 3, in the DRIVER: an emulation
  whose carved body carries no instruction is the IDENTITY on its
  arrival, `composition = []`, landing `IDENTITY`. THE ANSWER: 162 of 253
  cells proved on ALL FOUR targets, 106,032 attested ledger rows, 79.7%
  (ap1 120 / 57.6% → ap2 144 / 64.17% → ap3 151 / 64.29% → ap4 162 /
  79.7%); cells proved on NO target 56 → 20; runs carrying a cause 293 →
  237 of 1,012; runs task ap3 proved that this loop does not: 0. THE
  ARRIVAL-CONTRACT GROUP, 38 places open since task g1b, is 0 — and the
  probes found it was TWO populations, 7 derived arrivals and 31 halves
  of a flags place on the primitive route, which the driver's own rule
  already refused when the place was not halved. The three guards the
  brief names all hold: `check_L2` 259 / 172 STATED / 87 REFUSED with all
  178 files restored byte for byte, task o8's 243 / 197 / 155 / 216, and
  the h2 handful 24 of 24. Six pairs moved to `sat`, each with its
  counterexample, and the largest finding among them is that the cell key
  carries no immediate, so `mov` imm_gpr is not one mapping — the single
  awaiting-the owner item. Report:
  `PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly4.md`.
  Log:
  `PseudoCoupHQ/DevComms/log_246_task_ap4_autopoly_fourth_pass.md`.
  Status: closed, guard PASS on all three json products, instance `ap4`
  down.
- 2026-09-09: task ap3 closed — AutoPoly's loop, THIRD PASS. Two more of
  the causes task ap2 counted fixed in the layer that owns each, each
  measured on its own cells before the loop, plus two measurements the
  brief asked for on their own. THE ANSWER: the polyfill-complete set —
  cells proved on all four compiled targets — is **151 of 253, covering
  85,530 of the outer set's 133,044 attested ledger rows (64.29%)**,
  against task ap2's 144 / 85,368 / 64.17% and task ap1's 120 / 76,634 /
  57.6%; proved on none fell from 66 cells / 16,534 rows / 12.43% to 56 /
  15,134 / 11.38%; runs carrying a cause from 324 of 1,012 to 293; **runs
  task ap2 proved that this loop does not: 0**. FIX 1, the ARRIVAL side
  of task ap2's fix 3: a 128-bit arriving vector register is rewritten as
  two 64-bit arriving values, `Concat(seed_<family>_high,
  seed_<family>_low)`, so the place is rendered from two parameters a
  target can receive and the gate aligns them on two IN rows — 31 of its
  40 pairs now prove, and the 9 that do not are an EMPTY compiled body (a
  vector register copy the compiler elides), not this fix's cause. The
  guard is per PLACE and not per cell: a place task h2's fix 2 projects a
  lane out of does read its arrival above bit 63, and the guard lane is
  what caught the first form of the fix rewriting the handful's own two
  vector cells. FIX 2, the 32 x87 cells at `key_width` 80: task ap2's
  cause for them (`no setter row to compose the flag pair from`) is false
  about the objects — **0 of the 32 rows reads the arriving flag state**,
  so they were never flag consumers; a preseeded row is now composed with
  a setter only where one of its terms actually reads that state. The
  PROBE the brief puts first LANDS: `long double emu(long double a, long
  double b) { return a + b; }` at the corpus's own ship flags carves to
  `fldt 0x18(%rsp); fldt 0x8(%rsp); faddp %st,%st(1); ret`, so c's
  `long double` is the 80-bit holder and the 30 x87 arithmetic cells now
  render, compile and carve to the x87 opcode on c; rust, go and swift
  have no 80-bit holder and are refused BY NATURE, which is the brief's
  own rule. THEY STILL PROVE NOTHING, and the reason is a STOP rather
  than a result: the CANONICAL FORM refuses the c body `no answer home`
  — "this unit's own code names no register the answer is left in" —
  because a `long double` answer is left in st(0) and its arguments
  arrive on the stack, and neither is a register family. That is the
  arrival-contract question, now measured on the ANSWER side as well;
  flagged, not worked around. FIX 3: `model_translate.py check` runs
  again after the one authorised line in `load_rows` (`row["mnem"]`, the
  name task mn1 renamed the field to) — 259 rows, 172 STATED, 87 REFUSED,
  exactly the brief's expectation and exactly 153 + 19 of the stored
  artifact, which was snapshotted and RESTORED byte for byte. FIX 4: task
  h2's normalise-before-render measured ALONE, the whole loop run twice
  with one switch moved — it is **not a no-op at scale**: 15 of 1,012
  runs render a different source and 9 differ in verdict, but no proof
  moves either way (nine float cells differ only in a commutative operand
  order; `setp`/`setnp` render a body of 19 instructions instead of 26 on
  c and rust; three divide runs shuffle DISPROVED against UNDECIDED at
  the solver's ceiling), so it stays ON. The arrival-contract group and
  every `sat` were NOT touched: 38 places over the same 12 cells, `sat`
  152 places at the plain comparison and 67 surviving the caller-extension
  re-pose. Report:
  `PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly3.md`.
  Log:
  `PseudoCoupHQ/DevComms/log_245_task_ap3_autopoly_third_pass.md`
  (32 claims: 8 MATCHES, 0 DIFFERS, 24 UNVERIFIABLE, 0 REFUSED, 0
  NOT_RERUNNABLE). Status: closed, guard PASS on all three json products,
  instance `ap3` down.
- 2026-09-09: task ap2 closed — AutoPoly's loop, SECOND PASS, after the
  six mechanical causes task ap1 counted were fixed, one cause = one fix
  in the layer that owns it and each measured on exactly the pairs it
  targets BEFORE the loop. THE ANSWER: the polyfill-complete set — cells
  proved on all four compiled targets — is **144 of 253, covering 85,368
  of the outer set's 133,044 attested ledger rows (64.17%)**, against
  task ap1's 120 / 76,634 / 57.6%; proved on none fell from 96 cells /
  27,011 rows / 20.3% to 66 / 16,534 / 12.43%; runs carrying a cause from
  445 of 1,012 to 324; **runs task ap1 proved that this loop does not: 0**.
  Per target at the destination place: rendered and compiled 199 c / 199
  rust / 190 go / 190 swift (was 167/167/153/153); PROVED at the 3,000 ms
  ceiling of record 156 / 159 / 160 / 152 plus 20 / 21 / 0 / 17 under the
  caller-extension re-pose; `sat` 15 / 14 / 16 / 5; undecided 8 / 5 / 14 /
  16; refused 54 / 54 / 63 / 63. THE SIX FIXES and what each moved of the
  pairs it targets: (1) a literal memory operand is an arriving value —
  the reference gives one 128-bit symbol per operand text and a load into
  a lane reads only its low bits, so where every use lies inside 64 bits
  it becomes a 64-bit arrival — 72 of 134 now proved (driver); (2) a flag
  consumer's setter taken from the corpus's own flag-pair ledger rows
  where its own cell names none — 0 of 128, AND THAT IS THE FINDING: all
  32 cells are x87 mnemonics at `key_width` 80, and the corpus records 25
  flag consumers, every one a `set*` or a `cmov*`, so the census answers
  None and the cause stands unchanged (driver); (3) a 128-bit place is
  rendered as TWO 64-bit places, low and high, each its own written place
  for the gate, in every target — 13 of 56 and 5 of 30 now proved, the
  rest carrying two honest new causes (the HIGH half of a whole-register
  vector place reads an arriving xmm above bit 63, which no target can
  receive: 40 runs) (driver); (4) a widening move's `key_width` is its
  DESTINATION width, read from `reference.SIGN_EXTEND` / `ZERO_EXTEND` —
  16 of 24 now proved, the eight cells that carried a null key now carry
  one and none does (table); (5) three additive registrations in
  `reference.py` — `cmovg` and `movswq` kept by a SEPARATE
  `EMULATION_MNEMONICS` list (the corpus census `CORPUS_MNEMONICS` is
  untouched at 162), and `lea`'s base slot made optional, an absent base
  read as zero — 14 of 15 now proved; (6) task h2's normalise-before-
  render ungated, which had silently fallen out from under `g1b`, `g1c`
  and task ap1 (driver). GUARDS, all passing: task h2's 24 sources
  identical; the handful's 14 places identical to task g1b's own product
  in name, width, layer-5 text and arrival families; the four vector
  cells untouched by fix 3; `cmovne` / `setne` composing with the setter
  their own attestation names. The table's own counts are unchanged
  through the regeneration except the three this task's changes make
  (`table_mnemonics` 171→173, `translated_triples` 6,218→5,912, attested
  rows 1,215→1,218), and the outer set is the same 253 cells over the
  same 133,044 ledger rows. `check_L2` guarded off the stored artifact
  (259 rows, 87 REFUSED, 153 STATED + 19 DISCREPANCY) because
  `model_translate.py check` cannot run — log_237 §14 item 1, still open.
  Products: `.../emulation/autopoly/autopoly2.{py,json,md}`,
  `autopoly2_cells.json`, `autopoly2_runs.jsonl`, `src2/`, `lanes_ap2/`
  (twenty lanes). Log:
  `PseudoCoupHQ/DevComms/log_244_task_ap2_autopoly_second_pass.md`
  (20 claims: 6 MATCHES, 0 DIFFERS, 14 UNVERIFIABLE, 0 REFUSED, 0
  NOT_RERUNNABLE, at its fixed point over four passes). FLAGGED: the
  brief's `LAW.md` and `task_ap1_brief.md` were never staged, so the
  standing rules were read from `note_server_session_start_here.md` §2,
  `CLAUDE.md` and log_243, and whatever the law says under "stop rules"
  was not read. Status: closed, verifier zero DIFFERS, instance `ap2`
  down.
- 2026-09-09: task ap1 closed — AutoPoly's FIRST FULL LOOP. the owner's loop
  (`for arch_opcode_i in set_of_unique_arch_opcodes: for lang_i in {c,
  rust, go, swift}: find_emulation(arch_opcode_i)`) run over its whole
  measured outer set for the first time: the 253 attested cells of
  `PseudoCoupHQ/Research/oracle/arch_opcodes/model/model_table.json`
  (a distinct (`mnem`, shape, `key_width`) triple with a TRANSLATED row
  whose attestation records at least one ledger row — task m1b's 253,
  counted again from the table and agreeing in both directions with task
  m1's attestation file), most-attested first, x four compiled targets =
  1,012 runs, in 19 minutes on the tower. The method is task g1b's driver
  (`.../emulation/handful/handful.py`, TASK `g1c`) imported and called,
  not one line of it edited; task ap1's own program is the loop around it
  plus five pieces of bookkeeping (the order, an incremental one-line-per-
  run store that makes a stopped lane resumable, the one re-pose, an
  exception out of the driver recorded as that run's cause, and the
  aggregate). RESULT, per target, at the destination place: 253 attempted;
  rendered and compiled 167 c / 167 rust / 153 go / 153 swift (nothing
  that rendered failed to compile); LANDED 62 / 59 / 25 / 57; PROVED at
  the 3,000 ms ceiling of record 129 / 132 / 136 / 124, plus 15 / 16 / 0 /
  13 under the caller-extension re-pose; `sat` 10 / 11 / 8 / 2; undecided
  13 / 8 / 9 / 14; refused 86 / 86 / 100 / 100. THE POLYFILL-COMPLETE SET
  — cells proved on all four targets — is 120 of 253, covering 76,634 of
  the outer set's 133,044 attested ledger rows (57.6%); three of four 17
  cells, two 14, one 6, none 96 (20.3% of the rows), the none-list in full
  with the cause on each target in the report's section 4.2. THE
  PRIMITIVE ROUTE reaches 29 cells in c (2 more with setup), 22 in rust,
  17 in go, 9 in swift; the term route carries 184 / 193 / 198 / 206, and
  38 cells reach no route on any target. BY CAUSE, the four targets
  summed, 445 of 1,012 runs carry one and there are twelve causes: the
  three largest are a cell whose term reads state that is not an arrival
  register (134 runs), a flag-consuming cell whose attestation names no
  setter (128), and a vector cell whose `key_width` IS the place width so
  there is no lane to project (56). `sat`: 110 places at the plain
  comparison, 39 surviving the caller-extension re-pose (c 13, rust 15, go
  8, swift 3); the largest is `ucomiss` xmm_xmm 32 on ALL FOUR targets,
  2,270 ledger rows each, z3's counterexample naming the NaN region — the
  edge-region model measurable, with the caveat that `fp.to_ieee_bv` is
  uninterpreted there. THE HANDFUL REPRODUCES: 36 of its 40 (cell, target)
  pairs come out of this loop with task g1b's own route, landing and gate
  verdict (32 character for character; the four that differ are `idiv`,
  whose only difference is the re-pose ceiling, 30,000 ms here against the
  handful's 300,000 ms), and the other 4 are one cell, `sub` imm_gpr 64,
  which is NOT in this outer set because the corpus attests no `sub` with
  an immediate operand at any width — a compiler emits an ADD of a
  negative immediate instead. TWO THINGS FLAGGED: the arrival-contract
  question task g1b raised on the divide is general — 7 places over 5
  cells, every one on the primitive route, in three shapes (3 arriving
  values against 2 for `idiv`, 1 against 2 for `xor` gpr_same 32 with
  5,190 ledger rows, 0 against 1 for `mov` imm_gpr) — and eight cells of
  the table carry `key_width: null`, six of them attested, which the
  driver's `%d` label format cannot take (24 runs, recorded as a result by
  cause and not worked around). Report:
  `PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly/autopoly.md`.
  Log:
  `PseudoCoupHQ/DevComms/log_243_task_ap1_autopoly_first_full_loop.md`.
  Status: closed, guard PASS on both json products, instance `ap1` down.
