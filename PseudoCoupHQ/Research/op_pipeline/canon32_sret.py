#!/usr/bin/env python3
"""canon32_sret.py -- TASK 31 driver: the corpus survey for the
displaced (memory-return) ABI, the three-seat entry contract, the
canonical re-render, and the ground-truth-anchored gate.

WHAT IT DOES, in order:

  1. SURVEY. Runs `entry_contract3.detect_memory_return` over EVERY
     unit of all five compiled languages -- 1,779 units -- and tallies
     the reason each non-member fails, by test number. Nothing selects
     candidates by operator token, by result-type string, or by
     language: the four tests read the unit's own ship text and
     nothing else.
  2. GROUND-TRUTH CHECK. For every member, `canon4_units_<lang>.json`'s
     `mnem` is compared line by line against
     `op_units_<lang>.json`'s `probes[n]["ship"]["mnem"]`. A member
     whose two records disagree is refused, not gated.
  3. CONTRACT + RE-RENDER. The three-seat entry contract is built and
     the unit is erased to named field writes and re-rendered
     (`sret_render`).
  4. GATE. The re-rendered text is proved against the unit's OWN SHIP
     CODE by `sret_gate.check` -- answer register plus every cell of
     the answer image.

usage:
  canon32_sret.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import entry_contract3 as EC3          # noqa: E402
import sret_render                      # noqa: E402
import sret_gate                        # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]


def load(name):
    path = os.path.join(HERE, name)
    fh = open(path)
    doc = json.load(fh)
    fh.close()
    return doc


def survey():
    """(members, tally, totals) -- the computed corpus survey."""
    members = {}
    tally = {}
    totals = {}
    for lang in LANGS:
        units = load("canon4_units_%s.json" % lang)["units"]
        totals[lang] = len(units)
        for n, rec in units.items():
            mnem = rec.get("mnem") or []
            key = "%s/%s" % (lang, n)
            if not mnem:
                reason = "no-ship-mnemonic-recorded"
                tally[reason] = tally.get(reason, 0) + 1
                continue
            try:
                ok, evidence = EC3.detect_memory_return(mnem)
            except EC3.NotAnchorable as exc:
                reason = "shape-unrecognised"
                tally[reason] = tally.get(reason, 0) + 1
                del exc
                continue
            if not ok:
                reason = evidence["test"]
                tally[reason] = tally.get(reason, 0) + 1
                continue
            members[key] = {
                "lang": lang,
                "n": n,
                "destination_register": evidence["destination_register"],
                "store_offsets": [s["offset"]
                                  for s in evidence["stores"]],
                "store_widths_bits": [s["width_bits"]
                                      for s in evidence["stores"]],
                "declared_entry_contract_before":
                    rec.get("entry_contract"),
                "prior_refusal": rec.get("derive_refused"),
                "prior_status": rec.get("status"),
                "ship_mnem": mnem,
                "result_type_for_reading":
                    (rec.get("meta") or {}).get("result_type"),
                "operator": (rec.get("meta") or {}).get("operator"),
            }
    return members, tally, totals


def ground_truth_matches(lang, n, canon4_mnem):
    """(True, note) when canon4's `mnem` is line-identical to
    op_units' own ship mnemonic list for the same unit."""
    doc = load("op_units_%s.json" % lang)
    probes = doc.get("probes")
    if probes is None:
        return False, "op_units_%s.json carries no `probes`" % lang
    rec = probes.get(n)
    if rec is None:
        return False, "op_units_%s.json has no probe %s" % (lang, n)
    ship = rec.get("ship") or {}
    other = ship.get("mnem")
    if other is None:
        return False, "probe %s carries no ship mnemonic list" % n
    if list(other) != list(canon4_mnem):
        return False, ("canon4's `mnem` and op_units' ship `mnem` "
                       "DIFFER for %s/%s" % (lang, n))
    return True, ("canon4's `mnem` is line-identical to op_units' "
                  "own ship `mnem` (%d lines)" % len(other))


def run_member(key, row):
    lang = row["lang"]
    n = row["n"]
    ship = row["ship_mnem"]
    ok, note = ground_truth_matches(lang, n, ship)
    row["ground_truth_check"] = note
    if not ok:
        row["verdict"] = "REFUSED"
        row["detail"] = ("the ground-truth check failed: %s -- the "
                         "unit is not gated" % note)
        return row
    units = load("canon4_units_%s.json" % lang)["units"]
    meta = units[n].get("meta") or {}
    try:
        lines, erased, contract, evidence = \
            sret_render.canonical_text(lang, meta, ship)
    except (EC3.NotAnchorable, sret_render.NotRenderable) as exc:
        row["verdict"] = "REFUSED"
        row["detail"] = "the re-render refused: %s" % exc
        return row
    del evidence
    row["entry_contract_after"] = contract
    row["erased_form"] = erased
    row["canonical_text"] = lines
    row["candidate_differs_from_ship_text"] = (list(lines) !=
                                               list(ship))
    verdict, detail = sret_gate.check(ship, lines)
    row["verdict"] = verdict
    row["detail"] = detail
    return row


def main():
    members, tally, totals = survey()
    corpus = 0
    for lang in LANGS:
        corpus = corpus + totals[lang]
    print("SURVEY -- the four machine-form tests run over every unit "
          "of all five compiled languages")
    print("   corpus size: %d units (%s)"
          % (corpus, ", ".join("%s %d" % (L, totals[L])
                               for L in LANGS)))
    print("   members (all four tests hold): %d" % len(members))
    print("   non-members, by the test that refused them:")
    for reason in sorted(tally, key=lambda r: -tally[r]):
        print("      %-70s %d" % (reason, tally[reason]))
    total_non = 0
    for reason in tally:
        total_non = total_non + tally[reason]
    print("   breakdown adds up: %d non-members + %d members = %d"
          % (total_non, len(members), total_non + len(members)))
    print("")
    rows = {}
    counts = {}
    for key in sorted(members):
        row = run_member(key, members[key])
        rows[key] = row
        verdict = row["verdict"]
        counts[verdict] = counts.get(verdict, 0) + 1
        print("=" * 68)
        print("%s   [display label only: %r]" % (key, row["operator"]))
        print("  SHIP TEXT (ground truth):")
        for line in row["ship_mnem"]:
            print("      %s" % line)
        print("  %s" % row["ground_truth_check"])
        contract = row.get("entry_contract_after")
        if contract is not None:
            print("  ENTRY CONTRACT BEFORE (canon4's record): %r"
                  % row["declared_entry_contract_before"])
            print("  ENTRY CONTRACT AFTER (three seats, %s):"
                  % contract["abi"])
            for seat in contract["seats"]:
                print("      %-20s -> %%%-6s  (%s)"
                      % (seat["designation"], seat["register"],
                         seat["class"]))
            print("  EXIT CONTRACT: %s; %%%s holds %s"
                  % (contract["exit"]["answer"],
                     contract["exit"]["register"],
                     contract["exit"]["register_holds"]))
            print("  ERASED FORM:")
            for step in row["erased_form"]["steps"]:
                print("      store offset 0x%-3x width %-3d value %s"
                      % (step["offset"], step["width_bits"],
                         step["value"]))
            print("      exit adapter: result-destination -> "
                  "answer register")
            print("  CANONICAL TEXT (re-rendered):")
            for line in row["canonical_text"]:
                print("      %s" % line)
            print("  candidate differs from the ship text: %r"
                  % row["candidate_differs_from_ship_text"])
        print("  VERDICT: %s" % row["verdict"])
        print("  %s" % row["detail"])
    print("=" * 68)
    print("VERDICT TALLY: %r" % counts)
    doc = {
        "meta": {
            "produced_by": "canon32_sret.py",
            "role": "grouping artifact -- checked in full by "
                    "check_no_spelling_keys.py, no provenance "
                    "exemption claimed",
            "what": "the displaced-ABI (memory-return) family: the "
                    "three-seat entry contract, the erased form, the "
                    "canonical re-render, and the verdict against "
                    "each unit's own ship code",
            "membership_key": "machine form, four tests on the "
                              "unit's own ship text: one store base; "
                              "that base never written; that base "
                              "copied into the answer register; that "
                              "base never read as data",
            "corpus_units_surveyed": corpus,
            "member_count": len(members),
            "verdict_tally": counts,
            "non_member_reason_tally": tally,
        },
        "members": rows,
    }
    out = os.path.join(HERE, "canon32_sret_units.json")
    fh = open(out, "w")
    json.dump(doc, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()
    print("wrote canon32_sret_units.json -- %d members" % len(rows))
    survey_doc = {
        "meta": {
            "produced_by": "canon32_sret.py",
            "role": "grouping artifact -- checked in full by "
                    "check_no_spelling_keys.py, no provenance "
                    "exemption claimed",
            "what": "the computed corpus survey: how many units each "
                    "of the four machine-form tests refused",
            "corpus_units_surveyed": corpus,
            "per_language_units": totals,
            "member_count": len(members),
        },
        "non_member_reason_tally": tally,
        "member_keys": sorted(members),
    }
    out2 = os.path.join(HERE, "canon32_sret_survey.json")
    fh = open(out2, "w")
    json.dump(survey_doc, fh, indent=1, sort_keys=True)
    fh.write("\n")
    fh.close()
    print("wrote canon32_sret_survey.json")


if __name__ == "__main__":
    main()
