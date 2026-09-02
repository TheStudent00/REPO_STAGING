#!/usr/bin/env python3
"""canon22.py -- driver: THE INT-TO-FLOAT-CONVERSION EXTENSION OF THE
UCOMISD/UCOMISS FLAGS FAMILY. condition_table4.py's UNCHANGED
substitution (already operand-shape-agnostic, see condition_table8.py's
own header) + condition_table8.py's conversion-aware operand
classifier + canon22_float.py's z3 model + canon22_render.py's
XMM+conversion rendering + canon22_behaviour_check.py's real-z3-FPA
ground-truth gate, wired together exactly the way canon21.py wires its
own generation's pieces together -- this file IS canon17.py's own
follow-on, targeting the population condition_table4.py's own header
named and left out ("THIS FILE DOES NOT MODEL... int-to-float
conversion atom").

TARGET SET: every not-yet-converged, straight-line (0-branch) unit
whose own `normal_path_raw` contains at least one `CmpF64(` call AND
for which condition_table4.substitute_float_packed applies at least
one substitution -- IDENTICAL target set to canon17.py's own (the
substitution step never changed), so this driver reopens EVERY unit
canon17.py's own (unextended) driver already looked at, including ones
it already converged (harmless -- see `convert_one` below, which
refuses to touch an already-converged record) and the 130 units this
lap's own survey found refused purely on operand classification (see
condition_table8.py's own header for the exhaustive shape survey).

BASELINE: canon21_units_<lang>.json (the newest generation on disk
before this lap).

GATE: canon22_behaviour_check.anchored_check -- real z3 FPA, proves
each candidate directly against the unit's own real ship code.

usage:
  canon22.py [--in DIR] [--out DIR]
"""

import json
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import condition_table4 as CT4                                  # noqa: E402
import canon22_float as CF22                                     # noqa: E402
import canon22_render as R22                                     # noqa: E402
import canon22_behaviour_check as BC22                           # noqa: E402
import canon9 as C9                                              # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]

load_tree_units2 = C9.load_tree_units2

OLD_TEXT_FIELDS = [
    "canon21_text", "canon20_text", "canon19_text", "canon18_text",
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


def build_fixed_unit(tu2_unit):
    """condition_table4's UNCHANGED substitution + canon22_float's
    conversion-aware normalization over ONE unit's own raw text --
    (fixed_unit, applied, sub_note, norm_note). fixed_unit is None if
    there is nothing to substitute -- identical skip logic to
    canon17.build_fixed_unit (this file never widens the substitution
    step, only the operand classifier downstream of it)."""
    raw = tu2_unit.get("normal_path_raw")
    if tu2_unit.get("sem_ok") is False or raw is None:
        return None, 0, "n/a", "n/a"
    if "CmpF64(" not in raw:
        return None, 0, "no CmpF64 call in this unit's raw text", "n/a"
    new_raw, applied, sub_note = CT4.substitute_float_packed(raw)
    if applied == 0:
        return None, 0, sub_note, "n/a"
    new_root, ok, norm_note = CF22.normalize_v2e(new_raw)
    fixed = dict(tu2_unit)
    fixed["normal_path_raw"] = new_raw
    fixed["normal_path_root"] = new_root
    fixed["normalize_ok"] = ok
    fixed["normalize_note"] = norm_note
    return fixed, applied, sub_note, norm_note


def convert_one(lang, n, canon4_rec, old_rec, tu2_map, canon4_docs,
                 sem_map, workdir):
    if old_rec.get("branch_kind") != "straight_line":
        return None
    tu2 = tu2_map.get((lang, n))
    if tu2 is None:
        return None

    fixed_unit, cond_applied, cond_note, norm_note = \
        build_fixed_unit(tu2)
    if fixed_unit is None:
        return None

    old_text = old_text_of(old_rec)

    meta = old_rec.get("meta") or {}
    a_is_vector = meta.get("lhs_rep") in ("f32", "f64")
    R22.set_render_context(a_is_vector)

    result, ctxd = R22.render_unit22(fixed_unit, workdir)
    if not isinstance(result, list):
        return {
            "job1_convfcond_condition_substitutions": cond_applied,
            "job1_convfcond_substitution_note": cond_note,
            "job1_convfcond_normalize_note": norm_note,
            "job1_convfcond_candidate_text": None,
            "job1_convfcond_refusal_reason": result,
        }

    candidate = "; ".join(result)
    if candidate == old_text:
        return None

    verdict, detail = BC22.anchored_check(
        lang, n, canon4_docs, sem_map, candidate, a_is_vector)

    update = {
        "job1_convfcond_condition_substitutions": cond_applied,
        "job1_convfcond_substitution_note": cond_note,
        "job1_convfcond_normalize_note": norm_note,
        "job1_convfcond_candidate_text": candidate,
        "job1_convfcond_ground_truth_verdict": verdict,
        "job1_convfcond_ground_truth_detail": detail,
    }
    if verdict == "PROVED_EQUAL":
        update["canon22_text"] = candidate
        update["status"] = "converged"
        update["converged"] = True
        update["reason"] = "canon22.py (condition_table8.py's " \
            "conversion-extended ucomisd/ucomiss flags model, " \
            "canon22_render.py's XMM+conversion rendering, real z3 " \
            "FPA ground-truth gate): candidate proved equal to the " \
            "unit's own real ship code directly"
        return update

    update["job1_convfcond_decision"] = "KEEP_OLD -- %s: %s" % (
        verdict, detail[:200])
    return update


def run_language(lang, indir, outdir, canon4_docs, sem_map, tu2_map,
                  workdir):
    canon21_path = os.path.join(indir, "canon21_units_%s.json" % lang)
    doc = json.load(open(canon21_path))
    units = doc["units"]
    canon4_units = canon4_docs[lang]

    attempted = 0
    accepted = 0
    still_refused = 0
    no_candidate = 0
    skipped_not_our_shape = 0

    # ZERO-REGRESSIONS BY CONSTRUCTION: identical discipline to
    # canon21.py's own loop -- only a `not_yet_converged` record is
    # ever opened, so an already-converged unit's newest-generation
    # text cannot change here.
    for n, u in units.items():
        if u.get("status") != "not_yet_converged":
            continue
        update = convert_one(lang, n, canon4_units.get(n, {}), u,
                              tu2_map, canon4_docs, sem_map, workdir)
        if update is None:
            skipped_not_our_shape = skipped_not_our_shape + 1
            continue
        u.update(update)
        if update.get("job1_convfcond_candidate_text") is None and \
                "job1_convfcond_refusal_reason" in update:
            no_candidate = no_candidate + 1
            continue
        attempted = attempted + 1
        if update.get("status") == "converged":
            accepted = accepted + 1
        else:
            still_refused = still_refused + 1

    doc["job1_convfcond_tally"] = {
        "candidates_attempted": attempted,
        "accepted": accepted,
        "still_refused_after_attempt": still_refused,
        "no_candidate_at_all": no_candidate,
    }
    doc["meta"] = dict(doc["meta"])
    doc["meta"]["generator"] = "canon22.py (int-to-float conversion " \
        "extension of the ucomisd/ucomiss flags family) over " \
        "canon21_units_%s.json" % lang
    doc["meta"]["generated_at"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    name = os.path.join(outdir, "canon22_units_%s.json" % lang)
    fh = open(name, "w")
    json.dump(doc, fh, indent=1)
    fh.close()
    print("wrote %s (%d attempted, %d accepted, %d still refused, "
          "%d no candidate, %d not our shape)"
          % (name, attempted, accepted, still_refused, no_candidate,
             skipped_not_our_shape))
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
    print("canon22.py -- int-to-float conversion extension of the "
          "ucomisd/ucomiss flags family")

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

    workdir = tempfile.mkdtemp(prefix="canon22_asm_")

    totals = {"candidates_attempted": 0, "accepted": 0,
              "still_refused_after_attempt": 0,
              "no_candidate_at_all": 0}
    for lang in LANGS:
        doc = run_language(lang, indir, outdir, canon4_docs, sem_map,
                            tu2_map, workdir)
        for k in totals:
            totals[k] += doc["job1_convfcond_tally"][k]

    print("TOTAL: %r" % totals)
    print("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
