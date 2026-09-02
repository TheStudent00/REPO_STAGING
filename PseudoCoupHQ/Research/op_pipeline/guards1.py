#!/usr/bin/env python3
"""guards1.py -- STEP 4 of THE JOB. One row per (unit, guard),
condition/response/detection/language, read straight off
seeds1.json's per-unit guard lists (already the raw material core_
modes + the inline-alternate-path resolution produced). No operator
token in any key -- the operator appears once per row as a display
field only (`operator`), never as a grouping/pairing key; this file
groups NOTHING, it only lists rows, so check_no_spelling_keys.py is
run over it as the mechanical guard requires.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    seeds = json.load(open(os.path.join(HERE, "seeds1.json")))["seeds"]
    rows = []
    for unit_id, s in seeds.items():
        lang = s["lang"]
        for g in s.get("guards", []):
            rows.append(dict(
                unit=unit_id,
                language=lang,
                condition=g.get("condition"),
                response_kind=g.get("response") or g.get("kind"),
                detection=g.get("detection"),
            ))
    by_kind = {}
    for r in rows:
        by_kind[r["response_kind"]] = by_kind.get(r["response_kind"], 0) + 1
    out = dict(
        meta=dict(
            generator="guards1.py",
            role_note="raw material for the exception-family table "
                       "(next lap); one row per (unit, guard); no "
                       "operator token in any key -- see module "
                       "docstring.",
            row_count=len(rows),
            by_response_kind=by_kind,
        ),
        rows=rows)
    json.dump(out, open(os.path.join(HERE, "guards.json"), "w"), indent=1)
    print(json.dumps(dict(row_count=len(rows), by_response_kind=by_kind), indent=2))


if __name__ == "__main__":
    main()
