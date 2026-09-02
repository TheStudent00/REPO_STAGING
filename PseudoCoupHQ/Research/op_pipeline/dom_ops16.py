#!/usr/bin/env python3
"""dom_ops16.py -- the dom_op (family) construction over dominant_
table17.json, the next number after dom_ops13.json/dominant_table15.
json's pairing. Modeled on dominant_table15.py's own embedded dom_op
step (dom_ops7.py's rule via dom_ops_0branch.py, imported not
restated), but split into its own driver per this lap's instruction,
CONSUMING dominant_table18.json's own class rows rather than
rebuilding the class table itself.

Per-unit provenance (display_label, arity_bucket) is re-derived from
canon4_units_<lang>.json (the same source dominant_table17.py itself
reads for population/arity) keyed by the "lang/op_N" label already
present on each dominant_table18.json class-row member -- this does
NOT re-run the class-membership logic, it only supplies the node-
construction inputs DO.build_nodes/DB.node_row need.

THE SPELLING BAN: unchanged -- the class key already came in from
dominant_table18.json with no operator token in it; this file adds a
`display_label` per node (the token's one-time-per-unit display use),
never as a key.

usage:
  dom_ops16.py [--out DIR] [--table PATH]
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dom_ops as DO                                            # noqa: E402
import dom_ops_0branch as DB                                     # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]


def load_canon4():
    docs = {}
    for lang in LANGS:
        path = os.path.join(HERE, "canon4_units_%s.json" % lang)
        docs[lang] = json.load(open(path))["units"]
    return docs


def build_provenance(table, canon4_docs):
    prov = {}
    for row in table["rows"]:
        for m in row["members"]:
            label = m["unit"]
            if label in prov:
                continue
            lang, _, n = label.partition("/op_")
            u = canon4_docs.get(lang, {}).get(n)
            if u is None:
                continue
            prov[label] = {
                "lang": lang,
                "n": n,
                "display_label": u.get("operator"),
                "arity_bucket": DB.arity_bucket_of(u),
            }
    return prov


def run(table, prov):
    doc = {"table": table}

    nodes, index = DO.build_nodes(doc, prov)
    class_members = DO.fill_nodes(doc, nodes, index, prov)
    edges = DO.build_edges(doc, nodes, class_members, 0)
    best, ties = DO.best_per_language(nodes, edges)
    kept = DO.mutual_edges(nodes, edges, best)
    comps = DO.components(kept)
    checked, collisions = DO.assert_one_per_language(nodes, comps)

    singleton_count = sum(1 for c in comps if len(c) == 1)
    attached = set()
    for c in comps:
        attached.update(c)
    unattached = sorted(set(nodes.keys()) - attached)
    family_rows = []
    for members in comps:
        family_rows.append({
            "dom_op_id": "D%04d" % (len(family_rows) + 1),
            "size": len(members),
            "nodes": [DB.node_row(nodes, nid) for nid in members],
        })
    family_rows.sort(key=lambda r: r["size"], reverse=True)

    return {
        "class_count": len(table["rows"]),
        "nodes": len(nodes),
        "edges_raw": len(edges),
        "edges_mutual": len(kept),
        "dom_op_count": len(comps),
        "singleton_dom_ops": singleton_count,
        "nodes_in_a_dom_op": len(attached),
        "nodes_with_no_surviving_edge": len(unattached),
        "unattached_nodes": [DB.node_row(nodes, nid)
                            for nid in unattached],
        "equally_strongest_ties": len(ties),
        "same_language_collisions_in_one_component": len(collisions),
        "dom_ops": family_rows,
    }


def main(argv):
    outdir = HERE
    table_path = os.path.join(HERE, "dominant_table18.json")
    args = argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--out":
            i = i + 1
            outdir = args[i]
        elif args[i] == "--table":
            i = i + 1
            table_path = args[i]
        i = i + 1

    class_doc = json.load(open(table_path))
    table = {"rows": class_doc["rows"]}
    canon4_docs = load_canon4()
    prov = build_provenance(table, canon4_docs)
    result = run(table, prov)

    dom_ops_doc = {
        "meta": {
            "role": "generator provenance",
            "generator": "dom_ops16.py",
            "note": "the dom_op (family) construction over dominant_"
                   "table17.json's own class rows -- written to "
                   "dom_ops16.json, the next number after dom_ops13."
                   "json/dominant_table15.json's pairing",
            "construction": "dom_ops7.py's rule, unchanged (via "
                           "dom_ops_0branch.py, imported not "
                           "restated): nodes = (language, grammar "
                           "operator, arity); edges weighted by "
                           "shared-class then shared-type-key count; "
                           "mutual-strongest per foreign language; "
                           "connected components of the mutual-best "
                           "graph",
            "source_table": os.path.basename(table_path),
        },
        "class_count": result["class_count"],
        "nodes": result["nodes"],
        "edges_raw": result["edges_raw"],
        "edges_mutual": result["edges_mutual"],
        "dom_op_count": result["dom_op_count"],
        "singleton_dom_ops": result["singleton_dom_ops"],
        "nodes_in_a_dom_op": result["nodes_in_a_dom_op"],
        "nodes_with_no_surviving_edge":
            result["nodes_with_no_surviving_edge"],
        "unattached_nodes": result["unattached_nodes"],
        "equally_strongest_ties": result["equally_strongest_ties"],
        "same_language_collisions_in_one_component":
            result["same_language_collisions_in_one_component"],
        "dom_ops": result["dom_ops"],
    }
    dom_ops_path = os.path.join(outdir, "dom_ops16.json")
    fh = open(dom_ops_path, "w")
    json.dump(dom_ops_doc, fh, indent=1)
    fh.close()

    print("wrote %s" % dom_ops_path)
    print("classes    %d  (baseline: 926)" % result["class_count"])
    print("nodes      %d  (baseline: 135)" % result["nodes"])
    print("dom_ops    %d  (baseline: 26)" % result["dom_op_count"])
    print("edgeless   %d  (baseline: 23)"
          % result["nodes_with_no_surviving_edge"])
    print("singletons %d" % result["singleton_dom_ops"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
