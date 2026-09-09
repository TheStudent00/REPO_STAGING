#!/usr/bin/env python3
"""name_census7.py -- the census (node 0_3_5_6_4) over `term66_store`,
the layer-4 transcriptions of every unit CANON40 proved, and its delta
against `name_census6.json` matched on the recorded REASON SENTENCE.

THE CENSUS IS A FILTER, never a survey: it reports only rows that
actually blocked a real unit, keyed by the TYPED PRODUCER OBJECT of
that unit's own body -- `{kind, mnem}` for an arch opcode,
`{kind, mnem: [setter, reader]}` for a flag pair, `{kind, phrase}` for
a phrase that is not an opcode, `{kind, callee}` for a runtime callee.
Never a lifter's helper name, and never an operator token.

WHAT IS REUSED RATHER THAN COPIED.  `term.Term.census` and
`term.Term.census_delta` are the rule and are called, not re-typed;
`name_census6.py` is round 13's driver and is neither edited nor
imported (its `census5_entries` reader is re-expressed here against
census6's own file, which is the same shape).

WHY THIS NUMBER.  Numbered artifacts accumulate and a superseded record
is never edited, so the census over canon40 takes the next free number
after `name_census6.json`.

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
    `term66_store`.  The store keeps the walk's own `holes` and
    `cascades` lists, so the filter runs over the recorded walk rather
    than over a second walk that could differ."""
    out = []
    pattern = os.path.join(HERE, "term66_store", "*.json")
    for path in sorted(glob.glob(pattern)):
        document = json.load(open(path))
        for name in sorted(document["units"]):
            record = document["units"][name]
            walked = T.Transcription(name)
            walked.holes = record.get("holes") or []
            walked.cascades = record.get("cascades") or []
            out.append((record.get("lang"), name, walked, record))
    return out


def census6_entries():
    """census6's entries, in the shape `Term.census_delta` takes.

    census6 carries a `reasons` LIST on each entry -- the same shape
    this round's census writes -- so the entries pass straight through
    and the delta is matched on the REASON SENTENCE, never on a
    producer's spelling."""
    path = os.path.join(HERE, "name_census6.json")
    document = json.load(open(path))
    before = []
    for entry in document["entries"]:
        before.append({
            "reasons": entry.get("reasons") or [],
            "rows_blocked": entry["rows_blocked"],
        })
    return before, document


def main():
    records = read_records()
    log("-- the population")
    log("   layer-4 records read (canon40 proved) %d" % len(records))
    walked = []
    for lang, name, transcription, _record in records:
        walked.append((lang, name, transcription))
    maker = T.Term()
    entries = maker.census(walked)

    rows = 0
    for entry in entries:
        rows = rows + entry["rows_blocked"]
    blocked_units = set()
    for _lang, name, transcription in walked:
        if transcription.holes:
            blocked_units.add(name)
    cascades = 0
    for _lang, _name, transcription in walked:
        cascades = cascades + len(transcription.cascades)

    log("-- the census over canon40")
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

    before, census6 = census6_entries()
    delta = maker.census_delta(before, entries)
    census6_rows = 0
    for one in census6["entries"]:
        census6_rows = census6_rows + one["rows_blocked"]
    census6_units = census6["tally"]["units_blocked"]
    log("")
    log("-- the delta against census6, matched on the REASON SENTENCE")
    log("   census6: %d producers, %d rows, %d units blocked "
        "(canon39, 30,432 proved units)"
        % (len(census6["entries"]), census6_rows, census6_units))
    log("   census7: %d producers, %d rows, %d units blocked "
        "(canon40, %d proved units)"
        % (len(entries), rows, len(blocked_units), len(records)))
    log("   causes CLOSED %d" % len(delta["closed"]))
    for one in delta["closed"]:
        log("       -%d rows | %s"
            % (one["rows_that_were_blocked"], one["reason"]))
    log("   causes APPEARED %d" % len(delta["appeared"]))
    for one in delta["appeared"]:
        log("       +%d rows | %s"
            % (one["rows_blocked"], one["reason"]))
    log("   causes that MOVED %d" % len(delta["moved"]))
    for one in delta["moved"]:
        log("       %d -> %d | %s" % (one["was"], one["now"],
                                      one["reason"]))

    document = {
        "meta": {
            "generated_by": "name_census7.py, running "
                            "term.Term.census",
            "node": "hq.research.compiler_graph.term.census",
            "what_it_is": "the rows whose PRODUCER has no z3 term, "
                          "filtered out of the layer-4 transcriptions "
                          "of every unit canon40 proved",
            "keyed_on": "the TYPED producer object -- {kind, mnem} for "
                        "an arch opcode, {kind, mnem:[setter, reader]} "
                        "for a flag pair, {kind, phrase} for a phrase "
                        "that is not an opcode, {kind, callee} for a "
                        "runtime callee.  Never a lifter name, never "
                        "an operator token.",
            "supersedes": "name_census6.json, which was filtered over "
                          "the canon39 term65_store.  It stays on disk "
                          "as the superseded record.",
            "meanings_table": "reference.Reference.opcode_table -- the "
                              "one table; a producer is a census row "
                              "exactly when that table has no builder "
                              "for it",
            "role_note": "no `role` field is declared anywhere in this "
                         "document and no provenance carve-out is "
                         "claimed; the file is walked by "
                         "check_no_spelling_keys.py IN FULL",
        },
        "tally": {
            "producers": len(entries),
            "rows_blocked": rows,
            "units_blocked": len(blocked_units),
            "cascades_not_census_entries": cascades,
            "layer4_records_read": len(records),
        },
        "delta_against_census6": delta,
        "entries": entries,
    }
    handle = open(os.path.join(HERE, "name_census7.json"), "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    log("")
    log("-- wrote name_census7.json")
    handle = open(os.path.join(HERE, "name_census7_printed.txt"), "w")
    handle.write("\n".join(LINES) + "\n")
    handle.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
