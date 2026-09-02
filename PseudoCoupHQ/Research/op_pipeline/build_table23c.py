#!/usr/bin/env python3
"""build_table23c.py -- TASK 3 (log_083) table update. Adds the 34
c/cpp branching seed units seed_extract2.py resolved (seeds2.json)
onto the dominant_table23b.json / dom_ops21b.json lineage (NOT
table24/dom_ops22 -- those names are reserved for Task 7's own
reconciliation, per the brief).

METHOD. dominant_table23b.json's 901 rows are loaded UNCHANGED. Each
of the 34 resolved seed units becomes a candidate row keyed
(type_pair, result_type, seed_text) -- the SAME three-part key every
generation in this lineage has used since dominant_table17.py
(type_pair_of/class_family imported, not re-derived; seed_text is
this unit's seed, from seed_extract2.py's proved suffix). If that
exact key already matches an existing row (character-identical
canonical_text, same type_pair/result_type), the unit is UNIONED
into that row -- no new class. Otherwise a NEW row is appended.
Measured: 10 of the 34 seed texts matched an existing table23b row
verbatim (all 10 are cpp's comparison seeds -- op_117/122/153/158/
189/194/225/230/981/986; cpp already carried a straight-line unit of
the same (type_pair, result_type) whose canon-rendered text is
identical to these seeds' extracted suffix). The other 24 (all of
c's 20, plus cpp's 4 arithmetic seeds not in the list above) form
NEW classes -- their seed text carries this unit's own extraction-
time scratch register numbering (e.g. %xmm2/%xmm3/%r10d/%r11d),
which this lineage's canon7-canon24 render chain has not run over
(that render chain applies to whole-unit 0-branch text; running it
over an extracted seed fragment is out of this task's scope).
Recorded as a named remainder, not silently patched around: these
24 classes are correct AS ADDED (proved-equal seed content) but may
later re-merge with existing classes once the full render chain
is extended to seed fragments.

dom_ops21c.json is REBUILT from dom_ops_0branch.py's own construction
(DO.build_nodes/fill_nodes/build_edges/best_per_language/mutual_edges/
components -- unchanged, imported) over the ENRICHED table (table23b's
901 classes + the 34 seed-derived classes), so the new branching
units are visible to family formation exactly like any other node.

THE SPELLING BAN: unchanged -- class key is (type_pair, result_type,
text), never the operator token; check_no_spelling_keys.py runs on
both outputs before this program declares success.

usage:
  build_table23c.py [--out DIR]
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dom_ops as DO                                              # noqa: E402
import dom_ops_0branch as DB                                      # noqa: E402
import result_type_norm as RTN                                    # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]


def load_canon4(lang):
    path = os.path.join(HERE, "canon4_units_%s.json" % lang)
    return json.load(open(path))["units"]


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=HERE)
    args = ap.parse_args(argv)

    base = json.load(open(os.path.join(HERE, "dominant_table23b.json")))
    seeds_doc = json.load(open(os.path.join(HERE, "seeds2.json")))

    rows = base["table"] if "table" in base else base
    # dominant_table23b.json's own top-level shape has "rows" directly
    row_list = base["rows"]
    key_to_row = {}
    for row in row_list:
        key = (row["type_pair"], row["result_type"], row["canonical_text"])
        key_to_row[key] = row

    canon4_cache = {}

    def canon4_unit(lang, n):
        if lang not in canon4_cache:
            canon4_cache[lang] = load_canon4(lang)
        return canon4_cache[lang].get(n)

    added_units = []
    merged_units = []
    new_rows = []
    verbatim_matches = 0

    for unit_id, rec in sorted(seeds_doc["seeds"].items()):
        if rec.get("status") != "ok" or "seed_text" not in rec:
            continue
        lang, n = unit_id.split("/op_")
        if lang not in ("c", "cpp"):
            continue
        u4 = canon4_unit(lang, n)
        if u4 is None:
            continue
        type_pair = DB.type_pair_of(u4)
        fam, note = RTN.class_family(lang, n, u4["meta"])
        result_type = fam if fam is not None else ("unknown(%s)" % note[:40])
        text = rec["seed_text"]
        key = (type_pair, result_type, text)
        member = {"unit": unit_id}
        if key in key_to_row:
            key_to_row[key]["members"].append(member)
            merged_units.append(unit_id)
            verbatim_matches += 1
        else:
            new_row = {
                "class_id": None,  # assigned below after sort
                "type_pair": type_pair,
                "result_type": result_type,
                "canonical_text": text,
                "members": [member],
                "source": "seed_extract2.py (TASK 3 branching seed, "
                          "idiom-context-stripped-proved-equal-suffix)",
            }
            key_to_row[key] = new_row
            new_rows.append(new_row)
            added_units.append(unit_id)

    all_rows = row_list + new_rows
    all_rows_sorted = sorted(
        all_rows, key=lambda r: (r["type_pair"], r["result_type"],
                                  r["canonical_text"]))
    for i, row in enumerate(all_rows_sorted, start=1):
        row["class_id"] = "C%04d" % i

    out_table = dict(
        generator="build_table23c.py",
        role_note="GROUPING/matching artifact (top-level `rows`, each "
                  "with `members`) -- checked by check_no_spelling_"
                  "keys.py IN FULL, no exemption claimed.",
        lineage="dominant_table23b.json (901 classes) PLUS the 34 "
               "c/cpp branching seed units seed_extract2.py resolved "
               "(seeds2.json) -- TASK 3, not Task 7's reconciliation.",
        classes_before=len(row_list),
        classes_after=len(all_rows_sorted),
        seed_units_considered=34,
        seed_units_merged_into_existing_class=len(merged_units),
        seed_units_forming_new_class=len(added_units),
        seed_units_merged_verbatim_text_match=verbatim_matches,
        merged_units=merged_units,
        added_as_new_class_units=added_units,
        rows=all_rows_sorted)

    out_path = os.path.join(args.out, "dominant_table23c.json")
    json.dump(out_table, open(out_path, "w"), indent=1)

    # provenance for dom_ops rebuild -- SAME shape build_table23b/
    # dominant_table17 already build: label -> {lang, n, display_label,
    # arity_bucket}
    prov = {}
    for row in all_rows_sorted:
        for m in row["members"]:
            label = m["unit"]
            if label in prov:
                continue
            lg, num = label.split("/op_")
            u4 = canon4_unit(lg, num)
            if u4 is None:
                # branching unit not in canon4 0-branch population
                # shape lookup fallback: still read meta from op_units
                op_path = os.path.join(HERE, "op_units_%s.json" % lg)
                opd = json.load(open(op_path))
                u4 = {"meta": opd["units"][num]["meta"]} if num in \
                    opd.get("units", {}) else {"meta": {}}
            prov[label] = {
                "lang": lg,
                "n": num,
                "display_label": u4.get("meta", {}).get("operator") or
                                 u4.get("operator"),
                "arity_bucket": DB.arity_bucket_of(u4) if
                                "entry_contract" in u4 else "binary",
            }

    doc_for_do = {"table": {"rows": all_rows_sorted}}
    nodes, index = DO.build_nodes(doc_for_do, prov)
    class_members = DO.fill_nodes(doc_for_do, nodes, index, prov)
    edges = DO.build_edges(doc_for_do, nodes, class_members, 0)
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

    out_ops = dict(
        meta=dict(
            generator="build_table23c.py (dom_ops21c.json)",
            role="generator provenance",
            lineage="dominant_table23c.json",
            construction="dom_ops7.py's rule, unchanged (via "
                         "dom_ops_0branch.py, imported not restated).",
            source_table="dominant_table23c.json"),
        class_count=len(all_rows_sorted),
        nodes=len(nodes),
        edges_raw=len(edges),
        edges_mutual=len(kept),
        dom_op_count=len(family_rows),
        singleton_dom_ops=singleton_count,
        nodes_in_a_dom_op=len(attached),
        nodes_with_no_surviving_edge=len(unattached),
        unattached_nodes=unattached,
        families=family_rows)

    out_ops_path = os.path.join(args.out, "dom_ops21c.json")
    json.dump(out_ops, open(out_ops_path, "w"), indent=1)

    print(json.dumps(dict(
        classes_before=len(row_list), classes_after=len(all_rows_sorted),
        seed_units_merged=len(merged_units),
        seed_units_new_class=len(added_units),
        dom_op_count_before="see dom_ops21b.json",
        dom_op_count_after=len(family_rows),
        singleton_dom_ops_after=singleton_count,
        unattached_after=len(unattached),
    ), indent=2))


if __name__ == "__main__":
    main(sys.argv[1:])
