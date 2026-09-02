#!/usr/bin/env python3
"""canon8.py -- JOB 1 driver: RE-ANCHOR THE BEHAVIOUR GATE TO GROUND
TRUTH, and re-adjudicate every unit canon7's OLD (stale-anchor) gate
refused.

Reads canon7_units_<lang>.json (canon7.py's own output) UNCHANGED as
its starting corpus -- this file does not re-render anything, it only
re-JUDGES the 242 units that already went through canon7's behaviour
gate (the ones with a `behaviour_gate` field: 241 DISPROVED-against-
old-text + 1 UNDECIDED-against-old-text), using canon8_behaviour_
check.reanchor_unit() (see that file's header for the fix and its
justification).

WHY ONLY THOSE 242, not all 974 not_yet_converged units: the other 732
never reached the OLD gate at all -- they refused earlier, for reasons
unrelated to the anchor (no tree_match2 record, an assembly failure,
"no return path" from the renderer itself). Re-anchoring the GATE
cannot change a verdict that was never gated; those 732 are JOB 2's
target (attacking the render failures themselves), not this file's.

usage:
  canon8.py [--in DIR] [--out DIR]
"""

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon8_behaviour_check as BC8                            # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]


def load_sem_map():
    sem_map = {}
    for lang in LANGS:
        path = os.path.join(HERE, "sem_anchored_spill_%s.json" % lang)
        sem_map[lang] = json.load(open(path))["units"]
    return sem_map


def run_language(lang, indir, outdir, canon4_docs, sem_map, flip_log):
    canon7_path = os.path.join(indir, "canon7_units_%s.json" % lang)
    canon7_doc = json.load(open(canon7_path))
    units = canon7_doc["units"]

    reanchored_count = 0
    accepted_count = 0
    kept_old_count = 0
    neither_matches_count = 0
    already_converged_reanchored = 0
    already_converged_still_ok = 0
    already_converged_now_fails = 0

    for n, u in units.items():
        if u.get("behaviour_gate") is None:
            continue
        reanchored_count += 1
        if u["status"] == "converged":
            # this unit's candidate was ALREADY WRITTEN as canon7_text
            # (accepted under the OLD anchor -- proved equal to
            # canon5_text). Re-check that accepted text against
            # ground truth too: the anchor changed, and a candidate
            # that only ever had to match a possibly-wrong old text
            # deserves the same scrutiny. This is BEYOND the brief's
            # literal "re-adjudicate refused units" but is the same
            # fix applied consistently -- see this file's own report
            # notes on scope.
            already_converged_reanchored += 1
            old_text = u["canon5_text"]
            candidate = u["canon7_text"]
            verdict = BC8.reanchor_unit(
                lang, n, canon4_docs, sem_map, old_text, candidate)
            u["job1_reanchor"] = verdict
            u["canon8_text"] = candidate
            if verdict["decision"] == "ACCEPT_CANDIDATE":
                already_converged_still_ok += 1
            else:
                already_converged_now_fails += 1
            u["job1_verdict_change_note"] = (
                "already-converged unit re-checked against ground "
                "truth -> %r" % verdict["decision"])
            continue
        old_text = u["canon7_text"]
        candidate = u.get("rejected_candidate_text")
        if candidate is None:
            # the 1 UNDECIDED-with-no-candidate case, if it occurs --
            # nothing to re-judge, record why and move on.
            u["job1_reanchor"] = {
                "decision": "NO_CANDIDATE -- behaviour_gate was set "
                    "but no rejected_candidate_text was recorded "
                    "(should not happen; flagged for review)",
            }
            continue
        verdict = BC8.reanchor_unit(
            lang, n, canon4_docs, sem_map, old_text, candidate)
        u["job1_reanchor"] = verdict
        old_status = u["status"]
        old_gt = u.get("ground_truth_check")
        if verdict["decision"] == "ACCEPT_CANDIDATE":
            u["canon8_text"] = candidate
            u["status"] = "converged"
            u["converged"] = True
            u["reason"] = "JOB 1 re-anchor: candidate proved equal " \
                "to the unit's own real ship code directly " \
                "(canon8_behaviour_check.anchored_check)"
            accepted_count += 1
        else:
            u["canon8_text"] = old_text
            kept_old_count += 1
            if "NEITHER" in verdict["decision"]:
                neither_matches_count += 1
        # verdict-change audit trail: did the OLD ground_truth_check
        # bucket (78/65/98 from canon7) predict this decision?
        u["job1_verdict_change_note"] = (
            "old_status=%r old_ground_truth_check=%r -> "
            "new_decision=%r" % (old_status, old_gt,
                                  verdict["decision"]))

    canon7_doc["job1_reanchor_tally"] = {
        "units_reanchored": reanchored_count,
        "previously_refused_reanchored": reanchored_count -
            already_converged_reanchored,
        "accepted_candidate": accepted_count,
        "kept_old_text": kept_old_count,
        "kept_old_neither_matches_ground_truth": neither_matches_count,
        "already_converged_units_rechecked": already_converged_reanchored,
        "already_converged_still_matches_ground_truth":
            already_converged_still_ok,
        "already_converged_NO_LONGER_matches_ground_truth":
            already_converged_now_fails,
    }
    canon7_doc["meta"] = dict(canon7_doc["meta"])
    canon7_doc["meta"]["generator"] = "canon8.py (JOB 1 re-anchor " \
        "pass over canon7_units_%s.json)" % lang
    canon7_doc["meta"]["generated_at"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    canon7_doc["meta"]["behaviour_gate_baseline"] = \
        "REPLACED (JOB 1): every re-adjudicated unit is now proved " \
        "against its OWN REAL SHIP CODE directly (canon4_units's " \
        "`mnem` field), not against a prior rendering -- see " \
        "canon8_behaviour_check.py's header."

    name = os.path.join(outdir, "canon8_units_%s.json" % lang)
    fh = open(name, "w")
    json.dump(canon7_doc, fh, indent=1)
    fh.close()
    print("wrote %s (%d re-anchored [%d previously-refused, %d "
          "already-converged], %d accepted, %d kept old "
          "[%d neither-matches]; of the already-converged: %d still "
          "match ground truth, %d no longer do)"
          % (name, reanchored_count,
             reanchored_count - already_converged_reanchored,
             already_converged_reanchored, accepted_count,
             kept_old_count, neither_matches_count,
             already_converged_still_ok, already_converged_now_fails))
    return canon7_doc


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
    print("canon8.py -- JOB 1: re-anchoring the behaviour gate to "
          "ground truth")

    canon4_docs = {}
    for lang in LANGS:
        canon4_docs[lang] = json.load(open(
            os.path.join(indir, "canon4_units_%s.json" % lang)
        ))["units"]

    sem_map = load_sem_map()

    flip_log = []
    totals = {"units_reanchored": 0,
              "previously_refused_reanchored": 0,
              "accepted_candidate": 0,
              "kept_old_text": 0,
              "kept_old_neither_matches_ground_truth": 0,
              "already_converged_units_rechecked": 0,
              "already_converged_still_matches_ground_truth": 0,
              "already_converged_NO_LONGER_matches_ground_truth": 0}
    for lang in LANGS:
        doc = run_language(lang, indir, outdir, canon4_docs, sem_map,
                            flip_log)
        for k in totals:
            totals[k] += doc["job1_reanchor_tally"][k]

    print("TOTAL: %r" % totals)
    print("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
