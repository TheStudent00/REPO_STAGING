#!/usr/bin/env python3
"""core_rule2.py -- the shared scalar-core rule, version 2.

WHY A VERSION 2 EXISTS
----------------------

The version-1 rule states its own scope in words, in
`type_inventory_validate.py`:

    "A type is in the scalar core when an EXTRACTED class marking says it
     is an integer, a float or a truth value."

Its implementation does not match that sentence.  The membership test is
a tuple:

    NUMERIC_MARKS = ("integer_signed", "integer_unsigned", "float",
                     "numeric_grammar_marked")

There is no truth-value entry in it.  So a type whose extracted marking
says truth value falls through to `undecided` -- not by a decision, by a
missing tuple entry.  Two types are affected across the five compiled
languages:

    swift  Bool   marking `truth_value`                (Bool.swift:142)
    rust   bool   marking `nonnumeric_grammar_marked`  (rust.js const split)

Ruled 2026-09-01 (log_129 addendum, F35-1 / L125-1): booleans have been
in the ratified six-type core since the first probe run; this is a code
gap, and the fix is to add the truth-value mark to the SHARED rule.

WHAT VERSION 2 CHANGES, AND WHY IT IS ONE MECHANISM RATHER THAN TWO ROWS
-----------------------------------------------------------------------

The fix is NOT "also accept the string `truth_value`".  That would admit
swift and leave rust out, because rust's grammar marking
(`nonnumeric_grammar_marked`) is one marking covering three types --
`bool`, `char` and `str` -- and admitting it wholesale would drag text
and characters into a scalar core.  Naming `rust bool` by hand would be
the per-name patch this line bans.

Version 2 instead defers to the CLASS NORMALISATION that already exists
and is already used by `legality_filter.py`: the table that maps each
language's own marking into the four classes the legality rules speak in
(`integer_signed`, `integer_unsigned`, `float`, `truth_value`).

    THE RULE, v2: a type is in the scalar core when its NORMALISED class
    is one of the four.  A type whose marking normalises to nothing is
    undecided, exactly as before.

That is the version-1 sentence, implemented.  One membership test, one
place, no per-name row added by this module.

TWO CONSEQUENCES THAT WERE MEASURED, NOT ASSUMED

- rust's marking still normalises to nothing on its own, so version 2
  reads a SECOND authority for it -- rustc's own type-kind match, parsed
  at run time (RUST_KIND_SOURCE below).  `bool` gets a class there;
  `char` and `str` get none, so they stay out without being named.
- the six DECLARED stdint aliases (`int32_t` and co.) are deliberately
  NOT consulted for core membership.  A first cut admitted them and c/cpp
  went 56 -> 59; every one of the three is an alias of a type already in
  the core, so that would count one holder twice.  They remain lookup-only
  (DECLARED_ALIASES_FOR_LOOKUP_ONLY), and c/cpp are unchanged at 56.

WHAT IT DOES TO EACH LANGUAGE, stated so it can be checked

    c, cpp   `bool` normalises to integer_unsigned (clang's own
             BuiltinTypes.def declares it UNSIGNED_TYPE).  Already in the
             core in v1.  NO CHANGE.
    go       `IsBoolean` normalises to truth_value, and go's own branch
             already admitted IsBoolean via GO_SCALAR_FLAGS.  NO CHANGE.
    rust     `bool` normalises to truth_value.  ENTERS the core.
             `char` and `str` normalise to nothing.  Still out.
    swift    `Bool` normalises to truth_value.  ENTERS the core.

THE EVIDENCE FOR RUST'S TRUTH-VALUE NORMALISATION

`legality_filter.py` already carries `("rust", "bool"): "truth_value"` in
its DECLARED_CLASSES table, where it is marked as declared rather than
extracted (evidence class: human interpretation of stated design).  It
does not have to stay that weak.  rustc's own code generator enumerates
the operand's type kind and gives Bool its own arm, distinct from the
integer and float arms, in the same file `legality_rules.py` already
reads at the same pin:

    <WORKSPACE_DIR>/Sources/rust/compiler/rustc_codegen_cranelift/src/num.rs
    pin 7c329d6c76e11ca40c5673818ab0439c1be8962c
    line 105:  ty::Bool => crate::num::codegen_bool_binop(fx, bin_op, in_lhs, in_rhs),

Evidence class for "rust `bool` is a truth value and not an integer":
THE TOOL'S OWN TESTIMONY -- rustc's type-kind match, read at a named pin
and line.  This module records that citation; it does not weaken to a
declaration.

THE SPELLING BAN
----------------

Nothing here keys, groups, pairs or selects by an operator token.  This
module speaks only about TYPE spellings, and every type spelling it
emits rides on an object carrying `language` and `id`, with the spelling
in a `spelling` display field -- the shape `check_no_spelling_keys.py`
allows.

usage:
    /tmp/reconnect_venv/bin/python3 core_rule2.py
writes:
    type_inventory2_core2.json
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]

# The four classes the legality rules speak in.  Membership in this set IS
# the version-2 scalar-core test.
CORE_CLASSES = ("integer_signed", "integer_unsigned", "float", "truth_value")

# Each language's own marking -> one of the four classes.  Copied from
# `legality_filter.py :: CLASS_NORMALISATION` so the two agree; the rust
# truth-value row is the one addition, and its citation is in the module
# header.
CLASS_NORMALISATION = {
    "c": {
        "integer_signed": "integer_signed",
        "integer_unsigned": "integer_unsigned",
        "float": "float",
    },
    "cpp": {
        "integer_signed": "integer_signed",
        "integer_unsigned": "integer_unsigned",
        "float": "float",
    },
    "go": {
        "IsInteger": "integer_signed",
        "IsInteger|IsUnsigned": "integer_unsigned",
        "IsFloat": "float",
        "IsBoolean": "truth_value",
    },
    "rust": {
        "integer_signed": "integer_signed",
        "integer_unsigned": "integer_unsigned",
        "float": "float",
    },
    "swift": {
        "integer_signed": "integer_signed",
        "integer_unsigned": "integer_unsigned",
        "float": "float",
        "truth_value": "truth_value",
    },
}

# Spellings whose class no authority states in the inventory's own `class`
# field, resolved by DECLARATION rather than by extraction.  Carried over
# from `legality_filter.py :: DECLARED_CLASSES`, MINUS its rust `bool` row,
# which version 2 extracts instead (see RUST_KIND_SOURCE below).
#
# THESE NEVER ADD A MEMBER TO THE SCALAR CORE.  They exist so a probe
# written at one of the corpus's six hand-written holder types can be
# looked up during validation.  All six are ALIASES of types already in
# the core (`int32_t` is `int`, `int64_t` is `long`), so admitting them to
# the core would count the same holder twice.  Core membership is decided
# by EXTRACTED markings only; that separation is the whole reason this
# table is not consulted by `scalar_core`.
DECLARED_ALIASES_FOR_LOOKUP_ONLY = {
    ("c", "int32_t"): ("integer_signed", "log 116 F3: stdint.h typedef"),
    ("c", "int64_t"): ("integer_signed", "log 116 F3: stdint.h typedef"),
    ("c", "uint64_t"): ("integer_unsigned", "log 116 F3: stdint.h typedef"),
    ("cpp", "int32_t"): ("integer_signed", "log 116 F3: stdint.h typedef"),
    ("cpp", "int64_t"): ("integer_signed", "log 116 F3: stdint.h typedef"),
    ("cpp", "uint64_t"): ("integer_unsigned", "log 116 F3: stdint.h typedef"),
}

# ---- rust's missing class marking, EXTRACTED rather than declared -------
#
# rust.js splits its primitive types into a numeric set and the rest, and
# the inventory records the rest as `nonnumeric_grammar_marked` -- one
# marking covering `bool`, `char` and `str`.  That marking states no
# class, so it cannot normalise, and admitting it wholesale would drag
# text and characters into a scalar core.
#
# A second authority states the classes: rustc's code generator matches on
# the operand's TYPE KIND and gives each kind its own arm.  The arms are
# read from the file at run time -- not typed in -- and a missing block is
# a hard failure, the same discipline `legality_rules.py :: find_line()`
# uses.
RUST_KIND_SOURCE = os.path.expanduser(
    "<WORKSPACE_DIR>/Sources/rust/compiler/rustc_codegen_cranelift/src/num.rs")
RUST_KIND_PIN = "7c329d6c76e11ca40c5673818ab0439c1be8962c"
RUST_KIND_ANCHOR = "match in_lhs.layout().ty.kind() {"
# kind name -> the class of the four, for the arms that name a scalar.
# An arm naming no scalar class (RawPtr, FnPtr) contributes nothing, and a
# kind with NO arm at all (Char, Str) contributes nothing either -- which
# is how `char` and `str` stay out without being named here.
RUST_KIND_CLASS = {
    "Bool": "truth_value",
    "Int": "integer_signed",
    "Uint": "integer_unsigned",
    "Float": "float",
}


def rust_kind_arms():
    """The kind names rustc's binary-operation match gives an arm.

    Returns {kind_name: line_text}.  Raises if the anchor block is absent,
    so a moved or renamed match can never silently produce an empty table.
    """
    if not os.path.exists(RUST_KIND_SOURCE):
        raise SystemExit(
            "core_rule2: rust kind authority absent: %s" % RUST_KIND_SOURCE)
    lines = open(RUST_KIND_SOURCE).read().split("\n")
    start = None
    i = 0
    for line in lines:
        if RUST_KIND_ANCHOR in line:
            start = i
            break
        i = i + 1
    if start is None:
        raise SystemExit(
            "core_rule2: rust kind authority does not carry the anchor "
            "%r; refusing to guess" % RUST_KIND_ANCHOR)
    arms = {}
    j = start + 1
    while j < len(lines):
        line = lines[j]
        if line.strip().startswith("}"):
            break
        for token in re.findall(r"ty::([A-Za-z]+)", line):
            arms[token] = (j + 1, line.strip())
        j = j + 1
    return arms


def rust_extracted_classes():
    """rust spelling -> (class, citation), for the grammar-unmarked types.

    The join is by NAME IDENTITY between the source spelling and the kind
    the compiler names for it (`bool` <-> `ty::Bool`), which is the same
    join shape log 127 used for the other four languages' authority
    tables.  A spelling whose kind has no arm gets nothing.
    """
    arms = rust_kind_arms()
    out = {}
    for spelling in ("bool", "char", "str"):
        kind = spelling[:1].upper() + spelling[1:]
        if kind not in arms:
            continue
        cls = RUST_KIND_CLASS.get(kind)
        if cls is None:
            continue
        line_no, text = arms[kind]
        out[spelling] = (cls, {
            "source_file":
                "compiler/rustc_codegen_cranelift/src/num.rs",
            "pin": RUST_KIND_PIN,
            "line": line_no,
            "text": text,
            "join": "name identity between the source spelling and the "
                    "kind rustc names for it",
            "evidence_class": "the tool's own testimony",
        })
    return out

# The go branch of the v1 rule, unchanged.  Go's markings are flag strings
# rather than single class names, so the flags decide, then the
# normalisation names the class.
GO_DISQUALIFY = ("IsUntyped", "IsComplex", "IsString")

# The v1 tuple, kept for the delta report only.  Never used as a test here.
V1_NUMERIC_MARKS = ("integer_signed", "integer_unsigned", "float",
                    "numeric_grammar_marked")


RUST_EXTRACTED = None


def rust_extracted():
    global RUST_EXTRACTED
    if RUST_EXTRACTED is None:
        RUST_EXTRACTED = rust_extracted_classes()
    return RUST_EXTRACTED


def normalised_class(lang, spelling, marking):
    """The type's class in the four-class vocabulary, or None.

    EXTRACTED markings only.  The declared aliases are deliberately not
    consulted here -- see DECLARED_ALIASES_FOR_LOOKUP_ONLY.
    """
    if lang == "rust" and spelling in rust_extracted():
        return rust_extracted()[spelling][0]
    table = CLASS_NORMALISATION[lang]
    if marking is None:
        return None
    return table.get(marking)


def lookup_class(lang, spelling, marking):
    """The class for a spelling that appears on a PROBE, which may be one
    of the six declared aliases.  Used by validation, never by the core."""
    key = (lang, spelling)
    if key in DECLARED_ALIASES_FOR_LOOKUP_ONLY:
        return DECLARED_ALIASES_FOR_LOOKUP_ONLY[key][0]
    return normalised_class(lang, spelling, marking)


def in_core_v1(lang, marking):
    """The version-1 membership test, reproduced for the delta only."""
    if lang == "go":
        flags = marking.split("|") if marking else []
        if any(f in GO_DISQUALIFY for f in flags):
            return False
        return any(f in ("IsInteger", "IsFloat", "IsBoolean") for f in flags)
    return marking in V1_NUMERIC_MARKS


def scalar_core(lang, inv):
    """Version 2.  Returns (core, undecided), each a list of
    (spelling, marking, normalised_class)."""
    core = []
    undecided = []
    for entry in inv["languages"][lang]["types"]:
        spelling = entry["spelling"]
        if "::" in spelling:
            # a compiler-table id, not a source spelling: a probe cannot be
            # written with it.  Excluded exactly as version 1 excluded it.
            continue
        marking = entry.get("class")
        if lang == "go":
            flags = marking.split("|") if marking else []
            if any(f in GO_DISQUALIFY for f in flags):
                continue
            cls = normalised_class(lang, spelling, marking)
            if cls in CORE_CLASSES:
                core.append((spelling, marking, cls))
            continue
        cls = normalised_class(lang, spelling, marking)
        if cls in CORE_CLASSES:
            core.append((spelling, marking, cls))
        else:
            undecided.append((spelling, marking, cls))
    core = sorted(set(core))
    undecided = sorted(set(undecided))
    return core, undecided


def rows(lang, triples, tag):
    """Type spellings as UNIT OBJECTS, never as bare keys."""
    out = []
    i = 0
    for spelling, marking, cls in triples:
        out.append({
            "language": lang,
            "id": "%s/%s_%d" % (lang, tag, i),
            "spelling": spelling,
            "extracted_marking": marking,
            "normalised_class": cls,
        })
        i = i + 1
    return out


def build():
    inv_path = os.path.join(HERE, "type_inventory2.json")
    inv = json.load(open(inv_path))
    doc = {}
    doc["generated_by"] = "core_rule2.py"
    doc["reads"] = ["type_inventory2.json", RUST_KIND_SOURCE]
    doc["rust_extracted_class_citations"] = {
        k: {"class": v[0], "citation": v[1]}
        for k, v in rust_extracted().items()}
    doc["rule_v2"] = (
        "a type is in the scalar core when its NORMALISED class is one of "
        "integer_signed, integer_unsigned, float, truth_value; a type whose "
        "marking normalises to nothing is undecided and is never guessed")
    doc["rule_v1_that_this_supersedes"] = (
        "membership in the tuple ('integer_signed', 'integer_unsigned', "
        "'float', 'numeric_grammar_marked') -- which has no truth-value "
        "entry, so a truth value fell through to undecided by code gap")
    doc["ruling"] = (
        "log_129 addendum 2026-09-01, F35-1 / L125-1 RESOLVED: booleans "
        "have been in the ratified six-type core since the first probe run")
    doc["supersedes_nothing_on_disk"] = (
        "type_inventory_validate.py and type_inventory2_validation.json are "
        "not modified; this is a new file beside them")
    doc["languages"] = {}
    totals = {"core_v1": 0, "core_v2": 0, "entered": 0}
    for lang in LANGS:
        core, undecided = scalar_core(lang, inv)
        v1 = []
        for entry in inv["languages"][lang]["types"]:
            if "::" in entry["spelling"]:
                continue
            if in_core_v1(lang, entry.get("class")):
                v1.append(entry["spelling"])
        v1 = sorted(set(v1))
        v2_spellings = sorted(set(s for s, _m, _c in core))
        entered = [s for s in v2_spellings if s not in v1]
        left = [s for s in v1 if s not in v2_spellings]
        record = {}
        record["scalar_core_size_v1"] = len(v1)
        record["scalar_core_size_v2"] = len(v2_spellings)
        record["entered_the_core_under_v2"] = rows(
            lang,
            [t for t in core if t[0] in entered],
            "entered")
        record["left_the_core_under_v2"] = left
        record["scalar_core"] = rows(lang, core, "core")
        record["undecided"] = rows(lang, undecided, "undecided")
        doc["languages"][lang] = record
        totals["core_v1"] = totals["core_v1"] + len(v1)
        totals["core_v2"] = totals["core_v2"] + len(v2_spellings)
        totals["entered"] = totals["entered"] + len(entered)
    doc["totals"] = totals
    return doc


def refuse_own_output_on_spelling_failure(paths):
    cmd = [sys.executable, os.path.join(HERE, "check_no_spelling_keys.py")]
    cmd.extend(paths)
    done = subprocess.run(cmd, capture_output=True, text=True)
    print(done.stdout.strip())
    if done.returncode != 0:
        print(done.stderr.strip())
        for path in paths:
            if os.path.exists(path):
                os.remove(path)
        raise SystemExit("REFUSED OWN OUTPUT: spelling guard failed")


def main():
    doc = build()
    path = os.path.join(HERE, "type_inventory2_core2.json")
    fh = open(path, "w")
    json.dump(doc, fh, indent=1)
    fh.write("\n")
    fh.close()
    for lang in LANGS:
        record = doc["languages"][lang]
        entered = [r["spelling"] for r in record["entered_the_core_under_v2"]]
        print("%-6s core v1 %3d -> v2 %3d   entered: %s"
              % (lang,
                 record["scalar_core_size_v1"],
                 record["scalar_core_size_v2"],
                 ", ".join(entered) if entered else "(none)"))
    print("wrote %s" % path)
    refuse_own_output_on_spelling_failure([path])


if __name__ == "__main__":
    main()
