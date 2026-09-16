#!/usr/bin/env python3
"""compare.py -- Sail's softfloat beside the Lean bodies, point by point.

Reads the points, their tags, and the two harnesses' outputs (each line
echoes its input, so a misaligned line is caught, not compared). A point
AGREES when both the result bits and the five flag bits are equal.
Writes one JSON document and one markdown page.
"""
import argparse
import collections
import json

FLAG_BITS = [(0, "NX"), (1, "UF"), (2, "OF"), (3, "DZ"), (4, "NV")]    # the model's own order
MODE = {0: "RNE", 1: "RTZ", 2: "RDN", 3: "RUP", 4: "RMM"}
FORMATS = {16: (5, 10), 32: (8, 23), 64: (11, 52)}


def value_class(w, x):
    e, m = FORMATS[w]
    E = (x >> m) & ((1 << e) - 1)
    M = x & ((1 << m) - 1)
    sign = "neg" if (x >> (e + m)) & 1 else "pos"
    if E == 0:
        c = "zero" if M == 0 else "subnormal"
    elif E == (1 << e) - 1:
        c = "inf" if M == 0 else ("qnan" if (M >> (m - 1)) & 1 else "snan")
    else:
        c = "normal"
    return sign + "_" + c


def flag_names(f):
    return " ".join(n for b, n in FLAG_BITS if (f >> b) & 1) or "none"


def main():
    ap = argparse.ArgumentParser()
    for k in ("ops", "points", "tags", "sf", "lean", "json", "md"):
        ap.add_argument("--" + k, required=True)
    args = ap.parse_args()
    ops = {o["name"]: o for o in json.load(open(args.ops))["ops"]}
    P = open(args.points).read().split("\n")
    T = open(args.tags).read().split("\n")
    S = open(args.sf).read().split("\n")
    L = open(args.lean).read().split("\n")
    per = collections.OrderedDict()
    classes = collections.Counter()
    examples = collections.defaultdict(list)
    misaligned = unknown = 0
    for i, p in enumerate(P):
        if not p.strip():
            continue
        pp = p.split()
        s = S[i].split() if i < len(S) else []
        l = L[i].split() if i < len(L) else []
        if s[:4] != pp or l[:4] != pp:
            misaligned += 1
            continue
        if len(s) < 6 or len(l) < 6:
            unknown += 1
            continue
        name, rm = pp[0], int(pp[1], 16)
        a, b = int(pp[2], 16), int(pp[3], 16)
        sf_f, sf_r, le_f, le_r = int(s[4], 16), int(s[5], 16), int(l[4], 16), int(l[5], 16)
        op = ops[name]
        mode = MODE[rm] if op["shape"] == "rm2" else "none"
        origin = T[i].split()[0] if i < len(T) and T[i] else "?"
        row = per.setdefault(name, {"operation": name, "width": op["width"], "shape": op["shape"],
                                    "points": 0, "edge_points": 0, "random_points": 0, "agree": 0,
                                    "result_differs": 0, "flags_differ": 0, "both_differ": 0,
                                    "by_mode": collections.OrderedDict()})
        bm = row["by_mode"].setdefault(mode, {"mode": mode, "points": 0, "agree": 0, "disagree": 0})
        row["points"] += 1
        bm["points"] += 1
        row["edge_points" if origin == "edge" else "random_points"] += 1
        same_r, same_f = sf_r == le_r, sf_f == le_f
        if same_r and same_f:
            row["agree"] += 1
            bm["agree"] += 1
            continue
        bm["disagree"] += 1
        part = "result" if same_f else ("flags" if same_r else "both")
        row[{"result": "result_differs", "flags": "flags_differ", "both": "both_differ"}[part]] += 1
        ca, cb = value_class(op["width"], a), value_class(op["width"], b)
        classes[(name, mode, ca, cb, part, flag_names(sf_f ^ le_f))] += 1
        if len(examples[name]) < 8:
            examples[name].append({"operation": name, "mode": mode, "a": "%x" % a, "b": "%x" % b,
                                   "a_class": ca, "b_class": cb, "tag": T[i] if i < len(T) else "",
                                   "softfloat_flags": flag_names(sf_f), "softfloat_result": "%x" % sf_r,
                                   "lean_flags": flag_names(le_f), "lean_result": "%x" % le_r, "part": part})
    rows = []
    for r in per.values():
        r["by_mode"] = list(r["by_mode"].values())
        rows.append(r)
    total = sum(r["points"] for r in rows)
    agree = sum(r["agree"] for r in rows)
    doc = {"summary": {"operations": len(rows), "points": total, "agree": agree, "disagree": total - agree,
                       "misaligned_lines": misaligned, "unknown_lines": unknown},
           "per_operation": rows,
           "disagreement_classes": [{"operation": k[0], "mode": k[1], "a_class": k[2], "b_class": k[3],
                                     "part": k[4], "flag_bits_differing": k[5], "count": v}
                                    for k, v in sorted(classes.items(), key=lambda kv: (-kv[1], kv[0]))],
           "examples": [e for n in per for e in examples.get(n, [])]}
    json.dump(doc, open(args.json, "w"), indent=1)
    md = ["# level 0: the Lean bodies against Sail's softfloat", "",
          "| operations | points | agree | disagree | misaligned lines | unknown lines |",
          "|---|---|---|---|---|---|",
          "| %d | %d | %d | %d | %d | %d |" % (len(rows), total, agree, total - agree, misaligned, unknown), "",
          "| operation | width | points (edge, random) | agree | result differs | flags differ | both differ | modes with a disagreement |",
          "|---|---|---|---|---|---|---|---|"]
    for r in rows:
        bad = ", ".join("%s %d" % (m["mode"], m["disagree"]) for m in r["by_mode"] if m["disagree"])
        md.append("| %s | %d | %d (%d, %d) | %d | %d | %d | %d | %s |" % (
            r["operation"], r["width"], r["points"], r["edge_points"], r["random_points"], r["agree"],
            r["result_differs"], r["flags_differ"], r["both_differ"], bad or "none"))
    if doc["disagreement_classes"]:
        md += ["", "## disagreements by class", "",
               "| operation | mode | a | b | part | flag bits differing | count |", "|---|---|---|---|---|---|---|"]
        for c in doc["disagreement_classes"][:60]:
            md.append("| %s | %s | %s | %s | %s | %s | %d |" % (c["operation"], c["mode"], c["a_class"], c["b_class"],
                                                            c["part"], c["flag_bits_differing"], c["count"]))
        md += ["", "## examples (first per operation)", "",
               "| operation | mode | a | b | tag | softfloat flags | softfloat result | Lean flags | Lean result |",
               "|---|---|---|---|---|---|---|---|---|"]
        for e in doc["examples"]:
            md.append("| %s | %s | %s | %s | %s | %s | %s | %s | %s |" % (
                e["operation"], e["mode"], e["a"], e["b"], e["tag"], e["softfloat_flags"], e["softfloat_result"],
                e["lean_flags"], e["lean_result"]))
    open(args.md, "w").write("\n".join(md) + "\n")
    print("  points %d, agree %d, disagree %d, misaligned %d, unknown %d" % (total, agree, total - agree, misaligned, unknown))


if __name__ == "__main__":
    main()
