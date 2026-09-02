#!/usr/bin/env python3
"""canon15.py -- JOB 2 driver: THE CALL-SITE PAIRING FIX
(condition_table3.py), targeted ONLY at canon14_units_<lang>.json's
own `job1_candidate_text` bucket that stayed DISPROVED (the 20 units
canon14_worked_examples.txt's own "HONEST CLOSURE ACCOUNT" traced to
condition_table2.substitute_conditions's positional call-site pairing
-- cpp's 4 `a <=> b` units, swift's 16 Int32/Int64-vs-UInt64 mixed-
signedness compares).

Mirrors canon14.py's own driver shape (apply_wide_v2, gate call, byte-
identical-unless-accepted update rule), pointed at condition_table3
instead of condition_table2, and re-attempting ONLY the units named
above (never a unit outside that set -- this file cannot regress
anything, structurally, since every OTHER not_yet_converged unit is
copied through unchanged and every converged unit is never opened at
all).

GATE: canon12_behaviour_check.wide_anchored_check, unchanged -- the
same gate every generation in this lineage uses.

BASELINE: canon14_units_<lang>.json.

usage:
  canon15.py [--in DIR] [--out DIR]
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

job2_anchored_check = BC10.wide_anchored_check
load_tree_units2 = C9.load_tree_units2

# THE TARGET SET -- exactly the units canon14_worked_examples.txt's
# own closure account traced to the call-site pairing defect. Named
# explicitly (not "every not_yet_converged unit") so this driver's own
# blast radius is auditable at a glance and cannot silently grow.
TARGET_UNITS = {
    "cpp": ["750", "751", "756", "757"],
    "swift": ["296", "302", "342", "343", "378", "379", "404", "410",
              "440", "446", "450", "451", "512", "518", "522", "523"],
}


def apply_wide_v3(tu2_unit, canon4_lines):
    """canon14.apply_wide_v2, pointed at condition_table3's fixed
    substitution instead of condition_table2's."""
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
    fixed_unit, cond_applied, cond_note = apply_wide_v3(
        tu2, canon4_lines)

    old_text = old_rec.get("canon14_text") or old_rec.get(
        "canon13_text") or old_rec.get("canon12_text") or old_rec.get(
        "canon11_text") or old_rec.get("canon10_text")

    result, context_record = R14.render_unit14(fixed_unit, workdir)
    if not isinstance(result, list):
        return {
            "job2_pairing_candidate_text": None,
            "job2_pairing_refusal_reason": result,
        }

    candidate = "; ".join(result)
    if candidate == old_text:
        return None

    verdict, detail = job2_anchored_check(
        lang, n, canon4_docs, sem_map, candidate)

    update = {
        "job2_pairing_cause1_condition_substitutions": cond_applied,
        "job2_pairing_cause1_note": cond_note,
        "job2_pairing_candidate_text": candidate,
        "job2_pairing_ground_truth_verdict": verdict,
        "job2_pairing_ground_truth_detail": detail,
    }
    if verdict == "PROVED_EQUAL":
        update["canon15_text"] = candidate
        update["status"] = "converged"
        update["converged"] = True
        update["reason"] = "JOB 2 (condition_table3.py's value-based " \
            "call-site pairing): candidate proved equal to the " \
            "unit's own real ship code directly"
        return update

    update["canon15_text"] = old_text
    update["job2_pairing_decision"] = "KEEP_OLD -- %s: %s" % (
        verdict, detail[:200])
    return update


def run_language(lang, indir, outdir, canon4_docs, sem_map, tu2_map,
                  workdir):
    canon14_path = os.path.join(indir, "canon14_units_%s.json" % lang)
    doc = json.load(open(canon14_path))
    units = doc["units"]
    canon4_units = canon4_docs[lang]

    targets = TARGET_UNITS.get(lang, [])
    attempted = 0
    accepted = 0
    still_refused = 0
    no_candidate = 0

    for n in targets:
        u = units.get(n)
        if u is None or u["status"] != "not_yet_converged":
            continue
        update = convert_one(lang, n, canon4_units[n], u, tu2_map,
                              canon4_docs, sem_map, workdir)
        if update is None:
            continue
        u.update(update)
        if update.get("job2_pairing_candidate_text") is None and \
                "job2_pairing_refusal_reason" in update:
            no_candidate = no_candidate + 1
            continue
        attempted = attempted + 1
        if update.get("status") == "converged":
            accepted = accepted + 1
        else:
            still_refused = still_refused + 1

    doc["job2_pairing_tally"] = {
        "target_units_this_lang": len(targets),
        "candidates_attempted": attempted,
        "accepted": accepted,
        "still_refused_after_attempt": still_refused,
        "no_candidate_at_all": no_candidate,
    }
    doc["meta"] = dict(doc["meta"])
    doc["meta"]["generator"] = "canon15.py (JOB 2: the call-site " \
        "pairing defect) over canon14_units_%s.json" % lang
    doc["meta"]["generated_at"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    name = os.path.join(outdir, "canon15_units_%s.json" % lang)
    fh = open(name, "w")
    json.dump(doc, fh, indent=1)
    fh.close()
    print("wrote %s (%d attempted, %d accepted, %d still refused, "
          "%d no candidate)"
          % (name, attempted, accepted, still_refused, no_candidate))
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
    print("canon15.py -- JOB 2: the call-site pairing defect")

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
    workdir = tempfile.mkdtemp(prefix="canon15_asm_")

    totals = {"candidates_attempted": 0, "accepted": 0,
              "still_refused_after_attempt": 0,
              "no_candidate_at_all": 0}
    for lang in LANGS:
        doc = run_language(lang, indir, outdir, canon4_docs, sem_map,
                            tu2_map, workdir)
        for k in totals:
            totals[k] += doc["job2_pairing_tally"][k]

    print("TOTAL: %r" % totals)
    print("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
