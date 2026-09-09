#!/usr/bin/env python3
"""show61.py -- ONE TRANSCRIPTION, SHOWN LITERALLY.

The term CORE says a term is the ledger read from OUT-0 downward.
This file prints one unit's whole route so the claim can be checked
rather than believed: the body verbatim, every ledger row with its
typed producer, the body line the relink attached to that row, the
term each row carries, the OUT-0 read, the two gate verdicts, and the
layer-5 normalized text.

Usage: show61.py [unit-label]   (default `go/op_319`, the CORE's own
worked instance, whose layer-5 text is `v0 + v1`.)

Coding discipline: no compound one-liner statements.
No operator token appears in this file.
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canonical_form as CF                                      # noqa: E402
import gate as G                                                 # noqa: E402
import reference as R                                            # noqa: E402
import term as T                                                 # noqa: E402
import term61_run as RUN                                         # noqa: E402

LINES = []


def log(text):
    LINES.append(text)
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def find(label):
    for path in RUN.shards():
        document = json.load(open(path))
        units = document.get("units", {})
        if label in units:
            return units[label], os.path.basename(path)
    return None, None


def main():
    label = "go/op_319"
    if len(sys.argv) > 1:
        label = sys.argv[1]
    unit, where = find(label)
    if unit is None:
        log("no unit %r in canon39" % label)
        return 1
    reference = R.Reference()
    maker = T.Term(reference=reference,
                   runtime_routines=CF.runtime_routine_names(),
                   runtime_units=RUN.runtime_units())
    gate = G.Gate(reference=reference)

    log("UNIT            %s   (from %s)" % (label, where))
    log("language        %s" % unit.get("lang"))
    log("population      %s" % unit.get("population"))
    log("arrival         %s" % json.dumps(unit.get("arrival_families")))
    log("answer home     %s at %s bits"
        % (unit.get("result_family"), unit.get("result_width")))
    log("")
    log("THE BODY, VERBATIM (the compiler's own text, untouched)")
    for line in unit.get("body_verbatim") or []:
        log("    %s" % line)
    log("")
    log("THE WRAPPED TEXT (layer 3, the runnable record)")
    log("    %s" % unit.get("wrapped_text_resolved"))
    log("")

    rows, line_of_row, _occurrence = T.relink(
        unit, runtime_routines=CF.runtime_routine_names())
    walked = maker.transcribe(unit)
    log("THE LEDGER, ROW BY ROW, WITH THE LINE THE RELINK ATTACHED")
    log("    %-8s %-46s %-24s %s"
        % ("row", "produced_by (typed)", "line", "term"))
    for row in rows:
        name = row["row"]
        term = walked.terms.get(name)
        if term is None:
            shown = "(no term)"
        else:
            shown = str(term)
        shown = " ".join(shown.split())
        if len(shown) > 60:
            shown = shown[:57] + "..."
        line = line_of_row.get(name)
        if line is None:
            line = "-"
        log("    %-8s %-46s %-24s %s"
            % (name, json.dumps(row["produced_by"], sort_keys=True),
               line, shown))
    log("")
    log("THE READ AT OUT-0 (layer 4, the term)")
    if walked.out_term is None:
        log("    (no term: %s)" % RUN.why_no_term(walked))
        return 1
    log("    %s" % " ".join(str(walked.out_term).split()))
    log("")
    log("THE TWO GATE ROUTES")
    first = gate.prove_term_against_ship(walked.out_term, unit)
    log("    route one  %s" % first.outcome)
    log("               %s" % first.reason)
    second = gate.prove_term_against_text(walked.out_term, unit)
    log("    route two  %s" % second.outcome)
    log("               %s" % second.reason)
    log("")
    log("THE NORMALIZED TEXT (layer 5, the comparison key)")
    if first.proved() or second.proved():
        log("    %s" % maker.normalize(walked.out_term))
    else:
        log("    (withdrawn: a term that does not prove has no key)")
    log("")
    log("HOLES %d, CASCADES %d, SLOT DISAGREEMENTS %d"
        % (len(walked.holes), len(walked.cascades),
           len(walked.slot_disagreements)))

    stem = label.replace("/", "_")
    path = os.path.join(HERE, "show61_%s.txt" % stem)
    handle = open(path, "w")
    handle.write("\n".join(LINES) + "\n")
    handle.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
