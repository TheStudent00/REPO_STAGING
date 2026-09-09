#!/usr/bin/env python3
"""audit53.py -- TASK 53's figures, computed rather than asserted.

WHAT IS PRINTED, in order:

  1. PER POPULATION -- units, term built / no term built, proved on
     route one, proved on route two, proved on at least one route,
     disproved (withdrawn), undecided on both.  These are the same
     lines audit48b.py printed, so the two pages compare line for
     line against log 147 section 13.5.
  2. LAYER 3 AGAINST LAYER 5 -- distinct wrapped texts against
     distinct normalized texts, per population, over every unit with
     a layer-5 text and again over the proved units only.
  3. THE CENSUS DELTA BY CAUSE -- name_census3.json (canon37) against
     name_census4.json (canon38), grouped by the RECORDED REASON each
     entry carries, never by the producer's spelling.
  4. THE DIVISION-REMAINDER FINDING -- computed: which route-one
     disproofs read the remainder half.

THE CAUSE GROUPING IS EVIDENCE-KEYED.  Each census entry carries the
sentence saying why its producer has no term.  The grouping below
matches on that recorded sentence.  It does not read the producer's
mnemonic and it does not read any token: the candidate set comes from
the artifact's own recorded reason.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

No operator token appears in this file.

Coding discipline: no compound one-liner statements.
"""

import collections
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

CAUSES = (
    ("the machine stack has no block",
     "moves a value to or from the machine stack"),
    ("the implicit destination",
     "writes the quotient and the remainder into"),
    ("the implicit destination",
     "writes the wide product into registers it does not name"),
    ("the x87 stack has no rows",
     "on the x87 register stack"),
    ("an unconditional transfer is not a flag reader",
     "an unconditional transfer reads no flags"),
    ("the flags the setter left are not in the ledger",
     "left flags this file could not build"),
    ("the flags the setter left are not in the ledger",
     "no flag-setting arch opcode precedes"),
    ("the second byte of a register has no row",
     "names the SECOND byte of a register"),
    ("this opcode reads a carry no earlier opcode set",
     "reads the carry flag"),
    ("no opcode in the body writes the answer register",
     "no arch opcode in this body writes the answer"),
    ("the x87 extended value has no return path to the answer bits",
     "x87 extended value"),
    ("the comparison's own row is there and its sides are not",
     "could not be built into flags this file models"),
    ("the machine stack held this value before the unit was entered",
     "held before the unit was entered"),
)


def cause_of(reason):
    for label, marker in CAUSES:
        if marker in reason:
            return label
    return "not yet grouped: %s" % reason[:60]


def documents(stem):
    out = []
    for lang in ("c", "cpp", "go", "rust", "swift"):
        path = os.path.join(HERE, "%s_terms_%s.json" % (stem, lang))
        if os.path.exists(path):
            out.append(("original", path))
    path = os.path.join(HERE, "%s_interp.json" % stem)
    if os.path.exists(path):
        out.append(("interpreter", path))
    for path in sorted(glob.glob(os.path.join(
            HERE, "%s_regen_store" % stem, "*.json"))):
        out.append(("regenerated", path))
    return out


def section_one_and_two():
    per = collections.defaultdict(collections.Counter)
    contradictions = []
    distinct3 = collections.defaultdict(set)
    distinct5 = collections.defaultdict(set)
    all3 = collections.defaultdict(set)
    all5 = collections.defaultdict(set)
    for population, path in documents("layer4c"):
        document = json.load(open(path))
        for name, record in document["units"].items():
            counter = per[population]
            counter["units"] += 1
            ship = record["gate_ship_verdict"]
            text = record["gate_textorder_verdict"]
            if record.get("layer5_normalized_text") is not None:
                all3[population].add(record["layer3_wrapped_text"])
                all5[population].add(record["layer5_normalized_text"])
            if not record.get("term_built"):
                counter["no term built"] += 1
                continue
            counter["term built"] += 1
            proved = "PROVED_EQUAL" in (ship, text)
            disproved = "DISPROVED" in (ship, text)
            if proved and disproved:
                contradictions.append((name, ship, text))
            if disproved:
                counter["term DISPROVED -- withdrawn"] += 1
            elif proved:
                counter["term proved on at least one route"] += 1
            else:
                counter["term undecided on both routes"] += 1
            if ship == "PROVED_EQUAL":
                counter["proved on route one (the ship simulation)"] += 1
            if text == "PROVED_EQUAL":
                counter["proved on route two (the text-order walk)"] += 1
            if record.get("layer5_equals_layer3"):
                counter["layer 5 identical to layer 3"] += 1
            if not disproved:
                if proved:
                    distinct3[population].add(
                        record["layer3_wrapped_text"])
                    distinct5[population].add(
                        record["layer5_normalized_text"])
    grand = collections.Counter()
    for population in sorted(per):
        print("POPULATION: %s" % population)
        for key in sorted(per[population]):
            print("  %-48s %7d" % (key, per[population][key]))
            grand[key] += per[population][key]
        print("  %-48s %7d"
              % ("distinct layer-3 texts, every unit with a term",
                 len(all3[population])))
        print("  %-48s %7d"
              % ("distinct layer-5 texts, every unit with a term",
                 len(all5[population])))
        print("  %-48s %7d"
              % ("distinct layer-3 texts, proved units only",
                 len(distinct3[population])))
        print("  %-48s %7d"
              % ("distinct layer-5 texts, proved units only",
                 len(distinct5[population])))
        print("")
    print("ALL THREE POPULATIONS")
    for key in sorted(grand):
        print("  %-48s %7d" % (key, grand[key]))
    print("")
    print("CONSISTENCY -- units proved on one route and disproved on "
          "the other: %d" % len(contradictions))
    for item in contradictions[:20]:
        print("  %s" % (item,))
    print("")


def census_rows(path):
    if not os.path.exists(path):
        return None
    census = json.load(open(path))
    by_cause = collections.Counter()
    units_by_cause = collections.defaultdict(set)
    producers = collections.Counter()
    for entry in census["entries"]:
        label = cause_of(entry["cannot_model_because"])
        by_cause[label] += entry["rows_blocked"]
        units_by_cause[label].update(entry["units_blocked"])
        producers[label] += 1
    return census, by_cause, units_by_cause, producers


def section_three():
    print("THE CENSUS DELTA BY CAUSE -- name_census3 (canon37) against "
          "name_census4 (canon38)")
    print("")
    before = census_rows(os.path.join(HERE, "name_census3.json"))
    after = census_rows(os.path.join(HERE, "name_census4.json"))
    if before is None or after is None:
        print("  one of the two census files is not on disk yet")
        return
    labels = sorted(set(before[1]) | set(after[1]))
    print("%-58s %8s %8s %8s" % ("cause (the artifact's own recorded "
                                 "reason)", "rows 3", "rows 4",
                                 "delta"))
    print("-" * 88)
    for label in labels:
        older = before[1].get(label, 0)
        newer = after[1].get(label, 0)
        print("%-58s %8d %8d %8d"
              % (label[:58], older, newer, newer - older))
    print("-" * 88)
    print("%-58s %8d %8d %8d"
          % ("TOTAL ROWS", sum(before[1].values()),
             sum(after[1].values()),
             sum(after[1].values()) - sum(before[1].values())))
    print("%-58s %8d %8d %8d"
          % ("DISTINCT PRODUCERS", len(before[0]["entries"]),
             len(after[0]["entries"]),
             len(after[0]["entries"]) - len(before[0]["entries"])))
    units_before = set()
    for entry in before[0]["entries"]:
        units_before.update(entry["units_blocked"])
    units_after = set()
    for entry in after[0]["entries"]:
        units_after.update(entry["units_blocked"])
    print("%-58s %8d %8d %8d"
          % ("UNITS CARRYING AT LEAST ONE SUCH ROW", len(units_before),
             len(units_after), len(units_after) - len(units_before)))
    call_cause = after[0]["answer_produced_by_a_library_call"]
    print("")
    print("THE NEW CAUSE, reported rather than fixed")
    print("  %-56s %8s %8d"
          % ("answer produced by a library call", "--",
             call_cause["unit_count"]))
    print("  %s" % call_cause["cannot_model_because"])
    for one in call_cause["callees"]:
        print("      %-44s %d unit(s)" % (one["callee"],
                                          one["unit_count"]))
    print("")


def section_four():
    """the route-one disproofs, split by which half of the division
    the answer reads -- computed off the ledger's own `written_half`
    field, never off a mnemonic."""
    print("THE ROUTE-ONE DISPROOFS, split by the ledger's own "
          "`written_half` field")
    halves = collections.Counter()
    examples = collections.defaultdict(list)
    ledgers = {}
    for lang in ("c", "cpp", "go", "rust", "swift"):
        path = os.path.join(HERE, "canon38_wrapped_%s.json" % lang)
        if not os.path.exists(path):
            continue
        document = json.load(open(path))
        for name, unit in document["units"].items():
            if "ledger" in unit:
                ledgers[name] = unit["ledger"]
    for path in sorted(glob.glob(os.path.join(
            HERE, "canon38_regen_store", "*.json"))):
        document = json.load(open(path))
        for name, unit in document["units"].items():
            if "ledger" in unit:
                ledgers[name] = unit["ledger"]
    for population, path in documents("layer4c"):
        document = json.load(open(path))
        for name, record in document["units"].items():
            if record.get("gate_ship_verdict") != "DISPROVED":
                continue
            rows = ledgers.get(name) or []
            by_row = {}
            for row in rows:
                by_row[row["row"]] = row
            # walk OUT-0's own lineage and collect the halves it
            # actually reaches; a half written into a row the answer
            # never reads is not part of this answer.
            reached = []
            seen = set()
            stack = ["OUT-0"]
            while stack:
                here = stack.pop()
                if here in seen:
                    continue
                seen.add(here)
                row = by_row.get(here)
                if row is None:
                    continue
                written = row["produced_by"].get("writes_which_half")
                if written is not None:
                    if written not in reached:
                        reached.append(written)
                stack.extend(row["operands"])
            if not reached:
                half = "the answer's lineage reaches no written half"
            else:
                half = " / ".join(sorted(reached))
            halves[half] += 1
            if len(examples[half]) < 3:
                examples[half].append(name)
    total = sum(halves.values())
    print("  route-one disproofs in all: %d" % total)
    for half in sorted(halves, key=lambda one: -halves[one]):
        print("    %-50s %6d   %s"
              % (half, halves[half], ", ".join(examples[half])))
    print("")


def section_five():
    """THE ADDED ROWS, AND WHETHER THEY ARE GATE-PROVED.  Counted off
    the ledger's own block names -- STACK and X87 -- never off a
    mnemonic."""
    print("THE ROWS RULING 2 ADDED, and the gate's verdict on the "
          "units carrying them")
    ledgers = {}
    for lang in ("c", "cpp", "go", "rust", "swift"):
        path = os.path.join(HERE, "canon38_wrapped_%s.json" % lang)
        if not os.path.exists(path):
            continue
        document = json.load(open(path))
        for name, unit in document["units"].items():
            if "ledger" in unit:
                ledgers[name] = unit["ledger"]
    path = os.path.join(HERE, "canon38_interp.json")
    if os.path.exists(path):
        document = json.load(open(path))
        for name, unit in document["units"].items():
            if "ledger" in unit:
                ledgers[name] = unit["ledger"]
    for path in sorted(glob.glob(os.path.join(
            HERE, "canon38_regen_store", "*.json"))):
        document = json.load(open(path))
        for name, unit in document["units"].items():
            if "ledger" in unit:
                ledgers[name] = unit["ledger"]
    tally = collections.Counter()
    for population, path in documents("layer4c"):
        document = json.load(open(path))
        for name, record in document["units"].items():
            rows = ledgers.get(name) or []
            blocks = set()
            for row in rows:
                blocks.add(row["block"])
            ship = record.get("gate_ship_verdict")
            text = record.get("gate_textorder_verdict")
            proved = "PROVED_EQUAL" in (ship, text)
            disproved = "DISPROVED" in (ship, text)
            for block in ("STACK", "X87"):
                if block not in blocks:
                    continue
                tally["%s: units carrying such a row" % block] += 1
                if record.get("term_built"):
                    tally["%s: units with an OUT-0 term" % block] += 1
                if proved:
                    tally["%s: units proved on a route" % block] += 1
                elif disproved:
                    tally["%s: units disproved" % block] += 1
                else:
                    tally["%s: units undecided on both routes"
                          % block] += 1
    for key in sorted(tally):
        print("  %-52s %7d" % (key, tally[key]))
    print("")


def section_six():
    """THE TRANSITION, unit by unit: task 48's record (canon37) against
    task 53's (canon38)."""
    print("THE TRANSITION PER UNIT -- task 48's layer-4 record against "
          "task 53's")
    before = {}
    for population, path in documents("layer4b"):
        document = json.load(open(path))
        for name, record in document["units"].items():
            before[name] = record
    if not before:
        print("  task 48's artifacts are not on disk")
        return

    def state_of(record):
        if not record.get("term_built"):
            return "no term"
        ship = record.get("gate_ship_verdict")
        text = record.get("gate_textorder_verdict")
        if "DISPROVED" in (ship, text):
            return "withdrawn"
        if "PROVED_EQUAL" in (ship, text):
            return "proved"
        return "undecided"

    moves = collections.Counter()
    examples = collections.defaultdict(list)
    unmatched = 0
    for population, path in documents("layer4c"):
        document = json.load(open(path))
        for name, record in document["units"].items():
            older = before.get(name)
            if older is None:
                unmatched += 1
                continue
            key = (state_of(older), state_of(record))
            moves[key] += 1
            if len(examples[key]) < 3:
                examples[key].append(name)
    print("  %-14s %-14s %8s   %s"
          % ("task 48", "task 53", "units", "examples"))
    for key in sorted(moves, key=lambda one: -moves[one]):
        print("  %-14s %-14s %8d   %s"
              % (key[0], key[1], moves[key], ", ".join(examples[key])))
    print("  units in task 53 with no task-48 record: %d" % unmatched)
    print("")


def main():
    section_one_and_two()
    section_three()
    section_four()
    section_five()
    section_six()


if __name__ == "__main__":
    main()
