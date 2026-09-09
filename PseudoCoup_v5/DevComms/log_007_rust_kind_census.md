# log 007 — rust named-kind census, codegen crates

Date: 2026-08-05

**Scope caveat (read first):** this is the sparse codegen slice — two crates,
`Sources/rust/compiler/rustc_codegen_ssa` and
`Sources/rust/compiler/rustc_codegen_llvm` — not rustc entire.
`rustc_codegen_cranelift` was excluded entirely per project policy (that
backend is prohibited in this project line); no file under it was read or
counted.

## Grammar identity measured

- `tree-sitter` wheel: `0.26.0`
- `tree-sitter-rust` wheel: `0.24.2`
- `Language.abi_version`: `15`
- `Language.semantic_version`: `(0, 24, 1)`
- `Language.node_kind_count`: `355` (named + unnamed kinds together)
- Named kinds in the grammar's full kind set: `164` (153 occurring in this
  corpus + 11 in the zero set below)

## Corpus and file counts

- Files parsed (total): **111**
- Clean (no ERROR node below the top): **106**
- Files with at least one `has_error` tree: **5**

Files with `has_error`:

- `Sources/rust/compiler/rustc_codegen_llvm/src/llvm/enzyme_ffi.rs`
- `Sources/rust/compiler/rustc_codegen_llvm/src/llvm/ffi.rs`
- `Sources/rust/compiler/rustc_codegen_llvm/src/macros.rs`
- `Sources/rust/compiler/rustc_codegen_ssa/src/traits/mod.rs`
- `Sources/rust/compiler/rustc_codegen_ssa/src/traits/type_.rs`

These 5 files account for all 71 occurrences of the `ERROR` kind in the
frequency table below (`ERROR` appears in exactly 5 files, matching the
error-file count above — self-consistent).

## Totals

- Total nodes visited (named + unnamed): **544,137**
- Named nodes counted: **304,278**
- Distinct named kinds occurring at least once: **153**
- Named kinds in the grammar that never occur here (zero set): **11**

## Frequency table (kinds that occur, sorted by count descending)

Count = occurrences across the corpus. Files = number of distinct files the
kind appears in (out of 111).

| kind | count | files |
|---|---|---|
| identifier | 81367 | 111 |
| field_identifier | 20086 | 96 |
| field_expression | 18259 | 94 |
| call_expression | 17259 | 98 |
| arguments | 17259 | 98 |
| type_identifier | 11683 | 108 |
| scoped_identifier | 11148 | 110 |
| line_comment | 8854 | 105 |
| block | 6875 | 100 |
| expression_statement | 6850 | 98 |
| parameter | 5498 | 103 |
| lifetime | 4999 | 99 |
| let_declaration | 4985 | 88 |
| reference_type | 4020 | 100 |
| self | 3825 | 97 |
| token_tree | 3507 | 94 |
| type_arguments | 3164 | 103 |
| match_arm | 3126 | 74 |
| match_pattern | 3126 | 74 |
| generic_type | 3076 | 103 |
| string_content | 3072 | 87 |
| string_literal | 3057 | 87 |
| parameters | 2480 | 106 |
| doc_comment | 2480 | 90 |
| outer_doc_comment_marker | 2359 | 84 |
| if_expression | 2024 | 82 |
| tuple_struct_pattern | 2018 | 77 |
| integer_literal | 2018 | 78 |
| reference_expression | 1965 | 86 |
| mutable_specifier | 1923 | 93 |
| visibility_modifier | 1910 | 105 |
| scoped_type_identifier | 1905 | 92 |
| function_item | 1752 | 100 |
| macro_invocation | 1616 | 88 |
| primitive_type | 1614 | 96 |
| crate | 1575 | 98 |
| use_declaration | 1564 | 108 |
| binary_expression | 1551 | 74 |
| self_parameter | 1202 | 75 |
| lifetime_parameter | 1034 | 88 |
| type_parameters | 917 | 93 |
| field_declaration | 882 | 51 |
| field_initializer | 845 | 66 |
| else_clause | 794 | 70 |
| unary_expression | 763 | 70 |
| closure_expression | 744 | 73 |
| closure_parameters | 744 | 73 |
| match_expression | 733 | 75 |
| match_block | 733 | 75 |
| tuple_pattern | 732 | 66 |
| attribute | 707 | 64 |
| boolean_literal | 694 | 71 |
| attribute_item | 686 | 63 |
| function_signature_item | 676 | 26 |
| enum_variant | 659 | 37 |
| scoped_use_list | 634 | 94 |
| use_list | 634 | 94 |
| or_pattern | 576 | 54 |
| let_condition | 566 | 61 |
| tuple_expression | 555 | 59 |
| field_pattern | 549 | 51 |
| array_expression | 517 | 53 |
| return_expression | 479 | 62 |
| shorthand_field_initializer | 447 | 50 |
| index_expression | 442 | 42 |
| unsafe_block | 438 | 43 |
| struct_expression | 437 | 69 |
| field_initializer_list | 437 | 69 |
| type_cast_expression | 389 | 61 |
| struct_pattern | 389 | 53 |
| shorthand_field_identifier | 387 | 49 |
| pointer_type | 352 | 16 |
| array_type | 338 | 62 |
| declaration_list | 336 | 80 |
| remaining_field_pattern | 304 | 48 |
| assignment_expression | 297 | 47 |
| for_expression | 292 | 56 |
| field_declaration_list | 279 | 51 |
| impl_item | 276 | 69 |
| struct_item | 255 | 54 |
| trait_bounds | 238 | 46 |
| type_parameter | 237 | 42 |
| parenthesized_expression | 184 | 53 |
| try_expression | 177 | 26 |
| super | 164 | 47 |
| reference_pattern | 160 | 39 |
| escape_sequence | 153 | 33 |
| char_literal | 144 | 20 |
| tuple_type | 142 | 58 |
| metavariable | 133 | 9 |
| inner_doc_comment_marker | 121 | 26 |
| enum_item | 117 | 37 |
| enum_variant_list | 117 | 37 |
| mod_item | 116 | 22 |
| source_file | 111 | 111 |
| compound_assignment_expr | 111 | 19 |
| let_chain | 96 | 33 |
| unit_expression | 84 | 30 |
| use_wildcard | 84 | 51 |
| continue_expression | 82 | 20 |
| generic_function | 82 | 35 |
| dynamic_type | 81 | 13 |
| ordered_field_declaration_list | 81 | 25 |
| range_expression | 78 | 31 |
| ref_pattern | 74 | 23 |
| type_item | 72 | 13 |
| ERROR | 71 | 5 |
| type_binding | 70 | 16 |
| empty_statement | 66 | 28 |
| const_item | 55 | 18 |
| function_type | 52 | 21 |
| abstract_type | 52 | 25 |
| token_binding_pattern | 48 | 8 |
| fragment_specifier | 48 | 8 |
| block_comment | 44 | 18 |
| trait_item | 40 | 25 |
| function_modifiers | 40 | 10 |
| extern_modifier | 39 | 6 |
| mut_pattern | 35 | 22 |
| use_as_clause | 27 | 22 |
| unit_type | 26 | 13 |
| token_tree_pattern | 24 | 8 |
| captured_pattern | 21 | 3 |
| macro_definition | 21 | 9 |
| inner_attribute_item | 21 | 7 |
| macro_rule | 20 | 8 |
| token_repetition_pattern | 18 | 5 |
| token_repetition | 16 | 5 |
| associated_type | 16 | 4 |
| break_expression | 14 | 5 |
| foreign_mod_item | 13 | 2 |
| bracketed_type | 12 | 4 |
| qualified_type | 12 | 4 |
| slice_pattern | 11 | 7 |
| bounded_type | 11 | 7 |
| where_predicate | 11 | 6 |
| while_expression | 10 | 8 |
| try_block | 10 | 4 |
| where_clause | 10 | 6 |
| base_field_initializer | 8 | 6 |
| loop_expression | 7 | 4 |
| removed_trait_bound | 6 | 3 |
| generic_type_with_turbofish | 6 | 1 |
| never_type | 5 | 3 |
| range_pattern | 5 | 2 |
| static_item | 4 | 4 |
| float_literal | 4 | 1 |
| raw_string_literal | 4 | 4 |
| const_block | 2 | 2 |
| label | 2 | 1 |
| for_lifetimes | 1 | 1 |
| negative_literal | 1 | 1 |
| const_parameter | 1 | 1 |

153 rows, matching "distinct named kinds occurring" above.

## Zero set — named kinds in the grammar that never occur here

11 kinds, all named per `node_kind_is_named`, present in the grammar's full
kind table (`node_kind_count` = 355) but with zero occurrences across all
111 files:

- `async_block`
- `await_expression`
- `extern_crate_declaration`
- `gen_block`
- `generic_pattern`
- `higher_ranked_trait_bound`
- `shebang`
- `union_item`
- `use_bounds`
- `variadic_parameter`
- `yield_expression`

164 (occurring) + 11... correction: 153 occurring + 11 zero = 164 total named
kinds, matching the grammar-identity line above.

## Supertypes and subtype coverage

The grammar declares 5 supertypes. For each, the table below gives the
number of distinct sub-kinds the grammar lists under it, and the fraction of
this corpus's 304,278 named nodes that fall under one of those sub-kinds
(sum of the frequency-table counts for that supertype's listed sub-kinds,
divided by 304,278). Because sub-kind membership is a static grammar
declaration and not tied to where a node sits in a given tree, a kind such as
`identifier` or `scoped_identifier` — which is listed under both `_expression`
and `_pattern` — is counted toward both supertypes' totals; the five
fractions are not mutually exclusive and do not sum to 100%.

| supertype | distinct sub-kinds listed | occurrences (sum) | fraction of named nodes |
|---|---|---|---|
| `_expression` | 39 | 152,949 | 50.27% |
| `_pattern` | 18 (incl. 1 anonymous kind, `_`, not part of the named census) | 98,458 | 32.36% |
| `_type` | 17 | 25,112 | 8.25% |
| `_literal_pattern` | 7 | 5,922 | 1.95% |
| `_literal` | 6 | 5,921 | 1.95% |

Note on `_type`: the grammar lists `primitive_type` 17 times under this
supertype (once per primitive type token in the grammar source), all
collapsing to the single kind `primitive_type` in the compiled node table;
the "17" in this row is the raw listing length before dedup, kept as
reported by `Language.subtypes()` for `_type` id 216 — the distinct-kind
count used for the occurrence sum is smaller after dedup.

## Script used (re-runnable)

```python
#!/usr/bin/env python3
"""log_007 census script — rust named-kind census over codegen_ssa + codegen_llvm.
Uses pinned tree-sitter==0.26.0, tree-sitter-rust==0.24.2.
Terminology note: this script and its output avoid parent/child/sibling/
ancestor/descendant/orphan language for tree relationships, per project
communication protocol. Traversal below walks super-nodes down to sub-nodes.
"""
import os
import sys
from collections import Counter, defaultdict

import tree_sitter
import tree_sitter_rust

ROOTS = [
    "Sources/rust/compiler/rustc_codegen_ssa",
    "Sources/rust/compiler/rustc_codegen_llvm",
]

def find_rs_files(base):
    out = []
    for root in ROOTS:
        full = os.path.join(base, root)
        for dirpath, dirnames, filenames in os.walk(full):
            for fn in filenames:
                if fn.endswith(".rs"):
                    out.append(os.path.join(dirpath, fn))
    return sorted(out)

def main():
    base = sys.argv[1]
    language = tree_sitter.Language(tree_sitter_rust.language())
    parser = tree_sitter.Parser(language)

    files = find_rs_files(base)

    kind_counts = Counter()
    kind_file_sets = defaultdict(set)
    total_nodes = 0
    total_named_nodes = 0
    clean_files = []
    error_files = []

    for path in files:
        with open(path, "rb") as f:
            src = f.read()
        tree = parser.parse(src)
        has_error = tree.root_node.has_error
        if has_error:
            error_files.append(path)
        else:
            clean_files.append(path)

        # Walk from the top node down to sub-nodes, iteratively.
        stack = [tree.root_node]
        while stack:
            node = stack.pop()
            total_nodes += 1
            if node.is_named:
                total_named_nodes += 1
                kind_counts[node.type] += 1
                kind_file_sets[node.type].add(path)
            for i in range(node.child_count):
                stack.append(node.child(i))

    abi_version = language.abi_version
    semantic_version = language.semantic_version
    node_kind_count = language.node_kind_count

    all_named_kinds = set()
    for kind_id in range(node_kind_count):
        name = language.node_kind_for_id(kind_id)
        if name is not None and language.node_kind_is_named(kind_id):
            all_named_kinds.add(name)

    zero_set = sorted(all_named_kinds - set(kind_counts.keys()))

    supertypes = {}
    for sid in language.supertypes:
        name = language.node_kind_for_id(sid)
        subs = language.subtypes(sid)
        supertypes[name] = [language.node_kind_for_id(s) for s in subs]

    print("FILES", len(files), len(clean_files), len(error_files))
    for p in error_files:
        print("ERROR_FILE", p)
    print("TOTALS", total_nodes, total_named_nodes)
    print("ABI", abi_version, "SEMVER", semantic_version, "NODE_KIND_COUNT", node_kind_count)
    print("ZERO_SET_SIZE", len(zero_set), zero_set)
    for kind, cnt in kind_counts.most_common():
        print("FREQ", kind, cnt, len(kind_file_sets[kind]))
    print("SUPERTYPES", supertypes)

if __name__ == "__main__":
    main()
```

## open questions for the owner

- The `_expression` / `_pattern` supertype fractions overlap (e.g.
  `identifier` and `scoped_identifier` count toward both), because subtype
  membership is a static grammar fact, not a per-occurrence classification —
  this census cannot currently tell you how many of the 81,367 `identifier`
  nodes sit in expression position versus pattern position. Flagging, not
  deciding whether that split matters for the transpiler work.
- 5 files carry `has_error` — all inside `rustc_codegen_llvm/src/llvm/`
  and two `traits/` files in `rustc_codegen_ssa`. It is not established
  whether any of the 153 occurring kinds appear *only* inside these 5
  error-bearing files (i.e. whether removing them from the corpus would
  shrink the occurring-kind set below 153). Not checked here — would need a
  follow-up pass that excludes the 5 files and re-diffs the kind set.
  the ERROR kind is presumed a byproduct of a partial-parse zone within
  otherwise valid files, but the byte ranges of the ERROR nodes were not
  captured — whether the errors are e.g. from `enzyme_ffi.rs`/`ffi.rs` FFI
  macro use, or from `macro_rules!` bodies, is undetermined.
- Whether the 11 zero-set kinds (`async_block`, `await_expression`,
  `gen_block`, `yield_expression`, `higher_ranked_trait_bound`, etc.) being
  entirely absent reflects this being a synchronous, non-async codegen
  layer, or is an artifact of the 2-crate slice being too small a sample of
  rustc's surface syntax, is not something this measurement can resolve —
  it would need the same census run over a wider crate set to compare.
