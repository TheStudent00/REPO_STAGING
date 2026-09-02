#!/usr/bin/env python3
"""build_representatives2.py -- THE REPRESENTATIVE RULE, applied
correctly. Fixes build_representatives.py's ground (b), which is
CONFIRMED DEFECTIVE (AgentMemory, THE DEFECT, 2026-08-29 record):
it compared tree_matches3.json's `exact_normalized_root` clusters --
a z3-SIMPLIFIED bitvector form in which every unmodelled operation
(any call/instruction this lifter table has no entry for) collapses
to an opaque placeholder atom (`op_N` / `atom_N`). Two DIFFERENT
computations whose unmodelled cores both landed on a placeholder
compared EQUAL under that key. Measured proof, re-confirmed here:
tree_units3.json's own stored `normal_path_root` for c/op_130 (`+`)
and c/op_166 (`-`) on f64,f64 is the SAME bare atom, `op_2`, in both
records -- while their `normal_path_raw` (the pre-simplification
form, no unmodelled-collapse) is `Add64F0x2(ex128@0(in0:256),
ex128@0(in1:256))` for op_130 and `Sub64F0x2(ex128@0(in0:256),
ex128@0(in1:256))` for op_166 -- visibly different outermost
operations, correctly.

Grounds for union (proved evidence only, no similarity heuristics):

  (a) newest canonical texts (dominant_table17.load_generation_docs /
      final_text_of -- the SAME fall-through chain dominant_table17.py
      itself uses: canon23 -> canon22 -> ... -> canon7) are
      character-identical. UNCHANGED from build_representatives.py.

  (b) FIXED HERE. Compares tree_units3.json's own `normal_path_raw`
      field -- the RAW normalized expression, stored BEFORE the z3
      simplification/opaque-atom-collapse step (tree_units3.json's
      own `normalizer` field names the simplify step; `normal_path_raw`
      is the earlier field on the SAME record, read directly, not
      re-derived). Two units union under ground (b) only when their
      `normal_path_raw` strings are CHARACTER-IDENTICAL AND they share
      the class key (type_pair, machine-fact result type via
      result_type_norm.py) -- same restriction build_representatives.py
      already applied, kept unchanged; only the compared string
      changed. A unit whose `normal_path_raw` is a BARE opaque
      placeholder alone (matches `^(op|atom)_[0-9]+$` after stripping
      whitespace, i.e. the entire raw expression is nothing but one
      unmodelled atom, no surrounding structure) is REFUSED as a
      grounding value for this axis -- it can still be identical to
      itself as text, but such identity is never trusted to prove two
      DIFFERENT units equivalent, because a bare placeholder carries
      no information about what was computed. (Measured over the full
      1,779-unit corpus: zero records hit this shape in
      `normal_path_raw` -- see the printed count below -- so the
      refusal is a guard against a case that does not currently occur,
      not an active exclusion; it stays because the field's shape is
      not guaranteed to hold as the corpus grows.)

  (c) a proved cross-unit edge from a prior canon*_behaviour_check
      table. INVESTIGATED AND NOT FOUND, EXACTLY AS build_
      representatives.py RECORDED: canon20/21/22_behaviour_check.py's
      own `anchored_check` proves a CANDIDATE TEXT equal to THAT SAME
      UNIT's own real ship code (the per-unit convergence gate) -- a
      single-unit soundness proof, not a cross-unit equivalence edge.
      No table anywhere in this directory stores a proved (unit_X,
      unit_Y) edge distinct from grounds (a)/(b). Ground (c)
      contributes ZERO additional unions in this run, same as last
      lap; reported explicitly, not fabricated, and kept WIRED (the
      union call sits in the code, even though it never fires) so a
      future proved-edge table only has to be plugged in, not written.

Byte counts: identical method to build_representatives.py (canon_
roundtrip.json reuse where the newest text matches verbatim, else
fresh gcc -c -x assembler + objdump assembly) -- see that file's
docstring for the full account; not restated here since the method
did not change.

usage:
  build_representatives2.py
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
WORK = "/tmp/build_representatives2_work"

BARE_ATOM_RE = re.compile(r"^(op|atom)_[0-9]+$")


def is_bare_opaque_atom(raw_text):
    """the entire raw expression is nothing but one unmodelled
    placeholder atom -- no surrounding structure, no information
    about what was computed. Such a text may never GROUND an
    equivalence, per this lap's brief item 1."""
    if raw_text is None:
        return True
    return BARE_ATOM_RE.match(raw_text.strip()) is not None


def outermost_op(raw_text):
    """the head token of a normal_path_raw expression -- the
    substring up to its first '(' (or the whole string, if it has
    none, i.e. it is a bare atom or leaf). Used ONLY for the
    post-hoc sanity assertion in main(); never a grouping/matching
    key -- see check_no_spelling_keys.py's own definition of what a
    key is (operator TOKENS, not internal lifter opcode names; this
    guard is about the DEFECT -- cross-computation false merges --
    not about the spelling ban, a separate concern)."""
    if raw_text is None:
        return None
    idx = raw_text.find("(")
    if idx == -1:
        return raw_text.strip()
    return raw_text[:idx].strip()


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


def load_raw_normal_paths():
    """tree_units3.json's own `normal_path_raw` per (lang, n) --
    the pre-simplification field, read directly, never re-derived."""
    doc = json.load(open(os.path.join(HERE, "tree_units3.json")))
    out = {}
    for rec in doc["units"]:
        out[(rec["lang"], rec["n"])] = rec.get("normal_path_raw")
    return out


def main():
    gen_docs = DT17.load_generation_docs()
    units = DT17.load_0branch_units(gen_docs)  # (lang, n, u, text, gen)
    population = len(units)
    print("0-branch population: %d (verified via dominant_table17."
          "load_0branch_units, same call dominant_table17.py's own "
          "main() uses)" % population)

    canon4_docs = load_canon4()
    raw_of = load_raw_normal_paths()

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

    # ---- ground (b), FIXED: raw normalized expression identical +
    # class key, over tree_units3.json's normal_path_raw (pre-
    # simplification -- no unmodelled-op collapse) ----
    bare_atom_skipped = 0
    missing_raw = 0
    by_raw = {}
    for lab in text_of:
        lang, _, n = lab.partition("/op_")
        raw = raw_of.get((lang, n))
        if raw is None:
            missing_raw += 1
            continue
        if is_bare_opaque_atom(raw):
            bare_atom_skipped += 1
            continue
        by_raw.setdefault(raw, []).append(lab)

    print("ground (b): %d population labels had no normal_path_raw "
          "in tree_units3.json (excluded from this ground, not "
          "unioned on it)" % missing_raw)
    print("ground (b): %d population labels' normal_path_raw is a "
          "bare opaque placeholder atom alone -- REFUSED as a "
          "grounding value (item 1 of this lap's brief)"
          % bare_atom_skipped)

    b_unions = 0
    for raw, labs in by_raw.items():
        if len(labs) < 2:
            continue
        # split further by machine-fact result type (RTN) and by
        # type_pair, same restriction build_representatives.py's
        # ground (b) already applied via tree_matches3.json's own
        # type_pair key -- here derived directly since we are not
        # going through that file at all.
        by_rtype = {}
        for lab in labs:
            lang = lab.split("/op_")[0]
            n = lab.split("/op_")[1]
            fam, note = RTN.class_family(lang, n, meta_of[lab])
            rkey = fam if fam is not None else ("unknown:%s" % note)
            by_rtype.setdefault((type_pair_of[lab], rkey), []).append(lab)
        for (_tp, _rt), same_key_labs in by_rtype.items():
            if len(same_key_labs) < 2:
                continue
            labs_sorted = sorted(same_key_labs)
            first = labs_sorted[0]
            for other in labs_sorted[1:]:
                uf.union(first, other)
                record_edge(first, other, "b")
                b_unions += 1

    # ---- ground (c): investigated, not found (see module docstring)
    # -- WIRED but contributes zero unions, exactly as build_
    # representatives.py recorded. No cross-unit proved-edge table
    # exists in this directory today; when one does, its pairs are
    # unioned here, same shape as grounds (a)/(b) above:
    #     for (x, y) in proved_cross_unit_edges:
    #         uf.union(x, y); record_edge(x, y, "c")
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

    # ---- byte counts (unchanged method) ----
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
            "generator": "build_representatives2.py",
            "note": "additive layer: does not modify/overwrite any raw "
                   "extraction. THE REPRESENTATIVE RULE per AgentMemory "
                   "2026-08-29: fewest machine bytes, ties by (lang, "
                   "unit id) order. FIXES build_representatives.py's "
                   "ground (b), which compared z3-SIMPLIFIED "
                   "normalized-root text (tree_matches3.json's own "
                   "`exact_normalized_root`) in which unmodelled "
                   "operations collapse to an opaque placeholder atom "
                   "-- proof: c/op_130 (+) and c/op_166 (-) on f64,f64 "
                   "both stored normal_path_root == 'op_2'. This "
                   "generation compares tree_units3.json's own "
                   "normal_path_raw (pre-simplification) instead, and "
                   "refuses a bare-placeholder-alone text as a "
                   "grounding value.",
            "population": population,
            "grounds": {
                "a": "newest canonical text (dominant_table17 fall-"
                    "through chain) character-identical -- %d pairwise "
                    "unions" % a_unions,
                "b": "tree_units3.json normal_path_raw (PRE-SIMPLIFICATION"
                    " -- unmodelled ops are NOT collapsed to a "
                    "placeholder here, unlike build_representatives.py's"
                    " ground (b)) character-identical, further split by "
                    "(type_pair, result_type_norm.class_family), "
                    "restricted to 0-branch population, refusing any "
                    "bare-opaque-atom-alone text as a grounding value -- "
                    "%d pairwise unions (%d labels' raw text missing, "
                    "%d labels' raw text refused as a bare placeholder)"
                    % (b_unions, missing_raw, bare_atom_skipped),
                "c": "investigated: canon20/21/22_behaviour_check.py's "
                    "anchored_check proves a candidate text equal to "
                    "THAT UNIT's own ship code (single-unit soundness), "
                    "not a cross-unit edge; no cross-unit proved-edge "
                    "table exists in this directory -- 0 unions, kept "
                    "wired for when one exists",
            },
        },
        "groups": out_groups,
    }
    out_path = os.path.join(HERE, "representatives2.json")
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

    # ---- VERIFY THE DEFECT IS GONE (item 3 of this lap's brief) ----
    # The defect was specifically GROUND (b) unioning members whose
    # raw computation differs (the placeholder-collapse false merge).
    # Ground (a) unions members on IDENTICAL CANONICAL TEXT -- proven
    # machine equivalence by construction (byte identity, Level 1
    # matching per the ratified canonical-form rulings), independent
    # of how each language's lifter happened to RENDER the raw
    # computation graph (e.g. one compiler doing a sign-extend the
    # lifter names `zx64`, another achieving the identical byte-
    # identical result via `And8` masking -- THE CANONICALIZATION-
    # INCLUDES-CONVERGENCE ruling: same instructions, different
    # printings/lift paths, not different computations). So the
    # correct scope for this assertion is GROUND (b) ONLY: build a
    # union-find using ONLY the ground-(b) edges (raw-text-identical,
    # by construction always same outermost op) and confirm no such
    # b-only component was EXTENDED, when re-checked here, to mix
    # outermost ops -- i.e. confirm ground (b) itself never unions
    # across an outermost-op boundary. This is the literal defect
    # (G0039's four different arithmetic operators fused by ground
    # (b) alone; they are NOT byte-identical text, so ground (a)
    # never touched them) and it is what this check targets.
    print("")
    print("---- defect-gone verification (ground (b) only) ----")
    b_uf = UnionFind()
    for lab in text_of:
        b_uf.find(lab)
    for key, grounds in ground_edges.items():
        if "b" not in grounds:
            continue
        a, bb = tuple(key)
        b_uf.union(a, bb)
    b_components = {}
    for lab in text_of:
        root = b_uf.find(lab)
        b_components.setdefault(root, []).append(lab)
    violations = []
    for root, members in b_components.items():
        if len(members) < 2:
            continue
        ops_seen = {}
        for lab in members:
            lang, n = lab.split("/op_")
            raw = raw_of.get((lang, n))
            op = outermost_op(raw)
            ops_seen.setdefault(op, []).append(lab)
        if len(ops_seen) > 1:
            violations.append((root, ops_seen))
    if violations:
        print("DEFECT STILL PRESENT: %d ground-(b)-only component(s) "
              "mix members whose normal_path_raw outermost operation "
              "differs:" % len(violations))
        for root, ops_seen in violations[:20]:
            print("  %s: %r" % (root, ops_seen))
        raise SystemExit(
            "build_representatives2.py REFUSES its own output: the "
            "defect this generation exists to fix is still present.")
    print("PASS: no ground-(b)-only component mixes members whose "
          "normal_path_raw outermost operation differs (%d "
          "multi-member b-components checked)"
          % sum(1 for m in b_components.values() if len(m) > 1))

    # Whole-group (a-and-b-combined) mixes ARE expected and are
    # reported here for the record, NOT as violations: they are
    # ground-(a) convergence (identical canonical text, different
    # lift-path rendering of the same computation).
    combined_mixed = 0
    for g in out_groups:
        ops_seen = set()
        for m in g["members"]:
            lang, n = m["lang"], m["n"]
            ops_seen.add(outermost_op(raw_of.get((lang, n))))
        if len(ops_seen) > 1:
            combined_mixed += 1
    print("(for the record, not a violation) %d final group(s) mix "
          "normal_path_raw outermost operations ONLY because ground "
          "(a) identical-canonical-text convergence joined them -- "
          "e.g. one lifter's zx64 vs another's And8-masking rendering"
          " of the same byte-proven computation" % combined_mixed)

    print("")
    print("G0039 (build_representatives.py, the DEFECTIVE run) held "
          "c/op_130 (+), c/op_166 (-), c/op_202 (*), c/op_238 (/) in "
          "ONE group. Their new group assignments here:")
    watch = [("c", "130", "+"), ("c", "166", "-"),
             ("c", "202", "*"), ("c", "238", "/")]
    lab_to_group = {}
    for g in out_groups:
        for m in g["members"]:
            lab_to_group[m["unit"]] = g["group_id"]
    seen_groups = set()
    for lang, n, tok in watch:
        lab = "%s/op_%s" % (lang, n)
        gid = lab_to_group.get(lab, "NOT-IN-POPULATION")
        seen_groups.add(gid)
        print("  %s (display %s): %s -> group %s" % (lab, tok,
              text_of.get(lab), gid))
    if len(seen_groups) == 4:
        print("CONFIRMED: all four are in FOUR DIFFERENT groups.")
    else:
        print("NOT CONFIRMED: only %d distinct groups among the four "
              "(expected 4)." % len(seen_groups))


if __name__ == "__main__":
    main()
