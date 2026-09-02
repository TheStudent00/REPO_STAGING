#!/usr/bin/env python3
"""probe_gen_jit.py -- step 1 of the ratified pipeline for JIT languages.

This tool emits every candidate for javascript, csharp, and dart.
It leverages operator_arity.json to mechanically generate the operator functions.
For JITs, type specialization happens either via static types (C#, Dart) or 
dynamic warmup recipes (JS).

usage:
  probe_gen_jit.py javascript csharp dart
"""

import argparse
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARITY = os.path.join(HERE, "..", "kind_fuzz_clustering", "operator_arity.json")

LANGS = ["javascript", "csharp", "dart"]
BUCKETS = ["unary_prefix", "unary_postfix", "binary"]

EXCLUDED_BUCKETS = {
    "assignment": "compound assignment mutates a holder rather than producing a value",
    "ternary": "conditional operator takes three operands",
    "structural": "indexing, calls, member access",
}

HOLDERS = {
    "javascript": [
        ("i32", "number"),
        ("f64", "number"),
        ("bool", "boolean"),
    ],
    "csharp": [
        ("i32", "int"),
        ("i64", "long"),
        ("u64", "ulong"),
        ("f32", "float"),
        ("f64", "double"),
        ("bool", "bool"),
    ],
    "dart": [
        ("i64", "int"),
        ("f64", "double"),
        ("bool", "bool"),
    ],
}

EXCLUDED_OPS = {
    # Add any excluded JIT ops here if needed.
}

CMP = {"<", "<=", ">", ">=", "==", "!=", "===", "!=="}
LOGIC = {"&&", "||"}

def result_csharp(op, arity, pos, lt, rt):
    if arity == "binary":
        if op in CMP or op in LOGIC:
            return "bool", "cmp_is_bool"
        return lt, "binary_is_lhs"
    if op == "!":
        return "bool", "not_is_bool"
    return lt, "fallback_lhs"

def result_dart(op, arity, pos, lt, rt):
    if arity == "binary":
        if op in CMP or op in LOGIC:
            return "bool", "cmp_is_bool"
        if op == "/":
            return "double", "div_is_double"
        return lt, "binary_is_lhs"
    if op == "!":
        return "bool", "not_is_bool"
    return lt, "fallback_lhs"

def result_javascript(op, arity, pos, lt, rt):
    return "any", "dynamic"

RESULT = dict(csharp=result_csharp, dart=result_dart, javascript=result_javascript)

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

def emit_javascript(n, op, arity, pos, lt, rt, res):
    params = "a"
    if arity == "binary":
        params = "a, b"
    body = expression(op, arity, pos)
    lines = []
    lines.append("// probe %d -- %s %s" % (n, arity, op))
    lines.append("function op_%d(%s) {" % (n, params))
    lines.append("    return %s;" % body)
    lines.append("}")
    return "\n".join(lines) + "\n"

def emit_csharp(n, op, arity, pos, lt, rt, res):
    params = "%s a" % lt
    if arity == "binary":
        params = "%s a, %s b" % (lt, rt)
    body = expression(op, arity, pos)
    lines = []
    lines.append("// probe %d -- %s %s" % (n, arity, op))
    lines.append("public static %s op_%d(%s) {" % (res, n, params))
    lines.append("    return %s;" % body)
    lines.append("}")
    return "\n".join(lines) + "\n"

def emit_dart(n, op, arity, pos, lt, rt, res):
    params = "%s a" % lt
    if arity == "binary":
        params = "%s a, %s b" % (lt, rt)
    body = expression(op, arity, pos)
    lines = []
    lines.append("// probe %d -- %s %s" % (n, arity, op))
    lines.append("%s op_%d(%s) {" % (res, n, params))
    lines.append("    return %s;" % body)
    lines.append("}")
    return "\n".join(lines) + "\n"

def candidates(lang, inv):
    query_lang = "typescript" if lang == "javascript" else lang
    if query_lang not in inv["languages"]:
        return [], []
    buckets = inv["languages"][query_lang]["buckets"]
    out = []
    excluded = []
    for b in BUCKETS:
        if b not in buckets:
            continue
        ops = buckets[b]["operators"]
        arity = "binary" if b == "binary" else "unary"
        pos = "prefix" if b == "unary_prefix" else ("postfix" if b == "unary_postfix" else None)
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
            res, rule = RESULT[lang](op, arity, pos, lty, rty)
            if lang == "javascript":
                src = emit_javascript(n, op, arity, pos, lty, rty, res)
            elif lang == "csharp":
                src = emit_csharp(n, op, arity, pos, lty, rty, res)
            elif lang == "dart":
                src = emit_dart(n, op, arity, pos, lty, rty, res)
            rec["result_type"] = res
            rec["result_rule"] = rule
            rec["symbol"] = sym
            rec["symbol_exact"] = True
            rec["source"] = src
            probes[str(n)] = rec
            n += 1
    meta = dict(
        language=lang,
        holders=[dict(rep=r, type=t) for r, t in holders],
        buckets_read=list(BUCKETS),
        excluded_buckets=EXCLUDED_BUCKETS,
        excluded_operators=excluded_ops,
        acceptance="not consulted -- acceptance is discovered by the compiler",
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
        with open(path, "w") as fh:
            json.dump(doc, fh, indent=1)
        by = {}
        for rec in probes.values():
            key = rec["bucket"]
            by[key] = by.get(key, 0) + 1
        parts = ["%s %d" % (k, by.get(k, 0)) for k in BUCKETS]
        print("%-6s %5d candidates  (%s)  %d operators excluded"
              % (lang, len(probes), ", ".join(parts),
                 len(meta["excluded_operators"])))
        print("       wrote %s" % path)

if __name__ == "__main__":
    main()
