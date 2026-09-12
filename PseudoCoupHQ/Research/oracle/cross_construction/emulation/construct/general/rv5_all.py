#!/usr/bin/env python3
"""rv5: task t4's RISC-V driver at SHIP flags, unchanged, over EVERY RISC-V
cell (the owner, 2026-09-12: "i want all of them backstopped since the
computational complexity is exceptionally low") — not only the untwinned
ones. Both policies as rv_general runs them: native-first and
all-constructed (the backstop proper).
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import rv_general as RG                                          # noqa: E402

RV_DIR = os.path.dirname(os.path.abspath(sys.argv[5]))
sys.path.insert(0, RV_DIR)
import rv_loop as RL                                             # noqa: E402

def every_cell(twins_path):
    out = []
    for row in json.load(open(twins_path))["rows"]:
        out.append({"mnem": row["mnem"], "shape": row["shape"],
                    "key_width": row["key_width"],
                    "places": [p["writes"] for p in row["places"]]})
    return out

RL.untwinned = every_cell
print("rv5: the population is EVERY RISC-V cell of twins.json", flush=True)

if __name__ == "__main__":
    sys.exit(RG.main())
