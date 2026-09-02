#!/usr/bin/env python3
"""dominant_table2.py -- step 8 rebuilt under the four rulings of
2026-08-25.

It is `dominant_table.py` with four changes, and it imports that file
rather than copying it, so the parts that did not change cannot drift.
`dominant_table.json` and `table_digest.md` are RECORDS and are not
touched; this writes `dominant_table2.json`, `dominant_table2.md` and
`table_digest2.md`.

What changed
------------
1. THE CANONICAL RUNNABLE FORM.  Every unit now also carries the
   canonical text its registers were renamed into, and the bytes an
   assembler produced from that text (`canon_units_*.json`,
   `canon_roundtrip.json`).

2. TRACED-VARIABLES-PRIORITY.  Units the canonicaliser refused carry
   their refusal on the member record and take part in no canonical-byte
   edge.  They keep whatever edges the earlier passes gave them.

3. RESULT TYPE JOINS THE CLASS KEY.  A row keys on (operand types,
   RESULT type).  An edge between two units whose result types differ is
   not used, exactly as an edge across two operand type pairs is not
   used.  This is what kills the empty-core false merges: two units can
   be the same bytes (`ret` alone) and still be different classes,
   because what they hand back is not the same kind of thing.

4. Z3-PROVED EQUALITY IS CLASS-FORMING.  The total-equality edges now
   include every pair verdicts3b marked MATCHED on a z3 ground, and a
   class whose weakest edge is one of those says
   `z3-proved (deduction; rests on lifter + solver)`.
   Canonical-byte identity is also an edge, and it ranks with byte
   identity: it is the same machine bytes after a rename that only moved
   values between registers.

THE SPELLING BAN.  No operator token takes part in any key, grouping,
pairing, candidate selection or comparison scope here.  Classes come
from machine-form edges; the token is written once per unit, as
`operator`, on a unit object.  Run check_no_spelling_keys.py on the
output.

usage:
  dominant_table2.py [--in DIR] [--out DIR]
"""

import json
import os
import sys
import time

import dominant_table as base
import result_vocab

HERE = os.path.dirname(os.path.abspath(__file__))

LANGS = base.LANGS

TOTAL_EQUAL = base.TOTAL_EQUAL

EVIDENCE_ORDER = ["byte", "canon-byte", "sem", "core-text", "z3",
                  "unclassified"]

EVIDENCE_TEXT = {
    "byte": "byte identity (the two units are the same machine bytes)",
    "canon-byte": "canonical byte identity (after the rename into the "
                  "canonical runnable form, the two units assemble to "
                  "the same machine bytes)",
    "sem": "anchored sem identity (the two lifted forms are identical)",
    "core-text": "core-text identity: verdicts4's own column found the "
                 "two normal-path cores textually equal and their mode "
                 "sets equal, and verdicts3b recorded no identity "
                 "ground for the pair",
    "z3": "z3-proved (deduction; rests on lifter + solver)",
    "unclassified": "ground not recognised by this builder",
}


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


# ---------------------------------------------------------------- io

def load(indir):
    doc = base.load(indir)
    doc["canon"] = {}
    for lang in LANGS:
        name = "canon_units_%s.json" % lang
        path = os.path.join(indir, name)
        doc["canon"][lang] = json.load(open(path))
    path = os.path.join(indir, "canon_roundtrip.json")
    doc["roundtrip"] = json.load(open(path))
    doc["recovered_result_types"] = {}
    for lang in LANGS:
        path = os.path.join(indir, "result_types_%s.json" % lang)
        if not os.path.exists(path):
            continue
        doc["recovered_result_types"][lang] = json.load(open(path))
    return doc


# ------------------------------------------------------------- units

def result_type_of(lang, n, unit, doc):
    """-> (normal form, raw spelling, where it came from, note)."""
    recovered = doc["recovered_result_types"].get(lang)
    if recovered is not None:
        raw = recovered["result_types"].get(str(n))
        if raw is not None:
            norm, note = result_vocab.normalise(raw)
            where = "the tool's own testimony: DW_AT_type on the "\
                    "subprogram of a debug build of the recorded probe "\
                    "source"
            return norm, raw, where, note
    raw = unit.get("meta", {}).get("result_type")
    norm, note = result_vocab.normalise(raw)
    where = "recorded by the probe generator at generation time"
    if raw is None:
        where = "not recorded anywhere this builder reads"
    return norm, raw, where, note


def unit_index(doc):
    """every measured unit, keyed `lang/op_n`, with its result type and
    its canonical form attached."""
    out = {}
    for lang in LANGS:
        canon = doc["canon"][lang]["units"]
        units = doc["core_modes"][lang]["units"]
        for n, u in units.items():
            uid = "%s/op_%s" % (lang, n)
            rec = dict(u)
            norm, raw, where, note = result_type_of(lang, n, u, doc)
            rec["result_type"] = norm
            rec["result_type_as_the_language_spells_it"] = raw
            rec["result_type_ground"] = where
            rec["result_type_note"] = note
            c = canon.get(str(n))
            rec["canon_ok"] = False
            rec["canon_text"] = None
            rec["canon_refused"] = None
            rec["evictions"] = []
            if c is not None:
                rec["canon_ok"] = c.get("canon_ok", False)
                rec["canon_text"] = c.get("canon_text")
                rec["canon_refused"] = c.get("canon_refused")
                rec["evictions"] = c.get("evictions", [])
            trip = doc["roundtrip"]["units"].get(uid)
            rec["canon_bytes"] = None
            if trip is not None:
                rec["canon_bytes"] = trip.get("canon_bytes")
            out[uid] = rec
    return out


def class_key_of(unit):
    """the class key: operand types AND result type.  No operator token
    takes part in it."""
    return (unit["type_pair"], unit["result_type"])


# ------------------------------------------------------------- edges

def z3_edges(doc, units):
    """ruling 4: every pair verdicts3b marked MATCHED on a z3 ground."""
    out = {}
    for row in doc["verdicts3b"]["rows"]:
        for p in row.get("pairs", []):
            if p.get("verdict") != "MATCHED":
                continue
            ground = p.get("ground")
            if ground is None:
                continue
            if not ground.startswith("z3"):
                continue
            left = p["left"]
            right = p["right"]
            if left not in units:
                continue
            if right not in units:
                continue
            out[base.pair_key(left, right)] = "z3"
    return out


def canon_byte_edges(units):
    """units whose CANONICAL bytes are identical.  Candidates come from
    the bytes themselves, never from a token."""
    buckets = {}
    for uid in units:
        b = units[uid].get("canon_bytes")
        if not b:
            continue
        key = " ".join(b)
        if key not in buckets:
            buckets[key] = []
        buckets[key].append(uid)
    out = {}
    for key in buckets:
        group = sorted(buckets[key])
        if len(group) < 2:
            continue
        first = group[0]
        for other in group[1:]:
            out[base.pair_key(first, other)] = "canon-byte"
    return out


def build_classes(doc, units):
    """union the total-equality edges, the z3-proved MATCHED edges and
    the canonical-byte edges.  An edge is used only when its two units
    carry the SAME class key -- the same operand types and the same
    result type."""
    uf = base.UnionFind()
    edges = {}
    skipped_type_pair = 0
    skipped_result_type = 0
    counts = {}
    for uid in units:
        uf.add(uid)
    proposals = {}
    for row in doc["verdicts4"]["rows"]:
        for p in row["pairs"]:
            if p["column"] != TOTAL_EQUAL:
                continue
            left = p["left"]
            right = p["right"]
            if left not in units:
                continue
            if right not in units:
                continue
            proposals[base.pair_key(left, right)] = "verdicts4"
    for key, why in z3_edges(doc, units).items():
        if key in proposals:
            continue
        proposals[key] = "z3"
    for key, why in canon_byte_edges(units).items():
        if key in proposals:
            continue
        proposals[key] = "canon-byte"
    for key in sorted(proposals.keys()):
        left = key[0]
        right = key[1]
        if units[left]["type_pair"] != units[right]["type_pair"]:
            skipped_type_pair = skipped_type_pair + 1
            continue
        if units[left]["result_type"] != units[right]["result_type"]:
            skipped_result_type = skipped_result_type + 1
            continue
        uf.union(left, right)
        edges[key] = proposals[key]
        name = proposals[key]
        counts[name] = counts.get(name, 0) + 1
    buckets = {}
    for uid in units:
        root = uf.find(uid)
        if root not in buckets:
            buckets[root] = []
        buckets[root].append(uid)
    stats = {}
    stats["edges_skipped_because_operand_types_differ"] = \
        skipped_type_pair
    stats["edges_skipped_because_result_types_differ"] = \
        skipped_result_type
    stats["edges_by_source"] = counts
    return buckets, edges, stats


# ------------------------------------------------------------ classes

def close_over(units, proposals, use_result_type):
    """how many classes a given set of proposed edges makes."""
    uf = base.UnionFind()
    for uid in units:
        uf.add(uid)
    used = 0
    for key in sorted(proposals.keys()):
        left = key[0]
        right = key[1]
        if units[left]["type_pair"] != units[right]["type_pair"]:
            continue
        if use_result_type:
            if units[left]["result_type"] != units[right]["result_type"]:
                continue
        uf.union(left, right)
        used = used + 1
    roots = {}
    for uid in units:
        roots[uf.find(uid)] = True
    return len(roots), used


def movement(doc, units):
    """WHERE the class count moved, one ruling at a time.  Each step
    adds exactly one change to the step before it, so the difference
    between two steps is that change and nothing else."""
    verdicts4 = {}
    for row in doc["verdicts4"]["rows"]:
        for p in row["pairs"]:
            if p["column"] != TOTAL_EQUAL:
                continue
            left = p["left"]
            right = p["right"]
            if left not in units:
                continue
            if right not in units:
                continue
            verdicts4[base.pair_key(left, right)] = "verdicts4"
    zed = z3_edges(doc, units)
    canon = canon_byte_edges(units)

    steps = []
    a, a_used = close_over(units, verdicts4, False)
    steps.append(("as the table stood: verdicts4's total-equality "
                  "edges, keyed on operand types alone", a, a_used))
    b, b_used = close_over(units, verdicts4, True)
    steps.append(("ruling 3: the result type joins the class key", b,
                  b_used))
    withz3 = dict(verdicts4)
    added_z3 = 0
    for key in zed:
        if key in withz3:
            continue
        withz3[key] = "z3"
        added_z3 = added_z3 + 1
    c, c_used = close_over(units, withz3, True)
    steps.append(("ruling 4: z3-proved MATCHED pairs become "
                  "class-forming edges", c, c_used))
    withcanon = dict(withz3)
    added_canon = 0
    for key in canon:
        if key in withcanon:
            continue
        withcanon[key] = "canon-byte"
        added_canon = added_canon + 1
    d, d_used = close_over(units, withcanon, True)
    steps.append(("rulings 1 and 2: canonical-byte identity becomes an "
                  "edge", d, d_used))

    out = {}
    out["steps"] = []
    before = None
    for name, count, used in steps:
        rec = {}
        rec["step"] = name
        rec["classes"] = count
        rec["edges_used"] = used
        if before is not None:
            rec["change"] = count - before
        before = count
        out["steps"].append(rec)
    out["z3_pairs_verdicts3b_marked_MATCHED"] = len(zed)
    out["z3_pairs_that_were_not_already_a_verdicts4_edge"] = added_z3
    out["canonical_byte_pairs"] = len(canon)
    out["canonical_byte_pairs_that_were_not_already_an_edge"] = \
        added_canon
    out["why_new_edges_did_not_all_land"] = why_not(units, zed, canon,
                                                    verdicts4)
    return out


def why_not(units, zed, canon, verdicts4):
    """a new edge can fail to change anything for three reasons: the
    pair was already an edge, the two units carry different operand
    types, or -- ruling 3 -- they carry different result types."""
    out = {}
    for name, proposals in (("z3", zed), ("canonical bytes", canon)):
        rec = {}
        rec["proposed"] = len(proposals)
        rec["already_an_edge"] = 0
        rec["operand_types_differ"] = 0
        rec["result_types_differ"] = 0
        rec["used"] = 0
        for key in proposals:
            if key in verdicts4:
                rec["already_an_edge"] = rec["already_an_edge"] + 1
                continue
            left = key[0]
            right = key[1]
            if units[left]["type_pair"] != units[right]["type_pair"]:
                rec["operand_types_differ"] = \
                    rec["operand_types_differ"] + 1
                continue
            if units[left]["result_type"] != units[right]["result_type"]:
                rec["result_types_differ"] = \
                    rec["result_types_differ"] + 1
                continue
            rec["used"] = rec["used"] + 1
        out[name] = rec
    return out


def member_record(uid, unit):
    rec = base.member_record(uid, unit)
    rec["result_type"] = unit["result_type"]
    rec["result_type_as_the_language_spells_it"] = \
        unit["result_type_as_the_language_spells_it"]
    rec["canonical_form"] = unit["canon_text"]
    rec["canonicalisation_refused"] = unit["canon_refused"]
    rec["evictions"] = unit["evictions"]
    return rec


def one_class(cid, uids, units, edges, grounds, borders, corpus,
              class_of):
    row = base.one_class(cid, uids, units, edges, grounds, borders,
                         corpus, class_of)
    uids = sorted(uids)
    members = []
    for uid in uids:
        members.append(member_record(uid, units[uid]))
    row["members"] = members
    row["result_type"] = units[uids[0]]["result_type"]
    row["class_key"] = {}
    row["class_key"]["operand_types"] = row["type_pair"]
    row["class_key"]["result_type"] = row["result_type"]
    row["class_key"]["note"] = "no operator token takes part in this "\
                               "key"

    inside = set(uids)
    tally = {}
    for name in EVIDENCE_ORDER:
        tally[name] = 0
    carried = 0
    unrecorded = 0
    for key in edges:
        if key[0] not in inside:
            continue
        if key[1] not in inside:
            continue
        source = edges[key]
        rec = grounds.get(key)
        if source == "canon-byte":
            tally["canon-byte"] = tally["canon-byte"] + 1
            continue
        if source == "z3":
            tally["z3"] = tally["z3"] + 1
            continue
        if rec is None:
            unrecorded = unrecorded + 1
            tally["unclassified"] = tally["unclassified"] + 1
            continue
        name = rec["evidence"]
        tally[name] = tally.get(name, 0) + 1
        if rec["carried"]:
            carried = carried + 1
    weakest = None
    for name in EVIDENCE_ORDER:
        if tally[name] > 0:
            weakest = name
    evidence = {}
    evidence["member_pairs_by_class"] = tally
    evidence["member_pairs_carried_from_an_earlier_pass"] = carried
    evidence["member_pairs_with_no_recorded_ground"] = unrecorded
    evidence["weakest_evidence"] = weakest
    if weakest is None:
        evidence["weakest_evidence_text"] = "no edge: this class has "\
                                            "one member"
    else:
        evidence["weakest_evidence_text"] = EVIDENCE_TEXT[weakest]
    row["evidence"] = evidence
    return row


# -------------------------------------------------------------- build

def build(indir, outdir, every):
    started = time.time()
    log("step 8, rebuilt -- the dominant-operator table under the "
        "rulings of 2026-08-25")
    doc = load(indir)
    units = unit_index(doc)
    log("units read: %d" % len(units))
    grounds = base.ground_index(doc)
    log("unit pairs with a recorded ground: %d" % len(grounds))
    borders = base.border_index(doc, units)
    log("divergence pairs: %d" % len(borders))
    corpus = base.corpus_index(doc)
    log("corpus cells (language x operand type pair): %d" % len(corpus))
    moved = movement(doc, units)
    log("class-count movement, one ruling at a time:")
    for rec in moved["steps"]:
        text = ""
        if "change" in rec:
            text = "  (%+d)" % rec["change"]
        log("  %d classes%s -- %s" % (rec["classes"], text,
                                      rec["step"]))
    buckets, edges, stats = build_classes(doc, units)
    log("edges used: %d" % len(edges))
    for name in sorted(stats["edges_by_source"].keys()):
        log("  from %s: %d" % (name, stats["edges_by_source"][name]))
    log("edges skipped, operand types differ: %d"
        % stats["edges_skipped_because_operand_types_differ"])
    log("edges skipped, RESULT types differ: %d"
        % stats["edges_skipped_because_result_types_differ"])
    log("classes formed: %d" % len(buckets))

    roots = sorted(buckets.keys(), key=lambda r: (-len(buckets[r]), r))
    class_of = {}
    for i, root in enumerate(roots):
        cid = "K%04d" % (i + 1)
        for uid in buckets[root]:
            class_of[uid] = cid

    rows = []
    done = 0
    for i, root in enumerate(roots):
        cid = "K%04d" % (i + 1)
        rows.append(one_class(cid, buckets[root], units, edges, grounds,
                              borders, corpus, class_of))
        done = done + 1
        if done % every == 0:
            log("  ... [%d/%d] classes assembled" % (done, len(roots)))
    log("  ... [%d/%d] classes assembled" % (done, len(roots)))

    out = {}
    out["shape"] = "one row per equivalence class on one class key: "\
                   "operand types AND result type"
    out["class_definition"] = "the transitive closure of the "\
                              "total-equality edges of verdicts4, the "\
                              "z3-proved MATCHED pairs of verdicts3b, "\
                              "and canonical-byte identity, restricted "\
                              "to edges whose two units carry the same "\
                              "operand types and the same result type"
    out["candidate_set"] = "machine-form evidence only: verdicts4's "\
                           "rows, verdicts3b's solver verdicts, and "\
                           "equality of canonical bytes.  No operator "\
                           "token takes part in any key, grouping, "\
                           "pairing or selection here."
    out["spelling"] = "the operator token appears once per unit, as "\
                      "the display label `operator` on a member object "\
                      "beside `lang` and `n`."
    out["canonical_form"] = doc["canon"]["go"]["form"]
    out["traced_variables_priority"] = doc["canon"]["go"]["priority"]
    out["intention_note"] = "`intention` is null on every row by "\
                            "instruction.  `intention_candidates` is a "\
                            "mechanical hint: proposed, the owner settles."
    out["weakest_evidence_note"] = "a class is the transitive closure "\
                                   "of its edges, so it is only as "\
                                   "strong as its weakest edge."
    out["languages"] = LANGS
    out["units_considered"] = len(units)
    out["classes"] = len(rows)
    out["edges_used"] = len(edges)
    out["edge_statistics"] = stats
    out["class_count_movement"] = moved
    out["canonicalisation"] = canon_summary(doc)
    out["round_trip"] = trip_summary(doc)
    out["result_type_sources"] = result_type_summary(units)
    out["lifter"] = doc["verdicts4"].get("lifter")
    out["z3"] = doc["verdicts4"].get("z3")
    out["stats"] = base.stats(rows)
    out["rows"] = rows

    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    jpath = os.path.join(outdir, "dominant_table2.json")
    fh = open(jpath, "w")
    json.dump(out, fh, indent=1)
    fh.close()
    log("wrote %s" % jpath)
    mpath = os.path.join(outdir, "dominant_table2.md")
    fh = open(mpath, "w")
    fh.write(markdown(out))
    fh.close()
    log("wrote %s" % mpath)
    dpath = os.path.join(outdir, "table_digest2.md")
    fh = open(dpath, "w")
    fh.write(digest(out))
    fh.close()
    log("wrote %s" % dpath)
    log("wall time: %.1f s" % (time.time() - started))
    return out


def canon_summary(doc):
    out = {}
    for lang in LANGS:
        d = doc["canon"][lang]
        rec = {}
        rec["units_read"] = d["units_read"]
        rec["canonical"] = d["canonical"]
        rec["refused"] = d["refused"]
        rec["refusal_reasons"] = d["refusal_reasons"]
        rec["units_with_an_eviction"] = d["units_with_an_eviction"]
        rec["units_unchanged_by_the_rename"] = \
            d["units_unchanged_by_the_rename"]
        out[lang] = rec
    return out


def trip_summary(doc):
    d = doc["roundtrip"]
    out = {}
    out["units_assembled"] = d["units_assembled"]
    out["text_survives_the_round_trip"] = d["text_survives_the_round_trip"]
    out["text_does_not_survive"] = d["text_does_not_survive"]
    out["unchanged_units_whose_bytes_match_the_ship_build"] = \
        d["unchanged_units_whose_bytes_match_the_ship_build"]
    out["unchanged_units_whose_bytes_differ_from_the_ship_build"] = \
        d["unchanged_units_whose_bytes_differ_from_the_ship_build"]
    return out


def result_type_summary(units):
    out = {}
    for uid in units:
        where = units[uid]["result_type_ground"]
        out[where] = out.get(where, 0) + 1
    return out


# ----------------------------------------------------------- markdown

def markdown(out):
    lines = []
    lines.append("# The dominant-operator table, rebuilt")
    lines.append("")
    lines.append("Step 8 under the four rulings of 2026-08-25. One row "
                 "per equivalence class on one class key: operand types "
                 "AND result type.")
    lines.append("")
    lines.append("- class definition: %s" % out["class_definition"])
    lines.append("- candidate set: %s" % out["candidate_set"])
    lines.append("- spelling: %s" % out["spelling"])
    lines.append("- canonical form: %s" % out["canonical_form"])
    lines.append("- traced variables: %s" % out["traced_variables_priority"])
    lines.append("- lifter: %s ; z3 %s" % (out["lifter"], out["z3"]))
    lines.append("")
    lines.append("## counts")
    lines.append("")
    lines.append("| what | count |")
    lines.append("|---|---|")
    lines.append("| units considered | %d |" % out["units_considered"])
    lines.append("| classes | %d |" % out["classes"])
    lines.append("| edges used | %d |" % out["edges_used"])
    for name in sorted(out["edge_statistics"]["edges_by_source"].keys()):
        lines.append("| edges from %s | %d |"
                     % (name,
                        out["edge_statistics"]["edges_by_source"][name]))
    lines.append("| edges skipped, operand types differ | %d |"
                 % out["edge_statistics"]
                 ["edges_skipped_because_operand_types_differ"])
    lines.append("| edges skipped, result types differ | %d |"
                 % out["edge_statistics"]
                 ["edges_skipped_because_result_types_differ"])
    for k in sorted(out["stats"].keys()):
        v = out["stats"][k]
        if isinstance(v, dict):
            continue
        lines.append("| %s | %s |" % (k.replace("_", " "), v))
    lines.append("")
    for name in ["weakest_evidence_distribution",
                 "intention_candidate_distribution",
                 "type_family_distribution"]:
        lines.append("### %s" % name.replace("_", " "))
        lines.append("")
        lines.append("| bucket | classes |")
        lines.append("|---|---|")
        d = out["stats"][name]
        for k in sorted(d.keys(), key=lambda x: -d[x]):
            lines.append("| %s | %d |" % (k, d[k]))
        lines.append("")
    lines.append("## the rows")
    lines.append("")
    for row in out["rows"]:
        lines.append("### %s &middot; operand types (%s) &middot; result "
                     "type %s &middot; %d member(s), %d language(s)"
                     % (row["class_id"], row["type_pair"],
                        row["result_type"], row["size"],
                        len(row["languages"])))
        lines.append("")
        lines.append("- members: %s" % base.md_members(row))
        lines.append("- canonical core (from %s): `%s`"
                     % (row["canonical_core_from"],
                        json.dumps(row["canonical_core"])))
        lines.append("- mode inventory:")
        lines.append(base.md_fences(row))
        lines.append("- divergence at the border:")
        lines.append(base.md_border(row))
        lines.append("- evidence: %s ; weakest: %s"
                     % (json.dumps(row["evidence"]
                                   ["member_pairs_by_class"]),
                        row["evidence"]["weakest_evidence_text"]))
        lines.append("- languages present: %s"
                     % ", ".join(row["coverage"]["languages_present"]))
        lines.append("- languages absent:")
        lines.append(base.md_absent(row))
        lines.append("- intention: null; proposed candidate: %s (%s)"
                     % (row["intention_candidates"]["proposed_ur_kind"],
                        row["intention_candidates"]["status"]))
        lines.append("")
    return "\n".join(lines) + "\n"


# ------------------------------------------------------------- digest

def digest(out):
    lines = []
    lines.append("# dominant table, rebuilt -- flat digest")
    lines.append("")
    lines.append("Multi-language classes (>=3 languages), one plain "
                 "table each.")
    lines.append("`canonical mnem` = the unit's instructions after the "
                 "rename into the canonical runnable form (first 6); "
                 "`(rename refused)` where the canonicaliser refused, "
                 "with the reason under the table.")
    lines.append("")
    for row in out["rows"]:
        if len(row["languages"]) < 3:
            continue
        lines.append("## %s &middot; types (%s) &middot; result %s "
                     "&middot; %d members"
                     % (row["class_id"], row["type_pair"],
                        row["result_type"], row["size"]))
        lines.append("")
        lines.append("| lang | label | canonical mnem |")
        lines.append("| --- | --- | --- |")
        refusals = []
        for m in row["members"]:
            text = m["canonical_form"]
            if text is None:
                text = "(rename refused)"
                if m["canonicalisation_refused"] not in refusals:
                    refusals.append(m["canonicalisation_refused"])
            parts = text.split("; ")
            if len(parts) > 6:
                parts = parts[:6]
                parts.append("...")
            lines.append("| %s | `%s` | `%s` |"
                         % (m["lang"], m["operator"], "; ".join(parts)))
        lines.append("")
        for why in refusals:
            lines.append("- %s" % why)
        if refusals:
            lines.append("")
        lines.append("- weakest evidence: %s"
                     % row["evidence"]["weakest_evidence_text"])
        lines.append("")
    return "\n".join(lines) + "\n"


def main(argv):
    indir = HERE
    outdir = HERE
    every = 200
    i = 1
    while i < len(argv):
        if argv[i] == "--in":
            indir = argv[i + 1]
            i = i + 2
            continue
        if argv[i] == "--out":
            outdir = argv[i + 1]
            i = i + 2
            continue
        if argv[i] == "--every":
            every = int(argv[i + 1])
            i = i + 2
            continue
        print(__doc__)
        return 2
    build(indir, outdir, every)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
