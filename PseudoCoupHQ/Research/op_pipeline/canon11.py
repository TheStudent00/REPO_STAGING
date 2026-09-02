#!/usr/bin/env python3
"""canon11.py -- STAGE 1 driver: re-attempt every not_yet_converged
STRAIGHT-LINE unit through canon11_render.gen11 (the two single-site
fixes -- see canon11_render.py's own header for the full diagnosis of
each), gated by the SAME ground-truth-anchored check canon9.py itself
uses (canon9.job2_anchored_check, i.e. canon8_behaviour_check's
anchored_check with canon9's flag-aware Sim9 -- proves a candidate
against the unit's OWN REAL SHIP CODE directly, never a prior
rendering).

SCOPE: only straight_line units are re-attempted (branching units'
CAUSE-1 substitution lives inside render_branching_unit7, which this
lap's two fixes do not touch -- consistent with canon9.py's own
documented scope restriction). BASELINE is canon10_units_<lang>.json
(the current-best corpus); a unit not re-attempted, or re-attempted
but not accepted, is copied through BYTE-IDENTICAL -- zero regression
by construction, verified separately by uniqueness_audit-style diff
after this file runs (see this lap's own report).

DRIVER SHAPE: a straight port of canon9.py's own convert_one/
run_language, pointed at canon11_render instead of canon7_render, and
at canon10_units_<lang>.json instead of canon8_units_<lang>.json.

usage:
  canon11.py [--in DIR] [--out DIR]
"""

import json
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import tree_match2 as TM2                                       # noqa: E402
import condition_table2 as CT2                                  # noqa: E402
import canon11_render as R11                                    # noqa: E402
import canon9 as C9                                              # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]

apply_cause123_v2 = C9.apply_cause123_v2
job2_anchored_check = C9.job2_anchored_check
load_tree_units2 = C9.load_tree_units2


def convert_one(lang, n, canon4_rec, old_rec, tu2_map, canon4_docs,
                 sem_map, workdir):
    """returns None if this unit is not a candidate for re-attempt
    (copy old_rec through unchanged); otherwise a dict of the FIELDS
    TO UPDATE on top of old_rec. Mirrors canon9.convert_one exactly,
    pointed at canon11_render.render_unit11."""
    if old_rec.get("branch_kind") != "straight_line":
        return None
    tu2 = tu2_map.get((lang, n))
    if tu2 is None:
        return None

    canon4_lines = canon4_rec.get("derived_text")
    fixed_unit, cond_applied, cond_note = apply_cause123_v2(
        tu2, canon4_lines)

    old_text = old_rec.get("canon10_text") or old_rec.get(
        "canon9_text") or old_rec.get("canon8_text") or old_rec.get(
        "canon7_text")

    result, context_record = R11.render_unit11(fixed_unit, workdir)
    if not isinstance(result, list):
        return None  # still refuses, for a DIFFERENT reason -- out of
                      # STAGE 1's diagnosed scope (72 units).

    candidate = "; ".join(result)
    if candidate == old_text:
        return None  # no change -- nothing to re-adjudicate

    verdict, detail = job2_anchored_check(
        lang, n, canon4_docs, sem_map, candidate)

    update = {
        "stage1_cause1_condition_substitutions": cond_applied,
        "stage1_cause1_note": cond_note,
        "stage1_candidate_text": candidate,
        "stage1_ground_truth_verdict": verdict,
        "stage1_ground_truth_detail": detail,
    }
    if verdict == "PROVED_EQUAL":
        update["canon11_text"] = candidate
        update["status"] = "converged"
        update["converged"] = True
        update["reason"] = "STAGE 1 (canon11_render.py's two single-" \
            "site gen7 fixes -- stale comparison width off a zero-" \
            "extend concat, and De Morgan folding through a negated " \
            "concat): candidate proved equal to the unit's own real " \
            "ship code directly"
        return update

    update["canon11_text"] = old_text
    update["stage1_decision"] = "KEEP_OLD -- %s: %s" % (
        verdict, detail[:200])
    return update


def run_language(lang, indir, outdir, canon4_docs, sem_map, tu2_map,
                  workdir):
    canon10_path = os.path.join(indir, "canon10_units_%s.json" % lang)
    doc = json.load(open(canon10_path))
    units = doc["units"]
    canon4_units = canon4_docs[lang]

    attempted = 0
    accepted = 0
    still_refused = 0
    not_applicable = 0

    for n, u in units.items():
        if u["status"] != "not_yet_converged":
            continue
        update = convert_one(lang, n, canon4_units[n], u, tu2_map,
                              canon4_docs, sem_map, workdir)
        if update is None:
            not_applicable += 1
            continue
        attempted += 1
        u.update(update)
        if update.get("status") == "converged":
            accepted += 1
        else:
            still_refused += 1

    doc["stage1_tally"] = {
        "candidates_attempted": attempted,
        "accepted": accepted,
        "still_refused_after_attempt": still_refused,
        "not_applicable_this_pass": not_applicable,
    }
    doc["meta"] = dict(doc["meta"])
    doc["meta"]["generator"] = "canon11.py (STAGE 1: canon11_render " \
        "single-site gen7 fixes) over canon10_units_%s.json" % lang
    doc["meta"]["generated_at"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    name = os.path.join(outdir, "canon11_units_%s.json" % lang)
    fh = open(name, "w")
    json.dump(doc, fh, indent=1)
    fh.close()
    print("wrote %s (%d attempted, %d accepted, %d still refused, "
          "%d not applicable this pass)"
          % (name, attempted, accepted, still_refused, not_applicable))
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
    print("canon11.py -- STAGE 1: the two diagnosed renderer defects")

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
    workdir = tempfile.mkdtemp(prefix="canon11_asm_")

    totals = {"candidates_attempted": 0, "accepted": 0,
              "still_refused_after_attempt": 0,
              "not_applicable_this_pass": 0}
    for lang in LANGS:
        doc = run_language(lang, indir, outdir, canon4_docs, sem_map,
                            tu2_map, workdir)
        for k in totals:
            totals[k] += doc["stage1_tally"][k]

    print("TOTAL: %r" % totals)
    print("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
