#!/usr/bin/env python3
"""candidates_mirror.py -- THE THIRD CANDIDATE RULE.

Why this file exists
--------------------
verdicts3.py chose which units to compare by two rules, both
machine-form: CLUSTER (same bytes or same anchored lifted form) and
CONNECTION (a shared maximal sub-term over the anchored variables).
Both rules are about SHARED TEXT.  A unit whose text shares nothing
with any other unit is therefore never nominated at all, and it ends
up alone in a class of one.

dominant_table3.json holds 737 classes of size 1.  Some of those are
genuinely alone.  Others are alone only because the two rules above
are text rules: go's canonical form for one comparison is

    cmp %edi,%esi; setg %al; ret

and cpp's is

    cmp %esi,%edi; setl %al; ret

Different bytes, different lifted text, no shared sub-term -- and the
same answer for every input, because the operand order and the
condition are both flipped.  Nothing in the pipeline was ever asking
the solver about that pair, because nothing ever nominated it.

The third rule, stated exactly
------------------------------
  SINGLETON.  The left unit is the only member of its equivalence
  class in dominant_table3.json.

  and

  SAME CLASS KEY.  The right side is a class carrying the SAME class
  key: the same operand types AND the same result type.  That key is
  the class key the table already uses; it is ABI facts recorded by
  the probe generator plus the recovered result type.  No token.

  and

  REPRESENTATIVE.  A class is an equivalence class, so one member
  stands for all of them.  The right unit is the member of that class
  with the lexicographically smallest unit label that the unit loader
  actually loaded.  This choice is recorded on every pair
  (`right_class`, `right_is_representative_of`), so a reader can see
  which member answered for the class.

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
(operand_types, result_type) and `size`.  It reads no token.  The
token is written once per unit, as `operator`, on an object that also
carries `lang` and `n`.  check_no_spelling_keys.py is run on the
output and a FAIL means the output is refused.

The deciding is NOT re-derived.  `verdicts.judge` and
`z3_ext.z3_pair_ext` are imported and called exactly as verdicts3.py
calls them, through verdicts3's own `decide`, so a pair nominated by
this rule and a pair nominated by the other two are judged by the same
code.

Output: verdicts5.json (and verdicts5.md).  Prior artifacts are left
untouched.

usage:
  candidates_mirror.py [--budget=SECONDS] [--in DIR] [--out DIR]
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
import arch_sem as AS                                         # noqa: E402
import z3                                                     # noqa: E402

CACHE = "verdicts5_cache.json"


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def class_key_of(row):
    """the class key of one table row, as a tuple.  Operand types and
    result type; no token takes part."""
    key = row["class_key"]
    a = key["operand_types"]
    b = key["result_type"]
    return (a, b)


def unit_label(lang, n):
    return "%s/op_%s" % (lang, n)


def representative(row, by_label):
    """the member of one class that answers for it: the smallest unit
    label the unit loader actually loaded."""
    labels = []
    for m in row["members"]:
        labels.append(unit_label(m["lang"], m["n"]))
    labels.sort()
    for label in labels:
        if label in by_label:
            return label
    return None


def nominate(table, by_label):
    """every (singleton unit, other class) nomination the third rule
    makes."""
    by_key = {}
    for row in table["rows"]:
        key = class_key_of(row)
        if key not in by_key:
            by_key[key] = []
        by_key[key].append(row)

    reps = {}
    for row in table["rows"]:
        reps[row["class_id"]] = representative(row, by_label)

    out = []
    skipped = Counter()
    for row in table["rows"]:
        if row["size"] != 1:
            continue
        left = unit_label(row["members"][0]["lang"],
                          row["members"][0]["n"])
        if left not in by_label:
            skipped["singleton unit not loaded by the unit loader"] += 1
            continue
        key = class_key_of(row)
        for other in by_key[key]:
            if other["class_id"] == row["class_id"]:
                continue
            right = reps[other["class_id"]]
            if right is None:
                skipped["no member of the other class was loaded"] += 1
                continue
            if right == left:
                continue
            rec = {}
            rec["left"] = left
            rec["right"] = right
            rec["left_class"] = row["class_id"]
            rec["right_class"] = other["class_id"]
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
        a, b = k.split("|")
        out[(a, b)] = doc[k]
    return out


def save_cache(path, decided):
    doc = {}
    for key in decided:
        doc["%s|%s" % (key[0], key[1])] = decided[key]
    fh = open(path, "w")
    json.dump(doc, fh)
    fh.close()


def main():
    indir = HERE
    outdir = HERE
    budget = 0
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        a = args[i]
        if a.startswith("--budget="):
            budget = int(a.split("=")[1])
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
        by_label[unit_label(u["lang"], u["n"])] = u
    log("units loaded            %d" % len(by_label))

    path = os.path.join(indir, "dominant_table3.json")
    table = json.load(open(path))
    log("classes read            %d" % len(table["rows"]))

    noms, skipped = nominate(table, by_label)
    log("nominations             %d" % len(noms))
    log("skipped                 %s" % skipped)

    cache_path = os.path.join(outdir, CACHE)
    decided = load_cache(cache_path)
    log("already cached          %d" % len(decided))

    fresh = 0
    for rec in noms:
        left = rec["left"]
        right = rec["right"]
        pid = (left, right)
        if left > right:
            pid = (right, left)
        rec["pair_id"] = "%s|%s" % (pid[0], pid[1])
        if pid in decided:
            continue
        if budget > 0 and time.time() - started > budget:
            save_cache(cache_path, decided)
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
            save_cache(cache_path, decided)
            log("progress: %d fresh, %d cached, %ds elapsed"
                % (fresh, len(decided), int(time.time() - started)))

    save_cache(cache_path, decided)

    tally = Counter()
    pairs = []
    for rec in noms:
        pid = tuple(rec["pair_id"].split("|"))
        v = decided.get(pid)
        if v is None:
            continue
        keep = dict(rec)
        keep["verdict"] = v["verdict"]
        keep["ground"] = v.get("ground")
        keep["detail"] = v.get("detail")
        keep["tier1"] = v.get("tier1")
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
    doc["shape"] = "one entry per nomination the third candidate "\
                   "rule made: a unit alone in its class, against a "\
                   "representative of another class carrying the same "\
                   "class key"
    doc["candidate_set"] = "SINGLETON (the left unit is the only "\
                           "member of its class) and SAME CLASS KEY "\
                           "(same operand types and same result "\
                           "type).  No operator token takes part in "\
                           "any key, grouping, pairing or selection "\
                           "here."
    doc["spelling"] = "the operator token appears once per unit, as "\
                      "the display label `operator` on an object that "\
                      "also carries `lang` and `n`"
    doc["representative_rule"] = "a class is an equivalence class, so "\
                                 "one member answers for it: the "\
                                 "smallest unit label the unit loader "\
                                 "loaded.  Recorded per pair."
    doc["deciding"] = "verdicts3.decide, imported unchanged: "\
                      "verdicts.judge (bytes, anchored sem, the "\
                      "one-sided guard reading, the narrow z3 "\
                      "translation) then z3_ext.z3_pair_ext where the "\
                      "wider translation can say something new"
    doc["source_table"] = "dominant_table3.json"
    doc["languages"] = V.LANGS
    doc["units_loaded"] = len(by_label)
    doc["classes_read"] = len(table["rows"])
    doc["singleton_classes"] = sum(1 for r in table["rows"]
                                   if r["size"] == 1)
    doc["nominations"] = len(noms)
    doc["nominations_skipped"] = skipped
    doc["distinct_pairs"] = len(decided)
    doc["tally"] = dict(tally)
    doc["matched_count"] = len(matched)
    doc["z3"] = z3.get_version_string()
    doc["lifter"] = AS.LIFTER_ID
    doc["wall_seconds"] = round(time.time() - started, 2)
    doc["pairs"] = pairs

    path = os.path.join(outdir, "verdicts5.json")
    fh = open(path, "w")
    json.dump(doc, fh, indent=1)
    fh.write("\n")
    fh.close()
    log("wrote %s" % path)

    write_md(doc, os.path.join(outdir, "verdicts5.md"))
    log("wrote %s" % os.path.join(outdir, "verdicts5.md"))

    log("== the third candidate rule")
    log("   nominations   %d" % len(noms))
    log("   distinct pairs%d" % len(decided))
    for w in ("MATCHED", "DIFFERS-BY-DESIGN", "UNMATCHED", "UNDECIDED"):
        log("   %-20s %d" % (w, tally.get(w, 0)))
    return 0


def write_md(doc, path):
    out = []
    out.append("# verdicts5 -- the third candidate rule")
    out.append("")
    out.append("A unit alone in its class, nominated against every")
    out.append("other class carrying the same class key (same operand")
    out.append("types, same result type).  No operator token takes")
    out.append("part in the nomination; each member carries its token")
    out.append("as a display label only.")
    out.append("")
    out.append("- classes read: %d" % doc["classes_read"])
    out.append("- classes of size 1: %d" % doc["singleton_classes"])
    out.append("- nominations: %d" % doc["nominations"])
    out.append("- distinct unit pairs judged: %d" % doc["distinct_pairs"])
    out.append("- tally: %s" % doc["tally"])
    out.append("")
    out.append("## the MATCHED pairs")
    out.append("")
    out.append("| left | right | left label | right label | operand "
               "types | result | ground |")
    out.append("|---|---|---|---|---|---|---|")
    for p in doc["pairs"]:
        if p["verdict"] != "MATCHED":
            continue
        out.append("| %s | %s | `%s` | `%s` | %s | %s | %s |"
                   % (p["left"], p["right"],
                      p["left_member"]["operator"],
                      p["right_member"]["operator"],
                      p["operand_types"], p["result_type"],
                      p["ground"]))
    out.append("")
    fh = open(path, "w")
    fh.write("\n".join(out))
    fh.close()


if __name__ == "__main__":
    sys.exit(main())
