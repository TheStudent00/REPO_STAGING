# log 002 — brainstorm: the `ur` node, and what tree-sitter actually provides

2026-08-02, at the owner's request, before deepening
`pcv5.tools.ledgerer.ur`. A working record per protocol §18a — nothing
here settles anything. Every tree-sitter output below was produced and
observed today in the sandbox (py-tree-sitter with the first-party
`tree-sitter-rust` wheel); every project claim carries its file.

Revised the same day after the owner's reading: the two-column example and
the vocabulary section are his requests, §6 is new, and §7's questions
were rewritten where his answers moved them.

---

## 1. The high-level picture

- **The UR is the tree-sitter tree, kept whole, plus layers it never
  had.** Strictly richer means the substrate is never discarded: every
  UR node keeps its tree-sitter kind, span, bytes, and position, and
  adds identity (the positional-path id), a normalized kind, and
  annotation slots. The prior UR-AST failed the "strictly richer"
  intent by REPLACING the tree with ~30 neutral classes; the fix is to
  make normalization an ANNOTATION on the tree, not a substitute for
  it.
- **The vocabulary question has a collapsible form.** A grammar's node
  vocabulary is finite, enumerable, and machine-readable — 163 named
  kinds for rust, countable at runtime and published as
  `node-types.json` with every grammar, complete with each kind's
  fields and the possible child kinds of each field. So "did we handle
  everything" is a checkable totality claim per language, not a hope.
- **Reliability splits cleanly in two.** As a source of FORM,
  tree-sitter is reliable and the project has the receipts. As a
  source of MEANING it provides nothing, by design — no types, no name
  resolution, macros unexpanded. That absence is not a defect to work
  around; it is the gap the ledger exists to fill.
- **A lot of what we might have written is already shipped as data.**
  Each grammar carries query files: `tags.scm` (definitions and
  references), `injections.scm` (regions to re-parse, which is the
  macro answer), `highlights.scm`. §6 covers what exists so we do not
  rebuild it.

---

## 2. A worked example — source beside its tree

`/tmp/sample.rs`, parsed today. The right column lists the NAMED nodes
whose span STARTS on that line: depth in the tree, the grammar's field
role where it has one, and the kind. `→L n` means the node's span runs
to line n. Anonymous nodes (`{`, `,`, `->`) are omitted here for
reading, but they are real children and they count in child indices —
which is why idgen's positional path counts named and anonymous alike.

```rust
use std::collections::HashMap;

pub struct Counter {
    counts: HashMap<String, u32>,
    label: String,
}

impl Counter {
    pub fn new(label: &str) -> Self {
        Counter { counts: HashMap::new(), label: label.to_string() }
    }

    pub fn bump(&mut self, key: &str) -> u32 {
        let n = self.counts.entry(key.to_string()).or_insert(0);
        *n += 1;
        *n
    }
}
```

| line | source | named nodes starting on this line (depth, field: kind) |
| --- | --- | --- |
| 1 | `use std::collections::HashMap;` | `0` **source_file** →L19<br>`1` **use_declaration**<br>`2` argument: **scoped_identifier**<br>`3` path: **scoped_identifier**<br>`4` path: **identifier**<br>`4` name: **identifier**<br>`3` name: **identifier** |
| 3 | `pub struct Counter {` | `1` **struct_item** →L6<br>`2` **visibility_modifier**<br>`2` name: **type_identifier**<br>`2` body: **field_declaration_list** →L6 |
| 4 | `    counts: HashMap<String, u32>,` | `3` **field_declaration**<br>`4` name: **field_identifier**<br>`4` type: **generic_type**<br>`5` type: **type_identifier**<br>`5` type_arguments: **type_arguments**<br>`6` **type_identifier**<br>`6` **primitive_type** |
| 5 | `    label: String,` | `3` **field_declaration**<br>`4` name: **field_identifier**<br>`4` type: **type_identifier** |
| 8 | `impl Counter {` | `1` **impl_item** →L18<br>`2` type: **type_identifier**<br>`2` body: **declaration_list** →L18 |
| 9 | `    pub fn new(label: &str) -> Self {` | `3` **function_item** →L11<br>`4` **visibility_modifier**<br>`4` name: **identifier**<br>`4` parameters: **parameters**<br>`5` **parameter**<br>`6` pattern: **identifier**<br>`6` type: **reference_type**<br>`7` type: **primitive_type**<br>`4` return_type: **type_identifier**<br>`4` body: **block** →L11 |
| 10 | `        Counter { counts: HashMap::new(), label: label.to_string() }` | `5` **struct_expression**<br>`6` name: **type_identifier**<br>`6` body: **field_initializer_list**<br>`7` **field_initializer**<br>`8` field: **field_identifier**<br>`8` value: **call_expression**<br>`9` function: **scoped_identifier**<br>`10` path: **identifier**<br>`10` name: **identifier**<br>`9` arguments: **arguments**<br>`7` **field_initializer**<br>`8` field: **field_identifier**<br>`8` value: **call_expression**<br>`9` function: **field_expression**<br>`10` value: **identifier**<br>`10` field: **field_identifier**<br>`9` arguments: **arguments** |
| 13 | `    pub fn bump(&mut self, key: &str) -> u32 {` | `3` **function_item** →L17<br>`4` **visibility_modifier**<br>`4` name: **identifier**<br>`4` parameters: **parameters**<br>`5` **self_parameter**<br>`6` **mutable_specifier**<br>`6` **self**<br>`5` **parameter**<br>`6` pattern: **identifier**<br>`6` type: **reference_type**<br>`7` type: **primitive_type**<br>`4` return_type: **primitive_type**<br>`4` body: **block** →L17 |
| 14 | `        let n = self.counts.entry(key.to_string()).or_insert(0);` | `5` **let_declaration**<br>`6` pattern: **identifier**<br>`6` value: **call_expression**<br>`7` function: **field_expression**<br>`8` value: **call_expression**<br>`9` function: **field_expression**<br>`10` value: **field_expression**<br>`11` value: **self**<br>`11` field: **field_identifier**<br>`10` field: **field_identifier**<br>`9` arguments: **arguments**<br>`10` **call_expression**<br>`11` function: **field_expression**<br>`12` value: **identifier**<br>`12` field: **field_identifier**<br>`11` arguments: **arguments**<br>`8` field: **field_identifier**<br>`7` arguments: **arguments**<br>`8` **integer_literal** |
| 15 | `        *n += 1;` | `5` **expression_statement**<br>`6` **compound_assignment_expr**<br>`7` left: **unary_expression**<br>`8` **identifier**<br>`7` right: **integer_literal** |
| 16 | `        *n` | `5` **unary_expression**<br>`6` **identifier** |

Lines 2, 6, 7, 11, 12, 17, 18 start no node: closing braces and blanks
are anonymous tokens or whitespace inside a span that began earlier.

### What the table shows that prose does not

- **Nesting depth tracks syntactic containment exactly.** L14's chained
  call reaches depth 12 on one source line. A design that flattens
  "one line = one record" loses most of that line.
- **Field roles are given, not inferred.** `name:`, `parameters:`,
  `return_type:`, `body:`, `pattern:`, `value:`, `left:`, `right:` come
  from the grammar. The prior UR-AST hand-built exactly these role
  slots in per-language visitor code; the grammar already carries them
  as data.
- **Types appear as SYNTAX, never as resolution.** L4 gives
  `generic_type` wrapping `type_identifier` (`HashMap`) and its
  `type_arguments`. That `HashMap` is the one from L1's `use` is
  nowhere in the tree — that join is exactly ledger work.
- **`self` is its own kind**, and `self_parameter` is distinct from
  `parameter` (L13). Language-specific structure survives at this
  layer whether or not a neutral layer flattens it.

---

## 3. The vocabulary — what a grammar's kind set looks like

Rust, counted live: **355 kinds total, 163 named** (the rest are
anonymous tokens — punctuation and keywords). Python for comparison:
274 total, 128 named. The named set is the routing surface, and it is
strikingly regular — the kinds come in families by suffix.

- **`_item` (14)** — top-level declarations: `attribute_item`,
  `const_item`, `enum_item`, `foreign_mod_item`, `function_item`,
  `function_signature_item`, `impl_item`, `inner_attribute_item`,
  `mod_item`, `static_item`, `struct_item`, `trait_item`, `type_item`,
  `union_item`.
- **`_expression` (26)** — `array_expression`, `assignment_expression`,
  `await_expression`, `binary_expression`, `break_expression`,
  `call_expression`, `closure_expression`, `continue_expression`,
  `field_expression`, `for_expression`, `if_expression`,
  `index_expression`, `loop_expression`, `match_expression`,
  `parenthesized_expression`, `range_expression`,
  `reference_expression`, `return_expression`, `struct_expression`,
  `try_expression`, `tuple_expression`, `type_cast_expression`,
  `unary_expression`, `unit_expression`, `while_expression`,
  `yield_expression`.
- **type-related (24)** — `abstract_type`, `array_type`,
  `associated_type`, `bounded_type`, `bracketed_type`, `dynamic_type`,
  `function_type`, `generic_type`, `generic_type_with_turbofish`,
  `never_type`, `pointer_type`, `primitive_type`, `qualified_type`,
  `reference_type`, `scoped_type_identifier`, `tuple_type`,
  `type_arguments`, `type_binding`, `type_identifier`, `type_item`,
  `type_parameter`, `type_parameters`, `unit_type`.
- **bare kinds** — `arguments`, `attribute`, `block`, `crate`,
  `identifier`, `label`, `lifetime`, `metavariable`, `parameter`,
  `parameters`, `self`, `shebang`, `super`.

### `node-types.json` — the vocabulary as a document

Every grammar generates `src/node-types.json` describing each kind:
whether it is named, its fields, and the possible child kinds per
field. Two facts about it matter for `ur`:

- It makes the ts_kind→ur_kind map **checkable for totality** — a kind
  in the file with no mapping is a hole the census names.
- It carries **supertypes**: a grammar may declare hidden rules like
  `expression` as supertypes, and the file then records the subtypes
  each one wraps. That is a normalization layer the GRAMMAR AUTHOR
  already wrote. Where a grammar declares good supertypes, part of
  `ur_kind` may be read off rather than invented.

The file itself is not in the Python wheel — it lives in the grammar
repository beside the generated parser — but **the same information is
on the compiled `Language` object at runtime**: `supertypes`,
`subtypes(id)`, `node_kind_is_supertype`. Rust declares five, verified
today:

| supertype | subtypes | first few |
| --- | --- | --- |
| `_expression` | 40 | `_literal`, `array_expression`, `assignment_expression`, `async_block`, `await_expression`, `binary_expression`, `block`, `call_expression` |
| `_type` | 33 | `type_identifier`, `primitive_type`, … |
| `_pattern` | 18 | `_`, `_literal_pattern`, `captured_pattern`, `const_block`, `generic_pattern`, `identifier`, `macro_invocation` |
| `_literal_pattern` | 7 | `boolean_literal`, `char_literal`, `float_literal`, `integer_literal`, `negative_literal` |
| `_literal` | 6 | `boolean_literal`, `char_literal`, `float_literal`, `integer_literal`, `raw_string_literal`, `string_literal` |

So for rust, a large part of a neutral kind layer is READABLE rather
than invented: "is this an expression" is `_expression`'s subtype set,
maintained by the grammar author. Supertypes nest (`_literal` inside
`_expression`), so the layer is a small hierarchy, not a flat tag set.
Still unverified: per-grammar uptake elsewhere — c and cpp were not
checked today, and a grammar that declares none gives no help here.

---

## 4. Error recovery

`fn broken(a: { let x = ; }` parses to a tree with an `ERROR` node over
the unparseable stretch and correct structure resuming after it;
`root.has_error` flags it, and genuinely absent tokens appear as
MISSING nodes. Broken input degrades locally rather than failing the
parse — relevant because compiler sources under a pinned grammar will
occasionally use syntax the pin predates.

---

## 5. Macros: what the grammar gives, and what it does not

### 5.0 What "macro" means here

**macro**

- code that writes code. the programmer writes a short invocation; the
  compiler REPLACES it, before compiling, with whatever source the
  macro generates. so the text in the file is not the text that gets
  compiled.
- example tied to context: in rust, `println!("{}", x)` is a macro
  invocation — the `!` marks it. what actually compiles is a block of
  formatting and io calls the macro expands to, which appears nowhere
  in the file. rustc's own sources use macros heavily, and rustc's
  sources are pcv5's first ingest target.

Two related terms, since they come up together below.

**expansion**

- running the macro to produce the code it stands for. done by the
  language's compiler (rustc), not by a parser.
- example tied to context: `twice!(add(1, 2))` expands to
  `add(1, 2) + add(1, 2)`. no amount of parsing recovers that; only
  rustc knows the rule, because the rule is itself written in the file
  as `macro_rules! twice`.

**token_tree**

- tree-sitter's node kind for the contents of a macro invocation: a
  flat, brace-matched list of tokens with NO grammatical structure
  assigned. the grammar's honest way of saying "these are the
  characters; what they mean depends on a macro I cannot run."
- example tied to context: in the observation below, `(add(1, 2))` is
  one token_tree — there is no call_expression node inside it, so
  there is nothing for the ledger to record about that call.

Why this matters to `ur` and not merely to trivia: a UR built over raw
tree-sitter sees a `macro_invocation` and a `token_tree`, and nothing
about what the macro produces. For a project whose first target is a
compiler's own source, that is the difference between recording most
of a file and recording most of what the file MEANS.

### 5.0a Why a language would rely on macros at all

Asked by the owner, 2026-08-02: "why would a language rely on macros? i dont
see the benefit."

The benefit is always the same one — **removing repetition that the
type system cannot remove** — and it shows up where a function cannot
reach:

- **Variable arity and heterogeneous types.** `println!("{} {}", n,
  name)` takes any number of arguments of different types, checked at
  compile time. Rust has no variadic generic functions, so without a
  macro this is either N overloads or a runtime-typed list.
- **Code that must exist per type, not per value.** `#[derive(Clone,
  Debug)]` writes a `Clone` impl and a `Debug` impl for THAT struct's
  actual fields. A function cannot write an impl block.
- **Compile-time work.** `include_str!("x.txt")` embeds a file's
  contents at build time; `cfg!` selects code per platform before
  compilation. There is no runtime moment at which these could happen.
- **Tables that generate code.** The clearest example is in the file
  measured below: rustc lists 60 built-in macros as name-and-function
  pairs, and a macro turns each line into a registration call. Written
  by hand that is 60 near-identical statements to keep in step.

The cost is exactly our problem: **the source stops saying what the
program does.** A reader — human or transpiler — sees the invocation,
not the code. Rust accepts that cost deliberately, which is why the
language ships tooling (`cargo expand`, `-Zunpretty=expanded`) whose
whole purpose is showing the expansion.

### 5.0b Where macros are defined — with the two mechanisms kept apart

There are two different answers, and conflating them was implicit in
the question as asked ("how are macros defined? in the compiler").
Verified today against `rust-lang/rust` master, fetched 2026-08-02
(master moves; no commit pin was taken, so treat the line numbers as
"as fetched today").

**(1) Declarative macros — defined in ordinary source, not in the
compiler.** `macro_rules! twice { ... }` can appear in any `.rs` file,
including rustc's own. The compiler contains the machinery that
EXPANDS them, in the crate `compiler/rustc_expand/` (its
`src/mbe/macro_rules.rs` is the matcher). *Unverified: I have not
opened that file this session; the path is from the crate layout, not
from a read.*

**(2) Built-in macros — implemented IN the compiler, in Rust.** These
are the ones with no source-level definition anywhere: `println!`,
`assert!`, `derive`, `include_str!`. They live in
`compiler/rustc_builtin_macros/`, and the registration table is
`compiler/rustc_builtin_macros/src/lib.rs`, which I fetched and
measured (152 lines):

| line | what is there |
| --- | --- |
| L61 | `pub fn register_builtin_macros(resolver: &mut dyn ResolverExpand)` — the single entry point that installs every built-in |
| L63, L66, L69 | three `macro` definitions — `register_bang`, `register_attr`, `register_derive` — each turning a table line into a `register(...)` call |
| L73 | `register_bang! { ... }` — **31 entries**, the `name!()` macros: `asm`, `assert`, `cfg`, `column`, `compile_error`, `concat`, `env`, `file`, `format_args`, `include`, `include_bytes`, `include_str`, `line`, `module_path`, `option_env`, `stringify`, `unreachable`, … |
| L109 | `register_attr! { ... }` — **17 entries**, the `#[name]` attribute macros: `alloc_error_handler`, `bench`, `cfg_eval`, `derive`, `global_allocator`, `test`, `test_case`, … |
| L131 | `register_derive! { ... }` — **12 entries**, the `#[derive(Name)]` macros: `Clone`, `Copy`, `Debug`, `Default`, `Eq`, `Hash`, `Ord`, `PartialEq`, `PartialOrd`, `ConstParamTy`, `CoercePointee`, `From` |
| L145–L151 | four more registered individually: `quote`, `contracts_requires`, `contracts_ensures` |

So: **60 built-in macros registered in one table**, plus the
individually registered handful. Each name in the table points at a
function elsewhere in the same crate that does the expanding — e.g.
`assert: assert::expand_assert` sends `assert!` to
`rustc_builtin_macros/src/assert.rs`.

Note what that table IS: a list of macros, written using a macro.
Which is §5.0a's last bullet, in the compiler's own source.

### 5.0c A hard finding: the grammar cannot parse that file

Measured today, and it changes the reliability picture more than the
macro question does.

`rustc_builtin_macros/src/lib.rs` parsed with the stock
`tree-sitter-rust` grammar yields **`has_error: True`, with a single
`ERROR` node spanning L1–L153 — the entire file.** Not a local island:
nothing in the file is recoverable structure.

Bisected to the cause, with minimal cases:

| construct | parses? |
| --- | --- |
| `fn f() { let x = 1; }` | yes |
| `macro_rules! m { () => { 1 } }` (stable macros) | yes |
| `#![feature(decl_macro)]` (inner attribute) | yes |
| `m! { a: b, }` (macro call, brace form) | yes |
| `macro m($x:ident) { $x }` (**decl_macro, unstable**) | **no** |

rustc's own source uses `#![feature(decl_macro)]` and the `macro`
keyword — nightly-only syntax. The stock grammar targets stable Rust,
so it fails, and because the construct sits inside a function body the
failure swallows the enclosing item and cascades to the file.

Consequences worth carrying into the design, none of them fatal:

- **"Reliable as a form substrate" needs a qualifier**: reliable for
  the language the grammar targets. rustc is not written in that
  language — it is written in nightly Rust with feature gates.
- **Error recovery is weaker than §4's small example suggested.** A
  local break stayed local there; here one unsupported construct at
  depth took the whole file. Whether damage stays local depends on
  where the construct sits.
- **This is measurable before it is a surprise**, which is the
  argument for the census: parse every target file, count
  `has_error`, and know the number before building on it.
- **Options if it bites**: patch/fork the grammar for the feature
  syntax (grammars are just files, and pinning already implies we
  control which); or preprocess with the compiler's own expansion so
  the ingested source is expanded stable Rust; or accept per-file
  refusal, honestly recorded, and ingest what parses.

### 5.0d How often macros are actually used — MEASURED 2026-08-02

Run in the podman sandbox's agent lane against
`Sources/rust/compiler`, grammar pinned to PCv6's
manifest of record (`tree-sitter==0.26.0`,
`tree-sitter-rust==0.24.2`), by
`PRIVATE/PseudoCoup_v5/Research/census_macros.py`. Raw output
kept at `SandboxDesign/agent/out/macro_census2.txt`.

**Scope caveat, stated first because it bounds everything below:** the
checkout is a SPARSE one — three codegen crates, 187 `.rs` files,
84,452 lines. rustc as a whole is roughly 250 crates. This is the
codegen slice, which is the slice this project targets, not "the
compiler" entire.

Excluding the banned backend's crate, which the sparse checkout still
carries (see §5.0e):

| | rustc_codegen_ssa | rustc_codegen_llvm | both |
| --- | --- | --- | --- |
| files | 57 | 54 | 111 |
| macro invocations | 900 | 698 | 1,598 |

Over all 187 files including the banned crate: 2,854 invocations, 29
`macro_rules!` definitions, 235 derive attributes — **15.8 invocations
per file, 35.6 per thousand lines.**

The distribution is the useful part. The top ten account for well over
half of all invocations:

| count | macro | what it is |
| --- | --- | --- |
| 427 | `assert_eq!` | test/invariant checking |
| 327 | `format!` | string building |
| 263 | `bug!` | rustc's internal-compiler-error macro |
| 219 | `assert!` | invariant checking |
| 197 | `intrinsic_args!` | rustc-specific, destructures intrinsic call args |
| 193 | `vec!` | collection literal |
| 183 | `unreachable!` | control-flow assertion |
| 131 | `debug!` | tracing |
| 123 | `matches!` | pattern test as an expression |
| 118 | `writeln!` | formatted output |

**What that means for `ur`, and it is not what the earlier framing
implied.** The overwhelming majority of these are LEAF-ISH macros:
assertions, formatting, logging, collection literals. Their token
trees contain ordinary expressions, and their expansions do not
restructure the surrounding code. Only a handful — `intrinsic_args!`,
`bug!`'s span variants, the `if_regular!` / `require_simd!` family —
are rustc-specific control constructs whose meaning is genuinely
opaque without expansion.

So the macro problem is smaller than "rustc is macro-heavy" suggests:
re-parsing token trees (§6.3) recovers the arguments of `assert_eq!`,
`format!`, `vec!` and friends as real expressions, which is most of
the 2,854. Expansion is needed only for the rustc-specific minority.

### 5.0e Ingestibility, measured in the same pass

**181 of 187 files parse clean (96.8%); 6 contain an ERROR node
(3.2%). By line: 80,135 of 84,452 clean (94.9%).**

That is far better than §5.0c's single-file result suggested, and it
corrects the impression that finding: one file failing catastrophically
is not the norm. The six:

- `rustc_codegen_llvm/src/macros.rs`
- `rustc_codegen_llvm/src/llvm/ffi.rs`
- `rustc_codegen_llvm/src/llvm/enzyme_ffi.rs`
- `rustc_codegen_ssa/src/traits/mod.rs`
- `rustc_codegen_ssa/src/traits/type_.rs`
- one example file in the banned crate

Unverified: I have not bisected each of the six. The named suspect
from §5.0c — the unstable `macro` (decl_macro) keyword — is the likely
cause in at least `macros.rs` and the FFI files, but that is inference
from the earlier bisection, not a measurement of these six.

**The banned backend's crate is still in this checkout**:
`rustc_codegen_cranelift`, 76 files, 1,256 of the 2,854 invocations.
It is there because the sparse-checkout config on disk predates the
2026-08-02 prohibition; the rewritten `fetch_sources.sh` only governs
a fresh clone. Removing it from the working tree is one command on the
host and is the owner's to run:

```bash
git -C Sources/rust sparse-checkout set \
    compiler/rustc_codegen_ssa compiler/rustc_codegen_llvm
```

### 5.0f How the earlier "not measured" note read

the owner asked for the count. **I cannot produce it on this machine**, and
the reason is concrete rather than a shrug:

- The vendored rustc sources are NOT on disk.
  `PRIVATE/PseudoCoup_v5/Research/rust_routing/sources/` does not
  exist; it is created by that folder's `fetch_sources.sh`, which does
  a sparse `git clone` of `rust-lang/rust`, and it was never committed
  (nothing in git history under that path). This is also why PCv6's
  six `PCV5_ROOT` tests currently have nothing to resolve against.
- The sandbox has no rust toolchain (`rustc`, `cargo`, `rustup` all
  absent), and fetching the tree file-by-file over the network is not
  a census.

What can be run on the host, after `./fetch_sources.sh` in
`PRIVATE/PseudoCoup_v5/Research/rust_routing/`:

```bash
SRC=PRIVATE/PseudoCoup_v5/Research/rust_routing/sources/rust/compiler
# 1. crude but instant: invocation-shaped occurrences, and derive attrs
grep -rEo '\b[a-z_][a-z0-9_]*!' "$SRC" --include='*.rs' | wc -l
grep -rEo '#\[derive\([^)]*\)\]' "$SRC" --include='*.rs' | wc -l
# 2. the honest count: macro_invocation nodes, and how many files parse at all
python3 census_macros.py "$SRC"     # tree-sitter walk; to be written
```

The grep is an approximation — it counts `!` in string literals and
comments too — but it is the right order-of-magnitude first look. The
tree-sitter census is the real number AND gives the `has_error` rate
from §5.0c in the same pass, which is the more decisive figure for
whether rustc is ingestible as-is.

I can run both here the moment the sources are fetched, or write
`census_macros.py` now so it is ready.

### 5.1 What was observed

`let x = twice!(add(1, 2));` yields

- `macro_invocation` containing `identifier`, `!`, and `token_tree`.

A `token_tree` is a flat token list. The `add(1, 2)` call inside it has
no `call_expression` node — no structure, so nothing to ledger. Same
for `macro_rules!` bodies. rustc is macro-heavy, so this is real for
the first target.

**The grammar ships the first answer to this** (§6.3): re-parsing the
token content. Verified today — feeding `add(1, 2)` back through the
parser in a valid context yields the full `call_expression` →
`arguments` → `integer_literal` structure with no error. What re-parse
does NOT do is expand the macro: `twice!` doubling its argument is
invisible either way. Re-parsing recovers the syntax of what was
WRITTEN; only expansion gives what the compiler SEES.

---

## 6. What the tree-sitter API already does, so we do not rebuild it

Everything in §6.1–§6.8 is the tree-sitter API itself (py-tree-sitter
0.26.0, inspected today) or files shipped inside the grammar wheel.
§6.9 is external and marked as such.

### 6.0 The API surface, by what it answers

| the job | what the API gives |
| --- | --- |
| walk the tree efficiently | `TreeCursor` — `goto_first_child`, `goto_next_sibling`, `goto_parent`, plus `depth` and `descendant_index`. Cursor walking, not recursion over `children` lists |
| find the node at a position | `Node.descendant_for_byte_range`, `named_descendant_for_byte_range`, `descendant_for_point_range`, `first_child_for_byte` |
| read the grammar's role for a child | `Node.field_name_for_child`, `child_by_field_name`, `children_by_field_name` |
| enumerate the vocabulary | `Language.node_kind_count`, `node_kind_for_id`, `node_kind_is_named`, `node_kind_is_visible` |
| read the neutral kind hierarchy | `Language.supertypes`, `subtypes`, `node_kind_is_supertype` (§3) |
| get exact source text | `Node.text`, `byte_range`, `start_point` / `end_point` |
| tell comments from code | `Node.is_extra` — extras are IN the tree, flagged, not dropped |
| tell broken from missing | `Node.is_error`, `is_missing`, `has_error`, `Tree.root_node.has_error` |
| parse only part of a file | `Parser.included_ranges` (§6.3) |
| re-parse after an edit | `Tree.edit` + `Parser.parse(new_src, old_tree)`, then `Tree.changed_ranges`, `Node.has_changes` |
| select nodes by pattern | `Query` / `QueryCursor` (§6.1) |
| know what could come next | `LookaheadIterator` — valid symbols at a parse state |
| debug a tree visually | `Tree.print_dot_graph`, `Parser.print_dot_graphs`, `Parser.logger` |
| identify grammar version | `Language.name`, `abi_version`, `semantic_version` — rust today: abi 15, semver 0.24.1 |

Two of these bear directly on design choices we were about to make.
`Language.semantic_version` means **grammar pinning is checkable at
runtime**, not just at install time — the census can refuse a grammar
that is not the pinned one. And `Node.is_extra` means **comments are
already in the tree and already labelled**, so preserving them costs
nothing; PyHaxe's "comment preservation via tokenize" (transpiler
survey §3) was solving a problem this API does not have.

### 6.1 Queries are a data language for selecting nodes

Tree-sitter has an S-expression query language: patterns match node
structure and fields, `@captures` name what matched, and predicates
filter. Queries are DATA — text files loaded at runtime, not compiled
visitor code. This is directly relevant to open question 2 (map as
data or code): the "select these nodes, call them this" job already
has a data format with an engine behind it.

### 6.2 `tags.scm` — definitions and references, already written

Shipped in the rust wheel, 60 lines. Run against §2's sample today, it
captured, with no code written by us:

| capture | what it found in the sample |
| --- | --- |
| `definition.class` | `struct_item` Counter (L3) |
| `definition.function` | `new` (L9), `bump` (L13) |
| `definition.method` | `new` (L9), `bump` (L13) |
| `reference.implementation` | `impl_item` (L8) |
| `reference.call` | `label.to_string()` (L10), `key.to_string()`, `self.counts.entry(...)`, `.or_insert(...)` (L14) |
| `name` | the identifier inside each of the above |

This is the definition/reference split the ledger needs, per language,
maintained upstream. It is not name RESOLUTION — `reference.call` says
"a call happens here", not "it calls that definition" — but it is the
half that is pure syntax, and it is done.

### 6.3 `injections.scm` plus `included_ranges` — the opaque-region mechanism

Two halves, both in the API. The rust wheel's entire `injections.scm`
is two patterns: the `token_tree` of a `macro_invocation`, and of a
`macro_rule`, each declared as rust content to be re-parsed. So "which
regions are opaque, and what language is inside them" is
grammar-supplied data, not something we detect.

The execution half is `Parser.included_ranges`: the parser is told to
read only certain byte ranges and to treat everything else as absent.
Verified today — given `IGNORED PREFIX <<< fn g() { 1 + 2 } >>>
IGNORED SUFFIX` with `included_ranges` set to the middle span, the
parse yields a clean `source_file > function_item > block >
binary_expression` with no error, and the surrounding text is not a
parse problem because the parser never saw it. Byte offsets stay TRUE
TO THE ORIGINAL FILE, which is what lets a re-parsed macro body keep
addresses in the enclosing file's coordinate system.

#### CORRECTION, 2026-08-02: re-parsing is not general

An earlier draft of this section claimed re-parsing "recovers the
syntax as written", on the strength of one case (`add(1, 2)` inside a
`token_tree`, which parses cleanly as an expression). **That was one
lucky example generalized.** Measured against real macro shapes, the
naive re-parse fails on most of them:

| macro content | as expression | as argument list | as statements | as items |
| --- | --- | --- | --- | --- |
| `assert_eq!(a, b)` | no | **yes** | no | no |
| `format!("{} {}", x, y)` | no | **yes** | no | no |
| `vec![1, 2, 3]` | no | **yes** | no | no |
| `vec![0; n]` | **yes** | no | **yes** | no |
| `matches!(x, Some(_))` | no | **yes** | no | no |
| `matches!(x, Some(v) if v > 3)` | no | no | no | no |
| `write!(f, "{}", x)` | no | **yes** | no | no |
| `asm!("mov {0}, {1}", out(reg) a, in(reg) b)` | no | no | no | no |
| `cfg!(target_os = "linux")` | **yes** | **yes** | **yes** | no |
| `bitflags`-style block | no | no | no | no |
| `math_builder_methods! { add(a,b) => ... }` | no | no | no | no |

**No single assumed shape fits everything**, and two common macros
need opposite assumptions: `vec![0; n]` is an expression, while
`vec![1, 2, 3]` is an argument list. `matches!` with a guard fits
nothing, because its second argument is a PATTERN plus a guard — a
shape that appears nowhere else in the language.

So re-parsing is not a general recovery mechanism. It is a per-macro
one: it works once you already know which shape that macro takes.

#### Why the opacity exists at all

Not a tree-sitter weakness. **In Rust the macro defines the grammar of
its own arguments**, so no fixed grammar could parse macro contents —
and rustc does the same thing tree-sitter does, capturing an unparsed
token stream at parse time and deferring until expansion.

What the grammar CAN guarantee is exactly one thing: **balanced
delimiters.** That is the language's actual rule for macro input.
`token_tree` is therefore not a shrug; it is the strongest claim true
of every macro.

The contrast that explains the trade:

- **Lisp** — macros operate on already-parsed s-expressions. The
  reader parses a macro call like any other list, because code and
  data share one syntax. Macros are transparent to the parser.
- **Rust** — macros operate on token streams, before structure
  exists, precisely so they can introduce syntax the language does not
  have (`bitflags!`, `html!`, inline assembly). The expressive power
  IS the opacity.

#### What follows for `ur`

"Knowing the shape" is per-macro knowledge, and it is small tabular
data rather than code: macro name -> argument shape -> how to lift it
into UR. `assert_eq!` -> argument list, droppable. `vec!` -> two
shapes, both known. `math_builder_methods!` -> block dialect, needs a
real model. Per §5.0d's distribution, roughly twenty entries would
cover 94% of invocations in the measured crates.

The same mechanism serves genuinely embedded languages — SQL inside a
string, JS inside HTML — which is what injections were built for.

### 6.4 Incremental parsing and editing

`Tree.edit(...)` then `Parser.parse(new_source, old_tree)` re-parses
reusing unchanged subtrees; `Tree.changed_ranges(old, new)` reports
what actually moved, and `Node.has_changes` flags affected nodes.
Relevant to the owner's on-the-fly scenario (§8.2): keeping something current
against a changing file without a full rebuild.

### 6.5 Stack graphs — cross-file name resolution as prior art

*(EXTERNAL — not the tree-sitter API. A separate project built on top
of it, listed because it solves the composition shape the owner described.)*

GitHub's `stack-graphs` / `tree-sitter-stack-graphs` builds name
BINDING on top of tree-sitter: rules written in a graph-construction
DSL turn each file's syntax tree into a graph fragment, and binding
paths cross from one file to another when a root node is reached, so
resolution composes across files while staying per-file incremental.
It exists for Python, JavaScript, Java, Go.

This is the closest prior art to the owner's `build.merge([ledger_0,
ledger_1])`: same shape — per-file artifacts that compose — solved for
name binding at scale. Worth reading before designing the merge, even
if we do not adopt it. Two caveats, both unverified here: whether a
rust ruleset exists at usable quality, and that its output is a
binding graph, not our ledger, so adoption would mean either
translating its graph into ledger connections or borrowing only the
composition design.

---

## 7. Envisioning `ur` — a draft to argue with

### 7.1 One node shape, four layers

```
class URNode
	attributes:
		ts_kind
		named
		span
		fields
		children
		language
		id
		ur_kind
		semantic
		connections
	methods:
		text
		field
		walk
```

The layers, and where each comes from:

- **substrate** — `URNode.ts_kind`, `URNode.named`, `URNode.span`,
  `URNode.fields`, `URNode.children`, `URNode.language`. Exactly what
  §2 showed the parser provides, kept rather than transformed.
  `URNode.text` recovers source text from the span against the
  retained bytes; losslessness is substrate plus those bytes, nothing
  more.
- **identity** — `URNode.id`, the positional path (harvest part 2.1),
  minted by `ts_to_ur_mapper` during the walk. Carried as a field
  because the addendum found its absence is what broke the old
  UR-AST.
- **normalization** — `URNode.ur_kind`, a language-neutral tag. This
  is where the old UR-AST's value survives: as a TAG on the real node
  rather than a class replacing it. A neutral consumer reads
  `URNode.ur_kind`; anything needing the substrate still has it.
- **annotation** — `URNode.semantic` and `URNode.connections`, the
  slots the ledger reads and writes. `ur` defines the forms; the
  mappers fill them. `URNode.connections` is the owner's carrying capacity
  at the node level.

`ts_to_ur_mapper.map()` --> `URNode.id`, `URNode.ur_kind`
`ur_to_ledger_mapper.map()` --> `URNode.semantic`, `URNode.connections`

### 7.2 What this dissolves

- The addendum's "two trees that never met" (§2.5 there): there is one
  tree. The verification family's substrate and the semantic family's
  payload become layers of one node, joined by construction rather
  than by a mapping someone maintains.
- The transpiler survey's "two IR philosophies" tension softens: the
  tagged-tree line becomes a normalization layer OVER the concrete
  tree that the flat/compiled-probe line works against, rather than a
  competing structure.

---

## 8. Open questions

### 8.1 Macros — reframed after the owner's correction

**The earlier framing was wrong** and is corrected here rather than
deleted. It said macros bear on "whether compiler sources are
ingestible at useful depth", conflating two unrelated things. the owner,
2026-08-02:

> the ledgerer will ingest a single file. it produces a ledger. if
> another file contains the definitions of objects already on the
> ledger, it extends the ledger and its connections. the choice of
> following is for the transpiler and transpiler config/input.

So cross-file reach is not a ledgerer limit at all — it is
`builder.merge([ledger_0, ledger_1])`, and WHETHER to follow is the
transpiler's call. Also settled by the same message, and worth stating
because it bounds this node: **the ledgerer does not decide what is a
wrapper.** It holds nodes, and connects a node to a definition when it
can. Wrapper construction over unfollowed definitions is the
transpiler's.

What actually remains of the macro question, then, is narrow and
within one file: a `token_tree` has no structured nodes, so there is
nothing to record inside it. Three postures, and they compose:

1. **Record it honestly** — the `token_tree` becomes one UR node
   marked opaque, in the refusal posture applied to form: never
   silently empty, so a consumer can halt or skip knowingly.
2. **Re-parse via `injections.scm`** (§6.3) — grammar-supplied,
   verified working today. Recovers the syntax as written. Open
   sub-question: do re-parsed nodes get ids under the enclosing
   token_tree's path (a sub-address space), and are they marked as
   injected rather than direct?
3. **Expansion** is a different tool's job — it needs the real
   compiler, and it changes what the source IS. Notably it belongs
   with the tracer family's "observe the real thing" posture rather
   than with parsing.

### 8.2 The ts_kind→ur_kind map: data, code, or both

the owner leans data, "but potentially both", with a scenario: a transpiler
or tracer wanting a ledger on the fly, "without having to construct a
parser or whatever", or to keep something from going stale.

That scenario splits into two capabilities worth keeping apart:

- **Extracting without writing a visitor** — this is what queries
  (§6.1) already are. A `.scm` file plus the engine, no per-language
  code. `tags.scm` proves the pattern at exactly our granularity.
- **Updating without a full rebuild** — that is incremental parsing
  (§6.4), and it needs the parser, just not a fresh parse of the whole
  file.

A shape that satisfies both: the map is DATA (a per-language table, or
literally a query file), the census checks it against
`node-types.json` for totality, and generated or thin dispatch code
executes it. Code stays the engine; data stays the vocabulary. The
lineage's visitors put both in one place, which is why every new
language meant new code.

### 8.3 Serialization — the question restated plainly

The earlier phrasing ("byte-fidelity rules") assumed the ledger
context. Plainly: **does a UR tree ever get written to a file, or does
it only exist in memory during a run?**

- The 289-line ledger writes itself to JSON and reads itself back, with
  rules that make the round trip exact — sets become sorted arrays,
  tuples become arrays, and derived values are deliberately not
  written because they go stale and are recomputed. That is what
  "byte-fidelity" referred to: dump, load, dump again, and the second
  file matches the first byte for byte.
- The old UR-AST had no such thing: plain Python objects, never
  written anywhere.
- So the question for `ur`: if the ledger is the durable artifact and
  UR is scaffolding rebuilt by re-parsing, UR needs no format at all.
  If anything downstream wants the UR tree without the source, it
  needs one — and then it needs the same round-trip discipline, or it
  becomes a second store that can disagree with the first.

The keying note already leans one way: ids are addresses in the parse
tree as vendored, and re-ingesting changed source changes them. That
assumes re-parsing is normal rather than exceptional.

### 8.4 "The ~30-kind vocabulary" — what that phrase meant

It was shorthand for the class list in
`PUBLIC/PseudoCoup/pseudocoup/core/ur_ast.py` (154 lines): a
base `URNode` plus roughly thirty subclasses, one per neutral
construct — `ModuleNode`, `ClassDefNode`, `FunctionDefNode`,
`MethodDefNode`, `AssignmentNode`, `BinaryOpNode`, `UnaryOpNode`,
`CastNode`, `IdentifierNode`, `CallNode`, `IfNode`, `ForNode`,
`ModifierNode`, `DeclarativeNode`, and so on. Not snippets — Python
classes, each with a fixed set of child slots. Every language's
ingestor mapped its grammar's kinds onto those thirty, and every
emitter walked them.

the owner, 2026-08-02: "idk if i want to re-use anything from older work.
perhaps later on. currently, im looking to build some things fresh."
So the question is not what survives. It is: **what neutral kinds does
`ur_kind` need at all**, derived from the grammars we target rather
than inherited from a set grown for Kotlin-to-Dart application
transpilation. §3's family structure (14 items, 26 expressions, 24
type kinds for rust) is a better starting point than the old thirty,
and `node-types.json`'s supertypes may supply part of it directly.

---

## 9. Sources

- tree-sitter observations: produced 2026-08-02 in the sandbox,
  py-tree-sitter with the first-party `tree-sitter-rust` and
  `tree-sitter-python` wheels, plus the query files shipped inside the
  rust wheel (`queries/tags.scm`, `queries/injections.scm`,
  `queries/highlights.scm`). NOTE: wheel versions were whatever pip
  resolved today, not pinned — fine for a brainstorm, exactly what the
  pinning discipline forbids for real ingest.
- Static node types and supertypes:
  https://tree-sitter.github.io/tree-sitter/using-parsers/6-static-node-types
- Stack graphs: https://docs.rs/tree-sitter-stack-graphs and the
  paper, https://arxiv.org/pdf/2211.01224
- `PRIVATE/PseudoCoup_v5/DevComms/ledger_survey_2026-08-02_tree_sitter_ur_ast.md`
  — the addendum this builds on.
- `PRIVATE/PseudoCoup_v5/DevComms/log_001_ledgerer_harvest_findings.md`
  — the nine harvested parts.
- `PRIVATE/PseudoCoup_v5/DevComms/transpiler_survey_2026-07-27.md`
  §2, §3, §5 — the recorded parse/ingest/grammar numbers.
- `PRIVATE/PseudoCoup_v6/Planning/node_0_0_tools/node_0_0_0_ledgerer/SUPPORT_tree_sitter.md`
  — the archived `tree_sitter_base` design (pin + census + coverage).
