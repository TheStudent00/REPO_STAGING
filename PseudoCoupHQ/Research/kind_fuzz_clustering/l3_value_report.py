#!/usr/bin/env python3
"""l3_value_report.py -- the two written tables, at the value grain.

Writes `truthiness_table.md` and `trace_compare.md` over again, now
with the nine checked languages measured at the VALUE grain beside the
three open ones that always were.

The point of the rewrite is one sentence.  Log 037's table read a `T`
for the truth form in all twelve languages.  That `T` was an artifact
of the base value class: the condition slot was only ever handed one
truth value.  At the value grain the same slot is handed `true` AND
`false`, and every language that has a truth form splits.  A cell that
splits is the truthiness finding, and the holder grain could not see
it.
"""

import collections
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
RAW = os.path.join(HERE, "raw")

from l3_accept import holders                               # noqa: E402

FORMS = ["nothing", "truth", "whole", "fractional", "text",
         "sequence", "keyed", "nesting"]
SHORT = ["no", "tr", "wh", "fr", "tx", "sq", "ke", "ne"]
ALL12 = ["go", "rust", "cpp", "swift", "dart", "csharp", "kotlin",
         "java", "typescript", "python", "ruby", "php"]
NINE = ["go", "rust", "cpp", "swift", "dart", "csharp", "kotlin",
        "java", "typescript"]
OPEN3 = ["python", "ruby", "php"]


def code(counter):
    """one letter for a form's condition-slot verdict."""
    if not counter:
        return "-"
    if counter.get("HARNESS") and len(counter) == 1:
        return "H"
    t, e = counter.get("then", 0), counter.get("else", 0)
    r = counter.get("REFUSE", 0)
    if r and not t and not e:
        return "R"
    if r and (t or e):
        return "p"
    if t and e:
        return "S"
    if t:
        return "T"
    if e:
        return "E"
    if counter.get("RAISE"):
        return "X"
    return "?"


def load():
    v = {}
    p = os.path.join(HERE, "truthiness_value.json")
    if os.path.exists(p):
        v = json.load(open(p))
    h = {}
    # the HOLDER-grain baseline of log 037.  `truthiness.json` is
    # rewritten by l3_construct_read.py at whatever grain its LANES
    # table currently names, and that is now the VALUE grain for the
    # nine, so reading it here would compare a run against itself and
    # print no movement at all.  `truthiness_holder037.json` is log
    # 037's file, frozen, and is what movement must be measured
    # against.  (This cost log 038 one wrong table.)
    for name in ("truthiness_holder037.json", "truthiness.json"):
        p = os.path.join(HERE, name)
        if os.path.exists(p):
            h = json.load(open(p))
            break
    return v, h


def row(tab, lang):
    d = tab.get(lang) or {}
    return [code(collections.Counter(d.get(f) or {})) for f in FORMS]


def block(lines, width=55):
    return [l[:width] for l in lines]


def write_truthiness():
    val, hol = load()
    L = []
    A = L.append
    A("# truthiness_table.md")
    A("")
    A("The if-condition slot takes ONE operand. Run over every holder")
    A("and every value class, that single slot IS the cross-language")
    A("truthiness table. It is a one-operand table, so it is an")
    A("eight-form vector per language and never a sixty-four cell")
    A("grid.")
    A("")
    A("Rewritten 2026-08-19 with log 038, when the nine checked")
    A("languages reached the value grain. Read the WORDS below before")
    A("the letters.")
    A("")
    A("## the words used here")
    A("")
    A("```")
    A("form")
    A("    the layer-1 name for a kind of value.")
    A("    there are eight of them.")
    A("holder grain")
    A("    every holder at ONE value, its base.")
    A("    log 037 measured the nine this way.")
    A("value grain")
    A("    every holder at EVERY value class.")
    A("    log 038 measures the nine this way.")
    A("splits")
    A("    the same slot sent some values to the")
    A("    then arm and some to the else arm.")
    A("```")
    A("")
    A("## how to read a letter")
    A("")
    A("```")
    A("T   always then")
    A("E   always else")
    A("S   splits: some values then, some else")
    A("R   refused: the checker would not take")
    A("    a value of that form in a condition")
    A("p   part refused: some holders of that")
    A("    form accepted, some not")
    A("X   raised at every value")
    A("H   the recorder refused, not the")
    A("    language")
    A("-   not probed")
    A("```")
    A("")
    A("## the table, at the VALUE grain")
    A("")
    A("Columns are the first two letters of the eight forms.")
    A("")
    pend = [l for l in NINE if not os.path.exists(
        os.path.join(RAW, "vb_%s.txt" % l))]
    if pend:
        A("NOT YET AT THE VALUE GRAIN: " + ", ".join(pend) + ".")
        A("Those rows are log 037's HOLDER-grain letters, carried")
        A("forward unchanged, and a `T` in them means accepted at one")
        A("value and NOT proved uniform over its values. They are")
        A("marked again in the movement block below, where they are")
        A("simply absent.")
        A("")
    A("```")
    A("            " + " ".join(SHORT))
    for lang in ALL12:
        src = val if lang in val else hol
        A("%-11s " % lang + "  ".join(row(src, lang)))
    A("```")
    A("")
    A("## what MOVED from the holder grain")
    A("")
    A("The nine checked languages only. The three open ones were")
    A("always at the value grain and cannot move.")
    A("")
    A("```")
    A("            " + " ".join(SHORT))
    for lang in NINE:
        if lang not in val:
            continue
        h = row(hol, lang)
        v = row(val, lang)
        mark = ["%s>%s" % (a, b) if a != b else " . " for a, b in zip(h, v)]
        A("%-11s " % lang + " ".join(m if len(m) == 3 else m.center(3)
                                     for m in mark))
    A("```")
    A("")
    A("A cell reading `.` did not move. A cell reading `T>S` read")
    A("always-then at the holder grain and splits at the value grain.")
    A("")
    open(os.path.join(HERE, "truthiness_table.md"), "w").write(
        "\n".join(L) + "\n")
    return L


# ----------------------------------------------------------------------
def read(path):
    rows = {}
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        if line.startswith("__SUMMARY__"):
            continue
        p = line.split("|", 2)
        if len(p) == 3:
            rows[p[0]] = (p[1], p[2])
    return rows


def steps(payload):
    m = re.match(r"TRACE:(\d+)\[(.*)\]$", payload)
    if not m:
        return None
    return int(m.group(1)), m.group(2)


def write_trace_compare():
    """the flow family's answer, compared across the twelve, now with
    the loop's LENGTH varying with the value rather than fixed."""
    L = []
    A = L.append
    A("# trace_compare.md")
    A("")
    A("A trace is what a flow construct gives back instead of an")
    A("answer: the sequence of values at each joint, written in the")
    A("same bits encoding as an answer. That shared encoding is what")
    A("makes two languages' traces comparable at all.")
    A("")
    A("Rewritten 2026-08-19 with log 038.")
    A("")
    A("## the question this rewrite answers")
    A("")
    A("Log 037 compared traces at ONE value per holder, so every for")
    A("loop it recorded walked the same three whole numbers. The")
    A("question it could not reach was whether a trace depends on the")
    A("VALUE. It does, and the dependence is measured below.")
    A("")
    import l3_construct_read as R
    for lang in ALL12:
        vb = os.path.join(RAW, "vb_%s.txt" % lang)
        if not os.path.exists(vb):
            # the three open languages were always at the value grain
            # and their rows live in the file log 037 wrote, not in a
            # vb file.  read that one instead, so this table is the
            # twelve-language comparison it says it is.
            vb = os.path.join(RAW, R.LANES[lang][0])
        if not os.path.exists(vb):
            continue
        hs, _ = holders(lang)
        rows = read(vb)
        per = collections.defaultdict(list)
        for pid, (ty, payload) in rows.items():
            m = re.match(r"^Kflow\.for_(\d+)_(.+)$", pid)
            if not m:
                continue
            s = steps(payload)
            if s is None:
                continue
            per[int(m.group(1))].append((m.group(2), s[0]))
        if not per:
            continue
        A("## %s -- the for-iterable slot, by value class" % lang)
        A("")
        A("```")
        for i in sorted(per):
            ns = sorted(set(n for _, n in per[i]))
            A("holder %-2d %-11s steps %s"
              % (i, hs[i]["form"], ",".join(str(n) for n in ns[:8])))
        A("```")
        A("")
    open(os.path.join(HERE, "trace_compare.md"), "w").write(
        "\n".join(L) + "\n")
    return L


if __name__ == "__main__":
    write_truthiness()
    write_trace_compare()
    print("wrote truthiness_table.md and trace_compare.md")
