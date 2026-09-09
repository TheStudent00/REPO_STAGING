#!/usr/bin/env bash
# ap2_l4_cells.sh -- task ap2, step 0: the OUTER SET of the owner's loop, out
# of the REGENERATED arch-opcode model table and into a file the run
# lane reads.
#
# TASK ap1'S OWN LANE `ap1_l1_cells.sh`, with two things added and
# nothing taken away.  The first is the file it writes:
# `autopoly2_cells.json`, so task ap1's own cells file is not touched.
# The second is THE SETTER CENSUS, which task ap2's fix 2 reads:
#
#   `setter_census` -- per flag-CONSUMING mnemonic, the setters the
#   corpus's own flag-pair ledger rows record before it, with the
#   ledger rows each carries, summed over EVERY attested cell of that
#   mnemonic in `model_table_attest.json` and not only over the cells
#   of this outer set.  Task m1b's attestation pass walked 22,741 such
#   rows (`counts.flag_consumer_rows`), and each carries the pair
#   (setter, consumer) in the ledger row's own `mnem` list.  Where a
#   cell's own attestation names no setter -- task ap1's second largest
#   cause, 128 runs -- `handful.setter_from_the_corpus` reads this
#   census instead, and where the census names none either the cause
#   stands.
#
# THE KEY THIS FILE IS WRITTEN WITH is the table's own `key_width`
# field, which lane `ap2_l3_regenerate_the_table.sh` has just
# regenerated through `model_table.key_width` -- so the eight cells
# that carried null now carry the destination width of their widening
# move, and the driver can format a label for them.
#
# WHAT THIS LANE PRODUCES, one sentence: `autopoly2_cells.json`, the
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
# ABORT_MEMORY_AP2, checked after the parse and at the end. The heavy
# read is the 73 MB `model_table.json`; task h1's own lane measured its
# parse at 290,040 kB.
set -euo pipefail
echo "[1/2] task ap2: the attested cells, out of model_table.json"
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
        raise SystemExit("ABORT_MEMORY_AP2: %d kB at %s" % (peak, where))
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

# THE SETTER CENSUS (task ap2, fix 2).  Per flag-consuming mnemonic,
# every setter the corpus's own flag-pair ledger rows record before it,
# with the ledger rows each carries -- summed over EVERY attested cell
# of that mnemonic in `model_table_attest.json`, which is where task
# m1b's attestation pass put them (`cell["setter"]`, one entry per
# setter, built by `hold_setter` off the two-element `mnem` list of a
# flag-pair ledger row).
#
# THIS IS A COUNT PER MNEMONIC AND NOT A CANDIDATE CHOSEN BY A
# SPELLING: the key is the consumer's own `mnem`, which the ruling of
# 2026-09-08 states is the machine form, and the winner is whichever
# setter carries the most ledger rows.  Nothing is grouped or paired by
# an operator token.
census = {}
for cell in attested["cells"]:
    entries = cell.get("setter") or []
    if not entries:
        continue
    held = census.setdefault(cell["mnem"], {})
    for entry in entries:
        name = entry.get("mnem") if isinstance(entry, dict) else entry
        if name is None:
            continue
        count = 0
        if isinstance(entry, dict):
            count = entry.get("ledger_rows") or 0
        held[name] = held.get(name, 0) + count
setter_census = {}
for consumer in sorted(census):
    held = census[consumer]
    listed = []
    for name in sorted(held, key=lambda n: (-held[n], n)):
        listed.append({"mnem": name, "ledger_rows": held[name]})
    setter_census[consumer] = listed
print("")
print("   THE SETTER CENSUS: %d flag-consuming mnemonics"
      % len(setter_census))
for consumer in sorted(setter_census):
    listed = setter_census[consumer]
    text = []
    for entry in listed[:4]:
        text.append("%s %d" % (entry["mnem"], entry["ledger_rows"]))
    print("      %-10s %s" % (consumer, ", ".join(text)))

# The census can name a setter no cell of this outer set names, and a
# consumer whose own width is not in `widths`; both must be in the
# filters below or the row the driver asks for is not on the file.
for consumer in setter_census:
    for entry in setter_census[consumer]:
        setters.add(entry["mnem"])
for row in rows:
    if row.get("outcome") != "TRANSLATED":
        continue
    if row["mnem"] not in setter_census:
        continue
    if (row.get("attestation") or {}).get("ledger_rows"):
        widths.add(row.get("width"))
setters.discard(None)
widths.discard(None)
print("   after the census, setters wanted: %d, widths wanted: %s"
      % (len(setters), sorted(widths)))

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
handle = open("autopoly2_cells.json", "w")
json.dump({"meta": {"source": MODEL,
                    "task": "ap2",
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
                    "setter_rows": len(setter_rows),
                    "setter_census": len(setter_census),
                    "setter_census_is": "per flag-consuming mnemonic, "
                                        "the setters the corpus's own "
                                        "flag-pair ledger rows record "
                                        "before it, with the ledger "
                                        "rows each carries, summed "
                                        "over every attested cell of "
                                        "that mnemonic"},
           "asked": out,
           "setter_rows": setter_rows,
           "setter_census": setter_census},
          handle, indent=1, sort_keys=True)
handle.close()
print("")
print("   wrote autopoly2_cells.json, %d bytes"
      % os.path.getsize("autopoly2_cells.json"))
print("   peak resident: %d kB" % check("at the end"))
PY
echo "[2/2] done"
