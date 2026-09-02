#!/usr/bin/env python3
"""dominant_table.py -- step 8 of the ratified pipeline.

The deliverable: the DOMINANT-OPERATOR TABLE.  One row per (core
equivalence class, operand type pair).  A core equivalence class is
the transitive closure of the TOTAL-EQUALITY edges of verdicts4.json
-- the pairs whose cores are equal AND whose mode inventories agree.

What a row carries
------------------
  * members      -- language, unit id, and the operator token as a
                    DISPLAY LABEL (the one place a token is allowed)
  * canonical core -- one lifted sem form, the class representative
  * mode inventory -- per member, its fences: condition -> response
                    kind, with the interval-probe name where the mode
                    carries one (wrapping / growing / approximating)
  * divergence conditions -- inside the class (members whose fence
                    sets differ) and at its border (DIFFERS-BY-DESIGN
                    pairs, and core-equal-modes-differ pairs, that
                    touch a member)
  * evidence     -- how many member pairs rest on byte identity, on
                    anchored sem identity, on z3; how many were
                    carried from an earlier pass; and the WEAKEST
                    class present, because a transitively closed
                    class is only as strong as its weakest edge
  * coverage     -- languages present, and every absent language with
                    its reason (refused by the compiler's own type
                    checker, or measured but not equal)
  * intention    -- ALWAYS null.  `intention_candidates` carries the
                    mechanical hint read off the canonical core's top
                    operation, marked "proposed, the owner settles".  This
                    table feeds ur_kind; it does not rule it.

THE SPELLING BAN.  No operator token takes part in any key, grouping,
pairing, candidate selection or comparison scope here.  Classes come
from verdicts4's machine-form edges; the token is written once per
member, as `operator`, on a unit object.  Run
check_no_spelling_keys.py on the output.

usage:
  dominant_table.py [--in DIR] [--out DIR]
"""

import json
import os
import re
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))

LANGS = ["c", "cpp", "go", "rust", "swift"]

TOTAL_EQUAL = "total equality"

MODES_DIFFER = "core equality, modes differ"

# evidence classes, strongest first.  byte identity is an artifact
# fact (the same machine bytes); anchored sem identity is a fact about
# the lifted form with identities carried by construction; z3 is a
# proof about the lifter's MODEL of the machine -- testimony.
EVIDENCE_ORDER = ["byte", "sem", "core-text", "z3", "unclassified"]

EVIDENCE_TEXT = {
    "byte": "byte identity (the two units are the same machine bytes)",
    "sem": "anchored sem identity (the two lifted forms are identical)",
    "core-text": "core-text identity: verdicts4's own column found the "
                 "two normal-path cores textually equal and their mode "
                 "sets equal, and verdicts3b recorded no identity "
                 "ground for the pair",
    "z3": "z3 over the two lifted forms (a proof about the lifter's "
          "model, not about the bytes)",
    "unclassified": "ground not recognised by this builder",
}

# NOTE, stated because it is a real limit of this table: verdicts4
# decides core equality by TEXTUAL equality of the lifted core forms.
# A pair that only z3 proved equal therefore never carries a
# total-equality column, and so `z3` never appears as a class's
# evidence.  Pairs z3 proved equal but whose texts differ are outside
# every class here; they sit in the border/evidence view instead.

WRAPPER = re.compile(r"^(zx\d*|sx\d*|ex\d*|to\d+|widen|narrow)$")

CALL_NAME = re.compile(r"([A-Za-z_][A-Za-z0-9_]*)\s*\(")

ARITH = ("Add", "Sub", "Mul", "Div", "Mod", "Mull", "DivMod", "Neg")

BITWISE = ("And", "Or", "Xor", "Not", "Shl", "Shr", "Sar")

CONVERT = ("F32to", "F64to", "I32S", "I64S", "I32U", "I64U", "F64x",
           "ReinterpF")


def log(text):
    sys.stdout.write(text + "\n")
    sys.stdout.flush()


# ---------------------------------------------------------------- io

def load(indir):
    doc = {}
    doc["verdicts4"] = json.load(open(os.path.join(indir,
                                                   "verdicts4.json")))
    doc["verdicts3b"] = json.load(open(os.path.join(indir,
                                                    "verdicts3b.json")))
    doc["core_modes"] = {}
    doc["op_units"] = {}
    for lang in LANGS:
        name = "core_modes_%s.json" % lang
        doc["core_modes"][lang] = json.load(open(os.path.join(indir,
                                                              name)))
        name = "op_units_%s.json" % lang
        doc["op_units"][lang] = json.load(open(os.path.join(indir,
                                                            name)))
    return doc


# ------------------------------------------------------- union-find

class UnionFind(object):

    def __init__(self):
        self.up = {}

    def add(self, item):
        if item in self.up:
            return
        self.up[item] = item

    def find(self, item):
        self.add(item)
        root = item
        while self.up[root] != root:
            root = self.up[root]
        while self.up[item] != root:
            nxt = self.up[item]
            self.up[item] = root
            item = nxt
        return root

    def union(self, a, b):
        ra = self.find(a)
        rb = self.find(b)
        if ra == rb:
            return
        self.up[ra] = rb


# ------------------------------------------------------------ units

def unit_index(doc):
    """every measured unit, keyed by its machine id `lang/op_n`."""
    out = {}
    for lang in LANGS:
        units = doc["core_modes"][lang]["units"]
        for n, u in units.items():
            uid = "%s/op_%s" % (lang, n)
            out[uid] = u
    return out


def type_pair_of(unit):
    return unit["type_pair"]


def member_record(uid, unit):
    """a UNIT OBJECT: it carries lang + n, so `operator` on it is the
    permitted per-unit display label."""
    rec = {}
    rec["unit"] = uid
    rec["lang"] = unit["lang"]
    rec["n"] = unit["n"]
    rec["operator"] = unit["operator"]
    rec["type_pair"] = unit["type_pair"]
    rec["mode_count"] = len(unit["modes"])
    return rec


def fence_records(unit):
    out = []
    for m in unit["modes"]:
        f = {}
        f["condition"] = m.get("condition")
        f["response_kind"] = response_kind(m.get("response"))
        f["response_raw"] = m.get("response")
        f["detection"] = m.get("detection")
        f["interval_probe_name"] = m.get("mode_name")
        out.append(f)
    return out


def response_kind(response):
    """the response KIND.  A panic callee's name is carried on the raw
    response and printed, but two panics are the same kind."""
    if response is None:
        return None
    if response.startswith("panic-call"):
        return "panic-call"
    return response


def fence_key(fence):
    parts = []
    parts.append(str(fence.get("condition")))
    parts.append(str(fence.get("response_kind")))
    return " -> ".join(parts)


# ----------------------------------------------------------- classes

def classify_ground(ground):
    if ground is None:
        return "unclassified"
    if ground.startswith("byte identity"):
        return "byte"
    if ground.startswith("sem identity"):
        return "sem"
    if ground.startswith("z3"):
        return "z3"
    # verdicts3b had no identity ground for this pair, yet verdicts4's
    # column read the two records as totally equal.  The fact is
    # verdicts4's own core-text comparison.
    return "core-text"


def ground_index(doc):
    """for every unit pair, the ground verdicts3b recorded for it, and
    whether that verdict was carried from the earlier pass."""
    out = {}
    for row in doc["verdicts3b"]["rows"]:
        for p in row.get("pairs", []):
            key = pair_key(p["left"], p["right"])
            if key in out:
                continue
            rec = {}
            rec["ground"] = p.get("ground")
            rec["evidence"] = classify_ground(p.get("ground"))
            rec["verdict"] = p.get("verdict")
            rec["carried"] = p.get("carried_from") is not None
            rec["detail"] = p.get("detail")
            out[key] = rec
    return out


def pair_key(a, b):
    if a <= b:
        return (a, b)
    return (b, a)


def build_classes(doc, units):
    """union the TOTAL-EQUALITY edges.  An edge is used only when both
    of its units carry the same operand type pair, so a class never
    straddles two type pairs."""
    uf = UnionFind()
    edges = {}
    skipped_cross_type = 0
    for uid in units:
        uf.add(uid)
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
            if type_pair_of(units[left]) != type_pair_of(units[right]):
                skipped_cross_type = skipped_cross_type + 1
                continue
            uf.union(left, right)
            edges[pair_key(left, right)] = True
    buckets = {}
    for uid in units:
        root = uf.find(uid)
        if root not in buckets:
            buckets[root] = []
        buckets[root].append(uid)
    return buckets, edges, uf, skipped_cross_type


def border_index(doc, units):
    """every pair that states a DIVERGENCE: a differs-by-design pair
    (verdicts3b) or a core-equal-modes-differ pair (verdicts4)."""
    out = {}
    for row in doc["verdicts3b"]["rows"]:
        for p in row.get("pairs", []):
            if p.get("verdict") != "DIFFERS-BY-DESIGN":
                continue
            key = pair_key(p["left"], p["right"])
            rec = {}
            rec["kind"] = "differs-by-design"
            rec["left"] = p["left"]
            rec["right"] = p["right"]
            rec["guarded_side"] = p.get("guarded")
            rec["bare_side"] = p.get("bare")
            rec["guard_events"] = p.get("guard_events", [])
            rec["divergence_conditions"] = p.get("divergence_conditions",
                                                 [])
            out[key] = rec
    for row in doc["verdicts4"]["rows"]:
        for p in row["pairs"]:
            if p["column"] != MODES_DIFFER:
                continue
            key = pair_key(p["left"], p["right"])
            if key in out:
                continue
            rec = {}
            rec["kind"] = "core equal, modes differ"
            rec["left"] = p["left"]
            rec["right"] = p["right"]
            rec["modes_only_left"] = p.get("modes_only_left", [])
            rec["modes_only_right"] = p.get("modes_only_right", [])
            rec["shared_modes"] = p.get("shared_modes", [])
            out[key] = rec
    return out


# ---------------------------------------------------------- coverage

def corpus_index(doc):
    """per (language, type pair): how many probes the compiler accepted
    and how many its type checker refused, with one refusal quoted."""
    out = {}
    for lang in LANGS:
        probes = doc["op_units"][lang]["probes"]
        for n, p in probes.items():
            meta = p.get("meta", {})
            lhs = meta.get("lhs_rep")
            rhs = meta.get("rhs_rep")
            tp = "%s,%s" % (lhs, rhs)
            key = (lang, tp)
            if key not in out:
                out[key] = {"accepted": 0, "refused": 0, "sample": None}
            if p.get("refused"):
                out[key]["refused"] = out[key]["refused"] + 1
                if out[key]["sample"] is None:
                    out[key]["sample"] = str(p["refused"])[:200]
            else:
                out[key]["accepted"] = out[key]["accepted"] + 1
    return out


def coverage_for(type_pair, present, corpus):
    absent = []
    for lang in LANGS:
        if lang in present:
            continue
        info = corpus.get((lang, type_pair))
        rec = {}
        rec["language"] = lang
        if info is None:
            rec["reason"] = "unmeasured: this language's probe set has "\
                            "no candidate on this operand type pair"
            rec["evidence_class"] = "forced by construction (the "\
                                    "generated probe set is the record)"
        elif info["accepted"] == 0:
            rec["reason"] = "refused by the compiler's own type "\
                            "checker: %d of %d candidates on this "\
                            "operand type pair were refused" % (
                                info["refused"],
                                info["refused"] + info["accepted"])
            rec["refusal_sample"] = info["sample"]
            rec["evidence_class"] = "the tool's own testimony (the "\
                                    "compiler's refusal text)"
        else:
            rec["reason"] = "measured but not equal: %d accepted unit"\
                            "(s) on this operand type pair, none of "\
                            "which a total-equality edge placed in "\
                            "this class" % info["accepted"]
            rec["evidence_class"] = "forced by construction (the "\
                                    "absence of an edge)"
        absent.append(rec)
    return absent


# --------------------------------------------------------- intention

def top_operation(core):
    if not core:
        return None
    names = CALL_NAME.findall(core[0])
    for name in names:
        bare = name.split("@")[0]
        if WRAPPER.match(bare):
            continue
        return name
    return None


def starts_with_any(name, prefixes):
    for p in prefixes:
        if name.startswith(p):
            return True
    return False


def intention_hint(core):
    """the MECHANICAL hint, from the canonical core's top operation.
    Proposed only.  the owner settles ur_kind."""
    op = top_operation(core)
    if op is None:
        if not core:
            return ("value", "the unit computes nothing on the normal "
                             "path: the operand reaches the result "
                             "unchanged", None)
        return ("unassigned", "the canonical core carries no call to "
                              "read a top operation from", None)
    if op == "amd64g_calculate_condition":
        return ("choice", "the top operation is a condition "
                          "calculation: the unit produces a decision "
                          "value, which is choice-adjacent, not a "
                          "choice by itself", op)
    if op.startswith("Cmp"):
        return ("choice", "the top operation is a comparison: "
                          "choice-adjacent", op)
    if op == "ite":
        return ("choice", "the top operation selects between two "
                          "values", op)
    if op.startswith("st"):
        return ("mutation", "the top operation is a store", op)
    if starts_with_any(op, CONVERT):
        return ("value", "the top operation converts between "
                         "representations of a number", op)
    if starts_with_any(op, ARITH):
        return ("operation", "the top operation is arithmetic", op)
    if starts_with_any(op, BITWISE):
        return ("operation", "the top operation is bitwise", op)
    return ("unassigned", "the top operation is not in this builder's "
                          "hint map", op)


# ------------------------------------------------------------- build

def build(indir, outdir):
    started = time.time()
    log("step 8 -- the dominant-operator table")
    doc = load(indir)
    units = unit_index(doc)
    log("units read: %d" % len(units))
    grounds = ground_index(doc)
    log("unit pairs with a recorded ground: %d" % len(grounds))
    borders = border_index(doc, units)
    log("divergence pairs (differs-by-design + modes differ): %d"
        % len(borders))
    corpus = corpus_index(doc)
    log("corpus cells (language x operand type pair): %d" % len(corpus))
    buckets, edges, uf, skipped = build_classes(doc, units)
    log("total-equality edges used: %d" % len(edges))
    log("edges skipped because the two units carry different operand "
        "type pairs: %d" % skipped)
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
        if done % 100 == 0:
            log("  ... %d / %d classes assembled" % (done, len(roots)))
    log("  ... %d / %d classes assembled" % (done, len(roots)))

    out = {}
    out["shape"] = "one row per core equivalence class on one operand "\
                   "type pair"
    out["class_definition"] = "the transitive closure of verdicts4's "\
                              "TOTAL-EQUALITY edges (core equal and "\
                              "mode inventories agreeing), restricted "\
                              "to edges whose two units carry the same "\
                              "operand type pair"
    out["candidate_set"] = "verdicts4's machine-form rows, which came "\
                           "from cluster identity or a shared maximal "\
                           "sub-term on one operand type pair.  No "\
                           "operator token takes part in any key, "\
                           "grouping, pairing or selection here."
    out["spelling"] = "the operator token appears once per unit, as "\
                      "the display label `operator` on a member "\
                      "object beside `lang` and `n`."
    out["intention_note"] = "`intention` is null on every row by "\
                            "instruction.  `intention_candidates` is "\
                            "a mechanical hint read off the canonical "\
                            "core's top operation: proposed, the owner "\
                            "settles."
    out["weakest_evidence_note"] = "a class is the transitive closure "\
                                   "of its edges, so it is only as "\
                                   "strong as its weakest edge; "\
                                   "`weakest_evidence` states that "\
                                   "edge's class."
    out["languages"] = LANGS
    out["units_considered"] = len(units)
    out["classes"] = len(rows)
    out["edges_used"] = len(edges)
    out["edges_skipped_cross_type_pair"] = skipped
    out["lifter"] = doc["verdicts4"].get("lifter")
    out["z3"] = doc["verdicts4"].get("z3")
    out["excluded"] = doc["verdicts4"].get("excluded")
    out["excluded_rows"] = doc["verdicts4"].get("excluded_rows")
    out["stats"] = stats(rows)
    out["rows"] = rows

    if not os.path.isdir(outdir):
        os.makedirs(outdir)
    jpath = os.path.join(outdir, "dominant_table.json")
    fh = open(jpath, "w")
    json.dump(out, fh, indent=1)
    fh.close()
    log("wrote %s" % jpath)
    mpath = os.path.join(outdir, "dominant_table.md")
    fh = open(mpath, "w")
    fh.write(markdown(out))
    fh.close()
    log("wrote %s" % mpath)
    log("wall time: %.1f s" % (time.time() - started))
    return out


def one_class(cid, uids, units, edges, grounds, borders, corpus,
              class_of):
    uids = sorted(uids)
    members = []
    for uid in uids:
        members.append(member_record(uid, units[uid]))

    type_pair = type_pair_of(units[uids[0]])

    # canonical core: the class representative's sem form.  Every
    # member's core was proven equal to it; the TEXT can still differ
    # (two forms z3 proved equal are not two identical strings), so
    # the count of distinct texts is stated.
    forms = {}
    for uid in uids:
        text = json.dumps(units[uid]["core"])
        if text not in forms:
            forms[text] = []
        forms[text].append(uid)
    ordered = sorted(forms.keys())
    rep_text = ordered[0]
    rep_unit = sorted(forms[rep_text])[0]

    # the mode inventory, per member
    inventory = []
    fence_sets = {}
    for uid in uids:
        fences = fence_records(units[uid])
        rec = {}
        rec["unit"] = uid
        rec["lang"] = units[uid]["lang"]
        rec["n"] = units[uid]["n"]
        rec["operator"] = units[uid]["operator"]
        rec["fences"] = fences
        inventory.append(rec)
        keys = []
        for f in fences:
            keys.append(fence_key(f))
        fence_sets[uid] = sorted(set(keys))

    # divergence INSIDE the class: members whose fence sets differ.
    # By construction a total-equality edge means the two mode
    # inventories agreed, so anything here is a transitivity artefact
    # and is reported as such.
    inside = []
    distinct_fence_sets = {}
    for uid in uids:
        key = json.dumps(fence_sets[uid])
        if key not in distinct_fence_sets:
            distinct_fence_sets[key] = []
        distinct_fence_sets[key].append(uid)
    if len(distinct_fence_sets) > 1:
        for key in sorted(distinct_fence_sets.keys()):
            rec = {}
            rec["fence_set"] = json.loads(key)
            rec["units"] = sorted(distinct_fence_sets[key])
            inside.append(rec)

    # divergence at the BORDER: differs-by-design and modes-differ
    # pairs with one foot in this class
    border = []
    inside_set = set(uids)
    for key, rec in borders.items():
        left = rec["left"]
        right = rec["right"]
        hit_left = left in inside_set
        hit_right = right in inside_set
        if not hit_left and not hit_right:
            continue
        if hit_left and hit_right:
            where = "both units are members of this class"
        else:
            where = "one unit is a member of this class"
        item = dict(rec)
        item["scope"] = where
        item["other_class"] = None
        if hit_left and not hit_right:
            item["other_class"] = class_of.get(right)
        if hit_right and not hit_left:
            item["other_class"] = class_of.get(left)
        border.append(item)
    border.sort(key=lambda r: (r["kind"], r["left"], r["right"]))

    # evidence: every total-equality edge with both feet in the class
    tally = {}
    for name in EVIDENCE_ORDER:
        tally[name] = 0
    carried = 0
    unrecorded = 0
    for key in edges:
        if key[0] not in inside_set:
            continue
        if key[1] not in inside_set:
            continue
        rec = grounds.get(key)
        if rec is None:
            unrecorded = unrecorded + 1
            tally["unclassified"] = tally["unclassified"] + 1
            continue
        tally[rec["evidence"]] = tally[rec["evidence"]] + 1
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

    present = []
    for m in members:
        if m["lang"] not in present:
            present.append(m["lang"])
    present.sort(key=lambda x: LANGS.index(x))

    coverage = {}
    coverage["languages_present"] = present
    coverage["languages_absent"] = coverage_for(type_pair, present,
                                                corpus)

    kind, why, op = intention_hint(json.loads(rep_text))
    candidates = {}
    candidates["proposed_ur_kind"] = kind
    candidates["from_top_operation"] = op
    candidates["why"] = why
    candidates["status"] = "proposed, the owner settles"

    row = {}
    row["class_id"] = cid
    row["type_pair"] = type_pair
    row["size"] = len(uids)
    row["languages"] = present
    row["members"] = members
    row["canonical_core"] = json.loads(rep_text)
    row["canonical_core_from"] = rep_unit
    row["distinct_core_texts"] = len(forms)
    row["mode_inventory"] = inventory
    row["carries_modes"] = any_modes(inventory)
    row["divergence_inside_the_class"] = inside
    row["divergence_at_the_border"] = border
    row["evidence"] = evidence
    row["coverage"] = coverage
    row["intention"] = None
    row["intention_candidates"] = candidates
    return row


def any_modes(inventory):
    for rec in inventory:
        if rec["fences"]:
            return True
    return False


def type_family(type_pair):
    lhs = type_pair.split(",")[0]
    if lhs.startswith("i") or lhs.startswith("u"):
        return "integer"
    if lhs.startswith("f"):
        return "float"
    if lhs.startswith("bool"):
        return "bool"
    return "other"


def stats(rows):
    out = {}
    out["classes"] = len(rows)
    out["classes_size_1"] = 0
    out["classes_spanning_2_or_more_languages"] = 0
    out["classes_spanning_4_or_more_languages"] = 0
    out["classes_spanning_all_5_languages"] = 0
    out["classes_carrying_modes"] = 0
    out["classes_with_a_divergence_at_the_border"] = 0
    out["classes_with_a_fence_set_split_inside"] = 0
    weakest = {}
    hints = {}
    families = {}
    for r in rows:
        if r["size"] == 1:
            out["classes_size_1"] = out["classes_size_1"] + 1
        k = len(r["languages"])
        if k >= 2:
            out["classes_spanning_2_or_more_languages"] += 1
        if k >= 4:
            out["classes_spanning_4_or_more_languages"] += 1
        if k == 5:
            out["classes_spanning_all_5_languages"] += 1
        if r["carries_modes"]:
            out["classes_carrying_modes"] += 1
        if r["divergence_at_the_border"]:
            out["classes_with_a_divergence_at_the_border"] += 1
        if r["divergence_inside_the_class"]:
            out["classes_with_a_fence_set_split_inside"] += 1
        w = r["evidence"]["weakest_evidence"]
        name = str(w)
        weakest[name] = weakest.get(name, 0) + 1
        h = r["intention_candidates"]["proposed_ur_kind"]
        hints[h] = hints.get(h, 0) + 1
        fam = type_family(r["type_pair"])
        families[fam] = families.get(fam, 0) + 1
    out["weakest_evidence_distribution"] = weakest
    out["intention_candidate_distribution"] = hints
    out["type_family_distribution"] = families
    return out


# ---------------------------------------------------------- markdown

def md_members(row):
    parts = []
    for m in row["members"]:
        parts.append("%s `%s` (%s)" % (m["lang"], m["operator"],
                                       m["unit"]))
    return ", ".join(parts)


def md_fences(row):
    lines = []
    for rec in row["mode_inventory"]:
        if not rec["fences"]:
            continue
        for f in rec["fences"]:
            name = f["interval_probe_name"]
            if name is None:
                name = "(no interval-probe name)"
            lines.append("  - %s `%s`: %s -> %s [%s, %s]"
                         % (rec["lang"], rec["operator"],
                            f["condition"], f["response_kind"],
                            name, f["detection"]))
    if not lines:
        return "  - (no member carries a fence)"
    return "\n".join(lines)


def md_border(row):
    lines = []
    for b in row["divergence_at_the_border"][:6]:
        if b["kind"] == "differs-by-design":
            conds = []
            for c in b.get("divergence_conditions", []):
                conds.append(str(c.get("condition")))
            text = "; ".join(conds)
            if not text:
                text = "(condition not recorded)"
            lines.append("  - differs by design, %s vs %s: %s"
                         % (b["left"], b["right"], text))
        else:
            only = []
            for c in b.get("modes_only_left", []):
                only.append("only on %s: %s" % (b["left"],
                                                c.get("condition")))
            for c in b.get("modes_only_right", []):
                only.append("only on %s: %s" % (b["right"],
                                                c.get("condition")))
            text = "; ".join(only)
            if not text:
                text = "(no fence listed on either side)"
            lines.append("  - core equal, modes differ, %s vs %s: %s"
                         % (b["left"], b["right"], text))
    if not lines:
        return "  - (none)"
    more = len(row["divergence_at_the_border"]) - 6
    if more > 0:
        lines.append("  - ... and %d more" % more)
    return "\n".join(lines)


def md_absent(row):
    lines = []
    for a in row["coverage"]["languages_absent"]:
        lines.append("  - %s: %s" % (a["language"], a["reason"]))
    if not lines:
        return "  - (none: all five languages are present)"
    return "\n".join(lines)


def markdown(out):
    lines = []
    lines.append("# The dominant-operator table")
    lines.append("")
    lines.append("Step 8 of the ratified pipeline "
                 "(`node_0_3_5_compiler_graph`). One row per core "
                 "equivalence class on one operand type pair.")
    lines.append("")
    lines.append("- class definition: %s" % out["class_definition"])
    lines.append("- candidate set: %s" % out["candidate_set"])
    lines.append("- spelling: %s" % out["spelling"])
    lines.append("- intention: %s" % out["intention_note"])
    lines.append("- weakest evidence: %s" % out["weakest_evidence_note"])
    lines.append("- lifter: %s ; z3 %s" % (out["lifter"], out["z3"]))
    lines.append("")
    lines.append("## counts")
    lines.append("")
    lines.append("| what | count |")
    lines.append("|---|---|")
    lines.append("| units considered | %d |" % out["units_considered"])
    lines.append("| classes | %d |" % out["classes"])
    lines.append("| total-equality edges used | %d |" % out["edges_used"])
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
        lines.append("### %s &middot; operand types (%s) &middot; %d "
                     "member(s), %d language(s)"
                     % (row["class_id"], row["type_pair"], row["size"],
                        len(row["languages"])))
        lines.append("")
        lines.append("- members: %s" % md_members(row))
        lines.append("- canonical core (from %s): `%s`"
                     % (row["canonical_core_from"],
                        json.dumps(row["canonical_core"])))
        lines.append("- distinct core texts inside the class: %d"
                     % row["distinct_core_texts"])
        lines.append("- mode inventory:")
        lines.append(md_fences(row))
        lines.append("- divergence at the border:")
        lines.append(md_border(row))
        lines.append("- evidence: %s ; weakest: %s"
                     % (json.dumps(row["evidence"]
                                   ["member_pairs_by_class"]),
                        row["evidence"]["weakest_evidence_text"]))
        lines.append("- languages present: %s"
                     % ", ".join(row["coverage"]["languages_present"]))
        lines.append("- languages absent:")
        lines.append(md_absent(row))
        lines.append("- intention: null; proposed candidate: %s (%s) "
                     "-- %s"
                     % (row["intention_candidates"]["proposed_ur_kind"],
                        row["intention_candidates"]["status"],
                        row["intention_candidates"]["why"]))
        lines.append("")
    return "\n".join(lines) + "\n"


def main(argv):
    indir = HERE
    outdir = HERE
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
        print(__doc__)
        return 2
    build(indir, outdir)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
