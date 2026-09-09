#!/usr/bin/env python3
"""guard83_term_pool.py -- the UNMODIFIED spelling-key guard over every
JSON artifact TASK 83 ITSELF writes, run as ONE process.

WHAT THIS WALKS, and why it is not the list task 83 set out to
write.  The canon40 transcription could not be completed under the
round's stated 6 GB memory cap -- the cap fires on the units whose
ledger rows name an attached runtime callee, and the records it
produces are not records of the compiler (log_189 section 3).  So
`name_census7.json`, `the_pool6.json`, `the_families6.json`,
`exception_families6.json`, `pool5_pool6_delta.json` and
`pool6_prediction_check.json` DO NOT EXIST and are not in the walk.
Nothing is claimed for them.  What this guard walks is every JSON
artifact task 83 actually wrote, plus the store it left and the
shards it rolled back, none skipped.

WHY THIS FILE AND NOT `guard83.py`.  `guard83.py` is on disk from the
part-run of 2026-09-03 and its walk list names `render_back82_tally
.json`, `render_back82_state.json` and `render_back82_store/` -- the
products of the render_back task, which is a DIFFERENT task and did not
write them.  Run as it stands it refuses its own output for a missing
artifact task 83 does not produce.  A superseded artifact is never
edited, so `guard83.py` stays on disk exactly as it is and the walk
task 83 actually owes is written here as a new file.

Nothing is added to any field set, no artifact is declared out of the
walk, no `role` key and no field whitelist is introduced, and the store
is walked shard by shard rather than sampled.

WHAT IS REUSED RATHER THAN COPIED.  `guard66.run_guard` is the runner
and is called, not re-typed; it invokes `check_no_spelling_keys.py`
unmodified as a separate process with its own interpreter.

WRITES:
  guard83_term_pool_transcript.txt
  guard83_term_pool.json

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

No operator token appears in this file.
"""

import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import guard66 as G66                                            # noqa: E402

TRANSCRIPT = os.path.join(HERE, "guard83_term_pool_transcript.txt")
SUMMARY = os.path.join(HERE, "guard83_term_pool.json")

WRITTEN = [
    "term66_state.json",
    "audit66.json",
    "audit66_before_the_relink_fix.json",
    "probe83_relink_readings.json",
    "probe83d_callee_population.json",
    "probe83e_callee_bodies.json",
    "probe83f_one_unit_trace.json",
    "probe83g_ceiling.json",
]

STORES = ["term66_store", "term66_store_bound_fired_records"]


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
        "guard83_term_pool.py -- every JSON artifact task 83 writes, "
        "unmodified guard, ONE process.  Nothing was added to any "
        "field set, no carve-out was declared, and no artifact was "
        "put out of the walk: the stores are walked shard by shard, "
        "not sampled.")
    print("TASK 83: %d paths  PASS %d  FAIL %d  exempt %d  exit %d"
          % (counts["paths"], counts["pass_lines"],
             counts["fail_lines"], counts["exempt_lines"],
             counts["exit_code"]))
    handle = open(SUMMARY, "w")
    json.dump({
        "meta": {
            "produced_by": "guard83_term_pool.py",
            "guard": "check_no_spelling_keys.py, unmodified, run as a "
                     "separate process; nothing added to any field "
                     "set, no carve-out declared",
            "walked": "%d top-level artifacts plus every shard of "
                      "term66_store and of "
                      "term66_store_bound_fired_records"
                      % len(WRITTEN),
            "why_not_guard83": "guard83.py's walk list names the "
                               "render_back task's products, which "
                               "task 83 does not write; it stays on "
                               "disk unedited as the superseded "
                               "record.",
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
