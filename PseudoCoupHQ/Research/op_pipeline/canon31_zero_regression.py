#!/usr/bin/env python3
"""canon31_zero_regression.py -- TASK 26: prove this lap changed
nothing it was not supposed to change.

The check: every unit whose canon29_units_<lang>.json `status` is
"converged" (the 1,561 baseline of record) is compared field by field
against its canon31_units_<lang>.json record. Every field the
baseline carries must be byte-identical. Fields canon31 ADDS are
listed by name and counted, never waved past.

It also recounts the converged totals from disk rather than from any
report's arithmetic, and separately counts the units this lap's
branching audit withdrew (recorded status still "converged", audit
verdict not PROVED_EQUAL) -- the honest standing total is printed
beside the recorded one.

Coding discipline: no complex/compound one-liner statements.

usage:
  canon31_zero_regression.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANGS = ["c", "cpp", "go", "rust", "swift"]

ADDED_FIELD_PREFIX = "job8_"


def main():
    checked = 0
    differences = []
    added_fields = {}
    recorded_converged = 0
    withdrawn = 0
    per_lang = {}
    for lang in LANGS:
        p29 = os.path.join(HERE, "canon29_units_%s.json" % lang)
        p31 = os.path.join(HERE, "canon31_units_%s.json" % lang)
        u29 = json.load(open(p29))["units"]
        u31 = json.load(open(p31))["units"]
        before = 0
        after = 0
        for n, rec29 in u29.items():
            if rec29.get("status") == "converged":
                before = before + 1
            rec31 = u31.get(n)
            if rec31 is None:
                differences.append("%s/%s missing from canon31"
                                   % (lang, n))
                continue
            if rec29.get("status") != "converged":
                continue
            checked = checked + 1
            for field, value in rec29.items():
                if field not in rec31:
                    differences.append(
                        "%s/%s lost field %r" % (lang, n, field))
                    continue
                if json.dumps(rec31[field], sort_keys=True) != \
                        json.dumps(value, sort_keys=True):
                    differences.append(
                        "%s/%s field %r changed" % (lang, n, field))
            for field in rec31:
                if field in rec29:
                    continue
                added_fields[field] = added_fields.get(field, 0) + 1
                if not field.startswith(ADDED_FIELD_PREFIX):
                    differences.append(
                        "%s/%s gained unexpected field %r"
                        % (lang, n, field))
        for n, rec31 in u31.items():
            if rec31.get("status") == "converged":
                after = after + 1
                verdict = rec31.get("job8_branching_audit_verdict")
                if verdict is not None:
                    if verdict != "PROVED_EQUAL":
                        withdrawn = withdrawn + 1
        per_lang[lang] = (before, after)
        recorded_converged = recorded_converged + after
    print("baseline converged units compared field by field: %d"
          % checked)
    print("differences found: %d" % len(differences))
    for d in differences[:40]:
        print("   ", d)
    print("fields canon31 ADDED to baseline records: %r"
          % added_fields)
    print("per-language converged, canon29 -> canon31:")
    total_before = 0
    for lang in LANGS:
        before, after = per_lang[lang]
        total_before = total_before + before
        print("   %-6s %4d -> %4d  (%+d)"
              % (lang, before, after, after - before))
    print("   TOTAL  %4d -> %4d  (%+d)"
          % (total_before, recorded_converged,
             recorded_converged - total_before))
    print("branching-audit WITHDRAWN (recorded converged, re-gate "
          "against real ship blocks did not prove): %d" % withdrawn)
    print("honest standing converged total: %d"
          % (recorded_converged - withdrawn))
    if differences:
        print("ZERO-REGRESSION CHECK: FAIL")
        sys.exit(1)
    print("ZERO-REGRESSION CHECK: PASS")


if __name__ == "__main__":
    main()
