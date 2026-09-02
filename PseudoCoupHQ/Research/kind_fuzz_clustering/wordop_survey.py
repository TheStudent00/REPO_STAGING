#!/usr/bin/env python3
"""wordop_survey.py -- log 034 JOB B leg G.

Leg G of decision 43: a word-spelled token is GRAMMAR-DECLARED as a
binary operation of language L iff the grammar declares it among the
anonymous token types reachable from the OPERATOR slot of an L node
whose field shape is (left, operator, right) -- or, where L spells the
operator as a NAMED operator node instead of a field, among that node's
own anonymous tokens, the node being the one the binary-shaped
expression node names.

Reads only ../kind_signature_clustering/raw_all/<L>.node-types.json,
the same file l3_accept.ops() already reads.  Writes wordop_survey.json.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "..", "kind_signature_clustering", "raw_all")
FILE = {"go":"go","rust":"rust","cpp":"cpp","swift":"swift","dart":"dart",
        "csharp":"c-sharp","kotlin":"kotlin","java":"java",
        "typescript":"typescript__typescript","python":"python",
        "ruby":"ruby","php":"php__php"}
LANGS = ["go","rust","cpp","swift","dart","csharp","kotlin","java",
         "typescript","python","ruby","php"]
WORD = re.compile(r"^[A-Za-z_][A-Za-z_0-9 ]*$")

def load(L):
    return json.load(open(os.path.join(RAW, FILE[L]+".node-types.json")))

def anon_tokens(node):
    out = set()
    for f in (node.get("fields") or {}).values():
        for t in f.get("types", []):
            if not t.get("named"): out.add(t["type"])
    for t in (node.get("children") or {}).get("types", []):
        if not t.get("named"): out.add(t["type"])
    return out

def survey(L):
    nodes = load(L)
    by = {n["type"]: n for n in nodes}
    # the token inventory is kinds_<L>.json's own `anonymous` list --
    # the same file and the same field l3_accept.ops() already reads,
    # so leg G adds no new evidence source to the node.
    k = json.load(open(os.path.join(HERE, "kinds_%s.json" % L)))
    allanon = set(k.get("anonymous", []))
    for n in nodes:
        allanon |= anon_tokens(n)
    binaries, ops = [], set()
    for n in nodes:
        if not n.get("named"): continue
        fl = n.get("fields") or {}
        shape = set(fl)
        if shape == {"operators"}:
            # CHAINED shape (python comparison_operator): one repeated
            # operator field over a run of expression children.  Same
            # binary meaning, different grammar spelling.
            ct = [t["type"] for t in (n.get("children") or {}).get("types",[])]
            if not any("expression" in t for t in ct): continue
            toks = set(t["type"] for t in fl["operators"].get("types",[])
                       if not t.get("named"))
            if "=" in toks: continue
            binaries.append(n["type"]); ops |= toks
            continue
        if shape == {"left","right"}:
            # NAMED-NODE shape (kotlin in_expression): the grammar gives
            # the operation its own node type and spells the operator
            # only in the node's NAME.  Mechanical: the name's leading
            # word must itself be an anonymous token of this grammar.
            if not n["type"].endswith("_expression"): continue
            w = n["type"][:-len("_expression")]
            if not (WORD.match(w) and w in allanon): continue
            rt = [t["type"] for t in fl["right"].get("types", [])]
            if not any(("expression" in t) or t in ("expr","primary_expression")
                       for t in rt): continue
            binaries.append(n["type"]); ops.add(w)
            continue
        if shape != {"left","operator","right"}: continue
        # ASSIGNMENT family excluded mechanically: an operator slot that
        # admits the bare token "=" is the assignment family, not a
        # binary value operation.
        _ot = set(t["type"] for t in fl["operator"].get("types", [])
                  if not t.get("named"))
        if "=" in _ot: continue
        if _ot and all(t.endswith("=") for t in _ot): continue
        # the right slot must admit an EXPRESSION, not a TYPE: an
        # operation whose right operand is a type is a type test, not a
        # binary value operation, and layer 3 has no type operands.
        rt = [t["type"] for t in fl["right"].get("types", [])]
        if not any(("expression" in t) or t.endswith("literal")
                   or t in ("expr","primary_expression") for t in rt):
            continue
        binaries.append(n["type"])
        for t in fl["operator"].get("types", []):
            if t.get("named"):
                # NAMED operator node (dart shape): descend one level
                sub = by.get(t["type"])
                if sub: ops |= anon_tokens(sub)
            else:
                ops.add(t["type"])
    words = sorted(o for o in ops if WORD.match(o))
    return dict(language=L, binary_nodes=sorted(binaries),
                operator_tokens=sorted(ops),
                grammar_declared_words=words)

if __name__ == "__main__":
    out = {L: survey(L) for L in LANGS}
    json.dump(out, open(os.path.join(HERE,"wordop_survey.json"),"w"), indent=1)
    for L in LANGS:
        s = out[L]
        print("%-11s nodes=%-42s words=%s" % (
            L, ",".join(s["binary_nodes"]) or "-",
            ", ".join(s["grammar_declared_words"]) or "(none)"))
