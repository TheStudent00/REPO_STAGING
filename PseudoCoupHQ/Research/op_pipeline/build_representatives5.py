#!/usr/bin/env python3
"""build_representatives4.py -- JOB 2's final step: THE REPRESENTATIVE
RULE with ground (c) LIVE for the first time in this line. Additive
wrapper over build_representatives3.py's logic (JOB 1's constant-
substituted ground (b) is kept UNCHANGED, verbatim); does not modify
build_representatives3.py, representatives3.json, cross_unit_prover.py,
or proved_edges.json -- new file, new output, same wrapper-layer
precedent (build_representatives.py -> ...2 -> ...3 -> this).

GROUND (c), REAL AT LAST. Every build_representatives{,2,3}.py before
this one recorded ground (c) as "wired but never fires" -- no cross-
unit proved-edge table existed. cross_unit_prover.py now writes one
(proved_edges.json). This file unions EXACTLY the pairs whose
`verdict` field is the literal string "PROVED" -- never DISPROVED,
UNDECIDED, or REFUSED, and the check is on that recorded field, not a
re-derivation. 14 such edges exist in this lap's proved_edges.json,
ALL of them the ucomiss+setcc vs cmpeqss/cmpneqss-value-write idiom
pair (go's flag-based float equality/inequality vs cpp/rust/swift's
packed-compare-and-mask form) -- see this file's own printed report
for the full list.

THE REPRESENTATIVE RULE (AgentMemory, 2026-08-29) governs what a
proved (c) edge is allowed to do here: it is UNION evidence like (a)
and (b) -- two units PROVED equivalent belong in the same group, and
the group's representative is still picked by fewest machine bytes
among ALL members (tie-broken by (lang, unit id)), exactly the same
rule (a)/(b) already use. A (c) edge does NOT retroactively change
what (a)/(b) already unioned; it only ADDS new union facts UNION-FIND
would not otherwise have reached (here: connecting go's rendering to
the cpp/rust/swift rendering of the SAME comparison, which (a)/(b)
could never reach because the texts are not character-identical and
their raw expressions differ by rendering, not by computation).

Grounds for union, all three now live:
  (a) newest canonical text character-identical (unchanged).
  (b) normal_path_raw3 (JOB 1's constant-substituted raw expression)
      character-identical + class key (unchanged from ...3.py).
  (c) a proved_edges.json pair whose verdict is "PROVED" (NEW, REAL,
      this file).

usage:
  build_representatives4.py
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
WORK = "/tmp/build_representatives4_work"

BARE_ATOM_RE = re.compile(r"^(op|atom)_[0-9]+$")

LOAD_RE = re.compile(r"ld(32|64)/g0\((\d+):64\)")

MOV32_RE = re.compile(r"(?:^|;)\s*mov\s+\$(-?\d+)\s*,")
MOVABS64_RE = re.compile(r"(?:^|;)\s*movabs\s+\$(-?\d+)\s*,")


def is_bare_opaque_atom(raw_text):
    if raw_text is None:
        return True
    return BARE_ATOM_RE.match(raw_text.strip()) is not None


def outermost_op(raw_text):
    if raw_text is None:
        return None
    idx = raw_text.find("(")
    if idx == -1:
        return raw_text.strip()
    return raw_text[:idx].strip()


def substitute_constants(raw_text, canon_text):
    """Return (raw_text3, substitutions) where substitutions is a list
    of (matched_span, width, value) describing every ld32/ld64 load
    this function replaced with a literal const<W>(value) atom, read
    from the SAME unit's own canonical text. Never touches ld128 (out
    of scope, see module docstring) or a load width with zero/more
    than one matching immediate in the unit's own text."""
    if raw_text is None:
        return raw_text, []
    loads = list(LOAD_RE.finditer(raw_text))
    if not loads:
        return raw_text, []

    mov32_vals = [int(x) for x in MOV32_RE.findall(canon_text or "")]
    movabs_vals = [int(x) for x in MOVABS64_RE.findall(canon_text or "")]

    subs = []
    out = raw_text
    # replace from the end so earlier spans stay valid
    for m in reversed(loads):
        width = m.group(1)
        if width == "32":
            candidates = mov32_vals
        elif width == "64":
            candidates = movabs_vals
        else:
            candidates = []
        if len(candidates) != 1:
            continue
        value = candidates[0]
        replacement = "const%s(%d)" % (width, value)
        out = out[:m.start()] + replacement + out[m.end():]
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


def load_canon4():
    docs = {}
    for lang in LANGS:
        path = os.path.join(HERE, "canon4_units_%s.json" % lang)
        docs[lang] = json.load(open(path))["units"]
    return docs


def load_raw_normal_paths():
    doc = json.load(open(os.path.join(HERE, "tree_units3.json")))
    out = {}
    for rec in doc["units"]:
        out[(rec["lang"], rec["n"])] = rec.get("normal_path_raw")
    return out


def main():
    gen_docs = DT17.load_generation_docs()
    units = DT17.load_0branch_units(gen_docs)
    population = len(units)
    print("0-branch population: %d" % population)

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

    # ---- JOB 1: substitute recoverable constant values into a copy
    # of normal_path_raw, per unit, using ONLY that unit's own
    # canonical text ----
    raw3_of = {}
    substitution_log = []
    for lab in text_of:
        lang, _, n = lab.partition("/op_")
        raw = raw_of.get((lang, n))
        raw3, subs = substitute_constants(raw, text_of[lab])
        raw3_of[(lang, n)] = raw3
        if subs:
            substitution_log.append({
                "unit": lab,
                "raw_before": raw,
                "raw_after": raw3,
                "substitutions": [
                    {"matched": sp, "width": w, "value": v}
                    for sp, w, v in subs
                ],
            })

    print("JOB 1: %d units had >=1 constant load substituted with its "
          "recovered value" % len(substitution_log))

    uf = UnionFind()
    for lab in text_of:
        uf.find(lab)

    ground_edges = {}

    def record_edge(a, b, ground):
        if a == b:
            return
        key = frozenset((a, b))
        ground_edges.setdefault(key, set()).add(ground)

    # ---- ground (a): identical newest canonical text (unchanged) ----
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

    # ---- ground (b): now over normal_path_raw3 (value-substituted) --
    bare_atom_skipped = 0
    missing_raw = 0
    by_raw = {}
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

    print("ground (b): %d population labels had no normal_path_raw3"
          % missing_raw)
    print("ground (b): %d population labels' normal_path_raw3 is a "
          "bare opaque placeholder atom alone -- REFUSED"
          % bare_atom_skipped)

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
        for (_tp, _rt), same_key_labs in by_rtype.items():
            if len(same_key_labs) < 2:
                continue
            labs_sorted = sorted(same_key_labs)
            first = labs_sorted[0]
            for other in labs_sorted[1:]:
                uf.union(first, other)
                record_edge(first, other, "b")
                b_unions += 1

    # ---- ground (c): REAL, from proved_edges.json UNION proved_edges2
    # .json (this lap's mechanical sweep extension -- SAME rule,
    # SAME `verdict == "PROVED"` filter, just two source files
    # instead of one; proved_edges2.json is additive to proved_edges
    # .json per that file's own meta.merge_with, never a replacement) ----
    proved_paths = [os.path.join(HERE, "proved_edges.json"),
                     os.path.join(HERE, "proved_edges2.json")]
    c_unions = 0
    c_pairs_used = []
    seen_pairs = set()
    for proved_path in proved_paths:
        if not os.path.exists(proved_path):
            continue
        proved_doc = json.load(open(proved_path))
        for pair in proved_doc["pairs"]:
            if pair.get("verdict") != "PROVED":
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
            c_pairs_used.append((a, b))

    groups = {}
    for lab in text_of:
        root = uf.find(lab)
        groups.setdefault(root, []).append(lab)

    print("ground (a) pairwise unions issued: %d" % a_unions)
    print("ground (b) pairwise unions issued: %d" % b_unions)
    print("ground (c) pairwise unions issued: %d" % c_unions)
    print("groups formed: %d" % len(groups))

    member_grounds = {}
    for key, grounds in ground_edges.items():
        a, b = tuple(key)
        if uf.find(a) != uf.find(b):
            continue
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

    need_assemble = {}
    byte_source = {}
    for lab, text in text_of.items():
        rt_text, rt_nbytes = rt_text_of(lab)
        if rt_text is not None and rt_text == text:
            byte_source[lab] = ("canon_roundtrip.json", rt_nbytes)
        else:
            need_assemble[text] = None

    print("units needing fresh byte assembly: %d distinct texts"
          % len(need_assemble))

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
    print("units with no byte count obtainable: %d" % unassemblable)

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
            "role_note": "this file IS a GROUPING/matching artifact -- "
                        "checked by check_no_spelling_keys.py IN FULL.",
            "generator": "build_representatives5.py",
            "note": "ground (b) unchanged from build_representatives3.py "
                   "(JOB 1's constant-substituted normal_path_raw3). "
                   "ground (c) unions PROVED edges from BOTH proved_"
                   "edges.json and proved_edges2.json (this lap's "
                   "mechanical sweep extension) -- %d PROVED edges "
                   "total, `verdict` field only, never re-derived."
                   % c_unions,
            "population": population,
            "grounds": {
                "a": "newest canonical text character-identical -- %d "
                    "pairwise unions" % a_unions,
                "b": "normal_path_raw3 (value-substituted) character-"
                    "identical, further split by (type_pair, "
                    "result_type_norm.class_family), restricted to "
                    "0-branch population, refusing bare-opaque-atom-"
                    "alone text -- %d pairwise unions (%d missing, %d "
                    "refused as bare placeholder)"
                    % (b_unions, missing_raw, bare_atom_skipped),
                "c": "cross_unit_prover.py's proved_edges.json UNION "
                    "cross_unit_prover_extend.py's proved_edges2.json, "
                    "pairs with verdict==PROVED only -- %d pairwise "
                    "unions" % c_unions,
            },
            "job2_proved_edges_used": [
                {"a": a, "b": b} for a, b in c_pairs_used
            ],
        },
        "job1_substitutions": substitution_log,
        "groups": out_groups,
    }
    out_path = os.path.join(HERE, "representatives5.json")
    json.dump(doc, open(out_path, "w"), indent=1)
    print("wrote %s" % out_path)

    largest = max(len(g["members"]) for g in out_groups)
    print("largest group size: %d" % largest)

    # ---- JOB 1 VERIFICATION: G0022/G0023 split cleanly (unchanged
    # from build_representatives3.py; re-checked here since ground
    # (c) could in principle re-merge them -- it does not, since none
    # of the 14 proved edges touch these units) ----
    print("")
    print("---- JOB 1 verification: G0022/G0023 split ----")
    watch = [("c", "39", "++"), ("c", "45", "--"),
             ("cpp", "51", "++"), ("cpp", "57", "--"),
             ("c", "40", "++"), ("c", "46", "--"),
             ("cpp", "52", "++"), ("cpp", "58", "--")]
    lab_to_group = {}
    for g in out_groups:
        for m in g["members"]:
            lab_to_group[m["unit"]] = g["group_id"]
    for lang, n, tok in watch:
        lab = "%s/op_%s" % (lang, n)
        gid = lab_to_group.get(lab, "NOT-IN-POPULATION")
        print("  %s (display %s): group %s" % (lab, tok, gid))
    plus_groups = set(lab_to_group.get("%s/op_%s" % (l, n))
                       for l, n, t in watch if t == "++")
    minus_groups = set(lab_to_group.get("%s/op_%s" % (l, n))
                        for l, n, t in watch if t == "--")
    if len(plus_groups) == 2 and len(minus_groups) == 2 and \
            not (plus_groups & minus_groups):
        print("CONFIRMED: still split (f32 ++ group, f64 ++ group) vs "
              "(f32 -- group, f64 -- group), no overlap.")
    else:
        print("NOT CONFIRMED: plus_groups=%r minus_groups=%r"
              % (plus_groups, minus_groups))

    # ---- JOB 2 report: which groups the 14 proved edges actually
    # changed, vs representatives3.json ----
    print("")
    print("---- THIS LAP: groups formed/changed by the NEW ground (c) "
          "edges (proved_edges2.json only, vs representatives4.json) ----")
    rep4 = json.load(open(os.path.join(HERE, "representatives4.json")))
    r4_group_of = {}
    for g in rep4["groups"]:
        for m in g["members"]:
            r4_group_of[m["unit"]] = frozenset(
                mm["unit"] for mm in g["members"])
    proved2_path = os.path.join(HERE, "proved_edges2.json")
    new_pairs_used = []
    if os.path.exists(proved2_path):
        p2 = json.load(open(proved2_path))
        new_pairs_used = [(p["a"], p["b"]) for p in p2["pairs"]
                           if p.get("verdict") == "PROVED"]
    if not new_pairs_used:
        print("  NONE -- proved_edges2.json contributed 0 PROVED edges "
              "this lap, so representatives5.json's groups are "
              "identical to representatives4.json's (zero-regression "
              "by construction, not merely by comparison).")
    for a, b in new_pairs_used:
        before_a = r4_group_of.get(a, frozenset([a]))
        before_b = r4_group_of.get(b, frozenset([b]))
        after = frozenset(groups[uf.find(a)])
        print("  NEW proved edge %s <-> %s" % (a, b))
        print("    representatives4 group of %s: %d member(s)"
              % (a, len(before_a)))
        print("    representatives4 group of %s: %d member(s)"
              % (b, len(before_b)))
        print("    representatives5 combined group: %d member(s): %s"
              % (len(after), sorted(after)))


if __name__ == "__main__":
    main()
