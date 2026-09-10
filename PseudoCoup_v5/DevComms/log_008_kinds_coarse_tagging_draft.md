# log 008 — coarse tagging draft: rust named kinds -> the 21 intention buckets

2026-08-05. A DRAFT FOR DEE'S REVIEW, produced on request.

**What this is.** A proposed coarse tag for every one of the 163 named
kinds of the pinned `tree-sitter-rust` grammar, drawn from the validated
intentions artifact at
`PRIVATE/PseudoIR/Tools/intentions/pc_intentions.json` — its
`minimum_set` (11 universal objects) and its `intent_categories` (10
differentiator categories A-J), 21 buckets in all, plus two PROPOSED new
buckets argued for below. It serves
`PRIVATE/PseudoCoup_v5/DevComms/log_006_ur_kinds_vocabulary.md`
item 3 (what `ur_kind` classifies) and item 5 (the mechanical seed at
language one): the proposal is that the coarse layer of `ur_kind` is
these buckets rather than the grammar's five supertype families, and the
fine layer stays the grammar's own kinds.

**What this is NOT.** Not a settled vocabulary, and nothing here is
decided. Rows that plausibly carry two buckets record BOTH and are
flagged DUAL — log_006 leaves the exclusive-vs-primary question open and
this draft does not close it. Rows I am not confident in are flagged
UNCERTAIN and gathered in one section with what would resolve each.

**Method.** Kinds enumerated live from the compiled `Language` object
(`tree-sitter==0.26.0`, `tree-sitter-rust==0.24.2`): 163 named and
visible kinds, matching log_002 §3. The grammar's own `supertypes` /
`subtypes` tables were read as prior classification evidence — the
grammar author's five families `_expression` (40), `_type` (33),
`_pattern` (18), `_literal_pattern` (7), `_literal` (6). `node-types.json`
is NOT shipped in the Python wheel (checked: the wheel contains only the
binding, the `.so` and `queries/`), so the runtime API plus the grammar's
field names are the evidence used, alongside the intentions data's own
descriptions and its `t1_realizations` Rust cells. No row is assigned on
name resemblance.

One consequence of reading the supertype tables worth stating up front:
`macro_invocation` is simultaneously a sub-type of `_expression`,
`_pattern` AND `_type`, and `const_block` of both `_expression` and
`_pattern`. So position in the grammar cannot by itself decide a bucket.

---

## summary — kinds per bucket

Rows with two buckets are counted once under each, so the column sums to
more than 163.

| bucket | tier | count |
| --- | --- | --- |
| value | minimum_set | 13 |
| name | minimum_set | 20 |
| operation | minimum_set | 6 |
| sequence | minimum_set | 7 |
| choice | minimum_set | 5 |
| repetition | minimum_set | 6 |
| function | minimum_set | 13 |
| record | minimum_set | 16 |
| collection | minimum_set | 5 |
| mutation | minimum_set | 5 |
| service call | minimum_set | 2 |
| A suspension | category | 5 |
| B channels | category | 0 |
| C optionals | category | 2 |
| D pattern matching | category | 20 |
| E dispatch | category | 15 |
| F generics | category | 18 |
| G scoped cleanup | category | 0 |
| H events | category | 1 |
| I operator overloading | category | 0 |
| J metaprogramming | category | 14 |
| type-form (PROPOSED) | PROPOSED | 19 |
| declarative-form (PROPOSED) | PROPOSED | 13 |
| **total rows** | | **163** |

Flag totals: 42 rows flagged DUAL, 37 rows flagged UNCERTAIN (13 carry both), 97 rows unflagged.

---

## the full table

| kind | proposed bucket(s) | justification | flag |
| --- | --- | --- | --- |
| `abstract_type` | type-form (PROPOSED) + E dispatch | `impl Trait` in type position: bare type syntax, but its content is a trait bound, which is category E's object. | DUAL, UNCERTAIN |
| `arguments` | function | The grammar's `arguments` field of `call_expression`; it exists only as the argument list of a call. | — |
| `array_expression` | collection | Constructs an ordered many (`[a, b, c]` / `[v; n]`) — minimum-set object 9. | — |
| `array_type` | type-form (PROPOSED) + collection | A `_type` sub-type by the grammar's own supertype table; denotes a collection type rather than building one. | DUAL |
| `assignment_expression` | mutation | `left = right` writes to an existing name or field — minimum-set object 10 exactly. | — |
| `associated_type` | E dispatch + type-form (PROPOSED) | Only occurs inside `trait_item`/`impl_item` bodies; it is part of an interface's shape, spelled as type syntax. | DUAL |
| `async_block` | A suspension | `async { }` builds a Future value; t1_realizations A/Rust: "async compiles to a state-machine VALUE (Future); inert until polled". | — |
| `attribute` | declarative-form (PROPOSED) + J metaprogramming | The inner content of `#[...]`; non-executing annotation, but `derive`/proc-macro attributes are the J realization in Rust. | DUAL, UNCERTAIN |
| `attribute_item` | declarative-form (PROPOSED) + J metaprogramming | Outer `#[...]` applied to an item; same dual reading as `attribute`, at item granularity. | DUAL, UNCERTAIN |
| `await_expression` | A suspension | `.await` is the suspension point itself — category A's defining syntax. | — |
| `base_field_initializer` | record | `..base` inside `field_initializer_list`: fills remaining named fields of a record literal. | — |
| `binary_expression` | operation | Arithmetic, comparison and logic on two values — minimum-set object 3's description verbatim. | — |
| `block` | sequence | "do this, then that": an ordered run of statements. Also an `_expression` sub-type in Rust, which is a value-position fact, not a different object. | — |
| `block_comment` | declarative-form (PROPOSED) | Extra (`is_extra`), never executes, carries no object of either tier. | — |
| `boolean_literal` | value | A literal bool — minimum-set object 1 ("number, boolean, byte, text"). | — |
| `bounded_type` | F generics + E dispatch | `T: Trait` — a type parameter constrained by a trait: parameterization by type whose constraint is an interface. | DUAL |
| `bracketed_type` | type-form (PROPOSED) | Pure syntax wrapper around a type in qualified paths; contributes no object. | — |
| `break_expression` | repetition | Exits a loop (optionally with a value and a label); its only legal context is a loop body. | — |
| `call_expression` | function | "a parameterized block; call and return" — the call half of minimum-set object 7. | — |
| `captured_pattern` | D pattern matching | `name @ pattern` — a pattern-only construct, in the grammar's `_pattern` supertype set. | — |
| `char_literal` | value | A literal character — minimum-set object 1. | — |
| `closure_expression` | function + H events | A function as a value ("a function IS a value", minimum-set amendment); closures are also the Rust realization of callbacks in the H row. | DUAL, UNCERTAIN |
| `closure_parameters` | function | The parameter list of a closure; exists only inside `closure_expression`. | — |
| `compound_assignment_expr` | mutation + operation | `x += 1` both writes a name (object 10) and performs arithmetic (object 3). The exclusive-vs-primary ruling is open in log_006. | DUAL |
| `const_block` | J metaprogramming + value | `const { ... }` is compile-time evaluation producing a value — codegen-time work, closest to J; the min set has no compile-time-execution object. | DUAL, UNCERTAIN |
| `const_item` | name + value | Binds a written identifier to a constant value — object 2, with object 1 as the thing bound. | DUAL |
| `const_parameter` | F generics | `const N: usize` in `type_parameters`: parameterization of a type by a value, still the generics machinery. | — |
| `continue_expression` | repetition | Restarts a loop iteration; legal only inside a loop. | — |
| `crate` | name | A path root token appearing inside `scoped_identifier`/`scoped_use_list` — a name component. | — |
| `declaration_list` | sequence | The `body` of `mod_item` and `impl_item`: an ordered run of declarations. | UNCERTAIN |
| `doc_comment` | declarative-form (PROPOSED) | Extra; documentation text, no runtime object. | — |
| `dynamic_type` | E dispatch + type-form (PROPOSED) | `dyn Trait` is runtime dispatch through a trait object — E's object, spelled in type position. | DUAL |
| `else_clause` | choice | The alternative arm of `if_expression` — the second half of minimum-set object 5. | — |
| `empty_statement` | sequence | A bare `;` occupying a statement slot; contributes position in a sequence and nothing else. NONE is defensible. | UNCERTAIN |
| `enum_item` | record + D pattern matching | A sum type. The minimum set has `record` for products only; enums are named-variant data whose consumer is `match`. | DUAL, UNCERTAIN |
| `enum_variant` | record | One variant, optionally with fields — a named grouping of values. | UNCERTAIN |
| `enum_variant_list` | record | The `body` of `enum_item`; container of variants. | UNCERTAIN |
| `escape_sequence` | value | A sub-node of string/char literals; part of the literal's text value. | — |
| `expression_statement` | sequence | Wraps an expression into a statement slot — the "then that" of object 4. | — |
| `extern_crate_declaration` | name | Binds an external crate's name into the current namespace. | UNCERTAIN |
| `extern_modifier` | declarative-form (PROPOSED) + service call | `extern "C"`: a non-executing ABI annotation, but it marks the boundary to the platform, which is object 11's territory. | DUAL, UNCERTAIN |
| `field_declaration` | record | `name: Type` inside `field_declaration_list` — "values grouped under named fields", object 8. | — |
| `field_declaration_list` | record | The braced field block of a struct/union — object 8's container. | — |
| `field_expression` | record | `value.field` reads a named field off a record. | — |
| `field_identifier` | name | The identifier naming a field, in `field:` positions throughout. | — |
| `field_initializer` | record | `field: value` in a struct literal. | — |
| `field_initializer_list` | record | The braced body of `struct_expression`. | — |
| `field_pattern` | D pattern matching | Only occurs inside `struct_pattern`; destructuring, not construction. | — |
| `float_literal` | value | Literal number — object 1. | — |
| `for_expression` | repetition | Iteration over an iterator — object 6 ("while" as its stated exemplar). | — |
| `for_lifetimes` | F generics | `for<'a>` binder introducing lifetime parameters — parameterization by type-level entities. | UNCERTAIN |
| `foreign_mod_item` | service call | `extern { ... }` declares functions provided by the platform outside the language — object 11 ("request to the platform"). | UNCERTAIN |
| `fragment_specifier` | J metaprogramming | `:expr`, `:ident` etc. inside `macro_rule` matchers; exists only in macro definitions. | — |
| `function_item` | function | The definition form of minimum-set object 7. | — |
| `function_modifiers` | declarative-form (PROPOSED) + A suspension | A modifier bag (`const`, `async`, `unsafe`, `extern`); non-executing, except that `async` is precisely category A's marker. | DUAL, UNCERTAIN |
| `function_signature_item` | function + E dispatch | A body-less `fn ...;` — only legal in trait bodies and extern blocks, i.e. as an interface obligation. | DUAL |
| `function_type` | type-form (PROPOSED) + function | `fn(A) -> B` / `Fn(A) -> B`: a `_type` sub-type denoting the type of object 7. | DUAL |
| `gen_block` | A suspension | `gen { }` builds a generator; the A row names "async/await, coroutines, generators" as one category. | — |
| `generic_function` | F generics + function | A call target carrying explicit type arguments (turbofish); it is a call site plus type parameterization. | DUAL |
| `generic_pattern` | D pattern matching + F generics | A pattern in the `_pattern` supertype set carrying type arguments. | DUAL, UNCERTAIN |
| `generic_type` | F generics + type-form (PROPOSED) | `Vec<T>` — a `_type` sub-type whose whole content is type parameterization. | DUAL |
| `generic_type_with_turbofish` | F generics | The `::<>` spelling of the same parameterization; type-argument syntax only. | — |
| `higher_ranked_trait_bound` | F generics + E dispatch | `for<'a> Fn(&'a T)`: a quantified trait bound — generics machinery over an interface. | DUAL |
| `identifier` | name | The written identifier itself — minimum-set object 2. It is also in `_pattern`, where it binds; still a name. | — |
| `if_expression` | choice | "if" — object 5's description verbatim. | — |
| `impl_item` | E dispatch | `impl Trait for Type` is Rust's conformance declaration; t1 E/Rust names traits as the realization. | — |
| `index_expression` | collection | `a[i]` reads by position or key from an ordered/keyed many — object 9. | — |
| `inner_attribute_item` | declarative-form (PROPOSED) + J metaprogramming | `#![...]` applied to the enclosing item; same dual reading as `attribute_item`. | DUAL, UNCERTAIN |
| `inner_doc_comment_marker` | declarative-form (PROPOSED) | A marker token inside `doc_comment`; pure trivia. | — |
| `integer_literal` | value | Literal number — object 1. | — |
| `label` | repetition | `'outer:` labels loops and is the target of labelled `break`/`continue`; its only role is loop control. | UNCERTAIN |
| `let_chain` | choice + D pattern matching | `if let A = x && let B = y`: a conditional built out of pattern tests. | DUAL |
| `let_condition` | D pattern matching + choice | `let PAT = expr` in condition position: a refutable pattern test used as a branch condition. | DUAL |
| `let_declaration` | name | `let x = v;` binds a written identifier to a value — object 2 exactly. | — |
| `lifetime` | type-form (PROPOSED) | `'a` is a type-level annotation with no runtime object; it appears in type and generic positions. | UNCERTAIN |
| `lifetime_parameter` | F generics + type-form (PROPOSED) | A lifetime declared in `type_parameters` — parameterization, of a type-level entity. | DUAL |
| `line_comment` | declarative-form (PROPOSED) | Extra; no object. | — |
| `loop_expression` | repetition | Unconditional loop — object 6. | — |
| `macro_definition` | J metaprogramming | `macro_rules!` — "reflection, macros, codegen" is category J's description. | — |
| `macro_invocation` | J metaprogramming | Category J. Note it is simultaneously an `_expression`, a `_pattern` and a `_type` sub-type in the grammar, which is why it cannot be bucketed by position. | — |
| `macro_rule` | J metaprogramming | One matcher-to-template rule inside a macro definition. | — |
| `match_arm` | D pattern matching | One arm of `match_block`; pattern plus body. | — |
| `match_block` | D pattern matching | The braced arm list of `match_expression`. | — |
| `match_expression` | D pattern matching + choice | t1 D/Rust: "match is central: exhaustive, deep destructuring — reference realization". It is also structural choice, i.e. object 5 generalized. | DUAL |
| `match_pattern` | D pattern matching | The pattern-plus-guard slot of a `match_arm`. | — |
| `metavariable` | J metaprogramming | `$x` — exists only inside macro definitions and their expansions. | — |
| `mod_item` | sequence | A namespace container whose body is an ordered declaration list. Namespacing has no object in either tier; `sequence` is the containment fallback. | UNCERTAIN |
| `mut_pattern` | D pattern matching + mutation | `mut x` in a pattern: a binding form (D) that declares the binding writable (object 10). | DUAL |
| `mutable_specifier` | mutation + declarative-form (PROPOSED) | The bare `mut` token; it grants object 10's capability without performing it. | DUAL, UNCERTAIN |
| `negative_literal` | value | A `_literal_pattern` sub-type; a signed numeric literal. | — |
| `never_type` | type-form (PROPOSED) | `!` — a `_type` sub-type inhabited by nothing. | — |
| `or_pattern` | D pattern matching | `A | B` in pattern position — `_pattern` sub-type. | — |
| `ordered_field_declaration_list` | record | Tuple-struct fields: values grouped under positional rather than written names. | UNCERTAIN |
| `outer_doc_comment_marker` | declarative-form (PROPOSED) | Marker token inside `doc_comment`. | — |
| `parameter` | function | One formal parameter — the "parameterized" of object 7. | — |
| `parameters` | function | The `parameters` field of `function_item`. | — |
| `parenthesized_expression` | operation | Pure grouping: it changes operator precedence and nothing else. NONE is defensible. | UNCERTAIN |
| `pointer_type` | type-form (PROPOSED) | `*const T` / `*mut T` — a `_type` sub-type. | — |
| `primitive_type` | type-form (PROPOSED) + value | A `_type` sub-type (17 duplicate ids in the subtype table); denotes the type of object 1's values, is not itself a value. | DUAL |
| `qualified_type` | E dispatch + type-form (PROPOSED) | `<T as Trait>` disambiguates which trait impl a name comes from — dispatch selection in type syntax. | DUAL |
| `range_expression` | collection + operation | `a..b` builds a Range value that is iterated as an ordered many; the operator reading is also available. | DUAL, UNCERTAIN |
| `range_pattern` | D pattern matching | `1..=9` in pattern position — `_pattern` sub-type. | — |
| `raw_string_literal` | value | Literal text — object 1. | — |
| `ref_pattern` | D pattern matching | `ref x` binding mode — `_pattern` sub-type. | — |
| `reference_expression` | name | `&x` / `&mut x` produces a borrow of an existing binding. Borrowing/aliasing has no object in either tier; `name` is the nearest. | UNCERTAIN |
| `reference_pattern` | D pattern matching | `&pat` — `_pattern` sub-type. | — |
| `reference_type` | type-form (PROPOSED) | `&'a T` — a `_type` sub-type. | — |
| `remaining_field_pattern` | D pattern matching | `..` inside `struct_pattern`; pattern-only. | — |
| `removed_trait_bound` | E dispatch + F generics | `?Sized` — negates an implicit trait bound; a bound is E's object, appearing in F's machinery. | DUAL |
| `return_expression` | function | The "return" half of object 7. | — |
| `scoped_identifier` | name | `a::b` — a path naming a value or item; an `_expression` sub-type and a `_pattern` sub-type. | — |
| `scoped_type_identifier` | type-form (PROPOSED) + name | `a::B` in type position — a `_type` sub-type that is also a path. | DUAL |
| `scoped_use_list` | name | `a::{b, c}` inside `use_declaration`: names brought into scope. | UNCERTAIN |
| `self` | name | A binding referring to the receiver; an `_expression` sub-type, so it evaluates to a value like any name. | — |
| `self_parameter` | function + name | The receiver parameter of a method — a parameter (object 7) that binds a name. | DUAL |
| `shebang` | declarative-form (PROPOSED) | `#!/...` first line; never executes as Rust. | — |
| `shorthand_field_identifier` | name + record | `Foo { x }`: one token acting as both the field name and the value-bearing binding. | DUAL |
| `shorthand_field_initializer` | record | The initializer form of the same shorthand, inside `field_initializer_list`. | — |
| `slice_pattern` | D pattern matching + collection | `[a, b, ..]` destructures an ordered many. | DUAL |
| `source_file` | sequence | The root: an ordered run of items. Object 4 is the only structural object that fits a whole-file container. | UNCERTAIN |
| `static_item` | name + mutation | Binds a name at static-storage duration; `static mut` makes it writable. | DUAL |
| `string_content` | value | The text inside a string literal. | — |
| `string_literal` | value | Literal text — object 1; a `_literal` sub-type. | — |
| `struct_expression` | record | Constructs a record from named field initializers — object 8. | — |
| `struct_item` | record | Declares "values grouped under named fields" — object 8's description verbatim. | — |
| `struct_pattern` | D pattern matching | Destructures a record — `_pattern` sub-type. | — |
| `super` | name | Path root token, like `crate`. | — |
| `token_binding_pattern` | J metaprogramming | Occurs only inside `macro_rule` matchers. | — |
| `token_repetition` | J metaprogramming | `$(...)*` in a macro template. | — |
| `token_repetition_pattern` | J metaprogramming | `$(...)*` in a macro matcher. | — |
| `token_tree` | J metaprogramming | Unstructured balanced-delimiter token content of a macro; log_002 §5.0 records that it carries no grammatical structure at all. | — |
| `token_tree_pattern` | J metaprogramming | The matcher-side token tree. | — |
| `trait_bounds` | E dispatch + F generics | `: Trait + Trait` — the bound list; E's object appearing in F's declaration sites. | DUAL |
| `trait_item` | E dispatch | Declares an interface; t1 E/Rust names traits as the realization. | — |
| `try_block` | C optionals | `try { }` captures `?` propagation; t1 C/Rust: "Option<T> pure sum type; no null exists at all" — the `?`/Result machinery is C's Rust form. | UNCERTAIN |
| `try_expression` | C optionals | `?` short-circuits on absence/error — the propagation operator of the Option/Result sum types. | UNCERTAIN |
| `tuple_expression` | record | An anonymous product of values — object 8 without written field names. | UNCERTAIN |
| `tuple_pattern` | D pattern matching | `_pattern` sub-type. | — |
| `tuple_struct_pattern` | D pattern matching | `_pattern` sub-type. | — |
| `tuple_type` | type-form (PROPOSED) | `_type` sub-type denoting an anonymous product type. | — |
| `type_arguments` | F generics | The `<...>` list supplying types to a parameterized item — F's core syntax. | — |
| `type_binding` | F generics + E dispatch | `Item = T` inside `type_arguments`: fixes an associated type of a trait. | DUAL |
| `type_cast_expression` | operation | `x as T` converts a value; the border_lattice treats such crossings as conversions on values. | UNCERTAIN |
| `type_identifier` | type-form (PROPOSED) | A `_type` sub-type; the bare name of a type, no runtime object. | — |
| `type_item` | type-form (PROPOSED) + name | `type A = B;` binds a written identifier to a type rather than to a value. | DUAL |
| `type_parameter` | F generics | One declared type parameter — F's object. | — |
| `type_parameters` | F generics | The declaration list of type parameters. | — |
| `unary_expression` | operation | Negation/deref/not on one value — object 3. | — |
| `union_item` | record | Declares fields sharing storage; still "values grouped under named fields" structurally. | UNCERTAIN |
| `unit_expression` | value | `()` — the single inhabitant of the unit type; a value with no content. | — |
| `unit_type` | type-form (PROPOSED) | `()` in type position — a `_type` sub-type. | — |
| `unsafe_block` | sequence | Its body is an ordered run of statements; the `unsafe` obligation it carries has no object in either tier. | UNCERTAIN |
| `use_as_clause` | name | `as alias` — renames an imported name. | — |
| `use_bounds` | E dispatch + F generics | `use<'a, T>` precise capturing on `impl Trait`; constrains what an opaque type captures. | DUAL, UNCERTAIN |
| `use_declaration` | name | Binds a path's tail name into the current scope. Import/namespace has no object of its own; object 2 is the nearest true statement. | UNCERTAIN |
| `use_list` | name | `{a, b}` inside a use path — a set of names bound. | UNCERTAIN |
| `use_wildcard` | name | `*` — binds every public name of the path. | UNCERTAIN |
| `variadic_parameter` | function | `...` in extern signatures; a parameter form of object 7. | — |
| `visibility_modifier` | declarative-form (PROPOSED) | `pub`, `pub(crate)`: an access annotation; it executes nothing and creates no object. | — |
| `where_clause` | F generics + E dispatch | Constraint list on a generic item — F's machinery carrying E's bounds. | DUAL |
| `where_predicate` | F generics + E dispatch | One constraint inside `where_clause`. | DUAL |
| `while_expression` | repetition | "while" — object 6's description verbatim. | — |
| `yield_expression` | A suspension | Suspends a generator, yielding a value — category A ("async/await, coroutines, generators"). | — |

---

## the PROPOSED new buckets

Two, which is the smallest number that closes both named gaps. Each is
proposed, not adopted.

### 1. `type-form` — bare type syntax

The gap: the grammar declares a `_type` supertype with 33 sub-types, and
for a large part of them no object of either tier is present in the node.
`type_identifier` is the written name of a type; `primitive_type`,
`reference_type`, `pointer_type`, `never_type`, `unit_type`, `tuple_type`,
`array_type`, `bracketed_type` likewise denote types without constructing,
naming or operating on any value. Tagging them `value` would be false —
`u32` is not a number, it is what numbers are. Tagging them `name` would
be false in a different way, since object 2 is defined as "a binding from
a written identifier to a VALUE". Tagging them F (generics) would be
false for every non-parameterized one.

The argument for one bucket rather than several: the intentions artifact
is a theory of what a program DOES, and type syntax is what a program
SAYS about what it does. That is one distinction, not many, and it is
exactly the distinction the `_type` supertype already draws — which means
the bucket has prior classification evidence behind it and is close to
free to compute. It also gives F (generics) a clean job: F stays for
parameterization machinery (`type_parameters`, `type_arguments`,
`where_clause`, bounds), while type-form takes bare type spelling. Where
both are present the row is DUAL, e.g. `generic_type`.

Against it, and worth the owner weighing: the minimum set was built to be
universal across 12 languages, and type syntax is not universal in the
same way — Python's annotations and Rust's types are not the same object.
A bucket that means different things per language is weaker than the
other 21.

### 2. `declarative-form` — non-executing trivia and modifiers

The gap: `visibility_modifier`, `attribute`, `attribute_item`,
`inner_attribute_item`, `function_modifiers`, `extern_modifier`,
`mutable_specifier`, `shebang`, `line_comment`, `block_comment`,
`doc_comment` and the two doc-comment markers are in the tree, are real
nodes with spans, and perform nothing. Several are `is_extra` in the API
(log_002 §6.0: comments are in the tree and already labelled). The
minimum set has no object for them because they hold no intention — they
MODIFY where an intention is allowed to flow rather than carrying one.

The argument for one bucket: the alternative is NONE, and NONE is worse
here for a specific reason — the totality check that log_006 relies on
cannot distinguish "deliberately unbucketed" from "not yet done" if both
read as absent. A positive tag saying "classified, and the classification
is: carries no intention" keeps the census honest. This is the same
refusal posture log_002 §8.1 applies to `token_tree`: never silently
empty.

Against it: `pub` and `mut` are not inert in the way a comment is —
visibility governs what may reach a name, and `mut` grants object 10's
capability. Both are flagged DUAL above for that reason, and if the owner rules
that capability markers take the capability's bucket, this bucket shrinks
to comments, shebang and attributes.

### buckets that received nothing

Three of the 21 took no rows: **B (channels)**, **G (scoped cleanup)** and
**I (operator overloading)**. That is a finding rather than an oversight,
and it is consistent with the artifact's own Rust cells: B/Rust is `std
mpsc` (a library, not syntax), G/Rust is RAII via the `Drop` trait (an
`impl_item`, indistinguishable in the grammar from any other impl), and
I/Rust is operator traits (again ordinary impls). None of the three has
dedicated syntax in Rust, so no named kind can carry them. **This is
evidence for a real claim: a category can be present in a language and
invisible to its grammar.** Whatever fills those buckets has to come from
the ledger's name resolution, not from `ur_kind`. **H (events)** is in the
same position and appears only as a flagged dual on `closure_expression`.

---

## every UNCERTAIN row, gathered

37 rows. Grouped where one ruling settles several.

| kind | proposed | what would resolve it |
| --- | --- | --- |
| `abstract_type` | type-form (PROPOSED) + E dispatch | Whether a type-position construct whose content is a trait bound belongs in E or stays purely type-form. |
| `attribute` | declarative-form (PROPOSED) + J metaprogramming | A ruling on whether inert annotations that a proc-macro later consumes are J at the syntax layer or only once expanded. |
| `attribute_item` | declarative-form (PROPOSED) + J metaprogramming | Same as `attribute`: does J attach to the annotation, or only to what expands it? |
| `closure_expression` | function + H events | Whether H (events) is a Rust bucket at all — t1 H/Rust should be read as decisive before assigning it. |
| `const_block` | J metaprogramming + value | The minimum set has no compile-time-execution object; the owner to say whether J covers it or a new object is owed. |
| `declaration_list` | sequence | Whether container nodes get the bucket of what they contain or a structural bucket of their own. |
| `empty_statement` | sequence | Whether NONE is permitted for nodes that carry position but no object. |
| `enum_item` | record + D pattern matching | Sum types are not in the minimum set. the owner to rule whether `record` stretches to cover them or an object is missing. |
| `enum_variant` | record | Follows the `enum_item` ruling. |
| `enum_variant_list` | record | Follows the `enum_item` ruling. |
| `extern_crate_declaration` | name | Follows the import/namespace ruling (see `use_declaration`). |
| `extern_modifier` | declarative-form (PROPOSED) + service call | Whether the FFI boundary marker is trivia or an early signal of object 11. |
| `for_lifetimes` | F generics | Whether lifetime machinery is F or belongs entirely to the proposed type-form bucket. |
| `foreign_mod_item` | service call | Whether "service call" covers declared-but-not-called foreign functions, or only call sites. |
| `function_modifiers` | declarative-form (PROPOSED) + A suspension | The bag mixes inert modifiers with `async`; splitting it per token may be the real answer. |
| `generic_pattern` | D pattern matching + F generics | Rare construct; a corpus count would show whether it is worth a dual tag at all. |
| `inner_attribute_item` | declarative-form (PROPOSED) + J metaprogramming | Same as `attribute_item`. |
| `label` | repetition | Whether a label is a name (it is written and referred to) or loop control. |
| `lifetime` | type-form (PROPOSED) | Whether lifetimes are type-form or deserve their own bucket, given they have no analogue in the other eleven languages. |
| `mod_item` | sequence | Namespacing has no object; the owner to say whether `sequence` is an acceptable fallback or a bucket is owed. |
| `mutable_specifier` | mutation + declarative-form (PROPOSED) | Whether a capability marker is tagged with the capability it grants or as trivia. |
| `ordered_field_declaration_list` | record | Whether positional fields are `record` or `collection`. |
| `parenthesized_expression` | operation | Whether pure grouping nodes take a bucket or NONE. |
| `range_expression` | collection + operation | Whether ranges are a collection constructor or an operator; a corpus split of iterated vs indexed uses would settle it. |
| `reference_expression` | name | Borrowing has no object in either tier. This is the clearest candidate for a missing intention, and is the owner's call. |
| `scoped_use_list` | name | Follows the import/namespace ruling. |
| `source_file` | sequence | Same container question as `declaration_list`. |
| `try_block` | C optionals | Whether Rust's Result/`?` machinery is C (optionals) or an error-handling intention the categories do not carry. |
| `try_expression` | C optionals | Same as `try_block`; error propagation vs absence-in-types. |
| `tuple_expression` | record | Whether anonymous products are `record` or `collection`. |
| `type_cast_expression` | operation | Whether a cast is an operation on a value or a type-form construct. |
| `union_item` | record | Unions are storage overlap, not field grouping; whether `record` is honest here. |
| `unsafe_block` | sequence | The unsafe obligation has no bucket; whether that is a gap or deliberately out of scope. |
| `use_bounds` | E dispatch + F generics | Rare, recent syntax; a corpus count and a read of the grammar's own node types would firm it up. |
| `use_declaration` | name | Import/namespace has no object in either tier. One ruling covers the whole use/mod/extern-crate family. |
| `use_list` | name | Follows the import/namespace ruling. |
| `use_wildcard` | name | Follows the import/namespace ruling. |

Five clusters account for most of them:

1. **The import/namespace family** (`use_declaration`, `use_list`,
   `use_wildcard`, `scoped_use_list`, `extern_crate_declaration`,
   `mod_item`) — neither tier has an object for bringing names into
   scope. Provisionally `name`, on the grounds that a `use` really does
   bind a written identifier; but the binding is to an item, not a value,
   so object 2's own wording strains.
2. **Sum types** (`enum_item`, `enum_variant`, `enum_variant_list`) —
   the minimum set has `record` for products and nothing for sums, even
   though C (optionals) leans entirely on Rust's `Option` being a sum
   type (t1 C/Rust: "Option<T> pure sum type; no null exists at all").
3. **Borrowing** (`reference_expression`, and the type-side
   `reference_type`, `lifetime`, `lifetime_parameter`) — no object
   covers aliasing. The artifact's `border_lattice` has a copy-model
   class that turns on exactly this, so the concept is present in the
   research but not in the 21 buckets.
4. **Error propagation** (`try_expression`, `try_block`) — provisionally
   C, but C is "null safety, absence in types" and `?` over `Result` is
   error flow, which is a related but distinct thing.
5. **Structural containers** (`source_file`, `declaration_list`,
   `unsafe_block`, `empty_statement`, `parenthesized_expression`) — nodes
   that hold position without holding an object.

---

## open questions for the owner

1. **Exclusive or primary?** 42 of 163 rows carry two buckets. log_006
   leaves this open. If a kind may hold only one tag, roughly a fifth of
   the table needs a tie-break rule; if it may hold several, `ur_kind`
   becomes a set rather than a value, and the totality check changes
   shape.
2. **Do the two PROPOSED buckets get adopted, rejected, or replaced by a
   ruling that these kinds simply take NONE?** The argument above is that
   NONE damages the census; that argument is mine, not settled.
3. **Is a missing intention a finding worth recording?** Borrowing,
   sum types, namespacing and error propagation all landed in strained
   buckets. If the intentions artifact is fixed, `ur_kind` absorbs the
   strain. If the artifact can grow, this table is evidence about where.
4. **Does the coarse layer replace the supertype families or sit beside
   them?** log_006 item 5 assumed the five supertypes as the coarse layer.
   They are cheap, author-maintained and orthogonal to this proposal —
   keeping both is possible.
5. **Three empty buckets (B, G, I) and a near-empty one (H).** Does an
   intention with no syntax belong in `ur_kind` at all, or is that the
   ledger's job by construction?
6. **Language two.** Every judgement here is on Rust's grammar. Whether
   these buckets survive contact with c/cpp is untested, and log_006
   item 2 argues against guessing ahead of ingest.

---

## sources

- `PRIVATE/PseudoIR/Tools/intentions/pc_intentions.json` —
  `minimum_set`, `intent_categories`, `t1_realizations`, `border_lattice`.
- `PRIVATE/PseudoCoup_v5/DevComms/log_006_ur_kinds_vocabulary.md` —
  items 3 and 5, which this drafts for.
- `PRIVATE/PseudoCoup_v5/DevComms/log_002_ur_brainstorm.md` §2-§3 —
  the worked sample and the kind families.
- The compiled `Language` object, `tree-sitter==0.26.0` /
  `tree-sitter-rust==0.24.2`, enumerated 2026-08-05.
