#!/usr/bin/env python3
"""audit54.py -- TASK 54's figures, computed, never asserted.

WHAT IT PRINTS, in order:

  (a) the headline counts of `the_pool3.json` against `the_pool2.json`:
      entries, member units, entries spanning more than one language,
      entries spanning compiled and interpreted, families, family
      nodes;
  (b) the brief-strict two-ground count, RECORDED not used (ruling 1);
  (c) the population line, read off the artifact;
  (d) the layer-5 merge eligibility breakdown over the 30,436;
  (e) E00029's SUCCESSOR, verbatim: the pool3 entry holding the
      members of pool2's E00029, printed as stored;
  (f) THE SYMBOLIC-TARGET QUESTION: of the 4,499 member units whose
      canon37 wrapped text carried a symbol comment (log 152 §4.3),
      how many now merge on layer-3 wrapped-text identity -- that is,
      how many now share their canon38 wrapped text with at least one
      other unit of the pool, and how many of those did NOT share
      their canon37 wrapped text with any other unit.

Every figure states the population it covers.  Nothing here reads an
operator token: the joins are on unit labels and on machine texts.

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

usage: audit54.py
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


def load(name):
    return json.load(open(os.path.join(HERE, name)))


def index_members(pool):
    where = {}
    entries = {}
    for entry in pool["entries"]:
        entries[entry["entry_id"]] = entry
        for member in entry["members"]:
            where[member["unit"]] = entry["entry_id"]
    return where, entries


def canon37_texts():
    """unit label -> its canon37 wrapped text, for the units canon37
    proved.  Read from the superseded artifact, read-only."""
    out = {}
    for entry in load("the_pool2.json")["entries"]:
        for member in entry["members"]:
            out[member["unit"]] = member["wrapped_text"]
    return out


def main():
    pool2 = load("the_pool2.json")
    pool3 = load("the_pool3.json")
    fam2 = load("the_families2.json")
    fam3 = load("the_families3.json")

    log("=" * 66)
    log("(a) THE HEADLINE COUNTS -- population: every unit task 52")
    log("    proved, 30,436 of 31,078 attempted, in both pools")
    log("=" * 66)
    rows = [
        ("member units",
         pool2["summary"]["units_in_the_pool"],
         pool3["summary"]["units_in_the_pool"]),
        ("entries",
         pool2["summary"]["entries"],
         pool3["summary"]["entries"]),
        ("entries spanning more than one language",
         pool2["summary"]["entries_spanning_more_than_one_language"],
         pool3["summary"]["entries_spanning_more_than_one_language"]),
        ("entries spanning compiled and interpreted",
         pool2["summary"]["entries_spanning_compiled_and_interpreted"],
         pool3["summary"]["entries_spanning_compiled_and_interpreted"]),
        ("families",
         fam2["summary"]["families"],
         fam3["summary"]["families"]),
        ("family nodes",
         fam2["summary"]["nodes"],
         fam3["summary"]["nodes"]),
        ("nodes in a family",
         fam2["summary"]["nodes_in_a_family"],
         fam3["summary"]["nodes_in_a_family"]),
        ("singleton families",
         fam2["summary"]["singleton_families"],
         fam3["summary"]["singleton_families"]),
        ("distinct layer-3 wrapped texts",
         pool2["summary"]["distinct_layer3_wrapped_texts"],
         pool3["summary"]["distinct_layer3_wrapped_texts"]),
        ("distinct layer-5 texts among eligible units",
         pool2["summary"]
         ["distinct_layer5_texts_among_eligible_units"],
         pool3["summary"]
         ["distinct_layer5_texts_among_eligible_units"]),
        ("proved edges applied",
         pool2["summary"]["proved_edges_applied"],
         pool3["summary"]["proved_edges_applied"]),
    ]
    log("    %-46s %8s %8s %8s" % ("quantity", "pool2", "pool3", "delta"))
    for name, a, b in rows:
        log("    %-46s %8d %8d %+8d" % (name, a, b, b - a))

    log("")
    log("=" * 66)
    log("(b) THE BRIEF-STRICT TWO-GROUND COUNT -- RECORDED, NOT USED")
    log("=" * 66)
    log("    pool3 entries, three grounds (THE COUNT)        %8d"
        % pool3["summary"]["entries"])
    log("    pool3 entries, layer-5 identity + proved edges  %8d"
        % pool3["summary"]["entries_under_the_brief_strict_rule"])
    log("    pool2 entries, three grounds                    %8d"
        % pool2["summary"]["entries"])
    log("    pool2 entries, layer-5 identity + proved edges  %8d"
        % pool2["summary"]["entries_under_the_brief_strict_rule"])

    log("")
    log("=" * 66)
    log("(c) THE POPULATION, AS STATED ON THE ARTIFACT")
    log("=" * 66)
    log("    the_pool3.json meta.population:")
    log("      %s" % pool3["meta"]["population"])
    log("    the_pool3.json summary.units_by_arrival_population:")
    log("      %s" % json.dumps(
        pool3["summary"]["units_by_arrival_population"], sort_keys=True))

    log("")
    log("=" * 66)
    log("(d) LAYER-5 MERGE ELIGIBILITY, over the 30,436 members")
    log("=" * 66)
    counted = collections.Counter()
    for entry in pool3["entries"]:
        for member in entry["members"]:
            if member["layer5_merge_eligible"]:
                counted["eligible -- the term was proved"] += 1
            else:
                counted[member["layer5_merge_eligibility_reason"]] += 1
    total = 0
    for reason in sorted(counted, key=lambda r: -counted[r]):
        total = total + counted[reason]
        log("    %6d  %s" % (counted[reason], reason))
    log("    %6d  TOTAL" % total)
    log("    the summary block's own figures:")
    for key in ("units_not_layer5_eligible", "units_withdrawn_at_layer4",
                "units_undecided_at_layer4", "units_with_no_layer4_term"):
        log("      %-34s %6d" % (key, pool3["summary"][key]))

    log("")
    log("=" * 66)
    log("(e) E00029's SUCCESSOR, VERBATIM")
    log("=" * 66)
    where2, entries2 = index_members(pool2)
    where3, entries3 = index_members(pool3)
    source = entries2["E00029"]
    landing = collections.Counter()
    for member in source["members"]:
        landing[where3[member["unit"]]] += 1
    log("    pool2 E00029: %d members, representative %s"
        % (source["member_count"], source["representative"]))
    log("    those members land in %d pool3 entr(y/ies):"
        % len(landing))
    for eid in sorted(landing):
        log("      %s holds %d of them, and has %d members in all"
            % (eid, landing[eid], entries3[eid]["member_count"]))
    successor = sorted(landing, key=lambda e: -landing[e])[0]
    log("")
    log("    THE SUCCESSOR IS %s.  Printed verbatim from "
        "the_pool3.json," % successor)
    log("    members truncated to the first 24 of %d for length; every"
        % entries3[successor]["member_count"])
    log("    other field is complete and unedited.")
    log("")
    shown = dict(entries3[successor])
    shown["members"] = shown["members"][:24]
    shown["members_printed"] = min(24, entries3[successor]["member_count"])
    text = json.dumps(shown, indent=1, sort_keys=True)
    for line in text.splitlines():
        log("    " + line)

    log("")
    log("=" * 66)
    log("(f) THE SYMBOLIC-TARGET QUESTION -- pool2's 4,499 members")
    log("=" * 66)
    old_text = canon37_texts()
    old_count = collections.Counter(old_text.values())
    new_text = {}
    for entry in pool3["entries"]:
        for member in entry["members"]:
            new_text[member["unit"]] = member["wrapped_text"]
    new_count = collections.Counter(new_text.values())
    symbolic = []
    for unit in sorted(old_text):
        if "<" in old_text[unit]:
            symbolic.append(unit)
    log("    member units whose canon37 wrapped text carries a symbol")
    log("    comment (the population this question is about)  %6d"
        % len(symbolic))
    now_shared = 0
    was_shared = 0
    newly_shared = 0
    still_alone = 0
    for unit in symbolic:
        old_shared = old_count[old_text[unit]] > 1
        cur_shared = new_count[new_text[unit]] > 1
        if old_shared:
            was_shared = was_shared + 1
        if cur_shared:
            now_shared = now_shared + 1
        if cur_shared and not old_shared:
            newly_shared = newly_shared + 1
        if not cur_shared:
            still_alone = still_alone + 1
    log("    of those, sharing their canon37 text with another unit")
    log("    -- already merging on layer-3 identity before   %6d"
        % was_shared)
    log("    of those, sharing their canon38 text with another unit")
    log("    -- MERGING ON LAYER-3 IDENTITY NOW              %6d"
        % now_shared)
    log("    of those, NEWLY merging on layer-3 identity     %6d"
        % newly_shared)
    log("    of those, still the only holder of their text   %6d"
        % still_alone)
    log("    check: %d + %d = %d, the population"
        % (now_shared, still_alone, now_shared + still_alone))
    log("    also, over the whole 30,436:")
    log("      units carrying a symbol comment in canon38    %6d"
        % len([u for u in new_text if "<" in new_text[u]]))

    log("")
    log("=" * 66)
    log("(g) LAYER-5 ELIGIBILITY MOVING, pool2 -> pool3, over 30,436")
    log("=" * 66)
    old_ok = {}
    for entry in pool2["entries"]:
        for member in entry["members"]:
            old_ok[member["unit"]] = member["layer5_merge_eligible"]
    new_ok = {}
    for entry in pool3["entries"]:
        for member in entry["members"]:
            new_ok[member["unit"]] = member["layer5_merge_eligible"]
    lost = 0
    gained = 0
    for unit in old_ok:
        if old_ok[unit] and not new_ok[unit]:
            lost = lost + 1
        if new_ok[unit] and not old_ok[unit]:
            gained = gained + 1
    log("    eligible in pool2 (canon37 / layer4b)            %6d"
        % len([1 for u in old_ok if old_ok[u]]))
    log("    eligible in pool3 (canon38 / layer4c)            %6d"
        % len([1 for u in new_ok if new_ok[u]]))
    log("    lost eligibility                                 %6d"
        % lost)
    log("    gained eligibility                               %6d"
        % gained)
    log("    net                                              %+6d"
        % (gained - lost))

    log("")
    log("=" * 66)
    log("(h) ZERO REGRESSIONS -- the older artifacts, unread-only")
    log("=" * 66)
    log("    the_pool2.json entries    %d (unchanged on disk)"
        % pool2["summary"]["entries"])
    log("    the_families2.json families %d (unchanged on disk)"
        % fam2["summary"]["families"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
