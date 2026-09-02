#!/usr/bin/env python3
"""operator_x_exception.py -- STEP 4 of THE JOB: THE CROSS-AXIS VIEW.

For each OPERATOR family in dom_ops20.json (the seeded-grouping-by-
seed axis), which EXCEPTION families (exception_families.json, the
guard-component axis) do its member units carry, per language?

The two axes are NEVER merged (AgentMemory, SEEDED GROUPING UNDER
CONDITIONS): this file only JOINS them, on UNIT ID -- machine-form
membership, not a grouping key of its own. Row key is the operator
family's own id (`dom_op_id`, itself built from language+grammar-
operator+arity node identity by dom_ops19.py, upstream of this file)
paired with language; the value is a list of exception `family_id`s
(or the string "NONE"), never operator tokens. `operator`/`label`
fields present are per-unit or per-node display labels only, carried
through from the source files, same shape they already passed
check_no_spelling_keys.py in.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    dom = json.load(open(os.path.join(HERE, "dom_ops20.json")))
    ef = json.load(open(os.path.join(HERE, "exception_families.json")))
    g2 = json.load(open(os.path.join(HERE, "guards2.json")))

    unit_to_families = {}
    for fam in ef["families"]:
        for m in fam["members"]:
            unit_to_families.setdefault(m["unit"], set()).add(
                fam["family_id"])

    unit_guard_count = {u: rec["guard_count"]
                         for u, rec in g2["units"].items()}

    rows = []
    for dom_op in dom["dom_ops"]:
        dom_op_id = dom_op["dom_op_id"]
        by_lang = {}
        for node in dom_op["nodes"]:
            lang = node["lang"]
            entry = by_lang.setdefault(lang, dict(
                units=[], families=set(), all_zero_guard=True,
                any_unit_missing_from_guard_data=False))
            for u in node["units"]:
                entry["units"].append(u)
                fams = unit_to_families.get(u)
                if fams:
                    entry["families"] |= fams
                gc = unit_guard_count.get(u)
                if gc is None:
                    entry["any_unit_missing_from_guard_data"] = True
                elif gc != 0:
                    entry["all_zero_guard"] = False
        lang_row = {}
        for lang, entry in sorted(by_lang.items()):
            fams = sorted(entry["families"])
            lang_row[lang] = fams if fams else "NONE"
        rows.append(dict(
            dom_op_id=dom_op_id,
            display_labels=sorted(set(
                n["label"] for n in dom_op["nodes"])),
            languages=lang_row,
        ))

    out = dict(
        meta=dict(
            generator="operator_x_exception.py",
            role_note="THE CROSS-AXIS VIEW: for each operator family "
                      "(dom_ops20.json) which exception families "
                      "(exception_families.json) its member units "
                      "carry, per language. A JOIN on unit id, never a "
                      "merge of the two grouping axes. No operator "
                      "token in any grouping/pairing/row key -- rows "
                      "key on dom_op_id and exception family_id only.",
            sources=["dom_ops20.json", "exception_families.json",
                     "guards2.json"],
            row_count=len(rows),
        ),
        rows=rows,
    )
    json.dump(out, open(
        os.path.join(HERE, "operator_x_exception.json"), "w"), indent=1)

    for row in rows:
        if row["dom_op_id"] not in ("D0010", "D0015"):
            continue
        print("\n%s  %s" % (row["dom_op_id"], row["display_labels"]))
        for lang, fams in sorted(row["languages"].items()):
            print("   %-6s %s" % (lang, fams))

    print("\nwrote operator_x_exception.json (%d dom_op rows)" % len(rows))


if __name__ == "__main__":
    main()
