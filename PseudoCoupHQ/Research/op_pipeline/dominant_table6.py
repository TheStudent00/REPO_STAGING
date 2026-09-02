#!/usr/bin/env python3
"""dominant_table6.py -- the classes rebuilt after the WIDENED third
candidate rule.

What this file does, stated exactly so nothing is claimed that was not
done
------------------------------------------------------------------
It does NOT re-derive the classes from the unit records.  It takes the
partition dominant_table5.json already holds and ADDS the MATCHED
pairs verdicts6.json found -- the pairs the widened rule nominated and
that no earlier rule ever asked about.  The result is the transitive
closure of the old edge set plus the new one, which is what a full
rebuild would compute, because closure is closure.  This is the same
method dominant_table4.py used, and that file's merge code is
IMPORTED here rather than copied.

Every new edge is checked before it is used: both endpoints must carry
the same class key (operand types AND result type).  An edge that
fails that check is refused and recorded, not silently dropped.

RULED, and this is why the z3 edges are used at all: "Level-2
(z3-proved, deduction over bit arithmetic) edges ARE class-forming,
with the class's weakest-evidence marker saying so."  A class whose
weakest contributing edge is a z3 edge says `z3-proved (deduction;
rests on lifter + solver)`.

WHAT IS CARRIED RATHER THAN RECOMPUTED, named so a reader is not
misled: `bridges_out` / `bridges_in` on a merged row are the UNION of
the bridge records the merged rows carried, under the old class ids.
dominance.py was NOT re-run.  The rows say so in `bridges_note`.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key,
grouping, pairing, row structure, candidate selection, or comparison
scope, anywhere in this line -- not in matching, not in "which pairs
get compared", not in report rows, not in dropdowns.  The candidate
set for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from the
token.  The token appears exactly once per unit: as a display label on
the member.

usage:
  dominant_table6.py [--in DIR] [--out DIR] [--table NAME]
                     [--verdicts NAME]
"""

import json
import os
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dominant_table4 as T4                                  # noqa: E402

DEFAULT_TABLE = "dominant_table5.json"

DEFAULT_VERDICTS = "verdicts6.json"

OUT_NAME = "dominant_table6.json"


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def main():
    indir = HERE
    outdir = HERE
    table_name = DEFAULT_TABLE
    verdicts_name = DEFAULT_VERDICTS
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--in":
            i = i + 1
            indir = args[i]
        elif args[i] == "--out":
            i = i + 1
            outdir = args[i]
        elif args[i] == "--table":
            i = i + 1
            table_name = args[i]
        elif args[i] == "--verdicts":
            i = i + 1
            verdicts_name = args[i]
        i = i + 1

    started = time.time()

    path = os.path.join(indir, table_name)
    table = json.load(open(path))
    rows5 = table["rows"]
    log("source table            %s" % table_name)
    log("classes read            %d" % len(rows5))

    path = os.path.join(indir, verdicts_name)
    verdicts = json.load(open(path))
    log("verdicts read           %s" % verdicts_name)

    by_id = {}
    unit_class = {}
    for r in rows5:
        by_id[r["class_id"]] = r
        for m in r["members"]:
            unit_class[m["unit"]] = r["class_id"]

    sets = T4.Sets()
    for r in rows5:
        sets.add(r["class_id"])

    used = []
    refused = []
    offered = 0
    for p in verdicts["pairs"]:
        if p["verdict"] != "MATCHED":
            continue
        offered = offered + 1
        ca = unit_class.get(p["left"])
        cb = unit_class.get(p["right"])
        if ca is None or cb is None:
            refused.append(dict(pair=p["pair_id"],
                                why="an endpoint is in no class of "
                                    "the source table"))
            continue
        if T4.class_key_of(by_id[ca]) != T4.class_key_of(by_id[cb]):
            refused.append(dict(pair=p["pair_id"],
                                why="the two classes carry different "
                                    "class keys"))
            continue
        joined = sets.join(ca, cb)
        used.append(dict(pair=p["pair_id"], left_class=ca,
                         right_class=cb, ground=p["ground"],
                         joined_two_classes=joined))

    log("MATCHED pairs offered   %d" % offered)
    log("edges used              %d" % len(used))
    log("edges refused           %d" % len(refused))

    groups = {}
    for r in rows5:
        root = sets.find(r["class_id"])
        if root not in groups:
            groups[root] = []
        groups[root].append(r)

    # a ground recorded under an intermediate root must land on the
    # final root; re-key after all joins are done.
    final_grounds = {}
    for rec in used:
        root = sets.find(rec["left_class"])
        if root not in final_grounds:
            final_grounds[root] = []
        final_grounds[root].append(rec["ground"])

    keys = sorted(groups.keys(), key=lambda k: min(x["class_id"]
                                                   for x in groups[k]))
    # THE CLASS ID IS NOT RE-MINTED.  A merged class keeps the
    # SMALLEST of the class ids that merged into it, so every id an
    # earlier artifact names still resolves.
    rows6 = []
    remap = {}
    for k in keys:
        new_id = min(x["class_id"] for x in groups[k])
        for x in groups[k]:
            remap[x["class_id"]] = new_id
        rows6.append(T4.merged_row(new_id, groups[k],
                                   final_grounds.get(k, [])))

    before_singletons = []
    for r in rows5:
        if r["size"] == 1:
            before_singletons.append(r["class_id"])
    after_singletons = []
    for r in rows6:
        if r["size"] == 1:
            after_singletons.append(r["class_id"])

    stats = {}
    stats["classes"] = len(rows6)
    stats["classes_before"] = len(rows5)
    stats["classes_size_1"] = len(after_singletons)
    stats["classes_size_1_before"] = len(before_singletons)
    stats["classes_spanning_2_or_more_languages"] = \
        sum(1 for r in rows6 if len(r["languages"]) >= 2)
    stats["weakest_evidence_distribution"] = dict(Counter(
        str(r["evidence"]["weakest_evidence"]) for r in rows6))
    stats["merged_rows"] = sum(1 for r in rows6
                               if len(r["merged_from"]) > 1)

    out = {}
    out["shape"] = "one row per equivalence class on one class key: "\
                   "operand types AND result type"
    out["class_definition"] = "the transitive closure of the edge set "\
                              "%s used, plus the MATCHED pairs %s "\
                              "found under the WIDENED third candidate "\
                              "rule (classes of three or fewer "\
                              "members)" % (table_name, verdicts_name)
    out["candidate_set"] = "machine-form evidence only: the carried "\
                           "edge set, plus verdicts6's "\
                           "small-class-against-same-class-key "\
                           "nominations.  No operator token takes part "\
                           "in any key, grouping, pairing or selection "\
                           "here."
    out["spelling"] = "the operator token appears once per unit, as "\
                      "the display label `operator` on a member object "\
                      "beside `lang` and `n`."
    out["weakest_evidence_note"] = "a class is the transitive closure "\
                                   "of its edges, so it is only as "\
                                   "strong as its weakest edge."
    out["what_was_not_recomputed"] = "bridges_out / bridges_in are "\
                                     "carried under the old class "\
                                     "ids; dominance.py was NOT "\
                                     "re-run."
    out["source_table"] = table_name
    out["source_verdicts"] = verdicts_name
    out["languages"] = T4.LANGS
    out["classes"] = len(rows6)
    out["new_edges_used"] = used
    out["new_edges_refused"] = refused
    out["stats"] = stats
    out["wall_seconds"] = round(time.time() - started, 2)
    out["rows"] = rows6

    path = os.path.join(outdir, OUT_NAME)
    fh = open(path, "w")
    json.dump(out, fh, indent=1)
    fh.write("\n")
    fh.close()
    log("wrote %s" % path)

    write_md(out, os.path.join(outdir, OUT_NAME.replace(".json", ".md")))
    log("wrote %s" % OUT_NAME.replace(".json", ".md"))

    rewrite_bridges(indir, outdir, remap)

    log("classes  %d -> %d" % (len(rows5), len(rows6)))
    log("size-1   %d -> %d" % (len(before_singletons),
                               len(after_singletons)))
    return 0


def rewrite_bridges(indir, outdir, remap):
    """bridges4.json with its class ids moved onto the new classes.

    This is dominant_table4.rewrite_bridges' method, applied one step
    later.  dominance.py was NOT re-run.  This only follows the two
    class ids a bridge names into the class each one now sits in.  A
    bridge whose two ends landed in ONE class is dropped and counted:
    the two forms it related are now the same class, so there is
    nothing left to bridge.  Every surviving bridge keeps its own proof
    text unchanged, and says which ids it was proved under."""
    path = os.path.join(indir, "bridges4.json")
    if not os.path.exists(path):
        log("no bridges4.json to remap")
        return
    doc = json.load(open(path))
    kept = []
    collapsed = []
    for b in doc["bridges"]:
        a = remap.get(b["dominant_class"], b["dominant_class"])
        c = remap.get(b["dominated_class"], b["dominated_class"])
        rec = dict(b)
        rec["dominant_class"] = a
        rec["dominated_class"] = c
        if a == c:
            collapsed.append(rec)
            continue
        kept.append(rec)
    out = dict(doc)
    out["bridges"] = kept
    out["bridge_count"] = len(kept)
    out["remap_note"] = "class ids follow dominant_table6; "\
                        "dominance.py was NOT re-run.  Bridges whose "\
                        "two ends became one class are moved to "\
                        "`bridges_collapsed_by_a_merge`."
    carried = doc.get("bridges_collapsed_by_a_merge") or []
    out["bridges_collapsed_by_a_merge"] = carried + collapsed
    dest = os.path.join(outdir, "bridges6.json")
    fh = open(dest, "w")
    json.dump(out, fh, indent=1)
    fh.write("\n")
    fh.close()
    log("wrote %s (%d bridges kept, %d newly collapsed by a merge)"
        % (dest, len(kept), len(collapsed)))


def write_md(out, path):
    lines = []
    lines.append("# dominant_table6 -- classes after the widened third "
                 "candidate rule")
    lines.append("")
    lines.append("- source table: %s" % out["source_table"])
    lines.append("- source verdicts: %s" % out["source_verdicts"])
    lines.append("- classes: %d (was %d)"
                 % (out["stats"]["classes"],
                    out["stats"]["classes_before"]))
    lines.append("- classes of size 1: %d (was %d)"
                 % (out["stats"]["classes_size_1"],
                    out["stats"]["classes_size_1_before"]))
    lines.append("- rows that are a merge of two or more source "
                 "classes: %d" % out["stats"]["merged_rows"])
    lines.append("- weakest evidence: %s"
                 % out["stats"]["weakest_evidence_distribution"])
    lines.append("")
    lines.append("## the edges this table added")
    lines.append("")
    lines.append("| pair | left class | right class | ground | joined "
                 "two classes |")
    lines.append("|---|---|---|---|---|")
    for e in out["new_edges_used"]:
        lines.append("| %s | %s | %s | %s | %s |"
                     % (e["pair"], e["left_class"], e["right_class"],
                        e["ground"], e["joined_two_classes"]))
    lines.append("")
    lines.append("## the rows that merged")
    lines.append("")
    lines.append("| class | merged from | operand types | result | "
                 "languages | members | weakest evidence |")
    lines.append("|---|---|---|---|---|---|---|")
    for r in out["rows"]:
        if len(r["merged_from"]) < 2:
            continue
        labels = []
        for m in r["members"]:
            labels.append("%s `%s`" % (m["lang"], m["operator"]))
        lines.append("| %s | %s | %s | %s | %s | %s | %s |"
                     % (r["class_id"], ", ".join(r["merged_from"]),
                        r["type_pair"], r["result_type"],
                        ", ".join(r["languages"]), "; ".join(labels),
                        r["evidence"]["weakest_evidence"]))
    lines.append("")
    fh = open(path, "w")
    fh.write("\n".join(lines))
    fh.close()


if __name__ == "__main__":
    sys.exit(main())
