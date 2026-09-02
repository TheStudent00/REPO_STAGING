#!/usr/bin/env python3
"""build_union_table3.py -- TASK 39 step 5: THE UNION VIEW, rebuilt
over the compiled table's UNIVERSAL-FORM column.

WHAT CHANGES FROM build_union_table3.py: the three inputs, and only
the three inputs.  `dominant_table25.json` replaces
`dominant_table25.json` as the compiled view, `interp_join3.json`
replaces `interp_join3.json` as the edge source, and the output is
`union_table3.json`.  The construction -- three views, edges only
from PROVED_EQUAL relations, nothing merged, nothing destroyed -- is
build_union_table3.py's own, character for character.  Both compiled
tables are opened READ-ONLY and neither is written.

DEE'S RULING, log_115 (2026-09-01), which this file implements
literally: "INTERPRETER TABLE: THREE VIEWS.  Compiled table,
interpreter table, union -- joined by proved relations, nothing
merged, nothing destroyed.  Membership is not a pending ontology
question; it is construction."

SO THIS FILE BUILDS A NAVIGATION OBJECT, NOT A NEW TABLE.  It holds
three views:

  * `views.compiled`    -- an index of `dominant_table25.json`'s own
                           901 classes: class id, class key, canonical
                           text, member count, and every member's unit
                           id.  The table itself is opened READ-ONLY
                           and is not written, not copied over, and not
                           changed in any way.
  * `views.interpreter` -- the same index over `interp_table2.json`'s
                           classes.  Their text is the UNIVERSAL text
                           (designated locations, standardized loads)
                           and the arrival mode rides as an ANNOTATION
                           beside it, not inside the key -- the owner's
                           ruling of 2026-09-01.
  * `views.union_by_relations` -- the connected components of the graph
                           whose nodes are classes from either table
                           and whose edges are PROVED_EQUAL relations
                           from `interp_join3.json`.  A component is a
                           set of classes that a solver proved compute
                           the same thing.  The classes inside it stay
                           separate objects with their own ids; the
                           component names them, it does not absorb
                           them.

WHAT IS AND IS NOT AN EDGE.  Only a PROVED_EQUAL relation forms an
edge.  An OBSERVATION -- a proof run whose type key does not license
the comparison (php's handlers, java's JIT unit) -- is carried in its
own section and forms NO edge, because it is not a relation.  An
UNDECIDED or TYPE_INCOMPARABLE row forms no edge either.  This is the
"nothing merged" half of the ruling: a class only ever joins a
component through a proof.

NAVIGATION.  `unit_index` maps every unit id in either table to the
view it lives in, its class id, and its union component id where it
has one -- so any unit can be looked up from any of the three views.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim.

Run:
  /tmp/reconnect_venv/bin/python3 build_union_table3.py
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "union_table3.json")


def load(name):
    return json.load(open(os.path.join(HERE, name)))


def find(parent, node):
    while parent[node] != node:
        parent[node] = parent[parent[node]]
        node = parent[node]
    return node


def union(parent, left, right):
    a, b = find(parent, left), find(parent, right)
    if a == b:
        return
    if a < b:
        parent[b] = a
    else:
        parent[a] = b


def main():
    compiled = load("dominant_table25.json")
    interp = load("interp_table2.json")
    join = load("interp_join3.json")

    compiled_view = {}
    unit_index = {}
    for row in compiled["rows"]:
        node = "compiled:%s" % row["class_id"]
        compiled_view[row["class_id"]] = {
            "node_id": node,
            "type_pair": row["type_pair"],
            "result_type": row["result_type"],
            "canonical_text": row["canonical_text"],
            "member_count": len(row["members"]),
            "member_units": [m["unit"] for m in row["members"]],
        }
        for member in row["members"]:
            unit_index[member["unit"]] = {
                "view": "compiled",
                "class_id": row["class_id"],
                "node_id": node,
            }

    interp_view = {}
    for row in interp["rows"]:
        node = "interpreter:%s" % row["class_id"]
        interp_view[row["class_id"]] = {
            "node_id": node,
            "type_pair": row["type_pair"],
            "result_type": row["result_type"],
            "arrival_annotations_present":
                row["arrival_annotations_present"],
            "universal_text": row["universal_text"],
            "member_count": len(row["members"]),
            "member_units": [m["unit"] for m in row["members"]],
        }
        for member in row["members"]:
            unit_index[member["unit"]] = {
                "view": "interpreter",
                "class_id": row["class_id"],
                "node_id": node,
            }

    nodes = (["compiled:%s" % k for k in compiled_view]
             + ["interpreter:%s" % k for k in interp_view])
    parent = dict([(n, n) for n in nodes])

    edges = []
    for row in join["rows"]:
        if row.get("relation") != "PROVED_EQUAL":
            continue
        left = "interpreter:%s" % row["interp_class_id"]
        singles = []
        if row.get("compiled_class_id"):
            singles.append(row["compiled_class_id"])
        for entry in row.get("proved_equal_to", []):
            if entry.get("compiled_class_id"):
                singles.append(entry["compiled_class_id"])
        for class_id in singles:
            right = "compiled:%s" % class_id
            if right not in parent:
                continue
            union(parent, left, right)
            edges.append({
                "left_node_id": left,
                "right_node_id": right,
                "relation": "PROVED_EQUAL",
                "evidence": row.get("evidence")
                            or row.get("evidence_class"),
                "source_artifact": row.get("source_artifact")
                                   or "interp_join3.json",
            })
    for edge in join.get("interpreter_to_interpreter_edges", []):
        if edge.get("relation") != "PROVED_EQUAL":
            continue
        left = "interpreter:%s" % edge["left_class_id"]
        right = "interpreter:%s" % edge["right_class_id"]
        union(parent, left, right)
        edges.append({
            "left_node_id": left,
            "right_node_id": right,
            "relation": "PROVED_EQUAL",
            "evidence": edge.get("detail"),
            "source_artifact": "interp_join3.json",
        })

    groups = {}
    for node in nodes:
        groups.setdefault(find(parent, node), []).append(node)

    components = []
    for root in sorted(groups):
        members = sorted(groups[root])
        if len(members) == 1:
            continue
        has_interp = [m for m in members if m.startswith("interpreter:")]
        if not has_interp:
            # a compiled-only component cannot exist here: no edge in
            # this file ever joins two compiled classes.  Kept as a
            # check rather than an assumption.
            continue
        components.append({
            "component_id": "U%04d" % (len(components) + 1),
            "member_node_ids": members,
            "compiled_class_ids": [m.split(":", 1)[1] for m in members
                                   if m.startswith("compiled:")],
            "interpreter_class_ids": [m.split(":", 1)[1] for m in members
                                      if m.startswith("interpreter:")],
            "edges": [e for e in edges
                      if e["left_node_id"] in members
                      and e["right_node_id"] in members],
        })

    component_of = {}
    for component in components:
        for node in component["member_node_ids"]:
            component_of[node] = component["component_id"]
    for unit, entry in unit_index.items():
        entry["union_component_id"] = component_of.get(entry["node_id"])

    observations = []
    for row in join["rows"]:
        if not row.get("observation"):
            continue
        observations.append({
            "interp_unit": row["interp_unit"],
            "interp_class_id": row["interp_class_id"],
            "relation": row["relation"],
            "why_no_relation": row.get("why"),
            "observation": row["observation"],
            "forms_no_edge": True,
            "forms_no_edge_why":
                "an observation is a proof RUN without the type key "
                "that would license the comparison; the owner's ruling joins "
                "the views by PROVED RELATIONS, so an observation is "
                "recorded and never merged",
        })

    out = {
        "meta": {
            "generator": "build_union_table3.py",
            "role_note": "GROUPING/navigation artifact -- checked by "
                         "check_no_spelling_keys.py IN FULL, no "
                         "exemption claimed.",
            "task": "TASK 39 step 5 -- the union view, the third of "
                    "the owner's three views",
            "edge_rule": "PROVED_EQUAL relations only.  Observations, "
                         "UNDECIDED and TYPE_INCOMPARABLE rows form no "
                         "edge.",
            "opens_read_only": ["dominant_table25.json",
                                "interp_table2.json",
                                "interp_join3.json"],
            "writes_to_the_compiled_table": "NONE -- "
                "dominant_table25.json and dom_ops23.json are not "
                "written by this file or by any file in TASK 34",
        },
        "views": {
            "compiled": {
                "source": "dominant_table25.json (read-only)",
                "class_count": len(compiled_view),
                "classes": compiled_view,
            },
            "interpreter": {
                "source": "interp_table2.json (read-only)",
                "class_count": len(interp_view),
                "classes": interp_view,
            },
            "union_by_relations": {
                "source": "interp_join3.json's PROVED_EQUAL rows",
                "component_count": len(components),
                "components": components,
            },
        },
        "unit_index": unit_index,
        "observations_that_form_no_edge": observations,
        "summary": {
            "compiled_classes": len(compiled_view),
            "interpreter_classes": len(interp_view),
            "union_components": len(components),
            "proved_edges": len(edges),
            "units_indexed": len(unit_index),
        },
    }
    with open(OUT, "w") as fh:
        json.dump(out, fh, indent=1)
    print("wrote %s" % OUT)
    for component in components:
        print("%s  interpreter=%s  compiled=%s  edges=%d"
              % (component["component_id"],
                 component["interpreter_class_ids"],
                 component["compiled_class_ids"],
                 len(component["edges"])))
    print("summary: %s" % out["summary"])
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "check_no_spelling_keys.py"),
         OUT], capture_output=True, text=True)
    sys.stdout.write(proc.stdout)
    sys.stdout.write(proc.stderr)
    if proc.returncode != 0:
        print("REFUSING OWN OUTPUT: the spelling guard failed on %s" % OUT)
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main())
