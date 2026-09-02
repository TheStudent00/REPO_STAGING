#!/usr/bin/env python3
"""l3_boundary_report.py -- write boundaries.md from the folded
per-language boundary files.  Tables are pipe tables; raw blocks are
kept near fifty-five characters wide."""

import collections
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def load():
    rows, nomove = [], []
    for f in sorted(glob.glob(os.path.join(HERE, "boundaries_*.json"))):
        if "index" in f:
            continue
        d = json.load(open(f))
        rows += d["rows"]
        nomove += d["no_move"]
    return rows, nomove


def table(head, lines):
    out = ["| " + " | ".join(head) + " |",
           "|" + "|".join(["---"] * len(head)) + "|"]
    for l in lines:
        out.append("| " + " | ".join(str(x) for x in l) + " |")
    return "\n".join(out)


def main():
    rows, nomove = load()
    idx = json.load(open(os.path.join(HERE, "boundaries_index.json")))
    tg = json.load(open(os.path.join(HERE, "boundary_targets.json")))
    out = []
    A = out.append

    A("# boundaries.md — where each language changes its mind")
    A("")
    A("Written 2026-08-20 with log 042.  Every number here is a value "
      "a run printed, or arithmetic over such values.  A **boundary** "
      "is the least value of one operand at which an operation stops "
      "answering in one class and starts answering in another.  The "
      "class is outcome plus result type plus fidelity, where "
      "fidelity asks only whether the answer equals the exact "
      "mathematical result.")
    A("")
    A("The axis is the whole-number value axis of the value matrix:")
    A("")
    A("```")
    A("0  <  42  <  2^53+1  <  2^63-1  <  2^63  <  2^64-1")
    A("```")
    A("")

    A("## the run")
    A("")
    langs = sorted(set(r["language"] for r in rows))
    lines = []
    for l in langs:
        rr = [r for r in rows if r["language"] == l]
        nm = [r for r in nomove if r["language"] == l]
        pr = sum(r["probes"] for r in rr)
        lines.append([l, idx["per_language"][l]["targets"], len(rr),
                      len(nm), pr,
                      max(r["probes"] for r in rr) if rr else 0])
    lines.append(["ALL", sum(x[1] for x in lines), sum(x[2] for x in lines),
                  sum(x[3] for x in lines), sum(x[4] for x in lines),
                  max(x[5] for x in lines)])
    A(table(["language", "targets", "located", "no move", "probes",
             "worst probes"], lines))
    A("")
    A("`no move' means the two ends of the span answered in the SAME "
      "class at run time, so the stored disagreement did not survive "
      "re-measurement.  Those are named in §the disagreements.")
    A("")

    A("## the walls, in result space")
    A("")
    A("For `+', `-' and `*' the boundary in operand space is dull and "
      "the boundary in RESULT space is the wall.  A wall is counted "
      "here only where exactly one power of two lies in the span the "
      "bisection closed on, and only where the holder itself had room "
      "for the value.")
    A("")
    c = collections.Counter()
    for r in rows:
        if r["wall"] and r["powers_in_interval"] == 1 and \
                not r["holder_ran_out"]:
            c[(r["language"], r["varying_holder"], r["wall"])] += 1
    byl = collections.defaultdict(list)
    for (l, h, w), n in sorted(c.items()):
        byl[l].append((h, w, n))
    lines = []
    for l in sorted(byl):
        for h, w, n in byl[l]:
            lines.append([l, "`%s`" % h, w, n])
    A(table(["language", "varying holder", "wall", "boundaries"], lines))
    A("")

    A("## the erosion at 2^53")
    A("")
    A("A boundary that sits at 2^53 + 1 on the operand axis is a "
      "float-mantissa boundary: the value stops being representable "
      "and the answer stops agreeing with exact arithmetic.")
    A("")
    c = collections.Counter()
    for r in rows:
        if r["operand_shape"] == "2^53 + 1":
            c[(r["language"], r["operation"],
               r["varying_holder"], r["fixed_holder"])] += 1
    lines = [[l, "`%s`" % op, "`%s`" % vh, "`%s`" % fh, n]
             for (l, op, vh, fh), n in sorted(c.items())]
    A(table(["language", "operation", "varying holder", "other holder",
             "boundaries"], lines))
    A("")

    A("## the shift boundaries")
    A("")
    c = collections.Counter()
    for r in rows:
        if r["operation"] in ("<<", ">>"):
            c[(r["language"], r["operation"], r["varying_holder"],
               r["fixed_holder"], r["boundary"],
               r["answer_at_and_above"].split("|")[0])] += 1
    lines = [[l, "`%s`" % op, "`%s`" % vh, "`%s`" % fh, b, k, n]
             for (l, op, vh, fh, b, k), n in sorted(c.items())]
    A(table(["language", "operation", "varying holder", "other holder",
             "boundary", "becomes", "cells"], lines))
    A("")

    A("## the boundary at one")
    A("")
    A("Two hundred and more boundaries sit at the value 1.  They are "
      "not walls.  They are the divisor leaving zero, and the "
      "truthiness of zero.")
    A("")
    c = collections.Counter()
    for r in rows:
        if r["boundary"] == "1":
            c[(r["language"], r["operation"])] += 1
    lines = [[l, "`%s`" % op, n] for (l, op), n in sorted(c.items())]
    A(table(["language", "operation", "cells"], lines))
    A("")

    A("## where the holder ran out first")
    A("")
    A("Some boundaries are not the operation changing its mind but "
      "the holder ceasing to hold the axis value.  They are counted "
      "apart so they cannot be read as arithmetic.")
    A("")
    c = collections.Counter((r["language"], r["varying_holder"],
                             r["operand_shape"] or "-")
                            for r in rows if r["holder_ran_out"])
    lines = [[l, "`%s`" % h, s or "—", n] for (l, h, s), n in sorted(c.items())]
    A(table(["language", "holder", "boundary shape", "cells"], lines))
    A("")

    A("## the disagreements")
    A("")
    A("Where the stored answer and the re-measured run part company, "
      "the parting is written down rather than smoothed.")
    A("")
    c = collections.Counter((r["language"], r["operation"],
                             r["lhs_holder"], r["rhs_holder"])
                            for r in nomove)
    lines = [[l, "`%s`" % op, "`%s`" % a, "`%s`" % b, n]
             for (l, op, a, b), n in sorted(c.items())]
    A(table(["language", "operation", "lhs holder", "rhs holder", "cells"],
            lines))
    A("")

    A("## what was not run")
    A("")
    dl = collections.Counter()
    d = json.load(open(os.path.join(HERE, "boundary_targets.json")))
    import l3_boundary_gen as gen
    dd, forms, decls, pres = gen.load()
    keep, defer = gen.phase_a(dd, forms)
    for r in defer:
        dl[r["deferred"]] += 1
    A(table(["reason", "targets"],
            [[k, v] for k, v in sorted(dl.items(), key=lambda x: -x[1])]))
    A("")
    A("Beside those, %d target pairs needed no run at all: their two "
      "samples are adjacent integers, so the boundary is already "
      "exact in the stored answers." % tg["already_exact"])
    A("")

    p = os.path.join(HERE, "boundaries.md")
    open(p, "w").write("\n".join(out) + "\n")
    print("wrote %s" % p)


if __name__ == "__main__":
    main()
