#!/usr/bin/env python3
"""normalize79_pool_prediction.py -- THE PREDICTION task 83 will check:
how many of pool5's 1,831 entries merge, and how many split, when the
CORRECTED layer-5 rule replaces the uncorrected one and nothing else
changes.

IT DOES NOT REBUILD THE POOL.  Task 83 rebuilds it.  This file computes
what the rebuild must find, from the pool that exists plus the walk of
the corrected rule, so that the two can be held against each other.

HOW THE PREDICTION IS COMPUTED, and why it is not a guess.  `pool.py`
forms entries by closing three grounds under transitivity
(`Pool.merge`): layer-5 text identity among units whose term PROVED,
layer-3 wrapped-text identity, and the proved edges of the cross-unit
prover.  Only the FIRST ground changes here.  So the prediction is the
same three grounds run twice over the SAME members:

  * the CONTROL partition, using the layer-5 texts `the_pool5.json`
    already carries.  It must reproduce pool5's own 1,831 entries
    member for member; if it does not, the prediction is not computed
    from a reproduction of the pool and the file says so.
  * the PREDICTED partition, using the texts `normalize79_walk.py`
    printed under the corrected rule.

The two partitions are then compared by MEMBER SETS, exactly as
`Pool.compare` does -- a renumbering is not a change.

WRITES:
  normalize79_pool_prediction.json
  normalize79_pool_prediction_printed.txt

ONE PROCESS.

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

No operator token appears in this file, and no unit's display label is
read.
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import pool as P                                                 # noqa: E402

LINES = []


def log(text):
    LINES.append(text)
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def members_of_pool5():
    """unit -> the member record pool5 holds, plus unit -> entry id."""
    document = json.load(open(os.path.join(HERE, "the_pool5.json")))
    members = {}
    entry_of = {}
    order = []
    for entry in document["entries"]:
        for member in entry["members"]:
            name = member["unit"]
            members[name] = member
            entry_of[name] = entry["entry_id"]
            order.append(name)
    return document, members, entry_of, order


def partition(members, order, texts_by_unit):
    """the three grounds closed under transitivity, over the same
    members, with the layer-5 texts handed in."""
    joiner = P.UnionFind()
    for name in order:
        joiner.add(name)
    layer5_first = {}
    layer5_merges = 0
    eligible = 0
    for name in order:
        member = members[name]
        if not member.get("layer5_merge_eligible"):
            continue
        text = texts_by_unit.get(name)
        if not text:
            continue
        eligible = eligible + 1
        if text in layer5_first:
            joiner.union(layer5_first[text], name)
            layer5_merges = layer5_merges + 1
        else:
            layer5_first[text] = name
    layer3_first = {}
    layer3_merges = 0
    for name in order:
        text = members[name].get("wrapped_text")
        if not text:
            continue
        if text in layer3_first:
            joiner.union(layer3_first[text], name)
            layer3_merges = layer3_merges + 1
        else:
            layer3_first[text] = name
    present = {}
    for name in order:
        present[name] = True
    edges = P.proved_edge_list(present)
    for edge in edges:
        joiner.union(edge["left"], edge["right"])
    groups = {}
    for name in order:
        root = joiner.find(name)
        groups.setdefault(root, set())
        groups[root].add(name)
    stats = {
        "units_eligible_for_the_layer5_ground": eligible,
        "distinct_layer5_texts_among_eligible_units": len(layer5_first),
        "layer5_identity_merges": layer5_merges,
        "distinct_layer3_wrapped_texts": len(layer3_first),
        "layer3_identity_merges": layer3_merges,
        "proved_edges_applied": len(edges),
        "groups": len(groups),
    }
    return groups, stats


def as_sets(groups):
    out = []
    for root in groups:
        out.append(frozenset(groups[root]))
    return out


def compare(before_groups, after_groups):
    """splits and merges joined on MEMBER SETS, the shape
    `Pool.compare` uses."""
    before_of = {}
    index = 0
    before_members = {}
    for names in as_sets(before_groups):
        label = "B%05d" % index
        before_members[label] = names
        for name in names:
            before_of[name] = label
        index = index + 1
    after_of = {}
    index = 0
    after_members = {}
    for names in as_sets(after_groups):
        label = "A%05d" % index
        after_members[label] = names
        for name in names:
            after_of[name] = label
        index = index + 1
    splits = []
    merges = []
    for label in sorted(before_members):
        landed = set()
        for name in before_members[label]:
            landed.add(after_of[name])
        if len(landed) > 1:
            splits.append({
                "was_entry_member_count": len(before_members[label]),
                "became_entries": len(landed),
                "members": sorted(before_members[label])[:20],
            })
    for label in sorted(after_members):
        came_from = set()
        for name in after_members[label]:
            came_from.add(before_of[name])
        if len(came_from) > 1:
            merges.append({
                "entry_member_count": len(after_members[label]),
                "joined_entries": len(came_from),
                "members": sorted(after_members[label])[:20],
            })
    return splits, merges


def main():
    document, members, entry_of, order = members_of_pool5()
    log("-- THE POOL AS IT STANDS")
    log("   entries %d, members %d"
        % (len(document["entries"]), len(members)))

    old_texts = {}
    for name in members:
        text = members[name].get("layer5_normalized_text")
        if text:
            old_texts[name] = text
    control_groups, control_stats = partition(members, order, old_texts)
    log("")
    log("-- THE CONTROL: the same three grounds over the same members, "
        "with pool5's own texts")
    log("   groups the control forms                    %d"
        % control_stats["groups"])
    log("   pool5's own entry count                     %d"
        % len(document["entries"]))
    pool5_sets = set()
    for entry in document["entries"]:
        names = set()
        for member in entry["members"]:
            names.add(member["unit"])
        pool5_sets.add(frozenset(names))
    control_sets = set(as_sets(control_groups))
    reproduces = control_sets == pool5_sets
    log("   the control reproduces pool5 member for member  %s"
        % reproduces)

    label = "walk1"
    suffix = ""
    if "--walk" in sys.argv:
        label = sys.argv[sys.argv.index("--walk") + 1]
    if "--suffix" in sys.argv:
        suffix = sys.argv[sys.argv.index("--suffix") + 1]
    walk = json.load(open(os.path.join(
        HERE, "normalize79_walk_%s.json" % label)))
    new_texts = {}
    for name in walk["texts"]:
        if name in members:
            new_texts[name] = walk["texts"][name]
    log("")
    log("-- THE CORRECTED TEXTS")
    log("   units of the pool the corrected walk printed %d"
        % len(new_texts))

    predicted_groups, predicted_stats = partition(members, order,
                                                  new_texts)
    log("   groups the corrected rule forms              %d"
        % predicted_stats["groups"])
    log("   distinct layer-5 texts, pool5's own          %d"
        % control_stats["distinct_layer5_texts_among_eligible_units"])
    log("   distinct layer-5 texts, corrected            %d"
        % predicted_stats["distinct_layer5_texts_among_eligible_units"])

    splits, merges = compare(control_groups, predicted_groups)
    entries_merging = 0
    for one in merges:
        entries_merging = entries_merging + one["joined_entries"]
    log("")
    log("-- THE PREDICTION task 83 will check")
    log("   entries before                               %d"
        % control_stats["groups"])
    log("   entries after                                %d"
        % predicted_stats["groups"])
    log("   entries that MERGE (two or more become one)  %d entries "
        "in %d joins" % (entries_merging, len(merges)))
    log("   entries that SPLIT (one becomes two or more) %d"
        % len(splits))
    log("   members                                      %d before, "
        "%d after" % (len(members), len(members)))

    if merges:
        log("")
        log("   the largest join, printed")
        biggest = sorted(merges,
                         key=lambda one: -one["joined_entries"])[0]
        log("     %d earlier entries become one, %d members"
            % (biggest["joined_entries"], biggest["entry_member_count"]))
        for name in biggest["members"][:8]:
            log("       %s" % name)
    if splits:
        log("")
        log("   the splits, printed")
        for one in splits[:10]:
            log("     an entry of %d members becomes %d"
                % (one["was_entry_member_count"],
                   one["became_entries"]))
            for name in one["members"][:6]:
                log("       %s" % name)

    out = {
        "meta": {
            "generated_by": "normalize79_pool_prediction.py",
            "node": "hq.research.compiler_graph.term.normalize",
            "what_it_is": "how many of pool5's entries merge or split "
                          "under the corrected layer-5 rule, computed "
                          "from pool5's own members and the corrected "
                          "walk; the pool is NOT rebuilt here",
            "checked_by": "task 83's pool rebuild",
            "walk_read": label,
            "control_reproduces_pool5": reproduces,
        },
        "entries_before": control_stats["groups"],
        "entries_after": predicted_stats["groups"],
        "entries_that_merge": entries_merging,
        "joins": len(merges),
        "entries_that_split": len(splits),
        "control_statistics": control_stats,
        "predicted_statistics": predicted_stats,
        "merges": merges[:200],
        "splits": splits[:200],
    }
    handle = open(os.path.join(
        HERE, "normalize79_pool_prediction%s.json" % suffix), "w")
    json.dump(out, handle, indent=1, sort_keys=True)
    handle.close()
    handle = open(os.path.join(
        HERE,
        "normalize79_pool_prediction%s_printed.txt" % suffix), "w")
    handle.write("\n".join(LINES) + "\n")
    handle.close()
    log("")
    log("-- wrote normalize79_pool_prediction.json and "
        "normalize79_pool_prediction_printed.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
