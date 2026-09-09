#!/usr/bin/env python3
"""interp103_term.py -- TASK 103, round 19, step 2.1: build the term
for `cpython/long_mul`'s canonical-form record and report the verdict
of that term against the unit's OWN ship body.

WHAT IS REUSED, NOT COPIED.  `term97_walk.build` is CALLED to build
the one `Reference`, one `Term` and one `Gate` the round already uses
(this is "term97_walk.py's function" the brief names); `term66_run
.one_unit` -- the record `term97_walk.py`'s own docstring says is
reused rather than re-typed -- is CALLED on this task's own unit.
Neither `term97_walk.py` nor `term66_run.py` nor `term.py` nor
`gate.py` is edited.

THIS IS A NEW POPULATION FOR THIS MACHINERY, said plainly: canon40 (the
population `term66_run` / `term97_walk` finished) is the 31,078
COMPILED units; the eleven interpreter units task 96 put on
`canonical_form.py` were never walked through `Term.transcribe` by any
prior task.  So whatever verdict this program reports is the first
time this walk has been asked about an interpreter handler.

MEMORY BOUND, stated: one unit, one z3 context, in-process (no fork --
`term97_walk`'s fork-per-unit arrangement exists to keep z3's context
from accumulating across a POPULATION; one unit does not need it).
Named abort at the instance's stated 6 GB ceiling: `ABORT_MEMORY_T103`.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim.
"""

import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import term97_walk as T97                                        # noqa: E402
import term66_run as TR                                           # noqa: E402

CANONICAL = os.path.join(HERE, "interp103_canonical.json")
OUT = os.path.join(HERE, "interp103_term.json")

MEMORY_ABORT_KB = 6 * 1024 * 1024


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def memory_guard(where):
    now = peak_kb()
    if now > MEMORY_ABORT_KB:
        raise SystemExit(
            "ABORT_MEMORY_T103 at %s: peak resident %d kB is past the "
            "instance's stated 6 GB bound" % (where, now))
    return now


def area_row_shape_problem(unit):
    """None, or the named cause `term66_run.runtime_rows_of` will hit:
    it reads `row["produced_by"].get("kind")`, and the seventh block
    kind's AREA rows carry `produced_by == "arrival"` (a plain string,
    `t96_arriving_area`'s own convention), which has no `.get`."""
    for row in unit.get("ledger") or []:
        producer = row.get("produced_by")
        if not isinstance(producer, dict):
            return (
                "term66_run.runtime_rows_of reads "
                "row['produced_by'].get('kind') for every ledger row; "
                "row %r (block %r) carries produced_by=%r, which is a "
                "plain string, not the {kind: ...} shape ordinary rows "
                "carry -- t96_arriving_area.py's AREA rows were never "
                "walked through term66_run.one_unit before this task. "
                "Neither file is edited; the FORM 3 (Part B) term route "
                "is reported NOT_ATTEMPTED for this reason instead."
                % (row.get("row"), row.get("block"), producer))
    return None


def unit_from_form(record, form_key, name):
    """the shape `term.Term.transcribe` / `term66_run.one_unit` need:
    the FORM's own wrap() fields (body_verbatim, arrival_families,
    ledger, result_family, ...), plus the unit's name and language,
    exactly as a canon40 unit record carries them."""
    form = record[form_key]
    unit = dict(form)
    unit["unit"] = name
    unit["lang"] = "cpython"
    unit["population"] = "interpreter"
    unit["operator"] = record.get("label")
    unit["arrival_annotation"] = "plain"
    return unit


def main():
    print("[1/3] building the shared Reference / Term / Gate "
          "(term97_walk.build, unmodified)", flush=True)
    maker, gate, attached, readings = T97.build()
    memory_guard("build")

    record = json.load(open(CANONICAL))["record"]

    print("[2/3] cpython/long_mul, FORM 2 (canonical_form.py, Part A) "
          "-- term66_run.one_unit", flush=True)
    unit_form2 = unit_from_form(record, "the_canonical_form",
                                "cpython/long_mul")
    result_form2 = TR.one_unit(maker, gate, "cpython/long_mul",
                               unit_form2)
    memory_guard("form two term")

    print("[3/3] cpython/long_mul, FORM 3 (canonical_form.py + the "
          "seventh block kind, Part B) -- term66_run.one_unit",
          flush=True)
    unit_form3 = unit_from_form(
        record, "the_canonical_form_with_the_seventh_block",
        "cpython/long_mul")
    shape_problem = area_row_shape_problem(unit_form3)
    if shape_problem is not None:
        # NOT WORKED AROUND: `term66_run.runtime_rows_of` reads every
        # ledger row's `produced_by` as a dict with a `kind` field
        # (`producer.get("kind")`); the seventh block kind's AREA rows
        # carry `produced_by == "arrival"`, a plain string, which is a
        # real shape mismatch between task 96's ledger extension and
        # the canon40-era term machinery neither of them has been run
        # against the other before now.  Recorded as a named cause,
        # `term66_run.py` and `t96_arriving_area.py` are both left
        # exactly as they are.
        result_form3 = {
            "unit": "cpython/long_mul",
            "term_state": "NOT_ATTEMPTED",
            "why_not_attempted": shape_problem,
            "proved": False,
        }
    else:
        result_form3 = TR.one_unit(maker, gate, "cpython/long_mul",
                                   unit_form3)
    peak = memory_guard("form three term")

    document = {
        "meta": {
            "generator": "interp103_term.py",
            "task": "TASK 103 round 19 -- cpython's integer multiply "
                    "fast path against c's 64-bit multiply unit",
            "reused_unmodified": ["term97_walk.build",
                                  "term66_run.one_unit"],
            "note": "the eleven interpreter units were never walked "
                    "through Term.transcribe before this task; this is "
                    "the first verdict this machinery has produced for "
                    "an interpreter handler",
            "peak_resident_kb": peak,
            "memory_abort_name": "ABORT_MEMORY_T103",
        },
        "form_two": result_form2,
        "form_three": result_form3,
    }
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    print("wrote %s" % OUT, flush=True)
    print("peak resident kB: %d" % peak, flush=True)
    for key, result in (("form_two", result_form2),
                        ("form_three", result_form3)):
        print("%-10s term_state=%-10s outcome=%-10s proved=%s"
              % (key, result.get("term_state"), result.get("outcome"),
                 result.get("proved")), flush=True)
        if result.get("term_state") == "NO_TERM":
            print("   why_no_term: %s" % result.get("why_no_term"),
                  flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
