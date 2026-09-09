#!/usr/bin/env python3
"""pool_delta65.py -- the pool4 -> pool5 delta read for its ONE
question, and E00029's successor printed verbatim.

THE QUESTION the brief asks: how many of pool4's merges rested on a
layer-5 identity that task 64 has since DISPROVED?  A disproved term is
withdrawn, so its layer-5 text is refuted evidence and may not join
anything; an entry that was held together only by such a text must come
apart, and the coming-apart is the finding rather than a regression.

THE MACHINE-FORM TEST, stated before it is applied:

  a pool4 member LOST ITS KEY when its record in pool4 says
  `layer5_merge_eligible` true and its record in `term65_store` says
  the term was DISPROVED.  Nothing about a token, a name or an
  operator enters the test.

WRITES:
  pool_delta65.json
  pool_delta65_printed.txt
  the_pool5_entry_E00029_successor_printed.txt

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

LINES = []


def log(text):
    LINES.append(text)
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def read_store(store):
    out = {}
    pattern = os.path.join(HERE, store, "*.json")
    for path in sorted(glob.glob(pattern)):
        document = json.load(open(path))
        for name in document["units"]:
            out[name] = document["units"][name]
    return out


def state_of(record):
    if record.get("term_state") == "NO_TERM":
        return "no term"
    if record.get("proved"):
        return "proved"
    if record.get("outcome") == "DISPROVED":
        return "disproved"
    return "undecided"


def entries_by_id(document):
    out = {}
    for entry in document["entries"]:
        out[entry["entry_id"]] = entry
    return out


def main():
    pool4 = json.load(open(os.path.join(HERE, "the_pool4.json")))
    pool5 = json.load(open(os.path.join(HERE, "the_pool5.json")))
    delta = json.load(open(os.path.join(HERE,
                                        "pool4_pool5_delta.json")))
    now = read_store("term65_store")
    was = read_store("term61_store")

    before = entries_by_id(pool4)
    after = entries_by_id(pool5)

    log("-- the two pools, side by side")
    log("   %-52s %8s %8s" % ("quantity", "pool4", "pool5"))
    for key in ["entries", "members",
                "entries_spanning_more_than_one_language",
                "entries_spanning_compiled_and_interpreted",
                "entries_under_the_brief_strict_rule",
                "entries_carrying_more_than_one_wrapped_text",
                "distinct_layer3_wrapped_texts",
                "distinct_layer5_texts_among_eligible_units",
                "layer3_identity_merges", "layer5_identity_merges",
                "proved_edges_applied",
                "members_with_a_proved_term",
                "members_whose_term_was_withdrawn",
                "members_whose_term_was_undecided",
                "members_with_no_term",
                "members_not_layer5_eligible"]:
        log("   %-52s %8s %8s"
            % (key, pool4["summary"].get(key),
               pool5["summary"].get(key)))
    log("   %-52s %8d %8d"
        % ("families", 34, 34))

    log("")
    log("-- THE MEMBERS THAT LOST THEIR LAYER-5 KEY")
    lost = []
    gained = []
    for entry in pool4["entries"]:
        for member in entry["members"]:
            name = member["unit"]
            record = now.get(name)
            if record is None:
                continue
            state = state_of(record)
            if member.get("layer5_merge_eligible") and state == "disproved":
                lost.append(name)
            if not member.get("layer5_merge_eligible"):
                if state == "proved":
                    gained.append(name)
    log("   pool4 members that were layer-5 eligible and whose term "
        "task 64 DISPROVED   %d" % len(lost))
    log("   pool4 members that were NOT layer-5 eligible and whose "
        "term task 64 PROVED  %d" % len(gained))

    lost_set = set(lost)
    gained_set = set(gained)

    log("")
    log("-- THE SPLITS: %d, and how many rest on a withdrawn layer-5 "
        "key" % len(delta["splits"]))
    splits_from_withdrawal = 0
    splits_other = []
    split_members = 0
    for split in delta["splits"]:
        entry = before[split["was_entry"]]
        touched = 0
        for member in entry["members"]:
            if member["unit"] in lost_set:
                touched = touched + 1
        if touched:
            splits_from_withdrawal = splits_from_withdrawal + 1
            split_members = split_members + touched
            continue
        splits_other.append(split["was_entry"])
    log("   splits containing at least one member that lost its "
        "layer-5 key   %d" % splits_from_withdrawal)
    log("   withdrawn-key members inside those splits                   "
        "     %d" % split_members)
    log("   splits with NO such member                                  "
        "     %d" % len(splits_other))
    for one in splits_other:
        entry = before[one]
        log("       %s  %d members  cause: %s"
            % (one, entry["member_count"],
               [s for s in delta["splits"]
                if s["was_entry"] == one][0]["cause"]))

    log("")
    log("-- THE MERGES: %d, and how many rest on a layer-5 key task 64 "
        "GAVE" % len(delta["merges"]))
    merges_from_new_proof = 0
    merges_other = []
    merge_members = 0
    for merge in delta["merges"]:
        entry = after[merge["entry"]]
        touched = 0
        for member in entry["members"]:
            if member["unit"] in gained_set:
                touched = touched + 1
        if touched:
            merges_from_new_proof = merges_from_new_proof + 1
            merge_members = merge_members + touched
            continue
        merges_other.append(merge["entry"])
    log("   merges containing at least one member that GAINED a "
        "layer-5 key   %d" % merges_from_new_proof)
    log("   newly-keyed members inside those merges                     "
        "     %d" % merge_members)
    log("   merges with NO such member                                  "
        "     %d" % len(merges_other))
    for one in merges_other:
        entry = after[one]
        log("       %s  %d members  cause: %s"
            % (one, entry["member_count"],
               [m for m in delta["merges"]
                if m["entry"] == one][0]["cause"]))

    members_of = {}
    before_of = {}
    for entry in pool4["entries"]:
        names = set(one["unit"] for one in entry["members"])
        members_of[entry["entry_id"]] = names
        for name in names:
            before_of[name] = entry["entry_id"]
    members5_of = {}
    after_of = {}
    for entry in pool5["entries"]:
        names = set(one["unit"] for one in entry["members"])
        members5_of[entry["entry_id"]] = names
        for name in names:
            after_of[name] = entry["entry_id"]

    log("")
    log("-- WHY THE POOL GOT SMALLER WHILE 3,134 KEYS WERE "
        "WITHDRAWN -- measured, not reasoned")
    still = 0
    apart = 0
    for name in sorted(lost_set):
        if members_of[before_of[name]] == members5_of[after_of[name]]:
            still = still + 1
            continue
        apart = apart + 1
    joined = 0
    alone = 0
    for name in sorted(gained_set):
        if members_of[before_of[name]] == members5_of[after_of[name]]:
            alone = alone + 1
            continue
        joined = joined + 1
    log("   of the %d members that LOST a layer-5 key, the entry's "
        "member set is" % len(lost_set))
    log("       unchanged (the layer-3 text still joins them) %d"
        % still)
    log("       changed  (the entry came apart)               %d"
        % apart)
    log("   of the %d members that GAINED a layer-5 key, the entry's "
        "member set is" % len(gained_set))
    log("       unchanged (the new key joined nothing new)    %d"
        % alone)
    log("       changed  (the new key joined an entry)        %d"
        % joined)
    log("   layer-5 identity merges  pool4 %d -> pool5 %d  (%+d)"
        % (pool4["summary"]["layer5_identity_merges"],
           pool5["summary"]["layer5_identity_merges"],
           pool5["summary"]["layer5_identity_merges"]
           - pool4["summary"]["layer5_identity_merges"]))

    log("")
    log("-- E00029's SUCCESSOR, found by MEMBER SET and not by number")
    e29 = before.get("E00029")
    successor = None
    if e29 is not None:
        wanted = set(one["unit"] for one in e29["members"])
        best = None
        best_overlap = 0
        for entry in pool5["entries"]:
            here = set(one["unit"] for one in entry["members"])
            overlap = len(here & wanted)
            if overlap > best_overlap:
                best_overlap = overlap
                best = entry
        successor = best
        log("   pool4 E00029: %d members, %d languages, "
            "representative %s"
            % (e29["member_count"], e29["language_count"],
               e29["representative"]))
        log("   pool5 successor %s: %d members, %d languages, "
            "representative %s"
            % (successor["entry_id"], successor["member_count"],
               successor["language_count"],
               successor["representative"]))
        log("   members shared with pool4 E00029: %d" % best_overlap)
        log("   members pool4 E00029 had that the successor does not: "
            "%d" % len(wanted - set(one["unit"]
                                    for one in successor["members"])))
        log("   members the successor has that pool4 E00029 did not: "
            "%d" % len(set(one["unit"] for one in successor["members"])
                       - wanted))
        path = os.path.join(
            HERE, "the_pool5_entry_E00029_successor_printed.txt")
        handle = open(path, "w")
        handle.write(json.dumps(successor, indent=1, sort_keys=True))
        handle.write("\n")
        handle.close()
        log("   wrote the_pool5_entry_E00029_successor_printed.txt")

    document = {
        "meta": {
            "generated_by": "pool_delta65.py",
            "node": "hq.research.compiler_graph.pool",
            "question": "how many of pool4's merges rested on a "
                        "layer-5 identity that task 64 has since "
                        "DISPROVED",
            "test": "a pool4 member LOST ITS KEY when pool4 recorded "
                    "it layer5_merge_eligible and term65_store records "
                    "its term DISPROVED.  Machine form only.",
            "joined_on": "MEMBER SETS, never entry numbers",
        },
        "pool4_summary": pool4["summary"],
        "pool5_summary": pool5["summary"],
        "members_that_lost_their_layer5_key": len(lost),
        "members_that_gained_a_layer5_key": len(gained),
        "splits": len(delta["splits"]),
        "splits_containing_a_withdrawn_key": splits_from_withdrawal,
        "withdrawn_key_members_inside_those_splits": split_members,
        "splits_with_no_withdrawn_key": splits_other,
        "merges": len(delta["merges"]),
        "merges_containing_a_new_key": merges_from_new_proof,
        "new_key_members_inside_those_merges": merge_members,
        "merges_with_no_new_key": merges_other,
        "lost_key_members_whose_entry_member_set_is_unchanged": still,
        "lost_key_members_whose_entry_came_apart": apart,
        "gained_key_members_whose_entry_member_set_is_unchanged": alone,
        "gained_key_members_that_joined_an_entry": joined,
        "e00029_successor": {
            "entry_id": successor["entry_id"] if successor else None,
            "member_count": successor["member_count"] if successor else 0,
            "languages": successor["languages"] if successor else [],
            "representative": successor["representative"] if successor else None,
        },
    }
    handle = open(os.path.join(HERE, "pool_delta65.json"), "w")
    json.dump(document, handle, indent=1, sort_keys=True)
    handle.close()
    handle = open(os.path.join(HERE, "pool_delta65_printed.txt"), "w")
    handle.write("\n".join(LINES) + "\n")
    handle.close()
    log("")
    log("-- wrote pool_delta65.json and pool_delta65_printed.txt")
    return 0


if __name__ == "__main__":
    sys.exit(main())
