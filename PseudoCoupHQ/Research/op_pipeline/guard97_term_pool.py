#!/usr/bin/env python3
"""guard97_term_pool.py -- the UNMODIFIED `check_no_spelling_keys.py`
over every JSON artifact task 97 writes, ONE process.

WHY A NEW DRIVER RATHER THAN `guard83_term_pool.py`.  A superseded
artifact is never edited.  `guard83_term_pool.py`'s walk list names
`probe83d_callee_population.json`, `probe83f_one_unit_trace.json` and
`term66_store_bound_fired_records/` -- task 83's own products, which
task 97 does not write -- and does NOT name any of task 97's.  It stays
on disk exactly as it is, and the walk task 97 owes is this new file.

NOTHING IS PUT OUT OF THE WALK.  No field set is added to, no carve-out
is declared, and the store is walked shard by shard rather than
sampled.  `guard66.run_guard` starts
`check_no_spelling_keys.py` unmodified as ONE separate process over
every path at once.

WRITES:
  guard97_term_pool_transcript.txt
  guard97_term_pool.json

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

TRANSCRIPT = os.path.join(HERE, "guard97_term_pool_transcript.txt")
SUMMARY = os.path.join(HERE, "guard97_term_pool.json")

# every artifact task 97 writes and must be able to show.  A missing
# one is a refusal, never a silent skip.
REQUIRED = [
    "term66_state.json",
    "probe97a_unit_cost.json",
    "term97_finalize.json",
    "audit66.json",
    "name_census7.json",
]

# the pool's own products.  `pool66_run.py` REFUSES to build a pool
# whose member set is short of the canon40-proved population, and 44
# units of 30,324 are short (their layer-5 normalization does not
# converge -- log_202 section 4).  So these are written only if that
# refusal does not fire, and an absent one is NAMED here rather than
# passed over in silence.

# written when their step runs; named here so that a present one is
# walked and an absent one is reported rather than passed over.
IF_PRESENT = [
    "the_pool6.json",
    "the_pool6_bytes.json",
    "the_families6.json",
    "exception_families6.json",
    "pool5_pool6_delta.json",
    "pool6_prediction_check.json",
    "term97_control.json",
    "term97_pass2_a_slice0.json",
    "term97_pass2_a_slice1.json",
    "term97_pass2_a_slice2.json",
    "term97_pass2_a_slice3.json",
    "term97_pass2_b_slice0.json",
    "term97_flagged_slice0.json",
    "term97_flagged_slice1.json",
    "term97_flagged_slice2.json",
    "term97_flagged_slice3.json",
    "term97_flagged_slice4.json",
    "term97_flagged_slice5.json",
    "claims97b.json",
    "claims97c.json",
]

STORES = ["term66_store"]


def task97_paths():
    out = []
    absent = []
    for name in REQUIRED:
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            raise SystemExit(
                "REFUSED OWN OUTPUT: an artifact task 97 writes is "
                "missing from the walk: %s" % name)
        out.append(path)
    for name in IF_PRESENT:
        path = os.path.join(HERE, name)
        if not os.path.exists(path):
            absent.append(name)
            continue
        out.append(path)
    for store in STORES:
        pattern = os.path.join(HERE, store, "*.json")
        found = sorted(glob.glob(pattern))
        if not found:
            raise SystemExit(
                "REFUSED OWN OUTPUT: a store task 97 writes is empty: "
                "%s" % store)
        out.extend(found)
    return out, absent


def main(argv):
    paths, absent = task97_paths()
    counts = G66.run_guard(
        paths, TRANSCRIPT,
        "guard97_term_pool.py -- every JSON artifact task 97 writes, "
        "unmodified guard, ONE process.  Nothing was added to any "
        "field set, no carve-out was declared, and no artifact was "
        "put out of the walk: term66_store is walked shard by shard, "
        "not sampled.")
    print("TASK 97: %d paths  PASS %d  FAIL %d  exempt %d  exit %d"
          % (counts["paths"], counts["pass_lines"],
             counts["fail_lines"], counts["exempt_lines"],
             counts["exit_code"]))
    if absent:
        print("NOT ON DISK, named rather than skipped: %s"
              % ", ".join(absent))
    handle = open(SUMMARY, "w")
    json.dump({
        "meta": {
            "produced_by": "guard97_term_pool.py",
            "guard": "check_no_spelling_keys.py, unmodified, run as a "
                     "separate process; nothing added to any field "
                     "set, no carve-out declared",
            "walked": "%d top-level artifacts plus every shard of "
                      "term66_store" % (len(paths) - len(
                          glob.glob(os.path.join(HERE, "term66_store",
                                                 "*.json")))),
            "not_on_disk": absent,
            "why_not_guard83_term_pool": "its walk list names task "
                                         "83's own products and none "
                                         "of task 97's; a superseded "
                                         "artifact is never edited.",
        },
        "task97_artifacts": counts,
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
