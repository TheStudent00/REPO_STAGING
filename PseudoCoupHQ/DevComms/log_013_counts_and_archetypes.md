# log_013 — decision-6 counts fix (features v2) + archetype deduplication measurement over all 411 grammars

Date: 2026-08-12. Author: clustering agent for the owner's PseudoCoup research node (PCHQ). Plan-of-record step 2 of `CORE_0_3_0_kind_clustering.md`, plus the archetype measurement the owner asked for ahead of step 3.

Inputs: `~/Programming/PseudoCoupHQ/Research/kind_signature_clustering/` — `features.py` (modified, versioned v2 output), `spectrum.py` / `validate_holdout.py` (v2 flags added), `raw_all/` (411 fetched grammars, `grammar_inventory.json`). New outputs, same directory: `features_v2.json`, `features_v2_holdout.json`, `similarity_matrix_v2.npz`, `similarity_matrix_v2_holdout.npz`, `holdout_validation_v2.json`, `features_all.py`, `features_all.json`, `archetypes.json`, `compare_v2.py`.

Vocabulary: super-node / sub-node / co-node / sub-tree only; tree-sitter's JSON key `children` is quoted solely as its key name for what we call the sub-node spec.

## §1 Verdict

the owner's question — "is the cardinality of all potential vectors so great that we cannot simplify the pair-wise comparisons? ... I would imagine that 411 information sources would create a lot of identical vectors" — answered by measurement: yes, the shortcut is real and large. The 31,212 clusterable kinds of all 411 grammars collapse to 8,329 distinct counts-fixed feature vectors (archetypes), a 3.75x deduplication that shrinks the pairwise matrix from 487,078,866 pairs to 34,681,956 (14.0x fewer) — dense-over-archetypes survives scale comfortably (~132 MB condensed float32, minutes of compute), so the sparse top-k spectrum of plan step 3 is an option, not a necessity.

## §2 The counts fix (decision 6)

**What changed.** In v1, derived output positions were a SET: a kind "appears under `condition`" contributed one element whether 1 or 50 host kinds admit it there. In v2 (`features.py --v2`, writing `features_v2.json` / with `--hold-out-declared`, `features_v2_holdout.json`; v1 outputs untouched, so everything downstream of `features.json` is backward compatible), each derived position also carries the count of distinct host kinds admitting the kind under that tag.

**Sub-decisions ruled here** (documented in the `features.py` header):
- (a) counts are BUCKETED on a log2 scale (b0 = 1 host, b1 = 2-3, b2 = 4-7, b3 = 8-15, b4 = 16+), not raw — the weighted-Jaccard distance function of `cluster.py` is reused AS IS, so counts must be discretized to participate as set elements; log2 makes 1-vs-2 hosts a difference and 40-vs-50 not.
- (b) the presence element is KEPT alongside the new bucket element (`out:pos:<tag>` weight 2 + `out:pos:<tag>:xb<k>` weight 1): kinds admitted under the same role by very different host counts still share presence and differ on bucket — a graded separation, not a cliff, and it makes v1 features a strict subset of v2 features.
- (c) counts are DISTINCT HOST KINDS, not slots — a host admitting the same kind under the same tag in two slots counts once.
- (d) the input-signature abstraction stays presence-based — pushing buckets through `abstract_input()` would explode `in:*` cardinality and silently re-rule decision 5.

**Effect on the 1,271 identical-feature pairs** (log_010 §5's saturation count). Recomputed from features: v1 has 1,654 identical-feature cross-language pairs (383 c-cpp twins + 1,271 others). Under v2, 711 of the 1,271 split (560 remain identical), and 212 of the 383 c-cpp twins split too; total saturated cross-language pairs drop from 1,654 to 731. Log_010 §8's success criterion — "the saturated-pair count drops well below 1,654" — is met. The 560 survivors are genuinely indistinguishable under grammar-shipped data at current feature resolution (mostly single-position weak-sub-node-spec kinds whose admission counts also agree).

**Effect on hold-out AUC.** Re-running the full hold-out protocol on the v2 spectrum: mean AUC 0.712 -> 0.770 (median 0.665 -> 0.728), 22/29 groups >= 0.6 (was 21/29), mean within-supertype similarity 0.427 vs across 0.172 (was 0.411 vs 0.203) — the counts carry real signal, they don't just shuffle ties. Largest gains are exactly where log_010 diagnosed declaration-only membership: cpp `statement` 0.656 -> 0.993, c `expression` stays ~1 (0.997). The hand-picked secondary key dips 0.804 -> 0.775, consistent with its demoted, hand-chosen nature; the primary full-population validation improves.

**Do the log_010 §6 stable clusters survive?** Yes — 13 of the 14 checked wide-band member sets survive as EXACT maximal clusters in the v2 merge tree, most with wider bands than before (e.g. c/cpp `else_clause` 0.85 -> 0.52 narrower, but c/cpp preproc_if family 0.54 -> 0.50, comments-across-4-languages 0.42 -> 0.50, python:lambda + rust:closure_expression survives at width 0.15, c/cpp conditional_expression + rust:if_expression at width 0.24, the loop family at width 0.15, the body-list family at width 0.20). The single dissolution is the one log_010 already flagged as semantically suspect: s024 (c/cpp preproc kinds + python string-interpolation kinds + rust:qualified_type, glued by saturation degeneracy) is no longer an exact cluster — the counts split it, and the semantically clean c/cpp preproc-only 4-set emerges as its own maximal cluster over 0.00-0.47. That is the fix working as intended, not a regression.

## §3 Archetype measurement over all 411 grammars

Pipeline: `features_all.py` runs the UNCHANGED `features.build_features` (v2 counts on, declared memberships in) over every file in `raw_all/`, canonicalizes each kind's vector by a stable sha1 over its sorted element/weight JSON, and aggregates. All 411 grammars parsed, zero failures. Population accounting: 31,858 named entries (matches log_011's inventory exactly) − 646 supertype entries (excluded per decision 8: categories, not clusterable kinds) = **31,212 clusterable kinds**.

**Headline numbers:**

| measure | value |
|---|---|
| grammars processed | 411 (0 failures) |
| clusterable kinds | 31,212 |
| unique archetypes (distinct v2 vectors) | 8,329 |
| dedup ratio | 3.75x |
| singleton archetypes | 5,471 (65.7% of archetypes, 17.5% of kinds) |
| multi-member archetypes | 2,858 (covering 25,741 kinds, 82.5%) |
| top-20 archetypes cover | 11,784 kinds (37.8%) |
| pairwise matrix over kinds | 487,078,866 pairs |
| pairwise matrix over archetypes | 34,681,956 pairs (14.0x fewer) |

**Top 20 archetypes** (size, category spread, example members; full member lists in `archetypes.json`). The giants are exactly the weak-sub-node-spec shapes log_009/log_010 predicted would dominate at scale — now with count buckets separating them into distinct archetypes:

| rank | size | vector (readable) | categories | example members |
|---|---|---|---|---|
| 1 | 3,170 | leaf, one anon position, 1 host | gp 1155 / config 600 / dsl 408 / notation 402 / markup 364 / query 240 | abl:abstract, abl:alert_type, ... |
| 2 | 1,648 | anon slot (mult+req), self-positioned, 1 host | gp 663 / dsl 258 / config 229 / query 189 / notation 187 / markup 122 | ada:abort_statement, ada:accept_alternative, ... |
| 3 | 1,174 | leaf, one anon position, 2-3 hosts | gp 470 / config 202 / notation 172 / dsl 136 / markup 110 / query 84 | abl:abstract_modifier, abl:accum, ... |
| 4 | 911 | anon slot (req), self-positioned, 1 host | gp 270 / config 213 / notation 155 / dsl 150 / query 90 / markup 33 | abl:menu_element, ada:abortable_part, ... |
| 5 | 679 | anon slot (mult+req), self-positioned, 2-3 hosts | gp 266 / markup 106 / notation 89 / config 75 / query 72 / dsl 71 | ada:accept_statement, ada:component_declaration, ... |
| 6 | 473 | anon slot (mult), self-positioned, 1 host | gp 134 / notation 107 / config 90 / dsl 61 / markup 55 / query 26 | ada:exit_statement, ada:raise_statement, ... |
| 7 | 468 | leaf, one anon position, 4-7 hosts | gp 210 / config 66 / dsl 65 / markup 55 / notation 50 / query 22 | abl:all, abl:append, ... |
| 8 | 430 | leaf, one non-shared-role position, 1 host | gp 122 / markup 96 / dsl 77 / config 64 / notation 63 / query 8 | al:aggregate_function, al:content_keyword, ... |
| 9 | 371 | leaf, no derived position at all (comment-like) | gp 152 / dsl 71 / config 63 / notation 48 / markup 21 / query 16 | agda:comment, al:comment, al:pragma, ... |
| 10 | 325 | anon (mult+req) + 2-3-host anon position | gp 117 / notation 66 / config 50 / dsl 47 / query 26 / markup 19 | ada:aggregate, ada:array_type_definition, ... |
| 11 | 287 | (weak-spec variant) | gp 115 / config 56 / dsl 49 / notation 27 / query 24 / markup 16 | abl:asynchronous_phrase, abl:break_by, ... |
| 12 | 257 | (weak-spec variant) | gp 113 / markup 51 / dsl 31 / query 23 / notation 22 / config 17 | ada:declarative_part, ada:defining_identifier_list, ... |
| 13 | 229 | (weak-spec variant) | gp 85 / dsl 60 / config 36 / notation 27 / query 18 / markup 3 | apex:typeof_clause, bitbake:union_type, ... |
| 14 | 212 | (weak-spec variant) | config 69 / gp 68 / markup 33 / notation 22 / dsl 11 / query 9 | ada:sequence_of_statements, agda:data, ... |
| 15 | 212 | (weak-spec variant) | gp 71 / notation 42 / config 37 / markup 32 / dsl 25 / query 5 | ada:string_literal, ada:component_list, ... |
| 16 | 205 | (hoon-heavy single-grammar shape) | gp 205 | dafny:named_type, hoon:appendCell, ... |
| 17 | 195 | root-of-document shape | config 61 / notation 35 / dsl 31 / markup 28 / gp 27 / query 12 | agda:source_file, al:source_file, astro:document, ... |
| 18 | 195 | (weak-spec variant) | gp 75 / dsl 31 / notation 29 / markup 23 / config 24 / query 13 | ada:primary, ada:simple_return_statement, ... |
| 19 | 175 | leaf modifier shape | gp 86 / markup 32 / config 16 / query 15 / dsl 14 / notation 12 | abl:no_undo, ada:overriding_indicator, ... |
| 20 | 168 | gnu_asm-list family shape | gp 76 / dsl 50 / markup 16 / notation 13 / config 12 / query 1 | arduino:gnu_asm_clobber_list, ... |

Note rank 1 vs 3 vs 7: in v1 these three would have been ONE archetype (leaf + `pos:anon`); the count buckets split them by how many hosts admit them — the decision-6 fix visibly operating at scale.

**Per-category dedup ratio** (categories from `grammar_inventory.json`, provisional tags):

| category | kinds | archetypes | ratio |
|---|---|---|---|
| query | 1,548 | 320 | 4.84x |
| config | 3,434 | 847 | 4.05x |
| notation | 3,111 | 794 | 3.92x |
| markup | 2,635 | 830 | 3.17x |
| general-purpose | 15,444 | 5,391 | 2.86x |
| dsl | 5,032 | 1,766 | 2.85x |
| other | 8 | 7 | 1.14x |

(Per-category archetype counts overlap across categories, so they do not sum to 8,329.) The gradient is informative in itself: query and config grammars are structurally the most repetitive; general-purpose grammars carry the most distinct shape — consistent with role-richness driving vector diversity.

## §4 Dense vs sparse, grounded in the measured sizes

Recommendation: **run the step-3 spectrum DENSE over the 8,329 archetypes, carrying each archetype's member multiplicity as a weight; sparse top-k is demoted from necessity to optional presentation-layer optimization.** The numbers: the archetype condensed distance matrix is 34,681,956 float32 values ≈ 132 MB (vs 487,078,866 ≈ 1.86 GB over kinds, with the 3.9 GB square form of the latter marginal on ordinary hardware); the weighted-Jaccard computation over 34.7M pairs of small feature sets is minutes in vectorized form (the 800-kind matrix takes under a second; scaling ~108x in pairs with similar per-pair cost lands comfortably under an hour even unvectorized, and scipy average linkage on 8,329 observations is routine — seconds). Every kind inherits its archetype's row exactly (identical vectors have identical distances to everything), so nothing is approximated: dense-over-archetypes IS the full-population analysis, per the owner's no-sampling rule. Caveat carried: linkage must be multiplicity-aware (an archetype of 3,170 members is not one observation when averaging) — that is an implementation requirement for step 3, not a blocker. Sparse per-kind top-k counterpart lists remain the right SHAPE for reporting artifacts (best-counterparts at 31k kinds), just no longer for the matrix itself.

## §5 Carried interpretation decisions (update to log_010 §7)

- **Decision 6 (output positions are a set) — DISSOLVED** by this fix: positions carry log2-bucketed distinct-host counts in v2. It leaves behind four explicitly-ruled sub-decisions (§2 a-d), of which (a) bucket boundaries and (d) presence-based input signatures are new live interpretation decisions the owner may re-rule.
- **Decision 3 (feature-family weights)** — remains; the new `W_OUT_COUNT = 1` weight joins the inspectable knob set.
- **Decision 8 (supertype entries excluded)** — remains, and now has an exact population consequence at scale: 646 supertype entries excluded from 31,858 named entries.
- **Decision 11 (11-role vocabulary from log_008)** — remains and is now stretched furthest: the same 11 shared role names are applied to all 411 grammars, where "shared" was only ever established over the original survey languages. Flagged as the first candidate for re-derivation before step 3's basis report.
- Decisions 1, 2, 4, 5, 7 — remain unchanged.

Net: 8 remain (plus 2 new sub-decisions), 3 dissolved total (6, 9, 10).
