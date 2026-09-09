# log 009 — the form-invisible intentions (B, G, I): how they manifest in the codegen corpus

Date: 2026-08-05

**Scope caveat:** this measurement covers exactly two crates —
`~/Programming/Sources/rust/compiler/rustc_codegen_ssa` and
`~/Programming/Sources/rust/compiler/rustc_codegen_llvm` — 111 `.rs` files total.
`rustc_codegen_cranelift` was excluded per instruction (prohibited). This is not
"rustc" and not even "all of codegen"; it is two sparse, backend-specific crates.
Any generalization beyond this corpus is unsupported by this log.

## 0. Setup

Parser: `tree-sitter` 0.26.0 + `tree-sitter-rust` 0.24.2, full syntax tree walk per
file (see appendix script). All parse-based counts come from walking `impl_item`
super-nodes and reading their `trait` / `type` fields, plus counting
`use_declaration`, `call_expression`, `binary_expression`, `index_expression`,
`unary_expression` node types across the corpus. Grep is used only as a
cross-check, per task instructions, and reported separately wherever the two
numbers differ.

## 1. B — channels (message-passing concurrency)

| detection method | count | files |
|---|---|---|
| parse: `use_declaration` containing mpsc/channel/Sender/Receiver/crossbeam | 1 | 1 |
| grep: same keywords, any line (uses + type occurrences + comments) | 26 | 3 |

The single `use_declaration` hit:

| file | line | text |
|---|---|---|
| `~/Programming/Sources/rust/compiler/rustc_codegen_ssa/src/back/write.rs` | 5 | `use std::sync::mpsc::{Receiver, Sender, channel};` |

Grep cross-check shows the keyword appears in 3 files, but 2 of the 3
(`rustc_codegen_ssa/src/back/link.rs`, `rustc_codegen_llvm/src/builder.rs`) are
false positives for this category — `link.rs` uses "channel" to mean Rust
release channel (`CFG_RELEASE_CHANNEL`), and `builder.rs` has "channel" inside a
URL in a comment. The real channel usage is concentrated entirely in
`rustc_codegen_ssa/src/back/write.rs`, which contains 15 of the 26 raw grep
hits: the `use` declaration, 3 `channel()` call sites, and 11 `Sender<..>` /
`Receiver<..>` type occurrences in struct fields and function signatures.

| file | raw keyword hits |
|---|---|
| `rustc_codegen_ssa/src/back/write.rs` | 15 |
| `rustc_codegen_ssa/src/back/link.rs` | 4 (false positives — "release channel") |
| `rustc_codegen_llvm/src/builder.rs` | 1 (false positive — URL in comment) |

## 2. G — scoped cleanup (Drop / explicit drop / guard types)

### 2a. `impl Drop for X` (parse-based, `impl_item.trait` field == `Drop`)

| detection method | count | files |
|---|---|---|
| parse: `impl_item` trait field resolves to `Drop` | 12 | 9 |
| grep: `impl(<...>)?\s+Drop\s+for\s+` | 11 | 9 |

Gap explained: grep's `<[^>]*>` cannot match nested generic bounds. It misses
`rustc_codegen_llvm/src/builder.rs:53`:
`impl<'a, 'll, CX: Borrow<SCx<'ll>>> Drop for GenericBuilder<'a, 'll, CX>` —
the bound `Borrow<SCx<'ll>>` nests a second `<...>` inside the impl's generic
parameter list, which a non-nesting regex cannot cross. The parser has no such
limitation because it reads the actual `trait` field of the `impl_item` node.

Target types with `Drop`:

| file | line | type |
|---|---|---|
| `rustc_codegen_ssa/src/back/write.rs` | 2106 | `Coordinator<B>` |
| `rustc_codegen_llvm/src/builder.rs` | 53 | `GenericBuilder<'a, 'll, CX>` |
| `rustc_codegen_llvm/src/lib.rs` | 88 | `TimeTraceProfiler` |
| `rustc_codegen_llvm/src/lib.rs` | 502 | `ModuleLlvm` |
| `rustc_codegen_llvm/src/back/owned_target_machine.rs` | 89 | `OwnedTargetMachine` |
| `rustc_codegen_llvm/src/back/lto.rs` | 659 | `Buffer` |
| `rustc_codegen_llvm/src/back/lto.rs` | 672 | `ThinData` |
| `rustc_codegen_llvm/src/back/write.rs` | 401 | `DiagnosticHandlers<'a>` |
| `rustc_codegen_llvm/src/llvm/mod.rs` | 426 | `OperandBundleBox<'_>` |
| `rustc_codegen_llvm/src/llvm/enzyme_ffi.rs` | 550 | `TypeTree` |
| `rustc_codegen_llvm/src/debuginfo/di_builder.rs` | 30 | `DIBuilderBox<'ll>` |
| `rustc_codegen_llvm/src/debuginfo/metadata/type_map.rs` | 242 | `AdtStackPopGuard<'ll, 'tcx, 'a>` |

All 12 land in `impl_item`, tagged in FORM's ur_kind scheme with the same
generic `impl_item` kind as every other trait impl in the corpus (276
`impl_item` super-nodes total) — nothing at the kind level distinguishes a
`Drop` impl from an `Add` impl or a `Display` impl.

### 2b. Explicit `drop(...)` calls

| detection method | count | files |
|---|---|---|
| parse: `call_expression` whose function text is exactly `drop` | 27 | 8 |
| grep: literal `drop(` substring | 40 | — |

Grep overcounts here because `drop(` also matches inside longer identifiers and
inside the `fn drop(&mut self)` method signatures that are part of every `Drop`
impl body (the method definition itself contains the substring `drop(`), plus
calls like `self.drop(...)` on unrelated types where the substring still fires.
The parse-based count restricts to genuine call-expressions whose callee
resolves to the bare name `drop`.

### 2c. Guard-style types (`type_identifier` ending in `Guard`)

| type name |
|---|
| `AdtStackPopGuard` |
| `MutexGuard` |
| `TimingGuard` |
| `VerboseTimingGuard` |

4 distinct guard-style type names appear as type identifiers in the corpus.
Note `AdtStackPopGuard` already appears above as a `Drop`-impl target — RAII
guard types and explicit `Drop` impls overlap partially but are not identical
sets; `MutexGuard`, `TimingGuard`, `VerboseTimingGuard` are used (imported /
referenced) in this corpus without their `Drop` impl being defined here (they
come from `std`/`rustc_data_structures`), so they don't show up in the 2a
table, which only counts `Drop` impls whose definition sits inside these two
crates.

## 3. I — operator overloading

### 3a. `impl_item` whose trait is a `std::ops` trait

| trait | type | file | line |
|---|---|---|---|
| `IndexMut` | `Locals<'tcx, V>` | `rustc_codegen_ssa/src/mir/locals.rs` | 28 |
| `Deref` | `Builder<'_, 'll, 'tcx>` | `rustc_codegen_llvm/src/builder.rs` | 258 |
| `Deref` | `FullCx<'ll, 'tcx>` | `rustc_codegen_llvm/src/context.rs` | 58 |
| `Deref` | `GenericCx<'ll, T>` | `rustc_codegen_llvm/src/context.rs` | 69 |
| `DerefMut` | `GenericCx<'ll, T>` | `rustc_codegen_llvm/src/context.rs` | 78 |

Count: 5 operator-trait impls, 4 distinct target types (`Locals`, `Builder`,
`FullCx`, `GenericCx`). No arithmetic operators (`Add`/`Sub`/`Mul`/etc.) are
implemented anywhere in this corpus — the only overloaded traits present are
indexing (`IndexMut`) and dereference (`Deref`/`DerefMut`).

### 3b. Contrast: syntax nodes that could invoke an overload, corpus-wide

| node type | count |
|---|---|
| `binary_expression` | 1551 |
| `index_expression` | 442 |
| `unary_expression` | 763 |

These 2,756 syntax sites are candidate operator-invocation locations under
FORM; only 5 of them, corpus-wide, are backed by a custom `impl` inside these
two crates (the rest resolve to primitive-type operators or to `Deref`/`Index`
impls defined outside this corpus, e.g. in `std` or `rustc_index`).

## 4. Recoverability gap summary — form-only reading vs actual presence

| category | what ur_kind (form-only) sees | what is actually present | gap |
|---|---|---|---|
| B — channels | 0 dedicated kind; the 1 `use_declaration` and ~14 `Sender`/`Receiver` type mentions in `write.rs` all tag as generic `use_declaration` / `type_identifier` / field-type nodes, indistinguishable from any other import or type reference | 1 import site, 3 `channel()` call sites, 11 `Sender`/`Receiver` type occurrences, concentrated in 1 file (`rustc_codegen_ssa/src/back/write.rs`) | ur_kind gives no signal that a message-passing concurrency pattern exists at all; recoverable only by keyword/path matching against library names (`std::sync::mpsc`), not by kind |
| G — scoped cleanup | 12 `Drop` impls counted among 276 generic `impl_item` kinds (4.3%), with no kind-level marker distinguishing them from the other 264 impls; 27 `drop(` calls counted among all `call_expression` nodes, indistinguishable from any other function call; 4 `Guard`-suffixed types indistinguishable from any other `type_identifier` | 12 `Drop` impls (9 files), 27 explicit `drop()` calls (8 files), 4 guard-style type names | ur_kind sees "impl_item" and "call_expression" — the RAII/defer *intent* is only recoverable by reading the `trait` field text (`Drop`) or the callee name (`drop`) or a naming convention (`*Guard`), none of which are kind-level distinctions |
| I — operator overloading | 5 `impl_item` nodes among 276, again with no kind-level distinction from other trait impls; 2,756 `binary_expression`/`index_expression`/`unary_expression` syntax nodes give no indication whether they resolve to a primitive op or a custom `impl` | 5 operator-trait impls (`IndexMut`, `Deref` x2, `DerefMut`), backing an unknown subset of the 2,756 operator-shaped syntax sites | the *use* of overloading (which binary/index/unary expressions actually dispatch to a custom impl) is invisible to ur_kind entirely — kind tagging cannot distinguish `x + y` on `u32` from `x + y` on a hypothetical custom `Add` impl; only 5 sites define the overload, and the syntax layer can't tell which of the 2,756 expression sites call them |

Across all three categories, `impl_item` is the single generic kind carrying
12 + 5 = 17 of the form-invisible signal (out of 276 total `impl_item`
super-nodes, ~6.2%), and none of those 17 are distinguishable from ordinary
trait impls without reading the `trait` field text — i.e., without doing
exactly the parse-based, trait-name-aware analysis this log performed, and
which plain ur_kind tagging does not do.

## Appendix — measurement script

```python
import os, re, json
from tree_sitter import Language, Parser
import tree_sitter_rust as tsrust

LANG = Language(tsrust.language())
parser = Parser(LANG)

ROOT = "/sessions/<workspace>/mnt/Programming"  # resolved at run time
TARGET_DIRS = [
    os.path.join(ROOT, "Sources/rust/compiler/rustc_codegen_ssa"),
    os.path.join(ROOT, "Sources/rust/compiler/rustc_codegen_llvm"),
]

files = []
for d in TARGET_DIRS:
    for dirpath, dirnames, filenames in os.walk(d):
        for fn in filenames:
            if fn.endswith(".rs"):
                files.append(os.path.join(dirpath, fn))

OPS_TRAITS = set("""Add Sub Mul Div Rem Neg Not BitAnd BitOr BitXor Shl Shr
Index IndexMut Deref DerefMut AddAssign SubAssign MulAssign DivAssign RemAssign
BitAndAssign BitOrAssign BitXorAssign ShlAssign ShrAssign""".split())

channel_kw = re.compile(r'\b(mpsc|channel|Sender|Receiver|crossbeam)\b')

results = {
    "channel_hits": [], "drop_impls": [], "drop_calls": 0,
    "drop_call_files": set(), "guard_types": set(), "ops_impls": [],
    "binary_expr": 0, "index_expr": 0, "unary_expr": 0,
    "impl_item_total": 0, "use_decl_channel_files": set(),
}

def node_text(node, src):
    return src[node.start_byte:node.end_byte].decode('utf8', 'replace')

def walk(node, src, filepath):
    if node.type == "impl_item":
        results["impl_item_total"] += 1
        trait_node = node.child_by_field_name("trait")
        type_node = node.child_by_field_name("type")
        type_name = node_text(type_node, src) if type_node else "?"
        if trait_node:
            trait_simple = node_text(trait_node, src).split("::")[-1].split("<")[0].strip()
            if trait_simple == "Drop":
                results["drop_impls"].append((filepath, node.start_point[0] + 1, type_name))
            if trait_simple in OPS_TRAITS:
                results["ops_impls"].append((filepath, node.start_point[0] + 1, trait_simple, type_name))
    elif node.type == "call_expression":
        func = node.child_by_field_name("function")
        if func and node_text(func, src) == "drop":
            results["drop_calls"] += 1
            results["drop_call_files"].add(filepath)
    elif node.type == "binary_expression":
        results["binary_expr"] += 1
    elif node.type == "index_expression":
        results["index_expr"] += 1
    elif node.type == "unary_expression":
        results["unary_expr"] += 1
    elif node.type == "use_declaration":
        text = node_text(node, src)
        if channel_kw.search(text):
            results["channel_hits"].append((filepath, node.start_point[0] + 1, text.strip()))
            results["use_decl_channel_files"].add(filepath)
    elif node.type == "type_identifier":
        text = node_text(node, src)
        if text.endswith("Guard"):
            results["guard_types"].add(text)
    for child in node.children:
        walk(child, src, filepath)

for fp in files:
    with open(fp, 'rb') as f:
        src = f.read()
    walk(parser.parse(src).root_node, src, fp)
```

## open questions for the owner

- Is `impl_item.trait`-field parsing (as used here) the right long-term
  substitute for ur_kind, or should FORM itself gain sub-kinds for
  `Drop`/ops-trait impls so this doesn't require a bespoke script per query?
- The B category is a single-file phenomenon in this corpus
  (`rustc_codegen_ssa/src/back/write.rs`). Is a 1-file, 111-file-corpus
  finding strong enough to generalize the "B is invisible to FORM" claim, or
  does it need a larger/different corpus before log_008's claim is treated as
  established?
- Should "ledger-level analysis" (per the log_008 claim under test) be defined
  as exactly this trait-field-aware parse pass, or something broader that also
  tracks cross-file trait resolution (e.g. confirming `Sender`/`Receiver` truly
  resolve to `std::sync::mpsc` rather than a shadowing local type)?
- `MutexGuard`/`TimingGuard`/`VerboseTimingGuard` are used but not defined in
  this corpus — do we want a separate pass over their defining crates before
  treating "guard-style types" as measured, or is usage-only evidence
  sufficient for the G claim?
