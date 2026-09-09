#!/usr/bin/env python3
"""t96_analysis.py -- WHAT MOVED THE VERDICTS, separated into the two
things that could have.

TASK 96, round 19.  Ten of the eleven units move from UNDECIDED to
PROVED_BY_CONSTRUCTION.  TWO THINGS CHANGED AT ONCE between log_199's
baseline and this lap, and a report that does not separate them is
worthless:

  (a) THE FORM changed.  `region36` REWRITES every location in the
      body into `0x<offset>(%r15)`; `canonical_form.py` WRAPS a body
      it does not touch.

  (b) THE INSTRUMENT changed.  Task 94 gated with its own
      `gate_against_own_ship` (`t94_recarve.py`), which is SOLVER
      ONLY -- z3, or UNDECIDED.  This lap gates with `gate.py`'s
      `Gate.prove_wrapped`, which asks the solver first and falls to
      six mechanical checks when the reference has no model for
      something the body spells.

THIS PROGRAM SHOWS THAT (b) IS A CONSEQUENCE OF (a), NOT A SECOND
CAUSE.  It runs `gate.py`'s OWN structural checks against FORM 1's
text -- the same instrument, the other form -- and prints which check
fails and on which line.  `gate.py`'s own words for why the route
exists:

    "Because the canonical form applies NO transformation to the
    body, the obligation reduces to two claims that can be checked by
    looking: the compiler's body is present and unchanged, and the
    added plumbing cannot disturb it."

A form that rewrites the body cannot make the first claim.  If C1
fails on FORM 1's text, then the structural route was never available
to the region form, and the instrument difference is the form
difference wearing another hat.  If C1 PASSES on FORM 1's text, then
part of the movement IS an instrument artifact and this program says
so.  The answer is printed, not assumed.

It also prints, per unit and per form:
  * the solver route's own outcome and the exact thing it had no
    model for -- so a PROVED_BY_CONSTRUCTION is never read as a
    solver proof;
  * every one of the six checks' notes;
  * whether the longer solver limit was reached at all.

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

No operator token appears in this file.  The population is the eleven
records of `t96_canonical.json`, in that file's own order.

Coding discipline: no compound one-liner statements.

usage:
  t96_analysis.py           writes t96_analysis.json and
                            t96_wrapped_texts.txt
"""

import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import gate as GATE                                               # noqa: E402
import ledger as L                                                # noqa: E402

MEMORY_CAP_KB = 6 * 1024 * 1024
MEMORY_ABORT = "T96_ANALYSIS_MEMORY_ABORT"

SOURCE = os.path.join(HERE, "t96_canonical.json")
OUT = os.path.join(HERE, "t96_analysis.json")
TEXTS = os.path.join(HERE, "t96_wrapped_texts.txt")


def check_memory(where):
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if peak > MEMORY_CAP_KB:
        raise MemoryError(
            "%s: peak resident size %d kB passed the stated 6 GB "
            "bound at %s" % (MEMORY_ABORT, peak, where))
    return peak


def the_six_checks(rendering):
    """every one of `gate.py`'s six checks, asked one at a time so a
    pass is a list of six notes rather than one word."""
    gate = GATE.Gate()
    fields = dict(rendering)
    out = []
    checks = (gate.check_one, gate.check_two, gate.check_three,
              gate.check_four, gate.check_five, gate.check_six)
    for check in checks:
        try:
            passed, note = check(fields)
        except Exception as problem:                      # noqa: BLE001
            out.append({
                "check": check.__name__,
                "passed": False,
                "note": "%s raised %s: %s"
                        % (check.__name__, type(problem).__name__,
                           problem),
            })
            continue
        if isinstance(note, list):
            note = " | ".join(note)
        out.append({
            "check": check.__name__,
            "passed": bool(passed),
            "note": note,
        })
    return out


def form_one_under_this_instrument(record):
    """`gate.py`'s OWN six checks, asked of FORM 1's text.

    The fields are built exactly as they would be for any wrapped
    text: the body as the compiler emitted it, and the region form's
    text in place of the wrapped one.  FORM 1 has no prelude or
    epilogue of the canonical form's shape, so those are empty, which
    is the honest rendering of a form that has neither.
    """
    old = record["the_superseded_form"]
    if old.get("wrapped_text") is None:
        return {
            "asked": False,
            "why": "this unit has no FORM 1 text: %s"
                   % old.get("refusal"),
        }
    canonical = record["the_canonical_form"]
    body = canonical.get("body_verbatim")
    if body is None:
        return {"asked": False,
                "why": "this unit has no wrapped body to compare"}
    fields = {
        "wrapped_text": old["wrapped_text"],
        "body_verbatim": body,
        "body_as_read": canonical.get("body_as_read"),
        "branch_labels": canonical.get("branch_labels"),
        "prelude": [],
        "epilogue": [],
        "prelude_scratch": None,
        "epilogue_scratch": None,
        "arrival_families": canonical.get("arrival_families") or [],
        "result_family": canonical.get("result_family"),
        "result_width": canonical.get("result_width"),
        "returns": canonical.get("returns"),
        "out_row": canonical.get("out_row"),
    }
    checks = the_six_checks(fields)
    first_failure = None
    for entry in checks:
        if not entry["passed"]:
            first_failure = entry
            break
    return {
        "asked": True,
        "the_six_checks": checks,
        "the_first_failure": first_failure,
        "the_structural_route_is_available_to_form_one":
            first_failure is None,
    }


def solver_route_of(rendering):
    """what the SOLVER route did, said separately from the verdict.

    `gate.py` words a structural verdict as 'the reference has no
    model for something this body spells (X), and the form applies NO
    transformation to the body, so the six mechanical checks carry
    it'.  X is the thing the solver route stopped on.
    """
    detail = rendering.get("verdict_detail") or ""
    verdict = rendering.get("verdict")
    if verdict == GATE.PROVED_ON_SHIP:
        return {
            "the_solver_answered": True,
            "outcome": verdict,
            "what_it_had_no_model_for": None,
        }
    marker = "no model for something this body spells ("
    if marker in detail:
        piece = detail.split(marker, 1)[1]
        piece = piece.rsplit("), and", 1)[0]
        return {
            "the_solver_answered": False,
            "outcome": verdict,
            "what_it_had_no_model_for": piece,
        }
    return {
        "the_solver_answered": verdict in (GATE.PROVED_ON_SHIP,
                                           GATE.DISPROVED),
        "outcome": verdict,
        "what_it_had_no_model_for": None,
    }


def dump_texts(document, handle):
    for record in document["records"]:
        handle.write("=" * 70 + "\n")
        handle.write("UNIT %s\n" % record["unit"])
        handle.write("=" * 70 + "\n")
        old = record["the_superseded_form"]
        handle.write("\n-- FORM 1, region36 + canon36_universal "
                     "(SUPERSEDED RECORD) --\n")
        if old.get("wrapped_text") is None:
            handle.write("REFUSED: %s\n" % old.get("refusal"))
        else:
            for line in L.split_lines(old["wrapped_text"]):
                handle.write("  %s\n" % line)
        for key, title in (
                ("the_canonical_form",
                 "FORM 2, canonical_form.py (PART A)"),
                ("the_canonical_form_with_the_seventh_block",
                 "FORM 3, canonical_form.py + the seventh block "
                 "kind (PART B)")):
            rendering = record[key]
            handle.write("\n-- %s --\n" % title)
            if rendering.get("outcome") == "REFUSED":
                handle.write("REFUSED (%s): %s\n"
                             % (rendering.get("refusal_cause"),
                                rendering.get("refusal")))
                continue
            for line in L.split_lines(rendering["wrapped_text"]):
                handle.write("  %s\n" % line)
        handle.write("\n")


def main():
    document = json.load(open(SOURCE))
    records = []
    total = len(document["records"])
    for index, record in enumerate(document["records"]):
        sys.stderr.write("[%d/%d] %s\n" % (index + 1, total,
                                           record["unit"]))
        sys.stderr.flush()
        row = {
            "unit": record["unit"],
            "label": record.get("label"),
            "language": record.get("language"),
            "form_one_under_this_instrument":
                form_one_under_this_instrument(record),
        }
        for key, name in (
                ("the_canonical_form", "form_two"),
                ("the_canonical_form_with_the_seventh_block",
                 "form_three")):
            rendering = record[key]
            if rendering.get("outcome") == "REFUSED":
                row[name] = {
                    "outcome": "REFUSED",
                    "refusal_cause": rendering.get("refusal_cause"),
                    "refusal": rendering.get("refusal"),
                }
                continue
            row[name] = {
                "outcome": rendering.get("outcome"),
                "verdict": rendering.get("verdict"),
                "solver_route": solver_route_of(rendering),
                "the_six_checks": the_six_checks(rendering),
                "gate_at_20000ms": rendering.get("gate_at_20000ms"),
                "gate_at_120000ms": rendering.get("gate_at_120000ms"),
                "answer_changed_with_more_room":
                    rendering.get("answer_changed_with_more_room"),
                "wrapped_text_line_count":
                    len(L.split_lines(rendering["wrapped_text"])),
                "prelude": rendering.get("prelude"),
                "epilogue": rendering.get("epilogue"),
            }
        records.append(row)
        check_memory(record["unit"])

    available = 0
    asked = 0
    for row in records:
        one = row["form_one_under_this_instrument"]
        if not one.get("asked"):
            continue
        asked = asked + 1
        if one["the_structural_route_is_available_to_form_one"]:
            available = available + 1

    peak = check_memory("the end of the run")
    out = {
        "meta": {
            "generator": "t96_analysis.py",
            "task": "TASK 96 round 19 -- separating the form change "
                    "from the instrument change",
            "memory_bound_kB": MEMORY_CAP_KB,
            "memory_abort_name": MEMORY_ABORT,
            "peak_resident_size_kB": peak,
        },
        "records": records,
        "the_instrument_question": {
            "form_one_texts_asked": asked,
            "form_one_texts_the_structural_route_would_carry":
                available,
            "reading": "if this is 0, gate.py's structural route was "
                       "never available to the region form, so the "
                       "instrument difference between log_199 and this "
                       "lap is the FORM difference and not a second "
                       "cause",
        },
    }
    handle = open(OUT, "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    handle = open(TEXTS, "w")
    dump_texts(document, handle)
    handle.close()
    print("wrote %s" % OUT)
    print("wrote %s" % TEXTS)
    print("peak resident size kB: %d" % peak)
    print(json.dumps(out["the_instrument_question"], indent=1,
                     sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
