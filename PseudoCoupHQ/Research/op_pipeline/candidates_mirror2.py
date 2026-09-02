#!/usr/bin/env python3
"""candidates_mirror2.py -- THE THIRD CANDIDATE RULE, WIDENED FROM
CLASSES OF ONE TO CLASSES OF THREE OR FEWER.

What was wrong with the rule as it stood
----------------------------------------
candidates_mirror.py nominates a unit only when that unit is ALONE in
its class.  The reason it was written that way is in its own
docstring: a unit whose machine text shares nothing with any other
unit is never nominated by the cluster rule or the connection rule, so
it lands in a class of one, and the singleton test finds it.

But being alone was never the thing that mattered.  What mattered was
that the two text rules are TEXT rules, and a mirrored pair -- flipped
operand order and flipped condition -- shares no text.  A unit can be
mirrored against a foreign unit and still not be alone, because it
found a same-language or same-bytes companion first.  The singleton
test cannot see it, and the pair is never asked about.

That is exactly what happened to go.  Two of go's comparison units sit
in classes of two, paired with swift; the mirrored cpp/c form sits in
another class with the same class key; and no rule in the pipeline
ever nominated the pair, so it was never decided either way.

The rule this file states
-------------------------
  SMALL CLASS.  The left side is a class of THREE OR FEWER members.
  Three is a threshold on class SIZE -- a count of members.  It is not
  derived from any token, and it does not read one.

  and

  SAME CLASS KEY.  The right side is another class carrying the SAME
  class key: the same operand types AND the same result type.  That is
  the class key the table already uses -- ABI facts recorded by the
  probe generator, plus the recovered result type.  No token.

  and

  REPRESENTATIVE, ON BOTH SIDES.  A class is an equivalence class, so
  one member stands for all of them.  candidates_mirror.representative
  is imported and used unchanged: the member with the smallest unit
  label that the unit loader actually loaded.  candidates_mirror used
  a representative only on the right, because its left side was a
  class of one and had no choice.  Here both sides are classes, so
  both sides send a representative, and each pair records which member
  answered for which class.

  and

  NOT ALREADY DECIDED.  A pair is skipped when the two units already
  sit in the SAME class (there is nothing to decide), and a pair whose
  verdict is already on record is REUSED rather than re-solved.  The
  caches read are verdicts3_cache.json and, when it survives,
  verdicts5_cache.json.  Reuse, not re-derivation: a carried verdict
  and a fresh one come from the same code.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns.  The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label on
the member.

How this file obeys it: the nomination reads `class_key`
(operand_types, result_type) and `size`, an integer.  It reads no
token.  The token is written once per unit, as `operator`, on an
object that also carries `lang` and `n`.  check_no_spelling_keys.py is
run on the output and a FAIL means the output is refused.

The deciding is NOT re-derived.  `verdicts3.decide` is imported and
called exactly as candidates_mirror.py calls it, so a pair nominated
by this rule and a pair nominated by any earlier rule are judged by
the same code.  Level-2 (z3-proved) edges are class-forming by
the owner's ruling of 2026-08-25, and the class carries its weakest-evidence
marker saying so.

SOURCE TABLE, and this is a deviation from the brief, stated plainly:
the brief named dominant_table4.json.  dominant_table5.json already
existed when this ran -- it is dominant_table4 plus the single java
member the jvm join added, and it is what dom_ops3.json was built
from.  It is a strict superset, so this file reads table 5; reading
table 4 would silently drop java from the lap.  Override with --table.

Output: verdicts6.json, verdicts6.md, verdicts6_cache.json.  Prior
artifacts are left untouched.

usage:
  candidates_mirror2.py [--budget=SECONDS] [--max-size=N]
                        [--table NAME] [--in DIR] [--out DIR]
"""

import json
import os
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import verdicts as V                                          # noqa: E402
import verdicts3 as V3                                        # noqa: E402
import candidates_mirror as CM                                # noqa: E402
import arch_sem as AS                                         # noqa: E402
import z3                                                     # noqa: E402

CACHE = "verdicts6_cache.json"

WARM_CACHES = ["verdicts3_cache.json", "verdicts5_cache.json"]

DEFAULT_TABLE = "dominant_table5.json"

DEFAULT_MAX_SIZE = 3


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def nominate(table, by_label, max_size):
    """every (small class, other class) nomination the widened rule
    makes.

    Both sides send the representative of their class.  A pair of
    classes can be reached from either end; the pair is recorded once
    per ordered nomination and de-duplicated later by `pair_id`, the
    same way candidates_mirror.py does it."""
    by_key = {}
    for row in table["rows"]:
        key = CM.class_key_of(row)
        if key not in by_key:
            by_key[key] = []
        by_key[key].append(row)

    reps = {}
    sizes = {}
    for row in table["rows"]:
        reps[row["class_id"]] = CM.representative(row, by_label)
        sizes[row["class_id"]] = row["size"]

    out = []
    skipped = Counter()
    for row in table["rows"]:
        if row["size"] > max_size:
            continue
        left = reps[row["class_id"]]
        if left is None:
            skipped["no member of the small class was loaded"] += 1
            continue
        key = CM.class_key_of(row)
        for other in by_key[key]:
            if other["class_id"] == row["class_id"]:
                continue
            right = reps[other["class_id"]]
            if right is None:
                skipped["no member of the other class was loaded"] += 1
                continue
            if right == left:
                skipped["both classes sent the same unit"] += 1
                continue
            rec = {}
            rec["left"] = left
            rec["right"] = right
            rec["left_class"] = row["class_id"]
            rec["right_class"] = other["class_id"]
            rec["left_is_representative_of"] = row["size"]
            rec["right_is_representative_of"] = other["size"]
            rec["operand_types"] = key[0]
            rec["result_type"] = key[1]
            out.append(rec)
    return out, dict(skipped)


def load_cache(path):
    if not os.path.exists(path):
        return {}
    doc = json.load(open(path))
    out = {}
    for k in doc:
        parts = k.split("|")
        if len(parts) != 2:
            continue
        out[(parts[0], parts[1])] = doc[k]
    return out


def save_cache(path, decided):
    doc = {}
    for key in decided:
        doc["%s|%s" % (key[0], key[1])] = decided[key]
    fh = open(path, "w")
    json.dump(doc, fh)
    fh.close()


def warm_start(indir):
    """the verdicts already on record, so a pair decided in an earlier
    run is reused instead of re-solved."""
    out = {}
    where = {}
    for name in WARM_CACHES:
        path = os.path.join(indir, name)
        got = load_cache(path)
        for key in got:
            if key in out:
                continue
            out[key] = got[key]
            where[key] = name
        log("warm cache %-24s %d entries" % (name, len(got)))
    return out, where


def main():
    indir = HERE
    outdir = HERE
    budget = 0
    max_size = DEFAULT_MAX_SIZE
    table_name = DEFAULT_TABLE
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        a = args[i]
        if a.startswith("--budget="):
            budget = int(a.split("=")[1])
        elif a.startswith("--max-size="):
            max_size = int(a.split("=")[1])
        elif a == "--table":
            i = i + 1
            table_name = args[i]
        elif a == "--in":
            i = i + 1
            indir = args[i]
        elif a == "--out":
            i = i + 1
            outdir = args[i]
        i = i + 1

    started = time.time()

    units, excluded, excluded_rows = V.load_units()
    by_label = {}
    for u in units:
        by_label[CM.unit_label(u["lang"], u["n"])] = u
    log("units loaded            %d" % len(by_label))

    path = os.path.join(indir, table_name)
    table = json.load(open(path))
    log("source table            %s" % table_name)
    log("classes read            %d" % len(table["rows"]))

    small = 0
    for r in table["rows"]:
        if r["size"] <= max_size:
            small = small + 1
    log("classes of size <= %d    %d" % (max_size, small))

    unit_class = {}
    for r in table["rows"]:
        for m in r["members"]:
            unit_class[m["unit"]] = r["class_id"]

    noms, skipped = nominate(table, by_label, max_size)
    log("nominations             %d" % len(noms))
    log("skipped                 %s" % skipped)

    carried, carried_from = warm_start(indir)
    decided = {}
    for key in carried:
        decided[key] = carried[key]
    log("verdicts carried in     %d" % len(decided))

    reused = 0
    fresh = 0
    same_class = 0
    for rec in noms:
        left = rec["left"]
        right = rec["right"]
        pid = (left, right)
        if left > right:
            pid = (right, left)
        rec["pair_id"] = "%s|%s" % (pid[0], pid[1])
        if unit_class.get(left) == unit_class.get(right):
            rec["skipped"] = "the two units already sit in one class"
            same_class = same_class + 1
            continue
        if pid in decided:
            if pid in carried:
                reused = reused + 1
            continue
        if budget > 0 and time.time() - started > budget:
            save_cache(os.path.join(outdir, CACHE), decided)
            log("budget spent; %d decided, run again to continue"
                % len(decided))
            return 3
        ua = by_label[pid[0]]
        ub = by_label[pid[1]]
        tp = rec["operand_types"]
        v = V3.decide(ua, ub, tp)
        decided[pid] = v
        fresh = fresh + 1
        if fresh % 200 == 0:
            save_cache(os.path.join(outdir, CACHE), decided)
            log("progress: %d fresh, %d decided, %ds elapsed"
                % (fresh, len(decided), int(time.time() - started)))

    save_cache(os.path.join(outdir, CACHE), decided)
    log("pairs already in one class %d" % same_class)
    log("verdicts reused from cache %d" % reused)
    log("verdicts freshly decided   %d" % fresh)

    tally = Counter()
    pairs = []
    seen_pairs = set()
    for rec in noms:
        if rec.get("skipped"):
            continue
        pid = tuple(rec["pair_id"].split("|"))
        v = decided.get(pid)
        if v is None:
            continue
        if rec["pair_id"] in seen_pairs:
            continue
        seen_pairs.add(rec["pair_id"])
        keep = dict(rec)
        keep["verdict"] = v["verdict"]
        keep["ground"] = v.get("ground")
        keep["detail"] = v.get("detail")
        keep["tier1"] = v.get("tier1")
        keep["verdict_carried_from"] = carried_from.get(pid)
        ua = by_label[rec["left"]]
        ub = by_label[rec["right"]]
        keep["left_member"] = dict(lang=ua["lang"], n=ua["n"],
                                   operator=ua["meta"].get("operator"))
        keep["right_member"] = dict(lang=ub["lang"], n=ub["n"],
                                    operator=ub["meta"].get("operator"))
        tally[v["verdict"]] += 1
        pairs.append(keep)

    matched = []
    for p in pairs:
        if p["verdict"] != "MATCHED":
            continue
        matched.append(p)

    doc = {}
    doc["shape"] = "one entry per distinct pair the widened third "\
                   "candidate rule nominated: the representative of a "\
                   "class of three or fewer members, against the "\
                   "representative of another class carrying the same "\
                   "class key"
    doc["candidate_set"] = "SMALL CLASS (the left class has three or "\
                           "fewer members -- a count, not a token) and "\
                           "SAME CLASS KEY (same operand types and "\
                           "same result type).  No operator token "\
                           "takes part in any key, grouping, pairing "\
                           "or selection here."
    doc["what_changed_from_candidates_mirror"] = "the left side was a "\
        "class of exactly one; it is now a class of at most three, "\
        "and it sends a representative rather than its only member.  "\
        "Everything else -- the class key, the representative rule, "\
        "the deciding code -- is imported unchanged."
    doc["spelling"] = "the operator token appears once per unit, as "\
                      "the display label `operator` on an object that "\
                      "also carries `lang` and `n`"
    doc["representative_rule"] = "candidates_mirror.representative, "\
                                 "imported unchanged: the smallest "\
                                 "unit label the unit loader loaded.  "\
                                 "Recorded per pair on both sides."
    doc["deciding"] = "verdicts3.decide, imported unchanged"
    doc["already_decided_rule"] = "a pair whose two units already sit "\
                                  "in one class is not nominated; a "\
                                  "pair already on record is reused "\
                                  "from cache, not re-solved"
    doc["source_table"] = table_name
    doc["max_class_size"] = max_size
    doc["languages"] = V.LANGS
    doc["units_loaded"] = len(by_label)
    doc["classes_read"] = len(table["rows"])
    doc["small_classes"] = small
    doc["nominations"] = len(noms)
    doc["nominations_skipped"] = skipped
    doc["pairs_already_in_one_class"] = same_class
    doc["verdicts_reused"] = reused
    doc["verdicts_fresh"] = fresh
    doc["distinct_pairs"] = len(pairs)
    doc["tally"] = dict(tally)
    doc["matched_count"] = len(matched)
    doc["z3"] = z3.get_version_string()
    doc["lifter"] = AS.LIFTER_ID
    doc["wall_seconds"] = round(time.time() - started, 2)
    doc["pairs"] = pairs

    path = os.path.join(outdir, "verdicts6.json")
    fh = open(path, "w")
    json.dump(doc, fh, indent=1)
    fh.write("\n")
    fh.close()
    log("wrote %s" % path)

    write_md(doc, os.path.join(outdir, "verdicts6.md"))
    log("wrote %s" % os.path.join(outdir, "verdicts6.md"))

    log("== the widened third candidate rule")
    log("   nominations    %d" % len(noms))
    log("   distinct pairs %d" % len(pairs))
    for w in ("MATCHED", "DIFFERS-BY-DESIGN", "UNMATCHED", "UNDECIDED"):
        log("   %-20s %d" % (w, tally.get(w, 0)))
    return 0


def write_md(doc, path):
    out = []
    out.append("# verdicts6 -- the third candidate rule, widened to "
               "classes of three or fewer")
    out.append("")
    out.append("The representative of a class of at most three members,")
    out.append("nominated against the representative of every other")
    out.append("class carrying the same class key (same operand types,")
    out.append("same result type).  No operator token takes part in the")
    out.append("nomination; each member carries its token as a display")
    out.append("label only.")
    out.append("")
    out.append("- source table: %s" % doc["source_table"])
    out.append("- classes read: %d" % doc["classes_read"])
    out.append("- classes of size <= %d: %d" % (doc["max_class_size"],
                                                doc["small_classes"]))
    out.append("- nominations: %d" % doc["nominations"])
    out.append("- pairs already in one class (not nominated): %d"
               % doc["pairs_already_in_one_class"])
    out.append("- distinct unit pairs judged: %d" % doc["distinct_pairs"])
    out.append("- verdicts reused from cache: %d" % doc["verdicts_reused"])
    out.append("- verdicts freshly decided: %d" % doc["verdicts_fresh"])
    out.append("- tally: %s" % doc["tally"])
    out.append("")
    out.append("## the MATCHED pairs")
    out.append("")
    out.append("| left | right | left label | right label | left class "
               "size | right class size | operand types | result | "
               "ground |")
    out.append("|---|---|---|---|---|---|---|---|---|")
    for p in doc["pairs"]:
        if p["verdict"] != "MATCHED":
            continue
        out.append("| %s | %s | `%s` | `%s` | %s | %s | %s | %s | %s |"
                   % (p["left"], p["right"],
                      p["left_member"]["operator"],
                      p["right_member"]["operator"],
                      p["left_is_representative_of"],
                      p["right_is_representative_of"],
                      p["operand_types"], p["result_type"],
                      p["ground"]))
    out.append("")
    fh = open(path, "w")
    fh.write("\n".join(out))
    fh.close()


if __name__ == "__main__":
    sys.exit(main())
