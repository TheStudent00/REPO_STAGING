#!/usr/bin/env bash
# ap3_l4_cells_and_guards.sh -- task ap3: the outer set for this pass,
# and the guards on the two driver fixes, run BEFORE either is trusted
# and before the loop.
#
# THE OUTER SET.  It is task ap2's, unchanged: the same 253 attested
# cells over the same 133,044 attested ledger rows, with the eight
# `key_width`s task ap2's fix 4 moved off null already in it.  Nothing
# of this task touches the model table, so the cells file is COPIED
# rather than regenerated, and the copy's own counts are printed beside
# task ap2's so the copy is measured and not asserted.
#
# THE GUARDS.  Both fixes are unconditional in `handful.py` -- neither
# is gated on a task name, and `handful.use_task_ap3`'s docstring says
# why -- so every guard asks the same question: does an EARLIER task's
# population come out of the driver exactly as that task recorded it?
#
#   GUARD 1, task h2's own sources measurement (`handful.py
#   sources_counts`), which is also the ON side of fix 4's switch.
#   GUARD 2, the handful's ten cells through the ap3 driver, place by
#   place, against task g1b's own product: name, width, layer-5 text,
#   arrival families.
#   GUARD 3, THE BRIEF'S OWN GUARD ON FIX 1: the four vector cells of
#   the handful, and whether fix 1 touched their arrivals.  A place
#   whose uses all lie inside the low 64 bits must come out with NO
#   `arrivals_in_halves` record at all.
#   GUARD 4, task h1's `cmovne` / `setne`: both read the arriving flag
#   state, so fix 2's new condition must not reach them and both must
#   still compose with the setter their own attestation names.
#   GUARD 5, FIX 2'S OWN SIDE: the 32 x87 cells now reach the places
#   step, and what their places and homes are.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP3.
set -euo pipefail
ART=/projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
mkdir -p "$ART/src3" "$ART/src3_off"

echo "[1/6] the outer set: task ap2's cells file, copied"
if [ ! -f "$ART/autopoly3_cells.json" ]; then
  cp "$ART/autopoly2_cells.json" "$ART/autopoly3_cells.json"
fi
python3 - <<'PY'
import json
ART = ("/projects/PseudoCoupHQ/Research/oracle/cross_construction/"
       "emulation/autopoly")
for name in ("autopoly2_cells.json", "autopoly3_cells.json"):
    document = json.load(open("%s/%s" % (ART, name)))
    total = 0
    null = 0
    for record in document["asked"]:
        total = total + record["attested_ledger_rows"]
        if record["asked"]["key_width"] is None:
            null = null + 1
    print("   %-24s cells %d  attested ledger rows %d  null key_width "
          "%d  setter_census consumers %d  setter_rows %d"
          % (name, len(document["asked"]), total, null,
             len(document.get("setter_census") or {}),
             len(document.get("setter_rows") or [])))
PY

echo ""
echo "[2/6] GUARD 1 -- task h2's own sources measurement"
cd /projects/PseudoCoupHQ/Research/oracle/cross_construction/emulation/handful
python3 handful.py sources_counts

echo ""
echo "[3/6] GUARDS 2, 3, 4 and 5 -- through the ap3 driver"
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
cells = A.read_json(A.CELLS)
g1b = json.load(open(os.path.join(HERE, "handful", "handful3b.json")))
theirs = {}
for run in g1b["runs"]:
    for place in (run.get("places") or []):
        key = (run["mnem"], run["shape"], run["key_width"],
               place["writes"])
        theirs[key] = place
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
        home = place.get("home") or {}
        if home.get("family") not in R.XMM_NAMES:
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
print("   GUARD 5: FIX 2 -- the 32 x87 cells now reach the places step")
wanted = {}
for run in A.read_runs(A.BEFORE_RUNS):
    cause = A.cause_of(run)
    if cause is None or "no setter row to compose" not in cause:
        continue
    wanted[(run["mnem"], run["shape"], run["key_width"])] = run
reached = 0
still = []
print("   | cell | places | the home | bits | families |")
print("   |---|---|---|---|---|")
for key in sorted(wanted):
    held = H.cell_input(cells, key)
    if held.get("refusal_cause") is not None:
        still.append((key, held["refusal_cause"],
                      held.get("refusal_detail")))
        continue
    reached = reached + 1
    for place in held["places"]:
        print("   | `%s` %s %s | `%s` | %s | %s | %s |"
              % (key[0], key[1], key[2], place["writes"],
                 (place.get("home") or {}).get("family"),
                 place["bits"], place.get("families")))
print("")
print("   of the 32 cells, those that now reach the places step: %d"
      % reached)
print("   those still refused before it: %d" % len(still))
for key, cause, detail in still:
    print("      %s  %s: %s" % (key, cause, detail))
print("   peak resident: %d kB" % check("the guards"))
PY

echo ""
echo "[4/6] which form of the term each task's setting hands the renderer"
python3 autopoly3.py branch

echo ""
echo "[5/6] the outer set as the ap3 loop will walk it"
python3 autopoly3.py preflight

echo ""
echo "[6/6] THE SAMPLE: the first twenty runs, with the peak after each"
python3 autopoly3.py run 20
echo "done"
