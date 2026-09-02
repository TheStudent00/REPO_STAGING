#!/usr/bin/env python3
"""canon35_table_diff.py -- TASK 39: what the universal form did to
the class table, computed rather than asserted.

THE EXPECTATION UNDER TEST (the brief's own words, and it is an
expectation, not an assumption): "the universal form removes register-
idiosyncrasy (go's ABI differences become invisible below the
standardized loads), so cross-language classes may MERGE further".

This file measures it three ways and prints each verbatim:

  1.  CLASS COUNT.  dominant_table24.json vs dominant_table25.json,
      with the change decomposed into its two possible causes:
        (a) MERGE -- two table24 classes whose members all land in one
            table25 class;
        (b) LOSS -- a table24 class that shrinks or disappears because
            a member has no universal text.
      Nothing is attributed to (a) that (b) explains.

  2.  NODE AND FAMILY COUNTS, dom_ops22.json vs dom_ops23.json, and
      the FULL family membership comparison: every family whose node
      set changed is printed, both sides, with the units involved.

  3.  CROSS-LANGUAGE TEXT IDENTITY.  How many distinct universal texts
      are carried by units of more than one language, against the same
      count on the register-first texts.  This is the direct measure of
      "register idiosyncrasy removed": if the standardized loads hide
      an ABI difference, two languages that previously rendered
      differently now render the same characters.

Coding discipline: no complex/compound one-liner statements.

usage:
  canon35_table_diff.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "canon35_table_diff.json")
LANGS = ["c", "cpp", "go", "rust", "swift"]


def load(name):
    return json.load(open(os.path.join(HERE, name)))


def class_of_unit(doc):
    out = {}
    for row in doc["rows"]:
        for member in row["members"]:
            out[member["unit"]] = row["class_id"]
    return out


def members_of(doc):
    out = {}
    for row in doc["rows"]:
        names = []
        for member in row["members"]:
            names.append(member["unit"])
        out[row["class_id"]] = sorted(names)
    return out


def family_map(doc, key):
    out = {}
    for family in doc[key]:
        units = set()
        for node in family["nodes"]:
            units.update(node.get("units", []))
        out[family["dom_op_id"]] = sorted(units)
    return out


def main():
    t24 = load("dominant_table24.json")
    t25 = load("dominant_table25.json")
    d22 = load("dom_ops22.json")
    d23 = load("dom_ops23.json")

    left_out = set()
    for entry in t25["units_without_a_universal_text"]:
        left_out.add(entry["unit"])

    of24 = class_of_unit(t24)
    of25 = class_of_unit(t25)
    m24 = members_of(t24)
    m25 = members_of(t25)

    # (a) MERGES: a table25 class holding units that were in more than
    # one table24 class.
    merges = []
    for class_id in sorted(m25):
        sources = {}
        for unit in m25[class_id]:
            old = of24.get(unit)
            if old is None:
                continue
            sources.setdefault(old, []).append(unit)
        if len(sources) < 2:
            continue
        merges.append({
            "table25_class": class_id,
            "canonical_text": None,
            "table24_classes_merged": sorted(sources),
            "units_by_source_class": sources,
        })
    text_of_25 = {}
    for row in t25["rows"]:
        text_of_25[row["class_id"]] = row["canonical_text"]
    for one in merges:
        one["canonical_text"] = text_of_25[one["table25_class"]]

    # (b) LOSSES: a table24 class that lost members to the left-out set.
    losses = []
    for class_id in sorted(m24):
        gone = []
        for unit in m24[class_id]:
            if unit in left_out:
                gone.append(unit)
        if not gone:
            continue
        remaining = []
        for unit in m24[class_id]:
            if unit not in left_out:
                remaining.append(unit)
        losses.append({
            "table24_class": class_id,
            "units_left_out": gone,
            "units_remaining": remaining,
            "class_disappeared": len(remaining) == 0,
        })

    # (2) families
    f22 = family_map(d22, "families")
    f23 = family_map(d23, "families")
    by_units_22 = {}
    for name in f22:
        by_units_22[tuple(f22[name])] = name
    changed = []
    for name in sorted(f23):
        units = tuple(f23[name])
        if units in by_units_22:
            continue
        changed.append({
            "dom_ops23_family": name,
            "units": list(units),
            "nearest_dom_ops22_families": [
                {"family": other, "units": f22[other]}
                for other in sorted(f22)
                if set(f22[other]) & set(units)
            ],
        })
    vanished = []
    by_units_23 = {}
    for name in f23:
        by_units_23[tuple(f23[name])] = name
    for name in sorted(f22):
        units = tuple(f22[name])
        if units in by_units_23:
            continue
        vanished.append({"dom_ops22_family": name,
                         "units": list(units)})

    # (3) cross-language text identity, both forms
    universal_text_langs = {}
    prior_text_langs = {}
    for lang in LANGS:
        doc = load("canon35_universal_%s.json" % lang)["units"]
        for label, rec in doc.items():
            text = rec.get("universal_text")
            prior = rec.get("prior_text")
            # THE SAME UNIT SET ON BOTH SIDES.  Counting the register-
            # first texts over a larger population than the universal
            # texts would make the comparison meaningless, so a unit
            # counts only when it carries both.
            if text is None:
                continue
            if prior is None:
                continue
            universal_text_langs.setdefault(text, set()).add(lang)
            prior_text_langs.setdefault(prior, set()).add(lang)

    def cross_count(table):
        total = 0
        for text in table:
            if len(table[text]) > 1:
                total = total + 1
        return total

    cross_universal = cross_count(universal_text_langs)
    cross_prior = cross_count(prior_text_langs)

    doc = {
        "meta": {
            "produced_by": "canon35_table_diff.py",
            "role": "generator provenance",
        },
        "classes": {"dominant_table24": len(t24["rows"]),
                    "dominant_table25": len(t25["rows"])},
        "nodes": {"dom_ops22": d22["nodes"], "dom_ops23": d23["nodes"]},
        "families": {"dom_ops22": d22["dom_op_count"],
                     "dom_ops23": d23["dom_op_count"]},
        "edgeless": {
            "dom_ops22": d22["nodes_with_no_surviving_edge"],
            "dom_ops23": d23["nodes_with_no_surviving_edge"]},
        "merges": merges,
        "merge_count": len(merges),
        "classes_that_lost_members": losses,
        "families_changed": changed,
        "families_vanished": vanished,
        "distinct_texts": {
            "universal": len(universal_text_langs),
            "register_first": len(prior_text_langs)},
        "distinct_texts_carried_by_more_than_one_language": {
            "universal": cross_universal,
            "register_first": cross_prior},
    }
    fh = open(OUT, "w")
    json.dump(doc, fh, indent=1, sort_keys=True)
    fh.close()

    print("classes   24=%d   25=%d" % (len(t24["rows"]),
                                       len(t25["rows"])))
    print("nodes     22=%d   23=%d" % (d22["nodes"], d23["nodes"]))
    print("families  22=%d   23=%d" % (d22["dom_op_count"],
                                       d23["dom_op_count"]))
    print("edgeless  22=%d   23=%d"
          % (d22["nodes_with_no_surviving_edge"],
             d23["nodes_with_no_surviving_edge"]))
    print("")
    print("MERGES (a table25 class holding units from more than one "
          "table24 class): %d" % len(merges))
    for one in merges:
        print("  %s  <- %s" % (one["table25_class"],
                               ", ".join(one["table24_classes_merged"])))
        print("      %s" % one["canonical_text"])
        for source in sorted(one["units_by_source_class"]):
            print("      %s: %s"
                  % (source,
                     ", ".join(one["units_by_source_class"][source])))
    print("")
    print("TABLE24 CLASSES THAT LOST MEMBERS (a member has no "
          "universal text): %d" % len(losses))
    for one in losses:
        print("  %s  left out %s  remaining %d  disappeared=%s"
              % (one["table24_class"], ", ".join(one["units_left_out"]),
                 len(one["units_remaining"]),
                 one["class_disappeared"]))
    print("")
    print("FAMILY CHANGES: %d changed, %d vanished"
          % (len(changed), len(vanished)))
    for one in changed:
        print("  %s  units: %s" % (one["dom_ops23_family"],
                                   ", ".join(one["units"])))
        for near in one["nearest_dom_ops22_families"]:
            print("      dom_ops22 %s: %s"
                  % (near["family"], ", ".join(near["units"])))
    for one in vanished:
        print("  VANISHED %s  units: %s" % (one["dom_ops22_family"],
                                            ", ".join(one["units"])))
    print("")
    print("distinct texts: universal %d, register-first %d"
          % (len(universal_text_langs), len(prior_text_langs)))
    print("distinct texts carried by more than one language: "
          "universal %d, register-first %d"
          % (cross_universal, cross_prior))
    return 0


if __name__ == "__main__":
    sys.exit(main())
