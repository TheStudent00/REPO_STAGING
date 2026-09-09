#!/usr/bin/env python3
"""run_with_peak.py -- run one of this directory's programs IN THIS
PROCESS and print the peak resident set size it reached.

WHY IT EXISTS. Round 15's memory rule (log_183, "ADDED THIS ROUND")
requires a peak resident size beside every pass over the diaries or the
graphs. `/usr/bin/time -v` is the usual way to get one and is not
guaranteed to be installed in the sandbox image, so the figure is taken
from the kernel through `resource.getrusage(RUSAGE_SELF).ru_maxrss`,
which needs nothing installed and is the same number.

It runs the target with `runpy` under `run_name="__main__"`, so the
target's own `main()` and its own argument parser are what execute --
this file adds no behaviour of its own and changes no result.

    python3 t81/run_with_peak.py graph.py join --graph ... --out ...

The exit code is the target's own. The peak line is printed to stdout
whether the target succeeded or failed, because a failed pass's memory
is exactly the number a memory gate needs.

Plan node: hq.research.compiler_graph.graph
(Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_9_graph/
CORE_0_3_5_9_graph.md).

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24);
(2) verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix
brief itself reintroduced it as "same-operator pairs"). MECHANICAL
GUARD REQUIRED: every pipeline stage that groups or pairs units must
run the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim.
"""

import os
import resource
import runpy
import sys
import time


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    target = sys.argv[1]
    sys.argv = sys.argv[1:]
    here = os.path.dirname(os.path.abspath(target))
    if here not in sys.path:
        sys.path.insert(0, here)
    started = time.time()
    code = 0
    try:
        runpy.run_path(target, run_name="__main__")
    except SystemExit as stop:
        code = stop.code if isinstance(stop.code, int) else 1
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0
    print("PEAK RESIDENT %.1f MB   wall %.1f s   exit %s"
          % (peak, time.time() - started, code))
    sys.stdout.flush()
    return code


if __name__ == "__main__":
    sys.exit(main())
