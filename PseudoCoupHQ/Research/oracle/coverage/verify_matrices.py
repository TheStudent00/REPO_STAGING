#!/usr/bin/env python3
"""verify_matrices.py -- prints every cell of every cov1 matrix as one
line each, no arrows, so log_266's table claims carry a one-line
reproducing command. Read-only."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def show(path, readings, xs, ys):
    d = json.load(open(os.path.join(HERE, path)))
    for reading in readings:
        mat = d["matrices"][reading]
        for x in xs:
            for y in ys:
                c = mat[x][y]
                print("%s source=%s target=%s n=%d m=%d"
                      % (reading, x, y, c["n"], c["m"]))


show("coverage_x86.json", ["destination_only", "strict"],
     ["c", "cpp", "rust", "go", "swift"],
     ["c", "cpp", "rust", "go", "swift"])
show("coverage_riscv64.json", ["destination_only", "strict"],
     ["c", "go"], ["c", "cpp", "go", "rust"])
