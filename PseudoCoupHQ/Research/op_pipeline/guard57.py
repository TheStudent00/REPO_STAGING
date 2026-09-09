#!/usr/bin/env python3
"""guard57.py -- THE GUARD for task 57: the UNMODIFIED
check_no_spelling_keys.py, ONE process, over every file this task
writes.

This file RUNS `check_no_spelling_keys.py` as a separate process, with
its own interpreter.  It adds NOTHING to any field set, declares no
exemption, and edits no guard file.  Log 147 section 13.7's lesson is
the rule here: a stage that quiets the checker about its own field has
failed.

WHAT IS WALKED: `acceptance57.json` and `coverage57.json` -- every
JSON artifact task 57 writes.  Both declare `role: generator
provenance` on their own `meta`, which is a per-artifact provenance
record, not a field-set addition; nothing is added to any field set
here and no exemption is declared, so `grep -c exempt` over the
transcript must be 0.

usage:
  guard57.py

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
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GUARD = os.path.join(HERE, "check_no_spelling_keys.py")
TRANSCRIPT = os.path.join(HERE, "guard57_transcript.txt")
SUMMARY = os.path.join(HERE, "guard57.json")


def task57_paths():
    out = []
    out.append(os.path.join(HERE, "acceptance57.json"))
    out.append(os.path.join(HERE, "coverage57.json"))
    live = []
    for path in out:
        if os.path.exists(path):
            live.append(path)
    return live


def run_guard(paths, transcript_path, heading):
    command = [sys.executable, GUARD] + paths
    proc = subprocess.run(command, capture_output=True, text=True)
    handle = open(transcript_path, "w")
    handle.write("%s\n" % heading)
    handle.write("$ python3 check_no_spelling_keys.py "
                 "<%d paths, one process>\n\n" % len(paths))
    handle.write(proc.stdout)
    if proc.stderr.strip():
        handle.write("\n-- stderr --\n")
        handle.write(proc.stderr)
    handle.write("\nGUARD EXIT CODE = %d\n" % proc.returncode)
    handle.close()
    text = proc.stdout
    counts = {
        "paths": len(paths),
        "pass_lines": text.count("\nPASS ") + int(
            text.startswith("PASS ")),
        "fail_lines": text.count("\nFAIL ") + int(
            text.startswith("FAIL ")),
        "exempt_lines": 0,
        "exit_code": proc.returncode,
    }
    for line in text.splitlines():
        if "exempt" in line:
            counts["exempt_lines"] = counts["exempt_lines"] + 1
    return counts


def main(argv):
    paths = task57_paths()
    counts = run_guard(
        paths, TRANSCRIPT,
        "guard57.py -- every artifact task 57 writes, unmodified "
        "guard, ONE process.  Nothing was added to any field set, "
        "and no artifact was declared out of the walk.")
    print("TASK 57: %d paths  PASS %d  FAIL %d  exempt %d  exit %d"
          % (counts["paths"], counts["pass_lines"],
             counts["fail_lines"], counts["exempt_lines"],
             counts["exit_code"]))
    handle = open(SUMMARY, "w")
    json.dump({
        "meta": {
            "produced_by": "guard57.py",
            "guard": "check_no_spelling_keys.py, unmodified, run as a "
                     "separate process; nothing added to any field "
                     "set, no exemption declared",
        },
        "task57_artifacts": counts,
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
