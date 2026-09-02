#!/usr/bin/env python3
"""dominant_table13.py -- re-run the class table and dom_op construction
on THIS LAP'S newest converged text per unit (JOB 1/canon14_render.py,
JOB 2/canon15.py + condition_table3.py, JOB 3/canon16.py + canon16_xmm.py's
own accepted candidates, layered on top of canon13/12/11's Stage 1-4
work and everything before it).

Byte-for-byte the SAME construction dominant_table12.py already used
(dom_ops7.py's rule via dom_ops_0branch.py/dom_ops_0branch3.py, imported
not restated; result_type_norm.py's DWARF-machine-fact result type) --
the ONLY change is GENERATIONS, extended with this lap's THREE new
generations (canon16, canon15, canon14) ahead of the ones
dominant_table12.py already knew about. `final_text_of` already reads
"newest generation whose <gen>_text field is present", so a unit none
of this lap's jobs touched keeps falling through to its canon13_text
(or further) exactly as before -- no other logic changes.

SCOPE: 0-BRANCH POPULATION ONLY, same population-integrity assumption
dominant_table12.py already asserts (this lap's drivers -- canon14.py/
canon15.py/canon16.py -- each explicitly skip any unit whose
branch_kind isn't "straight_line" (canon14/15) or whose meta shape is
not the unary float-negate this lap's own canon16.py targets, itself
already a 0-branch-only population), so this lap cannot have touched a
branching unit; the SAME "refuse silently-wrong scope" check is kept,
now widened to cover canon16/canon15/canon14 too.

BASELINE (dominant_table12.json/dom_ops10.json, already on disk,
produced before this lap's JOB 1-3 work, matching the task's own cited
figures): 926 classes / 135 nodes / 26 families / 23 edgeless.

THE SPELLING BAN: unchanged, same as dominant_table12.py -- the class key
never includes the operator token, only type reps, result type, and
canon-text; the token is read exactly once per node as `display_label`.
check_no_spelling_keys.py is run on both outputs before this program
declares success (see the driver invocation after main() runs).

usage:
  dominant_table13.py [--out DIR]
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

GENERATIONS = ["canon16", "canon15", "canon14", "canon13", "canon12",
               "canon11", "canon10", "canon9", "canon8", "canon7"]

BRANCH_CHECK_GENERATIONS = ("canon16", "canon15", "canon14", "canon13",
                             "canon12", "canon11", "canon10", "canon9",
                             "canon8")


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
    text field is present in, this lap. Falls back to canon5_text
    (present on every canon7 record) if no generation ever touched
    it, which is the untouched-unit case."""
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
                # population-integrity check, widened for this lap's
                # three new generations -- refuse silently-wrong scope
                # if JOB 1-3 (or any earlier job) DID touch a
                # branching unit's text.
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
            "generator": "dominant_table13.py",
            "role_note": "this file is a GROUPING/matching artifact "
                        "(top-level `rows`, each with `members`) -- "
                        "it does NOT claim the generator-provenance "
                        "exemption (unlike dom_ops11.json beside it), "
                        "matching dominant_table12.json's own "
                        "precedent, and is checked by check_no_"
                        "spelling_keys.py IN FULL rather than by "
                        "exemption.",
            "construction": "dom_ops7.py's rule, unchanged (via "
                           "dom_ops_0branch.py/dom_ops_0branch3.py, "
                           "imported not restated)",
            "class_basis": "(type pair, result type, THIS LAP'S "
                          "FINAL CONVERGED TEXT) over the 0-branch "
                          "population -- no operator token in the "
                          "class key",
            "population": "canon4_units_*.json, 0-branch (erasure == "
                         "ok, derived_text is a list), text sourced "
                         "from canon16_text/canon15_text/canon14_text/"
                         "canon13_text/canon12_text/canon11_text/"
                         "canon10_text/canon9_text/canon8_text/"
                         "canon7_text, newest generation that touched "
                         "each unit -- see this file's own header",
            "baseline": "926 classes / 135 nodes / 26 families / 23 "
                       "edgeless (dominant_table12.json/dom_ops10.json, "
                       "already on disk, produced before this lap's "
                       "JOB 1-3 work -- the task's own cited figures)",
        },
        "classes": len(table["rows"]),
        "rows": table["rows"],
    }
    class_path = os.path.join(outdir, "dominant_table13.json")
    fh = open(class_path, "w")
    json.dump(class_doc, fh, indent=1)
    fh.close()

    dom_ops_doc = {
        "meta": {
            "role": "generator provenance",
            "generator": "dominant_table13.py",
            "note": "the dom_op (family) construction over the SAME "
                   "population/class table as dominant_table13.json "
                   "-- written to dom_ops11.json, the next number "
                   "after dom_ops10.json",
        },
        "population_size": result["population_size"],
        "generation_tally": result["generation_tally"],
        "class_count": result["class_count"],
        "unknown_result_type_units": result["unknown_result_type_units"],
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
    dom_ops_path = os.path.join(outdir, "dom_ops11.json")
    fh = open(dom_ops_path, "w")
    json.dump(dom_ops_doc, fh, indent=1)
    fh.close()

    print("wrote %s" % class_path)
    print("wrote %s" % dom_ops_path)
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
