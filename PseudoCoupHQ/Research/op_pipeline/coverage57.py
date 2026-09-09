#!/usr/bin/env python3
"""coverage57.py -- how far the ONE reference walks, against how far
the superseded route walked, over the SAME population.

For every canon38 unit record this program walks the unit's OWN SHIP
BODY twice: once with `reference.Reference` (this lap's file) and once
with `canon10_behaviour_check.Sim10` behind `gate48.reference_answer`
(the route the gate calls today, unedited).  It counts, per population
and in total, how many bodies each side carries to an answer term and
how many each refuses, and it groups the refusals by their own stated
reason.

This is the ZERO-REGRESSION check in the ruled sense: a unit the
superseded route answered and this one refuses is a regression and is
listed by name.  No verdict is computed here and no unit is proved --
that is the gate's job (task 58).  This file measures REACH.

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

Every unit is walked; nothing selects, groups or pairs by any token.

usage:
  coverage57.py
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon10_behaviour_check as BC10                        # noqa: E402
import reference as REF                                       # noqa: E402

OUT_JSON = os.path.join(HERE, "coverage57.json")


def every_record():
    paths = []
    for lang in ("c", "cpp", "go", "rust", "swift"):
        paths.append(os.path.join(HERE,
                                  "canon38_wrapped_%s.json" % lang))
    paths.append(os.path.join(HERE, "canon38_interp.json"))
    paths.extend(sorted(glob.glob(
        os.path.join(HERE, "canon38_regen_store", "*.json"))))
    for path in paths:
        if not os.path.exists(path):
            continue
        document = json.load(open(path))
        for record in document.get("units", {}).values():
            yield record


def has_a_body(record):
    """canon38 REFUSED some units and left them with no body.  The
    superseded route walks `record.get("body_verbatim") or []`, so an
    empty body walks to completion and hands back the seed of the
    answer register -- an answer to nothing.  Those units are counted
    in their own column and kept out of the comparison rather than
    read as either side reaching an answer."""
    for line in record.get("body_verbatim") or []:
        text = line.split("!!")[0].strip()
        if text == "":
            continue
        if text.endswith(":"):
            continue
        return True
    return False


def superseded_answer(record):
    """`gate48.reference_answer`'s own body, reproduced here so this
    measurement does not edit gate48.py or canon10."""
    simulator = BC10.Sim10({}, "ship")
    simulator.answer_family = record.get("result_family")
    simulator.answer_width = record.get("result_width")
    lines = list(record.get("body_verbatim") or [])
    return simulator.answer_value(lines)


def short(reason):
    return reason[:110]


def main(argv):
    reference = REF.Reference()
    populations = {}
    reasons_now = {}
    reasons_before = {}
    regressions = []
    gained = 0
    for record in every_record():
        population = record.get("population") or "unknown"
        if population not in populations:
            populations[population] = {
                "units": 0,
                "reference_reaches_an_answer": 0,
                "reference_refuses": 0,
                "superseded_reaches_an_answer": 0,
                "superseded_refuses": 0,
                "units_with_no_body": 0,
            }
        counts = populations[population]
        counts["units"] = counts["units"] + 1
        if not has_a_body(record):
            counts["units_with_no_body"] = \
                counts["units_with_no_body"] + 1
            continue

        now_ok = True
        try:
            reference.answer_for_unit(record)
        except Exception as problem:
            now_ok = False
            key = short("%s" % problem)
            reasons_now[key] = reasons_now.get(key, 0) + 1
        if now_ok:
            counts["reference_reaches_an_answer"] = \
                counts["reference_reaches_an_answer"] + 1
        else:
            counts["reference_refuses"] = \
                counts["reference_refuses"] + 1

        before_ok = True
        try:
            superseded_answer(record)
        except Exception as problem:
            before_ok = False
            key = short("%s" % problem)
            reasons_before[key] = reasons_before.get(key, 0) + 1
        if before_ok:
            counts["superseded_reaches_an_answer"] = \
                counts["superseded_reaches_an_answer"] + 1
        else:
            counts["superseded_refuses"] = \
                counts["superseded_refuses"] + 1

        if before_ok and not now_ok:
            regressions.append(record.get("unit"))
        if now_ok and not before_ok:
            gained = gained + 1

    total = {
        "units": 0,
        "reference_reaches_an_answer": 0,
        "reference_refuses": 0,
        "superseded_reaches_an_answer": 0,
        "superseded_refuses": 0,
        "units_with_no_body": 0,
    }
    for counts in populations.values():
        for key in total:
            total[key] = total[key] + counts[key]

    print("REACH, per population (every unit walked, none sampled)")
    print("  %-14s %8s %10s %9s %10s %9s %8s"
          % ("population", "units", "ref:answer", "ref:no",
             "old:answer", "old:no", "no body"))
    for name in sorted(populations):
        counts = populations[name]
        print("  %-14s %8d %10d %9d %10d %9d %8d"
              % (name, counts["units"],
                 counts["reference_reaches_an_answer"],
                 counts["reference_refuses"],
                 counts["superseded_reaches_an_answer"],
                 counts["superseded_refuses"],
                 counts["units_with_no_body"]))
    print("  %-14s %8d %10d %9d %10d %9d %8d"
          % ("ALL", total["units"],
             total["reference_reaches_an_answer"],
             total["reference_refuses"],
             total["superseded_reaches_an_answer"],
             total["superseded_refuses"],
             total["units_with_no_body"]))
    print()
    print("REGRESSIONS -- units the superseded route answered and this "
          "reference refuses: %d" % len(regressions))
    for name in regressions[:40]:
        print("  %s" % name)
    print()
    print("GAINED -- units this reference answers and the superseded "
          "route refused: %d" % gained)
    print()
    print("THE REFERENCE'S OWN REFUSALS, by their own stated reason:")
    for key in sorted(reasons_now, key=lambda k: -reasons_now[k]):
        print("  %6d  %s" % (reasons_now[key], key))
    print()
    print("THE SUPERSEDED ROUTE'S REFUSALS, by their own stated "
          "reason:")
    for key in sorted(reasons_before,
                      key=lambda k: -reasons_before[k]):
        print("  %6d  %s" % (reasons_before[key], key))

    handle = open(OUT_JSON, "w")
    json.dump({
        "meta": {
            "generator": "coverage57.py",
            "form": "reach of reference.py against the reach of the "
                    "superseded canon10 route, over every canon38 "
                    "unit record; no verdict is computed here",
        },
        "populations": populations,
        "all_three_populations": total,
        "regressions": regressions,
        "gained": gained,
        "reference_refusal_reasons": reasons_now,
        "superseded_refusal_reasons": reasons_before,
    }, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    print()
    print("wrote %s" % OUT_JSON)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
