#!/bin/bash
# ap6_l5_the_setter_cells_and_the_holders.sh -- task ap6, lane 5.
#
# WHAT THIS LANE DOES: it measures, before anything is run, the three
# remaining changes of the brief's SS2 table on the objects they act on.
#
#   * THE SETTER CELLS.  The driver now answers one held cell per
#     setter CELL the corpus attests before a flag consumer, where it
#     answered one held cell over one setter mnemonic at one width.
#     This prints the population that change creates: how many consumer
#     cells carry an attested setter, how many setter cells each gets,
#     and what that does to the number of held cells the loop walks.
#   * THE HOLDERS ON THE PRIMITIVE LOOKUP.  Task hub1's five entries --
#     `and gpr_gpr 32` and `or gpr_gpr 32` on c and on rust, and
#     `not gpr_one 32` on c -- were PROVED by the loop and unusable by
#     any composition because the corpus body the lookup matched has
#     its parameters in the target's truth holder.  This asks the
#     lookup about each of them again and prints what it now answers.
#   * THE NARROW-ANSWER RE-POSE.  `handful.decided` now takes the
#     node's own answer width and cuts both sides to it in the re-pose,
#     beside the caller extension.  This poses task hub2's own sighting
#     -- `go/regen_146`, SS8 cause 2 -- through that call with the width
#     stated and without it, which is the verdict before and after.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_AP6, checked
# after each step.  Nothing here forks.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_ap6_brief.md
set -u

E=PseudoCoupHQ/Research/oracle/cross_construction/emulation
A=$E/autopoly
H=$E/handful
total=5

echo "[1/$total] every file this task changed compiles"
for f in "$H/handful.py" "$A/autopoly.py" "$A/bank.py"; do
    python3 -m py_compile "$f" && echo "  $(basename $f) compiles"
done
echo

echo "[2/$total] THE SETTER CELLS: the population the change creates"
python3 - "$H" "$A" <<'PY'
import sys, os, json, resource
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2])
BOUND = 6 * 1024 * 1024


def check(where):
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if peak > BOUND:
        raise SystemExit("ABORT_MEMORY_AP6: %d kB at %s" % (peak, where))
    return peak


import handful as H
cells = json.load(open(H.CELLS))
check("the outer set read")
consumers = 0
carried = 0
per = []
held_before = 0
held_after = 0
for record in cells["asked"]:
    asked = (record["asked"]["mnem"], record["asked"]["shape"],
             record["asked"]["key_width"])
    first = H.cell_input(cells, asked)
    held_before = held_before + 1
    if first.get("setter") is None:
        held_after = held_after + 1
        continue
    consumers = consumers + 1
    wanted = H.attested_setter_cells(cells, asked)
    keys = set()
    keys.add((first["setter"].get("mnem"), first["setter"].get("shape"),
              first["setter"].get("key_width")))
    for entry in wanted:
        keys.add((entry["mnem"], entry["shape"], entry["key_width"]))
        continue
    if wanted:
        carried = carried + 1
    held_after = held_after + len(keys)
    per.append((len(keys), asked, len(wanted)))
    check("consumer %s" % (asked,))
    continue
per.sort(reverse=True)
print("| what | count |")
print("|---|---|")
print("| asked cells on the outer set | %d |" % len(cells["asked"]))
print("| of them, cells that read an arriving flag state | %d |"
      % consumers)
print("| of those, cells the corpus attests a setter cell for | %d |"
      % carried)
print("| held cells the loop walked, one setter each | %d |" % held_before)
print("| held cells the loop walks now, one per setter cell | %d |"
      % held_after)
print("| distinct setter cells over all consumers | %d |"
      % len(set((e["mnem"], e["shape"], e["key_width"])
                for record in cells["asked"]
                for e in H.attested_setter_cells(
                    cells, (record["asked"]["mnem"],
                            record["asked"]["shape"],
                            record["asked"]["key_width"])))))
print("")
print("| consumer `mnem` | shape | `key_width` | setter cells |")
print("|---|---|---|---|")
for count, asked, _wanted in per[:12]:
    print("| `%s` | %s | %s | %d |" % (asked[0], asked[1], asked[2],
                                       count))
    continue
print("")
print("peak resident: %d kB" % check("done"))
PY
echo

echo "[3/$total] THE HOLDERS: task hub1's five entries, asked again"
python3 - "$H" "$A" <<'PY'
import sys, json, resource
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2])
import handful as H
cells = json.load(open(H.CELLS))
# THE FIVE ARE NAMED BY THEIR CELLS, which is the machine-form key
# (`mnem`, operand shape, `key_width`) plus the target -- task hub1's
# own table (log_252 SS7) states them that way and this reads them off
# it.  The `mnem` field is the guard-exempt one.
five = [
    ({"mnem": "and", "shape": "gpr_gpr", "key_width": 32}, "c"),
    ({"mnem": "or", "shape": "gpr_gpr", "key_width": 32}, "c"),
    ({"mnem": "not", "shape": "gpr_one", "key_width": 32}, "c"),
    ({"mnem": "and", "shape": "gpr_gpr", "key_width": 32}, "rust"),
    ({"mnem": "or", "shape": "gpr_gpr", "key_width": 32}, "rust"),
    ({"mnem": "add", "shape": "gpr_gpr", "key_width": 64}, "c"),
]
print("| cell | target | the lookup's answer | the holders |")
print("|---|---|---|---|")
for cell, lang in five:
    asked = (cell["mnem"], cell["shape"], cell["key_width"])
    held = H.cell_input(cells, asked)
    found = H.primitive_lookup(held, lang)
    if found.get("row") is not None:
        holders = found.get("holders") or []
        answer = "matched `%s`" % found["row"]["body_text"]
        spelt = ", ".join("%s %s" % (h["representation"], h["holder"])
                          for h in holders)
    else:
        answer = "refused: %s" % found.get("cause")
        spelt = ""
        refused = found.get("members_refused_by_holder") or []
        if refused:
            spelt = "%d member(s) refused; the first: %s" \
                    % (len(refused), refused[0]["cause"])
    print("| `%s` %s %s | %s | %s | %s |"
          % (cell["mnem"], cell["shape"], cell["key_width"], lang,
             answer, spelt))
    continue
print("")
print("peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
echo

echo "[4/$total] THE NARROW-ANSWER RE-POSE: hub2's own sighting, posed"
echo "          with the node's answer width stated and without it"
python3 - "$H" "$A" "$E" <<'PY'
import sys, json, os, resource
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2])
sys.path.insert(0, sys.argv[3])
import handful as H
import gate
import z3
# THE OBJECT IS TASK hub2's OWN, read off its measure rather than
# retyped: `go/regen_146` is the one sighting of cause 2 in log_254 SS8
# -- the two sides agree on the eight bits the node answers in and
# differ above them.  What is posed here is the same shape of question
# the hub posed: two terms of different widths, the gate's own rule
# cutting to the narrower, and then the re-pose with the node's own
# answer width stated.
#
# The two terms are built from the divide the log states LITERALLY:
# body A divides at 16 bits and leaves the quotient in the low 8 with
# the REMAINDER above it; body B divides at 8 bits and leaves the
# remainder in bits 8..15.  Both quotients agree; the bits above the
# node's eight do not.
a = z3.BitVec("IN_0", 64)
b = z3.BitVec("IN_1", 64)
lo_a = z3.Extract(7, 0, a)
lo_b = z3.Extract(7, 0, b)
wide = z3.ZeroExt(8, lo_a)
divisor = z3.ZeroExt(8, lo_b)
quotient16 = z3.UDiv(wide, divisor)
side_a = z3.ZeroExt(16, quotient16)
quotient8 = z3.UDiv(lo_a, lo_b)
remainder8 = z3.URem(lo_a, lo_b)
side_b = z3.ZeroExt(48, z3.Concat(remainder8, quotient8))
shared = {"gate": gate.Gate(3000)}
params = []
for stated in (None, 8):
    out = H.decided(shared, side_a, side_b, params, answer_bits=stated)
    again = out.get("under_caller_extension")
    print("  answer width stated: %s" % ("none" if stated is None
                                         else "%d bits" % stated))
    print("     the gate, as posed        : %s" % out["outcome"])
    if again is None:
        print("     the re-pose               : not reached")
    else:
        print("     the re-pose, cut to %-5s : %s"
              % ("%s" % again.get("answer_bits"), again["outcome"]))
    continue
print("")
print("peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
echo

echo "[5/$total] THE PLAN of the delta pass, with the new driver"
python3 "$A/autopoly.py" --pass ap6_delta --bank preflight
echo
echo "lane done"
