#!/usr/bin/env python3
"""l3_boundary_targets.py -- derive the RANGE/BOUNDARY target list.

Layer 3, log 042.  The stored answers are point samples on the whole
number axis.  Where two NUMERICALLY ADJACENT samples of one operation
answer in different classes, a boundary sits between them and is a
measurable number.  This script finds every such pair, host side,
from the artifacts already on disk.  It runs nothing.

Reads   answers_<lang>.json        (the nine checked languages)
        behavior_<lang>_C.json     (python, ruby, php)
        manifest_<lang>.json       (holder forms and value literals)
Writes  boundary_targets.json

Answer class -- decision B1.  Two answers are in the same class when
they agree on all three of:
  * outcome          answer / raise / death / codegen_refuse
  * result type      the type name the language gave the result
  * fidelity         does the answer equal the exact mathematical
                     result, computed over the rationals
Fidelity is `na' where the exact result is not defined without taking
a position the measurement should not take -- division, remainder,
the shifts, and any operand that is not a number.  A pair that
differs only in an `na' fidelity is not a target; a pair that differs
in outcome or in result type is a target whatever the fidelity says.
"""

import json
import os
import struct
import sys
from fractions import Fraction

HERE = os.path.dirname(os.path.abspath(__file__))

# ---------------------------------------------------------------- axis

# the whole-number value classes, in numeric order.  the literal text
# is identical in every language's manifest, checked by axis_check().
WHOLE_AXIS = [
    ("base_zero", 0),
    ("base_42", 42),
    ("p53_plus1", (1 << 53) + 1),
    ("i64max", (1 << 63) - 1),
    ("i64max_plus1", (1 << 63)),
    ("u64max", (1 << 64) - 1),
]
WHOLE_ORDER = {n: k for k, (n, _) in enumerate(WHOLE_AXIS)}
WHOLE_VALUE = dict(WHOLE_AXIS)

# fractional value classes whose exact value is known
FRAC_VALUE = {
    "base_1_5": Fraction(1.5),
    "base_pi": Fraction(3.141592653589793),
    "point1": Fraction(0.1),
    "negzero": Fraction(0),
}

CHECKED = ["go", "rust", "cpp", "swift", "dart", "csharp",
           "kotlin", "java", "typescript"]
OPEN = ["python", "ruby", "php"]

EXACT_OPS = {"+", "-", "*", "<", "<=", ">", ">=", "==", "!="}
CMP_OPS = {"<", "<=", ">", ">=", "==", "!="}


def progress(msg):
    sys.stdout.write(msg + "\n")
    sys.stdout.flush()


# ------------------------------------------------------------- decode

def decode_bits(enc, payload):
    """Return a Fraction for a numeric answer, or None."""
    try:
        if enc.startswith("INT:"):
            bits = int(enc.split(":")[1])
            v = int(payload, 16)
            if v >= (1 << (bits - 1)):
                v -= (1 << bits)
            return Fraction(v)
        if enc.startswith("UINT:"):
            return Fraction(int(payload, 16))
        if enc.startswith("FLOAT:"):
            bits = int(enc.split(":")[1])
            raw = bytes.fromhex(payload)
            if bits == 64:
                f = struct.unpack(">d", raw)[0]
            elif bits == 32:
                f = struct.unpack(">f", raw)[0]
            else:
                return None
            if f != f or f in (float("inf"), float("-inf")):
                return None
            return Fraction(f)
        if enc == "BIGINT":
            s = payload
            neg = s.startswith("-")
            if neg:
                s = s[1:]
            if not s:
                return None
            return Fraction(-int(s, 16) if neg else int(s, 16))
        if enc == "BOOL":
            return Fraction(1) if payload == "true" else Fraction(0)
    except (ValueError, struct.error):
        return None
    return None


def decode_text(tname, text):
    """Return a Fraction for an open-language answer, or None."""
    t = tname.lower()
    if t in ("boolean", "bool", "trueclass", "falseclass"):
        if text in ("1", "True", "true"):
            return Fraction(1)
        if text in ("", "False", "false"):
            return Fraction(0)
        return None
    if t in ("integer", "int"):
        try:
            return Fraction(int(text))
        except ValueError:
            return None
    if t in ("double", "float"):
        try:
            f = float(text)
        except ValueError:
            return None
        if f != f or f in (float("inf"), float("-inf")):
            return None
        return Fraction(f)
    return None


def operand_exact(form, value):
    if form == "whole":
        return WHOLE_VALUE.get(value)
    if form == "fractional":
        v = FRAC_VALUE.get(value)
        return v
    return None


def exact_result(op, a, b):
    """Exact mathematical result as a Fraction, or None for `na'."""
    if a is None or b is None or op not in EXACT_OPS:
        return None
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    if op == "<":
        return Fraction(1) if a < b else Fraction(0)
    if op == "<=":
        return Fraction(1) if a <= b else Fraction(0)
    if op == ">":
        return Fraction(1) if a > b else Fraction(0)
    if op == ">=":
        return Fraction(1) if a >= b else Fraction(0)
    if op == "==":
        return Fraction(1) if a == b else Fraction(0)
    if op == "!=":
        return Fraction(1) if a != b else Fraction(0)
    return None


# -------------------------------------------------------------- rows

def rows_checked(lang):
    """Yield dicts: op, li, lv, lf, ri, rv, rf, outcome, rtype, got."""
    path = os.path.join(HERE, "answers_%s.json" % lang)
    d = json.load(open(path))
    for r in d["rows"]:
        lhs, rhs = r.get("lhs"), r.get("rhs")
        if not lhs or not rhs:
            continue
        res = r.get("result") or {}
        got = None
        rtype = None
        if r["outcome"] == "answer":
            rtype = res.get("type")
            got = decode_bits(res.get("encoding", ""), res.get("payload", ""))
        yield {
            "id": r["id"], "op": r["operation"],
            "lh": lhs["holder"], "lf": lhs["form"], "lv": lhs["value"],
            "rh": rhs["holder"], "rf": rhs["form"], "rv": rhs["value"],
            "outcome": r["outcome"], "rtype": rtype, "got": got,
        }


def rows_open(lang):
    m = json.load(open(os.path.join(HERE, "manifest_%s.json" % lang)))
    holders = {h["i"]: h for h in m["holders"]}
    vnames = {h["i"]: [vc[0] for vc in h["value_classes"]]
              for h in m["holders"]}
    d = json.load(open(os.path.join(HERE, "behavior_%s_C.json" % lang)))
    for key, cell in d["cells"].items():
        body = key[1:]
        i_s, rest = body.split("_", 1)
        j_s, rest = rest.split("_", 1)
        i, j = int(i_s), int(j_s)
        # value names may contain underscores: match longest first
        vx = vy = None
        for cand in sorted(vnames.get(i, []), key=len, reverse=True):
            if rest.startswith(cand + "_"):
                vx = cand
                rest2 = rest[len(cand) + 1:]
                break
        if vx is None:
            continue
        for cand in sorted(vnames.get(j, []), key=len, reverse=True):
            if rest2.startswith(cand + "_"):
                vy = cand
                op = rest2[len(cand) + 1:]
                break
        if vy is None:
            continue
        kind = cell[0]
        payload = cell[1] if len(cell) > 1 else ""
        tname, _, text = payload.partition(":")
        got = None
        rtype = None
        outcome = {"ANSWER": "answer", "RAISE": "raise",
                   "BUDGET": "budget"}.get(kind, kind.lower())
        if kind == "ANSWER":
            rtype = tname
            got = decode_text(tname, text)
        else:
            rtype = tname
        yield {
            "id": key, "op": op,
            "lh": holders[i]["holder"], "lf": holders[i]["form"], "lv": vx,
            "rh": holders[j]["holder"], "rf": holders[j]["form"], "rv": vy,
            "outcome": outcome, "rtype": rtype, "got": got,
        }


def classify(row):
    if row["outcome"] != "answer":
        return (row["outcome"], row["rtype"], "na")
    a = operand_exact(row["lf"], row["lv"])
    b = operand_exact(row["rf"], row["rv"])
    want = exact_result(row["op"], a, b)
    if want is None or row["got"] is None:
        fid = "na"
    else:
        fid = "exact" if row["got"] == want else "inexact"
    return ("answer", row["rtype"], fid)


# ------------------------------------------------------------- derive

def derive(lang, reader):
    rows = list(reader(lang))
    cells = {}
    for r in rows:
        cells[(r["op"], r["lh"], r["rh"], r["lv"], r["rv"])] = r
    targets = []
    exact_already = []
    for side in ("lhs", "rhs"):
        seen = {}
        for (op, lh, rh, lv, rv), r in cells.items():
            vary = lv if side == "lhs" else rv
            form = r["lf"] if side == "lhs" else r["rf"]
            if form != "whole" or vary not in WHOLE_ORDER:
                continue
            fixed = rv if side == "lhs" else lv
            seen.setdefault((op, lh, rh, side, fixed), {})[vary] = r
        for key, byval in seen.items():
            op, lh, rh, sd, fixed = key
            present = sorted(byval, key=lambda n: WHOLE_ORDER[n])
            for a, b in zip(present, present[1:]):
                ca, cb = classify(byval[a]), classify(byval[b])
                if ca == cb:
                    continue
                va, vb = WHOLE_VALUE[a], WHOLE_VALUE[b]
                rec = {
                    "language": lang, "operation": op,
                    "lhs_holder": lh, "rhs_holder": rh,
                    "varying_side": sd, "fixed_value": fixed,
                    "low_class": a, "low_value": str(va),
                    "high_class": b, "high_value": str(vb),
                    "low_answer": list(ca), "high_answer": list(cb),
                    "span": str(vb - va),
                    "low_id": byval[a]["id"], "high_id": byval[b]["id"],
                }
                if vb - va == 1:
                    rec["boundary"] = str(vb)
                    rec["how"] = "already exact: the samples are adjacent"
                    exact_already.append(rec)
                else:
                    targets.append(rec)
    return targets, exact_already


def main():
    all_t, all_e = [], []
    per = {}
    langs = [(l, rows_checked) for l in CHECKED] + \
            [(l, rows_open) for l in OPEN]
    for n, (lang, reader) in enumerate(langs, 1):
        progress("[%2d/%d] %s ..." % (n, len(langs), lang))
        t, e = derive(lang, reader)
        per[lang] = {"targets": len(t), "already_exact": len(e)}
        progress("        %d to bisect, %d already exact" % (len(t), len(e)))
        all_t += t
        all_e += e
    out = {
        "kind": "boundary_targets",
        "written": "log 042",
        "class_rule": "outcome + result type + fidelity (see module head)",
        "axis": [[n, str(v)] for n, v in WHOLE_AXIS],
        "per_language": per,
        "targets": len(all_t),
        "already_exact": len(all_e),
        "rows": all_t,
        "exact_rows": all_e,
    }
    p = os.path.join(HERE, "boundary_targets.json")
    json.dump(out, open(p, "w"), indent=1)
    progress("")
    progress("TOTAL to bisect  : %d" % len(all_t))
    progress("TOTAL already at : %d" % len(all_e))
    progress("wrote %s" % p)


if __name__ == "__main__":
    main()
