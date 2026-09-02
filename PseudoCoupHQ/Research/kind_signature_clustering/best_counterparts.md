# Best counterparts — readable slice

Full population is in `best_counterparts.json` (every one of the
800 kinds, its nearest counterpart in each other language).
Similarity = co-cluster fraction across the threshold spectrum.

## 20 highest cross-language pairs

| similarity | raw | kind A | kind B |
|---|---|---|---|
| 1.000 | 1.000 | c:abstract_array_declarator | cpp:abstract_array_declarator |
| 1.000 | 1.000 | c:abstract_array_declarator | cpp:abstract_pointer_declarator |
| 1.000 | 1.000 | c:abstract_array_declarator | cpp:array_declarator |
| 1.000 | 1.000 | c:abstract_array_declarator | cpp:pointer_declarator |
| 1.000 | 1.000 | c:abstract_pointer_declarator | cpp:abstract_array_declarator |
| 1.000 | 1.000 | c:abstract_pointer_declarator | cpp:abstract_pointer_declarator |
| 1.000 | 1.000 | c:abstract_pointer_declarator | cpp:array_declarator |
| 1.000 | 1.000 | c:abstract_pointer_declarator | cpp:pointer_declarator |
| 1.000 | 1.000 | c:alignas_qualifier | cpp:alignas_qualifier |
| 1.000 | 1.000 | c:alignof_expression | cpp:alignof_expression |
| 1.000 | 1.000 | c:alignof_expression | cpp:offsetof_expression |
| 1.000 | 1.000 | c:alignof_expression | cpp:parameter_pack_expansion |
| 1.000 | 1.000 | c:alignof_expression | cpp:requires_clause |
| 1.000 | 1.000 | c:alignof_expression | cpp:subscript_expression |
| 1.000 | 1.000 | c:array_declarator | cpp:abstract_array_declarator |
| 1.000 | 1.000 | c:array_declarator | cpp:abstract_pointer_declarator |
| 1.000 | 1.000 | c:array_declarator | cpp:array_declarator |
| 1.000 | 1.000 | c:array_declarator | cpp:pointer_declarator |
| 1.000 | 1.000 | c:attribute_declaration | cpp:attribute_declaration |
| 1.000 | 1.000 | c:attribute_declaration | cpp:field_initializer_list |

1654 cross-language pairs saturate at similarity ~1.0 (383 of them c<->cpp twins from near-identical shipped grammars; the rest are identical-featured weak-sub-node-spec kinds that merge at height 0).

## 20 highest NON-saturated cross-language pairs

| similarity | raw | kind A | kind B |
|---|---|---|---|
| 0.981 | 0.981 | c:preproc_elif | cpp:preproc_elif |
| 0.981 | 0.981 | c:preproc_elifdef | cpp:preproc_elifdef |
| 0.981 | 0.981 | c:preproc_if | cpp:preproc_if |
| 0.981 | 0.981 | c:preproc_ifdef | cpp:preproc_ifdef |
| 0.980 | 0.980 | c:parenthesized_expression | cpp:parenthesized_expression |
| 0.974 | 0.974 | c:conditional_expression | cpp:conditional_expression |
| 0.971 | 0.971 | c:case_statement | cpp:case_statement |
| 0.963 | 0.963 | c:labeled_statement | cpp:labeled_statement |
| 0.962 | 0.962 | c:concatenated_string | cpp:user_defined_literal |
| 0.962 | 0.962 | c:compound_statement | cpp:compound_statement |
| 0.958 | 0.958 | c:cast_expression | cpp:sizeof_expression |
| 0.958 | 0.958 | c:for_statement | cpp:for_statement |
| 0.958 | 0.958 | c:sizeof_expression | cpp:cast_expression |
| 0.957 | 0.957 | c:linkage_specification | cpp:linkage_specification |
| 0.957 | 0.957 | python:parenthesized_expression | rust:async_block |
| 0.957 | 0.957 | python:parenthesized_expression | rust:gen_block |
| 0.957 | 0.957 | python:parenthesized_expression | rust:try_block |
| 0.957 | 0.957 | python:parenthesized_expression | rust:unsafe_block |
| 0.956 | 0.956 | c:char_literal | cpp:generic_expression |
| 0.956 | 0.956 | c:generic_expression | cpp:char_literal |

## 10 most isolated kinds

No counterpart above the stated similarity anywhere — reported,
not hidden.

| kind | best cross-language similarity | best counterpart |
|---|---|---|
| dart:explicit_constructor_invocation | 0.016 | rust:call_expression |
| python:case_clause | 0.135 | rust:match_pattern |
| python:elif_clause | 0.135 | rust:match_pattern |
| python:if_statement | 0.135 | rust:match_pattern |
| rust:match_pattern | 0.154 | c:else_clause |
| rust:let_declaration | 0.221 | python:except_clause |
| rust:attribute | 0.244 | python:splat_type |
| rust:let_chain | 0.281 | python:lambda_parameters |
| rust:block_comment | 0.307 | python:format_expression |
| rust:line_comment | 0.307 | python:format_expression |
