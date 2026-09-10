# log_014 — the full-ecosystem spectrum: multiplicity-weighted merge tree over all 411 grammars (plan-of-record step 3)

Date: 2026-08-12. Author: clustering agent for the owner's PseudoCoup research node (PCHQ). Plan-of-record step 3 of `CORE_0_3_0_kind_clustering.md`, on the archetype basis measured in log_013.

Inputs: `PRIVATE/PseudoCoupHQ/Research/kind_signature_clustering/` — `features_all.json` (counts-fixed v2 vectors for all 31,212 clusterable kinds of 411 grammars, vectors-once format), `archetypes.json` (8,329 archetypes with member lists), `grammar_inventory.json` (category tags), the v2 distance function of `cluster.py` reused exactly.

New outputs, same directory: `spectrum_all.py`, `spectrum_all.npz` (+`_holdout`), `dist_all.npy` (+`_holdout`, distance checkpoints), `merge_tree_all.json`, `top_counterparts_all.json`, `features_all_holdout.json` / `archetypes_holdout.json` (via the new `--hold-out-declared` flag on `features_all.py`), `validate_all.py` / `holdout_validation_all.json`, `report_all.py` / `report_all.json`, `export_tree_all.py`, `make_explorer_all.py` / `dendrogram_explorer_all.html`, `verify_explorer_all.js`.

Vocabulary: super-node / sub-node / co-node / sub-tree only; tree-sitter's JSON key `children` is quoted solely as a key name.

## §1 Verdict

Yes — robust many-language structure exists at full-ecosystem scale: at the reference threshold 0.40 the spectrum yields 1,194 clusters of which 156 span ≥ 10 languages and together cover 24,161 of 31,212 kinds (77.4%); hold-out validation over 565 (grammar, supertype) groups from 118 self-refereeing grammars gives mean AUC 0.766 / median 0.777 (up from 0.712/0.665 at 5 languages); and the isolated end is EMPTY — no kind of any of the 411 grammars is without a counterpart somewhere at similarity ≥ 0.400.

## §2 The run

**Population.** All 31,212 clusterable kinds enter via their 8,329 archetypes; dense condensed distance matrix of 34,681,956 float32 pairs. Nothing sampled: identical vectors have identical distances to everything, so the archetype matrix IS the full-population analysis (log_013 §4).

**Distance.** The v2 weighted-Jaccard of `cluster.py`, unchanged: d(a,b) = 1 − Σ_{e∈Fa∩Fb} w[e] / Σ_{e∈Fa∪Fb} w[e]. Vectorized as a sparse Gram product (valid because every element's weight is fixed by feature family — verified at load, and the vectorized distances are spot-checked against `cluster.distance_matrix` on 200 random pairs at every run).

**Multiplicity-aware average linkage (the log_013 caveat, discharged).** Each archetype enters weighted by its member count. Lance–Williams update with n_A = total member KINDS in cluster A (not archetype count):

    d(C, A ∪ B) = (n_A · d(C, A) + n_B · d(C, B)) / (n_A + n_B)

Because co-members of one archetype are at pairwise distance exactly 0 and at identical distance to everything else, this is exactly unweighted UPGMA over the full 31,212-kind population — the average of kind-pair distances between two clusters equals the multiplicity-weighted average of their archetype distances. Implemented as a nearest-neighbor-chain agglomeration (average linkage is reducible, so NN-chain is exact); merges re-sorted by height into a scipy-conformant linkage matrix, monotonicity asserted.

**Runtimes** (sandbox, 2 cores, ~3 GB RAM). Distance stage: 34.7M pairs in ~5 s (hold-out variant: 29.1M pairs in 3.7 s); weighted linkage 1.1 s; cophenetic merge heights 0.2 s; whole main pipeline 14.3 s; hold-out feature rebuild over all 411 grammars 1.5 s; hold-out spectrum 15.1 s; validation 1.4 s; structure report 0.9 s. The ~20-minute checkpoint discipline was armed but never needed — the condensed distance matrix is still checkpointed to `dist_all*.npy` on first computation, and a rerun resumes from it.

**Artifacts.** `spectrum_all.npz` (archetype labels, multiplicities, linkage matrix, raw + merge-height condensed matrices; loader and `clusters_at(t)` query API in `spectrum_all.py`), `merge_tree_all.json` (nested tree for the explorer), `top_counterparts_all.json` (per-archetype top-10 nearest counterpart archetypes with similarities, sizes, example members — the presentation slice at kind scale).

## §3 Validation at scale

Protocol of log_010 §3 over the whole ecosystem: features rebuilt with declared supertype memberships held out (`features_all.py --hold-out-declared`; the hold-out population dedups differently — 7,635 archetypes, 4.09x), spectrum re-derived, then every (grammar, declared supertype) group with ≥ 3 clusterable members scored by Mann-Whitney AUC of held-out within-supertype vs same-grammar across similarities. Reference frame, not oracle, as ruled.

**Overall: 565 groups over 118 grammars — mean AUC 0.766, median 0.777, 436/565 (77.2%) ≥ 0.6; mean within-supertype similarity 0.523 vs across 0.228.**

| category | groups | mean AUC | median AUC | ≥ 0.6 |
|---|---|---|---|---|
| general-purpose | 363 | 0.781 | 0.821 | 290 |
| notation | 42 | 0.762 | 0.768 | 32 |
| markup | 31 | 0.744 | 0.747 | 21 |
| query | 8 | 0.735 | 0.704 | 7 |
| dsl | 85 | 0.729 | 0.720 | 61 |
| config | 36 | 0.730 | 0.717 | 25 |

Every category clears 0.7 mean AUC — the signal is not a general-purpose privilege. The 5-language run's 29 groups sit inside these 565; the scale-up IMPROVED the mean (0.712 → 0.766), consistent with log_013's finding that the counts fix carries real signal and with denser cross-language evidence per shape.

## §4 The empirical-universals table

The widest-band clusters spanning ≥ 30 languages — sub-trees (or single archetypes) whose exact member set survives the longest threshold band. Band = [birth, death); cohesion = multiplicity-weighted mean pairwise raw similarity over member kinds (1.0 for a single archetype, whose members are feature-identical). This is the first sight of the empirical basis that will face the intentions vocabulary in step 4. Top 30 by band width:

| # | gloss | langs | kinds | archetypes | categories (top) | band (width) | cohesion |
|---|---|---|---|---|---|---|---|
| 1 | the comment/pragma shape — leaf, no derived position at all | 265 | 371 | 1 | gp 152 / cfg 63 / dsl 71 | 0.00–0.40 (0.400) | 1.000 |
| 2 | single-position weak-spec phrase shape (interpolations, clause modifiers) | 118 | 287 | 1 | gp 115 / cfg 56 / dsl 49 | 0.00–0.33 (0.333) | 1.000 |
| 3 | the gnu_asm-operand-list shape (c-family asm clauses + slice/headline lookalikes) | 48 | 168 | 1 | gp 76 / dsl 50 | 0.00–0.33 (0.333) | 1.000 |
| 4 | guard/constraint phrase shape (type_constraint, by_phrase, use_declaration) | 50 | 103 | 1 | gp 45 / not 26 | 0.00–0.33 (0.333) | 1.000 |
| 5 | bare-name leaf shape (command_name, sym_name, shorthand identifiers) | 30 | 46 | 1 | cfg 12 / mk 11 / dsl 11 | 0.00–0.29 (0.286) | 1.000 |
| 6 | leaf modifier/specifier shape (no_undo, overriding_indicator, break/continue) | 74 | 175 | 1 | gp 86 / mk 32 | 0.00–0.25 (0.250) | 1.000 |
| 7 | leaf under one non-shared role (regex_pattern, preproc_directive, keywords) | 128 | 430 | 1 | gp 122 / mk 96 / dsl 77 | 0.00–0.25 (0.250) | 1.000 |
| 8 | named-reference leaf shape (statement_identifier, system_handle, import) | 70 | 122 | 1 | gp 56 / dsl 24 | 0.00–0.25 (0.250) | 1.000 |
| 9 | THE giant: leaf admitted at one anonymous position of one host (escape_sequence, string_content, keywords) | 378 | 3,170 | 1 | gp 1155 / cfg 600 / dsl 408 | 0.00–0.25 (0.250) | 1.000 |
| 10 | identifier/literal leaf shape (identifier, null, number, string) | 49 | 146 | 1 | gp 78 / qry 42 | 0.00–0.25 (0.250) | 1.000 |
| 11 | leaf at one anonymous position, 2–3 hosts (escape_sequence, tag_name, integer) | 283 | 1,174 | 1 | gp 470 / cfg 202 / not 172 | 0.00–0.25 (0.250) | 1.000 |
| 12 | leaf at one anonymous position, 4–7 hosts (comment, identifier, access_specifier) | 167 | 468 | 1 | gp 210 / cfg 66 / dsl 65 | 0.00–0.25 (0.250) | 1.000 |
| 13 | keyword/date/currency literal leaf shape | 34 | 50 | 1 | gp 31 | 0.00–0.20 (0.200) | 1.000 |
| 14 | THE ELSE FAMILY — else_clause + preproc_else + template else across categories | 37 | 48 | 20 | gp 26 / dsl 12 / mk 4 / cfg 2 | 0.63–0.83 (0.193) | 0.557 |
| 15 | raw-token/basic-type leaf shape (raw_string_delimiter, basic_type) | 36 | 164 | 1 | not 101 / gp 21 / cfg 20 | 0.00–0.18 (0.182) | 1.000 |
| 16 | the document-root archetype (source_file, document, program — one shape) | 194 | 195 | 1 | cfg 61 / not 35 / mk 28 | 0.00–0.17 (0.167) | 1.000 |
| 17 | the operator-token family (assignment_operator, unary_operator, test_operator) | 37 | 179 | 16 | gp 131 / dsl 26 | 0.45–0.61 (0.161) | 0.692 |
| 18 | name/tag/anno identifier family | 39 | 60 | 5 | mk 16 / gp 15 / dsl 13 / cfg 13 | 0.29–0.43 (0.144) | 0.889 |
| 19 | the include/import/preproc-call family (+ interpolations, facts) | 155 | 527 | 22 | gp 201 / cfg 72 / not 66 | 0.52–0.67 (0.143) | 0.727 |
| 20 | the pair/case shape family (pair, switch_case, init_declarator, initializer_pair) | 152 | 501 | 261 | gp 266 / dsl 101 / mk 46 | 0.73–0.87 (0.139) | 0.427 |
| 21 | the body/declaration-list family (class_body, declaration_list, switch_body) | 82 | 273 | 106 | gp 157 / dsl 77 | 0.54–0.67 (0.132) | 0.611 |
| 22 | operator-token core (tighter band of #17) | 32 | 102 | 5 | gp 58 / dsl 26 | 0.32–0.45 (0.126) | 0.863 |
| 23 | root/attribute weak-leaf shape | 33 | 34 | 1 | gp 12 / not 8 | 0.00–0.13 (0.125) | 1.000 |
| 24 | the binary/assignment expression family (binary_expression, assignment, comma_expression) | 130 | 454 | 309 | gp 254 / dsl 103 / mk 38 | 0.71–0.83 (0.123) | 0.377 |
| 25 | the enum/interface/switch body core (sub-tree of #21) | 56 | 142 | 24 | gp 95 / dsl 30 | 0.30–0.42 (0.121) | 0.850 |
| 26 | literal/empty-statement leaf family | 42 | 75 | 8 | gp 42 / not 9 / qry 8 | 0.23–0.34 (0.117) | 0.826 |
| 27 | the parameter-list family (parameter_list, parameters, formal_parameters, preproc_params) | 65 | 100 | 49 | gp 61 / dsl 22 | 0.58–0.70 (0.116) | 0.540 |
| 28 | weak-leaf label/modifier super-family (super-node over several leaf shapes) | 213 | 1,087 | 62 | gp 410 / not 217 / dsl 172 | 0.43–0.55 (0.114) | 0.689 |
| 29 | the document-root FAMILY (#16's super-node: source_file/program/document/translation_unit) | 397 | 447 | 104 | gp 149 / cfg 95 / dsl 76 | 0.56–0.67 (0.113) | 0.647 |
| 30 | parameter-list super-family (super-node of #27, + lambda/template params) | 65 | 102 | 50 | gp 61 / dsl 24 | 0.70–0.81 (0.111) | 0.531 |

(Category keys: gp = general-purpose, cfg = config, mk = markup, not = notation, qry = query.)

Just below the cut, and worth naming because step 4 will want them: **the loop/try/catch statement family** (while/for/do/try/catch/switch — 107 languages, 637 kinds, band 0.755–0.864, width 0.109), **the whole-leaf half of the ecosystem** (410 languages, 7,525 kinds joining as one sub-tree over 0.67–0.78), **the if/preproc_if/while conditional family** (67 languages, 165 kinds, band 0.704–0.812), and **the declaration/definition family** (function/class/enum/interface declarations — 212 languages, 2,020 kinds, band 0.775–0.877).

Reading the table honestly: rows 1–13, 15–16, 23 are single archetypes — the saturated weak-sub-node-spec shapes log_013's top-20 already named, now with their band widths measured; they are real universals of grammar-authoring convention (every language has a comment shape, a document root, escape-sequence leaves), but they are universals of SHAPE-POVERTY. The multi-archetype rows (14, 17–22, 24–30 and the four below the cut) are the semantically structured universals: else, operators, include/import, pair/case, body-lists, binary/assignment expressions, parameter lists, document roots, loops, conditionals, declarations. That reads like a first draft of a meta-language table of contents, derived from nothing but grammar-shipped structure.

## §5 Category-spanning findings

Per the owner's ruling: everything in, tagged, reported per category — and the question is which clusters cross the category lines. At the reference threshold 0.40 (1,194 clusters; 901 with > 1 kind, of which 646 cross languages and **473 — 52.5% — span categories**):

| category | kinds | merges cross-language within-category | sits in a category-spanning cluster |
|---|---|---|---|
| general-purpose | 15,444 | 13,921 (90.1%) | 12,866 (83.3%) |
| config | 3,434 | 3,145 (91.6%) | 3,313 (96.5%) |
| dsl | 5,032 | 4,337 (86.2%) | 4,691 (93.2%) |
| notation | 3,111 | 2,710 (87.1%) | 2,953 (94.9%) |
| markup | 2,635 | 2,217 (84.1%) | 2,524 (95.8%) |
| query | 1,548 | 1,375 (88.8%) | 1,456 (94.1%) |
| other | 8 | 0 | 8 (100.0%) |

Every category is majority-absorbed into category-spanning clusters; config is the MOST absorbed (96.5%) and general-purpose the least (83.3%) — general-purpose grammars are the only ones rich enough to sustain clusters of their own, while config/markup/query kinds overwhelmingly land in shared shapes. The categories do not partition the spectrum; they dissolve into it.

**The single most striking category-spanning finding is the else family (row 14 of §4):** one 37-language cluster, stable over the 0.19-wide band [0.63, 0.83), containing runtime `else_clause` from rust, c, cpp, arduino, sway, move, cairo, tact and qmljs; PREPROCESSOR `preproc_else` from c, cpp, fortran, glsl, cuda, hlsl and objc; template-language else from angular, smarty (`foreach_else`) and glimmer; and — the finding — config-grammar conditionals: `else_directive` from xresources (X11 resource files) and `preproc_else` from devicetree. The grammars agree, across four categories and with no access to each other, that "the alternative arm of a conditional" is one shape whether it lives in a systems language, a shader preprocessor, an HTML template, or an X11 config file. That is exactly the kind of empirical universal the intentions vocabulary must have a bucket for.

## §6 The isolated end

There is none — the sharpest single change from the 5-language run. Minimum nearest-counterpart similarity over all 8,329 archetypes is **0.400**; zero archetypes (zero kinds) sit below nearest-sim 0.4, only 17 archetypes / 46 kinds below 0.5, and no archetype anywhere shares no feature with everything else. At 5 languages the most isolated kind sat at 0.016 (dart:explicit_constructor_invocation); at 411 grammars everything has a neighbor. The loneliest shapes, reported not hidden: `typst:incomplete_return_expression` (0.400), make's `ifdef/ifeq/ifndef_directive` group (0.400), c-sharp's `preproc_region`/`preproc_endregion` + `dot:source_file` (0.400), `haskell:alternatives` (0.435), `just:if_expression` (0.439), `perl:else_clause` (0.444), `kcl:if_stmt` (0.450), rust/sway `let_declaration` (0.451), `jq:query` (0.465), ruby `block`/`do_block` (0.474). Even the "isolated" end is family-adjacent: it is mostly conditionals and declarations whose grammars carve unusual sub-node specs, not alien shapes.

## §7 Stability bands at scale vs the 5-language run

Do the log_010 §6 / log_013 §2 stable clusters reappear inside the big tree? Yes — every checked set survives, and each is now EMBEDDED in a many-language cluster rather than standing alone:

| old stable set | joins the big tree at | its containing cluster now |
|---|---|---|
| c/cpp `else_clause` | 0.000 (same archetype) | 19 kinds / 19 languages, band [0.00, 0.34) |
| c/cpp preproc_if family | 0.239 | 22 kinds / 12 languages, band [0.24, 0.31) |
| comments across 4 languages | 0.000 (same archetype) | THE comment archetype: 371 kinds / 265 languages, band [0.00, 0.40) |
| python:lambda + rust:closure_expression | 0.414 | 22 kinds / 19 languages, band [0.41, 0.45) |
| c/cpp conditional_expression + rust:if_expression | 0.592 | 72 kinds / 63 languages, band [0.59, 0.66) |
| loop family (do/while/for/switch, c/cpp/dart) | 0.430 | 99 kinds / 28 languages, band [0.43, 0.46) |
| body/list family (declaration_list, class_body, …) | 0.535 | 273 kinds / 82 languages, band [0.54, 0.67) |
| c/cpp `case_statement` | 0.113 | 10 kinds / 10 languages, band [0.11, 0.39) |

The pattern is uniform: the old 2–11-member assertions were previews of ecosystem-wide families ("else across c and cpp" was really "else across 19–37 languages"; "body-lists across 4 languages" was really 82). Exact-set maximality is mostly gone — at 411 grammars other languages' kinds share the very same archetypes — which is the scale-up working, not eroding: the assertion got stronger and wider, not lost.

## §8 Interpretation-decision update

Carried from log_013 §5 (8 remained + 2 sub-decisions). Step 3 changes:

- **NEW ruled decision: multiplicity-aware average linkage** — the §2 Lance–Williams formula with kind-count weights. Not a free knob so much as the unique choice that makes archetype-level agglomeration exactly equal full-population UPGMA; documented in `spectrum_all.py`, alternatives (complete linkage; archetype-count weights) available by the same code path if the owner wants a second spectrum.
- **Presentation parameters, explicitly NOT interpretation**: reference threshold 0.40 (a query, per ruling 1), the ≥ 30-language / ≥ 0.10-width cutoffs of §4's table, and top-k = 10 in `top_counterparts_all.json` — all are slices of the one merge tree; nothing downstream is derived from them.
- **Decision 11 (11-role vocabulary from the original survey languages)** — still the first candidate for re-derivation, and now measurably load-bearing: the shared-role features carried by all 411 grammars are keyed to role names established over a handful of languages. Before step 4 cross-references intentions, re-deriving the shared-role set over all 411 grammars is the highest-value re-ruling available.
- All others (1, 2, 3, 4, 5, 7, 8, sub-decisions a/d) remain unchanged. Net: 9 ruled decisions remain live (plus 2 sub-decisions), 3 dissolved historically.

## §9 Step-4 readiness

Step 4 (the basis report: widest-band many-language clusters cross-referenced against the 11 minimum-set objects and categories A–J) can start immediately. Its inputs exist: §4's table (with `report_all.json` carrying the full member lists per cluster, not just the top 30), `top_counterparts_all.json` for per-kind evidence, and `clusters_at(t)` for any alternative slice. The shape of the step-4 question is now sharp: the multi-archetype universals (else, operators, include/import, pair/case, body-lists, expressions, parameter-lists, roots, loops, conditionals, declarations) each need an intention bucket or are evidence of missing vocabulary — and the single-archetype universals (comments, escape sequences, document roots as one shape) test whether the intentions vocabulary distinguishes semantic role from grammar-authoring convention. Not done here, per the tasking.

## Explorer note

`dendrogram_explorer_all.html` (self-contained, D3 from cdnjs, tree inline, 1.6 MB) is the scale adaptation of log_012's explorer: 8,329 archetype leaves instead of 800 kind leaves, leaves colored by CATEGORY (7-color legend; 411 languages cannot be a legend), joined segments colored by category-mix entropy, hover shows archetype hash, multiplicity, category mix and a capped `language:kind` member list, search matches against member labels. The feedback-round-1 threshold-highlight feature is kept (yellow outlines = exact clusters of the partition at the dragged line, with the count-match console assertion). Scale handling: deeper culling (0.6 px vs 0.35), default threshold 0.6 (573 clusters) so the initial view is calm, zoom ceiling raised to 2000x. Verified headlessly (jsdom + d3, `verify_explorer_all.js`): cluster counts at t = 0.3 / 0.5 / 0.7 are 2,278 / 573 / 66, exactly matching `spectrum_all.clusters_at`, zero highlight-mismatch warnings, 7 legend entries. Real-browser interaction still unverified, as before.
