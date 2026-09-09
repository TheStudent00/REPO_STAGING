#!/usr/bin/env python3
"""audit58.py -- THE FIGURES for task 58, every one with its
population.

Joins task 53's recorded verdicts (`layer4c_terms_*.json`,
`layer4c_interp.json`, `layer4c_regen_store/*.json` -- read, never
edited) against task 58's (`gate58_store/*.json`) on the unit name,
and reports:

  * the four states per population, before and after, against log 153's
    23,132 proved / 415 withdrawn / 5,602 undecided / 1,287 no term;
  * the transition table, unit by unit, with three sightings each;
  * every movement's CAUSE, computed from the artifacts themselves --
    for a unit that gained a proof, the recorded reason the OLD run
    gave for not proving it; for a unit that lost one, the recorded
    reason the NEW run gives;
  * the consistency line: units proved on one route and disproved on
    the other, which must be 0;
  * `Gate.zero_regression` over the whole population, with its causes.

THE FOUR STATES, defined once so every count below is checkable.  A
unit is `withdrawn` when either route DISPROVED it; else `proved` when
either route proved it; else `no term` when the ledger built no OUT-0
term; else `undecided`.  This is exactly the reading log 153 section
1.2 used, so the two runs are directly comparable.

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
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gate as GATE                                               # noqa: E402

LANGS = ("c", "cpp", "go", "rust", "swift")
POPULATIONS = ("interpreter", "original", "regenerated")
STATES = ("proved", "withdrawn", "undecided", "no term")

LOG153 = {
    "proved": 23132,
    "withdrawn": 415,
    "undecided": 5602,
    "no term": 1287,
}
LOG153_PER_POPULATION = {
    "interpreter": {"proved": 9, "withdrawn": 0, "undecided": 0,
                    "no term": 0},
    "original": {"proved": 1635, "withdrawn": 12, "undecided": 81,
                 "no term": 35},
    "regenerated": {"proved": 21488, "withdrawn": 403,
                    "undecided": 5521, "no term": 1252},
}


def before_records():
    """task 53's own records, one mapping unit name -> record."""
    out = {}
    paths = [os.path.join(HERE, "layer4c_terms_%s.json" % lang)
             for lang in LANGS]
    paths.append(os.path.join(HERE, "layer4c_interp.json"))
    paths.extend(sorted(glob.glob(os.path.join(
        HERE, "layer4c_regen_store", "*.json"))))
    for path in paths:
        document = json.load(open(path))
        for name, record in document["units"].items():
            out[name] = record
    return out


def after_records():
    out = {}
    for path in sorted(glob.glob(os.path.join(HERE, "gate58_store",
                                              "*.json"))):
        document = json.load(open(path))
        for name, record in document["units"].items():
            out[name] = record
    return out


def state_before(record):
    ship = record.get("gate_ship_verdict")
    text = record.get("gate_textorder_verdict")
    if "DISPROVED" in (ship, text):
        return "withdrawn"
    if "PROVED_EQUAL" in (ship, text):
        return "proved"
    if not record.get("term_built"):
        return "no term"
    return "undecided"


def state_after(record):
    ship = (record.get("ship") or {}).get("outcome")
    text = (record.get("text") or {}).get("outcome")
    if GATE.DISPROVED in (ship, text):
        return "withdrawn"
    if GATE.PROVED_ON_SHIP in (ship, text):
        return "proved"
    if not record.get("term_built"):
        return "no term"
    return "undecided"


def population_of(record):
    value = record.get("population")
    if value == "original":
        return "original"
    if value == "regenerated":
        return "regenerated"
    return "interpreter"


def short(text, width=96):
    if text is None:
        return "(none recorded)"
    text = " ".join(text.split())
    if len(text) <= width:
        return text
    return text[:width]


def cause_of_a_gain(before):
    """the CAUSE a unit gained a proof: the recorded reason the OLD run
    gave for not proving it, taken off that unit's own task-53 record
    -- never a sentence typed here."""
    ship = before.get("gate_ship_verdict")
    if ship == "DISPROVED":
        return "the old run DISPROVED it: %s" \
            % short(before.get("gate_ship_detail"))
    if not before.get("term_built"):
        return "the old run built no term for OUT-0"
    return "the old run's route-one reason: %s" \
        % short(before.get("gate_ship_detail"))


def cause_of_a_loss(after):
    """the CAUSE a unit lost a proof: the recorded reason the NEW run
    gives, taken off that unit's own task-58 record."""
    ship = (after.get("ship") or {}).get("outcome")
    if ship == GATE.DISPROVED:
        return "the new run DISPROVED it on route one"
    return "the new run's route-one reason: %s" \
        % short((after.get("ship") or {}).get("reason"))


def main(argv):
    before = before_records()
    after = after_records()
    print("POPULATION LINE")
    print("  units in task 53's records: %d" % len(before))
    print("  units in task 58's records: %d" % len(after))
    missing = [name for name in before if name not in after]
    extra = [name for name in after if name not in before]
    print("  in task 53 and not in task 58: %d" % len(missing))
    print("  in task 58 and not in task 53: %d" % len(extra))
    print("")

    tally = {}
    for population in POPULATIONS:
        tally[population] = {
            "units": 0,
            "before": dict((state, 0) for state in STATES),
            "after": dict((state, 0) for state in STATES),
            "route one proved": 0,
            "route two proved": 0,
        }
    transitions = {}
    gains = {}
    losses = {}
    inconsistent = []
    for name, record in after.items():
        old = before.get(name)
        if old is None:
            continue
        population = population_of(record)
        counts = tally[population]
        counts["units"] = counts["units"] + 1
        was = state_before(old)
        now = state_after(record)
        counts["before"][was] = counts["before"][was] + 1
        counts["after"][now] = counts["after"][now] + 1
        ship = (record.get("ship") or {}).get("outcome")
        text = (record.get("text") or {}).get("outcome")
        if ship == GATE.PROVED_ON_SHIP:
            counts["route one proved"] = counts["route one proved"] + 1
        if text == GATE.PROVED_ON_SHIP:
            counts["route two proved"] = counts["route two proved"] + 1
        if GATE.PROVED_ON_SHIP in (ship, text) and \
                GATE.DISPROVED in (ship, text):
            inconsistent.append(name)
        key = (was, now)
        transitions.setdefault(key, []).append(name)
        if was != "proved" and now == "proved":
            gains.setdefault(cause_of_a_gain(old), []).append(name)
        if was == "proved" and now != "proved":
            losses.setdefault(cause_of_a_loss(record), []).append(name)

    for population in POPULATIONS:
        counts = tally[population]
        print("POPULATION: %s" % population)
        print("  units %d" % counts["units"])
        print("  state                 task 53   task 58    delta")
        for state in STATES:
            was = counts["before"][state]
            now = counts["after"][state]
            print("  %-20s %8d %9d %+8d" % (state, was, now, now - was))
        print("  route one (the term against the ship body) proved "
              "%d" % counts["route one proved"])
        print("  route two (the text-order walk) proved %d"
              % counts["route two proved"])
        print("")

    print("ALL THREE POPULATIONS, against log 153 section 1.2")
    print("  state                log 153   task 53   task 58    delta")
    totals_before = {}
    totals_after = {}
    for state in STATES:
        was = sum(tally[p]["before"][state] for p in POPULATIONS)
        now = sum(tally[p]["after"][state] for p in POPULATIONS)
        totals_before[state] = was
        totals_after[state] = now
        print("  %-19s %8d %9d %9d %+8d"
              % (state, LOG153[state], was, now, now - was))
    print("  %-19s %8d %9d %9d"
          % ("units", sum(LOG153.values()),
             sum(totals_before.values()), sum(totals_after.values())))
    print("")
    print("  log 153's per-population figures, reproduced from its "
          "own section 1.4, against this run:")
    for population in POPULATIONS:
        for state in STATES:
            said = LOG153_PER_POPULATION[population][state]
            here = tally[population]["before"][state]
            if said != here:
                print("    MISMATCH %s %s: log 153 said %d, this "
                      "run's reading of task 53's records says %d"
                      % (population, state, said, here))
    print("    (no MISMATCH line above means every one of the twelve "
          "figures agrees)")
    print("")

    print("CONSISTENCY -- units proved on one route and disproved on "
          "the other: %d" % len(inconsistent))
    if inconsistent:
        print("  " + ", ".join(sorted(inconsistent)[:10]))
    print("")

    print("THE TRANSITION, unit by unit")
    print("  task 53        task 58          units   sightings")
    ordered = sorted(transitions.items(), key=lambda p: -len(p[1]))
    for (was, now), names in ordered:
        print("  %-14s %-14s %7d   %s"
              % (was, now, len(names), ", ".join(sorted(names)[:3])))
    print("")

    print("EVERY GAINED PROOF, BY ITS COMPUTED CAUSE")
    print("  (the cause is the reason the unit's OWN task-53 record "
          "recorded for not proving it)")
    for cause, names in sorted(gains.items(), key=lambda p: -len(p[1])):
        print("  %6d  %s" % (len(names), cause))
        print("          sightings: %s" % ", ".join(sorted(names)[:3]))
    if not gains:
        print("  (none)")
    print("")

    print("EVERY LOST PROOF, BY ITS COMPUTED CAUSE")
    print("  (the cause is the reason the unit's OWN task-58 record "
          "gives)")
    for cause, names in sorted(losses.items(),
                               key=lambda p: -len(p[1])):
        print("  %6d  %s" % (len(names), cause))
        print("          sightings: %s" % ", ".join(sorted(names)[:3]))
    if not losses:
        print("  (none)")
    print("")

    print("WHAT IS STILL UNDECIDED, BY THE NEW RUN'S OWN RECORDED "
          "REASON (route one)")
    reasons = {}
    for name, record in after.items():
        if name not in before:
            continue
        if state_after(record) != "undecided":
            continue
        reason = short((record.get("ship") or {}).get("reason"), 88)
        reasons[reason] = reasons.get(reason, 0) + 1
    for reason, count in sorted(reasons.items(),
                                key=lambda p: -p[1])[:20]:
        print("  %6d  %s" % (count, reason))
    print("")

    print("WHAT BUILDS NO TERM, BY THE ARTIFACT'S OWN RECORDED REASON")
    noterm = {}
    for name, record in after.items():
        if name not in before:
            continue
        if state_after(record) != "no term":
            continue
        refused = record.get("transcription_refused")
        key = short(refused, 88) if refused else \
            "the ledger built no OUT-0 term (a census row, not a " \
            "silent gap)"
        noterm[key] = noterm.get(key, 0) + 1
    for key, count in sorted(noterm.items(), key=lambda p: -p[1])[:10]:
        print("  %6d  %s" % (count, key))
    print("")

    print("ZERO REGRESSION -- Gate.zero_regression over all three "
          "populations")
    gate = GATE.Gate()
    states_before = {}
    states_after = {}
    for name, record in after.items():
        if name not in before:
            continue
        states_before[name] = state_before(before[name])
        states_after[name] = state_after(record)
    report = gate.zero_regression(
        states_before, states_after,
        cause_of=lambda name: cause_of_a_loss(after[name]))
    print("  units still proved (kept)                    %d"
          % report["kept"])
    print("  proofs lost                                  %d"
          % report["lost"])
    print("  proofs gained                                %d"
          % report["gained"])
    print("  moved without ever holding a proof           %d"
          % report["moved_without_losing_a_proof"])
    print("  units missing from the new run               %d"
          % report["missing_from_the_new_run"])
    print("  LOST PROOFS WITH NO COMPUTED CAUSE           %d"
          % report["regressions_without_a_named_cause"])
    for entry in report["causes"]:
        print("    %6d  %s" % (entry["units"], entry["cause"]))
        print("            sightings: %s"
              % ", ".join(entry["sightings"]))

    out = {
        "meta": {
            "produced_by": "audit58.py",
            "population": "every unit task 52 proved: 9 interpreter, "
                          "1,763 original, 28,664 regenerated, 30,436 "
                          "in all",
            "the four states": "withdrawn if either route disproved; "
                               "else proved if either route proved; "
                               "else no term if the ledger built none; "
                               "else undecided",
        },
        "per_population": tally,
        "totals_before": totals_before,
        "totals_after": totals_after,
        "log153": LOG153,
        "consistency_units_proved_on_one_route_and_disproved_on_the_"
        "other": len(inconsistent),
        "transitions": dict(
            ("%s -> %s" % key, len(names))
            for key, names in transitions.items()),
        "gained_by_cause": dict(
            (cause, len(names)) for cause, names in gains.items()),
        "lost_by_cause": dict(
            (cause, len(names)) for cause, names in losses.items()),
        "still_undecided_by_reason": reasons,
        "no_term_by_reason": noterm,
        "zero_regression": report,
    }
    handle = open(os.path.join(HERE, "audit58.json"), "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
