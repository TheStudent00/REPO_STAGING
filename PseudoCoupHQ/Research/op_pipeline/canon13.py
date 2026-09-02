#!/usr/bin/env python3
"""canon13.py -- STAGE 4 driver: the 16 compound boolean branch shapes
(hi-equal/lo-compare And/Or trees -- see canon13_render.py's header
for the measured shapes and the gen_bool() fix).

Mirrors canon12.py's own driver shape exactly, pointed at
canon13_render instead of canon12_render. The normalizer is UNCHANGED
from Stage 2 (canon12_normalize.apply_wide_v2/normalize_v2) -- Stage
4's gap was purely a rendering gap, not a normalization gap (see
canon13_render.py's header: condition_table2.py's own substitution
already produces the And/Or shape; gen7/gen11/gen12 just had no rule
to turn it back into instructions).

GATE: canon12_behaviour_check.wide_anchored_check, reused UNCHANGED
(a strict superset of canon9.Sim9 -- adds idiv/cltd/cqto modeling that
costs nothing when a candidate text never uses those mnemonics, which
none of these 16 units' candidates do; verified by inspection of every
accepted candidate's own mnemonic list, this lap's report).

BASELINE: canon12_units_<lang>.json (STAGE 2's output). A unit not
re-attempted, or re-attempted but not accepted, is copied through
BYTE-IDENTICAL -- zero regression by construction, verified separately
(this lap's report).

usage:
  canon13.py [--in DIR] [--out DIR]
"""

import json
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import condition_table2 as CT2                                  # noqa: E402
import canon13_render as R13                                    # noqa: E402
import canon12_normalize as C12N                                 # noqa: E402
import canon12_behaviour_check as BC10                           # noqa: E402
import canon9 as C9                                              # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]

job2_anchored_check = BC10.wide_anchored_check
load_tree_units2 = C9.load_tree_units2


def apply_wide_v2(tu2_unit, canon4_lines):
    """canon12.apply_wide_v2, unchanged -- Stage 4 needs no new
    normalizer behaviour, only a new renderer rule (see file header)."""
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

    old_text = old_rec.get("canon12_text") or old_rec.get(
        "canon11_text") or old_rec.get("canon10_text") or old_rec.get(
        "canon9_text") or old_rec.get("canon8_text") or old_rec.get(
        "canon7_text")

    result, context_record = R13.render_unit13(fixed_unit, workdir)
    if not isinstance(result, list):
        return None

    candidate = "; ".join(result)
    if candidate == old_text:
        return None

    verdict, detail = job2_anchored_check(
        lang, n, canon4_docs, sem_map, candidate)

    update = {
        "stage4_cause1_condition_substitutions": cond_applied,
        "stage4_cause1_note": cond_note,
        "stage4_candidate_text": candidate,
        "stage4_ground_truth_verdict": verdict,
        "stage4_ground_truth_detail": detail,
    }
    if verdict == "PROVED_EQUAL":
        update["canon13_text"] = candidate
        update["status"] = "converged"
        update["converged"] = True
        update["reason"] = "STAGE 4 (canon13_render.py's gen_bool() " \
            "compound and/or boolean-condition codegen rule): " \
            "candidate proved equal to the unit's own real ship " \
            "code directly"
        return update

    update["canon13_text"] = old_text
    update["stage4_decision"] = "KEEP_OLD -- %s: %s" % (
        verdict, detail[:200])
    return update


def run_language(lang, indir, outdir, canon4_docs, sem_map, tu2_map,
                  workdir):
    canon12_path = os.path.join(indir, "canon12_units_%s.json" % lang)
    doc = json.load(open(canon12_path))
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

    doc["stage4_tally"] = {
        "candidates_attempted": attempted,
        "accepted": accepted,
        "still_refused_after_attempt": still_refused,
        "not_applicable_this_pass": not_applicable,
    }
    doc["meta"] = dict(doc["meta"])
    doc["meta"]["generator"] = "canon13.py (STAGE 4: compound " \
        "boolean branch shapes) over canon12_units_%s.json" % lang
    doc["meta"]["generated_at"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    name = os.path.join(outdir, "canon13_units_%s.json" % lang)
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
    print("canon13.py -- STAGE 4: compound boolean branch shapes")

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
    workdir = tempfile.mkdtemp(prefix="canon13_asm_")

    totals = {"candidates_attempted": 0, "accepted": 0,
              "still_refused_after_attempt": 0,
              "not_applicable_this_pass": 0}
    for lang in LANGS:
        doc = run_language(lang, indir, outdir, canon4_docs, sem_map,
                            tu2_map, workdir)
        for k in totals:
            totals[k] += doc["stage4_tally"][k]

    print("TOTAL: %r" % totals)
    print("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
