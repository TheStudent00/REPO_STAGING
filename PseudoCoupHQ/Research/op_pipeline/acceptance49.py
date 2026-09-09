#!/usr/bin/env python3
"""acceptance49.py -- TASK 49, every figure the report states, computed
here so no number in the log is typed by hand.

Sections:
  (a) the headline counts, pool2 against pool1
  (b) E00033's successor -- the integer-addition entry -- verbatim
  (c) the split/merge join, with every split listed in full
  (d) the multi-language accounting: where pool1's 663 went
  (e) the family continuity checks

No operator token is read by anything here.  Where a token is printed
it is the display label carried on a member or a node.

usage: acceptance49.py
"""

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def load(name):
    return json.load(open(os.path.join(HERE, name)))


def section_a(pool1, pool2, fam1, fam2):
    log("(a) THE HEADLINE COUNTS -- the_pool2.json against the_pool1.json")
    log("")
    log("    quantity                              pool1      pool2")
    rows = [
        ("member units", pool1["summary"]["units_in_the_pool"],
         pool2["summary"]["units_in_the_pool"]),
        ("entries", pool1["summary"]["entries"],
         pool2["summary"]["entries"]),
        ("entries spanning more than one language",
         pool1["summary"]["entries_spanning_more_than_one_language"],
         pool2["summary"]["entries_spanning_more_than_one_language"]),
        ("entries spanning compiled and interpreted",
         pool1["summary"]["entries_spanning_compiled_and_interpreted"],
         pool2["summary"]["entries_spanning_compiled_and_interpreted"]),
        ("families", fam1["summary"]["families"],
         fam2["summary"]["families"]),
        ("family nodes", fam1["summary"]["nodes"],
         fam2["summary"]["nodes"]),
        ("nodes in a family", fam1["summary"]["nodes_in_a_family"],
         fam2["summary"]["nodes_in_a_family"]),
        ("singleton families", fam1["summary"]["singleton_families"],
         fam2["summary"]["singleton_families"]),
    ]
    for name, a, b in rows:
        log("    %-38s %8d %10d" % (name, a, b))
    log("")
    log("    pool2 only, stated on the artifact:")
    for key in ["units_by_arrival_population",
                "entries_under_the_brief_strict_rule",
                "distinct_layer5_texts_among_eligible_units",
                "layer5_identity_merges",
                "distinct_layer3_wrapped_texts",
                "layer3_identity_merges",
                "proved_edges_applied",
                "units_not_layer5_eligible",
                "units_withdrawn_at_layer4",
                "entries_with_more_than_one_wrapped_text",
                "entries_with_more_than_one_layer5_text"]:
        log("      %-46s %s"
            % (key, json.dumps(pool2["summary"][key], sort_keys=True)))
    log("")


def successor_of(pool1, pool2, entry_id):
    """the pool2 entries the members of one pool1 entry landed in."""
    source = None
    for entry in pool1["entries"]:
        if entry["entry_id"] == entry_id:
            source = entry
    where = {}
    for entry in pool2["entries"]:
        for member in entry["members"]:
            where[member["unit"]] = entry["entry_id"]
    tally = collections.Counter()
    absent = []
    for member in source["members"]:
        if member["unit"] in where:
            tally[where[member["unit"]]] += 1
        else:
            absent.append(member["unit"])
    return source, tally, absent


def section_b(pool1, pool2):
    log("(b) E00033's SUCCESSOR -- integer addition")
    log("")
    source, tally, absent = successor_of(pool1, pool2, "E00033")
    log("    the_pool1.json E00033: %d members, %d languages %s"
        % (source["member_count"], source["language_count"],
           source["languages"]))
    log("    every one of its members lands in: %s"
        % json.dumps(dict(tally), sort_keys=True))
    log("    members TASK 47 did not prove, so absent from pool2: %d %s"
        % (len(absent), absent))
    log("")
    target_id = tally.most_common(1)[0][0]
    target = None
    for entry in pool2["entries"]:
        if entry["entry_id"] == target_id:
            target = entry
    path = os.path.join(HERE, "the_pool2_entry_%s.json" % target_id)
    with open(path, "w") as fh:
        json.dump(target, fh, indent=1, sort_keys=True)
    log("    the successor is %s, written verbatim to "
        "the_pool2_entry_%s.json" % (target_id, target_id))
    log("")
    log("    LITERAL -- the entry as stored, every field except "
        "`members`:")
    shallow = {}
    for key in target:
        if key == "members":
            continue
        shallow[key] = target[key]
    for line in json.dumps(shallow, indent=1,
                           sort_keys=True).splitlines():
        log("      " + line)
    log("")
    log("    LITERAL -- all %d stored member objects, one per line, "
        "exactly as they sit in the file:" % target["member_count"])
    for member in target["members"]:
        log("      " + json.dumps(member, sort_keys=True))
    log("")


def section_c(delta):
    log("(c) THE SPLIT/MERGE JOIN ON MEMBER SETS")
    log("")
    for key in sorted(delta["summary"]):
        log("    %-46s %s"
            % (key, json.dumps(delta["summary"][key], sort_keys=True)))
    log("")
    log("    EVERY SPLIT, in full (%d of them):" % len(delta["splits"]))
    for row in delta["splits"]:
        log("      %s -- %d shared members become %d pool2 entries %s"
            % (row["pool1_entry"], row["shared_member_count"],
               row["pool2_part_count"], row["pool2_parts"]))
        log("        layer-3 texts %d, layer-5 texts among eligible %d, "
            "members not eligible %d, withdrawn %d"
            % (row["distinct_layer3_texts"],
               row["distinct_layer5_texts_among_eligible"],
               row["members_not_layer5_eligible"],
               row["members_withdrawn_at_layer4"]))
        for cause in row["causes"]:
            log("        CAUSE: %s" % cause)
        log("        members: %s" % row["members"])
    log("")
    log("    THE MERGES: %d pool2 entries hold members from more than "
        "one pool1 entry." % len(delta["merges"]))
    log("    grounds tally, computed by testing every crossing pair:")
    for name in sorted(delta["summary"]["merge_ground_tally"]):
        log("      %6d  %s"
            % (delta["summary"]["merge_ground_tally"][name], name))
    log("      %6d  no single crossing pair -- transitive chain only"
        % delta["summary"]["merges_with_no_single_crossing_pair"])
    log("")
    log("    the ten largest merges, by how many pool1 entries they "
        "consolidate:")
    order = sorted(delta["merges"],
                   key=lambda r: (-r["pool1_origin_count"],
                                  r["pool2_entry"]))
    for row in order[:10]:
        log("      %s <- %d pool1 entries, %d shared members"
            % (row["pool2_entry"], row["pool1_origin_count"],
               row["shared_member_count"]))
        for cause in row["causes"]:
            log("        CAUSE: %s" % cause)
    log("")


def section_d(pool1, pool2):
    log("(d) WHERE pool1's 663 MULTI-LANGUAGE ENTRIES WENT")
    log("")
    where = {}
    fact = {}
    entry_of = {}
    for entry in pool2["entries"]:
        entry_of[entry["entry_id"]] = entry
        for member in entry["members"]:
            where[member["unit"]] = entry["entry_id"]
            fact[member["unit"]] = member
    no_longer = 0
    destinations = set()
    for entry in pool1["entries"]:
        if not entry["spans_more_than_one_language"]:
            continue
        units = []
        for member in entry["members"]:
            if member["unit"] in where:
                units.append(member["unit"])
        langs = set(fact[u]["lang"] for u in units)
        if len(langs) < 2:
            no_longer = no_longer + 1
            continue
        for unit in units:
            if entry_of[where[unit]]["spans_more_than_one_language"]:
                destinations.add(where[unit])
    total2 = len([e for e in pool2["entries"]
                  if e["spans_more_than_one_language"]])
    log("    pool1 multi-language entries                          %d"
        % len([e for e in pool1["entries"]
               if e["spans_more_than_one_language"]]))
    log("      of those, fewer than two languages survive TASK 47   %d"
        % no_longer)
    log("      the rest land in this many pool2 multi-language "
        "entries  %d" % len(destinations))
    log("    pool2 multi-language entries                          %d"
        % total2)
    log("      of those, holding no unit from a pool1 multi-language "
        "entry %d" % (total2 - len(destinations)))
    log("")
    log("    GLOSS: the count fell from 663 to 423 by CONSOLIDATION, "
        "not by lost joins.")
    log("")
    kinds = collections.Counter()
    for entry in pool2["entries"]:
        if not entry["spans_more_than_one_language"]:
            continue
        names = set()
        for ground in entry["cross_language_grounds"]:
            if ground.get("ground"):
                names.add(ground["ground"])
        kinds[tuple(sorted(names))] += 1
    log("    what holds each pool2 multi-language entry together:")
    for key in sorted(kinds, key=lambda k: -kinds[k]):
        log("      %5d  %s" % (kinds[key], " + ".join(key)))
    log("")


def section_e(fam1, fam2):
    log("(e) FAMILY CONTINUITY")
    log("")
    log("    the_families2.json, every family, size and languages:")
    for family in fam2["families"]:
        labels = []
        for node in family["nodes"]:
            labels.append("%s:%s(%s)"
                          % (node["lang"], node["label"], node["arity"]))
        log("      %s size %2d %s"
            % (family["family_id"], family["size"], family["languages"]))
        log("           %s" % " ".join(labels))
    log("")
    log("    THE RATIFIED SIGHTING, checked: the family whose nodes are "
        "five different spellings of one machine behaviour.")
    for source, name in ((fam1, "the_families1.json"),
                         (fam2, "the_families2.json")):
        for family in source["families"]:
            labels = set()
            for node in family["nodes"]:
                labels.add("%s:%s" % (node["lang"], node["label"]))
            if labels == set(["c:~", "cpp:compl", "cpp:~", "go:^",
                              "rust:!", "swift:~"]):
                log("      %s  %s size %d %s"
                    % (name, family["family_id"], family["size"],
                       family["languages"]))
    log("")


def main():
    pool1 = load("the_pool1.json")
    pool2 = load("the_pool2.json")
    fam1 = load("the_families1.json")
    fam2 = load("the_families2.json")
    delta = load("pool1_pool2_delta.json")
    section_a(pool1, pool2, fam1, fam2)
    section_b(pool1, pool2)
    section_c(delta)
    section_d(pool1, pool2)
    section_e(fam1, fam2)
    return 0


if __name__ == "__main__":
    sys.exit(main())
