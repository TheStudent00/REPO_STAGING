#!/usr/bin/env python3
"""asg_fold_lane.py -- fold the compound-assignment units into the
class table.

Method, and it is the one dominant_table4.py and dominant_table6.py
already use: do NOT re-derive the plain classes.  Take the partition
dominant_table6.json holds, SEED each accepted assignment unit as a
class of its own, add the edges the matching stages found, and take
the transitive closure.  Closure is closure, so this is what a full
rebuild would compute for the union -- given the same edges.

THE EDGES USED, and where each comes from
------------------------------------------
  1. verdicts3.json from the staged run over the combined universe:
     every MATCHED pair with at least one assignment endpoint.  That
     is the pipeline's own verdict, from `verdicts.judge` plus the
     solver, over the cluster and connection candidate rules.
     verdicts3 pairs only ACROSS languages, by the dom_op
     construction rule.

  2. asg_relation.json: whole-unit BYTE identity and whole-unit
     anchored SEM identity between an assignment unit and a plain
     unit, INCLUDING same-language pairs.  This is not a new kind of
     evidence -- byte identity and sem identity are the two strongest
     grounds `verdicts.judge` itself returns, and the class table has
     always used them.  It is added because verdicts3's
     cross-language-only pairing cannot see a same-language pair, and
     an assignment unit's nearest plain relative is usually in its own
     language.

  A CONNECTION IS NOT AN EDGE.  A shared sub-term is a candidate
  rule -- a reason to ASK -- never evidence of equivalence.  Units
  related only by a connection are seeded and stay in their own class
  unless a verdict joined them.

Every edge is checked before use: both endpoints must carry the same
class key (operand types AND result type).  A failing edge is refused
and recorded, never silently dropped.

THE RESULT-TYPE SPELLING PROBLEM, FLAGGED AND NOT DECIDED
----------------------------------------------------------
The class key carries the result type, in the one vocabulary
result_vocab.py defines.  The c and c++ assignment probes spell their
result type with the stdint names -- `int32_t`, `int64_t`,
`uint64_t` -- and result_vocab.py does not name those spellings, so
it returns them as `unmapped:`, which by its own design can equal
nothing else.  Left alone, every c and c++ assignment unit would sit
in a class key of its own and could never join a plain class: 600 of
the 749 units, silently inert.

result_vocab.py IS NOT EDITED by this program.  Ontology and naming
are the owner's to decide.  Instead this program carries a PROPOSAL, named
here and marked on every row it touches, which the owner can ratify or
strike:

    int32_t -> i32,  int64_t -> i64,  uint64_t -> u64

Its evidence class is NOT the weak one: `int32_t` is defined by the C
standard to be exactly a 32-bit signed integer, and the assignment
probe returns `a`, whose declared type it is -- forced by the probe's
shape, as the asg manifest's own `result_rule_note` says.  But it is
still a vocabulary decision, so it is reported, and `--no-proposal`
runs without it so the cost of not ratifying is visible.

WHAT IS NOT COMPUTED FOR A SEEDED ROW, named so no reader is misled:
`canonical_core`, `mode_inventory`, `carries_modes`, the divergence
lists and the bridge lists.  Those come from core_modes.py and
dominance.py, which were NOT run for the assignment units.  A seeded
row carries them empty, with `not_computed` naming each one.

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
  asg_fold_lane.py --stage DIR [--out DIR] [--no-proposal]
"""

import json
import os
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dominant_table4 as T4                                  # noqa: E402
import result_vocab as RV                                     # noqa: E402

ASG_N_OFFSET = 100000

SOURCE_TABLE = "dominant_table6.json"

OUT_NAME = "dominant_table7.json"

PROPOSED = {
    "int32_t": "i32",
    "int64_t": "i64",
    "uint64_t": "u64",
}

PROPOSAL_NOTE = "result_vocab.py does not name the stdint spellings; "\
                "this row used the PROPOSED extension int32_t->i32, "\
                "int64_t->i64, uint64_t->u64, which the owner has NOT "\
                "ratified"

NOT_COMPUTED = ["canonical_core", "mode_inventory", "carries_modes",
                "divergence_inside_the_class",
                "divergence_at_the_border", "bridges_out", "bridges_in"]


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


def result_type_of(raw, use_proposal):
    """the result type in the common vocabulary, plus how it got
    there."""
    norm, note = RV.normalise(raw)
    if not str(norm).startswith("unmapped:"):
        return norm, "result_vocab.py", None
    if use_proposal and raw in PROPOSED:
        return PROPOSED[raw], "the PROPOSED stdint extension", \
            PROPOSAL_NOTE
    return norm, "result_vocab.py", note


def type_pair_of(meta):
    a = meta.get("lhs_rep")
    b = meta.get("rhs_rep")
    if b is None:
        return "%s,None" % a
    return "%s,%s" % (a, b)


def seed_row(class_id, unit, use_proposal):
    """one assignment unit as a class of its own."""
    meta = unit["meta"]
    raw = meta.get("result_type")
    norm, ground, note = result_type_of(raw, use_proposal)
    tp = type_pair_of(meta)

    member = {}
    member["unit"] = "%s/op_%s" % (unit["lang"], unit["n"])
    member["lang"] = unit["lang"]
    member["n"] = unit["n"]
    member["operator"] = meta.get("operator")
    member["type_pair"] = tp
    member["mode_count"] = 0
    member["result_type"] = norm
    member["result_type_as_the_language_spells_it"] = raw
    member["bucket"] = meta.get("bucket")
    member["asg_source_n"] = meta.get("asg_source_n")
    member["canonical_form"] = None
    member["canonicalisation_refused"] = None
    member["evictions"] = []

    row = {}
    row["class_id"] = class_id
    row["class_key"] = dict(operand_types=tp, result_type=norm,
                            note="no operator token takes part in "
                                 "this key")
    row["type_pair"] = tp
    row["result_type"] = norm
    row["result_type_ground"] = ground
    row["result_type_note"] = note
    row["size"] = 1
    row["languages"] = [unit["lang"]]
    row["members"] = [member]
    row["merged_from"] = [class_id]
    row["canonical_core"] = []
    row["canonical_core_from"] = None
    row["distinct_core_texts"] = 0
    row["mode_inventory"] = []
    row["carries_modes"] = False
    row["divergence_inside_the_class"] = []
    row["divergence_at_the_border"] = []
    row["evidence"] = dict(
        member_pairs_by_class={},
        weakest_evidence=None,
        weakest_evidence_text="no edge: this class has one member",
        new_edge_grounds=[])
    row["coverage"] = dict(languages_present=[unit["lang"]],
                           languages_absent=[])
    row["intention"] = None
    row["intention_candidates"] = None
    row["bridges_out"] = []
    row["bridges_in"] = []
    row["bridges_note"] = "dominance.py was NOT run for the "\
                          "assignment units"
    row["seeded_from"] = "the compound-assignment run"
    row["not_computed"] = NOT_COMPUTED
    return row


def collect_edges(stage, asg_units):
    """the edges, from the two sources named in the docstring."""
    edges = []

    path = os.path.join(stage, "verdicts3.json")
    doc = json.load(open(path))
    seen = set()
    for row in doc["rows"]:
        for p in row.get("pairs") or []:
            if p.get("verdict") != "MATCHED":
                continue
            left = p["left"]
            right = p["right"]
            if left not in asg_units and right not in asg_units:
                continue
            pid = "%s|%s" % (left, right)
            if pid in seen:
                continue
            seen.add(pid)
            edges.append(dict(left=left, right=right,
                              ground=p.get("ground"),
                              source="verdicts3 over the combined "
                                     "universe"))

    path = os.path.join(stage, "asg_relation.json")
    doc = json.load(open(path))
    for rec in doc["rows"]:
        left = rec["unit"]
        for comp in rec["byte_companions"]:
            right = "%s/op_%s" % (comp["lang"], comp["n"])
            pid = "%s|%s" % (left, right)
            if pid in seen:
                continue
            seen.add(pid)
            edges.append(dict(left=left, right=right,
                              ground="byte identity",
                              source="asg_relation, whole-unit byte "
                                     "identity"))
        for comp in rec["sem_companions"]:
            right = "%s/op_%s" % (comp["lang"], comp["n"])
            pid = "%s|%s" % (left, right)
            if pid in seen:
                continue
            seen.add(pid)
            edges.append(dict(left=left, right=right,
                              ground="sem identity (anchored)",
                              source="asg_relation, whole-unit "
                                     "anchored sem identity"))
    return edges


def main():
    stage = None
    outdir = HERE
    use_proposal = True
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--stage":
            i = i + 1
            stage = args[i]
        elif args[i] == "--out":
            i = i + 1
            outdir = args[i]
        elif args[i] == "--no-proposal":
            use_proposal = False
        i = i + 1

    if stage is None:
        log("!! REFUSING: --stage DIR is required")
        return 2

    started = time.time()
    log("stdint proposal applied %s" % use_proposal)

    table = json.load(open(os.path.join(HERE, SOURCE_TABLE)))
    rows6 = table["rows"]
    log("plain classes read      %d" % len(rows6))

    rel = json.load(open(os.path.join(stage, "asg_relation.json")))

    sys.path.insert(0, stage)

    # the assignment units, from the relation record (which loaded them
    # through verdicts.load_units, so the exclusion rules applied).
    asg_units = {}
    for rec in rel["rows"]:
        asg_units[rec["unit"]] = rec
    log("assignment units        %d" % len(asg_units))

    # seed rows need the unit meta; read it from the staged units.
    metas = {}
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        path = os.path.join(stage, "op_units_%s.json" % lang)
        doc = json.load(open(path))
        for n, p in doc["probes"].items():
            metas[("%s/op_%s" % (lang, n))] = p["meta"]

    seeds = []
    order = sorted(asg_units)
    for idx, label in enumerate(order):
        lang = label.split("/")[0]
        n = label.split("op_")[1]
        unit = dict(lang=lang, n=n, meta=metas[label])
        seeds.append(seed_row("A%04d" % idx, unit, use_proposal))
    log("classes seeded          %d" % len(seeds))

    unmapped = 0
    for r in seeds:
        if str(r["result_type"]).startswith("unmapped:"):
            unmapped = unmapped + 1
    log("seeded rows whose result type is unmapped %d" % unmapped)

    allrows = list(rows6) + seeds
    by_id = {}
    unit_class = {}
    for r in allrows:
        by_id[r["class_id"]] = r
        for m in r["members"]:
            unit_class[m["unit"]] = r["class_id"]

    sets = T4.Sets()
    for r in allrows:
        sets.add(r["class_id"])

    edges = collect_edges(stage, asg_units)
    log("edges offered           %d" % len(edges))

    used = []
    refused = []
    refused_why = Counter()
    for e in edges:
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

    groups = {}
    for r in allrows:
        root = sets.find(r["class_id"])
        if root not in groups:
            groups[root] = []
        groups[root].append(r)

    final_grounds = {}
    for rec in used:
        root = sets.find(rec["left_class"])
        if root not in final_grounds:
            final_grounds[root] = []
        final_grounds[root].append(rec["ground"])

    keys = sorted(groups.keys(),
                  key=lambda k: min(str(x["class_id"])
                                    for x in groups[k]))
    rows7 = []
    for k in keys:
        new_id = min(str(x["class_id"]) for x in groups[k])
        rows7.append(T4.merged_row(new_id, groups[k],
                                   final_grounds.get(k, [])))

    # how many assignment units ended up in a class that also holds a
    # plain unit?  That is the question this lap asked.
    joined_plain = 0
    alone = 0
    with_plain_same_lang = 0
    for r in rows7:
        has_asg = False
        has_plain = False
        asg_langs = set()
        plain_langs = set()
        for m in r["members"]:
            if m.get("bucket") == "assignment" or \
                    int(m["n"]) >= ASG_N_OFFSET:
                has_asg = True
                asg_langs.add(m["lang"])
            else:
                has_plain = True
                plain_langs.add(m["lang"])
        if not has_asg:
            continue
        n_asg = 0
        for m in r["members"]:
            if m.get("bucket") == "assignment" or \
                    int(m["n"]) >= ASG_N_OFFSET:
                n_asg = n_asg + 1
        if has_plain:
            joined_plain = joined_plain + n_asg
            if asg_langs & plain_langs:
                with_plain_same_lang = with_plain_same_lang + n_asg
        else:
            alone = alone + n_asg

    log("")
    log("== the fold")
    log("   assignment units in a class that also holds a plain unit "
        "%d" % joined_plain)
    log("      of those, the class holds a plain unit of the SAME "
        "language %d" % with_plain_same_lang)
    log("   assignment units in a class with no plain unit %d" % alone)

    stats = {}
    stats["classes"] = len(rows7)
    stats["plain_classes_before"] = len(rows6)
    stats["classes_seeded"] = len(seeds)
    stats["classes_size_1"] = sum(1 for r in rows7 if r["size"] == 1)
    stats["assignment_units_with_a_plain_unit_in_their_class"] = \
        joined_plain
    stats["assignment_units_whose_class_holds_a_same_language_plain_"
          "unit"] = with_plain_same_lang
    stats["assignment_units_alone_of_their_kind"] = alone
    stats["seeded_rows_with_an_unmapped_result_type"] = unmapped
    stats["weakest_evidence_distribution"] = dict(Counter(
        str(r["evidence"]["weakest_evidence"]) for r in rows7))

    out = {}
    out["shape"] = "one row per equivalence class on one class key: "\
                   "operand types AND result type"
    out["class_definition"] = "the partition %s holds, plus one "\
                              "seeded class per accepted "\
                              "compound-assignment unit, plus the "\
                              "MATCHED edges the staged matching "\
                              "stages found, closed transitively" \
                              % SOURCE_TABLE
    out["candidate_set"] = "machine-form evidence only: the carried "\
                           "edge set, verdicts3 over the combined "\
                           "universe, and whole-unit byte / anchored "\
                           "sem identity.  No operator token takes "\
                           "part in any key, grouping, pairing or "\
                           "selection here."
    out["spelling"] = "the operator token appears once per unit, as "\
                      "the display label `operator` on a member "\
                      "object beside `lang` and `n`."
    out["a_connection_is_not_an_edge"] = "a shared sub-term is a "\
        "candidate rule, a reason to ask; it is never evidence of "\
        "equivalence, and no class here was formed by one."
    out["result_type_proposal"] = dict(
        applied=use_proposal,
        mapping=PROPOSED,
        status="PROPOSED, NOT RATIFIED.  result_vocab.py was not "
               "edited.  the owner decides ontology and naming.",
        why="result_vocab.py does not name the stdint spellings the c "
            "and c++ assignment probes use, so without this they are "
            "`unmapped:` and can equal nothing else.")
    out["what_was_not_computed_for_a_seeded_row"] = NOT_COMPUTED
    out["source_table"] = SOURCE_TABLE
    out["languages"] = T4.LANGS
    out["classes"] = len(rows7)
    out["new_edges_used"] = used
    out["new_edges_refused"] = refused
    out["stats"] = stats
    out["wall_seconds"] = round(time.time() - started, 2)
    out["rows"] = rows7

    path = os.path.join(outdir, OUT_NAME)
    fh = open(path, "w")
    json.dump(out, fh, indent=1)
    fh.write("\n")
    fh.close()
    log("wrote %s" % path)

    write_md(out, os.path.join(outdir,
                               OUT_NAME.replace(".json", ".md")))
    log("classes  %d + %d seeded -> %d"
        % (len(rows6), len(seeds), len(rows7)))
    return 0


def write_md(out, path):
    lines = []
    lines.append("# dominant_table7 -- the compound-assignment units "
                 "folded in")
    lines.append("")
    s = out["stats"]
    lines.append("- source table: %s" % out["source_table"])
    lines.append("- plain classes carried in: %d"
                 % s["plain_classes_before"])
    lines.append("- classes seeded, one per assignment unit: %d"
                 % s["classes_seeded"])
    lines.append("- classes after closure: %d" % s["classes"])
    lines.append("")
    lines.append("## did an assignment unit land with a plain unit?")
    lines.append("")
    lines.append("| outcome | assignment units |")
    lines.append("|---|---|")
    lines.append("| in a class that also holds a plain unit | %d |"
                 % s["assignment_units_with_a_plain_unit_in_their_class"])
    lines.append("| of those, a plain unit of the SAME language | %d |"
                 % s["assignment_units_whose_class_holds_a_same_"
                     "language_plain_unit"])
    lines.append("| in a class with no plain unit | %d |"
                 % s["assignment_units_alone_of_their_kind"])
    lines.append("")
    lines.append("## the result-type proposal")
    lines.append("")
    lines.append("%s" % out["result_type_proposal"]["status"])
    lines.append("")
    lines.append("- mapping: %s" % out["result_type_proposal"]["mapping"])
    lines.append("- applied in this run: %s"
                 % out["result_type_proposal"]["applied"])
    lines.append("- seeded rows still unmapped: %d"
                 % s["seeded_rows_with_an_unmapped_result_type"])
    lines.append("")
    fh = open(path, "w")
    fh.write("\n".join(lines))
    fh.close()


if __name__ == "__main__":
    sys.exit(main())
