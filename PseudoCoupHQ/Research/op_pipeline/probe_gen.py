#!/usr/bin/env python3
"""probe_gen.py -- step 1 of the ratified pipeline: CANDIDATE PROBES.

A PROBE is one compiled function that applies ONE operator to
PARAMETERS only.  Constants are banned: a constant operand is folded
at compile time and the operation we came to measure disappears.

This tool emits EVERY CANDIDATE.  It consults no acceptance file.
Whether a candidate is a real operation of the language is decided
later, by the compiler's own type checker, in the lane
(`lane_gen.py`) -- that is where overload resolution lives, and it is
the acceptance oracle.  A refusal is testimony, not a gap.

Inputs
------
../kind_fuzz_clustering/operator_arity.json
    the grammar-authored operator inventory, per language, in arity
    buckets.  Only three buckets are read here: unary_prefix,
    unary_postfix, binary.

HOLDERS (below, in this file, as data)
    the scalar core, per language: the signed ints, the unsigned int,
    the floats, the truth value.  Six reps -- i32 i64 u64 f32 f64
    bool -- in each language's own spelling.  These mirror the reps
    the arch campaign used.

What it emits, per language
---------------------------
probe_manifest_<lang>.json
    meta   the exclusions and the stated rules, with reasons
    probes n -> {operator, arity, position, lhs_type, rhs_type,
                 symbol, source, ...}

The probe number n is the map-back id: every later artifact keys on
`op_<n>` and resolves it here.

usage:
  probe_gen.py c cpp go rust swift
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARITY = os.path.join(HERE, "..", "kind_fuzz_clustering", "operator_arity.json")

LANGS = ["c", "cpp", "go", "rust", "swift"]

BUCKETS = ["unary_prefix", "unary_postfix", "binary"]

# The buckets deliberately NOT read.  Recorded in the manifest meta.
EXCLUDED_BUCKETS = {
    "assignment": "compound assignment mutates a holder rather than "
                  "producing a value; this first run is scoped to scalar "
                  "EXPRESSIONS, so the assignment bucket is out",
    "ternary": "the conditional operator takes three operands and a "
               "control-flow shape, not the one/two operand expression "
               "shape this run measures",
    "structural": "indexing, calls, member access and the like operate on "
                  "aggregates, not on the scalar core; out of scope for "
                  "this first run",
}


# ------------------------------------------------------------- holders
#
# rep      the campaign-wide name for the representation
# type     the language's own spelling of it
#
# The rep names are the arch campaign's, so a later stage can line the
# two campaigns up without a translation table.

HOLDERS = {
    "c": [
        ("i32", "int32_t"),
        ("i64", "int64_t"),
        ("u64", "uint64_t"),
        ("f32", "float"),
        ("f64", "double"),
        ("bool", "bool"),
    ],
    "cpp": [
        ("i32", "int32_t"),
        ("i64", "int64_t"),
        ("u64", "uint64_t"),
        ("f32", "float"),
        ("f64", "double"),
        ("bool", "bool"),
    ],
    "go": [
        ("i32", "int32"),
        ("i64", "int64"),
        ("u64", "uint64"),
        ("f32", "float32"),
        ("f64", "float64"),
        ("bool", "bool"),
    ],
    "rust": [
        ("i32", "i32"),
        ("i64", "i64"),
        ("u64", "u64"),
        ("f32", "f32"),
        ("f64", "f64"),
        ("bool", "bool"),
    ],
    "swift": [
        ("i32", "Int32"),
        ("i64", "Int64"),
        ("u64", "UInt64"),
        ("f32", "Float"),
        ("f64", "Double"),
        ("bool", "Bool"),
    ],
}


# ------------------------------------------------- operator exclusions
#
# An operator listed here is not a spelling this template can write
# down at all -- it is a grammar placeholder or it needs a name the
# probe has no way to supply.  Everything else is emitted and left to
# the compiler to accept or refuse.

EXCLUDED_OPS = {
    ("swift", "<custom_operator>"):
        "a grammar placeholder standing for any user-declared operator, "
        "not an operator spelling; there is nothing to write",
    ("swift", "."):
        "the implicit-member prefix needs a member NAME after it; with "
        "only a parameter to hand there is no probe to write",
}


# --------------------------------------------------- result type rules
#
# C and C++ need no rule: `auto` and `__typeof__` make the COMPILER
# state the result type, so acceptance stays entirely the type
# checker's.  Go, Rust and Swift require the result type in the
# signature, so a rule is stated here, per operator, and the rule used
# is RECORDED on every probe.  Where no rule is known the fallback is
# the left operand's type, and the probe is marked `fallback_lhs` --
# a refusal on such a probe may be the operator's or may be the
# fallback's, and must not be read as the operator's alone.

CMP = {"<", "<=", ">", ">=", "==", "!="}
LOGIC = {"&&", "||"}

RUST_TRAIT = {
    "+": "Add", "-": "Sub", "*": "Mul", "/": "Div", "%": "Rem",
    "&": "BitAnd", "|": "BitOr", "^": "BitXor", "<<": "Shl", ">>": "Shr",
}


def result_go(op, arity, pos, lt, rt):
    if arity == "binary":
        if op in CMP or op in LOGIC:
            return "bool", "cmp_is_bool"
        return lt, "binary_is_lhs"
    if op == "!":
        return "bool", "not_is_bool"
    if op == "&":
        return "*" + lt, "address_of_is_pointer"
    if op in ("+", "-", "^"):
        return lt, "unary_arith_is_operand"
    return lt, "fallback_lhs"


def result_rust(op, arity, pos, lt, rt):
    if arity == "binary":
        if op in CMP or op in LOGIC:
            return "bool", "cmp_is_bool"
        tr = RUST_TRAIT.get(op)
        if tr is not None:
            spelled = "<%s as core::ops::%s<%s>>::Output" % (lt, tr, rt)
            return spelled, "operator_trait_output"
        if op == "..":
            return "core::ops::Range<%s>" % lt, "range_type"
        if op == "..=":
            return "core::ops::RangeInclusive<%s>" % lt, "range_type"
        return lt, "fallback_lhs"
    if op == "-":
        return "<%s as core::ops::Neg>::Output" % lt, "operator_trait_output"
    if op == "!":
        return "<%s as core::ops::Not>::Output" % lt, "operator_trait_output"
    if op == "..":
        return "core::ops::RangeTo<%s>" % lt, "range_type"
    if op == "..=":
        return "core::ops::RangeToInclusive<%s>" % lt, "range_type"
    return lt, "fallback_lhs"


SWIFT_BOOL = CMP | LOGIC | {"===", "!==", "is"}


def result_swift(op, arity, pos, lt, rt):
    if arity == "binary":
        if op in SWIFT_BOOL:
            return "Bool", "cmp_is_bool"
        if op == "??":
            return lt, "coalesce_is_lhs"
        if op == "..<":
            return "Range<%s>" % lt, "range_type"
        if op == "...":
            return "ClosedRange<%s>" % lt, "range_type"
        return lt, "binary_is_lhs"
    if op == "!" and pos == "prefix":
        return "Bool", "not_is_bool"
    if op == "?" and pos == "postfix":
        return "%s?" % lt, "optional_type"
    if op in ("-", "+", "~"):
        return lt, "unary_arith_is_operand"
    return lt, "fallback_lhs"


RESULT = dict(go=result_go, rust=result_rust, swift=result_swift)


# ------------------------------------------------------ operator spelling

# A separator is needed exactly where the operator's own edge would
# otherwise run into the operand's name and make one longer word.
# `&raw const` ends in a letter, so `&raw consta` is what gluing gives
# -- a parse error that is the HARNESS's, not the language's.  `..<`
# ends in punctuation, so `..<a` is right.  The rule reads the edge
# character, never a list of names.
WORDCH = re.compile(r"\w")


def sep_before(op):
    return " " if WORDCH.match(op[-1]) else ""


def sep_after(op):
    return " " if WORDCH.match(op[0]) else ""


def spell_binary(op):
    return "a %s b" % op


def spell_prefix(op):
    return "%s%s%s" % (op, sep_before(op), "a")


def spell_postfix(op):
    return "%s%s%s" % ("a", sep_after(op), op)


def expression(op, arity, pos):
    if arity == "binary":
        return spell_binary(op)
    if pos == "prefix":
        return spell_prefix(op)
    return spell_postfix(op)


# --------------------------------------------------------- C and C++
#
# `__typeof__(<the same expression, on compound literals>)` in C and
# `auto` in C++ hand the result type back to the compiler.  Nothing
# about the operator's result is asserted here.

def typeof_expr(op, arity, pos, lt, rt):
    a = "(%s){0}" % lt
    if arity == "binary":
        b = "(%s){0}" % rt
        return "%s %s %s" % (a, op, b)
    if pos == "prefix":
        return "%s%s%s" % (op, sep_before(op), a)
    return "%s%s%s" % (a, sep_after(op), op)


def emit_c(n, op, arity, pos, lt, rt):
    head = ["#include <stdint.h>", "#include <stdbool.h>"]
    ty = typeof_expr(op, arity, pos, lt, rt)
    params = "%s a" % lt
    if arity == "binary":
        params = "%s a, %s b" % (lt, rt)
    body = expression(op, arity, pos)
    lines = []
    lines.append("/* probe %d -- %s %s */" % (n, arity, op))
    lines.extend(head)
    lines.append("")
    lines.append("__typeof__(%s)" % ty)
    lines.append("op_%d(%s)" % (n, params))
    lines.append("{")
    lines.append("    return %s;" % body)
    lines.append("}")
    return "\n".join(lines) + "\n"


def emit_cpp(n, op, arity, pos, lt, rt):
    head = ["#include <cstdint>", "#include <compare>", "#include <new>"]
    params = "%s a" % lt
    if arity == "binary":
        params = "%s a, %s b" % (lt, rt)
    body = expression(op, arity, pos)
    lines = []
    lines.append("// probe %d -- %s %s" % (n, arity, op))
    lines.extend(head)
    lines.append("")
    lines.append('extern "C" auto')
    lines.append("op_%d(%s)" % (n, params))
    lines.append("{")
    lines.append("    return %s;" % body)
    lines.append("}")
    return "\n".join(lines) + "\n"


# --------------------------------------------------------------- Go

def emit_go(n, op, arity, pos, lt, rt, res):
    params = "a %s" % lt
    call = "ga"
    if arity == "binary":
        params = "a %s, b %s" % (lt, rt)
        call = "ga, gb"
    body = expression(op, arity, pos)
    lines = []
    lines.append("// probe %d -- %s %s" % (n, arity, op))
    lines.append("package main")
    lines.append("")
    lines.append("//go:noinline")
    lines.append("func op_%d(%s) %s {" % (n, params, res))
    lines.append("\treturn %s" % body)
    lines.append("}")
    lines.append("")
    lines.append("var ga %s" % lt)
    if arity == "binary":
        lines.append("var gb %s" % rt)
    lines.append("var sink interface{}")
    lines.append("")
    lines.append("func main() {")
    lines.append("\tsink = op_%d(%s)" % (n, call))
    lines.append("\t_ = sink")
    lines.append("}")
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------- Rust

def emit_rust(n, op, arity, pos, lt, rt, res):
    params = "a: %s" % lt
    if arity == "binary":
        params = "a: %s, b: %s" % (lt, rt)
    body = expression(op, arity, pos)
    lines = []
    lines.append("// probe %d -- %s %s" % (n, arity, op))
    lines.append("#[no_mangle]")
    lines.append("pub fn op_%d(%s) -> %s {" % (n, params, res))
    lines.append("    %s" % body)
    lines.append("}")
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------ Swift

C_REPRESENTABLE = {"Int32", "Int64", "UInt64", "Float", "Double", "Bool"}


def emit_swift(n, op, arity, pos, lt, rt, res):
    params = "_ a: %s" % lt
    if arity == "binary":
        params = "_ a: %s, _ b: %s" % (lt, rt)
    body = expression(op, arity, pos)
    cdecl = res in C_REPRESENTABLE
    lines = []
    lines.append("// probe %d -- %s %s" % (n, arity, op))
    if cdecl:
        lines.append('@_cdecl("op_%d")' % n)
    lines.append("public func op_%d(%s) -> %s {" % (n, params, res))
    lines.append("    return %s" % body)
    lines.append("}")
    return "\n".join(lines) + "\n", cdecl


# ------------------------------------------------------------- build

def candidates(lang, inv):
    """every (operator, arity, position) this run will try."""
    buckets = inv["languages"][lang]["buckets"]
    out = []
    excluded = []
    for b in BUCKETS:
        ops = buckets[b]["operators"]
        arity = "binary" if b == "binary" else "unary"
        pos = None
        if b == "unary_prefix":
            pos = "prefix"
        if b == "unary_postfix":
            pos = "postfix"
        for op in ops:
            why = EXCLUDED_OPS.get((lang, op))
            if why is not None:
                excluded.append(dict(operator=op, bucket=b, reason=why))
                continue
            out.append((op, arity, pos, b))
    return out, excluded


def build(lang, inv):
    holders = HOLDERS[lang]
    ops, excluded_ops = candidates(lang, inv)
    probes = {}
    n = 0
    for op, arity, pos, bucket in ops:
        pairs = []
        if arity == "binary":
            for lrep, lty in holders:
                for rrep, rty in holders:
                    pairs.append((lrep, lty, rrep, rty))
        else:
            for lrep, lty in holders:
                pairs.append((lrep, lty, None, None))
        for lrep, lty, rrep, rty in pairs:
            rec = dict(n=n, operator=op, arity=arity, position=pos,
                       bucket=bucket,
                       lhs_rep=lrep, lhs_type=lty,
                       rhs_rep=rrep, rhs_type=rty,
                       expression=expression(op, arity, pos))
            sym = "op_%d" % n
            exact = True
            if lang == "c":
                src = emit_c(n, op, arity, pos, lty, rty)
                res = None
                rule = "compiler_states_it_typeof"
            elif lang == "cpp":
                src = emit_cpp(n, op, arity, pos, lty, rty)
                res = None
                rule = "compiler_states_it_auto"
            else:
                res, rule = RESULT[lang](op, arity, pos, lty, rty)
                if lang == "go":
                    src = emit_go(n, op, arity, pos, lty, rty, res)
                    sym = "main.op_%d" % n
                elif lang == "rust":
                    src = emit_rust(n, op, arity, pos, lty, rty, res)
                else:
                    src, cdecl = emit_swift(n, op, arity, pos, lty, rty, res)
                    exact = cdecl
            rec["result_type"] = res
            rec["result_rule"] = rule
            rec["symbol"] = sym
            rec["symbol_exact"] = exact
            rec["source"] = src
            probes[str(n)] = rec
            n += 1
    meta = dict(
        language=lang,
        holders=[dict(rep=r, type=t) for r, t in holders],
        buckets_read=list(BUCKETS),
        excluded_buckets=EXCLUDED_BUCKETS,
        excluded_operators=excluded_ops,
        acceptance="not consulted -- acceptance is discovered by the "
                   "compiler in the lane, never assumed here",
        constants="banned -- every operand is a parameter",
        result_rule_note="c and cpp let the compiler state the result "
                         "type (__typeof__ / auto).  go, rust and swift "
                         "need it in the signature, so each probe "
                         "carries the rule used; `fallback_lhs` means no "
                         "rule was known and the left operand's type was "
                         "used, so a refusal there may be the fallback's "
                         "and not the operator's",
    )
    return meta, probes


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("langs", nargs="+")
    args = ap.parse_args()

    inv = json.load(open(ARITY))

    for lang in args.langs:
        if lang not in LANGS:
            print("skip %s -- no probe template" % lang)
            continue
        meta, probes = build(lang, inv)
        path = os.path.join(HERE, "probe_manifest_%s.json" % lang)
        doc = dict(meta=meta, count=len(probes), probes=probes)
        fh = open(path, "w")
        json.dump(doc, fh, indent=1)
        fh.close()
        by = {}
        for rec in probes.values():
            key = rec["bucket"]
            by[key] = by.get(key, 0) + 1
        parts = []
        for k in BUCKETS:
            parts.append("%s %d" % (k, by.get(k, 0)))
        print("%-6s %5d candidates  (%s)  %d operators excluded"
              % (lang, len(probes), ", ".join(parts),
                 len(meta["excluded_operators"])))
        print("       wrote %s" % path)


if __name__ == "__main__":
    main()
