---
id: hq.research.progress
status: living
---

# PROGRESS — research

- 2026-08-12: node founded (the owner's ruling, PCv5 session — state
  record `PRIVATE/PseudoCoup_v5/DevComms/log_020_session_state_2026_08_12.md`).
  `PRIVATE/PseudoCoupHQ/Research/` created beside it.
- 2026-08-12: kind-signature-clustering landscape survey launched — fetch and
  compare `node-types.json` across rust, python, kotlin, dart, c,
  cpp; measure feature uniformity; report what clustering machinery
  would consume. done — report at
  `PRIVATE/PseudoCoupHQ/DevComms/log_008_kind_clustering_landscape.md`
  (log_007 was already taken).
- 2026-08-12: kind-signature-clustering first pass built and validated — features.py /
  cluster.py / validate.py over five languages (kotlin held out); known
  overlap re-emerged partially (purity 0.685, 1 fully + 14 partially of 15
  ground-truth rows). Report at
  `PRIVATE/PseudoCoupHQ/DevComms/log_009_clustering_first_pass.md`.
- 2026-08-12: kind-signature-clustering second pass per the owner's three rulings — merge-tree
  spectrum replaces the single cut (spectrum.py + similarity_matrix.npz,
  clusters as queries), full-population hold-out validation against
  tree-sitter's own supertype declarations (mean AUC 0.712 over 29 groups;
  hand key demoted to secondary check, AUC 0.804), cluster_by_language.md +
  best_counterparts.json over all 800 kinds. Interpretation decisions 9 and
  10 dissolved, 9 remain. Report at
  `PRIVATE/PseudoCoupHQ/DevComms/log_010_clustering_spectrum.md`.

- 2026-08-12: dendrogram_explorer.html shipped (Research/kind_signature_clustering/): interactive icicle of the full merge tree, draggable threshold slice with live cluster count, entropy-colored cross-language merges, search+zoom. Export via export_tree.py -> merge_tree.json. See DevComms/log_012_dendrogram_explorer.md.
- 2026-08-12: kind-signature-clustering enumeration survey (plan-of-record step 1) —
  415 grammars enumerated (both orgs + wiki), 389 ship node-types.json,
  411 files fetched to `Research/kind_signature_clustering/raw_all/` with per-grammar
  quality signals and provisional category tags in
  `Research/kind_signature_clustering/grammar_inventory.json`; 31,858 named kinds total;
  25.3% of grammars are kotlin-like zero-role. Report at
  `PRIVATE/PseudoCoupHQ/DevComms/log_011_grammar_enumeration.md`.
- 2026-08-12: kind-signature-clustering plan-of-record step 2 (decision-6 counts fix)
  + archetype measurement — features v2 (log2-bucketed distinct-host counts
  on derived output positions; versioned `features_v2.json`): 711 of the
  1,271 identical-feature pairs split (saturation 1,654 -> 731), hold-out
  mean AUC 0.712 -> 0.770, 13/14 log_010 §6 stable clusters survive exactly
  (only the flagged-suspect s024 dissolves, correctly). Archetypes over all
  411 grammars: 31,212 clusterable kinds -> 8,329 unique v2 vectors (3.75x
  dedup; matrix 487.1M -> 34.7M pairs, 14x); dense-over-archetypes with
  multiplicity weights recommended for step 3, sparse demoted to optional.
  Artifacts: `Research/kind_signature_clustering/{features_all.json,archetypes.json}`.
  Report at `PRIVATE/PseudoCoupHQ/DevComms/log_013_counts_and_archetypes.md`.
- 2026-08-12: kind-signature-clustering plan-of-record step 3 (full-ecosystem spectrum)
  — multiplicity-weighted average linkage over the 8,329 archetypes (exactly
  full-population UPGMA over 31,212 kinds; 34.7M-pair dense matrix, whole
  pipeline ~15 s), hold-out validation at scale mean AUC 0.766 / median
  0.777 over 565 (grammar, supertype) groups (every category > 0.7), 473 of
  901 multi-kind clusters at t=0.40 span categories, isolated end EMPTY
  (min nearest-counterpart sim 0.400), top-30 empirical-universals table
  produced, dendrogram_explorer_all.html (category-colored, verified
  headlessly). Artifacts: `Research/kind_signature_clustering/{spectrum_all.npz,
  merge_tree_all.json,top_counterparts_all.json,holdout_validation_all.json,
  report_all.json,dendrogram_explorer_all.html}`. Report at
  `PRIVATE/PseudoCoupHQ/DevComms/log_014_ecosystem_spectrum.md`.
- 2026-08-12: kind-signature-clustering plan-of-record step 4 (basis report) — the
  spectrum cross-referenced against the intentions vocabulary (11 objects +
  A–J + form tier): all objects but `service call` empirically realized
  (`choice` strongest), A/B/C/E/G/H/I shape-invisible ecosystem-wide
  (log_008's rust finding generalized), 4 of 5 log_008 strains corroborated
  (sum types refuted as a shape), 10 missing-vocabulary families enumerated
  (import 155 langs, error-handling, pair/case 152 langs, …), 12-target
  coverage incl. the kotlin zero-role evaluation (0.640 in ≥10-lang
  clusters, via shape-poverty affinity). Artifacts:
  `Research/kind_signature_clustering/{basis_xref.py,basis_xref_out.json}`. Report at
  `PRIVATE/PseudoCoupHQ/DevComms/log_015_basis_report.md`.
- 2026-08-17: kind_fuzz_clustering phases 1 and 2 — layer 3, python only.
  Probe design written down first as
  `Research/kind_fuzz_clustering/probe_design.md`, eleven numbered judgment
  calls for the owner. A probe's operand is a layer-2 CELL rather than a
  dominant, so python's phase-0 space of 686 becomes 20,024 probes over 62
  kinds / 100 signatures (R2: one per operator on a grammar menu), operands
  drawn from the 26 cells the layer-2 audit passed and their 117 values,
  every literal-spellable probe written both opaquely and as a bare
  literal. One agent-lane run, 64.5 s: 7,868 answered, 11,736 raised, 388
  compile-refused, 32 over budget, none lost; folded into the first
  behavior signatures (`behavior_python.json`). Findings the census did not
  hold: `Decimal(42) + Fraction(42)` raises though both equal 42;
  `list += tuple` answers where `list + tuple` raises, so an augmented
  operator NESTS over its plain form inside one language; `<>`/`print`/
  `exec` as statements survive in the grammar and refuse to compile.
  Phase 3 (the other ten) is gated on the owner's review. Report at
  `PRIVATE/PseudoCoupHQ/DevComms/log_024_layer3_python_fuzz.md`.

- 2026-08-18: the owner's note on egress polyfill, recorded verbatim
  for the record (design remark, not a ruling): "polyfill could
  be fairly straightforward for egress out of the Hub since we
  are modelling all the base components. so it might not be as
  fast as natively written code that maps more directly to
  IR/arch opcodes but still fairly fast since it is still
  written in the target language. i suppose it depends on how
  frequently that polyfilled object is run." Connection to this
  line's data: the layer-3 acceptance tables say per operation
  which targets accept it natively (no polyfill) and which have
  a gap (polyfill; run-frequency decides the cost's weight).

- 2026-08-19: **two housekeeping passes over work already done — the
  census fold-back, and seven logs rewritten into the readable
  register.** Neither ran a probe; neither changed a number.
  - **Fold-back.** The five census pages in
    `PRIVATE/PseudoCoupHQ/Research/dominant_intentions/` were
    hand-drafted 2026-08-13 and say on their face that every fact is
    UNVERIFIED — they were the harness's work order. Logs 024 to 037
    then answered them and the pages were never updated. Each page now
    ends with one dated `## layer-3 findings, folded back 2026-08-19`
    section carrying only what the runs proved that the page does not
    say, with the log and section on every claim, the level on every
    claim, and a small per-section glossary so the section reads
    standalone. Detail per page is on the dominant_intentions node's
    own PROGRESS.
  - **Rewrites.** Logs 027 through 033 were rebuilt in place into the
    shape logs 034 and 035 already had: a glossary of the log's own
    words first, then a restatement of every prior-log fact the log
    leans on, then the body — every term defined at first use, lane
    names carried with words, no sentence depending on an unread log,
    and a note at the top stating the content is identical and only
    the prose was rebuilt. Glossary entries ran 25 to 37 per log and
    restatement bullets 8 to 34.
  - **Section numbers held, which was the risk.** Other logs and the
    kind_fuzz_clustering CHECK and PROGRESS files point at these logs
    by section and by numbered item. The heading list of each of the
    seven was taken before and after and compared: **zero headings
    missing**, and log 027's finding 11, log 029's decisions 1 to 11,
    log 031's decisions 18 to 30, log 032's eight numbered surprises
    and log 033's decisions 31 to 42 all survive at their numbers.
    `bash PRIVATE/PseudoCoupHQ/hq.sh check` reports 0 errors,
    unchanged.
  - **Two things left open by choice.** Small internal
    inconsistencies were found in five of the seven logs and were
    LEFT AS WRITTEN, since the instruction was to rebuild prose and
    change no content — they are listed in the record log as
    candidates for a correction pass that is allowed to change
    content. Separately, one genuine repair was made in log 033,
    where the twelve-by-twelve agreement matrix's swift row carried
    fourteen cells against twelve columns and would not render; the
    two duplicated cells were dropped and no value changed.
  - Record:
    `PRIVATE/PseudoCoupHQ/DevComms/log_039_census_foldback_and_log_rewrites.md`.
- 2026-09-05: sub-node `arch_unit_oracle` (node_0_3_8) founded by the owner
  as a parallel line — compilers as unit subjects, our own Hub-like
  compiler as oracle, cross-language construction of units. Isolated
  from compiler_graph by folder, instance prefix and node. Founding
  log `PRIVATE/PseudoCoupHQ/DevComms/log_206_arch_unit_oracle_founding.md`. planned.
- 2026-09-06: RESTRUCTURED on the owner's ruling — each research project is
  its own realized sub-node holding its own sub-nodes, and this node
  becomes the master plan. Three projects: `intentions` (the five
  language-side lines), `operator_equivalence` (was `compiler_graph`;
  the eleven pipeline sub-nodes plus interp_feeder and
  remaining_languages moved under it), `arch_unit_oracle`. Ids kept;
  only `hq.research.compiler_graph` superseded by
  `hq.research.operator_equivalence`. Addresses moved for 68 folders
  and 276 files; every relative link under Planning rewritten and
  re-checked; address map in the CORE §8. The CORE now carries the
  objective (dominant operators and types for the Hub), each
  project's contribution, the state table, the dependency table, the
  agreed order of work, the shared rulings and the open rulings.
  Record: `PRIVATE/PseudoCoupHQ/DevComms/log_212_research_restructure_and_master_plan.md`.
  done.
- 2026-09-06: steps 1–3 of the master order opened in parallel on
  four Airlock instances, one implementer each, coordinator reviewing:
  t100 dominant operators (solver equivalence between pool entries,
  pool6 candidate), t101 dominant types (the DWARF join of language
  spellings to machine holders), o5 the lowering-route cut of task
  o4's variants, o6 the leftover of o4 typed by go's own front end
  (`go/types`), as a measurement of the typing route in CORE §5.
  in-progress.
- 2026-09-06 (later): the five tasks above were stopped by a usage
  limit mid-run and resumed from their state on disk. t101 had
  stopped correctly at a flag (the stored DWARF parameter tables carry
  name and location only — log_213), so step 3 continues as t101b:
  re-read parameter types from anchor builds by task 24's DW_AT_type
  walk, then join. o6's full go/types pass hit its memory bound at
  6.1 GB and is re-run with more room and per-package, per the
  standing rule. t100 had answered 14,600 of 43,410 pairs. New: o7,
  the owner's note of 2026-09-06 (`DevComms/note_for_research.md`) — does
  the compiler collapse an emulation of x's operator written in y's
  operators to the unit it emulates; c first, gated three ways
  (bytes, term text, proof), with a c→c control. in-progress.
- 2026-09-06 (evening): results of the parallel round, each checked
  by the coordinator against its artifacts.
  - step 1 (o5, log_215): go's lowering route = 5,446 of 103,475
    sites, 283 resolved into 104 variants; clang's cut is zero because
    the sparse llvm checkout does not cover task 95's emitter region.
    done, with the per-population breakdown owed.
  - step 3 (t101b, log_217): the type join built from 92,127 DWARF
    rows re-read at anchor builds: 32 holders (class × width), 88/88
    machine type keys served, 9 DWARF-vs-inventory disagreements
    listed; swift's base types carry no DWARF encoding. done.
  - typing route (o6, log_216): go/types per package types 79,799 of
    103,475 sites at 541 MB / 160 s against search's 22,810; the
    whole-tree shape needs >12.5 GB. done; input to CORE §5.
  - the owner's note (o7, log_218): emulations rendered from go/rust/swift
    terms, compiled by clang: 168/204 proved equivalent to the x unit
    (193/204 under the caller-extension reading of narrow arguments),
    5/204 byte-identical to an existing c unit against a c→c control
    ceiling of 14/33; where proof fails the x body guards a case the
    term lacks (6 of 11), 5 unattributed. done.
  - step 2 (t100): 18,307 of 43,410 entry pairs answered (162 proved
    edges, 17,351 disproved); third four-hour lane running; closes
    with the complete groups named. in-progress.
  - bank (t102, log_214): rounds 16–19 and o1–o4 verified from disk;
    zero stale rows. done.
- 2026-09-06 (night): o8 (log_220), the owner's per-opcode question: of the
  243 single-opcode units with a proved term across five languages,
  217 rendered and compiled to c; clang LANDED on the row's own
  opcode for 197, on a different single opcode for 2 (go `add` →
  `lea`), and did not collapse 18 (of which 5 are store-through-pointer
  bodies whose term is the pointer); 216 of 217 proved, 155 byte-
  identical. Never landed from any language: `movb`, `mul`, `pxor`,
  `xorps`. done.
- 2026-09-06 (night): o9 (log_223), the opcode signature census over
  the 243 single-opcode rows: 25 of 162 mnemonics carry attested
  (input holders → output holder) signatures; reading kinds read off
  the data (15 reading-blind, 8 sign-sensitive, 13 width-changing, 13
  reading-changing); 25 mnemonics collapse to 20 arithmetic ideas.
  The 137 mnemonics without a single-opcode row need the signature
  read from ledger rows of multi-opcode units (owed). The `lea`-driven
  sign-sensitive pairings are suspect and marked so. done.
- t103 (log_222): cpython's `long_mul` carved (658 bytes); term built
  but UNDECIDED against its own body — a ten-instruction digit-store
  loop inside `long_mul`; JIT not enabled in the image's 3.14.7 build.
  The loop limit of the term walk now blocks two populations. done.
- 2026-09-07: t100 closed (log_224). 21,502 of 43,410 entry pairs
  answered over three four-hour windows (largest type-key groups
  first): 226 proved, 19,640 disproved, 1,099 undecided (all
  sub-process wall-clock limits, none solver timeouts), 537
  unbuildable. Only 12 proved edges were APPLIED: the closure rule
  applies an edge only when both representatives' terms are proved
  against their own ship bodies, and 214 proved edges have one side
  unproved. pool6 CANDIDATE: 1,831 → 1,819 entries; not ratified. The
  merges text identity missed are operand-order variants of one
  computation (e.g. `If(v0 == Concat(0, Extract(31,0,v1)),0,1)` vs
  the swapped form) — a layer-5 normalization gap (commutative
  operand order), fixable without the solver. 5 of 88 groups
  complete; 61 groups untouched. done, with the 214 and the
  normalization gap owed.
- 2026-09-07: o10 (log_225), the signature census from ledger rows
  over all 31,078 units: 112 of 162 mnemonics carry signatures (38
  are flag readers, 12 never produce a ledger row); reading kinds
  counted; 112 → 79 ideas as an UPPER bound (the sign-sensitive pair
  rule fires on any operand position and so pairs float-precision
  twins like `addsd`/`addss`; restricting it to the operand that
  carries the sign is owed, decided by the coordinator, not a ruling).
  Non-IN rows carry width but class `unknown`, so most signatures are
  width-only. done.
- 2026-09-07: o11 (log_226), AutoPoly with rust as the target. The
  coverage table (62 term operators × {c, rust}): rust 42 direct, 20
  idiom, 0 none; the one hole is a SORT, 16-bit float (rustc 1.96.1
  refuses `f16`). 400 entries with a c/go/swift member and no rust
  member: 320 rendered, 320 compiled (rustc refused none), 243 proved
  (76%), 284 under the caller-extension reading (89%); control
  ceiling for byte identity 27/39 (69%, above clang's 42%). Per-opcode
  on rust: 99 of 107 LANDED (93%), the two elsewhere are `add`→`lea`
  as with clang. Idioms of note: division needs an unreachable hint
  at exactly the machine's undefined conditions to shed rust's two
  checks; float→int must use `to_int_unchecked` (plain `as`
  saturates). Owed, decided by the coordinator: rename the `mnemonic`
  field to `mnem` in o2/o8 artifacts (ends the guard collision);
  add `cmpordss`/`cmpordsd` to the shared opcode table (16 emulations
  UNDECIDED for want of it). done.
- 2026-09-07: L1 (log_227), Lean 4 as the gate's second discharger.
  Installed in the image (v4.24.0, core only). Eight of ten t100 edges
  re-proved with a checked certificate in ~0.2 s each (two refused:
  floating point, no bit-vector theory for it). The renderer's
  PRESERVATION THEOREM for the integer subset (18 constructors) is
  PROVED by structural induction, no `sorry`, axioms only the standard
  three; the proof forced a correction about C (the shift count is an
  `int` after promotion) and models undefined behaviour as `none`, so
  the theorem also says the rendered C is always defined. Costs:
  bit-blasted division proves at 16 bits in 283 s / 12 GB and not at
  32 or 64 within 600 s; Lean's `/` and SMT-LIB's `bvudiv` differ at a
  zero divisor. 25% of pool5's printed entries are inside the subset;
  integer side closed in 5–9 person-days, rust beside c 7–13, floating
  point 15–30 (its own line). Decided by the coordinator: next on the
  node, comparisons and truth connectives first (coverage toward
  ~60%), then the rust expression type; the term store's unguarded
  `bvudiv_i` print form is retired after t104 lands (a layer-5 change,
  audited the same way). done.
- 2026-09-07: log_228 (a branch conversation on Lean and the float
  model) reviewed; log_229 written: the purpose as levels 0–4 (the
  complete opcode mapping model → terms → dominant operators →
  emulation by two producers → AutoPoly/Hub), what in 228 stands,
  the over-corrected float estimate split (model: days; lemma
  library: weeks; bit-blasting: the fallback), the frontier named as
  memory and loops. SUPPORT_BRAINSTORM_autopoly §9 and the lean CORE's
  "proposed widening" added. Awaiting the owner: the lean node's definition;
  the synthesis route as a task.
- 2026-09-07: the owner ruled the alignment ("make the updates according to
  our alignment -- including your recommendations"). Recorded in the
  COREs: the typing route (front end as oracle); cross_construction
  unfrozen on the emulation route with sub-node `autopoly`;
  hub_compiler lowers by source composition (founding form kept under
  its date); the lean node is the operator-mapping proof system with
  three realized sub-nodes (model_translator, certificates,
  renderer_theorem) and the translator first; the synthesis route as
  a task. Master order §4.2 revised; §5 open reduced to the mode axis,
  pool6 ratification, type_vocabulary. done.
- 2026-09-07: o13 (log_231), render the mode. Of the 95 disproved
  emulations (36 c, 59 rust) only 10 carry a ledger guard row; the
  guard was rendered for those 10 and proved 3. The re-run's other
  gains (27/36 c, 42/59 rust proved) come from the caller-extension
  reading already applied in o7/o11, so the coordinator's expectation
  that most disproofs were guards was WRONG: most x bodies are total
  and the disagreement is elsewhere. 5 (4 c, 1 rust) have a correct
  guard and a differing guarded-body value; 26 remain disproved with
  no guard row, unattributed. Raising the ceiling to 30,000 ms moves
  3 verdicts; 3,000 ms is the record. Mode data for the ruling: 7 pool
  entries carry a mode, one carries three guard kinds. done.
- 2026-09-07: o12 (log_230), the synthesis route: compositions of c
  entries' terms (same type-key bucket) found by counterexample-guided
  search at depth ≤3 for 206 targets in 466 s: 4 PROVED (2 at depth 1,
  2 at depth 3), 135 none at depth 3, 16 undecided, 51 whose text the
  parser could not rebuild into z3. Far below the compiler route
  (168/204). Cause, by the coordinator's reading: the component
  library has no width adapters (extract, extend, concat, literals)
  as free glue, so a target whose term changes width cannot be
  reached; the 4 that composed are same-width. Decided: one more pass
  WITH adapters before the route is judged; no sub-node; no budget on
  the 16 undecided. done.
- 2026-09-07: L2 (log_232), the model translator. 160 of 171
  mnemonics translated from `reference.py`'s own builders into 3,933
  Lean definitions (floating point through 27 OPAQUE primitives — a
  placeholder, not yet a model). Check over the 259 single-opcode rows:
  39 definitional (`rfl`), 114 by `bv_decide`, 87 refused by cause
  (44 float, 21 stateful place, 16 no proved term, 6 other), 19
  DISCREPANCY — all `add`/`imul`/`sub`, one shape: the check's own
  composition of model steps pairs operands differently from the
  unit's proved term; the coordinator reads this as a bug in the
  check's composer, to be fixed and re-run, not a model discrepancy.
  Trust note: 61 of the 153 proofs carry `Lean.ofReduceBool` /
  `Lean.trustCompiler`, i.e. they rest on native evaluation, a weaker
  base than a kernel-checked certificate; to be re-proved by
  `bv_decide` proper or marked. Decided: the mnemonic field is `mnem`
  in Lean-side json as in o11 (no exemption); 259 vs 243 is the
  brief's own "with a proved term" filter, no mismatch. done.
- 2026-09-07: t104 closed (log_233). The one-function change to
  `Term.normalize` (order commutative operands before the first
  simplify) changed 225 of 27,866 printed texts; the store otherwise
  matches term66_store; the 44 non-converging units unchanged. The
  pairs t100 proved and text identity had missed NOW MERGE BY TEXT:
  cpp/op_509 and swift/regen_1023 both print
  `If(Concat(0, Extract(31, 0, v0)) == v1, 0, 1)` and sit in one
  pool104 entry (E00170, 264 members, c/cpp/swift); likewise E00156.
  pool104 candidate: 1,650 entries over 30,324 members — a DIFFERENT
  intake from pool5 (1,831 over 30,432; pool5 also carried the
  interpreter and swift units outside the term store), so the two
  entry counts are not before/after of one population; the closer's
  "same 4 matched" line undercounts what the store shows. Two guard
  violations in the task's own instrumentation fixed; the pass-2
  ceiling raised (3,072 → 7,168 MB, one worker) with both results
  reported. done. Next: pool6 over the re-normalized store on pool5's
  full intake, then ratification.
- 2026-09-08 (task mn1, log_235, first task run on the TOWER): the field
  `mnemonic` renamed `mnem` in the five oracle generators and every
  artifact regenerated by its own generator on the tower (o2 → o9, o10 →
  o8). Every headline count unchanged: 259 single-opcode rows, 162 unique
  mnemonics, o9 243/16, o10 31,078 units, o8 243/197/155/216. Three
  artifacts now pass the spelling guard clean for the first time
  (`unique_opcodes.json`, `per_opcode_population.json`,
  `per_opcode_held.json`). Four still fail, each pre-existing and reported
  by cause, with the coordinator's disposition: (A) o9's and o10's
  per-mnemonic tables are DICTS KEYED BY MNEMONIC (33 + 58 findings) — under
  the ruling of 2026-09-08 a mnemonic alone is a spelling, so these tables
  are keyed short of the machine-form triple; they stand as the census they
  were and are SUPERSEDED by task m1's table, not repaired; (B) the
  `mnemonic_a`/`mnemonic_b` pair fields, same disposition; (C) o8's
  `landed_mnemonic` field (57) and (D) o2's `zero_opcode_examples` records
  lacking a `lang` field (30) are shape fixes for one small closer after m1,
  not tasks of their own. Verifier: 22 claims, 15 MATCHES, 0 DIFFERS, 5
  UNVERIFIABLE, 2 NOT_RERUNNABLE. The remote path (`remote_lane.sh`,
  Airlock) carried every lane; peak RSS of the shard stream 113,608 kB.
  Task m1 (the model table keyed by the triple) started on the tower the
  same day.
- 2026-09-08 (task m1, log_236, on the tower): the arch-opcode MODEL TABLE,
  keyed by (mnemonic, operand form, width) per the ruling of the same day,
  `Research/oracle/arch_opcodes/model/`. Reference models 171 mnemonics;
  the corpus's 162 are ALL among them (corpus-only = 0; the 9 table-only are
  task 63's archive mnemonics). 62,418 sweep attempts, 34,867 translated,
  8,703 distinct triples with a mapping, 5,155 distinct mappings by printed
  text. The corpus, by one stream over the 332 shards (130,108 arch-opcode
  ledger rows, 109,052 placed), attests 219 cells; 83 of them have no
  translated row because the sweep never spelled that form. 86 mnemonics
  carry more than one mapping across their forms (`imul`, `div`, `idiv`,
  `mul` split one-operand vs two-operand as predicted); 2 of 24 same-builder
  groups are true aliases (`movapd movaps movdqa`; `fstp fstpt`). Guard PASS
  on all four json; verifier 12 claims, 0 differ. Three findings for the
  record: (1) `build_division` names no fault region — quotient and
  remainder are z3's total SDiv/SRem, so division by zero and MIN/-1 are
  total in the reference; the hardware's fault lives in the ledger's guard
  rows, not in the builder; (2) `build_binary`'s first line sends any
  one-operand line to the widening multiply, so one-operand `add and or sub
  xor` (no such encodings) get 24 wrong table rows, attested 0 times; (3)
  the sweep's shape grammar has no x87 `%st` operand, so 1,259 corpus rows
  are unclassified and the x87 cells collapse. The `add`/`lea` equality the
  brief expected is CROSS-FORM (`lea (%rdi,%rsi,1)` against `add %rsi,%rdi`)
  and the triple key never pairs it; at the same form the two differ
  (memory contents vs address), verdict `sat` at all 12 cells — the brief's
  expectation was wrong at the key level, the table is right. Closer m1b
  owed: restrict the one-operand branch to `mul`/`imul`, add `%st` shapes,
  re-run attestation; plus mn1's (C) and (D) shape fixes.
- 2026-09-08 (task m1b, log_237, on the tower): the model table's attestation
  join corrected (one `key_width` rule on both sides; flag-consumer rows
  read; three x87 shapes added to the sweep, additive; the reference's
  one-operand branch restricted to `mul`/`imul`, `check_L2` unchanged at
  259 rows / 172 STATED / 87 REFUSED under both changes). Coverage of the
  162, summing exactly: 134 mnemonics have a value cell on a translated
  row; 3 are attested at forms the sweep cannot model (`pcmpeqb pcmpeqd
  pmovmskb`, no builder); 17 are control transfers, attested by 1,201 guard
  rows, never by a value cell; 8 never placed, each with a measured cause
  (6 produce no ledger row: `nop nopl pop fstp fxch cwtd`; 2 recorded under
  a `non_opcode_phrase` producer: `movb`, `fstpt`). THE LOOP'S OUTER SET,
  measured: 257 attested (mnemonic, form, width) cells, 253 landing on a
  translated mapping, over 134 mnemonics; 22,741 flag-consumer rows now
  counted. Verifier 26 claims, 0 differ. Owed to a later closer, none
  blocking: `model_translate.load_rows` reads o2's old field name;
  o8's `landed_mnemonic` needs the record shape `landed: {mnem}` to satisfy
  the guard; `st_st` needs the second operand order (`%st(1),%st`, 1,139
  rows); `movb`/`fstpt` are a ledger fact, not a table defect.
- 2026-09-09 (tasks h1 and h1b, logs 238–239, on the tower): the FIRST
  `find_emulation` runs on CELLS of the model table (no unit behind them):
  ten cells × {c, rust}. 16 of 20 compiled; c and rust gave byte-identical
  bodies in every compiled case. Proved: `add` (landed on `lea`), `sub`
  imm (`lea`), `imul`, `sar`, `shr` (each on itself), `cmovne` (rendered as
  the setter+consumer pair, came back `test; cmove`), `setne` (`xor; test;
  setne`, proved under caller extension). Not proved, both printing defects
  of ours: `idiv` UNDECIDED at 3 s and 300 s because the table prints the
  dividend's sign extension as 32 joined one-bit copies (the pool's
  normaliser collapses this; the table's printer does not use it) and the
  compiler made 51 instructions of it; `addss`/`cvtsi2sd` refused by both
  renderers ("vector arrival used beyond its low lane": the cell's place is
  the whole 128-bit register, the renderers hold nothing wider than 64).
  h1b added the owner's composition column: each carved body as the list of table
  cells it is; every LANDED run is exactly one cell (its target); 198 raw
  instructions = 120 cells + 76 chaff + 2 unplaced (`cqto`, no operand →
  no width; a classifier gap for zero-operand opcodes). Verifiers 17/0
  differ and 17/0 differ. Next: h2, the same handful after the two printing
  fixes and the `cqto` width rule, then the go/swift printers, then the
  loop over the 253 cells.
- 2026-09-09 (task h2, log_240, on the tower): the handful re-run after the
  two printing fixes, both in the driver, renderers untouched (o8's 243
  rows re-run unchanged: 243/197/155/216). The lane projection turned the
  four float refusals into four runs that LAND on their own opcode and
  PROVE (`addss`, `cvtsi2sd`, c and rust), the upper lanes proved
  pass-through. The normaliser pass was a measured NO-OP: `Term.normalize`
  leaves the 32-copy sign extension as it is, so `idiv` is unchanged (76
  instructions, 51 after chaff, UNDECIDED at 3 s and 300 s) and h1's
  hypothesis that the copy shape is the cause is UNTESTED, not refuted. Now
  9 of 10 cells prove in both targets; c and rust byte-identical in all 14
  places both compile. `cqto` now classifies (zero-operand width rule).
  Flags: xmm operands carry no width in the classifier (`addss` line
  REFUSED in composition); `cbtw cltq cqo` classify to triples with no
  translated row. Reading for the next step: `idiv`'s body holds `idiv`
  itself plus 50 cells building a 64-bit dividend the term demanded; under
  the owner's primitive-plus-edge-regions model the emulation of a division cell
  is y's own `/` on the cell's holders (body `cltd; idiv`), and the term
  rendering is the fallback, not the first route. Next: g1 — the go and
  swift printers, primitive-first rendering with term rendering as
  fallback, the same handful on four targets.
- 2026-09-09 (tasks g1 and g1b, logs 241–242, on the tower): `find_emulation`
  for go and swift, PRIMITIVE-FIRST (a language operator whose whole body is
  the cell; else the term route). The handful on four targets: 36 of 40
  prove; the four that do not are `idiv` on every target. go's and swift's
  printers each worked on their first run of record, spellings measured
  against each compiler by probes. Two findings that need the owner: (1) the
  `idiv` cell reads THREE arrivals (dividend high half, low half, divisor)
  while every language's `/` reads two and derives the high half with
  `cltd`; the emulation is the cell RESTRICTED to the region high =
  sign-extension(low), and the gate, which aligns arrival rows one to one,
  cannot pose a comparison over a constrained region — an arrival-contract
  question, not a solver-time one (c's primitive route: body of 5, still
  undecided for this reason); (2) `swiftc -O` emits the exported entry as a
  one-`jmp` thunk to the mangled body, so the carve read the thunk (the
  unit-boundary ruling meeting a compiler that hides the body behind a
  second symbol). Also measured: the primitive route reaches an operator
  exactly when the target leaves the edge region undefined (c); rust, go and
  swift wrap their divides in guards inside the body, so no single-opcode
  row exists for them. Two instance facts fixed: `g1.conf` now mounts
  `sandbox-persist` read-only (an instance with no persist line gets an
  EMPTY volume of its own, and swift lives on sandbox-persist), and the
  image carries `libncurses6`. Verifiers 16/0 and 26/0 differ.
- 2026-09-09 (task ap1, log_243, on the tower): AUTOPOLY'S FIRST FULL LOOP —
  the 253 attested cells × {c, rust, go, swift}, 1,012 runs, g1b's driver
  unchanged, 19 minutes, peak 2.4 GB. Proved on ALL FOUR targets: 120 cells
  covering 76,634 of 133,044 attested ledger rows (57.6%) — the
  polyfill-complete set, first pass, no tuning. Three targets 17 cells
  (12.8%), two 14 (7.5%), one 6 (1.9%), none 96 cells (20.3%). Per target
  proved: c 129, rust 132, go 136, swift 124 of 253. Nothing that rendered
  failed to compile. 445 runs carry a cause, twelve distinct: (1) the term
  reads state that is not an arrival register, 134 runs / 37,874 rows; (2)
  no setter row to compose a flag pair, 128 / 6,284; (3) whole-register
  vector cells with no lane to project and no 128-bit holder, 56 / 19,324
  (+30 on go/swift for the 128-bit flags place); (4) `sat`, 31 destination
  places / 14,261 rows, the largest `ucomiss` on all four targets with the
  NaN region as counterexample (the float model); (5) six table cells with
  `key_width: null` crashed the driver, 24 runs / 19,448 rows (a table
  defect); (6) reference gaps `cmovg`, `movswq`, `lea 0x0(,%rdi,8)`; (7)
  the arrival-contract question, now general: 5 cells on the primitive
  route (`idiv` 3-vs-2, `xor` gpr_same 1-vs-2 with 5,190 rows, `mov`
  imm 0-vs-1). The handful reproduces (36 of 40 verbatim; the 4 differ by
  the re-pose ceiling only). Verifier 22 claims, 0 differ. Two rulings owed
  to the owner: the constrained-region comparison for derived arrivals; whether
  `key_width: null` is fixed in the table or the driver.
- 2026-09-09 (task ap2, log_244, on the tower): AutoPoly loop, SECOND PASS
  after the mechanical fixes (memory and flag state in the parameter plan;
  the 128-bit place as two 64-bit halves; six `widen_*` key widths; three
  reference registrations `cmovg`, `movswq`, base-less `lea`; h2's
  normaliser ungated). Proved on all four targets: 120 → 144 cells, 57.6%
  → 64.2% of attested ledger rows; on none: 96 → 66 (20.3% → 12.4%). ZERO
  regressions: every run ap1 proved, ap2 proves. Per target proved: c 156,
  rust 159, go 160, swift 152 of 253. What did not move, and why: the 128
  "no setter" runs are the 32 x87 cells at key width 80, not flag consumers
  (no setter exists; correctly left); `sat` 31 → 30 (+20 new places reaching
  the gate, mostly float NaN region and go's compare-masks at equal inputs);
  the arrival-contract cells unchanged (now 38 places over 12 cells,
  awaiting the owner); whole 128-bit VECTOR ARRIVALS still have no holder (40
  runs; the answer side is fixed, the arrival side is not). `check_L2`
  could not be re-derived because `model_translate.load_rows` still reads
  o2's old field name (open since log_237) — guarded off the stored
  artifact instead (259 / 87 REFUSED / 153 STATED + 19 DISCREPANCY). Two
  process facts: the session scratchpad was WIPED at 12:47, taking LAW.md
  and every brief before ap2's; ap2 ran under the standing rules in
  `DevComms/note_server_session_start_here.md` and CLAUDE.md and reached no
  stop rule; the law and all nine briefs of this round are now in the repo
  at `Research/LAW.md` and `Research/briefs/`. And one breach, self-reported:
  ap2 deleted one status file under `<runs>/ap2/` while renaming a
  lane (its log and `.done` entry survive); the LAW now states the
  never-delete rule with status files named. Verifier 20 claims, 0 differ.
- 2026-09-09 (task ap3, log_245, on the tower): AutoPoly loop, THIRD PASS.
  Proved on all four: 144 → 151 cells, 64.2% → 64.3% of attested rows; on
  none: 66 → 56 (11.4%); runs carrying a cause 324 → 293 of 1,012; zero
  regressions. What moved: a whole 128-bit VECTOR ARRIVAL now has a holder
  (two 64-bit parameters): 31 of 40 proved, the other 9 are
  register-to-register copies whose compiled body is EMPTY (`movaps`,
  `movapd`, `movdqa`: the identity, a pre-existing cause). The x87 cells:
  c's `long double` PROBED and LANDS (`faddp %st,%st(1)`), the 30 x87
  arithmetic cells now render, compile and carve to the x87 opcode on c —
  and prove nothing, because the canonical form names no ANSWER HOME for a
  value in st(0) and no ARRIVAL for a value on the stack: "this unit's own
  code names no register the answer is left in". That is the same question
  as the arrival-contract group (38 places, 12 cells, unchanged), now
  measured on the answer side: THE CANONICAL FORM'S CONTRACT KNOWS ONLY
  REGISTER FAMILIES. `model_translate.py check` un-blocked (one line;
  259 / 172 STATED / 87 REFUSED exactly as stored; the lane restored the
  check's overwritten files byte-identical). h2's fix 1 measured alone on
  1,012 runs: 15 sources differ, 9 verdicts differ, NO proof moves either
  way; kept on. One new `sat`: `idiv` gpr_one 16 on rust at IN_0 = 0x8000,
  the signed-division overflow edge, reached by the solver inside the same
  ceiling. Verifier 32 claims, 0 differ. Awaiting the owner: (1) the contract for
  values not in a register (derived arrivals; the x87 stack; the empty-body
  identity copies), one ruling covering 38 + 92 + 23 runs; (2) whether cpp
  becomes a fifth target (structural: changes what "all four" counts).
- 2026-09-09 (task ap4, log_246, on the tower): AutoPoly loop, FOURTH PASS,
  carrying the owner's ruling "a place may be stated by a constraint": derived
  arrivals as a REGION in the driver's check (`IN-0 = SignExt(IN-1)` for
  the divides; `gpr_same` binds one arrival; an immediate is a constant),
  the empty compiled body as the IDENTITY (33 of 34 places proved), and the
  x87 stack read in the driver over the reference's own state (the ledger's
  `fstpt`/`fldt` edges written; `answer_of` and `align_by_row` cannot read
  an x87 value and were not named by the brief, so the x87 population,
  114 runs / 6,284 rows, is UNCHANGED and remains the next closer's).
  Proved on ALL FOUR: 151 → 162 cells, 64.3% → 79.7% of attested ledger
  rows; on none: 56 → 20 cells (9.4%); runs with a cause 293 → 237; zero
  regressions; the arrival-contract group 38 → 0 (7 real derived-arrival
  places, 4 DISPROVED with the region printed, 3 PROVED; the other 31 were
  halves of a flags place the driver already refused unhalved). Per target
  proved: c 204, rust 170, go 177, swift 163 of 253. Three guards unchanged
  (check 259/172/87; o8 243/197/155/216; h2 handful 24/24). Verifier 34
  claims, 0 differ. New for the coordinator: an `imm_*` cell's key carries
  no immediate, so `mov` imm_gpr disproves against corpus rows with a
  different constant — the immediate is an INPUT of the mapping and the
  sweep bakes `$0x3` in; the next closer makes it symbolic. cpp as a fifth
  target: task ex1 (starting).
- 2026-09-09 (task ex1, log_248, on the tower): EXPANSION beyond the four.
  (1) cpp as a fifth compiled target: c's renderer with two measured
  differences (`extern "C"` linkage; `<cstdint>`/`<cstring>`), 305 of 309 c
  sources compile verbatim under `clang++ -std=c++20 -O1 -c`; cpp proves
  225 of 253 cells (63 outside the four-way set, the x87 arithmetic among
  them, since cpp has `long double`); cells proved on all four and not on
  cpp: 0, so all-five = all-four = 162 cells / 79.7%, both reported. (2) The
  interpreted languages: `find_emulation` rendered for cpython, php, ruby,
  java, javascript, dart, csharp (all seven runners present in the image or
  the persist volume), and a CHECK defined and stated LITERAL before it
  ran: the fuzz method over an ordered sample whose edge values come first
  (sign boundary, top, -1, the width's shift counts, subnormals, infinities,
  NaNs; ≤20,000 points per place). The handful, 70 runs: 70 rendered, ZERO
  disagreements at ~38,240 scored points per target; declines counted
  under each language's own word (division by zero; php's and c#'s
  refusal of MIN/-1; 630 points where the reference's float term has no
  numeral, the NaN region). An agreement is evidence, not a proof. Awaiting
  the owner: the JIT dumps (`jit_out_*`) are three formats none of which is
  objdump's, so "carve the JIT output" has no reader — a new instrument;
  whether the polyfill-complete set is counted at four or five targets
  (equal today; cpp is c's twin). Next: ap5 (x87 end to end; symbolic
  immediates), then ex2 (the interpreted loop over all 253 cells × 7).
- 2026-09-09/10 (task ap5, log_249, on the tower; cut off once by a usage
  limit, resumed from disk): FIFTH PASS. The x87 reading moved into the
  layer that owns it (`reference.answer_of` reads an `X87_<k>` home;
  `pool100_entry_equivalence.align_by_row` aligns an x87 arrival in both
  spellings; the driver's stop-gap `x87_answer_for_unit` removed): 36 x87
  c places PROVED, no x87 place `sat` or DISPROVED (the 80-bit explicit-
  integer-bit difference does not appear); rust/go/swift refused by nature.
  The immediate as an INPUT: 20 `imm_*` cells given a symbolic row
  (`shapes_for`, additive; 0 existing rows changed), six `sat` → proved.
  Proved on ALL FOUR: 162 → 165 cells, 79.7% → 80.25%. Four guards at
  their stated tallies. ONE REGRESSION, and the STOP fired: `sbb` imm_gpr
  8 on swift — the symbolic row renders with four parameters and swiftc
  answers the `@_cdecl` entry with a five-byte tail-call thunk (`jmp`,
  PLT32 relocation to the mangled symbol), so the carve holds one `jmp`
  and no arithmetic; ap4's three-parameter rendering carved 21 bytes and
  proved. Same mechanism as g1b's swift divide. COORDINATOR'S DECISION,
  to be carried by the next compiled-loop closer unless the owner objects: the
  carve follows exactly one unconditional `jmp` whose relocation names a
  symbol in the same object when that `jmp` is the whole body — the thunk
  is the compiler's linkage artifact, the unit is the function the
  exported symbol stands for; the unit-boundary ruling of 2026-09-04 is
  not changed, the reading of "the body" is. Verifier 38 claims, 0 differ.
  Started next, side by side: l3 (proof system), hub1 (Hub v1), ex2 (the
  interpreted loop).
- 2026-09-10 (task ex2, log_250, on the tower): THE INTERPRETED LOOP —
  253 cells × {cpython, php, ruby, java, javascript, dart, csharp}, 1,771
  runs, ex1's check unchanged. Every cell that rendered agreed on its whole
  sample on every target: 193 cells on cpython/ruby/javascript, 184 on
  php/java/dart/csharp; ZERO disagreements; zero timeouts. All seven
  interpreters agree on 184 cells / 116,057 rows / 87.2%; all twelve
  targets (five compiled proved ∩ seven agreeing) 158 cells / 75.2%. The
  loop's own runs found and fixed one harness defect in the interpreted
  route: a place name carrying `.` or `-` (`flags.low`, `stack_-8`) made
  an invalid identifier; six targets refused with a parse error, csharp's
  reused build folder RAN A STALE DLL from an earlier build and produced
  wrong answers that looked like language disagreements (17 runs) — fixed
  by sanitising both characters as the compiled route already does; the
  before-fix store is kept beside the run of record. Flags: the compiled
  route carries the same dormant hyphen gap; six nullary cells (self-XOR)
  cannot be checked by an interpreter (a harness gap); the all-five figure
  is a lower bound until cpp is re-run after ap5. Process: two closers
  ended their turns while the lane ran (the 120 s tool cut), the original
  implementer was woken by its own background wait and finished; the law
  and `remote_lane.sh wait` now enforce sliced waits. Verifier 0 differ.
- 2026-09-10 (task l3, log_251, on the tower): THE PROOF SYSTEM'S OWED
  ITEMS. The 19 DISCREPANCY rows of the L2 check were one defect in the
  check's composer — but NOT the one the coordinator named: neither side
  numbered arrivals by the C parameter convention or by ledger order; both
  are print-order rules, and the stored line's `v0`/`v1` come from
  `Term.normalize`'s commutative ordering (t104 added its first step after
  the check was written) while the composer numbered after a plain
  `z3.simplify`. Verified on the rows first, then the composer made to
  call `term.py`'s own `order_commutative`/`ordered_symbols` and to PROVE
  the naming per row against the stored line. All 19 now STATED by
  `bv_decide` (0.4–1.0 s each): the check reads 259 / 172 STATED / 87
  REFUSED, DISCREPANCY 0 — THE GUARD VALUE FOR EVERY LATER TASK. The "61
  native-evaluation proofs to re-prove": a false premise — `native_decide`
  occurs nowhere; `Lean.ofReduceBool` is `bv_decide`'s own axiom whenever
  it calls the SAT solver, Lean 4.24 offers no route out, and 0 of the 72
  such rows close by rewriting alone (`bv_normalize`). Trust classes over
  the 172 proved theorems: 20 no axiom, 19 propext/Quot.sound, 61 Lean's
  three, 72 also trusting the compiler; none with sorry. COORDINATOR'S
  DISPOSITION: the 72 stand as the SAT-certificate class (the lean node
  names it); `model_L2.json`'s mnemonic-keyed `per_mnemonic` summary is a
  diagnostic keyed short of the triple, superseded by the model table,
  not repaired. Verifier 29 claims, 0 differ.
- 2026-09-10 (task hub1, log_252, on the tower): HUB v1, FIRST FORM. The
  dictionary read off the loop (c 151 entries / rust 151 / go 161, holes by
  cause), the front end (tree-sitter-go + go/types; a node resolves where
  go's own compiler lowers that construct at those holders to ONE cell, by
  o2's narrow rule over go's own corpus; the candidate set is the type
  tuple, machine form), source composition (each node a call of its
  cell's proved emulation; the target's compiler lowers ACROSS the calls —
  measured: `a + b - c` on c came back `lea; sub; ret`, both calls gone),
  and the oracle test. The eight-function handful: c 4 proved / 4 holes,
  rust 5 / 3, go 5 proved on re-pose without `//go:noinline` / 3 holes.
  THE MEASURE over the corpus's own go units (134 that name one cell):
  composed c 100, rust 114, go 124; PROVED c 100 of 100, rust 114 of 114,
  go 108 of 124 on re-pose; DISPROVED 0. Everything composable is proved.
  The holes are structural, and they name Hub v2: (1) 61 of 253 cells
  write only flags — no comparison (`a != b`, `a < b`) composes without a
  flag state across nodes; the loop already proves the (setter, consumer)
  PAIR cells (`test; cmove`, `xor; test; setne`), so the front end should
  resolve a comparison feeding a select as the pair entry, no new flag
  machinery; (2) go's guarded constructs (`<<` at uint64 = six cells with
  the count guard; `/` at int32 = eight with the zero and overflow guards)
  lower to a SEQUENCE, never one cell: the Hub needs entries at the
  OPERATOR-BODY level too — the pool entries, whose emulations o7/o11
  already proved 76–95% to c and rust — the two AutoPoly branches meet
  here; (3) the primitive route's lookup key carries no holder widths, so
  five proved entries have truth-holder parameters a composition cannot
  use — a loop fix, cheap under bank1's delta mode. Verifier 28 claims, 0
  differ; peak 112 MB.
- 2026-09-10 (task bank1, log_253, on the tower): THE DESIGN ERROR IN THE
  LOOP, NAMED AND COSTED, in the coordinator's own words of 2026-09-10.
  "The passes re-derived every emulation from the cell's term every time,
  so a renderer change made the same cell yield a different artifact, and
  the old proof no longer described what had just been built." Counted on
  the STRICT reading (every written place, flags included), proved (cell,
  target) pairs per pass were 330 / 434 / 465 / 521 / 504, their union
  523; 19 pairs proved by some pass are not proved by the last, five of
  them cells on all four through pass 4 and not in pass 5 (`and`, `cmp`
  x2, `mov`, `or`, all `imm_gpr` — exactly what pass 5 changed). Passes 2
  to 5 spent 75% to 98% of their runs re-doing known results, and every
  change cost a full pass, three guards, a report and a verifier before
  its effect was visible. "A proof is a certificate about ONE artifact —
  the term text, the rendered source, the compiler and its flags, the
  carved body, the verdict — and a certificate cannot regress; only the
  machinery can fail to reproduce it. The deliverable is the LIBRARY, one
  proved emulation per (cell, target), and it only grows." The library is
  `certificates.jsonl` (12,593 certificates over 4,117 keys) and the loop
  is `autopoly.py --bank`: delta plus a 5% audit. Its first pass measured
  the residual cost — 707 runs against a full pass's 1,265, 55.9% of the
  runs and 81.9% of the seconds — and its audit caught the same mechanism
  again, seven artifacts changed under a moved renderer, zero alarms.
  Verifier 20 claims, 0 differ.
- 2026-09-10 (task hub2, log_254, on the tower): HUB v2 — the dictionary at
  two levels, read from the bank (cell entries joined back to their run by
  sha256) and from o7/o11's proved pool-entry emulations (body level), with
  a PAIR level (setter+consumer, key = two cells) for comparisons. Over
  hub1's own 134 units every figure is equal (the regression guard). Over
  EVERY corpus go unit (590), which hub1 could not ask: c composes 325 /
  proves 290 (+32 under caller extension, 3 disproved with counterexamples
  kept), rust 276 / 260 (+13, 3), go 132 / 116 on re-pose — the body level
  gives c 215 composed / 184 proved and rust 152 / 140 on top of the cell
  level's 100 / 114. The handful: `f5` (uint64 shift, six cells in go's
  body) now PROVES on c from two body-level entries, and c's compiler
  lowered across the two calls to ONE clamp where go's own body has two.
  `f8` (compare feeding a select) resolves to its pair (`cmp gpr_gpr 32` +
  `setne gpr_one 8`) but the loop rendered `setne` over one setter only
  (`test gpr_gpr 8`): the design hole became one missing run. `f6` (div):
  its pool entry carries no layer-5 text. Dictionary per target: c 176
  cell / 39 pair / 195 body entries; rust 175 / 38 / 285; go 161 / 34 / 0.
  Loop-side changes it names (next closer): each flag consumer rendered
  over EVERY attested setter cell (44 distinct pairs in go's corpus; 10
  served today, 58 possible); the primitive lookup carrying holders; a
  narrow-answer re-pose in the gate. Note: `dictionary2.json` and the
  bank's `certificates.json` are held out of git by the repo-daemon's
  high-entropy guard (sha256 strings); the `.md` is in git and the json
  rebuilds in a second. Verifier 22 claims, 0 differ; peak 123 MB.
- 2026-09-10 (task ap6, log_255, on the tower; cut off once, resumed from
  disk): ONE VERSIONED DRIVER. Task-name gates in the driver 9 → 0 (75
  branches switched on a task label → 0; opcode-name branches: the one
  `ret` of the carver); the driver's and each renderer's sha256 recorded
  on every run and certificate; `handful_frozen.py` keeps the pre-strip
  driver so the closed passes still reproduce. The 100% re-derivation
  audit through the gate-free driver: 1,227 certified triples, 0 alarms.
  Flag consumers rendered over EVERY attested setter cell: distinct
  (consumer, setter) pairs 39 → 397, pair-level certificates 2,623 →
  7,519; the audit's matcher now keys on the setter (its first pass
  raised three false alarms by comparing `cmp gpr_mem 8` against `cmp
  gpr_gpr 8`, same term text, different arrival contract — the term text
  does not carry the contract, an owed record field). The lookup carries
  holders: hub1's five unusable entries matched at a real holder, 5 of 5.
  Re-attempts by code version. The three readings on all four: strict 94
  cells / 49.4%, destination-only 147 / 73.1%, corpus-needed 137 / 68.0%;
  all five now equals all four on every reading. Delta pass 2,499 runs /
  2,172 s — larger than a full pass because a consumer is now one run per
  posed setter; 1,053 newly certified. Owed: `hub.gate_two_bodies` passes
  no answer width (one argument); the sweep seeds no consumer row at the
  setter's width for 102 of hub2's 111 pair holes (`model_translate`).
  Verifier 30 claims, 0 differ.
- 2026-09-10 (task ref1, log_256, on the tower): LEVEL 0 CHECKED AGAINST AN
  INDEPENDENT READING — the K-framework x86-64 semantics (Strata's learned
  formulas, chip-tested; NCSA licence; read from `/sources`, never copied).
  A grammar over their ~30-function rule language → z3 per written place;
  their variant matched to our (mnem, shape, key_width) by the rule HEAD
  (the file names are in the opposite operand order); Intel's `undefMInt`
  made a free symbol and the undefined REGION computed. Of our 5,912
  triples (the table on `key_width`), 368 are reached by their reading:
  180 agree on every compared place (45,058 attested rows), 144 disagree
  on at least one (28,523 rows), 44 have nothing comparable (float and
  divide rules use functions the parser lacks). 1,779 places compared:
  760 agree, 383 disagree, 0 unknown at 3 s, 197 undefined, 439 refused.
  THE 383 DISAGREEMENTS REST ON FOUR LINES OF `reference.py`: (1)
  `full64` zero-extends EVERY sub-64-bit register write, while the
  hardware (and their reading) keeps the upper bits at 8 and 16 — 116
  places, 27 mnemonics, `setne gpr_one 8` alone attested by 10,335 rows;
  (2) `build_carry_binary` (adc/sbb) leaves the flags without the carry
  it read — 204 places, `sbb` 2,510 rows; (3) `condition_table.cond_to_z3`
  computes every condition on L−R, right for sub/cmp, wrong-shaped after
  `add`/`neg`; (4) `sub`/`sbb` are missing from `WIDTH_IS_NOT_A_SUFFIX`,
  so `sub %esi,(%rax)` is modelled at 8 bits — 12 places. Undefined
  regions per Intel: `AF` after and/or/xor/test; `AF OF PF SF` after bt;
  all six after div/idiv; `AF PF SF ZF` after imul/mul; the shifts'
  `OF`, and `CF OF` on the out-of-range count. Also: the model table on
  disk has 5,912 triples, not the 8,703 of log_236 (re-keyed by m1b), and
  ap5's symbolic-immediate spellings have no rows in it (never re-swept).
  Verifier 19 claims, 0 differ; 4.9 s, 64 MB. NOTHING DECIDED: the
  reference is the line's ground truth; its correction is the owner's ruling.
- 2026-09-10: task ref2 STARTED on the owner's word ("oh yeah, go"): the four corrections to `reference.py`/`condition_table.py`, each proved against the K reading, then the table, term store, pool and bank re-derived beside the old.
- 2026-09-10 (task t2, log_257, on the tower): THE SECOND TIER — construct
  what a target lacks from `& | ^ ~`, a conditional and variables over the
  target's widest word (128 on c/cpp/rust, 64 on go/swift), smallest width
  first; eight schemas general in (width, word); 199 schema obligations
  to z3, 0 disproved; 147 Lean theorems proved. Of 149 width/kind
  refusals over 51 cells: 24 places constructed, 14 PROVED — `adc`,
  `sbb`, `shld`, `shrd` at 64 on go and swift — every one discharged by
  the schema's lemma inside Lean's kernel (`lemma+gate` 14, `sat` 0,
  `canonical` 0 by construction: a constructed term never prints the
  wide operation's text). Bank 19,455 → 24,758 certificates; destination
  reading on all four 147 → 154 cells (73.1% → 75.2%), strict 94 → 96,
  corpus-needed 137 → 141. THE COMPILER COLLAPSED NONE OF THEM: LANDED 0
  of 14, bodies 4–17 instructions against the one the cell names (one
  swift `mul` collapsed but its equality is not discharged, so not
  banked) — against 31% of term-rendered emulations landing on their own
  opcode (ap6): the compiler's peepholes see ordinary arithmetic, not a
  composition equal to a primitive. What blocks the rest, each a named
  thing: (1) the x87 family, 129 of 149, refused at the ARRIVAL/ANSWER
  contract — an 80-bit value must arrive as integer words (a contract
  statement, in the spirit of the 2026-09-09 ruling); (2) the divider,
  the softfloats and every schema of that shape cannot be RENDERED: the
  renderers and `term_to_lean.py` print one nested expression with no
  named intermediate, so a step reading its previous step three times
  is written 3^width times — naming intermediates opens all of them at
  once; (3) the product's high half has no proof at any width (a miter of
  two multipliers; the algebraic statement is in `construct/lean/OWED.md`);
  (4) the tier's source is not part of `code_version`, which is why t2
  re-ran a full pass (669 runs) instead of a delta. Verifier 0 differ.
- 2026-09-10 (task rv1 started, Opus, on the tower beside ref2): RISC-V as
  a second architecture, an exploration not a pivot. The image now carries
  the rust riscv64gc target, Sail 0.20.2 and the sail-riscv C simulator
  `sail_riscv_sim` (Isla dropped: it builds only against Sail's unreleased
  master). rv1 = ten handful units compiled for riscv64 with clang and go,
  carved by llvm-objdump; level 0 for RV64IM in two readings (builders in
  `reference.py`'s shape; the ratified Sail model run concretely at edge
  and random points, ≤20,000 per instruction); the claim measured (x86
  term against RISC-V term by z3); the surface counted per layer. t3
  (renderer intermediates, x87 as two words, tier in code_version) waits
  for ref2's corrected terms.
- 2026-09-10 (task rv1 finished, Opus, on the tower): **the RISC-V
  exploration has its answer, and it is a number.** Level 0 for RISC-V is
  free and it agrees with our own reading: 44 instructions, 860,304 points,
  zero disagreements between `riscv_reference.py` and the ratified Sail
  model's simulator (a check at points, never an equality). Of the ten
  handful units compiled for riscv64, 7 of 10 terms are IDENTICAL to their
  x86 twin after `Term.normalize` and 3 differ on two causes — the two
  ABIs' narrow-argument extension rule, and x86's trapping division against
  RISC-V's total one. The per-architecture surface is 2,644 lines, 44% of it
  the lifter; the term, `Term.normalize`, the term store, the model table
  and the probe corpus all transferred unchanged, which is the measured form
  of the owner's hypothesis that the library is keyed by MAPPINGS and not by
  opcode names. A planning sub-node for the RISC-V line is wanted and is
  the owner's to create. Task rv2 (transfer by term identity, certificates
  re-verified on riscv64) is unblocked. Evidence:
  `PRIVATE/PseudoCoupHQ/DevComms/log_258_task_rv1_riscv_as_a_second_architecture.md`.
- 2026-09-10 (task rv1 closed, log_258): RISC-V handful. Ten cells' units
  compiled for riscv64 (clang, go) and carved: `add`→`c.add`, `imul`→
  `mulw`, `sar`→`sraw`, `idiv`→`divw`, `cmovne`→`czero.eqz`, `setne`→
  `xor; sltu`, `addss`→`fadd.s`, `cvtsi2sd`→`fcvt.d.w`. Level 0 for
  RV64IM in `riscv_reference.py` (44 mnemonics, 858 variants) against the
  ratified Sail model run concretely: 860,304 points, 0 disagree (A CHECK
  AT POINTS, NOT AN EQUALITY); 54 refused by name (loads/stores/branches
  19, float family 34, auipc 1). THE CLAIM: of 10, IDENTICAL after
  `Term.normalize` 7, DIFFER 3, no corpus unit 1 (the `sub` immediate cell:
  the probe corpus never puts a literal on an operand). The 3 differ for
  two named causes, both contract, neither meaning: (A) the ABI's narrow-
  argument rule — x86 reads 32 bits of an int32 argument where riscv64's
  ABI sign-extends to 64 (`setne`, `cmovne` units); (B) `idiv` traps on a
  zero divisor where `divw` defines the answer. THE SURFACE: 5 files,
  2,644 lines (2,174 code): lifter 1,174 (44% of everything), carve 291,
  convention 326, attestation 303, level-0 check 550. Transferred
  untouched: the term store, the model table, `Term.normalize`, the bank,
  the proofs. Flags: no riscv64 glibc headers in the image
  (`-nostdlibinc`); a planning sub-node for RISC-V is wanted (the owner's to
  create). Tally 7 MATCHES / 2 UNVERIFIABLE (prose) / 0 DIFFERS; guard
  PASS on all seven json. rv2 (the transfer by term identity) starts now,
  beside ref2.

- **2026-09-10 — task rv2 (arch_unit_oracle): the polyfill library's transfer
  to a second architecture, measured.** THE HYPOTHESIS, the owner's own words: *"if
  we already know what is proven in x86 ... it should also be true in RISC-V
  ... it should shrink the workload substantially."* MEASURED: of the 255
  RISC-V cells, **161 (63.1%) have an x86 cell that computes the same term at
  the operation's own width**, so the loop had to be run on only 94 (36.9%) —
  that is the shrinkage the hypothesis asked for. **Every certificate that
  compiled and walked was PROVED and none was disproved: 103 of them, plus 434
  interpreted certificates that transfer as they are.** What is smaller than
  the twin count is what ACTUALLY arrived: only 34 cells had a twin the bank
  holds a proof for, because the x86 loop has itself proved only part of its
  own table — a limit on the x86 side, not on the transfer. The three
  readings of the polyfill-complete set COINCIDE on RISC-V (74 cells) because
  the architecture has no flags register. Two contract differences, both
  findings and neither a meaning difference: a 32-bit result is sign-extended
  into a riscv64 register and zero-extended into an x86 one (20 of the 103
  proofs hold at the operation's width and not at the whole register), and
  x86's `idiv` traps where RISC-V's divides are total. Task ref2 is correcting
  `reference.py` in the same hours, so rv2 read the PRE-correction reference
  ref2 kept beside its work and reproduced the x86 table's own text on 8,403
  of 8,403 place rows; when ref2's corrected model table lands, `twins.json`
  must be re-run against it. Log 259; artifacts under
  `PRIVATE/PseudoCoupHQ/Research/oracle/riscv/`.
- 2026-09-10 (task rv2 closed, log_259): THE TRANSFER of the proved
  library to riscv64, measured. RISC-V's own model table has 255 cells
  with a written place. A cell has an x86 TWIN when the two terms are
  equal: 102 (40.0%) at the whole written place, 161 (63.1%) at the
  cell's own width — the gap is one architecture fact, RISC-V's 32-bit
  forms sign-extend into the whole register where x86's zero-extend.
  INHERITANCE: 734 x86 certificates whose cell has a twin were compiled
  for riscv64 and gated: 103 PROVED, 0 DISPROVED, 0 UNDECIDED (c 32, go
  71); 434 interpreted agreements transfer as they are; 197 refused for
  named installs (rust: no std for the freestanding target, 61; c: no
  riscv64 `string.h`, 15; cpp and swift not attempted). THE LOOP over
  the 94 untwinned cells: 188 runs, 135 proved, 82 distinct cells. All
  told 116 of 255 cells (45.5%) hold a proved riscv64 emulation. The
  three readings coincide on RISC-V (no flags register: one place per
  cell): 74 cells proved on both compiled targets. Side results: the
  corpus compiled for riscv64 refuses exactly the probes the x86 build
  refuses (0 disagreements); 31 riscv64 singletons attested. Flags: the
  run walked with the PRE-correction x86 reference (hash recorded;
  8,403 of 8,403 table rows reproduce under it) — twins re-run when
  ref2's table lands; clang 21 emits Zba/Zbb/Zbs (`c.zext.w add.uw c.mul
  bseti fsgnjn.d`, 27 rows) which the RISC-V lifter has no entry for;
  the 734 riscv64 certificates sit in `riscv/certificates_riscv64.jsonl`
  with `arch: riscv64`, not yet in the bank (ref2 was writing it). Tally
  7 match / 0 differ / 13 prose. FOR DEE: whether the Hub's dictionary
  key carries the arrival contract's extension rule (20 of 103 inherited
  proofs hold at the operation's width, not the whole register).
- 2026-09-10 (task rv3 PART DONE, log_260): the two rows of the RISC-V
  transfer that need nobody else. THE LIFTER's missing vocabulary was
  settled by EVIDENCE: every certificate source on a compiled target was
  built for riscv64 and carved (244 of 244, zero build refusals) and the
  mnemonics with no entry counted — `c.zext.w` 12, `add.uw` 8, `c.mul` 6 —
  with `bseti` and `fsgnjn.d` from rv2's own loop store, five in all, and
  not one row more than the bodies spell. Each was written in the
  reference's own shape and checked against the ratified Sail model at
  points before use: 5 rows, 68 variants, 99,968 points, 99,968 agree, 0
  disagree, so 0 defects. One finding on the way: the model REFUSED the
  float row until the harness switched the float unit on (`mstatus.FS` is
  Off at reset), which is the model being right, not the reference being
  wrong. THE INHERITANCE re-run with the image's new riscv64 standard
  libraries: 244 PROVED of 734 (was 103), 0 DISPROVED, 0 UNDECIDED, 56
  refused (was 197). Per target: c 58 (was 32 proved / 15 build-refused /
  11 walk-refused), cpp 54 (was not attempted), go 71, rust 61 (was 61
  build-refused), swift 56 not attempted — the image carries no `swiftc`
  at all, which is wider than "no riscv64 swift". Of the 244 proved at the
  cell's own width, 174 also hold at the whole register and 70 do not: the
  extension rule again. Cells reached by inheritance 35 (was 34); union
  with rv2's own loop 117 of 255, WITH ITS READING — rv2's loop ran under
  the pre-correction twins and the old lifter. Closed rv2's flags 2, 3, 4
  and 7. WAITS FOR ref2, whose DevComms log does not exist: twins against
  the corrected model table, the riscv64 certificates into the bank with
  `arch` (bank before: 24,758 records, every one with `arch` absent), and
  the loop on the new delta. FOR DEE: the extension-rule ruling, and
  whether swift stays out of the riscv64 column.
- 2026-09-10 (ruling, the owner; task t4 started, Opus, on the tower beside
  ref2): THE GENERAL CONSTRUCTION IS THE TOP PRIORITY. "it is meant to
  be capable of proving as a guarantee." What t2 built was eight
  schemas for the refused shapes, not the method; the method is one
  construction per OPERATION KIND (add, mul, div, rem, the shifts, the
  compares, extend/extract/concat, the float kinds as softfloat), general
  in width and word, proved once, composed over any term by a renderer
  that binds every node to a named variable, the native operator winning
  where it exists. Deliverable: every cell without a proof in a row with
  a named cause, on both architectures; the readings beside t2's and
  rv3's; the collapse column; where the gate runs out. t3 shrinks to the
  x87 arrival and the code version; rv3b follows.
- 2026-09-10 (task ref2 closed, log_261): LEVEL 0 CORRECTED. Four
  defects in `reference.py`/`condition_table.py`, each a hardware fact
  (a write below 32 bits leaves the register's other bits alone; adc/sbb
  add the carry INTO the destination and the flags read that sum; a
  condition is a reading of CF ZF SF OF PF as the setter's own builder
  computed them, not always a subtraction; `sub`/`sbb` in the no-suffix
  list so `sub %esi,(%rax)` is 32 bits). Before: the K-framework reading
  disagreed at 383 of 1,779 written places; after: NONE. Undefined 197
  and unstatable 439 unmoved (the corrections closed disagreements
  rather than hiding them). Lean model check 259/172/87/0 after each
  correction. Re-derived: the model table swept five times, 2,370 of
  14,534 places moved, attributed per correction, no attempt changed
  outcome; the term store re-printed beside the old (27,682 records,
  4,874 texts changed, 0 s-expression disagreements, 0 operand-order
  disagreements over 27,642 units); 200 canon40 proofs all hold. Flags:
  the bank's re-attempt rule hashes the driver/loop/renderer, NOT the
  reference (widened in-process; permanent = one line, t3 takes it); 184
  term-store records do not converge at 10,240 MB; the guard refused
  three json files (bare mnemonic lists) — right, fixed to `mnem` rows.
  Instance brought down by the coordinator; artifacts synced back.
- 2026-09-11 (task t4 closed, log_262, 18 h on the tower): THE GENERAL
  CONSTRUCTION TIER — one construction per operation kind (bitwise,
  complement, equality, conditional, wiring, add, multiply, divide,
  remainder, the float kinds as softfloat), general in width and word,
  composed over any term with every node bound to a name; the native
  operator first, the construction where none exists. MEASURED: 268
  places constructed, 246 PROVED — every one by the kind's own Lean
  lemma (proof by structure; z3 needed for none), 22 refused (go and
  swift where the arrival is wider than the 64-bit word). The proved
  kinds: bitwise, complement, equality, conditional and wiring at 8, 56
  and 64 bits on c, cpp and rust. THE EDGE, measured: multiply, divide,
  remainder and the float kinds at 16 bits and above CONSTRUCT but do not
  PROVE — Lean's bit-level decision times out at 16-bit multiply, z3 runs
  from 30 s to 3,000 s and answers by its 4 GB memory bound; the form
  actually used on those rows is NONE (196 construction instances: lemma
  132, sat 8, none 56). go's constructions over a 64-bit word run to
  19,299 instructions on average and were not gated (cap 4,000). THE
  PASS IS PARTIAL: 304 of 654 planned (cell, target) runs executed; the
  rest left behind by name in `t4_general_left_behind.json` after
  z3 out-of-memory aborts and one segfault. READINGS on x86 unchanged
  (96 / 154 / 141 of 205; +8 bank pairs); RISC-V 117 → 119 of 255 (`divw`,
  `remw` reached only by this tier). COLLAPSE: LANDED 27, LANDED_ELSEWHERE
  37, NOT_COLLAPSED 269 — the compiler folds a minority of constructions
  back to the instruction. OWED, in order: the general Lean lemma over
  every width (bv_decide decides at a fixed width only); an algebraic
  lemma for multiply/divide (the structure route, since bit-level
  deciders cannot); the delta pass over the 350 unreached places; the
  word-64 blow-up on go/swift. Guard 23/23 PASS; verifier 6 MATCHES / 0
  DIFFERS.
- 2026-09-12 (rv4, rv5; logs 263, 264): the owner's timed rounds on RISC-V.
  Optimization off made the check worse (cause not yet measured;
  log_263's stated cause retracted in log_264). Running the loop over
  EVERY RISC-V arch-opcode instead of the untwinned ones: 244 of 255
  proved (95.7%) in five minutes, from 117 — the population filter,
  not the method, was the gap. 12 remain, all divide / multiply-high /
  float subtraction / unsigned-to-float.
- 2026-09-12 (task cov1, log_266): THE REACH OF THE PROVED EMULATIONS.
  A unit of x is expressible in y when every arch-opcode it holds has a
  proved emulation on y. RISC-V: c→rust 369 of 369, go→rust 105 of 105,
  c→c 351 of 369, go→go 102 of 105; the only blockers are the divide
  and remainder family and `czero.eqz` on go. x86 (destination-only):
  c→c 4,578 of 10,367 (44%), c++→c++ 7,631 of 17,569 (43%), rust→rust
  489 of 685 (71%), go→go 153 of 577 (27%), swift→swift 237 of 1,229
  (19%); the blockers are the SAME handful in every pair — `cmp`
  (flags only, no destination), `test`, `push` (the stack), `movslq`
  (the widening move) — structural instructions, not arithmetic: a
  few cells hold thousands of units back. Strict reading lower again
  (`setne` and the flag pairs). Length view: units of 1–5 instructions
  mostly expressible; over 10, almost none (one blocker sinks a unit).
  Four x86 cells attested with no bank record (pcmpeqb/pcmpeqd/pmovmskb).
- 2026-09-12 (bb1, log_267): the bit-blast route — z3's own circuits,
  no authored arithmetic — proves 203 of 255 RISC-V arch-opcodes on go,
  202 on rust, 136 on c/c++ (the lifter lacks the bit-manipulation
  instructions clang writes for gate code). Three routes together: 251
  of 255 on at least one language, 235 on all four. The divide family
  compiles to 100k–250k instructions and is over the check's ceiling.
