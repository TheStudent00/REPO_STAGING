#!/usr/bin/env python3
"""canon25.py -- log_084 lap, item 2 of the coordinator's "jobs 1 and
3 are mechanical, do them now" instruction: re-wires canon12_
normalize.py's EXISTING widening-arithmetic model (WIDE_MUL_OPS =
{Mul64, Mul32}, WIDE_DIVMOD_OPS = {DivModS128to64, DivModU128to64} --
written for STAGE 2 / canon12.py, proved on the bulk of this family
already) to the CURRENT tree_units3.json baseline, the same
adoption pattern canon24.py used to re-point condition_table4's
float-packed-flags model at raw text sourced from tree_units3 instead
of the old tu2 convention.

MEASURED TARGET (survey, log_084's own script, reproduced here): 14
not-yet-converged units, over canon24_units_<lang>.json (the newest
baseline on disk), whose OWN normal_path_raw (read from
tree_units3.json, the adopted baseline) contains a raw Mul32/Mul64/
DivModS128to64/DivModU128to64 call:

    Mul32: 1 (swift/op_114)
    Mul64: 1 (swift/op_121)
    DivModS128to64: 6 (go)
    DivModU128to64: 6 (go)

NO NEW MODEL IS WRITTEN HERE. canon12_normalize.normalize_v2 (the z3
wide-bitvector model) and canon12_render.render_unit12 (the %rax/
%rdx-pinned idiv/div codegen) are called UNCHANGED, function
reference, not copied -- identical reuse discipline to canon12_
render.py's own header ("canon7_render.py nor canon11_render.py's own
source is edited"). The only new code in this file is the driver
plumbing: read canon24_units_<lang>.json, re-source normal_path_raw
from tree_units3.json (the CURRENT baseline, replacing canon12.py's
own tu2_map), skip the CAUSE-1 condition substitution step (measured,
this lap: none of the 14 target units carry an amd64g_calculate_
condition call alongside the wide-arithmetic call, so condition_
table2's OLD, tu2-shaped substitution machinery is never invoked --
correct-by-construction, not a guess), run normalize_v2 + render_
unit12 + wide_anchored_check, and write canon25_units_<lang>.json.

ZERO REGRESSIONS: only a `status != "converged"` record is ever
opened -- identical discipline to canon24.py; an already-converged
unit's own text is never touched by this file.

usage:
  canon25.py [--in DIR] [--out DIR]
"""

import json
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon12_normalize as C12N                                 # noqa: E402
import canon12_render as R12                                     # noqa: E402
import canon12_behaviour_check as BC10                            # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]

WIDE_NAMES = (
    "Mul32(", "Mul64(", "DivModS128to64(", "DivModU128to64(")

render_unit12 = R12.render_unit12
wide_anchored_check = BC10.wide_anchored_check


def load_tree_units3():
    path = os.path.join(HERE, "tree_units3.json")
    doc = json.load(open(path))
    out = {}
    for u in doc["units"]:
        out[(u["lang"], u["n"])] = u
    return out


def is_our_shape(raw_text):
    if raw_text is None:
        return False
    for name in WIDE_NAMES:
        if name in raw_text:
            return True
    return False


def convert_one(lang, n, old_rec, tu3_rec, canon4_docs, sem_map,
                 workdir):
    if old_rec.get("branch_kind") != "straight_line":
        return None
    if tu3_rec is None:
        return None
    raw = tu3_rec.get("normal_path_raw")
    if tu3_rec.get("sem_ok") is False or raw is None:
        return None
    if not is_our_shape(raw):
        return None
    if "amd64g_calculate_condition" in raw:
        # measured, this lap: none of the 14-unit target population
        # combines a condition call with a wide-arithmetic call --
        # refuse honestly rather than invoke the OLD tu2-shaped
        # condition_table2 substitution against a tree_units3-shaped
        # raw text it was never proved against.
        return {
            "job2_widerewire_candidate_text": None,
            "job2_widerewire_refusal_reason":
                "raw text also carries an amd64g_calculate_condition "
                "call -- out of this file's measured/proved scope "
                "(see file header); not attempted",
        }

    norm, ok, note = C12N.normalize_v2(raw)
    if not ok:
        return {
            "job2_widerewire_candidate_text": None,
            "job2_widerewire_refusal_reason":
                "z3 failed to normalize this unit's own raw text "
                "under canon12_normalize's wide-arithmetic model "
                "(%s)" % note,
        }

    fixed_unit = dict(
        lang=lang, n=n, sem_ok=True,
        normal_path_root=norm, normalize_ok=True,
        normal_path_raw=raw)

    result, ctxd = render_unit12(fixed_unit, workdir)
    if not isinstance(result, list):
        return {
            "job2_widerewire_normalized_root": norm,
            "job2_widerewire_candidate_text": None,
            "job2_widerewire_refusal_reason": result,
        }

    candidate = "; ".join(result)

    verdict, detail = wide_anchored_check(
        lang, n, canon4_docs, sem_map, candidate)

    update = {
        "job2_widerewire_normalized_root": norm,
        "job2_widerewire_candidate_text": candidate,
        "job2_widerewire_ground_truth_verdict": verdict,
        "job2_widerewire_ground_truth_detail": detail,
    }
    if verdict == "PROVED_EQUAL":
        update["canon25_text"] = candidate
        update["status"] = "converged"
        update["converged"] = True
        update["reason"] = "canon25.py (log_084 lap, item 2: re-" \
            "wiring canon12_normalize.py's own proved widening-" \
            "arithmetic model -- Mul32/Mul64/DivModS128to64/" \
            "DivModU128to64 -- to the current tree_units3.json " \
            "baseline): candidate proved bit-level equal to the " \
            "unit's own real ship code directly"
        return update

    update["job2_widerewire_decision"] = "KEEP_OLD -- %s: %s" % (
        verdict, detail[:200])
    return update


def run_language(lang, indir, outdir, canon4_docs, sem_map, tu3_map,
                  workdir):
    canon24_path = os.path.join(indir, "canon24_units_%s.json" % lang)
    doc = json.load(open(canon24_path))
    units = doc["units"]

    attempted = 0
    accepted = 0
    disproved = 0
    undecided = 0
    no_candidate = 0
    skipped_not_our_shape = 0

    for n, u in units.items():
        if u.get("status") == "converged":
            continue
        tu3 = tu3_map.get((lang, n))
        update = convert_one(lang, n, u, tu3, canon4_docs, sem_map,
                              workdir)
        if update is None:
            skipped_not_our_shape = skipped_not_our_shape + 1
            continue
        u.update(update)
        if update.get("job2_widerewire_candidate_text") is None:
            no_candidate = no_candidate + 1
            continue
        attempted = attempted + 1
        if update.get("status") == "converged":
            accepted = accepted + 1
        elif update.get(
                "job2_widerewire_ground_truth_verdict") == \
                "DISPROVED":
            disproved = disproved + 1
        else:
            undecided = undecided + 1

    doc["job2_widerewire_tally"] = {
        "candidates_attempted": attempted,
        "accepted": accepted,
        "disproved": disproved,
        "undecided": undecided,
        "no_candidate_at_all": no_candidate,
    }
    doc["meta"] = dict(doc["meta"])
    doc["meta"]["generator"] = "canon25.py (log_084 lap, item 2: " \
        "re-wire canon12_normalize's widening model to the current " \
        "tree_units3.json baseline) over canon24_units_%s.json" % \
        lang
    doc["meta"]["generated_at"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    name = os.path.join(outdir, "canon25_units_%s.json" % lang)
    fh = open(name, "w")
    json.dump(doc, fh, indent=1)
    fh.close()
    print("wrote %s (%d attempted, %d accepted, %d disproved, %d "
          "undecided, %d no candidate, %d not our shape)"
          % (name, attempted, accepted, disproved, undecided,
             no_candidate, skipped_not_our_shape))
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
    print("canon25.py -- log_084 item 2: re-wire canon12_normalize's "
          "widening model to the current baseline")

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

    workdir = tempfile.mkdtemp(prefix="canon25_asm_")

    totals = {"candidates_attempted": 0, "accepted": 0,
              "disproved": 0, "undecided": 0,
              "no_candidate_at_all": 0}
    for lang in LANGS:
        doc = run_language(lang, indir, outdir, canon4_docs, sem_map,
                            tu3_map, workdir)
        for k in totals:
            totals[k] += doc["job2_widerewire_tally"][k]

    print("TOTAL: %r" % totals)
    print("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
