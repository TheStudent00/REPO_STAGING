#!/usr/bin/env python3
"""render_back82_tally.py -- the tally over `render_back82_store/`,
the return path with task 83's relink fix as well as the settled
`ledger.py`, beside `render_back81_store/`, which is the same path with
the settled `ledger.py` alone.

The comparison is therefore ONE CHANGE: the relink fix.

WHAT IS REUSED RATHER THAN COPIED.  `render_back_tally.walk` and
`.report` are the tally; `render_back80_tally.difference_section` is
the count-by-count comparison; `render_back81_tally.per_unit_difference`
and `.read_store` are the unit-by-unit comparison.  Nothing is
re-typed.

THE SPELLING BAN, pasted verbatim as required:

"THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim."

No operator token appears in this file.

Coding discipline: no compound one-liner statements.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import render_back80_tally as R80T                                # noqa: E402
import render_back81_tally as R81T                                # noqa: E402
import render_back_tally as RT                                    # noqa: E402

STORE = os.path.join(HERE, "render_back82_store")
BEFORE_STORE = os.path.join(HERE, "render_back81_store")
BEFORE = os.path.join(HERE, "render_back81_tally.json")
OUT = os.path.join(HERE, "render_back82_tally.json")
PRINTED = os.path.join(HERE, "render_back82_tally_printed.txt")
LEDGER_NOTE = os.path.join(HERE, "render_back82_ledger_sha256.txt")


def main():
    RT.STORE = STORE
    document = RT.walk()
    handle = open(LEDGER_NOTE)
    digest = handle.read().strip()
    handle.close()
    document["meta"] = {
        "produced_by": "render_back82_tally.py",
        "read_from": "render_back82_store/",
        "node": "hq.research.compiler_graph.term.render_back",
        "what_changed": "task 83's relink fix in term.py -- the relink "
                        "is handed the runtime answer readings and the "
                        "toolchain the render was handed.  ledger.py "
                        "is the same settled blob render_back81 read, "
                        "so this comparison isolates the relink fix.",
        "ledger_sha256": digest,
        "population": "the same 26,040 units of the 30,432 "
                      "canon39-proved ones whose layer-4 term "
                      "term61_store records as proved",
    }
    before = None
    if os.path.exists(BEFORE):
        before = json.load(open(BEFORE))
    printed = RT.report(document)
    printed = printed.replace("computed from render_back_store/",
                              "computed from render_back82_store/")
    comparison = R80T.difference_section(document, before)
    for index, line in enumerate(comparison):
        comparison[index] = line.replace(
            "AGAINST ROUND 13 (read off render_back_tally.json, "
            "the artifact, not a log)",
            "AGAINST THE SETTLED-LEDGER RE-RUN (read off "
            "render_back81_tally.json, the artifact, not a log)")
        comparison[index] = comparison[index].replace(
            "  count                                      round 13 this round",
            "  count                                     rb81   this re-run")
    printed = printed + "\n".join(comparison) + "\n"
    now_store = R81T.read_store(STORE)
    before_store = R81T.read_store(BEFORE_STORE)
    lines, per_unit = R81T.per_unit_difference(now_store, before_store)
    for index, line in enumerate(lines):
        lines[index] = line.replace("against task 80's own store",
                                    "against render_back81_store")
    document["per_unit_against_render_back81"] = per_unit
    printed = printed + "\n".join(lines) + "\n"
    handle = open(OUT, "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    handle = open(PRINTED, "w")
    handle.write(printed)
    handle.close()
    sys.stdout.write(printed)


if __name__ == "__main__":
    main()
