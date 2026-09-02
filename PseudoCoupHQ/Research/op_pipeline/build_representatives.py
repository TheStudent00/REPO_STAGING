#!/usr/bin/env python3
"""build_representatives.py -- THE REPRESENTATIVE RULE, applied as a new
additive layer over the 0-branch population (dominant_table17.py's own
1,641 units).

Grounds for union (proved evidence only, no similarity heuristics):

  (a) newest canonical texts (dominant_table17.load_generation_docs /
      final_text_of -- the SAME fall-through chain dominant_table17.py
      itself uses: canon23 -> canon22 -> ... -> canon7) are
      character-identical.

  (b) normalized expressions are character-identical (tree_matches3.
      json's own `exact_normalized_root` clusters -- z3-simplified
      bitvector form, ret-block-first selection, the adopted
      normalizer per that file's own `normalizer` field) AND the two
      units share the class key: (type_pair, machine-fact result type
      via result_type_norm.py). tree_matches3.json's own clusters are
      keyed by type_pair already; this script further splits each
      cluster by RTN.class_family so result-type is enforced too, and
      restricts membership to the 0-branch population.

  (c) a proved cross-unit edge from a prior canon*_behaviour_check
      table. INVESTIGATED AND NOT FOUND: canon20_behaviour_check.py/
      canon21_behaviour_check.py/canon22_behaviour_check.py's own
      `anchored_check` proves a CANDIDATE TEXT equal to THAT SAME
      UNIT's own real ship code (the per-unit convergence gate,
      recorded as canon*_units_<lang>.json's `behaviour_gate`/
      `job1_reanchor` fields) -- it is a single-unit soundness proof,
      not a cross-unit equivalence edge between two different units.
      No table anywhere in this directory stores a proved (unit_X,
      unit_Y) edge distinct from grounds (a)/(b). Ground (c)
      therefore contributes ZERO additional unions in this run; this
      is reported explicitly rather than fabricated.

Byte counts: canon_roundtrip.json's own `units` map gives real
assembled bytes (clang, the same tool named in its own `assembler`
field) keyed "lang/op_N", but for the base canon.py text -- NOT
necessarily this unit's newest converged text. Where the newest text
equals that recorded text exactly, the recorded byte count is reused
directly (ground: canon_roundtrip.json). Where it differs (a later
canon* generation changed the text) or the unit is absent from
canon_roundtrip.json, this script assembles the text itself, same
method roundtrip.py uses (`.text`/`.globl`/`.type`/label/`.size`,
one assembler invocation, `objdump -d` read back) -- SUBSTITUTING
`gcc -c -x assembler` for roundtrip.py's `clang` because this host has
no clang; gcc's assembler-only path (`-c -x assembler`) invokes the
same GNU `as` clang itself shells out to for this target, so the
emitted bytes are the same encoder's output. Noted, not hidden.

usage:
  build_representatives.py
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import dominant_table17 as DT17                                  # noqa: E402
import dom_ops_0branch as DB                                      # noqa: E402
import result_type_norm as RTN                                    # noqa: E402

LANGS = ["c", "cpp", "go", "rust", "swift"]

CC = "gcc"
OBJDUMP = "objdump"
WORK = "/tmp/build_representatives_work"


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


def load_canon4():
    docs = {}
    for lang in LANGS:
        path = os.path.join(HERE, "canon4_units_%s.json" % lang)
        docs[lang] = json.load(open(path))["units"]
    return docs


def main():
    gen_docs = DT17.load_generation_docs()
    units = DT17.load_0branch_units(gen_docs)  # (lang, n, u, text, gen)
    population = len(units)
    print("0-branch population: %d (verified via dominant_table17."
          "load_0branch_units, same call dominant_table17.py's own "
          "main() uses)" % population)

    canon4_docs = load_canon4()

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

    uf = UnionFind()
    for lab in text_of:
        uf.find(lab)

    ground_edges = {}  # frozenset({a,b}) -> set of grounds

    def record_edge(a, b, ground):
        if a == b:
            return
        key = frozenset((a, b))
        ground_edges.setdefault(key, set()).add(ground)

    # ---- ground (a): identical newest canonical text ----
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

    # ---- ground (b): normalized expression identical + class key ----
    matches_doc = json.load(open(os.path.join(HERE, "tree_matches3.json")))
    b_unions = 0
    for cluster in matches_doc["exact_normalized_root"]:
        members = cluster.get("members", [])
        pop_members = []
        for m in members:
            lang, n = m["lang"], m["n"]
            lab = label_of.get((lang, n))
            if lab is None:
                continue  # not in 0-branch population
            pop_members.append(lab)
        if len(pop_members) < 2:
            continue
        # split further by machine-fact result type (RTN), since
        # tree_matches3.json's own key is type_pair only
        by_rtype = {}
        for lab in pop_members:
            lang = lab.split("/op_")[0]
            n = lab.split("/op_")[1]
            fam, note = RTN.class_family(lang, n, meta_of[lab])
            rkey = fam if fam is not None else ("unknown:%s" % note)
            by_rtype.setdefault((type_pair_of[lab], rkey), []).append(lab)
        for (_tp, _rt), labs in by_rtype.items():
            if len(labs) < 2:
                continue
            labs_sorted = sorted(labs)
            first = labs_sorted[0]
            for other in labs_sorted[1:]:
                uf.union(first, other)
                record_edge(first, other, "b")
                b_unions += 1

    # ---- ground (c): investigated, not found (see module docstring) ----
    c_unions = 0

    # ---- assemble groups ----
    groups = {}
    for lab in text_of:
        root = uf.find(lab)
        groups.setdefault(root, []).append(lab)

    print("ground (a) pairwise unions issued: %d" % a_unions)
    print("ground (b) pairwise unions issued: %d" % b_unions)
    print("ground (c) pairwise unions issued: %d (none found; see "
          "docstring)" % c_unions)
    print("groups formed: %d" % len(groups))

    # per-member grounds: which ground(s) touched each member (any edge
    # incident on it, restricted to edges INSIDE its final group)
    member_grounds = {}
    for key, grounds in ground_edges.items():
        a, b = tuple(key)
        if uf.find(a) != uf.find(b):
            continue  # shouldn't happen, both directions unioned together
        member_grounds.setdefault(a, set()).update(grounds)
        member_grounds.setdefault(b, set()).update(grounds)

    # ---- byte counts ----
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

    need_assemble = {}  # text -> None
    byte_source = {}  # lab -> ("canon_roundtrip.json" | "assembled", nbytes)
    for lab, text in text_of.items():
        rt_text, rt_nbytes = rt_text_of(lab)
        if rt_text is not None and rt_text == text:
            byte_source[lab] = ("canon_roundtrip.json", rt_nbytes)
        else:
            need_assemble[text] = None

    print("units needing fresh byte assembly (text not found verbatim "
          "in canon_roundtrip.json): %d distinct texts" % len(need_assemble))

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
            nb = len(out_bytes.get(name, []))
            result[text] = nb
        return result, skipped

    assembled_bytes, assemble_skipped = assemble_texts(list(need_assemble.keys()))
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

    unassemblable = sum(1 for _l, (src, nb) in byte_source.items()
                        if nb is None)
    print("units with no byte count obtainable (unassemblable text): %d"
          % unassemblable)

    # ---- pick representative per group ----
    def sort_key(lab):
        lang, _, n = lab.partition("/op_")
        try:
            nn = int(n)
        except ValueError:
            nn = n
        return (lang, nn)

    out_groups = []
    gi = 0
    for root, members in groups.items():
        gi += 1
        gid = "G%04d" % gi
        # candidates with known byte counts
        with_bytes = [(m, byte_source[m][1]) for m in members
                      if byte_source[m][1] is not None]
        members_sorted = sorted(members, key=sort_key)
        if with_bytes:
            min_b = min(b for _m, b in with_bytes)
            tied = [m for m, b in with_bytes if b == min_b]
            tied_sorted = sorted(tied, key=sort_key)
            rep = tied_sorted[0]
            rep_bytes = min_b
        else:
            rep = members_sorted[0]
            rep_bytes = None
        out_groups.append({
            "group_id": gid,
            "representative": {
                "unit": rep,
                "text": text_of[rep],
                "bytes": rep_bytes,
                "byte_source": byte_source[rep][0],
            },
            "members": [
                {
                    "unit": m,
                    "lang": m.split("/op_")[0],
                    "n": m.split("/op_")[1],
                    "text": text_of[m],
                    "bytes": byte_source[m][1],
                    "byte_source": byte_source[m][0],
                    "grounds": sorted(member_grounds.get(m, set())),
                }
                for m in members_sorted
            ],
            "distinct_texts_in_group": sorted(set(text_of[m]
                                              for m in members)),
        })

    out_groups.sort(key=lambda g: (-len(g["members"]), g["group_id"]))

    doc = {
        "meta": {
            "role_note": "this file IS a GROUPING/matching artifact "
                        "(top-level `groups`, each with `members`) -- "
                        "it does NOT claim the generator-provenance "
                        "exemption; checked by check_no_spelling_keys."
                        "py IN FULL.",
            "generator": "build_representatives.py",
            "note": "additive layer: does not modify/overwrite any raw "
                   "extraction. THE REPRESENTATIVE RULE per AgentMemory "
                   "2026-08-29: fewest machine bytes, ties by (lang, "
                   "unit id) order.",
            "population": population,
            "grounds": {
                "a": "newest canonical text (dominant_table17 fall-"
                    "through chain) character-identical -- %d pairwise "
                    "unions" % a_unions,
                "b": "tree_matches3.json exact_normalized_root cluster, "
                    "further split by (type_pair, result_type_norm."
                    "class_family), restricted to 0-branch population "
                    "-- %d pairwise unions" % b_unions,
                "c": "investigated: canon20/21/22_behaviour_check.py's "
                    "anchored_check proves a candidate text equal to "
                    "THAT UNIT's own ship code (single-unit soundness), "
                    "not a cross-unit edge; no cross-unit proved-edge "
                    "table exists in this directory -- 0 unions",
            },
        },
        "groups": out_groups,
    }
    out_path = os.path.join(HERE, "representatives.json")
    json.dump(doc, open(out_path, "w"), indent=1)
    print("wrote %s" % out_path)

    sizes = {}
    multi_text_groups = 0
    for g in out_groups:
        s = len(g["members"])
        sizes[s] = sizes.get(s, 0) + 1
        if len(g["distinct_texts_in_group"]) > 1:
            multi_text_groups += 1
    print("group size histogram: %r" % sorted(sizes.items()))
    print("groups with >1 distinct canonical text among members: %d"
          % multi_text_groups)
    largest = max(len(g["members"]) for g in out_groups)
    print("largest group size: %d" % largest)


if __name__ == "__main__":
    main()
