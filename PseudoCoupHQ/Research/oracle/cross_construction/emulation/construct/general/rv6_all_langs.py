#!/usr/bin/env python3
"""rv6: rv5 (every RISC-V cell, both routes, ship flags) on ALL the compiled
languages the image can aim at riscv64 — c, cpp, go, rust — using rv3's
compile routes (c/cpp with --gcc-toolchain=/usr so <string.h> resolves;
rust with the linux-gnu target). swift has no riscv64 SDK in the image
(swift 6.0.3: "could not find module '_Concurrency' for target
'riscv64-unknown-linux-gnu'") and is a flag, not a row.
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
import inherit as INH                                            # noqa: E402
import inherit_rv3 as INH3                                       # noqa: E402

def every_cell(twins_path):
    return [{"mnem": r["mnem"], "shape": r["shape"], "key_width": r["key_width"],
             "places": [p["writes"] for p in r["places"]]}
            for r in json.load(open(twins_path))["rows"]]

RL.untwinned = every_cell
INH3.install()                                       # rv3's routes and argument sequences: c, cpp, rust, go
RG.TARGETS = ["c", "cpp", "go", "rust"]
print("rv6: every RISC-V cell x %s, rv3's compile routes" % RG.TARGETS, flush=True)

if __name__ == "__main__":
    sys.exit(RG.main())
