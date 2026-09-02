# Clusters by language (reference threshold 0.40)

Rows = clusters discovered at the reference slice of the merge
tree; any other slice is a query (`spectrum.clusters_at(t)`).
Cohesion = mean within-cluster raw weighted-Jaccard similarity.
Band = threshold range [birth, death) over which this exact
member set is a maximal cluster in the merge tree; width in
parentheses. Singleton clusters are omitted (45 of them).

| cluster | cohesion | band (width) | rust | python | dart | c | cpp |
|---|---|---|---|---|---|---|---|
| s000 | 0.737 | 0.39-0.41 (0.02) | base_field_initializer, expression_statement, for_lifetimes, function_modifiers, where_clause | chevron, constrained_type, decorator, dictionary_splat, finally_clause, string_content, union_type, with_clause | argument_part, assertion, binary_operator, catch_clause, configurable_uri, configuration_uri, configuration_uri_condition, constant_constructor_signature, finally_clause, import_or_export, initialized_identifier_list, initializer_list_entry, initializers, library_export, library_import, library_name, method_signature, mixin_application, mixins, named_parameter_types, normal_parameter_type, optional_parameter_types, optional_positional_parameter_types, parameter_type_list, part_directive, part_of_directive, postfix_operator, prefix_operator, static_final_declaration_list, type_alias, type_bound, type_cast, type_parameter, type_test | alignas_qualifier, attribute_declaration, attribute_specifier, bitfield_clause, ms_based_modifier, ms_pointer_modifier, type_qualifier | alignas_qualifier, attribute_declaration, attribute_specifier, bitfield_clause, compound_requirement, explicit_function_specifier, field_initializer_list, ms_based_modifier, ms_pointer_modifier, noexcept, throw_specifier, trailing_return_type, type_qualifier |
| s001 | 0.950 | 0.30-0.42 (0.12) | empty_statement, escape_sequence, mutable_specifier, shebang, string_content | break_statement, continue_statement, escape_interpolation, escape_sequence, import_prefix, keyword_separator, pass_statement, positional_separator, string_end, string_start, wildcard_import | additive_operator, as_operator, bitwise_operator, case_builtin, const_builtin, equality_operator, escape_sequence, final_builtin, identifier_dollar_escaped, increment_operator, inferred_type, is_operator, minus_operator, multiplicative_operator, negation_operator, relational_operator, script_tag, shift_operator, tilde_operator | character, escape_sequence, gnu_asm_qualifier, ms_restrict_modifier, ms_signed_ptr_modifier, ms_unaligned_ptr_modifier, ms_unsigned_ptr_modifier, storage_class_specifier, string_content, variadic_parameter | access_specifier, auto, character, default_method_clause, delete_method_clause, escape_sequence, gnu_asm_qualifier, lambda_default_capture, literal_suffix, ms_call_modifier, ms_restrict_modifier, ms_signed_ptr_modifier, ms_unaligned_ptr_modifier, ms_unsigned_ptr_modifier, pure_virtual_clause, raw_string_content, ref_qualifier, storage_class_specifier, string_content, virtual_specifier |
| s002 | 0.730 | 0.40-0.46 (0.06) | block | unary_operator | — | alignof_expression, cast_expression, char_literal, compound_literal_expression, concatenated_string, extension_expression, false, field_expression, generic_expression, gnu_asm_expression, identifier, null, number_literal, offsetof_expression, parenthesized_expression, pointer_expression, sizeof_expression, string_literal, subscript_expression, true, unary_expression, update_expression | alignof_expression, cast_expression, char_literal, co_await_expression, compound_literal_expression, concatenated_string, delete_expression, extension_expression, false, field_expression, generic_expression, gnu_asm_expression, identifier, lambda_expression, null, number_literal, offsetof_expression, parameter_pack_expansion, parenthesized_expression, pointer_expression, raw_string_literal, requires_clause, requires_expression, sizeof_expression, string_literal, subscript_expression, this, true, unary_expression, update_expression, user_defined_literal |
| s003 | 0.716 | 0.38-0.41 (0.03) | array_expression, async_block, await_expression, boolean_literal, break_expression, char_literal, continue_expression, float_literal, gen_block, generic_function, identifier, index_expression, integer_literal, macro_invocation, metavariable, parenthesized_expression, range_expression, raw_string_literal, return_expression, self, string_literal, try_block, try_expression, tuple_expression, unary_expression, unit_expression, unsafe_block, yield_expression | as_pattern, attribute, await, comparison_operator, concatenated_string, conditional_expression, dictionary, dictionary_comprehension, ellipsis, false, float, generator_expression, identifier, integer, list, list_comprehension, list_splat, none, not_operator, parenthesized_expression, set, set_comprehension, string, true, tuple | — | — | — |
| s004 | 0.820 | 0.36-0.42 (0.06) | — | — | argument, assertion_arguments, assignable_expression, await_expression, cascade_selector, catch_parameters, combinator, conditional_assignable_selector, constructor_invocation, constructor_param, declaration, dotted_identifier_list, factory_constructor_signature, field_initializer, function_body, function_expression_body, identifier_list, import_specification, index_selector, initialized_identifier, label, mixin_application_class, mixin_declaration, module_name, named_argument, operator_signature, optional_formal_parameters, qualified, redirecting_factory_constructor_signature, redirection, static_final_declaration, super_formal_parameter, switch_label, template_substitution, typed_identifier, uri, uri_test | ms_declspec_modifier | base_class_clause, field_initializer, friend_declaration, ms_declspec_modifier, type_requirement, using_declaration |
| s005 | 0.711 | 0.39-0.50 (0.11) | trait_bounds | class_pattern, type_parameter | function_type, interfaces, type_arguments | abstract_array_declarator, abstract_parenthesized_declarator, abstract_pointer_declarator, array_declarator, attributed_declarator, declaration, parenthesized_declarator, pointer_declarator, type_descriptor | abstract_array_declarator, abstract_parenthesized_declarator, abstract_pointer_declarator, abstract_reference_declarator, array_declarator, attributed_declarator, new_declarator, parenthesized_declarator, pointer_declarator, reference_declarator, type_descriptor |
| s006 | 0.947 | 0.13-0.41 (0.28) | — | — | additive_expression, bitwise_and_expression, bitwise_or_expression, bitwise_xor_expression, cascade_section, const_object_expression, equality_expression, list_literal, logical_and_expression, logical_or_expression, multiplicative_expression, new_expression, parenthesized_expression, postfix_expression, relational_expression, selector, set_or_map_literal, shift_expression, symbol_literal, throw_expression, type_cast_expression, type_test_expression, unary_expression, unconditional_assignable_selector | — | — |
| s007 | 0.694 | 0.37-0.42 (0.05) | generic_pattern, label, self_parameter, shorthand_field_initializer, token_repetition, token_repetition_pattern, token_tree_pattern, tuple_pattern, type_parameters, use_list, use_wildcard, visibility_modifier | case_pattern, complex_pattern, dotted_name, generic_type, global_statement, keyword_pattern, member_type, nonlocal_statement, parenthesized_list_splat, splat_pattern, splat_type, union_pattern | — | — | — |
| s008 | 0.708 | 0.36-0.43 (0.07) | — | — | assert_statement, block, local_function_declaration, local_variable_declaration | attributed_statement, compound_statement, expression_statement, labeled_statement, return_statement | attributed_statement, co_return_statement, co_yield_statement, compound_statement, expression_statement, labeled_statement, return_statement, throw_statement |
| s009 | 0.780 | 0.39-0.59 (0.20) | declaration_list, enum_variant_list, field_declaration_list, field_initializer_list, match_block, ordered_field_declaration_list | — | class_body, enum_body, extension_body, switch_block | declaration_list, enumerator_list, field_declaration_list | declaration_list, enumerator_list, field_declaration_list |
| s010 | 0.919 | 0.29-0.45 (0.17) | doc_comment, fragment_specifier, inner_doc_comment_marker, outer_doc_comment_marker | type_conversion | — | preproc_arg, preproc_directive, statement_identifier, system_lib_string | preproc_arg, preproc_directive, statement_identifier, system_lib_string |
| s011 | 0.732 | 0.35-0.44 (0.09) | never_type, remaining_field_pattern, unit_type | — | type_identifier, void_type | field_identifier, ms_call_modifier, primitive_type, type_identifier | field_identifier, primitive_type, raw_string_delimiter |
| s012 | 0.770 | 0.35-0.54 (0.19) | — | — | do_statement, switch_statement, while_statement | do_statement, for_statement, switch_statement, while_statement | do_statement, for_statement, switch_statement, while_statement |
| s013 | 0.940 | 0.18-0.41 (0.22) | parameter, variadic_parameter | — | — | field_declaration, parameter_declaration, type_definition | field_declaration, optional_parameter_declaration, parameter_declaration, template_instantiation, type_definition, variadic_parameter_declaration |
| s014 | 0.866 | 0.26-0.41 (0.15) | — | — | decimal_floating_point_literal, decimal_integer_literal, false, hex_integer_literal, identifier, if_null_expression, null_literal, string_literal, super, this, true | — | — |
| s015 | 0.714 | 0.33-0.51 (0.19) | attribute_item, inner_attribute_item, use_declaration | assert_statement, decorated_definition, delete_statement, exec_statement, expression_statement, print_statement, raise_statement, return_statement | — | — | — |
| s016 | 0.753 | 0.34-0.48 (0.14) | assignment_expression, binary_expression, compound_assignment_expr | binary_operator, boolean_operator | — | assignment_expression, binary_expression | assignment_expression, binary_expression, fold_expression |
| s017 | 0.725 | 0.36-0.47 (0.11) | — | — | — | attribute, enumerator, macro_type_specifier, preproc_def, preproc_function_def | attribute, concept_definition, enumerator, preproc_def, preproc_function_def |
| s018 | 1.000 | 0.00-0.46 (0.46) | — | — | — | gnu_asm_clobber_list, gnu_asm_goto_list, gnu_asm_input_operand_list, gnu_asm_output_operand_list, subscript_range_designator | gnu_asm_clobber_list, gnu_asm_goto_list, gnu_asm_input_operand_list, gnu_asm_output_operand_list, subscript_range_designator |
| s019 | 0.759 | 0.39-0.50 (0.11) | captured_pattern, mut_pattern, or_pattern, ref_pattern, reference_pattern, slice_pattern, struct_pattern, tuple_struct_pattern | list_pattern, tuple_pattern | — | — | — |
| s020 | 0.729 | 0.33-0.42 (0.09) | abstract_type, array_type, dynamic_type, generic_type, pointer_type, reference_type | — | — | sized_type_specifier | placeholder_type_specifier, sized_type_specifier |
| s021 | 0.857 | 0.33-0.51 (0.18) | — | — | — | break_statement, continue_statement, goto_statement, seh_leave_statement | break_statement, continue_statement, goto_statement, seh_leave_statement |
| s022 | 0.839 | 0.33-0.43 (0.10) | — | — | break_statement, continue_statement, expression_statement, return_statement, spread_element, throw_expression_without_cascade, yield_each_statement, yield_statement | — | — |
| s023 | 0.821 | 0.28-0.58 (0.30) | — | — | — | enum_specifier, struct_specifier, union_specifier | class_specifier, enum_specifier, struct_specifier, union_specifier |
| s024 | 1.000 | 0.00-0.62 (0.62) | qualified_type | format_expression, interpolation | — | preproc_call, preproc_include | preproc_call, preproc_include |
| s025 | 0.717 | 0.34-0.40 (0.06) | const_item, enum_variant, extern_crate_declaration, function_signature_item, macro_definition, mod_item, static_item | — | — | — | — |
| s026 | 1.000 | 0.00-0.42 (0.42) | — | comment, line_continuation | comment, documentation_comment | comment | comment |
| s027 | 0.711 | 0.36-0.41 (0.05) | bracketed_type | relative_import | — | field_designator, subscript_designator | field_designator, subscript_designator |
| s028 | 0.829 | 0.35-0.55 (0.20) | — | — | — | gnu_asm_input_operand, gnu_asm_output_operand, init_declarator | gnu_asm_input_operand, gnu_asm_output_operand, init_declarator |
| s029 | 0.735 | 0.34-0.45 (0.11) | lifetime_parameter, token_binding_pattern, type_binding, type_parameter | — | — | — | alias_declaration, optional_type_parameter_declaration |
| s030 | 0.726 | 0.38-0.42 (0.04) | bounded_type, removed_trait_bound, tuple_type | if_clause | — | — | decltype, dependent_type |
| s031 | 0.725 | 0.38-0.50 (0.12) | — | format_specifier, slice | superclass | — | requirement_seq, subscript_argument_list, template_parameter_list |
| s032 | 0.783 | 0.30-0.43 (0.13) | — | — | enum_constant, formal_parameter, function_signature, getter_signature, marker_annotation, setter_signature | — | — |
| s033 | 0.855 | 0.25-0.41 (0.16) | associated_type, enum_item, struct_item, trait_item, type_item, union_item | — | — | — | — |
| s034 | 0.722 | 0.40-0.52 (0.12) | function_type | — | — | abstract_function_declarator, function_declarator | abstract_function_declarator, function_declarator |
| s035 | 0.748 | 0.33-0.46 (0.13) | call_expression | call | — | call_expression | call_expression, new_expression |
| s036 | 0.852 | 0.28-0.45 (0.17) | — | else_clause | — | seh_except_clause, seh_finally_clause | seh_except_clause, seh_finally_clause |
| s037 | 0.809 | 0.27-0.43 (0.16) | — | — | for_statement, try_statement | seh_try_statement | seh_try_statement, try_statement |
| s038 | 0.733 | 0.33-0.47 (0.15) | closure_parameters, parameters | lambda_parameters, parameters | — | — | parameter_list |
| s039 | 0.714 | 0.33-0.44 (0.11) | crate, primitive_type, super, type_identifier | — | — | — | type_identifier |
| s040 | 0.707 | 0.35-0.48 (0.13) | foreign_mod_item, impl_item | match_statement, try_statement, with_statement | — | — | — |
| s041 | 0.680 | 0.38-0.41 (0.04) | field_initializer, let_condition, match_arm | pair, with_item | — | — | — |
| s042 | 0.849 | 0.24-0.41 (0.17) | field_expression, match_expression, reference_expression, type_cast_expression | subscript | — | — | — |
| s043 | 0.892 | 0.15-0.69 (0.53) | — | — | — | preproc_elif, preproc_if | preproc_elif, preproc_if |
| s044 | 0.892 | 0.15-0.47 (0.32) | — | — | — | preproc_elifdef, preproc_ifdef | preproc_elifdef, preproc_ifdef |
| s045 | 0.725 | 0.37-0.53 (0.16) | — | — | — | preproc_else, translation_unit | preproc_else, translation_unit |
| s046 | 0.773 | 0.29-0.41 (0.12) | — | — | — | — | destructor_name, operator_name, structured_binding_declarator, variadic_declarator |
| s047 | 0.742 | 0.30-0.53 (0.23) | source_file | module | dimensions, throws | — | — |
| s048 | 0.794 | 0.24-0.53 (0.28) | const_block, for_expression, loop_expression, while_expression | — | — | — | — |
| s049 | 0.771 | 0.33-0.62 (0.29) | if_expression | — | — | conditional_expression | conditional_expression |
| s050 | 0.728 | 0.31-0.54 (0.24) | — | — | if_statement | if_statement | if_statement |
| s051 | 0.937 | 0.10-0.47 (0.38) | — | — | — | parameter_list, preproc_params | preproc_params |
| s052 | 0.721 | 0.31-0.41 (0.10) | type_arguments | — | — | — | dependent_name, lambda_capture_specifier |
| s053 | 0.802 | 0.30-0.42 (0.12) | field_declaration, field_pattern | — | — | — | namespace_alias_definition |
| s054 | 0.683 | 0.37-0.45 (0.09) | field_identifier, shorthand_field_identifier | — | — | — | namespace_identifier |
| s055 | 0.822 | 0.27-0.47 (0.20) | use_bounds | — | — | — | type_parameter_declaration, variadic_type_parameter_declaration |
| s056 | 0.775 | 0.25-0.46 (0.21) | — | — | class_definition, enum_declaration, extension_declaration | — | — |
| s057 | 0.711 | 0.36-0.50 (0.14) | function_item | class_definition, function_definition | — | — | — |
| s058 | 0.919 | 0.10-0.40 (0.30) | — | default_parameter, keyword_argument, typed_default_parameter | — | — | — |
| s059 | 0.786 | 0.28-0.42 (0.13) | — | dictionary_splat_pattern, list_splat_pattern, typed_parameter | — | — | — |
| s060 | 0.686 | 0.33-0.47 (0.14) | — | expression_list, type, yield | — | — | — |
| s061 | 0.839 | 0.24-0.42 (0.17) | — | future_import_statement, import_from_statement, import_statement | — | — | — |
| s062 | 0.810 | 0.29-0.46 (0.17) | higher_ranked_trait_bound, scoped_use_list, use_as_clause | — | — | — | — |
| s063 | 0.619 | 0.38-0.44 (0.06) | — | — | arguments | argument_list | — |
| s064 | 0.971 | 0.03-0.45 (0.42) | — | — | — | case_statement | case_statement |
| s065 | 0.893 | 0.11-0.48 (0.37) | — | — | — | comma_expression | comma_expression |
| s066 | 1.000 | 0.00-0.85 (0.85) | — | — | — | else_clause | else_clause |
| s067 | 0.857 | 0.14-0.43 (0.29) | — | — | — | function_definition | function_definition |
| s068 | 0.769 | 0.23-0.41 (0.18) | — | — | — | initializer_pair | initializer_pair |
| s069 | 0.957 | 0.04-0.60 (0.55) | — | — | — | linkage_specification | linkage_specification |
| s070 | 1.000 | 0.00-0.42 (0.42) | — | — | — | preproc_defined | preproc_defined |
| s071 | 0.743 | 0.26-0.42 (0.16) | — | — | — | — | argument_list, initializer_list |
| s072 | 0.812 | 0.19-0.45 (0.26) | — | — | lambda_expression | — | catch_clause |
| s073 | 1.000 | 0.00-0.57 (0.57) | — | — | — | — | constraint_conjunction, constraint_disjunction |
| s074 | 0.733 | 0.27-0.53 (0.26) | — | — | — | — | operator_cast, pointer_type_declarator |
| s075 | 0.771 | 0.23-0.50 (0.28) | — | — | — | — | qualified_identifier, template_function |
| s076 | 0.688 | 0.31-0.42 (0.11) | extern_modifier | — | — | — | simple_requirement |
| s077 | 0.833 | 0.17-0.44 (0.27) | arguments | — | — | — | template_argument_list |
| s078 | 0.636 | 0.36-0.52 (0.15) | — | — | — | — | template_declaration, template_template_parameter_declaration |
| s079 | 0.655 | 0.34-0.45 (0.11) | scoped_type_identifier | — | — | — | template_type |
| s080 | 0.810 | 0.19-0.51 (0.32) | — | — | assignment_expression, assignment_expression_without_cascade | — | — |
| s081 | 0.684 | 0.32-0.47 (0.16) | — | — | formal_parameter_list, type_parameters | — | — |
| s082 | 0.667 | 0.33-0.46 (0.13) | const_parameter | — | initialized_variable_definition | — | — |
| s083 | 0.741 | 0.26-0.45 (0.19) | — | assignment, augmented_assignment | — | — | — |
| s084 | 0.893 | 0.11-0.41 (0.31) | closure_expression | lambda | — | — | — |
| s085 | 0.769 | 0.23-0.41 (0.18) | scoped_identifier | named_expression | — | — | — |
| s086 | 0.667 | 0.33-0.45 (0.12) | macro_rule | type_alias_statement | — | — | — |
| s087 | 1.000 | 0.00-0.69 (0.69) | block_comment, line_comment | — | — | — | — |
