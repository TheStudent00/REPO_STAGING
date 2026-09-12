#!/usr/bin/env python3
"""verify_blockers.py -- prints the top-3-of-10 blocking cells for every
(source, target) pair, one line each, no arrows, matching log_266
Tables 5-7. Read-only."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def cellstr(c):
    return "%s/%s/%d" % (c["mnem"], c["shape"], c["key_width"])


def show(path, readings, xs, ys):
    d = json.load(open(os.path.join(HERE, path)))
    for reading in readings:
        blk = d["blocking_cells_top10"][reading]
        for x in xs:
            for y in ys:
                top = blk[x][y][:3]
                if not top:
                    s = "none"
                else:
                    s = ";".join("%s(%d)" % (cellstr(t["cell"]),
                                              t["blocked_units"])
                                 for t in top)
                print("%s source=%s target=%s top3=%s" % (reading, x, y, s))


show("coverage_x86.json", ["destination_only", "strict"],
     ["c", "cpp", "go", "rust", "swift"],
     ["c", "cpp", "go", "rust", "swift"])
show("coverage_riscv64.json", ["destination_only"],
     ["c", "go"], ["c", "cpp", "go", "rust"])
