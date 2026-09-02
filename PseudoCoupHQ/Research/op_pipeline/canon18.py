#!/usr/bin/env python3
"""canon18.py -- JOB 2 driver: THE SIGNED-ZERO-EXTENSION SIGN-TEST FIX
(canon12_normalize.py's own new `_signed_operand`/`SIGNED_COND_OPS`,
this lap's fix).

job2_remaining_refusals_report.txt's own PART B named the cause
exactly, on swift's 8 remaining Int32-vs-UInt64 units (op_296 etc):
the rendered sign test for a 32-bit signed operand was `0 >s
zero_extend_64(a)` -- STRUCTURALLY unable to ever be true, because a
zero-extended 64-bit value's own bit 63 is always 0, regardless of the
original 32-bit value's own sign. Root cause, confirmed by direct
trace of the raw VEX text (tree_units2.json's own normal_path_raw):
VEX's `amd64g_calculate_condition` always stores cc_dep1/cc_dep2
ZERO-extended to 64 bits (`zx64(...)`) in the guest state, regardless
of the REAL operation width; canon12_normalize.py's own COND_OPS
rewrite (the ONLY place that turns a synthetic CondXX(dep1,dep2) node
into a z3 predicate) used dep1/dep2 as-parsed (64-bit, post zero-
extension) for EVERY condition, including the six SIGNED ones
(CondSLT/CondSGE/CondSLE/CondSGT/CondSGN/CondNSGN) -- exactly the ones
whose predicate depends on the operand's OWN sign bit, so exactly the
ones a zero-extension silently breaks. THE FIX (canon12_normalize.py,
`_signed_operand`): for those six ops only, an operand that is
STRUCTURALLY a zero-extension node (`zx<W>(inner)`) is re-derived
SIGN-extended instead, reading inner's own sign bit at its own true
width -- a pure ADDITION gated on a structural AST shape, changing
nothing for any operand that is not itself a zx-wrapper (the shape
every already-converged unit's own condition rewrite already has).

THIS DRIVER re-attempts EVERY not_yet_converged straight-line unit
(not a pre-filtered bucket -- the fix lives inside the shared z3
condition model, so the honest thing is to let the fixed normalizer
see everything still open and let the gate decide, exactly canon14.py's
own stated reasoning for the same shape of fix) against
canon17_units_<lang>.json's own baseline (JOB 1/2/3's own newest prior
generation). Uses condition_table3's value-based-first pairing
(already the best pairing this lineage has -- unchanged) and
canon14_render's renderer (unchanged) -- ONLY canon12_normalize.py's
semantics changed this lap.

GATE: canon12_behaviour_check.wide_anchored_check, unchanged -- the
same superset gate every generation since canon13 uses: every
candidate is proved against the unit's OWN real ship mnemonic text,
never a prior rendering.

BASELINE: canon17_units_<lang>.json. A unit not re-attempted, or
re-attempted but not accepted, is copied through BYTE-IDENTICAL --
zero regression by construction (this driver only ever WRITES a new
canon18_text field when the gate itself returns PROVED_EQUAL on a
candidate that differs from the prior text; verified separately by
this lap's own report, a programmatic diff of every already-converged
unit's newest text before/after).

THE SPELLING BAN: this driver groups nothing by operator token -- it
iterates every not_yet_converged unit by (lang, n) and asks the SAME
gate the same question for each, one unit at a time; the class table
(dominant_table.py) is the only place units are ever grouped, and it
groups by machine-form evidence, never by this driver's own pass.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements -- every splittable statement is split across lines.

usage:
  canon18.py [--in DIR] [--out DIR]
"""

import json
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import condition_table3 as CT3                                  # noqa: E402
import canon14_render as R14                                    # noqa: E402
import canon12_normalize as C12N                                 # noqa: E402
import canon12_behaviour_check as BC10                           # noqa: E402
import canon9 as C9                                              # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]

job2b_anchored_check = BC10.wide_anchored_check
load_tree_units2 = C9.load_tree_units2

OLD_TEXT_FIELDS = [
    "canon17_text", "canon16_text", "canon15_text", "canon14_text",
    "canon13_text", "canon12_text", "canon11_text", "canon10_text",
    "canon9_text", "canon8_text", "canon7_text",
]


def old_text_of(old_rec):
    for f in OLD_TEXT_FIELDS:
        v = old_rec.get(f)
        if v is not None:
            return v
    return None


def apply_wide_v4(tu2_unit, canon4_lines):
    """canon15.apply_wide_v3, pointed at the SAME condition_table3
    pairing (unchanged) but canon12_normalize's now-fixed cond model
    (see file header)."""
    out = dict(tu2_unit)
    raw = tu2_unit.get("normal_path_raw")
    if tu2_unit.get("sem_ok") is False or raw is None:
        return out, 0, "n/a"
    if "amd64g_calculate_condition" in raw:
        raw, applied, sub_note = CT3.resolve_conditions3(
            raw, canon4_lines)
    else:
        applied, sub_note = 0, "no amd64g_calculate_condition call"
    norm, ok, note = C12N.normalize_v2(raw)
    out["normal_path_raw"] = raw
    out["normal_path_root"] = norm
    out["normalize_ok"] = ok
    out["normalize_note"] = note
    return out, applied, sub_note


def convert_one(lang, n, canon4_rec, old_rec, tu2_map, canon4_docs,
                 sem_map, workdir):
    if old_rec.get("branch_kind") != "straight_line":
        return None
    tu2 = tu2_map.get((lang, n))
    if tu2 is None:
        return None

    canon4_lines = canon4_rec.get("derived_text")
    fixed_unit, cond_applied, cond_note = apply_wide_v4(
        tu2, canon4_lines)

    old_text = old_text_of(old_rec)

    result, context_record = R14.render_unit14(fixed_unit, workdir)
    if not isinstance(result, list):
        return {
            "job2b_signfix_candidate_text": None,
            "job2b_signfix_refusal_reason": result,
        }

    candidate = "; ".join(result)
    if candidate == old_text:
        return None

    verdict, detail = job2b_anchored_check(
        lang, n, canon4_docs, sem_map, candidate)

    update = {
        "job2b_signfix_condition_substitutions": cond_applied,
        "job2b_signfix_note": cond_note,
        "job2b_signfix_candidate_text": candidate,
        "job2b_signfix_ground_truth_verdict": verdict,
        "job2b_signfix_ground_truth_detail": detail,
    }
    if verdict == "PROVED_EQUAL":
        update["canon18_text"] = candidate
        update["status"] = "converged"
        update["converged"] = True
        update["reason"] = "JOB 2 (canon12_normalize.py's " \
            "_signed_operand fix -- signed conditions read a zero-" \
            "extended operand's OWN sign bit at its true width " \
            "instead of the always-0 top bit of the storage width): " \
            "candidate proved equal to the unit's own real ship " \
            "code directly"
        return update

    update["job2b_signfix_decision"] = "KEEP_OLD -- %s: %s" % (
        verdict, detail[:200])
    return update


def run_language(lang, indir, outdir, canon4_docs, sem_map, tu2_map,
                  workdir):
    canon17_path = os.path.join(indir, "canon17_units_%s.json" % lang)
    doc = json.load(open(canon17_path))
    units = doc["units"]
    canon4_units = canon4_docs[lang]

    attempted = 0
    accepted = 0
    still_refused = 0
    no_candidate = 0
    not_applicable = 0

    for n, u in units.items():
        if u.get("status") != "not_yet_converged":
            continue
        update = convert_one(lang, n, canon4_units.get(n, {}), u,
                              tu2_map, canon4_docs, sem_map, workdir)
        if update is None:
            not_applicable = not_applicable + 1
            continue
        u.update(update)
        if update.get("job2b_signfix_candidate_text") is None and \
                "job2b_signfix_refusal_reason" in update:
            no_candidate = no_candidate + 1
            continue
        attempted = attempted + 1
        if update.get("status") == "converged":
            accepted = accepted + 1
        else:
            still_refused = still_refused + 1

    doc["job2b_signfix_tally"] = {
        "candidates_attempted": attempted,
        "accepted": accepted,
        "still_refused_after_attempt": still_refused,
        "no_candidate_at_all": no_candidate,
        "not_applicable_this_pass": not_applicable,
    }
    doc["meta"] = dict(doc["meta"])
    doc["meta"]["generator"] = "canon18.py (JOB 2: the signed-zero-" \
        "extension sign-test fix) over canon17_units_%s.json" % lang
    doc["meta"]["generated_at"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    name = os.path.join(outdir, "canon18_units_%s.json" % lang)
    fh = open(name, "w")
    json.dump(doc, fh, indent=1)
    fh.close()
    print("wrote %s (%d attempted, %d accepted, %d still refused, "
          "%d no candidate, %d not applicable)"
          % (name, attempted, accepted, still_refused, no_candidate,
             not_applicable))
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
    print("canon18.py -- JOB 2: the signed-zero-extension sign-test "
          "fix")

    canon4_docs = {}
    for lang in LANGS:
        canon4_docs[lang] = json.load(open(
            os.path.join(indir, "canon4_units_%s.json" % lang)
        ))["units"]

    sem_map = {}
    for lang in LANGS:
        path = os.path.join(indir, "sem_anchored_spill_%s.json" % lang)
        sem_map[lang] = json.load(open(path))["units"]

    tu2_map = load_tree_units2()

    workdir = tempfile.mkdtemp(prefix="canon18_asm_")

    totals = {"candidates_attempted": 0, "accepted": 0,
              "still_refused_after_attempt": 0,
              "no_candidate_at_all": 0,
              "not_applicable_this_pass": 0}
    for lang in LANGS:
        doc = run_language(lang, indir, outdir, canon4_docs, sem_map,
                            tu2_map, workdir)
        for k in totals:
            totals[k] += doc["job2b_signfix_tally"][k]

    print("TOTAL: %r" % totals)
    print("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
