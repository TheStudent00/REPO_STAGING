# log_010 — kind-clustering second pass: the spectrum view, full-population hold-out validation, presentation artifacts

Date: 2026-08-12. Author: clustering agent for the owner's PseudoCoup research node (PCHQ). Second pass over the first-pass pipeline of `log_009`, implementing the owner's three rulings of 2026-08-12.

Inputs: `PRIVATE/PseudoCoupHQ/Research/kind_signature_clustering/` — `features.py` and the weighted-Jaccard distance function of `cluster.py` reused AS IS (the only change to `features.py` is an additive hold-out flag); five languages pooled (rust, python, dart, c, cpp; kotlin still excluded), 800 named kinds — the FULL population, none sampled.

New outputs on disk, all under `PRIVATE/PseudoCoupHQ/Research/kind_signature_clustering/`:

| file | what |
|---|---|
| `spectrum.py` | merge tree + pairwise merge heights + query API (`clusters_at(t)`, `stability_bands()`) |
| `similarity_matrix.npz` | full pairwise continuous similarity (319,600 pairs) + the merge tree itself |
| `similarity_matrix_holdout.npz` | same, from features rebuilt without declared supertype memberships |
| `features_holdout.json` | the hold-out feature build (`features.py --hold-out-declared`) |
| `validate_holdout.py`, `holdout_validation.json` | hold-out validation against tree-sitter's own declarations |
| `report_population.py` | whole-population reporting (rulings 2b, 3) |
| `best_counterparts.json` / `.md` | for EVERY kind, nearest counterpart in each other language + readable slice |
| `cluster_by_language.md` | clusters × languages table with cohesion and stability bands |
| `aggregates.json` | 5×5 pair means, top pairs, isolated kinds, band widths |

Vocabulary: super-node / sub-node / co-node / sub-tree only; tree-sitter's JSON key `children` is quoted solely as its key name for what we call the sub-node spec.

## §1 Verdict

Yes — held-out validation confirms the signal: with declared supertype memberships removed from the features, the similarity spectrum still recovers tree-sitter's own supertypes at mean AUC 0.712 over 29 (language, supertype) groups (21/29 ≥ 0.6; mean within-supertype similarity 0.411 vs 0.203 across), the hand-picked 15-row key (secondary check) separates from the cross-language background at AUC 0.804 (0.487 within-row vs 0.209 background), and the spectrum view shows exactly where the structure is strong: coherent families persist over threshold bands up to 0.85 wide, while the first pass's two grab-bag clusters exist only in 0.02- and 0.12-wide bands.

## §2 What changed from pass one, mapped to the three rulings

**Ruling 1 — defer the clustering decision.** The first pass asserted one slice (average linkage, threshold 0.40, 133 clusters). Now the agglomerative merge tree is the artifact: `spectrum.py` computes, for every one of the 319,600 pairs of kinds, the merge height at which the pair joins under average linkage over the unchanged first-pass distance function (imported from `cluster.py`, not reimplemented). Similarity is defined as 1 − merge height, which is exactly the pair's co-cluster fraction across the [0, 1] threshold spectrum. Storage is `.npz`, not `.json`: 319,600 labeled float pairs as JSON runs ~20 MB and loads slowly, while the `.npz` holds the condensed matrices in float32 (~2 MB) plus the merge tree (linkage matrix), from which any slice is reproducible; the small loader lives in `spectrum.py` itself (`load_spectrum()`). Clusters at any threshold are now QUERIES — `spectrum.clusters_at(t)` — and the query at the old threshold 0.40 reproduces the first-pass partition exactly (133 clusters), so nothing from pass one is lost, only its privileged status.

**Ruling 2 — full population, not 73.** The hand-picked 15-row / 73-member key is demoted to a clearly-labeled secondary check. Primary validation is now (a) hold-out against tree-sitter's own declarations over the full population (§3) and (b) whole-population best-counterpart reporting: `best_counterparts.json` covers all 800 kinds, each with its nearest counterpart in each of the four other languages and the similarity value (§5). For the hold-out, `features.py` gained the flag `--hold-out-declared` — declared memberships are entangled (the `out_sig` that carries them also feeds the input-signature abstraction), so a flag at the source is the only clean cut; a post-hoc filter on `out:sup:*` elements would have left declared memberships leaking through `in:*` features. Supertype references inside slot type lists are kept: they are input-side grammar structure, not membership assertions about the kind being featured.

**Ruling 3 — presentation artifacts.** `cluster_by_language.md` (rows = discovered clusters at the stated reference threshold 0.40, columns = the five languages, cells = member kind names, each row carrying internal cohesion and its stability band) — the analysis-side analogue of `roles_by_language.md`. And the similarity matrix as data (`similarity_matrix.npz`) plus readable aggregate slices: 5×5 language-pair means, top cross-language pairs, and the 10 most isolated kinds — reported, not hidden (§5).

## §3 Hold-out validation results

Protocol: rebuild features without declared supertype memberships, re-derive the merge-tree spectrum from them, then measure whether the resulting similarities separate within-supertype pairs from across-supertype pairs of the same language. AUC is the Mann-Whitney statistic: probability that a random within pair is more similar than a random across pair (0.5 = no signal). This is a reference frame, not an oracle (the owner's words) — tree-sitter does not know cross-language truths and its supertypes are per-language design choices — so these numbers are evidence of agreement, not a score that was maximized.

| language | supertype | n members | mean within | mean across | AUC |
|---|---|---|---|---|---|
| rust | `_declaration_statement` | 21 | 0.281 | 0.162 | 0.600 |
| rust | `_expression` | 39 | 0.472 | 0.170 | 0.886 |
| rust | `_literal` | 6 | 0.734 | 0.245 | 0.930 |
| rust | `_literal_pattern` | 7 | 0.679 | 0.242 | 0.920 |
| rust | `_pattern` | 16 | 0.338 | 0.228 | 0.626 |
| rust | `_type` | 17 | 0.296 | 0.221 | 0.591 |
| python | `_compound_statement` | 9 | 0.215 | 0.155 | 0.483 |
| python | `_simple_statement` | 16 | 0.287 | 0.223 | 0.516 |
| python | `expression` | 7 | 0.380 | 0.222 | 0.670 |
| python | `parameter` | 9 | 0.247 | 0.226 | 0.460 |
| python | `pattern` | 6 | 0.316 | 0.254 | 0.628 |
| python | `primary_expression` | 25 | 0.595 | 0.178 | 0.972 |
| dart | `_declaration` | 3 | 0.332 | 0.209 | 0.532 |
| dart | `_literal` | 10 | 0.687 | 0.239 | 0.929 |
| dart | `_statement` | 16 | 0.304 | 0.189 | 0.546 |
| c | `_abstract_declarator` | 4 | 0.538 | 0.221 | 0.904 |
| c | `_declarator` | 6 | 0.441 | 0.222 | 0.796 |
| c | `_field_declarator` | 6 | 0.431 | 0.217 | 0.739 |
| c | `_type_declarator` | 7 | 0.375 | 0.213 | 0.678 |
| c | `expression` | 26 | 0.534 | 0.148 | 0.995 |
| c | `statement` | 16 | 0.338 | 0.157 | 0.665 |
| c | `type_specifier` | 7 | 0.307 | 0.166 | 0.590 |
| cpp | `_abstract_declarator` | 5 | 0.551 | 0.237 | 0.891 |
| cpp | `_declarator` | 12 | 0.345 | 0.215 | 0.637 |
| cpp | `_field_declarator` | 9 | 0.369 | 0.220 | 0.638 |
| cpp | `_type_declarator` | 8 | 0.404 | 0.225 | 0.685 |
| cpp | `expression` | 39 | 0.498 | 0.149 | 0.910 |
| cpp | `statement` | 21 | 0.325 | 0.161 | 0.656 |
| cpp | `type_specifier` | 12 | 0.286 | 0.181 | 0.561 |

Summary: mean AUC 0.712, median 0.665; 21/29 groups at AUC ≥ 0.6; mean within 0.411 vs mean across 0.203. The pattern is informative: expression-family supertypes are recovered almost perfectly without their declarations (c `expression` 0.995, python `primary_expression` 0.972, rust `_literal` 0.930, cpp `expression` 0.910), while statement-family supertypes are recovered weakly (python `_compound_statement` 0.483, python `_simple_statement` 0.516, dart `_statement` 0.546) — statements are grouped by the grammars for syntactic-position reasons, not shared internal shape, so their membership genuinely lives in the declaration, whereas expression membership is redundantly encoded in structure. Only 2/29 groups sit below 0.5 (python `_compound_statement` 0.483, python `parameter` 0.460), i.e. essentially no anti-signal anywhere.

Secondary check, clearly labeled HAND-PICKED: the 15-row key of `validate.py`, scored against the hold-out spectrum — mean within-row similarity 0.487 vs background cross-language mean 0.209, AUC 0.804.

## §4 Clusters by language

Full table: `PRIVATE/PseudoCoupHQ/Research/kind_signature_clustering/cluster_by_language.md` — 88 non-singleton clusters at the reference threshold 0.40 (45 singletons omitted from the table, listed count only), each with cohesion (mean within-cluster raw weighted-Jaccard similarity) and stability band (the threshold range over which that exact member set is a maximal cluster in the merge tree). The 15 largest, inline (columns rust | python | dart | c | cpp):

| cluster | cohesion | band (width) | rust | python | dart | c | cpp |
|---|---|---|---|---|---|---|---|
| s000 (n=67) | 0.737 | 0.39–0.41 (0.02) | base_field_initializer, expression_statement, for_lifetimes, function_modifiers, where_clause | chevron, constrained_type, decorator, dictionary_splat, finally_clause, string_content, union_type, with_clause | 34 kinds incl. catch_clause, method_signature, type_alias, part_directive | alignas_qualifier, attribute_declaration, attribute_specifier, bitfield_clause, ms_based_modifier, ms_pointer_modifier, type_qualifier | 13 kinds incl. noexcept, trailing_return_type, throw_specifier |
| s001 (n=65) | 0.950 | 0.30–0.42 (0.12) | empty_statement, escape_sequence, mutable_specifier, shebang, string_content | break_statement, continue_statement, pass_statement, escape_sequence, +7 | 19 operator/builtin token kinds | character, escape_sequence, storage_class_specifier, +7 | 20 kinds incl. access_specifier, virtual_specifier, auto |
| s002 (n=55) | 0.730 | 0.40–0.46 (0.06) | block | unary_operator | — | 22 kinds incl. identifier, string_literal, number_literal, field_expression | 31 kinds incl. identifier, string_literal, lambda_expression, this |
| s003 (n=53) | 0.716 | 0.38–0.41 (0.03) | 28 kinds incl. identifier, integer_literal, string_literal, return_expression | 25 kinds incl. identifier, integer, string, conditional_expression | — | — | — |
| s004 (n=44) | 0.820 | 0.36–0.42 (0.06) | — | — | 37 kinds incl. argument, qualified, uri, function_body | ms_declspec_modifier | base_class_clause, field_initializer, friend_declaration, using_declaration, +2 |
| s005 (n=26) | 0.711 | 0.39–0.50 (0.11) | trait_bounds | class_pattern, type_parameter | function_type, interfaces, type_arguments | 9 declarator kinds | 11 declarator kinds |
| s007 (n=24) | 0.694 | 0.37–0.42 (0.05) | 12 kinds incl. tuple_pattern, type_parameters, use_list | 12 kinds incl. case_pattern, dotted_name, generic_type | — | — | — |
| s008 (n=17) | 0.708 | 0.36–0.43 (0.07) | — | — | assert_statement, block, local_function_declaration, local_variable_declaration | attributed_statement, compound_statement, expression_statement, labeled_statement, return_statement | + co_return_statement, co_yield_statement, throw_statement |
| s009 (n=16) | 0.780 | 0.39–0.59 (0.20) | declaration_list, enum_variant_list, field_declaration_list, field_initializer_list, match_block, ordered_field_declaration_list | — | class_body, enum_body, extension_body, switch_block | declaration_list, enumerator_list, field_declaration_list | declaration_list, enumerator_list, field_declaration_list |
| s010 (n=13) | 0.919 | 0.29–0.45 (0.17) | doc_comment, fragment_specifier, inner/outer_doc_comment_marker | type_conversion | — | preproc_arg, preproc_directive, statement_identifier, system_lib_string | same four as c |
| s011 (n=12) | 0.732 | 0.35–0.44 (0.09) | never_type, remaining_field_pattern, unit_type | — | type_identifier, void_type | field_identifier, ms_call_modifier, primitive_type, type_identifier | field_identifier, primitive_type, raw_string_delimiter |
| s013 (n=11) | 0.940 | 0.18–0.41 (0.22) | parameter, variadic_parameter | — | — | field_declaration, parameter_declaration, type_definition | + optional_parameter_declaration, variadic_parameter_declaration, template_instantiation |
| s012 (n=11) | 0.770 | 0.35–0.54 (0.19) | — | — | do_statement, switch_statement, while_statement | do_statement, for_statement, switch_statement, while_statement | same four as c |
| s015 (n=11) | 0.714 | 0.33–0.51 (0.18) | attribute_item, inner_attribute_item, use_declaration | assert_statement, decorated_definition, delete_statement, exec_statement, expression_statement, print_statement, raise_statement, return_statement | — | — | — |
| s018 (n=10) | 1.000 | 0.00–0.46 (0.46) | — | — | — | gnu_asm_* lists (4), subscript_range_designator | same five as c |

(Cells abbreviated here where a cluster has >10 members in one language; the linked file has every member name verbatim.)

## §5 Whole-population findings

**Per-language-pair mean similarity** (spectrum similarity = co-cluster fraction; diagonal = within-language pairs):

| mean sim | rust | python | dart | c | cpp |
|---|---|---|---|---|---|
| rust | 0.196 | 0.199 | 0.194 | 0.179 | 0.182 |
| python | 0.199 | 0.208 | 0.205 | 0.183 | 0.188 |
| dart | 0.194 | 0.205 | 0.252 | 0.191 | 0.199 |
| c | 0.179 | 0.183 | 0.191 | 0.187 | 0.191 |
| cpp | 0.182 | 0.188 | 0.199 | 0.191 | 0.191 |

The matrix is strikingly flat (0.179–0.208 off-diagonal): background similarity is language-agnostic, so the high-similarity pairs below sit far above a uniform floor. Dart's elevated diagonal (0.252) is its fieldless-majority self-similarity.

**Saturation**: 1,654 cross-language pairs sit at similarity ~1.0 (merge height 0). 383 are c↔cpp twins from near-identical shipped grammars; the remaining 1,271 are identical-featured weak-sub-node-spec kinds — the first pass's grab-bag phenomenon, now precisely quantified. The top-20-pairs list is therefore reported twice in `best_counterparts.md`: as-is (all saturated) and de-saturated. Highest non-saturated pairs: c:preproc_elif↔cpp:preproc_elif 0.981 and three more preproc pairs at 0.981, c↔cpp parenthesized_expression 0.980, conditional_expression 0.974, case_statement 0.971 — and the first non-c/cpp entries: python:parenthesized_expression↔rust:{async_block, gen_block, try_block, unsafe_block} at 0.957.

**Best-counterpart highlights** (every kind's row is in `best_counterparts.json`; similarity values are spectrum similarities): rust:function_item↔python:function_definition 0.640; python:call→rust:call_expression 0.733 and →c/cpp:call_expression 0.672; c:binary_expression→python:binary_operator and →rust:binary_expression both 0.665 (→cpp 1.0); dart:if_statement→c:if_statement 0.794; python:class_definition→rust:function_item 0.640 (the name+body+parameters definitional shape crossing the class/function boundary, as in pass one's c057); rust:match_expression→python:subscript 0.761 (a value+field shape collision — the features cannot see match arms as conditionals); python:lambda↔rust:closure_expression joined in a cluster stable over a 0.31-wide band.

**The 10 most isolated kinds** (best cross-language similarity anywhere — reported, not hidden):

| kind | best cross-language sim | best counterpart |
|---|---|---|
| dart:explicit_constructor_invocation | 0.016 | cpp:destructor_name |
| python:case_clause | 0.135 | dart:on_part |
| python:elif_clause | 0.135 | dart:on_part |
| python:if_statement | 0.135 | dart:on_part |
| rust:match_pattern | 0.154 | python:case_pattern |
| rust:let_declaration | 0.221 | dart:static_final_declaration |
| rust:attribute | 0.244 | dart:combinator |
| rust:let_chain | 0.281 | dart:type_test |
| rust:block_comment | 0.307 | dart:comment |
| rust:line_comment | 0.307 | dart:comment |

python:if_statement's isolation (0.135) retroactively explains its first-pass stray in the if_conditional row: its `alternative`-carrying elif-chain shape genuinely has no near counterpart under these features; that stray was a property of the data, not a clustering artifact.

## §6 Stability across the spectrum

A cluster's band [birth, death) is the threshold range over which its exact member set is a maximal cluster in the merge tree; band width is the strength of the assertion the data supports. The widest-band multi-language clusters — the assertions the data DOES support:

| rank | cluster | members | band (width) | cohesion |
|---|---|---|---|---|
| 1 | s066 | c:else_clause, cpp:else_clause | 0.00–0.85 (0.85) | 1.000 |
| 2 | s024 | c:preproc_call, c:preproc_include, cpp:preproc_call, cpp:preproc_include, python:format_expression, python:interpolation, rust:qualified_type (4 langs) | 0.00–0.62 (0.62) | 1.000 |
| 3 | s069 | c:linkage_specification, cpp:linkage_specification | 0.04–0.60 (0.55) | 0.957 |
| 4 | s043 | c:preproc_elif, c:preproc_if, cpp:preproc_elif, cpp:preproc_if | 0.15–0.69 (0.54) | 0.892 |
| 5 | s018 | c/cpp gnu_asm_{clobber,goto,input_operand,output_operand}_list + subscript_range_designator (10 kinds) | 0.00–0.46 (0.46) | 1.000 |
| 6 | s064 | c:case_statement, cpp:case_statement | 0.03–0.45 (0.42) | 0.971 |
| 7 | s070 | c:preproc_defined, cpp:preproc_defined | 0.00–0.42 (0.42) | 1.000 |
| 8 | s026 | c:comment, cpp:comment, dart:comment, dart:documentation_comment, python:comment, python:line_continuation (4 langs) | 0.00–0.42 (0.42) | 1.000 |
| 9 | s051 | c:parameter_list, c:preproc_params, cpp:preproc_params | 0.10–0.47 (0.38) | 0.937 |
| 10 | s065 | c:comma_expression, cpp:comma_expression | 0.11–0.48 (0.37) | 0.893 |

Caveat carried honestly: 7 of these 10 are c↔cpp pairs, i.e. stable because the two grammars are near-copies — true but unsurprising. The widest bands crossing language families are the interesting assertions: s024 (0.62 — though its cohesion-1.0 core is partly the saturation degeneracy: python's string-interpolation kinds and rust:qualified_type share an identical minimal feature shape with the preproc kinds, so this one is wide but semantically suspect), s026 comments across 4 languages (0.42, semantically right), python:lambda + rust:closure_expression (s084, 0.11–0.41, width 0.31), c/cpp:conditional_expression + rust:if_expression (s049, 0.33–0.62, width 0.29 — pass one's flagship unexpected-but-right merge survives as a wide-band cluster), the parameter/field declaration family s013 (0.18–0.41, width 0.22), the body-carrying container-list family s009 (0.39–0.59, width 0.20, 4 languages), and the do/while/for/switch family s012 (0.35–0.54, width 0.19, 3 languages).

At the other end: the grab-bags exist only in narrow bands — s000 (67 kinds, 5 languages) is a maximal cluster only over 0.39–0.41 (width 0.02), s003 (python/rust leaves, 53 kinds) only over 0.38–0.41 (width 0.03), s002 (c/cpp leaves, 55 kinds) over 0.40–0.46 (width 0.06), s001 over 0.30–0.42 (width 0.12). Exactly 1 multi-language cluster has width < 0.03 (s000). The first pass's headline number "133 clusters" was thus dominated by structures that exist essentially only at the threshold that was chosen; the spectrum view separates them from the wide-band families without asserting either away.

## §7 Remaining interpretation decisions

Of log_009 §6's eleven decisions:

**Dissolved:**
- **Decision 10** (threshold 0.40 / average linkage chosen by inspection) — dissolved by construction under ruling 1: the threshold is now a query parameter of `clusters_at(t)`; 0.40 survives only as a stated reference slice for the presentation table, and every cluster in that table carries the band over which it exists independent of the choice. (Linkage note: average linkage itself remains a choice, but it is now a property of one merge tree rather than of the asserted result; a complete-linkage tree can be built by the same code path if the owner wants a second spectrum.)
- **Decision 9** (hand-picked ground-truth row choices) — dissolved as a primary instrument under ruling 2: validation is now hold-out against declarations over the full population; the 15-row key persists only as a labeled secondary check, so its row choices no longer move any headline number.

**Remain (still-live interpretations the owner may re-rule):**
- **Decision 1** (supertype alias table) — remains, and is now doubly load-bearing: the hold-out drops declared memberships but keeps aliased supertype references in slot type lists, and §3's per-supertype rows are keyed by the raw per-language spellings.
- **Decision 2** (non-shared roles bucketed as one boolean) — remains.
- **Decision 3** (hand-set feature-family weights) — remains, and the saturation count of §5 (1,271 identical-featured weak-sub-node-spec pairs) is the sharpest measurement yet of what these weights cannot separate.
- **Decision 4** (`tok` bucket erases operator identity) — remains.
- **Decision 5** (union-of-signatures input abstraction) — remains.
- **Decision 6** (derived output positions are a set, no counts/hosts) — remains; still the designated first fix before kotlin (§8).
- **Decision 7** (declared memberships one level deep) — remains in the main pipeline; trivially moot inside the hold-out build, where declared memberships are absent altogether.
- **Decision 8** (supertype entries excluded from the population) — remains, with a new role: the excluded declarations are precisely the hold-out targets of §3.
- **Decision 11** (11-role vocabulary inherited from log_008, not recomputed for five languages) — remains.

Net: 9 remain, 2 dissolved (9 and 10), with decision 10 dissolved by construction exactly as ruled.

## §8 Kotlin evaluation plan

The hold-out run of §3 is, unplanned, a dress rehearsal for kotlin: it demonstrates that features WITHOUT any declared supertype memberships — which is kotlin's permanent condition, since its grammar declares no roles and no supertypes — still recover supertype structure at mean AUC 0.712. But the same run also localizes the risk: kotlin's kinds will carry only sub-node-spec features, the population that saturates (1,271 identical-featured cross pairs) and lands in the narrow-band grab-bags (s000, width 0.02).

Plan, in order:
1. Re-rule decision 6 first: enrich derived output positions with counts or host-kind output signatures, and derive pseudo-supertypes for fieldless grammars by slot co-occurrence (kinds admitted by the same slots behave as one supertype — log_008 §7). Success criterion, measurable before kotlin is touched: the saturated-pair count drops well below 1,654 and s000's band stays narrow or the cluster disperses.
2. Extend `spectrum.py` to score kotlin kinds against the existing merge tree: compute each kotlin kind's weighted-Jaccard distance to all 800 pooled kinds, then report its merge height into the tree (the height at which it would join its nearest sub-tree) — a spectrum-native replacement for the first pass's nearest-medoid plan, so kotlin also gets similarity values on the same [0, 1] scale, not one assigned cluster.
3. Validate two ways, mirroring this log: (a) whole-population — every kotlin kind gets a best-counterpart row appended to `best_counterparts.json`, isolation reported not hidden; (b) a ~10-kind hand list (`if_expression`, `call_expression`, `function_declaration`, ...) as the labeled secondary check only, pass criterion: known counterparts join the wide-band clusters of §6 at merge heights inside those clusters' bands.
