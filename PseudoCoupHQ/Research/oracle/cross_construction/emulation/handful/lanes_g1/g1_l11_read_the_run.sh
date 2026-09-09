#!/usr/bin/env bash
# g1_l11_read_the_run.sh -- task g1: read lane g1_l9's own run of the
# forty -- the tally, the by-cause section, and the re-posed gate calls
# -- before anything is written about it.
#
# WHY: the deliverable is a table, a by-cause list and two tallies, and
# each of those is a count the program derives rather than one this
# task asserts.  This lane prints them so the log quotes the program's
# own output.
#
# MEMORY BOUND: 4 GB resident, named abort ABORT_MEMORY_G1.
set -euo pipefail
H=PseudoCoupHQ/Research/oracle/cross_construction/emulation
echo "[1/3] task g1: handful.py tally3"
python3 $H/handful/handful.py tally3
echo "[2/3] task g1: what did not work, by cause"
sed -n '\%^### 3.1 Refusals%,\%^## 5%p' $H/handful/handful3.md
echo "[3/3] task g1: every gate call re-posed at 300,000 ms"
python3 - <<'PY'
import json
d = json.load(open("PseudoCoupHQ/Research/oracle/"
                   "cross_construction/emulation/handful/handful3.json"))
print("re-posed:", d["meta"].get("recheck_count"),
      "at", d["meta"].get("recheck_ceiling_ms"), "ms")
for run in d["runs"]:
    for place in run.get("places") or []:
        check = place.get("check") or {}
        again = check.get("recheck")
        if again is None:
            continue
        print("   %s %s %s/%s [%s]: %s at 3000 ms, %s at %s ms"
              % (run["mnem"], run["shape"], run["key_width"],
                 run["lang"], place["writes"], check.get("outcome"),
                 again.get("outcome"), again.get("ceiling_ms")))
PY
