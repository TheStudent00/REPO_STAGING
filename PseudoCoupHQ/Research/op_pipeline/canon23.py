#!/usr/bin/env python3
"""canon23.py -- driver: log_081 work item 2, THE FAN-OUT TRACER over
MULTI-ATOM condition refusals. condition_table9.py's combined float-
packed-flags (condition_table4.py) + direct-numeric integer LOGIC/SUB
(this file's own new companion) substitution, run in ONE pass over the
SAME unit's raw text, + canon22_float.py's z3 model (already handles
BOTH atom families in its own fallback chain, unmodified -- see
condition_table9.py's own header) + canon22_render.py's XMM+conversion
rendering (already dispatches `fcond` atoms and falls through to the
inherited CondXX/If rendering for everything else, unmodified) +
canon22_behaviour_check.py's real-z3-FPA ground-truth gate (already
interprets ordinary integer test/setcc lines via its own inherited
Sim9f.exec_line, unmodified) -- wired together exactly the way
canon22.py wires its own generation's pieces together. NONE of those
four files needed a single line changed: the missing piece named in
the work order ("resolve EACH atom through its applicable table and
combine the resolved predicates with the boolean structure the
normalized expression already records") was PURELY a substitution-
coverage gap, closed by condition_table9.py alone.

TARGET SET: every not-yet-converged unit in canon22_units_<lang>.json
whose own tree_units3.json record (the ADOPTED tree_match3.py
baseline -- ret-block-first selection) has a `normal_path_raw`
containing 2 OR MORE `amd64g_calculate_condition(` call sites (the
"fan-out" shape this file exists for -- a single boolean expression
built from more than one flag-reading atom, exactly SEEDED GROUPING
UNDER CONDITIONS's "trace follows transformations indefinitely" ruling
applied to condition atoms specifically). A unit with 0 or 1 such call
is never opened here -- canon17/19/20/21/22.py's own single-atom
drivers already covered that population; this file cannot regress it
structurally, by the same "never widened beyond its own target set"
guarantee every driver in this lineage states for itself.

BASELINE: canon22_units_<lang>.json (the newest generation on disk
before this lap). RAW SOURCE: tree_units3.json (tree_match3.py's own
ret-block-first `normal_path_raw`/`normal_path_root` -- NOT
tree_units2.json/tree_match2's global-largest-tree rule, which this
lap's own AgentMemory entry names as ADOPTED specifically to replace).

GATE: canon22_behaviour_check.anchored_check, imported unchanged.

ZERO REGRESSIONS: only a `status != "converged"` record is ever
opened (identical discipline to every driver in this lineage); an
already-converged unit's newest-generation text field is never
touched by this file's own loop.

usage:
  canon23.py [--in DIR] [--out DIR]
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

LANGS = ["c", "cpp", "go", "rust", "swift"]

OLD_TEXT_FIELDS = [
    "canon22_text", "canon21_text", "canon20_text", "canon19_text",
    "canon18_text", "canon17_text", "canon16_text", "canon15_text",
    "canon14_text", "canon13_text", "canon12_text", "canon11_text",
    "canon10_text", "canon9_text", "canon8_text", "canon7_text",
]

CALL_RE = re.compile(r"amd64g_calculate_condition\(")


def old_text_of(old_rec):
    for f in OLD_TEXT_FIELDS:
        v = old_rec.get(f)
        if v is not None:
            return v
    return None


def load_tree_units3():
    """tree_units3.json's own per-unit records, keyed (lang, n) --
    the SAME shape tree_units2.json's own records use (lang, n,
    sem_ok, normal_path_raw, normal_path_root, normalize_ok, ...), so
    every downstream consumer built for tu2 (build_fixed_unit-style
    substitution, render_unit22, anchored_check) works unchanged."""
    path = os.path.join(HERE, "tree_units3.json")
    doc = json.load(open(path))
    out = {}
    for u in doc["units"]:
        out[(u["lang"], u["n"])] = u
    return out


def multi_atom_call_count(tu3_unit):
    raw = tu3_unit.get("normal_path_raw")
    if raw is None:
        return 0
    return len(CALL_RE.findall(raw))


def build_fixed_unit(tu3_unit):
    """condition_table9's combined substitution + canon22_float's
    z3 model, over ONE unit's own tree_units3.json raw text.
    (fixed_unit, float_applied, int_applied, sub_note, unresolved,
    norm_note). fixed_unit is None if this unit is not this file's own
    target shape (fewer than 2 amd64g_calculate_condition calls, or no
    raw text at all)."""
    raw = tu3_unit.get("normal_path_raw")
    if tu3_unit.get("sem_ok") is False or raw is None:
        return None, 0, 0, "n/a", [], "n/a"
    if multi_atom_call_count(tu3_unit) < 2:
        return None, 0, 0, "not this file's own target shape (fewer " \
            "than 2 amd64g_calculate_condition calls)", [], "n/a"
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
            "job2_fanout_float_condition_substitutions": float_applied,
            "job2_fanout_int_condition_substitutions": int_applied,
            "job2_fanout_substitution_note": sub_note,
            "job2_fanout_normalize_note": norm_note,
            "job2_fanout_candidate_text": None,
            "job2_fanout_refusal_reason": "no return path: %d "
            "amd64g_calculate_condition call(s) left unresolved by "
            "condition_table9.py's own SUB/LOGIC/float whitelist: %r"
            % (len(unresolved), unresolved),
        }

    old_text = old_text_of(old_rec)

    meta = old_rec.get("meta") or {}
    a_is_vector = meta.get("lhs_rep") in ("f32", "f64")
    R22.set_render_context(a_is_vector)

    result, ctxd = R22.render_unit22(fixed_unit, workdir)
    if not isinstance(result, list):
        return {
            "job2_fanout_float_condition_substitutions": float_applied,
            "job2_fanout_int_condition_substitutions": int_applied,
            "job2_fanout_substitution_note": sub_note,
            "job2_fanout_normalize_note": norm_note,
            "job2_fanout_candidate_text": None,
            "job2_fanout_refusal_reason": result,
        }

    candidate = "; ".join(result)
    if candidate == old_text:
        return None

    verdict, detail = BC22.anchored_check(
        lang, n, canon4_docs, sem_map, candidate, a_is_vector)

    update = {
        "job2_fanout_float_condition_substitutions": float_applied,
        "job2_fanout_int_condition_substitutions": int_applied,
        "job2_fanout_substitution_note": sub_note,
        "job2_fanout_normalize_note": norm_note,
        "job2_fanout_candidate_text": candidate,
        "job2_fanout_ground_truth_verdict": verdict,
        "job2_fanout_ground_truth_detail": detail,
    }
    if verdict == "PROVED_EQUAL":
        update["canon23_text"] = candidate
        update["status"] = "converged"
        update["converged"] = True
        update["reason"] = "canon23.py (log_081 item 2, the fan-out " \
            "tracer: condition_table9.py's combined float-packed + " \
            "direct-numeric-integer condition substitution over " \
            "tree_units3.json's ret-block-first raw text, canon22_" \
            "render.py's XMM+conversion rendering, real z3 FPA " \
            "ground-truth gate): candidate proved equal to the " \
            "unit's own real ship code directly"
        return update

    update["job2_fanout_decision"] = "KEEP_OLD -- %s: %s" % (
        verdict, detail[:200])
    return update


def run_language(lang, indir, outdir, canon4_docs, sem_map, tu3_map,
                  workdir):
    canon22_path = os.path.join(indir, "canon22_units_%s.json" % lang)
    doc = json.load(open(canon22_path))
    units = doc["units"]
    canon4_units = canon4_docs[lang]

    attempted = 0
    accepted = 0
    still_refused = 0
    no_candidate = 0
    skipped_not_our_shape = 0

    # ZERO-REGRESSIONS BY CONSTRUCTION: only a non-converged record is
    # ever opened, so an already-converged unit's newest text field
    # cannot change here -- identical discipline to canon22.py's own
    # loop, verified programmatically by this lap's own guard script
    # (see report).
    for n, u in units.items():
        if u.get("status") == "converged":
            continue
        update = convert_one(lang, n, canon4_units.get(n, {}), u,
                              tu3_map, canon4_docs, sem_map, workdir)
        if update is None:
            skipped_not_our_shape = skipped_not_our_shape + 1
            continue
        u.update(update)
        if update.get("job2_fanout_candidate_text") is None and \
                "job2_fanout_refusal_reason" in update:
            no_candidate = no_candidate + 1
            continue
        attempted = attempted + 1
        if update.get("status") == "converged":
            accepted = accepted + 1
        else:
            still_refused = still_refused + 1

    doc["job2_fanout_tally"] = {
        "candidates_attempted": attempted,
        "accepted": accepted,
        "still_refused_after_attempt": still_refused,
        "no_candidate_at_all": no_candidate,
    }
    doc["meta"] = dict(doc["meta"])
    doc["meta"]["generator"] = "canon23.py (log_081 item 2: the " \
        "fan-out condition tracer, multi-atom amd64g_calculate_" \
        "condition/CmpF64 refusals) over canon22_units_%s.json, " \
        "raw text re-sourced from tree_units3.json" % lang
    doc["meta"]["generated_at"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    name = os.path.join(outdir, "canon23_units_%s.json" % lang)
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
    print("canon23.py -- log_081 item 2: the fan-out condition "
          "tracer")

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

    workdir = tempfile.mkdtemp(prefix="canon23_asm_")

    totals = {"candidates_attempted": 0, "accepted": 0,
              "still_refused_after_attempt": 0,
              "no_candidate_at_all": 0}
    for lang in LANGS:
        doc = run_language(lang, indir, outdir, canon4_docs, sem_map,
                            tu3_map, workdir)
        for k in totals:
            totals[k] += doc["job2_fanout_tally"][k]

    print("TOTAL: %r" % totals)
    print("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
