#!/usr/bin/env python3
"""build_table19.py -- dominant_table19.json: dominant_table17.json's
same construction, REKEYED so every member of a proved representatives2
.json group shares one text (the group's representative text) instead
of its own newest-converged text -- SAME construction build_table18.py
already used, over representatives2.json (the CORRECTED grounding)
instead of representatives.json (the defective one). Class key:
(type_pair, machine-fact result_type, REPRESENTATIVE TEXT). Additive:
does not touch dominant_table17.json, representatives.json, or
dominant_table18.json.

usage:
  build_table19.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dominant_table17 as DT17                                  # noqa: E402
import dom_ops as DO                                              # noqa: E402
import dom_ops_0branch as DB                                      # noqa: E402
import result_type_norm as RTN                                    # noqa: E402


def main():
    reps = json.load(open(os.path.join(HERE, "representatives2.json")))
    rep_text_of = {}
    for g in reps["groups"]:
        rep_text = g["representative"]["text"]
        for m in g["members"]:
            rep_text_of[m["unit"]] = rep_text

    gen_docs = DT17.load_generation_docs()
    units = DT17.load_0branch_units(gen_docs)

    prov = {}
    classes = {}
    unknown_result_type = 0
    for lang, n, u, _text, _gen in units:
        label = "%s/op_%s" % (lang, n)
        prov[label] = {
            "lang": lang,
            "n": n,
            "display_label": u.get("operator"),
            "arity_bucket": DB.arity_bucket_of(u),
        }
        tkey = DB.type_pair_of(u)
        fam, note = RTN.class_family(lang, n, u.get("meta"))
        if fam is None:
            unknown_result_type += 1
            rkey = "unknown(%s)" % note[:40]
        else:
            rkey = fam
        rep_text = rep_text_of[label]
        ckey = (tkey, rkey, rep_text)
        classes.setdefault(ckey, {"type_pair": tkey, "members": []})
        classes[ckey]["members"].append({"unit": label})

    rows = []
    order = sorted(classes.keys())
    i = 0
    for ckey in order:
        i += 1
        cid = "C%04d" % i
        rec = classes[ckey]
        rows.append({
            "class_id": cid,
            "type_pair": rec["type_pair"],
            "result_type": ckey[1],
            "members": rec["members"],
        })

    doc = {"table": {"rows": rows}}
    nodes, index = DO.build_nodes(doc, prov)
    class_members = DO.fill_nodes(doc, nodes, index, prov)
    edges = DO.build_edges(doc, nodes, class_members, 0)
    best, ties = DO.best_per_language(nodes, edges)
    kept = DO.mutual_edges(nodes, edges, best)
    comps = DO.components(kept)
    DO.assert_one_per_language(nodes, comps)

    singleton_count = sum(1 for c in comps if len(c) == 1)
    attached = set()
    for c in comps:
        attached.update(c)
    unattached = sorted(set(nodes.keys()) - attached)

    print("classes    %d  (pre-defect baseline: 926)" % len(rows))
    print("nodes      %d  (baseline: 135)" % len(nodes))
    print("dom_ops    %d  (baseline: 26)" % len(comps))
    print("edgeless   %d  (baseline: 23)" % len(unattached))
    print("singletons %d" % singleton_count)
    print("unknown result type %d" % unknown_result_type)

    class_doc = {
        "meta": {
            "generator": "build_table19.py",
            "role_note": "GROUPING/matching artifact (top-level `rows`,"
                        " each with `members`) -- checked by check_no_"
                        "spelling_keys.py IN FULL, no exemption claimed.",
            "construction": "dominant_table17.py's rule, unchanged, "
                           "EXCEPT the text component of the class key "
                           "is now the REPRESENTATIVE text from "
                           "representatives2.json (THE REPRESENTATIVE "
                           "RULE, AgentMemory 2026-08-29, over the "
                           "CORRECTED ground (b) -- see build_"
                           "representatives2.py's docstring for the "
                           "fix) rather than each unit's own "
                           "newest-converged text",
            "population": "1,641 0-branch units, same population as "
                         "dominant_table17.json",
            "baseline": "dominant_table17.json: 926 classes / 135 "
                       "nodes / 26 families / 23 edgeless "
                       "(pre-representative-rule; the number this "
                       "corrected run is compared against, per this "
                       "lap's brief)",
            "supersedes": "dominant_table18.json, which rekeyed on "
                         "representatives.json -- CONFIRMED DEFECTIVE "
                         "(see build_representatives2.py's docstring): "
                         "its ground (b) merged units on a z3-"
                         "simplified normalized-root that collapses "
                         "unmodelled operations to an opaque "
                         "placeholder atom, so distinct computations "
                         "(e.g. f64 +, -, *, / all landing on the "
                         "single placeholder text 'op_2') compared "
                         "equal. dominant_table18.json and dom_ops16."
                         "json are KEPT ON DISK as the defect record, "
                         "per this lap's instruction; not deleted, "
                         "not silently superseded.",
        },
        "classes": len(rows),
        "rows": rows,
    }
    out_path = os.path.join(HERE, "dominant_table19.json")
    json.dump(class_doc, open(out_path, "w"), indent=1)
    print("wrote %s" % out_path)


if __name__ == "__main__":
    main()
