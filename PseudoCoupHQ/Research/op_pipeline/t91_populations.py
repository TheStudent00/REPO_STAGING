#!/usr/bin/env python3
"""t91_populations.py -- THE TWO POPULATIONS TASK 91 RE-GATES, read off
the artifact that recorded them rather than off any report's prose.

WHAT THIS FILE DOES.  log 153 section 1.2 states four states over one
population of 30,436 units: 23,132 proved on at least one route, 415
DISPROVED and withdrawn, 5,602 undecided on both routes, 1,287 with no
term at all.  Those four numbers were computed by `audit53.py` from
`layer4c_terms_{c,cpp,go,rust,swift}.json`, `layer4c_interp.json` and
`layer4c_regen_store/*.json`.  This file recomputes them from the SAME
artifacts with the SAME rule audit53 used, and writes the unit NAMES of
each of the four buckets, so the re-gate of task 91 joins to log 153's
own populations unit by unit and never by a retyped total.

THE RULE, copied from `audit53.section_one_and_two` rather than
restated: a record with `term_built` false is `no term`; otherwise
`PROVED_EQUAL` on either route is `proved`, `DISPROVED` on either route
is `withdrawn` (and a record that is both is a contradiction, counted
and named), and anything else is `undecided`.

READS ONLY.  `layer4c*` and `audit53.py` are superseded records of task
53 and are not edited by this file.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

No operator token appears in this file.  A unit is named by its own
machine-form identity (`<language>/<unit id>`); nothing is grouped,
paired or selected by any spelling.

Coding discipline (the owner's ruling): no compound one-liner statements.

usage:
  t91_populations.py            writes t91_populations.json
"""

import collections
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

LANGS = ("c", "cpp", "go", "rust", "swift")
OUT = os.path.join(HERE, "t91_populations.json")


def documents():
    """every task-53 verdict document, with the population it holds.
    The same list `audit53.documents('layer4c')` builds."""
    out = []
    for lang in LANGS:
        path = os.path.join(HERE, "layer4c_terms_%s.json" % lang)
        if os.path.exists(path):
            out.append(("original", path))
    path = os.path.join(HERE, "layer4c_interp.json")
    if os.path.exists(path):
        out.append(("interpreter", path))
    pattern = os.path.join(HERE, "layer4c_regen_store", "*.json")
    for path in sorted(glob.glob(pattern)):
        out.append(("regenerated", path))
    return out


def state_of(record):
    """audit53's own four-way rule, reproduced."""
    if not record.get("term_built"):
        return "no term"
    ship = record.get("gate_ship_verdict")
    text = record.get("gate_textorder_verdict")
    proved = "PROVED_EQUAL" in (ship, text)
    disproved = "DISPROVED" in (ship, text)
    if disproved:
        return "withdrawn"
    if proved:
        return "proved"
    return "undecided"


def build():
    buckets = collections.defaultdict(list)
    per_population = collections.defaultdict(collections.Counter)
    reasons = {}
    where = {}
    contradictions = []
    for population, path in documents():
        document = json.load(open(path))
        for name, record in document["units"].items():
            ship = record.get("gate_ship_verdict")
            text = record.get("gate_textorder_verdict")
            if "PROVED_EQUAL" in (ship, text) and \
                    "DISPROVED" in (ship, text):
                contradictions.append(name)
            state = state_of(record)
            buckets[state].append(name)
            per_population[population][state] += 1
            per_population[population]["units"] += 1
            where[name] = population
            reasons[name] = {
                "ship_verdict": ship,
                "ship_detail": record.get("gate_ship_detail"),
                "text_verdict": text,
                "text_detail": record.get("gate_textorder_detail"),
            }
    return buckets, per_population, reasons, where, contradictions


def main():
    buckets, per_population, reasons, where, contradictions = build()
    total = 0
    for state in buckets:
        total = total + len(buckets[state])
    document = {
        "meta": {
            "generated_by": "t91_populations.py",
            "read_from": ("layer4c_terms_<lang>.json, "
                          "layer4c_interp.json, "
                          "layer4c_regen_store/*.json"),
            "the_rule": ("audit53.section_one_and_two's own four-way "
                         "rule, reproduced"),
            "log_153_section_1_2": {
                "proved": 23132,
                "withdrawn": 415,
                "undecided": 5602,
                "no term": 1287,
                "units": 30436,
            },
        },
        "counts": {},
        "per_population": {},
        "contradictions": sorted(contradictions),
        "units_in_all": total,
        "buckets": {},
        "task_53_reason": reasons,
        "population_of": where,
    }
    for state in sorted(buckets):
        document["counts"][state] = len(buckets[state])
        document["buckets"][state] = sorted(buckets[state])
    for population in sorted(per_population):
        document["per_population"][population] = \
            dict(per_population[population])
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    print("wrote %s" % OUT)
    print("")
    print("THE FOUR BUCKETS, against log 153 section 1.2")
    print("  %-12s %10s %10s %8s" % ("state", "log 153", "here",
                                     "delta"))
    expected = document["meta"]["log_153_section_1_2"]
    for state in ("proved", "withdrawn", "undecided", "no term"):
        here = document["counts"].get(state, 0)
        there = expected[state]
        print("  %-12s %10d %10d %+8d" % (state, there, here,
                                          here - there))
    print("  %-12s %10d %10d %+8d" % ("units", expected["units"],
                                      total, total - expected["units"]))
    print("")
    print("  contradictions (proved on one route, disproved on the "
          "other): %d" % len(contradictions))
    print("")
    print("PER POPULATION")
    for population in sorted(document["per_population"]):
        counts = document["per_population"][population]
        print("  %s" % population)
        for state in ("proved", "withdrawn", "undecided", "no term",
                      "units"):
            print("    %-12s %8d" % (state, counts.get(state, 0)))


if __name__ == "__main__":
    main()
