#!/usr/bin/env python3
"""verbatim_diag.py -- keep stored compiler testimony verbatim.

THE DEFECT THIS REPAIRS
-----------------------
`lane_gen.py` builds the lane script that runs inside Airlock.  The
driver it embeds writes one line per probe into a PIPE-DELIMITED text
file, for example:

    op_178|REFUSED|error[E0277]: no implementation for `i32 | f64`

and `fold.py` reads that file back with `ln.split("|")`.  A `|` inside
the compiler's own words would therefore split into extra fields and
corrupt the record.  The author's answer (lane_gen.py lines 192, 365,
368, 371, 373) was to SUBSTITUTE the character:

    text.replace("|", "/")        # and, in clean(), ";" -> ","

That removes the collision, and it also removes the truth.  Rust probe
178 asked about `a | b`; rustc answered "no implementation for
`i32 | f64`"; the store holds "no implementation for `i32 / f64`".
The stored testimony now says the compiler said something it did not
say.  The evidence doctrine (AgentMemory) is that stored testimony is
verbatim, so the substitution is a defect and not a formatting choice.

THE REASON THE SUBSTITUTION EXISTED, AND THE PROPER SOLUTION
------------------------------------------------------------
The reason is a delimiter collision, and it is real -- dropping the
replacement without replacing the mechanism would corrupt `fold.py`'s
parse.  Two delimiters are load-bearing in the lane format:

  `|`  the field separator            (fold.py read_lanes, ln.split("|"))
  `;`  the sub-item separator, used for the mnemonic list and for the
       DWARF row list                (fold.py: parts[4].split(";"),
                                      fold.py dwarf_rows: text.split(";"))

The proper solution for a delimiter collision is ESCAPING, not
substitution: escaping is reversible, substitution is not.  This module
carries the escape codec and a verbatim replacement for `firstline()`.

THE CODEC (v1)
--------------
    \\   ->  \\\\      (the escape character itself, escaped first)
    |    ->  \\p
    ;    ->  \\s
    \\n  ->  \\n  (a literal newline never reaches a record line)
    \\r  ->  \\r

`decode` is the exact inverse.  A lane file written by the verbatim
path announces itself with a first line

    #verbatim-escape v1

so a reader can tell an escaped file from a legacy file and refuse to
decode a legacy one (decoding a legacy line would change a literal
backslash that the compiler really did emit -- the same class of
mistake as the defect itself).

NOT A MODIFICATION OF ANYTHING EXISTING
---------------------------------------
`lane_gen.py` and `fold.py` are untouched.  This module is imported by
`lane_gen_verbatim.py` (writes lanes whose driver escapes) and by
`fold_verbatim.py` (folds a lane file whose driver escaped).
"""

import re

MARKER = "#verbatim-escape v1"

_ENC = [("\\", "\\\\"), ("|", "\\p"), (";", "\\s"),
        ("\n", "\\n"), ("\r", "\\r")]


def encode(text):
    """make `text` safe to place in one pipe-delimited field, reversibly."""
    for raw, rep in _ENC:
        text = text.replace(raw, rep)
    return text


def decode(text):
    """the exact inverse of `encode`."""
    out = []
    i = 0
    n = len(text)
    back = {"p": "|", "s": ";", "n": "\n", "r": "\r", "\\": "\\"}
    while i < n:
        c = text[i]
        if c == "\\" and i + 1 < n and text[i + 1] in back:
            out.append(back[text[i + 1]])
            i += 2
            continue
        out.append(c)
        i += 1
    return "".join(out)


DIAG = re.compile(r"^[^\s:]+:\d+(:\d+)?:")


def firstline_verbatim(txt, limit=200):
    """the compiler's own words, unaltered, chosen by lane_gen's own rule.

    Same three passes as `lane_gen.firstline` -- a line saying `error`,
    then a line in the `file:line:col:` diagnostic shape, then the first
    non-banner line -- with the substitution removed.  The `[:limit]`
    truncation is kept: truncation loses tail, it does not alter words.
    """
    lines = [ln.strip() for ln in txt.splitlines() if ln.strip()]
    for ln in lines:
        if re.search(r"\berror\b", ln, re.I):
            return ln[:limit]
    for ln in lines:
        if DIAG.match(ln):
            return ln[:limit]
    for ln in lines:
        if not ln.startswith("#"):
            return ln[:limit]
    if lines:
        return lines[0][:limit]
    return "(no diagnostic)"


def clean_verbatim(text):
    """lane_gen.clean without the two substitutions (DWARF attribute text)."""
    return " ".join(text.split())


def selftest():
    cases = [
        "error[E0277]: no implementation for `i32 | f64`",
        "invalid operation: a || b (mismatched types)",
        "a |= b; c",
        "back\\slash and | and ;",
        "plain text",
        "",
    ]
    bad = 0
    for c in cases:
        r = decode(encode(c))
        ok = (r == c) and ("|" not in encode(c)) and (";" not in encode(c))
        print("%-5s enc=%-52r dec-roundtrip=%s" % ("ok" if ok else "FAIL",
                                                   encode(c), r == c))
        if not ok:
            bad += 1
    src = ("unit.rs:5:13: error[E0277]: no implementation for `i32 | f64`\n"
           "note: the trait `BitOr<f64>` is not implemented\n")
    got = firstline_verbatim(src)
    want = "unit.rs:5:13: error[E0277]: no implementation for `i32 | f64`"
    print("%-5s firstline_verbatim -> %r" % ("ok" if got == want else "FAIL",
                                             got))
    if got != want:
        bad += 1
    print("selftest: %d failures" % bad)
    return bad


if __name__ == "__main__":
    import sys
    sys.exit(1 if selftest() else 0)
