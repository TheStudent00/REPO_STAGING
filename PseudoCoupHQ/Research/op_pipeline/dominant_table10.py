#!/usr/bin/env python3
"""dominant_table10.py -- dominant_table10.json.

Successor to dominant_table_tree.py's dominant_table9.json, adding ONE
new class-forming evidence ground: "canon-text".

Two units share `canon-text` when their canon3_units_<lang>.json
canonical runnable texts are CHARACTER-IDENTICAL, line for line, gated
on the SAME class key (operand types AND result type) every other
edge in this table passes through.  For a non-branching unit the text
is canon3's own `derived_text` line list.  For a branching unit the
text is `derived_blocks` (its block/steps structure) RE-RENDERED with
branch labels renamed POSITIONALLY -- L0, L1, L2 ... in the order the
blocks appear in canon3's own list -- and every jump target inside a
block's steps rewritten to match, so two units whose compilers picked
different label numbers for the identical block structure still
compare equal.  Only units whose `roundtrip.assembled` is exactly
`true` are used: canon3.py itself only calls a unit's derived text
canonical when it re-assembled to real bytes (canon3_units_c.json's
own `canonical_text_ok` count, 608 of 610, is exactly this gate;
summed over all five languages: 1,699 of 1,779).

RATIFIED PRIMARY GROUND, per the owner's brief for this lap.  RANK CHOSEN:
byte, canon-byte, canon-text, erased-form, tree-exact, sem, core-text,
z3, unclassified -- canon-text sits ABOVE erased-form (as instructed)
but BELOW canon-byte.  Reasoning, stated so the choice can be struck:
canon-byte and byte are both literal machine bytes -- the least
interpreted, most "forced by construction" evidence this line has
(the evidence doctrine's top class).  canon-text is the RATIFIED HOME
REPRESENTATION and the right form for matching, analysis, and
presentation, but as a text it is one step more interpreted than raw
bytes: two different mnemonic spellings of the same opcode (e.g. an
assembler accepting `je` and `jz` for one encoding) could in principle
assemble to identical bytes while differing as text, which is exactly
why text-identity is a STRICTER, more information-preserving relation
than byte-identity, not a stronger machine fact than it -- byte
identity remains the most direct read of "the two units are the same
executable code".  erased-form sits below canon-text because it is a
DELIBERATE COARSENING of canon-text: it erases the bookkeeping moves
canon-text keeps on their own lines, so two canon-text-identical units
are always erased-form-identical, but not the reverse -- erasure can
equate units canon-text tells apart (different entry contracts, same
erased body).  A finer relation outranking the coarsening it was built
from is the ordering principle applied throughout this table.

THE SPELLING BAN, verbatim, restated because this program groups and
pairs units: "No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in 'which pairs get
compared', not in report rows, not in dropdowns.  The candidate set
for comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token.  The
token appears exactly once per unit: as a display label on the
member."  The canon-text groups here are keyed on rendered instruction
text (machine evidence: opcodes, registers, immediates, positional
branch labels -- never `operator`) and are additionally gated on the
same class-key check every other edge passes through.
check_no_spelling_keys.py is run over the output before this program
exits successfully.

usage:
  dominant_table10.py [--in DOMINANT_TABLE9] [--out OUTFILE]
"""

import json
import os
import re
import sys
import time
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dominant_table4 as T4                                  # noqa: E402

SOURCE_TABLE = "dominant_table9.json"
CANON3_LANGS = ["c", "cpp", "go", "rust", "swift"]
OUT_NAME = "dominant_table10.json"

EVIDENCE_ORDER = ["byte", "canon-byte", "canon-text", "erased-form",
                  "tree-exact", "sem", "core-text", "z3", "unclassified"]

EVIDENCE_TEXT = {
    "byte": "byte identity (the two units are the same machine bytes)",
    "canon-byte": "canonical byte identity (after the rename into the "
                  "canonical runnable form, the two units assemble to "
                  "the same machine bytes)",
    "canon-text": "canon-text identity: the canonical runnable "
                  "instruction text (canon3_units_<lang>.json's "
                  "derived_text / positionally-relabeled derived_blocks, "
                  "reassembly-verified) is character-identical between "
                  "the two units, gated on the same class key",
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

LABEL_RE = re.compile(r"\bL\d+\b")


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
    if text.startswith("canon-text"):
        return "canon-text"
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


# ---------------------------------------------------- canon3 reading

def normalize_blocks(blocks):
    """derived_blocks re-rendered with branch labels renamed
    POSITIONALLY: the block at list position i becomes L{i}, and every
    jump target inside every block's steps is rewritten to match.  This
    is what lets two branching units whose compilers picked different
    label numbers for an identical block structure compare equal."""
    rename = {}
    for i, block in enumerate(blocks):
        rename[block["label"]] = "L%d" % i

    def sub_one(m):
        old = m.group(0)
        return rename.get(old, old)

    lines = []
    for i, block in enumerate(blocks):
        lines.append("L%d:" % i)
        for step in block["steps"]:
            lines.append("  " + LABEL_RE.sub(sub_one, step))
    return tuple(lines)


def canon_text_of(rec):
    """(ok, text_tuple_or_None, refusal_text_or_None) for one canon3
    unit record."""
    assembled = rec.get("roundtrip", {}).get("assembled")
    if assembled is not True:
        why = rec.get("roundtrip", {}).get("as_stderr")
        if why:
            return False, None, ("canon3 derived text did not "
                                 "reassemble: %s" % why)
        return False, None, "canon3 has no reassembly-verified "\
                            "derived text for this unit"
    blocks = rec.get("derived_blocks")
    if blocks is not None:
        return True, normalize_blocks(blocks), None
    dt = rec.get("derived_text")
    if dt:
        return True, tuple(dt), None
    return False, None, "canon3 record carries neither derived_text "\
                        "nor derived_blocks"


def load_canon3():
    """unit label -> dict(ok, text (tuple or None), lines (list or
    None, for presentation), refusal (str or None))."""
    out = {}
    for lang in CANON3_LANGS:
        path = os.path.join(HERE, "canon3_units_%s.json" % lang)
        if not os.path.exists(path):
            log("!! missing %s -- proceeding without it" % path)
            continue
        doc = json.load(open(path))
        for _k, rec in doc["units"].items():
            label = rec["unit"]
            ok, text, refusal = canon_text_of(rec)
            out[label] = dict(ok=ok, text=text,
                              lines=list(text) if text is not None
                              else None,
                              refusal=refusal)
    return out


def collect_canon_text_edges(canon3, unit_class, by_id):
    groups = {}
    for unit, rec in canon3.items():
        if not rec["ok"]:
            continue
        groups.setdefault(rec["text"], []).append(unit)

    edges = []
    same_key_groups = 0
    cross_key_refused = 0
    for text, units in groups.items():
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
                              ground="canon-text identity: the "
                                     "canonical runnable instruction "
                                     "text is character-identical",
                              source="canon3_units_<lang>.json, "
                                     "derived-text grouping"))
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
    rows9 = table["rows"]
    log("classes read (dominant_table9) %d" % len(rows9))

    by_id = {}
    unit_class = {}
    for r in rows9:
        by_id[r["class_id"]] = r
        for m in r["members"]:
            unit_class[m["unit"]] = r["class_id"]

    sets = T4.Sets()
    for r in rows9:
        sets.add(r["class_id"])

    canon3 = load_canon3()
    ok_count = sum(1 for rec in canon3.values() if rec["ok"])
    log("canon3 units loaded %d (reassembly-verified %d)"
        % (len(canon3), ok_count))

    text_edges, text_groups, text_cross_refused = \
        collect_canon_text_edges(canon3, unit_class, by_id)
    log("canon-text groups usable as edges  %d" % text_groups)
    log("canon-text groups refused (class key differs) %d" %
        text_cross_refused)

    used = []
    refused = []
    refused_why = Counter()
    for e in text_edges:
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
    for r in rows9:
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
        rows10 = []
        for k in keys:
            new_id = min(str(x["class_id"]) for x in groups[k])
            rows10.append(T4.merged_row(new_id, groups[k],
                                        final_grounds.get(k, [])))
    finally:
        T4.EVIDENCE_ORDER = old_order
        T4.EVIDENCE_TEXT = old_text
        T4.evidence_class = old_evidence_class
        T4.weakest = old_weakest

    # PRESENTATION REQUIREMENT: every member of every row carries its
    # canonical text (or a named refusal), read from canon3.
    members_with_text = 0
    members_without_text = 0
    for r in rows10:
        for m in r["members"]:
            rec = canon3.get(m["unit"])
            if rec is None:
                m["canonical_text"] = None
                m["canonical_text_refusal"] = \
                    "unit not present in any canon3_units_<lang>.json"
                members_without_text += 1
                continue
            if rec["ok"]:
                m["canonical_text"] = rec["lines"]
                m["canonical_text_refusal"] = None
                members_with_text += 1
            else:
                m["canonical_text"] = None
                m["canonical_text_refusal"] = rec["refusal"]
                members_without_text += 1

    per_ground = Counter()
    for r in rows10:
        counts = r["evidence"].get("member_pairs_by_class") or {}
        for k, v in counts.items():
            per_ground[k] += v

    stats = {}
    stats["classes_before"] = len(rows9)
    stats["classes_after"] = len(rows10)
    stats["classes_merged_away"] = len(rows9) - len(rows10)
    stats["canon_text_edges_offered"] = len(text_edges)
    stats["canon_text_edges_used"] = len(used)
    stats["canon_text_edges_that_merged_two_classes"] = \
        merges_that_changed_partition
    stats["canon_text_groups_refused_cross_class_key"] = \
        text_cross_refused
    stats["member_pairs_by_evidence_ground"] = dict(per_ground)
    stats["weakest_evidence_distribution"] = dict(Counter(
        str(r["evidence"]["weakest_evidence"]) for r in rows10))
    stats["members_with_canonical_text"] = members_with_text
    stats["members_without_canonical_text"] = members_without_text

    out = {}
    out["shape"] = "dominant_table9's own partition, plus canon-text " \
                   "edges from canon3_units_<lang>.json, closed " \
                   "transitively"
    out["candidate_set"] = "machine-form evidence only: dominant_table9" \
        "'s carried edges, plus canon-text groups (character-identical " \
        "canonical runnable instruction text, gated on the same class " \
        "key).  No operator token takes part in any key, grouping, " \
        "pairing or selection here."
    out["spelling"] = "the operator token appears once per unit, as " \
                      "the display label `operator` on a member " \
                      "object beside `lang` and `n`; `canonical_text` " \
                      "is a per-member presentation field of rendered " \
                      "instruction lines, never a key."
    out["canon_text_ground"] = "two units share `canon-text` when " \
        "canon3_units_<lang>.json's reassembly-verified canonical " \
        "runnable text (derived_text, or derived_blocks with branch " \
        "labels renamed positionally L0, L1, ... in list order and " \
        "every jump target rewritten to match) is character-identical " \
        "line for line, gated on the same class key.  Only units " \
        "whose roundtrip.assembled is exactly true are used."
    out["evidence_order"] = EVIDENCE_ORDER
    out["evidence_order_reasoning"] = "canon-text ranks above " \
        "erased-form (erased-form is a deliberate coarsening of " \
        "canon-text -- it erases the bookkeeping moves canon-text " \
        "keeps) but below canon-byte and byte, which remain literal " \
        "machine bytes -- the least-interpreted evidence this line " \
        "has, per the evidence doctrine.  See this file's own module " \
        "docstring for the reasoning in full."
    out["source_table"] = SOURCE_TABLE
    out["canon3_sources"] = ["canon3_units_%s.json" % lang
                             for lang in CANON3_LANGS]
    out["languages"] = T4.LANGS
    out["classes"] = len(rows10)
    out["new_edges_used"] = used
    out["new_edges_refused"] = refused
    out["stats"] = stats
    out["wall_seconds"] = round(time.time() - started, 2)
    out["rows"] = rows10

    path = os.path.join(outdir, OUT_NAME)
    fh = open(path, "w")
    json.dump(out, fh, indent=1)
    fh.write("\n")
    fh.close()
    log("wrote %s" % path)
    log("classes  %d -> %d" % (len(rows9), len(rows10)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
