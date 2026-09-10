---
id: pcv5.tools.ledgerer.support.metaprogramming
status: draft
---

# SUPPORT — metaprogramming

How the ledgerer models code that writes code. Design direction settled
in conversation 2026-08-02; the reasoning and the measurements behind
it are in
`PRIVATE/PseudoCoup_v5/DevComms/log_003_metaprogramming_model.md`.

---

## 1. The position

**Meta-programming is code, and code is represented losslessly. There
is no exception carved out for it.**

A macro definition is tokens. A procedural macro is a program. Both go
into the UR the way any other code does, and the ledger records them
the way it records anything else.

The thing that made this look hard was a confusion between two
operations that are not the same:

| operation | what it means | is it always possible |
| --- | --- | --- |
| **representation** | holding the meta-program's own logic — its definition, its inputs, its position | **yes, always, losslessly** |
| **evaluation** | computing what one particular call produces | only by running the logic |

**Representation is never blocked.** No kind of code resists being put
in a tree.

**Evaluation is a separate job**, with its own cost and its own
failure modes, and the ledger does not require it to be complete.

## 2. Rust is the tip of the spear

The first ingest target is rustc's own source, so Rust's
meta-programming is what the model is built against first.

That ordering is deliberate rather than incidental: **Rust has the most
opaque meta-programming of the targets in view.** Its macros take
unparsed tokens and may invent syntax the language does not otherwise
have. A model that holds Rust holds the easier cases.

For comparison, and to keep the model from becoming Rust-shaped:

| language | meta-programming | how opaque |
| --- | --- | --- |
| Rust | `macro_rules!`, built-ins, proc macros | high — arbitrary token input, arbitrary programs |
| C / C++ | preprocessor | high in a different way — text substitution, not even balanced |
| Python | decorators, metaclasses, `exec` | low — operates on already-parsed objects at run time |
| Lisp | macros | low — code and data share one syntax |

The general shape the ledger needs is therefore **a meta-node with
three parts**, not a Rust feature: the thing that generates, the place
it was invoked, and what it produced. Section 4.

## 3. Rust's three kinds, kept apart

The kinds differ in **where the definition lives**, and that is what
decides how the ledger treats each one.

**Kind one — `macro_rules!`. The definition is source, and it is data.**

A pattern and a template, both plain tokens. Reading them requires no
compiler. Expansion is computable from them alone, which is
demonstrated by the working engine at
`PRIVATE/PseudoCoup_v5/Research/macro_engine.py`.

Covers everything defined in the corpus, including the standard
library's own — `assert_eq!` is `macro_rules!`, in
`library/core/src/macros/mod.rs`.

**Kind two — built-ins. There is no definition to read.**

`format_args!`, `derive`, `asm!` and about fifty-seven others are
functions inside the compiler, registered in one table at
`rustc_builtin_macros/src/lib.rs`. Their behaviour is compiled Rust,
not a pattern.

These need a hand-written model, keyed by compiler version. This is the
only place a version-keyed table is required.

**Kind three — procedural macros. The definition is an arbitrary
program.**

Shipped by third-party crates, compiled to a library the compiler loads
and runs. Their AST can be represented like any other Rust; their
OUTPUT exists only after execution.

## 4. What the ledger holds

Per meta-programming site, four things, and the connectors between them
are ordinary typed connections — the carrying capacity the ledger
already has, not a special case:

- **the invocation** — the node as written, honestly opaque. Its
  contents are a balanced token list and nothing more is claimed about
  them.
- **the definition** — the generator's own nodes, when the definition
  is in the corpus. For `macro_rules!` this is pattern and template.
  For a proc macro it is that crate's code.
- **the produced nodes** — what one call yields, when evaluation has
  been done.
- **the connectors** — invocation to definition, and produced to
  invocation.

**A ledger with the first two and not the third is still correct.** It
is a complete record of the source. Expansion is a DERIVED VIEW,
computed when wanted, not a precondition for ledgering.

That is the property worth protecting: nothing is lost by declining to
expand, and nothing is guessed.

## 5. Evaluation: when it is needed, and when it is not

The deciding question is **whether the expansion creates names that
other code refers to.**

**Ordinary — expands to expressions or statements inside a body.**
Creates no definitions. `assert_eq!`, `format!`, `vec!`, `debug!`.

Skipping evaluation costs nothing: there is no name anywhere for
anything to resolve to.

**Structure-generating — expands to definitions.** Functions,
constants, types. `math_builder_methods!`, `declare_constant!`.

Skipping evaluation leaves the ledger without an entry for a name that
other files call. That is a hole, not a simplification.

**The trap, which frequency counts hide.** Invocation count and
structural weight point in opposite directions:

| macro | invocations | what it creates |
| --- | --- | --- |
| `assert_eq!` | 427 | nothing nameable |
| `math_builder_methods!` | 2 | ~27 methods, `sdiv` among them |

A ranking by count puts the macro that matters at the bottom. **The
selection rule is therefore "does it produce definitions", never "is it
common".**

## 6. How evaluation is done

**`macro_rules!` — our own engine, one invocation at a time.**

Self-contained, no build, and the alignment is exact because we choose
what to expand and where the result attaches.

**Built-ins and proc macros — the real toolchain.**

`cargo expand` or `rustc -Zunpretty=expanded`, which require building
the crate and its dependencies.

**The problem this creates, named rather than discovered later:** the
toolchain expands a whole crate, and its output does not say which
chunk came from which call. The ledgerer works a file at a time, so the
two do not line up. Aligning them is real work and it is confined to
this group.

**What the run must record when it happens:** the compiler version, the
`cfg` flags, and the target. All three change what a call produces, so
an expansion without them is not reproducible.

## 7. Facts about Rust that the model must not assume away

- **A macro's arguments have no fixed grammar.** Each macro defines how
  its own contents are read. There is no shape that fits all of them —
  `vec![0; n]` is an expression while `vec![1, 2, 3]` is an argument
  list, and `asm!` is neither.
- **The one guarantee is balanced delimiters.** That is why the parser
  gives a flat token list and nothing more, and why treating that list
  as honest rather than deficient is correct.
- **Expansion happens before names are resolved.** A macro cannot be
  modelled as a function call, because the names it creates must exist
  before any function could have run.
- **Determinism is a convention, not a guarantee.** A proc macro is an
  arbitrary program and may read files, environment or the clock.
  Nothing enforces that two runs agree.

## 7a. Two properties the design can rely on

Measured 2026-08-02; the numbers are in
`PRIVATE/PseudoCoup_v5/DevComms/log_004_macro_resolution_and_names.md`.

**Finding the definition is free from the parse.** Two query patterns
give every invocation's name and every definition's name and location.
What limits reach is the corpus, not the parser: 7.9% of invocations
resolve to a definition inside the two crates, and the unresolved
remainder is dominated by std's `macro_rules!` macros, which become
readable the moment `library/core` joins the checkout.

**A `macro_rules!` macro cannot compute an identifier.** Its template
either writes a literal name or drops in one captured from the call.
So a produced name is always readable statically — it is in the
template or in the invocation, and both are in the parse.

That property does NOT extend to proc macros, which may build
identifiers by string work. The boundary therefore falls exactly on the
three kinds: one and two are statically readable, three is not.

## 8. Open, and the owner's to settle

- **Where expansion sits relative to the file boundary.** The ledgerer
  ingests one file; toolchain expansion is per crate. Either the
  ledgerer gains a crate-level mode for this, or expansion becomes a
  separate stage feeding it.
- **Which toolchain version is used for a non-compiler target.** A
  project may pin one in `rust-toolchain.toml`; the fallback is stable,
  with a manual override. Reading the project's own pin makes the
  result match what that project's build would produce.
- **Whether `library/core` joins the corpus.** The current checkout is
  compiler folders only, so the standard library's macro definitions —
  `assert_eq!` among them — are absent. Adding it turns kind one's
  coverage from "in-crate" into "in-crate and std".
- **How far the generalization in §2 is designed for now**, versus
  discovered when the second language arrives.
