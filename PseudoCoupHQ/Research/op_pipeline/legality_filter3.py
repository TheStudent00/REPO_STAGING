#!/usr/bin/env python3
"""legality_filter3.py -- the legality reduction recomputed on the
CORRECTED type inventory (the declarable witness).

WHAT CHANGED SINCE legality_filter2.py, AND NOTHING ELSE
--------------------------------------------------------
The candidate space is a cross-product over each language's SCALAR CORE,
and the core is read out of the type inventory.  Version 2 read
`type_inventory2.json`, whose types are those an AUTHORITY names.  This
version reads `type_inventory3.json`, whose types are those an authority
names AND that this target actually accepts in a declaration (compiled,
in the trickle container, at the probe lanes' own flags).

The RULES are untouched: `legality_rules.json` is read as it stands, and
`core_rule2.scalar_core` is the same membership test, applied to a
smaller inventory.  Nothing existing on disk is modified.

THE SPELLING BAN
----------------
Candidates are selected and grouped by (operator UNIT id, type pair);
type spellings ride on objects carrying `language` and `id`.  No key,
grouping, pairing or row structure is an operator token.  The output is
walked by the guard and this program deletes its own output on failure.

usage:  /tmp/reconnect_venv/bin/python3 legality_filter3.py
writes: legality_reduction3.json
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import legality_filter as v1                               # noqa: E402
import legality_filter2 as v2                              # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]


def main():
    rules_doc = json.load(open(os.path.join(HERE, "legality_rules.json")))
    inv3 = json.load(open(os.path.join(HERE, "type_inventory3.json")))
    inv2 = json.load(open(os.path.join(HERE, "type_inventory2.json")))
    by_id = {}
    for record in rules_doc["rules"]:
        by_id[(record["language"], record["rule_id"])] = record["shape"]
    units = {}
    for lang in LANGS:
        units[lang] = []
    for row in rules_doc["operator_units"]:
        units[row["language"]].append(row)

    red = v2.reduction(by_id, units, inv3)
    red["generated_by"] = "legality_filter3.py"
    red["type_inventory"] = "type_inventory3.json (extracted AND declarable)"
    red["population"] = (
        "the five compiled languages' operator units as legality_rules.json "
        "carries them, crossed with each language's EXTRACTED SCALAR CORE "
        "under core_rule2 read from type_inventory3.json -- the inventory "
        "whose types this target accepts in a declaration. No probe is "
        "written or compiled by this program.")
    red["core_sizes_v2_vs_v3"] = []
    import core_rule2
    for lang in LANGS:
        c2, _u2 = core_rule2.scalar_core(lang, inv2)
        c3, _u3 = core_rule2.scalar_core(lang, inv3)
        gone = sorted(set(s for s, _m, _c in c2)
                      - set(s for s, _m, _c in c3))
        red["core_sizes_v2_vs_v3"].append({
            "language": lang,
            "core_over_inventory2": len(c2),
            "core_over_inventory3": len(c3),
            "left_the_core": [{"language": lang,
                               "id": "%s/left_%d" % (lang, i),
                               "spelling": s}
                              for i, s in enumerate(gone)],
        })

    path = os.path.join(HERE, "legality_reduction3.json")
    fh = open(path, "w")
    json.dump(red, fh, indent=1)
    fh.write("\n")
    fh.close()

    old = json.load(open(os.path.join(HERE, "legality_reduction2.json")))
    print("%-6s %6s %6s   %10s %10s   %10s %10s"
          % ("lang", "core2", "core3", "naive2", "naive3",
             "compile2", "compile3"))
    for i in range(len(LANGS)):
        a = old["languages"][i]
        b = red["languages"][i]
        print("%-6s %6d %6d   %10d %10d   %10d %10d"
              % (b["language"], a["extracted_scalar_core_size"],
                 b["extracted_scalar_core_size"],
                 a["naive_cross_product"], b["naive_cross_product"],
                 a["must_compile"], b["must_compile"]))
    print("%-6s %6s %6s   %10d %10d   %10d %10d"
          % ("TOTAL", "", "", old["totals"]["naive"], red["totals"]["naive"],
             old["totals"]["must_compile"], red["totals"]["must_compile"]))
    print("wrote %s" % path)

    cmd = [sys.executable, os.path.join(HERE, "check_no_spelling_keys.py"),
           path]
    done = subprocess.run(cmd, capture_output=True, text=True)
    print(done.stdout.strip())
    if done.returncode != 0:
        print(done.stderr.strip())
        os.remove(path)
        raise SystemExit("REFUSED OWN OUTPUT: spelling guard failed")


if __name__ == "__main__":
    main()
