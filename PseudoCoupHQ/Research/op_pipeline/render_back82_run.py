#!/usr/bin/env python3
"""render_back82_run.py -- the SECOND re-run of the return path, with
task 83's relink fix in `term.py` as well as the settled `ledger.py`.

WHY TWO RE-RUNS AND NOT ONE.  Task 80's owed re-run asks one question:
does the return path move when `ledger.py` settles?  Answering it means
changing one thing.  `render_back81_run.py` did exactly that -- settled
`ledger.py`, `term.py` as task 80 left it -- and its answer is on disk.
Task 83 then found and fixed a defect in `term.relink` (the relink was
not handed the runtime answer readings the render was handed), which is
a SECOND change to the same path.  Folding it into the first run would
have made neither question answerable.  So this file asks the second
question on its own: does the return path move when the relink fix
lands on top?

WHAT IS HELD FIXED: the same population (the 26,040 units of the 30,432
canon39-proved ones whose layer-4 term `term61_store` records as
proved), the same driver code, the same assembler, the same gate.

WHAT IS REUSED RATHER THAN COPIED.  `render_back81_run.run` is called
with this file's own store and state paths; through it,
`render_back80_run.walk_one_shard` and `render_back_run`'s `Assembler`,
`one_unit`, `proved_terms_of`, `new_tools` and `shards`.  Nothing is
re-typed.

MEMORY BOUND: one canon39 shard opened, walked and dropped before the
next; 6 GB resident with the named abort `ABORT_MEMORY`, checked by
`render_back80_run.check_memory`.

ONE PROCESS.  Resumable: `render_back82_state.json`.

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

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import render_back81_run as R81                                  # noqa: E402

STORE = os.path.join(HERE, "render_back82_store")
STATE = os.path.join(HERE, "render_back82_state.json")
LEDGER_NOTE = os.path.join(HERE, "render_back82_ledger_sha256.txt")


if __name__ == "__main__":
    budget = 36000
    if len(sys.argv) > 1:
        budget = int(sys.argv[1])
    R81.STORE = STORE
    R81.STATE = STATE
    R81.LEDGER_NOTE = LEDGER_NOTE
    finished = R81.run(budget)
    if not finished:
        sys.exit(3)
