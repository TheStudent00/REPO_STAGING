---
id: hq.research.progress
status: living
---

# PROGRESS — research

- 2026-08-12: node founded (the owner's ruling, PCv5 session — state
  record `<WORKSPACE_DIR>/PseudoCoup_v5/DevComms/log_020_session_state_2026_08_12.md`).
  `<WORKSPACE_DIR>/PseudoCoupHQ/Research/` created beside it.
- 2026-08-12: kind-signature-clustering landscape survey launched — fetch and
  compare `node-types.json` across rust, python, kotlin, dart, c,
  cpp; measure feature uniformity; report what clustering machinery
  would consume. done — report at
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_008_kind_clustering_landscape.md`
  (log_007 was already taken).
- 2026-08-12: kind-signature-clustering first pass built and validated — features.py /
  cluster.py / validate.py over five languages (kotlin held out); known
  overlap re-emerged partially (purity 0.685, 1 fully + 14 partially of 15
  ground-truth rows). Report at
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_009_clustering_first_pass.md`.
- 2026-08-12: kind-signature-clustering second pass per the owner's three rulings — merge-tree
  spectrum replaces the single cut (spectrum.py + similarity_matrix.npz,
  clusters as queries), full-population hold-out validation against
  tree-sitter's own supertype declarations (mean AUC 0.712 over 29 groups;
  hand key demoted to secondary check, AUC 0.804), cluster_by_language.md +
  best_counterparts.json over all 800 kinds. Interpretation decisions 9 and
  10 dissolved, 9 remain. Report at
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_010_clustering_spectrum.md`.

- 2026-08-12: dendrogram_explorer.html shipped (Research/kind_signature_clustering/): interactive icicle of the full merge tree, draggable threshold slice with live cluster count, entropy-colored cross-language merges, search+zoom. Export via export_tree.py -> merge_tree.json. See DevComms/log_012_dendrogram_explorer.md.
- 2026-08-12: kind-signature-clustering enumeration survey (plan-of-record step 1) —
  415 grammars enumerated (both orgs + wiki), 389 ship node-types.json,
  411 files fetched to `Research/kind_signature_clustering/raw_all/` with per-grammar
  quality signals and provisional category tags in
  `Research/kind_signature_clustering/grammar_inventory.json`; 31,858 named kinds total;
  25.3% of grammars are kotlin-like zero-role. Report at
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_011_grammar_enumeration.md`.
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
  Report at `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_013_counts_and_archetypes.md`.
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
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_014_ecosystem_spectrum.md`.
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
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_015_basis_report.md`.
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
  `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_024_layer3_python_fuzz.md`.

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
    `<WORKSPACE_DIR>/PseudoCoupHQ/Research/dominant_intentions/` were
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
    `bash <WORKSPACE_DIR>/PseudoCoupHQ/hq.sh check` reports 0 errors,
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
    `<WORKSPACE_DIR>/PseudoCoupHQ/DevComms/log_039_census_foldback_and_log_rewrites.md`.
