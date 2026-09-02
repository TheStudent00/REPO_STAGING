#!/usr/bin/env python3
"""build_table24.py -- TASK 7 (log_083/log_090): reconcile the two
table lineages (dominant_table22/dom_ops20 vs dominant_table23c/
dom_ops21c) into ONE table, dominant_table24.json / dom_ops22.json.

THE DIVERGENCE THIS FILE CLOSES (PROGRESS.md 2026-08-29..31,
AgentMemory THE REPRESENTATIVE RULE): table22's lineage applies THE
REPRESENTATIVE RULE (proved-equal units share one canonical text, the
group's simplest member) but its text comes from representatives5
.json, built BEFORE canon24 existed and before this session's
proved_edges3.json (84+4 new proofs). table23's lineage carries
canon24-newest text but does NOT apply the representative rule at
all -- it uses each unit's OWN newest text as the class key, so
proved-equal units with different renderer output form separate
classes. Neither lineage alone is both currents at once. This file
is both: canon24-newest text AS THE GROUND, representative
substitution rebuilt on proved_edges.json + proved_edges2.json +
proved_edges3.json (all three, union), full population, both rounds
of resolved seeds (seeds2.json, additive superset of seeds1.json).

METHOD, five steps.

STEP 1 -- 0-branch population, canon24-newest text. Reuses
dominant_table17.load_generation_docs/load_0branch_units UNCHANGED,
monkeypatched exactly as build_table23.py did (canon24 prepended to
the fall-through order). 1,641 units, one newest-generation text
each.

STEP 2 -- representative substitution, REBUILT on this session's
full proof state. Union-find over three grounds, the same three
grounds build_representatives5.py used, re-run here because ground
(a)'s input text changed (canon24 now included) and ground (c)'s
input proofs changed (proved_edges3.json, this session's 84 direct +
4 transitive proofs, was never unioned into any representatives*.json
on disk):
  (a) newest (canon24-included) text character-identical.
  (b) normal_path_raw3 (constant-substituted raw expression,
      build_representatives4/5.py's own substitute_constants
      function, imported unchanged) character-identical, split by
      (type_pair, result_type).
  (c) proved_edges.json UNION proved_edges2.json UNION
      proved_edges3.json, verdict PROVED or PROVED_TRANSITIVE only.
Each group's representative is the fewest-machine-bytes member (tie
broken by (lang, unit id) order) -- AgentMemory THE REPRESENTATIVE
RULE, unchanged rule, freshly applied. EVERY member of a group
(not only the representative) is re-keyed onto the representative's
text for class formation -- that is what makes proved-equal units
with different rendered text land in the SAME class row, closing the
table23-lineage gap named above.

STEP 3 -- class rows: (type_pair, result_type, representative_text)
over the re-keyed 0-branch population. Ground (b) is *_norm; ground
(c) is machine-fact result_type_norm.class_family, never the operator
spelling.

STEP 4 -- branching units. seeds2.json (additive superset of
seeds1.json: 66 "ok" seeds = seeds1's original 32 + this session's 34
c/cpp conversion-idiom seeds) is joined to a class row whose
canonical_text equals the seed's seed_text EXACTLY -- text equality
against the now-representative-substituted canonical text, so a seed
whose match depended on representatives5.json's now-stale text is
re-resolved honestly against the current text. A seed matching no row
or more than one row is left OUT, recorded, never guessed.

STEP 5 -- dom_ops22 over the full table, dom_ops_0branch.py's
provenance-fallback pattern (canon4 unit when available, else
op_units_<lang>.json's own meta) reused unchanged from
build_table23c.py so branching units are visible to family formation.

THE SPELLING BAN: dominant_table24.json's class key is (type_pair,
result_type, text) -- never the operator token -- and it is checked
by check_no_spelling_keys.py WITHOUT the provenance exemption, per
the task brief. dom_ops22.json carries `display_label` per node
(ratified node identity) exactly as dom_ops20/21/21c do, and may use
the SAME provenance exemption those files use.

usage:
  build_table24.py [--out DIR]
"""
import argparse
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dominant_table17 as DT17                                  # noqa: E402
import dom_ops as DO                                              # noqa: E402
import dom_ops_0branch as DB                                      # noqa: E402
import result_type_norm as RTN                                    # noqa: E402

DT17.GENERATIONS = ["canon24"] + DT17.GENERATIONS
DT17.BRANCH_CHECK_GENERATIONS = tuple(
    ["canon24"] + list(DT17.BRANCH_CHECK_GENERATIONS))

LANGS = ["c", "cpp", "go", "rust", "swift"]
CC = "gcc"
OBJDUMP = "objdump"
WORK = "/tmp/build_table24_work"

LOAD_RE = re.compile(r"ld(32|64)/g0\((\d+):64\)")
MOV32_RE = re.compile(r"(?:^|;)\s*mov\s+\$(-?\d+)\s*,")
MOVABS64_RE = re.compile(r"(?:^|;)\s*movabs\s+\$(-?\d+)\s*,")
BARE_ATOM_RE = re.compile(r"^(op|atom)_[0-9]+$")


def is_bare_opaque_atom(raw_text):
    if raw_text is None:
        return True
    return BARE_ATOM_RE.match(raw_text.strip()) is not None


def substitute_constants(raw_text, canon_text):
    """Unchanged from build_representatives4/5.py."""
    if raw_text is None:
        return raw_text, []
    loads = list(LOAD_RE.finditer(raw_text))
    if not loads:
        return raw_text, []
    mov32_vals = [int(x) for x in MOV32_RE.findall(canon_text or "")]
    movabs_vals = [int(x) for x in MOVABS64_RE.findall(canon_text or "")]
    subs = []
    out = raw_text
    for m in reversed(loads):
        width = m.group(1)
        candidates = mov32_vals if width == "32" else \
            (movabs_vals if width == "64" else [])
        if len(candidates) != 1:
            continue
        value = candidates[0]
        out = out[:m.start()] + ("const%s(%d)" % (width, value)) + \
            out[m.end():]
        subs.append((m.group(0), width, value))
    return out, subs


class UnionFind(object):
    def __init__(self):
        self.parent = {}

    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.parent[ra] = rb


def load_raw_normal_paths():
    doc = json.load(open(os.path.join(HERE, "tree_units3.json")))
    out = {}
    for rec in doc["units"]:
        out[(rec["lang"], rec["n"])] = rec.get("normal_path_raw")
    return out


def sort_key(lab):
    lang, _, n = lab.partition("/op_")
    try:
        nn = int(n)
    except ValueError:
        nn = n
    return (lang, nn)


def build_representative_groups(units):
    """Returns (rep_text_of: label -> representative text,
    member_grounds: label -> sorted list of grounds,
    group_report: list of group summaries for the artifact)."""
    label_of = {}
    text_of = {}
    meta_of = {}
    type_pair_of = {}
    for lang, n, u, text, gen in units:
        lab = "%s/op_%s" % (lang, n)
        label_of[(lang, n)] = lab
        text_of[lab] = text
        meta_of[lab] = u.get("meta")
        type_pair_of[lab] = DB.type_pair_of(u)

    raw_of = load_raw_normal_paths()
    raw3_of = {}
    for lab in text_of:
        lang, _, n = lab.partition("/op_")
        raw = raw_of.get((lang, n))
        raw3, _subs = substitute_constants(raw, text_of[lab])
        raw3_of[(lang, n)] = raw3

    uf = UnionFind()
    for lab in text_of:
        uf.find(lab)
    ground_edges = {}

    def record_edge(a, b, ground):
        if a == b:
            return
        key = frozenset((a, b))
        ground_edges.setdefault(key, set()).add(ground)

    # ground (a)
    by_text = {}
    for lab, text in text_of.items():
        by_text.setdefault(text, []).append(lab)
    a_unions = 0
    for text, labs in by_text.items():
        if len(labs) < 2:
            continue
        labs_sorted = sorted(labs)
        first = labs_sorted[0]
        for other in labs_sorted[1:]:
            uf.union(first, other)
            record_edge(first, other, "a")
            a_unions += 1

    # ground (b)
    by_raw = {}
    missing_raw = 0
    bare_atom_skipped = 0
    for lab in text_of:
        lang, _, n = lab.partition("/op_")
        raw3 = raw3_of.get((lang, n))
        if raw3 is None:
            missing_raw += 1
            continue
        if is_bare_opaque_atom(raw3):
            bare_atom_skipped += 1
            continue
        by_raw.setdefault(raw3, []).append(lab)
    b_unions = 0
    for raw3, labs in by_raw.items():
        if len(labs) < 2:
            continue
        by_rtype = {}
        for lab in labs:
            lang = lab.split("/op_")[0]
            n = lab.split("/op_")[1]
            fam, note = RTN.class_family(lang, n, meta_of[lab])
            rkey = fam if fam is not None else ("unknown:%s" % note)
            by_rtype.setdefault((type_pair_of[lab], rkey), []).append(lab)
        for _key, same in by_rtype.items():
            if len(same) < 2:
                continue
            same_sorted = sorted(same)
            first = same_sorted[0]
            for other in same_sorted[1:]:
                uf.union(first, other)
                record_edge(first, other, "b")
                b_unions += 1

    # ground (c) -- proved_edges.json UNION 2 UNION 3, this file's
    # own extension: PROVED and PROVED_TRANSITIVE both count as
    # proofs (transitive closure over already-PROVED pairs is not a
    # weaker proof, it costs no new solver call because the union-find
    # itself performs the closure -- proved_edges3.json's own meta
    # records this distinction, never re-derived here).
    c_unions = 0
    c_pairs_used = []
    seen_pairs = set()
    proved_paths = ["proved_edges.json", "proved_edges2.json",
                     "proved_edges3.json"]
    for pp in proved_paths:
        path = os.path.join(HERE, pp)
        if not os.path.exists(path):
            continue
        doc = json.load(open(path))
        for pair in doc["pairs"]:
            v = pair.get("verdict")
            if v not in ("PROVED", "PROVED_TRANSITIVE"):
                continue
            a, b = pair["a"], pair["b"]
            key = frozenset((a, b))
            if key in seen_pairs:
                continue
            seen_pairs.add(key)
            if a not in text_of or b not in text_of:
                continue
            uf.union(a, b)
            record_edge(a, b, "c")
            c_unions += 1
            c_pairs_used.append({"a": a, "b": b, "source": pp,
                                  "verdict": v})

    groups = {}
    for lab in text_of:
        root = uf.find(lab)
        groups.setdefault(root, []).append(lab)

    member_grounds = {}
    for key, grounds in ground_edges.items():
        a, b = tuple(key)
        if uf.find(a) != uf.find(b):
            continue
        member_grounds.setdefault(a, set()).update(grounds)
        member_grounds.setdefault(b, set()).update(grounds)

    # byte counts: canon_roundtrip.json first, gcc+objdump fallback --
    # unchanged from build_representatives5.py
    rt_doc = json.load(open(os.path.join(HERE, "canon_roundtrip.json")))
    rt_units = rt_doc["units"]

    def rt_text_of(lab):
        rec = rt_units.get(lab)
        if rec is None:
            return None, None
        mnem = rec.get("canon_mnem")
        if not mnem:
            return None, None
        return "; ".join(mnem), len(rec.get("canon_bytes") or [])

    byte_source = {}
    need_assemble = {}
    for lab, text in text_of.items():
        rt_text, rt_nbytes = rt_text_of(lab)
        if rt_text is not None and rt_text == text:
            byte_source[lab] = ("canon_roundtrip.json", rt_nbytes)
        else:
            need_assemble[text] = None

    def assemble_texts(texts):
        os.makedirs(WORK, exist_ok=True)
        spath = os.path.join(WORK, "reps.s")
        opath = os.path.join(WORK, "reps.o")
        lines_out = ["        .text"]
        label_map = {}
        skipped = {}
        i = 0
        for text in texts:
            lines = [ln.strip() for ln in text.split(";") if ln.strip()]
            bad = None
            for ln in lines:
                if "<" in ln:
                    bad = "the text names a branch target the extract " \
                          "does not carry"
                elif "!!reloc" in ln:
                    bad = "the text carries a relocation note"
                elif "(%rip)" in ln:
                    bad = "the text carries a rip-relative operand"
                elif "#" in ln:
                    bad = "the text carries a disassembler comment"
                if bad:
                    break
            if bad:
                skipped[text] = bad
                continue
            i += 1
            name = "rep_%d" % i
            label_map[name] = text
            lines_out.append("        .globl %s" % name)
            lines_out.append("        .type %s, @function" % name)
            lines_out.append("%s:" % name)
            for ln in lines:
                lines_out.append("        %s" % ln)
            lines_out.append("        .size %s, .-%s" % (name, name))
        open(spath, "w").write("\n".join(lines_out) + "\n")
        if not label_map:
            return {}, skipped
        cmd = [CC, "-c", "-x", "assembler", spath, "-o", opath]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError("assembly failed: %s" % proc.stderr[:2000])
        cmd = [OBJDUMP, "-d", opath]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            raise RuntimeError("objdump failed: %s" % proc.stderr[:2000])
        SYM = re.compile(r"^[0-9a-f]+ <([^>]+)>:")
        LINE = re.compile(r"^\s*([0-9a-f]+):\s*((?:[0-9a-f]{2} )+)")
        out_bytes = {}
        current = None
        for line in proc.stdout.splitlines():
            m = SYM.match(line)
            if m:
                current = m.group(1)
                out_bytes[current] = []
                continue
            if current is None:
                continue
            m = LINE.match(line)
            if m:
                out_bytes[current].extend(m.group(2).split())
        result = {}
        for name, text in label_map.items():
            result[text] = len(out_bytes.get(name, []))
        return result, skipped

    assembled_bytes, assemble_skipped = assemble_texts(
        list(need_assemble.keys()))
    for lab, text in text_of.items():
        if lab in byte_source:
            continue
        if text in assembled_bytes:
            byte_source[lab] = ("assembled(gcc -c -x assembler + objdump)",
                                assembled_bytes[text])
        elif text in assemble_skipped:
            byte_source[lab] = ("UNASSEMBLABLE: %s" % assemble_skipped[text],
                                None)
        else:
            byte_source[lab] = ("UNKNOWN", None)

    rep_text_of = {}
    group_report = []
    gi = 0
    for root, members in groups.items():
        gi += 1
        gid = "G%04d" % gi
        with_bytes = [(m, byte_source[m][1]) for m in members
                      if byte_source[m][1] is not None]
        members_sorted = sorted(members, key=sort_key)
        if with_bytes:
            min_b = min(b for _m, b in with_bytes)
            tied = sorted([m for m, b in with_bytes if b == min_b],
                          key=sort_key)
            rep = tied[0]
            rep_bytes = min_b
        else:
            rep = members_sorted[0]
            rep_bytes = None
        for m in members:
            rep_text_of[m] = text_of[rep]
        group_report.append({
            "group_id": gid,
            "representative": {"unit": rep, "text": text_of[rep],
                                "bytes": rep_bytes,
                                "byte_source": byte_source[rep][0]},
            "members": [
                {"unit": m, "own_text": text_of[m],
                 "bytes": byte_source[m][1],
                 "grounds": sorted(member_grounds.get(m, set()))}
                for m in members_sorted
            ],
            "distinct_own_texts_in_group":
                sorted(set(text_of[m] for m in members)),
        })
    group_report.sort(key=lambda g: (-len(g["members"]), g["group_id"]))

    meta = {
        "grounds": {
            "a": "%d pairwise unions (newest, canon24-included, text "
                 "character-identical)" % a_unions,
            "b": "%d pairwise unions (normal_path_raw3 constant-"
                 "substituted, split by type_pair+result_type; %d "
                 "missing raw, %d bare-opaque-atom refused)"
                 % (b_unions, missing_raw, bare_atom_skipped),
            "c": "%d pairwise unions (proved_edges.json UNION "
                 "proved_edges2.json UNION proved_edges3.json, "
                 "PROVED/PROVED_TRANSITIVE only)" % c_unions,
        },
        "groups_formed": len(groups),
        "proved_pairs_used": c_pairs_used,
    }
    return rep_text_of, meta, group_report, text_of


def build_0branch_rows(units, rep_text_of):
    prov = {}
    classes = {}
    unknown_result_type = 0
    generation_tally = {}
    for lang, n, u, text, gen in units:
        label = "%s/op_%s" % (lang, n)
        prov[label] = {
            "lang": lang, "n": n,
            "display_label": u.get("operator"),
            "arity_bucket": DB.arity_bucket_of(u),
        }
        generation_tally[gen] = generation_tally.get(gen, 0) + 1
        tkey = DB.type_pair_of(u)
        fam, note = RTN.class_family(lang, n, u.get("meta"))
        rkey = fam if fam is not None else ("unknown(%s)" % note[:40])
        rep_text = rep_text_of.get(label, text)
        ckey = (tkey, rkey, rep_text)
        classes.setdefault(ckey, {"type_pair": tkey, "text": rep_text,
                                   "members": []})
        classes[ckey]["members"].append({
            "unit": label,
            "own_text_before_representative_substitution": text,
        })
    rows = []
    for i, ckey in enumerate(sorted(classes.keys()), start=1):
        rec = classes[ckey]
        rows.append({
            "class_id": "C%04d" % i,
            "type_pair": rec["type_pair"],
            "result_type": ckey[1],
            "canonical_text": rec["text"],
            "members": rec["members"],
        })
    return prov, rows, unknown_result_type, generation_tally


def add_branching_members(rows):
    """Seed-text equality is tried against TWO pools on each row: its
    representative (post-substitution) canonical_text, AND every
    0-branch member's own pre-substitution text (carried on the row
    as `own_text_before_representative_substitution`). Both source
    lineages' seed matches were built against a PRE-representative-
    substitution text (table22 against representatives5.json's own
    text, table23c against canon24-newest-own text) -- restricting
    match to the representative text alone would silently regress
    both, dropping seed joins the representative rule's text-merging
    did not itself invalidate. A row is still one candidate: if a
    seed's text hits two DIFFERENT rows across either pool, that is
    ambiguity, honestly reported, not resolved by preference order."""
    seeds = json.load(open(os.path.join(HERE, "seeds2.json")))["seeds"]
    text_to_rows = {}

    def add_text(text, row):
        text_to_rows.setdefault(text, set()).add(row["class_id"])

    row_by_id = {row["class_id"]: row for row in rows}
    for row in rows:
        add_text(row["canonical_text"], row)
        for m in row["members"]:
            own = m.get("own_text_before_representative_substitution")
            if own is not None:
                add_text(own, row)

    added, unmatched, ambiguous = [], [], []
    for unit_id, s in sorted(seeds.items()):
        if s.get("status") != "ok":
            continue
        seed_text = s.get("seed_text")
        candidate_ids = sorted(text_to_rows.get(seed_text, set()))
        if len(candidate_ids) == 0:
            unmatched.append({"unit": unit_id, "seed_text": seed_text})
            continue
        if len(candidate_ids) > 1:
            ambiguous.append({"unit": unit_id, "seed_text": seed_text,
                               "candidate_classes": candidate_ids})
            continue
        row = row_by_id[candidate_ids[0]]
        row["members"].append({
            "unit": unit_id, "branching": True,
            "seed_text": s["seed_text"], "seed_method": s["method"],
            "guards": s.get("guards", []),
        })
        added.append((unit_id, row["class_id"]))
    return added, unmatched, ambiguous


def load_canon4(lang, cache):
    if lang not in cache:
        path = os.path.join(HERE, "canon4_units_%s.json" % lang)
        cache[lang] = json.load(open(path))["units"]
    return cache[lang]


def build_provenance(rows):
    """Same fallback pattern build_table23c.py used: canon4 unit when
    the label is a 0-branch unit, else op_units_<lang>.json's own
    meta for a branching unit."""
    prov = {}
    canon4_cache = {}
    opunits_cache = {}
    for row in rows:
        for m in row["members"]:
            label = m["unit"]
            if label in prov:
                continue
            lg, num = label.split("/op_")
            units = load_canon4(lg, canon4_cache)
            u4 = units.get(num)
            if u4 is not None:
                display = u4.get("meta", {}).get("operator") or \
                    u4.get("operator")
                arity = DB.arity_bucket_of(u4)
            else:
                if lg not in opunits_cache:
                    op_path = os.path.join(HERE, "op_units_%s.json" % lg)
                    opunits_cache[lg] = json.load(open(op_path))
                opd = opunits_cache[lg]
                rec = opd.get("units", {}).get(num, {})
                display = rec.get("meta", {}).get("operator")
                arity = "binary"
            prov[label] = {"lang": lg, "n": num, "display_label": display,
                           "arity_bucket": arity}
    return prov


def run_dom_ops(rows, prov):
    doc = {"table": {"rows": rows}}
    nodes, index = DO.build_nodes(doc, prov)
    class_members = DO.fill_nodes(doc, nodes, index, prov)
    edges = DO.build_edges(doc, nodes, class_members, 0)
    best, ties = DO.best_per_language(nodes, edges)
    kept = DO.mutual_edges(nodes, edges, best)
    comps = DO.components(kept)
    DO.assert_one_per_language(nodes, comps)

    singleton_count = sum(1 for c in comps if len(c) == 1)
    attached = set()
    for c in comps:
        attached.update(c)
    unattached = sorted(set(nodes.keys()) - attached)
    family_rows = []
    for members in comps:
        family_rows.append({
            "dom_op_id": "D%04d" % (len(family_rows) + 1),
            "size": len(members),
            "nodes": [DB.node_row(nodes, nid) for nid in members],
        })
    family_rows.sort(key=lambda r: r["size"], reverse=True)
    return nodes, {
        "nodes": len(nodes), "edges_raw": len(edges),
        "edges_mutual": len(kept), "dom_op_count": len(comps),
        "singleton_dom_ops": singleton_count,
        "nodes_in_a_dom_op": len(attached),
        "nodes_with_no_surviving_edge": len(unattached),
        "unattached_nodes": unattached,
        "families": family_rows,
    }


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=HERE)
    args = ap.parse_args(argv)

    gen_docs = DT17.load_generation_docs()
    units = DT17.load_0branch_units(gen_docs)
    population_0branch = len(units)

    rep_text_of, rep_meta, group_report, own_text_of = \
        build_representative_groups(units)

    prov0, rows, unknown_result_type, generation_tally = \
        build_0branch_rows(units, rep_text_of)

    added, unmatched, ambiguous = add_branching_members(rows)

    class_doc = {
        "generator": "build_table24.py",
        "role_note": "GROUPING/matching artifact (top-level `rows`, "
                     "each with `members`) -- checked by check_no_"
                     "spelling_keys.py IN FULL, no exemption claimed "
                     "(task brief requirement).",
        "lineage": "reconciliation of dominant_table22.json/dom_ops20"
                   ".json (full population, representative rule, "
                   "pre-canon24 representatives5.json) and dominant_"
                   "table23c.json/dom_ops21c.json (canon24-newest "
                   "text, no representative rule, seeds1+seeds2) -- "
                   "see build_table24.py docstring for the method.",
        "population": "1,779 full corpus: %d 0-branch units (canon24-"
                     "included newest text, then representative-"
                     "substituted) + %d branching units joined by "
                     "seed-text equality against the representative-"
                     "substituted class text (seeds2.json, 66 "
                     "resolved seeds attempted, %d matched, %d "
                     "unmatched, %d ambiguous)"
                     % (population_0branch, len(added), len(added),
                        len(unmatched), len(ambiguous)),
        "representative_rule": rep_meta,
        "generation_tally": generation_tally,
        "unknown_result_type_units": unknown_result_type,
        "classes_before_branching": len(rows),
        "unmatched_branching_seeds": unmatched,
        "ambiguous_branching_seeds": ambiguous,
        "rows": rows,
    }

    prov = build_provenance(rows)
    nodes, dom_ops_result = run_dom_ops(rows, prov)

    # ---- UNRECONCILED BIN (STOP RULE): units that had a cross-
    # language dom_op family placement in EITHER source lineage
    # (dom_ops20.json / dom_ops21c.json) but do not land in any
    # table24 family, because their seed's proved-equal target text
    # was produced by a text-consolidation rule (representatives5
    # .json's grouping for table22; table23b.py's own proved-edge
    # consolidation for table23c) that this file's own
    # representative-groups step does not reproduce character-for-
    # character. Named, not silently dropped -- see log_090. ----
    def family_units(fams):
        out = {}
        for f in fams:
            us = set()
            for n in f["nodes"]:
                us.update(n.get("units", []))
            for u in us:
                out[u] = f["dom_op_id"]
        return out

    fam24 = family_units(dom_ops_result["families"])
    d20 = json.load(open(os.path.join(HERE, "dom_ops20.json")))
    d21c = json.load(open(os.path.join(HERE, "dom_ops21c.json")))
    fam20 = family_units(d20["dom_ops"])
    fam21c = family_units(d21c["families"])

    unreconciled = []
    seen = set()
    for src_name, fam_src in (("dom_ops20.json (table22 lineage)", fam20),
                               ("dom_ops21c.json (table23c lineage)",
                                fam21c)):
        for unit, fam_id in fam_src.items():
            if unit in fam24 or unit in seen:
                continue
            if unit not in fam21c and unit not in fam20:
                continue
            seen.add(unit)
            unreconciled.append({
                "unit": unit,
                "family_in_source_lineage": fam_id,
                "source_lineage": src_name,
                "status_in_table24": "unmatched" if any(
                    r["unit"] == unit for r in unmatched) else (
                    "ambiguous" if any(r["unit"] == unit
                                       for r in ambiguous) else
                    "not a branching seed unit / not attempted"),
                "cause": "the seed's proved-equal target text was "
                        "produced by a text-consolidation rule "
                        "(representatives5.json's pre-canon24 "
                        "grouping, or table23b.py's own proved-edge "
                        "consolidation) that this file's "
                        "representative-groups step (canon24 text + "
                        "proved_edges.json/2/3 union-find) does not "
                        "reproduce character-for-character -- an "
                        "un-ratified method question (which text-"
                        "consolidation rule is canonical for a seed "
                        "match target), not resolved here per the "
                        "task's STOP RULE.",
            })
    unreconciled.sort(key=lambda r: r["unit"])
    class_doc["unreconciled_branching_units"] = unreconciled
    class_doc["unreconciled_branching_units_count"] = len(unreconciled)

    class_path = os.path.join(args.out, "dominant_table24.json")
    json.dump(class_doc, open(class_path, "w"), indent=1)

    dom_ops_doc = {
        "meta": {
            "generator": "build_table24.py (dom_ops22.json)",
            "role": "generator provenance -- carries `display_label` "
                    "per node (ratified node identity), same "
                    "provenance exemption dom_ops20/21/21c use.",
            "construction": "dom_ops7.py's rule, unchanged (via "
                            "dom_ops_0branch.py / dom_ops.py, "
                            "imported not restated).",
            "source_table": "dominant_table24.json",
        },
        "class_count": len(rows),
    }
    dom_ops_doc.update(dom_ops_result)
    dom_ops_path = os.path.join(args.out, "dom_ops22.json")
    json.dump(dom_ops_doc, open(dom_ops_path, "w"), indent=1)

    group_path = os.path.join(args.out, "representatives24.json")
    json.dump({"meta": rep_meta, "groups": group_report},
               open(group_path, "w"), indent=1)

    print(json.dumps({
        "population_0branch": population_0branch,
        "classes": len(rows),
        "nodes": dom_ops_result["nodes"],
        "dom_op_count": dom_ops_result["dom_op_count"],
        "edgeless": dom_ops_result["nodes_with_no_surviving_edge"],
        "singleton_dom_ops": dom_ops_result["singleton_dom_ops"],
        "branching_added": len(added),
        "branching_unmatched": len(unmatched),
        "branching_ambiguous": len(ambiguous),
        "groups_formed": rep_meta["groups_formed"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
