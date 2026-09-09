#!/usr/bin/env python3
"""ledger_guard.py -- THE UNMODIFIED GUARD OVER EVERY TASK-59 JSON,
IN ONE PROCESS.

Runs `check_no_spelling_keys.py` as a separate process, unmodified,
over every JSON artifact task 59 wrote.  Nothing is added to any field
set, no exemption is declared, and no guard file is edited.  The
transcript is written to `ledger_guard_transcript.txt`, and
`grep -c exempt` over it must be 0.

Coding discipline: no compound one-liner statements.
"""

import glob
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
GUARD = os.path.join(HERE, "check_no_spelling_keys.py")
TRANSCRIPT = os.path.join(HERE, "ledger_guard_transcript.txt")

WRITTEN_BY_TASK_59 = [
    "runtime_callee_units.json",
    "runtime_callee_attachments.json",
    "out_of_scope_library_calls_superseded.json",
]


def main():
    paths = []
    for name in WRITTEN_BY_TASK_59:
        full = os.path.join(HERE, name)
        if os.path.exists(full):
            paths.append(full)
    argv = [sys.executable, GUARD] + paths
    done = subprocess.run(argv, capture_output=True, text=True)
    text = done.stdout + done.stderr
    header = ("# guard: check_no_spelling_keys.py, unmodified, one "
              "process, %d artifacts\n# exit %d\n"
              % (len(paths), done.returncode))
    open(TRANSCRIPT, "w").write(header + text)
    print(header + text, end="")
    return done.returncode


sys.exit(main())
