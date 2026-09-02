#!/usr/bin/env python3
"""result_vocab.py -- one vocabulary for the RESULT TYPE.

Ruling 3 of 2026-08-25 puts the result type into the class key.  The
five languages spell their types five ways, so the spellings have to be
brought to one vocabulary before they can be compared -- otherwise every
class would split by language and the table would say nothing.

Where each spelling comes from, and what class of evidence it is:

  * go, rust, swift -- `meta.result_type`, recorded by the probe
    generator at generation time.  Forced by construction.
  * c, c++ -- recovered by `result_types.py` from DW_AT_type on the
    `op_N` subprogram of a `-g` build.  The tool's own testimony.

Two spellings this program does NOT resolve, and says so on the row
rather than guessing:

  * rust's `<i32 as core::ops::Neg>::Output` -- an associated type the
    corpus never resolved.  Reading it as `i32` would be human
    interpretation of stated design, the weakest class, so it is left
    unresolved and marked.
  * anything else this map does not name.  It is carried through
    verbatim, prefixed `unmapped:`, so it can never quietly equal
    something else.
"""

import re

DIRECT = {
    # the common vocabulary, already in it
    "i32": "i32",
    "i64": "i64",
    "u64": "u64",
    "f32": "f32",
    "f64": "f64",
    "bool": "bool",
    # go
    "int32": "i32",
    "int64": "i64",
    "uint64": "u64",
    "float32": "f32",
    "float64": "f64",
    # c and c++, as the debug information names them
    "int": "i32",
    "long int": "i64",
    "long unsigned int": "u64",
    "unsigned long": "u64",
    "long": "i64",
    "float": "f32",
    "double": "f64",
    "_Bool": "bool",
    # swift
    "Int32": "i32",
    "Int64": "i64",
    "UInt64": "u64",
    "Float": "f32",
    "Double": "f64",
    "Bool": "bool",
}

POINTER = re.compile(r"^pointer to (.+)$")

GO_POINTER = re.compile(r"^\*(.+)$")

SWIFT_OPTIONAL = re.compile(r"^(.+)\?$")

GENERIC = re.compile(r"^([A-Za-z_][A-Za-z0-9_:<>]*?)<(.+)>$")

RUST_ASSOC = re.compile(r"^<(.+) as (.+)>::Output$")


def strip_module(name):
    """`core::ops::RangeTo` and `RangeTo` are the same thing said twice;
    swift says `Range`, rust says `core::ops::Range`."""
    text = name
    if "::" in text:
        text = text.split("::")[-1]
    return text


def normalise(spelling):
    """-> (normal form, note).  The note is None when the map named the
    type outright."""
    if spelling is None:
        return None, "the corpus records no result type for this unit"
    text = str(spelling).strip()
    if text in DIRECT:
        return DIRECT[text], None
    hit = RUST_ASSOC.match(text)
    if hit:
        return ("unresolved associated type: %s" % text,
                "an associated type the corpus never resolved; reading "
                "it as the operand type would be interpretation of "
                "stated design, so it is left unresolved")
    hit = POINTER.match(text)
    if hit:
        inner, note = normalise(hit.group(1))
        return "pointer to %s" % inner, note
    hit = GO_POINTER.match(text)
    if hit:
        inner, note = normalise(hit.group(1))
        return "pointer to %s" % inner, note
    hit = SWIFT_OPTIONAL.match(text)
    if hit:
        inner, note = normalise(hit.group(1))
        return "optional %s" % inner, note
    hit = GENERIC.match(text)
    if hit:
        head = strip_module(hit.group(1))
        inner, note = normalise(hit.group(2))
        return "%s of %s" % (head, inner), note
    if text.startswith("struct "):
        inner = strip_module(text[7:])
        got, note = normalise(inner)
        if not got.startswith("unmapped:"):
            return got, note
        return (inner, "a language's own named type, carried under its "
                       "bare name")
    return ("unmapped: %s" % text,
            "this vocabulary does not name this spelling, so it is "
            "carried verbatim and can equal nothing else")
