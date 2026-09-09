#!/usr/bin/env python3
"""interp103_gate_c181.py -- TASK 103, round 19, step 2: gate
`cpython/long_mul`'s term against `c/op_181`'s term and body, on the
projection where both operands are compact.

THE PROJECTION, LITERAL, from the source this task read (Include/
internal/pycore_long.h, this ship build -- interp103_report.md quotes
the lines verbatim):

    _PyLong_BothAreCompact(a, b):
        (a->long_value.lv_tag | b->long_value.lv_tag) < (2 << NON_SIZE_BITS)
    NON_SIZE_BITS = 3, so the threshold is 2 << 3 = 16 = 0xf+1
    (`cmp $0xf,%rcx; jbe ...` in the compiled body is this test).
    PyLong_SHIFT = 30 (Include/cpython/longintrepr.h, 64-bit build).

A tag combined-OR under 16 means each operand's own digit count is 0
or 1 (tag = 8*ndigits + sign/flag bits, NON_SIZE_BITS=3 low bits).  One
digit is `PyLong_SHIFT` = 30 bits.  So: **the projection is both
operands' MAGNITUDE in [0, 2**30 - 1], independently signed** --
value in [-(2**30-1), 2**30-1] each.  This is stated once here and
never recomputed elsewhere in this task's artifacts.

WHY THIS PROGRAM DOES NOT REACH A SOLVER QUERY.  `interp103_term.json`
already answers whether `cpython/long_mul`'s FORM 2 term is proved
equal to the unit's own ship body: it is not -- UNDECIDED on both
routes gate.py tries (§ meta.route_ship / route_text below, read back
rather than recomputed).  A term whose own verdict is UNDECIDED is not
sound ground to gate against a SECOND unit's term: doing so would be
comparing c/op_181's PROVED term to an object this same task's own
machinery could not certify, and reporting whatever z3 said about that
pairing as "the handler's term against c's" would misstate what was
asked and answered.  So this program's OWN gate is: read
`interp103_term.json`'s form_two verdict, and if it is not proved,
refuse to project rather than manufacture a comparison -- reported
here as **NO_TERM**, by the SAME two named causes, plus the reason the
one path that could still supply a sound per-operand binding (the
seventh block kind, Part B) is unavailable (recorded in
`interp103_term.json`'s `form_three` field: `NOT_ATTEMPTED`, ledger
shape mismatch).  This mirrors exactly the class of outcome the brief
names: "NO_TERM by cause ... the walk refuses cycles; say exactly
where" -- corrected, by the machine's own evidence, from "a loop in
x_mul / Karatsuba" (never reached: `k_mul` is a `call`, a transfer OUT
of the unit's own bounds, not walked into) to the loop this body
itself contains at its own bytes, named by address in
interp103_report.md.

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

TERM_IN = os.path.join(HERE, "interp103_term.json")
POOL_IN = os.path.join(HERE, "the_pool5.json")
C_UNITS_IN = os.path.join(HERE, "canon40_wrapped_c.json")
OUT = os.path.join(HERE, "interp103_gate_c181.json")

MEMORY_ABORT_KB = 6 * 1024 * 1024

PROJECTION = {
    "literal_source": "Include/internal/pycore_long.h (this ship "
                      "build): `_PyLong_BothAreCompact(a, b): "
                      "(a->long_value.lv_tag | b->long_value.lv_tag) < "
                      "(2 << NON_SIZE_BITS)`, NON_SIZE_BITS = 3 -- the "
                      "compiled test is `cmp $0xf,%rcx; jbe ...` "
                      "(threshold 0x10). PyLong_SHIFT = 30 "
                      "(Include/cpython/longintrepr.h).",
    "meaning": "each operand's own digit count is 0 or 1 (tag = "
              "8*ndigits + 3 flag bits); one digit is 30 bits",
    "bound": "both operands' magnitude in [0, 2**30 - 1], "
            "independently signed -- value in "
            "[-(2**30-1), 2**30-1] each",
    "value_low": -(2**30 - 1),
    "value_high": 2**30 - 1,
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


def c181_pool_entry():
    pool = json.load(open(POOL_IN))
    for entry in pool["entries"]:
        for member in entry["members"]:
            if member["unit"] == "c/op_181":
                return entry["entry_id"], member
    raise SystemExit("c/op_181 not found in the_pool5.json")


def main():
    entry_id, member = c181_pool_entry()
    print("[1/2] c/op_181's pool entry and proved term (read, not "
          "rebuilt): entry %s, term_outcome=%s, "
          "layer5_normalized_text=%r"
          % (entry_id, member.get("term_outcome"),
             member.get("layer5_normalized_text")), flush=True)

    term_doc = json.load(open(TERM_IN))
    form_two = term_doc["form_two"]
    form_three = term_doc["form_three"]

    print("[2/2] cpython/long_mul's own term verdict, read back from "
          "interp103_term.json rather than recomputed", flush=True)
    proved = bool(form_two.get("proved"))

    if proved:
        # not reached today, kept honest rather than dead code with a
        # false guarantee: if a future run of interp103_term.py DOES
        # prove the term, this branch is where a real z3 projection
        # query belongs, gated by G.Gate.comparable on the two out
        # terms.  It is not written speculatively here.
        outcome = "NOT_IMPLEMENTED_FOR_A_PROVED_TERM"
        cause = ("form_two.proved is true, which this task's own run "
                "never observed; a solver-level projection over the "
                "compact bound would be the next step and is not "
                "written here because it was not exercised")
    else:
        outcome = "NO_TERM"
        cause = {
            "headline": "cpython/long_mul's FORM 2 term is UNDECIDED "
                        "against its own body on both routes gate.py "
                        "tries, so it is not sound ground to gate "
                        "against c/op_181's PROVED term; no projected "
                        "comparison is run",
            "route_ship": form_two.get("verdict_ship", {}).get(
                "reason"),
            "route_text": form_two.get("verdict_text", {}).get(
                "reason"),
            "seventh_block_kind_unavailable":
                form_three.get("why_not_attempted"),
            "correction_to_the_briefs_own_guess":
                "the brief's example cause was 'a loop in x_mul / "
                "Karatsuba'; k_mul is never walked into (it is a "
                "`call`, a transfer OUT of long_mul's own bounds, "
                "attached as a runtime_callee row, not a cycle). The "
                "REAL cycle the reference named is a loop INSIDE "
                "long_mul's own bytes: the digit-store loop at "
                "0x1396c0..0x1396d3 (`jne 1396c0`) that fills a "
                "freshly allocated 2-digit result when the product "
                "needs more than one 30-bit digit but fewer than "
                "three. interp103_report.md quotes its bytes.",
        }

    document = {
        "meta": {
            "generator": "interp103_gate_c181.py",
            "task": "TASK 103 round 19 -- cpython's integer multiply "
                    "fast path against c's 64-bit multiply unit",
            "reused_read_only": ["the_pool5.json (c/op_181's pool "
                                 "entry and proved term)",
                                 "interp103_term.json (this task's "
                                 "own prior step)"],
            "peak_resident_kb": memory_guard("end"),
            "memory_abort_name": "ABORT_MEMORY_T103",
        },
        "projection": PROJECTION,
        "c_op_181": {
            "pool_entry_id": entry_id,
            "term_outcome": member.get("term_outcome"),
            "term_state": member.get("term_state"),
            "layer5_normalized_text": member.get(
                "layer5_normalized_text"),
            "wrapped_text": member.get("wrapped_text"),
        },
        "cpython_long_mul": {
            "term_state": form_two.get("term_state"),
            "proved_against_own_body": proved,
            "verdict_ship": form_two.get("verdict_ship"),
            "verdict_text": form_two.get("verdict_text"),
        },
        "outcome": outcome,
        "cause": cause,
    }
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    print("wrote %s" % OUT, flush=True)
    print("outcome: %s" % outcome, flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
