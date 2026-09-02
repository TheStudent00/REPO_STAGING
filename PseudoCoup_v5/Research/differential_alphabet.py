#!/usr/bin/env python3
"""Differential token-alphabet check — two independent authorities on
Rust's token set, compared.

    python3 <WORKSPACE_DIR>/PseudoCoup_v5/Research/differential_alphabet.py

Why it exists (the owner, 2026-08-12): the compiler "cares about compiling,
not creating a user interface for interpreting/processing tokens" —
so it does not replace the grammar as the author of our tables, but
it can INFORM AND VERIFY them. This is that verification, and it
needs no corpus: a token rustc has and the pinned grammar lacks is
the pin falling behind the language, found without waiting for a
source file that happens to use it.

Authority A — the pinned grammar (tree-sitter-rust 0.24.2), read
live from the compiled parser: every visible anonymous token.

Authority B — rustc's own token alphabet, transcribed from the doc
comments of `pub enum TokenKind` in
`compiler/rustc_ast/src/token.rs` (rust-lang/rust, master, fetched
2026-08-12). That is the POST-GLUE list: rustc's lexer
(`rustc_lexer`) emits single characters, and `TokenKind::glue`
joins them into `!=`, `->`, `+=` — the same granularity
tree-sitter uses, which is what makes the comparison meaningful.

TRANSCRIBED, not fetched at run time: the constant below is typed
from the source and is therefore only as current as its fetch date.
Re-fetch when the pin moves.

Not covered here: keywords. rustc holds those as `Ident` plus a
symbol table (`rustc_span::symbol::kw`), not in `TokenKind`, so the
56 word-like anonymous tokens of the grammar need a second
comparison against that list.
"""

from tree_sitter import Language
import tree_sitter_rust as tsr


# rustc_ast::token::TokenKind — punctuation and structural symbols,
# spelling -> rustc's name for it.
RUSTC_PUNCT = {
    "=": "Eq", "<": "Lt", "<=": "Le", "==": "EqEq", "!=": "Ne",
    ">=": "Ge", ">": "Gt", "&&": "AndAnd", "||": "OrOr", "!": "Bang",
    "~": "Tilde", "+": "Plus", "-": "Minus", "*": "Star", "/": "Slash",
    "%": "Percent", "^": "Caret", "&": "And", "|": "Or", "<<": "Shl",
    ">>": "Shr", "+=": "PlusEq", "-=": "MinusEq", "*=": "StarEq",
    "/=": "SlashEq", "%=": "PercentEq", "^=": "CaretEq", "&=": "AndEq",
    "|=": "OrEq", "<<=": "ShlEq", ">>=": "ShrEq", "@": "At", ".": "Dot",
    "..": "DotDot", "...": "DotDotDot", "..=": "DotDotEq", ",": "Comma",
    ";": "Semi", ":": "Colon", "::": "PathSep", "->": "RArrow",
    "<-": "LArrow", "=>": "FatArrow", "#": "Pound", "$": "Dollar",
    "?": "Question", "'": "SingleQuote", "(": "OpenParen",
    ")": "CloseParen", "{": "OpenBrace", "}": "CloseBrace",
    "[": "OpenBracket", "]": "CloseBracket",
}


def grammar_anonymous_tokens():
    """Every visible anonymous token of the pinned grammar, read from
    the compiled parser rather than any file."""
    lang = Language(tsr.language())
    return {lang.node_kind_for_id(i) for i in range(lang.node_kind_count)
            if not lang.node_kind_is_named(i) and lang.node_kind_is_visible(i)}


def split_punctuation(tokens):
    """(punctuation, word-like). Word-like tokens are keywords and
    fragment specifiers, which rustc keeps elsewhere."""
    punct = {t for t in tokens if not (t[:1].isalpha() or t[:1] == "_")}
    return punct, tokens - punct


def compare():
    anon = grammar_anonymous_tokens()
    punct, words = split_punctuation(anon)
    return {
        "grammar_anonymous": len(anon),
        "grammar_punctuation": sorted(punct),
        "grammar_words": sorted(words),
        "agree": sorted(set(RUSTC_PUNCT) & punct),
        "rustc_only": sorted(set(RUSTC_PUNCT) - punct),
        "grammar_only": sorted(punct - set(RUSTC_PUNCT)),
    }


def main():
    r = compare()
    print(f"grammar anonymous tokens : {r['grammar_anonymous']} "
          f"({len(r['grammar_punctuation'])} punctuation, "
          f"{len(r['grammar_words'])} word-like)")
    print(f"rustc TokenKind punctuation: {len(RUSTC_PUNCT)}")
    print(f"AGREE on {len(r['agree'])} punctuation tokens")
    print("in rustc, not in the pinned grammar: "
          + ", ".join(f"{t!r} ({RUSTC_PUNCT[t]})" for t in r["rustc_only"]))
    print("in the pinned grammar, not in rustc's list: "
          + ", ".join(repr(t) for t in r["grammar_only"]))


if __name__ == "__main__":
    main()
