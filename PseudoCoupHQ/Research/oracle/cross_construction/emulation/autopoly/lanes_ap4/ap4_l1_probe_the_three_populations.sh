#!/usr/bin/env bash
# ap4_l1_probe_the_three_populations.sh -- task ap4: what the three
# populations the brief names actually hold, asked of the objects
# before one line of a fix is written.
#
#  [1] THE CELLS FILE: task ap3's copied here as `autopoly4_cells.json`
#      and its counts re-measured on this machine.
#  [2] THE DERIVED ARRIVAL (change 1): task ap3's 38 places over 12
#      cells whose cause is `the IN rows cannot be aligned`.  Per cell:
#      the families the CELL reads, the families the EMULATION reads,
#      the corpus row's own body text, and which of the cell's arrivals
#      the corpus always produces by a zero-operand setup instruction.
#  [3] THE IDENTITY (change 3): every run whose cause is `this unit
#      record carries no body`, with its carved body text LITERAL, so
#      an empty body is told from an x87 body by the object.
#  [4] THE x87 STACK (change 2): the canonical form asked for one x87
#      c body, its refusal LITERAL, and what the ledger already names
#      for an x87 row.
#
# MEMORY BOUND: 6 GB resident, named abort ABORT_MEMORY_AP4.  This lane
# reads `autopoly4_cells.json` (2 MB) and task ap3's store (5 MB) and
# runs no gate call; the peak is printed at the end.
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
CELLS4 = os.path.join(HERE, "autopoly", "autopoly4_cells.json")
print("[1/4] THE CELLS FILE, re-measured on this machine")
cells = A.read_json(CELLS4)
print("   cells on autopoly4_cells.json: %d" % len(cells["asked"]))
total = 0
for record in cells["asked"]:
    total = total + record["attested_ledger_rows"]
print("   attested ledger rows over the outer set: %d" % total)
print("   identical to autopoly3_cells.json: %s"
      % (A.read_json(A.CELLS) == cells))
guard("after the cells file")

runs = A.read_runs(A.RUNS)
print("")
print("[2/4] THE DERIVED ARRIVAL -- task ap3's `the IN rows cannot be "
      "aligned`")
print("   the widening tables the brief names, LITERAL:")
print("      reference.SPREAD_SIGN      = %r"
      % sorted(R.SPREAD_SIGN))
print("      reference.ACCUMULATOR_WIDEN = %r"
      % sorted(R.ACCUMULATOR_WIDEN))
print("")
group = {}
places_declined = 0
for run in runs:
    for place in (run.get("places") or []):
        check = place.get("check") or {}
        reason = check.get("reason") or ""
        if "the IN rows cannot be aligned" not in reason:
            continue
        places_declined = places_declined + 1
        key = (run["mnem"], run["shape"], run["key_width"])
        entry = group.setdefault(key, {"langs": set(), "places": {},
                                       "run": run})
        entry["langs"].add(run["lang"])
        entry["places"].setdefault(place.get("writes"), set()).add(
            run["lang"])
print("   places the gate declined on the IN-row alignment: %d"
      % places_declined)
print("   distinct cells: %d" % len(group))
print("")
print("| cell | targets | the corpus row's own body | the families "
      "the CELL reads | the families the EMULATION reads | the places |")
print("|---|---|---|---|---|---|")
for key in sorted(group):
    entry = group[key]
    run = entry["run"]
    held = {"mnem": key[0], "shape": key[1], "key_width": key[2]}
    row = H.chosen_row(cells, key, held)
    line = (row or {}).get("line")
    body = (row or {}).get("body_text")
    cell_families = None
    body_families = None
    for place in (run.get("places") or []):
        check = place.get("check") or {}
        if "cannot be aligned" not in (check.get("reason") or ""):
            continue
        cell_families = place.get("families")
        params = place.get("params") or []
        try:
            body_families = H.expected_families(run["lang"], params)
        except Exception as problem:
            body_families = "%s" % problem
        break
    print("| `%s` %s %s | %s | `%s` | %s | %s | %s |"
          % (key[0], key[1], key[2],
             ",".join(sorted(entry["langs"])),
             line or body or "-- no row --",
             cell_families, body_families,
             ", ".join(sorted(entry["places"]))))
guard("after the derived arrivals")

print("")
print("   THE CELLS' OWN TERMS, per place, so the relation between two "
      "arrivals is read off the object:")
for key in sorted(group):
    held = {"mnem": key[0], "shape": key[1], "key_width": key[2]}
    row = H.chosen_row(cells, key, held)
    if row is None:
        print("   `%s` %s %s -- no row" % key)
        continue
    places, flags = H.terms_of_row(row)
    print("")
    print("   `%s` %s %s   row %s   line `%s`"
          % (key[0], key[1], key[2], row.get("row_id"),
             row.get("line")))
    records = H.places_as_records(row, places, flags, [])
    for record in records:
        term = record.get("term")
        if term is None:
            continue
        print("      place `%s` %d bits, families %s"
              % (record["writes"], record["bits"],
                 record.get("families")))
        print("         %s" % H.T.one_line(term)[:400])
guard("after the terms")

print("")
print("[3/4] THE IDENTITY -- every run of `this unit record carries no "
      "body`")
empty = []
for run in runs:
    cause = A.cause_of(run)
    if cause is None:
        continue
    if "carries no body" not in cause:
        continue
    empty.append(run)
print("   runs: %d" % len(empty))
shapes = {}
for run in empty:
    place = A.the_weakest_place(run)
    body = (place or {}).get("body_text")
    shapes.setdefault(body, []).append(
        (run["mnem"], run["shape"], run["key_width"], run["lang"]))
print("")
print("| the carved body, LITERAL | runs | the cells |")
print("|---|---|---|")
for body in sorted(shapes, key=lambda b: (-len(shapes[b]), str(b))):
    names = []
    for one in shapes[body][:6]:
        names.append("`%s` %s %s/%s" % one)
    if len(shapes[body]) > 6:
        names.append("... %d more" % (len(shapes[body]) - 6))
    print("| `%s` | %d | %s |" % (body, len(shapes[body]),
                                  "; ".join(names)))
print("")
print("   ONE EMPTY-BODY RUN IN FULL, its place record:")
for run in empty:
    place = A.the_weakest_place(run)
    if (place or {}).get("body_text") not in (None, "", "ret"):
        continue
    print("      %s %s %s -> %s" % (run["mnem"], run["shape"],
                                    run["key_width"], run["lang"]))
    print("      writes            %s" % place.get("writes"))
    print("      bits              %s" % place.get("bits"))
    print("      families          %s" % place.get("families"))
    print("      home              %s" % place.get("home"))
    print("      params            %s" % place.get("params"))
    print("      body_text         %r" % place.get("body_text"))
    print("      landing           %s"
          % (place.get("landing") or {}).get("verdict"))
    print("      the source, LITERAL:")
    for line in (place.get("source") or "").rstrip("\n").split("\n"):
        print("         %s" % line)
    break
guard("after the identity")

print("")
print("[4/4] THE x87 STACK -- the canonical form asked for one x87 c "
      "body")
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
    print("   %s %s %s -> c, place `%s`"
          % (run["mnem"], run["shape"], run["key_width"], run["lang"],
             place.get("writes")))
    print("   the carved body, LITERAL: %s" % place.get("body_text"))
    recorded = E.recorded_facts("c/probe", "probe",
                                place["body_bytes"].split(),
                                place["body_text"].split("; "))
    print("   recorded_facts result_family: %r"
          % recorded.get("result_family"))
    print("   recorded_facts result_width:  %r"
          % recorded.get("result_width"))
    print("   recorded_facts arrival_families: %r"
          % recorded.get("arrival_families"))
    print("   recorded_facts entry_contract:   %r"
          % recorded.get("entry_contract"))
    canon = CF.render_one(shared["form"], shared["gate"], recorded)
    print("   canonical_form outcome:  %r" % canon.get("outcome"))
    print("   canonical_form refusal_cause: %r"
          % canon.get("refusal_cause"))
    print("   canonical_form refusal:  %r" % canon.get("refusal"))
print("")
print("   the ledger's own x87 vocabulary, LITERAL:")
print("      ledger.BLOCK_ORDER        = %r" % (L.BLOCK_ORDER,))
print("      ledger.X87_POSITIONS      = %r" % L.X87_POSITIONS)
print("      ledger.X87_LOADS          = %r" % sorted(L.X87_LOADS))
print("      ledger.X87_STORES_POP     = %r" % sorted(L.X87_STORES_POP))
print("   what `answer_registers_of_body` says about that body:")
if found is not None:
    reading = L.answer_registers_of_body(
        L.split_lines(place["body_text"]))
    for name in sorted(reading):
        print("      %-24s %r" % (name, reading[name]))
print("")
print("peak resident: %d kB" % guard("end"))
PY
echo "done"
