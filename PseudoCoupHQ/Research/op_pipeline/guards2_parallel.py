#!/usr/bin/env python3
"""guards2_parallel.py -- Task 5(c): carry interp_jvm.md's ONE measured
deopt-continue-elsewhere row (java's division unit, u2.m3, forced by
construction) into the exception-family raw material, with its
weaker-provenance mark, WITHOUT touching guards2.json.

FINDING 4 (log_082 PART 2): core_modes_java.json holds one unit
(the addition) with empty modes, so guards2.json carries zero java
guard rows and the 34 exception families were built without the only
non-C-family deopt evidence in the corpus.

This file does not re-run guards2.py's full sweep (that would rewrite
guards2.json in place). It loads guards2.json's own rows/units
UNCHANGED, and appends exactly the rows core_modes_java2.json adds
(this task's own new file -- see that file's `provenance_note`),
carrying `provenance_is_weaker: true` on every added row so a reader
of guards2_parallel.json can never mistake it for equal-strength
evidence.

usage:
  guards2_parallel.py
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    base = json.load(open(os.path.join(HERE, "guards2.json")))
    rows = list(base["rows"])
    units_summary = dict(base["units"])
    by_kind = dict(base["meta"]["by_response_kind"])
    by_source = dict(base["meta"]["by_source"])

    extra_path = os.path.join(HERE, "core_modes_java2.json")
    d = json.load(open(extra_path))
    added = 0
    for n, u in d["units"].items():
        unit_id = "java/op_%s" % n
        operator = u.get("operator")
        modes = u.get("modes", [])
        for m in modes:
            rk = m.get("response")
            rows.append(dict(
                unit=unit_id,
                language="java",
                operator=operator,
                condition=m.get("condition"),
                response_kind=rk,
                detection=m.get("detection"),
                source="core_modes_java2 (Task 5c retrofit)",
                provenance_is_weaker=True,
            ))
            by_kind[rk] = by_kind.get(rk, 0) + 1
            by_source["core_modes_java2"] = (
                by_source.get("core_modes_java2", 0) + 1)
            added += 1
        prior = units_summary.get(unit_id)
        base_count = prior["guard_count"] if prior else 0
        units_summary[unit_id] = dict(
            unit=unit_id, language="java", operator=operator,
            guard_count=base_count + len(modes),
            provenance_is_weaker=True)

    zero_guard_units = sum(1 for v in units_summary.values()
                            if v["guard_count"] == 0)

    out = dict(
        meta=dict(
            generator="guards2_parallel.py",
            role_note="guards2.json's own rows, UNCHANGED, plus the "
                       "java division unit's measured deopt-continue-"
                       "elsewhere guard (interp_jvm.json u2.m3), added "
                       "with its weaker-provenance mark. Task 5(c) of "
                       "log_083. No operator token in any key -- see "
                       "module docstring.",
            row_count=len(rows),
            unit_count=len(units_summary),
            zero_guard_unit_count=zero_guard_units,
            rows_added_this_file=added,
            by_response_kind=by_kind,
            by_source=by_source,
            predecessor="guards2.json (guards2.py, 305 rows, java "
                        "absent from the guard evidence)",
        ),
        rows=rows,
        units=units_summary,
    )
    out_path = os.path.join(HERE, "guards2_parallel.json")
    json.dump(out, open(out_path, "w"), indent=1)
    print("wrote %s" % out_path)
    print("rows: %d (base %d + %d added)"
          % (len(rows), len(base["rows"]), added))


if __name__ == "__main__":
    main()
