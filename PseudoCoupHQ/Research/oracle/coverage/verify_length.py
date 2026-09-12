#!/usr/bin/env python3
"""verify_length.py -- prints the diagonal (x==y) length-view buckets for
both architectures and both readings, matching log_266 Tables 8-10.
Read-only."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
BUCKETS = ["1", "2", "3-5", "6-10", "over-10"]


def show(path, readings, xs):
    d = json.load(open(os.path.join(HERE, path)))
    for reading in readings:
        lv = d["length_view"][reading]
        for x in xs:
            row = lv[x].get(x, {})
            parts = []
            for b in BUCKETS:
                if b in row:
                    parts.append("%s=%d/%d" % (b, row[b]["n"], row[b]["m"]))
            print("%s source=%s %s" % (reading, x, " ".join(parts)))


show("coverage_x86.json", ["destination_only", "strict"],
     ["c", "cpp", "rust", "go", "swift"])
show("coverage_riscv64.json", ["destination_only", "strict"], ["c", "go"])
