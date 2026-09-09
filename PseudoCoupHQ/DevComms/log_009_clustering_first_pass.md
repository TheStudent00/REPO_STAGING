# log_009 — kind-clustering first pass: features, clustering, validation

Date: 2026-08-12. Author: clustering agent for the owner's PseudoCoup research node (PCHQ).
Inputs: `~/Programming/PseudoCoupHQ/Research/kind_signature_clustering/raw/` (five languages: rust, python, dart, c, cpp; kotlin deliberately excluded from this pass — it declares no roles/supertypes and will be evaluated against the validated clusters later, per §7).
Outputs on disk: `features.json`, `clusters.json`, `validation.txt`, all under `~/Programming/PseudoCoupHQ/Research/kind_signature_clustering/`.

Vocabulary: super-node / sub-node / co-node / sub-tree only; tree-sitter's JSON key `children` is quoted solely as its key name for what we call the sub-node spec.

## §1 Verdict

Partially — the known cross-language overlap re-emerges but with per-row strays: 1 of 15 ground-truth rows fully co-clustered, 14 of 15 partially (0 scattered), purity 0.685 over 73 ground-truth members; the strays are systematic (leaf kinds cluster by output-position profile, which is language-family-flavored) rather than random.

## §2 Pipeline

Three scripts under `~/Programming/PseudoCoupHQ/Research/kind_signature_clustering/`:

| script | consumes | emits |
|---|---|---|
| `features.py` | `raw/<lang>.node-types.json` × 5 | `features.json` — per (language, kind): flat weighted feature set + readable decomposition |
| `cluster.py` | `features.json` | `clusters.json` — 133 clusters over 800 kinds (primary config) + stability section |
| `validate.py` | `clusters.json` + built-in 15-row ground-truth table | `validation.txt` — per-row verdicts, over-merge list, purity |

Features per (language, kind), grammar-shipped data only (full documentation in the `features.py` module docstring): shared-role slot presence (11-role vocabulary from log_008 §4.3, non-shared roles bucketed as one boolean), per-slot arity flags (`multiple`/`required` verbatim), per-slot input-type sets abstracted to language-comparable signatures (concrete kind names collapsed to their derived output-type signatures; supertype references aliased; unnamed tokens bucketed as `tok`), declared plus derived output-type memberships (derivation is purely mechanical grammar inversion: a kind's output type is the set of positions — shared role, other-role bucket, or anonymous sub-node-spec position — that admit it, expanding supertype references recursively; declared supertype membership adds aliased `sup:` elements), is-leaf, has-sub-node-spec.

The distance function, stated in full: d(a, b) = 1 − Σ w(e) for e in Fa ∩ Fb ÷ Σ w(e) for e in Fa ∪ Fb — weighted Jaccard over the flat feature sets, with family weights: role presence 3.0, is-leaf 3.0, output-type elements 2.0, per-slot input-signature elements 1.0 (0.5 for the sub-node spec), arity flags 1.0, boolean buckets 1.0. Booleans participate as present-when-true elements, i.e. exact-match terms. Clustering is deterministic agglomerative (Lance-Williams), primary configuration average linkage cut at distance 0.40; seed-free by construction.

## §3 Validation results

Purity 0.685 (majority-row fraction over the 73 ground-truth members). Per row:

| ground-truth row | verdict | detail |
|---|---|---|
| binary_expression | partially | 4/5 in c016; strayed: dart:additive_expression→c006 |
| if_conditional | partially | 3/5 in c049; strayed: rust:if_expression→c048, python:if_statement→c118 |
| function_definition | partially | 2/5 in c057; strayed: dart:function_signature→c031, c:function_definition→c067, cpp:function_definition→c067 |
| call | fully | all 4 in c034 (dart has no single call kind; row is 4-language) |
| parameter_list | partially | 3/5 in c037; strayed: dart:formal_parameter_list→c053, c:parameter_list→c050 |
| identifier | partially | 2/5 in c003; strayed: dart:identifier→c014, c:identifier→c002, cpp:identifier→c002 |
| string_literal | partially | 2/5 in c003; strayed: dart:string_literal→c014, c:string_literal→c002, cpp:string_literal→c002 |
| number_literal | partially | 2/5 in c003; strayed: dart:decimal_integer_literal→c014, c:number_literal→c002, cpp:number_literal→c002 |
| assignment | partially | 3/5 in c016; strayed: python:assignment→c082, dart:assignment_expression→c080 |
| for_loop | partially | 2/5 in c012; strayed: rust:for_expression→c047, python:for_statement→c117, dart:for_statement→c036 |
| while_loop | partially | 3/5 in c012; strayed: rust:while_expression→c047, python:while_statement→c120 |
| return | partially | 2/5 in c008; strayed: rust:return_expression→c003, python:return_statement→c015, dart:return_statement→c022 |
| field_access | partially | 2/4 in c002; strayed: rust:field_expression→c041, python:attribute→c003 (dart is selector-based, no counterpart; row is 4-language) |
| block | partially | 3/5 in c008; strayed: rust:block→c002, python:block→c111 |
| argument_list | partially | 2/5 in c063; strayed: rust:arguments→c077, python:argument_list→c110, cpp:argument_list→c071 |

Converse (over-merging — clusters that mix ground-truth rows): c002 mixes identifier/string_literal/number_literal/field_access/block; c003 mixes identifier/string_literal/number_literal/return/field_access; c008 mixes return/block; c012 mixes for_loop/while_loop; c014 mixes identifier/string_literal/number_literal; c016 mixes binary_expression/assignment; c047 mixes for_loop/while_loop. Note that several of these "over-merges" are penalized by the purity score yet are arguably correct at a coarser grain (all-leaf-literals; loops-as-a-family; operator-shaped binaries) — the ground-truth rows are finer than what the features can separate for leaves.

## §4 Most interesting clusters beyond ground truth

Unexpected merges that look RIGHT:

- c048 = `['c:conditional_expression', 'cpp:conditional_expression', 'rust:if_expression']` — the optimizer put rust's expression-valued if with the C-family ternary, not with statement-if. That is semantically defensible (both are condition/consequence/alternative expressions) and was not asked for.
- c034 = `['c:call_expression', 'cpp:call_expression', 'cpp:new_expression', 'python:call', 'rust:call_expression']` — cpp `new_expression` joining the call cluster is right: it is an arguments-carrying invocation shape.
- c016 = `['c:assignment_expression', 'c:binary_expression', 'cpp:assignment_expression', 'cpp:binary_expression', 'cpp:fold_expression', 'python:binary_operator', 'python:boolean_operator', 'rust:assignment_expression', 'rust:binary_expression', 'rust:compound_assignment_expr']` — the full left/operator/right family, including cpp `fold_expression`, coheres across four languages.
- c012 = `['c:do_statement', 'c:for_statement', 'c:switch_statement', 'c:while_statement', 'cpp:do_statement', 'cpp:for_statement', 'cpp:switch_statement', 'cpp:while_statement', 'dart:do_statement', 'dart:switch_statement', 'dart:while_statement']` — a coherent "body-carrying control statement" family; switch joining the loops is a coarser but sensible grain.
- c057 = `['python:class_definition', 'python:function_definition', 'rust:function_item']` — name+body+parameters definitional shape.

Merges that look WRONG:

- c000 (67 members) and c001 (65 members) are grab-bags of kinds whose only feature is a sub-node spec with weakly informative inputs — e.g. c000 spans `c:type_qualifier`, `dart:library_import`, `python:decorator`, `rust:where_clause`. The sub-node-spec-only kinds (all of dart's fieldless majority lands here) do not carry enough shared signal at these weights.
- Leaf kinds split by language family instead of merging across it: c002 = c/cpp leaves-and-primaries (55 members incl. `c:identifier`, `cpp:string_literal`, plus intruder `rust:block`), c003 = python/rust equivalents (53 members), c014 = dart's (11 members incl. `dart:identifier`, `dart:true`). Cause: a leaf's vector is almost entirely its derived output-position profile, and position profiles are language-family-flavored (c/cpp share declarator positions; python/rust share pattern positions). This one cause explains the identifier, string_literal, number_literal, and field_access strays simultaneously.

## §5 Stability

Agglomerative clustering is seed-free, so stability was probed across the free parameters instead: pair-Jaccard (co-clustered pairs shared ÷ co-clustered pairs in either run) of the primary run (average linkage, threshold 0.40, 133 clusters) versus: average/0.35 → 0.846 (158 clusters); average/0.45 → 0.761 (103 clusters); complete/0.55 → 0.648 (109 clusters). Membership churn is thus moderate: roughly 15% of co-membership pairs move per 0.05 of threshold, and the linkage switch reshuffles a third — mostly inside the two grab-bag clusters (c000/c001), while the ground-truth-relevant small clusters are the stable part.

## §6 Honest limitations — numbered interpretation decisions

Every one of these is an interpretation the owner may re-rule; the rest of the pipeline is mechanical.

1. Supertype alias table: language-specific supertype spellings were manually mapped to shared names (`_expression`/`expression`/`primary_expression` → expression; `_compound_statement`/`_simple_statement`/`_declaration_statement`/`statement`/`_statement` → statement; `_literal`/`_literal_pattern` → literal; `_pattern`/`pattern` → pattern; `_type`/`type_specifier` → type; the four c/cpp declarator supertypes → declarator; `_declaration` → declaration; python `parameter` → parameter). Folding rust `_declaration_statement` and python's two statement supertypes into one "statement" is the strongest judgment call in the table.
2. Non-shared role names are bucketed into a single boolean (`has_other_roles`) and a single position tag (`pos:other_role`) rather than aligned pairwise (e.g. c/cpp `declarator` vs rust `pattern` are simply "other"). This discards real signal to avoid a second manual table.
3. Feature-family weights (role presence 3, is-leaf 3, output types 2, input signatures 1, sub-node-spec inputs 0.5, arity/booleans 1) are hand-set, not learned. The leaf-splitting failure in §4 is directly weight-sensitive.
4. Unnamed tokens in slot type lists are collapsed to the single bucket `tok`; operator tokens therefore carry no identity (a `+` slot equals a `<<` slot).
5. A slot's input abstraction takes the UNION of the admitted kinds' output signatures, losing multiplicity and co-occurrence structure inside the slot.
6. Derived output positions do not distinguish host kinds — appearing under `condition` of one kind equals appearing under `condition` of fifty kinds (set semantics, no counts).
7. Declared supertype membership is taken one level deep as shipped; derived positions expand supertype references in type lists recursively, so nesting is handled on the input side only.
8. Supertype entries themselves are excluded from the clusterable population (they are categories, not kinds).
9. Ground-truth row choices: dart is represented by `additive_expression` for the binary row and omitted from the call and field_access rows (its grammar is selector-based with no single call/access kind); python `block` stands in for suite. These choices move the purity number.
10. Primary cut threshold 0.40 and average linkage were chosen by inspection of cluster-size distribution, not by an objective criterion.
11. The 11-role shared vocabulary is inherited from log_008 §4.3 (roles in ≥5 of 6 grammars) rather than recomputed over the five-language subset.

## §7 Recommended next step for the kotlin evaluation

Kotlin has no roles and no supertypes, so its kinds carry only sub-node-spec features — exactly the population that lands in the c000/c001 grab-bags today. Before scoring kotlin, fix the leaf/sub-node-spec weakness: (a) enrich derived output positions with counts or host-kind output signatures (re-ruling decision 6), and (b) derive pseudo-supertypes for fieldless grammars by input-kind co-occurrence (kinds admitted by the same slots behave as one supertype — log_008 §7 already argued this is well-posed). Then score each kotlin kind by nearest-cluster medoid distance under the same weighted Jaccard, and validate against a hand list of ~10 known kotlin counterparts (`if_expression`, `call_expression`, `function_declaration`, ...): the pass criterion is that known counterparts land in the validated clusters of this log at distance comparable to the intra-cluster spread.
