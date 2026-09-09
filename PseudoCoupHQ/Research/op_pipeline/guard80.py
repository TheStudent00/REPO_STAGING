#!/usr/bin/env python3
"""guard80.py -- the UNMODIFIED spelling-key check over every JSON
artifact task 80 writes, in ONE process.

WHAT IS REUSED RATHER THAN COPIED.  `guard66.py`'s own `run_guard`
does the work; this file only names task 80's artifacts.  The guard
itself, `check_no_spelling_keys.py`, is run as a separate process and
is not imported, not edited, and not given a field whitelist or an
exemption.

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

Coding discipline: no compound one-liner statements.
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import guard66 as G66                                            # noqa: E402

TRANSCRIPT = os.path.join(HERE, "guard80_transcript.txt")
SUMMARY = os.path.join(HERE, "guard80.json")


def task80_paths():
    """every JSON artifact task 80 writes.  Nothing is declared out of
    the walk."""
    out = []
    named = [
        "probe80_conditional_shapes.json",
        "render_back80_E00029.json",
        "render_back80_tally.json",
        "render_back80_state.json",
    ]
    for name in named:
        path = os.path.join(HERE, name)
        if os.path.exists(path):
            out.append(path)
    pattern = os.path.join(HERE, "render_back80_store", "*.json")
    out.extend(sorted(glob.glob(pattern)))
    return out


def main(argv):
    paths = task80_paths()
    counts = G66.run_guard(
        paths, TRANSCRIPT,
        "guard80.py -- every JSON artifact task 80 writes, unmodified "
        "guard, ONE process.  Nothing was added to any field set, and "
        "no artifact was declared out of the walk.")
    print("TASK 80: %d paths  PASS %d  FAIL %d  exempt %d  exit %d"
          % (counts["paths"], counts["pass_lines"],
             counts["fail_lines"], counts["exempt_lines"],
             counts["exit_code"]))
    handle = open(SUMMARY, "w")
    json.dump({
        "meta": {
            "produced_by": "guard80.py",
            "guard": "check_no_spelling_keys.py, unmodified, run as a "
                     "separate process; nothing added to any field "
                     "set, no exemption declared",
        },
        "task80_artifacts": counts,
    }, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    if counts["fail_lines"]:
        return 1
    if counts["exempt_lines"]:
        return 1
    return counts["exit_code"]


if __name__ == "__main__":
    sys.exit(main(sys.argv))
