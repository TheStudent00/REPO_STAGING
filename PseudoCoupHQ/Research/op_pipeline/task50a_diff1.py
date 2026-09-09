#!/usr/bin/env python3
"""task50a_diff1.py -- what the corrected emitter changes, over the WHOLE
swift candidate set, and how that lines up with the 276 refusals.

THE TWO CANDIDATE SETS, BOTH WALKED
-----------------------------------
  probe_manifest_swift.json    the ORIGINAL run: 6 hand-written holder
                               types, 1,086 candidates.
  probe_manifest2_swift.json   the REGENERATION: the extracted scalar
                               core, 4,187 candidates.  This is the set
                               the 276 refusals came from.

For every candidate in each set, the stored source is compared against
what `probe_gen3.emit_swift` writes for the same record.  A candidate
whose text is unchanged is counted and not listed; a candidate whose
text changes is listed with the DIRECTION of the change:

  attribute_removed   the old emitter attached @_cdecl and the
                      corrected one does not (the F45-4 defect)
  attribute_added     the corrected one attaches it and the old one did
                      not (the hand list was too narrow as well as
                      wrong in position; recorded, not hidden)

THE CROSS-CHECK AGAINST THE COMPILER'S REFUSALS
------------------------------------------------
The 276 are re-derived from the trickle stores by the same walk
`regen_validate1.py` used -- holders all declarable, oracle verdict
`legal`, refused, message shape equal to shape_0001's text as
`regen_witness_validation1.json` banked it -- and the id set is
compared with the `attribute_removed` set.  The comparison is set
equality, both directions, and both differences are printed.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim.

Every candidate in this program is selected by PROBE ID and grouped by
TYPE evidence and by the compiler's own message shape.  No token is a
key, a group or a selector anywhere.

usage:  /tmp/reconnect_venv/bin/python3 task50a_diff1.py
writes: task50a_diff1.json
"""

import collections
import glob
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import probe_gen3                                          # noqa: E402
import regen_validate1                                     # noqa: E402

PRODUCT = os.path.join(HERE, "task50a_diff1.json")
BANKED = os.path.join(HERE, "regen_witness_validation1.json")


def walk_manifest(path, tag):
    """Compare every stored swift source with the corrected emitter's."""
    doc = json.load(open(path))
    same = 0
    changed = []
    for key in sorted(doc["probes"], key=lambda k: int(k)):
        rec = doc["probes"][key]
        before = rec["source"]
        after, cdecl_after = probe_gen3.emit_swift(
            rec["n"], rec["operator"], rec["arity"], rec["position"],
            rec["lhs_type"], rec["rhs_type"], rec["result_type"])
        if before == after:
            same += 1
            continue
        cdecl_before = rec["symbol_exact"]
        if cdecl_before and not cdecl_after:
            direction = "attribute_removed"
        elif cdecl_after and not cdecl_before:
            direction = "attribute_added"
        else:
            direction = "text_changed_without_an_attribute_change"
        changed.append({
            "language": "swift",
            "manifest": tag,
            "id": "swift/probe_%s" % key,
            "n": rec["n"],
            "lhs_type": rec["lhs_type"],
            "rhs_type": rec["rhs_type"],
            "result_type": rec["result_type"],
            "direction": direction,
            "source_before": before,
            "source_after": after,
        })
    return same, changed


SHAPE_TEXT = None


def refusal_ids_of_the_banked_shape():
    """Re-derive the 276 from the trickle stores, by the banked shape."""
    global SHAPE_TEXT
    banked = json.load(open(BANKED))
    shapes = banked["miss_shapes"]
    if len(shapes) != 1:
        raise SystemExit("REFUSE: expected one banked miss shape, saw %d"
                         % len(shapes))
    SHAPE_TEXT = shapes[0]["text"]
    banked_count = shapes[0]["count"]
    ok_types = regen_validate1.declarable_sets()
    quirk_doc = json.load(open(os.path.join(HERE, "legality_quirks.json")))
    quirk_ids = set()
    for row in quirk_doc["annotations"]:
        quirk_ids.add((row["language"], row["rule_id"]))
    files = sorted(glob.glob(os.path.join(HERE, "trickle_store",
                                          "op_units2_swift_*.json")))
    found = {}
    for path in files:
        doc = json.load(open(path))
        lang = doc["language"]
        for key in doc["probes"]:
            probe = doc["probes"][key]
            meta = probe["meta"]
            accepted = ("ship" in probe) and (
                probe.get("refused") in (None, "", False))
            if accepted:
                continue
            holders = [meta["lhs_type"]]
            if meta.get("rhs_type"):
                holders.append(meta["rhs_type"])
            if not all(h in ok_types[lang] for h in holders):
                continue
            if meta.get("filter_verdict") != "legal":
                continue
            hits_q = [r for r in (meta.get("rule_ids") or [])
                      if (lang, r) in quirk_ids]
            if hits_q:
                continue
            text = probe.get("refused") or ""
            if regen_validate1.shape_of(text) != SHAPE_TEXT:
                continue
            found["swift/probe_%s" % key] = text
    return found, banked_count, len(files)


def main():
    manifests = [
        ("probe_manifest_swift.json", "original_run"),
        ("probe_manifest2_swift.json", "regeneration"),
    ]
    per_manifest = []
    all_changed = []
    for name, tag in manifests:
        path = os.path.join(HERE, name)
        same, changed = walk_manifest(path, tag)
        directions = collections.Counter(c["direction"] for c in changed)
        per_manifest.append({
            "manifest": name,
            "tag": tag,
            "candidates": same + len(changed),
            "text_unchanged": same,
            "text_changed": len(changed),
            "by_direction": dict(directions),
        })
        all_changed.extend(changed)
        print("%-28s %5d candidates  %5d unchanged  %4d changed  %s"
              % (name, same + len(changed), same, len(changed),
                 dict(directions)))

    refusals, banked_count, files_read = refusal_ids_of_the_banked_shape()
    removed = set(c["id"] for c in all_changed
                  if c["manifest"] == "regeneration"
                  and c["direction"] == "attribute_removed")
    refused_ids = set(refusals)
    only_refused = sorted(refused_ids - removed)
    only_removed = sorted(removed - refused_ids)
    print("banked shape count %d ; re-derived from %d store files: %d"
          % (banked_count, files_read, len(refused_ids)))
    print("attribute_removed in the regeneration set: %d" % len(removed))
    print("in the refusals but not fixed: %d" % len(only_refused))
    print("fixed but not in the refusals: %d" % len(only_removed))

    doc = {}
    doc["generated_by"] = "task50a_diff1.py"
    doc["task"] = "50(a) -- the swift probe emitter's @_cdecl test"
    doc["reads"] = ["probe_manifest_swift.json", "probe_manifest2_swift.json",
                    "swift_cdecl_witness1.json",
                    "regen_witness_validation1.json",
                    "trickle_store/op_units2_swift_*.json"]
    doc["spelling_ban"] = (
        "candidates are selected by probe id and grouped by type evidence "
        "and by the compiler's own message shape; no key, grouping, "
        "pairing or row structure is an operator token")
    doc["banked_population_note"] = (
        "the banked 29,288 accepted probes PREDATE this fix: they were "
        "produced by probe_gen.py's emitter as it stood on 2026-09-02, "
        "and nothing in this task re-runs the regeneration or rewrites a "
        "banked store")
    doc["per_manifest"] = per_manifest
    doc["banked_miss_shape_text"] = SHAPE_TEXT
    doc["banked_miss_shape_count"] = banked_count
    doc["rederived_refusal_count"] = len(refused_ids)
    doc["attribute_removed_in_regeneration"] = len(removed)
    doc["in_the_refusals_but_not_fixed"] = only_refused
    doc["fixed_but_not_in_the_refusals"] = only_removed
    doc["set_equality"] = (len(only_refused) == 0 and len(only_removed) == 0)
    doc["changed"] = all_changed
    fh = open(PRODUCT, "w")
    json.dump(doc, fh, indent=1)
    fh.write("\n")
    fh.close()
    print("wrote %s" % PRODUCT)
    cmd = [sys.executable, os.path.join(HERE, "check_no_spelling_keys.py"),
           PRODUCT]
    done = subprocess.run(cmd, capture_output=True, text=True)
    print(done.stdout.strip())
    if done.returncode != 0:
        print(done.stderr.strip())
        os.remove(PRODUCT)
        raise SystemExit("REFUSED OWN OUTPUT: spelling guard failed")


if __name__ == "__main__":
    main()
