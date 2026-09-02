#!/usr/bin/env python3
"""build_guards5.py -- Task 19 step 4: add the `growing` mode row for
CPython's + (branch-to-alternate-computation) to the guard record of
record.  guards4.json is NOT modified -- this writes a NEW file,
guards5.json, that carries guards4.json's 313 rows verbatim plus ONE
new row, with provenance marks distinguishing it.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the
member. HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure. A brief handed to any subagent for this
line MUST paste this paragraph verbatim.

The new row's `operator` field is a per-unit display label on a unit
object (it carries a `language`/`unit` field identifying ONE row), the
same shape every other row in guards4.json already uses -- this file
does not add a new grouping shape, it adds one row of the existing
shape.
"""
import json

SRC = "guards4.json"
OUT = "guards5.json"

with open(SRC) as f:
    base = json.load(f)

base_rows = base["rows"]

new_row = {
    "unit": "cpython/long_add_fastpath",
    "language": "cpython",
    "operator": "+",
    "condition": "the operands are not both compact -- not _PyLong_BothAreCompact(a, b), i.e. at least one operand fails the cmp $0xf test at long_add+0x1f (the compact-fast-path unit carved in interp_fastpath.json is never entered)",
    "response_kind": "grows",
    "detection": "branch-to-alternate-computation",
    "source": "interp_fastpath.json (mode_reading_proposal.proposed_row) via TASK 19, proposal_representation_dimension.json",
    "provenance_is_weaker": True,
    "provenance_note": (
        "this row is a PROPOSAL, not a ratified measurement of the kind "
        "guards4.json's other 313 rows carry. It is the FIRST recorded "
        "instance of detection route 'branch-to-alternate-computation' "
        "(AgentMemory, the owner approved 2026-08-31) and the FIRST recorded "
        "instance of response_kind 'grows' in this corpus. Membership in "
        "any ratified table is the owner's call; this row exists so the guard "
        "record of record carries the fact for his ratification, per "
        "TASK 19 step 4."
    ),
    "first_grows_instance": True,
    "first_branch_to_alternate_computation_instance": True,
}

rows = list(base_rows) + [new_row]

by_response_kind = dict(base["meta"]["by_response_kind"])
by_response_kind["grows"] = by_response_kind.get("grows", 0) + 1

by_source = dict(base["meta"]["by_source"])
by_source["interp_fastpath.json (task19 proposal)"] = 1

meta = {
    "generator": "build_guards5.py",
    "role_note": (
        "THE GUARD RECORD OF RECORD, superseding guards4.json for "
        "downstream reads. guards4.json's 313 rows, UNMODIFIED and "
        "carried verbatim (guards4.json itself is untouched on disk), "
        "plus ONE new row: the `growing` mode row for CPython's + "
        "(branch-to-alternate-computation), added under TASK 19 step 4. "
        "guards4.json is preserved as a prior lineage entry, same as "
        "guards2_parallel.json/guards3.json were preserved when "
        "guards4.json superseded them."
    ),
    "predecessor": "guards4.json (build_guards5.py's only input)",
    "row_count": len(rows),
    "base_row_count": len(base_rows),
    "rows_added_this_file": 1,
    "by_response_kind": by_response_kind,
    "by_source": by_source,
}

out = {"meta": meta, "rows": rows}

with open(OUT, "w") as f:
    json.dump(out, f, indent=2)

print("wrote", OUT, "rows:", len(rows))
