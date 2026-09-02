#!/usr/bin/env python3
"""dominant_table_containment.py -- ANNOTATION ONLY.

Adds a `contains` field to every class row of dominant_table9.json:
a list of {class_id, via} entries.  Class X contains class Y when some
unit in X's guard-bearing structure contains, as its normal-path
expression, the WHOLE normalized expression of some unit in Y --
tree_matches2.json's own containment edges (sub-tree containment over
the spill/reload-fixed normal-path root), mapped through unit -> class
membership as dominant_table9.json already states it.

THIS DOES NOT MERGE ANYTHING.  Containment is recorded as a directional
relation between two classes that may (and, per the modulo family
below, mostly now do not, since tree-exact already unified them)
remain separate rows; it never joins a union-find set and never changes
`size`, `languages`, or `members`.  The distinction matters precisely
because compositional matching (AgentMemory, 2026-08-26) treats
containment as evidence a component RECURS across two units, not as
evidence the two units are the SAME equivalence class -- that stronger
claim is tree-exact's and sem's and byte's to make, not this file's.

THE SPELLING BAN: containment edges come from tree_matches2.json, whose
own candidate scope is the shared operand type pair -- machine
evidence -- never `operator`.  This file adds nothing to that scope; it
only re-keys existing edges by class id.  `operator` appears here only
inside a `via` string, as a display label.

usage:
  dominant_table_containment.py [--table dominant_table9.json]
                                 [--matches tree_matches2.json]
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

TABLE = "dominant_table9.json"
MATCHES = "tree_matches2.json"


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def main():
    table_path = os.path.join(HERE, TABLE)
    matches_path = os.path.join(HERE, MATCHES)
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--table":
            i += 1
            table_path = args[i]
        elif args[i] == "--matches":
            i += 1
            matches_path = args[i]
        i += 1

    table = json.load(open(table_path))
    matches = json.load(open(matches_path))

    unit_class = {}
    for r in table["rows"]:
        for m in r["members"]:
            unit_class[m["unit"]] = r["class_id"]

    by_id = {r["class_id"]: r for r in table["rows"]}
    for r in table["rows"]:
        r["contains"] = []

    seen = set()
    edges_mapped = 0
    edges_skipped_same_class = 0
    edges_skipped_unmapped = 0
    for e in matches["containment"]:
        cont = e["container"]
        held = e["contained"]
        x_unit = "%s/op_%s" % (cont["lang"], cont["n"])
        y_unit = "%s/op_%s" % (held["lang"], held["n"])
        x_class = unit_class.get(x_unit)
        y_class = unit_class.get(y_unit)
        if x_class is None or y_class is None:
            edges_skipped_unmapped += 1
            continue
        if x_class == y_class:
            edges_skipped_same_class += 1
            continue
        via = ("%s (%s) contains %s (%s)"
              % (x_unit, cont["operator"], y_unit, held["operator"]))
        dedup_key = (x_class, y_class, via)
        if dedup_key in seen:
            continue
        seen.add(dedup_key)
        by_id[x_class]["contains"].append(dict(class_id=y_class, via=via))
        edges_mapped += 1

    rows_with_containment = sum(1 for r in table["rows"] if r["contains"])

    log("containment edges read from %s: %d" % (MATCHES,
                                                 len(matches["containment"])))
    log("mapped to distinct class-level entries: %d" % edges_mapped)
    log("skipped (both endpoints already the same class): %d"
        % edges_skipped_same_class)
    log("skipped (an endpoint unit is not in dominant_table9): %d"
        % edges_skipped_unmapped)
    log("rows carrying at least one containment entry: %d"
        % rows_with_containment)

    table["containment_note"] = (
        "annotation only -- `contains` never triggers a merge; a class "
        "row's members/size/languages are exactly dominant_table_tree.py's "
        "own union-find output")
    table["containment_stats"] = dict(
        edges_read=len(matches["containment"]),
        edges_mapped=edges_mapped,
        edges_skipped_same_class=edges_skipped_same_class,
        edges_skipped_unmapped=edges_skipped_unmapped,
        rows_with_containment=rows_with_containment,
    )

    json.dump(table, open(table_path, "w"), indent=1)
    log("wrote %s (in place, contains field added)" % table_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
