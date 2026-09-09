#!/usr/bin/env python3
"""cross1_length_one.py -- task o1, deliverable A.

Reads /projects/PseudoCoupHQ/Research/op_pipeline/the_pool5.json and
computes, for every ORDERED pair of languages (x, y) among the
languages the pool actually holds: over all pool entries carrying a
y member, which are BUILT (the same entry also carries an x member,
length-one construction -- see CORE_0_3_8_2_cross_construction.md,
"construction of y from x", length one) and which are NOT_BUILT.

Every key in the output is a pool entry_id or a language name -- no
operator token is ever a key, grouping, pairing, or row. The
'operator' field, when quoted at all, is a per-member display label,
read by nothing structural here (matches the_pool5.json's own
'operator_note').

Writes cross1_length_one.json beside this script.
"""
import json
import sys

POOL_PATH = "/projects/PseudoCoupHQ/Research/op_pipeline/the_pool5.json"
OUT_PATH = "/projects/PseudoCoupHQ/Research/oracle/cross_construction/cross1_length_one.json"


def load_pool():
    with open(POOL_PATH) as f:
        return json.load(f)


def main():
    pool = load_pool()
    entries = pool["entries"]

    # Which languages does the pool actually hold, and how many
    # entries carry a member in each.
    lang_entry_count = {}
    for e in entries:
        for lang in e["languages"]:
            lang_entry_count[lang] = lang_entry_count.get(lang, 0) + 1

    # The corpus the coordinator counted (c, cpp, swift, go, rust) --
    # confirm which of those (and any others) the pool holds.
    corpus_five = ["c", "cpp", "swift", "go", "rust"]
    held_langs = sorted(lang_entry_count.keys(), key=lambda l: -lang_entry_count[l])
    corpus_five_present = [l for l in corpus_five if l in lang_entry_count]
    corpus_five_absent = [l for l in corpus_five if l not in lang_entry_count]
    other_langs_present = [l for l in held_langs if l not in corpus_five]

    # The matrix is built over the five-language corpus (the languages
    # with enough pool entries to make a matrix cell meaningful); the
    # other-present languages are reported separately, by count only,
    # per the brief's "say the others have no pool entries" test --
    # here they have a handful, so we say exactly how many rather than
    # imply zero.
    matrix_langs = corpus_five_present

    # entry_id -> set of languages present as members, and one example
    # member (lang -> layer5 text) per entry, for the "quoted example"
    # requirement.
    entry_langs = {}
    entry_text_by_lang = {}
    for e in entries:
        eid = e["entry_id"]
        langs = set(e["languages"])
        entry_langs[eid] = langs
        by_lang = {}
        for m in e["members"]:
            by_lang.setdefault(m["lang"], m["layer5_normalized_text"])
        entry_text_by_lang[eid] = by_lang

    pairs = {}
    table_rows = []
    for x in matrix_langs:
        row = {"x": x, "cells": {}}
        for y in matrix_langs:
            if x == y:
                continue
            y_entries = [eid for eid, langs in entry_langs.items() if y in langs]
            built = [eid for eid in y_entries if x in entry_langs[eid]]
            not_built = [eid for eid in y_entries if x not in entry_langs[eid]]
            total_y = len(y_entries)
            pct = (100.0 * len(built) / total_y) if total_y else 0.0
            pairs[f"{x}|{y}"] = {
                "x": x,
                "y": y,
                "built_entry_ids": sorted(built),
                "not_built_entry_ids": sorted(not_built),
                "built_count": len(built),
                "total_y_entries": total_y,
                "percent_built": round(pct, 2),
            }
            row["cells"][y] = f"{len(built)}/{total_y} ({pct:.1f}%)"
        table_rows.append(row)

    # Symmetric view: entries carrying members in ALL of the
    # five-language corpus set.
    all_five_set = set(corpus_five_present)
    all_five_entries = sorted(
        eid for eid, langs in entry_langs.items() if all_five_set.issubset(langs)
    )

    # One quoted example per (x,y) row-cell: a built entry + text, a
    # not_built entry + text (for y and, where present, for x).
    examples = {}
    for key, cell in pairs.items():
        x, y = cell["x"], cell["y"]
        ex = {}
        if cell["built_entry_ids"]:
            eid = cell["built_entry_ids"][0]
            ex["built"] = {
                "entry_id": eid,
                "y_text": entry_text_by_lang[eid].get(y),
                "x_text": entry_text_by_lang[eid].get(x),
            }
        if cell["not_built_entry_ids"]:
            eid = cell["not_built_entry_ids"][0]
            ex["not_built"] = {
                "entry_id": eid,
                "y_text": entry_text_by_lang[eid].get(y),
            }
        examples[key] = ex

    out = {
        "task": "o1 deliverable A -- length-one construction map",
        "pool_source": POOL_PATH,
        "pool_entry_count": len(entries),
        "languages_pool_holds": {
            lang: lang_entry_count[lang] for lang in held_langs
        },
        "corpus_five_present": corpus_five_present,
        "corpus_five_absent_from_pool": corpus_five_absent,
        "other_languages_present_low_count": {
            l: lang_entry_count[l] for l in other_langs_present
        },
        "matrix_languages": matrix_langs,
        "pairs": pairs,
        "examples_per_pair": examples,
        "all_five_language_entries": {
            "languages": sorted(all_five_set),
            "entry_ids": all_five_entries,
            "count": len(all_five_entries),
        },
        "table_rows": table_rows,
    }

    with open(OUT_PATH, "w") as f:
        json.dump(out, f, indent=2, sort_keys=True)

    total = len(matrix_langs) * (len(matrix_langs) - 1)
    i = 0
    print(f"pool entries: {len(entries)}")
    print(f"languages pool holds: {lang_entry_count}")
    print(f"matrix languages: {matrix_langs}")
    print(f"all-five entries: {len(all_five_entries)}")
    print()
    print("| x \\ y | " + " | ".join(matrix_langs) + " |")
    print("|---" * (len(matrix_langs) + 1) + "|")
    for row in table_rows:
        cells = [row["cells"].get(y, "--") for y in matrix_langs]
        print(f"| {row['x']} | " + " | ".join(cells) + " |")
    for key in pairs:
        i += 1
        print(f"[{i}/{total}] pair {key} done")
    print("wrote", OUT_PATH)


if __name__ == "__main__":
    main()
