#!/usr/bin/env python3
"""l3_read.py -- fold lane output into the phase-3 result files.

Reads raw/ac_<lang>.txt (acceptance routes A1/A2) and raw/rc_<lang>.txt
(route C) and writes, per CORE_0_3_2 phase 3 point 6:

  acceptance_<lang>_<route>.json   verdict per (operation, lhs holder,
                                   rhs holder), every row carrying
                                   (form, holder, value class)
  behavior_<lang>_C.json           answer per (operation, form, holder,
                                   value class) -- route C only, since
                                   only execution yields an ANSWER

Overlap cells keep BOTH routes' verdicts.  Disagreements are recorded
as findings and are never reconciled silently (ruling 5, overlap
discipline).
"""

import json
import os
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
sys.path.insert(0, HERE)
from progress import Progress          # noqa: E402

ROUTE = dict(go="A2", rust="A2", cpp="A2", swift="A2", dart="A2",
             csharp="A1", kotlin="A1", java="A1", typescript="A1")


def read_acceptance(lang):
    p = os.path.join(RAW, "ac_%s.txt" % lang)
    if not os.path.exists(p):
        return None
    space = json.load(open(os.path.join(HERE, "space_%s.json" % lang)))
    hs = space["holders"]
    ops = space["operations"]
    rows = {}
    summary = None
    lines = open(p, errors="replace").read().splitlines()
    pg = Progress(len(lines), "read:%s" % lang, every=5000)
    for line in lines:
        pg.tick()
        if line.startswith("__SUMMARY__"):
            summary = line.split("|")[1:]
            continue
        parts = line.split("|", 2)
        if len(parts) < 2 or not parts[0].startswith("P"):
            continue
        try:
            i, j, k = (int(x) for x in parts[0][1:].split("_"))
        except ValueError:
            continue
        if i >= len(hs) or j >= len(hs) or k >= len(ops):
            continue
        rows["%s|%d|%d" % (ops[k], i, j)] = dict(
            operation=ops[k],
            lhs=dict(form=hs[i]["form"], holder=hs[i]["rep"]),
            rhs=dict(form=hs[j]["form"], holder=hs[j]["rep"]),
            verdict=parts[1],
            detail=(parts[2] if len(parts) > 2 else "")[:160])
    pg.close()
    acc = sum(1 for r in rows.values() if r["verdict"] == "ACCEPT")
    # COMPLETENESS GATE.  A lane can die mid-run and still exit 0 -- it
    # happened three times on 2026-08-18 (rust EBUSY, php class
    # redeclare fatal, python OOM kill).  A truncated file must never
    # be read as a measurement, so say so here, loudly and in the file.
    expect = len(hs) * len(hs) * len(ops)
    complete = (len(rows) == expect) and (summary is not None)
    out = dict(language=lang, route=ROUTE.get(lang, "?"),
               grain="(operation, lhs holder, rhs holder)",
               holders=hs, operations=ops,
               probes=len(rows), expected_probes=expect,
               complete=complete,
               completeness="COMPLETE" if complete else
               "TRUNCATED -- %d of %d probes%s; do not read as a "
               "measurement" % (len(rows), expect,
                                "" if summary else
                                ", and the lane wrote no summary line"),
               accept=acc, refuse=len(rows) - acc,
               lane_summary=summary, cells=rows)
    if not complete:
        print("  !! %s acceptance INCOMPLETE: %d of %d probes, summary=%s"
              % (lang, len(rows), expect, bool(summary)))
    json.dump(out, open(os.path.join(
        HERE, "acceptance_%s_%s.json" % (lang, ROUTE.get(lang, "X"))), "w"))
    return out


def read_routec(lang):
    p = os.path.join(RAW, "rc_%s.txt" % lang)
    if not os.path.exists(p):
        return None
    cells = {}
    kinds = Counter()
    summary = None
    lines = open(p, errors="replace").read().splitlines()
    pg = Progress(len(lines), "read:%s(C)" % lang, every=50000)
    for line in lines:
        pg.tick()
        if line.startswith("__SUMMARY__"):
            summary = line.split("|")[1:]
            continue
        # The probe id ENDS with the operation, and one operation in
        # most menus is a bare "|" -- the same character this format
        # delimits with.  A left split therefore tears the id of every
        # `|` and `||` probe apart.  Measured 2026-08-18: it lost
        # exactly one operation's rows in ruby (11,881) and php
        # (8,281).  So find the VERDICT token instead of counting
        # delimiters: it is the first field that is one of the four
        # words a driver can write.
        f = line.split("|")
        vi = next((n for n, x in enumerate(f)
                   if x in ("ANSWER", "RAISE", "REFUSE", "BUDGET")), None)
        if vi is None or vi == 0:
            continue
        pid = "|".join(f[:vi])
        cells[pid] = (f[vi], "|".join(f[vi + 1:]))
        kinds[f[vi]] += 1
    pg.close()
    # Same gate as acceptance.  Route C's driver writes __SUMMARY__ as
    # its LAST act, so a missing summary line means the run died.
    complete = summary is not None
    note = "COMPLETE"
    if not complete:
        note = ("TRUNCATED -- the lane wrote no summary line, so it died "
                "mid-run; %d probes present; do not read as a measurement"
                % len(cells))
        print("  !! %s route C INCOMPLETE: no summary line, %d probes"
              % (lang, len(cells)))
    out = dict(language=lang, route="C",
               grain="(operation, form, holder, value class)",
               probes=len(cells), kinds=dict(kinds),
               complete=complete, completeness=note,
               lane_summary=summary, cells=cells)
    json.dump(out, open(os.path.join(HERE, "behavior_%s_C.json" % lang), "w"))
    return out


def main():
    idx = {}
    for lang in ROUTE:
        r = read_acceptance(lang)
        if r:
            idx[lang] = dict(route=r["route"], probes=r["probes"],
                             accept=r["accept"], refuse=r["refuse"])
    for lang in ("python", "ruby", "php"):
        r = read_routec(lang)
        if r:
            idx[lang] = dict(route="C", probes=r["probes"], kinds=r["kinds"])
    json.dump(idx, open(os.path.join(HERE, "phase3_index.json"), "w"), indent=1)
    print("\n| language | route | probes | accept | refuse |")
    print("|---|---|---|---|---|")
    for lang, d in idx.items():
        if d["route"] == "C":
            k = d["kinds"]
            print("| %s | C | %d | answers %d | raises %d, refusals %d |"
                  % (lang, d["probes"], k.get("ANSWER", 0),
                     k.get("RAISE", 0), k.get("REFUSE", 0)))
        else:
            print("| %s | %s | %d | %d | %d |"
                  % (lang, d["route"], d["probes"], d["accept"], d["refuse"]))


if __name__ == "__main__":
    main()
