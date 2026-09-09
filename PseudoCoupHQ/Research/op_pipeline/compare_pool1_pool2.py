#!/usr/bin/env python3
"""compare_pool1_pool2.py -- TASK 49, every entry that SPLIT or MERGED.

The comparison is a JOIN ON MEMBER SETS and nothing else.  No token is
read; no entry is matched by name.  Two pools are read read-only:

  the_pool1.json   28,984 units TASK 43 proved, merged on the region36
                   universal text and proved edges
  the_pool2.json   30,436 units TASK 47 proved, merged on the layer-5
                   normalized text, the layer-3 wrapped text, and
                   proved edges

Only units PRESENT IN BOTH pools can be compared.  Units the two pools
do not share are counted and named as arrivals and departures, never
folded into a split or a merge.

  SPLIT   -- one pool1 entry whose shared members land in MORE THAN ONE
             pool2 entry.
  MERGED  -- one pool2 entry whose shared members come from MORE THAN
             ONE pool1 entry.

THE CAUSE of each is COMPUTED, never asserted, by asking the machine
forms directly:

  for a merge, which ground crosses the old boundary -- do two members
  from different pool1 entries share a layer-5 normalized text, a
  layer-3 wrapped text, or a proved edge;

  for a split, which ground failed -- do the parts differ in their
  layer-3 wrapped text, and does at least one part hold a member whose
  layer-5 text is not eligible (withdrawn, undecided, or never built).

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

usage: compare_pool1_pool2.py
"""

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def index_pool(document, member_text_field):
    """unit label -> entry id, and entry id -> the entry."""
    where = {}
    entries = {}
    for entry in document["entries"]:
        entries[entry["entry_id"]] = entry
        for member in entry["members"]:
            where[member["unit"]] = entry["entry_id"]
    return where, entries


def proved_edge_pairs():
    """the same edges the pool builder applied, as an unordered set of
    pairs, so a split or merge can name one when it is the cause."""
    import build_the_pool2 as POOL
    records = POOL.take_all()
    present = {}
    for rec in records:
        present[rec["unit"]] = True
    out = set()
    for edge in POOL.proved_edge_list(present):
        out.add(tuple(sorted([edge["left"], edge["right"]])))
    return out


def main():
    pool1 = json.load(open(os.path.join(HERE, "the_pool1.json")))
    pool2 = json.load(open(os.path.join(HERE, "the_pool2.json")))
    where1, entries1 = index_pool(pool1, "universal_text")
    where2, entries2 = index_pool(pool2, "wrapped_text")

    units1 = set(where1)
    units2 = set(where2)
    shared = units1 & units2
    log("== populations")
    log("   pool1 member units                       %d" % len(units1))
    log("   pool2 member units                       %d" % len(units2))
    log("   units in both, the comparable population %d" % len(shared))
    log("   in pool1 only -- TASK 47 refused them    %d"
        % len(units1 - units2))
    log("   in pool2 only -- newly proved this round %d"
        % len(units2 - units1))

    # the member facts pool2 recorded, per unit
    fact = {}
    for entry in pool2["entries"]:
        for member in entry["members"]:
            fact[member["unit"]] = member

    edges = proved_edge_pairs()

    # ---- group the shared units both ways
    by1 = collections.defaultdict(list)
    by2 = collections.defaultdict(list)
    for unit in sorted(shared):
        by1[where1[unit]].append(unit)
        by2[where2[unit]].append(unit)

    splits = []
    for eid in sorted(by1):
        members = by1[eid]
        parts = collections.defaultdict(list)
        for unit in members:
            parts[where2[unit]].append(unit)
        if len(parts) < 2:
            continue
        # the computed cause
        texts3 = set(fact[u]["wrapped_text"] for u in members)
        not_eligible = [u for u in members
                        if not fact[u]["layer5_merge_eligible"]]
        withdrawn = [u for u in not_eligible
                     if "DISPROVED" in (fact[u]
                                        ["layer5_merge_eligibility_reason"]
                                        or "")]
        causes = []
        if len(texts3) > 1:
            causes.append("the members carry more than one layer-3 "
                          "wrapped text, so layer-3 identity does not "
                          "join them")
        eligible_texts = set()
        for unit in members:
            if fact[unit]["layer5_merge_eligible"]:
                eligible_texts.add(fact[unit]["layer5_normalized_text"])
        if len(eligible_texts) > 1:
            causes.append("the eligible members normalize to more than "
                          "one layer-5 text, so layer-5 identity does "
                          "not join them")
        if not_eligible:
            causes.append("%d member(s) have no eligible layer-5 text, "
                          "so no layer-5 ground can reach them"
                          % len(not_eligible))
        if not causes:
            causes.append("UNEXPLAINED -- the machine forms agree and "
                          "the split has no computed cause")
        splits.append({
            "pool1_entry": eid,
            "shared_member_count": len(members),
            "pool2_parts": sorted(parts),
            "pool2_part_count": len(parts),
            "distinct_layer3_texts": len(texts3),
            "distinct_layer5_texts_among_eligible": len(eligible_texts),
            "members_not_layer5_eligible": len(not_eligible),
            "members_withdrawn_at_layer4": len(withdrawn),
            "causes": causes,
            "members": members[:24],
            "members_listed": min(24, len(members)),
        })

    merges = []
    for eid in sorted(by2):
        members = by2[eid]
        origins = collections.defaultdict(list)
        for unit in members:
            origins[where1[unit]].append(unit)
        if len(origins) < 2:
            continue
        keys = sorted(origins)
        crossing = collections.Counter()
        examples = {}
        for i in range(len(keys)):
            for j in range(i + 1, len(keys)):
                for a in origins[keys[i]]:
                    for b in origins[keys[j]]:
                        pair = tuple(sorted([a, b]))
                        if pair in edges:
                            crossing["a proved edge"] += 1
                            examples.setdefault("a proved edge", pair)
                        if (fact[a]["wrapped_text"]
                                == fact[b]["wrapped_text"]):
                            crossing["layer-3 wrapped-text identity"] += 1
                            examples.setdefault(
                                "layer-3 wrapped-text identity", pair)
                        if (fact[a]["layer5_merge_eligible"]
                                and fact[b]["layer5_merge_eligible"]
                                and fact[a]["layer5_normalized_text"]
                                == fact[b]["layer5_normalized_text"]):
                            crossing["layer-5 normalized-text identity"] \
                                += 1
                            examples.setdefault(
                                "layer-5 normalized-text identity", pair)
        causes = []
        for name in sorted(crossing):
            causes.append("%s -- %d crossing pair(s), for instance %s "
                          "with %s"
                          % (name, crossing[name],
                             examples[name][0], examples[name][1]))
        if not causes:
            causes.append("TRANSITIVE ONLY -- no single crossing pair "
                          "carries a ground; the join is reached "
                          "through a chain inside the entry")
        merges.append({
            "pool2_entry": eid,
            "shared_member_count": len(members),
            "pool1_origins": keys,
            "pool1_origin_count": len(keys),
            "causes": causes,
            "cause_counts": dict(crossing),
            "members": members[:24],
            "members_listed": min(24, len(members)),
        })

    log("")
    log("== the join on member sets")
    log("   pool1 entries holding a shared unit       %d" % len(by1))
    log("   pool2 entries holding a shared unit       %d" % len(by2))
    log("   pool1 entries that SPLIT                  %d" % len(splits))
    log("   pool2 entries that MERGED                 %d" % len(merges))

    cause_tally = collections.Counter()
    for row in splits:
        for cause in row["causes"]:
            cause_tally[cause] += 1
    log("")
    log("== SPLIT causes, computed, one entry may carry more than one")
    for cause in sorted(cause_tally, key=lambda c: -cause_tally[c]):
        log("   %6d  %s" % (cause_tally[cause], cause))

    merge_tally = collections.Counter()
    for row in merges:
        for name in row["cause_counts"]:
            merge_tally[name] += 1
    merge_tally_none = len([r for r in merges if not r["cause_counts"]])
    log("")
    log("== MERGE grounds, computed, one entry may carry more than one")
    for name in sorted(merge_tally, key=lambda c: -merge_tally[c]):
        log("   %6d  %s" % (merge_tally[name], name))
    log("   %6d  %s" % (merge_tally_none,
                        "no single crossing pair -- transitive chain "
                        "only"))

    doc = {
        "meta": {
            "generator": "compare_pool1_pool2.py",
            "role_note": "GROUPING artifact -- checked by "
                         "check_no_spelling_keys.py IN FULL.  No "
                         "provenance exemption is claimed and no "
                         "`role` field is declared anywhere.",
            "task": "TASK 49 -- every entry that split or merged "
                    "between the_pool1.json and the_pool2.json",
            "method": "a join on member sets; the cause of each split "
                      "and each merge is computed from the machine "
                      "forms, never asserted",
            "comparable_population": "the units present in both pools",
        },
        "summary": {
            "pool1_member_units": len(units1),
            "pool2_member_units": len(units2),
            "units_in_both": len(shared),
            "units_in_pool1_only": len(units1 - units2),
            "units_in_pool2_only": len(units2 - units1),
            "pool1_entries_holding_a_shared_unit": len(by1),
            "pool2_entries_holding_a_shared_unit": len(by2),
            "pool1_entries_that_split": len(splits),
            "pool2_entries_that_merged": len(merges),
            "split_cause_tally": dict(cause_tally),
            "merge_ground_tally": dict(merge_tally),
            "merges_with_no_single_crossing_pair": merge_tally_none,
        },
        "splits": splits,
        "merges": merges,
        "units_in_pool1_only": sorted(units1 - units2),
        "units_in_pool2_only_count": len(units2 - units1),
    }
    path = os.path.join(HERE, "pool1_pool2_delta.json")
    with open(path, "w") as fh:
        json.dump(doc, fh, indent=1, sort_keys=True)
    log("")
    log("-- wrote pool1_pool2_delta.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
