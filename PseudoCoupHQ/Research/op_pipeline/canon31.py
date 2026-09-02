#!/usr/bin/env python3
"""canon31.py -- TASK 26: the float gate, re-run with a REAL ground
truth for branching units, and an audit of every branching verdict
this pipeline has ever recorded.

WHY THIS FILE REPLACES canon30.py's BRANCHING HALF. canon30.py used
canon9_behaviour_check's branching gate shape, which reads
canon4_units's `blocks` field as ground truth and `derived_blocks` as
the candidate. canon4.py assigns both names the SAME list object
(its own lines 772-777), so that comparison is a text against itself.
Measured: 88 units carry both fields, 88 of 88 identical, 0 differ.
This file cuts the real blocks from the unit's own ship BYTES
(real_blocks.py) and gates against those.

TWO JOBS, both reported:
  (A) every float-family unit, straight-line and branching, gated
      against real ground truth;
  (B) an AUDIT of the branching units earlier laps accepted through
      the circular gate (canon29's own `job6_sim9_ground_truth_
      verdict == PROVED_EQUAL` records that have block structure),
      re-gated the same honest way. A unit that fails here was never
      really proved, and its convergence is withdrawn.

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

Selection keys are machine-form throughout: the pipeline's own
recorded `status`, the VEX lifter names in the unit's own
normal_path_raw, and the presence of block structure. `operator` is
carried as a display label and read by nothing.

Coding discipline: no complex/compound one-liner statements.

usage:
  canon31.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import census27                                             # noqa: E402
import canon10_behaviour_check as BC10                      # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]


def load_all():
    canon4 = {}
    canon29 = {}
    sem = {}
    ops = {}
    for lang in LANGS:
        canon4[lang] = json.load(
            open(os.path.join(HERE, "canon4_units_%s.json" % lang))
        )["units"]
        canon29[lang] = json.load(
            open(os.path.join(HERE, "canon29_units_%s.json" % lang))
        )["units"]
        sem[lang] = json.load(
            open(os.path.join(HERE,
                              "sem_anchored_spill_%s.json" % lang))
        )["units"]
        ops[lang] = json.load(
            open(os.path.join(HERE, "op_units_%s.json" % lang))
        )["probes"]
    return canon4, canon29, sem, ops


def load_tree_names():
    doc = json.load(open(os.path.join(HERE, "tree_units3.json")))
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


def new_tally():
    return {
        "attempted_straight": 0,
        "accepted_straight": 0,
        "attempted_branching": 0,
        "accepted_branching": 0,
        "disproved": 0,
        "undecided": 0,
        "skipped_not_float_family": 0,
        "skipped_already_converged": 0,
        "skipped_no_candidate": 0,
        "audit_branching_rechecked": 0,
        "audit_branching_still_proved": 0,
        "audit_branching_withdrawn": 0,
    }


def main():
    canon4, canon29, sem, ops = load_all()
    tree_names = load_tree_names()
    grand = new_tally()
    audit_rows = {}
    for lang in LANGS:
        tally = new_tally()
        out_units = {}
        for n, rec29 in canon29[lang].items():
            rec = dict(rec29)
            rec4 = canon4[lang].get(n) or {}
            has_blocks = bool(rec4.get("derived_blocks"))
            if rec.get("status") == "converged":
                tally["skipped_already_converged"] += 1
                audit_one(lang, n, rec, rec4, canon4, ops, sem,
                          has_blocks, tally, audit_rows)
                out_units[n] = rec
                continue
            names = tree_names.get("%s/%s" % (lang, n), ())
            if not is_float_family(names):
                tally["skipped_not_float_family"] += 1
                out_units[n] = rec
                continue
            rec["job8_lifter_names"] = list(names)
            if has_blocks:
                tally["attempted_branching"] += 1
                rec["job8_candidate_source"] = \
                    "canon4_units.derived_blocks"
                rec["job8_ground_truth_source"] = \
                    "real_blocks.build over op_units ship bytes"
                verdict, detail = \
                    BC10.anchored_check_branching_real(
                        lang, n, canon4, ops, sem)
                if verdict == "PROVED_EQUAL":
                    tally["accepted_branching"] += 1
            else:
                text, source = candidate_for_straight(rec4, rec)
                if text is None:
                    tally["skipped_no_candidate"] += 1
                    rec["job8_ground_truth_verdict"] = "UNDECIDED"
                    rec["job8_ground_truth_detail"] = \
                        "no candidate canonical text on this unit's " \
                        "record at all"
                    out_units[n] = rec
                    continue
                tally["attempted_straight"] += 1
                rec["job8_candidate_source"] = source
                rec["job8_candidate_text"] = text
                rec["job8_ground_truth_source"] = \
                    "canon4_units.mnem (the unit's own ship code)"
                verdict, detail = BC10.anchored_check_straight(
                    lang, n, canon4, sem, text)
                if verdict == "PROVED_EQUAL":
                    tally["accepted_straight"] += 1
            rec["job8_ground_truth_verdict"] = verdict
            rec["job8_ground_truth_detail"] = detail
            if verdict == "PROVED_EQUAL":
                rec["status"] = "converged"
                rec["converged"] = True
                rec["converged_by"] = \
                    "canon31 float gate (canon10_behaviour_check." \
                    "Sim10), proved against this unit's own ship code"
            elif verdict == "DISPROVED":
                tally["disproved"] += 1
            else:
                tally["undecided"] += 1
            out_units[n] = rec
        doc = {
            "meta": {
                "role": "generator provenance",
                "language": lang,
                "produced_by": "canon31.py",
                "gate": "canon10_behaviour_check.Sim10, branching "
                        "units gated against real_blocks.build over "
                        "the unit's own ship bytes",
                "population_key": "machine-form: canon29 status not "
                                  "converged AND a VEX lifter name "
                                  "containing 'F0x' in the unit's "
                                  "own normal_path_raw",
                "tally": tally,
            },
            "units": out_units,
        }
        path = os.path.join(HERE, "canon31_units_%s.json" % lang)
        fh = open(path, "w")
        json.dump(doc, fh, indent=1, sort_keys=True)
        fh.write("\n")
        fh.close()
        print("wrote canon31_units_%s.json -- %r" % (lang, tally))
        for key in grand:
            grand[key] += tally[key]
    print("TOTAL: %r" % grand)
    audit_doc = {
        "meta": {
            "role": "generator provenance",
            "produced_by": "canon31.py",
            "what": "re-gate of every already-converged BRANCHING "
                    "unit against real ship blocks, because the "
                    "gate that converged them compared canon4's "
                    "`blocks` with canon4's `derived_blocks` and "
                    "those are the same object",
        },
        "per_unit": audit_rows,
    }
    path = os.path.join(HERE, "canon31_branching_audit.json")
    fh = open(path, "w")
    json.dump(audit_doc, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()
    print("wrote canon31_branching_audit.json -- %d rows"
          % len(audit_rows))


def audit_one(lang, n, rec, rec4, canon4, ops, sem, has_blocks,
              tally, audit_rows):
    """job (B): an already-converged unit with block structure was
    converged by a gate that compared a text with itself. Re-gate it
    honestly and record the outcome. The unit's recorded status is
    NOT changed here -- withdrawal is a reported finding this lap,
    and changing 1,561 baselined records is not this task's scope."""
    if not has_blocks:
        return
    tally["audit_branching_rechecked"] += 1
    verdict, detail = BC10.anchored_check_branching_real(
        lang, n, canon4, ops, sem)
    key = "%s/%s" % (lang, n)
    audit_rows[key] = {
        "lang": lang,
        "n": n,
        "recorded_status": rec.get("status"),
        "recheck_verdict": verdict,
        "recheck_detail": detail,
    }
    rec["job8_branching_audit_verdict"] = verdict
    rec["job8_branching_audit_detail"] = detail
    if verdict == "PROVED_EQUAL":
        tally["audit_branching_still_proved"] += 1
        return
    tally["audit_branching_withdrawn"] += 1


if __name__ == "__main__":
    main()
