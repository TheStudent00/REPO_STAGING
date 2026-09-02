#!/usr/bin/env python3
"""dom_ops_0branch2.py -- item 3 of the canon5 work list: RE-RUN the
0-branch DOM_OP construction on canon5 text.

This is dom_ops_0branch.py, UNCHANGED in every rule -- same population
filter (0-branch: canon4 erasure == "ok", derived_text is a list, no
derived_blocks), same class key shape (type pair, result type, TEXT),
same dom_ops.py construction (nodes = (language, grammar operator,
arity); edges weighted by shared-class then shared-type-key count;
mutual-strongest per foreign language; connected components) -- with
exactly ONE substitution: the TEXT component of the class key is now
canon5_units_<lang>.json's `canon5_text` (the converged, transform-
and-return canonical text) instead of canon4_units_<lang>.json's
`derived_mnem_joined`. `result_type_of`/`arity_bucket_of`/
`type_pair_of` still read the ENTRY CONTRACT and META off the canon4
record (canon5_units_<lang>.json does not duplicate those fields --
see canon5.py's docstring: this file is deliberately a thin overlay,
not a restatement) -- "dom_ops rule unchanged" means exactly this:
the same machine-form evidence, the same construction, only the text
a class is keyed on has gone through the extra convergence step.

THE SPELLING BAN: unchanged from dom_ops_0branch.py -- the class key
never includes the operator token, only type reps and the canon5
text; the token is read exactly once per node as `display_label`.

usage:
  dom_ops_0branch2.py [--out DIR]
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dom_ops as DO  # noqa: E402  (build_nodes, fill_nodes, build_edges,
                       #             best_per_language, mutual_edges,
                       #             components, assert_one_per_language)
import dom_ops_0branch as DB  # noqa: E402  (result_type_of, type_pair_of,
                               #             arity_bucket_of, node_row)

LANGS = ["c", "cpp", "go", "rust", "swift"]


def load_0branch_units():
    """the SAME 0-branch population dom_ops_0branch.py used (canon4's
    own erasure=="ok" / derived_text-is-a-list filter -- unchanged),
    with each unit's canon5 record joined on (lang, n) for its
    canon5_text/status."""
    out = []
    missing_canon5 = 0
    for lang in LANGS:
        canon4_path = os.path.join(HERE, "canon4_units_%s.json" % lang)
        canon5_path = os.path.join(HERE, "canon5_units_%s.json" % lang)
        canon4_doc = json.load(open(canon4_path))
        canon5_doc = json.load(open(canon5_path))
        canon5_units = canon5_doc["units"]
        for n, u in canon4_doc["units"].items():
            if "derived_blocks" in u:
                continue
            if u.get("erasure") != "ok":
                continue
            if not isinstance(u.get("derived_text"), list):
                continue
            c5 = canon5_units.get(n)
            if c5 is None or c5.get("canon5_text") is None:
                missing_canon5 = missing_canon5 + 1
                continue
            out.append((lang, n, u, c5))
    if missing_canon5:
        sys.stderr.write(
            "!! %d 0-branch units had no canon5_text (should not "
            "happen -- canon5.py falls back to canon4 text for "
            "every unit with canon4 text)\n" % missing_canon5)
    return out


def build_provenance_and_table(units):
    prov = {}
    classes = {}
    for lang, n, u, c5 in units:
        label = "%s/op_%s" % (lang, n)
        prov[label] = {
            "lang": lang,
            "n": n,
            "display_label": u.get("operator"),
            "arity_bucket": DB.arity_bucket_of(u),
        }
        tkey = DB.type_pair_of(u)
        rkey = DB.result_type_of(u)
        text = c5["canon5_text"]
        ckey = (tkey, rkey, text)
        classes.setdefault(ckey, {"type_pair": tkey, "members": []})
        classes[ckey]["members"].append({"unit": label})
    rows = []
    order = sorted(classes.keys())
    i = 0
    for ckey in order:
        i = i + 1
        cid = "C%04d" % i
        rec = classes[ckey]
        rows.append({
            "class_id": cid,
            "type_pair": rec["type_pair"],
            "result_type": ckey[1],
            "members": rec["members"],
        })
    return prov, {"rows": rows}


def main(argv):
    outdir = HERE
    args = argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--out":
            i = i + 1
            outdir = args[i]
        i = i + 1

    units = load_0branch_units()
    prov, table = build_provenance_and_table(units)
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

    out = {
        "meta": {
            "role": "generator provenance",
            "generator": "dom_ops_0branch2.py",
            "construction": "dom_ops7.py's rule, unchanged (via "
                           "dom_ops_0branch.py, imported not "
                           "restated): nodes = (language, grammar "
                           "operator, arity); edges weighted by "
                           "shared-class then shared-type-key count; "
                           "mutual-strongest per foreign language; "
                           "connected components of the mutual-best "
                           "graph",
            "class_basis": "(type pair, result type, canon5 "
                          "TRANSFORM-AND-RETURN CONVERGED text) over "
                          "the 0-branch population only -- no "
                          "operator token in the class key -- the "
                          "one change from dom_ops_0branch.py is "
                          "this text source (canon5_text, not "
                          "canon4's derived_mnem_joined)",
            "population": "canon4_units_*.json, 0-branch (derived_text "
                         "is a list, erasure == ok), joined to "
                         "canon5_units_*.json for canon5_text -- the "
                         "SAME population dom_ops_0branch.py used",
            "baseline_for_comparison": "dom_ops_0branch.json (canon4 "
                                      "text): 135 nodes, 26 dom_ops, "
                                      "73 edgeless nodes",
        },
        "population_size": len(units),
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

    name = os.path.join(outdir, "dom_ops_0branch2.json")
    fh = open(name, "w")
    json.dump(out, fh, indent=1)
    fh.close()
    print("wrote %s" % name)
    print("population(0-branch)  %d" % len(units))
    print("classes                %d" % len(table["rows"]))
    print("nodes                  %d" % len(nodes))
    print("dom_ops (families)     %d" % len(comps))
    print("  singletons           %d" % singleton_count)
    print("  edgeless             %d" % len(unattached))
    print("largest 5 families:")
    for fam in sorted(family_rows, key=lambda f: -f["size"])[:5]:
        langs = sorted(set(nr["lang"] for nr in fam["nodes"]))
        print("  %s size=%d langs=%s" % (fam["dom_op_id"], fam["size"],
                                         langs))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
