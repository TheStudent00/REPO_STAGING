# syn_shim — can tree-sitter stand in for `syn`?

2026-08-02. Research spike answering log_004 §5's first open item:
whether `syn`'s API surface, as proc macros actually use it, is small
enough to polyfill over tree-sitter — so that transpiled proc-macro
logic could run without transpiling a full Rust parser.

**Answer: yes at this scale, demonstrated end to end on a real derive
from the corpus.**

## What is here

| file | what it is |
| --- | --- |
| `syn_shim.py` | the shim: `DeriveInput`, `DataStruct`, `DataEnum`, `Field`, `Variant`, `parse_derive_input()` — syn's entry shape, backed by tree-sitter |
| `derive_try_from_u32.py` | the `TryFromU32` derive's logic as a Python function over the shim, plus the run and the verification |
| `run.sh` | runs the demo against the vendored corpus |

Grammar pin: `tree-sitter==0.26.0`, `tree-sitter-rust==0.24.2` — the
same pins as PCv6's manifest of record.

## The demonstration

Input, real, from
`Sources/rust/compiler/rustc_codegen_llvm/src/coverageinfo/mapgen.rs:27`:

```rust
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord, TryFromU32)]
enum CovmapVersion {
    Version7 = 6,
}
```

Output, produced by shim + Python logic, byte-shape matching the
`macro_rules! TryFromU32` template in
`rustc_codegen_llvm/src/macros.rs`:

```rust
impl ::core::convert::TryFrom<u32> for CovmapVersion {
    type Error = u32;
    fn try_from(value: u32) -> ::core::result::Result<CovmapVersion, u32> {
        if value == const { CovmapVersion::Version7 as u32 } { return Ok(CovmapVersion::Version7); }
        Err(value)
    }
}
```

Verified: the output re-parses as valid Rust with zero errors.

Two details that make this demo pointed rather than convenient:

- `TryFromU32`'s definition lives in `macros.rs` — **one of the six
  files the stock grammar cannot parse.** The expansion was still
  reproducible, because the derive's LOGIC was reimplemented over the
  shim; only its input (the enum) needed parsing.
- Four of its five real users are enums in `llvm/ffi.rs` — **also
  unparseable.** The one parseable user (`CovmapVersion`) is what the
  demo runs on. The grammar patch (log_004 companion discussion) would
  unlock the other four.

## The surface measurement behind the "yes"

`compiler/rustc_macros` at 1.97.0 — the crate holding `Diagnostic`,
`Subdiagnostic`, `Encodable`, `Decodable`, `Lift`, the query system
macros: 22 files, 4,613 lines.

- **33 distinct `syn::` paths referenced.** Top of the list:
  `spanned::Spanned`, `Data::{Struct,Enum,Union}`, `parse_quote`,
  `punctuated::Punctuated`, `parse::ParseStream`, `Ident`, `Path`,
  `Error`, `Field`.
- Via `use syn::{...}`: roughly 25 more types (`Attribute`, `Meta`,
  `LitStr`, `Token`, `Type`, `Fields`, ...). Call it **~50 types
  total**, most of them thin data shapes over things tree-sitter
  already produces.
- `quote! { ... }` appears 199 times plus 5 `quote_spanned!` — but
  quote is TEMPLATING, not parsing: a shim for it is string/token
  interpolation, the easy half.
- Complications, honestly: `parse_quote!` (7 uses) parses GENERATED
  text back into syn types — a shim must parse arbitrary Rust
  fragments, which tree-sitter can do but which widens the needed
  surface; and `synstructure` (a helper crate over syn) is a
  dependency of the derive style used by several of the rustc_macros.

## What this does and does not establish

- **Does:** the architecture works — proc-macro logic expressed in the
  hub language, over a syn-shaped API backed by the parser we already
  have, producing verifiable expansions of real corpus code.
- **Does not:** that TRANSPILED (rather than reimplemented) proc-macro
  bodies run against the shim. The demo hand-translated the logic. The
  gap between the two is exactly the transpiler's job, which is the
  point of the project — but it is a gap.
- **Does not:** cover `parse_quote!`/`synstructure`-style usage, which
  is where the shim's surface would grow.
