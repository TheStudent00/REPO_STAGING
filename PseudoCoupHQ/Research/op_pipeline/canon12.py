#!/usr/bin/env python3
"""canon12.py -- STAGE 2 driver: 128-bit widening arithmetic (Mul64,
Mul32, DivModU128to64, DivModS128to64 -- see canon12_normalize.py's
header for the model and canon12_render.py's for the codegen rule).

Mirrors canon11.py's own driver shape exactly (itself a straight port
of canon9.py's convert_one/run_language), pointed at canon12_render
instead of canon11_render, and at a normalizer
(canon12_normalize.apply_wide_v2, below) that runs condition_table2's
CAUSE-1 substitution first -- unchanged -- then the wide-arithmetic
model instead of tree_match2.normalize.

BASELINE: canon11_units_<lang>.json (STAGE 1's output). A unit not
re-attempted, or re-attempted but not accepted, is copied through
BYTE-IDENTICAL -- zero regression by construction, verified separately
(this lap's report).

usage:
  canon12.py [--in DIR] [--out DIR]
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
import canon12_render as R12                                    # noqa: E402
import canon12_normalize as C12N                                 # noqa: E402
import canon12_behaviour_check as BC10                           # noqa: E402
import canon9 as C9                                              # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]

job2_anchored_check = BC10.wide_anchored_check
load_tree_units2 = C9.load_tree_units2


def apply_wide_v2(tu2_unit, canon4_lines):
    """canon9.apply_cause123_v2, pointed at canon12_normalize's wide-
    arithmetic model instead of tree_match2.normalize -- the CAUSE-1
    condition substitution step itself is UNCHANGED (most of these
    units carry no amd64g_calculate_condition call at all, so this is
    a no-op for them; kept for units that combine a condition with a
    wide-arithmetic atom, if any)."""
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

    old_text = old_rec.get("canon11_text") or old_rec.get(
        "canon10_text") or old_rec.get("canon9_text") or old_rec.get(
        "canon8_text") or old_rec.get("canon7_text")

    result, context_record = R12.render_unit12(fixed_unit, workdir)
    if not isinstance(result, list):
        return None

    candidate = "; ".join(result)
    if candidate == old_text:
        return None

    verdict, detail = job2_anchored_check(
        lang, n, canon4_docs, sem_map, candidate)

    update = {
        "stage2_cause1_condition_substitutions": cond_applied,
        "stage2_cause1_note": cond_note,
        "stage2_candidate_text": candidate,
        "stage2_ground_truth_verdict": verdict,
        "stage2_ground_truth_detail": detail,
    }
    if verdict == "PROVED_EQUAL":
        update["canon12_text"] = candidate
        update["status"] = "converged"
        update["converged"] = True
        update["reason"] = "STAGE 2 (canon12_normalize.py's z3 wide-" \
            "bitvector model for Mul64/Mul32/DivModU128to64/" \
            "DivModS128to64, rendered by canon12_render.py's %rax/" \
            "%rdx-pinned idiv/div rule): candidate proved equal to " \
            "the unit's own real ship code directly"
        return update

    update["canon12_text"] = old_text
    update["stage2_decision"] = "KEEP_OLD -- %s: %s" % (
        verdict, detail[:200])
    return update


def run_language(lang, indir, outdir, canon4_docs, sem_map, tu2_map,
                  workdir):
    canon11_path = os.path.join(indir, "canon11_units_%s.json" % lang)
    doc = json.load(open(canon11_path))
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

    doc["stage2_tally"] = {
        "candidates_attempted": attempted,
        "accepted": accepted,
        "still_refused_after_attempt": still_refused,
        "not_applicable_this_pass": not_applicable,
    }
    doc["meta"] = dict(doc["meta"])
    doc["meta"]["generator"] = "canon12.py (STAGE 2: 128-bit " \
        "widening arithmetic) over canon11_units_%s.json" % lang
    doc["meta"]["generated_at"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    name = os.path.join(outdir, "canon12_units_%s.json" % lang)
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
    print("canon12.py -- STAGE 2: 128-bit widening arithmetic")

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
    workdir = tempfile.mkdtemp(prefix="canon12_asm_")

    totals = {"candidates_attempted": 0, "accepted": 0,
              "still_refused_after_attempt": 0,
              "not_applicable_this_pass": 0}
    for lang in LANGS:
        doc = run_language(lang, indir, outdir, canon4_docs, sem_map,
                            tu2_map, workdir)
        for k in totals:
            totals[k] += doc["stage2_tally"][k]

    print("TOTAL: %r" % totals)
    print("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
