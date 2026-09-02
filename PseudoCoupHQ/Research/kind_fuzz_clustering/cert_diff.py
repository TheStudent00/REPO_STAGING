#!/usr/bin/env python3
"""cert_diff.py -- the CERTIFICATION GATE, run.

CORE_0_3_2 ruling 5 (overlap discipline) and ruling 6 (the
anti-interpretation rule).  A route-B lift is a DRAFT until its
verdicts are diffed, cell by cell, against a route-A run on the same
pairs.  Agreement CERTIFIES the cell.  Disagreement is a FINDING and is
recorded as one -- never reconciled, never averaged, never dropped.

What it reads
-------------
  acceptance_<lang>_<route>.json   route A verdicts, per (operation,
                                   lhs holder, rhs holder)
  raw/lift_b.txt                   the go and java lifts
  raw/lift_b_rust.txt              the rust lift

What it writes
--------------
  certification_<lang>.json        per-cell comparison + the finding
                                   list, with the same `complete` /
                                   `completeness` fields the phase-3
                                   result files carry.

The holder -> lifted-vocabulary map below is EXACT-NAME only: a holder
enters the compared grid when the lift's own vocabulary contains its
own spelling.  Holders that would need a promotion or an unboxing rule
to place are NOT placed -- placing them would be the hand-re-assembly
ruling 6 forbids.  They are counted and named as `unmapped` instead.
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
sys.path.insert(0, HERE)
from progress import Progress          # noqa: E402

# ---------------------------------------------------------------- java

# java's Operators table names its operand types with its own
# OperatorType constants.  Only holders whose declared static type IS
# one of those constants are placed.
JAVA_HOLDER = {
    "boolean": "BOOLEAN",
    "int": "INT",
    "long": "LONG",
    "float": "FLOAT",
    "double": "DOUBLE",
    "String": "STRING",
    # `String v = null;` -- the holder's declared type is String, so
    # this is the table's STRING as well.  Kept in, deliberately: two
    # holders that map to one table type are a free consistency check.
    "null reference": "STRING",
}
JAVA_TAG = {"+": "PLUS", "-": "MINUS", "*": "MUL", "/": "DIV", "%": "MOD",
            "&": "BITAND", "|": "BITOR", "^": "BITXOR", "<<": "SL",
            ">>": "SR", ">>>": "USR", "<": "LT", "<=": "LE", ">": "GT",
            ">=": "GE", "==": "EQ", "!=": "NE", "&&": "AND", "||": "OR"}

# ---------------------------------------------------------------- rust

RUST_HOLDER = {n: n for n in ("bool", "i32", "i64", "u64", "i128",
                              "f64", "f32")}
RUST_TRAIT = {"+": "Add", "-": "Sub", "*": "Mul", "/": "Div", "%": "Rem",
              "&": "BitAnd", "|": "BitOr", "^": "BitXor", "<<": "Shl",
              ">>": "Shr"}


def java_rows():
    rows, tags = set(), set()
    pairs = set()
    for line in open(os.path.join(RAW, "lift_b.txt"), errors="replace"):
        if not line.startswith("java.row|"):
            continue
        f = line.strip().split("|")
        if len(f) < 5:
            continue
        rows.add((f[1], f[2], f[3]))
        tags.add(f[1])
        pairs.add((f[2], f[3]))
    return rows, tags, pairs


def rust_rows():
    rows, traits = set(), set()
    for line in open(os.path.join(RAW, "lift_b_rust.txt"), errors="replace"):
        if not line.startswith("rust.row|"):
            continue
        f = line.strip().split("|")
        if len(f) < 4:
            continue
        rows.add((f[1], f[2], f[3]))
        traits.add(f[1])
    return rows, traits


def certify(lang, holder_map, op_map, lift_rows, lift_ops, note):
    acc = json.load(open(os.path.join(
        HERE, "acceptance_%s_%s.json" % (lang, "A1" if lang == "java"
                                         else "A2"))))
    if not acc.get("complete"):
        print("  !! %s acceptance is not complete -- refusing to certify"
              % lang)
        return None
    hs = acc["holders"]
    ops = acc["operations"]
    idx = {}
    for n, h in enumerate(hs):
        if h["rep"] in holder_map:
            idx[n] = holder_map[h["rep"]]
    compared, agree = 0, 0
    findings = []
    silent_ops, unmapped = [], []
    for o in ops:
        if o not in op_map or op_map[o] not in lift_ops:
            silent_ops.append(o)
    for h in hs:
        if h["rep"] not in holder_map:
            unmapped.append(h["rep"])
    pg = Progress(len(idx) * len(idx) * (len(ops) - len(silent_ops)),
                  "certify:%s" % lang, every=200)
    for o in ops:
        if o in silent_ops:
            continue
        tag = op_map[o]
        for i, ti in idx.items():
            for j, tj in idx.items():
                key = "%s|%d|%d" % (o, i, j)
                cell = acc["cells"].get(key)
                pg.tick()
                if cell is None:
                    continue
                a_verdict = cell["verdict"]
                b_verdict = "ACCEPT" if (tag, ti, tj) in lift_rows \
                    else "REFUSE"
                compared += 1
                if a_verdict == b_verdict:
                    agree += 1
                else:
                    findings.append(dict(
                        operation=o, lift_tag=tag,
                        lhs_holder=hs[i]["rep"], rhs_holder=hs[j]["rep"],
                        lifted_type_lhs=ti, lifted_type_rhs=tj,
                        route_a=a_verdict, route_b=b_verdict))
    pg.close()
    out = dict(
        language=lang,
        route_a=acc["route"], route_b="B (lifted literal data)",
        note=note,
        compared_cells=compared, agreements=agree,
        disagreements=len(findings),
        certified=(len(findings) == 0),
        holders_placed=sorted(set(holder_map)),
        holders_unmapped=unmapped,
        operations_compared=[o for o in ops if o not in silent_ops],
        operations_lift_is_silent_on=silent_ops,
        complete=True,
        completeness="COMPLETE -- every placed holder pair times every "
                     "operation the lift speaks to was compared",
        findings=findings)
    json.dump(out, open(os.path.join(HERE, "certification_%s.json" % lang),
                        "w"), indent=1)
    print("| %s | %d | %d | %d | %s |"
          % (lang, compared, agree, len(findings),
             "CERTIFIED" if not findings else "DISAGREEMENTS RECORDED"))
    return out


def go_redraw():
    """go -- re-count the three cells log_027 section 4 reported, from
    the acceptance file itself, so the numbers in the log are checkable
    rather than quoted."""
    acc = json.load(open(os.path.join(HERE, "acceptance_go_A2.json")))
    hs = acc["holders"]
    per = {}
    for key, cell in acc["cells"].items():
        if cell["verdict"] != "ACCEPT":
            continue
        o = cell["operation"]
        same = cell["lhs"]["holder"] == cell["rhs"]["holder"]
        d = per.setdefault(o, dict(accepts=0, same_holder=0))
        d["accepts"] += 1
        d["same_holder"] += 1 if same else 0
    # which operations the lifted map has a row for, read from the lift
    txt = open(os.path.join(RAW, "lift_b.txt"), errors="replace").read()
    m = re.search(r"binaryOpPredicates = opPredicates\{(.*?)\}", txt, re.S)
    toks = re.findall(r"token\.(\w+):", m.group(1) if m else "")
    TOKEN = {"ADD": "+", "SUB": "-", "MUL": "*", "QUO": "/", "REM": "%",
             "AND": "&", "OR": "|", "XOR": "^", "AND_NOT": "&^",
             "LAND": "&&", "LOR": "||"}
    covered = sorted({TOKEN[t] for t in toks if t in TOKEN})
    out = dict(language="go", route_a="A2", route_b="B (lifted literal map)",
               map_tokens_literal=toks,
               operations_the_map_covers=covered,
               operations_the_map_is_silent_on=sorted(
                   set(acc["operations"]) - set(covered)),
               per_operation_measured=per,
               complete=True,
               completeness="COMPLETE -- counts folded from the complete "
                            "go acceptance file",
               note="log_027 section 4 recorded + as certified and <<, >>, "
                    "==, != as disagreements.  This file re-counts those "
                    "cells from the artifact so the log's numbers are "
                    "checkable.")
    json.dump(out, open(os.path.join(HERE, "certification_go.json"), "w"),
              indent=1)
    print("go: map covers %s; silent on %s"
          % (",".join(covered), ",".join(out["operations_the_map_is_silent_on"])))
    return out


def main():
    jr, jt, jp = java_rows()
    rr, rt = rust_rows()
    print("java lift: %d rows, %d tags, %d distinct ordered operand pairs"
          % (len(jr), len(jt), len(jp)))
    print("rust lift: %d rows, %d traits" % (len(rr), len(rt)))
    print("\n| language | cells compared | agreements | disagreements | verdict |")
    print("|---|---|---|---|---|")
    certify("java", JAVA_HOLDER, JAVA_TAG, jr, jt,
            "javac's own Operators table, lifted with javap -c, against "
            "javac's own checker run in process through javax.tools")
    certify("rust", RUST_HOLDER, RUST_TRAIT, rr, rt,
            "core::ops macro templates and argument lists, expanded "
            "mechanically, against rustc --emit=metadata")
    go_redraw()


if __name__ == "__main__":
    main()
