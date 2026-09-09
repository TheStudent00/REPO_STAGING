# log_015 — the basis report: the ecosystem cluster structure faces the intentions vocabulary (plan-of-record step 4)

Date: 2026-08-12. Author: clustering agent for the owner's PseudoCoup research node (PCHQ). Plan-of-record step 4 of `CORE_0_3_0_kind_clustering.md`, on the full-ecosystem spectrum of log_014.

Inputs: `PseudoCoupHQ/Research/kind_signature_clustering/` — `spectrum_all.py` (`clusters_at` query API), `spectrum_all.npz`, `merge_tree_all.json`, `report_all.json`, `features_all.json`, `archetypes.json`, `grammar_inventory.json`. The vocabulary faced: `PseudoIR/Tools/intentions/pc_intentions.json` (`minimum_set`, 11 objects; `intent_categories` A–J; `t1_realizations`) with `minimum_intention_set.md` for definitions, plus the form tier ruled into `ur.KINDS` (`PseudoCoup_v5/Tools/ledgerer/ur.py`: type-form, declarative-form, proof-form). The hand-analysis this replaces: PCv5 `log_008_kinds_coarse_tagging_draft.md` (its five strain clusters and its empty buckets B/G/I, near-empty H).

New artifact: `basis_xref.py` / `basis_xref_out.json` (same directory) — the mechanical cross-reference; every claim below is reproducible from it.

Vocabulary rule: super-node / sub-node / co-node / sub-tree only.

## §1 Verdict

Yes — the ecosystem structure provides an empirical basis for `ur.kinds`, and what it says about the intentions vocabulary is: **confirmed at the core, needs additions at the edges, and needs one restructuring insight absorbed.** (V1) Every one of the 11 minimum-set objects except `service call` has a stable many-language cluster or coherent cluster family realizing it, with `choice` the single strongest case in the whole ecosystem (dedicated if/else/ternary clusters of 24–37 languages with the widest multi-archetype bands measured, carrying exactly the condition/consequence/alternative role structure); (V2) of the ten categories A–J, only D (pattern matching), F (generics) and J (metaprogramming) have clusters of their own — A, B, C-as-optionals, E, G, H and I are **shape-invisible ecosystem-wide**, precisely generalizing PCv5 log_008's rust-only finding: their keyword-bearing kinds exist by name in dozens of grammars but everywhere take the SHAPE of something else (an `await_expression` is shaped like a unary expression, an `interface_declaration` like a `class_declaration`, a `with_statement` like a `try_statement`, an `operator_declaration` like a `function_declaration`); (V3) the converse direction is the report's sharpest yield — at least six stable, wide, many-language families have NO good home in the vocabulary (import/include, error-handling clauses, the pair/case association shape, body/declaration-lists, document roots, control-transfer statements), and four of PCv5 log_008's five hand-diagnosed strains are corroborated by independent ecosystem-scale evidence while one (sum types) is refuted as a SHAPE claim; and (V4) the two ruled form-tier buckets are the best-confirmed entries of all (the comment/declarative shape is the single widest-band universal in the ecosystem, 265 languages), while proof-form finds no ecosystem cluster — consistent with its origin as rust's private apparatus. The vocabulary's 11 objects survive contact with 411 grammars; its categories are real intentions but mostly not grammar shapes; and the grammar shapes it lacks are now enumerated with language counts attached.

## §2 Method and the matching interpretation decisions

The cross-reference is mechanical: clusters are queries against the one merge tree (per the standing ruling), matched to buckets by two evidence channels kept separate so name-matching bias stays visible — (a) kind-NAME evidence: regex per bucket over member kind names; (b) STRUCTURAL evidence: the role/position features (`in:*`, `out:*`) of the matched clusters' archetype vectors, read from `features_all.json`. Every knob is listed:

1. **Reference threshold 0.40** for the primary partition (1,194 clusters), inherited from log_014 as a presentation slice, not a derivation. Because log_014 §4 showed the big semantic families form ABOVE 0.40 (else 0.63–0.83, pair/case 0.73–0.87, loop/try 0.755–0.864, declarations 0.775–0.877), three coarser query slices were added: t = 0.55, 0.68, 0.78. All four are queries of the same tree.
2. **Name patterns**: one regex per bucket (the exact patterns are in `basis_xref.py`, `PAT`). Examples: `choice` = `if|else|conditional|ternary|elif|elsif|unless`; `E dispatch` = `trait|interface|protocol|impl|implements|extends|virtual`. Each pattern is an interpretation; all are English-centric (see §8).
3. **Match criterion at t=0.40**: a cluster counts for a bucket if ≥5 members match, ≥40% of its kinds match, and it spans ≥5 languages. The 40% floor suppresses the giant shape-poverty clusters where every pattern matches a little.
4. **Keyword tracing for the sparse categories** (A, B, C, E, G, H, I, plus D/F/import/enum probes): at each coarse threshold, ALL kinds whose names match the category's keywords are located, and the clusters holding them are profiled (share of cluster, cluster width in languages, dominant co-member names). "No cluster of its own" means: at no threshold does any cluster reach even 15% composition from the category's keyword kinds, except where stated.
5. **Missing-vocabulary criterion**: clusters at t=0.40 with ≥10 languages, ≥20 kinds, and <50% of members matching ANY bucket pattern; then hand-glossed. The hand-glossing is interpretation; the candidate list is mechanical.
6. **Band computation**: per cluster, birth = merge height of its top internal merge, death = height of the merge dissolving it into a super-node — computed from the linkage matrix, matching log_014's convention.
7. **Coverage metrics for the 12 targets**: a kind is "covered" if its t=0.40 cluster spans ≥10 languages; "isolated-ish" if its cluster spans ≤2 languages. Both thresholds are choices.
8. **Confidence scale**: strong = dedicated many-language cluster(s) with BOTH name and role evidence; moderate = clusters exist but are narrow, c-family-propagated, or shared with another bucket; weak = trace evidence only; none = keyword kinds disperse into other buckets' shapes.
9. **Language identity**: multi-grammar repos count per grammar (`typescript__typescript` and `typescript__tsx` are distinct), inherited from the inventory. The 12 targets are matched to `python, typescript__typescript, java, c-sharp, go, rust, ruby, php__php, kotlin, cpp, dart, swift` — **all 12 are present in the inventory** (kotlin included).
10. **Category tags** (gp/config/dsl/…) are the enumeration agent's provisional tags, used descriptively only.

## §3 The bucket-by-bucket table

All 24 buckets: 11 minimum-set objects, categories A–J, 3 form buckets. "Langs" = languages of the best matched cluster(s); band as [birth, death).

| # | bucket | matched cluster(s) | langs | band (width) | category mix | name ev. | structural ev. | confidence |
|---|---|---|---|---|---|---|---|---|
| 1 | value | literal-leaf clusters (string/number/bool/null/char), 3 co-node clusters at t=0.40; identifier/literal leaf shape (log_014 row 10) | 24+23+16; 49 | 0.395–0.459 (~0.06 each) | gp-heavy + qry/cfg | 65–68% | leaves at literal/value positions of few hosts | **strong** |
| 2 | name | identifier cluster (75 kinds); bare-name leaf shape (log_014 row 5) | 61; 39 | 0.399–0.410; 0.286–0.430 (0.144) | gp + cfg/mk/dsl | 69–73% | leaf under name/identifier roles, many hosts | **strong** |
| 3 | operation | binary_expression cluster + unary_expression cluster; binary/assignment super-family (log_014 row 24) | 30+29; 130 | ~0.36–0.41; family 0.71–0.83 (0.123) | gp 254 / dsl 103 | 48–59% | in/out left+right+operator roles | **strong** |
| 4 | sequence | document-root cluster (source_file/program, 276 kinds; family log_014 row 29: 397 langs); body/declaration-list family (row 21) | 275; 82 | 0.397–0.422; 0.54–0.67 (0.132) | all categories | 47–79% | repeated-item container, no derived positions | **strong** (as container family) |
| 5 | choice | if_statement cluster; else_clause cluster; ternary/conditional cluster; THE ELSE FAMILY (log_014 row 14, 4 categories); if/preproc_if family | 24; 24; 34; 37; 67 | 0.372–0.537 (0.165); 0.342–0.492 (0.150); 0.370–0.458; 0.63–0.83 (0.193); 0.704–0.812 | gp+dsl+mk+cfg | 92–100% | **condition / consequence / alternative roles verbatim** | **strong — the strongest bucket in the ecosystem** |
| 6 | repetition | do/while/for cluster (80 kinds); break/continue cluster; loop/try super-family (107 langs) | 27; 20; 107 | 0.388–0.430; 0.26–0.41 (0.149); 0.755–0.864 | gp-heavy | 50–85% | condition + body roles | **strong** (super-family shared with error handling, see §5) |
| 7 | function | method/function-definition cluster; parameter-list family (log_014 rows 27/30); arguments clusters; declaration super-family (212 langs) | 30; 65; 25; 212 | 0.351–0.409; 0.58–0.70 (0.116); 0.389–0.449; 0.775–0.877 | gp 61 / dsl 22 | 78–100% | name + parameters + body roles | **strong** |
| 8 | record | field_declaration_list/struct-body cluster; field/property-identifier cluster; declaration family (shared) | 28; 17 | 0.331–0.423 (0.092); 0.301–0.418 | gp/dsl | 45–60% | field-list containers under body role | **moderate** — record declarations are NOT separable from class/interface/enum declarations (§5) |
| 9 | collection | argument/element-list clusters; body-list family (shared with 4 and 8) | 22–28 | 0.33–0.44 | gp/dsl/cfg | 41–56% | homogeneous repeated positions | **moderate** — the data sees "list of items", not "collection value" |
| 10 | mutation | assignment clusters (30 kinds; 24 kinds pure) | 18; 12 | 0.39–0.42; 0.278–0.412 (0.135) | gp/dsl | 47–100% | left + right roles, statement position | **moderate** — merges into the binary/assignment family at 0.71 (§5) |
| 11 | service call | gnu_asm operand cluster only (c-family propagation + lookalikes, log_014 row 3) | 16 (48 with lookalikes) | 0.393–0.487 | gp/dsl | 54% | asm clause roles | **weak** — extern/foreign kinds disperse |
| A | suspension | none. 96 keyword kinds (await/async/yield/generator) ecosystem-wide; max share of any cluster 4% — shaped as unary/parenthesized expressions and modifiers | — | — | — | 0 clusters | dispersal measured at t=0.55/0.68/0.78 | **none** (shape-invisible) |
| B | channels | none. 21 keyword kinds total (channel/select/send/go); disperse into statement and pair clusters | — | — | — | 0 | dispersal | **none** |
| C | optionals | none as optional-shape (51 nullable/optional kinds disperse into leaf/type clusters). But see §4 row M2: the try/catch/finally ERROR family clusters strongly and is the C-adjacent shape that actually exists | — | — | — | 0 | dispersal | **none** (as absence-in-types); error handling is real and homeless |
| D | pattern matching | switch/case clusters (30% purity, 27 langs; case_statement 14 langs); array/tuple-pattern cluster (13 langs, 100%); pair/case super-family (152 langs, shared) | 27; 14; 13; 152 | 0.372–0.485; family 0.73–0.87 (0.139) | gp 266 / dsl 101 | 30–100% | value + arm/pattern roles | **moderate** |
| E | dispatch | none of its own. interface/trait/protocol declarations sit INSIDE the general declaration family (co-nodes of class/function/enum declarations, 21–212 langs) | — | — | — | <2% of any cluster | shaped exactly as declarations | **none** as separate shape (§5) |
| F | generics | type_parameters/type_arguments clusters (156-lang and 200-lang containers, low purity); c-family template clusters (8–11 langs, 48–63%) | 156/200 (shared); 8–11 (pure) | 0.26–0.53 | gp-heavy | 19–63% | parameter-list shape over type-level items | **weak–moderate** — pure clusters are c-family propagation |
| G | scoped cleanup | none of its own. with/using/defer kinds cluster WITH try_statement (26-lang cluster, §4 row M2) — the data files G under error-handling shape | — | — | — | 15% max, inside try cluster | with_statement ≈ try_statement structurally | **none** as separate shape; confirms log_008 |
| H | events | none. 33 keyword kinds; event/delegate declarations shaped as function declarations (max 1% of any cluster) | — | — | — | 0 | dispersal | **none** |
| I | operator overloading | none. 7 keyword kinds in the whole ecosystem; operator declarations shaped as function declarations | — | — | — | 0 | dispersal | **none** — the least grammar-visible category, ecosystem-wide |
| J | metaprogramming | preproc_call/preproc_include cluster; preproc_params cluster; preproc_region archetype; include/import family (155 langs, shared with the homeless import shape, §4 M1) | 20; 21; 18; 155 | 0.333–0.473; one archetype 0.0–0.765 (0.765!) | gp + cfg + not | 42–54% | directive shapes, weak-spec phrase | **moderate** |
| T | type-form | primitive_type cluster; type_identifier cluster; type/type_descriptor container (139 langs at 0.55); raw-token/basic-type leaf (log_014 row 15) | 14; 12; 139; 36 | 0.34–0.46; 0.0–0.18 | gp + not | 46–90% | type-position leaves and phrases | **strong** |
| Df | declarative-form | THE comment archetype (log_014 row 1) — the widest band in the ecosystem; modifier/specifier leaf shapes (rows 6, 28: 74 and 213 langs) | 265; 74; 213 | 0.00–0.40 (**0.400**); 0.00–0.25; 0.43–0.55 | ALL categories | 84% | leaf, no derived position at all | **strong — best-confirmed bucket of all 24** |
| Pf | proof-form | none. lifetime/borrow/reference_type kinds disperse; rust's are among its isolated kinds (§6) | — | — | — | 0 | dispersal | **none** — ecosystem does not share rust's proof apparatus (expected) |

## §4 The missing-vocabulary table — stable many-language clusters with no good home

Candidates produced mechanically (decision 5), glossed by hand. The last column names the PCv5 log_008 strain each corroborates (strains: 1 import/namespace, 2 sum types, 3 borrowing, 4 error propagation, 5 structural containers).

| # | family | how wide / stable | what it is | log_008 strain corroborated |
|---|---|---|---|---|
| M1 | include/import/preproc-call family | 155 langs, 527 kinds, band 0.52–0.67 (0.143); import/use/require kinds join across categories | bringing names into scope — bindings to items, not values; `name`'s wording strains exactly as log_008 said | **strain 1 (import/namespace) — corroborated at 155-language scale** |
| M2 | error-handling clause family | try/catch/finally clusters: 26 langs at 41% purity (t=0.55); seh_except/finally + catch_clause cluster 22 langs; absorbed into the 107-language loop/try family at 0.755–0.864 | try/catch/finally/rescue/ensure as one clause shape; `with_statement`/`using` cluster INSIDE it | **strain 4 (error propagation) — corroborated; and it absorbs G** |
| M3 | pair/case association family | 152 langs, 501 kinds, band 0.73–0.87 (0.139); tight 63-lang core (pair, initializer_pair, pair_pattern, match_arm, label_pair) at 0.36–0.41 | "key associated with value" — one shape spanning dict pairs, switch cases, match arms, initializers; no bucket owns association | new — not among log_008's five (its `match_arm` sat comfortably in D; the ecosystem shows the shape is far bigger than D) |
| M4 | body/declaration-list family | 82 langs, 273 kinds, 0.54–0.67 (0.132); enum/interface/switch-body core 56 langs | structural containers holding position, not intention | **strain 5 (structural containers) — corroborated** |
| M5 | document-root family | 397 langs, 447 kinds, 0.56–0.67; single-archetype core 194 langs | the whole-file container | **strain 5 — corroborated** (log_008's `source_file` UNCERTAIN row) |
| M6 | control-transfer statement family | return/break/continue/goto/assert clusters, 22–68 langs (68-lang cluster at t=0.78) | non-local exit as one leaf-statement shape; split today across function (return) and repetition (break/continue), goto/assert homeless | adjacent to strain 4 (log_008 derived `exception` = "choice + early return through call layers") |
| M7 | operator-token family | 37 langs, 179 kinds, 0.45–0.61 (0.161) | operator spellings as classified leaves (assignment_operator, unary_operator, test_operator) | new — `operation` covers the expression, nothing covers the operator token |
| M8 | guard/constraint phrase family | 50–53 langs (type_constraint, guard, by_phrase, use_declaration lookalikes), log_014 row 4 | a constraining clause attached to a construct — E/F borderland with no bucket | partial: log_008's trait_bounds/where_clause DUAL rows |
| M9 | interpolation/format family | 121-lang cluster (interpolation, format_expression, format_specifier) | string interpolation — which the O6 verdict itself names "the ergonomic spelling" yet no bucket carries | new |
| M10 | the shape-poverty giants | 369-lang/5,035-kind and 398-lang/5,256-kind blobs at t=0.40 | universals of grammar-authoring convention (weak-spec phrases, single-position leaves), not of intention | none — evidence FOR the form tier: the vocabulary is rightly silent; ur.kinds needs forms to absorb them |

**The refuted strain: sum types (strain 2).** enum/variant/union kinds (329 by name) form NO cluster of their own at any threshold: enum bodies land in the body-list family, variants in field/variant clusters beside `field_declaration`, enum declarations in the declaration family beside structs. Ecosystem-wide, sum-ness is invisible to grammar shape — a sum type is SHAPED like a record. log_008's strain was real as a semantics gap, but the data says fixing it is a vocabulary decision, not something the grammars will decide. **Borrowing (strain 3)** likewise finds no ecosystem cluster (rust's reference/lifetime kinds are among its isolated ones) — consistent with the proof-form ruling rather than with a new intention bucket.

**The H/B/G/I question answered:** log_008 found events, channels, scoped cleanup and operator overloading syntax-invisible in rust. Ecosystem-wide at 411 grammars: B has 21 keyword kinds, H 33, I 7 — and none of the four ever composes more than 15% of any cluster (G's peak, inside the try cluster). The invisibility is not a rust quirk; it is the ecosystem's verdict. What log_008 predicted — "whatever fills those buckets has to come from the ledger's name resolution, not from ur_kind" — holds at full scale.

## §5 Granularity findings

Where the data disagrees with the vocabulary's grain:

**Over-fine (the data refuses to separate):**
- **E dispatch vs record vs function, at declaration level.** class/struct/interface/trait/protocol/enum/function declarations are ONE family (212 languages, band 0.775–0.877; already mixed in the 21-language cluster at t=0.55). Grammars agree a declaration is a declaration; what is declared is a name-resolution fact.
- **mutation vs operation.** `assignment` and `binary_expression` are one family at 0.71–0.83 (130 languages). The narrow assignment clusters exist below, so mutation is separable at fine grain — but the ecosystem treats "left op right" as one shape.
- **G vs error handling.** `with_statement`/`using` cluster inside the try/catch shape. If M2 becomes a bucket, G's grammar-visible remnant lives there.
- **choice vs J at the conditional.** The else family spans runtime else, preprocessor else, template else and config else (log_014 §5); the if/preproc_if family likewise. The alternative-arm shape does not respect the runtime/dev-time line the vocabulary draws between object 5 and category J.
- **D vs the pair shape.** match_arm/switch_case sit inside the 152-language pair/case family with dict pairs and initializers.

**Over-coarse (one bucket, several independently stable clusters):**
- **sequence** splits four ways: document-root (397 langs), body/declaration-lists (82), statement runs, control-transfer statements (M6) — each with its own band.
- **value** splits by hosting shape into stable literal-leaf clusters (string-ish / bool-null-ish / numeric-ish) that never merge below 0.4.
- **function** splits into definition / parameter-list / arguments / call clusters, each stable and many-language — the vocabulary's single object covers at least four distinct grammar shapes.
- **name** splits into general identifier leaves, bare-name leaves, and field/property identifiers.
Over-coarseness of this kind is benign for a coarse tier (the sub-clusters are sub-trees of one region) — listed for completeness; the over-fine cases are the ones that bite, because they make some ur_kind assignments undecidable from shape alone, exactly as log_008's DUAL flags anticipated.

## §6 The 12 target languages

All 12 have grammars in the inventory. Per language at t=0.40: fraction of kinds in ≥10-language clusters, fraction isolated-ish (cluster ≤2 languages):

| language | kinds | in ≥10-lang clusters | isolated-ish |
|---|---|---|---|
| cpp | 223 | 0.865 | 0.009 |
| swift | 72 | 0.847 | 0.028 |
| typescript | 176 | 0.710 | 0.000 |
| dart | 219 | 0.648 | 0.247 |
| kotlin | 114 | 0.640 | 0.123 |
| go | 107 | 0.579 | 0.103 |
| java | 142 | 0.563 | 0.035 |
| python | 122 | 0.525 | 0.008 |
| php | 157 | 0.510 | 0.287 |
| rust | 163 | 0.423 | 0.135 |
| c-sharp | 219 | 0.416 | 0.315 |
| ruby | 134 | 0.336 | 0.336 |

The basis covers the 12 well at the core and honestly at the edges. cpp/swift/typescript are near-fully embedded. dart and php isolate on their fine-grained expression ladders (dart spells `additive_expression`/`bitwise_and_expression`/… as separate kinds with idiosyncratic specs; php on its `include_expression`/`heredoc`/`encapsed_string` inventory). rust isolates on its proof apparatus and macro machinery (`reference_type`, `lifetime`-adjacent kinds, `token_repetition*`) — the proof-form ruling absorbs exactly these. c-sharp (0.315 isolated) and ruby (0.336) are the weak spots: c-sharp's rich pattern/declaration inventory (`*_pattern`, `accessor_declaration`, `conversion_operator_declaration`) and ruby's keywordless clause spellings (`if`, `elsif`, `else`, `method`, `block`, `do_block` — already the loneliest shapes in log_014 §6) carve sub-node specs no other grammar matches exactly. For those two, the per-kind `top_counterparts_all.json` evidence (nearest counterparts, not cluster membership) is the usable basis.

**Kotlin — the held-out zero-role case, finally evaluated.** Kotlin's grammar ships zero roles (25.3% of grammars share this, log_011), and at 5 languages it was uninterpretable. With the ecosystem as context, kotlin lands respectably: 114 clusterable kinds, 64.0% in ≥10-language clusters, only 12.3% isolated-ish — better coverage than java, python, rust or c-sharp. But the coverage is of a specific KIND: because kotlin's vectors carry no role features, its kinds overwhelmingly join the saturated weak-spec shapes — its largest memberships are the 369-language and 398-language shape-poverty giants (`class_body`, `function_body`, `when_expression`-adjacent containers, all the `*_modifier` leaves), the 283-language single-position leaf shape, and the 192/113-language container families. Where kotlin needs STRUCTURE to be matched, it isolates: its five type kinds (`nullable_type`, `non_nullable_type`, `function_type`, `user_type`, `parenthesized_type`) form a private 1-language cluster, `as/in/is_expression` a private trio, and `while_statement`/`when_entry`/`assignment` sit in ≤2-language clusters while every roled grammar's equivalents join the wide statement families. One genuine embedding: kotlin's `class_declaration`/`function_declaration`/`object_declaration`/`companion_object` join a real 15-language declaration cluster. Verdict: the basis covers kotlin's kinds, but by shape-poverty affinity rather than semantic structure — a zero-role grammar is classifiable by the ecosystem, and the classification says mostly "weak-spec container/leaf", which is true of the grammar, not of the language. For ur_kind mapping, kotlin will need the name evidence and `top_counterparts_all.json` more than the cluster partition.

## §7 What this recommends for ur.kinds — PROPOSALS for the owner

Naming and adoption are the owner's; these are proposals with evidence attached, superseding-by-addition in spirit.

- **P1 (adopt the core).** The 11 objects + the ruled form tier are empirically grounded; no change needed to value/name/operation/sequence/choice/repetition/function. `choice` and `declarative-form` are the two buckets the ecosystem confirms hardest.
- **P2 (an import/namespace bucket).** M1 is a 155-language family currently strained into `name`. The single best-evidenced addition.
- **P3 (an error-handling bucket).** M2: try/catch/finally as a first-class bucket; C stays "absence in types" (a semantics claim, not a shape); G's grammar-visible remnant files here.
- **P4 (an association/pair bucket, or an explicit ruling that D absorbs it).** M3 spans 152 languages; today its kinds would scatter across record/collection/D.
- **P5 (structural-container handling).** M4/M5/M6: either a `container-form` addition to the form tier, or a ruling that body-lists/roots take their content's bucket. log_008 question 5's answer at scale is: NONE damages the census, a form absorbs it cleanly.
- **P6 (record the shape-invisibility of A/B/C/E/G/H/I as a standing fact).** These categories stay in the vocabulary as intentions but should be documented as ledger-resolved, not grammar-resolved — log_008's claim, now ecosystem-verified. Their `ur_kind` realizations will be duals on function/declaration/statement shapes.
- **P7 (drop the sum-type strain as a kinds question).** The data refuses a sum-type shape; if PC wants sum types distinguished (C leans on it), that is a vocabulary/semantics decision to take with eyes open, not one the grammars will support.
- **P8 (interpolation).** M9 (121 languages) deserves at least a named home, given O6 already legislates interpolation as the canonical spelling.
- **P9 (per-language mapping strategy).** For roled grammars, map via cluster membership; for zero-role grammars (kotlin + 25.3% of the ecosystem) and the two outliers (ruby, c-sharp), map via nearest-counterpart evidence plus names. One strategy will not fit all 12.

## §8 Honest limits

- **Name-matching bias.** The regexes are mine, English-centric, and tuned once; a kind named in another convention (or another natural language) is invisible to channel (a). Channel (b) (roles) mitigates but role names themselves are English (decision 11 of the standing list — the 11-role vocabulary derived from the original survey languages — remains the highest-value re-ruling before these results are leaned on hard).
- **Category tags are provisional** (enumeration agent's, single pass; the owner may re-rule), and the gp/cfg mixes quoted inherit that.
- **The 40%-purity and ≥10-language thresholds** shape which clusters "count"; all four thresholds are queries and every table above is reproducible at other slices via `clusters_at`.
- **Shape ≠ semantics, both ways.** A category can be present and shape-invisible (§3 A–I); a shape can be wide and semantics-free (M10). The cross-reference measures grammar-authoring agreement, which is evidence about the vocabulary, not a verdict on it.
- **Kotlin's good coverage number is partly an artifact of zero-role saturation** (§6) — stated there, restated here because a bare 0.640 would mislead.
- **Multi-grammar languages** (typescript/tsx, php/php_only) inflate some language counts by 1–2; no conclusion above turns on it.

Sources: log_014 (§4 table, §5 else family, §6 isolated end), log_013, log_011, PCv5 log_008, `pc_intentions.json`, `minimum_intention_set.md`, `ur.py` KINDS, and `basis_xref_out.json` for every number not attributed to a prior log.
