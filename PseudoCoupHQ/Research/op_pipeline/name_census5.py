#!/usr/bin/env python3
"""name_census5.py -- the census over canon39, written by
`term.Term.census` (node 0_3_5_6_4).

THE CENSUS IS A FILTER, NEVER A SURVEY.  It reports only rows that
actually blocked a real unit, keyed by the TYPED PRODUCER of that
unit's own body -- never by a lifter's helper name and never by an
operator token.  Each entry carries a written reason sentence, and it
is that sentence, not a producer's spelling, that groups entries when
two rounds are compared.

WRITES:
  name_census5.json          the census over canon39
  name_census5_printed.txt   the census printed, and the delta vs
                             census4 by cause

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

import term as T                                                 # noqa: E402

LINES = []


def log(text):
    LINES.append(text)
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def read_records():
    """(lang, unit, transcription-shaped record) for every unit in
    term61_store."""
    out = []
    pattern = os.path.join(HERE, "term61_store", "*.json")
    for path in sorted(glob.glob(pattern)):
        document = json.load(open(path))
        for name in sorted(document["units"]):
            record = document["units"][name]
            walked = T.Transcription(name)
            walked.holes = record.get("holes") or []
            walked.cascades = record.get("cascades") or []
            out.append((record.get("lang"), name, walked, record))
    return out


def census4_reasons():
    """census4's entries, read as {reason sentence: rows blocked}."""
    path = os.path.join(HERE, "name_census4.json")
    document = json.load(open(path))
    out = {}
    for entry in document["entries"]:
        reason = entry.get("cannot_model_because")
        if reason is None:
            continue
        out.setdefault(reason, 0)
        out[reason] += entry["rows_blocked"]
    return out, document


def main():
    records = read_records()
    log("-- the population")
    log("   layer-4 records read %d" % len(records))
    walked = []
    for lang, name, transcription, _record in records:
        walked.append((lang, name, transcription))
    maker = T.Term()
    entries = maker.census(walked)

    rows = 0
    units = set()
    for entry in entries:
        rows = rows + entry["rows_blocked"]
        for name in entry["units"]:
            units.add(name)
    blocked_units = set()
    for _lang, name, transcription in walked:
        if transcription.holes:
            blocked_units.add(name)
    cascades = 0
    for _lang, _name, transcription in walked:
        cascades = cascades + len(transcription.cascades)

    log("-- the census over canon39")
    log("   producers %d" % len(entries))
    log("   rows blocked %d" % rows)
    log("   units blocked %d" % len(blocked_units))
    log("   cascades (not census entries) %d" % cascades)
    log("")
    log("   %-46s %8s %8s  %s"
        % ("producer", "rows", "units", "languages"))
    for entry in entries:
        log("   %-46s %8d %8d  %s"
            % (T.producer_key(entry["producer"]),
               entry["rows_blocked"], entry["units_blocked"],
               ",".join(entry["languages"])))
    log("")
    log("-- each producer's written reason sentence")
    for entry in entries:
        log("   %s" % T.producer_key(entry["producer"]))
        for reason in entry["reasons"]:
            log("       %s" % reason)

    was, census4 = census4_reasons()
    before = []
    for reason in sorted(was):
        before.append({"reasons": [reason], "rows_blocked": was[reason]})
    delta = maker.census_delta(before, entries)
    log("")
    log("-- the delta against census4, matched on the REASON SENTENCE")
    log("   census4: %d producers, %d rows"
        % (len(census4["entries"]),
           sum(one["rows_blocked"] for one in census4["entries"])))
    log("   census5: %d producers, %d rows" % (len(entries), rows))
    log("   causes CLOSED %d" % len(delta["closed"]))
    for one in delta["closed"]:
        log("       -%d rows | %s"
            % (one["rows_that_were_blocked"], one["reason"]))
    log("   causes APPEARED %d" % len(delta["appeared"]))
    for one in delta["appeared"]:
        log("       +%d rows | %s" % (one["rows_blocked"], one["reason"]))
    log("   causes that MOVED %d" % len(delta["moved"]))
    for one in delta["moved"]:
        log("       %d -> %d | %s" % (one["was"], one["now"],
                                      one["reason"]))

    document = {
        "meta": {
            "generated_by": "name_census5.py, running "
                            "term.Term.census",
            "node": "hq.research.compiler_graph.term.census",
            "what_it_is": "the rows whose PRODUCER has no z3 term, "
                          "filtered out of the layer-4 transcriptions "
                          "of every unit canon39 proved",
            "keyed_on": "the TYPED producer object -- {kind, mnem} for "
                        "an arch opcode, {kind, mnem:[setter, reader]} "
                        "for a flag pair, {kind, phrase} for a phrase "
                        "that is not an opcode, {kind, callee} for a "
                        "runtime callee.  Never a lifter name, never "
                        "an operator token.",
            "supersedes": "name_census4.json, which was filtered over "
                          "canon38.  It stays on disk as the "
                          "superseded record.",
            "meanings_table": "reference.Reference.opcode_table -- the "
                              "one table; a producer is a census row "
                              "exactly when that table has no builder "
                              "for it",
        },
        "tally": {
            "producers": len(entries),
            "rows_blocked": rows,
            "units_blocked": len(blocked_units),
            "cascades_not_census_entries": cascades,
            "layer4_records_read": len(records),
        },
        "delta_against_census4": delta,
        "entries": entries,
    }
    handle = open(os.path.join(HERE, "name_census5.json"), "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    log("")
    log("-- wrote name_census5.json")
    handle = open(os.path.join(HERE, "name_census5_printed.txt"), "w")
    handle.write("\n".join(LINES) + "\n")
    handle.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
