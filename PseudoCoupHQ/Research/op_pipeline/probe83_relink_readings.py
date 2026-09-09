#!/usr/bin/env python3
"""probe83_relink_readings.py -- the MEASUREMENT that decides whether
`term.relink` refusing 3,927 canon40 units is a defect in the relink or
a genuine gap in the one meanings table.

WHAT IS BEING ASKED.  `audit66_printed.txt` reports 3,962 units of the
30,324 canon40 proved with NO layer-4 term, and 3,927 of them carry one
written reason shape:

    the relink refused: relink raised Refusal: the transfer names
    '__truncsfhf2', which one of this machine's archives defines, but
    no reading of that body was handed to the ledger

That sentence is `ledger.Ledger.runtime_answer`'s own refusal.  Task 78
gave `ledger.Ledger` two new arguments -- `runtime_answers` (the
register families each attached callee's own body changes) and
`toolchain` -- and `canonical_form.CanonicalForm.wrap` hands both in
when it renders a unit.  `term.relink` builds its own `Ledger` subclass
and hands in neither, so the re-walk cannot make the rows the stored
ledger has, and refuses.

THE TWO POSSIBILITIES, and what separates them:

  A. A DEFECT IN THE RELINK.  Handed the same readings and toolchain
     the render was handed, the re-walk makes the same rows and
     `term.check_rebuild` passes.  Then the 3,927 are an artifact of
     the relink, not a fact about the corpus.
  B. A GENUINE GAP.  Even handed them, the re-walk disagrees with the
     stored ledger, or the walk then stops inside the attached callee's
     body at a producer the one table has no builder for.  Then the
     units belong in the census and the count stands.

This probe does not edit `term.py`.  It re-expresses `term.relink`'s
walk locally, with the two arguments added, and reports what happens on
a sample and then on every one of the refused units.  The duplication
is deliberate and temporary: the live module is not changed until the
measurement has decided which possibility holds and the rule has been
written into the CORE.

WRITES:
  probe83_relink_readings.json
  probe83_relink_readings_printed.txt

MEMORY BOUND: one canon40 shard is opened, walked and dropped before
the next; the bound is 6 GB resident with the named abort
`ABORT_MEMORY`.

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
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canonical_form as CF                                      # noqa: E402
import ledger as L                                               # noqa: E402
import term as T                                                 # noqa: E402
import term66_run as T66                                         # noqa: E402

LINES = []
MEMORY_CAP_KB = 6 * 1024 * 1024


def log(text):
    LINES.append(text)
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def check_memory():
    used = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if used > MEMORY_CAP_KB:
        raise SystemExit(
            "ABORT_MEMORY: peak resident %d kB passed the stated cap "
            "of %d kB" % (used, MEMORY_CAP_KB))
    return used


class _LineStamping(L.Ledger):
    """`term._LineStamping`, with the two arguments task 78 gave
    `ledger.Ledger` passed through.  Everything else is identical."""

    def __init__(self, runtime_routines=None, runtime_answers=None,
                 toolchain=None):
        L.Ledger.__init__(self, runtime_routines=runtime_routines,
                          runtime_answers=runtime_answers,
                          toolchain=toolchain)
        self.current_line = None
        self.occurrence = 0
        self.line_of_row = {}
        self.occurrence_of_row = {}

    def add(self, block, size, type_name, produced_by, operands,
            note=None, resident=None):
        row = L.Ledger.add(self, block, size, type_name, produced_by,
                           operands, note=note, resident=resident)
        self.line_of_row[row.name()] = self.current_line
        self.occurrence_of_row[row.name()] = self.occurrence
        return row


def relink_with_readings(unit, runtime_routines, runtime_answers,
                         toolchain):
    """`term.relink`, with the readings and the toolchain handed to the
    ledger the re-walk builds."""
    body = unit.get("body_verbatim")
    if not body:
        raise T.RelinkDisagreement("the unit record carries no body")
    ledger = _LineStamping(runtime_routines=runtime_routines,
                           runtime_answers=runtime_answers,
                           toolchain=toolchain)

    def recording_mnemonic_of(line):
        ledger.current_line = line
        ledger.occurrence = ledger.occurrence + 1
        return T._ORIGINAL_MNEMONIC_OF(line)

    families = unit.get("arrival_families") or []
    L.mnemonic_of = recording_mnemonic_of
    try:
        prelude = CF.Prelude(ledger).emit(families)
        arrival_rows = prelude[2]
        ledger.current_line = None
        ledger.walk_dataflow(body, arrival_rows, families)
    finally:
        L.mnemonic_of = T._ORIGINAL_MNEMONIC_OF
    stored = unit.get("ledger") or []
    rebuilt = ledger.as_list()
    T.check_rebuild(stored, rebuilt)
    return stored, ledger.line_of_row, ledger.occurrence_of_row


def refused_units():
    """the units `term66_store` records with NO term whose written
    reason is the ledger's own runtime-answer refusal."""
    head = ("the relink refused: relink raised Refusal: the transfer "
            "names")
    out = set()
    pattern = os.path.join(HERE, "term66_store", "*.json")
    for path in sorted(glob.glob(pattern)):
        document = json.load(open(path))
        for name in document["units"]:
            record = document["units"][name]
            if record.get("term_state") != "NO_TERM":
                continue
            reason = record.get("why_no_term") or ""
            if reason.startswith(head):
                out.add(name)
    return out


def main():
    wanted = refused_units()
    log("-- the population this probe asks about")
    log("   canon40 proved units whose term66 record carries the "
        "ledger's runtime-answer refusal: %d" % len(wanted))

    readings = CF.runtime_answer_readings()
    routines = CF.runtime_routine_names(readings)
    log("   readings handed in: %d keys, %d routine names"
        % (len(readings), len(routines)))

    tallies = {
        "relinked": 0,
        "relink still refused": 0,
        "rebuild disagreed": 0,
    }
    sightings = {}
    for key in tallies:
        sightings[key] = []
    peak = 0
    for path in T66.shards():
        document = json.load(open(path))
        found = wanted & set(document.get("units", {}))
        if not found:
            continue
        for name in sorted(found):
            unit = dict(document["units"][name])
            unit["unit"] = name
            toolchain = CF.TOOLCHAIN_OF_LANGUAGE.get(unit.get("lang"))
            try:
                relink_with_readings(unit, routines, readings,
                                     toolchain)
                outcome = "relinked"
            except T.RelinkDisagreement as problem:
                outcome = "rebuild disagreed"
                if len(sightings[outcome]) < 6:
                    sightings[outcome].append("%s: %s"
                                              % (name, problem))
            except Exception as problem:                # noqa: BLE001
                outcome = "relink still refused"
                if len(sightings[outcome]) < 6:
                    sightings[outcome].append(
                        "%s: %s: %s" % (name, type(problem).__name__,
                                        problem))
            if outcome == "relinked" and len(sightings[outcome]) < 6:
                sightings[outcome].append(name)
            tallies[outcome] = tallies[outcome] + 1
        peak = check_memory()

    log("")
    log("-- WHAT HAPPENS WHEN THE READINGS AND THE TOOLCHAIN ARE "
        "HANDED IN")
    for key in sorted(tallies, key=lambda one: -tallies[one]):
        log("   %6d  %s" % (tallies[key], key))
        for one in sightings[key]:
            log("           %s" % one)
    log("")
    log("   peak resident %d kB against the stated 6 GB cap" % peak)

    verdict = None
    if tallies["relinked"] == len(wanted):
        verdict = ("A DEFECT IN THE RELINK.  Every one of the %d "
                   "refused units re-walks and its rebuild matches "
                   "the stored canon40 ledger row for row once the "
                   "same readings and toolchain the render was handed "
                   "are handed to the relink." % len(wanted))
    else:
        verdict = ("MIXED.  %d of %d re-walk cleanly; the rest are "
                   "named above with their own refusal, and belong to "
                   "the census rather than to the relink."
                   % (tallies["relinked"], len(wanted)))
    log("")
    log("-- THE VERDICT")
    log("   %s" % verdict)

    document = {
        "meta": {
            "generated_by": "probe83_relink_readings.py",
            "node": "hq.research.compiler_graph.term.transcribe",
            "what_it_is": "whether term.relink's refusal of 3,927 "
                          "canon40 units is a defect in the relink or "
                          "a gap in the one meanings table",
            "method": "term.relink re-expressed locally with the "
                      "runtime answer readings and the toolchain "
                      "passed to the ledger it builds; term.py is NOT "
                      "edited by this probe",
        },
        "units_asked_about": len(wanted),
        "readings_keys": len(readings),
        "routine_names": len(routines),
        "tallies": tallies,
        "sightings": sightings,
        "verdict": verdict,
        "peak_resident_kb": peak,
    }
    handle = open(os.path.join(HERE, "probe83_relink_readings.json"),
                  "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    handle = open(os.path.join(
        HERE, "probe83_relink_readings_printed.txt"), "w")
    handle.write("\n".join(LINES) + "\n")
    handle.close()
    log("")
    log("-- wrote probe83_relink_readings.json and "
        "probe83_relink_readings_printed.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
