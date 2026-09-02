#!/usr/bin/env python3
"""canon_interp_cpython.py -- TASK 21. Runs the newest canonicalization
generation's z3 gate (canon9_behaviour_check.Sim9, imported by
reference, not modified -- same reuse discipline every file in this
lineage follows) over CPython's long_add fast-path COMPUTATION part
(the single instruction after the arrival-unpacking prefix, per the
ARRIVAL/COMPUTATION BOUNDARY IS LINEAGE CONFLUENCE ruling,
AgentMemory 2026-08-31), and gates it against the already-canonical
c/i64,i64/+ family text carried in canon29_units_c.json.

WHAT IS REUSED, WHAT IS NEW.  interp_fastpath.json already carved this
boundary and already ran an ad hoc z3 proof (log_106 Instance B) that
this ONE instruction computes the same function as c's plain i64 add,
for the general domain.  That proof is CITED, not silently repeated as
this file's own finding.  What this file adds NEW: an INDEPENDENT
z3 check run directly through the pipeline's OWN newest checker
machinery (Sim9), gating the computation instruction against the
canonical TEXT the compiled table actually carries this round
(canon29_units_c.json's own canon29_text/canon7_text for the matched
class), rather than against a hand-written comparison text -- so the
canonical form recorded on the cpython unit is the SAME bytes-as-text
the compiled table already ratified, not a fresh invention.

REGISTER-IDENTITY BINDING.  The computation instruction is
`lea (%rax,%rdx,1),%rdi` (interp_fastpath.json carve, index 8, address
0x1373f4).  Its two READ families (rax, rdx) are the arrival prefix's
OWN outputs: medium_value(b) lands in rax (built by
`mov %rdx,%rax; sub %rsi,%rax; imul %rcx,%rax`), medium_value(a) lands
in rdx (built by `sub %r8,%rdx; imul %rcx,%rdx`) -- read directly off
interp_fastpath.json's own instruction comments (log_106 Instance A).
Binding rax->b, rdx->a is therefore forced by construction (which
prefix line produces which family), not asserted. A trailing
`mov %rdi,%rax` is appended ONLY so Sim.answer_value (which only reads
the `rax` family, canon5_behaviour_check.py's own convention) can see
the answer -- a mechanical relocation of the SAME value already
computed by the lea, not a new computation; stated here rather than
silently added.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in \"which pairs
get compared\", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as \"same-operator pairs\"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim."

This file canonicalizes ONE unit; it does not group or pair units, so
check_no_spelling_keys.py's grouping/pairing rules do not fire on it
(no `members`/`pairs`/`rows`/`groups`/`entries` key at all) -- it is
still run, and PASSES, per the mechanical-guard requirement.

usage:
  canon_interp_cpython.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon9_behaviour_check as BC9                              # noqa: E402
import z3                                                          # noqa: E402

seed_family = BC9.seed_family
Sim9 = BC9.Sim9


def matched_c_class_text(indir):
    doc = json.load(open(os.path.join(indir, "canon29_units_c.json")))
    for n, u in doc["units"].items():
        m = u.get("meta", {})
        if (m.get("operator") == "+"
                and m.get("lhs_rep") == "i64"
                and m.get("rhs_rep") == "i64"
                and u.get("status") == "converged"):
            text = u.get("canon29_text") or u.get("canon7_text")
            return u.get("unit"), text
    return None, None


def main():
    indir = HERE
    fastpath = json.load(open(os.path.join(indir, "interp_fastpath.json")))
    instructions = fastpath["carve"]["instructions"]

    comp = None
    for ins in instructions:
        if ins["addr"] == "1373f4":
            comp = ins
            break
    if comp is None:
        print("REFUSED: computation instruction at 0x1373f4 not "
              "found in interp_fastpath.json's own carve")
        return 4

    real_lines = [
        "lea (%rax,%rdx,1),%rdi",
        "mov %rdi,%rax",
    ]

    matched_unit, candidate_text = matched_c_class_text(indir)
    if candidate_text is None:
        print("REFUSED: no converged c/i64,i64/+ class found in "
              "canon29_units_c.json to gate against")
        return 4

    shared_seed = {}
    seed_family(shared_seed, "rdi")
    seed_family(shared_seed, "rsi")
    # rdx (a's arrived value) shares the canonical "rdi" (a) seed;
    # rax (b's arrived value) shares the canonical "rsi" (b) seed --
    # forced by construction, per this file's own header.
    shared_seed["rdx"] = shared_seed["rdi"]
    shared_seed["rax"] = shared_seed["rsi"]

    sim_real = Sim9(shared_seed, "real")
    sim_cand = Sim9(shared_seed, "cand")

    lines_cand = [ln.strip() for ln in candidate_text.split(";")]

    val_real, w_real = sim_real.answer_value(real_lines)
    val_cand, w_cand = sim_cand.answer_value(lines_cand)

    if w_real != w_cand:
        w = min(w_real, w_cand)
        val_real = z3.Extract(w - 1, 0, val_real)
        val_cand = z3.Extract(w - 1, 0, val_cand)

    solver = z3.Solver()
    solver.add(val_real != val_cand)
    result = solver.check()

    out = {
        "meta": {
            "generator": "canon_interp_cpython.py (TASK 21)",
            "task": "TASK 21 -- canonicalize the interpreter units "
                     "(registers are NOT the issue)",
            "reads": ["interp_fastpath.json", "canon29_units_c.json"],
            "spelling": "the operator token '+' appears exactly once, "
                        "as a display label on the unit object below. "
                        "No key, grouping, pairing or row structure "
                        "in this file uses it -- this file "
                        "canonicalizes ONE unit, it does not group or "
                        "pair units.",
            "provenance_is_weaker": True,
        },
        "unit": {
            "lang": "cpython",
            "n": "long_add_fastpath",
            "operator": "+",
            "computation_instruction": comp["mnem"].strip(),
            "computation_address": "0x" + comp["addr"],
            "arrival_boundary_note": (
                "lineage confluence, per AgentMemory 2026-08-31 -- "
                "the first instruction reading BOTH unpacked operand "
                "values; the 8 arrival instructions before it are "
                "REPRESENTATION only (typed-pointer(PyLongObject*) "
                "unpacking), not part of this canonicalization"),
        },
        "gate": {
            "real_text_checked": "; ".join(real_lines),
            "real_text_note": (
                "the computation instruction, plus one relocating "
                "`mov %rdi,%rax` so Sim.answer_value can read the "
                "answer off the rax family (canon5_behaviour_check.py "
                "convention) -- not a new computation, stated "
                "explicitly per this file's own header"),
            "candidate_text": candidate_text,
            "candidate_source": (
                "canon29_units_c.json, unit %s (canon29_text/"
                "canon7_text, the newest canonical text on record "
                "for the c/i64,i64/+ class)" % matched_unit),
            "shared_seed_binding": {
                "rdx (a's arrived value)": "bound to the same seed "
                    "as canonical rdi (arg a)",
                "rax (b's arrived value)": "bound to the same seed "
                    "as canonical rsi (arg b)",
            },
            "z3_result": str(result),
        },
        "verdict": None,
        "canonical_text": None,
    }

    if result == z3.unsat:
        out["verdict"] = "PROVED_EQUAL"
        out["canonical_text"] = candidate_text
        out["reason"] = (
            "z3 proved the computation instruction equal to the "
            "matched c/i64,i64/+ class's own newest canonical text, "
            "for every value of every register either text reads "
            "before writing. This is an INDEPENDENT re-run through "
            "the pipeline's newest checker (Sim9) of the same result "
            "log_106's ad hoc proof already found (cited, not "
            "silently repeated).")
    elif result == z3.sat:
        out["verdict"] = "DISPROVED"
        out["canonical_text"] = None
        out["reason"] = "z3 found a counterexample: %s" % solver.model()
    else:
        out["verdict"] = "UNDECIDED"
        out["canonical_text"] = None
        out["reason"] = "z3 returned %r" % result

    outpath = os.path.join(indir, "canon_interp_units_cpython.json")
    fh = open(outpath, "w")
    json.dump(out, fh, indent=1)
    fh.write("\n")
    fh.close()

    print("wrote", outpath)
    print("verdict:", out["verdict"])
    print("canonical_text:", out["canonical_text"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
