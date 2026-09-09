#!/usr/bin/env python3
"""audit65.py -- the four states of `term65_store` counted per arrival
population and read against task 64's `regate64_store`, plus the
consistency line and the layer-5 tally.

WHAT IT ANSWERS, in the brief's own order:

  1. the four states -- proved / disproved / undecided / no term --
     per population, term65 beside task 64, with every difference
     named as a finding with its cause;
  2. the consistency line: units proved on one route and DISPROVED on
     the other, which must be 0;
  3. layer 5: how many proved terms produced a normalized text, and
     how many refused;
  4. the disproved population carried with its CAUSE, so the 2,862
     units of log_168 section 5.3 are visible as one cause rather
     than 3,134 separate facts.

WRITES:
  audit65.json
  audit65_printed.txt

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

LINES = []

STATES = ["proved", "disproved", "undecided", "no term"]

POPULATIONS = ["original", "interpreter", "regenerated"]


def log(text):
    LINES.append(text)
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def read_store(store):
    out = {}
    pattern = os.path.join(HERE, store, "*.json")
    for path in sorted(glob.glob(pattern)):
        document = json.load(open(path))
        for name in document["units"]:
            out[name] = document["units"][name]
    return out


def state_of(record):
    """the FOUR STATES, read off one record.  The same function task
    64 used, so the two rounds are counted the same way."""
    if record.get("term_state") == "NO_TERM":
        return "no term"
    if record.get("proved"):
        return "proved"
    if record.get("outcome") == "DISPROVED":
        return "disproved"
    return "undecided"


def tally(records):
    out = {}
    for name in records:
        record = records[name]
        population = record.get("population")
        key = (population, state_of(record))
        out[key] = out.get(key, 0) + 1
    return out


def disproved_cause(record):
    """the CAUSE a disproof is carried with.

    log_168 section 5.3 established one cause for the bulk of them:
    the unit's body transfers into a routine the toolchain's own
    archive defines, and canon39's ledger -- built with the four-name
    runtime set of task 59 -- carries no row for that transfer, so the
    stored term asserts the transfer changed nothing.  The machine-form
    test for that cause is on the record itself: the body has a call
    line and the ledger made no runtime_callee row for it.  Everything
    else is 'another cause', counted and not explained away."""
    calls = record.get("call_lines") or 0
    rows = record.get("runtime_callee_rows") or 0
    targets = record.get("call_targets") or []
    if calls > 0 and rows == 0:
        return cause_of_a_rowless_transfer(targets)
    if calls > 0:
        return ("a transfer into the compiler's own runtime that the "
                "ledger DID row; the disproof has another cause")
    if record.get("holes"):
        return ("the body does not transfer and the walk left a hole; "
                "the disproof has another cause")
    return ("the body does not transfer and the walk left no hole; "
            "the disproof has another cause")


def is_positional_label(target):
    """`L0`, `L1`, ... -- the positional branch label the wrapped text
    puts in place of an address.  ROUND 10 RULING (4) makes labels
    positional in the wrapped text, so a transfer whose target prints
    as one is a transfer the wrapped text has already normalized; the
    routine's own identity lives in the attachment file, not here."""
    if len(target) < 2:
        return False
    if target[0] != "L":
        return False
    return target[1:].isdigit()


def cause_of_a_rowless_transfer(targets):
    """the cause of a disproof on a body that transfers and whose
    ledger made no row for the transfer, split by the SHAPE of the
    target -- machine form, never a name we chose.

    Three shapes appear, and they are three different facts:
    a positional label (the archive routine, whose identity the
    attachment file holds), a named panic routine (a guard response,
    not a lowering), and an indirect transfer through memory."""
    named = []
    indirect = 0
    labels = 0
    for target in targets:
        if is_positional_label(target):
            labels = labels + 1
            continue
        if target.startswith("*"):
            indirect = indirect + 1
            continue
        named.append(target)
    if named:
        return ("the body transfers to a NAMED routine that is not a "
                "lowering -- a panic or abort path reached on a guard, "
                "so the disproof is about the guard's response, not "
                "about a missing runtime row")
    if indirect and not labels:
        return ("the body transfers INDIRECTLY through memory, so the "
                "target is not statically named and no runtime row "
                "could be made for it")
    return ("log_168 section 5.3: the body transfers into a routine "
            "the toolchain's archive defines and canon39's ledger "
            "carries no row for it, so the stored term asserts the "
            "transfer changed nothing.  FIX PLANNED ROUND 14 -- the "
            "canon rebuild with the archive index's own runtime set.")


def call_targets():
    """unit -> the targets its body transfers to, read off the wrapped
    text canon39 stored.  One pass over the same shards term65_run
    walked."""
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
        for name in document.get("units", {}):
            unit = document["units"][name]
            if unit.get("outcome") != "WRAPPED_TEXT_PROVED":
                continue
            found = []
            for raw in unit.get("body_verbatim") or []:
                text = raw.split("!!")[0].strip()
                if text == "":
                    continue
                head = text.split(" ", 1)[0]
                if head != "call":
                    continue
                if " " not in text:
                    found.append("")
                    continue
                found.append(text.split(" ", 1)[1].strip())
            if found:
                out[name] = found
    return out


def call_bearing(record):
    """does this unit's body transfer at all?  Read off the banked
    task-64 record's own count, which the re-gate wrote."""
    return record.get("call_lines")


def main():
    now = read_store("term65_store")
    was = read_store("regate64_store")
    log("-- the populations")
    log("   term65_store records  %d" % len(now))
    log("   regate64_store records %d" % len(was))

    tally_now = tally(now)
    tally_was = tally(was)

    log("")
    log("-- THE FOUR STATES, per arrival population")
    log("   %-14s %-11s %9s %9s %7s"
        % ("population", "state", "task 64", "term65", "move"))
    totals_now = {}
    totals_was = {}
    differences = []
    for population in POPULATIONS:
        for state in STATES:
            key = (population, state)
            a = tally_was.get(key, 0)
            b = tally_now.get(key, 0)
            totals_was[state] = totals_was.get(state, 0) + a
            totals_now[state] = totals_now.get(state, 0) + b
            log("   %-14s %-11s %9d %9d %+7d"
                % (population, state, a, b, b - a))
            if a != b:
                differences.append({
                    "population": population,
                    "state": state,
                    "task64": a,
                    "term65": b,
                })
    log("")
    for state in STATES:
        log("   %-14s %-11s %9d %9d %+7d"
            % ("ALL", state, totals_was.get(state, 0),
               totals_now.get(state, 0),
               totals_now.get(state, 0) - totals_was.get(state, 0)))
    log("   %-14s %-11s %9d %9d"
        % ("ALL", "TOTAL", len(was), len(now)))
    log("")
    log("   the brief's line from task 64: 26,594 proved / 3,134 "
        "disproved / 285 undecided / 419 no term over 30,432")
    log("   term65 reproduces:            %d / %d / %d / %d over %d"
        % (totals_now.get("proved", 0),
           totals_now.get("disproved", 0),
           totals_now.get("undecided", 0),
           totals_now.get("no term", 0), len(now)))
    log("   states that differ from task 64: %d" % len(differences))
    for one in differences:
        log("       %s %s: %d -> %d"
            % (one["population"], one["state"], one["task64"],
               one["term65"]))

    log("")
    log("-- WHY they reproduce, said mechanically rather than claimed")
    banked = 0
    gated_here = 0
    disagreements = 0
    for name in now:
        record = now[name]
        source = record.get("verdict_source") or ""
        if source.startswith("regate64_store"):
            banked = banked + 1
        else:
            gated_here = gated_here + 1
        if record.get("transcription_agrees_with_task64") is False:
            disagreements = disagreements + 1
    log("   verdicts carried from the gate of record  %d" % banked)
    log("   verdicts gated by this run                %d" % gated_here)
    log("   units where this run's transcription and task 64's "
        "disagree about whether a term exists  %d" % disagreements)

    log("")
    log("-- THE CONSISTENCY LINE")
    inconsistent = []
    for name in now:
        record = now[name]
        ship = record.get("verdict_ship") or {}
        text = record.get("verdict_text") or {}
        outcomes = [ship.get("outcome"), text.get("outcome")]
        if "PROVED" in outcomes and "DISPROVED" in outcomes:
            inconsistent.append(name)
    log("   units proved on one route and disproved on the other: %d"
        % len(inconsistent))

    log("")
    log("-- LAYER 5, computed only for a PROVED term")
    with_text = 0
    refused_text = 0
    texts = set()
    for name in now:
        record = now[name]
        if not record.get("proved"):
            continue
        if record.get("layer5_normalized_text"):
            with_text = with_text + 1
            texts.add(record["layer5_normalized_text"])
            continue
        refused_text = refused_text + 1
    log("   proved terms                       %d"
        % totals_now.get("proved", 0))
    log("   of them, a normalized text exists  %d" % with_text)
    log("   of them, normalization refused     %d" % refused_text)
    log("   distinct layer-5 texts             %d" % len(texts))

    log("")
    log("-- THE DISPROVED POPULATION, carried with its CAUSE")
    causes = {}
    targets = call_targets()
    for name in now:
        record = now[name]
        if state_of(record) != "disproved":
            continue
        banked_record = was.get(name) or {}
        record_for_cause = dict(record)
        record_for_cause["call_lines"] = banked_record.get("call_lines")
        record_for_cause["call_targets"] = targets.get(name) or []
        cause = disproved_cause(record_for_cause)
        causes.setdefault(cause, 0)
        causes[cause] = causes[cause] + 1
    for cause in sorted(causes, key=lambda one: -causes[one]):
        log("   %6d  %s" % (causes[cause], cause))
    log("")
    log("   THE DISPROVED ARE NOT LAYER-5 ELIGIBLE.  A term that does "
        "not prove is withdrawn, not kept as a weaker key, so these "
        "%d units enter the pool as members that cannot merge on "
        "layer 5 and carry their cause."
        % totals_now.get("disproved", 0))

    document = {
        "meta": {
            "generated_by": "audit65.py",
            "node": "hq.research.compiler_graph.term",
            "gate_of_record": "regate64_store -- task 64",
            "what_it_is": "the four states of term65_store per "
                          "arrival population, read against task 64, "
                          "with the consistency line, the layer-5 "
                          "tally and the disproved population's "
                          "causes",
        },
        "term65": {
            "records": len(now),
            "proved": totals_now.get("proved", 0),
            "disproved": totals_now.get("disproved", 0),
            "undecided": totals_now.get("undecided", 0),
            "no_term": totals_now.get("no term", 0),
        },
        "task64": {
            "records": len(was),
            "proved": totals_was.get("proved", 0),
            "disproved": totals_was.get("disproved", 0),
            "undecided": totals_was.get("undecided", 0),
            "no_term": totals_was.get("no term", 0),
        },
        "per_population": [
            {"population": population, "state": state,
             "task64": tally_was.get((population, state), 0),
             "term65": tally_now.get((population, state), 0)}
            for population in POPULATIONS for state in STATES],
        "states_that_differ": differences,
        "verdicts_from_the_gate_of_record": banked,
        "verdicts_gated_by_this_run": gated_here,
        "transcription_disagreements_with_task64": disagreements,
        "units_proved_on_one_route_and_disproved_on_the_other":
            len(inconsistent),
        "layer5": {
            "proved_terms": totals_now.get("proved", 0),
            "with_a_normalized_text": with_text,
            "normalization_refused": refused_text,
            "distinct_texts": len(texts),
        },
        "disproved_by_cause": causes,
    }
    handle = open(os.path.join(HERE, "audit65.json"), "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    handle = open(os.path.join(HERE, "audit65_printed.txt"), "w")
    handle.write("\n".join(LINES) + "\n")
    handle.close()
    log("")
    log("-- wrote audit65.json and audit65_printed.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
