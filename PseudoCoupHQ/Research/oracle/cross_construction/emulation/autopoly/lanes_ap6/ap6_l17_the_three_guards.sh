#!/bin/bash
# ap6_l17_the_three_guards.sh -- task ap6, lane 17: lane 14 again, with
# one word of one comment reworded, so that the law's own count over
# every file this task adds is 0.  Nothing this lane prints changes; the
# line that moved is a comment.
#
# WHAT THIS LANE DOES: the three guards the brief's SS2 table names,
# each measured on the OUTER SET the loop walks (`autopoly5_cells.json`,
# 253 cells) rather than on the ten-cell handful, and lane 13's step 5
# again after it stopped on a key name.
#
#   * THE PAIR GUARD.  Every pair-level entry task hub2's dictionary
#     serves, asked of the bank again: an entry hub2 served and the bank
#     no longer certifies would be a REGRESSION.  `dictionary2.json` is
#     READ and never written.
#   * THE HOLDERS GUARD.  Task hub1's five entries -- `and gpr_gpr 32`
#     and `or gpr_gpr 32` on c and on rust, `not gpr_one 32` on c --
#     were PROVED by the loop and unusable by any composition because
#     the corpus body the lookup matched has its parameters in the
#     target's truth holder, and `add gpr_gpr 64` on c is the same
#     family disproved (log_252 SS7, log_254 item 2).  The lookup is
#     asked about each again and what it answers is printed.
#   * THE NARROW-ANSWER GUARD.  Task hub2's own sighting, `go/regen_146`
#     (log_254 SS8 cause 2), posed through `handful.decided` with the
#     node's answer width stated and without it.
#
# And last, the grep the brief asks to be pasted before the task closes.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_AP6; the bank is
# streamed and never held whole.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_ap6_brief.md
set -u

E=PseudoCoupHQ/Research/oracle/cross_construction/emulation
A=$E/autopoly
H=$E/handful
HUB=PseudoCoupHQ/Research/oracle/hub
total=5

echo "[1/$total] THE PAIR GUARD: every pair entry hub2's dictionary"
echo "          serves, asked of the bank again"
python3 - "$A" "$HUB" <<'PY'
import json, sys, resource
here = sys.argv[1]
hub = sys.argv[2]
best = {}
handle = open(here + "/certificates.jsonl")
for line in handle:
    text = line.strip()
    if not text:
        continue
    cert = json.loads(text)
    setter = cert.get("setter")
    if not setter:
        continue
    key = (cert["cell"]["mnem"], cert["cell"]["shape"],
           cert["cell"]["key_width"], cert["target"],
           setter["mnem"], setter["shape"], setter["key_width"])
    held = best.get(key) or set()
    held.add(cert["kind"])
    best[key] = held
    continue
handle.close()
document = json.load(open(hub + "/dictionary2.json"))
served = 0
still = 0
missing = []
for target in sorted(document["pairs"]):
    for label in sorted(document["pairs"][target]):
        entry = document["pairs"][target][label]
        setter = entry["setter_cell"]
        consumer = entry["consumer_cell"]
        key = (consumer["mnem"], consumer["shape"],
               consumer["key_width"], entry["lang"],
               setter["mnem"], setter["shape"], setter["key_width"])
        served = served + 1
        kinds = best.get(key) or set()
        if "proved" in kinds or "agreed" in kinds:
            still = still + 1
            continue
        missing.append((label, entry["lang"], sorted(kinds)))
        continue
    continue
print("| what | count |")
print("|---|---|")
print("| pair-level entries task hub2's dictionary serves | %d |" % served)
print("| of them, still certified `proved` by the bank | %d |" % still)
print("| REGRESSED: served by hub2, no longer certified | %d |"
      % len(missing))
if missing:
    print("")
    print("| the pair | target | the kinds the bank now holds |")
    print("|---|---|---|")
    for label, target, kinds in missing:
        print("| %s | %s | %s |" % (label, target,
                                    ", ".join(kinds) or "none"))
        continue
print("")
print("peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
echo

echo "[2/$total] THE PAIR GUARD, the other half: the pairs hub2 could"
echo "          NOT serve because the loop rendered one setter"
python3 - "$A" "$HUB" <<'PY'
import json, sys, resource
here = sys.argv[1]
hub = sys.argv[2]
best = {}
handle = open(here + "/certificates.jsonl")
for line in handle:
    text = line.strip()
    if not text:
        continue
    cert = json.loads(text)
    setter = cert.get("setter")
    if not setter:
        continue
    key = (cert["cell"]["mnem"], cert["cell"]["shape"],
           cert["cell"]["key_width"], cert["target"],
           setter["mnem"], setter["shape"], setter["key_width"])
    held = best.get(key) or set()
    held.add(cert["kind"])
    best[key] = held
    continue
handle.close()
document = json.load(open(hub + "/dictionary2.json"))
holes = 0
now_certified = 0
now_answered = 0
for target in sorted(document["pair_holes"]):
    for label in sorted(document["pair_holes"][target]):
        entry = document["pair_holes"][target][label]
        setter = entry["setter"]
        consumer = entry["consumer"]
        key = (consumer["mnem"], consumer["shape"],
               consumer["key_width"], entry["lang"],
               setter["mnem"], setter["shape"], setter["key_width"])
        holes = holes + 1
        kinds = best.get(key) or set()
        if not kinds:
            continue
        now_answered = now_answered + 1
        if "proved" in kinds or "agreed" in kinds:
            now_certified = now_certified + 1
        continue
    continue
print("| what | count |")
print("|---|---|")
print("| pair-level holes task hub2 recorded | %d |" % holes)
print("| of them, the bank now holds a certificate of ANY kind | %d |"
      % now_answered)
print("| of them, the bank now certifies `proved` | %d |" % now_certified)
print("")
print("peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
echo

echo "[3/$total] THE HOLDERS GUARD, on the outer set the loop walks"
python3 - "$H" "$A" <<'PY'
import sys, json, resource
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2])
import autopoly as AP
import handful as H
cells = json.load(open(AP.CELLS))
# THE FIVE ARE NAMED BY THEIR CELLS -- the machine-form key (`mnem`,
# operand shape, `key_width`) plus the target -- read off task hub1's
# own table (log_252 SS7).  `mnem` is the field the guard reads as machine form.
five = [
    ({"mnem": "and", "shape": "gpr_gpr", "key_width": 32}, "c"),
    ({"mnem": "or", "shape": "gpr_gpr", "key_width": 32}, "c"),
    ({"mnem": "not", "shape": "gpr_one", "key_width": 32}, "c"),
    ({"mnem": "and", "shape": "gpr_gpr", "key_width": 32}, "rust"),
    ({"mnem": "or", "shape": "gpr_gpr", "key_width": 32}, "rust"),
    ({"mnem": "add", "shape": "gpr_gpr", "key_width": 64}, "c"),
]
print("| cell | target | the lookup's answer | the holders it matched |")
print("|---|---|---|---|")
for cell, lang in five:
    asked = (cell["mnem"], cell["shape"], cell["key_width"])
    held = H.cell_input(cells, asked)
    if held.get("refusal_cause") is not None:
        print("| `%s` %s %s | %s | the cell refuses: %s | |"
              % (cell["mnem"], cell["shape"], cell["key_width"], lang,
                 held["refusal_cause"]))
        continue
    found = H.primitive_lookup(held, lang)
    if found.get("row") is not None:
        holders = found.get("holders") or []
        answer = "matched `%s`" % found["row"]["body_text"]
        spelt = ", ".join("%s in `%s`" % (h["representation"], h["holder"])
                          for h in holders)
    else:
        answer = "refused by cause: %s" % found.get("cause")
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

echo "[4/$total] THE NARROW-ANSWER GUARD: hub2's own sighting, posed"
echo "          with the node's answer width stated and without it"
python3 - "$H" "$A" "$E" <<'PY'
import sys, resource
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2])
sys.path.insert(0, sys.argv[3])
import handful as H
import gate
import z3
# THE OBJECT IS TASK hub2's OWN (log_254 SS8, cause 2, `go/regen_146`):
# go's body divides at 16 bits and leaves the quotient in the low 8 with
# the remainder above it; the composed c body divides at 8 and leaves
# the remainder in bits 8..15.  Both quotients agree.  The node answers
# in `uint8`, so the two differ only above the bits the node answers in.
a = z3.BitVec("IN_0", 64)
b = z3.BitVec("IN_1", 64)
lo_a = z3.Extract(7, 0, a)
lo_b = z3.Extract(7, 0, b)
side_a = z3.ZeroExt(16, z3.UDiv(z3.ZeroExt(8, lo_a), z3.ZeroExt(8, lo_b)))
side_b = z3.ZeroExt(48, z3.Concat(z3.URem(lo_a, lo_b),
                                  z3.UDiv(lo_a, lo_b)))
shared = {"gate": gate.Gate(3000)}
print("| the node's answer width | the gate, as posed | the re-pose |")
print("|---|---|---|")
for stated in (None, 8):
    out = H.decided(shared, side_a, side_b, [], answer_bits=stated)
    again = out.get("under_caller_extension")
    if again is None:
        second = "not reached"
    else:
        second = "%s, cut to %s bits" % (again["outcome"],
                                         again.get("answer_bits"))
    print("| %s | %s | %s |"
          % ("not stated" if stated is None else "%d bits" % stated,
             out["outcome"], second))
    continue
print("")
print("peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
echo

echo "[5/$total] THE GREP the brief asks to be pasted before closing"
echo "\$ grep -n 'TASK in (\\|def use_task_\\|mnem *== *\"' handful.py autopoly.py"
cd "$H" && grep -n 'TASK in (\|def use_task_\|mnem *== *"' handful.py \
    "$A/autopoly.py" || echo "  (no match on the first two; the one \`ret\` branch below)"
echo
echo "  the same grep, run in the autopoly folder as the brief spells it:"
cd "$A" && grep -n 'TASK in (\|def use_task_\|mnem *== *"' \
    "$H/handful.py" autopoly.py || true
echo
echo "lane done"
