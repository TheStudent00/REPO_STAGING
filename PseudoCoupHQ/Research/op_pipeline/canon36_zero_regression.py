#!/usr/bin/env python3
"""canon36_zero_regression.py -- TASK 43: zero regression in the ruled
sense, and the merge measurement.

THE RULED SENSE, quoted from the round-8 brief because it is not the
usual one: the new texts REPLACE the old as the canonical column, so
"zero regressions" means NO UNIT THAT WAS PROVED UNDER ANY PRIOR FORM
LOSES PROVED STATUS WITHOUT A NAMED, PROVED CAUSE.  Text change is the
point, not a regression.

WHAT THIS FILE COMPUTES, each from disk:
  * the round-8 proved set (canon35_universal_<lang>.json, outcome
    UNIVERSAL_TEXT_PROVED) against the round-9 proved set
    (canon36_universal_<lang>.json, outcome REGION_TEXT_PROVED), unit
    by unit, with every unit that lost proved status named;
  * the merge measurement the round-8 lap could not obtain: distinct
    texts before and after, texts carried by more than one language,
    and how many round-8 texts MERGE into one round-9 text.  Round 8
    measured zero merges and 77 splits and said so; this is the same
    measurement on the register-free form;
  * the sha256 of every artifact this lap must NOT have touched, so a
    later reader can recompute rather than trust.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation).  No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns.  The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label
on the member.  HISTORY OF VIOLATIONS, so the pattern is visible: (1)
the arch campaign's cross-language matrix (caught by the owner
2026-08-24); (2) verdicts.py's row pairing (caught by the owner 2026-08-25
-- the fix brief itself reintroduced it as "same-operator pairs").
MECHANICAL GUARD REQUIRED: every pipeline stage that groups or pairs
units must run the spelling-key check
(op_pipeline/check_no_spelling_keys.py) and refuse its own output on
failure.  A brief handed to any subagent for this line MUST paste
this paragraph verbatim."
"""

import hashlib
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]
OUT = os.path.join(HERE, "canon36_zero_regression.json")

WATCHED = [
    "canon35_universal_c.json", "canon35_universal_cpp.json",
    "canon35_universal_go.json", "canon35_universal_rust.json",
    "canon35_universal_swift.json", "dominant_table24.json",
    "dominant_table25.json", "dom_ops22.json", "dom_ops23.json",
    "interp_table2.json", "interp_join2.json", "interp_join3.json",
    "union_table2.json", "union_table3.json", "interp_canon35.json",
]


def load(name):
    return json.load(open(os.path.join(HERE, name)))


def main():
    before = {}
    after = {}
    before_text = {}
    after_text = {}
    for lang in LANGS:
        for label, rec in load("canon35_universal_%s.json"
                               % lang)["units"].items():
            before[label] = rec.get("outcome")
            if rec.get("outcome") == "UNIVERSAL_TEXT_PROVED":
                before_text[label] = rec.get("universal_text")
        for label, rec in load("canon36_universal_%s.json"
                               % lang)["units"].items():
            after[label] = rec.get("outcome")
            if rec.get("outcome") == "REGION_TEXT_PROVED":
                after_text[label] = rec.get("universal_text")

    lost = []
    gained = []
    for label in sorted(set(before) | set(after)):
        was = before.get(label) == "UNIVERSAL_TEXT_PROVED"
        now = after.get(label) == "REGION_TEXT_PROVED"
        if was and not now:
            lost.append({"unit": label, "round9_outcome": after.get(label)})
        if now and not was:
            gained.append(label)

    cross = {}
    for label, text in after_text.items():
        lang = label.split("/")[0]
        cross.setdefault(text, set()).add(lang)
    cross_before = {}
    for label, text in before_text.items():
        lang = label.split("/")[0]
        cross_before.setdefault(text, set()).add(lang)

    shared = set(before_text) & set(after_text)
    forward = {}
    backward = {}
    for label in shared:
        forward.setdefault(before_text[label], set()).add(after_text[label])
        backward.setdefault(after_text[label], set()).add(before_text[label])
    merges = 0
    for _new, olds in backward.items():
        if len(olds) > 1:
            merges = merges + 1
    splits = 0
    for _old, news in forward.items():
        if len(news) > 1:
            splits = splits + 1

    watched = {}
    for name in WATCHED:
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            continue
        digest = hashlib.sha256(open(path, "rb").read()).hexdigest()
        watched[name] = digest
    status = subprocess.run(
        ["git", "status", "--porcelain"] +
        ["Research/op_pipeline/" + n for n in WATCHED],
        cwd=os.path.join(HERE, "..", ".."),
        capture_output=True, text=True)

    document = {
        "meta": {
            "role": "generator provenance",
            "produced_by": "canon36_zero_regression.py",
        },
        "population": len(after),
        "round8_proved": len(before_text),
        "round9_proved": len(after_text),
        "units_that_lost_proved_status": lost,
        "units_that_gained_proved_status": sorted(gained),
        "distinct_texts": {
            "round8": len(set(before_text.values())),
            "round9": len(set(after_text.values())),
        },
        "texts_carried_by_more_than_one_language": {
            "round8": len([t for t, s in cross_before.items()
                           if len(s) > 1]),
            "round9": len([t for t, s in cross.items() if len(s) > 1]),
        },
        "round8_texts_that_merge_into_one_round9_text": merges,
        "round8_texts_that_split_into_more_than_one": splits,
        "units_carrying_both_texts": len(shared),
        "watched_artifact_sha256": watched,
        "watched_artifact_git_status": status.stdout.strip(),
    }
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    for key in ("population", "round8_proved", "round9_proved",
                "distinct_texts",
                "texts_carried_by_more_than_one_language",
                "round8_texts_that_merge_into_one_round9_text",
                "round8_texts_that_split_into_more_than_one",
                "units_carrying_both_texts"):
        print("%-46s %s" % (key, json.dumps(document[key])))
    print("units that lost proved status: %d" % len(lost))
    for entry in lost:
        print("   %-14s round9=%s" % (entry["unit"],
                                      entry["round9_outcome"]))
    print("units that gained proved status: %d" % len(gained))
    print("watched artifacts, git status (empty = all unmodified):")
    print(status.stdout.strip() or "  (no lines)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
