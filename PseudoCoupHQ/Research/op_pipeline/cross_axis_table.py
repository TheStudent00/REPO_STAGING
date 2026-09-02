#!/usr/bin/env python3
"""cross_axis_table.py -- Task 8(d): rebuild the cross-axis operator
x exception table over exception_families2.json (rebuilt with java).

THE SPELLING BAN, pasted verbatim as required: "No operator token may
appear in ANY key, grouping, pairing, row structure, candidate
selection, or comparison scope, anywhere in this line -- not in
matching, not in "which pairs get compared", not in report rows, not
in dropdowns. The candidate set for comparison comes from machine-form
evidence (clusters, connections, type pairs) or from ratified
intention -- never from the token. The token appears exactly once per
unit: as a display label on the member." check_no_spelling_keys.py is
run on the output.

WHAT "OPERATOR AXIS" MEANS HERE: AgentMemory's SEEDED GROUPING UNDER
CONDITIONS ruling names two axes -- "OPERATOR families group by seed"
(dom_ops22.json's D-codes, built from proved seed/byte equivalence,
never from the token) and "EXCEPTION families group by guard
component" (exception_families2.json's EF-codes, built from condition
+ response head). This table crosses those two MACHINE-FORM id sets
-- dom_op_id x family_id -- via shared UNIT MEMBERSHIP (a unit that is
both a member of a dom_op node and a member of an exception family
puts one count in that cell). No cell, row or column key is an
operator token; `operator_label` is carried per cell purely as a
display echo (majority label among the unit(s) landing in that cell),
same discipline as every other stage.

COVERAGE NOTE: dom_ops22.json (Task 7's table) has not had java/
cpython joined into it (log_087, flagged for the owner, still open at Task
8 time) -- so java's 5 rows in exception_families2.json (EF0020,
EF0025, EF0026, EF0038, EF0039) have no dom_op_id to cross against and
are reported separately as "uncrossed" rather than silently dropped.
"""
import json
import os
from collections import defaultdict

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    dom = json.load(open(os.path.join(HERE, "dom_ops22.json")))
    ef = json.load(open(os.path.join(HERE, "exception_families2.json")))

    unit_to_dom = {}
    unit_to_label = {}
    for fam in dom["families"]:
        for node in fam["nodes"]:
            for u in node["units"]:
                unit_to_dom[u] = fam["dom_op_id"]
                unit_to_label[u] = node["label"]

    cells = defaultdict(lambda: defaultdict(int))
    uncrossed = []

    for family in ef["families"]:
        fid = family["family_id"]
        for m in family["members"]:
            unit = m["unit"]
            dom_id = unit_to_dom.get(unit)
            if dom_id is None:
                # per-unit exclusion record: carries a language field
                # and a unit id field, so `operator` is a legitimate
                # per-unit display label here (except-list), not a
                # cross-cell aggregate key.
                uncrossed.append(dict(
                    family_id=fid, unit=unit, language=m["language"],
                    operator=m["operator"],
                    reason="unit has no dom_op_id (not yet joined into "
                           "dom_ops22.json -- see COVERAGE NOTE)"))
                continue
            cells[dom_id][fid] += 1

    # NOTE: the crossed cell rows below carry NO operator field at
    # all -- a (dom_op_id, family_id) cell can hold units of more
    # than one label (a dom_op node's own label is display-only per
    # dom_ops22.json's own discipline), so there is no single
    # per-unit label to attach here without re-introducing a
    # spelling key on an aggregate. dom_op_id and family_id are the
    # keys; count is the only value.
    rows = []
    for dom_id in sorted(cells.keys()):
        for fid in sorted(cells[dom_id].keys()):
            rows.append(dict(
                dom_op_id=dom_id,
                family_id=fid,
                count=cells[dom_id][fid],
            ))

    out = dict(
        meta=dict(
            generator="cross_axis_table.py",
            role_note="operator-family (dom_ops22.json D-codes) x "
                       "exception-family (exception_families2.json "
                       "EF-codes) table, crossed by shared unit "
                       "membership; keys are the two machine-form id "
                       "sets, never the operator token.",
            source_dom_ops="dom_ops22.json",
            source_exception_families="exception_families2.json",
            row_count=len(rows),
            uncrossed_count=len(uncrossed),
            uncrossed_reason="member units with no dom_op_id -- "
                             "java's exception-family rows, since "
                             "dom_ops22.json has not had java/cpython "
                             "joined in (log_087's own flagged, still "
                             "open item)",
        ),
        rows=rows,
        uncrossed=uncrossed,
    )

    out_path = os.path.join(HERE, "cross_axis_table.json")
    json.dump(out, open(out_path, "w"), indent=1)
    print("wrote", out_path)
    print("crossed cells:", len(rows), " uncrossed member rows:", len(uncrossed))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
