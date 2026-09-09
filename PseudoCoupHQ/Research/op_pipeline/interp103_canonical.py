#!/usr/bin/env python3
"""interp103_canonical.py -- TASK 103, round 19, step 2: `cpython/
long_mul` onto `canonical_form.py`, exactly as task 96 put the eleven
onto it (log_201).

WHAT IS REUSED, NOT COPIED.  `canonical_form.new_form`,
`t96_onto_canonical_form.AreaForm`, `.render_form_two`,
`.render_form_three` and `.contract_families` are CALLED, not
re-typed.  Neither `canonical_form.py` nor `t96_onto_canonical_form.py`
nor `t96_arriving_area.py` is edited.  FORM 2 is Part A (the ledger
prelude/epilogue, body verbatim); FORM 3 is Part A plus the seventh
block kind (an arriving addressable area) where the body needs one.
There is no FORM 1 for this unit -- `region36`/`canon36_universal` are
superseded records task 96 already stopped rendering into, and this
unit was never carved under them, so the FORM-1 field says so rather
than being invented.

THE ARRIVAL CONTRACT, read off the body the same way task 94 read
`long_add`'s (`t94_recarve.json`'s own evidence field, quoted in
interp103_report.md): the first touch of `%rdi` and `%rsi` are both
READS at a fixed displacement (`0x10`, the `lv_tag` field) before
either register is written, and the SysV convention agrees they are
argument 0 and argument 1.  `%rax` carries the returned pointer on
every `ret` this body has.  `{a: rdi, b: rsi, result: rax,
result_width: 64}`.

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

MEMORY BOUND, stated: one function body (658 bytes), one ledger, one
gate call.  Expected peak resident size under 200 MB (t96's own peaks
were 55-60 MB over eleven units).  Named abort at the instance's
stated 6 GB ceiling: `ABORT_MEMORY_T103`.
"""

import json
import os
import resource
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canonical_form as CF                                      # noqa: E402
import t96_onto_canonical_form as T96                             # noqa: E402

IN = os.path.join(HERE, "interp103_bounds.json")
OUT = os.path.join(HERE, "interp103_canonical.json")

MEMORY_ABORT_KB = 6 * 1024 * 1024

ARRIVAL_CONTRACT = {
    "a": "rdi",
    "b": "rsi",
    "result": "rax",
    "result_width": 64,
    "evidence": "read off the body: `mov 0x10(%rdi),%rax` and "
               "`mov 0x10(%rsi),%rdx` are the first dereferences of "
               "either family and are both reads, before either "
               "register is written (the copy `mov %rdi,%rbx` at "
               "entry is not a dereference); the SysV convention "
               "agrees. Same evidence shape as cpython/long_add's own "
               "arrival_contract in t94_recarve.json.",
}


def peak_kb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss


def memory_guard(where):
    now = peak_kb()
    if now > MEMORY_ABORT_KB:
        raise SystemExit(
            "ABORT_MEMORY_T103 at %s: peak resident %d kB is past the "
            "instance's stated 6 GB bound" % (where, now))
    return now


def main():
    bounds = json.load(open(IN))["record"]
    body = bounds.get("body") or []
    body_verbatim = [row["mnem"] for row in body]
    body_bytes = "".join(row["bytes"].replace(" ", "") for row in body)

    unit = {
        "unit": bounds["unit"],
        "label": bounds["label"],
        "language": bounds["language"],
        "handler_function": bounds["handler_function"],
        "body_verbatim": body_verbatim,
        "body_bytes": body_bytes,
        "arrival_contract": ARRIVAL_CONTRACT,
        "old_form": {
            "outcome": "NOT APPLICABLE",
            "wrapped_text": None,
            "note": "this unit was never carved under region36 / "
                    "canon36_universal (FORM 1): task 94/96 carved "
                    "only the addition population. FORM 1 is a "
                    "superseded record as of 2026-09-05 and this task "
                    "does not render into it.",
        },
        "old_verdict": None,
        "old_verdict_cause": None,
    }

    print("[1/3] FORM 2 -- canonical_form.py, unmodified", flush=True)
    plain = CF.new_form()
    form_two = T96.render_form_two(plain, unit)
    memory_guard("form two")

    print("[2/3] FORM 3 -- canonical_form.py + t96_arriving_area.py",
          flush=True)
    area_form = T96.AreaForm(
        runtime_routines=plain.runtime_routines,
        unattached_callers=plain.unattached_callers,
        runtime_answers=plain.runtime_answers)
    form_three = T96.render_form_three(area_form, unit)
    memory_guard("form three")

    print("[3/3] writing %s" % OUT, flush=True)
    record = {
        "unit": unit["unit"],
        "label": unit["label"],
        "language": unit["language"],
        "handler_function": unit["handler_function"],
        "body_instruction_count": len(body_verbatim),
        "body_bytes_were_read": bool(body_bytes),
        "arrival_contract": unit["arrival_contract"],
        "the_superseded_form": unit["old_form"],
        "the_canonical_form": form_two,
        "the_canonical_form_with_the_seventh_block": form_three,
    }
    peak = memory_guard("the end of the run")
    document = {
        "meta": {
            "generator": "interp103_canonical.py",
            "task": "TASK 103 round 19 -- cpython's integer multiply "
                    "fast path against c's 64-bit multiply unit",
            "reused_unmodified": [
                "canonical_form.new_form",
                "t96_onto_canonical_form.AreaForm",
                "t96_onto_canonical_form.render_form_two",
                "t96_onto_canonical_form.render_form_three",
            ],
            "form_two": "canonical_form.CanonicalForm.wrap, unmodified",
            "form_three": "the same, plus t96_arriving_area.py's "
                          "seventh block kind",
            "gate": "gate.py Gate.prove_wrapped against the unit's OWN "
                    "ship body, at 20,000 ms and again at 120,000 ms "
                    "when the first answer was undecided for time -- "
                    "the STRUCTURAL route (six mechanical checks), not "
                    "a term proof; see interp103_term.json for the "
                    "term route",
            "boundary": "the owner's ruling of 2026-09-05, applied here "
                        "exactly as task 94/96 applied it to "
                        "cpython/long_add: the unit is the whole "
                        "handler function's body.",
            "memory_bound_kB": MEMORY_ABORT_KB,
            "memory_abort_name": "ABORT_MEMORY_T103",
            "peak_resident_size_kB": peak,
            "spelling": "the member's display label travels on the "
                        "field `label`; no key, grouping, pairing, row "
                        "structure or selection in this file uses it",
        },
        "record": record,
    }
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    print("wrote %s" % OUT, flush=True)
    print("peak resident size kB: %d" % peak, flush=True)
    print("FORM 2 outcome: %s  verdict: %s"
          % (form_two.get("outcome"), form_two.get("verdict")),
          flush=True)
    print("FORM 3 outcome: %s  verdict: %s"
          % (form_three.get("outcome"), form_three.get("verdict")),
          flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
