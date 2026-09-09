---
id: hq.research.progress
status: living
---

# PROGRESS — research

- 2026-08-12: node founded (the owner's ruling, PCv5 session — state
  record `~/Programming/PseudoCoup_v5/DevComms/log_020_session_state_2026_08_12.md`).
  `~/Programming/PseudoCoupHQ/Research/` created beside it.
- 2026-08-12: kind-signature-clustering landscape survey launched — fetch and
  compare `node-types.json` across rust, python, kotlin, dart, c,
  cpp; measure feature uniformity; report what clustering machinery
  would consume. done — report at
  `~/Programming/PseudoCoupHQ/DevComms/log_008_kind_clustering_landscape.md`
  (log_007 was already taken).
- 2026-08-12: kind-signature-clustering first pass built and validated — features.py /
  cluster.py / validate.py over five languages (kotlin held out); known
  overlap re-emerged partially (purity 0.685, 1 fully + 14 partially of 15
  ground-truth rows). Report at
  `~/Programming/PseudoCoupHQ/DevComms/log_009_clustering_first_pass.md`.
- 2026-08-12: kind-signature-clustering second pass per the owner's three rulings — merge-tree
  spectrum replaces the single cut (spectrum.py + similarity_matrix.npz,
  clusters as queries), full-population hold-out validation against
  tree-sitter's own supertype declarations (mean AUC 0.712 over 29 groups;
  hand key demoted to secondary check, AUC 0.804), cluster_by_language.md +
  best_counterparts.json over all 800 kinds. Interpretation decisions 9 and
  10 dissolved, 9 remain. Report at
  `~/Programming/PseudoCoupHQ/DevComms/log_010_clustering_spectrum.md`.

- 2026-08-12: dendrogram_explorer.html shipped (Research/kind_signature_clustering/): interactive icicle of the full merge tree, draggable threshold slice with live cluster count, entropy-colored cross-language merges, search+zoom. Export via export_tree.py -> merge_tree.json. See DevComms/log_012_dendrogram_explorer.md.
- 2026-08-12: kind-signature-clustering enumeration survey (plan-of-record step 1) —
  415 grammars enumerated (both orgs + wiki), 389 ship node-types.json,
  411 files fetched to `Research/kind_signature_clustering/raw_all/` with per-grammar
  quality signals and provisional category tags in
  `Research/kind_signature_clustering/grammar_inventory.json`; 31,858 named kinds total;
  25.3% of grammars are kotlin-like zero-role. Report at
  `~/Programming/PseudoCoupHQ/DevComms/log_011_grammar_enumeration.md`.
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
  Report at `~/Programming/PseudoCoupHQ/DevComms/log_013_counts_and_archetypes.md`.
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
  `~/Programming/PseudoCoupHQ/DevComms/log_014_ecosystem_spectrum.md`.
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
  `~/Programming/PseudoCoupHQ/DevComms/log_015_basis_report.md`.
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
  `~/Programming/PseudoCoupHQ/DevComms/log_024_layer3_python_fuzz.md`.

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
    `~/Programming/PseudoCoupHQ/Research/dominant_intentions/` were
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
    `bash ~/Programming/PseudoCoupHQ/hq.sh check` reports 0 errors,
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
    `~/Programming/PseudoCoupHQ/DevComms/log_039_census_foldback_and_log_rewrites.md`.
- 2026-09-05: sub-node `arch_unit_oracle` (node_0_3_8) founded by the owner
  as a parallel line — compilers as unit subjects, our own Hub-like
  compiler as oracle, cross-language construction of units. Isolated
  from compiler_graph by folder, instance prefix and node. Founding
  log `~/Programming/PseudoCoupHQ/DevComms/log_206_arch_unit_oracle_founding.md`. planned.
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
  Record: `~/Programming/PseudoCoupHQ/DevComms/log_212_research_restructure_and_master_plan.md`.
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
