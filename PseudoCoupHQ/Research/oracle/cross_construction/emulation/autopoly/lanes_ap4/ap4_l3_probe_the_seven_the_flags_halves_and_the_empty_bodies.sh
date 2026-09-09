#!/usr/bin/env bash
# ap4_l3_probe_the_seven_the_flags_halves_and_the_empty_bodies.sh --
# task ap4: the THIRD probe, and it is what change 1 is written against.
#
#  [1] THE SEVEN PLACES whose cell really does read a different NUMBER
#      of arrivals from the emulation (task ap3's 38 minus the 31 that
#      are a HALF of a flags place).  Per place: the cell's own row and
#      its `line`, the matched corpus row's body, which line of that
#      body classifies to the cell, and what the reference simulator
#      leaves in every register when the body's own setup is run before
#      it -- which is the relation between the two sides' arrivals,
#      read off the reference rather than reasoned about.
#  [2] THE 31 FLAGS HALVES: every place named `flags.*` on task ap3's
#      store, its route and its verdict, so what the driver's own
#      primitive-flags rule already refuses when the place is NOT
#      halved can be measured on the halves.
#  [3] THE EMPTY BODIES: every run whose carved body is `ret` alone,
#      with the place, its families, its home and its parameter plan.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP4.
set -euo pipefail
cd PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
python3 - <<'PY'
import os
import resource
import sys

HERE = "PseudoCoupHQ/Research/oracle/cross_construction/emulation"
sys.path.insert(0, os.path.join(HERE, "handful"))
sys.path.insert(0, os.path.join(HERE, "autopoly"))
sys.path.insert(0, HERE)
import z3
import emulate as E
import handful as H
import reference as R
import model_table as MTAB
import single_opcode_units as SOU
import autopoly3 as A

ABORT_KB = 6 * 1024 * 1024


def peak():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def guard(where):
    got = peak()
    if got > ABORT_KB:
        raise SystemExit("ABORT_MEMORY_AP4: %d kB at %s" % (got, where))
    return got


A.use_task_ap3()
MTAB._install_gpr_widths()
cells = A.read_json(A.CELLS)
runs = A.read_runs(A.RUNS)

declined = []
for run in runs:
    for place in (run.get("places") or []):
        check = place.get("check") or {}
        if "the IN rows cannot be aligned" not in (check.get("reason")
                                                   or ""):
            continue
        declined.append((run, place))

print("[1/3] THE PLACES THAT ARE NOT A HALF OF A FLAGS PLACE")
seven = []
halves = []
for run, place in declined:
    if (place.get("writes") or "").split(".")[0] == "flags":
        halves.append((run, place))
    else:
        seven.append((run, place))
print("   declined places: %d" % len(declined))
print("   of those, a half of a flags place: %d" % len(halves))
print("   of those, not a flags place at all: %d" % len(seven))
print("")
for run, place in seven:
    key = (run["mnem"], run["shape"], run["key_width"])
    held = {"mnem": key[0], "shape": key[1], "key_width": key[2]}
    row = H.chosen_row(cells, key, held)
    print("== `%s` %s %s -> %s, place `%s`, route %s"
          % (key[0], key[1], key[2], run["lang"], place.get("writes"),
             run.get("route")))
    print("   the cell's row, its keys: %s" % sorted(row or {}))
    for name in ("row_id", "line", "mnem", "texts", "shape",
                 "key_width", "preseeded", "operand_form"):
        if row is not None and name in row:
            print("      row[%-12s] = %r" % (name, row[name]))
    print("   the cell's families: %s" % place.get("families"))
    print("   the cell's term, LITERAL: %s" % (place.get("text") or "")[:300])
    found = run.get("primitive") or {}
    prow = found.get("row") or {}
    body = prow.get("body_text")
    print("   the matched corpus row's body, LITERAL: %s" % body)
    probe = found.get("probe") or {}
    print("   the probe's expression, LITERAL: %r"
          % probe.get("expression"))
    print("   the probe's arity/lhs/rhs: %r %r %r"
          % (probe.get("arity"), probe.get("lhs_rep"),
             probe.get("rhs_rep")))
    print("   the emulation's parameter plan: %s"
          % [(p.get("name"), p.get("holder"), p.get("bits"))
             for p in (place.get("params") or [])])
    if body is None:
        print("")
        continue
    lines = body.split("; ")
    stripped = SOU.strip_chaff(lines, "narrow")
    print("   the body stripped by task o2's narrow rule: %s"
          % "; ".join(stripped))
    # WHERE THE CELL'S OWN INSTRUCTION IS, by the table's own classifier
    at = None
    for index, line in enumerate(stripped):
        mnem, operands = SOU.parse_insn(line)
        shape, width, cause = MTAB.classify_line(mnem, line, 0)
        marker = ""
        if mnem == key[0] and shape == key[1] and width == key[2]:
            at = index
            marker = "   <== the cell"
        print("      [%d] %-34s classifies to (%s, %s, %s)%s"
              % (index, line, mnem, shape, width, marker))
    if at is None:
        print("      the cell's own instruction is not in this body")
        print("")
        continue
    print("   THE REFERENCE RUN over the %d line(s) before it, on a "
          "fresh state:" % at)
    state = R.MachineState()
    stopped = None
    for line in stripped[:at]:
        try:
            R.REFERENCE.step(state, line)
        except Exception as problem:
            stopped = "%s: %s" % (type(problem).__name__, problem)
            break
    if stopped is not None:
        print("      the reference stopped: %s" % stopped)
    for family in sorted(state.registers):
        term = state.registers[family]
        if term is None:
            continue
        print("      %%%-5s = %s" % (family, H.T.one_line(term)[:160]))
    print("   the operands of the cell's own instruction in the body: "
          "%s" % (SOU.parse_insn(stripped[at])[1],))
    print("")
guard("after the seven")

print("")
print("[2/3] EVERY PLACE NAMED `flags.*` ON TASK ap3'S STORE")
counted = {}
for run in runs:
    for place in (run.get("places") or []):
        writes = place.get("writes") or ""
        if not writes.startswith("flags."):
            continue
        route = run.get("route")
        check = place.get("check") or {}
        verdict = check.get("outcome") or place.get("refusal_cause") \
            or "not rendered"
        counted.setdefault((route, verdict), []).append(
            (run["mnem"], run["shape"], run["key_width"], run["lang"],
             writes))
print("   places named `flags.*`: %d"
      % sum(len(v) for v in counted.values()))
print("")
print("| route | what the place says | places |")
print("|---|---|---|")
for key in sorted(counted, key=lambda k: (-len(counted[k]), str(k))):
    print("| %s | %s | %d |" % (key[0], key[1], len(counted[key])))
print("")
print("   the PROVED ones in full, because generalising the driver's "
      "own primitive-flags refusal to a half would move them:")
for key in sorted(counted, key=lambda k: str(k)):
    if key[0] not in ("primitive", "primitive+setup"):
        continue
    if key[1] not in ("PROVED_ON_SHIP",):
        continue
    for one in counted[key]:
        print("      `%s` %s %s / %s  place `%s`" % one)
print("")
print("   AND THE RUN-LEVEL QUESTION: of the runs holding a `flags.*` "
      "place on the primitive route, which are PROVED as a whole?")
proved_runs = 0
for run in runs:
    if run.get("route") not in ("primitive", "primitive+setup"):
        continue
    has = False
    for place in (run.get("places") or []):
        if (place.get("writes") or "").startswith("flags."):
            has = True
    if not has:
        continue
    if A.cause_of(run) is None:
        proved_runs = proved_runs + 1
        print("      PROVED: `%s` %s %s / %s"
              % (run["mnem"], run["shape"], run["key_width"],
                 run["lang"]))
print("   proved runs holding a `flags.*` place on the primitive "
      "route: %d" % proved_runs)
guard("after the flags halves")

print("")
print("[3/3] THE EMPTY BODIES")
empty = []
for run in runs:
    for place in (run.get("places") or []):
        if place.get("body_text") != "ret":
            continue
        empty.append((run, place))
print("   places whose carved body is `ret` alone: %d" % len(empty))
print("")
print("| cell | lang | place | route | the place's families | the "
      "place's home | the parameter plan | what it says now |")
print("|---|---|---|---|---|---|---|---|")
for run, place in empty:
    check = place.get("check") or {}
    says = check.get("outcome") or place.get("refusal_cause") or "--"
    plan = []
    for param in (place.get("params") or []):
        plan.append("%s:%s/%s bits %s"
                    % (param.get("name"), param.get("holder"),
                       param.get("family"), param.get("bits")))
    print("| `%s` %s %s | %s | `%s` | %s | %s | %s | %s | %s |"
          % (run["mnem"], run["shape"], run["key_width"], run["lang"],
             place.get("writes"), run.get("route"),
             place.get("families"), (place.get("home") or {}).get("family"),
             "; ".join(plan) or "--", says))
print("")
print("   ONE IN FULL:")
if empty:
    run, place = empty[0]
    print("      `%s` %s %s -> %s, place `%s`"
          % (run["mnem"], run["shape"], run["key_width"], run["lang"],
             place.get("writes")))
    print("      the cell's term, LITERAL: %s"
          % (place.get("text") or "")[:300])
    print("      the gate's reason, LITERAL: %s"
          % ((place.get("check") or {}).get("reason")))
    print("      the landing: %s"
          % ((place.get("landing") or {}).get("verdict")))
print("")
print("peak resident: %d kB" % guard("end"))
PY
echo "done"
