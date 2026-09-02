#!/usr/bin/env python3
"""canon26.py -- log_084 lap, item 3 of the coordinator's "resolution
claims without a gate run stay unverified" instruction: re-runs
canon23.py's OWN PROVEN MACHINERY (condition_table9's combined float-
packed + direct-numeric-integer substitution, canon22_float's z3
model, canon22_render's XMM+conversion rendering, canon22_behaviour_
check's real z3 FPA ground-truth gate -- every one of the four
imported UNCHANGED, function reference not copy, identical reuse
discipline to canon23.py's own header) against the CURRENT baseline
(canon24_units_<lang>.json), with ONE difference from canon23.py:
canon23.py's own `multi_atom_call_count(...) < 2` gate (its file
targets ONLY units with 2-OR-MORE amd64g_calculate_condition call
sites -- single-atom units were canon17-22's own target, a DIFFERENT
population) is widened to `< 1`, so THIS file also re-attempts the
single-atom residue log_084's own survey found still not-yet-converged
at the canon24 baseline (33 of the 57 units the survey counted).

WHY THIS IS THE RIGHT WAY TO ANSWER "does condition_table9's
substitution actually converge units, or only resolve the numeric
layer": log_084's first section INTERPRETED the 56/57-resolved-at-
substitution-layer finding as blocked by a missing render rule for
boolean OR/AND combinations of named FCxx atoms. That was an
INTERPRETATION (evidence class stated as such in the log), not a gate
run. canon23.py's own already-converged 2+-atom population is proof
that canon22_render.py's generic dispatch DOES already compose named
condition atoms through ordinary bitwise Or8/And8 nodes (it delegates
to the generic z3-node renderer for everything gen17/gen22's own
fcond-atom hook does not intercept directly) -- so the interpretation
in log_084's first section may have been wrong. This file finds out
by actually running the gate, not by re-reading the code more
carefully.

BASELINE: canon24_units_<lang>.json. RAW SOURCE: tree_units3.json,
unchanged from canon23.py.

ZERO REGRESSIONS: only a `status != "converged"` record is ever
opened -- identical discipline to canon23.py/canon24.py; an already-
converged unit's own text is never touched by this file.

usage:
  canon26.py [--in DIR] [--out DIR]
"""

import json
import os
import re
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import condition_table9 as CT9                                  # noqa: E402
import canon22_float as CF22                                     # noqa: E402
import canon22_render as R22                                     # noqa: E402
import canon22_behaviour_check as BC22                           # noqa: E402
import canon23 as C23                                            # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]

CALL_RE = C23.CALL_RE
old_text_of = C23.old_text_of
load_tree_units3 = C23.load_tree_units3


def any_atom_call_count(tu3_unit):
    raw = tu3_unit.get("normal_path_raw")
    if raw is None:
        return 0
    return len(CALL_RE.findall(raw))


def build_fixed_unit(tu3_unit):
    """IDENTICAL to canon23.build_fixed_unit except the threshold is
    `< 1` (any unit with at least one amd64g_calculate_condition call)
    instead of canon23.py's own `< 2` (see file header)."""
    raw = tu3_unit.get("normal_path_raw")
    if tu3_unit.get("sem_ok") is False or raw is None:
        return None, 0, 0, "n/a", [], "n/a"
    if any_atom_call_count(tu3_unit) < 1:
        return None, 0, 0, "not this file's own target shape (no " \
            "amd64g_calculate_condition calls)", [], "n/a"
    new_raw, float_applied, int_applied, float_note, unresolved = \
        CT9.substitute_all(raw)
    if float_applied == 0 and int_applied == 0:
        return None, 0, 0, float_note, unresolved, "n/a"
    new_root, ok, norm_note = CF22.normalize_v2e(new_raw)
    fixed = dict(tu3_unit)
    fixed["normal_path_raw"] = new_raw
    fixed["normal_path_root"] = new_root
    fixed["normalize_ok"] = ok
    fixed["normalize_note"] = norm_note
    return fixed, float_applied, int_applied, float_note, unresolved, \
        norm_note


def convert_one(lang, n, canon4_rec, old_rec, tu3_map, canon4_docs,
                 sem_map, workdir):
    if old_rec.get("branch_kind") != "straight_line":
        return None
    tu3 = tu3_map.get((lang, n))
    if tu3 is None:
        return None

    fixed_unit, float_applied, int_applied, sub_note, unresolved, \
        norm_note = build_fixed_unit(tu3)
    if fixed_unit is None:
        return None

    if unresolved:
        return {
            "job3_anyatom_float_condition_substitutions": float_applied,
            "job3_anyatom_int_condition_substitutions": int_applied,
            "job3_anyatom_substitution_note": sub_note,
            "job3_anyatom_normalize_note": norm_note,
            "job3_anyatom_candidate_text": None,
            "job3_anyatom_refusal_reason": "no return path: %d "
            "amd64g_calculate_condition call(s) left unresolved by "
            "condition_table9.py's own SUB/LOGIC/float whitelist: %r"
            % (len(unresolved), unresolved),
        }

    if not fixed_unit.get("normalize_ok"):
        return {
            "job3_anyatom_float_condition_substitutions": float_applied,
            "job3_anyatom_int_condition_substitutions": int_applied,
            "job3_anyatom_substitution_note": sub_note,
            "job3_anyatom_normalize_note": norm_note,
            "job3_anyatom_candidate_text": None,
            "job3_anyatom_refusal_reason":
                "no return path: canon22_float.normalize_v2e failed "
                "on the condition_table9-substituted text (%s)" %
                norm_note,
        }

    old_text = old_text_of(old_rec)

    meta = old_rec.get("meta") or {}
    a_is_vector = meta.get("lhs_rep") in ("f32", "f64")
    R22.set_render_context(a_is_vector)

    result, ctxd = R22.render_unit22(fixed_unit, workdir)
    if not isinstance(result, list):
        return {
            "job3_anyatom_float_condition_substitutions": float_applied,
            "job3_anyatom_int_condition_substitutions": int_applied,
            "job3_anyatom_substitution_note": sub_note,
            "job3_anyatom_normalize_note": norm_note,
            "job3_anyatom_candidate_text": None,
            "job3_anyatom_refusal_reason": result,
        }

    candidate = "; ".join(result)
    if candidate == old_text:
        return None

    verdict, detail = BC22.anchored_check(
        lang, n, canon4_docs, sem_map, candidate, a_is_vector)

    update = {
        "job3_anyatom_float_condition_substitutions": float_applied,
        "job3_anyatom_int_condition_substitutions": int_applied,
        "job3_anyatom_substitution_note": sub_note,
        "job3_anyatom_normalize_note": norm_note,
        "job3_anyatom_candidate_text": candidate,
        "job3_anyatom_ground_truth_verdict": verdict,
        "job3_anyatom_ground_truth_detail": detail,
    }
    if verdict == "PROVED_EQUAL":
        update["canon26_text"] = candidate
        update["status"] = "converged"
        update["converged"] = True
        update["reason"] = "canon26.py (log_084 lap, item 3: re-run " \
            "canon23.py's own proven fan-out machinery -- condition_" \
            "table9 substitution, canon22_float normalize, canon22_" \
            "render, canon22_behaviour_check -- widened from >=2 to " \
            ">=1 amd64g_calculate_condition call sites, against the " \
            "current canon24_units baseline): candidate proved " \
            "equal to the unit's own real ship code directly"
        return update

    update["job3_anyatom_decision"] = "KEEP_OLD -- %s: %s" % (
        verdict, detail[:200])
    return update


def run_language(lang, indir, outdir, canon4_docs, sem_map, tu3_map,
                  workdir):
    canon24_path = os.path.join(indir, "canon24_units_%s.json" % lang)
    doc = json.load(open(canon24_path))
    units = doc["units"]
    canon4_units = canon4_docs[lang]

    attempted = 0
    accepted = 0
    still_refused = 0
    no_candidate = 0
    skipped_not_our_shape = 0

    for n, u in units.items():
        if u.get("status") == "converged":
            continue
        update = convert_one(lang, n, canon4_units.get(n, {}), u,
                              tu3_map, canon4_docs, sem_map, workdir)
        if update is None:
            skipped_not_our_shape = skipped_not_our_shape + 1
            continue
        u.update(update)
        if update.get("job3_anyatom_candidate_text") is None and \
                "job3_anyatom_refusal_reason" in update:
            no_candidate = no_candidate + 1
            continue
        attempted = attempted + 1
        if update.get("status") == "converged":
            accepted = accepted + 1
        else:
            still_refused = still_refused + 1

    doc["job3_anyatom_tally"] = {
        "candidates_attempted": attempted,
        "accepted": accepted,
        "still_refused_after_attempt": still_refused,
        "no_candidate_at_all": no_candidate,
    }
    doc["meta"] = dict(doc["meta"])
    doc["meta"]["generator"] = "canon26.py (log_084 lap, item 3: " \
        "re-run canon23.py's own proven fan-out machinery, widened " \
        "to any-atom-count, over canon24_units_%s.json" % lang
    doc["meta"]["generated_at"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    name = os.path.join(outdir, "canon26_units_%s.json" % lang)
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
    print("canon26.py -- log_084 item 3: re-run the proven fan-out "
          "machinery, any-atom-count, over the current baseline")

    canon4_docs = {}
    for lang in LANGS:
        canon4_docs[lang] = json.load(open(
            os.path.join(indir, "canon4_units_%s.json" % lang)
        ))["units"]

    sem_map = {}
    for lang in LANGS:
        path = os.path.join(indir, "sem_anchored_spill_%s.json" % lang)
        sem_map[lang] = json.load(open(path))["units"]

    tu3_map = load_tree_units3()
    workdir = tempfile.mkdtemp(prefix="canon26_asm_")

    totals = {"candidates_attempted": 0, "accepted": 0,
              "still_refused_after_attempt": 0,
              "no_candidate_at_all": 0}
    for lang in LANGS:
        doc = run_language(lang, indir, outdir, canon4_docs, sem_map,
                            tu3_map, workdir)
        for k in totals:
            totals[k] += doc["job3_anyatom_tally"][k]

    print("TOTAL: %r" % totals)
    print("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
