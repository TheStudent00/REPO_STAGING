#!/usr/bin/env python3
"""the_pool1_original_subset.py -- TASK 44's continuity figures.

The compiled-only table ceases to exist as an object.  Anyone who
wants one FILTERS THE POOL.  This program is that filter, written once
so the continuity figures for the original corpus of 1,779 units are
DERIVED from `the_pool1.json` rather than kept as a second table.

How each figure is derived, stated before it is printed:

  entries        -- the pool's entries, keeping only members whose
                    `population` field reads `original`, and dropping
                    an entry that has no such member.  Nothing is
                    re-grouped: the merge already happened over the
                    whole pool, and this only hides members.
  nodes          -- THE DOM_OP CONSTRUCTION RULE's node set over that
                    filtered view: (language, grammar-operator,
                    arity), unchanged.
  families       -- the same rule's connected components over that
                    filtered view.
  unattached     -- nodes with no surviving mutual-best edge.

These are compared with round 8's 898 / 137 / 26 / 20, which were
computed over `dominant_table25.json`.  The comparison is stated with
its own caveat rather than as a like-for-like: that table's class key
was (operand-type key, result family, representative text), while a
pool entry's merge key is the machine text or a proved edge alone.  A
difference in the entry count is therefore expected and is a property
of the merge rule, not a regression.

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

usage: the_pool1_original_subset.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dom_ops                                          # noqa: E402
import build_the_pool1 as POOL                          # noqa: E402
import build_the_families1 as FAM                       # noqa: E402


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def figures(pool, prov, keep):
    rows = []
    members_kept = 0
    for entry in pool["entries"]:
        here = [m for m in entry["members"] if keep(m)]
        if not here:
            continue
        members_kept = members_kept + len(here)
        rows.append({
            "class_id": entry["entry_id"],
            "type_pair": entry["type_key"],
            "members": [{"unit": m["unit"]} for m in here],
        })
    doc = {"table": {"rows": rows}}
    nodes, index = dom_ops.build_nodes(doc, prov)
    class_members = dom_ops.fill_nodes(doc, nodes, index, prov)
    edges = dom_ops.build_edges(doc, nodes, class_members, 0)
    best, _ties = dom_ops.best_per_language(nodes, edges)
    kept = dom_ops.mutual_edges(nodes, edges, best)
    comps = dom_ops.components(kept)
    attached = {}
    for members in comps:
        for nid in members:
            attached[nid] = True
    return {
        "member_units": members_kept,
        "entries": len(rows),
        "nodes": len(nodes),
        "edges_raw": len(edges),
        "edges_mutual": len(kept),
        "families": len(comps),
        "nodes_in_a_family": len(attached),
        "nodes_with_no_surviving_edge": len(nodes) - len(attached),
    }


def main():
    pool = json.load(open(os.path.join(HERE, "the_pool1.json")))
    records = []
    records.extend(POOL.take_original())
    records.extend(POOL.take_interpreter())
    records.extend(POOL.take_regenerated())
    prov = FAM.provenance_over_the_pool(records)

    log("== the whole pool, no filter")
    whole = figures(pool, prov, lambda m: True)
    log(json.dumps(whole, indent=1, sort_keys=True))

    log("== filtered to members whose population reads 'original'")
    orig = figures(pool, prov, lambda m: m["population"] == "original")
    log(json.dumps(orig, indent=1, sort_keys=True))

    log("== round 8's compiled-only figures, for continuity")
    prior = json.load(open(os.path.join(HERE, "dom_ops23.json")))
    log(json.dumps({
        "class_count": prior["class_count"],
        "nodes": prior["nodes"],
        "dom_op_count": prior["dom_op_count"],
        "nodes_with_no_surviving_edge":
            prior["nodes_with_no_surviving_edge"],
    }, indent=1, sort_keys=True))

    log("== members by arrival population, over the whole pool")
    counts = {}
    langs = {}
    for entry in pool["entries"]:
        for m in entry["members"]:
            counts[m["population"]] = counts.get(m["population"], 0) + 1
            langs[m["lang"]] = langs.get(m["lang"], 0) + 1
    log(json.dumps(counts, indent=1, sort_keys=True))
    log("== members by language, over the whole pool")
    log(json.dumps(langs, indent=1, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
