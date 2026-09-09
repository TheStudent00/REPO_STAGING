#!/usr/bin/env bash
# ap4_l2_probe_the_two_sides_and_the_x87_form.sh -- task ap4: the SECOND
# probe, and the part of the first that stopped on its own format string.
#
#  [1] THE TWO SIDES OF EVERY DECLINED PLACE.  For each of the 38 places
#      task ap3's gate declined on the IN-row alignment: the route the
#      run took, the emulation's own parameter plan, the emulation's
#      rendered or matched source, its carved body, and the cell's term
#      -- so the relation between the cell's arrivals and the
#      emulation's is read off the objects rather than reasoned about.
#  [2] THE x87 FORM: what `emulate.recorded_facts` says about an x87 c
#      body, what `canonical_form.render_one` then refuses, and the
#      ledger's own x87 vocabulary.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP4.  Reads the
# cells file and task ap3's store; runs no gate call.
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
runs = A.read_runs(A.RUNS)

print("[1/2] THE TWO SIDES of every place the gate declined on the "
      "IN-row alignment")
declined = []
for run in runs:
    for place in (run.get("places") or []):
        check = place.get("check") or {}
        if "the IN rows cannot be aligned" not in (check.get("reason")
                                                   or ""):
            continue
        declined.append((run, place))
print("   places: %d" % len(declined))
print("")
print("| cell | lang | place | route | the cell's arrivals | the "
      "emulation's parameter plan | the emulation's arrivals |")
print("|---|---|---|---|---|---|---|")
for run, place in declined:
    params = place.get("params") or []
    plan = []
    for param in params:
        plan.append("%s:%s/%s" % (param.get("name"),
                                  param.get("holder"),
                                  param.get("family")))
    try:
        body = H.expected_families(run["lang"], params)
    except Exception as problem:
        body = "%s" % problem
    print("| `%s` %s %s | %s | `%s` | %s | %s | %s | %s |"
          % (run["mnem"], run["shape"], run["key_width"], run["lang"],
             place.get("writes"), run.get("route"),
             place.get("families"), ", ".join(plan) or "--", body))
guard("after the table")

print("")
print("   ONE RUN PER CELL IN FULL -- the source the emulation is, its "
      "carved body, and the cell's own term:")
seen = set()
for run, place in declined:
    key = (run["mnem"], run["shape"], run["key_width"])
    if key in seen:
        continue
    seen.add(key)
    print("")
    print("== `%s` %s %s -> %s, place `%s`, route %s"
          % (key[0], key[1], key[2], run["lang"], place.get("writes"),
             run.get("route")))
    found = run.get("primitive") or {}
    row = found.get("row")
    if row is not None:
        print("   the matched primitive row, LITERAL:")
        print("      body_text : %s" % row.get("body_text"))
        print("      rule      : %s" % found.get("rule"))
        print("      member    : %s" % found.get("member"))
    print("   the emulation's source, LITERAL:")
    for line in (place.get("source") or "-- none --").rstrip(
            "\n").split("\n"):
        print("      %s" % line)
    print("   the carved body, LITERAL: %s" % place.get("body_text"))
    print("   the cell's term for this place, LITERAL:")
    print("      %s" % (place.get("text") or "")[:600])
    check = place.get("check") or {}
    print("   the gate's reason, LITERAL: %s" % check.get("reason"))
    print("   the body's own arrival families read off the canonical "
          "form: %s" % check.get("arrival_families_read_off_the_body"))
guard("after the full runs")

print("")
print("[2/2] THE x87 FORM")
import canonical_form as CF
import ledger as L
shared = H.build_shared()
found = None
for run in runs:
    if run["lang"] != "c":
        continue
    for place in (run.get("places") or []):
        home = (place.get("home") or {}).get("family")
        if not E.is_an_x87_arrival(home):
            continue
        if not place.get("compiled"):
            continue
        found = (run, place)
        break
    if found is not None:
        break
if found is None:
    print("   no compiled x87 c place on task ap3's store")
else:
    run, place = found
    print("   `%s` %s %s -> %s, place `%s`"
          % (run["mnem"], run["shape"], run["key_width"], run["lang"],
             place.get("writes")))
    print("   the carved body, LITERAL: %s" % place.get("body_text"))
    print("   the emulation's source, LITERAL:")
    for line in (place.get("source") or "").rstrip("\n").split("\n"):
        print("      %s" % line)
    recorded = E.recorded_facts("c/probe", "probe",
                                place["body_bytes"].split(),
                                place["body_text"].split("; "))
    for name in ("result_family", "result_width", "arrival_families",
                 "entry_contract"):
        print("   recorded_facts %-18s %r" % (name, recorded.get(name)))
    canon = CF.render_one(shared["form"], shared["gate"], recorded)
    for name in ("outcome", "refusal_cause", "refusal"):
        print("   canonical_form %-18s %r" % (name, canon.get(name)))
    print("   what `answer_registers_of_body` says about that body:")
    reading = L.answer_registers_of_body(
        L.split_lines(place["body_text"]))
    for name in sorted(reading):
        print("      %-24s %r" % (name, reading[name]))
    print("   what `answer_home_from_real` says:")
    import canon10_behaviour_check as BC10
    print("      %r" % (BC10.answer_home_from_real(
        L.split_lines(place["body_text"])),))
print("")
print("   the ledger's own x87 vocabulary, LITERAL:")
print("      ledger.BLOCK_ORDER    = %r" % (L.BLOCK_ORDER,))
print("      ledger.X87_POSITIONS  = %r" % L.X87_POSITIONS)
print("      ledger.X87_LOADS      = %r" % sorted(L.X87_LOADS))
print("      ledger.X87_STORES_POP = %r" % sorted(L.X87_STORES_POP))
print("      canonical_form's refusal texts, LITERAL:")
import canonical_form as CF2
print("         %r" % (CF2.REFUSAL_CAUSES
                       if hasattr(CF2, "REFUSAL_CAUSES") else
                       "not a module attribute"))
print("")
print("peak resident: %d kB" % guard("end"))
PY
echo "done"
