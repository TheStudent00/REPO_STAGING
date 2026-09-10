#!/bin/bash
# ap6_l6_the_setter_cell_population.sh -- task ap6, lane 6.
#
# WHAT THIS LANE DOES: it reads the OUTER SET the loop actually walks --
# `autopoly5_cells.json`, 253 asked cells -- and measures the setter
# cell population under the two readings that are available in it, so
# the driver's rule is chosen on the objects and not assumed.  Lane 5
# read `handful_cells.json`, which is the ten-cell handful and not the
# outer set, so its numbers are about the wrong file.
#
#   READING A, the cross product: every cell the sweep gives a setter
#   whose MNEMONIC the consumer's own attestation records before it.
#   READING B, the corpus's own: the same, and the setter row's OWN
#   attestation records it inside a flag pair (`flag_pair_rows` above
#   zero), which is task m1b's flag-pair reading at cell granularity on
#   the setter side.
#
# Reading B is the one the brief asks for -- "every setter cell the
# corpus ATTESTS before it" -- and this lane is what says how far apart
# the two are.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_AP6, checked
# per consumer cell.  Nothing here forks.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_ap6_brief.md
set -u

E=PseudoCoupHQ/Research/oracle/cross_construction/emulation
A=$E/autopoly
H=$E/handful
total=2

echo "[1/$total] the setter rows of the outer set, by attestation"
python3 - "$H" "$A" <<'PY'
import sys, json, resource
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2])
import autopoly as AP
cells = json.load(open(AP.CELLS))
rows = cells.get("setter_rows") or []
translated = [r for r in rows if r.get("outcome") == "TRANSLATED"]
paired = [r for r in translated
          if ((r.get("attestation") or {}).get("flag_pair_rows") or 0) > 0]
def cellset(held):
    return set((r["mnem"], r.get("shape"), r.get("key_width"))
               for r in held)
print("| what | count |")
print("|---|---|")
print("| rows on the outer set's `setter_rows` | %d |" % len(rows))
print("| of them TRANSLATED | %d |" % len(translated))
print("| distinct cells among those | %d |" % len(cellset(translated)))
print("| TRANSLATED and recorded inside a flag pair by the corpus | %d |"
      % len(paired))
print("| distinct cells among THOSE | %d |" % len(cellset(paired)))
print("")
print("peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
echo

echo "[2/$total] the two readings, per consumer cell of the outer set"
python3 - "$H" "$A" <<'PY'
import sys, json, resource
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2])
BOUND = 6 * 1024 * 1024


def check(where):
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if peak > BOUND:
        raise SystemExit("ABORT_MEMORY_AP6: %d kB at %s" % (peak, where))
    return peak


import autopoly as AP
import handful as H
cells = json.load(open(AP.CELLS))
rows = cells.get("setter_rows") or []
per = []
consumers = 0
held_before = 0
after_a = 0
after_b = 0
for record in cells["asked"]:
    asked = (record["asked"]["mnem"], record["asked"]["shape"],
             record["asked"]["key_width"])
    held_before = held_before + 1
    first = H.cell_input(cells, asked)
    if first.get("setter") is None:
        after_a = after_a + 1
        after_b = after_b + 1
        continue
    consumers = consumers + 1
    attested = {}
    for row in record.get("rows") or []:
        for entry in ((row.get("attestation") or {}).get("setter") or []):
            was = attested.get(entry["mnem"]) or 0
            if (entry.get("ledger_rows") or 0) > was:
                attested[entry["mnem"]] = entry.get("ledger_rows") or 0
            continue
        continue
    a = set()
    b = set()
    default = (first["setter"].get("mnem"), first["setter"].get("shape"),
               first["setter"].get("key_width"))
    a.add(default)
    b.add(default)
    for row in rows:
        if row.get("outcome") != "TRANSLATED":
            continue
        if row["mnem"] not in attested:
            continue
        key = (row["mnem"], row.get("shape"), row.get("key_width"))
        a.add(key)
        if ((row.get("attestation") or {}).get("flag_pair_rows") or 0) > 0:
            b.add(key)
        continue
    after_a = after_a + len(a)
    after_b = after_b + len(b)
    per.append((len(b), len(a), asked))
    check("consumer %s" % (asked,))
    continue
per.sort(reverse=True)
print("| what | held cells |")
print("|---|---|")
print("| the loop as it was, one setter cell per asked cell | %d |"
      % held_before)
print("| asked cells that read an arriving flag state | %d |" % consumers)
print("| READING A, the cross product | %d |" % after_a)
print("| READING B, the corpus's own flag-pair rows | %d |" % after_b)
print("")
print("| consumer `mnem` | shape | `key_width` | reading B | reading A |")
print("|---|---|---|---|---|")
for count_b, count_a, asked in per[:30]:
    print("| `%s` | %s | %s | %d | %d |"
          % (asked[0], asked[1], asked[2], count_b, count_a))
    continue
print("")
print("peak resident: %d kB" % check("done"))
PY
echo
echo "lane done"
