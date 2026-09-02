#!/usr/bin/env python3
"""canon35_zero_regression.py -- TASK 39: zero regression, IN THE
RULED SENSE, computed from disk.

WHAT "ZERO REGRESSION" MEANS HERE, quoted from the round-8 brief
(log_129) because it is the binding definition and it is NOT the usual
one: "the universal-form texts REPLACE the register-first texts as the
canonical column, so 'zero regressions' there means no unit loses its
PROVED status and no class loses members without a named, proved
cause -- text change is the point, not a regression".

So this file computes three things and refuses to average any of them:

  A.  THE STANDING CONVERGED COUNT BEFORE, recomputed from disk, not
      read from any report: canon31_units_<lang>.json `status`, with
      canon31's own branching audit withdrawing a unit whose
      `job8_branching_audit_verdict` is present and is not
      PROVED_EQUAL, canon33_units.json's `newly_converged` folded in,
      and canon32_sret_units.json's five displaced-ABI members folded
      in.  Each population is printed with its per-language
      breakdown.

  B.  THE CROSS-TAB, recorded status x universal-form outcome, every
      cell.  A "regression" is exactly one cell family: a unit that
      was converged (or a proved sret member) and now carries no
      universal text.  Every such unit is named, with its recorded
      cause verbatim.

  C.  THE UNTOUCHED ARTIFACTS.  dominant_table24.json and the round-7
      interpreter artifacts must be byte-identical to what they were
      before this lap.  Their sha256 is computed here and printed; the
      report pastes it beside the value recorded in log_124/log_119 so
      a later reader can check the claim rather than trust it.

Coding discipline: no complex/compound one-liner statements.

usage:
  canon35_zero_regression.py
"""

import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]
OUT = os.path.join(HERE, "canon35_zero_regression.json")

WATCHED = [
    "dominant_table24.json", "dom_ops22.json",
    "dominant_table24b.json", "dom_ops22b.json",
    "interp_canon35.json", "interp_table2.json", "interp_join2.json",
    "union_table2.json",
    "canon31_units_c.json", "canon31_units_cpp.json",
    "canon31_units_go.json", "canon31_units_rust.json",
    "canon31_units_swift.json",
    "canon32_sret_units.json", "canon33_units.json",
    "canon33_arrival_modes.json",
]


def load(name):
    return json.load(open(os.path.join(HERE, name)))


def sha256_of(name):
    path = os.path.join(HERE, name)
    digest = hashlib.sha256()
    fh = open(path, "rb")
    digest.update(fh.read())
    fh.close()
    return digest.hexdigest()


def standing_status():
    """label -> the standing status BEFORE this lap, from disk."""
    c33 = load("canon33_units.json")["units"]
    sret = set(load("canon32_sret_units.json")["members"])
    out = {}
    for lang in LANGS:
        units = load("canon31_units_%s.json" % lang)["units"]
        for n, rec in units.items():
            label = "%s/op_%s" % (lang, n)
            status = rec.get("status")
            audit = rec.get("job8_branching_audit_verdict")
            if status == "converged":
                if audit is not None:
                    if audit != "PROVED_EQUAL":
                        status = "withdrawn"
            newer = c33.get(label)
            if newer is not None:
                if newer.get("outcome") == "newly_converged":
                    status = "converged"
            if "%s/%s" % (lang, n) in sret:
                status = "converged (displaced ABI)"
            out[label] = status
    return out


def main():
    before = standing_status()
    after = {}
    causes = {}
    per_language = {}
    for lang in LANGS:
        doc = load("canon35_universal_%s.json" % lang)["units"]
        counts = {}
        for label, rec in doc.items():
            after[label] = rec["outcome"]
            reason = rec.get("refusal")
            if reason is None:
                reason = rec.get("gate_detail")
            causes[label] = reason
            key = rec["outcome"]
            counts[key] = counts.get(key, 0) + 1
        per_language[lang] = counts

    before_counts = {}
    for label in before:
        key = before[label]
        before_counts[key] = before_counts.get(key, 0) + 1

    before_per_language = {}
    for label in before:
        lang = label.split("/")[0]
        bucket = before_per_language.setdefault(lang, {})
        key = before[label]
        bucket[key] = bucket.get(key, 0) + 1

    cross = {}
    for label in sorted(before):
        key = "%s -> %s" % (before[label], after.get(label))
        cross[key] = cross.get(key, 0) + 1

    lost = []
    gained = []
    for label in sorted(before):
        was_proved = before[label].startswith("converged")
        now_proved = after.get(label) == "UNIVERSAL_TEXT_PROVED"
        if was_proved and not now_proved:
            lost.append({
                "unit": label,
                "status_before": before[label],
                "outcome_after": after.get(label),
                "named_cause": causes.get(label),
            })
        if not was_proved and now_proved:
            gained.append({
                "unit": label,
                "status_before": before[label],
            })

    # D. THE CONVERGED COUNT UNDER THE UNIVERSAL FORM, and the units
    # that carry a text but are NOT converged.  A unit is converged
    # when its canonical text is proved against its OWN SHIP CODE.  A
    # universal text admitted by gate 1 inherits that standing from
    # the prior text it was proved equal to -- so a unit whose prior
    # text never had a ship proof (or had one withdrawn) does NOT
    # become converged by gaining a universal text.  It is counted
    # separately, by name, and never folded into the headline.
    converged_after = []
    text_without_a_ship_proof = []
    ship_docs = {}
    for lang in LANGS:
        ship_docs.update(load("canon35_universal_%s.json" % lang)
                         ["units"])
    for label in sorted(before):
        record = ship_docs.get(label) or {}
        if record.get("outcome") != "UNIVERSAL_TEXT_PROVED":
            continue
        if before[label].startswith("converged"):
            converged_after.append(label)
            continue
        if record.get("ship_gate_verdict") == "PROVED_EQUAL":
            converged_after.append(label)
            continue
        text_without_a_ship_proof.append({
            "unit": label,
            "status_before": before[label],
            "ship_gate_verdict": record.get("ship_gate_verdict"),
            "ship_gate_detail": record.get("ship_gate_detail"),
        })

    watched = {}
    for name in WATCHED:
        watched[name] = sha256_of(name)

    doc = {
        "meta": {
            "produced_by": "canon35_zero_regression.py",
            "role": "generator provenance",
            "definition_of_zero_regression":
                "log_129: no unit loses its PROVED status and no class "
                "loses members without a named, proved cause; the text "
                "change is the point, not a regression",
        },
        "population": len(before),
        "standing_before": before_counts,
        "standing_before_per_language": before_per_language,
        "universal_after": per_language,
        "cross_tab": cross,
        "lost_proved_status": lost,
        "gained_proved_status_count": len(gained),
        "gained_proved_status": gained,
        "converged_under_the_universal_form": len(converged_after),
        "converged_under_the_universal_form_units": converged_after,
        "text_without_a_ship_proof_count":
            len(text_without_a_ship_proof),
        "text_without_a_ship_proof": text_without_a_ship_proof,
        "watched_artifact_sha256": watched,
        "pass": len(lost) == 0,
    }
    fh = open(OUT, "w")
    json.dump(doc, fh, indent=1, sort_keys=True)
    fh.close()

    print("population %d" % len(before))
    print("standing before: %s" % json.dumps(before_counts,
                                             sort_keys=True))
    total_after = {}
    for lang in per_language:
        for key in per_language[lang]:
            total_after[key] = total_after.get(key, 0) + \
                per_language[lang][key]
    print("universal after: %s" % json.dumps(total_after,
                                             sort_keys=True))
    print("")
    for key in sorted(cross):
        print("  %-52s %d" % (key, cross[key]))
    print("")
    print("units that were converged and now carry no universal "
          "text: %d" % len(lost))
    for one in lost:
        print("  %-14s %-26s %s" % (one["unit"], one["status_before"],
                                    (one["named_cause"] or "")[:90]))
    print("")
    print("units that were NOT converged and now carry a proved "
          "universal text: %d" % len(gained))
    print("converged UNDER THE UNIVERSAL FORM: %d of %d"
          % (len(converged_after), len(before)))
    print("carry a universal text but are NOT converged (the prior "
          "text they rest on has no standing ship proof): %d"
          % len(text_without_a_ship_proof))
    return 0


if __name__ == "__main__":
    sys.exit(main())
