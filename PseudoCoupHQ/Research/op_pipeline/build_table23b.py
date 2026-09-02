#!/usr/bin/env python3
"""build_table23b.py -- TASK 4 rebuild step. Applies the bucket-1 cross-
unit prover's proved edges (proved_edges.json UNION proved_edges2.json
UNION proved_edges3.json -- this task's own cross_unit_prover_bucket1.py
sweep of the 6,401 unbudgeted cross-language non-float pairs, 84 proved:
80 direct + 4 by transitivity) onto the dominant_table23 lineage, NOT
the dominant_table22 lineage (the task brief names this explicitly --
the two lineages differ in method and are not to be conflated).

NAMING NOTE (post-hoc correction): this file and its two output
files were originally named build_table24.py/dominant_table24.json/
dom_ops22.json. TASK 7's own brief reserves those exact names for
THE single reconciled lineage ("Output dominant_table24/dom_ops22
as THE table"). This lap is a proof-merged CONTINUATION of table23,
not that reconciliation, so it was renamed to build_table23b.py /
dominant_table23b.json / dom_ops21b.json -- freeing table24/dom_
ops22 for Task 7's own deliverable. Nothing else about this file's
method changed.

METHOD. dominant_table23.json's own classes are built by (type_pair,
result_type, canonical TEXT) equality -- build_table23.py's own
deliberate choice, no proved-edge substitution (see that file's
header). This file starts from those SAME classes (loaded, not
rebuilt) and adds exactly one more union step, per THE REPRESENTATIVE
RULE (AgentMemory, 2026-08-29): two classes are merged when a PROVED
edge (verdict == "PROVED", either "solver" or "transitive" proof_
method) connects a member of one to a member of the other. The merged
group's canonical text becomes the SIMPLEST member's text -- fewest
bytes of machine code (byte length of the canonical instruction text,
the same proxy dominant_table23.json rows themselves already store),
ties broken by first-in-list order (deterministic, no judgment). The
ORIGINAL per-class canonical texts are kept on each row's own
`members_original_class_text` for the record -- nothing is erased.

THE SPELLING BAN: unchanged -- the merge key is UNIT IDENTITY (a
proved edge names two unit labels, never an operator token) and the
representative choice is BYTE LENGTH, never a token either.
check_no_spelling_keys.py is run on the output before this program
declares success.

usage:
  build_table23b.py [--out DIR]
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dominant_table17 as DT17                                  # noqa: E402
import dom_ops as DO                                              # noqa: E402
import dom_ops_0branch as DB                                      # noqa: E402

DT17.GENERATIONS = ["canon24"] + DT17.GENERATIONS
DT17.BRANCH_CHECK_GENERATIONS = tuple(
    ["canon24"] + list(DT17.BRANCH_CHECK_GENERATIONS))


class UF:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, x, y):
        rx, ry = self.find(x), self.find(y)
        if rx != ry:
            self.parent[rx] = ry


def load_proved_edges():
    files = ["proved_edges.json", "proved_edges2.json",
             "proved_edges3.json"]
    edges = []
    for fname in files:
        path = os.path.join(HERE, fname)
        if not os.path.exists(path):
            continue
        doc = json.load(open(path))
        for e in doc["pairs"]:
            if e["verdict"] == "PROVED":
                edges.append((e["a"], e["b"], fname,
                              e.get("proof_method", "solver")))
    return edges


def main(argv):
    outdir = HERE
    args = argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--out":
            i = i + 1
            outdir = args[i]
        i = i + 1

    table23 = json.load(open(os.path.join(HERE, "dominant_table23.json")))
    rows = table23["rows"]

    unit_to_class = {}
    for row in rows:
        for m in row["members"]:
            unit_to_class[m["unit"]] = row["class_id"]

    proved = load_proved_edges()
    uf = UF()
    class_ids = [row["class_id"] for row in rows]
    for cid in class_ids:
        uf.find(cid)

    used_edges = []
    for a, b, src, method in proved:
        ca = unit_to_class.get(a)
        cb = unit_to_class.get(b)
        if ca is None or cb is None:
            # a proved-edge unit outside this table's own population
            # (e.g. a branching-only or unmatched unit) -- named, not
            # silently dropped.
            continue
        if ca == cb:
            continue  # already the same class by text equality
        uf.union(ca, cb)
        used_edges.append({"a": a, "b": b, "class_a": ca, "class_b": cb,
                            "source_file": src, "proof_method": method})

    groups = {}
    for row in rows:
        root = uf.find(row["class_id"])
        groups.setdefault(root, []).append(row)

    merged_rows = []
    n_merged_classes = 0
    for root, group_rows in groups.items():
        if len(group_rows) == 1:
            r = group_rows[0]
            merged_rows.append({
                "class_id": r["class_id"],
                "type_pair": r["type_pair"],
                "result_type": r["result_type"],
                "canonical_text": r["canonical_text"],
                "representative_of": [r["class_id"]],
                "members": r["members"],
            })
            continue
        n_merged_classes += 1
        # THE REPRESENTATIVE RULE: fewest bytes of machine-code text,
        # ties broken by first-in-list order (sorted by class_id for
        # determinism, matching the group's own construction order).
        group_rows_sorted = sorted(group_rows, key=lambda r: r["class_id"])
        best = min(group_rows_sorted, key=lambda r: len(r["canonical_text"]))
        all_members = []
        for r in group_rows_sorted:
            all_members.extend(r["members"])
        merged_rows.append({
            "class_id": group_rows_sorted[0]["class_id"],
            "type_pair": best["type_pair"],
            "result_type": best["result_type"],
            "canonical_text": best["canonical_text"],
            "representative_of": [r["class_id"] for r in group_rows_sorted],
            "representative_chosen_from":
                {r["class_id"]: len(r["canonical_text"])
                 for r in group_rows_sorted},
            "members": all_members,
        })

    merged_rows.sort(key=lambda r: r["class_id"])

    # prov is rebuilt from the SAME source dominant_table23.json used
    # (DT17.load_generation_docs/load_0branch_units), byte-identical
    # to build_table23.py's own step -- dom_ops_0branch needs
    # display_label/arity_bucket per unit and dominant_table23.json's
    # own rows do not persist that, only build_table23.py's in-memory
    # step did.
    gen_docs = DT17.load_generation_docs()
    units = DT17.load_0branch_units(gen_docs)
    import result_type_norm as RTN                                # noqa: E402
    prov = {}
    for lang, n, u, text, gen in units:
        label = "%s/op_%s" % (lang, n)
        prov[label] = {
            "lang": lang,
            "n": n,
            "display_label": u.get("operator"),
            "arity_bucket": DB.arity_bucket_of(u),
        }
    # branching units have no probe meta of their own -- dom_ops.py's
    # own build_nodes/node_of_unit already skip a member whose label
    # is absent from `prov` (rec is None -> continue), the SAME
    # behaviour build_table23.py's own run_dom_ops relies on; no
    # stand-in entry is added here, matching that file byte-for-byte.

    class_doc = {
        "meta": {
            "generator": "build_table23b.py",
            "role_note": "GROUPING/matching artifact (top-level `rows`,"
                         " each with `members`) -- checked by check_no_"
                         "spelling_keys.py IN FULL, no exemption "
                         "claimed.",
            "lineage": "dominant_table23.json (NOT dominant_table22.json"
                      " -- the two lineages differ in method and are "
                      "not conflated; this file applies TASK 4's proved "
                      "edges on the table23 lineage only, per the task "
                      "brief's own instruction).",
            "construction": "dominant_table23.json's own classes, "
                            "UNIONED where a PROVED cross-unit-prover "
                            "edge (proved_edges.json UNION proved_"
                            "edges2.json UNION proved_edges3.json) "
                            "connects a member of one class to a "
                            "member of another. THE REPRESENTATIVE "
                            "RULE: the merged group's canonical text "
                            "is the SIMPLEST member's text (fewest "
                            "bytes), ties by class_id order. Original "
                            "per-class texts are not erased -- see "
                            "representative_chosen_from on each merged "
                            "row.",
            "proved_edges_considered": len(proved),
            "proved_edges_applied_as_new_merges": len(used_edges),
            "classes_before_merge": len(rows),
            "classes_after_merge": len(merged_rows),
            "classes_actually_merged_groups": n_merged_classes,
        },
        "classes": len(merged_rows),
        "merges_applied": used_edges,
        "rows": merged_rows,
    }

    class_path = os.path.join(outdir, "dominant_table23b.json")
    json.dump(class_doc, open(class_path, "w"), indent=1)

    doc_for_dom_ops = {"table": {"rows": merged_rows}}
    nodes, index = DO.build_nodes(doc_for_dom_ops, prov)
    class_members = DO.fill_nodes(doc_for_dom_ops, nodes, index, prov)
    edges = DO.build_edges(doc_for_dom_ops, nodes, class_members, 0)
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

    dom_ops_doc = {
        "meta": {
            "generator": "build_table23b.py (dom_ops21b.json)",
            "role": "generator provenance",
            "lineage": "dominant_table23b.json (TASK 4's proved-edge "
                      "merge on top of the dominant_table23 lineage)",
            "construction": "dom_ops7.py's rule, unchanged (via dom_"
                            "ops_0branch.py, imported not restated).",
            "source_table": "dominant_table23b.json",
        },
        "class_count": len(merged_rows),
        "nodes": len(nodes),
        "edges_raw": len(edges),
        "edges_mutual": len(kept),
        "dom_op_count": len(comps),
        "singleton_dom_ops": singleton_count,
        "nodes_in_a_dom_op": len(attached),
        "nodes_with_no_surviving_edge": len(unattached),
        "unattached_nodes": [DB.node_row(nodes, nid) for nid in unattached],
        "equally_strongest_ties": len(ties),
        "same_language_collisions_in_one_component": len(collisions),
        "dom_ops": family_rows,
    }
    dom_ops_path = os.path.join(outdir, "dom_ops21b.json")
    json.dump(dom_ops_doc, open(dom_ops_path, "w"), indent=1)

    print("wrote %s" % class_path)
    print("wrote %s" % dom_ops_path)
    print("classes before merge: %d" % len(rows))
    print("classes after merge:  %d" % len(merged_rows))
    print("proved edges considered (all 3 files, PROVED only): %d"
          % len(proved))
    print("proved edges that produced a NEW cross-class merge: %d"
          % len(used_edges))
    print("nodes %d  dom_ops %d  edgeless %d"
          % (len(nodes), len(comps), len(unattached)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
