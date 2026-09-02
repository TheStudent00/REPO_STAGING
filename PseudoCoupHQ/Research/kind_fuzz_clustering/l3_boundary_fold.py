#!/usr/bin/env python3
"""l3_boundary_fold.py -- read the bisection lanes back and write
boundaries_<lang>.json plus the readable boundaries.md.

For every target the run printed one line:
    B|tid|last_low|first_high|sig_low|sig_high|probes|other_classes
    N|tid|sig_low|sig_high            (the two ends agreed at run time)

The located boundary is `first_high': the least value of the varying
operand at which the answer class is no longer the low class.  Beside
it this records the boundary in RESULT space -- the exact value the
operation would have had -- because that is where the powers of two
live.  An operand boundary of 9223372036854775766 means nothing until
you see that adding 42 to it gives exactly 2^63.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.abspath(os.path.join(HERE, "..", "..", "..",
                                   "SandboxDesign", "agent", "out"))
RAW = os.path.join(HERE, "raw")

from l3_boundary_targets import WHOLE_VALUE            # noqa: E402
import l3_boundary_gen as gen                          # noqa: E402

POWERS = {1 << k: k for k in range(1, 129)}


def progress(m):
    sys.stdout.write(m + "\n")
    sys.stdout.flush()


def exact(op, a, b):
    if op == "+":
        return a + b
    if op == "-":
        return a - b
    if op == "*":
        return a * b
    return None


def wall_of(op, lo, hi, f, vary_lhs):
    """The wall the boundary sits on, in result space.

    Returns (result below, result at, wall, how many powers of two the
    interval holds).  A wall is only pinned when the interval holds
    exactly one of them; a wider interval names the largest and says
    how many it had to choose between.
    """
    if op not in ("+", "-", "*"):
        return None, None, None, 0
    a1, b1 = (lo, f) if vary_lhs else (f, lo)
    a2, b2 = (hi, f) if vary_lhs else (f, hi)
    r1, r2 = exact(op, a1, b1), exact(op, a2, b2)
    if r1 is None or r2 is None:
        return None, None, None, 0
    lo_r, hi_r = min(r1, r2), max(r1, r2)
    if lo_r < 0 <= hi_r:
        return str(r1), str(r2), "0 (the unsigned floor)", 1
    inside = [k for p, k in POWERS.items() if lo_r < p <= hi_r]
    if inside:
        return str(r1), str(r2), "2^%d" % max(inside), len(inside)
    return str(r1), str(r2), None, 0


# how much room a holder has for a value from the axis.  where a
# boundary sits at or above this, what changed is that the HOLDER ran
# out of room, not that the operation changed its mind.
HOLDER_CAP = {
    ("cpp", "int32_t"): 1 << 31, ("go", "int32"): 1 << 31,
    ("rust", "i32"): 1 << 31, ("csharp", "int"): 1 << 31,
    ("csharp", "short"): 1 << 15, ("java", "int"): 1 << 31,
    ("java", "Integer"): 1 << 31, ("java", "short"): 1 << 15,
    ("kotlin", "Int"): 1 << 31, ("typescript", "number"): 1 << 53,
    ("dart", "int"): 1 << 63, ("dart", "double (whole number)"): 1 << 53,
    ("java", "long"): 1 << 63, ("java", "Long"): 1 << 63,
    ("kotlin", "Long"): 1 << 63, ("csharp", "long"): 1 << 63,
    ("go", "int64"): 1 << 63, ("go", "int"): 1 << 63,
    ("rust", "i64"): 1 << 63, ("cpp", "int64_t"): 1 << 63,
    ("php", "int"): 1 << 63, ("python", "ctypes.c_int64"): 1 << 63,
    ("go", "uint64"): 1 << 64, ("rust", "u64"): 1 << 64,
    ("cpp", "uint64_t"): 1 << 64, ("csharp", "ulong"): 1 << 64,
    ("kotlin", "ULong"): 1 << 64,
}


def capacity(lang, holder, b):
    cap = HOLDER_CAP.get((lang, holder))
    return bool(cap) and b >= cap


def operand_shape(b):
    """Where the boundary sits on the operand axis itself."""
    for p, k in POWERS.items():
        if b == p:
            return "2^%d" % k
        if b == p + 1:
            return "2^%d + 1" % k
        if b == p - 1:
            return "2^%d - 1" % k
    if b in (0, 1, 2):
        return str(b)
    return None


def main():
    tg = json.load(open(os.path.join(HERE, "boundary_targets.json")))
    forms = {}
    d, forms, decls, pres = gen.load()
    keep, defer = gen.phase_a(d, forms)
    by_tid = {r["tid"]: r for r in keep}
    for n, r in enumerate(tg["rows"]):
        r["tid"] = n
    os.makedirs(RAW, exist_ok=True)
    per = {}
    allrows = []
    langs = sorted(set(r["language"] for r in keep))
    for lang in langs:
        p = os.path.join(OUT, "bnd_%s.out" % lang)
        if not os.path.exists(p):
            progress("  %-11s MISSING lane output" % lang)
            continue
        text = open(p).read()
        open(os.path.join(RAW, "bnd_%s.out" % lang), "w").write(text)
        rows, nomove = [], []
        for line in text.splitlines():
            f = line.split("|")
            if f[0] == "N":
                tid = int(f[1])
                t = by_tid.get(tid)
                if t is None:
                    continue
                nomove.append({
                    "tid": tid, "language": lang,
                    "operation": t["operation"],
                    "lhs_holder": t["lhs_holder"],
                    "rhs_holder": t["rhs_holder"],
                    "fixed_value": t["fixed_value"],
                    "low_class": t["low_class"],
                    "high_class": t["high_class"],
                    "stored_low": t["low_answer"],
                    "stored_high": t["high_answer"],
                    "runtime_both": "|".join(f[2:5]),
                })
                continue
            if f[0] != "B":
                continue
            tid = int(f[1])
            t = by_tid.get(tid)
            if t is None:
                continue
            lo, hi = int(f[2]), int(f[3])
            slo = "|".join(f[4:7])
            shi = "|".join(f[7:10])
            probes = int(f[10])
            other = f[11] if len(f) > 11 else ""
            fx = WHOLE_VALUE[t["fixed_value"]]
            vary_lhs = t["varying_side"] == "lhs"
            r1, r2, wall, npow = wall_of(t["operation"], lo, hi,
                                          fx, vary_lhs)
            rows.append({
                "tid": tid, "language": lang,
                "operation": t["operation"],
                "lhs_holder": t["lhs_holder"],
                "rhs_holder": t["rhs_holder"],
                "varying_side": t["varying_side"],
                "varying_holder": t["vary_holder"],
                "fixed_holder": t["fixed_holder"],
                "fixed_value": t["fixed_value"],
                "fixed_number": str(fx),
                "sample_low": t["low_value"],
                "sample_high": t["high_value"],
                "last_of_low_class": str(lo),
                "boundary": str(hi),
                "answer_below": slo,
                "answer_at_and_above": shi,
                "other_classes_seen": other,
                "probes": probes,
                "result_below": r1,
                "result_at": r2,
                "wall": wall,
                "powers_in_interval": npow,
                "operand_shape": operand_shape(hi),
                "holder_ran_out": capacity(lang, t["vary_holder"], hi),
                "stored_low_answer": t["low_answer"],
                "stored_high_answer": t["high_answer"],
            })
        per[lang] = {"located": len(rows), "no_move_at_runtime": len(nomove),
                     "targets": sum(1 for t in keep if t["language"] == lang)}
        json.dump({"kind": "boundaries", "language": lang,
                   "located": len(rows), "no_move_at_runtime": len(nomove),
                   "rows": rows, "no_move": nomove},
                  open(os.path.join(HERE, "boundaries_%s.json" % lang), "w"),
                  indent=1)
        allrows += rows
        progress("  %-11s %5d located  %4d no-move  -> boundaries_%s.json"
                 % (lang, len(rows), len(nomove), lang))
    json.dump({"kind": "boundaries_index", "per_language": per,
               "located_total": len(allrows),
               "deferred": len(defer)},
              open(os.path.join(HERE, "boundaries_index.json"), "w"), indent=1)
    progress("located total: %d" % len(allrows))
    return allrows, per, defer, tg


if __name__ == "__main__":
    main()
