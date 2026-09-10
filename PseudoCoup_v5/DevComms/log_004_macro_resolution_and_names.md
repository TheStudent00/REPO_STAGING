# log 004 — can the ledgerer find a macro's definition, and know what it produces?

2026-08-02. Two questions the owner asked, both measured rather than
reasoned. Companion to
`PRIVATE/PseudoCoup_v5/DevComms/log_003_metaprogramming_model.md`,
which holds the model; this log holds the resolution numbers.

Measured over `rustc_codegen_ssa` and `rustc_codegen_llvm` in
`Sources/rust`, grammar pinned to
`tree-sitter==0.26.0` / `tree-sitter-rust==0.24.2`, run in the podman
sandbox agent lane. Scripts kept under
`SandboxDesign/agent/drop/`.

---

## 1. Can tree-sitter point an invocation at its definition?

**Yes for the pointing, no for the resolving. The gap is the corpus,
not the parser.**

Two query patterns are all it takes — no code, just data handed to the
query engine:

```
(macro_invocation macro: (identifier) @name)
(macro_definition name: (identifier) @name)
```

| measure | value |
| --- | --- |
| distinct macros invoked | 49 |
| definitions present in these two crates | 17 |
| invoked names with a local definition | 17 |
| **invocations covered** | **125 of 1,576 — 7.9%** |

The 17, each located exactly by the parse:

| macro | where |
| --- | --- |
| `math_builder_methods` | `rustc_codegen_llvm/src/builder.rs:267` |
| `set_math_builder_methods` | `rustc_codegen_llvm/src/builder.rs:277` |
| `declare_constant` | `rustc_codegen_llvm/src/debuginfo/dwarf_const.rs:7` |
| `declare_fixed_metadata_kinds` | `rustc_codegen_llvm/src/llvm/metadata_kind.rs:9` |
| `generate_arg_methods` | `rustc_codegen_ssa/src/back/linker.rs:238` |
| `if_regular` | `rustc_codegen_ssa/src/back/write.rs:119` |
| `return_if_di_node_created_in_meantime` | `rustc_codegen_llvm/src/debuginfo/metadata.rs:80` |
| `require`, `require_simd`, `require_simd_or_scalable`, `require_int_or_uint_ty`, `return_error` | `rustc_codegen_llvm/src/intrinsic.rs:1962–2406` |
| `arith_red`, `minmax_red`, `bitwise_red`, `arith_binary`, `arith_unary` | `rustc_codegen_llvm/src/intrinsic.rs:2863–3263` |

**The 92% that does not resolve is all elsewhere-defined**, and the top
of it is std:

```
217  bug!      197  format!    142  assert!
131  debug!    105  matches!   104  assert_eq!
 88  writeln!   86  vec!        69  unreachable!
```

**So the lever is the corpus, not the tooling.** Adding `library/core`
to the checkout turns most of that list from unresolvable into
readable, because those are all `macro_rules!` — kind one, definitions
that are data.

**One limit to state before it bites.** The match is by NAME, not by
resolution. tree-sitter does not know which `foo!` is meant when two
crates define one, and Rust's own rules for that are textual order plus
imports. With 17 local definitions this is not a live problem. At std
scale it becomes one, and the honest posture is the refusal rule —
where two definitions could match, write `unresolvable` rather than
choose.

---

## 2. Is the produced name knowable without running the macro?

**For `macro_rules!`: always. This is structural, not a happy
accident.**

A `macro_rules!` template can do exactly two things with an identifier:
write a literal one, or drop in one that was captured from the call.
**It cannot compute a new identifier.** So the produced name is either
in the template or in the invocation, and both are in the parse.

`math_builder_methods! { add(a,b) => LLVMBuildAdd }` — the template
says `fn $name`, the invocation says `add`. The produced name is `add`,
read statically.

Of the 17 local definitions:

| what it produces | count | which |
| --- | --- | --- |
| items, name substituted from the call | 5 | `math_builder_methods`, `set_math_builder_methods`, `declare_constant`, `declare_fixed_metadata_kinds`, `generate_arg_methods` |
| items, name literal | 0 | — |
| no items at all | 12 | the `require*` / `return_error` / `arith_*` / `if_regular` family |

The 12 produce statements. There is no name to recover because none is
created, so leaving them opaque loses nothing.

**For proc macros: not in general.** A proc macro is an arbitrary
program and may build identifiers by string work — `format_ident!` and
the `paste` crate do exactly this. Then the name exists only after the
macro runs.

*(Historical note: `concat_idents!` gave `macro_rules!` a way to build
identifiers, but it was unstable for its whole life and was removed
between 1.85 and 1.97 — see log_003 §6. So the "cannot compute an
identifier" property holds for stable Rust.)*

---

## 3. How much kind three is actually in the first target

Derive attributes in the two crates, split by which kind they are:

| | uses |
| --- | --- |
| total derive uses | 474 |
| built-in — kind two | 325 |
| **proc macro — kind three** | **149** |

The kind-three names, all of them rustc's own internal proc macros
rather than third-party:

| uses | derive |
| --- | --- |
| 111 | `Diagnostic` |
| 13 | `Encodable` |
| 13 | `Decodable` |
| 5 | `TryFromU32` |
| 5 | `Subdiagnostic` |
| 2 | `StableHash` |

**What this sizes.** Kind three is present but narrow: six names, one
of which is two thirds of the uses. And `Diagnostic` generates error
reporting code — not routing logic, so it is very likely droppable for
this project's purpose. That is a judgement, not a measurement.

`TryFromU32` is the interesting one: its definition IS in the corpus,
at `rustc_codegen_llvm/src/macros.rs` — one of the six files the
grammar cannot parse.

---

## 4. the owner's question: could the third kind be transpiled and run?

**Yes in principle, and it is a striking fit — the project's own
capability would solve its own hard case.**

A proc macro is a Rust function from tokens to tokens. PseudoCoup
transpiles Rust. Transpile the proc macro and you have a function in
the hub language that performs the expansion; run it, read the names
out of what it returns.

Nothing about that is circular: the proc macro is ordinary Rust, using
no compiler internals.

**What it actually costs, in order of weight:**

- **The `proc_macro` API must be polyfilled.** `TokenStream`, `Group`,
  `Punct`, `Ident`, `Literal`, `Span`. This is the cheap part and the
  measurement supports it: that public surface changed by ZERO lines
  across 1.95 to 1.97 (log_003 §6), so a polyfill written once stays
  written.
- **`syn` and `quote` are the real cost.** Almost every proc macro
  parses its input with `syn` — a full Rust parser as a library — and
  builds output with `quote`. Transpiling those is a large job.
  - The interesting alternative: `syn`'s job is parsing Rust, and we
    already have a parser. A `syn`-shaped polyfill backed by
    tree-sitter would avoid transpiling it. Whether `syn`'s API surface
    is small enough for that is unmeasured.
- **Behaviour is unconstrained.** A proc macro may read files or the
  environment. Anything transpiled inherits that.

**Sequencing consequence.** This is downstream work, not a precondition
— kind three is 149 derive uses out of 1,576 macro invocations here,
and its most common member is diagnostics. The ledger's honest posture
in the meantime is to record the invocation, mark the produced names
`unresolvable`, and let the transpiler decide whether to follow.

---

## 5. What is not measured

- ~~Whether `syn`'s API surface is small enough to polyfill against
  tree-sitter.~~ **MEASURED AND PROTOTYPED the same day — see §6.**
- Whether `Diagnostic`-generated code is genuinely irrelevant to
  routing, or merely looks it.
- Name-collision rate once `library/core` joins the corpus — the point
  at which name matching stops being sufficient.

---

## 6. The syn-shim spike — measured, then built

Research folder: `PRIVATE/PseudoCoup_v5/Research/syn_shim/`
(shim, derive logic, runner, README with full detail).

**The surface, measured on `compiler/rustc_macros` at 1.97.0** — the
crate holding `Diagnostic`, `Encodable`, `Decodable` and the rest (22
files, 4,613 lines): **33 distinct `syn::` paths**, ~50 types in all
via imports, plus `quote!` 199 times. quote is templating, not parsing
— the easy half. Complications recorded honestly: `parse_quote!` (7
uses, parses GENERATED text back into syn types) and the
`synstructure` helper crate, both of which widen a shim's surface.

**The prototype, run against the real corpus:** a syn-shaped
`parse_derive_input()` backed by tree-sitter, and the `TryFromU32`
derive's logic as a Python function over it. Fed the real
`CovmapVersion` enum from
`rustc_codegen_llvm/src/coverageinfo/mapgen.rs:27`, it produced the
expansion matching the `macro_rules!` template — and the output
re-parses as valid Rust, zero errors.

Two facts that make the demo pointed rather than convenient:
`TryFromU32`'s own definition sits in `macros.rs`, one of the six
unparseable files, and four of its five real users are enums in
`llvm/ffi.rs` — also unparseable. The expansion was reproducible
anyway, because only the INPUT enum needed parsing.

**What it establishes / what it does not:** the architecture works —
proc-macro logic in the hub language over a parser we already have,
producing verifiable expansions. NOT established: that transpiled
(rather than hand-reimplemented) proc-macro bodies run against the
shim. That gap is the transpiler's job.
