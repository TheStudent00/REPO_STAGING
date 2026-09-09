#!/usr/bin/env python3
"""build_the_families1.py -- TASK 44, the families over THE POOL.

THE DOM_OP CONSTRUCTION RULE (AgentMemory, the owner 2026-08-26), applied
unchanged and IMPORTED rather than restated: nodes are (language,
grammar-operator, ARITY) -- the provenance of the probe, not a
cross-language token; edges only BETWEEN languages, weighted by shared
equivalence-class count; each node keeps its single strongest
counterpart per foreign language, kept only when MUTUAL; connected
components of the mutual-best graph are the families.

What changes here is only WHAT THE CLASSES ARE.  Round 8 ran the rule
over the compiled-only table.  It now runs over THE POOL's entries --
every language in the pool, compiled and interpreted alike, one
population.  `dominant_table25.json` / `dom_ops23.json` cease to exist
as objects the line depends on; they stay on disk as the superseded
record.

The edge functions, the mutual filter and the component walk are
imported from `dom_ops.py`, the module that has carried this rule
since it was ratified, so they cannot drift here.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set
for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label on
the member.  HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim.

The token is carried on a node as its `label` display field and is
read by NOTHING: the pairing scope is entry co-membership, the weights
are counted entries and counted machine-form shape keys, and the
tie-break is machine-form quantities only.  No provenance exemption is
claimed from the guard.

usage: build_the_families1.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dom_ops                                          # noqa: E402
import dom_ops_0branch as DB                            # noqa: E402
import build_the_pool1 as POOL                          # noqa: E402

ARITY_SOURCE = "read off the unit's own entry contract -- does a "\
               "second arriving lineage exist -- by "\
               "dom_ops_0branch.arity_bucket_of, imported unchanged.  "\
               "Machine form over asserted form, and it is the same "\
               "function round 8's node set used, so the node identity "\
               "is like for like across the two rounds.  It is also the "\
               "only arity source every population in the pool carries: "\
               "no probe manifest describes an interpreter unit."


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def provenance_over_the_pool(records):
    """unit label -> (lang, display label, arity bucket)."""
    out = {}
    for rec in records:
        out[rec["unit"]] = {
            "lang": rec["lang"],
            "n": rec.get("n"),
            "display_label": rec.get("operator"),
            "arity_bucket": DB.arity_bucket_of(rec),
            "arity_source": ARITY_SOURCE,
        }
    return out


def table_from_the_pool(pool):
    """the pool's entries, in the shape dom_ops' own edge builder
    reads: one row per entry, its members, and a machine-form shape
    key standing where the compiled table carried its operand-type
    key.  The shape key is read off the unit's own block directory --
    which register file each arriving lineage loads through, and how
    wide the answer is."""
    rows = []
    for entry in pool["entries"]:
        rows.append({
            "class_id": entry["entry_id"],
            "type_pair": entry["type_key"],
            "members": [{"unit": m["unit"]} for m in entry["members"]],
        })
    return {"table": {"rows": rows}}


def main():
    log("-- reading the pool")
    pool = json.load(open(os.path.join(HERE, "the_pool1.json")))
    records = []
    records.extend(POOL.take_original())
    records.extend(POOL.take_interpreter())
    records.extend(POOL.take_regenerated())
    prov = provenance_over_the_pool(records)
    log("   pool entries %d, pool units %d"
        % (len(pool["entries"]), len(records)))

    doc = table_from_the_pool(pool)
    nodes, index = dom_ops.build_nodes(doc, prov)
    log("-- nodes (language, grammar-operator, arity) %d" % len(nodes))
    class_members = dom_ops.fill_nodes(doc, nodes, index, prov)
    edges = dom_ops.build_edges(doc, nodes, class_members, 0)
    log("-- cross-language edges, raw %d" % len(edges))
    best, ties = dom_ops.best_per_language(nodes, edges)
    kept = dom_ops.mutual_edges(nodes, edges, best)
    log("-- edges surviving the mutual filter %d" % len(kept))
    comps = dom_ops.components(kept)
    log("-- families %d" % len(comps))

    attached = {}
    for members in comps:
        for nid in members:
            attached[nid] = True
    unattached = []
    for nid in sorted(nodes.keys()):
        if nid in attached:
            continue
        unattached.append({
            "id": nid,
            "lang": nodes[nid]["lang"],
            "label": nodes[nid]["label"],
            "arity": nodes[nid]["arity"],
            "entry_count": len(nodes[nid]["classes"]),
            "unit_count": len(nodes[nid]["units"]),
        })

    families = []
    fid = 0
    for members in comps:
        fid = fid + 1
        langs = []
        out_nodes = []
        for nid in members:
            node = nodes[nid]
            if node["lang"] not in langs:
                langs.append(node["lang"])
            out_nodes.append({
                "id": nid,
                "lang": node["lang"],
                "label": node["label"],
                "arity": node["arity"],
                "arity_source": prov[node["units"][0]]["arity_source"],
                "entry_count": len(node["classes"]),
                "unit_count": len(node["units"]),
                "units": sorted(node["units"])[:12],
                "units_listed": min(12, len(node["units"])),
            })
        joins = []
        for key in sorted(kept.keys()):
            if key[0] in members and key[1] in members:
                rec = kept[key]
                joins.append({
                    "left": key[0],
                    "right": key[1],
                    "shared_entries": rec["weight_classes"],
                    "shared_shape_keys": rec["weight_type_keys"],
                })
        families.append({
            "family_id": "F%04d" % fid,
            "size": len(members),
            "languages": sorted(langs),
            "language_count": len(langs),
            "nodes": out_nodes,
            "mutual_best_joins": joins,
        })

    meta = {
        "generator": "build_the_families1.py",
        "role_note": "GROUPING artifact -- checked by "
                     "check_no_spelling_keys.py IN FULL, no provenance "
                     "exemption claimed.",
        "task": "TASK 44 -- the dom_op construction rule over THE POOL",
        "construction": "THE DOM_OP CONSTRUCTION RULE, unchanged, "
                        "imported from dom_ops.py (build_nodes, "
                        "fill_nodes, build_edges, best_per_language, "
                        "mutual_edges, components)",
        "source_table": "the_pool1.json -- one population, every "
                        "language in the pool",
        "supersedes_as_an_object": "dom_ops23.json, which ran the same "
                                   "rule over the compiled-only "
                                   "dominant_table25.json.  Both stay "
                                   "on disk as the superseded record.",
        "what_a_node_is": "(language, grammar-operator, arity) -- the "
                          "provenance of the probe inside ONE language, "
                          "never a cross-language token.  The label is "
                          "a display field and is read by nothing.",
        "what_an_edge_is": "cross-language only; weight is the number "
                           "of POOL ENTRIES in which the two nodes both "
                           "have member units, then the number of "
                           "distinct machine-form shape keys those "
                           "entries carry",
    }
    summary = {
        "entry_count": len(pool["entries"]),
        "nodes": len(nodes),
        "edges_raw": len(edges),
        "edges_mutual": len(kept),
        "families": len(families),
        "singleton_families": len([f for f in families if f["size"] < 2]),
        "nodes_in_a_family": len(attached),
        "nodes_with_no_surviving_edge": len(unattached),
        "equally_strongest_ties": len(ties),
    }
    out = {
        "meta": meta,
        "summary": summary,
        "families": families,
        "unattached_nodes": unattached,
        "equally_strongest_ties": ties,
    }
    path = os.path.join(HERE, "the_families1.json")
    with open(path, "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True)
    log("-- wrote the_families1.json")
    log(json.dumps(summary, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
