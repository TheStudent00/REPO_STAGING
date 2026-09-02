#!/usr/bin/env python3
"""build_table23.py -- JOB 3 (log_082 lap): REBUILD THE CLASS TABLE AND
dom_ops ON THE NEWEST TEXT PER UNIT, canon24 included.

METHOD, stated plainly because this lap deliberately does NOT reuse
representatives5.json's own proved-equivalence substitution (build_
table21.py's own method, the one that produced the on-disk 919/139/
26/23 baseline this lap was told to compare against): representatives5
.json was built BEFORE canon24 existed, so every one of JOB 1's 42
newly-converged units still carries its OLD (pre-canon24, unconverged)
text inside that file's own groups -- reusing it unchanged would leave
the class table blind to JOB 1's own convergence work, defeating this
job's own purpose. Regenerating representatives5.json itself (re-
running cross_unit_prover.py's own proof sweep) is a DIFFERENT lap's
job, out of scope here. So this file follows dominant_table17.py's own
DIRECT method instead -- (type pair, result type, NEWEST GENERATION'S
OWN TEXT) as the class key, generation fall-through only, no
representative substitution -- extended with canon24 at the front of
the fall-through order. THE COMPARISON THIS ENTAILS, stated honestly:
dominant_table17.json's OWN un-represented baseline (926 classes / 135
nodes / 26 dom_ops / 23 edgeless, 0-branch only) is the apples-to-
apples number for THIS file's own method; the task's stated 919/139/
26/23 is the REPRESENTATIVE-substituted lineage's own number (dom_
ops20.json over dominant_table22.json) -- both are reported below,
named by which method produced each.

STEP 1 (0-branch, 1,641 units): dominant_table17.py's own `load_
generation_docs`/`load_0branch_units`, monkeypatched (GENERATIONS/
BRANCH_CHECK_GENERATIONS with "canon24" prepended -- the SAME "extend
the fall-through order, touch nothing else" change canon21/22/23 each
made to dominant_table15/17.py in turn) then a direct re-port of
dominant_table17.build_provenance_and_table, with the class's own
canonical TEXT kept on the row (dominant_table17.py's own rows do not
carry it -- needed here, step 2, to match a branching unit's seed
text against the newly-built classes, since seeds1.json's own
`matched_class` IDs are dominant_table21.json's row numbering, not
this file's own).

STEP 2 (branching units, build_table22.py's own rule, reused
UNCHANGED IN SHAPE): each of seeds1.json's "ok" seeds is joined to
whichever of THIS file's own classes has the identical canonical text
-- by TEXT EQUALITY, not by copying build_table22.py's own stale class
IDs across. A seed matching zero or more than one class here is
reported, honestly, never guessed.

STEP 3: dom_ops over the FULL (0-branch + branching) table, dom_ops7
.py's rule via dom_ops_0branch.py (imported, unchanged) -- byte-
identical construction to dom_ops19/20.py's own.

THE SPELLING BAN: unchanged -- the class key is (type pair, result
type, canonical text), never the operator token; `operator` is
recorded exactly once per node as `display_label` (dom_ops_0branch.py's
own convention, untouched). check_no_spelling_keys.py is run on the
output before this program declares success.

usage:
  build_table23.py [--out DIR]
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

DT17.GENERATIONS = ["canon24"] + DT17.GENERATIONS
DT17.BRANCH_CHECK_GENERATIONS = tuple(
    ["canon24"] + list(DT17.BRANCH_CHECK_GENERATIONS))

TASK_BASELINE = dict(classes=919, nodes=139, dom_ops=26, edgeless=23)
DIRECT_METHOD_BASELINE = dict(classes=926, nodes=135, dom_ops=26,
                               edgeless=23)


def build_0branch_classes(units):
    """dominant_table17.build_provenance_and_table, re-ported so each
    row ALSO carries its own canonical `text` (needed by step 2's own
    text-equality seed match) -- everything else byte-identical."""
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
        classes.setdefault(ckey, {"type_pair": tkey, "text": text,
                                   "members": []})
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
            "canonical_text": rec["text"],
            "members": rec["members"],
        })
    return prov, rows, unknown_result_type, generation_tally


def add_branching_members(rows):
    """STEP 2. Returns (added, unmatched, ambiguous) -- see file
    header."""
    seeds = json.load(open(os.path.join(HERE, "seeds1.json")))["seeds"]
    text_to_rows = {}
    for row in rows:
        text_to_rows.setdefault(row["canonical_text"], []).append(row)

    added = []
    unmatched = []
    ambiguous = []
    for unit_id, s in seeds.items():
        if s.get("status") != "ok":
            continue
        seed_text = s.get("seed_text")
        candidates = text_to_rows.get(seed_text, [])
        if len(candidates) == 0:
            unmatched.append({
                "unit": unit_id, "seed_text": seed_text,
                "old_matched_class": s.get("matched_class"),
                "note": "no class in THIS table has this seed's exact "
                        "canonical text -- the class its seed used to "
                        "match (dominant_table21.json's %s) either "
                        "changed text under canon24 or never existed "
                        "in this method's own construction"
                        % s.get("matched_class"),
            })
            continue
        if len(candidates) > 1:
            ambiguous.append({
                "unit": unit_id, "seed_text": seed_text,
                "candidate_classes": [c["class_id"] for c in candidates],
            })
            continue
        row = candidates[0]
        row["members"].append({
            "unit": unit_id,
            "branching": True,
            "seed_text": s["seed_text"],
            "seed_method": s["method"],
            "guards": s["guards"],
        })
        added.append((unit_id, row["class_id"]))
    return added, unmatched, ambiguous


def run_dom_ops(rows, prov):
    doc = {"table": {"rows": rows}}
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
        "nodes": len(nodes),
        "edges_raw": len(edges),
        "edges_mutual": len(kept),
        "dom_op_count": len(comps),
        "singleton_dom_ops": singleton_count,
        "nodes_in_a_dom_op": len(attached),
        "nodes_with_no_surviving_edge": len(unattached),
        "unattached_nodes": [DB.node_row(nodes, nid) for nid in
                              unattached],
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

    gen_docs = DT17.load_generation_docs()
    units = DT17.load_0branch_units(gen_docs)
    prov, rows, unknown_result_type, generation_tally = \
        build_0branch_classes(units)

    added, unmatched, ambiguous = add_branching_members(rows)

    class_doc = {
        "meta": {
            "generator": "build_table23.py",
            "role_note": "GROUPING/matching artifact (top-level `rows`,"
                         " each with `members`) -- checked by check_no_"
                         "spelling_keys.py IN FULL, no exemption "
                         "claimed.",
            "construction": "dominant_table17.py's own direct method "
                            "(type pair, machine-fact result type, "
                            "NEWEST GENERATION TEXT) -- generation "
                            "fall-through extended with canon24 ahead "
                            "of canon23/22/21/..., NOT representatives5"
                            ".json's proved-equivalence substitution "
                            "(see this file's own header for why).",
            "population": "1,779 full corpus: %d 0-branch (generation-"
                          "fallthrough text, canon24 included) + %d "
                          "branching units joined to an existing class "
                          "by exact seed-text equality (%d seeds could "
                          "not be matched under this method's own "
                          "class texts, %d were ambiguous -- see "
                          "unmatched_branching_seeds/ambiguous_"
                          "branching_seeds below)"
                          % (len(units), len(added), len(unmatched),
                             len(ambiguous)),
            "generation_tally": generation_tally,
            "unknown_result_type_units": unknown_result_type,
            "task_baseline_representative_lineage":
                "919 classes / 139 nodes / 26 dom_ops / 23 edgeless "
                "(dom_ops20.json over dominant_table22.json, the "
                "representatives5.json-substituted lineage)",
            "direct_method_own_baseline":
                "926 classes / 135 nodes / 26 dom_ops / 23 edgeless "
                "(dominant_table17.json/dom_ops -- THIS file's own "
                "method, pre-canon24, 0-branch only)",
        },
        "classes": len(rows),
        "unmatched_branching_seeds": unmatched,
        "ambiguous_branching_seeds": ambiguous,
        "rows": rows,
    }

    dom_ops_result = run_dom_ops(rows, prov)

    class_path = os.path.join(outdir, "dominant_table23.json")
    json.dump(class_doc, open(class_path, "w"), indent=1)

    dom_ops_doc = {
        "meta": {
            "generator": "build_table23.py (dom_ops21.json)",
            "role": "generator provenance",
            "note": "the dom_op (family) construction over dominant_"
                    "table23.json's own class rows (JOB 3, log_082 "
                    "lap, canon24 included).",
            "construction": "dom_ops7.py's rule, unchanged (via dom_"
                            "ops_0branch.py, imported not restated): "
                            "nodes = (language, grammar operator, "
                            "arity); edges weighted by shared-class "
                            "then shared-type-key count; mutual-"
                            "strongest per foreign language; connected "
                            "components of the mutual-best graph",
            "source_table": "dominant_table23.json",
        },
        "class_count": len(rows),
    }
    dom_ops_doc.update(dom_ops_result)
    dom_ops_path = os.path.join(outdir, "dom_ops21.json")
    json.dump(dom_ops_doc, open(dom_ops_path, "w"), indent=1)

    print("wrote %s" % class_path)
    print("wrote %s" % dom_ops_path)
    print()
    print("population(0-branch)  %d" % len(units))
    print("branching added       %d  unmatched %d  ambiguous %d"
          % (len(added), len(unmatched), len(ambiguous)))
    print("generation tally      %r" % generation_tally)
    print()
    print("classes    %d  (task baseline: %d | direct-method baseline: %d)"
          % (len(rows), TASK_BASELINE["classes"],
             DIRECT_METHOD_BASELINE["classes"]))
    print("nodes      %d  (task baseline: %d | direct-method baseline: %d)"
          % (dom_ops_result["nodes"], TASK_BASELINE["nodes"],
             DIRECT_METHOD_BASELINE["nodes"]))
    print("dom_ops    %d  (task baseline: %d | direct-method baseline: %d)"
          % (dom_ops_result["dom_op_count"], TASK_BASELINE["dom_ops"],
             DIRECT_METHOD_BASELINE["dom_ops"]))
    print("edgeless   %d  (task baseline: %d | direct-method baseline: %d)"
          % (dom_ops_result["nodes_with_no_surviving_edge"],
             TASK_BASELINE["edgeless"],
             DIRECT_METHOD_BASELINE["edgeless"]))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
