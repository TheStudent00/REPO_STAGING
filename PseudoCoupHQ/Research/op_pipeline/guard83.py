#!/usr/bin/env python3
"""guard83.py -- the UNMODIFIED spelling-key guard over EVERY JSON
artifact task 83 writes, run as ONE process.

Nothing is added to any field set, no artifact is declared out of the
walk, and no exemption is declared anywhere.  The three stores are
walked shard by shard, not sampled.

WHAT IS REUSED RATHER THAN COPIED.  `guard66.run_guard` is the runner
and is called, not re-typed; it is the same function task 80's own
guard used.

WRITES:
  guard83_transcript.txt
  guard83.json

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

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import guard66 as G66                                            # noqa: E402

TRANSCRIPT = os.path.join(HERE, "guard83_transcript.txt")
SUMMARY = os.path.join(HERE, "guard83.json")

WRITTEN = [
    "audit66.json",
    "audit66_before_the_relink_fix.json",
    "probe83_relink_readings.json",
    "name_census7.json",
    "the_pool6.json",
    "the_pool6_bytes.json",
    "the_families6.json",
    "exception_families6.json",
    "pool5_pool6_delta.json",
    "pool6_prediction_check.json",
    "render_back81_tally.json",
    "render_back82_tally.json",
    "term66_state.json",
    "render_back81_state.json",
    "render_back82_state.json",
]

STORES = [
    "term66_store",
    "render_back81_store",
    "render_back82_store",
]


def task83_paths():
    out = []
    for name in WRITTEN:
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            raise SystemExit(
                "REFUSED OWN OUTPUT: an artifact task 83 writes is "
                "missing from the walk: %s" % name)
        out.append(path)
    for store in STORES:
        pattern = os.path.join(HERE, store, "*.json")
        found = sorted(glob.glob(pattern))
        if not found:
            raise SystemExit(
                "REFUSED OWN OUTPUT: a store task 83 writes is empty: "
                "%s" % store)
        out.extend(found)
    return out


def main(argv):
    paths = task83_paths()
    counts = G66.run_guard(
        paths, TRANSCRIPT,
        "guard83.py -- every JSON artifact task 83 writes, unmodified "
        "guard, ONE process.  Nothing was added to any field set, and "
        "no artifact was declared out of the walk: the three stores "
        "are walked shard by shard, not sampled.")
    print("TASK 83: %d paths  PASS %d  FAIL %d  exempt %d  exit %d"
          % (counts["paths"], counts["pass_lines"],
             counts["fail_lines"], counts["exempt_lines"],
             counts["exit_code"]))
    handle = open(SUMMARY, "w")
    json.dump({
        "meta": {
            "produced_by": "guard83.py",
            "guard": "check_no_spelling_keys.py, unmodified, run as a "
                     "separate process; nothing added to any field "
                     "set, no exemption declared",
            "walked": "%d top-level artifacts plus every shard of "
                      "term66_store, render_back81_store and "
                      "render_back82_store"
                      % len(WRITTEN),
        },
        "task83_artifacts": counts,
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
