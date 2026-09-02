#!/usr/bin/env python3
"""guards2.py -- completes THE JOB's step 1 (COMPLETE THE GUARD DATA).

guards1.py (44 rows) read only seeds1.json, which holds only the 68
BRANCHING units seed_extract1.py processed (5 languages, erasure=="ok"
units with more than one block). That missed:

  (a) every core_modes_*.json unit seed_extract1.py never touched:
      single-block units (route 2/solver-localized modes only reach
      those), java (seed_extract1's LANGS list omits it), and any
      branching unit whose seed stayed UNRESOLVED -- core_modes does
      not care about seed resolution, it records modes per unit
      regardless.
  (b) the EMPTY guard list as data: a unit with zero modes is the row
      "this unit checks nothing" and guard_count 0 is recorded for
      every unit, not just guarded ones -- this is how c/cpp's
      undefined-behaviour stance (bare `idiv`, no branch, no trap)
      becomes visible in the table at all.
  (c) seed_extract1.py's own EXTRA guard kind, `inline-special-case`
      (the go/op_132 b==-1 disjoint-return-group shape), which is
      NOT a core_modes mode at all -- it is seed_extract1's own
      resolution-by-table-lookup layer on top of core_modes, so it is
      folded in from seeds1.json separately, taking only rows of that
      kind (trap-or-panic rows from seeds1 are the same rows already
      swept straight from core_modes -- taking both would double them).

One row per (unit, guard). Every unit gets a units[] entry with
guard_count, including 0. No operator token in any key, grouping,
pairing, row structure, candidate selection or comparison scope
(THE SPELLING BAN) -- `operator` is a display field only, same as
guards1.py. check_no_spelling_keys.py is run on the output.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))

CORE_MODES_LANGS = ["c", "cpp", "go", "java", "rust", "swift"]


def main():
    rows = []
    units_summary = {}
    by_kind = {}
    by_source = {}

    for lang in CORE_MODES_LANGS:
        path = os.path.join(HERE, "core_modes_%s.json" % lang)
        if not os.path.exists(path):
            continue
        d = json.load(open(path))
        for n, u in d["units"].items():
            unit_id = "%s/op_%s" % (lang, n)
            operator = u.get("operator")
            modes = u.get("modes", [])
            for m in modes:
                rk = m.get("response")
                rows.append(dict(
                    unit=unit_id,
                    language=lang,
                    operator=operator,
                    condition=m.get("condition"),
                    response_kind=rk,
                    detection=m.get("detection"),
                    source="core_modes",
                ))
                by_kind[rk] = by_kind.get(rk, 0) + 1
                by_source["core_modes"] = by_source.get("core_modes", 0) + 1
            # EMPTY IS DATA: every unit gets a units[] entry, guard_count
            # 0 included -- this is the only place a "checks nothing"
            # unit (e.g. c/cpp bare idiv, no branch, no trap) becomes a
            # row at all.
            units_summary[unit_id] = dict(
                unit=unit_id, language=lang, operator=operator,
                guard_count=len(modes))

    # fold in seed_extract1.py's own extra guard kind: inline-special-
    # case rows are NOT core_modes modes, they are seed_extract1's
    # disjoint-return-group resolution layer. trap-or-panic rows in
    # seeds1.json are copies of rows already swept above from
    # core_modes directly and are skipped here to avoid duplicating
    # them.
    seeds_path = os.path.join(HERE, "seeds1.json")
    extra = 0
    if os.path.exists(seeds_path):
        seeds = json.load(open(seeds_path))["seeds"]
        for unit_id, s in seeds.items():
            lang = s.get("lang")
            operator = s.get("operator")
            for g in s.get("guards", []):
                if g.get("kind") != "inline-special-case":
                    continue
                conds = g.get("conditions") or []
                cond_text = None
                if conds:
                    cond_text = conds[0].get("text") or conds[0].get("condition")
                rows.append(dict(
                    unit=unit_id,
                    language=lang,
                    operator=operator,
                    condition=cond_text,
                    response_kind=g.get("response"),
                    detection=g.get("detection"),
                    source="seeds1-inline-alternate-path",
                    seed_status=s.get("status"),
                ))
                rk = g.get("response")
                by_kind[rk] = by_kind.get(rk, 0) + 1
                by_source["seeds1-inline-alternate-path"] = \
                    by_source.get("seeds1-inline-alternate-path", 0) + 1
                extra += 1
                if unit_id in units_summary:
                    units_summary[unit_id]["guard_count"] += 1
                else:
                    # unit not in any core_modes_*.json we read (should
                    # not happen -- seed_extract1 sources core_modes
                    # itself -- but record honestly if it does).
                    units_summary[unit_id] = dict(
                        unit=unit_id, language=lang, operator=operator,
                        guard_count=1,
                        note="unit not found in core_modes_*.json sweep")

    zero_guard_units = sum(1 for v in units_summary.values()
                            if v["guard_count"] == 0)

    out = dict(
        meta=dict(
            generator="guards2.py",
            role_note="completed raw material for the exception-family "
                       "table: one row per (unit, guard), swept from "
                       "EVERY core_modes_<lang>.json unit (all "
                       "languages, single-block and branching, "
                       "resolved-seed and unresolved-seed alike) plus "
                       "seed_extract1.py's inline-special-case layer "
                       "from seeds1.json. No operator token in any key "
                       "-- see module docstring.",
            row_count=len(rows),
            unit_count=len(units_summary),
            zero_guard_unit_count=zero_guard_units,
            inline_special_case_folded_in=extra,
            by_response_kind=by_kind,
            by_source=by_source,
            predecessor="guards.json (guards1.py, 44 rows, seeds1.json "
                        "branching units only)",
        ),
        rows=rows,
        units=units_summary,
    )
    json.dump(out, open(os.path.join(HERE, "guards2.json"), "w"), indent=1)
    print(json.dumps(dict(
        row_count=len(rows),
        unit_count=len(units_summary),
        zero_guard_unit_count=zero_guard_units,
        inline_special_case_folded_in=extra,
        by_response_kind=by_kind,
        by_source=by_source,
    ), indent=2))


if __name__ == "__main__":
    main()
