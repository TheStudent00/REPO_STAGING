"""Construct tree-sitter parsers and parse source; the ONLY place in PCv6 that owns parsing.

Provenance: dispatch pattern from
0_Archive/PseudoCoup_v1/pseudocoup/core/parser.py (the 49-line
13-language factory), rebuilt on the tree_sitter 0.26 API with
pip-pinned grammar packages (see pins/MANIFEST.md). Nothing outside
this tool constructs a Parser.
"""
import importlib

import tree_sitter

# grammar name -> pip package module (pinned in pins/MANIFEST.md)
GRAMMARS = {
    "python": "tree_sitter_python",
    "rust": "tree_sitter_rust",
    "cpp": "tree_sitter_cpp",
}


def get_language(name: str) -> "tree_sitter.Language":
    """Return the tree_sitter.Language for a registered grammar name."""
    if name not in GRAMMARS:
        raise KeyError(
            f"tree_sitter_base: unknown grammar {name!r}; "
            f"registered: {sorted(GRAMMARS)}")
    mod = importlib.import_module(GRAMMARS[name])
    return tree_sitter.Language(mod.language())


def get_parser(name: str) -> "tree_sitter.Parser":
    """Return a Parser bound to the named grammar."""
    return tree_sitter.Parser(get_language(name))


def parse_bytes(src: bytes, name: str):
    """Parse source bytes with the named grammar; returns the Tree."""
    if not isinstance(src, bytes):
        raise TypeError("tree_sitter_base: parse_bytes wants bytes "
                        "(encode explicitly; no silent decode guesses)")
    return get_parser(name).parse(src)


def parse_file(path: str, name: str):
    """Parse a file with the named grammar; returns the Tree."""
    with open(path, "rb") as f:
        return parse_bytes(f.read(), name)
