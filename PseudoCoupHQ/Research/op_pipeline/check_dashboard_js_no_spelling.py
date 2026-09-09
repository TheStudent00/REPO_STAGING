#!/usr/bin/env python3
"""check_dashboard_js_no_spelling.py -- the spelling-ban check over the
PAGE'S CODE, beside check_no_spelling_keys.py which checks the DATA.

The guard walks json.  The dashboard's grouping, selection and comparison
live in javascript, so this reads the same operator inventory the guard
reads (`probe_manifest_*.json`, the `operator` field of every probe) and
reports every string literal in the page's own code whose text IS one of
those tokens.  A key can only be written as a literal, so no literal
means no key.

Coincidences are named, not waved away: `&` and `<` are html escapes,
`/` is the artifacts' own unit-id separator (`c/op_100`), and so on.
Each one is printed with what it is, and the exit code counts only
literals that are NOT in that named list.

usage: check_dashboard_js_no_spelling.py FILE [FILE ...]
"""

import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# a literal whose text happens to be a token, with what it actually is.
NAMED_COINCIDENCES = {
    "&": "html escaping in esc()",
    "<": "html escaping in esc()",
    ">": "html escaping in esc()",
    "/": "the artifacts' own unit-id separator, as in c/op_100",
}

LITERAL = re.compile(r'"((?:[^"\\]|\\.)*)"' + r"|'((?:[^'\\]|\\.)*)'")


def inventory():
    spec = importlib.util.spec_from_file_location(
        "guard", os.path.join(HERE, "check_no_spelling_keys.py"))
    guard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guard)
    return guard.inventory()


def check(path, toks):
    bad = 0
    named = 0
    with open(path) as fh:
        lines = fh.read().splitlines()
    for n, line in enumerate(lines, 1):
        for m in LITERAL.finditer(line):
            text = m.group(1)
            if text is None:
                text = m.group(2)
            if text not in toks:
                continue
            if text in NAMED_COINCIDENCES:
                print("     %s:%d  %r -- %s"
                      % (os.path.basename(path), n, text,
                         NAMED_COINCIDENCES[text]))
                named += 1
                continue
            print("FAIL %s:%d  string literal %r is an operator token in a "
                  "position that could be a key" % (path, n, text))
            bad += 1
    if bad:
        return 1
    print("PASS %s -- no operator token is written as a literal, so none "
          "can be a key (%d named coincidences above)"
          % (os.path.basename(path), named))
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
