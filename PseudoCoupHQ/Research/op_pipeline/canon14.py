#!/usr/bin/env python3
"""canon14.py -- JOB 1 driver: re-attempts EVERY not_yet_converged unit
(not a pre-filtered bucket -- the defect canon14_render.py fixes was
found in THREE separate places, none of them sharing one z3-op or
condition-shape filter, so the honest thing is to let the fixed
renderer see everything still open and let the gate decide) against
canon13_units_<lang>.json's own baseline (STAGE 4's output, the newest
prior generation).

Mirrors canon13.py's own driver shape (apply_wide_v2, the tu2_map /
canon4_docs / sem_map loading, the gate call, the byte-identical-
unless-accepted update rule) exactly, pointed at canon14_render
instead of canon13_render. The normalizer is UNCHANGED from Stage 2/4
-- this lap's gap was purely a rendering gap (see canon14_render.py's
header).

GATE: canon12_behaviour_check.wide_anchored_check, reused UNCHANGED --
the same superset gate canon13.py already used, itself built directly
on canon8_behaviour_check's re-anchored-to-real-ship-code check (see
that file's own header): every candidate is proved against the unit's
OWN real ship mnemonic text, never a prior rendering.

BASELINE: canon13_units_<lang>.json. A unit not re-attempted, or
re-attempted but not accepted, is copied through BYTE-IDENTICAL --
zero regression by construction, verified separately (this lap's
report runs a programmatic diff).

usage:
  canon14.py [--in DIR] [--out DIR]
"""

import json
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import condition_table2 as CT2                                  # noqa: E402
import canon14_render as R14                                    # noqa: E402
import canon12_normalize as C12N                                 # noqa: E402
import canon12_behaviour_check as BC10                           # noqa: E402
import canon9 as C9                                              # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]

job1_anchored_check = BC10.wide_anchored_check
load_tree_units2 = C9.load_tree_units2


def apply_wide_v2(tu2_unit, canon4_lines):
    """canon13.apply_wide_v2, unchanged -- see that file's own header;
    JOB 1 needs no new normalizer behaviour, only the renderer fix."""
    out = dict(tu2_unit)
    raw = tu2_unit.get("normal_path_raw")
    if tu2_unit.get("sem_ok") is False or raw is None:
        return out, 0, "n/a"
    if "amd64g_calculate_condition" in raw:
        raw, applied, sub_note = CT2.resolve_conditions(
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
    fixed_unit, cond_applied, cond_note = apply_wide_v2(
        tu2, canon4_lines)

    old_text = old_rec.get("canon13_text") or old_rec.get(
        "canon12_text") or old_rec.get("canon11_text") or old_rec.get(
        "canon10_text") or old_rec.get("canon9_text") or old_rec.get(
        "canon8_text") or old_rec.get("canon7_text")

    result, context_record = R14.render_unit14(fixed_unit, workdir)
    if not isinstance(result, list):
        return {
            "job1_candidate_text": None,
            "job1_refusal_reason": result,
        }

    candidate = "; ".join(result)
    if candidate == old_text:
        return None

    verdict, detail = job1_anchored_check(
        lang, n, canon4_docs, sem_map, candidate)

    update = {
        "job1_cause1_condition_substitutions": cond_applied,
        "job1_cause1_note": cond_note,
        "job1_candidate_text": candidate,
        "job1_ground_truth_verdict": verdict,
        "job1_ground_truth_detail": detail,
    }
    if verdict == "PROVED_EQUAL":
        update["canon14_text"] = candidate
        update["status"] = "converged"
        update["converged"] = True
        update["reason"] = "JOB 1 (canon14_render.py's dead-leaf " \
            "fold + semantic extend recognizer): candidate proved " \
            "equal to the unit's own real ship code directly"
        return update

    update["canon14_text"] = old_text
    update["job1_decision"] = "KEEP_OLD -- %s: %s" % (
        verdict, detail[:200])
    return update


def run_language(lang, indir, outdir, canon4_docs, sem_map, tu2_map,
                  workdir):
    canon13_path = os.path.join(indir, "canon13_units_%s.json" % lang)
    doc = json.load(open(canon13_path))
    units = doc["units"]
    canon4_units = canon4_docs[lang]

    attempted = 0
    accepted = 0
    still_refused = 0
    not_applicable = 0
    no_candidate = 0

    for n, u in units.items():
        if u["status"] != "not_yet_converged":
            continue
        update = convert_one(lang, n, canon4_units[n], u, tu2_map,
                              canon4_docs, sem_map, workdir)
        if update is None:
            not_applicable = not_applicable + 1
            continue
        u.update(update)
        if update.get("job1_candidate_text") is None and \
                "job1_refusal_reason" in update:
            no_candidate = no_candidate + 1
            continue
        attempted = attempted + 1
        if update.get("status") == "converged":
            accepted = accepted + 1
        else:
            still_refused = still_refused + 1

    doc["job1_tally"] = {
        "candidates_attempted": attempted,
        "accepted": accepted,
        "still_refused_after_attempt": still_refused,
        "no_candidate_at_all": no_candidate,
        "not_applicable_this_pass": not_applicable,
    }
    doc["meta"] = dict(doc["meta"])
    doc["meta"]["generator"] = "canon14.py (JOB 1: the bit-serial " \
        "reconstruction defect) over canon13_units_%s.json" % lang
    doc["meta"]["generated_at"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    name = os.path.join(outdir, "canon14_units_%s.json" % lang)
    fh = open(name, "w")
    json.dump(doc, fh, indent=1)
    fh.close()
    print("wrote %s (%d attempted, %d accepted, %d still refused, "
          "%d no candidate, %d not applicable this pass)"
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
    print("canon14.py -- JOB 1: the bit-serial reconstruction defect")

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
    workdir = tempfile.mkdtemp(prefix="canon14_asm_")

    totals = {"candidates_attempted": 0, "accepted": 0,
              "still_refused_after_attempt": 0,
              "no_candidate_at_all": 0,
              "not_applicable_this_pass": 0}
    for lang in LANGS:
        doc = run_language(lang, indir, outdir, canon4_docs, sem_map,
                            tu2_map, workdir)
        for k in totals:
            totals[k] += doc["job1_tally"][k]

    print("TOTAL: %r" % totals)
    print("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
