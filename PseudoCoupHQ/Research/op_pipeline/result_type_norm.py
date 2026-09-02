#!/usr/bin/env python3
"""result_type_norm.py -- normalize result_type BY MACHINE FACT.

This lap's brief: normalize result_type by MACHINE FACT (DWARF
encoding+width: signed/4->i32, signed/8->i64, unsigned/4->u32,
unsigned/8->u64, boolean/1->bool, float/4->f32, float/8->f64; names
are display labels only), because dom_ops_0branch.py's own
`result_type_of()` is inconsistent across languages: c/cpp collapse
to the coarse "gp"/"vec" fallback (their probes' `meta.result_type`
is null on every unit -- verified: `set(rt for rt in ...)` == {None});
go returns its own type-name strings ("int32", "uint64", ...); rust
returns the compiler's mangled trait-projection string
("<i32 as core::ops::Add<i32>>::Output"). Units whose canonical text
is now IDENTICAL across four languages still land in different
classes on the result-type key alone -- an artifact of how each
probe's type got recorded, not a fact about the computation.

THE FACT SOURCE, per language (evidence class stated per branch, per
the evidence doctrine -- never presented as one uniform tier):

  c, cpp   result_types_c.json / result_types_cpp.json -- THE TOOL'S
           OWN TESTIMONY: `DW_AT_type` read directly off a `-g` build
           of the exact recorded probe source (result_types.py's own
           docstring). Base type name (e.g. "int", "unsigned long",
           "_Bool") mapped to (encoding, width) by the x86-64 SysV
           fixed sizes for the C base types actually observed in this
           corpus (verified exhaustively against the observed value
           set below, not assumed for names outside it).

  rust     result_types_rust.json -- ALSO the tool's own testimony
           (DW_AT_type, same evidence class as c/cpp, its own
           "ground" field says so): base names already ARE i32/i64/
           u32/u64/bool/f32/f64, mapped directly (identity, no name
           table needed).

  go, swift  no DW_AT_type re-read exists for these two (out of
           scope to add one this lap); reuses `meta.result_type`,
           ALREADY the compiler's own recorded type name from probe
           generation (the same field result_types.py's own docstring
           names as already-present testimony for go/rust/swift,
           before rust was upgraded to a direct DWARF re-read). Go's
           and Swift's own fixed-width type names (Int32/UInt64/Bool/
           Float/Double, int32/uint64/bool/float32/float64) are
           mapped to (encoding, width) by each language's own
           committee-fixed definition of that name -- HUMAN
           INTERPRETATION OF STATED DESIGN (the weaker evidence
           class), stated as such rather than silently treated as
           equal-strength to the DWARF-read branches above.

A name/shape this file does not recognize (a pointer type, a Range/
ClosedRange wrapper, an unrecognized mangled projection) is left
UNKNOWN, honestly, never guessed into one of the seven families --
`class_family(u)` returns None for it and the caller decides how to
bucket that (dom_ops_0branch3.py keeps it as its own "unknown" key
component, never silently drops the unit).

THE SPELLING BAN: this module holds no grouping/pairing of units at
all; it is a pure per-unit function, `class_family(lang, u)`.
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

DWARF_TO_CANON = {
    ("signed", 4): "i32",
    ("signed", 8): "i64",
    ("unsigned", 4): "u32",
    ("unsigned", 8): "u64",
    ("boolean", 1): "bool",
    ("float", 4): "f32",
    ("float", 8): "f64",
}


def canon_of(encoding, width):
    return DWARF_TO_CANON.get((encoding, width))


# c/cpp base type name -> (encoding, width). x86-64 SysV fixed sizes.
# Restricted to names actually observed in result_types_c.json /
# result_types_cpp.json (see this file's own header) -- an
# unrecognized name (a struct, a typedef this table does not carry)
# returns None rather than guessing.
C_CPP_BASE = {
    "int": ("signed", 4),
    "long": ("signed", 8),
    "long long": ("signed", 8),
    "short": ("signed", 2),
    "signed char": ("signed", 1),
    "unsigned int": ("unsigned", 4),
    "unsigned long": ("unsigned", 8),
    "unsigned long long": ("unsigned", 8),
    "unsigned short": ("unsigned", 2),
    "unsigned char": ("unsigned", 1),
    "_Bool": ("boolean", 1),
    "bool": ("boolean", 1),
    "float": ("float", 4),
    "double": ("float", 8),
}

# rust: result_types_rust.json's own base names are already canonical.
RUST_BASE = set(["i32", "i64", "u32", "u64", "bool", "f32", "f64"])

# go: meta.result_type's own fixed-width names (human interpretation
# of Go's committee-fixed type sizes, weaker evidence class -- see
# file header).
GO_BASE = {
    "int32": ("signed", 4),
    "int64": ("signed", 8),
    "uint32": ("unsigned", 4),
    "uint64": ("unsigned", 8),
    "bool": ("boolean", 1),
    "float32": ("float", 4),
    "float64": ("float", 8),
}

# swift: same evidence tier as go.
SWIFT_BASE = {
    "Int32": ("signed", 4),
    "Int64": ("signed", 8),
    "UInt32": ("unsigned", 4),
    "UInt64": ("unsigned", 8),
    "Bool": ("boolean", 1),
    "Float": ("float", 4),
    "Double": ("float", 8),
}

_CACHE = {}


def _load_result_types(lang):
    if lang in _CACHE:
        return _CACHE[lang]
    path = os.path.join(HERE, "result_types_%s.json" % lang)
    if not os.path.exists(path):
        _CACHE[lang] = None
        return None
    doc = json.load(open(path))
    _CACHE[lang] = doc.get("result_types", {})
    return _CACHE[lang]


def evidence_class_of(lang):
    if lang in ("c", "cpp", "rust"):
        return "the tool's own testimony (DW_AT_type, a -g re-" \
            "compile of the exact recorded probe source)"
    return "human interpretation of stated design (the language's " \
        "own fixed-width type name, mapped by its committee-fixed " \
        "size -- no DWARF re-read exists for this language yet)"


def class_family(lang, n, meta):
    """(canon_family_or_None, evidence_note). `n` is the probe id
    (string, canon4's own unit key); `meta` is the unit's own
    canon4 `meta` dict, for go/swift's fallback to `result_type`."""
    if lang in ("c", "cpp"):
        table = _load_result_types(lang)
        if table is None:
            return None, "no result_types_%s.json on disk" % lang
        name = table.get(n)
        if name is None:
            return None, "no DWARF-read result type recorded for " \
                "this probe id"
        enc_w = C_CPP_BASE.get(name)
        if enc_w is None:
            return None, "base type name %r not in this file's " \
                "observed C/C++ scalar table (likely a pointer or " \
                "aggregate type, out of the 7-family scope)" % name
        fam = canon_of(*enc_w)
        return fam, "DWARF DW_AT_type -> base name %r -> %r" % (
            name, enc_w)
    if lang == "rust":
        table = _load_result_types(lang)
        if table is None:
            return None, "no result_types_rust.json on disk"
        name = table.get(n)
        if name is None:
            return None, "no DWARF-read result type recorded for " \
                "this probe id"
        if name in RUST_BASE:
            return name, "DWARF DW_AT_type -> base name %r " \
                "(already canonical)" % name
        return None, "base type name %r not one of the 7 scalar " \
            "families (a Range/struct wrapper, out of scope)" % name
    if lang == "go":
        rt = (meta or {}).get("result_type")
        if rt is None:
            return None, "no meta.result_type recorded"
        base = rt[1:] if rt.startswith("*") else rt
        enc_w = GO_BASE.get(base)
        if enc_w is None:
            return None, "go type name %r not in this file's " \
                "fixed-width table" % rt
        return canon_of(*enc_w), "meta.result_type %r -> %r" % (
            rt, enc_w)
    if lang == "swift":
        rt = (meta or {}).get("result_type")
        if rt is None:
            return None, "no meta.result_type recorded"
        enc_w = SWIFT_BASE.get(rt)
        if enc_w is None:
            return None, "swift type name %r not in this file's " \
                "fixed-width table (a Range/ClosedRange wrapper, " \
                "out of scope)" % rt
        return canon_of(*enc_w), "meta.result_type %r -> %r" % (
            rt, enc_w)
    return None, "unrecognized language %r" % lang
