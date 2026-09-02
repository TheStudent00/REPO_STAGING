#!/usr/bin/env python3
"""l3_matrix_read.py -- fold the value-matrix shards.

Reads raw/vm_<lang>_<shard>.txt and writes valuematrix_<lang>.json.

It carries the same COMPLETENESS GATE the rest of phase 3 carries, in
the same shape: expected probes from matrix_plan.json, a required
`__SUMMARY__` line PER SHARD, and `complete` / `completeness` fields
written into the result file.  A lane's exit code is not evidence that
it finished.

The stored grain is chosen so the file answers ruling 3's question
without carrying a row that says nothing.  For every (operation, lhs
holder, rhs holder) it records:

  * `uniform` -- one verdict across the whole value cross product, and
    which verdict it is; this is the case the acceptance run assumed
  * `split`   -- more than one verdict, with EVERY value-class pair
    that differs from the acceptance run's verdict listed in full

A split is the finding: it would mean a statically checked language's
verdict is not a function of the holder pair alone.  Every probe stays
in raw/ either way.
"""

import json
import os
import sys
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
sys.path.insert(0, HERE)
from progress import Progress          # noqa: E402
from l3_read import ROUTE              # noqa: E402


def read(lang, plan):
    files = sorted(f for f in os.listdir(RAW)
                   if f.startswith("vm_%s_" % lang) and f.endswith(".txt"))
    if not files:
        return None
    space = json.load(open(os.path.join(HERE, "space_%s.json" % lang)))
    hs, ops = space["holders"], space["operations"]
    vclass = [h["value_classes"] for h in hs]
    cells = defaultdict(dict)
    summaries, rows = [], 0
    for fn in files:
        lines = open(os.path.join(RAW, fn), errors="replace").read().splitlines()
        pg = Progress(len(lines), "vm:%s:%s" % (lang, fn), every=50000)
        for line in lines:
            pg.tick()
            if line.startswith("__SUMMARY__"):
                summaries.append(line.split("|")[1:])
                continue
            p = line.split("|", 2)
            if len(p) < 2 or not p[0].startswith("P"):
                continue
            try:
                i, j, x, y, k = (int(v) for v in p[0][1:].split("_"))
            except ValueError:
                continue
            if i >= len(hs) or j >= len(hs) or k >= len(ops):
                continue
            cells["%s|%d|%d" % (ops[k], i, j)][(x, y)] = p[1]
            rows += 1
        pg.close()

    base = None
    bp = os.path.join(HERE, "acceptance_%s_%s.json"
                      % (lang, ROUTE.get(lang, "A2")))
    if os.path.exists(bp):
        base = json.load(open(bp))

    uniform, split, out_cells = 0, 0, {}
    for key, tab in cells.items():
        vs = set(tab.values())
        # split from the RIGHT.  The key is "<operation>|<i>|<j>" and one
        # operation in most menus is a bare `|`, so a left split tears
        # the key of every `|` and `||` cell apart -- the same fault
        # log_027 5.1 finding 11 measured on the reading side, in a
        # different file.
        op, i, j = key.rsplit("|", 2)
        i, j = int(i), int(j)
        rec = dict(operation=op,
                   lhs=dict(form=hs[i]["form"], holder=hs[i]["rep"]),
                   rhs=dict(form=hs[j]["form"], holder=hs[j]["rep"]),
                   probes=len(tab))
        if len(vs) == 1:
            uniform += 1
            rec["shape"] = "uniform"
            rec["verdict"] = next(iter(vs))
        else:
            split += 1
            rec["shape"] = "split"
            rec["verdicts"] = sorted(vs)
            rec["by_value_class"] = [
                dict(lhs_value_class=vclass[i][x], rhs_value_class=vclass[j][y],
                     verdict=v) for (x, y), v in sorted(tab.items())]
        if base:
            b = base["cells"].get(key)
            rec["acceptance_run_verdict"] = b["verdict"] if b else None
        out_cells[key] = rec

    expect = 0
    for p in plan.get("plan", []):
        if p["language"] == lang:
            expect = p["probes"]
            shards = p["shards"]
            break
    else:
        shards = len(files)
    complete = (rows == expect) and (len(summaries) == shards)
    note = "COMPLETE" if complete else (
        "TRUNCATED -- %d of %d probes over %d of %d shard summary lines; "
        "do not read as a measurement" % (rows, expect, len(summaries), shards))
    if not complete:
        print("  !! %s value matrix INCOMPLETE: %s" % (lang, note))
    res = dict(language=lang, route=ROUTE.get(lang, "?") + " value matrix",
               grain="(operation, lhs holder, rhs holder) x full value "
                     "cross product",
               probes=rows, expected_probes=expect,
               shards_present=len(files), shards_expected=shards,
               shard_summaries=summaries,
               pair_cells=len(out_cells),
               uniform_cells=uniform, split_cells=split,
               complete=complete, completeness=note,
               cells=out_cells)
    json.dump(res, open(os.path.join(HERE, "valuematrix_%s.json" % lang), "w"))
    print("| %s | %d | %d | %d | %d | %s |"
          % (lang, rows, len(out_cells), uniform, split,
             "COMPLETE" if complete else "INCOMPLETE"))
    return res


def main():
    plan = json.load(open(os.path.join(HERE, "matrix_plan.json")))
    print("| language | probes folded | pair cells | uniform | split | gate |")
    print("|---|---|---|---|---|---|")
    idx = {}
    for p in plan["plan"]:
        r = read(p["language"], plan)
        if r:
            idx[p["language"]] = dict(probes=r["probes"],
                                      expected=r["expected_probes"],
                                      uniform=r["uniform_cells"],
                                      split=r["split_cells"],
                                      complete=r["complete"])
    json.dump(idx, open(os.path.join(HERE, "valuematrix_index.json"), "w"),
              indent=1)


if __name__ == "__main__":
    main()
