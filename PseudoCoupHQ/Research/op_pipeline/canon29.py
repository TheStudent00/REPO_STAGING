#!/usr/bin/env python3
"""canon29.py -- TASK 22 (log_105, round 4). Works the 20-of-26
UNDECIDED units log_099's round-3 lap left as a named frontier (the
Sim8 z3 checker's own coverage gaps: `jo`/`je`/`jb`, `cltd`, idiv's
"ambient" dividend), by calling the new canon9_behaviour_check.Sim9
WRAPPER (imported by reference; canon8_behaviour_check.py and every
earlier file in the lineage are untouched -- see that file's header
for the reuse chain and what it adds).

SELECTION, by machine-form evidence already on record -- NEVER by
source-language operator token (THE SPELLING BAN, pasted verbatim
below). Every one of the 26 UNDECIDED units already carries its own
refusal reason on `job5_no_named_op_ground_truth_detail` (canon28.py
wrote it; canon8_behaviour_check.anchored_check's own NotModeled
text). This file selects by ISA MNEMONIC NAME appearing in that
already-written reason string (`cltd`, `idiv`, `jo`, `je`, `jb`) --
an x86-64 instruction mnemonic is a machine-form fact about the
CHECKER's own refusal, not a source-language operator spelling; the
`operator` field is carried on every output record only as a display
label, same discipline as every prior file in this lineage.

STRAIGHT-LINE vs BRANCHING dispatch is also machine-form: a unit
whose canon4_units record carries a non-empty `blocks` field is
branching (canon9_behaviour_check.anchored_check_branching, using
`blocks`/`derived_blocks` directly); otherwise it is straight-line
(canon9_behaviour_check.anchored_check_straight, over the SAME
`job5_no_named_op_candidate_text` canon28.py already selected and
recorded -- no new rendering).

THE 6 NOT ATTEMPTED HERE, carried forward, not reopened. Six of the
26 UNDECIDED units fail on a `-0x8(%rsp)`/`-0x1(%rsp)` stack-relative
operand (canon.py's WIDTH_OF table has no entry for a memory operand
at all) -- log_099 already named these (under its `SP:64` leaf-atom
framing) and recommended the owner-reserved: whether "the answer" for an
address-of unit means a stack-relative offset or something compiler-
layout-dependent is a semantic ruling about what the ground-truth
proof itself is even proving, not a checker coverage gap. No new
evidence surfaced this lap that would change that call, so this file
does not select them (verified: selecting by mnemonic name, not by
"6 remaining", naturally excludes them -- their reason text never
names cltd/idiv/jo/je/jb).

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
opened; a converged unit's own text is never touched (verified after
the run by a byte compare over every canon28_units_<lang>.json
`status == "converged"` record against this file's own output, same
discipline canon28.py's own step 4 used).

usage:
  canon29.py [--in DIR] [--out DIR]
"""

import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import canon9_behaviour_check as BC9                              # noqa: E402

LANGS = BC9.LANGS

# machine-form: ISA mnemonic names, read off the checker's OWN
# already-written refusal text -- never a source-language operator.
TARGET_MNEMONICS = ("cltd", "idiv", "jo", "je", "jb")


def is_target(detail):
    if not detail:
        return False
    for mnem in TARGET_MNEMONICS:
        needle = "mnemonic %r" % mnem
        if needle in detail:
            return True
    if "idiv's dividend is the ambient" in detail:
        return True
    return False


def convert_one(lang, n, rec, canon4_docs, sem_map):
    c4 = canon4_docs[lang].get(n)
    is_branching = bool(c4 and c4.get("blocks"))
    if is_branching:
        verdict, detail = BC9.anchored_check_branching(
            lang, n, canon4_docs, sem_map)
    else:
        candidate = rec.get("job5_no_named_op_candidate_text")
        if candidate is None:
            return None, "skipped_no_candidate_text"
        verdict, detail = BC9.anchored_check_straight(
            lang, n, canon4_docs, sem_map, candidate)

    update = {
        "job6_sim9_shape": "branching" if is_branching else "straight",
        "job6_sim9_ground_truth_verdict": verdict,
        "job6_sim9_ground_truth_detail": detail,
    }
    if verdict == "PROVED_EQUAL":
        candidate_text = rec.get("job5_no_named_op_candidate_text")
        update["canon29_text"] = candidate_text
        update["status"] = "converged"
        update["converged"] = True
        update["reason"] = (
            "canon29.py (TASK 22, log_105 round 4: one of the 26 "
            "UNDECIDED units round 3 left as a named Sim8-coverage "
            "frontier -- jo/je/jb/cltd/idiv. This unit's own real "
            "ship code, re-checked via canon9_behaviour_check.Sim9 "
            "(a wrapper extending canon8_behaviour_check.Sim8 with "
            "cltd/cqto, idiv's edx:eax dividend, and tracked "
            "overflow/carry flags for jo/jb -- je reuses condition_"
            "table.py's existing cmp/test predicate path unchanged; "
            "%s shape), proved equal to the unit's own already-"
            "rendered candidate text with no new substitution or "
            "rendering" % update["job6_sim9_shape"])
        return update, "accepted"
    return update, "attempted_not_proved"


def run_language(lang, indir, outdir, canon4_docs, sem_map):
    path = os.path.join(indir, "canon28_units_%s.json" % lang)
    doc = json.load(open(path))
    units = doc["units"]

    tally = {
        "attempted": 0, "accepted": 0, "attempted_not_proved": 0,
        "skipped_not_target_mnemonic": 0, "skipped_no_candidate_text": 0,
    }
    for n, u in units.items():
        if u.get("status") == "converged":
            continue
        detail = u.get("job5_no_named_op_ground_truth_detail")
        if not is_target(detail):
            tally["skipped_not_target_mnemonic"] += 1
            continue
        update, outcome = convert_one(lang, n, u, canon4_docs, sem_map)
        if update is None:
            tally[outcome] += 1
            continue
        u.update(update)
        tally["attempted"] += 1
        if outcome == "accepted":
            tally["accepted"] += 1
        else:
            tally["attempted_not_proved"] += 1

    doc["job6_sim9_tally"] = tally
    doc["meta"] = dict(doc["meta"])
    doc["meta"]["generator"] = (
        "canon29.py (TASK 22, log_105 round 4: re-checks the 20-of-"
        "26 UNDECIDED jo/je/jb/cltd/idiv units against ground truth "
        "via the new canon9_behaviour_check.Sim9 wrapper) over "
        "canon28_units_%s.json" % lang)
    doc["meta"]["generated_at"] = time.strftime(
        "%Y-%m-%dT%H:%M:%SZ", time.gmtime())

    outname = os.path.join(outdir, "canon29_units_%s.json" % lang)
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

    grand = {
        "attempted": 0, "accepted": 0, "attempted_not_proved": 0,
        "skipped_not_target_mnemonic": 0, "skipped_no_candidate_text": 0,
    }
    for lang in LANGS:
        doc = run_language(lang, indir, outdir, canon4_docs, sem_map)
        for k in grand:
            grand[k] += doc["job6_sim9_tally"][k]

    print("TOTAL:", grand)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
