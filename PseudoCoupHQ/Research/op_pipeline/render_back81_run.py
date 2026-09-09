#!/usr/bin/env python3
"""render_back81_run.py -- TASK 83's owed re-run of the return path
(`term.RenderBack`, node 0_3_5_6_5) against the SETTLED `ledger.py`.

WHY THIS FILE EXISTS.  Task 80 ran `render_back80_run.py` while task 78
was still editing `ledger.py`; `log_185` section 9.2 records the settled
blob as sha256 `90d05e6b0b086b2125f8743684c4c67c1201e0c63cf78f6d1ceeb49031da2c6f`
and `log_187` section 12 names the re-run as the first thing a next lap
should do.  This is that re-run.

WHAT IS HELD FIXED, so the comparison is like-for-like.  Everything
except `ledger.py`: the same population (the 26,040 units of the 30,432
canon39-proved ones whose layer-4 term `term61_store` records as
proved), the same driver code, the same assembler, the same gate.  A
different population would make the difference between this run and
task 80's un-attributable, which is the whole point of the re-run.

WHAT IS REUSED RATHER THAN COPIED.  This file imports
`render_back80_run` and calls its `walk_one_shard`, and through it
`render_back_run`'s `Assembler`, `one_unit`, `proved_terms_of`,
`new_tools` and `shards`.  Nothing of either driver is re-typed here;
what is new is only WHERE the answers are written, so task 80's own
store stays on disk untouched as the record it is.

MEMORY BOUND, stated as the round requires: one canon39 shard is
opened, walked and dropped before the next; the bound is 6 GB resident,
checked after every shard, with the named abort `ABORT_MEMORY`.  The
check is `render_back80_run.check_memory`, called and not copied.

ONE PROCESS.  Resumable: `render_back81_state.json` names the shards
already written.

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

No operator token appears in this file.  The `operator` field of a unit
record is a display label the reused driver copies onto the member and
never reads, never groups on and never pairs on.

Coding discipline: no compound one-liner statements.
"""

import hashlib
import json
import os
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import render_back80_run as R80                                  # noqa: E402
import render_back_run as RB                                     # noqa: E402

STORE = os.path.join(HERE, "render_back81_store")
STATE = os.path.join(HERE, "render_back81_state.json")
LEDGER_NOTE = os.path.join(HERE, "render_back81_ledger_sha256.txt")


def ledger_sha256():
    """the blob of `ledger.py` THIS run read, written beside the store
    so the re-run can never be confused with task 80's."""
    handle = open(os.path.join(HERE, "ledger.py"), "rb")
    body = handle.read()
    handle.close()
    return hashlib.sha256(body).hexdigest()


def load_state():
    if not os.path.exists(STATE):
        return {"done": [], "started": time.time()}
    return json.load(open(STATE))


def save_state(state):
    handle = open(STATE, "w")
    json.dump(state, handle, indent=1, sort_keys=True)
    handle.close()


def run(budget_seconds):
    if not os.path.isdir(STORE):
        os.makedirs(STORE)
    digest = ledger_sha256()
    handle = open(LEDGER_NOTE, "w")
    handle.write(digest + "  ledger.py\n")
    handle.close()
    print("ledger.py sha256 %s" % digest)
    sys.stdout.flush()
    state = load_state()
    done = set(state["done"])
    tools = RB.new_tools()
    assembler = RB.Assembler(tools[3])
    started = time.time()
    every = RB.shards()
    for path in every:
        key = os.path.relpath(path, HERE)
        if key in done:
            continue
        if time.time() - started > budget_seconds:
            print("budget spent; %d shards still to walk"
                  % (len(every) - len(done)))
            sys.stdout.flush()
            return False
        out, skipped, rendered = R80.walk_one_shard(path, tools,
                                                    assembler)
        written = os.path.join(STORE, key.replace("/", "__"))
        handle = open(written, "w")
        json.dump({"shard": key,
                   "skipped_no_proved_term": skipped,
                   "ledger_sha256": digest,
                   "units": out}, handle, sort_keys=True)
        handle.close()
        done.add(key)
        state["done"] = sorted(done)
        save_state(state)
        peak = R80.check_memory()
        print("%s: %d with proved terms, %d rendered, %d skipped, "
              "peak %d kB" % (key, len(out), rendered, skipped, peak))
        sys.stdout.flush()
    print("all %d shards walked" % len(done))
    return True


if __name__ == "__main__":
    budget = 36000
    if len(sys.argv) > 1:
        budget = int(sys.argv[1])
    finished = run(budget)
    if not finished:
        sys.exit(3)
