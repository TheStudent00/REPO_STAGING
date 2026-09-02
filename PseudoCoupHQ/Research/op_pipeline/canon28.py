#!/usr/bin/env python3
"""canon28.py -- TASK 15 (log_097 round 3), working the top-ranked
bucket of log_093's fresh census (`__no_named_op_found__`, 126 units)
by its OWN diagnosed sub-shape, not the bucket in general.

log_093 split that bucket into three: 104 units with `status ==
"unchanged"` and NO reason field at all (NEVER ATTEMPTED by any
driver in the canon17..canon27 lineage), 16 units refused upstream at
canon4's own erasure step ("too many distinct join paths" -- a
different pipeline stage's shape, out of scope here), and 6 units
carrying a `leaf atom 'SP:64'` refusal (a stack-pointer read, also a
different shape). This file works ONLY the 104.

WHY THE 104 WERE NEVER ATTEMPTED (read this lap, canon26.py in full):
every driver from canon17 through canon27 gates its OWN target shape
by `any_atom_call_count(tu3_unit) < 1: return None` (canon26.py
`build_fixed_unit`) or an equivalent float-family check -- i.e. every
driver in this lineage ONLY ever attempts units that need an
amd64g_calculate_condition or float-family SUBSTITUTION first. A unit
that needs NO substitution at all (its `canon7_text` is already the
final candidate -- e.g. `c/op_7`, `~a` -> `mov %rdi,%rax; not %rax;
ret`) was never selected by ANY driver's shape filter, so it was never
run through the behaviour gate either -- not because it is hard, it
is the SIMPLEST population in the whole 322 (bare unary ops, bare
literal constants, bare `in0` identity passthroughs), but because no
driver's population filter ever included "no substitution needed" as
a target shape.

THE FIX, mechanical, following existing precedent exactly: this file
selects the 104-shaped population the SAME way census27.py already
does (zero amd64g_calculate_condition / float-family / wide-op names
literally present in the unit's OWN `tree_units3.json`
`normal_path_raw`, via `census27.names_from_raw` imported unchanged),
and for each one, runs the SAME re-anchored gate every later driver in
this lineage already uses (`canon8_behaviour_check.anchored_check`,
imported unchanged, function reference not copy -- the same gate
canon27's own `job1_reanchor` calls) directly against the unit's own
newest already-rendered text (`canon7_text`, falling back to
`canon5_text`/`canon4_text` if absent), with NO new substitution, NO
new rendering, NO new modelling. If PROVED_EQUAL, the unit converges;
otherwise its per-unit verdict is recorded and it stays open.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim."

Candidate selection here is by LIFTER-NAME ABSENCE (a machine-form
fact about `normal_path_raw`) and by `status`/`reason` fields (also
machine-form) -- never by the source-language operator token; the
`operator` field is carried only as a per-unit display label, same
discipline as every prior file in this lineage.

ZERO REGRESSIONS: only a `status != "converged"` record is ever
opened; a converged unit's own text is never touched.

usage:
  canon28.py [--in DIR] [--out DIR]
"""

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import census27 as CENSUS27                                      # noqa: E402
import canon8_behaviour_check as BC8                              # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]


def candidate_text_of(rec):
    """the newest already-rendered text on this record, in the same
    latest-first order every prior file in this lineage prefers --
    canon7_text is the newest stage that runs unconditionally for
    every unit (canon5/canon6/canon7 apply to the whole population,
    not to a substitution-gated subset); canon5_text/canon4_text are
    the fallbacks for the rare record missing it."""
    for key in ("canon7_text", "canon5_text", "canon4_text"):
        v = rec.get(key)
        if v:
            return v, key
    return None, None


def convert_one(lang, n, rec, tu3_map, canon4_docs, sem_map):
    tu3 = tu3_map.get((lang, n))
    if tu3 is None:
        return None, "skipped_no_tree_units3_record"
    raw = tu3.get("normal_path_raw")
    if raw is None:
        return None, "skipped_no_tree_units3_record"
    if CENSUS27.names_from_raw(raw):
        return None, "skipped_has_named_op"  # not this file's shape

    candidate, source_field = candidate_text_of(rec)
    if candidate is None:
        return None, "skipped_no_candidate_text"

    verdict, detail = BC8.anchored_check(
        lang, n, canon4_docs, sem_map, candidate)

    update = {
        "job5_no_named_op_source_field": source_field,
        "job5_no_named_op_candidate_text": candidate,
        "job5_no_named_op_ground_truth_verdict": verdict,
        "job5_no_named_op_ground_truth_detail": detail,
    }
    if verdict == "PROVED_EQUAL":
        update["canon28_text"] = candidate
        update["status"] = "converged"
        update["converged"] = True
        update["reason"] = (
            "canon28.py (TASK 15, log_097 round 3: the "
            "'__no_named_op_found__' 104-unit 'unchanged'/never-"
            "attempted sub-shape -- no driver in the canon17..canon27 "
            "lineage ever selected units needing zero "
            "amd64g_calculate_condition/float-family substitution; "
            "this file runs the SAME re-anchored gate "
            "(canon8_behaviour_check.anchored_check, imported "
            "unchanged) directly against the unit's own already-"
            "rendered %s with no new substitution/rendering/"
            "modelling): candidate proved equal to the unit's own "
            "real ship code directly" % source_field)
        return update, "accepted"
    return update, "attempted_not_proved"


def run_language(lang, indir, outdir, canon4_docs, sem_map, tu3_map):
    path = os.path.join(indir, "canon27_units_%s.json" % lang)
    doc = json.load(open(path))
    units = doc["units"]

    tally = {
        "attempted": 0, "accepted": 0, "attempted_not_proved": 0,
        "skipped_has_named_op": 0, "skipped_no_candidate_text": 0,
        "skipped_no_tree_units3_record": 0,
    }
    for n, u in units.items():
        if u.get("status") == "converged":
            continue
        update, outcome = convert_one(
            lang, n, u, tu3_map, canon4_docs, sem_map)
        if update is None:
            tally[outcome] += 1
            continue
        u.update(update)
        tally["attempted"] += 1
        if outcome == "accepted":
            tally["accepted"] += 1
        else:
            tally["attempted_not_proved"] += 1

    doc["job5_no_named_op_tally"] = tally
    doc["meta"] = dict(doc["meta"])
    doc["meta"]["generator"] = (
        "canon28.py (TASK 15, log_097 round 3: gates the "
        "__no_named_op_found__ 'unchanged'/never-attempted 104-unit "
        "sub-shape directly against ground truth, no substitution) "
        "over canon27_units_%s.json" % lang)
    doc["meta"]["generated_at"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    outname = os.path.join(outdir, "canon28_units_%s.json" % lang)
    fh = open(outname, "w")
    json.dump(doc, fh, indent=1)
    fh.close()
    print("wrote %s -- %r" % (outname, tally))
    return doc


def main(argv):
    indir = HERE
    outdir = HERE
    i = 1
    while i < len(argv):
        if argv[i] == "--in":
            indir = argv[i + 1]
            i += 2
            continue
        if argv[i] == "--out":
            outdir = argv[i + 1]
            i += 2
            continue
        print(__doc__)
        return 2

    canon4_docs = {}
    for lang in LANGS:
        canon4_docs[lang] = json.load(open(
            os.path.join(indir, "canon4_units_%s.json" % lang)
        ))["units"]

    sem_map = {}
    for lang in LANGS:
        p = os.path.join(indir, "sem_anchored_spill_%s.json" % lang)
        sem_map[lang] = json.load(open(p))["units"]

    tu3_map = CENSUS27.load_tree_units3()

    grand = {
        "attempted": 0, "accepted": 0, "attempted_not_proved": 0,
        "skipped_has_named_op": 0, "skipped_no_candidate_text": 0,
        "skipped_no_tree_units3_record": 0,
    }
    for lang in LANGS:
        doc = run_language(lang, indir, outdir, canon4_docs, sem_map,
                            tu3_map)
        for k in grand:
            grand[k] += doc["job5_no_named_op_tally"][k]

    print("TOTAL:", grand)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
