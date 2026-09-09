#!/usr/bin/env python3
"""type_inventory.py -- TASK 29 (a): the EXTRACTED scalar type inventory.

WHY THIS EXISTS
---------------
probe_gen.py's `HOLDERS` table is a HAND-WRITTEN six-row list per
language (i32 i64 u64 f32 f64 bool).  the owner's ruling of 2026-09-01: the
type inventory is EXTRACTED, NEVER HAND-WRITTEN -- the operator
inventory already is (operator_arity.json carries its own authority
line, every operator attributed to the grammar rule that admits it),
and the type half must be brought to the same standard.

This program writes `type_inventory.json` in operator_arity.json's
style: per language, per type, the authority that admits it, pinned.
It does NOT touch probe_gen.py and it does NOT regenerate probes --
TASK 29 (c) reserves the regeneration decision to the owner, with numbers
from type_inventory_validate.py.

THE SPELLING BAN
----------------
No operator token appears in any key, grouping, pairing, row structure,
candidate selection or comparison scope of this program's output.  This
file's subject is TYPES; the only tokens it writes are type spellings,
read out of the sources named below.  The output is checked by
check_no_spelling_keys.py.

THE THREE WITNESSES, and what each one is
-----------------------------------------
grammar
    The tree-sitter grammar source, pinned, from the same
    `grammar_cache/` operator_arity.py reads.  A grammar rule that
    admits a type spelling as a LITERAL TOKEN is a closed, human-written
    enumeration: nothing else can be parsed as a primitive type.  This
    is the ratified route -- the same route the operator inventory came
    down.

compiler_table
    The compiler's own type table, read out of the compiler's source at
    a pinned revision.  Clang's `BuiltinTypes.def` for c/cpp, go/types'
    `universe.go` `Typ` array for go, rustc_codegen_cranelift's
    `common.rs` scalar match for rust.

corpus_accepted
    The type spellings that actually appear on probes THIS CORPUS'S
    COMPILER ACCEPTED, read from op_units_<lang>.json (`tally.accepted`
    rows: the ones carrying a `ship` build).  This witness cannot admit
    a type the probe generator never asked about, so it is a
    CONFIRMING witness only, never an enumerating one.  It is recorded
    because it is the only witness whose evidence class is "the
    compiler said yes to this exact spelling in this exact corpus".

THE WITNESS THE BRIEF ASKED FOR AND THIS PROGRAM REFUSES
--------------------------------------------------------
`dwarf_observed`.  The brief names "DWARF base types observed in the
corpus" as a third witness.  It is REFUSED here, for a checked reason,
not skipped: the corpus artifacts carry DWARF FORMAL-PARAMETER
LOCATIONS only, never the DW_AT_type chain, and the binaries the
locations were read from live under /persist, which does not exist on
this machine.  Both facts are re-checked at run time by
`dwarf_refusal()` below and the checked result is written into the
output, so the refusal is evidence rather than an assertion.

SCALAR CLASSIFICATION IS ALSO EXTRACTED
---------------------------------------
Whether a type is an integer, a float or a truth value is not decided
here by inspection of its name.  Each witness carries its own class
marking and that marking is what is recorded:
  * clang's .def file marks each row SIGNED_TYPE / UNSIGNED_TYPE /
    FLOATING_TYPE;
  * go/types' `Typ` rows carry `IsInteger`, `IsUnsigned`, `IsFloat`,
    `IsBoolean`, `IsComplex`, `IsString`, `IsUntyped`;
  * the rust grammar splits its own list into `numericTypes` and the
    three extras it concatenates (`bool`, `str`, `char`);
  * the c grammar's `primitive_type` rule is one flat token list with
    no class marking, so c/cpp rows from the grammar witness are
    marked `class_source: "unmarked_in_grammar"` and take their class
    from the compiler_table witness where the two agree on a spelling.

USAGE
  /tmp/reconnect_venv/bin/python3 type_inventory.py
writes, next to this file:
  type_inventory.json
  type_inventory.md
"""

import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
KFC = os.path.normpath(os.path.join(HERE, "..", "kind_fuzz_clustering"))
CACHE = os.path.join(KFC, "grammar_cache")
ARITY = os.path.join(KFC, "operator_arity.json")
SOURCES = os.path.expanduser("Sources")

LANGS = ["c", "cpp", "go", "rust", "swift"]

# Which cached grammar file carries each language's type rules.  These
# are the same file names operator_arity.py's GRAMMARS table uses, and
# the pinned version string is read from operator_arity.json rather
# than restated here.
GRAMMAR_FILE_FOR_TYPES = {
    "c": "c.js",
    "cpp": "c_for_cpp.js",
    "go": "go.js",
    "rust": "rust.js",
    "swift": "swift.js",
}

# The rule names searched for in a grammar that has no type-token rule.
# Recorded so a refusal says what was looked for.
TYPE_RULE_NAMES_SEARCHED = [
    "primitive_type", "builtin_type", "predeclared_type", "basic_type",
    "scalar_type", "numeric_type", "simple_type",
]


def run(cmd):
    p = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


# ---------------------------------------------------------------- pins

def git_pin(repo, what):
    code, out, _ = run("git -C %s log -1 --format=%%H" % repo)
    if code != 0:
        return {"present": False, "what": what}
    return {"present": True, "what": what, "path": repo, "commit": out.strip()}


def pins():
    arity = json.load(open(ARITY))
    gv = arity["grammar_versions"]
    out = {
        "grammar_cache": {
            "dir": CACHE,
            "versions": {f: gv[f] for f in sorted(set(
                GRAMMAR_FILE_FOR_TYPES.values())) if f in gv},
            "quoted_from": os.path.normpath(ARITY) + " :: grammar_versions",
        },
        "llvm_project": {
            "path": os.path.join(SOURCES, "llvm-project"),
            "read_at_ref": "llvmorg-21.1.8",
            "read_how": "git show llvmorg-21.1.8:<path> -- the working tree "
                        "of that checkout is at llvmorg-24-init and is NOT read",
            "why_this_ref": "the corpus's c and cpp probes were compiled by "
                            "/usr/bin/clang and /usr/bin/clang++, recorded as "
                            "'Ubuntu clang version 21.1.8 (6ubuntu1)' in "
                            "ordering_encoding.json line 6 and in "
                            "DevComms/log_077_returning_session_briefing.md's "
                            "toolchain table",
        },
        "golang_src": git_pin(os.path.join(SOURCES, "golang_src"),
                              "the vendored go tree read for go/types' Typ table"),
        "rust_sources": git_pin(os.path.join(SOURCES, "rust"),
                                "the vendored rust tree (PARTIAL: three codegen "
                                "crates only)"),
    }
    # the go tree is two releases ahead of the toolchain that compiled the
    # corpus; that is a difference, so it is stated, not smoothed over.
    gv_file = os.path.join(SOURCES, "golang_src",
                           "src/internal/goversion/goversion.go")
    if os.path.exists(gv_file):
        m = re.search(r"const Version = (\d+)", open(gv_file).read())
        out["golang_src"]["goversion_const"] = m.group(1) if m else None
        out["golang_src"]["mismatch_note"] = (
            "goversion.Version = %s (go 1.%s-dev) whereas the corpus's go "
            "probes were compiled by the container's go1.26.0; the type "
            "table is read from the vendored tree because that is the tree "
            "on disk, and the difference is recorded here rather than "
            "assumed away" % (m.group(1) if m else "?", m.group(1) if m else "?"))
    return out


# ------------------------------------------------- witness 1: grammar

def _grammar_text(fname):
    path = os.path.join(CACHE, fname)
    if not os.path.exists(path):
        return None
    return open(path).read()


def grammar_c_like(fname):
    """c.js / c_for_cpp.js: `primitive_type: _ => token(choice( ... ))`.

    The rule body holds plain quoted tokens plus three spread-map lines
    of the shape `...[8, 16, 32, 64].map(n => `int${n}_t`)`.  Both are
    expanded here; nothing is added from memory.
    """
    txt = _grammar_text(fname)
    if txt is None:
        return None, "grammar file not in cache"
    m = re.search(r"primitive_type:\s*_\s*=>\s*token\(choice\((.*?)\)\),",
                  txt, re.S)
    if not m:
        return None, "no primitive_type rule in %s" % fname
    body = m.group(1)
    rows = []
    for lit in re.findall(r"'([^']+)'", body):
        rows.append((lit, "literal"))
    for widths, tmpl in re.findall(
            r"\.\.\.\[([0-9,\s]+)\]\.map\(n\s*=>\s*`([^`]+)`\)", body):
        for w in [x.strip() for x in widths.split(",") if x.strip()]:
            rows.append((tmpl.replace("${n}", w), "spread_map"))
    return rows, None


def grammar_rust(fname):
    """rust.js: `const numericTypes = [...]` then
    `const primitiveTypes = numericTypes.concat(['bool', 'str', 'char'])`.

    The split is the grammar's own, so it is carried through as the
    class marking: numeric vs the three extras.
    """
    txt = _grammar_text(fname)
    if txt is None:
        return None, "grammar file not in cache"
    mn = re.search(r"const numericTypes = \[(.*?)\];", txt, re.S)
    mp = re.search(r"const primitiveTypes = numericTypes\.concat\(\[(.*?)\]\);",
                   txt, re.S)
    if not mn or not mp:
        return None, "numericTypes/primitiveTypes consts not found in %s" % fname
    rows = [(t, "numericTypes") for t in re.findall(r"'([^']+)'", mn.group(1))]
    rows += [(t, "primitiveTypes_concat") for t in
             re.findall(r"'([^']+)'", mp.group(1))]
    return rows, None


def grammar_absent(fname):
    """go.js / swift.js: verify that no type-token rule exists, and say
    which names were searched for."""
    txt = _grammar_text(fname)
    if txt is None:
        return None, "grammar file not in cache"
    found = [n for n in TYPE_RULE_NAMES_SEARCHED
             if re.search(r"^\s*%s:\s*" % n, txt, re.M)]
    if found:
        return None, "unexpected: rule(s) %s DO exist in %s" % (found, fname)
    return [], ("no type-token rule in %s; searched for %s. This grammar "
                "spells every type name as an ordinary identifier "
                "(go.js: `_type_identifier: $ => alias($.identifier, "
                "$.type_identifier)`; swift.js: `user_type` / "
                "`_simple_user_type`), so the grammar route ADMITS NOTHING "
                "here and the inventory for this language cannot be "
                "grammar-authored" % (fname, TYPE_RULE_NAMES_SEARCHED))


def witness_grammar(lang):
    fname = GRAMMAR_FILE_FOR_TYPES[lang]
    if lang in ("c", "cpp"):
        rows, err = grammar_c_like(fname)
        rule = "primitive_type"
    elif lang == "rust":
        rows, err = grammar_rust(fname)
        rule = "primitiveTypes (module-level const, spread into "
        rule += "`alias(choice(...primitiveTypes), $.primitive_type)`)"
    else:
        rows, err = grammar_absent(fname)
        rule = None
    return {"grammar_file": fname, "rule": rule, "rows": rows, "refusal": err}


# ------------------------------------------ witness 2: compiler table

CLANG_DEF = "clang/include/clang/AST/BuiltinTypes.def"


def compiler_table_clang():
    repo = os.path.join(SOURCES, "llvm-project")
    code, out, err = run("git -C %s show llvmorg-21.1.8:%s" % (repo, CLANG_DEF))
    if code != 0:
        return None, "git show failed: %s" % err.strip()[:200]
    rows = []
    lines = out.splitlines()
    for i, line in enumerate(lines):
        m = re.search(r"(SIGNED_TYPE|UNSIGNED_TYPE|FLOATING_TYPE)\((\w+),",
                      line)
        if not m:
            continue
        macro, ident = m.group(1), m.group(2)
        cls = {"SIGNED_TYPE": "integer_signed",
               "UNSIGNED_TYPE": "integer_unsigned",
               "FLOATING_TYPE": "float"}[macro]
        # The C spelling of each builtin is stated in the comment line
        # immediately above it, in single quotes ("// 'unsigned long'").
        # That comment is the .def file's own join between the builtin id
        # and the source spelling, so the join is EXTRACTED, not written
        # here.
        spellings = []
        j = i - 1
        while j >= 0 and lines[j].strip().startswith("//"):
            if "---" not in lines[j]:
                spellings = re.findall(r"'([^']+)'", lines[j]) + spellings
            j -= 1
            break
        rows.append((ident, cls, macro, spellings))
    return rows, None


def compiler_table_go():
    path = os.path.join(SOURCES, "golang_src", "src/go/types/universe.go")
    if not os.path.exists(path):
        return None, "universe.go not on disk at %s" % path
    txt = open(path).read()
    m = re.search(r"var Typ = \[\]\*Basic\{(.*?)\n\}", txt, re.S)
    if not m:
        return None, "Typ table not found in universe.go"
    rows = []
    for flags, name in re.findall(r"\{\s*\w+,\s*([^,]+),\s*\"([^\"]+)\"\}",
                                  m.group(1)):
        rows.append((name, [f.strip() for f in flags.split("|")]))
    return rows, None


CRANELIFT_COMMON = "compiler/rustc_codegen_cranelift/src/common.rs"


def compiler_table_rust():
    path = os.path.join(SOURCES, "rust", CRANELIFT_COMMON)
    if not os.path.exists(path):
        return None, "not on disk at %s" % path
    txt = open(path).read()
    rows = []
    for enum, var in re.findall(r"\b(IntTy|UintTy|FloatTy)::(\w+)\s*=>", txt):
        cls = {"IntTy": "integer_signed", "UintTy": "integer_unsigned",
               "FloatTy": "float"}[enum]
        rows.append((var, cls, enum))
    if not rows:
        return None, "no IntTy/UintTy/FloatTy match arms in %s" % CRANELIFT_COMMON
    return rows, None


def compiler_table_swift():
    guesses = ["swift", "swift-project", "swiftlang"]
    present = [g for g in guesses if os.path.exists(os.path.join(SOURCES, g))]
    return None, ("no swift compiler or stdlib source on disk: %s holds %s; "
                  "searched for %s. swift's scalar type names (Int32, UInt64, "
                  "Float, Double, Bool) are stdlib DECLARATIONS, not grammar "
                  "tokens and not compiler-table rows reachable from here, so "
                  "swift has NO enumerating witness in this run"
                  % (SOURCES, sorted(os.listdir(SOURCES)), guesses + present))


def witness_compiler_table(lang):
    if lang in ("c", "cpp"):
        rows, err = compiler_table_clang()
        return {"source": "%s @ llvmorg-21.1.8" % CLANG_DEF,
                "read_how": "git show", "rows": rows, "refusal": err,
                "note": "these are clang's BUILTIN type ids, not C source "
                        "spellings; the fixed-width spellings the probes use "
                        "(int32_t, uint64_t) are stdint.h typedefs OVER these "
                        "builtins, and they are admitted by the grammar "
                        "witness, not by this one"}
    if lang == "go":
        rows, err = compiler_table_go()
        return {"source": "golang_src :: src/go/types/universe.go :: var Typ",
                "read_how": "regex over the vendored file", "rows": rows,
                "refusal": err,
                "note": "each row carries go/types' own class flags, which is "
                        "where this file's scalar classification for go comes "
                        "from"}
    if lang == "rust":
        rows, err = compiler_table_rust()
        return {"source": "rust :: %s" % CRANELIFT_COMMON,
                "read_how": "regex over the vendored file", "rows": rows,
                "refusal": err,
                "note": "the vendored rust tree is a PARTIAL checkout (three "
                        "codegen crates); rustc's own ty::IntTy/UintTy/FloatTy "
                        "definitions are not on disk, so this reads the "
                        "cranelift back end's exhaustive match over those "
                        "enums -- an exhaustive match is a complete "
                        "enumeration of the enum's variants by construction, "
                        "which is why it is usable as the table"}
    rows, err = compiler_table_swift()
    return {"source": None, "rows": rows, "refusal": err}


# ------------------------------------------- witness 3: corpus accepted

def witness_corpus(lang):
    path = os.path.join(HERE, "op_units_%s.json" % lang)
    if not os.path.exists(path):
        return {"source": None, "rows": None, "refusal": "no op_units file"}
    d = json.load(open(path))
    seen = {}
    for row in d["probes"].values():
        if "ship" not in row:
            continue
        m = row["meta"]
        for side in ("lhs_type", "rhs_type"):
            t = m.get(side)
            if t:
                seen[t] = seen.get(t, 0) + 1
    return {"source": "op_units_%s.json" % lang,
            "read_how": "type spellings on every probe carrying a `ship` build",
            "tally": d["tally"],
            "rows": sorted(seen.items()),
            "refusal": None,
            "note": "CONFIRMING ONLY: this witness can never admit a spelling "
                    "the probe generator did not ask about, so its silence "
                    "about a type is not evidence against that type"}


# ------------------------------------------- the refused fourth witness

def dwarf_refusal():
    checked = {}
    checked["persist_dir_exists"] = os.path.exists("/persist")
    keys = set()
    for lang in LANGS:
        path = os.path.join(HERE, "op_units_%s.json" % lang)
        if not os.path.exists(path):
            continue
        d = json.load(open(path))
        for row in d["probes"].values():
            for side in ("ship", "anchor"):
                for e in (row.get(side) or {}).get("dwarf", []) or []:
                    keys |= set(e)
    checked["dwarf_entry_fields_in_corpus"] = sorted(keys)
    checked["has_type_field"] = any("type" in k for k in keys)
    return {
        "witness": "dwarf_observed",
        "status": "REFUSED",
        "why": "the corpus's DWARF records are formal-parameter LOCATIONS "
               "only; no DW_AT_type chain was ever stored, and the binaries "
               "those locations were read from live under /persist, which "
               "is not present on this machine. Reading DWARF base types for "
               "the compiled five therefore needs a fresh lane run in the "
               "sandbox, which TASK 29 does not authorise.",
        "checked": checked,
        "precedent_that_does_have_it": "dwarf_typed_key.json -- the "
                                       "interpreter track's DWARF read, which "
                                       "did open binaries and did follow "
                                       "DW_AT_type; that route is available, "
                                       "it just has not been run over the "
                                       "compiled five's probe binaries",
    }


# ------------------------------------------------------------- assembly

def build():
    inv = {
        "generated_by": "type_inventory.py",
        "task": "TASK 29 (a) -- the extracted scalar type inventory",
        "authority": "tree-sitter grammar sources and the compilers' own type "
                     "tables, each row attributed to the file and rule that "
                     "admits it; nothing is filled in from memory. Modelled on "
                     "operator_arity.json, which does the same for operators.",
        "replaces": "the hand-written HOLDERS table in probe_gen.py (six rows "
                    "per language). NOTHING IS MODIFIED BY THIS RUN: probe_gen.py "
                    "is left exactly as it is and this file is additive.",
        "spelling_ban": "no operator token appears in any key, grouping, "
                        "pairing or row structure here; the subject of this "
                        "file is types",
        "pins": pins(),
        "witness_definitions": {
            "grammar": "a tree-sitter grammar rule admits the spelling as a "
                       "literal token",
            "compiler_table": "the compiler's own type table names it, at a "
                              "pinned revision",
            "corpus_accepted": "a probe carrying this spelling was accepted by "
                               "the corpus's own compiler (confirming only)",
        },
        "refused_witness": dwarf_refusal(),
        "languages": {},
    }

    for lang in LANGS:
        g = witness_grammar(lang)
        c = witness_compiler_table(lang)
        p = witness_corpus(lang)

        types = {}

        def touch(spelling):
            return types.setdefault(spelling, {
                "admitted_by": [], "class": None, "class_source": None})

        if g["rows"]:
            ver = inv["pins"]["grammar_cache"]["versions"].get(
                g["grammar_file"])
            for spelling, how in g["rows"]:
                e = touch(spelling)
                e["admitted_by"].append({
                    "witness": "grammar",
                    "grammar_file": g["grammar_file"],
                    "grammar_version": ver,
                    "rule": g["rule"],
                    "verification": how,
                })
                if lang == "rust":
                    e["class"] = ("numeric_grammar_marked" if how == "numericTypes"
                                  else "nonnumeric_grammar_marked")
                    e["class_source"] = "rust.js const split"
                else:
                    e["class_source"] = "unmarked_in_grammar"

        if c.get("rows"):
            for row in c["rows"]:
                if lang == "go":
                    spelling, flags = row
                    e = touch(spelling)
                    e["admitted_by"].append({
                        "witness": "compiler_table", "source": c["source"],
                        "flags": flags, "verification": "table_row"})
                    e["class"] = "|".join(flags)
                    e["class_source"] = "go/types Typ flags"
                elif lang in ("c", "cpp"):
                    ident, cls, macro, spellings = row
                    e = touch("clang_builtin::%s" % ident)
                    e["admitted_by"].append({
                        "witness": "compiler_table", "source": c["source"],
                        "declared_as": macro, "c_spellings": spellings,
                        "verification": "table_row"})
                    e["class"] = cls
                    e["class_source"] = macro
                    # attach the class to the SOURCE SPELLING as well, where
                    # the .def file's own comment states one
                    for sp in spellings:
                        s = touch(sp)
                        s["admitted_by"].append({
                            "witness": "compiler_table", "source": c["source"],
                            "declared_as": macro,
                            "joined_via": "the .def comment line above the "
                                          "macro, which states the C spelling",
                            "builtin_id": ident,
                            "verification": "table_row_comment_join"})
                        if s["class"] is None:
                            s["class"] = cls
                            s["class_source"] = macro
                else:
                    ident, cls, macro = row
                    e = touch("rustc_enum::%s" % ident)
                    e["admitted_by"].append({
                        "witness": "compiler_table", "source": c["source"],
                        "declared_as": macro, "verification": "table_row"})
                    e["class"] = cls
                    e["class_source"] = macro
                    # rustc's enum variant names are the source spellings
                    # with the first letter upper-cased (`IntTy::I32` is the
                    # type written `i32`; `FloatTy::F64` is `f64`).  The
                    # join is a case fold, and it is only recorded when the
                    # folded spelling is ALREADY admitted by the grammar
                    # witness -- so the join can never invent a spelling.
                    folded = ident.lower()
                    if folded in types:
                        s = types[folded]
                        s["admitted_by"].append({
                            "witness": "compiler_table", "source": c["source"],
                            "declared_as": macro, "enum_variant": ident,
                            "joined_via": "case fold of the enum variant name, "
                                          "accepted only because the grammar "
                                          "witness already admits this spelling",
                            "verification": "table_row_case_fold_join"})
                        if s["class"] in (None, "numeric_grammar_marked"):
                            s["class"] = cls
                            s["class_source"] = macro

        if p.get("rows"):
            for spelling, count in p["rows"]:
                e = touch(spelling)
                e["admitted_by"].append({
                    "witness": "corpus_accepted", "source": p["source"],
                    "accepted_probe_sides": count,
                    "verification": "observed_on_accepted_probe"})

        inv["languages"][lang] = {
            "witnesses": {
                "grammar": {k: v for k, v in g.items() if k != "rows"},
                "compiler_table": {k: v for k, v in c.items() if k != "rows"},
                "corpus_accepted": {k: v for k, v in p.items() if k != "rows"},
            },
            "counts": {
                "grammar_admitted": len(g["rows"] or []),
                "compiler_table_admitted": len(c.get("rows") or []),
                "corpus_confirmed": len(p.get("rows") or []),
                "distinct_entries": len(types),
            },
            # THE SPELLING BAN, mechanically: a type spelling is never a
            # dict key and never a bare list element here.  Each type is a
            # UNIT OBJECT carrying its own `language` and `id`, with the
            # spelling as the `spelling` field on that unit.  This matters
            # because a handful of type spellings collide with operator
            # spellings somewhere in the 91-token inventory (`void` is one),
            # and check_no_spelling_keys.py is right to refuse them as keys.
            "types": [
                dict(language=lang, id="%s/type_%d" % (lang, i),
                     spelling=sp, **e)
                for i, (sp, e) in enumerate(sorted(types.items()))],
        }
    return inv


def render_md(inv):
    out = []
    A = out.append
    A("# type_inventory -- the extracted scalar type inventory (TASK 29a)\n")
    A("Generated by `type_inventory.py`. Companion of "
      "`../kind_fuzz_clustering/operator_arity.json`, which does the same job "
      "for operators.\n")
    A("## Pins\n")
    A("| what | pin |")
    A("|---|---|")
    for f, v in sorted(inv["pins"]["grammar_cache"]["versions"].items()):
        A("| grammar `%s` | %s |" % (f, v))
    A("| clang type table | `%s` @ llvmorg-21.1.8, read by `git show` |"
      % CLANG_DEF)
    for k in ("golang_src", "rust_sources"):
        p = inv["pins"][k]
        A("| %s | %s |" % (k, p.get("commit", "NOT PRESENT")))
    A("")
    A("## Per language\n")
    A("| language | grammar admits | compiler table admits | corpus confirms |")
    A("|---|---|---|---|")
    for lang in LANGS:
        c = inv["languages"][lang]["counts"]
        A("| %s | %d | %d | %d |" % (lang, c["grammar_admitted"],
                                     c["compiler_table_admitted"],
                                     c["corpus_confirmed"]))
    A("")
    for lang in LANGS:
        L = inv["languages"][lang]
        A("### %s\n" % lang)
        for wname in ("grammar", "compiler_table", "corpus_accepted"):
            w = L["witnesses"][wname]
            if w.get("refusal"):
                A("- **%s: refused** -- %s" % (wname, w["refusal"]))
        A("")
        A("| spelling | class | admitted by |")
        A("|---|---|---|")
        for e in L["types"]:
            A("| `%s` | %s | %s |" % (
                e["spelling"], e["class"] or "-",
                ", ".join(sorted({a["witness"] for a in e["admitted_by"]}))))
        A("")
    return "\n".join(out)


def refuse_own_output_on_spelling_failure(paths):
    """THE MECHANICAL GUARD (AgentMemory, the owner 2026-08-25).

    Every stage that groups or pairs units runs check_no_spelling_keys.py
    over its own output and REFUSES that output on failure -- the file is
    removed and the program exits nonzero, so a spelling-keyed artifact
    can never be left on disk for a later stage to inherit.
    """
    cmd = [sys.executable, os.path.join(HERE, "check_no_spelling_keys.py")]
    cmd += paths
    p = subprocess.run(cmd, capture_output=True, text=True)
    sys.stdout.write(p.stdout)
    sys.stderr.write(p.stderr)
    if p.returncode != 0:
        for path in paths:
            if os.path.exists(path):
                os.remove(path)
        print("REFUSED OWN OUTPUT: spelling-key check failed; "
              "the written file(s) were removed")
        return False
    return True


def main():
    inv = build()
    jpath = os.path.join(HERE, "type_inventory.json")
    with open(jpath, "w") as fh:
        json.dump(inv, fh, indent=1)
    mpath = os.path.join(HERE, "type_inventory.md")
    with open(mpath, "w") as fh:
        fh.write(render_md(inv))
    for lang in LANGS:
        c = inv["languages"][lang]["counts"]
        print("%-6s grammar=%-3d compiler_table=%-3d corpus=%-3d entries=%d"
              % (lang, c["grammar_admitted"], c["compiler_table_admitted"],
                 c["corpus_confirmed"], c["distinct_entries"]))
    if not refuse_own_output_on_spelling_failure([jpath]):
        return 1
    print("wrote %s" % jpath)
    print("wrote %s" % mpath)
    return 0


if __name__ == "__main__":
    sys.exit(main())
