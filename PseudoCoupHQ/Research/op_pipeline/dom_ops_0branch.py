#!/usr/bin/env python3
"""dom_ops_0branch.py -- REAL DOM_OP construction over the 0-branch
population, item 3 of the canon4 work list.

Classes are (type pair, result type, canon4 TEXT) over 0-branch units
only -- machine-form evidence (operand-type reps read straight off the
probe's own meta, result family read off the unit's entry contract,
and the canon4-cleaned instruction text itself), never the operator
token.  dom_ops7.py's construction rule is reused UNCHANGED (imported
from dom_ops.py, not re-derived): nodes = (language, grammar operator,
arity); edge weight = shared-class count then shared type-key count;
each node keeps its single strongest counterpart per foreign language,
kept only when mutual; connected components of the mutual-best graph
are the dominant operators.

THE SPELLING BAN: the class key never includes the operator token --
only type reps (i32, i32*, ...) and the canon4 text.  The token is
read exactly once per node, as `display_label`/`label` -- the same
place dom_ops.py itself has always put it (its own docstring: "nodes
are DISCOVERED from machine evidence ... nodes are (language,
grammar-operator, arity) -- provenance of the probe").

usage:
  dom_ops_0branch.py [--out DIR]
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dom_ops as DO  # noqa: E402  (build_nodes, fill_nodes, build_edges,
                       #             best_per_language, mutual_edges,
                       #             components, assert_one_per_language)

LANGS = ["c", "cpp", "go", "rust", "swift"]


def load_0branch_units():
    """0-branch canon4 units: erasure == "ok" and derived_text is a
    list (straight-line -- excludes anything carrying derived_blocks,
    exactly uniqueness_audit.py's population test)."""
    out = []
    for lang in LANGS:
        path = os.path.join(HERE, "canon4_units_%s.json" % lang)
        doc = json.load(open(path))
        for n, u in doc["units"].items():
            if "derived_blocks" in u:
                continue
            if u.get("erasure") != "ok":
                continue
            if not isinstance(u.get("derived_text"), list):
                continue
            out.append((lang, n, u))
    return out


def result_type_of(u):
    """coarse result type read from machine-form evidence only: the
    unit's own meta.result_type when the probe recorded one, else the
    entry contract's result register FAMILY collapsed to "gp" (general
    purpose integer/pointer) or "vec" (xmm/float) -- never the operator
    token, never a hand -asserted type name."""
    meta = u.get("meta", {})
    rt = meta.get("result_type")
    if rt:
        return rt
    contract = u.get("entry_contract") or {}
    fam = contract.get("result")
    if fam is None:
        return "unknown"
    return "vec" if fam.startswith("xmm") else "gp"


def type_pair_of(u):
    meta = u.get("meta", {})
    lhs = meta.get("lhs_rep")
    rhs = meta.get("rhs_rep")
    return "%s,%s" % (lhs, rhs)


def arity_bucket_of(u):
    """arity read off the entry contract itself (does a "b" register
    exist), not off the probe's own `bucket`/`arity` field -- machine
    form over asserted form, but the two agree everywhere checked."""
    contract = u.get("entry_contract") or {}
    return "binary" if contract.get("b") is not None else "unary"


def build_provenance_and_table(units):
    prov = {}
    classes = {}
    for lang, n, u in units:
        label = "%s/op_%s" % (lang, n)
        prov[label] = {
            "lang": lang,
            "n": n,
            "display_label": u.get("operator"),
            "arity_bucket": arity_bucket_of(u),
        }
        tkey = type_pair_of(u)
        rkey = result_type_of(u)
        text = u.get("derived_mnem_joined")
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


def node_row(nodes, nid):
    node = nodes[nid]
    return {
        "id": node["id"],
        "lang": node["lang"],
        "label": node["label"],
        "arity": node["arity"],
        "unit_count": len(node["units"]),
        "class_count": len(node["classes"]),
        "units": node["units"],
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
            "nodes": [node_row(nodes, nid) for nid in members],
        })

    out = {
        "meta": {
            "role": "generator provenance",
            "generator": "dom_ops_0branch.py",
            "construction": "dom_ops7.py's rule, unchanged: nodes = "
                           "(language, grammar operator, arity); "
                           "edges weighted by shared-class then "
                           "shared-type-key count; mutual-strongest "
                           "per foreign language; connected "
                           "components of the mutual-best graph",
            "class_basis": "(type pair, result type, canon4 "
                          "dead-mov-cleaned text) over the 0-branch "
                          "population only -- no operator token in "
                          "the class key",
            "population": "canon4_units_*.json, 0-branch (derived_text "
                         "is a list, erasure == ok)",
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
        "unattached_nodes": [node_row(nodes, nid) for nid in unattached],
        "equally_strongest_ties": len(ties),
        "same_language_collisions_in_one_component": len(collisions),
        "dom_ops": family_rows,
    }

    name = os.path.join(outdir, "dom_ops_0branch.json")
    fh = open(name, "w")
    json.dump(out, fh, indent=1)
    fh.close()
    print("wrote %s" % name)
    print("population(0-branch)  %d" % len(units))
    print("classes                %d" % len(table["rows"]))
    print("nodes                  %d" % len(nodes))
    print("dom_ops (families)     %d" % len(comps))
    print("  singletons           %d" % singleton_count)
    print("largest 5 families:")
    for fam in sorted(family_rows, key=lambda f: -f["size"])[:5]:
        langs = sorted(set(nr["lang"] for nr in fam["nodes"]))
        print("  %s size=%d langs=%s" % (fam["dom_op_id"], fam["size"],
                                         langs))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
