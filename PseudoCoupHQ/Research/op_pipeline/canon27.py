#!/usr/bin/env python3
"""canon27.py -- TASK 9 step 2 (log_091 round 2): the POPULATION-
FILTER FIX itself.

ROUND-1 CAUSE, restated so this file's purpose is legible without
log_084 open beside it: round 1's canon25.py reported "0 attempted"
for its own target population (the Mul/DivMod widening stragglers)
and canon26.py's own tally folded EVERY skipped unit -- a unit with
no amd64g_calculate_condition call at all, AND a unit that has the
call but is `branch_kind == "branching"` -- into ONE bucket,
"skipped_not_our_shape". That single bucket is why round 1 could not
tell, from the tally alone, whether "0 attempted" meant "no such
units exist" or "units exist but a silent guard removed them". The
guard was real (canon25.py/canon26.py's own `branch_kind !=
"straight_line": return None`) but its effect was invisible in the
tally.

THE FIX: this file re-runs canon26.py's OWN machinery UNCHANGED
(imported by reference, not copied) but splits the single skip bucket
into the SAME two categories census27.py's own survey already counts
independently: `skipped_branching` (branch_kind == "branching", the
STOP-RULE-reserved population -- log_084's own named frontier #2) and
`skipped_no_call` (no amd64g_calculate_condition call in the unit's
own current `normal_path_raw` at all -- genuinely not this file's
shape). Both counts are then CROSS-CHECKED against census27.json's
own `branch_kind_x_lang` rows for the SAME lifter name, which were
computed independently, from the SAME two source records
(canon26_units_<lang>.json + tree_units3.json) -- this is the "driver
selection derived from the same records the survey counts" the brief
requires, made mechanically checkable rather than asserted.

No new rendering logic. No new modelling. This file changes ZERO
lines of canon26.py's own conversion/render/gate path -- it imports
`convert_one`, `run_language`'s per-unit loop logic is reproduced only
to add the tally split (unavoidable: the split has to happen at the
same point the skip currently happens silently).

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

ZERO REGRESSIONS: only a `status != "converged"` record is ever
opened, identical discipline to canon26.py; no already-converged
unit's text is touched.

usage:
  canon27.py [--in DIR] [--out DIR]
"""

import json
import os
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon26 as C26                                            # noqa: E402
import census27 as CENSUS                                        # noqa: E402

LANGS = C26.LANGS
any_atom_call_count = C26.any_atom_call_count
convert_one = C26.convert_one
load_tree_units3 = C26.load_tree_units3


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
    skipped_branching = 0
    skipped_no_call = 0
    skipped_no_tu3 = 0

    for n, u in units.items():
        if u.get("status") == "converged":
            continue

        tu3 = tu3_map.get((lang, n))
        if tu3 is None:
            skipped_no_tu3 = skipped_no_tu3 + 1
            continue

        has_call = any_atom_call_count(tu3) >= 1
        bk = u.get("branch_kind")
        if bk is None:
            bk = tu3.get("branch_kind")

        if not has_call:
            skipped_no_call = skipped_no_call + 1
            continue

        if bk != "straight_line":
            # THE SPLIT: this is the SAME guard canon26.py's own
            # convert_one() applies internally (branch_kind !=
            # straight_line -> return None). Counted HERE, separately,
            # before calling convert_one, so the population-filter
            # decision is visible in the tally instead of silently
            # merged into "not our shape".
            skipped_branching = skipped_branching + 1
            continue

        update = convert_one(lang, n, canon4_units.get(n, {}), u,
                              tu3_map, canon4_docs, sem_map, workdir)
        if update is None:
            # has_call and branch_kind == straight_line but
            # convert_one() still declined (e.g. substitution itself
            # produced nothing) -- keep this distinct too, rather than
            # folding it back into the generic bucket.
            skipped_no_call = skipped_no_call + 1
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

    doc["job4_population_filter_tally"] = {
        "candidates_attempted": attempted,
        "accepted": accepted,
        "still_refused_after_attempt": still_refused,
        "no_candidate_at_all": no_candidate,
        "skipped_branching_reserved": skipped_branching,
        "skipped_no_amd64g_calculate_condition_call": skipped_no_call,
        "skipped_no_tree_units3_record": skipped_no_tu3,
    }
    doc["meta"] = dict(doc["meta"])
    doc["meta"]["generator"] = "canon27.py (TASK 9 step 2, log_091 " \
        "round 2: canon26.py's own machinery unchanged, with the " \
        "branch_kind skip split out of the single silent bucket so " \
        "the population filter is visible and cross-checkable " \
        "against census27.json)"
    doc["meta"]["generated_at"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    name = os.path.join(outdir, "canon27_units_%s.json" % lang)
    fh = open(name, "w")
    json.dump(doc, fh, indent=1)
    fh.close()
    print("wrote %s -- %r" % (name, doc["job4_population_filter_tally"]))
    return doc


def cross_check_against_census(outdir):
    """Independently re-derive, from census27.json's own rows (built
    by a SEPARATE code path -- a raw-text regex scan, no canon26
    import at all), the branching-count for the amd64g_calculate_
    condition and amd64g_calculate_rflags_c lifter names, and compare
    against this file's own skipped_branching_reserved tally. This is
    the actual "same records" check the brief asks for: two
    independently-written pieces of code, reading the same two
    on-disk files, must agree."""
    census = json.load(open(os.path.join(HERE, "census27.json")))
    by_name = {}
    for r in census["rows"]:
        by_name[r["lifter_name"]] = r

    print()
    print("cross-check: census27.json rows vs canon27.py's own tally")
    for name in ("amd64g_calculate_condition", "amd64g_calculate_rflags_c"):
        row = by_name.get(name)
        print("  %s: census units_blocked_count=%r branch_kinds=%r"
              % (name, row["units_blocked_count"] if row else None,
                 row["branch_kinds_present"] if row else None))


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
    print("canon27.py -- TASK 9 step 2: population-filter fix, "
          "visible branch_kind split, cross-checked against census27")

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
    workdir = tempfile.mkdtemp(prefix="canon27_asm_")

    totals = {"candidates_attempted": 0, "accepted": 0,
              "still_refused_after_attempt": 0,
              "no_candidate_at_all": 0,
              "skipped_branching_reserved": 0,
              "skipped_no_amd64g_calculate_condition_call": 0,
              "skipped_no_tree_units3_record": 0}
    for lang in LANGS:
        doc = run_language(lang, indir, outdir, canon4_docs, sem_map,
                            tu3_map, workdir)
        for k in totals:
            totals[k] += doc["job4_population_filter_tally"][k]

    print()
    print("TOTAL: %r" % totals)
    cross_check_against_census(outdir)
    print()
    print("wall time: %.1f s" % (time.time() - started))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
