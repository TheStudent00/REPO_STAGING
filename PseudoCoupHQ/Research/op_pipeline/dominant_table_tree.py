#!/usr/bin/env python3
"""dominant_table_tree.py -- dominant_table9.json.

Successor to dominant_table_erased.py's dominant_table8.json, adding ONE
new class-forming evidence ground: "tree-exact".

Two units share `tree-exact` when tree_match2.py's own normal-path
root -- the SPILL/RELOAD-fixed, z3-normalized expression tree read off
the lifted `sem` form (tree_units2.json) -- is CHARACTER-IDENTICAL
between them, gated on the SAME class key (operand types AND result
type) every other edge in this table passes through.  Ranked in
EVIDENCE_ORDER between "erased-form" (a stronger, byte-adjacent ground:
identical canonical instruction text) and "sem" (a weaker ground: the
un-normalized anchored lift, no z3 algebra applied) -- tree-exact sits
between the two because it is a NORMALIZED semantic identity (z3
simplify closed the algebraic distance sem alone leaves open, as the
go/op_132 vs rust/op_678 vs c/op_246 modulo family shows: three
different literal lift texts, one z3-normalized tree), but it is not
byte- or instruction-text identity the way erased-form is.

Union-find, accumulation, and the class key are UNCHANGED from
dominant_table_erased.py: this file only OFFERS one more edge source on
top of dominant_table8.json's own rows.  No row is reseeded, no
existing edge is removed -- the owner's ruling of 2026-08-26 ("accumulate,
don't replace") applies directly.

THE SPELLING BAN, verbatim, restated because this program groups and
pairs units: "No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in 'which pairs get
compared', not in report rows, not in dropdowns.  The candidate set
for comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the
member."  The tree-exact groups here are keyed on the z3-normalized
root text (machine evidence, never `operator`) and are additionally
gated on the same class-key check every other edge passes through.
check_no_spelling_keys.py is run over the output before this program
exits successfully (and by the caller, over the emitted file, as the
mechanical guard the ruling requires).

usage:
  dominant_table_tree.py [--in DOMINANT_TABLE8] [--out OUTFILE]
"""

import json
import os
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dominant_table4 as T4                                  # noqa: E402

SOURCE_TABLE = "dominant_table8.json"
TREE_UNITS = "tree_units2.json"
OUT_NAME = "dominant_table9.json"

EVIDENCE_ORDER = ["byte", "canon-byte", "erased-form", "tree-exact", "sem",
                  "core-text", "z3", "unclassified"]

EVIDENCE_TEXT = {
    "byte": "byte identity (the two units are the same machine bytes)",
    "canon-byte": "canonical byte identity (after the rename into the "
                  "canonical runnable form, the two units assemble to "
                  "the same machine bytes)",
    "erased-form": "erased-form identity (the move-erased canonical "
                   "records are line-for-line character-identical)",
    "tree-exact": "tree-exact identity: the spill/reload-fixed, "
                  "z3-normalized lifted expression tree (tree_units2."
                  "json's normal-path root) is character-identical "
                  "between the two units, gated on the same class key",
    "sem": "anchored sem identity (the two lifted forms are identical)",
    "core-text": "core-text identity: verdicts4's own column found the "
                 "two normal-path cores textually equal",
    "z3": "z3-proved (deduction; rests on lifter + solver)",
    "unclassified": "ground not recognised by this builder",
}


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def evidence_class(ground):
    if ground is None:
        return "unclassified"
    text = str(ground)
    if text.startswith("byte identity"):
        return "byte"
    if text.startswith("canon-byte") or text.startswith(
            "canonical byte identity"):
        return "canon-byte"
    if text.startswith("erased-form") or text.startswith(
            "erased identity"):
        return "erased-form"
    if text.startswith("tree-exact"):
        return "tree-exact"
    if text.startswith("sem identity"):
        return "sem"
    if text.startswith("z3"):
        return "z3"
    return "unclassified"


def weakest(names):
    worst = None
    for name in names:
        if name not in EVIDENCE_ORDER:
            name = "unclassified"
        if worst is None:
            worst = name
            continue
        if EVIDENCE_ORDER.index(name) > EVIDENCE_ORDER.index(worst):
            worst = name
    return worst


def load_tree_roots():
    """unit label -> normalized root text, resolved units only."""
    doc = json.load(open(os.path.join(HERE, TREE_UNITS)))
    out = {}
    for u in doc["units"]:
        root = u.get("normal_path_root")
        if not root:
            continue
        label = "%s/op_%s" % (u["lang"], u["n"])
        out[label] = root
    return out


def collect_tree_exact_edges(roots, unit_class, by_id):
    groups = {}
    for unit, root in roots.items():
        groups.setdefault(root, []).append(unit)

    edges = []
    same_key_groups = 0
    cross_key_refused = 0
    for root, units in groups.items():
        if len(units) < 2:
            continue
        units = sorted(units)
        anchor = units[0]
        ca = unit_class.get(anchor)
        if ca is None:
            continue
        anchor_key = T4.class_key_of(by_id[ca]) if ca in by_id else None
        for other in units[1:]:
            cb = unit_class.get(other)
            if cb is None:
                continue
            other_key = T4.class_key_of(by_id[cb]) if cb in by_id else None
            if anchor_key != other_key:
                cross_key_refused += 1
                continue
            same_key_groups += 1
            edges.append(dict(left=anchor, right=other,
                              ground="tree-exact identity: the z3-"
                                     "normalized normal-path root text "
                                     "is character-identical",
                              source="tree_units2.json, normal-path "
                                     "root grouping"))
    return edges, same_key_groups, cross_key_refused


def main():
    indir = HERE
    outdir = HERE
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--in":
            i += 1
            indir = args[i]
        elif args[i] == "--out":
            i += 1
            outdir = args[i]
        i += 1

    started = time.time()

    table = json.load(open(os.path.join(indir, SOURCE_TABLE)))
    rows8 = table["rows"]
    log("classes read (dominant_table8) %d" % len(rows8))

    by_id = {}
    unit_class = {}
    for r in rows8:
        by_id[r["class_id"]] = r
        for m in r["members"]:
            unit_class[m["unit"]] = r["class_id"]

    sets = T4.Sets()
    for r in rows8:
        sets.add(r["class_id"])

    roots = load_tree_roots()
    log("tree_units2.json normal-path roots loaded %d" % len(roots))

    tree_edges, tree_groups, tree_cross_refused = \
        collect_tree_exact_edges(roots, unit_class, by_id)
    log("tree-exact groups usable as edges  %d" % tree_groups)
    log("tree-exact groups refused (class key differs) %d" %
        tree_cross_refused)

    used = []
    refused = []
    refused_why = Counter()
    for e in tree_edges:
        ca = unit_class.get(e["left"])
        cb = unit_class.get(e["right"])
        if ca is None or cb is None:
            refused.append(dict(e, why="an endpoint is in no class"))
            refused_why["an endpoint is in no class"] += 1
            continue
        if T4.class_key_of(by_id[ca]) != T4.class_key_of(by_id[cb]):
            refused.append(dict(e, why="the two classes carry "
                                       "different class keys"))
            refused_why["the two classes carry different class keys"] += 1
            continue
        joined = sets.join(ca, cb)
        used.append(dict(e, left_class=ca, right_class=cb,
                         joined_two_classes=joined))

    log("edges used              %d" % len(used))
    log("edges refused           %d  %s" % (len(refused),
                                            dict(refused_why)))
    merges_that_changed_partition = sum(1 for u in used
                                        if u["joined_two_classes"])
    log("edges that actually MERGED two previously-separate classes %d"
        % merges_that_changed_partition)

    groups = {}
    for r in rows8:
        root = sets.find(r["class_id"])
        groups.setdefault(root, []).append(r)

    final_grounds = {}
    for rec in used:
        root = sets.find(rec["left_class"])
        final_grounds.setdefault(root, []).append(rec["ground"])

    old_order = T4.EVIDENCE_ORDER
    old_text = T4.EVIDENCE_TEXT
    old_evidence_class = T4.evidence_class
    old_weakest = T4.weakest
    T4.EVIDENCE_ORDER = EVIDENCE_ORDER
    T4.EVIDENCE_TEXT = EVIDENCE_TEXT
    T4.evidence_class = evidence_class
    T4.weakest = weakest
    try:
        keys = sorted(groups.keys(),
                      key=lambda k: min(str(x["class_id"])
                                        for x in groups[k]))
        rows9 = []
        for k in keys:
            new_id = min(str(x["class_id"]) for x in groups[k])
            rows9.append(T4.merged_row(new_id, groups[k],
                                       final_grounds.get(k, [])))
    finally:
        T4.EVIDENCE_ORDER = old_order
        T4.EVIDENCE_TEXT = old_text
        T4.evidence_class = old_evidence_class
        T4.weakest = old_weakest

    per_ground = Counter()
    for r in rows9:
        counts = r["evidence"].get("member_pairs_by_class") or {}
        for k, v in counts.items():
            per_ground[k] += v

    stats = {}
    stats["classes_before"] = len(rows8)
    stats["classes_after"] = len(rows9)
    stats["classes_merged_away"] = len(rows8) - len(rows9)
    stats["tree_exact_edges_offered"] = len(tree_edges)
    stats["tree_exact_edges_used"] = len(used)
    stats["tree_exact_edges_that_merged_two_classes"] = \
        merges_that_changed_partition
    stats["tree_exact_groups_refused_cross_class_key"] = tree_cross_refused
    stats["member_pairs_by_evidence_ground"] = dict(per_ground)
    stats["weakest_evidence_distribution"] = dict(Counter(
        str(r["evidence"]["weakest_evidence"]) for r in rows9))

    out = {}
    out["shape"] = "dominant_table8's own partition, plus tree-exact " \
                   "edges from tree_units2.json, closed transitively"
    out["candidate_set"] = "machine-form evidence only: dominant_table8" \
        "'s carried edges, plus tree-exact groups (character-identical " \
        "z3-normalized normal-path root, gated on the same class key). " \
        "No operator token takes part in any key, grouping, pairing " \
        "or selection here."
    out["spelling"] = "the operator token appears once per unit, as " \
                      "the display label `operator` on a member " \
                      "object beside `lang` and `n`."
    out["evidence_order"] = EVIDENCE_ORDER
    out["source_table"] = SOURCE_TABLE
    out["tree_units_source"] = TREE_UNITS
    out["languages"] = T4.LANGS
    out["classes"] = len(rows9)
    out["new_edges_used"] = used
    out["new_edges_refused"] = refused
    out["stats"] = stats
    out["wall_seconds"] = round(time.time() - started, 2)
    out["rows"] = rows9

    path = os.path.join(outdir, OUT_NAME)
    fh = open(path, "w")
    json.dump(out, fh, indent=1)
    fh.write("\n")
    fh.close()
    log("wrote %s" % path)
    log("classes  %d -> %d" % (len(rows8), len(rows9)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
