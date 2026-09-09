# log 018 — the differential token-alphabet check: rustc and the pinned grammar compared

2026-08-12. Run at the owner's instruction ("run it. if it can help improve
our design, we will update accordingly"), closing the thread he opened
three times across this conversation: the compiler is a knowledge
resource, and the burden was on me to examine it rather than defend
the grammar's sufficiency.

The script is
`~/Programming/PseudoCoup_v5/Research/differential_alphabet.py`, run
with no arguments; it reads the pinned grammar live and holds rustc's
list as a transcribed constant.

---

## 1. The finding, in one line

**Two independent descriptions of Rust's token set agree on 51 of the
~55 punctuation tokens, and every one of the 6 disagreements is
explained by a difference in purpose, not by an error in either.**

---

## 2. What was compared

- **Authority A — the pinned grammar.** `tree-sitter-rust 0.24.2`,
  read from the compiled parser: 111 visible anonymous tokens, of
  which 55 are punctuation and 56 are word-like (keywords, fragment
  specifiers).
  - correction to an earlier figure: this conversation said "115
    anonymous tokens" on 2026-08-11. That count was a LIST with
    duplicate ids; the distinct set is 111. The design conclusions
    drawn from it are unaffected.
- **Authority B — rustc's own alphabet.** `pub enum TokenKind` in
  `compiler/rustc_ast/src/token.rs` (rust-lang/rust, master, fetched
  2026-08-12): 53 punctuation and structural symbols, transcribed
  into the script as a constant.
  - the choice of THIS file rather than `rustc_lexer` is the whole
    reason the comparison works. `rustc_lexer::TokenKind` is
    pre-glue: it has `Bang` and `Eq` but no `Ne`. `rustc_ast`'s list
    is post-glue and carries `!=`, `->`, `+=`, `..=` — the same
    granularity tree-sitter puts in the tree.
  - the joining is one function in that file, `TokenKind::glue`
    (`(Bang, Eq) => Ne`, `(Minus, Gt) => RArrow`, ...), and its
    inverse `break_two_token_op`.

## 3. The disagreements, by cause

Two causes, three tokens each. Neither is a defect.

- **rustc keeps two tokens the language no longer uses**, for
  diagnostics: `~` (Tilde) and `<-` (LArrow). No valid Rust program
  contains either, so a grammar that only describes valid programs
  has no reason to carry them.
- **the grammar exposes four sub-token delimiters rustc fuses**:
  `"`, `//`, `/*`, `*/`. rustc's lexer emits a whole string literal
  or comment as ONE token; tree-sitter splits the delimiters out so
  the interior is addressable as its own node.
  - this is the owner's own framing confirmed in data (2026-08-12): "the
    compiler cares about compiling, not creating a user interface
    for interpreting/processing tokens in an abstract
    representation."
  - it also underwrites a design decision already made: `string_content`
    and `doc_comment` are content-bearing leaves carrying `text`
    precisely because tree-sitter splits them out. Under rustc's
    tokenization they would not be separately addressable.

## 4. What this changes in the design

- **The grammar stays the AUTHOR of the pack's tables.** Nothing
  here displaces the 2026-08-11 ruling: rustc's list is an alphabet
  with no arrangements — it never says which tokens belong to which
  construct, which is what stencils and variant-roles are made of.
- **rustc becomes a corpus-free STALENESS DETECTOR, which is new.**
  A token present in rustc's list and absent from the pinned
  grammar's is the pin falling behind the language. Today that set
  is `{~, <-}` and both are explained, so the pin is CURRENT by this
  test — a stronger statement than the corpus could make, because
  it does not depend on any file happening to use the construct.
  - relation to the `ERROR` signal: same fact, found earlier. The
    corpus finds a gap only when a file exercises it (the 5 nightly
    `decl_macro` files); this check finds it at the alphabet level
    with no files at all.
- **Proposed, NOT decided (naming and structure are the owner's):** this
  belongs beside `LanguagePack.check_pin` as a second check — the
  pin check asks "is the grammar the version we recorded?", this
  asks "is that version still level with the language?". A name and
  a decision on whether it is one method or two is the owner's.

## 5. What is still unchecked

- **Keywords.** 56 word-like anonymous tokens (`fn`, `struct`,
  `impl`, `where`, `dyn`, the fragment specifiers `expr`/`ident`/`tt`
  ...) were NOT compared. rustc does not keep keywords in
  `TokenKind`; they are `Ident` plus a symbol table
  (`rustc_span::symbol::kw`). A second comparison against that table
  would extend this check to the whole alphabet.
- **Other languages.** Whether an equivalent authority exists per
  language is unknown and is a real question for the 12-language
  objective: this check may be a Rust luxury rather than a pack
  requirement. It is cheap where it exists and absent where it does
  not; nothing in the pack design should DEPEND on it.
- **Transcription currency.** rustc's list is typed into the script,
  not fetched at run time, so it is only as current as its fetch
  date (2026-08-12). Re-fetch when the pin moves.
