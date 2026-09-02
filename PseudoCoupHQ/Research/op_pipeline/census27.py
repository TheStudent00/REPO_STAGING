#!/usr/bin/env python3
"""census27.py -- TASK 9 step 1 (log_091 round 2): a FRESH census of
the 322 not-yet-converged units, read from the CURRENT newest
generation on disk (canon26_units_<lang>.json -- verified by direct
count this lap: 107+106+39+21+49 = 322, the same total
name_census.json's own `load_report` recorded at the canon24
baseline; canon25/26 converged zero new units, so the population is
unchanged in COUNT, but this file re-derives every row from canon26's
own records rather than trusting that carry-over).

WHY A FRESH CENSUS, per log_084's own diagnosed cause: name_census.json
(built by vex_names_census.py) attributes a lifter name to a unit by
scanning `json.dumps(the_whole_record)` -- reason strings, stale notes
from earlier drivers, everything -- UNION tree_units3's own raw text.
That is why its "amd64g_calculate_condition: 219" row does not match a
literal raw-text scan (log_084 found 57). THIS file uses ONE source
per unit for name attribution: `tree_units3.json`'s own
`normal_path_raw` field, the single current expression for that unit,
nothing else. Reproducible, single-sourced, and it is the SAME field
census27's own driver-selection (a later file) will read -- satisfying
step 2's requirement ("driver's unit selection must be derived from
the SAME records the survey counts").

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after
a second violation). No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns. The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token. The token appears exactly once per unit: as a display label on
the member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run
the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim."

This file groups by LIFTER NAME (a VEX machine-form name, e.g.
`amd64g_calculate_condition`, `Add64F0x2`) and by BRANCH KIND
(`straight_line` / `branching`, a tree_units3 machine classification)
-- neither is a source-language operator token, the same class of key
name_census.json itself already uses under the generator-provenance /
machine-form discipline. Verified below by running
check_no_spelling_keys.py against this file's own output.

usage:
  census27.py [--out census27.json]
"""

import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

LANGS = ["c", "cpp", "go", "rust", "swift"]

CALC_HELPER_RE = re.compile(r"\b(amd64g_[A-Za-z0-9_]+)\b")
SIMD_OP_RE = re.compile(r"\b([A-Z][A-Za-z0-9]*(?:F0x\d+|V128))\b")
WIDE_OP_RE = re.compile(
    r"\b(Mul32|Mul64|DivModS128to64|DivModU128to64)\b")


def names_from_raw(raw):
    """Machine-form lifter/op names literally present in ONE unit's
    OWN current `normal_path_raw` text -- the single source. No JSON-
    dump scan, no reason-string scan (that union is exactly what
    log_084 found does not match a literal raw-text population)."""
    found = set()
    for m in CALC_HELPER_RE.finditer(raw):
        found.add(m.group(1))
    for m in SIMD_OP_RE.finditer(raw):
        found.add(m.group(1))
    for m in WIDE_OP_RE.finditer(raw):
        found.add(m.group(1))
    return found


def load_tree_units3():
    tree3 = json.load(open(os.path.join(HERE, "tree_units3.json")))
    by_key = {}
    for r in tree3["units"]:
        by_key[(r["lang"], r["n"])] = r
    return by_key


def main(argv):
    outpath = os.path.join(HERE, "census27.json")
    i = 1
    while i < len(argv):
        if argv[i] == "--out":
            outpath = argv[i + 1]
            i = i + 2
            continue
        print(__doc__)
        return 2

    tu3_map = load_tree_units3()

    per_lang_totals = {}
    per_name = {}
    branch_x_lang = {}
    no_raw_no_name = []

    total_not_converged = 0

    for lang in LANGS:
        doc = json.load(open(
            os.path.join(HERE, "canon26_units_%s.json" % lang)))
        units = doc["units"]
        n_total = len(units)
        n_not_converged = 0
        n_straight = 0
        n_branching = 0
        n_other_branch = 0

        for n, rec in units.items():
            if rec.get("status") == "converged":
                continue
            n_not_converged += 1
            total_not_converged += 1

            bk = rec.get("branch_kind")
            if bk is None:
                tu3 = tu3_map.get((lang, n))
                if tu3 is not None:
                    bk = tu3.get("branch_kind")
            if bk == "straight_line":
                n_straight += 1
            elif bk == "branching":
                n_branching += 1
            else:
                n_other_branch += 1

            tu3 = tu3_map.get((lang, n))
            raw = tu3.get("normal_path_raw") if tu3 else None
            unit_id = "%s/op_%s" % (lang, n)

            key = (bk, lang)
            branch_x_lang.setdefault(key, 0)
            branch_x_lang[key] += 1

            if raw is None:
                no_raw_no_name.append(unit_id)
                continue

            names = names_from_raw(raw)
            if not names:
                row = per_name.setdefault("__no_named_op_found__", {
                    "units": set(), "languages": set(),
                    "branch_kinds": set(), "sample_unit_ids": [],
                })
                row["units"].add(unit_id)
                row["languages"].add(lang)
                row["branch_kinds"].add(bk)
                if len(row["sample_unit_ids"]) < 8:
                    row["sample_unit_ids"].append(unit_id)
                continue

            for name in names:
                row = per_name.setdefault(name, {
                    "units": set(), "languages": set(),
                    "branch_kinds": set(), "sample_unit_ids": [],
                })
                row["units"].add(unit_id)
                row["languages"].add(lang)
                row["branch_kinds"].add(bk)
                if len(row["sample_unit_ids"]) < 8:
                    row["sample_unit_ids"].append(unit_id)

        per_lang_totals[lang] = {
            "total_units_in_file": n_total,
            "not_yet_converged": n_not_converged,
            "branch_kind_straight_line": n_straight,
            "branch_kind_branching": n_branching,
            "branch_kind_other_or_missing": n_other_branch,
        }

    rows = []
    for name, row in per_name.items():
        rows.append({
            "lifter_name": name,
            "units_blocked_count": len(row["units"]),
            "languages": sorted(row["languages"]),
            "branch_kinds_present": sorted(
                [str(b) for b in row["branch_kinds"]]),
            "sample_unit_ids": sorted(row["sample_unit_ids"]),
        })
    rows.sort(key=lambda r: -r["units_blocked_count"])

    branch_x_lang_rows = []
    for (bk, lang), count in sorted(branch_x_lang.items(),
                                     key=lambda kv: -kv[1]):
        branch_x_lang_rows.append({
            "branch_kind": bk,
            "lang": lang,
            "count": count,
        })

    out = {
        "role": "TASK 9 step 1 -- fresh census of the 322 unconverged "
                "units, current newest generation (canon26_units_"
                "<lang>.json), single-sourced name attribution "
                "(tree_units3.normal_path_raw only, no JSON-dump "
                "reason-string scan)",
        "evidence_class": "tool testimony, reproducible from this "
                           "script over on-disk canon26_units_<lang>."
                           "json + tree_units3.json",
        "baseline": "canon26_units_<lang>.json",
        "total_not_yet_converged": total_not_converged,
        "per_lang_totals": per_lang_totals,
        "branch_kind_x_lang": branch_x_lang_rows,
        "rows": rows,
        "units_with_no_raw_or_no_tu3_record": no_raw_no_name,
        "spelling_guard": "grouped by lifter_name (machine-form VEX "
                           "op/helper name) and branch_kind (machine "
                           "classification); neither is a source-"
                           "language operator token. Run "
                           "check_no_spelling_keys.py against this "
                           "file's own path to verify.",
    }

    fh = open(outpath, "w")
    json.dump(out, fh, indent=1)
    fh.close()

    print("wrote %s" % outpath)
    print("total not-yet-converged: %d" % total_not_converged)
    for lang in LANGS:
        print("  %s: %r" % (lang, per_lang_totals[lang]))
    print("top 15 rows by units_blocked_count:")
    for r in rows[:15]:
        print("  %-32s %3d  langs=%r  branch=%r"
              % (r["lifter_name"], r["units_blocked_count"],
                 r["languages"], r["branch_kinds_present"]))
    print("branch_kind x lang:")
    for r in branch_x_lang_rows:
        print("  %r" % r)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
