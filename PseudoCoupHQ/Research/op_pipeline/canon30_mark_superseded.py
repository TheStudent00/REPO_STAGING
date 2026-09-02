#!/usr/bin/env python3
"""canon30_mark_superseded.py -- TASK 26 housekeeping.

canon30.py was this lap's first float gate. Its STRAIGHT-LINE half is
sound and canon31 reproduces it exactly (74 accepted, same units). Its
BRANCHING half is VOID: it inherited canon9_behaviour_check's shape of
reading canon4_units's `blocks` as ground truth against
`derived_blocks` as the candidate, and canon4.py assigns both names
the same list object, so those 42 "PROVED_EQUAL" verdicts compared a
text with itself.

Rather than delete the artifact (it is the evidence of how the defect
was found), this file stamps every canon30_units_<lang>.json meta
block with a superseded notice naming canon31_units_<lang>.json, and
stamps the void verdict on each affected unit record, so nothing
downstream can read a circular verdict as a result.

Coding discipline: no complex/compound one-liner statements.

usage:
  canon30_mark_superseded.py
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]

NOTICE = (
    "SUPERSEDED by canon31_units_<lang>.json. The branching verdicts "
    "in this file are VOID: they were produced by a gate that read "
    "canon4_units's `blocks` field as ground truth against its "
    "`derived_blocks` field as the candidate, and canon4.py assigns "
    "both names the same list object (its own lines 772-777), so the "
    "comparison was a text against itself. The straight-line "
    "verdicts in this file are sound and canon31 reproduces them."
)


def main():
    total_voided = 0
    for lang in LANGS:
        path = os.path.join(HERE, "canon30_units_%s.json" % lang)
        doc = json.load(open(path))
        doc["meta"]["superseded"] = NOTICE
        voided = 0
        for n, rec in doc["units"].items():
            source = rec.get("job7_candidate_source")
            if source != "canon4_units.derived_blocks":
                continue
            rec["job7_verdict_void"] = NOTICE
            voided = voided + 1
        fh = open(path, "w")
        json.dump(doc, fh, indent=1, sort_keys=True)
        fh.write("\n")
        fh.close()
        print("stamped canon30_units_%s.json -- %d branching "
              "verdicts marked void" % (lang, voided))
        total_voided = total_voided + voided
    print("TOTAL branching verdicts marked void: %d" % total_voided)


if __name__ == "__main__":
    main()
