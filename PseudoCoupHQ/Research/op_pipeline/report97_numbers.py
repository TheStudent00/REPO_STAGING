#!/usr/bin/env python3
"""report97_numbers.py -- every number log_202 states, printed off the
artifacts themselves, one section per command.

WHY IT EXISTS.  `check_conventions_log_claims.py` re-runs the commands
a DevComms log pasted and sorts each claim into matches / differs /
unverifiable.  Task 94 scored 19 matched of 32, 28% unverifiable.  A
claim only counts if the log carries a command that reproduces it, so
this file gives every figure in log_202 exactly one short, read-only,
non-elided command that prints it off the artifact on disk.

It computes nothing new.  It reads and counts.

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

No operator token appears in this file.  Nothing here groups, pairs or
selects units; it counts rows of artifacts already written.

usage:
  report97_numbers.py walk
  report97_numbers.py flags
  report97_numbers.py pass2
  report97_numbers.py control
  report97_numbers.py states
  report97_numbers.py pool
  report97_numbers.py census
  report97_numbers.py contamination
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def say(text):
    sys.stdout.write(text + "\n")


def tally(values):
    counts = {}
    for value in values:
        counts[value] = counts.get(value, 0) + 1
    return counts


def read(name):
    return json.load(open(os.path.join(HERE, name)))


def store_records():
    total = 0
    shards = sorted(glob.glob(os.path.join(HERE, "term66_store",
                                           "*.json")))
    for path in shards:
        total = total + len(json.load(open(path))["units"])
    return len(shards), total


def canon40_population():
    proved = 0
    attempted = 0
    inputs = []
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        inputs.append(os.path.join(HERE,
                                   "canon40_wrapped_%s.json" % lang))
    inputs.append(os.path.join(HERE, "canon40_interp.json"))
    inputs.extend(sorted(glob.glob(os.path.join(
        HERE, "canon40_regen_store", "*.json"))))
    for path in inputs:
        document = json.load(open(path))
        for name in document.get("units", {}):
            attempted = attempted + 1
            if document["units"][name].get("outcome") \
                    == "WRAPPED_TEXT_PROVED":
                proved = proved + 1
    return len(inputs), attempted, proved


def walk():
    inputs, attempted, proved = canon40_population()
    shards, records = store_records()
    state = read("term66_state.json")
    say("canon40 inputs                       %d" % inputs)
    say("canon40 units attempted              %d" % attempted)
    say("canon40 units proved (the population) %d" % proved)
    say("term66_store shards                  %d" % shards)
    say("term66_store records                 %d" % records)
    say("term66_state.json done inputs        %d" % len(state["done"]))
    say("records short of the population      %d" % (proved - records))
    pass1 = 0
    for path in sorted(glob.glob(os.path.join(
            HERE, "term97_flagged_slice*.json"))):
        pass1 = pass1 + json.load(open(path))["records_walked"]
    say("records pass 1 walked                %d" % pass1)
    say("records carried in from the handoff  %d" % (records - pass1
                                                     - stored_in_pass2()))
    say("records pass 2 added                 %d" % stored_in_pass2())


def pass2_rows():
    rows = []
    for path in sorted(glob.glob(os.path.join(HERE,
                                              "term97_pass2_*.json"))):
        for row in json.load(open(path))["rows"]:
            rows.append((os.path.basename(path), row))
    return rows


def stored_in_pass2():
    names = set()
    for where, row in pass2_rows():
        if not row["stored"]:
            continue
        names.add((row["shard"], row["unit"]))
    return len(names)


def flags():
    rows = []
    peaks = []
    for path in sorted(glob.glob(os.path.join(
            HERE, "term97_flagged_slice*.json"))):
        document = json.load(open(path))
        rows.extend(document["flagged"])
        peaks.append(document["parent_peak_kb"])
    say("flagged by pass 1                    %d" % len(rows))
    say("flagged by the word pass 1 recorded  %s"
        % json.dumps(tally(r["pass1_word"] for r in rows),
                     sort_keys=True))
    say("flagged by the token that fired      %s"
        % json.dumps(tally(str(r["pass1_token"]) for r in rows),
                     sort_keys=True))
    say("flagged by the term state pass 1 saw %s"
        % json.dumps(tally(str(r["pass1_partial_term_state"])
                           for r in rows), sort_keys=True))
    say("flagged by the verdict pass 1 saw    %s"
        % json.dumps(tally(str(r["pass1_partial_verdict"])
                           for r in rows), sort_keys=True))
    say("flagged by runtime-callee row count  %s"
        % json.dumps(tally(r["runtime_callee_rows"] for r in rows),
                     sort_keys=True))
    say("inputs holding a flagged unit        %d"
        % len(set(r["shard"] for r in rows)))
    say("pass 1 slice parents, peak resident kB %s" % sorted(peaks))


def pass2():
    legs = sorted(glob.glob(os.path.join(HERE,
                                         "term97_pass2_*.json")))
    for path in legs:
        document = json.load(open(path))
        say("%-32s ceiling %6d MB  wall %5d s  flagged %3d  "
            "stored %3d  not finished %3d"
            % (os.path.basename(path), document["ceiling_mb"],
               document["seconds"], document["flagged"],
               document["now_stored"],
               document["still_not_finished"]))
    rows = pass2_rows()
    say("pass-2 rows over every leg           %d" % len(rows))
    say("rows by the word the leg recorded    %s"
        % json.dumps(tally(row["pass2_word"] for where, row in rows),
                     sort_keys=True))
    landed = {}
    for where, row in rows:
        if not row["stored"]:
            continue
        key = "%s / %s" % (row.get("pass2_term_state"),
                           row.get("pass2_verdict"))
        landed[key] = landed.get(key, 0) + 1
    say("where the stored ones landed         %s"
        % json.dumps(landed, sort_keys=True))
    stuck = []
    for where, row in rows:
        if row["stored"]:
            continue
        stuck.append((row["shard"], row["unit"], row["pass2_word"],
                      row["pass2_ceiling_mb"], row["pass2_seconds"]))
    say("units still not finished             %d" % len(set(
        (one[0], one[1]) for one in stuck)))
    for one in sorted(set(stuck))[:40]:
        say("   %s %s %s at %d MB and %d s"
            % (one[0], one[1], one[2], one[3], one[4]))


def control():
    document = read("term97_control.json")
    say("control ceiling MB                   %d"
        % document["ceiling_mb"])
    say("control wall clock s                 %d" % document["seconds"])
    say("every Nth stored record              %d" % document["every"])
    say("records compared                     %d" % document["compared"])
    say("records identical                    %d" % document["identical"])
    say("records that differ                  %d" % document["differ"])
    fields = {}
    for row in document["rows"]:
        for field in row["fields_that_differ"]:
            fields[field] = fields.get(field, 0) + 1
    say("fields that differ, by field         %s"
        % json.dumps(fields, sort_keys=True))
    for row in document["rows"]:
        if row["identical"] is not False:
            continue
        say("   %s %s fields %s"
            % (row["shard"], row["unit"], row["fields_that_differ"]))


def states():
    document = read("audit66.json")
    before = document["term65"]
    after = document["term66"]
    say("the round-14 line, over %d records" % before["records"])
    say("   proved %d  disproved %d  undecided %d  no term %d"
        % (before["proved"], before["disproved"], before["undecided"],
           before["no_term"]))
    say("term66 over canon40, over %d records" % after["records"])
    say("   proved %d  disproved %d  undecided %d  no term %d"
        % (after["proved"], after["disproved"], after["undecided"],
           after["no_term"]))
    say("units proved on one route and disproved on the other %d"
        % document["units_proved_on_one_route_and_disproved_on_the_other"])
    say("layer 5: proved terms %d, with a normalized text %d, "
        "refused %d, distinct texts %d"
        % (document["layer5"]["proved_terms"],
           document["layer5"]["with_a_normalized_text"],
           document["layer5"]["normalization_refused"],
           document["layer5"]["distinct_texts_term66"]))
    say("movement rows recorded                %d"
        % len(document["movements"]))
    say("units carried by those rows           %d"
        % sum(one["units"] for one in document["movements"]))
    rows = sorted(document["movements"],
                  key=lambda one: (-one["units"], one["was"],
                                   one["now"]))
    for one in rows:
        say("   %6d units | was %-10s now %-10s | %s"
            % (one["units"], one["was"], one["now"], one["cause"]))
    say("the four states per arrival population")
    for one in document["per_population"]:
        say("   %-12s %-10s term65 %6d  term66 %6d"
            % (one["population"], one["state"], one["term65"],
               one["term66"]))
    say("what remains disproved, by computed cause")
    remains = document["what_remains_disproved_by_cause"]
    for key in sorted(remains, key=lambda k: (-remains[k], k)):
        say("   %6d | %s" % (remains[key], key))


def pool():
    before = read("the_pool5.json")["summary"]
    if not os.path.exists(os.path.join(HERE, "the_pool6.json")):
        say("the_pool6.json is NOT on disk.")
        say("pool66_run.py refused its own output: a pool cannot be "
            "built over a member set short of the population it "
            "names.")
        say("the pool5 line this round would have been read against:")
        for key in sorted(before):
            say("   %-52s %8s" % (key, before[key]))
        say("   %-52s %8d"
            % ("families",
               read("the_families5.json")["summary"]["families"]))
        return
    after = read("the_pool6.json")["summary"]
    families_before = read("the_families5.json")["summary"]["families"]
    families_after = read("the_families6.json")["summary"]["families"]
    keys = ["entries", "members",
            "entries_spanning_more_than_one_language",
            "entries_spanning_compiled_and_interpreted",
            "members_with_a_proved_term",
            "members_whose_term_was_withdrawn",
            "members_whose_term_was_undecided",
            "members_with_no_term",
            "members_not_layer5_eligible",
            "entries_carrying_more_than_one_wrapped_text",
            "distinct_layer5_texts_among_eligible_units"]
    say("%-52s %8s %8s %8s" % ("", "pool5", "pool6", "delta"))
    for key in keys:
        one = before.get(key)
        two = after.get(key)
        if one is None or two is None:
            say("%-52s %8s %8s" % (key, one, two))
            continue
        say("%-52s %8d %8d %8d" % (key, one, two, two - one))
    say("%-52s %8d %8d %8d" % ("families", families_before,
                               families_after,
                               families_after - families_before))
    delta = read("pool5_pool6_delta.json")
    for key in sorted(delta):
        value = delta[key]
        if isinstance(value, list):
            say("delta.%-46s %8d rows" % (key, len(value)))
            continue
        if isinstance(value, dict):
            say("delta.%-46s %8d keys" % (key, len(value)))
            continue
        say("delta.%-46s %8s" % (key, value))


def census():
    document = read("name_census7.json")
    for key in sorted(document):
        value = document[key]
        if isinstance(value, list):
            say("%-52s %8d rows" % (key, len(value)))
            continue
        if isinstance(value, dict):
            say("%-52s %8d keys" % (key, len(value)))
            continue
        say("%-52s %8s" % (key, value))


def contamination():
    """THE ONE PLACE THIS ROUND'S SHORTFALL LEAKS INTO A CAUSE
    SENTENCE, measured rather than left for a reader to find.

    `audit66.py` decides "not in canon40's proved set" by asking
    whether the unit has a record in `term66_store`.  44 units of the
    30,324 canon40 proves have no record because their layer-5
    normalization does not converge, not because canon40 refused
    them -- so for those 44 the cause sentence audit66.json carries is
    WRONG.  This counts them against that row's own population."""
    document = read("audit66.json")
    row = None
    for one in document["movements"]:
        if one["now"] != "not in canon40's proved set":
            continue
        row = one
    if row is None:
        say("audit66.json has no row landing outside canon40's "
            "proved set")
        return
    say("the movement row, its population and its cause")
    say("   units %d" % row["units"])
    say("   was %s, now %s" % (row["was"], row["now"]))
    say("   cause: %s" % row["cause"])
    short = set()
    for one in read("term97_finalize.json")["inputs_short"]:
        for name in one.get("missing_units") or []:
            short.add(name)
    say("units this round could not finish             %d" % len(short))
    seen = set(row["sightings"])
    say("of the row's pasted sightings, how many are ours %d of %d"
        % (len(seen & short), len(seen)))
    inputs, attempted, proved = canon40_population()
    say("canon40 units attempted                       %d" % attempted)
    say("canon40 units proved                          %d" % proved)
    say("canon40 units NOT proved                      %d"
        % (attempted - proved))
    say("the row's units, less the ones we could not finish %d"
        % (row["units"] - len(short)))


def main():
    what = sys.argv[1]
    table = {"walk": walk, "flags": flags, "pass2": pass2,
             "control": control, "states": states, "pool": pool,
             "census": census, "contamination": contamination}
    if what not in table:
        raise SystemExit("unknown section %r" % what)
    table[what]()


if __name__ == "__main__":
    main()
