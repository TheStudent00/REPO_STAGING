# Operator inventory by arity

Read out of tree-sitter grammar sources. Every operator below is attributed to the grammar rule that admits it; nothing is filled in from memory. Regenerate with `python3 operator_arity.py`.

## Grammar versions used

| grammar file | repository | ref | path |
|---|---|---|---|
| `c.js` | tree-sitter/tree-sitter-c | `v0.24.2` | `grammar.js` |
| `c_for_cpp.js` | tree-sitter/tree-sitter-c | `v0.23.6` | `grammar.js` |
| `cpp.js` | tree-sitter/tree-sitter-cpp | `v0.23.4` | `grammar.js` |
| `rust.js` | tree-sitter/tree-sitter-rust | `v0.24.2` | `grammar.js` |
| `go.js` | tree-sitter/tree-sitter-go | `v0.25.0` | `grammar.js` |
| `swift.js` | alex-pinkus/tree-sitter-swift | `0.7.3` | `grammar.js` |
| `csharp.js` | tree-sitter/tree-sitter-c-sharp | `v0.23.5` | `grammar.js` |
| `java.js` | tree-sitter/tree-sitter-java | `v0.23.5` | `grammar.js` |
| `kotlin.js` | fwcd/tree-sitter-kotlin | `0.3.8` | `grammar.js` |
| `dart.js` | UserNobody14/tree-sitter-dart | `be07cf7118d3dba06236a3f19541685a68209934` | `grammar.js` |
| `javascript.js` | tree-sitter/tree-sitter-javascript | `v0.23.1` | `grammar.js` |
| `typescript.js` | tree-sitter/tree-sitter-typescript | `v0.23.2` | `common/define-grammar.js` |
| `php.js` | tree-sitter/tree-sitter-php | `v0.24.2` | `common/define-grammar.js` |
| `python.js` | tree-sitter/tree-sitter-python | `v0.25.0` | `grammar.js` |
| `ruby.js` | tree-sitter/tree-sitter-ruby | `v0.23.1` | `grammar.js` |

`c_for_cpp.js` is the C base that tree-sitter-cpp v0.23.4 builds on (it declares `tree-sitter-c: ^0.23.1`). tree-sitter-c `grammar.js` is byte-identical between v0.23.6 and v0.24.2, so the C and C++ rows rest on the same C text.

## Counts per bucket

| language | unary_prefix | unary_postfix | binary | assignment | ternary | structural | total |
|---|---|---|---|---|---|---|---|
| **cpp** | 14 | 3 | 25 | 14 | 1 | 8 | 65 |
| **rust** | 8 | 3 | 22 | 11 | 0 | 7 | 51 |
| **go** | 7 | 3 | 19 | 14 | 0 | 8 | 51 |
| **swift** | 16 | 5 | 28 | 6 | 1 | 5 | 61 |
| **c** | 15 | 2 | 18 | 11 | 1 | 9 | 56 |
| **csharp** | 10 | 3 | 24 | 13 | 1 | 10 | 61 |
| **java** | 6 | 2 | 20 | 12 | 1 | 8 | 49 |
| **kotlin** | 6 | 3 | 24 | 6 | 0 | 5 | 44 |
| **dart** | 9 | 3 | 24 | 14 | 1 | 8 | 59 |
| **typescript** | 13 | 3 | 27 | 16 | 1 | 7 | 67 |
| **php** | 16 | 2 | 30 | 15 | 1 | 7 | 71 |
| **python** | 8 | 0 | 27 | 15 | 1 | 5 | 56 |
| **ruby** | 9 | 0 | 27 | 14 | 1 | 5 | 56 |

Counts are distinct spellings per bucket. `++`/`--` appear in both the prefix and postfix rows where the grammar admits both. Open-set placeholders (`<custom_operator>`, `<simple_identifier>`) count as one each and are flagged in the per-language tables.

## Full spellings

### cpp

Grammar: tree-sitter/tree-sitter-cpp@v0.23.4 :: grammar.js; tree-sitter/tree-sitter-c@v0.23.6 :: grammar.js

| bucket | n | operators | admitting rule(s) |
|---|---|---|---|
| unary_prefix | 14 | `!` `~` `-` `+` `not` `compl` `*` `&` `++` `--` `sizeof` `co_await` `new` `delete` | unary_expression (`c_for_cpp.js`)<br>unary_expression (`cpp.js`)<br>pointer_expression (`c_for_cpp.js`)<br>update_expression (`c_for_cpp.js`)<br>sizeof_expression (`c_for_cpp.js`)<br>co_await_expression (`cpp.js`)<br>new_expression (`cpp.js`)<br>delete_expression (`cpp.js`) |
| unary_postfix | 3 | `++` `--` `...` | update_expression (`c_for_cpp.js`)<br>parameter_pack_expansion (`cpp.js`) |
| binary | 25 | `+` `-` `*` `/` `%` `\|\|` `&&` `\|` `^` `&` `==` `!=` `>` `>=` `<=` `<` `<<` `>>` `<=>` `or` `and` `bitor` `xor` `bitand` `not_eq` | binary_expression (`c_for_cpp.js`)<br>binary_expression (`cpp.js`) |
| assignment | 14 | `=` `*=` `/=` `%=` `+=` `-=` `<<=` `>>=` `&=` `^=` `\|=` `and_eq` `or_eq` `xor_eq` | assignment_expression (`cpp.js`) |
| ternary | 1 | `?:` | conditional_expression (`c_for_cpp.js`) |
| structural | 8 | `f(...)` `a[i]` `.` `.*` `->` `(T)x` `,` `(pack op ...)` | call_expression (`c_for_cpp.js`)<br>subscript_expression (`cpp.js`)<br>field_expression (`cpp.js`)<br>cast_expression (`c_for_cpp.js`)<br>comma_expression (`c_for_cpp.js`)<br>fold_expression (`cpp.js`) |

Notes:

- `unary_expression` (`c_for_cpp.js`): inherited from the C base grammar
- `unary_expression` (`cpp.js`): C++ override adds the alternative-token spellings
- `update_expression` (`c_for_cpp.js`): prefix arm
- `sizeof_expression` (`c_for_cpp.js`): the C++ override widens it: `($, original) => choice(original, seq('sizeof','...','(',identifier,')'))`, adding `sizeof...(pack)`
- `update_expression` (`c_for_cpp.js`): postfix arm
- `binary_expression` (`c_for_cpp.js`): reached through `original` in the C++ override
- `binary_expression` (`cpp.js`): C++ adds three-way comparison and the alternative tokens
- `assignment_expression` (`cpp.js`): ASSIGNMENT_OPERATORS module const
- `subscript_expression` (`cpp.js`): C++ widens the index to a subscript_argument_list (a[i, j])
- `fold_expression` (`cpp.js`): _unary_left_fold / _unary_right_fold / _binary_fold over FOLD_OPERATORS

Declaration-side annex (not counted above):

- `_fold_operator` (`cpp.js`), 38 spellings: `+` `-` `*` `/` `%` `^` `&` `\|` `=` `<` `>` `<<` `>>` `+=` `-=` `*=` `/=` `%=` `^=` `&=` `\|=` `>>=` `<<=` `==` `!=` `<=` `>=` `&&` `\|\|` `,` `.*` `->*` `or` `and` `bitor` `xor` `bitand` `not_eq`
  - the FOLD_OPERATORS table -- the operators that may appear inside a C++17 fold, not standalone expression operators
- `operator_name` (`cpp.js`), 51 spellings: `co_await` `+` `-` `*` `/` `%` `^` `&` `\|` `~` `!` `=` `<` `>` `+=` `-=` `*=` `/=` `%=` `^=` `&=` `\|=` `<<` `>>` `>>=` `<<=` `==` `!=` `<=` `>=` `<=>` `&&` `\|\|` `++` `--` `,` `->*` `->` `()` `[]` `xor` `bitand` `bitor` `compl` `not` `xor_eq` `and_eq` `or_eq` `not_eq` `and` `or`
  - the spellings that may follow the `operator` keyword in an overload declarator -- a declaration-side inventory, not an expression-side one. `->*` appears HERE and in the fold table but in NO expression rule of tree-sitter-cpp v0.23.4, so `a->*p` has no dedicated node kind in this grammar.

Operators with no counterpart elsewhere in the line:

- `<=>` -- three-way comparison
- `.*` -- member-through-object-pointer
- `and/or/xor/bitand/bitor/compl/not/not_eq/and_eq/or_eq/xor_eq` -- alternative tokens for the punctuation operators
- `co_await` -- coroutine await

### rust

Grammar: tree-sitter/tree-sitter-rust@v0.24.2 :: grammar.js

| bucket | n | operators | admitting rule(s) |
|---|---|---|---|
| unary_prefix | 8 | `-` `*` `!` `&` `&raw const` `&raw mut` `..` `..=` | unary_expression (`rust.js`)<br>reference_expression (`rust.js`)<br>range_expression (`rust.js`) |
| unary_postfix | 3 | `?` `..` `.await` | try_expression (`rust.js`)<br>range_expression (`rust.js`)<br>await_expression (`rust.js`) |
| binary | 22 | `&&` `\|\|` `&` `\|` `^` `==` `!=` `<` `<=` `>` `>=` `<<` `>>` `+` `-` `*` `/` `%` `..` `...` `..=` `as` | binary_expression (`rust.js`)<br>range_expression (`rust.js`)<br>type_cast_expression (`rust.js`) |
| assignment | 11 | `=` `+=` `-=` `*=` `/=` `%=` `&=` `\|=` `^=` `<<=` `>>=` | assignment_expression (`rust.js`)<br>compound_assignment_expr (`rust.js`) |
| ternary | 0 | _(none in this grammar)_ | - |
| structural | 7 | `f(...)` `a[i]` `.` `!` `::` `::<>` `\|...\|` | call_expression (`rust.js`)<br>index_expression (`rust.js`)<br>field_expression (`rust.js`)<br>macro_invocation (`rust.js`)<br>scoped_identifier (`rust.js`)<br>generic_function (`rust.js`)<br>closure_expression (`rust.js`) |

Notes:

- `reference_expression` (`rust.js`): seq('&', choice(seq('raw', choice('const', mutable_specifier)), optional(mutable_specifier)), value) -- the raw-reference forms are assembled from separate tokens
- `range_expression` (`rust.js`): prefix arm seq(choice('..','...','..='), expr) -- the grammar writes the choice once and reuses it in three arms
- `range_expression` (`rust.js`): postfix arm seq(expr, '..')
- `await_expression` (`rust.js`): prec(PREC.field, seq(expr, '.', 'await')) -- two tokens
- `range_expression` (`rust.js`): two-operand arm seq(expr, choice('..','...','..='), expr)
- `macro_invocation` (`rust.js`): m!(...) -- macro call
- `generic_function` (`rust.js`): turbofish
- `closure_expression` (`rust.js`): closure parameter list, delimited by '|'

Operators with no counterpart elsewhere in the line:

- `..` -- range (prefix, infix and postfix forms)
- `..=` -- inclusive range
- `?` -- postfix try
- `.await` -- postfix await
- `&raw const / &raw mut` -- raw reference

### go

Grammar: tree-sitter/tree-sitter-go@v0.25.0 :: grammar.js

| bucket | n | operators | admitting rule(s) |
|---|---|---|---|
| unary_prefix | 7 | `+` `-` `!` `^` `*` `&` `<-` | unary_expression (`go.js`) |
| unary_postfix | 3 | `++` `--` `...` | inc_statement (`go.js`)<br>dec_statement (`go.js`)<br>variadic_argument (`go.js`) |
| binary | 19 | `*` `/` `%` `<<` `>>` `&` `&^` `+` `-` `\|` `^` `==` `!=` `<` `<=` `>` `>=` `&&` `\|\|` | binary_expression (`go.js`) |
| assignment | 14 | `*=` `/=` `%=` `<<=` `>>=` `&=` `&^=` `+=` `-=` `\|=` `^=` `=` `:=` `<-` | assignment_statement (`go.js`)<br>short_var_declaration (`go.js`)<br>send_statement (`go.js`) |
| ternary | 0 | _(none in this grammar)_ | - |
| structural | 8 | `f(...)` `a[i]` `a[i:j]` `a[i:j:k]` `.` `x.(T)` `T(x)` `T[A]` | call_expression (`go.js`)<br>index_expression (`go.js`)<br>slice_expression (`go.js`)<br>selector_expression (`go.js`)<br>type_assertion_expression (`go.js`)<br>type_conversion_expression (`go.js`)<br>type_instantiation_expression (`go.js`) |

Notes:

- `binary_expression` (`go.js`): table over the module consts multiplicativeOperators, additiveOperators, comparativeOperators plus '&&' and '||'
- `assignment_statement` (`go.js`): assignmentOperators = multiplicative.concat(additive).map(o => o + '=').concat('=') -- built by string concatenation, so the compound spellings never appear as literals in the source
- `short_var_declaration` (`go.js`): declare-and-store
- `send_statement` (`go.js`): channel send; a store
- `type_instantiation_expression` (`go.js`): generic instantiation

Operators with no counterpart elsewhere in the line:

- `&^` -- bit clear (AND NOT); also &^= in the assignment set
- `:=` -- declare-and-store
- `<-` -- channel receive (prefix) and channel send (statement)

### swift

Grammar: alex-pinkus/tree-sitter-swift@0.7.3 :: grammar.js

| bucket | n | operators | admitting rule(s) |
|---|---|---|---|
| unary_prefix | 16 | `++` `--` `-` `+` `!` `&` `~` `.` `<custom_operator>` `try` `try?` `try!` `await` `consume` `..<` `...` | _prefix_unary_operator (`swift.js`)<br>try_operator (`swift.js`)<br>await_expression (`swift.js`)<br>consume_expression (`swift.js`)<br>open_start_range_expression (`swift.js`) |
| unary_postfix | 5 | `++` `--` `!` `?` `...` | _postfix_unary_operator (`swift.js`)<br>_expression (`swift.js`)<br>open_end_range_expression (`swift.js`) |
| binary | 28 | `*` `/` `%` `+` `-` `<` `>` `<=` `>=` `!=` `!==` `==` `===` `&` `\|` `^` `<<` `>>` `&&` `\|\|` `??` `..<` `...` `is` `as` `as?` `as!` `<custom_operator>` | _multiplicative_operator (`swift.js`)<br>_additive_operator (`swift.js`)<br>_comparison_operator (`swift.js`)<br>_equality_operator (`swift.js`)<br>_bitwise_binary_operator (`swift.js`)<br>_conjunction_operator (`swift.js`)<br>_disjunction_operator (`swift.js`)<br>_nil_coalescing_operator (`swift.js`)<br>_range_operator (`swift.js`)<br>check_expression (`swift.js`)<br>as_operator (`swift.js`)<br>infix_expression (`swift.js`) |
| assignment | 6 | `+=` `-=` `*=` `/=` `%=` `=` | _assignment_and_operator (`swift.js`) |
| ternary | 1 | `?:` | ternary_expression (`swift.js`) |
| structural | 5 | `f(...)` `a[i]` `.` `\\.` `#selector(...)` | value_arguments (`swift.js`)<br>navigation_suffix (`swift.js`)<br>key_path_expression (`swift.js`)<br>selector_expression (`swift.js`) |

Notes:

- `_prefix_unary_operator` (`swift.js`): '!' arrives as $.bang and '.' as $._dot, both external scanner tokens aliased back to their text form
- `_prefix_unary_operator` (`swift.js`): OPEN SET: $.custom_operator is a scanner-produced token, so user-defined prefix operators are admitted without being enumerated
- `try_operator` (`swift.js`): seq('try', choice(optional($._try_operator_type), ...)) where _try_operator_type is token.immediate('!')|token.immediate('?')
- `open_start_range_expression` (`swift.js`): _range_operator in prefix position
- `_postfix_unary_operator` (`swift.js`): '!' is $.bang, an external scanner token
- `_expression` (`swift.js`): seq($._expression, alias($._immediate_quest, '?')) -- optional unwrap/chain suffix
- `_equality_operator` (`swift.js`): '==' arrives as $._eq_eq (scanner token)
- `check_expression` (`swift.js`): $._is_operator
- `as_operator` (`swift.js`): choice($._as, $._as_quest, $._as_bang), scanner tokens aliased to 'as' / 'as?' / 'as!'
- `infix_expression` (`swift.js`): OPEN SET: seq(lhs, $.custom_operator, rhs). Swift's overflow operators &+ &- &* and every user-defined infix operator go through here; the grammar does NOT enumerate them.
- `_assignment_and_operator` (`swift.js`): '=' arrives as $._equal_sign -> alias($._eq_custom, '='). NOTE the grammar admits no &=, |=, ^=, <<=, >>=, &&=, ||=, ??=
- `ternary_expression` (`swift.js`): seq(condition, $._quest, if_true, ':', if_false)
- `value_arguments` (`swift.js`): one rule covers both paren call arguments and bracket subscript arguments
- `navigation_suffix` (`swift.js`): $._dot, scanner token aliased to '.'

Operators with no counterpart elsewhere in the line:

- `..<` -- half-open range
- `as? / as!` -- conditional and forced cast
- `try? / try!` -- optional and forced try
- `??` -- nil coalescing

### c

Grammar: tree-sitter/tree-sitter-c@v0.24.2 :: grammar.js

| bucket | n | operators | admitting rule(s) |
|---|---|---|---|
| unary_prefix | 15 | `!` `~` `-` `+` `*` `&` `++` `--` `sizeof` `__alignof__` `__alignof` `_alignof` `alignof` `_Alignof` `__extension__` | unary_expression (`c.js`)<br>pointer_expression (`c.js`)<br>update_expression (`c.js`)<br>sizeof_expression (`c.js`)<br>alignof_expression (`c.js`)<br>extension_expression (`c.js`) |
| unary_postfix | 2 | `++` `--` | update_expression (`c.js`) |
| binary | 18 | `+` `-` `*` `/` `%` `\|\|` `&&` `\|` `^` `&` `==` `!=` `>` `>=` `<=` `<` `<<` `>>` | binary_expression (`c.js`) |
| assignment | 11 | `=` `*=` `/=` `%=` `+=` `-=` `<<=` `>>=` `&=` `^=` `\|=` | assignment_expression (`c.js`) |
| ternary | 1 | `?:` | conditional_expression (`c.js`) |
| structural | 9 | `f(...)` `a[i]` `.` `->` `(T)x` `(T){...}` `,` `_Generic` `offsetof` | call_expression (`c.js`)<br>subscript_expression (`c.js`)<br>field_expression (`c.js`)<br>cast_expression (`c.js`)<br>compound_literal_expression (`c.js`)<br>comma_expression (`c.js`)<br>generic_expression (`c.js`)<br>offsetof_expression (`c.js`) |

Notes:

- `update_expression` (`c.js`): prefix arm of the choice(seq(op, arg), seq(arg, op))
- `extension_expression` (`c.js`): GNU extension marker
- `update_expression` (`c.js`): postfix arm
- `conditional_expression` (`c.js`): seq(condition, '?', optional(consequence), ':', alternative); the optional consequence also admits the GNU `a ?: b`

Operators with no counterpart elsewhere in the line:

- `_Generic` -- type-generic selection
- `?:` -- the GNU elided-middle form is admitted (optional consequence)

### csharp

Grammar: tree-sitter/tree-sitter-c-sharp@v0.23.5 :: grammar.js

| bucket | n | operators | admitting rule(s) |
|---|---|---|---|
| unary_prefix | 10 | `++` `--` `+` `-` `!` `~` `&` `^` `*` `await` | prefix_unary_expression (`csharp.js`)<br>_pointer_indirection_expression (`csharp.js`)<br>await_expression (`csharp.js`) |
| unary_postfix | 3 | `++` `--` `!` | postfix_unary_expression (`csharp.js`) |
| binary | 24 | `&&` `\|\|` `>>` `>>>` `<<` `&` `^` `\|` `+` `-` `*` `/` `%` `<` `<=` `==` `!=` `>=` `>` `??` `as` `is` `..` `with` | binary_expression (`csharp.js`)<br>as_expression (`csharp.js`)<br>is_expression (`csharp.js`)<br>range_expression (`csharp.js`)<br>with_expression (`csharp.js`) |
| assignment | 13 | `=` `+=` `-=` `*=` `/=` `%=` `&=` `^=` `\|=` `<<=` `>>=` `>>>=` `??=` | assignment_expression (`csharp.js`) |
| ternary | 1 | `?:` | conditional_expression (`csharp.js`) |
| structural | 10 | `f(...)` `a[i]` `.` `->` `?.` `?[` `(T)x` `switch` `sizeof` `default` | invocation_expression (`csharp.js`)<br>element_access_expression (`csharp.js`)<br>member_access_expression (`csharp.js`)<br>conditional_access_expression (`csharp.js`)<br>cast_expression (`csharp.js`)<br>switch_expression (`csharp.js`)<br>sizeof_expression (`csharp.js`)<br>default_expression (`csharp.js`) |

Notes:

- `prefix_unary_expression` (`csharp.js`): '^' here is the index-from-end operator ^1
- `postfix_unary_expression` (`csharp.js`): '!' is the null-forgiving operator
- `conditional_access_expression` (`csharp.js`): seq(expr, '?', choice(member_binding_expression, element_binding_expression))

Operators with no counterpart elsewhere in the line:

- `>>>` -- unsigned right shift; also >>>=
- `??=` -- null-coalescing assignment
- `^` -- index-from-end in prefix position
- `?.` -- null-conditional access
- `..` -- range
- `with` -- record copy-and-update

### java

Grammar: tree-sitter/tree-sitter-java@v0.23.5 :: grammar.js

| bucket | n | operators | admitting rule(s) |
|---|---|---|---|
| unary_prefix | 6 | `+` `-` `!` `~` `++` `--` | unary_expression (`java.js`)<br>update_expression (`java.js`) |
| unary_postfix | 2 | `++` `--` | update_expression (`java.js`) |
| binary | 20 | `>` `<` `>=` `<=` `==` `!=` `&&` `\|\|` `+` `-` `*` `/` `&` `\|` `^` `%` `<<` `>>` `>>>` `instanceof` | binary_expression (`java.js`)<br>instanceof_expression (`java.js`) |
| assignment | 12 | `=` `+=` `-=` `*=` `/=` `&=` `\|=` `^=` `%=` `<<=` `>>=` `>>>=` | assignment_expression (`java.js`) |
| ternary | 1 | `?:` | ternary_expression (`java.js`) |
| structural | 8 | `f(...)` `a[i]` `.` `(T)x` `::` `->` `new` `switch` | method_invocation (`java.js`)<br>array_access (`java.js`)<br>field_access (`java.js`)<br>cast_expression (`java.js`)<br>method_reference (`java.js`)<br>lambda_expression (`java.js`)<br>object_creation_expression (`java.js`)<br>switch_expression (`java.js`) |

Notes:

- `update_expression` (`java.js`): prefix arms
- `update_expression` (`java.js`): postfix arms
- `object_creation_expression` (`java.js`): literal 'new' sits in _unqualified_object_creation_expression

Operators with no counterpart elsewhere in the line:

- `>>>` -- unsigned right shift; also >>>=
- `::` -- method reference

### kotlin

Grammar: fwcd/tree-sitter-kotlin@0.3.8 :: grammar.js

| bucket | n | operators | admitting rule(s) |
|---|---|---|---|
| unary_prefix | 6 | `++` `--` `-` `+` `!` `*` | _prefix_unary_operator (`kotlin.js`)<br>spread_expression (`kotlin.js`) |
| unary_postfix | 3 | `++` `--` `!!` | _postfix_unary_operator (`kotlin.js`) |
| binary | 24 | `*` `/` `%` `+` `-` `<` `>` `<=` `>=` `!=` `!==` `==` `===` `&&` `\|\|` `?:` `..` `in` `!in` `is` `!is` `as` `as?` `<simple_identifier>` | _multiplicative_operator (`kotlin.js`)<br>_additive_operator (`kotlin.js`)<br>_comparison_operator (`kotlin.js`)<br>_equality_operator (`kotlin.js`)<br>conjunction_expression (`kotlin.js`)<br>disjunction_expression (`kotlin.js`)<br>elvis_expression (`kotlin.js`)<br>range_expression (`kotlin.js`)<br>_in_operator (`kotlin.js`)<br>_is_operator (`kotlin.js`)<br>_as_operator (`kotlin.js`)<br>infix_expression (`kotlin.js`) |
| assignment | 6 | `+=` `-=` `*=` `/=` `%=` `=` | _assignment_and_operator (`kotlin.js`)<br>assignment (`kotlin.js`) |
| ternary | 0 | _(none in this grammar)_ | - |
| structural | 5 | `f(...)` `a[i]` `.` `::` `?.` | call_suffix (`kotlin.js`)<br>_indexing_suffix (`kotlin.js`)<br>_member_access_operator (`kotlin.js`) |

Notes:

- `elvis_expression` (`kotlin.js`): binary elvis, NOT a ternary
- `infix_expression` (`kotlin.js`): OPEN SET: seq(lhs, $.simple_identifier, rhs). Kotlin's bitwise operations (and, or, xor, shl, shr, ushr, inv) are infix FUNCTIONS and reach the tree through here -- the grammar enumerates no bitwise operator tokens at all.
- `_member_access_operator` (`kotlin.js`): '?.' is alias($.safe_nav, '?.')

Operators with no counterpart elsewhere in the line:

- `?:` -- elvis (BINARY, not a ternary)
- `!!` -- postfix not-null assertion
- `as?` -- safe cast
- `!in / !is` -- negated containment / type test
- `?.` -- safe navigation

### dart

Grammar: UserNobody14/tree-sitter-dart@be07cf7118d3dba06236a3f19541685a68209934 :: grammar.js

| bucket | n | operators | admitting rule(s) |
|---|---|---|---|
| unary_prefix | 9 | `-` `!` `~` `++` `--` `await` `throw` `...` `...?` | prefix_operator (`dart.js`)<br>increment_operator (`dart.js`)<br>await_expression (`dart.js`)<br>throw_expression (`dart.js`)<br>spread_element (`dart.js`) |
| unary_postfix | 3 | `++` `--` `!` | postfix_operator (`dart.js`)<br>_exclamation_operator (`dart.js`) |
| binary | 24 | `*` `/` `%` `~/` `+` `-` `<<` `>>` `>>>` `&` `^` `\|` `<` `>` `<=` `>=` `==` `!=` `&&` `\|\|` `??` `is` `is!` `as` | _multiplicative_operator (`dart.js`)<br>_additive_operator (`dart.js`)<br>_shift_operator (`dart.js`)<br>_bitwise_operator (`dart.js`)<br>relational_operator (`dart.js`)<br>equality_operator (`dart.js`)<br>logical_and_operator (`dart.js`)<br>logical_or_operator (`dart.js`)<br>_if_null_expression (`dart.js`)<br>is_operator (`dart.js`)<br>as_operator (`dart.js`) |
| assignment | 14 | `=` `+=` `-=` `*=` `/=` `%=` `~/=` `<<=` `>>=` `>>>=` `&=` `^=` `\|=` `??=` | _assignment_operator (`dart.js`) |
| ternary | 1 | `?:` | conditional_expression (`dart.js`) |
| structural | 8 | `f(...)` `a[i]` `.` `?.` `?[` `..` `?..` `as` | argument_part (`dart.js`)<br>index_selector (`dart.js`)<br>unconditional_assignable_selector (`dart.js`)<br>conditional_assignable_selector (`dart.js`)<br>cascade_section (`dart.js`)<br>type_cast (`dart.js`) |

Notes:

- `prefix_operator` (`dart.js`): choice(minus_operator, negation_operator, tilde_operator)
- `increment_operator` (`dart.js`): prefix arm of unary_expression
- `spread_element` (`dart.js`): seq('...', optional('?'), expr) -- two tokens
- `postfix_operator` (`dart.js`): postfix_operator => $.increment_operator
- `_exclamation_operator` (`dart.js`): null assertion, reached through `selector`
- `is_operator` (`dart.js`): seq(token('is'), optional($._exclamation_operator)) -- two tokens
- `conditional_assignable_selector` (`dart.js`): seq('?', $.index_selector) -- assembled from '?' and '['

Operators with no counterpart elsewhere in the line:

- `??` -- if-null; also ??=
- `?.` -- conditional member access
- `..` -- cascade; '?..' is the null-aware cascade
- `~/` -- truncating division; also ~/=
- `...?` -- null-aware spread
- `!` -- postfix null assertion

### typescript

Grammar: tree-sitter/tree-sitter-typescript@v0.23.2 :: common/define-grammar.js; tree-sitter/tree-sitter-javascript@v0.23.1 :: grammar.js

| bucket | n | operators | admitting rule(s) |
|---|---|---|---|
| unary_prefix | 13 | `!` `~` `-` `+` `typeof` `void` `delete` `++` `--` `await` `new` `...` `<T>x` | unary_expression (`javascript.js`)<br>update_expression (`javascript.js`)<br>await_expression (`javascript.js`)<br>new_expression (`javascript.js`)<br>spread_element (`javascript.js`)<br>type_assertion (`typescript.js`) |
| unary_postfix | 3 | `++` `--` `!` | update_expression (`javascript.js`)<br>non_null_expression (`typescript.js`) |
| binary | 27 | `&&` `\|\|` `>>` `>>>` `<<` `&` `^` `\|` `+` `-` `*` `/` `%` `**` `<` `<=` `==` `===` `!=` `!==` `>=` `>` `??` `instanceof` `in` `as` `satisfies` | binary_expression (`javascript.js`)<br>as_expression (`typescript.js`)<br>satisfies_expression (`typescript.js`) |
| assignment | 16 | `=` `+=` `-=` `*=` `/=` `%=` `^=` `&=` `\|=` `>>=` `>>>=` `<<=` `**=` `&&=` `\|\|=` `??=` | assignment_expression (`javascript.js`)<br>augmented_assignment_expression (`javascript.js`) |
| ternary | 1 | `?:` | ternary_expression (`javascript.js`) |
| structural | 7 | `f(...)` `?.()` `a[i]` `.` `?.` `f<T>` `,` | call_expression (`typescript.js`)<br>subscript_expression (`javascript.js`)<br>member_expression (`javascript.js`)<br>optional_chain (`javascript.js`)<br>instantiation_expression (`typescript.js`)<br>sequence_expression (`javascript.js`) |

Notes:

- `update_expression` (`javascript.js`): prefix arms
- `type_assertion` (`typescript.js`): seq($.type_arguments, $.expression) -- the angle-bracket cast
- `update_expression` (`javascript.js`): postfix arms
- `ternary_expression` (`javascript.js`): seq(condition, alias($._ternary_qmark, '?'), consequence, ':', alternative)
- `call_expression` (`typescript.js`): TS override adds optional type_arguments to the call
- `sequence_expression` (`javascript.js`): prec.right(commaSep1($.expression))

Operators with no counterpart elsewhere in the line:

- `satisfies` -- type-conformance check (TS only)
- `??=` -- null-coalescing assignment
- `&&= / ||=` -- logical assignment
- `?.` -- optional chaining

### php

Grammar: tree-sitter/tree-sitter-php@v0.24.2 :: common/define-grammar.js

| bucket | n | operators | admitting rule(s) |
|---|---|---|---|
| unary_prefix | 16 | `+` `-` `~` `!` `++` `--` `@` `clone` `print` `include` `include_once` `require` `require_once` `yield` `yield from` `...` | unary_op_expression (`php.js`)<br>update_expression (`php.js`)<br>error_suppression_expression (`php.js`)<br>clone_expression (`php.js`)<br>print_intrinsic (`php.js`)<br>include_expression (`php.js`)<br>include_once_expression (`php.js`)<br>require_expression (`php.js`)<br>require_once_expression (`php.js`)<br>yield_expression (`php.js`)<br>variadic_unpacking (`php.js`) |
| unary_postfix | 2 | `++` `--` | update_expression (`php.js`) |
| binary | 30 | `instanceof` `??` `**` `and` `or` `xor` `\|\|` `&&` `\|` `^` `&` `==` `!=` `<>` `===` `!==` `<` `>` `<=` `>=` `<=>` `\|>` `.` `<<` `>>` `+` `-` `*` `/` `%` | binary_expression (`php.js`) |
| assignment | 15 | `=` `=&` `**=` `*=` `/=` `%=` `+=` `-=` `.=` `<<=` `>>=` `&=` `^=` `\|=` `??=` | assignment_expression (`php.js`)<br>reference_assignment_expression (`php.js`)<br>augmented_assignment_expression (`php.js`) |
| ternary | 1 | `?:` | conditional_expression (`php.js`) |
| structural | 7 | `f(...)` `a[i]` `->` `?->` `::` `(int)x` `match` | function_call_expression (`php.js`)<br>_dereferencable_subscript_expression (`php.js`)<br>member_access_expression (`php.js`)<br>nullsafe_member_access_expression (`php.js`)<br>class_constant_access_expression (`php.js`)<br>cast_expression (`php.js`)<br>match_expression (`php.js`) |

Notes:

- `update_expression` (`php.js`): prefix arm
- `update_expression` (`php.js`): postfix arm
- `binary_expression` (`php.js`): '|>' is the PHP 8.5 pipe operator; '.' is string concatenation
- `reference_assignment_expression` (`php.js`): seq(left, '=', '&', right) -- two tokens
- `conditional_expression` (`php.js`): seq(condition, '?', optional(body), ':', alternative) -- the optional body is the short ternary `a ?: b`
- `_dereferencable_subscript_expression` (`php.js`): aliased to `subscript_expression`
- `cast_expression` (`php.js`): cast_type enumerates array/binary/bool/boolean/double/float/int/integer/object/real/string/unset

Operators with no counterpart elsewhere in the line:

- `<=>` -- spaceship comparison
- `??` -- null coalescing; also ??=
- `?->` -- nullsafe member access
- `|>` -- pipe (PHP 8.5)
- `<>` -- legacy inequality
- `@` -- error suppression
- `.` -- string concatenation (binary), also .=

### python

Grammar: tree-sitter/tree-sitter-python@v0.25.0 :: grammar.js

| bucket | n | operators | admitting rule(s) |
|---|---|---|---|
| unary_prefix | 8 | `+` `-` `~` `not` `await` `*` `**` `lambda` | unary_operator (`python.js`)<br>not_operator (`python.js`)<br>await (`python.js`)<br>list_splat (`python.js`)<br>dictionary_splat (`python.js`)<br>lambda (`python.js`) |
| unary_postfix | 0 | _(none in this grammar)_ | - |
| binary | 27 | `+` `-` `*` `@` `/` `%` `//` `**` `\|` `&` `^` `<<` `>>` `and` `or` `<` `<=` `==` `!=` `>=` `>` `<>` `in` `not in` `is` `is not` `as` | binary_operator (`python.js`)<br>boolean_operator (`python.js`)<br>comparison_operator (`python.js`)<br>as_pattern (`python.js`) |
| assignment | 15 | `=` `+=` `-=` `*=` `/=` `@=` `//=` `%=` `**=` `>>=` `<<=` `&=` `^=` `\|=` `:=` | assignment (`python.js`)<br>augmented_assignment (`python.js`)<br>named_expression (`python.js`) |
| ternary | 1 | `if-else` | conditional_expression (`python.js`) |
| structural | 5 | `f(...)` `a[i]` `.` `a[i:j]` `a[i:j:k]` | call (`python.js`)<br>subscript (`python.js`)<br>attribute (`python.js`)<br>slice (`python.js`) |

Notes:

- `binary_operator` (`python.js`): '@' is matrix multiplication
- `comparison_operator` (`python.js`): '<>' is the Python-2 inequality; 'not in'/'is not' arrive as aliased hidden tokens
- `assignment` (`python.js`): seq(left, choice(seq('=', right), seq(':', type), seq(':', type, '=', right))) -- the ':' arm is the annotated form
- `named_expression` (`python.js`): walrus
- `conditional_expression` (`python.js`): seq(expression, 'if', expression, 'else', expression) -- Python spells its ternary with keywords, not ?:
- `slice` (`python.js`): seq(optional(expr), ':', optional(expr), optional(seq(':', optional(expr))))

Operators with no counterpart elsewhere in the line:

- `//` -- floor division; also //=
- `@` -- matrix multiplication; also @=
- `:=` -- walrus
- `<>` -- Python-2 inequality, still admitted by the grammar
- `if-else` -- the ternary, spelled with keywords

### ruby

Grammar: tree-sitter/tree-sitter-ruby@v0.23.1 :: grammar.js

| bucket | n | operators | admitting rule(s) |
|---|---|---|---|
| unary_prefix | 9 | `defined?` `not` `-` `+` `!` `~` `*` `**` `&` | unary (`ruby.js`)<br>command_unary (`ruby.js`)<br>splat_argument (`ruby.js`)<br>hash_splat_argument (`ruby.js`)<br>block_argument (`ruby.js`) |
| unary_postfix | 0 | _(none in this grammar)_ | - |
| binary | 27 | `and` `or` `\|\|` `&&` `<<` `>>` `<` `<=` `>` `>=` `&` `^` `\|` `+` `-` `/` `%` `*` `==` `!=` `===` `<=>` `=~` `!~` `**` `..` `...` | binary (`ruby.js`)<br>range (`ruby.js`) |
| assignment | 14 | `=` `+=` `-=` `*=` `**=` `/=` `\|\|=` `\|=` `&&=` `&=` `%=` `>>=` `<<=` `^=` | assignment (`ruby.js`)<br>operator_assignment (`ruby.js`)<br>command_operator_assignment (`ruby.js`) |
| ternary | 1 | `?:` | conditional (`ruby.js`) |
| structural | 5 | `f(...)` `.` `&.` `::` `a[i]` | call (`ruby.js`)<br>_call_operator (`ruby.js`)<br>element_reference (`ruby.js`) |

Notes:

- `unary` (`ruby.js`): '-' arrives as _unary_minus / _binary_minus aliased back to '-'
- `command_unary` (`ruby.js`): same operator set in command (paren-less) position
- `splat_argument` (`ruby.js`): alias($._splat_star, '*')
- `binary` (`ruby.js`): '-', '*', '**' arrive as _binary_minus / _binary_star / _binary_star_star aliased back to their text form
- `command_operator_assignment` (`ruby.js`): command (paren-less) position
- `_call_operator` (`ruby.js`): choice('.', '&.', token.immediate('::'))
- `element_reference` (`ruby.js`): alias($._element_reference_bracket, '[')

Declaration-side annex (not counted above):

- `operator` (`ruby.js`), 30 spellings: `..` `\|` `^` `&` `<=>` `==` `===` `=~` `>` `>=` `<` `<=` `+` `!=` `-` `*` `/` `%` `!` `!~` `**` `<<` `>>` `~` `+@` `-@` `~@` `[]` `[]=` ```
  - the spellings that may be DEFINED as a method name (`def <op>`) -- a declaration-side inventory, not an expression-side one. `+@`/`-@`/`~@` are the unary forms and `[]`/`[]=` the index read/write forms.

Operators with no counterpart elsewhere in the line:

- `=~` -- regexp match
- `!~` -- negated regexp match
- `<=>` -- spaceship comparison
- `&.` -- safe navigation
- `defined?` -- definedness test
- `===` -- case-equality
- `||= / &&=` -- conditional stores

## Census coverage (space_<lang>.json `operations`)

| language | census n | grammar binary n | covered | missed | in census but not in the grammar binary bucket |
|---|---|---|---|---|---|
| **cpp** | 19 | 25 | 19 (76%) | `or` `and` `bitor` `xor` `bitand` `not_eq` | - |
| **rust** | 19 | 22 | 19 (86%) | `...` `..=` `as` | - |
| **go** | 19 | 19 | 19 (100%) | - | - |
| **swift** | 6 | 27 | 6 (22%) | `/` `%` `+` `-` `<=` `!=` `!==` `==` `===` `&` `\|` `^` `<<` `>>` `??` `..<` `...` `is` `as` `as?` `as!` | - |
| **c** | _no space_c.json_ | 18 | 0 | 18 | - |
| **csharp** | 20 | 24 | 20 (83%) | `>>>` `as` `..` `with` | - |
| **java** | 20 | 20 | 20 (100%) | - | - |
| **kotlin** | 17 | 23 | 16 (70%) | `!==` `===` `!in` `is` `!is` `as` `as?` | `&` |
| **dart** | 17 | 24 | 17 (71%) | `+` `-` `>>>` `!=` `is` `is!` `as` | - |
| **typescript** | 23 | 27 | 23 (85%) | `>>>` `instanceof` `as` `satisfies` | - |
| **php** | _no space_php.json_ | 30 | 0 | 30 | - |
| **python** | _no space_python.json_ | 27 | 0 | 27 | - |
| **ruby** | _no space_ruby.json_ | 27 | 0 | 27 | - |

No `space_<lang>.json` exists at all for: `c`, `php`, `python`, `ruby` -- those languages have no behaviour census to compare against, so their whole binary bucket is unreached rather than partially reached.

The census `operations` lists are binary-operator lists, so they are compared against the `binary` bucket only. The last column is not an error in the census: it holds operators the census exercised that this table files under another bucket (or that the grammar admits only through an open-set rule).
