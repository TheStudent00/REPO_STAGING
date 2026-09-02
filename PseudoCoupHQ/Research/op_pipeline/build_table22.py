#!/usr/bin/env python3
"""build_table22.py -- STEP 3 of THE JOB. Extends
dominant_table21.json (1,641 0-branch units) with the branching
units seed_extract1.py resolved (seeds1.json, status "ok"): each
resolved branching unit is added as a MEMBER of the existing class
whose canonical text equals the unit's seed_text (guarded
containment made concrete -- go modulo's L3+L4 seed lands in c
modulo's class). Its guards ride along as data on the member, never
as part of the class key. Construction rule for the class key itself
is UNCHANGED (build_table19/21's rule); this file only adds members
to existing classes, never mints a new class from a seed alone (a
branching unit whose seed matches nothing existing is left out,
same "unresolved" honesty as seed_extract1.py).

Population is now the FULL 1,779, split: 1,641 0-branch (unchanged
membership) + however many of the 138 branching units resolved.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    table = json.load(open(os.path.join(HERE, "dominant_table21.json")))
    seeds = json.load(open(os.path.join(HERE, "seeds1.json")))["seeds"]

    by_class = {row["class_id"]: row for row in table["rows"]}

    added = []
    for unit_id, s in seeds.items():
        if s.get("status") != "ok":
            continue
        cid = s.get("matched_class")
        if not cid or cid not in by_class:
            continue
        row = by_class[cid]
        row["members"].append(dict(
            unit=unit_id,
            branching=True,
            seed_text=s["seed_text"],
            seed_method=s["method"],
            guards=s["guards"]))
        added.append((unit_id, cid))

    new_table = dict(
        meta=dict(
            generator="build_table22.py",
            role_note="GROUPING/matching artifact (top-level `rows`, "
                       "each with `members`) -- checked by "
                       "check_no_spelling_keys.py IN FULL, no "
                       "exemption claimed.",
            construction="dominant_table21.json's class rows, "
                         "UNCHANGED, plus branching-unit members "
                         "added by exact seed-text match against an "
                         "existing class's canonical text (guarded "
                         "containment, AgentMemory SEEDED GROUPING "
                         "UNDER CONDITIONS). No new class is minted "
                         "from a seed alone this lap.",
            population="1,779 full corpus: 1,641 0-branch (unchanged) "
                       "+ %d branching units joined by seed identity "
                       "(%d branching units seed_extract1.py could not "
                       "resolve this lap stay OUT of the table, "
                       "honestly, see seeds1.json/survey1.json)"
                       % (len(added),
                          sum(1 for s in seeds.values()
                              if s.get("status") != "ok")),
            baseline="dom_ops19.json (built over dominant_table21.json): "
                     "919 classes / 135 nodes / 26 dom_ops / 21 edgeless",
        ),
        classes=table["classes"],
        rows=table["rows"],
    )
    json.dump(new_table, open(os.path.join(HERE, "dominant_table22.json"), "w"),
               indent=1)

    print("classes:", new_table["classes"], "(unchanged -- no new class minted)")
    print("branching members added:", len(added))
    by_lang = {}
    for uid, cid in added:
        lang = uid.split("/")[0]
        by_lang[lang] = by_lang.get(lang, 0) + 1
    print("by language:", by_lang)
    print()
    print("changed classes (had a branching member added):")
    seen_classes = sorted(set(cid for _, cid in added))
    for cid in seen_classes:
        row = by_class[cid]
        print(" ", cid, row["type_pair"], "->", row["result_type"],
              "members now:", len(row["members"]))
        for m in row["members"]:
            if isinstance(m, dict) and m.get("branching"):
                print("      +", m["unit"], "guards:",
                      [g.get("response") for g in m["guards"]])


if __name__ == "__main__":
    main()
