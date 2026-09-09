#!/usr/bin/env bash
# ap3_l7_guards_again_and_the_sample.sh -- task ap3: the guards a fourth
# time, and the twenty-run sample the law asks for, against the driver
# as the two defects the earlier passes MEASURED leave it.
#
# WHAT THE EARLIER PASSES CAUGHT, both in this task's own new code and
# neither in a fix's idea:
#   * lane `ap3_l5`: fix 1 reached the handful's two vector cells,
#     because a place task h2's fix 2 projects a lane out of does read
#     its arrival above bit 63 and the projection is what makes that not
#     matter.  `vector_arrivals_in_halves` now leaves such a place alone.
#   * lane `ap3_l6`: `emulate.is_an_x87_arrival` spelled a bare `st` as
#     an x87 prefix, and `push` gpr_one 64 writes a place whose name
#     begins `st` -- so all four targets refused the corpus's
#     third-most-attested cell.  The prefix list is now `X87_` and
#     `x87_` and nothing else.
#
# THE STORE IS STARTED AGAIN.  The 40 lines lanes `ap3_l5` and `ap3_l6`
# wrote are runs of the driver as those two defects left it, so they
# are moved aside -- to `autopoly3_runs.jsonl.before_the_guards_passed`,
# NOT removed -- and the loop of record begins on an empty store.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP3.
set -euo pipefail
ART=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
mkdir -p "$ART/src3" "$ART/src3_off"
if [ -f "$ART/autopoly3_runs.jsonl" ]; then
  mv "$ART/autopoly3_runs.jsonl" \
     "$ART/autopoly3_runs.jsonl.before_the_guards_passed"
  echo "the earlier store moved aside: $(wc -l < "$ART/autopoly3_runs.jsonl.before_the_guards_passed") line(s)"
fi

echo ""
echo "[1/5] GUARD 1 -- task h2's own sources measurement"
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
python3 handful.py sources_counts

echo ""
echo "[2/5] GUARDS 2, 3, 4 and 5 -- through the ap3 driver"
cd "$ART"
python3 - <<'PY'
import json
import os
import resource
import sys

HERE = "/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation"
sys.path.insert(0, os.path.join(HERE, "handful"))
sys.path.insert(0, os.path.join(HERE, "autopoly"))
import autopoly3 as A
import handful as H
import reference as R
import emulate as E

ABORT_KB = 6 * 1024 * 1024


def check(where):
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if peak > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_AP3: %d kB at %s" % (peak, where))
    return peak


A.use_task_ap3()
print("   handful.TASK %s  fixes_are_on %s  primitive_first %s  "
      "setup_is_allowed %s  NORMALISE_BEFORE_RENDER %s"
      % (H.TASK, H.fixes_are_on(), H.primitive_first(),
         H.setup_is_allowed(), H.NORMALISE_BEFORE_RENDER))
print("   emulate.X87_ARRIVAL, LITERAL: %r" % (E.X87_ARRIVAL,))
print("   emulate.FLOAT, LITERAL: %r" % (E.FLOAT,))
print("   handful.TARGETS_WITH_AN_80_BIT_HOLDER, LITERAL: %r"
      % (H.TARGETS_WITH_AN_80_BIT_HOLDER,))
cells = A.read_json(A.CELLS)
g1b = json.load(open(os.path.join(HERE, "handful", "handful3b.json")))
theirs = {}
for run in g1b["runs"]:
    for place in (run.get("places") or []):
        theirs[(run["mnem"], run["shape"], run["key_width"],
                place["writes"])] = place
print("   places task g1b's own product records: %d" % len(theirs))

same = 0
differs = []
missing = []
for asked in H.ASKED:
    held = H.cell_input(cells, asked)
    if held.get("refusal_cause") is not None:
        print("   %-9s %-9s %-4s REFUSED before the places: %s: %s"
              % (asked + (held["refusal_cause"],
                          held.get("refusal_detail"))))
        continue
    for place in held["places"]:
        key = (asked[0], asked[1], asked[2], place["writes"])
        earlier = theirs.get(key)
        if earlier is None:
            missing.append(key)
            continue
        mine = (place["writes"], place["bits"], place["text"],
                place.get("families"))
        yours = (earlier["writes"], earlier["bits"], earlier["text"],
                 earlier.get("families"))
        if mine == yours:
            same = same + 1
        else:
            differs.append((key, yours, mine))
print("")
print("   GUARD 2: places of the handful's ten cells that come out "
      "IDENTICAL (name, width, layer-5 text, arrival families): %d"
      % same)
print("   places that DIFFER: %d" % len(differs))
for key, yours, mine in differs:
    print("      %s" % (key,))
    print("         task g1b: %s" % (yours,))
    print("         task ap3: %s" % (mine,))
print("   places task ap3 produces that task g1b's product has no row "
      "for: %d  %s" % (len(missing), missing))

print("")
print("   GUARD 3: the vector places of the handful, and whether task "
      "ap3's fix 1 touched their arrivals")
for asked in H.ASKED:
    held = H.cell_input(cells, asked)
    if held.get("refusal_cause") is not None:
        continue
    for place in held["places"]:
        if (place.get("home") or {}).get("family") not in R.XMM_NAMES:
            continue
        print("      %-9s %-9s %-4s %-12s bits %-4s halved: %-5s "
              "arrivals_in_halves: %s families %s"
              % (asked[0], asked[1], asked[2], place["writes"],
                 place["bits"], place.get("halved") is not None,
                 place.get("arrivals_in_halves"),
                 place.get("families")))

print("")
print("   GUARD 4: the setter each flag-reading cell of the handful "
      "composes with, and the reason the driver gives")
for asked in H.ASKED:
    held = H.cell_input(cells, asked)
    setter = held.get("setter")
    if setter is None:
        continue
    print("      %-9s %-9s %-4s setter %-8s why: %s"
          % (asked[0], asked[1], asked[2], setter["mnem"],
             setter["why"]))

print("")
print("   GUARD 6: THE PLACES OF `push` gpr_one 64, the cell the bare "
      "`st` prefix refused")
held = H.cell_input(cells, ("push", "gpr_one", 64))
for place in held.get("places") or []:
    print("      `%s` bits %s home %s families %s x87? %s"
          % (place["writes"], place["bits"],
             (place.get("home") or {}).get("family"),
             place.get("families"),
             E.is_an_x87_arrival(place["writes"])))
print("   peak resident: %d kB" % check("the guards"))
PY

echo ""
echo "[3/5] the outer set as the ap3 loop will walk it"
python3 autopoly3.py preflight

echo ""
echo "[4/5] FIX 1, MEASURED ON ITS OWN 40 PAIRS, before the loop"
python3 autopoly3.py measure 'beyond its low lane'

echo ""
echo "[5/5] THE SAMPLE: the first twenty runs, with the peak after each"
python3 autopoly3.py run 20
echo "done"
