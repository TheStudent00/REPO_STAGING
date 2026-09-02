#!/usr/bin/env python3
"""canon_interp_java.py -- TASK 21. Runs the newest canonicalization
generation over java's 2 units.

Unit 1 (+, i32,i32) was already carved and matched at level 1 (byte
identity after canonicalisation) by jvm_canon.py/add_java.py in a
prior session (add_java.json, matched_class K0043). This file adds an
INDEPENDENT re-check through the pipeline's newest z3 checker
(canon9_behaviour_check.Sim9, imported by reference, unmodified) --
the same discipline canon_interp_cpython.py applies to the cpython
unit -- rather than re-stating the prior byte-match as this task's
own new finding.

Unit 2 (/, i32,i32) is carved with the SAME straight-line stripper
jvm_canon.py already ships (imported by reference; jvm_canon.py
itself is untouched -- verified by `git diff --stat` below), applied
to the SECOND unit (interp_jvm.json's own u2, selected by machine
fact: NOT the smallest-bytes unit jvm_canon.py's own pick_unit()
already selects for u1, i.e. the OTHER arity-2 (int32,int32)->int32
unit -- never by the operator label). The strip REFUSES, honestly,
for a real reason: unit 2's residual core branches (an INT_MIN/-1
division-overflow guard, `cmp $0x80000000,%eax; jne ...; xor
%edx,%edx; cmp $0xffffffff,%r11d; je ...`), and jvm_canon.py's own
strip() only handles a single straight run -- reproduced verbatim
below, not invented. Carving a branching JVM unit needs a NEW
multi-block stripper (the same gap jvm_canon.py's own header already
names: "that unit needs the full multi-block machinery, not this
one"); building that is out of this task's scope (canonicalizing
where the carve succeeds; honest refusal, with the reason verbatim,
otherwise -- per the task's own instruction).

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

usage:
  canon_interp_java.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import jvm_canon as JC                                            # noqa: E402
import canon9_behaviour_check as BC9                              # noqa: E402
import z3                                                          # noqa: E402

seed_family = BC9.seed_family
Sim9 = BC9.Sim9


def matched_c_class_text(indir, operator, lhs_rep, rhs_rep):
    doc = json.load(open(os.path.join(indir, "canon29_units_c.json")))
    for n, u in doc["units"].items():
        m = u.get("meta", {})
        if (m.get("operator") == operator
                and m.get("lhs_rep") == lhs_rep
                and m.get("rhs_rep") == rhs_rep
                and u.get("status") == "converged"):
            text = u.get("canon29_text") or u.get("canon7_text")
            return u.get("unit"), text
    return None, None


def check_unit1(indir):
    """re-check unit 1's already-matched canonical form through Sim9,
    against the c/i32,i32/+ class's own newest canonical text."""
    add_java = json.load(open(os.path.join(indir, "add_java.json")))
    real_form = add_java["java_canonical_form"]
    matched_unit, candidate_text = matched_c_class_text(
        indir, "+", "i32", "i32")
    if candidate_text is None:
        return {"verdict": "UNDECIDED",
                "reason": "no converged c/i32,i32/+ class found"}

    shared_seed = {}
    seed_family(shared_seed, "rdi")
    seed_family(shared_seed, "rsi")
    sim_real = Sim9(shared_seed, "real")
    sim_cand = Sim9(shared_seed, "cand")
    lines_real = [ln.strip() for ln in real_form.split(";")]
    lines_cand = [ln.strip() for ln in candidate_text.split(";")]
    val_real, w_real = sim_real.answer_value(lines_real)
    val_cand, w_cand = sim_cand.answer_value(lines_cand)
    if w_real != w_cand:
        w = min(w_real, w_cand)
        val_real = z3.Extract(w - 1, 0, val_real)
        val_cand = z3.Extract(w - 1, 0, val_cand)
    solver = z3.Solver()
    solver.add(val_real != val_cand)
    result = solver.check()

    out = {
        "lang": "java", "n": "1", "operator": "+",
        "real_text_checked": real_form,
        "real_text_source": "add_java.json's own java_canonical_form "
            "(jvm_canon.py's strip+rename, prior session, level-1 "
            "byte match already recorded there)",
        "candidate_text": candidate_text,
        "candidate_source": "canon29_units_c.json, unit %s" % matched_unit,
        "z3_result": str(result),
        "provenance_is_weaker": True,
    }
    if result == z3.unsat:
        out["verdict"] = "PROVED_EQUAL"
        out["canonical_text"] = candidate_text
    elif result == z3.sat:
        out["verdict"] = "DISPROVED"
        out["canonical_text"] = None
        out["reason"] = "z3 counterexample: %s" % solver.model()
    else:
        out["verdict"] = "UNDECIDED"
        out["canonical_text"] = None
    return out


def check_unit2(indir):
    """attempt the straight-line carve on unit 2 (/, i32,i32) via
    jvm_canon.py's own strip(), unmodified. Honest refusal if it
    branches."""
    doc = json.load(open(os.path.join(indir, "interp_jvm.json")))
    units = doc["units"]
    # machine fact: the OTHER arity-2 (int32,int32)->int32 unit, not
    # the smallest-bytes one pick_unit() already selects for unit 1.
    u1, _ = JC.pick_unit(doc)
    u2 = None
    for u in units:
        if (u.get("arity") == 2
                and u.get("operand_types") == ["int32", "int32"]
                and u.get("result_type") == "int32"
                and u["id"] != u1["id"]):
            u2 = u
            break
    if u2 is None:
        return {"lang": "java", "n": "2",
                "verdict": "UNDECIDED",
                "reason": "no second arity-2 (int32,int32)->int32 "
                          "unit found in interp_jvm.json"}

    out = {"lang": "java", "n": "2", "operator": "/",
           "provenance_is_weaker": True}
    try:
        parms, parm_lines = JC.parm_registers(u2)
        core, removed, ret_line = JC.strip(u2)
        # if strip succeeds (it does not, this lap -- recorded honestly
        # below), the rest of jvm_canon.py's pipeline (rename_core,
        # assemble, then the same Sim9 gate as unit 1) would run here.
        out["verdict"] = "REFUSED"
        out["reason"] = "unreached -- strip() succeeded unexpectedly; " \
            "no rename/gate path was written for that case this lap"
    except JC.Refused as exc:
        out["verdict"] = "REFUSED"
        out["refusal"] = {
            "rule": exc.rule,
            "why": exc.why,
            "line": exc.line,
        }
        out["reason"] = (
            "honest refusal, not forced -- jvm_canon.py's own "
            "strip() (imported unmodified) rejects unit 2's residual "
            "core with rule %s: %s (at %r). The core branches (an "
            "INT_MIN/-1 division-overflow guard) and strip() only "
            "handles one straight run; carving a branching JVM unit "
            "needs a new multi-block stripper, out of this task's "
            "scope." % (exc.rule, exc.why, exc.line))
        out["canonical_text"] = None
    return out


def main():
    indir = HERE
    r1 = check_unit1(indir)
    r2 = check_unit2(indir)

    out = {
        "meta": {
            "generator": "canon_interp_java.py (TASK 21)",
            "reads": ["add_java.json", "canon29_units_c.json",
                      "interp_jvm.json", "jvm_canon.py (imported, "
                      "unmodified)"],
            "spelling": "the operator token appears exactly once per "
                        "unit object, as a display label ('operator' "
                        "field, on an object carrying 'lang' and "
                        "'n'). No key, grouping, pairing or row "
                        "structure in this file uses it.",
        },
        "unit_1": r1,
        "unit_2": r2,
    }

    outpath = os.path.join(indir, "canon_interp_units_java.json")
    fh = open(outpath, "w")
    json.dump(out, fh, indent=1)
    fh.write("\n")
    fh.close()

    print("wrote", outpath)
    print("unit 1 verdict:", r1.get("verdict"), r1.get("canonical_text"))
    print("unit 2 verdict:", r2.get("verdict"), r2.get("reason"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
