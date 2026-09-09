#!/usr/bin/env python3
"""audit64.py -- the round-13 re-gate, read against round 12's, with
every movement's cause computed off the units' own artifacts.

Node: `hq.research.compiler_graph.gate` (0_3_5_5), sub-node
`zero_regression`.

WHAT IS JOINED.  `term61_store/*.json` (round 12, task 61, over
canon39) against `regate64_store/*.json` (this round, the same
canon39 units through the same `term.py` and `gate.py`, over the
branch-following `reference.py`).  The join is on the unit name.  The
four states are read off each record by ONE function, `state_of`, so
the two runs are read the same way.

EVERY MOVEMENT CARRIES A COMPUTED CAUSE.  A cause is never asserted: it
is read off the unit's own record, or computed from the unit's own
stored body and stored ledger.  The two that are computed:

  * "the reference now follows this body's branches" -- the unit's own
    text carries a conditional transfer.
  * "the stored ledger has no row for the transfer into the compiler's
    own runtime" -- the unit's own text carries a `call` whose callee
    one of this machine's builtins archives DEFINES, and the unit's
    OWN STORED LEDGER carries no row whose producer names that callee.

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

Every grouping below is by STATE, by POPULATION, by LANGUAGE or by
COMPUTED CAUSE.  No operator token is read anywhere in this file.

Coding discipline: no compound one-liner statements.

usage:
  audit64.py
"""

import collections
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

LINES = []


def say(text=""):
    LINES.append(text)
    print(text)


def state_of(record):
    if record.get("term_state") == "NO_TERM":
        return "no term"
    if record.get("proved"):
        return "proved"
    if record.get("outcome") == "DISPROVED":
        return "disproved"
    return "undecided"


def read_store(folder):
    out = {}
    for path in sorted(glob.glob(os.path.join(HERE, folder,
                                              "*.json"))):
        document = json.load(open(path))
        for name, record in document.get("units", {}).items():
            out[name] = record
    return out


def canon_units():
    """the canon39 records themselves, for the causes that are computed
    off a unit's own body and its own stored ledger."""
    out = {}
    paths = []
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        paths.append(os.path.join(HERE,
                                  "canon39_wrapped_%s.json" % lang))
    paths.append(os.path.join(HERE, "canon39_interp.json"))
    paths.extend(sorted(glob.glob(os.path.join(
        HERE, "canon39_regen_store", "*.json"))))
    for path in paths:
        if not os.path.exists(path):
            continue
        document = json.load(open(path))
        for name, record in document.get("units", {}).items():
            if record.get("outcome") != "WRAPPED_TEXT_PROVED":
                continue
            out[name] = record
    return out


def attachments():
    path = os.path.join(HERE, "canon39_callee_attachments.json")
    if not os.path.exists(path):
        return {}
    return json.load(open(path)).get("units", {})


def ledger_names_the_callee(record, callee):
    for row in record.get("ledger") or []:
        producer = row.get("produced_by") or {}
        if producer.get("kind") != "runtime_callee":
            continue
        if producer.get("callee") == callee:
            return True
    return False


def has_a_conditional_transfer(record):
    import reference as R
    for raw in record.get("body_verbatim") or []:
        text = raw.split("!!")[0].strip()
        if text == "":
            continue
        if R.is_conditional_transfer(text.split(" ", 1)[0]):
            return True
    return False


def cause_of(name, was, now, canon, attached, new_record):
    """the cause of one unit's movement, computed off its own
    artifacts.  Never asserted."""
    record = canon.get(name)
    if record is None:
        return "the unit is not in canon39's proved population"
    attachment = attached.get(name) or {}
    callees = attachment.get("callees") or []
    unmodelled = []
    for callee in callees:
        if ledger_names_the_callee(record, callee):
            continue
        unmodelled.append(callee)
    if now == "disproved" and unmodelled:
        return ("the unit's own stored canon39 ledger carries NO row "
                "for its transfer into the compiler's own runtime, so "
                "its term asserts the transfer changed nothing; the "
                "reference now walks that callee's body, and the two "
                "disagree")
    if now == "proved" and was != "proved":
        if attachment.get("attached"):
            return ("the reference now enters the attached runtime "
                    "callee's body and returns through its answer "
                    "register")
        if has_a_conditional_transfer(record):
            return ("the reference now follows this body's own "
                    "branches and merges them at the join")
        return ("the reference now models something this body spells "
                "that it refused before (the narrow division and "
                "widening multiply, or a rip-relative address)")
    if was == "proved" and now != "proved":
        return ("A PROOF WAS LOST: %s" % (new_record.get("reason")
                                          or new_record.get(
                                              "why_no_term")))
    reason = new_record.get("reason")
    if reason is None:
        reason = new_record.get("why_no_term")
    if reason is None:
        reason = "no reason recorded on the new record"
    return "the new run's own recorded reason: %s" % reason[:180]


def consistency(store):
    """units proved on one route and DISPROVED on the other.  The gate
    CORE: 'two routes never contradict'."""
    out = []
    for name, record in store.items():
        ship = record.get("verdict_ship") or {}
        text = record.get("verdict_text") or {}
        first = ship.get("outcome")
        second = text.get("outcome")
        if first is None or second is None:
            continue
        proved = ("PROVED_ON_SHIP", "PROVED_BY_CONSTRUCTION")
        if first in proved and second == "DISPROVED":
            out.append(name)
            continue
        if second in proved and first == "DISPROVED":
            out.append(name)
    return out


def table(title, rows, header):
    say(title)
    say("   " + header)
    for row in rows:
        say("   " + row)
    say()


def main():
    old = read_store("term61_store")
    new = read_store("regate64_store")
    canon = canon_units()
    attached = attachments()
    say("=" * 70)
    say("THE POPULATION")
    say("=" * 70)
    say("canon39 records 30,432 units WRAPPED_TEXT_PROVED.  Round 12's "
        "run (`term61_store`) holds %d of them; this round's re-gate "
        "(`regate64_store`) holds %d." % (len(old), len(new)))
    say()

    # -- the four states, per population ------------------------------
    say("=" * 70)
    say("THE FOUR STATES, PER POPULATION")
    say("=" * 70)
    populations = ["original", "interpreter", "regenerated"]
    states = ["proved", "disproved", "undecided", "no term"]
    was_count = collections.Counter()
    now_count = collections.Counter()
    for name, record in old.items():
        population = record.get("population") or "unknown"
        was_count[(population, state_of(record))] += 1
    for name, record in new.items():
        population = record.get("population") or "unknown"
        now_count[(population, state_of(record))] += 1
    say("%-14s %-10s %10s %10s %8s"
        % ("population", "state", "task 61", "task 64", "move"))
    for population in populations:
        for state in states:
            before = was_count[(population, state)]
            after = now_count[(population, state)]
            say("%-14s %-10s %10d %10d %+8d"
                % (population, state, before, after, after - before))
    say("%-14s %-10s %10d %10d %+8d"
        % ("ALL", "proved",
           sum(was_count[(p, "proved")] for p in populations),
           sum(now_count[(p, "proved")] for p in populations),
           sum(now_count[(p, "proved")] for p in populations)
           - sum(was_count[(p, "proved")] for p in populations)))
    say("%-14s %-10s %10d %10d"
        % ("ALL", "TOTAL", sum(was_count.values()),
           sum(now_count.values())))
    say()
    say("the round-12 baseline the brief names: 26,040 proved / 0 "
        "disproved / 3,865 undecided / 527 no term over 30,432")
    say("recomputed here from `term61_store`: %d / %d / %d / %d over %d"
        % (sum(was_count[(p, "proved")] for p in populations),
           sum(was_count[(p, "disproved")] for p in populations),
           sum(was_count[(p, "undecided")] for p in populations),
           sum(was_count[(p, "no term")] for p in populations),
           sum(was_count.values())))
    say()

    # -- the transition, unit by unit ---------------------------------
    say("=" * 70)
    say("THE TRANSITION, UNIT BY UNIT (units in BOTH runs)")
    say("=" * 70)
    moves = collections.Counter()
    sightings = collections.defaultdict(list)
    for name, record in sorted(new.items()):
        if name not in old:
            continue
        was = state_of(old[name])
        now = state_of(record)
        moves[(was, now)] += 1
        if len(sightings[(was, now)]) < 3:
            sightings[(was, now)].append(name)
    say("%-10s %-10s %8s   %s"
        % ("task 61", "task 64", "units", "sightings"))
    for key, count in sorted(moves.items(), key=lambda one: -one[1]):
        say("%-10s %-10s %8d   %s"
            % (key[0], key[1], count, ", ".join(sightings[key])))
    say()
    only_new = sorted(set(new) - set(old))
    only_old = sorted(set(old) - set(new))
    say("in task 64 and not task 61: %d %s"
        % (len(only_new), only_new[:5]))
    say("in task 61 and not task 64: %d %s"
        % (len(only_old), only_old[:5]))
    say()

    # -- every movement, by computed cause ----------------------------
    say("=" * 70)
    say("EVERY MOVEMENT, BY COMPUTED CAUSE")
    say("=" * 70)
    for key in sorted(moves, key=lambda one: -moves[one]):
        was, now = key
        if was == now:
            continue
        causes = collections.Counter()
        examples = {}
        for name, record in new.items():
            if name not in old:
                continue
            if state_of(old[name]) != was:
                continue
            if state_of(record) != now:
                continue
            cause = cause_of(name, was, now, canon, attached, record)
            causes[cause] += 1
            examples.setdefault(cause, []).append(name)
        say("-- %s -> %s  (%d units)" % (was, now, moves[key]))
        for cause, count in causes.most_common():
            say("   %6d | %s" % (count, cause))
            say("          | sightings: %s"
                % ", ".join(sorted(examples[cause])[:3]))
        say()

    # -- zero regression ----------------------------------------------
    say("=" * 70)
    say("ZERO REGRESSION")
    say("=" * 70)
    lost = []
    for name, record in new.items():
        if name not in old:
            continue
        if state_of(old[name]) != "proved":
            continue
        if state_of(record) == "proved":
            continue
        lost.append(name)
    say("units PROVED in task 61 and not proved in task 64: %d"
        % len(lost))
    for name in sorted(lost)[:20]:
        say("   %s: %s" % (name, (new[name].get("reason")
                                  or new[name].get("why_no_term"))))
    say()

    # -- the consistency line -----------------------------------------
    say("=" * 70)
    say("THE CONSISTENCY LINE")
    say("=" * 70)
    clash = consistency(new)
    say("units proved on one route and disproved on the other: %d"
        % len(clash))
    for name in sorted(clash)[:20]:
        say("   %s" % name)
    say()

    # -- the four named causes of log_160 section 1.7 -----------------
    say("=" * 70)
    say("THE FOUR NAMED CAUSES OF log_160 SECTION 1.7, TESTED")
    say("=" * 70)
    buckets = {
        "runtime callee not yet attached": 0,
        "a conditional transfer": 0,
        "a rip-relative address computation": 0,
        "a narrow division or widening multiply": 0,
        "another reason": 0,
    }
    outcomes = collections.defaultdict(collections.Counter)
    for name, record in old.items():
        if state_of(record) != "undecided":
            continue
        reason = record.get("reason") or ""
        key = "another reason"
        if "runtime callee not yet attached" in reason:
            key = "runtime callee not yet attached"
        elif "is a census row" in reason and "'j" in reason:
            key = "a conditional transfer"
        elif "address computation over base register" in reason:
            key = "a rip-relative address computation"
        elif "is not modeled" in reason and ("division" in reason
                                             or "multiply" in reason):
            key = "a narrow division or widening multiply"
        buckets[key] += 1
        if name in new:
            outcomes[key][state_of(new[name])] += 1
        else:
            outcomes[key]["absent"] += 1
    say("%-42s %8s   %s"
        % ("task 61's undecided, by its own reason", "units",
           "what task 64 made of them"))
    for key in buckets:
        say("%-42s %8d   %s"
            % (key, buckets[key], dict(outcomes[key])))
    say()

    # -- task 66's 36 rendered-but-unproved units ---------------------
    say("=" * 70)
    say("TASK 66's 36 RENDERED-BUT-UNPROVED UNITS")
    say("=" * 70)
    tally_path = os.path.join(HERE, "render_back_tally.json")
    if not os.path.exists(tally_path):
        say("`render_back_tally.json` is not on disk; nothing to read")
    else:
        tally = json.load(open(tally_path))
        for row in tally.get("not_proved_causes", []):
            say("-- %d units | %s" % (row["units"], row["cause"]))
            here = collections.Counter()
            for name in row.get("sightings", []):
                if name in new:
                    here[state_of(new[name])] += 1
                else:
                    here["not in this run"] += 1
            say("   the SIGHTINGS this task can join on (%d of the %d "
                "the cause lists): %s"
                % (len(row.get("sightings", [])), row["units"],
                   dict(here)))
            for name in sorted(row.get("sightings", []))[:3]:
                if name not in new:
                    continue
                say("     %s -> %s | %s"
                    % (name, state_of(new[name]),
                       (new[name].get("reason")
                        or new[name].get("why_no_term") or "")[:150]))
            say()

    out = {
        "meta": {
            "produced_by": "audit64.py",
            "population": "canon39's 30,432 WRAPPED_TEXT_PROVED units",
            "baseline": "term61_store (round 12, task 61)",
            "this_round": "regate64_store (round 13, task 64)",
        },
        "four_states": [
            {"population": population, "state": state,
             "task_61": was_count[(population, state)],
             "task_64": now_count[(population, state)]}
            for population in populations for state in states
        ],
        "transitions": [
            {"was": key[0], "now": key[1], "units": count,
             "sightings": sightings[key]}
            for key, count in sorted(moves.items(),
                                     key=lambda one: -one[1])
        ],
        "proofs_lost": sorted(lost),
        "consistency_clashes": sorted(clash),
    }
    handle = open(os.path.join(HERE, "audit64.json"), "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.close()
    handle = open(os.path.join(HERE, "audit64_printed.txt"), "w")
    handle.write("\n".join(LINES) + "\n")
    handle.close()
    return 0


sys.exit(main())
