# log 021 — the rust kind-map proposal: pack-generator output (P-a, the q1 instrument)

Date: 2026-08-13. Author: clustering agent, for the owner's review. This is the PCv5-side landing of PCHQ research step P-a (PCHQ log_016 §6): the pack generator now exists, rust ran first, and this log carries its full output — the instrument that turns q1 (ratify the ts_kind → ur_kind map; log_017 open questions) from 163 raw judgments into “review the evidence, rule the residue.”

Artifacts (all under `~/Programming/PseudoCoupHQ/Research/kind_signature_clustering/`, all re-derivable):

- `pack_generator.py` — the generator, language-agnostic (`python3 pack_generator.py rust`)
- `proposed_kind_map_rust.json` — machine-readable rows (kind, proposed, confidence, evidence, intention_note, residue flag)
- `proposed_kind_map_rust.md` — the same table for human eyes
- `compare_rust_hand.py` / `comparison_rust_hand.json` — the diff against PCv5 log_008's hand draft

The hand draft (log_008) was used ONLY as a comparison target, never as input evidence: the machine proposes from the ecosystem basis alone, so §4's agreement and disagreement are themselves findings.

Vocabulary rule: super-node / sub-node / co-node / sub-tree only.

## §1 Verdict

Of rust's 163 named visible kinds, the machine proposes an ur_kind for **106 (65%): 22 strong, 54 moderate, 30 weak**; the **residue is 57 rows (35%)**. Read against the basis's own measure of rust — only 42.3% of its kinds sit in ≥10-language clusters at t=0.40, its expression tier clusters with its own lineage (sway, jakt) and nobody else (log_015 §6) — this is about as much as the ecosystem can independently vouch for: the machine reproduces the decidable core (declarations, containers, literals, operators, control flow, the pair/container rulings) and refuses exactly where rust is structurally private (the expression apparatus, the `_pattern` family, the macro token machinery) or where the old draft leaned on categories (D/F/J) that the two-layer ruling now keeps out of ur_kind. Where both the hand and the machine committed firmly, they agree on 31 of 64 rows — and most of the 33 firm disagreements are ruling-driven (container-form, pair, the declaration family), not accidents. Confidence was never padded to shrink the residue: every proposal carries its cluster ids, language counts, band position, counterpart votes and LABELED name evidence, and 30 of the 106 are explicitly weak.

## §2 The generator mechanism and its documented decisions

One merge tree, queried — never re-derived. The mechanism, per `pack_generator.py` (every knob a documented constant in the file header and this section):

1. **Anchors.** The t=0.40 partition is recomputed and verified against `basis_xref_out.json` (1,194 clusters), then the bucket-anchor clusters are re-derived with basis_xref's exact criterion (≥5 name-matches, ≥40% of members, ≥5 languages), uncapped (basis_xref kept a top-6 presentation slice; anchoring wants them all). Three routing rules: (a) a cluster hit by several buckets anchors only the bucket with the highest match fraction, exact ties dropped; (b) the RULED container re-route — an object-bucket anchor dominated (≥40%) by document-root/body-list names re-anchors `container-form` (M4/M5 become the ruled form); (c) the RULED additions `import`/`try`/`pair` anchor on log_015 §4's core clusters, pinned by cluster id and self-checked against an expected member each. `interpolation` currently has NO anchor: its 121-language M9 cluster is 3% name-pure at t=0.40, below the 10% admission floor — it stays a name-note until a purer slice is pinned. Categories A–J keep their matched clusters as INTENTION anchors, used for notes only. The anchor set that resulted:

- **value**: cl335 (11 langs, 155 kinds, e.g. cast_expression/parenthesized_expression); cl208 (13 langs, 59 kinds, e.g. integer/float); cl750 (23 langs, 60 kinds, e.g. number/null); cl203 (6 langs, 28 kinds, e.g. signed_number/false); cl751 (24 langs, 60 kinds, e.g. number/string); cl207 (16 langs, 63 kinds, e.g. identifier/boolean); cl317 (6 langs, 41 kinds, e.g. word/string_literal); cl294 (9 langs, 84 kinds, e.g. identifier/float); cl748 (6 langs, 18 kinds, e.g. type_identifier/escape_sequence)
- **name**: cl758 (61 langs, 75 kinds, e.g. identifier/namespace_identifier); cl1094 (10 langs, 10 kinds, e.g. module_name/by_ref); cl752 (39 langs, 60 kinds, e.g. shorthand_field_identifier/name); cl759 (36 langs, 56 kinds, e.g. identifier/name); cl1093 (6 langs, 6 kinds, e.g. dotted_name/namespace_name); cl1058 (9 langs, 10 kinds, e.g. module_name/dotted_name); cl749 (16 langs, 16 kinds, e.g. identifier/string); cl1131 (17 langs, 20 kinds, e.g. pointer_type_declarator/image_name); cl1092 (10 langs, 12 kinds, e.g. dependent_name/command_name); cl753 (17 langs, 20 kinds, e.g. field_identifier/property_identifier)
- **operation**: cl193 (11 langs, 21 kinds, e.g. binary_expression/assignment_expression); cl325 (29 langs, 61 kinds, e.g. unary_expression/update_expression); cl910 (11 langs, 15 kinds, e.g. unary_expression/exposed_operator); cl897 (8 langs, 9 kinds, e.g. unary_expression/unary_operator); cl324 (12 langs, 14 kinds, e.g. unary_expression/unary_operator); cl191 (17 langs, 18 kinds, e.g. binary_expression/binary_expr); cl179 (20 langs, 31 kinds, e.g. binary_expression/assignment_expression); cl176 (23 langs, 32 kinds, e.g. binary_expression/assignment_expression); cl180 (30 langs, 49 kinds, e.g. binary_expression/assignment_expression); cl774 (7 langs, 21 kinds, e.g. operator/operator_identifier); cl773 (9 langs, 56 kinds, e.g. hash_operator/prefix_operator)
- **sequence**: cl873 (6 langs, 6 kinds, e.g. block/then); cl225 (11 langs, 11 kinds, e.g. sequence_expression/tuple)
- **choice**: cl79 (9 langs, 22 kinds, e.g. while_statement/if_statement); cl729 (8 langs, 9 kinds, e.g. else_clause/else_statement); cl126 (12 langs, 12 kinds, e.g. conditional_expression/ternary_expression); cl809 (5 langs, 5 kinds, e.g. else_clause/else); cl120 (6 langs, 6 kinds, e.g. if_expression/if); cl810 (24 langs, 25 kinds, e.g. else_clause/foreach_else); cl80 (7 langs, 11 kinds, e.g. if_statement/else_if_clause); cl808 (13 langs, 13 kinds, e.g. preproc_else/else_statement); cl111 (9 langs, 11 kinds, e.g. if_statement/if); cl89 (7 langs, 7 kinds, e.g. elif_clause/elseif_statement); cl107 (24 langs, 24 kinds, e.g. if_statement); cl117 (34 langs, 38 kinds, e.g. ternary_expression/conditional_expression); cl114 (7 langs, 8 kinds, e.g. if_statement/guard_statement)
- **repetition**: cl681 (8 langs, 11 kinds, e.g. while_statement/repeat_statement); cl670 (10 langs, 19 kinds, e.g. while_statement/switch_statement); cl360 (6 langs, 16 kinds, e.g. loop_expression/const_block); cl671 (27 langs, 80 kinds, e.g. do_statement/while_statement); cl688 (8 langs, 15 kinds, e.g. while_statement/for_statement); cl676 (5 langs, 6 kinds, e.g. for_range_loop/expansion_statement); cl715 (14 langs, 27 kinds, e.g. for_statement/with_statement); cl848 (20 langs, 44 kinds, e.g. break_statement/continue_statement); cl344 (5 langs, 5 kinds, e.g. while_expression/while_loop); cl134 (10 langs, 10 kinds, e.g. for_in_statement/foreach_statement)
- **function**: cl828 (24 langs, 24 kinds, e.g. formal_parameters/parameter_list); cl295 (5 langs, 9 kinds, e.g. call_expression/function_call); cl917 (15 langs, 15 kinds, e.g. arguments/argument_list); cl920 (16 langs, 17 kinds, e.g. argument_list/arguments); cl823 (21 langs, 28 kinds, e.g. preproc_params/parameter_list); cl503 (14 langs, 30 kinds, e.g. preproc_function_def/preproc_def); cl525 (30 langs, 50 kinds, e.g. method_definition/function_declaration); cl922 (22 langs, 27 kinds, e.g. argument_list/arguments); cl459 (8 langs, 12 kinds, e.g. functional_notation/element); cl527 (11 langs, 19 kinds, e.g. function_declaration/method_signature); cl304 (10 langs, 10 kinds, e.g. call_expression/call); cl921 (25 langs, 26 kinds, e.g. arguments/argument_list); cl1114 (11 langs, 21 kinds, e.g. type_parameter_declaration/variadic_type_parameter_declaration); cl826 (20 langs, 25 kinds, e.g. parameters/parameter_list); cl884 (10 langs, 16 kinds, e.g. function_declarator/abstract_function_declarator); cl546 (10 langs, 43 kinds, e.g. function_declaration/class_declaration); cl915 (10 langs, 10 kinds, e.g. argument_list/arguments); cl364 (16 langs, 18 kinds, e.g. arrow_function/lambda); cl334 (14 langs, 22 kinds, e.g. call_expression/new_expression); cl434 (5 langs, 10 kinds, e.g. method_invocation/codeOf); cl417 (5 langs, 13 kinds, e.g. module_def/function_type); cl532 (8 langs, 14 kinds, e.g. type_binding/abbrev); cl827 (10 langs, 12 kinds, e.g. parameters/formal_parameters); cl441 (9 langs, 27 kinds, e.g. function_expression/class); cl705 (10 langs, 10 kinds, e.g. function_definition)
- **record**: cl516 (9 langs, 34 kinds, e.g. enum_specifier/struct_specifier); cl654 (7 langs, 9 kinds, e.g. explicit_constructor_invocation/invocation)
- **collection**: cl1085 (14 langs, 26 kinds, e.g. initializer_list/array_initializer); cl226 (5 langs, 9 kinds, e.g. expression_list/yield); cl927 (5 langs, 5 kinds, e.g. initializer_list)
- **mutation**: cl158 (18 langs, 30 kinds, e.g. assignment_statement/assignment); cl175 (12 langs, 24 kinds, e.g. assignment_expression/augmented_assignment_expression)
- **service call**: cl604 (16 langs, 35 kinds, e.g. init_declarator/gnu_asm_input_operand)
- **import**: cl983 (20 langs, 39 kinds, e.g. preproc_call/preproc_include)
- **try**: cl735 (14 langs, 27 kinds, e.g. catch_clause/finally_clause); cl703 (9 langs, 10 kinds, e.g. catch_clause/lambda_expression); cl673 (15 langs, 30 kinds, e.g. try_statement/seh_try_statement); cl716 (22 langs, 35 kinds, e.g. seh_except_clause/seh_finally_clause)
- **pair**: cl628 (63 langs, 95 kinds, e.g. initializer_pair/pair_pattern); cl627 (25 langs, 43 kinds, e.g. pair/extends_clause)
- **D pattern matching**: cl380 (13 langs, 22 kinds, e.g. array_pattern/object_pattern); cl1108 (6 langs, 24 kinds, e.g. use_list/range_pattern); cl851 (14 langs, 14 kinds, e.g. case_statement/export_statement); cl635 (11 langs, 18 kinds, e.g. match_arm/case_statement); cl378 (9 langs, 9 kinds, e.g. rest_pattern); cl649 (11 langs, 11 kinds, e.g. switch_statement/return_statement); cl726 (9 langs, 9 kinds, e.g. switch_default)
- **F generics**: cl881 (6 langs, 6 kinds, e.g. template_template_parameter_declaration/template_declaration); cl882 (8 langs, 8 kinds, e.g. template_declaration/attribute); cl194 (5 langs, 10 kinds, e.g. constraint_conjunction/constraint_disjunction)
- **J metaprogramming**: cl1104 (11 langs, 12 kinds, e.g. decorator/type_arguments); cl1070 (10 langs, 14 kinds, e.g. type_annotation/type_parameters); cl504 (5 langs, 7 kinds, e.g. annotation/marker_annotation); cl1064 (11 langs, 17 kinds, e.g. asserts_annotation/type_predicate_annotation); cl52 (18 langs, 24 kinds, e.g. source_file/preproc_include)
- **type-form**: cl963 (5 langs, 13 kinds, e.g. function_type/aliased_type); cl1035 (5 langs, 13 kinds, e.g. named_type/type_application); cl31 (9 langs, 16 kinds, e.g. intrinsic_type/move_type); cl799 (14 langs, 19 kinds, e.g. primitive_type/prefix_list); cl224 (5 langs, 10 kinds, e.g. generic_type/scoped_type_identifier); cl800 (5 langs, 5 kinds, e.g. type_identifier)
- **declarative-form**: cl785 (265 langs, 371 kinds, e.g. comment/block_comment)
- **container-form**: cl992 (56 langs, 142 kinds, e.g. switch_body/enumerator_list); cl993 (28 langs, 34 kinds, e.g. field_declaration_list/declaration_list); cl1005 (275 langs, 276 kinds, e.g. source_file/program); cl988 (13 langs, 14 kinds, e.g. external_declaration/heading_body); cl995 (13 langs, 15 kinds, e.g. class_body/block); cl1012 (10 langs, 12 kinds, e.g. program/source_file); cl1013 (26 langs, 26 kinds, e.g. source_file/program); cl991 (11 langs, 17 kinds, e.g. declaration_list/field_declaration_list); cl1002 (11 langs, 11 kinds, e.g. source_file/config_file)

2. **Per-kind evidence, on a band.** Each kind's cluster is queried at seven slices (0.40, 0.48, 0.55, 0.62, 0.68, 0.73, 0.78 — log_015's four reference thresholds plus midpoints), not one cut. Hierarchy makes co-clustering an O(1) test (an anchor sits wholly inside exactly one cluster at every t ≥ 0.40). A join counts only under the four-part dilution guard: containing cluster < 300 languages and < 3,000 kinds (excludes the shape-poverty giants), ≥ 10 languages (evidence means many-language agreement), ≤ 5.0 kinds per language (semantic families run 1–4; blobs run 5–20+), and ≤ 1/3 own-language members (a cluster dominated by rust's own kinds is self-affinity, not agreement). The last three tests were added after trial runs on rust in which rust's private expression cluster merged with a 9-language leaf blob at 0.48 and dragged thirty expression kinds into `value`.
3. **Proposal.** ur_kind = the shape bucket with the lowest join threshold; joins at the same band slice pool, and the wider anchor wins the pool (a 0.05 margin — a wider margin let a 16-language closure cluster outvote the loop family's own earlier join in trials). Two floored fallback channels: counterpart votes (≥3 of the top-10 nearest counterpart archetypes sitting in one bucket's anchors; the secondary evidence of log_015 §7 P9), and a name-only route that is ALWAYS weak, ALWAYS labeled, and legal only for the form tier — any form if the kind is cluster-isolated (≤2 languages), and `declarative-form`/`proof-form` even without isolation (a grammar that gives comments internal structure leaves the 265-language comment archetype without ceasing to be trivia; proof-form HAS no ecosystem cluster anywhere, so name evidence is the only evidence that can ever exist for it). Objects are never proposed on names alone.
4. **Confidence, mechanical:** strong = join at t ≤ 0.55, anchor ≥ 10 languages, anchor purity ≥ 0.7 (or ≥ 50-language anchor), no competitor at the same slice, no name conflict; moderate = join at t ≤ 0.68 failing one of strong's margins; weak = band-top joins, mixed anchors (purity < 0.5), counterpart votes at the floor, name conflicts, and every name-only row. Below all floors → residue.
5. **Two-layer discipline.** Categories A–J are never proposed. Category anchors (D/F/J) and category name matches emit intention NOTES on the row — duals for the ledger's later resolution, per the ruling that replaced log_008's 42 per-row DUAL tie-breaks.
6. **Totality.** Rows = named visible kinds of the pinned grammar (`raw/rust.node-types.json`: `named` true, name not starting with `_`; supertype entries are hidden nodes and excluded). Checked equal to the 163 kinds in the cluster data and to the compiled-grammar pin of log_008; each kind appears exactly once.

## §3 The proposal table — all 163 rows

This is the review artifact (same content as `proposed_kind_map_rust.md`). Evidence abbreviations: “joins anchor clN (K langs) at t=X” is the cluster channel; counterpart votes are out of 10; name evidence is always labeled as such.

| kind | proposed | conf | evidence | intention note |
| --- | --- | --- | --- | --- |
| `abstract_type` | type-form | moderate | type-form: joins anchor cl799 (14 langs) at t=0.68 (containing cluster 74 kinds / 20 langs); name evidence (labeled): type-form | — |
| `arguments` | function | strong | function: joins anchor cl922 (22 langs) at t=0.40 (containing cluster 27 kinds / 22 langs); collection: joins anchor cl927 (5 langs) at t=0.73 (containing cluster 140 kinds / 82 langs); counterparts: function 10/10; name evidence (labeled): function | — |
| `array_expression` | **none** | — | name evidence (labeled): collection | — |
| `array_type` | type-form | moderate | type-form: joins anchor cl799 (14 langs) at t=0.68 (containing cluster 74 kinds / 20 langs); name evidence (labeled): collection, type-form | — |
| `assignment_expression` | operation | moderate | operation: joins anchor cl179 (20 langs) at t=0.40 (containing cluster 31 kinds / 20 langs); mutation: joins anchor cl175 (12 langs) at t=0.55 (containing cluster 164 kinds / 76 langs); counterparts: operation 8/10; name evidence (labeled): mutation | co-clusters with F generics anchors at t=0.62 (cluster evidence) |
| `associated_type` | function | moderate | function: joins anchor cl532 (8 langs) at t=0.48 (containing cluster 140 kinds / 41 langs); name evidence (labeled): type-form | — |
| `async_block` | **none** | — | name evidence (labeled): container-form | name evidence (name only, unweighed): A suspension |
| `attribute` | **none** | — | — | name evidence (name only, unweighed): J metaprogramming |
| `attribute_item` | **none** | — | — | name evidence (name only, unweighed): J metaprogramming |
| `await_expression` | **none** | — | — | name evidence (name only, unweighed): A suspension |
| `base_field_initializer` | **none** | — | name evidence (labeled): record | — |
| `binary_expression` | operation | strong | operation: joins anchor cl179 (20 langs) at t=0.40 (containing cluster 31 kinds / 20 langs); mutation: joins anchor cl175 (12 langs) at t=0.55 (containing cluster 164 kinds / 76 langs); counterparts: operation 10/10; name evidence (labeled): operation | co-clusters with F generics anchors at t=0.62 (cluster evidence) |
| `block` | value | weak | counterparts: value 7/10; name evidence (labeled): sequence | — |
| `block_comment` | declarative-form | weak | name evidence (labeled): declarative-form | co-clusters with J metaprogramming anchors at t=0.40 (cluster evidence) |
| `boolean_literal` | value | moderate | counterparts: value 10/10; name evidence (labeled): value | — |
| `bounded_type` | type-form | moderate | type-form: joins anchor cl1035 (5 langs) at t=0.55 (containing cluster 106 kinds / 23 langs); counterparts: type-form 1/10; name evidence (labeled): type-form | name evidence (name only, unweighed): F generics |
| `bracketed_type` | name | moderate | name: joins anchor cl1058 (9 langs) at t=0.62 (containing cluster 696 kinds / 160 langs); name evidence (labeled): type-form | co-clusters with J metaprogramming anchors at t=0.55 (cluster evidence) |
| `break_expression` | **none** | — | name evidence (labeled): repetition | — |
| `call_expression` | function | weak | counterparts: function 6/10; name evidence (labeled): function | — |
| `captured_pattern` | **none** | — | — | name evidence (name only, unweighed): D pattern matching |
| `char_literal` | value | moderate | counterparts: value 10/10; name evidence (labeled): value | — |
| `closure_expression` | function | strong | function: joins anchor cl364 (16 langs) at t=0.48 (containing cluster 24 kinds / 21 langs); repetition: joins anchor cl360 (6 langs) at t=0.62 (containing cluster 66 kinds / 38 langs); counterparts: function 4/10; name evidence (labeled): function | — |
| `closure_parameters` | function | strong | function: joins anchor cl826 (20 langs) at t=0.40 (containing cluster 25 kinds / 20 langs); counterparts: function 10/10; name evidence (labeled): function | — |
| `compound_assignment_expr` | operation | moderate | operation: joins anchor cl179 (20 langs) at t=0.40 (containing cluster 31 kinds / 20 langs); mutation: joins anchor cl175 (12 langs) at t=0.55 (containing cluster 164 kinds / 76 langs); counterparts: operation 10/10; name evidence (labeled): mutation | co-clusters with F generics anchors at t=0.62 (cluster evidence) |
| `const_block` | repetition | moderate | repetition: joins anchor cl360 (6 langs) at t=0.55 (containing cluster 25 kinds / 12 langs); function: joins anchor cl364 (16 langs) at t=0.62 (containing cluster 66 kinds / 38 langs); counterparts: repetition 10/10; name evidence (labeled): container-form | — |
| `const_item` | function | strong | function: joins anchor cl503 (14 langs) at t=0.48 (containing cluster 325 kinds / 67 langs) | co-clusters with J metaprogramming anchors at t=0.48 (cluster evidence) |
| `const_parameter` | **none** | — | name evidence (labeled): function | — |
| `continue_expression` | **none** | — | name evidence (labeled): repetition | — |
| `crate` | value | weak | value: joins anchor cl207 (16 langs) at t=0.40 (containing cluster 63 kinds / 16 langs); counterparts: value 10/10 | — |
| `declaration_list` | container-form | strong | container-form: joins anchor cl991 (11 langs) at t=0.40 (containing cluster 17 kinds / 11 langs); counterparts: container-form 10/10; name evidence (labeled): sequence, collection, container-form | — |
| `doc_comment` | declarative-form | weak | counterparts: name 3/10; name evidence (labeled): declarative-form | — |
| `dynamic_type` | type-form | moderate | type-form: joins anchor cl799 (14 langs) at t=0.68 (containing cluster 74 kinds / 20 langs); counterparts: type-form 2/10; name evidence (labeled): type-form | — |
| `else_clause` | choice | moderate | choice: joins anchor cl809 (5 langs) at t=0.55 (containing cluster 30 kinds / 29 langs); counterparts: choice 5/10, container-form 1/10; name evidence (labeled): choice | — |
| `empty_statement` | **none** | — | — | — |
| `enum_item` | function | moderate | function: joins anchor cl532 (8 langs) at t=0.48 (containing cluster 140 kinds / 41 langs); name evidence (labeled): record | — |
| `enum_variant` | function | moderate | function: joins anchor cl503 (14 langs) at t=0.48 (containing cluster 325 kinds / 67 langs); name evidence (labeled): record | co-clusters with J metaprogramming anchors at t=0.48 (cluster evidence) |
| `enum_variant_list` | container-form | moderate | container-form: joins anchor cl992 (56 langs) at t=0.40 (containing cluster 142 kinds / 56 langs); counterparts: container-form 10/10; name evidence (labeled): record, collection | — |
| `escape_sequence` | **none** | — | name evidence (labeled): sequence | — |
| `expression_statement` | **none** | — | — | — |
| `extern_crate_declaration` | function | moderate | function: joins anchor cl525 (30 langs) at t=0.48 (containing cluster 91 kinds / 39 langs); name evidence (labeled): service call, import | — |
| `extern_modifier` | function | moderate | function: joins anchor cl1114 (11 langs) at t=0.40 (containing cluster 21 kinds / 11 langs); name: joins anchor cl1094 (10 langs) at t=0.62 (containing cluster 317 kinds / 75 langs); counterparts: function 3/10; name evidence (labeled): service call, declarative-form | co-clusters with D pattern matching anchors at t=0.62 (cluster evidence); co-clusters with J metaprogramming anchors at t=0.62 (cluster evidence) |
| `field_declaration` | **none** | — | name evidence (labeled): record | — |
| `field_declaration_list` | container-form | strong | container-form: joins anchor cl993 (28 langs) at t=0.40 (containing cluster 34 kinds / 28 langs); counterparts: container-form 10/10; name evidence (labeled): sequence, record, collection, container-form | — |
| `field_expression` | **none** | — | name evidence (labeled): record | — |
| `field_identifier` | name | strong | name: joins anchor cl753 (17 langs) at t=0.40 (containing cluster 20 kinds / 17 langs); counterparts: name 8/10; name evidence (labeled): name, record | — |
| `field_initializer` | pair | weak | pair: joins anchor cl628 (63 langs) at t=0.55 (containing cluster 210 kinds / 102 langs); service call: joins anchor cl604 (16 langs) at t=0.73 (containing cluster 501 kinds / 152 langs); counterparts: D pattern matching 8/10, pair 2/10; name evidence (labeled): record | co-clusters with D pattern matching anchors at t=0.40 (cluster evidence); counterpart evidence: D pattern matching 8/10 |
| `field_initializer_list` | container-form | moderate | container-form: joins anchor cl992 (56 langs) at t=0.40 (containing cluster 142 kinds / 56 langs); counterparts: container-form 10/10; name evidence (labeled): record, collection | — |
| `field_pattern` | **none** | — | name evidence (labeled): record | name evidence (name only, unweighed): D pattern matching |
| `float_literal` | value | moderate | counterparts: value 10/10; name evidence (labeled): value | — |
| `for_expression` | repetition | moderate | repetition: joins anchor cl360 (6 langs) at t=0.55 (containing cluster 25 kinds / 12 langs); function: joins anchor cl364 (16 langs) at t=0.62 (containing cluster 66 kinds / 38 langs); counterparts: repetition 6/10; name evidence (labeled): repetition | — |
| `for_lifetimes` | proof-form | weak | name evidence (labeled): repetition, proof-form | — |
| `foreign_mod_item` | repetition | weak | repetition: joins anchor cl715 (14 langs) at t=0.40 (containing cluster 27 kinds / 14 langs); try: joins anchor cl716 (22 langs) at t=0.48 (containing cluster 100 kinds / 58 langs); counterparts: repetition 5/10; name evidence (labeled): repetition, service call | co-clusters with D pattern matching anchors at t=0.62 (cluster evidence) |
| `fragment_specifier` | **none** | — | counterparts: name 1/10 | — |
| `function_item` | function | strong | function: joins anchor cl525 (30 langs) at t=0.40 (containing cluster 50 kinds / 30 langs); counterparts: function 8/10; name evidence (labeled): function | — |
| `function_modifiers` | declarative-form | weak | name evidence (labeled): function, declarative-form | — |
| `function_signature_item` | function | strong | function: joins anchor cl525 (30 langs) at t=0.48 (containing cluster 91 kinds / 39 langs); counterparts: function 4/10; name evidence (labeled): function | — |
| `function_type` | function | moderate | function: joins anchor cl884 (10 langs) at t=0.62 (containing cluster 56 kinds / 24 langs); counterparts: function 3/10; name evidence (labeled): function, type-form | co-clusters with F generics anchors at t=0.62 (cluster evidence) |
| `gen_block` | **none** | — | name evidence (labeled): container-form | — |
| `generic_function` | **none** | — | counterparts: value 1/10; name evidence (labeled): function | name evidence (name only, unweighed): F generics |
| `generic_pattern` | **none** | — | counterparts: D pattern matching 2/10 | counterpart evidence: D pattern matching 2/10; name evidence (name only, unweighed): D pattern matching, F generics |
| `generic_type` | type-form | moderate | type-form: joins anchor cl799 (14 langs) at t=0.68 (containing cluster 74 kinds / 20 langs); name evidence (labeled): type-form | name evidence (name only, unweighed): F generics |
| `generic_type_with_turbofish` | name | weak | counterparts: name 7/10 | co-clusters with J metaprogramming anchors at t=0.78 (cluster evidence); name evidence (name only, unweighed): F generics |
| `higher_ranked_trait_bound` | import | weak | import: joins anchor cl983 (20 langs) at t=0.68 (containing cluster 531 kinds / 156 langs); counterparts: value 1/10 | name evidence (name only, unweighed): E dispatch, F generics |
| `identifier` | value | weak | counterparts: value 6/10; name evidence (labeled): name | — |
| `if_expression` | choice | strong | choice: joins anchor cl126 (12 langs) at t=0.55 (containing cluster 30 kinds / 27 langs); counterparts: choice 9/10; name evidence (labeled): choice | — |
| `impl_item` | repetition | weak | repetition: joins anchor cl715 (14 langs) at t=0.40 (containing cluster 27 kinds / 14 langs); try: joins anchor cl716 (22 langs) at t=0.48 (containing cluster 100 kinds / 58 langs); counterparts: repetition 5/10 | co-clusters with D pattern matching anchors at t=0.62 (cluster evidence); name evidence (name only, unweighed): E dispatch |
| `index_expression` | **none** | — | name evidence (labeled): collection | — |
| `inner_attribute_item` | **none** | — | — | name evidence (name only, unweighed): J metaprogramming |
| `inner_doc_comment_marker` | declarative-form | weak | counterparts: name 3/10; name evidence (labeled): declarative-form | — |
| `integer_literal` | value | moderate | counterparts: value 10/10; name evidence (labeled): value | — |
| `label` | function | moderate | function: joins anchor cl1114 (11 langs) at t=0.55 (containing cluster 153 kinds / 39 langs); name: joins anchor cl1094 (10 langs) at t=0.62 (containing cluster 317 kinds / 75 langs) | co-clusters with D pattern matching anchors at t=0.62 (cluster evidence); co-clusters with J metaprogramming anchors at t=0.62 (cluster evidence) |
| `let_chain` | **none** | — | — | — |
| `let_condition` | pair | weak | pair: joins anchor cl627 (25 langs) at t=0.40 (containing cluster 43 kinds / 25 langs); service call: joins anchor cl604 (16 langs) at t=0.73 (containing cluster 501 kinds / 152 langs); counterparts: pair 10/10 | co-clusters with D pattern matching anchors at t=0.55 (cluster evidence) |
| `let_declaration` | pair | weak | counterparts: D pattern matching 4/10, pair 3/10 | counterpart evidence: D pattern matching 4/10 |
| `lifetime` | name | moderate | name: joins anchor cl1094 (10 langs) at t=0.40 (containing cluster 10 kinds / 10 langs); function: joins anchor cl1114 (11 langs) at t=0.62 (containing cluster 317 kinds / 75 langs); counterparts: name 3/10; name evidence (labeled): proof-form | co-clusters with D pattern matching anchors at t=0.62 (cluster evidence); co-clusters with J metaprogramming anchors at t=0.62 (cluster evidence) |
| `lifetime_parameter` | proof-form | weak | name evidence (labeled): function, proof-form | — |
| `line_comment` | declarative-form | weak | name evidence (labeled): declarative-form | co-clusters with J metaprogramming anchors at t=0.40 (cluster evidence) |
| `loop_expression` | repetition | moderate | repetition: joins anchor cl360 (6 langs) at t=0.55 (containing cluster 25 kinds / 12 langs); function: joins anchor cl364 (16 langs) at t=0.62 (containing cluster 66 kinds / 38 langs); counterparts: repetition 10/10; name evidence (labeled): repetition | — |
| `macro_definition` | function | strong | function: joins anchor cl525 (30 langs) at t=0.48 (containing cluster 91 kinds / 39 langs) | name evidence (name only, unweighed): J metaprogramming |
| `macro_invocation` | **none** | — | — | name evidence (name only, unweighed): J metaprogramming |
| `macro_rule` | mutation | weak | mutation: joins anchor cl158 (18 langs) at t=0.55 (containing cluster 70 kinds / 37 langs); repetition: joins anchor cl134 (10 langs) at t=0.68 (containing cluster 148 kinds / 62 langs); counterparts: mutation 1/10 | co-clusters with F generics anchors at t=0.73 (cluster evidence); name evidence (name only, unweighed): J metaprogramming |
| `match_arm` | pair | weak | pair: joins anchor cl628 (63 langs) at t=0.55 (containing cluster 210 kinds / 102 langs); service call: joins anchor cl604 (16 langs) at t=0.73 (containing cluster 501 kinds / 152 langs); counterparts: D pattern matching 8/10, pair 2/10; name evidence (labeled): pair | co-clusters with D pattern matching anchors at t=0.40 (cluster evidence); counterpart evidence: D pattern matching 8/10; name evidence (name only, unweighed): D pattern matching |
| `match_block` | container-form | strong | container-form: joins anchor cl992 (56 langs) at t=0.40 (containing cluster 142 kinds / 56 langs); counterparts: container-form 10/10; name evidence (labeled): container-form | name evidence (name only, unweighed): D pattern matching |
| `match_expression` | **none** | — | counterparts: repetition 1/10 | name evidence (name only, unweighed): D pattern matching |
| `match_pattern` | **none** | — | — | name evidence (name only, unweighed): D pattern matching |
| `metavariable` | value | weak | counterparts: value 6/10; name evidence (labeled): name | — |
| `mod_item` | function | strong | function: joins anchor cl525 (30 langs) at t=0.48 (containing cluster 91 kinds / 39 langs) | — |
| `mut_pattern` | **none** | — | — | name evidence (name only, unweighed): D pattern matching |
| `mutable_specifier` | proof-form | weak | counterparts: name 2/10; name evidence (labeled): proof-form | — |
| `negative_literal` | **none** | — | name evidence (labeled): value | — |
| `never_type` | type-form | strong | type-form: joins anchor cl799 (14 langs) at t=0.40 (containing cluster 19 kinds / 14 langs); counterparts: type-form 5/10; name evidence (labeled): type-form | — |
| `or_pattern` | **none** | — | — | name evidence (name only, unweighed): D pattern matching |
| `ordered_field_declaration_list` | container-form | strong | container-form: joins anchor cl993 (28 langs) at t=0.40 (containing cluster 34 kinds / 28 langs); counterparts: container-form 10/10; name evidence (labeled): sequence, record, collection, container-form | — |
| `outer_doc_comment_marker` | declarative-form | weak | counterparts: name 3/10; name evidence (labeled): declarative-form | — |
| `parameter` | **none** | — | name evidence (labeled): function | — |
| `parameters` | function | strong | function: joins anchor cl827 (10 langs) at t=0.40 (containing cluster 12 kinds / 10 langs); counterparts: function 8/10; name evidence (labeled): function | — |
| `parenthesized_expression` | **none** | — | — | — |
| `pointer_type` | type-form | moderate | type-form: joins anchor cl799 (14 langs) at t=0.68 (containing cluster 74 kinds / 20 langs); name evidence (labeled): type-form | — |
| `primitive_type` | type-form | moderate | type-form: joins anchor cl799 (14 langs) at t=0.68 (containing cluster 74 kinds / 20 langs); counterparts: type-form 3/10, value 1/10; name evidence (labeled): type-form | — |
| `qualified_type` | import | weak | import: joins anchor cl983 (20 langs) at t=0.48 (containing cluster 515 kinds / 153 langs); name evidence (labeled): type-form | — |
| `range_expression` | **none** | — | — | — |
| `range_pattern` | mutation | weak | repetition: joins anchor cl134 (10 langs) at t=0.68 (containing cluster 148 kinds / 62 langs); mutation: joins anchor cl158 (18 langs) at t=0.68 (containing cluster 148 kinds / 62 langs); counterparts: mutation 7/10 | co-clusters with F generics anchors at t=0.73 (cluster evidence); name evidence (name only, unweighed): D pattern matching |
| `raw_string_literal` | value | moderate | counterparts: value 10/10; name evidence (labeled): value | — |
| `ref_pattern` | proof-form | weak | name evidence (labeled): proof-form | name evidence (name only, unweighed): D pattern matching |
| `reference_expression` | **none** | — | — | — |
| `reference_pattern` | **none** | — | — | name evidence (name only, unweighed): D pattern matching |
| `reference_type` | type-form | moderate | type-form: joins anchor cl799 (14 langs) at t=0.68 (containing cluster 74 kinds / 20 langs); name evidence (labeled): type-form, proof-form | — |
| `remaining_field_pattern` | **none** | — | counterparts: name 1/10; name evidence (labeled): record | name evidence (name only, unweighed): D pattern matching |
| `removed_trait_bound` | type-form | moderate | type-form: joins anchor cl1035 (5 langs) at t=0.55 (containing cluster 106 kinds / 23 langs) | name evidence (name only, unweighed): E dispatch, F generics |
| `return_expression` | **none** | — | name evidence (labeled): function | — |
| `scoped_identifier` | function | moderate | function: joins anchor cl434 (5 langs) at t=0.55 (containing cluster 100 kinds / 41 langs); counterparts: function 3/10; name evidence (labeled): name | — |
| `scoped_type_identifier` | function | moderate | function: joins anchor cl434 (5 langs) at t=0.68 (containing cluster 120 kinds / 45 langs) | — |
| `scoped_use_list` | type-form | moderate | type-form: joins anchor cl31 (9 langs) at t=0.48 (containing cluster 115 kinds / 44 langs); name evidence (labeled): collection | — |
| `self` | value | moderate | counterparts: value 10/10 | — |
| `self_parameter` | **none** | — | name evidence (labeled): function | — |
| `shebang` | declarative-form | weak | name evidence (labeled): declarative-form | — |
| `shorthand_field_identifier` | name | strong | name: joins anchor cl752 (39 langs) at t=0.40 (containing cluster 60 kinds / 39 langs); counterparts: name 10/10; name evidence (labeled): name, record | — |
| `shorthand_field_initializer` | **none** | — | name evidence (labeled): record | — |
| `slice_pattern` | **none** | — | name evidence (labeled): collection | name evidence (name only, unweighed): D pattern matching |
| `source_file` | container-form | strong | container-form: joins anchor cl1005 (275 langs) at t=0.40 (containing cluster 276 kinds / 275 langs); counterparts: container-form 10/10; name evidence (labeled): sequence, container-form | — |
| `static_item` | function | strong | function: joins anchor cl503 (14 langs) at t=0.48 (containing cluster 325 kinds / 67 langs) | co-clusters with J metaprogramming anchors at t=0.48 (cluster evidence) |
| `string_content` | **none** | — | name evidence (labeled): value | — |
| `string_literal` | value | moderate | counterparts: value 10/10; name evidence (labeled): value | — |
| `struct_expression` | function | moderate | function: joins anchor cl434 (5 langs) at t=0.62 (containing cluster 105 kinds / 43 langs); counterparts: function 2/10; name evidence (labeled): record | — |
| `struct_item` | function | moderate | function: joins anchor cl532 (8 langs) at t=0.48 (containing cluster 140 kinds / 41 langs); name evidence (labeled): record | — |
| `struct_pattern` | **none** | — | name evidence (labeled): record | name evidence (name only, unweighed): D pattern matching |
| `super` | value | weak | value: joins anchor cl207 (16 langs) at t=0.40 (containing cluster 63 kinds / 16 langs); counterparts: value 10/10 | — |
| `token_binding_pattern` | function | strong | function: joins anchor cl503 (14 langs) at t=0.48 (containing cluster 325 kinds / 67 langs) | co-clusters with J metaprogramming anchors at t=0.48 (cluster evidence); name evidence (name only, unweighed): D pattern matching |
| `token_repetition` | function | moderate | function: joins anchor cl1114 (11 langs) at t=0.48 (containing cluster 26 kinds / 12 langs); name: joins anchor cl1094 (10 langs) at t=0.62 (containing cluster 317 kinds / 75 langs) | co-clusters with D pattern matching anchors at t=0.62 (cluster evidence); co-clusters with J metaprogramming anchors at t=0.62 (cluster evidence) |
| `token_repetition_pattern` | function | moderate | function: joins anchor cl1114 (11 langs) at t=0.48 (containing cluster 26 kinds / 12 langs); name: joins anchor cl1094 (10 langs) at t=0.62 (containing cluster 317 kinds / 75 langs) | co-clusters with D pattern matching anchors at t=0.62 (cluster evidence); co-clusters with J metaprogramming anchors at t=0.62 (cluster evidence); name evidence (name only, unweighed): D pattern matching |
| `token_tree` | function | moderate | function: joins anchor cl917 (15 langs) at t=0.48 (containing cluster 30 kinds / 29 langs); collection: joins anchor cl927 (5 langs) at t=0.73 (containing cluster 140 kinds / 82 langs); counterparts: function 2/10 | — |
| `token_tree_pattern` | function | moderate | function: joins anchor cl1114 (11 langs) at t=0.48 (containing cluster 26 kinds / 12 langs); name: joins anchor cl1094 (10 langs) at t=0.62 (containing cluster 317 kinds / 75 langs) | co-clusters with D pattern matching anchors at t=0.62 (cluster evidence); co-clusters with J metaprogramming anchors at t=0.62 (cluster evidence); name evidence (name only, unweighed): D pattern matching |
| `trait_bounds` | **none** | — | — | name evidence (name only, unweighed): E dispatch, F generics |
| `trait_item` | function | moderate | function: joins anchor cl532 (8 langs) at t=0.48 (containing cluster 140 kinds / 41 langs) | name evidence (name only, unweighed): E dispatch |
| `try_block` | **none** | — | name evidence (labeled): try, container-form | — |
| `try_expression` | **none** | — | name evidence (labeled): try | — |
| `tuple_expression` | **none** | — | name evidence (labeled): collection | — |
| `tuple_pattern` | **none** | — | counterparts: D pattern matching 1/10; name evidence (labeled): collection | counterpart evidence: D pattern matching 1/10; name evidence (name only, unweighed): D pattern matching |
| `tuple_struct_pattern` | **none** | — | name evidence (labeled): record, collection | name evidence (name only, unweighed): D pattern matching |
| `tuple_type` | type-form | moderate | type-form: joins anchor cl799 (14 langs) at t=0.68 (containing cluster 74 kinds / 20 langs); name evidence (labeled): collection, type-form | — |
| `type_arguments` | function | moderate | name: joins anchor cl1094 (10 langs) at t=0.62 (containing cluster 317 kinds / 75 langs); function: joins anchor cl1114 (11 langs) at t=0.62 (containing cluster 317 kinds / 75 langs); counterparts: J metaprogramming 6/10; name evidence (labeled): function | co-clusters with J metaprogramming anchors at t=0.40 (cluster evidence); co-clusters with D pattern matching anchors at t=0.55 (cluster evidence); counterpart evidence: J metaprogramming 6/10; name evidence (name only, unweighed): F generics |
| `type_binding` | **none** | — | — | — |
| `type_cast_expression` | **none** | — | name evidence (labeled): operation | — |
| `type_identifier` | type-form | moderate | type-form: joins anchor cl799 (14 langs) at t=0.68 (containing cluster 74 kinds / 20 langs); counterparts: name 4/10, type-form 3/10; name evidence (labeled): type-form | — |
| `type_item` | function | moderate | function: joins anchor cl532 (8 langs) at t=0.48 (containing cluster 140 kinds / 41 langs) | — |
| `type_parameter` | **none** | — | name evidence (labeled): function | name evidence (name only, unweighed): F generics |
| `type_parameters` | function | moderate | name: joins anchor cl1094 (10 langs) at t=0.62 (containing cluster 317 kinds / 75 langs); function: joins anchor cl1114 (11 langs) at t=0.62 (containing cluster 317 kinds / 75 langs); counterparts: D pattern matching 2/10, J metaprogramming 1/10; name evidence (labeled): function | co-clusters with D pattern matching anchors at t=0.48 (cluster evidence); co-clusters with J metaprogramming anchors at t=0.55 (cluster evidence); counterpart evidence: D pattern matching 2/10, J metaprogramming 1/10; name evidence (name only, unweighed): F generics |
| `unary_expression` | **none** | — | name evidence (labeled): operation | — |
| `union_item` | function | moderate | function: joins anchor cl532 (8 langs) at t=0.48 (containing cluster 140 kinds / 41 langs) | — |
| `unit_expression` | value | weak | counterparts: value 4/10 | — |
| `unit_type` | type-form | strong | type-form: joins anchor cl799 (14 langs) at t=0.40 (containing cluster 19 kinds / 14 langs); counterparts: type-form 5/10; name evidence (labeled): type-form | — |
| `unsafe_block` | **none** | — | name evidence (labeled): container-form | — |
| `use_as_clause` | type-form | moderate | type-form: joins anchor cl31 (9 langs) at t=0.48 (containing cluster 115 kinds / 44 langs); name evidence (labeled): import | — |
| `use_bounds` | **none** | — | name evidence (labeled): import | name evidence (name only, unweighed): F generics |
| `use_declaration` | **none** | — | name evidence (labeled): import | — |
| `use_list` | function | moderate | name: joins anchor cl1094 (10 langs) at t=0.62 (containing cluster 317 kinds / 75 langs); function: joins anchor cl1114 (11 langs) at t=0.62 (containing cluster 317 kinds / 75 langs); counterparts: D pattern matching 5/10, name 1/10; name evidence (labeled): collection, import | co-clusters with D pattern matching anchors at t=0.48 (cluster evidence); co-clusters with J metaprogramming anchors at t=0.55 (cluster evidence); counterpart evidence: D pattern matching 5/10 |
| `use_wildcard` | function | moderate | name: joins anchor cl1094 (10 langs) at t=0.62 (containing cluster 317 kinds / 75 langs); function: joins anchor cl1114 (11 langs) at t=0.62 (containing cluster 317 kinds / 75 langs); counterparts: D pattern matching 1/10; name evidence (labeled): import | co-clusters with D pattern matching anchors at t=0.48 (cluster evidence); co-clusters with J metaprogramming anchors at t=0.55 (cluster evidence); counterpart evidence: D pattern matching 1/10 |
| `variadic_parameter` | **none** | — | name evidence (labeled): function | — |
| `visibility_modifier` | function | moderate | function: joins anchor cl1114 (11 langs) at t=0.48 (containing cluster 26 kinds / 12 langs); name: joins anchor cl1094 (10 langs) at t=0.62 (containing cluster 317 kinds / 75 langs); name evidence (labeled): declarative-form | co-clusters with D pattern matching anchors at t=0.62 (cluster evidence); co-clusters with J metaprogramming anchors at t=0.62 (cluster evidence) |
| `where_clause` | **none** | — | — | name evidence (name only, unweighed): F generics |
| `where_predicate` | mutation | weak | repetition: joins anchor cl134 (10 langs) at t=0.68 (containing cluster 148 kinds / 62 langs); mutation: joins anchor cl158 (18 langs) at t=0.68 (containing cluster 148 kinds / 62 langs) | co-clusters with F generics anchors at t=0.73 (cluster evidence) |
| `while_expression` | repetition | moderate | repetition: joins anchor cl360 (6 langs) at t=0.55 (containing cluster 25 kinds / 12 langs); function: joins anchor cl364 (16 langs) at t=0.62 (containing cluster 66 kinds / 38 langs); counterparts: repetition 10/10; name evidence (labeled): repetition | — |
| `yield_expression` | **none** | — | — | name evidence (name only, unweighed): A suspension |

## §4 The comparison with log_008's hand draft

Counts over the 163 rows (hand rows normalized: the PROPOSED form names of log_008 map to the ruled names):

| class | count |
| --- | --- |
| agree (hand firm, machine matches) | 31 |
| disagree (hand firm, machine differs) | 33 |
| hand had no answer (UNCERTAIN/DUAL), machine proposes | 42 (machine picks one of the hand's own candidates in 11, something else in 31) |
| machine has no answer (residue) | 57 (the hand had flagged 24 of them itself; 33 it had answered firmly) |

Where both sides committed firmly the machine matched the hand on 31 of 64. The 33 firm disagreements, individually:

| kind | hand (log_008) | machine | comment |
| --- | --- | --- | --- |
| `assignment_expression` | mutation | operation (moderate) | the over-fine finding of log_015 §5 in the flesh: to the ecosystem, left-op-right is one shape at t=0.40 and the pure assignment family only joins at 0.55. Genuinely open — the ruled vocabulary keeps `mutation`, so the hand's reading likely stands at ratification, with the shape ambiguity now on record (the machine lists mutation as competitor evidence). |
| `block` | sequence | value (weak) | machine noise: rust's structurally odd `block` vector drifts to leaf/value anchors on counterpart votes (7/10), weak, name conflict flagged. Hand right (`sequence`). |
| `bracketed_type` | type-form | name (moderate) | machine noise via a 9-language name/alias cluster. Hand right (`type-form`). |
| `crate` | name | value (weak) | the bare-leaf shape merger (log_015 §5): path-root tokens cluster with literal leaves. Weak, mixed anchor flagged. Hand right (`name`). |
| `field_declaration_list` | record | container-form (strong) | ruling-driven: `container-form` (M4 body-lists, ruled 2026-08-12) supersedes the hand's `record`. Machine right by ruling. |
| `field_initializer` | record | pair (weak) | ruling-driven: the M3 pair/case family explicitly holds the initializer_pair kinds. Machine right by ruling (weak only because the anchor is name-mixed). |
| `field_initializer_list` | record | container-form (moderate) | same as `field_declaration_list`: container-form by ruling. Machine right. |
| `generic_type_with_turbofish` | F generics | name (weak) | the hand used category F, no longer mappable; the machine's `name` (counterpart votes, weak) is a placeholder. Genuinely open; F belongs in the intention note. |
| `identifier` | name | value (weak) | bare-leaf merger again: identifier and literal leaves share clusters ecosystem-wide, so the machine cannot split `name` from `value` for bare leaves. Weak, conflict flagged. Hand right (`name`). |
| `impl_item` | E dispatch | repetition (weak) | E is shape-invisible (standing fact). The shape evidence is real — a 14-language statement-with-body family holding for/with/try/impl — but `repetition` is weak noise from that mixed cluster. Genuinely open; residue-grade; E stays a ledger-resolved dual. |
| `let_declaration` | name | pair (weak) | counterpart drift into the pair family (`let PAT = value` IS a key-with-value shape), weak. Genuinely open — the hand read the binding, the machine reads the shape. |
| `macro_definition` | J metaprogramming | function (strong) | the two-layer ruling at work: the SHAPE is a definition (declaration family, strong), and the hand's J is the intention dual, ledger-resolved. Machine right by ruling. |
| `macro_rule` | J metaprogramming | mutation (weak) | matcher `=>` template is assignment-shaped to the ecosystem (weak). Genuinely open — `pair` is at least as arguable (M3 holds match arms), and J stays the intention dual either way. |
| `match_arm` | D pattern matching | pair (weak) | ruling-driven: M3 `pair` absorbs match arms (the 63-language core holds them by name). Machine right by ruling; D dual visible in the counterpart votes. |
| `match_block` | D pattern matching | container-form (strong) | ruling-driven: the arm list is a body-list container (M4). Machine right by ruling, strong. |
| `metavariable` | J metaprogramming | value (weak) | machine noise (leafy counterpart drift to `value`). The shape answer should probably be `name`; J stays the dual. Open. |
| `range_pattern` | D pattern matching | mutation (weak) | machine noise at the band top (t=0.68), weak. Residue-grade; D noted. |
| `ref_pattern` | D pattern matching | proof-form (weak) | the labeled name-only proof-form route: binding-mode `ref` filed with the borrow apparatus. Defensible under the proof-form ruling, but it is name evidence — the owner's call; D noted. |
| `scoped_identifier` | name | function (moderate) | machine noise via a narrow half-pure cluster (5 languages, purity 0.50). Hand right (`name` — paths are names). |
| `self` | name | value (moderate) | bare-leaf merger; 10/10 counterparts sit in value anchors because `self` is an expression leaf. Hand right semantically (`name`); shape alone cannot decide this row. |
| `struct_expression` | record | function (moderate) | narrow-anchor noise (same 5-language cluster as scoped_identifier). Hand right (`record`). |
| `struct_item` | record | function (moderate) | the declaration-family finding (log_015 §5): struct/class/interface/enum/function declarations are ONE 212-language family, and its best-anchored bucket is `function`. Genuinely open — if `record` is to stay distinct at declaration level, that is a vocabulary ruling the grammars will not make for us. |
| `super` | name | value (weak) | as `crate`: bare-leaf merger, weak. Hand right (`name`). |
| `token_binding_pattern` | J metaprogramming | function (strong) | macro token machinery is argument/parameter-list shaped to the ecosystem; the hand's J is a category. The `function` tag is honest shape but useless for the pack — this family belongs with the opacity rule (PCv5 log_002 §8.1) whatever the bucket; note the J dual is NOT auto-noted here (the token_* names miss the J name pattern — a name-bias example from the other side). |
| `token_repetition` | J metaprogramming | function (moderate) | see `token_binding_pattern` — same family, same comment. |
| `token_repetition_pattern` | J metaprogramming | function (moderate) | see `token_binding_pattern`. |
| `token_tree` | J metaprogramming | function (moderate) | see `token_binding_pattern`; log_002 records token_tree carries no grammatical structure at all, so the opacity rule owns it regardless. |
| `token_tree_pattern` | J metaprogramming | function (moderate) | see `token_binding_pattern`. |
| `trait_item` | E dispatch | function (moderate) | declaration family again: an interface is shaped as a declaration (E shape-invisible). Machine right as shape; E is the ledger-resolved dual. |
| `type_arguments` | F generics | function (moderate) | F is a category; the shape is a parameter-list over type-level items — log_015's F row says exactly this. Machine right as shape; F noted. |
| `type_parameters` | F generics | function (moderate) | as `type_arguments`. |
| `use_as_clause` | name | type-form (moderate) | machine moderate via an as-clause/alias cluster routed type-form; hand said `name`. Genuinely open — the row belongs to the import family, which the current anchors under-reach (§5). |
| `visibility_modifier` | declarative-form | function (moderate) | machine noise via the same weak 11-language cluster that pulls several modifier-ish rows toward `function`. Hand right (`declarative-form`). |

**The hand-open rows (42), grouped.** Where the hand hedged (UNCERTAIN/DUAL) and the machine committed: the container ruling resolves the hand's whole structural-container cluster the way log_015 P5 predicted (`source_file`, `declaration_list`, `enum_variant_list`, `ordered_field_declaration_list` → container-form, three of them strong); the declaration family absorbs the hand's name/value/record hesitations (`const_item`, `static_item`, `mod_item`, `enum_item`, `enum_variant`, `union_item`, `type_item`, `associated_type`, `extern_crate_declaration` → function — right as shape, with the sum-type caveat of log_015 §4 standing); the proof-form ruling takes `lifetime_parameter`, `mutable_specifier`, `for_lifetimes` (name-labeled, weak, exactly as the ruling intends); `let_condition` lands in pair per M3's own member list; and the import family rows (`use_list`, `use_wildcard`, `scoped_use_list`) go wrong or sideways — see §5. The eleven matches include `if_expression`/`else_clause` hand-choice confirmations and the literal family.

**The 33 hand-firm rows the machine leaves unanswered** are dominated by the expression tier (`await_expression`, `unary_expression`, `index_expression`, `return_expression`, …) — the machine refuses what only rust-lineage grammars share, while the hand tagged them from semantics the basis cannot corroborate. Those hand tags are probably RIGHT; the point of the instrument is that they are now visibly hand-ruled rather than machine-laundered.

## §5 The residue — the owner's review list (57 rows)

Five families account for nearly all of it: (1) the isolated expression tier (~20 rows — nearest counterparts are rust/sway/jakt only); (2) the `_pattern` family (~12 rows — D is a category, and the pattern shapes never meet the pair anchors under the guards); (3) the macro/attribute apparatus (`attribute`, `attribute_item`, `inner_attribute_item`, `macro_invocation`, `fragment_specifier` — J is a category; opacity rule territory); (4) the import family core (`use_declaration`, `use_bounds` — M1's rust members sit in leaf-statement shapes that never reach the include-flavored anchor; the two import proposals that DID fire, `qualified_type` and `higher_ranked_trait_bound`, are weak and almost certainly wrong — the import anchor needs a better pin before language two); (5) giant-absorbed and singleton kinds (`parameter`, `string_content`, `empty_statement`, … — swallowed by the 283/369-language blobs at t=0.40, where membership means nothing).

| kind | partial evidence | hand draft said (comparison only, NOT input) |
| --- | --- | --- |
| `array_expression` | name evidence (labeled): collection | collection |
| `async_block` | name evidence (labeled): container-form; name evidence (name only, unweighed): A suspension | A suspension |
| `attribute` | name evidence (name only, unweighed): J metaprogramming | declarative-form + J metaprogramming |
| `attribute_item` | name evidence (name only, unweighed): J metaprogramming | declarative-form + J metaprogramming |
| `await_expression` | name evidence (name only, unweighed): A suspension | A suspension |
| `base_field_initializer` | name evidence (labeled): record | record |
| `break_expression` | name evidence (labeled): repetition | repetition |
| `captured_pattern` | name evidence (name only, unweighed): D pattern matching | D pattern matching |
| `const_parameter` | name evidence (labeled): function | F generics |
| `continue_expression` | name evidence (labeled): repetition | repetition |
| `empty_statement` | — | sequence |
| `escape_sequence` | name evidence (labeled): sequence | value |
| `expression_statement` | — | sequence |
| `field_declaration` | name evidence (labeled): record | record |
| `field_expression` | name evidence (labeled): record | record |
| `field_pattern` | name evidence (labeled): record; name evidence (name only, unweighed): D pattern matching | D pattern matching |
| `fragment_specifier` | counterparts: name 1/10 | J metaprogramming |
| `gen_block` | name evidence (labeled): container-form | A suspension |
| `generic_function` | name evidence (labeled): function; counterparts: value 1/10; name evidence (name only, unweighed): F generics | F generics + function |
| `generic_pattern` | counterparts: D pattern matching 2/10; counterpart evidence: D pattern matching 2/10; name evidence (name only, unweighed): D pattern matching, F generics | D pattern matching + F generics |
| `index_expression` | name evidence (labeled): collection | collection |
| `inner_attribute_item` | name evidence (name only, unweighed): J metaprogramming | declarative-form + J metaprogramming |
| `let_chain` | — | choice + D pattern matching |
| `macro_invocation` | name evidence (name only, unweighed): J metaprogramming | J metaprogramming |
| `match_expression` | counterparts: repetition 1/10; name evidence (name only, unweighed): D pattern matching | D pattern matching + choice |
| `match_pattern` | name evidence (name only, unweighed): D pattern matching | D pattern matching |
| `mut_pattern` | name evidence (name only, unweighed): D pattern matching | D pattern matching + mutation |
| `negative_literal` | name evidence (labeled): value | value |
| `or_pattern` | name evidence (name only, unweighed): D pattern matching | D pattern matching |
| `parameter` | name evidence (labeled): function | function |
| `parenthesized_expression` | — | operation |
| `range_expression` | — | collection + operation |
| `reference_expression` | — | name |
| `reference_pattern` | name evidence (name only, unweighed): D pattern matching | D pattern matching |
| `remaining_field_pattern` | name evidence (labeled): record; counterparts: name 1/10; name evidence (name only, unweighed): D pattern matching | D pattern matching |
| `return_expression` | name evidence (labeled): function | function |
| `self_parameter` | name evidence (labeled): function | function + name |
| `shorthand_field_initializer` | name evidence (labeled): record | record |
| `slice_pattern` | name evidence (labeled): collection; name evidence (name only, unweighed): D pattern matching | D pattern matching + collection |
| `string_content` | name evidence (labeled): value | value |
| `struct_pattern` | name evidence (labeled): record; name evidence (name only, unweighed): D pattern matching | D pattern matching |
| `trait_bounds` | name evidence (name only, unweighed): E dispatch, F generics | E dispatch + F generics |
| `try_block` | name evidence (labeled): try, container-form | C optionals |
| `try_expression` | name evidence (labeled): try | C optionals |
| `tuple_expression` | name evidence (labeled): collection | record |
| `tuple_pattern` | name evidence (labeled): collection; counterparts: D pattern matching 1/10; counterpart evidence: D pattern matching 1/10; name evidence (name only, unweighed): D pattern matching | D pattern matching |
| `tuple_struct_pattern` | name evidence (labeled): record, collection; name evidence (name only, unweighed): D pattern matching | D pattern matching |
| `type_binding` | — | F generics + E dispatch |
| `type_cast_expression` | name evidence (labeled): operation | operation |
| `type_parameter` | name evidence (labeled): function; name evidence (name only, unweighed): F generics | F generics |
| `unary_expression` | name evidence (labeled): operation | operation |
| `unsafe_block` | name evidence (labeled): container-form | sequence |
| `use_bounds` | name evidence (labeled): import; name evidence (name only, unweighed): F generics | E dispatch + F generics |
| `use_declaration` | name evidence (labeled): import | name |
| `variadic_parameter` | name evidence (labeled): function | function |
| `where_clause` | name evidence (name only, unweighed): F generics | F generics + E dispatch |
| `yield_expression` | name evidence (name only, unweighed): A suspension | A suspension |

## §6 What language two costs

Running language two is one command (`python3 pack_generator.py <language>`) plus a review session; nothing in the generator reads rust-specific data — the anchors, band, guards and channels are ecosystem-level, and the ruled-addition pins are ecosystem clusters, not rust ones. Three honest caveats on “language-agnostic”: (a) the evidence-floor knobs (the four join guards, the 0.05 pooling margin, the counterpart floors, the purity gates) were TUNED on rust trial runs — they are documented constants, but their first contact with another roled grammar (c/cpp is the natural next) should re-examine them before the output is trusted at the same level; (b) the name patterns inherit basis_xref's English-centric regexes plus one documented deviation (`type_identifier` excluded from `name`), and the proof-form pattern is spelled in rust's own words (`lifetime`, `mutable_specifier`, …) — harmless for languages that lack the apparatus, load-bearing only for rust; (c) for zero-role grammars (kotlin and 25.3% of the ecosystem) the cluster channel under-fires by construction (log_015 §6), leaving counterpart votes and labeled name evidence to carry the map — P9's split-strategy warning is embodied in code paths that exist but got light exercise on rust. Also carried forward: the `interpolation` bucket currently has no admissible anchor and the `import` anchor is include-flavored — both worth re-pinning before a language where those families matter (python, typescript). Expected cost: minutes of compute, one review, no new code for roled grammars; possibly a counterpart-channel strengthening for the zero-role family.

## Sources

- PCHQ log_015 (basis report), log_016 (P-a definition), log_014 (spectrum); PCv5 log_008 (hand draft, comparison target), log_017 (q1); `ur.py` KINDS (ruled vocabulary, 2026-08-12).
- `basis_xref.py`/`basis_xref_out.json`, `spectrum_all.py`, `archetypes.json`, `top_counterparts_all.json`, `raw/rust.node-types.json` — the inputs; `pack_generator.py` — the mechanism; every number above is reproducible from them.
