#!/usr/bin/env bash
# ap1_l1_cells.sh -- task ap1, step 0: the OUTER SET of the owner's loop, out
# of the arch-opcode model table and into a file the run lane reads.
#
# WHAT THIS LANE PRODUCES, one sentence: `autopoly_cells.json`, the
# same shape task h1's `handful_cells.json` has (an `asked` list, one
# entry per (mnem, operand shape, key_width) triple carrying every
# model-table row at that triple, plus the `setter_rows` a flag-reading
# cell needs to compose its pair), for every ATTESTED cell instead of
# for the ten task h1's brief named.
#
# WHICH CELLS: every distinct (mnem, shape, key_width) triple that has
# at least one row with `outcome == TRANSLATED` and
# `attestation.ledger_rows > 0`. Task m1b measured that set at 253
# (log_237 section 8, "attested cells 257 placed 253 unplaced 4"); this
# lane counts it again from the table itself rather than trusting the
# number.
#
# WHAT IS DROPPED FROM A STORED ROW, and why it is safe: the row's
# `mapping` field, which holds the built term per written place as
# text. `handful.py` never reads it -- `terms_of_row` REBUILDS the
# terms by calling `model_table.places_of_attempt` on the row's own
# `mnem` / `operands` / `preseeded` / `flags_in` / `width`, which is
# the same call task m1b's edges pass makes. Dropping it is what keeps
# this file tens of megabytes rather than gigabytes. The lane prints
# the field list of a stored row so the drop is visible.
#
# MEMORY BOUND: 6 GB resident on this one process, named abort
# ABORT_MEMORY_AP1, checked after the parse and at the end. The heavy
# read is the 73 MB `model_table.json`; task h1's own lane measured its
# parse at 290,040 kB.
set -euo pipefail
echo "[1/2] task ap1: the attested cells, out of model_table.json"
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 - <<'PY'
import json
import os
import resource

MODEL = ("/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/"
         "model_table.json")
ATTEST = ("/projects/PseudoCoupHQ/Research/oracle/arch_opcodes/model/"
          "model_table_attest.json")
ABORT_KB = 6 * 1024 * 1024


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def check(where):
    peak = peak_kb()
    if peak > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_AP1: %d kB at %s" % (peak, where))
    return peak


print("   parsing %s" % MODEL)
document = json.load(open(MODEL))
print("   peak after the parse: %d kB" % check("after the parse"))
rows = document["rows"]
print("   rows in the table: %d" % len(rows))
counts = document["counts"]
print("   the table's own counts: attested_cells %d placed %d"
      % (counts["attested_cells"], counts["attested_cells_placed"]))

sample = rows[0]
print("   a row's own fields: %s" % sorted(sample.keys()))

by_key = {}
for row in rows:
    key = (row["mnem"], row.get("shape"), row.get("key_width"))
    by_key.setdefault(key, []).append(row)
print("   distinct (mnem, shape, key_width) triples in the table: %d"
      % len(by_key))

wanted = []
for key in sorted(by_key):
    ledger = 0
    translated = 0
    for row in by_key[key]:
        if row.get("outcome") != "TRANSLATED":
            continue
        translated = translated + 1
        held = (row.get("attestation") or {}).get("ledger_rows") or 0
        if held > ledger:
            ledger = held
    if translated == 0:
        continue
    if ledger <= 0:
        continue
    wanted.append((ledger, key))
print("   triples with a TRANSLATED row and ledger_rows > 0: %d"
      % len(wanted))

attested = json.load(open(ATTEST))
attested_keys = set()
for cell in attested["cells"]:
    if (cell.get("ledger_rows") or 0) <= 0:
        continue
    attested_keys.add((cell["mnem"], cell["shape"], cell["key_width"]))
print("   task m1's own attested cell list holds %d keys with "
      "ledger_rows > 0" % len(attested_keys))
mine = set(key for _ledger, key in wanted)
print("   in mine and not in m1's: %s" % sorted(mine - attested_keys))
print("   in m1's and not in mine: %s" % sorted(attested_keys - mine))

# THE ORDER: most-used cell first, so a stopped lane has already
# finished the cells that carry the most of the corpus.
wanted.sort(key=lambda pair: (-pair[0], pair[1]))
print("")
print("   the twenty cells with the most attested ledger rows:")
for ledger, key in wanted[:20]:
    print("      %-10s %-10s %-4s  ledger_rows %d"
          % (key[0], key[1], key[2], ledger))

DROP = ("mapping",)
out = []
widths = set()
setters = set()
for ledger, key in wanted:
    held = []
    for row in by_key[key]:
        kept = {}
        for field in row:
            if field in DROP:
                continue
            kept[field] = row[field]
        held.append(kept)
    for row in held:
        if row.get("outcome") != "TRANSLATED":
            continue
        name = (row.get("flags_in") or {}).get("mnem")
        if name is not None:
            setters.add(name)
            widths.add(row.get("width"))
        for entry in ((row.get("attestation") or {}).get("setter") or []):
            if isinstance(entry, dict):
                setters.add(entry.get("mnem"))
            else:
                setters.add(entry)
            widths.add(row.get("width"))
    out.append({"asked": {"mnem": key[0], "shape": key[1],
                          "key_width": key[2]},
                "attested_ledger_rows": ledger,
                "rows": held})
setters.discard(None)
widths.discard(None)
print("")
print("   the setters these cells name: %d -- %s"
      % (len(setters), sorted(setters)))
print("   the widths those consumer rows carry: %s" % sorted(widths))

# THE SETTER ROWS, filtered by exactly what `handful.setter_row_for`
# reads -- the setter's own `mnem` and the consumer's `width` -- and by
# nothing else, so the row it picks out of this file is the row it
# would have picked out of the whole table.
setter_rows = []
for row in rows:
    if row["mnem"] not in setters:
        continue
    if row.get("outcome") != "TRANSLATED":
        continue
    if not row.get("writes_the_flags"):
        continue
    if row.get("width") not in widths:
        continue
    kept = {}
    for field in row:
        if field in DROP:
            continue
        kept[field] = row[field]
    setter_rows.append(kept)
print("   TRANSLATED flag-writing setter rows kept: %d" % len(setter_rows))

document = None
rows = None
by_key = None
handle = open("autopoly_cells.json", "w")
json.dump({"meta": {"source": MODEL,
                    "task": "ap1",
                    "what": "every attested cell of the arch-opcode "
                            "model table (a distinct (mnem, shape, "
                            "key_width) triple with a TRANSLATED row "
                            "whose attestation records at least one "
                            "ledger row), each with every model-table "
                            "row at that triple, in descending order "
                            "of attested ledger rows; plus every "
                            "TRANSLATED flag-writing row of the "
                            "setters those cells name, at the widths "
                            "they name",
                    "dropped_from_every_row": list(DROP),
                    "cells": len(out),
                    "setter_rows": len(setter_rows)},
           "asked": out,
           "setter_rows": setter_rows},
          handle, indent=1, sort_keys=True)
handle.close()
print("")
print("   wrote autopoly_cells.json, %d bytes"
      % os.path.getsize("autopoly_cells.json"))
print("   peak resident: %d kB" % check("at the end"))
PY
echo "[2/2] done"
