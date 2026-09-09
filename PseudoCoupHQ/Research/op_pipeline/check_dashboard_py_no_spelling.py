#!/usr/bin/env python3
"""check_dashboard_py_no_spelling.py -- the spelling-ban check over PYTHON
page code, beside check_no_spelling_keys.py (which checks the DATA) and
check_dashboard_js_no_spelling.py (which checks JavaScript page code).

Why a third one.  `dashboard_ouro.py` renders the dashboard in python,
inside Ourobrowser, so the grouping, selection and comparison that used
to live in JavaScript now live in python source.  Neither existing guard
reads it: one walks json documents, the other walks string literals in
javascript.

THE BAN (AgentMemory, restated by the owner 2026-08-25): no operator token may
appear in ANY key, grouping, pairing, row structure, candidate selection
or comparison scope.  The token appears exactly once per unit, as a
display label on the member.

WHAT THIS PROGRAM DOES.  It reads the SAME operator inventory the data
guard reads -- `check_no_spelling_keys.inventory()`, the `operator` field
of every probe in `probe_manifest_*.json` -- and then walks the python
file's syntax tree looking for a string constant whose text is one of
those tokens sitting in a position that decides identity:

  1. a KEY in a dict display            {"+": ...}
  2. a SUBSCRIPT index                   table["+"]
  3. a COMPARISON operand                if row.operator == "+"
  4. a MEMBERSHIP element                if tok in ("+", "-")
  5. the first argument of a lookup      d.get("+"), d.setdefault("+")

Each of those is a place where the token would decide which units are
grouped, paired or compared.  Anything else -- a token in a docstring or
a comment about the ban itself -- is reported as a mention and does not
fail, because a mention cannot key anything.

Reading the syntax tree rather than grepping matters: a grep for `"+"`
cannot tell a dict key from a piece of prose, and this line has already
been burned twice by a token that got into a key by accident.

usage: check_dashboard_py_no_spelling.py FILE [FILE ...]
"""

import ast
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

LOOKUP_METHODS = {"get", "setdefault", "pop"}


def inventory():
    """the operator inventory, read from the UNMODIFIED data guard."""
    spec = importlib.util.spec_from_file_location(
        "guard", os.path.join(HERE, "check_no_spelling_keys.py"))
    guard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guard)
    return guard.inventory()


def text_of(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    return None


def key_positions(tree):
    """every (line, text, what the position is) where a string constant
    decides identity."""
    found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            for key in node.keys:
                text = text_of(key)
                if text is not None:
                    found.append((key.lineno, text, "a key in a dict display"))
        elif isinstance(node, ast.Subscript):
            text = text_of(node.slice)
            if text is not None:
                found.append((node.lineno, text, "a subscript index"))
        elif isinstance(node, ast.Compare):
            for side in [node.left] + list(node.comparators):
                text = text_of(side)
                if text is not None:
                    found.append((node.lineno, text, "a comparison operand"))
            for side in node.comparators:
                if isinstance(side, (ast.Tuple, ast.List, ast.Set)):
                    for element in side.elts:
                        text = text_of(element)
                        if text is not None:
                            found.append((node.lineno, text,
                                          "a membership element"))
        elif isinstance(node, ast.Call):
            func = node.func
            if isinstance(func, ast.Attribute) and func.attr in LOOKUP_METHODS:
                if node.args:
                    text = text_of(node.args[0])
                    if text is not None:
                        found.append((node.lineno, text,
                                      "the first argument of .%s()" % func.attr))
    return found


def mentions(tree, toks):
    """a token appearing anywhere else -- prose, a docstring, a message."""
    out = []
    for node in ast.walk(tree):
        text = text_of(node)
        if text is None:
            continue
        if text in toks:
            out.append((getattr(node, "lineno", 0), text))
    return out


def check(path, toks):
    with open(path) as fh:
        source = fh.read()
    tree = ast.parse(source, filename=path)

    bad = 0
    for line, text, what in key_positions(tree):
        if text not in toks:
            continue
        print("FAIL %s:%d  the string %r is an operator token, and it is %s"
              % (path, line, text, what))
        bad += 1

    said = mentions(tree, toks)
    for line, text in said:
        print("     %s:%d  %r appears as a value or a piece of prose, in no "
              "position that keys anything" % (os.path.basename(path), line,
                                               text))
    if bad:
        return 1
    print("PASS %s -- no operator token sits in a key, a subscript, a "
          "comparison, a membership test or a lookup (%d mention(s) above)"
          % (os.path.basename(path), len(said)))
    return 0


def main(argv):
    if len(argv) < 2:
        print(__doc__)
        return 2
    toks = inventory()
    print("operator inventory: %d tokens read from probe_manifest_*.json"
          % len(toks))
    worst = 0
    for path in argv[1:]:
        rc = check(path, toks)
        if rc > worst:
            worst = rc
    return worst


if __name__ == "__main__":
    sys.exit(main(sys.argv))
