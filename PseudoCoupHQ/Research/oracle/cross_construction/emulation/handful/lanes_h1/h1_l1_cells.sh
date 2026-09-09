#!/usr/bin/env bash
# h1_l1_cells.sh -- task h1, step 0: find the brief's ten cells in the
# arch-opcode model table and write them, and nothing else, to a small
# json the run lane reads.
#
# WHY A LANE OF ITS OWN: `model_table.json` is 73 MB of json and the
# whole of it has to be parsed to pick ten rows out of it. The law
# requires the memory bound stated and sampled first, so this lane
# prints its own peak resident size before anything heavier runs.
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_H1, checked
# after the parse. The task's whole bound is the same 4 GB.
set -euo pipefail
echo "[1/2] task h1: the ten cells, out of model_table.json"
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
python3 - <<'PY'
import json
import os
import resource
import sys

MODEL = ("/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/"
         "model_table.json")
ABORT_KB = 4 * 1024 * 1024


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check(where):
    peak = peak_kb()
    if peak > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_H1: %d kB at %s" % (peak, where))
    return peak


WANTED = [
    ("add", "gpr_gpr", 32),
    ("sub", "imm_gpr", 64),
    ("imul", "gpr_gpr", 32),
    ("sar", "cl_gpr", 32),
    ("shr", "cl_gpr", 64),
    ("idiv", "gpr_one", 32),
    ("cmovne", "gpr_gpr", 32),
    ("setne", "gpr_one", 8),
    ("addss", "xmm_xmm", 32),
    ("cvtsi2sd", "gpr_xmm", 64),
]

print("   parsing %s" % MODEL)
document = json.load(open(MODEL))
print("   peak after the parse: %d kB" % check("after the parse"))
rows = document["rows"]
print("   rows in the table: %d" % len(rows))

by_key = {}
for row in rows:
    key = (row["mnem"], row.get("shape"), row.get("key_width"))
    by_key.setdefault(key, []).append(row)

out = []
for key in WANTED:
    held = by_key.get(key) or []
    translated = [r for r in held if r.get("outcome") == "TRANSLATED"]
    print("")
    print("   CELL %s %s %s: %d row(s) at this key, %d TRANSLATED"
          % (key[0], key[1], key[2], len(held), len(translated)))
    for row in held:
        print("      row_id %s width %s outcome %s flags_in %s "
              "preseeded %s places %s"
              % (row["row_id"], row.get("width"), row.get("outcome"),
                 (row.get("flags_in") or {}).get("mnem"),
                 row.get("preseeded"),
                 [p["writes"] for p in (row.get("mapping") or [])]))
        attestation = row.get("attestation") or {}
        if attestation:
            print("         attestation: units %s ledger_rows %s setter %s"
                  % (attestation.get("units"),
                     attestation.get("ledger_rows"),
                     json.dumps(attestation.get("setter"))))
    out.append({"asked": {"mnem": key[0], "shape": key[1],
                          "key_width": key[2]},
                "rows": held})

# every row of the same mnemonic, so a cell absent at the asked key can
# be replaced by the nearest attested cell of that mnemonic.
neighbours = {}
for key in WANTED:
    same = []
    for row in rows:
        if row["mnem"] != key[0]:
            continue
        if row.get("outcome") != "TRANSLATED":
            continue
        attestation = row.get("attestation") or {}
        if not attestation.get("units"):
            continue
        same.append({"row_id": row["row_id"], "shape": row.get("shape"),
                     "width": row.get("width"),
                     "key_width": row.get("key_width"),
                     "units": attestation.get("units")})
    neighbours[key[0]] = same

print("")
print("   attested TRANSLATED cells per mnemonic asked for:")
for mnem in sorted(neighbours):
    seen = sorted(set((r["shape"], r["key_width"]) for r in neighbours[mnem]))
    print("      %-10s %s" % (mnem, seen))

# the flag setters the two consumer cells record, with the setter's own
# rows, so the pair can be composed.
setters = set()
for record in out:
    for row in record["rows"]:
        for entry in ((row.get("attestation") or {}).get("setter") or []):
            if isinstance(entry, dict):
                setters.add(entry.get("mnem"))
            else:
                setters.add(entry)
        held = (row.get("flags_in") or {}).get("mnem")
        if held is not None:
            setters.add(held)
setters.discard(None)
print("")
print("   the setters these cells name: %s" % sorted(setters))

setter_rows = []
for row in rows:
    if row["mnem"] not in setters:
        continue
    if row.get("outcome") != "TRANSLATED":
        continue
    if not row.get("writes_the_flags"):
        continue
    setter_rows.append(row)
print("   TRANSLATED flag-writing rows of those setters: %d"
      % len(setter_rows))
for row in setter_rows:
    if row.get("shape") not in ("gpr_gpr", "gpr_one", "imm_gpr"):
        continue
    print("      %s %s %s width %s key_width %s places %s"
          % (row["row_id"], row["mnem"], row.get("shape"),
             row.get("width"), row.get("key_width"),
             [p["writes"] for p in (row.get("mapping") or [])]))

document = None
rows = None
by_key = None
handle = open("handful_cells.json", "w")
json.dump({"meta": {"source": MODEL,
                    "what": "the ten cells the task h1 brief names, "
                            "each with every model-table row at its "
                            "(mnem, shape, key_width), plus every "
                            "TRANSLATED flag-writing row of the "
                            "setters those cells record"},
           "asked": out,
           "setter_rows": setter_rows,
           "attested_cells_per_mnem": neighbours},
          handle, indent=1, sort_keys=True)
handle.close()
print("")
print("   wrote handful_cells.json")
print("   peak resident: %d kB" % check("at the end"))
PY
echo "[2/2] done"
