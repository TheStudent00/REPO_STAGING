# log 003 — how the metaprogramming model was arrived at

2026-08-02. The working record behind
`~/Programming/PseudoCoup_v5/Planning/node_0_0_tools/node_0_0_0_ledgerer/SUPPORT_metaprogramming.md`,
which holds the design direction itself. This log holds the
measurements, the demonstrations, and the wrong turns — kept because
the wrong turns are where the reasoning is.

Everything measured here was run against
`~/Programming/Sources/rust/compiler`, in the podman sandbox's agent
lane, with the grammar pinned to PCv6's manifest of record
(`tree-sitter==0.26.0`, `tree-sitter-rust==0.24.2`).

---

## 1. The measurements

### 1a. Scope

The checkout holds three crates, 187 `.rs` files, 84,452 lines. Two are
the ones in view — `rustc_codegen_ssa` and `rustc_codegen_llvm`, 111
files, 1,598 macro invocations. The third is under the standing
prohibition and is still on disk; the totals below include it unless
stated. rustc entire is roughly 250 crates, so none of this describes
"the compiler" — it describes the codegen slice, which is the slice
this project targets.

### 1b. Macro use

| measure | value |
| --- | --- |
| macro invocations | 2,854 |
| `macro_rules!` definitions in-crate | 29 |
| derive attributes | 235 |
| invocations per file | 15.8 |
| invocations per thousand lines | 35.6 |

Top of the distribution, which is what drove the ordinary /
structure-generating split:

| count | macro | count | macro |
| --- | --- | --- | --- |
| 427 | `assert_eq!` | 131 | `debug!` |
| 327 | `format!` | 123 | `matches!` |
| 263 | `bug!` | 118 | `writeln!` |
| 219 | `assert!` | 61 | `msg!` |
| 197 | `intrinsic_args!` | 56 | `panic!` |
| 193 | `vec!` | 47 | `span_bug!` |
| 183 | `unreachable!` | 45 | `write!` |

Grouped by what a slicer would do with them, over the top 25 (2,676
invocations, 94% of all use):

| group | count | share |
| --- | --- | --- |
| assertions and logging | 922 | 34% |
| divergence markers | 549 | 21% |
| formatting and collections | 715 | 27% |
| pattern and cfg tests | 145 | 5% |
| rustc-specific semantics | 345 | 13% |

### 1c. Parse rate

**181 of 187 files parse clean (96.8%); 94.9% by line.** The six that
fail:

- `rustc_codegen_llvm/src/macros.rs`
- `rustc_codegen_llvm/src/llvm/ffi.rs`
- `rustc_codegen_llvm/src/llvm/enzyme_ffi.rs`
- `rustc_codegen_ssa/src/traits/mod.rs`
- `rustc_codegen_ssa/src/traits/type_.rs`
- one example file in the prohibited crate

The named cause, bisected on one file: the unstable `macro` keyword
(decl_macro), which the stock grammar does not accept. Whether each of
the six fails for that reason is **unverified** — only the first was
bisected.

Two of the six are load-bearing for the LLVM path: `llvm/ffi.rs` is the
FFI wall named as a stage in
`~/Programming/PseudoCoup_v5/DevComms/plan_llvm_rust_2026-07-27.md`,
and `macros.rs` defines that crate's own macros. **A 96.8% pass rate
does not mean 96.8% of the value.**

---

## 2. The demonstrations

Two runnable files, both standard library only.

**`~/Programming/PseudoCoup_v5/Research/macro_demo.py`** — what a macro
IS: tokens in, tokens out, run before parsing. Hand-written per macro,
which is its limitation and the reason for the second file.

**`~/Programming/PseudoCoup_v5/Research/macro_engine.py`** — the
operator itself. One engine that names no macro; each macro is a
pattern and a template handed to it as data. Verified on three
definitions including the shape of the real `math_builder_methods!`.

Two bugs found while writing the engine, both kept as comments in the
file because both are instructive:

- **A hole's capture ends at whatever the pattern expects next**, and
  that may be a GROUP rather than a token. Checking only for a token
  made `$name:ident(...)` swallow the whole invocation.
- **Templates have no fragment specifiers.** Parsing a template with
  the pattern rules read `: u32` in `const $n : u32` as a specifier and
  deleted it.

---

## 3. The wrong turns, and what corrected them

**Wrong turn one: "rustc is macro-heavy, so macros are the sharpest
problem."**

Corrected by §1b. Macro-heavy is true; heavy with *noise* is the useful
form. 87% are assertions, logging, formatting and collections.

**Wrong turn two: "re-parsing token trees recovers the arguments."**

Generalized from one lucky case. Measured against real macro shapes,
the naive re-parse fails on most of them, because a comma-separated
argument list is not an expression:

| macro content | as expression | as argument list | as statements |
| --- | --- | --- | --- |
| `assert_eq!(a, b)` | no | yes | no |
| `vec![0; n]` | yes | no | yes |
| `matches!(x, Some(v) if v > 3)` | no | no | no |
| `asm!("mov {0}, {1}", out(reg) a, ...)` | no | no | no |

**No column fits everything**, and two forms of the same macro need
opposite assumptions. Re-parsing works only once the macro's shape is
known, which is per-macro knowledge.

**Wrong turn three: treating representation and evaluation as one
question.**

This was the substantive error, and the owner named it. Several answers
raised nondeterminism and `cfg` sensitivity against a question about
whether meta-programming can be REPRESENTED. Those facts belong to
evaluation only. They say nothing about whether the logic can be held
in a tree, and raising them there was obstructive.

The correction is §1 of the SUPPORT file: representation is always
possible and lossless; evaluation is a separate operation.

**Wrong turn four: recommending against a design because of the text
round-trip.**

An AST export would remove the text round-trip. It would not remove the
need to RUN a proc macro, because macro output only exists after the
macro runs. Those are different barriers and only the second is real.

---

## 4. Facts established about Rust's macro system

Each of these was demonstrated rather than asserted, and each shaped
the model.

- **A macro is a function from tokens to tokens**, run before parsing.
  Its author supplies a pattern and a template; the engine does the
  matching and filling.
- **The macro's output is parsed as ordinary code afterwards.** Source
  with a macro call and source with the expansion already written
  produce identical machine code, because expansion happens first
  either way.
- **A macro cannot be a function call**, because the names it creates
  must exist before name resolution, and a function has not run by
  then. In a language that resolves names at run time — Python — the
  same job IS a function.
- **Expansion lands where the invocation sat.** Inside an `impl` block
  it produces methods; inside a function body it produces items local
  to that body.
- **`macro_rules!` is data.** `assert_eq!` in `library/core`,
  `declare_constant!` and `math_builder_methods!` in the codegen
  crates, all read as pattern plus template.
- **Built-ins are not.** 60 are registered in one table at
  `rustc_builtin_macros/src/lib.rs`: 31 bang macros, 17 attribute
  macros, 12 derives.
- **rustc tracks where expanded code came from.** Every span carries a
  `SyntaxContext`; `rustc_codegen_ssa/src/mir/debuginfo.rs:854` warns
  that spans "could have distinct SyntaxContexts". That is the same
  edge the ledger needs, already present in the compiler.

---

## 5. What is not yet measured

- ~~Churn of macro definitions.~~ **MEASURED 2026-08-02 — see §6.**

- **Which in-crate `macro_rules!` definitions generate definitions
  rather than statements.** 29 exist; roughly six or seven appear to
  generate items, from reading their templates. That is a reading, not
  a count.
- **Whether each of the six unparseable files fails for the decl_macro
  reason.** One was bisected; five were not.

---

## 6. Churn across releases — measured 2026-08-02

**Rust has no major versions.** It has been 1.x since 2015. The three
most recent stable releases are 1.95.0, 1.96.0, 1.97.0, and those are
what was compared. The real "major" boundary in Rust is the EDITION
(2015 / 2018 / 2021 / 2024), which is not measured here.

Method: three paths only, fetched at three tags into sandbox scratch —
5.6 MB total, no effect on `~/Programming/Sources`. Script kept at
`~/Programming/SandboxDesign/agent/drop/macro_churn.sh`.

| kind | path | 1.95 -> 1.96 | 1.96 -> 1.97 |
| --- | --- | --- | --- |
| 1 — `macro_rules!` in core | `library/core/src/macros` | 24 lines, 1 file | 1 line, 1 file |
| 2 — built-ins | `compiler/rustc_builtin_macros` | 215+/98-, 19 files | 215+/106-, 15 files |
| 3 — proc macro API | `library/proc_macro/src` | **no change** | 11 lines, bridge internals only |

### What the numbers hide, in both directions

**Kind 1 looks tiny and contains the one genuinely output-changing
edit.** Of the 24 lines, most are documentation. One is not —
`assert_matches!`'s template gained a pair of braces:

```
-    ($left:expr, ... $(,)?) => {
+    ($left:expr, ... $(,)?) => {{
         match $left { ... }
-    },
+    }},
```

The expansion changes from a bare `match` to a block containing a
`match`. **That is a change in the shape of the produced nodes**, which
is exactly the class of change a ledger would record differently before
and after. It rode along with the macro being stabilized in 1.96.

Across both transitions, **no `macro_rules!` definition was added or
removed** from core.

**Kind 2 looks large and its surface is stable.** The registration
table at `rustc_builtin_macros/src/lib.rs` did not change in either
transition — no built-in added, none removed — and no expander function
signature changed. What churned is implementation:

| file | lines changed, 1.95 -> 1.97 |
| --- | --- |
| `eii.rs` | 178 |
| `errors.rs` | 114 |
| `autodiff.rs` | 89 |
| `format.rs` | 75 |
| `env.rs` | 53 |

`format.rs` is the one to watch: `format_args!` sits at the bottom of
`format!`, `write!`, `println!` and `panic!`, so a change there reaches
a large share of the invocations counted in §1b.

**Kind 3 is frozen where it matters.** `library/proc_macro/src/lib.rs`
— the public surface a proc macro is written against — changed by ZERO
lines across two releases. The only movement was in `bridge/`, the
private transport between compiler and macro.

### The finding, stated against expectation

The risk ranking is the reverse of the effort ranking.

- The kind needing **no** version-keyed model (kind 1, read from
  source) churns least, and what churn there is arrives with the
  source, so it is self-correcting.
- The kind needing a version-keyed model (kind 2) has a **stable
  surface and an unstable interior** — the table of what exists is
  safe to hardcode, the behaviour behind it is not.
- The kind that sounds most volatile (kind 3, arbitrary programs) has
  the most stable interface. Its variability comes from the CRATE
  version shipping the macro, not from rustc.

### What follows

Pin the toolchain, record it in the ledger, re-derive built-in models
when it moves. Two releases produced one output-shape change in kind 1
and none in the kind 2 surface, so re-derivation is rare — but "rare"
is not "never", which is the argument for recording the version rather
than assuming it.

**Not measured:** edition boundaries, where larger shifts would live.
