#!/usr/bin/env python3
"""canon30.py -- TASK 26 (log_109 round 5) driver: gate the FLOAT
FAMILY against each unit's OWN SHIP CODE, using canon10_behaviour_
check.Sim10.

POPULATION SELECTION -- machine-form, no operator token. A unit is in
this lap's population when BOTH hold:

  (1) canon29_units_<lang>.json's own `status` is not "converged"
      (the current baseline of record, 1,561 converged of 1,779), and
  (2) census27.names_from_raw over tree_units3.json's own
      `normal_path_raw` finds at least one VEX lifter name containing
      "F0x" -- the packed-float SIMD op names (Add32F0x4, Sub64F0x2,
      Div32F0x4, CmpEQ64F0x2, ...).

Both keys are machine-form: (1) is the pipeline's own recorded status,
(2) is a lifter name emitted by pyvex about the unit's own bytes. The
`operator` field is carried on the output records as a DISPLAY LABEL
only and is never read by any selection, grouping or comparison in
this file. Each unit is gated ALONE against its own ship code -- this
file never pairs two units with each other.

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

WHICH TEXT IS GATED. For a straight-line unit, the unit's own newest
CANONICAL TEXT on its record, in this order of preference:
canon7_text, canon5_text, canon4_text, then the joined `derived_text`
list -- the field actually used is recorded per unit
(`job7_candidate_source`), never left implicit. For a branching unit,
canon4_units_<lang>.json's own `derived_blocks` against its own
`blocks`, the same pairing canon29 used.

ZERO REGRESSIONS. Every unit already `converged` in canon29 is copied
through byte-identically; this file only ever changes a unit that was
NOT converged. The check is run and printed by
canon30_zero_regression.py, not asserted here.

Coding discipline (the owner's ruling): no complex/compound one-liner
statements.

usage:
  canon30.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import census27                                             # noqa: E402
import canon10_behaviour_check as BC10                      # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]


def load_docs():
    canon4_docs = {}
    canon29_docs = {}
    sem_docs = {}
    for lang in LANGS:
        p4 = os.path.join(HERE, "canon4_units_%s.json" % lang)
        canon4_docs[lang] = json.load(open(p4))["units"]
        p29 = os.path.join(HERE, "canon29_units_%s.json" % lang)
        canon29_docs[lang] = json.load(open(p29))["units"]
        ps = os.path.join(HERE, "sem_anchored_spill_%s.json" % lang)
        sem_docs[lang] = json.load(open(ps))["units"]
    return canon4_docs, canon29_docs, sem_docs


def load_tree_names():
    """unit key -> tuple of machine-form lifter names found in that
    unit's OWN normal_path_raw."""
    path = os.path.join(HERE, "tree_units3.json")
    doc = json.load(open(path))
    out = {}
    for rec in doc["units"]:
        key = "%s/%s" % (rec["lang"], rec["n"])
        raw = rec.get("normal_path_raw") or ""
        out[key] = tuple(sorted(census27.names_from_raw(raw)))
    return out


def is_float_family(names):
    for name in names:
        if "F0x" in name:
            return True
    return False


def candidate_for_straight(rec4, rec29):
    for field in ("canon7_text", "canon5_text", "canon4_text"):
        text = rec29.get(field)
        if isinstance(text, str) and text.strip() != "":
            return text, field
    derived = rec4.get("derived_text")
    if isinstance(derived, list) and derived:
        return "; ".join(derived), "canon4_units.derived_text"
    return None, None


def main():
    canon4_docs, canon29_docs, sem_docs = load_docs()
    tree_names = load_tree_names()
    grand = {
        "attempted": 0,
        "accepted": 0,
        "attempted_not_proved": 0,
        "disproved": 0,
        "skipped_not_float_family": 0,
        "skipped_already_converged": 0,
        "skipped_no_candidate": 0,
    }
    for lang in LANGS:
        tally = {
            "attempted": 0,
            "accepted": 0,
            "attempted_not_proved": 0,
            "disproved": 0,
            "skipped_not_float_family": 0,
            "skipped_already_converged": 0,
            "skipped_no_candidate": 0,
        }
        out_units = {}
        for n, rec29 in canon29_docs[lang].items():
            rec = dict(rec29)
            if rec.get("status") == "converged":
                tally["skipped_already_converged"] += 1
                out_units[n] = rec
                continue
            names = tree_names.get("%s/%s" % (lang, n), ())
            if not is_float_family(names):
                tally["skipped_not_float_family"] += 1
                out_units[n] = rec
                continue
            rec4 = canon4_docs[lang].get(n) or {}
            rec["job7_lifter_names"] = list(names)
            has_blocks = bool(rec4.get("derived_blocks"))
            if has_blocks:
                rec["job7_candidate_source"] = \
                    "canon4_units.derived_blocks"
                verdict, detail = BC10.anchored_check_branching(
                    lang, n, canon4_docs, sem_docs)
            else:
                text, source = candidate_for_straight(rec4, rec29)
                if text is None:
                    tally["skipped_no_candidate"] += 1
                    rec["job7_float_ground_truth_verdict"] = \
                        "UNDECIDED"
                    rec["job7_float_ground_truth_detail"] = \
                        "no candidate canonical text on this " \
                        "unit's record at all"
                    out_units[n] = rec
                    continue
                rec["job7_candidate_source"] = source
                rec["job7_candidate_text"] = text
                verdict, detail = BC10.anchored_check_straight(
                    lang, n, canon4_docs, sem_docs, text)
            tally["attempted"] += 1
            rec["job7_float_ground_truth_verdict"] = verdict
            rec["job7_float_ground_truth_detail"] = detail
            if verdict == "PROVED_EQUAL":
                tally["accepted"] += 1
                rec["status"] = "converged"
                rec["converged"] = True
                rec["converged_by"] = "canon30 float gate " \
                    "(canon10_behaviour_check.Sim10), proved " \
                    "against this unit's own ship code"
            else:
                tally["attempted_not_proved"] += 1
                if verdict == "DISPROVED":
                    tally["disproved"] += 1
            out_units[n] = rec
        doc = {
            "meta": {
                "role": "generator provenance",
                "language": lang,
                "produced_by": "canon30.py",
                "gate": "canon10_behaviour_check.Sim10 -- float "
                        "vocabulary as uninterpreted functions, "
                        "lane/copy/spill structure exact",
                "population_key": "machine-form: canon29 status not "
                                  "converged AND a VEX lifter name "
                                  "containing 'F0x' in the unit's "
                                  "own normal_path_raw",
                "tally": tally,
            },
            "units": out_units,
        }
        out_path = os.path.join(HERE, "canon30_units_%s.json" % lang)
        fh = open(out_path, "w")
        json.dump(doc, fh, indent=1, sort_keys=True)
        fh.write("\n")
        fh.close()
        print("wrote canon30_units_%s.json -- %r" % (lang, tally))
        for key in grand:
            grand[key] += tally[key]
    print("TOTAL: %r" % grand)


if __name__ == "__main__":
    main()
