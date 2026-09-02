#!/usr/bin/env python3
"""dom_ops_0branch3.py -- RE-RUN the 0-branch DOM_OP construction on
canon7 text, reported BOTH with the old (inconsistent) result_type_of
and with the DWARF-machine-fact result_type_norm.py fix.

dom_ops_0branch.py's construction rule is reused UNCHANGED (imported,
not re-derived), same as dom_ops_0branch2.py already did for canon5
text: nodes = (language, grammar operator, arity); edges weighted by
shared-class then shared-type-key count; each node keeps its single
strongest counterpart per foreign language, kept only when MUTUAL;
connected components of the mutual-best graph are the dominant
operators.

TWO substitutions from dom_ops_0branch2.py, both named in this lap's
brief:
  1. the TEXT component of the class key is now canon7_units_<lang>.
     json's `canon7_text` (this lap's context-carrying convergence),
     not canon5's.
  2. the RESULT-TYPE component of the class key is computed TWO WAYS
     in the SAME run -- `result_type_of()` (dom_ops_0branch.py's
     original, kept unchanged, inconsistent across languages as
     documented there) and `result_type_norm.class_family()` (this
     lap's DWARF-machine-fact fix) -- so the two dom_op tables can be
     reported side by side against the SAME population and the SAME
     text, isolating exactly what the result-type fix changes.

THE SPELLING BAN: unchanged -- the class key never includes the
operator token, only type reps, result type, and canon7 text; the
token is read exactly once per node as `display_label`.

usage:
  dom_ops_0branch3.py [--out DIR]
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dom_ops as DO                                            # noqa: E402
import dom_ops_0branch as DB                                     # noqa: E402
import result_type_norm as RTN                                   # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]


def load_0branch_units():
    out = []
    missing_canon7 = 0
    for lang in LANGS:
        canon4_path = os.path.join(HERE, "canon4_units_%s.json" % lang)
        canon7_path = os.path.join(HERE, "canon7_units_%s.json" % lang)
        canon4_doc = json.load(open(canon4_path))
        canon7_doc = json.load(open(canon7_path))
        canon7_units = canon7_doc["units"]
        for n, u in canon4_doc["units"].items():
            if "derived_blocks" in u:
                continue
            if u.get("erasure") != "ok":
                continue
            if not isinstance(u.get("derived_text"), list):
                continue
            c7 = canon7_units.get(n)
            if c7 is None or c7.get("canon7_text") is None:
                missing_canon7 = missing_canon7 + 1
                continue
            out.append((lang, n, u, c7))
    if missing_canon7:
        sys.stderr.write(
            "!! %d 0-branch units had no canon7_text (should not "
            "happen -- canon7.py falls back to canon5_text for "
            "every unit with canon4 text)\n" % missing_canon7)
    return out


def build_provenance_and_table(units, use_dwarf_result_type):
    prov = {}
    classes = {}
    unknown_result_type = 0
    for lang, n, u, c7 in units:
        label = "%s/op_%s" % (lang, n)
        prov[label] = {
            "lang": lang,
            "n": n,
            "display_label": u.get("operator"),
            "arity_bucket": DB.arity_bucket_of(u),
        }
        tkey = DB.type_pair_of(u)
        if use_dwarf_result_type:
            fam, note = RTN.class_family(lang, n, u.get("meta"))
            if fam is None:
                unknown_result_type += 1
                rkey = "unknown(%s)" % note[:40]
            else:
                rkey = fam
        else:
            rkey = DB.result_type_of(u)
        text = c7["canon7_text"]
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
    return prov, {"rows": rows}, unknown_result_type


def run_one(units, use_dwarf_result_type, generator_label):
    prov, table, unknown_result_type = build_provenance_and_table(
        units, use_dwarf_result_type)
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

    return {
        "result_type_source": generator_label,
        "population_size": len(units),
        "class_count": len(table["rows"]),
        "unknown_result_type_units": unknown_result_type,
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
    args = argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--out":
            i = i + 1
            outdir = args[i]
        i = i + 1

    units = load_0branch_units()

    old_result = run_one(
        units, False, "dom_ops_0branch.py's original result_type_of "
        "(c/cpp collapse to gp/vec; go/rust/swift use their own raw "
        "meta.result_type strings, inconsistent across languages)")
    dwarf_result = run_one(
        units, True, "result_type_norm.py's DWARF-machine-fact fix "
        "(signed/4->i32, signed/8->i64, unsigned/4->u32, "
        "unsigned/8->u64, boolean/1->bool, float/4->f32, "
        "float/8->f64 -- names are display labels only)")

    out = {
        "meta": {
            "role": "generator provenance",
            "generator": "dom_ops_0branch3.py",
            "construction": "dom_ops7.py's rule, unchanged (via "
                           "dom_ops_0branch.py, imported not "
                           "restated): nodes = (language, grammar "
                           "operator, arity); edges weighted by "
                           "shared-class then shared-type-key count; "
                           "mutual-strongest per foreign language; "
                           "connected components of the mutual-best "
                           "graph",
            "class_basis": "(type pair, result type, canon7 TEXT) "
                          "over the 0-branch population only -- no "
                          "operator token in the class key -- run "
                          "TWICE against the SAME population/text, "
                          "once with each result-type source, so the "
                          "isolated effect of the DWARF fix is "
                          "visible",
            "population": "canon4_units_*.json, 0-branch (derived_text "
                         "is a list, erasure == ok), joined to "
                         "canon7_units_*.json for canon7_text -- the "
                         "SAME population dom_ops_0branch.py/"
                         "dom_ops_0branch2.py used",
            "baseline_for_comparison": "dom_ops_0branch.json (canon4 "
                                      "text): 135 nodes, 26 dom_ops, "
                                      "73 edgeless nodes",
        },
        "with_old_result_type": old_result,
        "with_dwarf_result_type": dwarf_result,
    }

    name = os.path.join(outdir, "dom_ops_0branch3.json")
    fh = open(name, "w")
    json.dump(out, fh, indent=1)
    fh.close()
    print("wrote %s" % name)
    print("population(0-branch)          %d" % len(units))
    print()
    print("WITH OLD result_type_of:")
    print("  classes    %d" % old_result["class_count"])
    print("  nodes      %d" % old_result["nodes"])
    print("  dom_ops    %d" % old_result["dom_op_count"])
    print("  singletons %d" % old_result["singleton_dom_ops"])
    print("  edgeless   %d" % old_result["nodes_with_no_surviving_edge"])
    print()
    print("WITH DWARF result_type (result_type_norm.py):")
    print("  classes    %d" % dwarf_result["class_count"])
    print("  nodes      %d" % dwarf_result["nodes"])
    print("  dom_ops    %d" % dwarf_result["dom_op_count"])
    print("  singletons %d" % dwarf_result["singleton_dom_ops"])
    print("  edgeless   %d" % dwarf_result["nodes_with_no_surviving_edge"])
    print("  unknown result type (excluded from a scalar family) %d"
          % dwarf_result["unknown_result_type_units"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
