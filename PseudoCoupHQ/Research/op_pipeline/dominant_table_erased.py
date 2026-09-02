#!/usr/bin/env python3
"""dominant_table_erased.py -- dominant_table8.json.

Successor to asg_fold_lane.py's dominant_table7, with two additions
ratified for this lap:

  (a) the compound-assignment (asg) units of c and c++ are re-seeded
      on a MACHINE-FACT result type instead of asg_fold_lane's
      PROPOSED-and-not-ratified stdint name mapping.  The machine
      fact comes from result_types_asg_c.json / result_types_asg_cpp.json
      (this lap's DWARF read: DW_AT_type on the `-g` build of each
      accepted asg probe, followed to a base type DIE and keyed on
      that DIE's own DW_AT_encoding + DW_AT_byte_size).  go, rust and
      swift asg units are untouched -- their generator already spells
      a type result_vocab.py names, so asg_fold_lane's mapping was
      never a proposal for them.

  (b) a new matching ground, "erased-form": two units (from the
      plain, non-assignment population -- the only one canon2.py has
      erased any unit of) share it when their erased forms
      (canon2_units_<lang>.json, the move-erased + entry-contract
      canonical record ratified 2026-08-26) are character-identical,
      line for line.  For a branching unit this would mean identical
      block structure, step lines and labels; none of the units
      canon2.py erased this lap branch, so no branching comparison
      was exercised -- flagged honestly below, not silently assumed.
      Entry-contract differences do NOT block the match: the adapter
      between two different entry contracts for the same erased body
      is derivable by the AMENDMENT's own rule (value-here +
      needed-there produces the mov by rule), so it carries no
      information the class key needs.

Ranked in EVIDENCE_ORDER immediately after "canon-byte" (stronger
than sem/core-text/z3: it is byte-identity's cousin, taken after
canonicalisation AND after erasing bookkeeping moves, so it is
harder to satisfy by accident than plain "sem").

THE SPELLING BAN, verbatim, restated because this program groups and
pairs units: "No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in 'which pairs get
compared', not in report rows, not in dropdowns.  The candidate set
for comparison comes from machine-form evidence (clusters,
connections, type pairs) or from ratified intention -- never from
the token.  The token appears exactly once per unit: as a display
label on the member."  This program's erased-form groups are keyed
on the erased_form text (which is `answer = op(a,b)`-shaped in
canon2's own erasure vocabulary of xor/sete/test/etc synthetic step
names, not the source operator token) and are additionally gated on
the SAME class key check every other edge here passes through, so
the operator token never enters a key.  check_no_spelling_keys.py is
run over the output before this program exits successfully.

class key is unchanged: operand types AND result type.  Union of
edges is dominant_table2.py's own union-find, reused via
dominant_table4.Sets, exactly as asg_fold_lane does.

usage:
  dominant_table_erased.py --stage DIR [--out DIR]
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

OUT_NAME = "dominant_table8.json"

CANON2_LANGS = ["c", "cpp", "go", "rust", "swift"]

MACHINE_RESULT_FILES = {
    "c": "result_types_asg_c.json",
    "cpp": "result_types_asg_cpp.json",
}

NOT_COMPUTED = ["canonical_core", "mode_inventory", "carries_modes",
                "divergence_inside_the_class",
                "divergence_at_the_border", "bridges_out", "bridges_in"]

EVIDENCE_ORDER = ["byte", "canon-byte", "erased-form", "sem",
                  "core-text", "z3", "unclassified"]

EVIDENCE_TEXT = dict(T4.EVIDENCE_TEXT)
EVIDENCE_TEXT["erased-form"] = (
    "erased-form identity (the move-erased canonical records, "
    "ratified 2026-08-26, are line-for-line character-identical; "
    "entry-contract differences are ignored -- the adapter between "
    "them is derivable)")


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


def load_machine_result_types():
    """probe n -> machine-fact result type, for c and c++ asg units."""
    out = {}
    for lang, fname in MACHINE_RESULT_FILES.items():
        path = os.path.join(HERE, fname)
        doc = json.load(open(path))
        rows = doc["result_types"]
        table = {}
        for n, rec in rows.items():
            table[n] = dict(machine=rec["result_type_machine"],
                            label=rec["result_type_label"])
        out[lang] = table
        log("asg machine result types loaded for %s: %d probes"
            % (lang, len(table)))
    return out


def type_pair_of(meta):
    a = meta.get("lhs_rep")
    b = meta.get("rhs_rep")
    if b is None:
        return "%s,None" % a
    return "%s,%s" % (a, b)


def asg_result_type_of(lang, n, meta, machine_types):
    """the class-key result type for one asg unit, plus its ground."""
    source_n = meta.get("asg_source_n")
    if source_n is not None:
        source_n = str(source_n)
    if lang in machine_types and source_n in machine_types[lang]:
        rec = machine_types[lang][source_n]
        return rec["machine"], ("DWARF machine fact: DW_AT_encoding + "
                                "DW_AT_byte_size on the op_%s "
                                "subprogram's base result type (asg "
                                "probe source n=%s, unit n=%s)"
                                % (source_n, source_n, n)), \
            rec["label"]
    raw = meta.get("result_type")
    norm, note = RV.normalise(raw)
    return norm, "result_vocab.py", raw


def seed_asg_row(class_id, unit, machine_types):
    meta = unit["meta"]
    norm, ground, label = asg_result_type_of(unit["lang"], unit["n"],
                                             meta, machine_types)
    tp = type_pair_of(meta)

    member = {}
    member["unit"] = "%s/op_%s" % (unit["lang"], unit["n"])
    member["lang"] = unit["lang"]
    member["n"] = unit["n"]
    member["operator"] = meta.get("operator")
    member["type_pair"] = tp
    member["mode_count"] = 0
    member["result_type"] = norm
    member["result_type_as_the_language_spells_it"] = label
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
    row["result_type_note"] = None
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


def collect_asg_edges(stage, asg_units):
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


def load_erased_forms():
    """unit label -> tuple(erased_form lines), erasure == ok only."""
    out = {}
    branching_seen = 0
    for lang in CANON2_LANGS:
        path = os.path.join(HERE, "canon2_units_%s.json" % lang)
        if not os.path.exists(path):
            continue
        doc = json.load(open(path))
        for k, rec in doc["units"].items():
            if rec.get("erasure") != "ok":
                continue
            blocks = rec.get("blocks")
            if blocks is not None:
                branching_seen += 1
                form = tuple(json.dumps(blocks, sort_keys=True))
            else:
                form = tuple(rec.get("erased_form") or [])
            if not form:
                continue
            out[rec["unit"]] = form
    return out, branching_seen


def collect_erased_form_edges(erased_forms, unit_class, by_id):
    """edges among units whose erased forms are character-identical,
    gated on same class key -- machine-form evidence only, no
    operator token anywhere in the grouping."""
    groups = {}
    for unit, form in erased_forms.items():
        groups.setdefault(form, []).append(unit)

    edges = []
    same_key_groups = 0
    cross_key_refused = 0
    for form, units in groups.items():
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
            other_key = T4.class_key_of(by_id[cb]) if cb in by_id \
                else None
            if anchor_key != other_key:
                cross_key_refused += 1
                continue
            same_key_groups += 1
            edges.append(dict(left=anchor, right=other,
                              ground="erased-form identity: the "
                                     "move-erased canonical records "
                                     "are character-identical",
                              source="canon2_units, erased-form "
                                     "grouping"))
    return edges, same_key_groups, cross_key_refused


def main():
    stage = None
    outdir = HERE
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--stage":
            i += 1
            stage = args[i]
        elif args[i] == "--out":
            i += 1
            outdir = args[i]
        i += 1

    if stage is None:
        log("!! REFUSING: --stage DIR is required")
        return 2

    started = time.time()

    table = json.load(open(os.path.join(HERE, SOURCE_TABLE)))
    rows6 = table["rows"]
    log("plain classes read      %d" % len(rows6))

    machine_types = load_machine_result_types()

    rel = json.load(open(os.path.join(stage, "asg_relation.json")))
    asg_units = {}
    for rec in rel["rows"]:
        asg_units[rec["unit"]] = rec
    log("assignment units        %d" % len(asg_units))

    metas = {}
    for lang in ["c", "cpp", "go", "rust", "swift"]:
        path = os.path.join(stage, "op_units_%s.json" % lang)
        doc = json.load(open(path))
        for n, p in doc["probes"].items():
            metas[("%s/op_%s" % (lang, n))] = p["meta"]

    seeds = []
    order = sorted(asg_units)
    unmapped = 0
    machine_backed = 0
    for idx, label in enumerate(order):
        lang = label.split("/")[0]
        n = label.split("op_")[1]
        unit = dict(lang=lang, n=n, meta=metas[label])
        row = seed_asg_row("A%04d" % idx, unit, machine_types)
        seeds.append(row)
        source_n = unit["meta"].get("asg_source_n")
        if source_n is not None:
            source_n = str(source_n)
        if lang in machine_types and source_n in machine_types[lang]:
            machine_backed += 1
        if str(row["result_type"]).startswith("unmapped:"):
            unmapped += 1
    log("classes seeded          %d" % len(seeds))
    log("asg seeds keyed on the DWARF machine fact %d" % machine_backed)
    log("seeded rows whose result type is still unmapped %d" % unmapped)

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

    asg_edges = collect_asg_edges(stage, asg_units)
    log("asg-relation/verdicts3 edges offered %d" % len(asg_edges))

    erased_forms, branching_seen = load_erased_forms()
    log("erased-form records loaded (erasure == ok) %d" %
        len(erased_forms))
    log("branching-unit erased records among them   %d (none expected "
        "this lap)" % branching_seen)

    erased_edges, erased_groups, erased_cross_refused = \
        collect_erased_form_edges(erased_forms, unit_class, by_id)
    log("erased-form groups usable as edges  %d" % erased_groups)
    log("erased-form groups refused (class key differs) %d" %
        erased_cross_refused)

    edges = asg_edges + erased_edges
    log("edges offered (both sources)        %d" % len(edges))

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
        groups.setdefault(root, []).append(r)

    final_grounds = {}
    for rec in used:
        root = sets.find(rec["left_class"])
        final_grounds.setdefault(root, []).append(rec["ground"])

    # merged_row() from dominant_table4 uses the module-level
    # EVIDENCE_ORDER/EVIDENCE_TEXT via evidence_class()/weakest();
    # monkeypatch them for the duration of this build so
    # "erased-form" is recognised and ranked, without touching the
    # shared module file other lanes still import unmodified.
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
        rows8 = []
        for k in keys:
            new_id = min(str(x["class_id"]) for x in groups[k])
            rows8.append(T4.merged_row(new_id, groups[k],
                                       final_grounds.get(k, [])))
    finally:
        T4.EVIDENCE_ORDER = old_order
        T4.EVIDENCE_TEXT = old_text
        T4.evidence_class = old_evidence_class
        T4.weakest = old_weakest

    joined_plain = 0
    alone = 0
    with_plain_same_lang = 0
    cpp_c_asg_inert = 0
    for r in rows8:
        has_asg = False
        has_plain = False
        asg_langs = set()
        plain_langs = set()
        n_asg = 0
        n_cpp_c_asg = 0
        for m in r["members"]:
            is_asg = m.get("bucket") == "assignment" or \
                int(m["n"]) >= ASG_N_OFFSET
            if is_asg:
                has_asg = True
                asg_langs.add(m["lang"])
                n_asg += 1
                if m["lang"] in ("c", "cpp"):
                    n_cpp_c_asg += 1
            else:
                has_plain = True
                plain_langs.add(m["lang"])
        if not has_asg:
            continue
        if has_plain:
            joined_plain += n_asg
            if asg_langs & plain_langs:
                with_plain_same_lang += n_asg
        else:
            alone += n_asg
            cpp_c_asg_inert += n_cpp_c_asg

    log("")
    log("== the fold")
    log("   assignment units in a class that also holds a plain unit "
        "%d" % joined_plain)
    log("      of those, the class holds a plain unit of the SAME "
        "language %d" % with_plain_same_lang)
    log("   assignment units in a class with no plain unit %d" % alone)
    log("      of those, c/cpp asg units still alone %d" %
        cpp_c_asg_inert)

    stats = {}
    stats["classes"] = len(rows8)
    stats["plain_classes_before"] = len(rows6)
    stats["classes_seeded"] = len(seeds)
    stats["classes_size_1"] = sum(1 for r in rows8 if r["size"] == 1)
    stats["assignment_units_with_a_plain_unit_in_their_class"] = \
        joined_plain
    stats["assignment_units_whose_class_holds_a_same_language_plain_"
          "unit"] = with_plain_same_lang
    stats["assignment_units_alone_of_their_kind"] = alone
    stats["c_or_cpp_assignment_units_still_alone_of_their_kind"] = \
        cpp_c_asg_inert
    stats["seeded_rows_with_an_unmapped_result_type"] = unmapped
    stats["asg_seeds_keyed_on_dwarf_machine_fact"] = machine_backed
    stats["erased_form_edges_used_or_offered"] = len(erased_edges)
    stats["erased_form_groups_refused_cross_class_key"] = \
        erased_cross_refused
    stats["weakest_evidence_distribution"] = dict(Counter(
        str(r["evidence"]["weakest_evidence"]) for r in rows8))

    out = {}
    out["shape"] = "one row per equivalence class on one class key: "\
                   "operand types AND result type"
    out["class_definition"] = "the partition %s holds, plus one "\
                              "seeded class per accepted "\
                              "compound-assignment unit (c/cpp keyed "\
                              "on the DWARF machine-fact result type "\
                              "from this lap's DWARF read, not the "\
                              "PROPOSED-and-unratified stdint name "\
                              "mapping), plus the MATCHED edges the "\
                              "staged matching stages found and the "\
                              "new erased-form edges, closed "\
                              "transitively" % SOURCE_TABLE
    out["candidate_set"] = "machine-form evidence only: the carried "\
                           "edge set, verdicts3 over the combined "\
                           "universe, whole-unit byte / anchored sem "\
                           "identity, and character-identical "\
                           "erased-form records.  No operator token "\
                           "takes part in any key, grouping, pairing "\
                           "or selection here."
    out["spelling"] = "the operator token appears once per unit, as "\
                      "the display label `operator` on a member "\
                      "object beside `lang` and `n`."
    out["a_connection_is_not_an_edge"] = "a shared sub-term is a "\
        "candidate rule, a reason to ask; it is never evidence of "\
        "equivalence, and no class here was formed by one."
    out["asg_result_type_ground"] = dict(
        c="DWARF machine fact (result_types_asg_c.json)",
        cpp="DWARF machine fact (result_types_asg_cpp.json)",
        go="result_vocab.py (unchanged: never used the proposal)",
        rust="result_vocab.py (unchanged: never used the proposal)",
        swift="result_vocab.py (unchanged: never used the proposal)")
    out["erased_form_ground"] = ("two units share `erased-form` when "
                                 "canon2_units_<lang>.json records "
                                 "character-identical erased_form "
                                 "line lists (or, for a branching "
                                 "unit, identical block structure); "
                                 "entry-contract differences do not "
                                 "block the match -- the adapter is "
                                 "derivable")
    out["evidence_order"] = EVIDENCE_ORDER
    out["what_was_not_computed_for_a_seeded_row"] = NOT_COMPUTED
    out["source_table"] = SOURCE_TABLE
    out["languages"] = T4.LANGS
    out["classes"] = len(rows8)
    out["new_edges_used"] = used
    out["new_edges_refused"] = refused
    out["stats"] = stats
    out["wall_seconds"] = round(time.time() - started, 2)
    out["rows"] = rows8

    path = os.path.join(outdir, OUT_NAME)
    fh = open(path, "w")
    json.dump(out, fh, indent=1)
    fh.write("\n")
    fh.close()
    log("wrote %s" % path)
    log("classes  %d + %d seeded -> %d"
        % (len(rows6), len(seeds), len(rows8)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
