#!/usr/bin/env python3
"""pool6_prediction_check.py -- TASK 79's prediction, CHECKED against
the pool task 83 actually built, with every difference attributed.

THE PREDICTION, quoted from `CORE_0_3_5_6_3_normalize.md`'s settled
rule and from `normalize79_pool_prediction_printed.txt`: pool5's
**1,831 entries become 1,813** -- 50 entries merge in 21 joins, 11
entries split, 30,432 members unchanged; of the 11 splits, 5 are false
merges the corrected rule repairs and 6 are proved-equal pairs the text
ground stops carrying.

WHAT THE PREDICTION HELD FIXED, and what this build did not.  Task 79
computed its prediction over POOL5's OWN MEMBERS with only the layer-5
texts replaced, and it took those texts from a transcription layer
PINNED to the blobs of 2026-09-03 23:02 -- before task 78's corrected
destination rule landed.  That isolates one change: the normalizer.
`the_pool6.json` carries three changes at once:

  1. THE MEMBER SET.  canon40 proves 30,324 wrapped texts where canon39
     proved 30,432.
  2. WHAT EACH TERM IS.  Task 78's destination rule changes the ledger,
     and the term is a transcription of the ledger.
  3. HOW A PROVED TERM PRINTS.  Task 79's normalizer.

So `the_pool6.json`'s entry count is NOT the predicted 1,813, and
saying it agreed or disagreed without separating those three would be a
number without a population.  This file does the separation:

  A. the CONTROL -- task 79's own prediction recomputed here, which
     must reproduce 1,813;
  B. the MEMBERS -- who left the pool and who entered, by name;
  C. the TEXTS -- for the members in both, how many print a different
     layer-5 text under canon40 than the pinned walk printed, and
     whether they are still layer-5 eligible at all;
  D. the PARTITIONS -- the predicted partition and pool6's own,
     restricted to the members they share, compared by member set, so
     every split and merge between them is counted;
  E. THE ANSWER -- whether the prediction held, stated either way.

WHAT IS REUSED RATHER THAN COPIED.
`normalize79_pool_prediction.members_of_pool5`, `.partition`,
`.as_sets` and `.compare` are called, not re-typed, so the control is
computed by the same code that made the prediction.

WRITES:
  pool6_prediction_check.json
  pool6_prediction_check_printed.txt

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

No operator token appears in this file, and no unit's display label is
read.

Coding discipline: no compound one-liner statements.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import normalize79_pool_prediction as NP                          # noqa: E402

LINES = []

PREDICTED_ENTRIES = 1813
PREDICTED_MERGING = 50
PREDICTED_JOINS = 21
PREDICTED_SPLITS = 11


def log(text):
    LINES.append(text)
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def pool6_groups():
    """unit -> entry, and the member sets, read off `the_pool6.json`."""
    document = json.load(open(os.path.join(HERE, "the_pool6.json")))
    sets = []
    entry_of = {}
    texts = {}
    eligible = set()
    for entry in document["entries"]:
        names = set()
        for member in entry["members"]:
            names.add(member["unit"])
            entry_of[member["unit"]] = entry["entry_id"]
            text = member.get("layer5_normalized_text")
            if text:
                texts[member["unit"]] = text
            if member.get("layer5_merge_eligible"):
                eligible.add(member["unit"])
        sets.append(frozenset(names))
    return document, sets, entry_of, texts, eligible


def restrict(sets, keep):
    """a partition restricted to a set of members: every group loses
    the members not in `keep`, and a group left empty disappears.
    Restriction is what makes two partitions over different member sets
    comparable at all, and it is stated rather than assumed."""
    out = []
    for names in sets:
        left = names & keep
        if left:
            out.append(frozenset(left))
    return out


def as_groups(sets):
    """the shape `normalize79_pool_prediction.compare` takes: a mapping
    from a root label to a member set."""
    out = {}
    index = 0
    for names in sets:
        out["G%06d" % index] = set(names)
        index = index + 1
    return out


def main():
    log("== A. THE CONTROL: task 79's prediction, recomputed by task "
        "79's own code")
    document5, members5, entry_of5, order5 = NP.members_of_pool5()
    old_texts = {}
    for name in members5:
        text = members5[name].get("layer5_normalized_text")
        if text:
            old_texts[name] = text
    control_groups, control_stats = NP.partition(members5, order5,
                                                 old_texts)
    walk = json.load(open(os.path.join(
        HERE, "normalize79_walk_pre78_walk1.json")))
    new_texts = {}
    for name in walk["texts"]:
        if name in members5:
            new_texts[name] = walk["texts"][name]
    predicted_groups, predicted_stats = NP.partition(members5, order5,
                                                     new_texts)
    splits, merges = NP.compare(control_groups, predicted_groups)
    entries_merging = 0
    for one in merges:
        entries_merging = entries_merging + one["joined_entries"]
    log("   pool5's own entry count                      %d"
        % len(document5["entries"]))
    log("   the control reproduces pool5's count          %d"
        % control_stats["groups"])
    log("   the predicted count                           %d"
        % predicted_stats["groups"])
    log("   predicted merges  %d entries in %d joins"
        % (entries_merging, len(merges)))
    log("   predicted splits  %d" % len(splits))
    log("   the CORE and log_186 record 1,813 / 50 in 21 / 11")
    control_ok = (predicted_stats["groups"] == PREDICTED_ENTRIES
                  and entries_merging == PREDICTED_MERGING
                  and len(merges) == PREDICTED_JOINS
                  and len(splits) == PREDICTED_SPLITS)
    log("   the recomputation reproduces the recorded prediction: %s"
        % control_ok)

    log("")
    log("== B. THE MEMBERS: who left the pool and who entered")
    document6, sets6, entry_of6, texts6, eligible6 = pool6_groups()
    members6 = set(entry_of6)
    was = set(members5)
    left = sorted(was - members6)
    entered = sorted(members6 - was)
    shared = was & members6
    log("   pool5 members                                 %d"
        % len(was))
    log("   pool6 members                                 %d"
        % len(members6))
    log("   members in both                               %d"
        % len(shared))
    log("   members that LEFT the pool                    %d"
        % len(left))
    log("       %s" % ", ".join(left[:6]))
    log("   members that ENTERED the pool                 %d"
        % len(entered))
    log("       %s" % ", ".join(entered[:6]))

    log("")
    log("== C. THE TEXTS, for the members in both")
    same = 0
    moved = 0
    lost_eligibility = 0
    gained_eligibility = 0
    both_none = 0
    moved_sightings = []
    for name in sorted(shared):
        predicted_text = new_texts.get(name)
        actual_text = texts6.get(name)
        if predicted_text is None and actual_text is None:
            both_none = both_none + 1
            continue
        if predicted_text is not None and actual_text is None:
            lost_eligibility = lost_eligibility + 1
            continue
        if predicted_text is None and actual_text is not None:
            gained_eligibility = gained_eligibility + 1
            continue
        if predicted_text == actual_text:
            same = same + 1
            continue
        moved = moved + 1
        if len(moved_sightings) < 6:
            moved_sightings.append(name)
    log("   the pinned corrected walk and canon40 print the SAME "
        "text  %d" % same)
    log("   they print a DIFFERENT text                            "
        "  %d" % moved)
    for name in moved_sightings:
        log("       %s" % name)
    log("   the pinned walk printed a text, canon40 has none        "
        " %d" % lost_eligibility)
    log("   the pinned walk printed none, canon40 has a text        "
        " %d" % gained_eligibility)
    log("   neither printed a text                                  "
        " %d" % both_none)

    log("")
    log("== D. THE PARTITIONS, restricted to the members they share")
    predicted_sets = NP.as_sets(predicted_groups)
    predicted_restricted = restrict(predicted_sets, shared)
    actual_restricted = restrict(sets6, shared)
    log("   groups the PREDICTED partition has over the shared "
        "members  %d" % len(predicted_restricted))
    log("   groups POOL6's partition has over the shared members     "
        " %d" % len(actual_restricted))
    d_splits, d_merges = NP.compare(as_groups(predicted_restricted),
                                    as_groups(actual_restricted))
    joined = 0
    for one in d_merges:
        joined = joined + one["joined_entries"]
    log("   predicted groups that SPLIT in pool6                    "
        " %d" % len(d_splits))
    log("   pool6 groups that JOIN predicted groups                 "
        " %d groups in %d joins" % (joined, len(d_merges)))
    identical = set(predicted_restricted) == set(actual_restricted)
    log("   the two partitions are IDENTICAL over the shared "
        "members  %s" % identical)

    log("")
    log("== E. THE ANSWER")
    log("   the_pool6.json entries                        %d"
        % len(document6["entries"]))
    log("   task 79's predicted entry count               %d"
        % PREDICTED_ENTRIES)
    log("   difference                                    %+d"
        % (len(document6["entries"]) - PREDICTED_ENTRIES))
    if identical and not left and not entered:
        answer = ("THE PREDICTION HELD EXACTLY.  pool6's partition is "
                  "the predicted partition, member set for member set.")
    elif identical:
        answer = ("THE PREDICTION HELD ON THE POPULATION IT WAS MADE "
                  "OVER.  Over the %d members pool5 and pool6 share, "
                  "the predicted partition and pool6's own are "
                  "identical; the entry counts differ because the "
                  "member sets differ (%d left, %d entered)."
                  % (len(shared), len(left), len(entered)))
    else:
        answer = ("THE PREDICTION DID NOT HOLD EXACTLY.  Over the %d "
                  "members pool5 and pool6 share, %d predicted groups "
                  "split and %d groups join, and %d units print a "
                  "different layer-5 text under canon40 than the "
                  "pinned walk printed.  The prediction isolated the "
                  "normalizer; pool6 also carries task 78's ledger and "
                  "a different member set, and section C measures how "
                  "much of the difference each carries."
                  % (len(shared), len(d_splits), joined, moved))
    log("   %s" % answer)

    out = {
        "meta": {
            "generated_by": "pool6_prediction_check.py",
            "node": "hq.research.compiler_graph.pool",
            "what_it_is": "task 79's pool prediction checked against "
                          "the pool task 83 built, with the three "
                          "changes separated: the member set, task "
                          "78's ledger, and task 79's normalizer",
            "prediction_source": "normalize79_pool_prediction_printed"
                                 ".txt and CORE_0_3_5_6_3_normalize.md",
            "role_note": "no `role` field is declared anywhere in this "
                         "document and no provenance carve-out is "
                         "claimed",
        },
        "control": {
            "pool5_entries": len(document5["entries"]),
            "control_groups": control_stats["groups"],
            "predicted_groups": predicted_stats["groups"],
            "predicted_entries_merging": entries_merging,
            "predicted_joins": len(merges),
            "predicted_splits": len(splits),
            "reproduces_the_recorded_prediction": control_ok,
        },
        "members": {
            "pool5": len(was),
            "pool6": len(members6),
            "shared": len(shared),
            "left": left,
            "entered": entered,
        },
        "texts_over_the_shared_members": {
            "same": same,
            "different": moved,
            "different_sightings": moved_sightings,
            "predicted_a_text_canon40_has_none": lost_eligibility,
            "predicted_none_canon40_has_a_text": gained_eligibility,
            "neither": both_none,
        },
        "partitions_over_the_shared_members": {
            "predicted_groups": len(predicted_restricted),
            "pool6_groups": len(actual_restricted),
            "predicted_groups_that_split": len(d_splits),
            "pool6_groups_that_join": len(d_merges),
            "predicted_groups_joined": joined,
            "identical": identical,
        },
        "answer": {
            "pool6_entries": len(document6["entries"]),
            "predicted_entries": PREDICTED_ENTRIES,
            "difference": len(document6["entries"]) - PREDICTED_ENTRIES,
            "statement": answer,
        },
    }
    handle = open(os.path.join(HERE, "pool6_prediction_check.json"),
                  "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.close()
    handle = open(os.path.join(
        HERE, "pool6_prediction_check_printed.txt"), "w")
    handle.write("\n".join(LINES) + "\n")
    handle.close()
    log("")
    log("-- wrote pool6_prediction_check.json and "
        "pool6_prediction_check_printed.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
