#!/usr/bin/env python3
"""canon19.py -- JOB 1 driver: THE PACKED-MASK FLOAT COMPARE FAMILY
(cmpeqsd/cmpneqsd/cmpeqss/cmpneqss), condition_table5.py's
substitution + canon19_float.py's z3 model + canon19_render.py's XMM
rendering + canon19_behaviour_check.py's ground-truth-anchored gate,
wired together exactly the way canon17.py wires its own generation's
pieces together.

TARGET SET: every not-yet-converged, straight-line (0-branch) unit
whose own `normal_path_raw` contains at least one `CmpEQ64F0x2(` or
`CmpEQ32F0x4(` call AND for which condition_table5.substitute_packed_
mask actually applies at least one substitution (a unit whose packed
compare is wrapped in a shape outside condition_table5.py's own
grammar -- an int-to-float conversion operand, a compile-time-
materialized float constant, or the SEPARATE "final extraction step
missing from normal_path_raw" defect this lap's own survey found and
named, NOT this file's own scope -- stays untouched, `applied` is 0,
and this driver correctly skips it). Never widened beyond that: a unit
whose text does not match condition_table5's own grammar is never
opened at all, so this driver cannot regress anything else in the
corpus, structurally, the same guarantee canon14/15/16/17/18.py's own
drivers state.

BASELINE: canon18_units_<lang>.json (JOB 2's own output, the newest
generation on disk before this file).

GATE: canon19_behaviour_check.anchored_check -- proves each candidate
directly against the unit's own real ship code (canon4_units's own
`mnem`), the SAME re-anchored-to-ground-truth discipline every
generation in this lineage already uses.

usage:
  canon19.py [--in DIR] [--out DIR]
"""

import json
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import condition_table5 as CT5                                  # noqa: E402
import canon19_float as CF19                                     # noqa: E402
import canon19_render as R19                                     # noqa: E402
import canon19_behaviour_check as BC19                           # noqa: E402
import canon9 as C9                                              # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]

load_tree_units2 = C9.load_tree_units2

OLD_TEXT_FIELDS = [
    "canon18_text", "canon17_text", "canon16_text", "canon15_text",
    "canon14_text", "canon13_text", "canon12_text", "canon11_text",
    "canon10_text", "canon9_text", "canon8_text", "canon7_text",
]


def old_text_of(old_rec):
    for f in OLD_TEXT_FIELDS:
        v = old_rec.get(f)
        if v is not None:
            return v
    return None


def build_fixed_unit(tu2_unit):
    """apply condition_table5's substitution + canon19_float's
    normalization to ONE unit's own raw text -- (fixed_unit, applied,
    sub_note, norm_note). fixed_unit is None if there is nothing to
    substitute (see file header)."""
    raw = tu2_unit.get("normal_path_raw")
    if tu2_unit.get("sem_ok") is False or raw is None:
        return None, 0, "n/a", "n/a"
    if "CmpEQ64F0x2(" not in raw and "CmpEQ32F0x4(" not in raw:
        return None, 0, "no packed-mask compare call in this unit's " \
            "raw text", "n/a"
    new_raw, applied, sub_note = CT5.substitute_packed_mask(raw)
    if applied == 0:
        return None, 0, sub_note, "n/a"
    new_root, ok, norm_note = CF19.normalize_v2c(new_raw)
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
    R19.set_render_context(a_is_vector)

    result, ctxd = R19.render_unit19(fixed_unit, workdir)
    if not isinstance(result, list):
        return {
            "job1_packmask_condition_substitutions": cond_applied,
            "job1_packmask_substitution_note": cond_note,
            "job1_packmask_normalize_note": norm_note,
            "job1_packmask_candidate_text": None,
            "job1_packmask_refusal_reason": result,
        }

    candidate = "; ".join(result)
    if candidate == old_text:
        return None

    verdict, detail = BC19.anchored_check(
        lang, n, canon4_docs, sem_map, candidate, a_is_vector)

    update = {
        "job1_packmask_condition_substitutions": cond_applied,
        "job1_packmask_substitution_note": cond_note,
        "job1_packmask_normalize_note": norm_note,
        "job1_packmask_candidate_text": candidate,
        "job1_packmask_ground_truth_verdict": verdict,
        "job1_packmask_ground_truth_detail": detail,
    }
    if verdict == "PROVED_EQUAL":
        update["canon19_text"] = candidate
        update["status"] = "converged"
        update["converged"] = True
        update["reason"] = "JOB 1 (condition_table5.py's packed-mask " \
            "float compare model, canon19_render.py's XMM rendering): " \
            "candidate proved equal to the unit's own real ship " \
            "code directly"
        return update

    update["job1_packmask_decision"] = "KEEP_OLD -- %s: %s" % (
        verdict, detail[:200])
    return update


def run_language(lang, indir, outdir, canon4_docs, sem_map, tu2_map,
                  workdir):
    canon18_path = os.path.join(indir, "canon18_units_%s.json" % lang)
    doc = json.load(open(canon18_path))
    units = doc["units"]
    canon4_units = canon4_docs[lang]

    attempted = 0
    accepted = 0
    still_refused = 0
    no_candidate = 0
    skipped_not_our_shape = 0

    for n, u in units.items():
        if u.get("status") != "not_yet_converged":
            continue
        update = convert_one(lang, n, canon4_units.get(n, {}), u,
                              tu2_map, canon4_docs, sem_map, workdir)
        if update is None:
            skipped_not_our_shape = skipped_not_our_shape + 1
            continue
        u.update(update)
        if update.get("job1_packmask_candidate_text") is None and \
                "job1_packmask_refusal_reason" in update:
            no_candidate = no_candidate + 1
            continue
        attempted = attempted + 1
        if update.get("status") == "converged":
            accepted = accepted + 1
        else:
            still_refused = still_refused + 1

    doc["job1_packmask_tally"] = {
        "candidates_attempted": attempted,
        "accepted": accepted,
        "still_refused_after_attempt": still_refused,
        "no_candidate_at_all": no_candidate,
    }
    doc["meta"] = dict(doc["meta"])
    doc["meta"]["generator"] = "canon19.py (JOB 1: the packed-mask " \
        "float compare family) over canon18_units_%s.json" % lang
    doc["meta"]["generated_at"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    name = os.path.join(outdir, "canon19_units_%s.json" % lang)
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
    print("canon19.py -- JOB 1: the packed-mask float compare family")

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

    workdir = tempfile.mkdtemp(prefix="canon19_asm_")

    totals = {"candidates_attempted": 0, "accepted": 0,
              "still_refused_after_attempt": 0,
              "no_candidate_at_all": 0}
    for lang in LANGS:
        doc = run_language(lang, indir, outdir, canon4_docs, sem_map,
                            tu2_map, workdir)
        for k in totals:
            totals[k] += doc["job1_packmask_tally"][k]

    print("TOTAL: %r" % totals)
    print("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
