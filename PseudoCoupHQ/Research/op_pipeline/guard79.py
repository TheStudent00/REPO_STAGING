#!/usr/bin/env python3
"""guard79.py -- the UNMODIFIED spelling-key guard over every JSON
artifact task 79 writes, run as ONE process.

Nothing is added to any field set, no artifact is declared out of the
walk, and no exemption is declared anywhere.

WRITES:
  guard79_transcript.txt
  guard79.json

Coding discipline: no compound one-liner statements.

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
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GUARD = os.path.join(HERE, "check_no_spelling_keys.py")
TRANSCRIPT = os.path.join(HERE, "guard79_transcript.txt")
SUMMARY = os.path.join(HERE, "guard79.json")

WRITTEN = [
    "normalize79_walk_walk1.json",
    "normalize79_walk_walk2.json",
    "normalize79_walk_walk3.json",
    "normalize79_walk_pre78_walk1.json",
    "normalize79_walk_pre78_walk2.json",
    "normalize79_walk_pre78_walk3.json",
    "acceptance79.json",
    "acceptance79_pre78.json",
    "normalize79_pool_prediction.json",
    "normalize79_split_causes.json",
    "normalize79_cause.json",
]


def task79_paths():
    out = []
    for name in WRITTEN:
        path = os.path.join(HERE, name)
        if os.path.exists(path):
            out.append(path)
        else:
            raise SystemExit(
                "REFUSED OWN OUTPUT: an artifact task 79 writes is "
                "missing from the walk: %s" % name)
    return out


def main(argv):
    paths = task79_paths()
    command = [sys.executable, GUARD]
    command.extend(paths)
    proc = subprocess.run(command, capture_output=True, text=True)
    text = proc.stdout + proc.stderr
    handle = open(TRANSCRIPT, "w")
    handle.write("guard79.py -- every JSON artifact task 79 writes, "
                 "unmodified guard, ONE process.  Nothing was added to "
                 "any field set, and no artifact was declared out of "
                 "the walk.\n\n")
    handle.write("command: %s ... (%d paths)\n\n"
                 % (" ".join(command[:2]), len(paths)))
    handle.write(text)
    handle.close()
    passes = text.count("PASS")
    fails = text.count("FAIL")
    exempt = 0
    for line in text.splitlines():
        if "exempt" in line:
            exempt = exempt + 1
    print("TASK 79: %d paths  PASS %d  FAIL %d  exempt %d  exit %d"
          % (len(paths), passes, fails, exempt, proc.returncode))
    handle = open(SUMMARY, "w")
    json.dump({
        "meta": {
            "produced_by": "guard79.py",
            "guard": "check_no_spelling_keys.py, unmodified, run as a "
                     "separate process; nothing added to any field "
                     "set, no exemption declared",
        },
        "task79_artifacts": {
            "paths": len(paths),
            "pass_lines": passes,
            "fail_lines": fails,
            "exempt_lines": exempt,
            "exit_code": proc.returncode,
        },
    }, handle, indent=1, sort_keys=True)
    handle.write("\n")
    handle.close()
    if fails:
        return 1
    if exempt:
        return 1
    return proc.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv))
