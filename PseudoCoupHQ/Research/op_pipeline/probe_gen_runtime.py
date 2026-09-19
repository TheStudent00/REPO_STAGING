#!/usr/bin/env python3
"""probe_gen_runtime.py -- step 1 for the runtime languages.

php, ruby, python and java have operator tables in operator_arity.json and no
probe manifest, so their arch-unit populations were never measured; what stood
in log 287 for them was a handful of hand-named interpreter symbols, which
counts nothing.  An arch-unit is one hi-op with its holders, so a population is
the hi-op x holder product, and that is what this writes.

It is probe_gen_jit.py's shape with four more languages: a holder list, a
result rule, and a source template each.  The operators come from
operator_arity.json exactly as they do for every other language -- none is
written out here.

usage:  probe_gen_runtime.py php ruby python java
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ARITY = os.path.join(HERE, "..", "kind_fuzz_clustering", "operator_arity.json")
LANGS = ["php", "ruby", "python", "java"]
BUCKETS = ["unary_prefix", "unary_postfix", "binary"]

EXCLUDED_BUCKETS = {
    "assignment": "compound assignment mutates a holder rather than producing a value",
    "ternary": "conditional operator takes three operands",
    "structural": "indexing, calls, member access",
}

# a holder is (rep, the name the language writes for it)
HOLDERS = {
    # php 7+ scalar type declarations ARE the arrival annotation
    "php": [("i64", "int"), ("f64", "float"), ("bool", "bool")],
    # ruby declares nothing; the holder is what the caller passes, and the
    # class names are what the probe's own comment records
    "ruby": [("i64", "Integer"), ("f64", "Float"), ("bool", "Boolean")],
    "python": [("i64", "int"), ("f64", "float"), ("bool", "bool")],
    "java": [("i32", "int"), ("i64", "long"), ("f32", "float"),
             ("f64", "double"), ("bool", "boolean")],
}

CMP = {"<", "<=", ">", ">=", "==", "!=", "<=>", "===", "!=="}
LOGIC = {"&&", "||", "and", "or", "&", "|"}


def result(lang, op, arity, pos, lt, rt):
    if arity == "binary":
        if op in CMP:
            return {"php": "bool", "ruby": "Boolean",
                    "python": "bool", "java": "boolean"}[lang], "cmp_is_bool"
        if op in LOGIC and lt == rt:
            return lt, "logic_is_lhs"
        return lt, "binary_is_lhs"
    if op in ("!", "not"):
        return {"php": "bool", "ruby": "Boolean",
                "python": "bool", "java": "boolean"}[lang], "not_is_bool"
    return lt, "fallback_lhs"


def expression(op, arity, pos):
    if arity == "binary":
        return "a %s b" % op
    return ("%sa" % op) if pos == "prefix" else ("a%s" % op)


def emit_php(n, op, arity, pos, lt, rt, res):
    args = "%s $a, %s $b" % (lt, rt) if arity == "binary" else "%s $a" % lt
    body = expression(op, arity, pos).replace("a", "$a").replace("b", "$b")
    return ("// probe %d -- %s %s\nfunction op_%d(%s): %s {\n    return %s;\n}\n"
            % (n, arity, op, n, args, res, body))


def emit_ruby(n, op, arity, pos, lt, rt, res):
    args = "a, b" if arity == "binary" else "a"
    return ("# probe %d -- %s %s, holders %s/%s -> %s\ndef op_%d(%s)\n  %s\nend\n"
            % (n, arity, op, lt, rt, res, n, args, expression(op, arity, pos)))


def emit_python(n, op, arity, pos, lt, rt, res):
    args = "a: %s, b: %s" % (lt, rt) if arity == "binary" else "a: %s" % lt
    return ("# probe %d -- %s %s\ndef op_%d(%s) -> %s:\n    return %s\n"
            % (n, arity, op, n, args, res, expression(op, arity, pos)))


def emit_java(n, op, arity, pos, lt, rt, res):
    args = "%s a, %s b" % (lt, rt) if arity == "binary" else "%s a" % lt
    return ("// probe %d -- %s %s\npublic static %s op_%d(%s) {\n"
            "    return %s;\n}\n"
            % (n, arity, op, res, n, args, expression(op, arity, pos)))


EMIT = {"php": emit_php, "ruby": emit_ruby,
        "python": emit_python, "java": emit_java}


def candidates(lang, inv):
    if lang not in inv["languages"]:
        return []
    buckets = inv["languages"][lang]["buckets"]
    out = []
    for b in BUCKETS:
        if b not in buckets:
            continue
        arity = "binary" if b == "binary" else "unary"
        pos = "prefix" if b == "unary_prefix" else (
            "postfix" if b == "unary_postfix" else None)
        for op in buckets[b]["operators"]:
            out.append((op, arity, pos, b))
    return out


def build(lang, inv):
    holders = HOLDERS[lang]
    probes, n = {}, 0
    for op, arity, pos, bucket in candidates(lang, inv):
        if arity == "binary":
            pairs = [(lr, lt, rr, rt) for lr, lt in holders for rr, rt in holders]
        else:
            pairs = [(lr, lt, None, None) for lr, lt in holders]
        for lrep, lty, rrep, rty in pairs:
            res, rule = result(lang, op, arity, pos, lty, rty)
            probes[str(n)] = dict(
                n=n, operator=op, arity=arity, position=pos, bucket=bucket,
                lhs_rep=lrep, lhs_type=lty, rhs_rep=rrep, rhs_type=rty,
                expression=expression(op, arity, pos),
                result_type=res, result_rule=rule,
                symbol="op_%d" % n, symbol_exact=True,
                source=EMIT[lang](n, op, arity, pos, lty, rty, res))
            n += 1
    return {"meta": {"language": lang,
                     "holders": [dict(rep=r, type=t) for r, t in holders],
                     "buckets_read": list(BUCKETS),
                     "excluded_buckets": EXCLUDED_BUCKETS,
                     "operators_from": "kind_fuzz_clustering/operator_arity.json",
                     "count": len(probes)},
            "probes": probes}


def main():
    inv = json.load(open(ARITY))
    for lang in (sys.argv[1:] or LANGS):
        doc = build(lang, inv)
        out = os.path.join(HERE, "probe_manifest_%s.json" % lang)
        json.dump(doc, open(out, "w"), indent=1)
        print("%-8s %4d probes -> %s"
              % (lang, doc["meta"]["count"], os.path.basename(out)))


if __name__ == "__main__":
    main()
