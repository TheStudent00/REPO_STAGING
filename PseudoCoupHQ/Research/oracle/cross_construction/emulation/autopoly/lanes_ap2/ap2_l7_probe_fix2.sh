#!/usr/bin/env bash
# ap2_l7_probe_fix2.sh -- task ap2: why fix 2 did not move its 128
# pairs, asked of the objects rather than reasoned about.
#
# Lane ap2_l6 measured fix 2 on the 128 pairs task ap1 refused for `no
# setter row to compose the flag pair from: None at width 8` and all
# 128 still say it, with the setter still spelled None -- which means
# `handful.setter_from_the_corpus` answered None, which means the
# census has no entry under that consumer's own `mnem`.  This lane
# prints the two sides of that lookup: the 32 cells the cause covers,
# and what the census holds for each.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 - <<'PY'
import json
import os
import sys

HERE = "PseudoCoupHQ/Research/oracle/cross_construction/emulation"
sys.path.insert(0, os.path.join(HERE, "handful"))
sys.path.insert(0, os.path.join(HERE, "autopoly"))
import autopoly2 as A
import handful as H

A.use_task_ap2()
cells = A.read_json(A.CELLS)
census = cells.get("setter_census")
print("the cells file: %s" % A.CELLS)
print("it holds a setter_census: %s" % (census is not None))
if census is not None:
    print("consumers in the census: %d -- %s"
          % (len(census), sorted(census)))

wanted = []
for run in A.read_runs(A.AP1_RUNS):
    cause = A.cause_of(run)
    if cause is None or "no setter row to compose" not in cause:
        continue
    wanted.append(run)
print("")
print("task ap1's runs with that cause: %d" % len(wanted))
seen = {}
for run in wanted:
    seen[(run["mnem"], run["shape"], run["key_width"])] = 1
print("distinct cells: %d" % len(seen))
print("")
print("| cell | in the census | the census's own top setter | the "
      "chosen row's flags_in | preseeded | TRANSLATED rows |")
print("|---|---|---|---|---|---|")
for key in sorted(seen):
    top = "--"
    if census and key[0] in census:
        entry = census[key[0]][0]
        top = "%s %d" % (entry["mnem"], entry["ledger_rows"])
    held = {}
    row = H.chosen_row(cells, key, held)
    count = 0
    for record in cells["asked"]:
        if (record["asked"]["mnem"], record["asked"]["shape"],
                record["asked"]["key_width"]) != key:
            continue
        for one in record["rows"]:
            if one.get("outcome") == "TRANSLATED":
                count = count + 1
    print("| `%s` %s %s | %s | %s | %s | %s | %d |"
          % (key[0], key[1], key[2],
             bool(census and key[0] in census), top,
             (row or {}).get("flags_in"),
             (row or {}).get("preseeded"), count))

print("")
print("the setter rows the file holds, by (mnem, width, shape), for the "
      "setters the census names:")
holder = {}
for row in cells["setter_rows"]:
    holder.setdefault((row["mnem"], row.get("width")), set()).add(
        row.get("shape"))
for key in sorted(holder, key=lambda k: (k[0], str(k[1]))):
    print("   %-9s width %-4s shapes %s"
          % (key[0], key[1], sorted(holder[key])))
PY
echo "done"
