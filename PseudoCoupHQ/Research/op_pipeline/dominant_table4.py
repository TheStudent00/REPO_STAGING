#!/usr/bin/env python3
"""dominant_table4.py -- the classes rebuilt after the third candidate
rule.

What this file does, stated exactly so nothing is claimed that was not
done
------------------------------------------------------------------
It does NOT re-derive the classes from the unit records.  It takes the
partition dominant_table3.json already holds -- which is itself the
transitive closure of verdicts4's total-equality edges, verdicts3b's
z3-proved MATCHED pairs and canonical-byte identity -- and ADDS the
MATCHED pairs verdicts5.json found, which are the pairs the first two
candidate rules never nominated.  The result is the transitive closure
of the old edge set plus the new one, which is what a full rebuild
would compute, because closure is closure.

Every new edge is checked before it is used: both endpoints must carry
the same class key (operand types AND result type).  An edge that
fails that check is refused and recorded, not silently dropped.  By
construction of the third candidate rule none should fail; the check
is here because the ruling says the key is part of the class, and a
check that never fires is still the check.

RULED, and this is why the z3 edges are used at all: "Level-2
(z3-proved, deduction over bit arithmetic) edges ARE class-forming,
with the class's weakest-evidence marker saying so."  A class whose
weakest contributing edge is a z3 edge says `z3-proved (deduction;
rests on lifter + solver)`.

WHAT IS CARRIED RATHER THAN RECOMPUTED, named so a reader is not
misled: `bridges_out` / `bridges_in` on a merged row are the UNION of
the bridge records the merged rows carried in dominant_table3, under
the old class ids.  dominance.py was not re-run.  The rows say so in
`bridges_note`.  `intention_candidates` is carried from the largest
contributing row.  Everything else on a merged row -- size, languages,
members, canonical cores, mode inventory, divergences, evidence,
coverage -- is recomputed from the merged member set.

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
  dominant_table4.py [--in DIR] [--out DIR]
"""

import json
import os
import sys
import time
from collections import Counter

LANGS = ["c", "cpp", "go", "rust", "swift"]

EVIDENCE_ORDER = ["byte", "canon-byte", "sem", "core-text", "z3",
                  "unclassified"]

EVIDENCE_TEXT = {
    "byte": "byte identity (the two units are the same machine bytes)",
    "canon-byte": "canonical byte identity (after the rename into the "
                  "canonical runnable form, the two units assemble to "
                  "the same machine bytes)",
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
    """which evidence class one recorded ground belongs to."""
    if ground is None:
        return "unclassified"
    text = str(ground)
    if text.startswith("byte identity"):
        return "byte"
    if text.startswith("sem identity"):
        return "sem"
    if text.startswith("z3"):
        return "z3"
    return "unclassified"


def weakest(names):
    """the weakest evidence class among those named."""
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


# ------------------------------------------------------- union-find

class Sets(object):

    def __init__(self):
        self.up = {}

    def add(self, x):
        if x not in self.up:
            self.up[x] = x

    def find(self, x):
        self.add(x)
        while self.up[x] != x:
            self.up[x] = self.up[self.up[x]]
            x = self.up[x]
        return x

    def join(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return False
        self.up[rb] = ra
        return True


# ---------------------------------------------------------------- io

def load(indir):
    doc = {}
    path = os.path.join(indir, "dominant_table3.json")
    doc["table"] = json.load(open(path))
    path = os.path.join(indir, "verdicts5.json")
    doc["verdicts5"] = json.load(open(path))
    return doc


def class_key_of(row):
    key = row["class_key"]
    return (key["operand_types"], key["result_type"])


# ------------------------------------------------------------ merge

def merged_row(new_id, rows, edge_grounds):
    """one row of the new table, from the rows that merged into it."""
    rows = sorted(rows, key=lambda r: r["class_id"])
    members = []
    seen = set()
    for r in rows:
        for m in r["members"]:
            if m["unit"] in seen:
                continue
            seen.add(m["unit"])
            members.append(m)
    members.sort(key=lambda m: m["unit"])

    langs = []
    for m in members:
        if m["lang"] not in langs:
            langs.append(m["lang"])
    langs.sort()

    cores = []
    for r in rows:
        for c in r.get("canonical_core") or []:
            if c not in cores:
                cores.append(c)

    modes = []
    for r in rows:
        for entry in r.get("mode_inventory") or []:
            modes.append(entry)
    modes.sort(key=lambda e: e["unit"])

    div_inside = []
    for r in rows:
        for d in r.get("divergence_inside_the_class") or []:
            div_inside.append(d)
    div_border = []
    for r in rows:
        for d in r.get("divergence_at_the_border") or []:
            div_border.append(d)

    carries = False
    for r in rows:
        if r.get("carries_modes"):
            carries = True

    names = []
    for r in rows:
        w = r["evidence"].get("weakest_evidence")
        if w is not None:
            names.append(w)
    for g in edge_grounds:
        names.append(evidence_class(g))
    worst = weakest(names)

    counts = Counter()
    for r in rows:
        by = r["evidence"].get("member_pairs_by_class") or {}
        for k in by:
            counts[k] += by[k]
    for g in edge_grounds:
        counts[evidence_class(g)] += 1

    bridges_out = []
    bridges_in = []
    for r in rows:
        for b in r.get("bridges_out") or []:
            bridges_out.append(b)
        for b in r.get("bridges_in") or []:
            bridges_in.append(b)

    biggest = rows[0]
    for r in rows:
        if r["size"] > biggest["size"]:
            biggest = r

    present = sorted(set(langs))
    absent = []
    for entry in biggest.get("coverage", {}).get("languages_absent") or []:
        if entry["language"] in present:
            continue
        absent.append(entry)

    out = {}
    out["class_id"] = new_id
    out["class_key"] = biggest["class_key"]
    out["type_pair"] = biggest["type_pair"]
    out["result_type"] = biggest["result_type"]
    out["size"] = len(members)
    out["languages"] = langs
    out["members"] = members
    out["merged_from"] = [r["class_id"] for r in rows]
    out["canonical_core"] = cores
    out["canonical_core_from"] = biggest.get("canonical_core_from")
    out["distinct_core_texts"] = len(cores)
    out["mode_inventory"] = modes
    out["carries_modes"] = carries
    out["divergence_inside_the_class"] = div_inside
    out["divergence_at_the_border"] = div_border
    out["evidence"] = dict(
        member_pairs_by_class=dict(counts),
        weakest_evidence=worst,
        weakest_evidence_text=(EVIDENCE_TEXT.get(worst)
                               if worst is not None
                               else "no edge: this class has one member"),
        new_edge_grounds=sorted(set(edge_grounds)),
    )
    out["coverage"] = dict(languages_present=present,
                           languages_absent=absent)
    out["intention"] = None
    out["intention_candidates"] = biggest.get("intention_candidates")
    out["bridges_out"] = bridges_out
    out["bridges_in"] = bridges_in
    out["bridges_note"] = "carried from dominant_table3 under the old "\
                          "class ids; dominance.py was NOT re-run for "\
                          "this table"
    return out


def main():
    indir = os.path.dirname(os.path.abspath(__file__))
    outdir = indir
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--in":
            i = i + 1
            indir = args[i]
        elif args[i] == "--out":
            i = i + 1
            outdir = args[i]
        i = i + 1

    started = time.time()
    doc = load(indir)
    table = doc["table"]
    rows3 = table["rows"]
    log("classes read            %d" % len(rows3))

    by_id = {}
    unit_class = {}
    for r in rows3:
        by_id[r["class_id"]] = r
        for m in r["members"]:
            unit_class[m["unit"]] = r["class_id"]

    sets = Sets()
    for r in rows3:
        sets.add(r["class_id"])

    used = []
    refused = []
    grounds = {}
    for p in doc["verdicts5"]["pairs"]:
        if p["verdict"] != "MATCHED":
            continue
        ca = unit_class.get(p["left"])
        cb = unit_class.get(p["right"])
        if ca is None or cb is None:
            refused.append(dict(pair=p["pair_id"],
                                why="an endpoint is in no class of "
                                    "dominant_table3"))
            continue
        if class_key_of(by_id[ca]) != class_key_of(by_id[cb]):
            refused.append(dict(pair=p["pair_id"],
                                why="the two classes carry different "
                                    "class keys"))
            continue
        joined = sets.join(ca, cb)
        rec = dict(pair=p["pair_id"], left_class=ca, right_class=cb,
                   ground=p["ground"], joined_two_classes=joined)
        used.append(rec)
        root = sets.find(ca)
        if root not in grounds:
            grounds[root] = []
        grounds[root].append(p["ground"])

    log("MATCHED pairs offered   %d"
        % sum(1 for p in doc["verdicts5"]["pairs"]
              if p["verdict"] == "MATCHED"))
    log("edges used              %d" % len(used))
    log("edges refused           %d" % len(refused))

    groups = {}
    for r in rows3:
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
    # SMALLEST of the class ids that merged into it, so every id
    # bridges.json names still resolves, and the remap below only has
    # to move the absorbed ids.
    rows4 = []
    remap = {}
    for k in keys:
        new_id = min(x["class_id"] for x in groups[k])
        for x in groups[k]:
            remap[x["class_id"]] = new_id
        rows4.append(merged_row(new_id, groups[k],
                                final_grounds.get(k, [])))

    before_singletons = []
    for r in rows3:
        if r["size"] == 1:
            before_singletons.append(r["class_id"])
    after_singletons = []
    for r in rows4:
        if r["size"] == 1:
            after_singletons.append(r["class_id"])

    stats = {}
    stats["classes"] = len(rows4)
    stats["classes_before"] = len(rows3)
    stats["classes_size_1"] = len(after_singletons)
    stats["classes_size_1_before"] = len(before_singletons)
    stats["classes_spanning_2_or_more_languages"] = \
        sum(1 for r in rows4 if len(r["languages"]) >= 2)
    stats["classes_spanning_all_5_languages"] = \
        sum(1 for r in rows4 if len(r["languages"]) == 5)
    stats["weakest_evidence_distribution"] = dict(Counter(
        str(r["evidence"]["weakest_evidence"]) for r in rows4))
    stats["merged_rows"] = sum(1 for r in rows4
                               if len(r["merged_from"]) > 1)

    out = {}
    out["shape"] = "one row per equivalence class on one class key: "\
                   "operand types AND result type"
    out["class_definition"] = "the transitive closure of the edge set "\
                              "dominant_table3 used, plus the MATCHED "\
                              "pairs verdicts5 found under the third "\
                              "candidate rule"
    out["candidate_set"] = "machine-form evidence only: verdicts4's "\
                           "rows, verdicts3b's solver verdicts, "\
                           "canonical-byte identity, and verdicts5's "\
                           "singleton-against-same-class-key "\
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
                                     "carried from dominant_table3 "\
                                     "under the old class ids; "\
                                     "dominance.py was NOT re-run."
    out["languages"] = LANGS
    out["classes"] = len(rows4)
    out["new_edges_used"] = used
    out["new_edges_refused"] = refused
    out["stats"] = stats
    out["wall_seconds"] = round(time.time() - started, 2)
    out["rows"] = rows4

    path = os.path.join(outdir, "dominant_table4.json")
    fh = open(path, "w")
    json.dump(out, fh, indent=1)
    fh.write("\n")
    fh.close()
    log("wrote %s" % path)

    write_md(out, rows3, os.path.join(outdir, "dominant_table4.md"))
    log("wrote %s" % os.path.join(outdir, "dominant_table4.md"))

    rewrite_bridges(indir, outdir, remap)

    log("classes  %d -> %d" % (len(rows3), len(rows4)))
    log("size-1   %d -> %d" % (len(before_singletons),
                               len(after_singletons)))
    return 0


def rewrite_bridges(indir, outdir, remap):
    """bridges.json with its class ids moved onto the new classes.

    dominance.py was NOT re-run.  This only follows the two class ids
    a bridge names into the class each one now sits in.  A bridge
    whose two ends landed in ONE class is dropped and counted: the two
    forms it related are now the same class, so there is nothing left
    to bridge.  Every surviving bridge keeps its own proof text
    unchanged, and says which ids it was proved under.
    """
    path = os.path.join(indir, "bridges.json")
    if not os.path.exists(path):
        log("no bridges.json to remap")
        return
    doc = json.load(open(path))
    kept = []
    collapsed = []
    for b in doc["bridges"]:
        a = remap.get(b["dominant_class"], b["dominant_class"])
        c = remap.get(b["dominated_class"], b["dominated_class"])
        rec = dict(b)
        rec["proved_under_class_ids"] = dict(
            dominant=b["dominant_class"], dominated=b["dominated_class"])
        rec["dominant_class"] = a
        rec["dominated_class"] = c
        if a == c:
            collapsed.append(rec)
            continue
        kept.append(rec)
    out = dict(doc)
    out["bridges"] = kept
    out["bridge_count"] = len(kept)
    out["remap_note"] = "class ids follow dominant_table4; "\
                        "dominance.py was NOT re-run.  Bridges whose "\
                        "two ends became one class are moved to "\
                        "`bridges_collapsed_by_a_merge`."
    out["bridges_collapsed_by_a_merge"] = collapsed
    dest = os.path.join(outdir, "bridges4.json")
    fh = open(dest, "w")
    json.dump(out, fh, indent=1)
    fh.write("\n")
    fh.close()
    log("wrote %s (%d bridges kept, %d collapsed by a merge)"
        % (dest, len(kept), len(collapsed)))


def write_md(out, rows3, path):
    lines = []
    lines.append("# dominant_table4 -- classes after the third "
                 "candidate rule")
    lines.append("")
    lines.append("- classes: %d (was %d)"
                 % (out["stats"]["classes"],
                    out["stats"]["classes_before"]))
    lines.append("- classes of size 1: %d (was %d)"
                 % (out["stats"]["classes_size_1"],
                    out["stats"]["classes_size_1_before"]))
    lines.append("- rows that are a merge of two or more table-3 "
                 "classes: %d" % out["stats"]["merged_rows"])
    lines.append("- weakest evidence: %s"
                 % out["stats"]["weakest_evidence_distribution"])
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
