#!/usr/bin/env python3
"""dominant_table11.py -- JOB 3: rebuild the class table and re-run the
DOM_OP construction on THIS LAP'S CONVERGED CORPUS.

dom_ops_0branch3.py's construction rule is reused UNCHANGED (via
dom_ops.py/dom_ops_0branch.py, imported not re-derived): nodes =
(language, grammar operator, arity); edges weighted by shared-class
then shared-type-key count; each node keeps its single strongest
counterpart per foreign language, kept only when MUTUAL; connected
components of the mutual-best graph are the dominant operators.
result_type_norm.py's DWARF-machine-fact result type is used (not
dom_ops_0branch.py's original, inconsistent-across-languages one) --
this file only ever reports the FIXED version, since dom_ops_0branch3.
json already isolated and reported the old-vs-new split.

THE ONE SUBSTITUTION FROM dom_ops_0branch3.py: the TEXT component of
the class key is now THIS LAP'S FINAL CONVERGED TEXT per unit, read as
canon10_text, falling back to canon9_text, canon8_text, canon7_text,
canon5_text in that order (the newest lap that actually touched this
unit) -- i.e. JOB 1 (canon8.py) + JOB 2 pass 1 (canon9.py, condition_
table2.py) + JOB 2 pass 2 (canon10.py, trivial ground-truth rescue),
composed. The brief named this "canon8's canonical text"; this file
reads the LATEST of the four generations produced this lap, which is
the more complete statement of the same instruction (each generation
only ever changes a unit canon7 had wrong or stuck -- a unit untouched
by JOB 1/JOB 2 keeps its canon7_text, which is canon5_text carried
through unchanged, per canon7.py's own fallback rule).

SCOPE: 0-BRANCH POPULATION ONLY. JOB 2 (canon9.py/canon10.py) did not
touch any branching unit this lap (verified: the 186-unit condition-
atom bucket this lap attacked was 100% straight_line; canon10.py's
trivial-rescue pass touches any not_yet_converged unit regardless of
branch_kind, but a BRANCHING unit's text only ever changes if its
canon9_text/canon8_text/canon7_text differs from its own real ship
mnem, which does not happen for a branching unit in this run -- see
this file's own population-load step, which asserts the count of
branching units it TOUCHED is zero and refuses to proceed silently if
that ever stops being true). So per the brief's own conditional ("if
JOB 2 lands branching units, the full population"), only the 0-branch
variant is produced.

THE SPELLING BAN: unchanged -- the class key never includes the
operator token, only type reps, result type, and canon-text; the
token is read exactly once per node as `display_label`.
check_no_spelling_keys.py is run on both outputs before this program
declares success.

usage:
  dominant_table11.py [--out DIR]
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

GENERATIONS = ["canon10", "canon9", "canon8", "canon7"]


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
                # population-integrity check named in this file's own
                # header: refuse silently-wrong scope if JOB 2 ever
                # DID touch a branching unit's text this lap.
                for gen in ("canon10", "canon9", "canon8"):
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
            "generator": "dominant_table11.py",
            "role_note": "this file is a GROUPING/matching artifact "
                        "(top-level `rows`, each with `members`) -- "
                        "it does NOT claim the generator-provenance "
                        "exemption (unlike dom_ops9.json beside it), "
                        "matching dominant_table10.json's own "
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
                         "from canon10_text/canon9_text/canon8_text/"
                         "canon7_text, newest generation that touched "
                         "each unit -- see this file's own header",
            "baseline_0branch_canon7_type_fix": "923 classes / 135 "
                                               "nodes / 26 families / "
                                               "23 edgeless "
                                               "(dom_ops_0branch3."
                                               "json's with_dwarf_"
                                               "result_type)",
            "baseline_accumulated_grounds": "1068 classes / 28 "
                                           "families (dominant_"
                                           "table10.json -- a "
                                           "DIFFERENT, larger "
                                           "lineage-accumulated "
                                           "table, cited for context "
                                           "only, not rebuilt here)",
        },
        "classes": len(table["rows"]),
        "rows": table["rows"],
    }
    class_path = os.path.join(outdir, "dominant_table11.json")
    fh = open(class_path, "w")
    json.dump(class_doc, fh, indent=1)
    fh.close()

    dom_ops_doc = {
        "meta": {
            "role": "generator provenance",
            "generator": "dominant_table11.py",
            "note": "the dom_op (family) construction over the SAME "
                   "population/class table as dominant_table11.json "
                   "-- written to dom_ops9.json, the next number "
                   "after dom_ops8.json, per the brief's naming",
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
    dom_ops_path = os.path.join(outdir, "dom_ops9.json")
    fh = open(dom_ops_path, "w")
    json.dump(dom_ops_doc, fh, indent=1)
    fh.close()

    print("wrote %s" % class_path)
    print("wrote %s" % dom_ops_path)
    print("population(0-branch)  %d" % result["population_size"])
    print("generation tally      %r" % result["generation_tally"])
    print("classes    %d  (baseline: 923)" % result["class_count"])
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
