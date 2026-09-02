#!/usr/bin/env python3
"""canon20.py -- JOB 3 driver: THE PACKED FLOAT ARITHMETIC FAMILY.
condition_table6.py's shape classifier + canon20_arith.py's renderer +
canon20_behaviour_check.py's z3-FPA ground-truth gate, wired together
in canon16.py's own self-contained style (this family's own whole
expression is always exactly one `<ARITHOP>(P, Q)` call -- there is no
outer wrapper for gen7's tree-walking machinery to add, so this driver
never routes through it, exactly like canon16.py's own float-negate
driver).

TARGET SET: every not-yet-converged, straight-line unit whose own
`normal_path_raw` is CLASSIFIED by condition_table6.classify_arith
(the `direct`/`conv`/`const` grammar; see that file's own header for
the population survey and for what is explicitly OUT of this file's
own scope -- the `ins@0(...)`-top "wrong subtree selected" defect, and
the u64/i64-via-magic-constant conversion idiom). A unit whose text
does not classify is never opened at all, so this driver cannot
regress anything else in the corpus, structurally, the same guarantee
every driver in this lineage states.

BASELINE: canon19_units_<lang>.json (JOB 1's own output, the newest
generation on disk before this file).

GATE: canon20_behaviour_check.anchored_check -- z3 FLOATING POINT
THEORY (fpAdd/fpSub/fpMul/fpDiv/fpSignedToFP/fpFPToFP), bit-level
comparison via fpToIEEEBV, a per-unit solver timeout with timeouts
counted as UNDECIDED (never a refusal, never a silent pass) -- see
that file's own header.

usage:
  canon20.py [--in DIR] [--out DIR]
"""

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import condition_table6 as CT6                                  # noqa: E402
import canon20_arith as A20                                     # noqa: E402
import canon20_behaviour_check as BC20                           # noqa: E402
import canon9 as C9                                              # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]

load_tree_units2 = C9.load_tree_units2

OLD_TEXT_FIELDS = [
    "canon19_text", "canon18_text", "canon17_text", "canon16_text",
    "canon15_text", "canon14_text", "canon13_text", "canon12_text",
    "canon11_text", "canon10_text", "canon9_text", "canon8_text",
    "canon7_text",
]


def old_text_of(old_rec):
    for f in OLD_TEXT_FIELDS:
        v = old_rec.get(f)
        if v is not None:
            return v
    return None


def convert_one(lang, n, canon4_rec, old_rec, tu2_map):
    if old_rec.get("branch_kind") != "straight_line":
        return None
    tu2 = tu2_map.get((lang, n))
    if tu2 is None:
        return None
    raw = tu2.get("normal_path_raw")
    if tu2.get("sem_ok") is False or raw is None:
        return None
    if not any(op + "(" in raw for op in CT6.ARITH_OPS):
        return None

    classified = CT6.classify_arith(raw)
    if classified is None:
        return None
    op_kind, precision, p_operand, q_operand = classified

    meta = old_rec.get("meta") or {}
    a_is_vector = meta.get("lhs_rep") in ("f32", "f64")
    operator = old_rec.get("operator") or tu2.get("operator")

    try:
        lines = A20.render_arith(op_kind, precision, p_operand,
                                  q_operand, operator, a_is_vector)
    except A20.Unsupported as exc:
        return {
            "job3_arith_candidate_text": None,
            "job3_arith_refusal_reason": str(exc),
        }

    candidate = "; ".join(lines)
    # NOTE, deliberately NOT the "candidate == old_text: skip" dedup
    # every other driver in this lineage uses: THIS unit's own stored
    # canon7_text/.../canon19_text is not a prior GATED attempt at
    # this exact synthesis (no earlier generation could render XMM
    # float-arithmetic instructions at all before this file) -- for
    # a unit whose renderer output happens to already equal real
    # ship code's own mnem verbatim (measured: common in this
    # bucket), that stored text is canon4's own REAL SHIP mnem
    # itself, carried forward as a not-yet-converged unit's
    # placeholder, NEVER a verdict. Skipping on text equality here
    # would silently refuse to gate-prove units this renderer gets
    # exactly right -- so every classified unit is gated, always.

    real_mnem = canon4_rec.get("mnem")
    if not real_mnem:
        return {
            "job3_arith_candidate_text": candidate,
            "job3_arith_refusal_reason":
                "no real ship mnem recorded for this unit",
        }
    real_text = "; ".join(real_mnem)

    resolved_const_bits = None
    for operand in (p_operand, q_operand):
        if operand[0] == "const":
            sign = A20.CONST_SIGN.get(operator)
            if sign is not None:
                resolved_const_bits = A20.float_bits(
                    sign * 1.0, precision)

    verdict, detail = BC20.anchored_check(
        real_text, candidate, precision, resolved_const_bits)

    update = {
        "job3_arith_shape": "%s(%r,%r)" % (op_kind, p_operand,
                                            q_operand),
        "job3_arith_candidate_text": candidate,
        "job3_arith_ground_truth_verdict": verdict,
        "job3_arith_ground_truth_detail": detail,
    }
    if verdict == "PROVED_EQUAL":
        update["canon20_text"] = candidate
        update["status"] = "converged"
        update["converged"] = True
        update["reason"] = "JOB 3 (condition_table6.py's packed " \
            "float arithmetic grammar, canon20_arith.py's " \
            "rendering, canon20_behaviour_check.py's z3-FPA gate): " \
            "candidate proved bit-level equal to the unit's own " \
            "real ship code directly"
        return update

    update["job3_arith_decision"] = "KEEP_OLD -- %s: %s" % (
        verdict, detail[:200])
    return update


def run_language(lang, indir, outdir, canon4_docs, tu2_map):
    canon19_path = os.path.join(indir, "canon19_units_%s.json" % lang)
    doc = json.load(open(canon19_path))
    units = doc["units"]
    canon4_units = canon4_docs[lang]

    attempted = 0
    accepted = 0
    disproved = 0
    undecided = 0
    no_candidate = 0
    skipped_not_our_shape = 0

    for n, u in units.items():
        if u.get("status") != "not_yet_converged":
            continue
        update = convert_one(lang, n, canon4_units.get(n, {}), u,
                              tu2_map)
        if update is None:
            skipped_not_our_shape = skipped_not_our_shape + 1
            continue
        u.update(update)
        if update.get("job3_arith_candidate_text") is None:
            no_candidate = no_candidate + 1
            continue
        attempted = attempted + 1
        if update.get("status") == "converged":
            accepted = accepted + 1
        elif update.get("job3_arith_ground_truth_verdict") == \
                "DISPROVED":
            disproved = disproved + 1
        else:
            undecided = undecided + 1

    doc["job3_arith_tally"] = {
        "candidates_attempted": attempted,
        "accepted": accepted,
        "disproved": disproved,
        "undecided": undecided,
        "no_candidate_at_all": no_candidate,
    }
    doc["meta"] = dict(doc["meta"])
    doc["meta"]["generator"] = "canon20.py (JOB 3: the packed float " \
        "arithmetic family, z3 FPA) over canon19_units_%s.json" \
        % lang
    doc["meta"]["generated_at"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    name = os.path.join(outdir, "canon20_units_%s.json" % lang)
    fh = open(name, "w")
    json.dump(doc, fh, indent=1)
    fh.close()
    print("wrote %s (%d attempted, %d accepted, %d disproved, %d "
          "undecided, %d no candidate, %d not our shape)"
          % (name, attempted, accepted, disproved, undecided,
             no_candidate, skipped_not_our_shape))
    return doc


def main(argv):
    indir = HERE
    outdir = HERE
    i = 1
    while i < len(argv):
        if argv[i] == "--in":
            indir = argv[i + 1]
            i = i + 2
            continue
        if argv[i] == "--out":
            outdir = argv[i + 1]
            i = i + 2
            continue
        print(__doc__)
        return 2

    started = time.time()
    print("canon20.py -- JOB 3: the packed float arithmetic family "
          "(z3 FPA)")

    canon4_docs = {}
    for lang in LANGS:
        canon4_docs[lang] = json.load(open(
            os.path.join(indir, "canon4_units_%s.json" % lang)
        ))["units"]

    tu2_map = load_tree_units2()

    totals = {"candidates_attempted": 0, "accepted": 0,
              "disproved": 0, "undecided": 0,
              "no_candidate_at_all": 0}
    for lang in LANGS:
        doc = run_language(lang, indir, outdir, canon4_docs, tu2_map)
        for k in totals:
            totals[k] += doc["job3_arith_tally"][k]

    print("TOTAL: %r" % totals)
    print("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
