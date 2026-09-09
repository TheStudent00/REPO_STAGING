# log 010 — token_tree re-parse coverage, measured

2026-08-05

**Scope caveat:** this measurement covers exactly two crates —
`~/Programming/Sources/rust/compiler/rustc_codegen_ssa` and
`~/Programming/Sources/rust/compiler/rustc_codegen_llvm` — both of which are sparse
relative to the full rustc tree (111 `.rs` files, 1616 macro invocations total).
`rustc_codegen_cranelift` was excluded per instruction. Numbers below are not a
claim about the whole compiler; they are a direct check of the log_002 §6.3
"~94% with ~20 shape entries" estimate against real token_trees from a bounded,
representative corpus. Tooling: `tree-sitter==0.26.0` + `tree-sitter-rust==0.24.2`
(Python bindings), same stack as the ledger_survey work.

## 1. What was collected

Every `macro_invocation` super-node was walked in all 111 files. For each one:
the macro path/identifier (via the grammar's `macro` field), and the raw byte
text strictly between the outer `token_tree` sub-node's opening and closing
delimiters (i.e. the delimiters themselves excluded).

- **Total macro invocations found: 1616**
- **Distinct macro names: 58**
- **Top 20 macro names by invocation count account for 1473 / 1616 = 91.15%**
  of all invocations by raw frequency (before any re-parse attempt — this is
  just "how concentrated is the name distribution," the input to the log_002
  claim, not the coverage result itself).

## 2. Shape table (top 20 by count)

Shapes: `expression` | `argument-list` | `statements` | `items` |
`format-first-arg-list` | `opaque` (own grammar, no standard shape fits).

Wrappers used, byte-exact:

| shape | wrapper |
|---|---|
| expression | `fn f(){let _=(CONTENT);}` |
| argument-list / format-first-arg-list | `fn f(){g(CONTENT);}` |
| array-literal (vec!-specific) | `fn f(){let _=[CONTENT];}` |
| statements | `fn f(){CONTENT}` |
| items | CONTENT parsed as a bare source file, no wrapper |
| opaque | never wrapped — counts as uncovered by definition |

`array-literal` was added as a variant of `argument-list` specifically because
`vec!` content splits into two incompatible forms — `vec![a, b, c]` (comma
list) and `vec![0; n]` (repeat form, semicolon-separated) — exactly the
`vec![0; n]` vs `vec![1,2,3]` tension log_002 §6.3 called out. A plain
`g(CONTENT)` call wrapper accepts the comma form but produces an ERROR on the
semicolon form (a semicolon is not valid inside a call argument list); wrapping
as an array literal `[CONTENT]` accepts both, because Rust's array-literal
grammar already has this exact two-form structure built in. Confirmed present
in the corpus, e.g. `vec![shift_idx; in_len as _]` and `vec![0; len as usize]`
in `rustc_codegen_llvm`.

| macro | count | shape | 1–2 observed examples |
|---|---|---|---|
| `bug!` | 219 | format-first-arg-list | `"unsupported float: {:?}", self` |
| `format!` | 201 | format-first-arg-list | `"~{{st({})}}", i` |
| `assert!` | 142 | argument-list | `self.size.bytes().is_multiple_of(hint_vector_elem.size(cx).bytes())` |
| `debug!` | 131 | format-first-arg-list | `"Asm Input Type: {:?}", *v` — also uses tracing's `?ident` field shorthand, see §3 |
| `matches!` | 105 | opaque | `scalar.primitive(), Primitive::Int(..)` (pattern + optional `if` guard, not an expression grammar) |
| `assert_eq!` | 104 | argument-list | `thin_modules.len(), module_names.len()` |
| `writeln!` | 88 | format-first-arg-list | `writer, "{module} {key}"` |
| `vec!` | 86 | array-literal | `shift_idx; in_len as _` and `tptr, ti64, ti32, tptr` |
| `unreachable!` | 69 | format-first-arg-list | `"clobber-only"` |
| `msg!` (rustc diagnostic) | 61 | format-first-arg-list | `"failed to parse target machine config to target machine: {$error}"` |
| `info!` | 43 | format-first-arg-list | `"adding bitcode from {}", name` |
| `write!` | 39 | format-first-arg-list | `template_str, "{offset:+}"` |
| `span_bug!` | 39 | format-first-arg-list | `line_spans[0], "LLVM asm constraint validation failed"` |
| `require!` | 29 | argument-list | `args[0].layout.ty == out_ty, InvalidMonomorphization::ExpectedVectorElementType { span, name, ... }` |
| `panic!` | 23 | format-first-arg-list | `"Architecture {arch} does not support GpuKernel calling convention"` |
| `if_regular!` | 21 | argument-list | `Some(sess.opts.optimize), None` |
| `debug_assert!` | 19 | argument-list | `scalar_b.is_always_valid(cx)` |
| `require_simd!` | 19 | argument-list | `args[1].layout.ty, SimdArgument` |
| `return_error!` | 18 | argument-list | `InvalidMonomorphization::SimdShuffle { span, name, ty: idx_ty }` |
| `assert_matches!` | 17 | opaque | `reg, InlineAsmRegOrRegClass::Reg(_)` (same pattern-grammar issue as `matches!`) |

Macros outside this 20-entry table (38 distinct names, 143 invocations total)
count as uncovered by construction, regardless of what a re-parse would show —
that is the definition of "not in the table" being tested.

## 3. Re-parse coverage result

A re-parse "covers" an invocation if the wrapped buffer, parsed fresh, has no
`ERROR` node and no `is_missing` sub-node anywhere strictly inside the injected
CONTENT region (byte range tracked precisely against the wrapper's known
prefix/suffix lengths).

| metric | value |
|---|---|
| Total invocations | 1616 |
| Covered (re-parses clean under its table shape) | 1341 |
| **Coverage %** | **82.98%** |
| log_002 §6.3 estimate | ~94% |
| Delta | −11.0 points |

Per-macro results (all 20 table entries plus the aggregate residue):

| macro | count | shape | covered | failed |
|---|---|---|---|---|
| `bug!` | 219 | format-first-arg-list | 219 | 0 |
| `format!` | 201 | format-first-arg-list | 201 | 0 |
| `assert!` | 142 | argument-list | 142 | 0 |
| `debug!` | 131 | format-first-arg-list | 122 | 9 |
| `matches!` | 105 | opaque | 0 | 105 |
| `assert_eq!` | 104 | argument-list | 104 | 0 |
| `writeln!` | 88 | format-first-arg-list | 88 | 0 |
| `vec!` | 86 | array-literal | 86 | 0 |
| `unreachable!` | 69 | format-first-arg-list | 69 | 0 |
| `msg!` | 61 | format-first-arg-list | 61 | 0 |
| `info!` | 43 | format-first-arg-list | 42 | 1 |
| `write!` | 39 | format-first-arg-list | 39 | 0 |
| `span_bug!` | 39 | format-first-arg-list | 39 | 0 |
| `require!` | 29 | argument-list | 29 | 0 |
| `panic!` | 23 | format-first-arg-list | 23 | 0 |
| `if_regular!` | 21 | argument-list | 21 | 0 |
| `debug_assert!` | 19 | argument-list | 19 | 0 |
| `require_simd!` | 19 | argument-list | 19 | 0 |
| `return_error!` | 18 | argument-list | 18 | 0 |
| `assert_matches!` | 17 | opaque | 0 | 17 |
| *(38 names not in table)* | 143 | — | 0 | 143 |
| **Total** | **1616** | | **1341** | **275** |

18 of 20 tabled macros hit 100% coverage under their assigned shape. The two
misses inside the table are `matches!`/`assert_matches!` (opaque by
construction, 122 combined failures) and a small residue inside `debug!`/`info!`
(10 combined failures) — see cause breakdown below.

## 4. Failure residue, grouped by cause

275 uncovered invocations, by cause:

| cause | count | % of failures | detail |
|---|---|---|---|
| macro-defines-its-own-grammar: pattern + guard syntax | 122 | 44.4% | `matches!(expr, Pattern::Variant(_) if guard)` and `assert_matches!` — the second CONTENT segment is a match-arm pattern, not an expression. `Primitive::Int(..)` and `X86InlineAsmRegClass::mmx_reg \| ...` are not valid as call arguments or as `let` expressions; `..` and `\|`-patterns are pattern-grammar-only tokens. No single one of the six candidate shapes accepts this. |
| macro-defines-its-own-grammar: tracing field shorthand | 10 | 3.6% | Inside `debug!`/`info!` specifically: the `tracing` crate's `?ident` shorthand (captures `ident` and formats it with `{:?}`) is not valid as a call-argument expression under standard Rust grammar — `?` is a postfix try-operator in real Rust, not a prefix debug-capture sigil. Examples: `debug!(?sym, ?fn_attrs)`, `info!(?err, "Error while checking if gold was the linker")`. This is a genuine own-grammar case nested inside an otherwise-covered macro family — the shape table is right at the macro-name granularity but wrong at the per-invocation granularity for this subset. |
| unknown macros not in the 20-entry table | 143 | 52.0% | 38 distinct names. Sampled inspection shows this residue is itself mixed: (a) same-shape twins of tabled macros that a slightly larger table would trivially pick up — `smallvec!` (14, array-literal-shaped like `vec!`), `trace!`/`warn!`/`println!`/`eprintln!`/`tracing::debug!` (28 combined, format-first-arg-list-shaped like `debug!`/`info!`), `debug_assert_eq!`/`debug_assert_ne!`/`assert_ne!` (10 combined, argument-list-shaped like `assert_eq!`), `std::assert_matches!`/`std::matches!` (4, same opaque case as `matches!`); and (b) macros with a real own grammar that resist all six shapes: `mem::offset_of!` (12, `Type, field.path` — a type-then-field-path grammar, not an expression), `find_attr!` (10, `tcx, def_id, Pattern(binding) => expr` — a match-arm-shaped DSL), `bitflags!`/`bitflags::bitflags!` (6, whole item definitions with a custom flag-constant sub-language — the log_002 §6.3 "bitflags-style" case, confirmed present), `rustc_index::newtype_index!` (2, doc-comment-plus-struct DSL), `declare_constant!` (9, `IDENT: Type` colon-typed-name pairs, invalid as an expression), and the `*_red!`/`arith_*!`/`*math_builder_methods!`/`load_ptrs_by_symbols_*!` family (≈18 combined, small internal codegen DSLs, one-off `ident: ident, bool`-shaped argument lists that are not valid call arguments because of the bare colon). |

Two categories the task asked to check for turned out empty in this corpus:
"guard patterns like `matches!` with `if`" is real and is the single largest
failure cause (122, see row 1); "genuinely malformed content" was not observed
— every failure traces to a real grammar mismatch between the macro's actual
argument-shape and the shape assigned (or to the shape not being assigned at
all), not to garbled or incomplete token_tree text.

## 5. Byte-offset sanity check

Three worked examples, confirming that offsets inside the re-parsed
(wrapped) buffer can be mapped back to exact byte coordinates in the original
source file. Method: for each invocation, `content`'s exact byte range inside
the original file is located directly (`file_bytes.find(content, outer_start)`,
unambiguous since it starts the search at the macro invocation's own
outer-node start byte); the wrapper's fixed prefix length gives the arithmetic
offset needed to translate any position inside the wrapped tree's injected
region back to `original_offset = orig_start + (wrapped_offset - prefix_len)`.

| # | macro | file | CONTENT byte range in original file | wrapped-tree top structure |
|---|---|---|---|---|
| 1 | `bug!` | `.../rustc_codegen_ssa/src/abi.rs` | 5408–5439 | `source_file → function_item → block → expression_statement → call_expression` (CONTENT lands inside `arguments`) |
| 2 | `format!` | `.../rustc_codegen_ssa/src/asm.rs` | 3595–3611 | same top structure, CONTENT inside `arguments` |
| 3 | `vec!` | `.../rustc_codegen_llvm/src/.../profiling.rs` | 433–464 | `source_file → function_item → block → let_declaration → array_expression` (CONTENT lands inside the array-literal's element list) |

One negative but useful finding from this check: `Parser.included_ranges`
pointed directly at the original file's CONTENT byte range (with no wrapper
text present) does **not**, by itself, recover a clean sub-tree — it reproduces
an `ERROR` co-node, because the CONTENT bytes alone (e.g. `"unsupported float:
{:?}", self`) are not syntactically valid at the top of a source file; they
only become valid once the wrapper's surrounding tokens are actually present
in the buffer being parsed. `included_ranges` is the right primitive for
multi-language embedding where the surrounding valid-language tokens already
exist in the same buffer; it is not a shortcut around needing the synthetic
wrapper here. The practical offset-recovery path that was confirmed to work is
the arithmetic remap above (wrapped-buffer offset minus fixed prefix length,
plus original CONTENT start), not `included_ranges`.

## 6. Rustc-specific macros: re-parseable, or genuinely opaque?

Contrast requested against `bug!`, `intrinsic_args!`, `if_regular!`,
`require_simd!`.

| macro | present in this corpus | count | re-parseable under a standard shape? |
|---|---|---|---|
| `bug!` | yes | 219 | Yes — `format-first-arg-list`, 219/219 covered (100%). Its content is ordinary `"fmt string", args...`, structurally identical to `panic!`/`format!`. |
| `span_bug!` | yes | 39 | Yes — `format-first-arg-list`, 39/39 covered (100%). Same shape as `bug!` with a leading `span` expression, which a call-argument list absorbs without difficulty. |
| `if_regular!` | yes | 21 | Yes — `argument-list`, 21/21 covered (100%). Content is comma-separated expression pairs, standard call-argument shape. |
| `require_simd!` | yes | 19 | Yes — `argument-list`, 19/19 covered (100%). |
| `require!` | yes | 29 | Yes — `argument-list`, 29/29 covered (100%). |
| `return_error!` | yes | 18 | Yes — `argument-list`, 18/18 covered (100%). |
| `msg!` | yes | 61 | Yes — `format-first-arg-list`, 61/61 covered (100%). |
| `intrinsic_args!` | **no** | 0 | Not present in `rustc_codegen_ssa` or `rustc_codegen_llvm` — confirmed absent by direct text search (`grep -rl "intrinsic_args!"` over both crates returns no files). Cannot be measured from this corpus; flagged rather than guessed. |
| `find_attr!` | yes | 10 | No — opaque relative to the six standard shapes. Its content is `tcx, def_id, Pattern(bindings) => expr`, a match-arm-shaped internal DSL; none of `expression`/`argument-list`/`statements`/`items`/`array-literal` accept a bare `=>` arm outside a `match` block. |
| `require_int_or_uint_ty!` | yes | 6 | Not in the 20-entry table (below the cutoff); not tested. |

The rustc-internal diagnostic macros sampled here (`bug!`, `span_bug!`,
`msg!`, `require!`, `require_simd!`, `return_error!`, `if_regular!`) are, in
this corpus, **not** a distinct hard case — every one of them reached 100%
coverage under one of the two most common shapes (`format-first-arg-list` or
`argument-list`). The genuinely opaque rustc-internal macro observed here is
`find_attr!`, which is opaque for the same structural reason as `matches!`: it
smuggles match-arm grammar (`Pattern => expr`) inside its token_tree.
`intrinsic_args!` could not be assessed — it does not occur in either crate in
scope.

## Appendix — measurement script

Ran against `tree-sitter==0.26.0`, `tree-sitter-rust==0.24.2` (pip). The
`tree_sitter.Node.child`/`child_count`/`child_by_field_name` calls below are
the library's own API names for a syntax tree's relational structure; no
prose in this log or in these comments otherwise uses parent/child-family
vocabulary for tree relations — super-node/sub-node/co-node/sub-tree are used
instead throughout.

```python
import os, glob, collections, pickle
from tree_sitter import Language, Parser
import tree_sitter_rust as tsrust

RLANG = Language(tsrust.language())
parser = Parser(RLANG)

ROOT = "~/Programming/Sources/rust/compiler"
DIRS = ["rustc_codegen_ssa", "rustc_codegen_llvm"]  # cranelift excluded (prohibited)

files = []
for d in DIRS:
    files += glob.glob(os.path.join(ROOT, d, "**", "*.rs"), recursive=True)

invocations = []
for fp in files:
    src = open(fp, "rb").read()
    tree = parser.parse(src)

    def walk(node):
        if node.type == "macro_invocation":
            name_node = node.child_by_field_name("macro")
            name = src[name_node.start_byte:name_node.end_byte].decode("utf8", "replace")
            tt = None
            for i in range(node.child_count):
                sub = node.child(i)
                if sub.type == "token_tree":
                    tt = sub
            if tt is not None:
                # strip the outer delimiter bytes to get raw CONTENT
                content = src[tt.start_byte + 1: tt.end_byte - 1]
                invocations.append({
                    "file": fp, "name": name, "content": content,
                    "outer_start": node.start_byte, "outer_end": node.end_byte,
                })
        for i in range(node.child_count):
            walk(node.child(i))

    walk(tree.root_node)

# --- shape wrappers ---
SHAPES = {
    "bug": "format-first-arg-list", "format": "format-first-arg-list",
    "assert": "argument-list", "debug": "format-first-arg-list",
    "matches": "opaque", "assert_eq": "argument-list",
    "writeln": "format-first-arg-list", "vec": "array-literal",
    "unreachable": "format-first-arg-list", "msg": "format-first-arg-list",
    "info": "format-first-arg-list", "write": "format-first-arg-list",
    "span_bug": "format-first-arg-list", "require": "argument-list",
    "panic": "format-first-arg-list", "if_regular": "argument-list",
    "debug_assert": "argument-list", "require_simd": "argument-list",
    "return_error": "argument-list", "assert_matches": "opaque",
}

def wrap(shape, content: bytes):
    if shape == "expression":
        return b"fn f(){let _=(" + content + b");}", 14, 14 + len(content)
    if shape in ("argument-list", "format-first-arg-list"):
        return b"fn f(){g(" + content + b");}", 9, 9 + len(content)
    if shape == "array-literal":
        return b"fn f(){let _=[" + content + b"];}", 14, 14 + len(content)
    if shape == "statements":
        return b"fn f(){" + content + b"}", 7, 7 + len(content)
    if shape == "items":
        return content, 0, len(content)
    return None

def has_error_in_region(node, lo, hi):
    if node.end_byte <= lo or node.start_byte >= hi:
        return False
    if node.type == "ERROR" or node.is_missing:
        return True
    return any(has_error_in_region(node.child(i), lo, hi) for i in range(node.child_count))

covered = 0
for inv in invocations:
    shape = SHAPES.get(inv["name"])
    if shape is None or shape == "opaque":
        continue
    wrapped, lo, hi = wrap(shape, inv["content"])
    tree = parser.parse(wrapped)
    if not has_error_in_region(tree.root_node, lo, hi):
        covered += 1

print(f"{covered}/{len(invocations)} = {covered/len(invocations)*100:.2f}% covered")
```

## open questions for the owner

- Is 82.98% (measured, 2 crates) close enough to the log_002 §6.3 "~94%"
  estimate to keep using that number in planning docs, or should the ~94%
  figure be retired/replaced now that a real measurement exists? Not this
  log's call.
- The single biggest failure cause (122/275, 44%) is the `matches!`-family
  pattern-plus-guard grammar. Is a seventh shape ("match-arm-pattern",
  splitting CONTENT into an expression part and a pattern part and wrapping
  as `fn f(){match (EXPR) { PATTERN => () }}`) worth adding, given `matches!`
  content doesn't reliably split on the first top-level comma (nested
  generics/turbofish contain commas too)? Left undecided here.
- Should the shape table be grown past ~20 entries toward the "same-shape
  twins" identified in §4 (`smallvec!`, `trace!`, `warn!`, `println!`,
  `eprintln!`, `debug_assert_eq!`, `debug_assert_ne!`, `assert_ne!`, roughly
  10 more names covering another ~50 invocations at near-zero design cost),
  or does that undercut the point of the original "~20 entries" framing?
- This log only used 2 sparse crates. Is a wider re-run (more of
  `~/Programming/Sources/rust/compiler`, cranelift still excluded) warranted
  before this number is treated as durable, or is 1616 invocations/58 macro
  names enough signal for now?
- `intrinsic_args!` could not be measured (absent from both crates in scope).
  Worth a follow-up log against whichever crate actually defines/uses it?
