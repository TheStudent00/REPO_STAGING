#!/usr/bin/env python3
"""audit66.py -- the four states of `term66_store` (canon40) counted per
arrival population and read against `term65_store` (canon39), every
movement carried with its COMPUTED cause, the consistency line, the
layer-5 tally, the expectation of log_168 section 5.3 TESTED, and the
442 units task 79 flagged RESOLVED BY CAUSE.

WHAT IT ANSWERS, in the brief's own order:

  1. the four states -- proved / disproved / undecided / no term --
     per population, term66 beside term65, against the round-13 line
     26,594 / 3,134 / 285 / 419 over 30,432;
  2. EVERY MOVEMENT with its computed cause, joined on the unit name,
     so a unit that changed state is counted once with a reason and
     never as two independent facts;
  3. the consistency line: units proved on one route and DISPROVED on
     the other, which must be 0;
  4. layer 5: how many proved terms produced a normalized text, how
     many refused, and how many distinct texts;
  5. THE EXPECTATION, tested rather than assumed: log_168 section 5.3
     said the disproved population was dominated by units whose runtime
     transfer had no ledger row.  log_185 section 5.1 recomputed the
     CARRYING population as 3,619 in canon39 and 0 in canon40.  This
     audit measures how many of canon39's 3,134 disproved units stop
     being disproved, and names what remains BY CAUSE;
  6. THE 442 task 79 flagged -- units whose OUT-0 built a term under
     canon39's ledger and builds none under canon40's -- grouped by the
     written reason the walk itself recorded, so the answer is a cause
     list and not a unit list.

WRITES:
  audit66.json
  audit66_printed.txt

WHAT IS REUSED RATHER THAN COPIED.  `audit65.state_of` and
`audit65.is_positional_label` are called, not re-typed, so the two
rounds count the four states by one function and read a transfer
target's SHAPE by one rule.  `audit65.disproved_cause` is NOT reused:
its sentences name canon39 and a fix planned for round 14, and copying
them onto canon40 rows would put a false statement inside an artifact.
The cause sentences below are this round's own and say canon40.

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

import audit65 as A65                                            # noqa: E402

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


def tally(records):
    out = {}
    for name in records:
        record = records[name]
        population = record.get("population")
        key = (population, A65.state_of(record))
        out[key] = out.get(key, 0) + 1
    return out


# ------------------------------------------------------------------
# the cause of a disproof, on a canon40 record
# ------------------------------------------------------------------

def transfer_shape(record):
    """the SHAPE of what this body transfers to, read off the targets
    the wrapped text itself carries.  Three shapes, three facts: a
    positional label (the archive routine, whose identity the
    attachment file holds), a named routine (a panic or abort path),
    and an indirect transfer through memory."""
    named = 0
    indirect = 0
    labels = 0
    for target in record.get("call_targets") or []:
        if A65.is_positional_label(target):
            labels = labels + 1
            continue
        if target.startswith("*"):
            indirect = indirect + 1
            continue
        named = named + 1
    return named, indirect, labels


def disproved_cause(record):
    """the CAUSE a canon40 disproof is carried with.

    The machine-form tests are on the record itself: how many transfer
    lines the body has, how many ledger rows name a runtime callee, and
    the shape of the transfer targets."""
    calls = record.get("call_lines") or 0
    rows = record.get("runtime_callee_rows") or 0
    named, indirect, labels = transfer_shape(record)
    if calls == 0:
        if record.get("holes"):
            return ("the body does not transfer and the walk left a "
                    "hole; the disproof is about a producer the one "
                    "table has no builder for")
        return ("the body does not transfer and the walk left no "
                "hole; the disproof is about the modelled meaning of "
                "an opcode the table does have")
    if rows > 0:
        return ("the body transfers into the compiler's own runtime "
                "and canon40's ledger DID row it, one row per register "
                "family the attached callee changes; the disproof has "
                "another cause")
    if named > 0:
        return ("the body transfers to a NAMED routine that is not a "
                "lowering -- a panic or abort path reached on a guard, "
                "so the disproof is about the guard's response and no "
                "runtime row is owed")
    if indirect > 0 and labels == 0:
        return ("the body transfers INDIRECTLY through memory, so the "
                "target is not statically named and no runtime row "
                "could be made for it")
    return ("the body transfers to a positional label and canon40's "
            "ledger made no row for it; this is the shape log_168 "
            "section 5.3 named and canon40 was built to close")


def carrier_population(records):
    """log_185 section 5.1's carrying population, recomputed on this
    store: a unit whose body transfers and whose ledger carries NO row
    naming a runtime callee.  The measurement there was over the whole
    31,078 attempted; this one is over the store's own population and
    says so."""
    total = 0
    for name in records:
        record = records[name]
        calls = record.get("call_lines") or 0
        rows = record.get("runtime_callee_rows") or 0
        if calls == 0:
            continue
        if rows > 0:
            continue
        total = total + 1
    return total


def transferring(records):
    total = 0
    for name in records:
        if (records[name].get("call_lines") or 0) > 0:
            total = total + 1
    return total


def runtime_rows(records):
    total = 0
    for name in records:
        total = total + (records[name].get("runtime_callee_rows") or 0)
    return total


# ------------------------------------------------------------------
# the report
# ------------------------------------------------------------------

def four_states(now, was):
    tally_now = tally(now)
    tally_was = tally(was)
    log("-- THE FOUR STATES, per arrival population")
    log("   %-14s %-11s %9s %9s %7s"
        % ("population", "state", "term65", "term66", "move"))
    totals_now = {}
    totals_was = {}
    rows = []
    for population in POPULATIONS:
        for state in STATES:
            key = (population, state)
            a = tally_was.get(key, 0)
            b = tally_now.get(key, 0)
            totals_was[state] = totals_was.get(state, 0) + a
            totals_now[state] = totals_now.get(state, 0) + b
            log("   %-14s %-11s %9d %9d %+7d"
                % (population, state, a, b, b - a))
            rows.append({"population": population, "state": state,
                         "term65": a, "term66": b})
    log("")
    for state in STATES:
        log("   %-14s %-11s %9d %9d %+7d"
            % ("ALL", state, totals_was.get(state, 0),
               totals_now.get(state, 0),
               totals_now.get(state, 0) - totals_was.get(state, 0)))
    log("   %-14s %-11s %9d %9d"
        % ("ALL", "TOTAL", len(was), len(now)))
    return totals_now, totals_was, rows


def movements(now, was):
    """EVERY movement, joined on the unit name.

    A unit in one store and not the other is its own movement class,
    because the two populations are not the same set: canon39 proved
    30,432 wrapped texts and canon40 proves 30,324."""
    moves = {}
    detail = {}
    for name in sorted(now):
        before = was.get(name)
        after = A65.state_of(now[name])
        if before is None:
            key = ("not in canon39's proved set", after)
        else:
            key = (A65.state_of(before), after)
        moves[key] = moves.get(key, 0) + 1
        detail.setdefault(key, [])
        detail[key].append(name)
    for name in sorted(was):
        if name in now:
            continue
        key = (A65.state_of(was[name]), "not in canon40's proved set")
        moves[key] = moves.get(key, 0) + 1
        detail.setdefault(key, [])
        detail[key].append(name)
    return moves, detail


def movement_cause(key, names, now, was):
    """the COMPUTED cause of one movement class.

    Nothing here is asserted: each cause is a statement about fields on
    the records themselves, and the counts that support it are printed
    beside it."""
    before, after = key
    if before == after:
        return "no movement -- the state is the same in both rounds"
    if after == "not in canon40's proved set":
        return ("canon40 did not prove this unit's WRAPPED TEXT, so it "
                "was never transcribed this round; the layer-3 route "
                "is where it stopped, not the term route")
    if before == "not in canon39's proved set":
        return ("canon39 did not prove this unit's WRAPPED TEXT, so "
                "term65 never transcribed it; canon40 proves it and "
                "the term route reaches it for the first time")
    rowed = 0
    rowless = 0
    for name in names:
        rows = now[name].get("runtime_callee_rows") or 0
        if rows > 0:
            rowed = rowed + 1
            continue
        rowless = rowless + 1
    if before == "disproved" and after == "proved":
        return ("the ledger now rows the runtime transfer, so the term "
                "no longer asserts the transfer changed nothing "
                "(%d of %d carry a runtime row in canon40)"
                % (rowed, len(names)))
    if before == "disproved" and after == "no term":
        return ("the ledger now rows the runtime transfer and the walk "
                "descends into the attached callee's own body, where a "
                "producer the one table has no builder for stops the "
                "walk (%d of %d carry a runtime row in canon40)"
                % (rowed, len(names)))
    if before == "proved" and after == "no term":
        return ("the ledger now rows the runtime transfer and the walk "
                "descends into the attached callee's own body, where a "
                "producer the one table has no builder for stops the "
                "walk (%d of %d carry a runtime row in canon40)"
                % (rowed, len(names)))
    if after == "proved":
        return ("the transcription changed under canon40's ledger and "
                "the gate now proves the term (%d of %d carry a "
                "runtime row in canon40)" % (rowed, len(names)))
    if after == "disproved":
        return ("the transcription changed under canon40's ledger and "
                "the gate now finds a starting state under which the "
                "term and the unit's own machine code differ (%d of "
                "%d carry a runtime row in canon40)"
                % (rowed, len(names)))
    if after == "undecided":
        return ("the transcription changed under canon40's ledger and "
                "neither route answered inside its limit (%d of %d "
                "carry a runtime row in canon40)"
                % (rowed, len(names)))
    return ("the transcription changed under canon40's ledger (%d of "
            "%d carry a runtime row in canon40)" % (rowed, len(names)))


def main():
    now = read_store("term66_store")
    was = read_store("term65_store")
    log("-- the populations")
    log("   term66_store records (canon40 proved) %d" % len(now))
    log("   term65_store records (canon39 proved) %d" % len(was))
    log("   canon40 proved 30,324 of 31,078 attempted; canon39 proved "
        "30,432 of the same 31,078 (log_185 section 4.1)")
    log("")

    totals_now, totals_was, per_population = four_states(now, was)
    log("")
    log("   the round-13 line: 26,594 proved / 3,134 disproved / 285 "
        "undecided / 419 no term over 30,432")
    log("   term65_store reproduces:  %d / %d / %d / %d over %d"
        % (totals_was.get("proved", 0), totals_was.get("disproved", 0),
           totals_was.get("undecided", 0),
           totals_was.get("no term", 0), len(was)))
    log("   term66 over canon40:      %d / %d / %d / %d over %d"
        % (totals_now.get("proved", 0), totals_now.get("disproved", 0),
           totals_now.get("undecided", 0),
           totals_now.get("no term", 0), len(now)))

    log("")
    log("-- EVERY MOVEMENT, joined on the unit name, with its computed "
        "cause")
    moves, detail = movements(now, was)
    ordered = sorted(moves, key=lambda one: -moves[one])
    movement_rows = []
    for key in ordered:
        names = detail[key]
        cause = movement_cause(key, names, now, was)
        log("   %6d  %-30s -> %-30s" % (moves[key], key[0], key[1]))
        log("           cause: %s" % cause)
        log("           sightings: %s" % ", ".join(sorted(names)[:4]))
        movement_rows.append({
            "was": key[0],
            "now": key[1],
            "units": moves[key],
            "cause": cause,
            "sightings": sorted(names)[:8],
        })

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
    log("-- LAYER 5, computed only for a PROVED term, by task 79's "
        "corrected rule")
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
    was_texts = set()
    for name in was:
        record = was[name]
        if not record.get("proved"):
            continue
        if record.get("layer5_normalized_text"):
            was_texts.add(record["layer5_normalized_text"])
    log("   proved terms                       %d"
        % totals_now.get("proved", 0))
    log("   of them, a normalized text exists  %d" % with_text)
    log("   of them, normalization refused     %d" % refused_text)
    log("   distinct layer-5 texts, term66     %d" % len(texts))
    log("   distinct layer-5 texts, term65     %d" % len(was_texts))

    log("")
    log("-- THE EXPECTATION OF log_168 SECTION 5.3, TESTED")
    log("   the carrying population, recomputed on each store: a unit "
        "whose body transfers and whose ledger carries NO row naming a "
        "runtime callee")
    log("   term65_store (canon39 proved, %d units)" % len(was))
    log("       units whose body transfers               %d"
        % transferring(was))
    log("       of those, with NO runtime row            %d"
        % carrier_population(was))
    log("       runtime_callee rows over the store       %d"
        % runtime_rows(was))
    log("   term66_store (canon40 proved, %d units)" % len(now))
    log("       units whose body transfers               %d"
        % transferring(now))
    log("       of those, with NO runtime row            %d"
        % carrier_population(now))
    log("       runtime_callee rows over the store       %d"
        % runtime_rows(now))
    log("")
    was_disproved = []
    for name in was:
        if A65.state_of(was[name]) == "disproved":
            was_disproved.append(name)
    still = []
    left = {}
    for name in was_disproved:
        record = now.get(name)
        if record is None:
            left["not in canon40's proved set"] = \
                left.get("not in canon40's proved set", 0) + 1
            continue
        state = A65.state_of(record)
        left[state] = left.get(state, 0) + 1
        if state == "disproved":
            still.append(name)
    log("   canon39's disproved population           %d"
        % len(was_disproved))
    log("   where each of them stands in canon40:")
    for state in sorted(left, key=lambda one: -left[one]):
        log("       %6d  %s" % (left[state], state))

    log("")
    log("-- WHAT REMAINS DISPROVED, by cause")
    causes = {}
    cause_sightings = {}
    for name in now:
        if A65.state_of(now[name]) != "disproved":
            continue
        cause = disproved_cause(now[name])
        causes[cause] = causes.get(cause, 0) + 1
        cause_sightings.setdefault(cause, [])
        cause_sightings[cause].append(name)
    for cause in sorted(causes, key=lambda one: -causes[one]):
        log("   %6d  %s" % (causes[cause], cause))
        log("           sightings: %s"
            % ", ".join(sorted(cause_sightings[cause])[:4]))

    log("")
    log("-- THE 442 TASK 79 FLAGGED, resolved by cause")
    log("   task 79 measured, over the 26,594 units term65 proved, "
        "that 442 build no OUT-0 term under the ledger as task 78 left "
        "it (209 c, 233 cpp).  The same population is recomputed here "
        "off the two stores rather than carried from the log.")
    lost = []
    for name in was:
        if not was[name].get("proved"):
            continue
        record = now.get(name)
        if record is None:
            continue
        if record.get("term_state") == "NO_TERM":
            lost.append(name)
    by_lang = {}
    by_reason = {}
    reason_sightings = {}
    for name in lost:
        lang = now[name].get("lang")
        by_lang[lang] = by_lang.get(lang, 0) + 1
        reason = now[name].get("why_no_term")
        by_reason[reason] = by_reason.get(reason, 0) + 1
        reason_sightings.setdefault(reason, [])
        reason_sightings[reason].append(name)
    log("   units term65 PROVED whose term66 record has NO term  %d"
        % len(lost))
    log("   by language: %s" % json.dumps(by_lang, sort_keys=True))
    log("   by the written reason the walk itself recorded:")
    for reason in sorted(by_reason, key=lambda one: -by_reason[one]):
        log("       %6d  %s" % (by_reason[reason], reason))
        log("               sightings: %s"
            % ", ".join(sorted(reason_sightings[reason])[:4]))
    rowed = 0
    for name in lost:
        if (now[name].get("runtime_callee_rows") or 0) > 0:
            rowed = rowed + 1
    log("   of them, carrying at least one runtime_callee row in "
        "canon40: %d of %d" % (rowed, len(lost)))

    document = {
        "meta": {
            "generated_by": "audit66.py",
            "node": "hq.research.compiler_graph.term",
            "what_it_is": "the four states of term66_store (canon40) "
                          "per arrival population, read against "
                          "term65_store (canon39), with every movement "
                          "carried with its computed cause, the "
                          "consistency line, the layer-5 tally, the "
                          "log_168 expectation tested and the 442 of "
                          "task 79 resolved by cause",
            "before": "term65_store -- canon39, task 64's verdicts",
            "after": "term66_store -- canon40, gated by term66_run.py",
        },
        "term66": {
            "records": len(now),
            "proved": totals_now.get("proved", 0),
            "disproved": totals_now.get("disproved", 0),
            "undecided": totals_now.get("undecided", 0),
            "no_term": totals_now.get("no term", 0),
        },
        "term65": {
            "records": len(was),
            "proved": totals_was.get("proved", 0),
            "disproved": totals_was.get("disproved", 0),
            "undecided": totals_was.get("undecided", 0),
            "no_term": totals_was.get("no term", 0),
        },
        "per_population": per_population,
        "movements": movement_rows,
        "units_proved_on_one_route_and_disproved_on_the_other":
            len(inconsistent),
        "layer5": {
            "proved_terms": totals_now.get("proved", 0),
            "with_a_normalized_text": with_text,
            "normalization_refused": refused_text,
            "distinct_texts_term66": len(texts),
            "distinct_texts_term65": len(was_texts),
        },
        "the_expectation": {
            "term65_units_that_transfer": transferring(was),
            "term65_of_those_with_no_runtime_row":
                carrier_population(was),
            "term65_runtime_callee_rows": runtime_rows(was),
            "term66_units_that_transfer": transferring(now),
            "term66_of_those_with_no_runtime_row":
                carrier_population(now),
            "term66_runtime_callee_rows": runtime_rows(now),
            "canon39_disproved_population": len(was_disproved),
            "where_they_stand_in_canon40": left,
        },
        "what_remains_disproved_by_cause": causes,
        "the_442": {
            "units_term65_proved_with_no_term66_term": len(lost),
            "by_language": by_lang,
            "by_written_reason": by_reason,
            "carrying_a_runtime_callee_row_in_canon40": rowed,
            "units": sorted(lost),
        },
    }
    handle = open(os.path.join(HERE, "audit66.json"), "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    handle = open(os.path.join(HERE, "audit66_printed.txt"), "w")
    handle.write("\n".join(LINES) + "\n")
    handle.close()
    log("")
    log("-- wrote audit66.json and audit66_printed.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
