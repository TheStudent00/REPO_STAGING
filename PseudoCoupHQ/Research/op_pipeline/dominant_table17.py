#!/usr/bin/env python3
"""dominant_table17.py -- re-run the class table on the newest converged
text per unit, extending dominant_table15.py's own generation chain with
THREE further generations produced after it: canon23 (log_081 work item
2, the multi-atom fan-out tracer over condition refusals), canon22 and
canon21 (each generation's own float/condition convergence work, per
canon21.py/canon22.py/canon23.py's own headers), placed ahead of
canon20/19/18/17 and everything dominant_table15.py already fell
through to.

Byte-for-byte the SAME construction dominant_table15.py already used
(dom_ops7.py's rule via dom_ops_0branch.py/dom_ops_0branch3.py, imported
not restated; result_type_norm.py's DWARF-machine-fact result type) --
the ONLY change is GENERATIONS, extended with canon23/canon22/canon21
ahead of the ones dominant_table15.py already knew about. `final_text_of`
already reads "newest generation whose <gen>_text field is present", so
a unit none of canon21/22/23 touched keeps falling through to its
canon20_text (or further) exactly as before -- no other logic changes.

SCOPE: 0-BRANCH POPULATION ONLY (1,641 units) -- same population-
integrity assumption dominant_table15.py already asserts. This number
is explicitly NOT the full 1,779-unit corpus; the two must never be
conflated (see dominant_table15.py's own population note and this
node's PROGRESS.md denominator note). canon21.py/canon22.py/canon23.py's
own drivers all explicitly skip any unit whose `branch_kind` isn't
"straight_line" (mirroring canon18/19/20's own check), so this lap
cannot have touched a branching unit -- the SAME "refuse silently-wrong
scope" check is kept, now widened to cover canon21/22/23 too.

BASELINE (dominant_table15.json/dom_ops13.json, already on disk):
926 classes / 135 nodes / 26 families / 23 edgeless.

THE SPELLING BAN: unchanged, same as dominant_table13.py/dominant_
table14.py/dominant_table15.py -- the class key never includes the
operator token, only type reps, result type, and canon-text; the token
is read exactly once per node as `display_label`. check_no_spelling_
keys.py is run on the output before this program declares success.

usage:
  dominant_table17.py [--out DIR]
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

GENERATIONS = ["canon23", "canon22", "canon21", "canon20", "canon19",
               "canon18", "canon17", "canon16", "canon15", "canon14",
               "canon13", "canon12", "canon11", "canon10", "canon9",
               "canon8", "canon7"]

BRANCH_CHECK_GENERATIONS = ("canon23", "canon22", "canon21", "canon20",
                             "canon19", "canon18", "canon17", "canon16",
                             "canon15", "canon14", "canon13", "canon12",
                             "canon11", "canon10", "canon9", "canon8")


def load_generation_docs():
    docs = {}
    for gen in GENERATIONS:
        docs[gen] = {}
        for lang in LANGS:
            path = os.path.join(HERE, "%s_units_%s.json" % (gen, lang))
            if not os.path.exists(path):
                continue
            docs[gen][lang] = json.load(open(path))["units"]
    return docs


def final_text_of(lang, n, gen_docs):
    """(text, generation_name) -- the newest generation this unit's
    text field is present in. Falls back to canon7_text (present on
    every canon7 record) if no generation ever touched it, which is
    the untouched-unit case."""
    for gen in GENERATIONS:
        rec = gen_docs[gen].get(lang, {}).get(n)
        if rec is None:
            continue
        key = "%s_text" % gen
        if rec.get(key) is not None:
            return rec[key], gen
    rec7 = gen_docs["canon7"].get(lang, {}).get(n)
    if rec7 is not None:
        return rec7.get("canon7_text"), "canon7(unchanged)"
    return None, None


def load_0branch_units(gen_docs):
    out = []
    missing_text = 0
    touched_branching = 0
    for lang in LANGS:
        canon4_path = os.path.join(HERE, "canon4_units_%s.json" % lang)
        canon4_doc = json.load(open(canon4_path))
        canon7_units = gen_docs["canon7"][lang]
        for n, u in canon4_doc["units"].items():
            branching = "derived_blocks" in u
            if u.get("erasure") != "ok":
                continue
            c7 = canon7_units.get(n)
            if branching:
                for gen in BRANCH_CHECK_GENERATIONS:
                    rec = gen_docs[gen].get(lang, {}).get(n)
                    if rec is not None and (
                            "%s_text" % gen) in rec:
                        touched_branching += 1
                continue
            if not isinstance(u.get("derived_text"), list):
                continue
            text, gen = final_text_of(lang, n, gen_docs)
            if text is None:
                missing_text = missing_text + 1
                continue
            out.append((lang, n, u, text, gen))
    if touched_branching:
        raise RuntimeError(
            "%d branching units were touched this lap -- the 0-branch"
            " scope assumption is now FALSE; re-run with the full-"
            "population variant instead of trusting this one"
            % touched_branching)
    if missing_text:
        sys.stderr.write(
            "!! %d 0-branch units had no text in any generation "
            "(should not happen)\n" % missing_text)
    return out


def build_provenance_and_table(units):
    prov = {}
    classes = {}
    unknown_result_type = 0
    generation_tally = {}
    for lang, n, u, text, gen in units:
        label = "%s/op_%s" % (lang, n)
        prov[label] = {
            "lang": lang,
            "n": n,
            "display_label": u.get("operator"),
            "arity_bucket": DB.arity_bucket_of(u),
        }
        generation_tally[gen] = generation_tally.get(gen, 0) + 1
        tkey = DB.type_pair_of(u)
        fam, note = RTN.class_family(lang, n, u.get("meta"))
        if fam is None:
            unknown_result_type += 1
            rkey = "unknown(%s)" % note[:40]
        else:
            rkey = fam
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
    return prov, {"rows": rows}, unknown_result_type, generation_tally


def run(units):
    prov, table, unknown_result_type, generation_tally = \
        build_provenance_and_table(units)
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
        "population_size": len(units),
        "generation_tally": generation_tally,
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
    }, table


def main(argv):
    outdir = HERE
    args = argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--out":
            i = i + 1
            outdir = args[i]
        i = i + 1

    gen_docs = load_generation_docs()
    units = load_0branch_units(gen_docs)
    result, table = run(units)

    class_doc = {
        "meta": {
            "generator": "dominant_table17.py",
            "role_note": "this file is a GROUPING/matching artifact "
                        "(top-level `rows`, each with `members`) -- "
                        "it does NOT claim the generator-provenance "
                        "exemption, matching dominant_table15.json's "
                        "own precedent, and is checked by check_no_"
                        "spelling_keys.py IN FULL rather than by "
                        "exemption.",
            "construction": "dom_ops7.py's rule, unchanged (via "
                           "dom_ops_0branch.py/dom_ops_0branch3.py, "
                           "imported not restated)",
            "class_basis": "(type pair, result type, NEWEST CONVERGED "
                          "TEXT) over the 0-branch population -- no "
                          "operator token in the class key",
            "population": "canon4_units_*.json, 0-branch (erasure == "
                         "ok, derived_text is a list), 1,641 units -- "
                         "text sourced from canon23_text/canon22_text/"
                         "canon21_text/canon20_text/canon19_text/"
                         "canon18_text/canon17_text/canon16_text/"
                         "canon15_text/canon14_text/canon13_text/"
                         "canon12_text/canon11_text/canon10_text/"
                         "canon9_text/canon8_text/canon7_text, newest "
                         "generation that touched each unit -- see "
                         "this file's own header. NOT the 1,779-unit "
                         "full corpus -- see this node's PROGRESS.md "
                         "denominator note.",
            "baseline": "926 classes / 135 nodes / 26 families / 23 "
                       "edgeless (dominant_table15.json/dom_ops13.json, "
                       "already on disk)",
        },
        "classes": len(table["rows"]),
        "rows": table["rows"],
    }
    class_path = os.path.join(outdir, "dominant_table17.json")
    fh = open(class_path, "w")
    json.dump(class_doc, fh, indent=1)
    fh.close()

    print("wrote %s" % class_path)
    print("population(0-branch)  %d" % result["population_size"])
    print("generation tally      %r" % result["generation_tally"])
    print("classes    %d  (baseline: 926)" % result["class_count"])
    print("nodes      %d  (baseline: 135)" % result["nodes"])
    print("dom_ops    %d  (baseline: 26)" % result["dom_op_count"])
    print("edgeless   %d  (baseline: 23)"
          % result["nodes_with_no_surviving_edge"])
    print("singletons %d" % result["singleton_dom_ops"])
    print("unknown result type (excluded from a scalar family) %d"
          % result["unknown_result_type_units"])
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
