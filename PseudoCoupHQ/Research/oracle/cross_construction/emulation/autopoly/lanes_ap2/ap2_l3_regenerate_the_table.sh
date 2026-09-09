#!/usr/bin/env bash
# ap2_l3_regenerate_the_table.sh -- task ap2, fix 4, the second half:
# the table's own rows regenerated for the cells the new `key_width`
# case moves, and the attestation join re-run over them.
#
# WHAT IS REGENERATED AND WHAT IS NOT.  `model_table.key_width` is the
# ONE width rule and both sides of the join call it, so the two files
# the join reads -- `model_table_rows.json` (the sweep's rows) and
# `model_table_attest.json` (the corpus's attested cells) -- have their
# `key_width` field RECOMPUTED by that function over each record's own
# `mnem` and `width`.  Nothing else in either file is touched: the
# sweep is not re-run, no term is rebuilt, no attestation is re-read
# off the shards.  Then `model_table.assemble_command` -- the table's
# own join, unchanged -- is called, which re-joins the attestation onto
# the rows by (mnem, shape, key_width), recounts, and rewrites
# `model_table.json`.
#
# WHY THAT IS THE WHOLE OF IT: `assemble_command` reads the two files
# and `model_table_edges.json`, and the edges document contributes only
# aggregate counts, never a key of the join.
#
# GUARD, pasted before and after: the table's own `counts`, the number
# of rows carrying an attestation, and the outer set (attested cells,
# their ledger rows, and how many carry a null key_width).  A copy of
# the three files as they stood is left beside them with the suffix
# `.before_ap2`, so the before state is an object and not a memory.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP2.  The heavy
# reads are `model_table_rows.json` (50 MB) and `model_table.json`
# (73 MB); task ap1 measured the latter's parse at 290,040 kB.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/arch_opcodes/model

echo "[1/4] the before state, off the files as they stand"
cp -n model_table_rows.json model_table_rows.json.before_ap2
cp -n model_table_attest.json model_table_attest.json.before_ap2
cp -n model_table.json model_table.json.before_ap2
python3 - <<'PY'
import json
import resource

ABORT_KB = 6 * 1024 * 1024


def check(where):
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if peak > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_AP2: %d kB at %s" % (peak, where))
    return peak


document = json.load(open("model_table.json"))
counts = document["counts"]
print("   BEFORE, the table's own counts:")
for name in sorted(counts):
    if isinstance(counts[name], (int, float)):
        print("      %-40s %s" % (name, counts[name]))
rows = document["rows"]
attested_rows = 0
outer = {}
null_key = 0
for row in rows:
    held = (row.get("attestation") or {}).get("ledger_rows") or 0
    if held > 0:
        attested_rows = attested_rows + 1
    if row.get("outcome") != "TRANSLATED" or held <= 0:
        continue
    key = (row["mnem"], row.get("shape"), row.get("key_width"))
    outer[key] = max(outer.get(key, 0), held)
for key in outer:
    if key[2] is None:
        null_key = null_key + 1
print("   BEFORE, rows carrying an attestation: %d of %d"
      % (attested_rows, len(rows)))
print("   BEFORE, the outer set: %d cells, %d attested ledger rows, "
      "%d with a null key_width"
      % (len(outer), sum(outer[k] for k in outer), null_key))
print("   peak resident: %d kB" % check("before"))
PY

echo "[2/4] key_width recomputed on the two files the join reads"
python3 - <<'PY'
import json
import resource
import sys
sys.path.insert(0, "PseudoCoupHQ/Research/op_pipeline")
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/arch_opcodes/model")
import model_table as MTAB

ABORT_KB = 6 * 1024 * 1024


def check(where):
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if peak > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_AP2: %d kB at %s" % (peak, where))
    return peak


def refresh(path, holder):
    document = json.load(open(path))
    records = document[holder]
    moved = {}
    for record in records:
        before = record.get("key_width")
        after = MTAB.key_width(record["mnem"], record.get("width"))
        if before == after:
            continue
        record["key_width"] = after
        key = (record["mnem"], str(before), str(after))
        moved[key] = moved.get(key, 0) + 1
    print("   %s: %d of %d %s moved"
          % (path, sum(moved[k] for k in moved), len(records), holder))
    for key in sorted(moved):
        print("      %-8s %s -> %s   %d" % (key[0], key[1], key[2],
                                            moved[key]))
    handle = open(path, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    print("   peak resident: %d kB" % check(path))


refresh("model_table_rows.json", "rows")
refresh("model_table_attest.json", "cells")
PY

echo "[3/4] the table's own join, re-run: model_table.py assemble"
python3 model_table.py assemble

echo "[4/4] the after state, the same readings"
python3 - <<'PY'
import json
import resource

ABORT_KB = 6 * 1024 * 1024


def check(where):
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if peak > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_AP2: %d kB at %s" % (peak, where))
    return peak


document = json.load(open("model_table.json"))
counts = document["counts"]
print("   AFTER, the table's own counts:")
for name in sorted(counts):
    if isinstance(counts[name], (int, float)):
        print("      %-40s %s" % (name, counts[name]))
rows = document["rows"]
attested_rows = 0
outer = {}
null_key = 0
for row in rows:
    held = (row.get("attestation") or {}).get("ledger_rows") or 0
    if held > 0:
        attested_rows = attested_rows + 1
    if row.get("outcome") != "TRANSLATED" or held <= 0:
        continue
    key = (row["mnem"], row.get("shape"), row.get("key_width"))
    outer[key] = max(outer.get(key, 0), held)
for key in outer:
    if key[2] is None:
        null_key = null_key + 1
print("   AFTER, rows carrying an attestation: %d of %d"
      % (attested_rows, len(rows)))
print("   AFTER, the outer set: %d cells, %d attested ledger rows, "
      "%d with a null key_width"
      % (len(outer), sum(outer[k] for k in outer), null_key))
print("")
print("   the widening-move cells of the outer set, after:")
for key in sorted(outer, key=lambda k: (-outer[k], k)):
    if not str(key[1] or "").startswith("widen_"):
        continue
    print("      %-8s %-14s key_width %-4s ledger_rows %d"
          % (key[0], key[1], key[2], outer[key]))
print("   peak resident: %d kB" % check("after"))
PY
echo "done"
