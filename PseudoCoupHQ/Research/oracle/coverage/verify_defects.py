#!/usr/bin/env python3
"""verify_defects.py -- reproduces the two named findings of log_266: the
c/cpp identical destination-only coverage, and the riscv64
out-of-population check after the c.nop fix. Read-only."""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def cpp_check():
    d = json.load(open(os.path.join(HERE, "bank_x86.json")))
    cells = d["cells"]
    both_present = 0
    same = 0
    diff = 0
    for entry in cells:
        t = entry["targets"]
        if "c" in t and "cpp" in t:
            both_present = both_present + 1
            if t["c"]["destination_only"] == t["cpp"]["destination_only"]:
                same = same + 1
            else:
                diff = diff + 1
    c_only = sum(1 for e in cells
                 if "c" in e["targets"] and "cpp" not in e["targets"])
    print("both_present=%d same=%d diff=%d c_only_no_cpp=%d"
          % (both_present, same, diff, c_only))


def nop_check():
    riscv_dir = os.path.join(HERE, "..", "riscv")
    population = set()
    for row in json.load(open(os.path.join(riscv_dir, "twins.json")))["rows"]:
        population.add((row["mnem"], row["shape"], row["key_width"]))
    outside = 0
    nop_seen = 0
    for line in open(os.path.join(HERE, "units_riscv64.jsonl")):
        row = json.loads(line)
        for c in row["cells"]:
            key = (c["mnem"], c["shape"], c["key_width"])
            if c["mnem"] == "c.nop":
                nop_seen = nop_seen + 1
            if key not in population:
                outside = outside + 1
    print("cells_outside_255_population=%d nop_cells_seen=%d"
          % (outside, nop_seen))


def never_attempted_x86():
    bank = set()
    for e in json.load(open(os.path.join(HERE, "bank_x86.json")))["cells"]:
        c = e["cell"]
        bank.add((c["mnem"], c["shape"], c["key_width"]))
    seen = {}
    for line in open(os.path.join(HERE, "units_x86.jsonl")):
        row = json.loads(line)
        for c in row["cells"]:
            k = (c["mnem"], c["shape"], c["key_width"])
            if k not in bank:
                seen[k] = seen.get(k, 0) + 1
    print("x86 cells attested with zero bank record for any target: %d"
          % len(seen))
    for k in sorted(seen):
        print("  cell mnem=%s shape=%s key_width=%s units=%d"
              % (k[0], k[1], k[2], seen[k]))


def x86_subset_check():
    attested = set()
    for c in json.load(open(os.path.join(
            HERE, "..", "arch_opcodes", "model",
            "model_table_attest.json")))["cells"]:
        attested.add((c["mnem"], c["shape"], c["key_width"]))
    outside = 0
    for line in open(os.path.join(HERE, "units_x86.jsonl")):
        row = json.loads(line)
        for c in row["cells"]:
            k = (c["mnem"], c["shape"], c["key_width"])
            if k not in attested:
                outside = outside + 1
    print("x86 attested cells=%d cells_outside_attested_population=%d"
          % (len(attested), outside))


cpp_check()
nop_check()
never_attempted_x86()
x86_subset_check()
