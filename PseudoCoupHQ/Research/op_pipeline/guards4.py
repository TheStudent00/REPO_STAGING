#!/usr/bin/env python3
"""guards4.py -- Task 8(a)/(b): the ONE guard record of record.

WHAT GUARDS3.JSON ACTUALLY IS (Task 8(a), determined by reading
guards_java_deopt.py and diffing its output against guards2.json and
guards2_parallel.json): guards3.json is a FOLD, built directly on top
of guards2.json's own 305 unmodified rows, adding ALL EIGHT mode rows
found in interp_jvm.json's two units (u1 addition, u2 division) --
not merely the one division/deopt row. It is NOT a superset of
guards2_parallel.json and not built from it; the two are independent
forks off guards2.json:
  - guards2_parallel.json (log_087, Task 5c) carries exactly ONE java
    row -- the op_2 zero-divisor deopt guard, retrofit into
    core_modes.py's row shape, field `provenance_is_weaker`.
  - guards3.json (guards_java_deopt.py, undocumented in log_087)
    carries all 8 modes verbatim from interp_jvm.json (u1.m1, u1.m2,
    u1.m9, u2.m1, u2.m2, u2.m3, u2.m4, u2.m9), field `weaker_provenance`
    (different spelling of the same concept).
  guards3.json's java content is a strict superset of guards2_parallel's
  java content (its u2.m3 row is the same measured zero-divisor guard,
  differently phrased) -- see log_092's correction note for why
  log_087's claim that u2.m4/u2.m9 were "explicitly NOT carried" is
  false: guards3.json, sitting on disk in this same directory,
  carries them.

WHAT THIS SCRIPT DOES: takes guards2.json's 305 rows UNCHANGED as the
base (same base every fork used), and adds the 8 java rows using
guards3's fuller carry (all measured modes, not just the one), but
normalizes the provenance field name to `provenance_is_weaker`
(add_java.json's own field name -- the precedent named in the Task 8
brief) rather than guards3's `weaker_provenance`, so the record of
record uses one consistent field name for this mark everywhere.

OUTPUT: guards4.json -- meant to be the SINGLE guard record all
downstream exception-axis work reads from now on. guards2.json,
guards2_parallel.json and guards3.json are left exactly as they are
(new-files-only rule); they remain on disk as superseded attempts,
named here and in log_092.

THE SPELLING BAN, pasted verbatim as required: "No operator token may
appear in ANY key, grouping, pairing, row structure, candidate
selection, or comparison scope, anywhere in this line -- not in
matching, not in "which pairs get compared", not in report rows, not
in dropdowns. The candidate set for comparison comes from machine-form
evidence (clusters, connections, type pairs) or from ratified
intention -- never from the token. The token appears exactly once per
unit: as a display label on the member." `operator` here is a display
field only, exactly as guards2.json/guards3.json already treat it;
check_no_spelling_keys.py is run on the output below.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    guards2 = json.load(open(os.path.join(HERE, "guards2.json")))
    guards3 = json.load(open(os.path.join(HERE, "guards3.json")))

    rows = list(guards2["rows"])
    assert len(rows) == 305, "base row count drifted: %d" % len(rows)

    java_rows = [r for r in guards3["rows"] if r.get("language") == "java"]
    assert len(java_rows) == 8, "expected 8 java rows in guards3.json, got %d" % len(java_rows)

    by_kind = dict(guards2["meta"]["by_response_kind"])
    by_source = dict(guards2["meta"]["by_source"])

    for r in java_rows:
        row = dict(r)
        # normalize the provenance field name to add_java.json's own
        # spelling; drop the old-named field so there is one name.
        weaker = row.pop("weaker_provenance", True)
        row["provenance_is_weaker"] = bool(weaker)
        rows.append(row)
        rk = row["response_kind"]
        by_kind[rk] = by_kind.get(rk, 0) + 1
        by_source["interp_jvm.json"] = by_source.get("interp_jvm.json", 0) + 1

    out = dict(
        meta=dict(
            generator="guards4.py",
            role_note="THE GUARD RECORD OF RECORD (Task 8b). guards2.json's "
                       "305 rows, unmodified, plus all 8 measured java mode "
                       "rows carried in from guards3.json (itself sourced "
                       "verbatim from interp_jvm.json), with the provenance "
                       "mark's field name normalized to add_java.json's own "
                       "`provenance_is_weaker`. Supersedes guards2_parallel.json "
                       "(1 java row) and guards3.json (8 java rows, other field "
                       "name) as the single downstream source for the "
                       "exception axis.",
            predecessor="guards2.json (guards2.py) + guards3.json (guards_java_deopt.py)",
            row_count=len(rows),
            base_row_count=305,
            java_rows_added=len(java_rows),
            by_response_kind=by_kind,
            by_source=by_source,
        ),
        rows=rows,
    )

    out_path = os.path.join(HERE, "guards4.json")
    json.dump(out, open(out_path, "w"), indent=1)
    print("wrote", out_path)
    print("rows total:", len(rows), "(", len(java_rows), "java rows added)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
