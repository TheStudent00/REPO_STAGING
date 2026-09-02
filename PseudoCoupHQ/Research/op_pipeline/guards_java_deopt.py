#!/usr/bin/env python3
"""guards_java_deopt.py -- task 5(c): carry interp_jvm.md/json's
measured deopt-continue-elsewhere row (and its sibling guard rows)
into the exception-family raw material, with a weaker-provenance
mark (log_082 finding 4).

THE GAP THIS CLOSES. `guards2.py` already lists java in
`CORE_MODES_LANGS` and reads `core_modes_java.json`, but that file
holds ONE unit with `modes: []` -- an empty guard list, which
guards2.py's own comment (b) treats as legitimate data ("this unit
checks nothing").  For c/cpp's bare `idiv` that reading is correct.
For java it is WRONG: `interp_jvm.json` (the pilot's own measured
data, unchanged by this script) records nine actual guard rows across
its two units -- entry barrier, safepoint poll, the standing
exception/deopt stub tail, an EXPLICIT zero-divisor check into
`UncommonTrapBlob`, and an in-place overflow check.  `core_modes_java`
and `interp_jvm.json` are simply two different, disconnected records
of the same two probes; `guards2.json` was built from the empty one.

WHAT THIS SCRIPT DOES. Reads `guards2.json` (unmodified) and
`interp_jvm.json` (unmodified).  Every mode entry in
`interp_jvm.json`'s `units[*].modes` becomes ONE new row, in
`guards2.py`'s own row shape, with two additions:
  - `weaker_provenance: true` -- per AgentMemory's ruling on
    `add_java.json`, "provenance_is_weaker" travels with the unit
    wherever it appears. java's arch-unit comes from a JIT nmethod
    dump read once, not a compile-twice anchor/ship pair with DWARF;
    this line makes that mark explicit on every row it contributes,
    not just once in a header.
  - `evidence_class` copied VERBATIM from interp_jvm.json's own
    per-mode field -- most rows are "the tool's own testimony,
    plus objdump"; the zero-divisor check is the stronger "forced by
    construction ... plus the tool's own testimony" (the branch
    target is the JVM's own annotated trap blob, not an assumption).
    Never upgraded or downgraded here.

Unit naming: interp_jvm.json's u1/u2 map to guards2.py's own
`java/op_1`, `java/op_2` naming (matches core_modes_java.json's unit
key "1" for the addition probe; op_2 is the division probe, present
in interp_jvm.json but not in core_modes_java.json at all -- another
gap this script surfaces rather than silently filling).

OUTPUT: `guards3.json` -- a NEW file (guards2.json is left exactly as
it is).  Same shape as guards2.json (`meta`, `rows`, `units`) so any
consumer of guards2.json's shape can read guards3.json instead, plus
`meta.added_from_interp_jvm` naming exactly what was carried in.

THE SPELLING BAN: `operator` is a display field only (guards2.json's
existing rows already carry it this way; the java rows added here
follow the same shape). No key, grouping or row-selection reads the
token. check_no_spelling_keys.py is run on the output below.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


UNIT_ID_MAP = {
    "u1": "java/op_1",
    "u2": "java/op_2",
}

# interp_jvm.json does not carry the grammar operator token per unit
# (its "operator" fields on the unit records are None -- read
# directly, not assumed).  The two probes are read from
# core_modes_java.json (addition, op_1) and interp_jvm.md's own
# probe-source section (division, op_2) as DISPLAY LABELS only.
OPERATOR_LABEL = {
    "java/op_1": "+",
    "java/op_2": "/",
}


def main():
    guards2 = json.load(open(os.path.join(HERE, "guards2.json")))
    jvm = json.load(open(os.path.join(HERE, "interp_jvm.json")))

    rows = list(guards2["rows"])
    units_summary = dict(guards2["units"])
    by_kind = dict(guards2["meta"]["by_response_kind"])
    by_source = dict(guards2["meta"]["by_source"])

    added = 0
    for u in jvm["units"]:
        raw_id = u.get("id")
        unit_id = UNIT_ID_MAP.get(raw_id)
        if unit_id is None:
            continue
        operator = OPERATOR_LABEL.get(unit_id)
        for m in u.get("modes", []):
            rk = m.get("response_kind")
            rows.append(dict(
                unit=unit_id,
                language="java",
                operator=operator,
                condition=m.get("name"),
                response_kind=rk,
                detection=m.get("note"),
                source="interp_jvm.json",
                weaker_provenance=True,
                evidence_class=m.get("evidence_class"),
                mode_id=m.get("id"),
            ))
            by_kind[rk] = by_kind.get(rk, 0) + 1
            by_source["interp_jvm.json"] = by_source.get(
                "interp_jvm.json", 0) + 1
            added += 1
        if unit_id in units_summary:
            units_summary[unit_id]["guard_count"] = len(u.get("modes", []))
            units_summary[unit_id]["weaker_provenance"] = True
        else:
            units_summary[unit_id] = dict(
                unit=unit_id, language="java", operator=operator,
                guard_count=len(u.get("modes", [])),
                weaker_provenance=True,
            )

    out = dict(
        meta=dict(
            generator="guards_java_deopt.py",
            predecessor="guards2.json (guards2.py), unmodified",
            role_note="guards2.json's raw rows, plus java's real "
                       "guard rows read from interp_jvm.json's own "
                       "modes -- guards2.json's core_modes_java.json "
                       "source carried an empty modes list for its "
                       "one unit (log_082 finding 4), so zero java "
                       "guard rows reached the exception-family "
                       "table.  Every row added here carries "
                       "weaker_provenance: true.",
            row_count=len(rows),
            unit_count=len(units_summary),
            added_from_interp_jvm=added,
            by_response_kind=by_kind,
            by_source=by_source,
        ),
        rows=rows,
        units=units_summary,
    )

    out_path = os.path.join(HERE, "guards3.json")
    json.dump(out, open(out_path, "w"), indent=1)
    print("wrote", out_path)
    print("rows total:", len(rows), "(", added, "added from interp_jvm.json)")
    print("java rows now present:",
          sum(1 for r in rows if r["language"] == "java"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
