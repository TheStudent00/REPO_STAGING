#!/usr/bin/env bash
# ap2_l5_driver_guards.sh -- task ap2: the guards on the four fixes
# that live in the DRIVER, run before any of them is trusted and before
# the loop.
#
# The four fixes are unconditional in `handful.py` -- none is gated on
# a task name, and `handful.use_task_ap2`'s docstring says why -- so
# the question every guard here asks is the same one: does an EARLIER
# task's population come out of the driver exactly as that task
# recorded it?
#
#   GUARD 1, fix 6 (task h2's normalise-before-render, ungated).
#   `handful.py sources_counts` is task h2's OWN measurement: the same
#   places rendered from both forms of the term, the two source texts
#   compared character for character.  It writes nothing.
#
#   GUARD 2, fixes 1, 2 and 3, on task g1b's forty runs.  For each of
#   the handful's ten cells, `handful.cell_input` is called through the
#   ap2 driver and the places it produces are compared against the
#   places task g1b's own product `handful3b.json` records -- the
#   place's name, its width, its layer-5 text and its arrival families.
#   Everything the three fixes touch is upstream of the render, so if
#   those four readings are unchanged, nothing task g1b measured moved.
#
#   GUARD 3, the four vector cells.  `addss` 32 and its like have a
#   lane NARROWER than their 128-bit place, so task h2's fix 2 projects
#   it and task ap2's fix 3 must leave them alone.  The lane record is
#   printed and the halving record is shown to be absent.
#
#   GUARD 4, task h1's `cmovne` / `setne`.  Both name a setter in their
#   own attestation, so fix 2's corpus census must not be reached at
#   all: the setter each composes with is printed with the reason the
#   driver gives for it.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP2.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful

echo "[1/4] GUARD 1 -- task h2's own sources measurement"
python3 handful.py sources_counts

echo "[2/4] GUARD 2, 3 and 4 -- the handful's ten cells through the ap2 driver"
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 - <<'PY'
import json
import os
import resource
import sys

HERE = "PseudoCoupHQ/Research/oracle/cross_construction/emulation"
sys.path.insert(0, os.path.join(HERE, "handful"))
sys.path.insert(0, os.path.join(HERE, "autopoly"))
import autopoly2 as A
import handful as H

ABORT_KB = 6 * 1024 * 1024


def check(where):
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if peak > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_AP2: %d kB at %s" % (peak, where))
    return peak


A.use_task_ap2()
cells = A.read_json(A.CELLS)
g1b = json.load(open(os.path.join(HERE, "handful", "handful3b.json")))

# TASK g1b'S OWN PLACES, off its product, keyed by the cell and the
# place's own name.
theirs = {}
for run in g1b["runs"]:
    for place in (run.get("places") or []):
        key = (run["mnem"], run["shape"], run["key_width"],
               place["writes"])
        theirs[key] = place
print("   places task g1b's own product records: %d" % len(theirs))

VECTOR = set()
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
        home = place.get("home") or {}
        if home.get("family") in __import__("reference").XMM_NAMES:
            VECTOR.add(key)
print("")
print("   GUARD 2: places of the handful's ten cells that come out "
      "IDENTICAL (name, width, layer-5 text, arrival families): %d"
      % same)
print("   places that DIFFER: %d" % len(differs))
for key, yours, mine in differs:
    print("      %s" % (key,))
    print("         task g1b: %s" % (yours,))
    print("         task ap2: %s" % (mine,))
print("   places task ap2 produces that task g1b's product has no row "
      "for: %d  %s" % (len(missing), missing))

print("")
print("   GUARD 3: the vector places of the handful, and whether task "
      "ap2's fix 3 touched them")
for asked in H.ASKED:
    held = H.cell_input(cells, asked)
    if held.get("refusal_cause") is not None:
        continue
    for place in held["places"]:
        home = place.get("home") or {}
        if home.get("family") not in __import__("reference").XMM_NAMES:
            continue
        print("      %-9s %-9s %-4s %-10s bits %-4s halved: %s"
              % (asked[0], asked[1], asked[2], place["writes"],
                 place["bits"], place.get("halved")))

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
    print("         from the corpus census: %s"
          % setter.get("from_the_corpus"))
print("   peak resident: %d kB" % check("the guards"))
PY

echo "[3/4] which form of the term each task's setting hands the renderer"
python3 autopoly2.py branch

echo "[4/4] the outer set as the ap2 loop will walk it"
python3 autopoly2.py preflight | grep -v 'peak resident'
echo "done"
