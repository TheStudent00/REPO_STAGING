#!/usr/bin/env python3
"""print_delta54.py -- EVERY split and EVERY merge between
`the_pool2.json` and `the_pool3.json`, printed in full with its
computed cause.

`compare_pool2_pool3.py` computes the causes and writes
`pool2_pool3_delta.json`.  This file only PRINTS that artifact, in
full, so the log can carry every row rather than a sample.  It
computes nothing and asserts nothing.

Nothing here reads an operator token.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns.  The candidate set
for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label on
the member.  HISTORY OF VIOLATIONS, so the pattern is visible: (1) the
arch campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
itself reintroduced it as "same-operator pairs").  MECHANICAL GUARD
REQUIRED: every pipeline stage that groups or pairs units must run the
spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
its own output on failure.  A brief handed to any subagent for this
line MUST paste this paragraph verbatim.

Coding discipline: no compound one-liner statements.

usage: print_delta54.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def main():
    doc = json.load(open(os.path.join(HERE, "pool2_pool3_delta.json")))
    splits = doc["splits"]
    merges = doc["merges"]

    log("EVERY SPLIT -- a pool2 entry whose shared members land in more")
    log("than one pool3 entry.  Population: the 30,436 units in both")
    log("pools.  Count: %d." % len(splits))
    log("")
    for row in splits:
        log("SPLIT %s -- %d shared members into %d pool3 entries %s"
            % (row["pool2_entry"], row["shared_member_count"],
               row["pool3_part_count"], ",".join(row["pool3_parts"])))
        log("   distinct layer-3 texts %d; distinct layer-5 texts among "
            "eligible %d; members with no eligible layer-5 text %d; "
            "withdrawn %d"
            % (row["distinct_layer3_texts"],
               row["distinct_layer5_texts_among_eligible"],
               row["members_not_layer5_eligible"],
               row["members_withdrawn_at_layer4"]))
        for cause in row["causes"]:
            log("   CAUSE: %s" % cause)
        log("   members (%d of %d listed): %s"
            % (row["members_listed"], row["shared_member_count"],
               " ".join(row["members"])))
        log("")

    log("")
    log("EVERY MERGE -- a pool3 entry whose shared members come from")
    log("more than one pool2 entry.  Population: the 30,436 units in")
    log("both pools.  Count: %d." % len(merges))
    log("")
    for row in merges:
        log("MERGE %s -- %d shared members from %d pool2 entries"
            % (row["pool3_entry"], row["shared_member_count"],
               row["pool2_origin_count"]))
        log("   pool2 origins: %s" % ",".join(row["pool2_origins"]))
        for cause in row["causes"]:
            log("   CAUSE: %s" % cause)
        log("")

    # the same 60 splits, one line each, for the report's own table
    lines = []
    for row in splits:
        short = []
        for cause in row["causes"]:
            if cause.startswith("the members carry more"):
                short.append("more than one layer-3 text")
            elif cause.startswith("the eligible members normalize"):
                short.append("more than one layer-5 text")
            elif "no eligible layer-5 text" in cause:
                short.append("%d member(s) with no eligible layer-5 "
                             "text" % row["members_not_layer5_eligible"])
            else:
                short.append(cause)
        lines.append("%s  %4d members  into %d pool3 entries [%s]  "
                     "l3 texts %d  l5 texts %d  CAUSE: %s"
                     % (row["pool2_entry"], row["shared_member_count"],
                        row["pool3_part_count"],
                        ",".join(row["pool3_parts"]),
                        row["distinct_layer3_texts"],
                        row["distinct_layer5_texts_among_eligible"],
                        "; ".join(short)))
    handle = open(os.path.join(HERE, "pool2_pool3_splits_oneline.txt"),
                  "w")
    handle.write("\n".join(lines) + "\n")
    handle.close()

    # the same 719 merges, one line each, for the report's own table
    lines = []
    for row in merges:
        causes = []
        for name in sorted(row["cause_counts"]):
            causes.append("%s x%d" % (name, row["cause_counts"][name]))
        if not causes:
            causes = ["TRANSITIVE ONLY -- no single crossing pair"]
        lines.append("%s  %4d members  from %2d pool2 entries [%s]  "
                     "CAUSE: %s"
                     % (row["pool3_entry"], row["shared_member_count"],
                        row["pool2_origin_count"],
                        ",".join(row["pool2_origins"]),
                        "; ".join(causes)))
    handle = open(os.path.join(HERE, "pool2_pool3_merges_oneline.txt"),
                  "w")
    handle.write("\n".join(lines) + "\n")
    handle.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
