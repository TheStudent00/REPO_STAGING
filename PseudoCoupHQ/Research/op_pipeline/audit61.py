#!/usr/bin/env python3
"""audit61.py -- the figures for TASK 61's term run, per population,
with every movement's COMPUTED cause and the consistency line.

BASELINE: task 58's re-gate over canon38 (`gate58_store/*.json`),
whose headline is 25,179 proved / 0 withdrawn / 3,970 undecided /
1,287 no term over 30,436 units.
NOW: task 61's transcription over canon39 (`term61_store/*.json`),
over 30,432 units.

THE FOUR STATES, and what each means, said once:
  proved      a term was built and z3 proved it equal to the unit's
              own machine code on at least one route, with no route
              disproving it
  withdrawn   a term was built and a route DISPROVED it; the term is
              withdrawn, not kept as a weaker key
  undecided   a term was built and neither route proved it
  no term     no term was built at all -- a census row, not a verdict

THE CONSISTENCY LINE is the count of units proved on one route and
disproved on the other.  It must be 0: a unit cannot be both.

Coding discipline: no compound one-liner statements.

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

LINES = []

TASK58 = {"proved": 25179, "withdrawn": 0, "undecided": 3970,
          "no term": 1287}


def log(text):
    LINES.append(text)
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def read_now():
    out = {}
    pattern = os.path.join(HERE, "term61_store", "*.json")
    for path in sorted(glob.glob(pattern)):
        document = json.load(open(path))
        for name in document["units"]:
            out[name] = document["units"][name]
    return out


def read_before():
    out = {}
    pattern = os.path.join(HERE, "gate58_store", "*.json")
    for path in sorted(glob.glob(pattern)):
        document = json.load(open(path))
        for name in document["units"]:
            out[name] = document["units"][name]
    return out


def state_now(record):
    if record.get("term_state") != "TERM":
        return "no term"
    if record.get("outcome") == "DISPROVED":
        return "withdrawn"
    if record.get("proved"):
        return "proved"
    return "undecided"


def state_before(record):
    if not record.get("term_built"):
        return "no term"
    outcomes = [record["ship"]["outcome"], record["text"]["outcome"]]
    if "PROVED_ON_SHIP" in outcomes:
        return "proved"
    if "PROVED_BY_CONSTRUCTION" in outcomes:
        return "proved"
    if "DISPROVED" in outcomes:
        return "withdrawn"
    return "undecided"


def cause_before(record):
    """the COMPUTED cause of a movement: the reason THAT UNIT'S OWN
    earlier record recorded for not proving it.  Never typed."""
    if not record.get("term_built"):
        return "the old run built no term: %s" % (
            record.get("transcription_refused") or "no reason recorded")
    outcomes = [record["ship"]["outcome"], record["text"]["outcome"]]
    if "DISPROVED" in outcomes:
        return "the old run DISPROVED it"
    return "the old run's route-one reason: %s" % \
        record["ship"]["reason"][:110]


def cause_now(record):
    """the cause of a unit that does not prove NOW, read off its own
    record."""
    if record.get("term_state") != "TERM":
        return "no term now: %s" % (record.get("why_no_term")
                                    or "no reason recorded")
    if record.get("outcome") == "DISPROVED":
        return "disproved now"
    reason = (record.get("verdict_ship") or {}).get("reason") or ""
    return "undecided now, route one: %s" % reason[:110]


def tally(counts, key):
    counts[key] = counts.get(key, 0) + 1


def main():
    now = read_now()
    before = read_before()
    log("-- the populations")
    log("   canon39 units transcribed (task 61) %d" % len(now))
    log("   canon38 units gated       (task 58) %d" % len(before))

    states = {}
    by_population = {}
    by_language = {}
    consistency = 0
    runtime_rows = 0
    runtime_units = 0
    slot_disagreements = 0
    for name in sorted(now):
        record = now[name]
        state = state_now(record)
        tally(states, state)
        population = record.get("population")
        by_population.setdefault(population, {})
        tally(by_population[population], state)
        lang = record.get("lang")
        by_language.setdefault(lang, {})
        tally(by_language[lang], state)
        ship = (record.get("verdict_ship") or {}).get("outcome")
        text = (record.get("verdict_text") or {}).get("outcome")
        pair = [ship, text]
        if "DISPROVED" in pair:
            if "PROVED_ON_SHIP" in pair:
                consistency = consistency + 1
        if record.get("runtime_callee_rows"):
            runtime_units = runtime_units + 1
            runtime_rows = runtime_rows + record["runtime_callee_rows"]
        slot_disagreements = slot_disagreements + len(
            record.get("slot_disagreements") or [])

    log("")
    log("-- THE FOUR STATES, task 58 over canon38 -> task 61 over "
        "canon39")
    log("   %-12s %10s %10s %8s" % ("state", "task 58", "task 61",
                                    "move"))
    for key in ["proved", "withdrawn", "undecided", "no term"]:
        was = TASK58[key]
        count = states.get(key, 0)
        log("   %-12s %10d %10d %+8d" % (key, was, count, count - was))
    log("   %-12s %10d %10d %+8d"
        % ("TOTAL", sum(TASK58.values()), len(now),
           len(now) - sum(TASK58.values())))

    log("")
    log("CONSISTENCY -- units proved on one route and disproved on "
        "the other: %d" % consistency)

    log("")
    log("-- by arrival population")
    for population in sorted(by_population):
        counts = by_population[population]
        total = sum(counts.values())
        log("   %-12s total %6d | %s"
            % (population, total, json.dumps(counts, sort_keys=True)))

    log("")
    log("-- by language")
    for lang in sorted(by_language):
        counts = by_language[lang]
        total = sum(counts.values())
        log("   %-8s total %6d | %s"
            % (lang, total, json.dumps(counts, sort_keys=True)))

    log("")
    log("-- THE TRANSITION, unit by unit (only units in BOTH runs)")
    transitions = {}
    sightings = {}
    for name in sorted(now):
        if name not in before:
            continue
        was = state_before(before[name])
        got = state_now(now[name])
        key = (was, got)
        transitions[key] = transitions.get(key, 0) + 1
        sightings.setdefault(key, [])
        if len(sightings[key]) < 3:
            sightings[key].append(name)
    log("   %-12s %-12s %8s   %s"
        % ("task 58", "task 61", "units", "sightings"))
    ordered = sorted(transitions.items(), key=lambda one: -one[1])
    for (was, got), count in ordered:
        log("   %-12s %-12s %8d   %s"
            % (was, got, count, ", ".join(sightings[(was, got)])))

    log("")
    log("-- GAINED, by COMPUTED cause (the reason the unit's OWN "
        "task-58 record recorded)")
    gained = {}
    for name in sorted(now):
        if name not in before:
            continue
        if state_before(before[name]) == "proved":
            continue
        if state_now(now[name]) != "proved":
            continue
        cause = cause_before(before[name])
        gained[cause] = gained.get(cause, 0) + 1
    for cause in sorted(gained, key=lambda one: -gained[one]):
        log("   %6d | %s" % (gained[cause], cause))
    if not gained:
        log("   (none)")

    log("")
    log("-- LOST, by COMPUTED cause (the reason the unit's OWN "
        "task-61 record records)")
    lost = {}
    for name in sorted(now):
        if name not in before:
            continue
        if state_before(before[name]) != "proved":
            continue
        if state_now(now[name]) == "proved":
            continue
        cause = cause_now(now[name])
        lost[cause] = lost.get(cause, 0) + 1
    for cause in sorted(lost, key=lambda one: -lost[one]):
        log("   %6d | %s" % (lost[cause], cause))
    if not lost:
        log("   (none)")

    log("")
    log("-- units in one run and not the other")
    only_now = []
    only_before = []
    for name in now:
        if name not in before:
            only_now.append(name)
    for name in before:
        if name not in now:
            only_before.append(name)
    log("   in task 61 and not task 58: %d %s"
        % (len(only_now), sorted(only_now)[:4]))
    log("   in task 58 and not task 61: %d %s"
        % (len(only_before), sorted(only_before)[:4]))

    log("")
    log("-- the runtime callee expectation")
    log("   units carrying a runtime_callee row %d" % runtime_units)
    log("   runtime_callee rows %d" % runtime_rows)
    runtime_states = {}
    for name in now:
        if not now[name].get("runtime_callee_rows"):
            continue
        tally(runtime_states, state_now(now[name]))
    log("   their states %s" % json.dumps(runtime_states,
                                          sort_keys=True))

    log("")
    log("-- operand slots checked, not assumed")
    log("   recorded slot disagreements %d" % slot_disagreements)

    document = {
        "meta": {
            "produced_by": "audit61.py",
            "population_now": "every unit canon39 proved: %d" % len(now),
            "population_before": "every unit canon38 proved, gated by "
                                 "task 58: %d" % len(before),
            "the_four_states": "proved / withdrawn / undecided / no "
                               "term, defined in this file's header",
        },
        "task58": TASK58,
        "task61": states,
        "consistency_units_proved_on_one_route_and_disproved_on_the_other":
            consistency,
        "by_population": by_population,
        "by_language": by_language,
        "transitions": dict(("%s -> %s" % key, value)
                            for key, value in transitions.items()),
        "gained_by_cause": gained,
        "lost_by_cause": lost,
        "units_only_in_task61": sorted(only_now),
        "units_only_in_task58": sorted(only_before),
        "runtime_callee_units": runtime_units,
        "runtime_callee_rows": runtime_rows,
        "runtime_callee_states": runtime_states,
        "slot_disagreements": slot_disagreements,
    }
    handle = open(os.path.join(HERE, "audit61.json"), "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    handle = open(os.path.join(HERE, "audit61_printed.txt"), "w")
    handle.write("\n".join(LINES) + "\n")
    handle.close()
    log("")
    log("-- wrote audit61.json and audit61_printed.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
