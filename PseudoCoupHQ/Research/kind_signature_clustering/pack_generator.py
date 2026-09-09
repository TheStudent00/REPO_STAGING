#!/usr/bin/env python3
"""pack_generator.py — P-a of the kind-clustering plan (PCHQ log_016 §6):
the per-language ts_kind -> ur_kind PROPOSAL machinery.

Consumes the ecosystem basis (spectrum_all + archetypes + basis_xref
anchors + top_counterparts_all) plus the RULED vocabulary
(PseudoCoup_v5/Tools/ledgerer/ur.py KINDS, 2026-08-12:
15 objects incl. import/try/pair/interpolation; forms incl.
container-form) and emits, for one language:

    proposed_kind_map_<language>.json   (machine-readable)
    proposed_kind_map_<language>.md     (human review table)

Every named visible kind of the grammar appears exactly once; rows the
evidence cannot carry go to the RESIDUE (proposed=none) — the human
review list. Per the two-layer classification ruling (ur.py, PCHQ
log_016): only SHAPE buckets (the 15 objects + 4 forms) are ever
proposed as ur_kind; the categories A–J are intentions, never mapped —
where evidence suggests one, it is emitted as an intention NOTE on the
row. Name evidence is always LABELED as name evidence (log_015 §8:
name bias).

Usage:  python3 pack_generator.py <language>     # e.g. rust

MECHANISM (each step mechanical; every knob a documented constant):

1. ANCHORS. Recompute the t=0.40 partition (verified against
   basis_xref_out.json: 1,194 clusters) and re-derive the bucket-anchor
   clusters with basis_xref's exact criterion (>=5 name-matches, >=40%
   of members, >=5 languages), uncapped (basis_xref kept a top-6
   presentation slice; anchoring wants them all). Then:
   a. a cluster hit by several buckets anchors only the bucket with
      the highest match fraction; exact ties drop the cluster (it is
      ambiguous as an anchor);
   b. RULED re-route (container-form, 2026-08-12): an object-bucket
      anchor whose members are dominated (>= CONTAINER_FRAC) by
      document-root / body-list names re-anchors container-form —
      this is M4/M5 of log_015 §4 becoming the ruled form;
   c. RULED additions: the new objects import/try/pair/interpolation
      anchor on the log_015 §4 core clusters (M1/M2/M3/M9), pinned by
      t=0.40 cluster id and self-checked against an expected member
      each (the ids are reproducible: same tree, same fcluster);
   d. category buckets A–J keep their matched clusters as INTENTION
      anchors — used for notes only, never for ur_kind.

2. PER-KIND EVIDENCE. For each named kind of the language, its
   archetype leaf is located and its cluster is queried at the
   THRESHOLD BAND (several reference slices of the one merge tree, not
   one cut). Because the tree is hierarchical, an anchor cluster sits
   wholly inside exactly one cluster at every t >= 0.40, so
   co-clustering is an O(1) id comparison. A join at t only counts
   under the DILUTION GUARD: the containing cluster must span
   < MAX_LANGS languages and < MAX_KINDS kinds — this excludes the
   shape-poverty giants (369/398 languages, ~5,000 kinds each,
   log_014 §4) whose membership means grammar-authoring convention,
   not shared shape.

3. PROPOSAL. ur_kind = the shape bucket with the LOWEST join
   threshold (strongest co-clustering); ties break by wider anchor,
   then counterpart votes. Two fallback channels, each floored:
   - counterparts: >= CP_VOTE_FLOOR of the kind's top-10 nearest
     counterpart archetypes (top_counterparts_all.json) sitting in one
     bucket's anchors proposes that bucket (secondary evidence, per
     log_015 §7 P9);
   - name-only (LABELED): permitted ONLY for form-tier buckets and
     ONLY for cluster-isolated kinds (t=0.40 cluster <= ISO_LANGS
     languages) — this is log_015 §6's proof-form absorption; objects
     are never proposed on names alone (name-bias guard).

4. CONFIDENCE (documented criteria, applied mechanically):
   strong   = cluster join at t <= T_STRONG with anchor >= 10
              languages, no competing bucket joining within
              COMPETE_MARGIN, and no name-evidence conflict;
   moderate = cluster join at t <= T_MODERATE, or a strong-band join
              that fails a margin/width/name test, or counterpart
              votes >= CP_VOTE_MODERATE;
   weak     = join only at the band top, counterpart votes at the
              floor, or the name-only form route.
   Below all floors -> RESIDUE: proposed=none, partial evidence kept.

5. TOTALITY. Rows are the named visible kinds of the grammar
   (raw/<language>.node-types.json: `named` true, name not starting
   "_"; supertype entries are hidden nodes and thus excluded), checked
   equal to the kinds present in the cluster data; each appears
   exactly once.

Vocabulary rule: super-node / sub-node / co-node / sub-tree only.
"""
import json
import os
import re
import sys
from collections import Counter

import numpy as np
from scipy.cluster.hierarchy import fcluster

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from spectrum_all import load_spectrum_all

# ------------------------------------------------------------ constants
# The threshold band: log_015's four reference slices plus midpoints
# for band resolution. All are queries of the one merge tree.
BAND = (0.40, 0.48, 0.55, 0.62, 0.68, 0.73, 0.78)
# Dilution guard (step 2), four tests, all documented against measured
# family shapes (log_014 §4, log_015 §§3–4). A join counts only when
# the containing cluster looks like ecosystem AGREEMENT rather than
# blob or self-affinity:
#   - width caps: the shape-poverty giants span 369/398 languages and
#     ~5,000 kinds at t=0.40 and only grow; every legitimate semantic
#     family stays far below (widest: declaration super-family, 212
#     languages);
#   - MIN_JOIN_LANGS: evidence means many-language agreement — the
#     containing cluster must span >= 10 languages (log_015 decision 7
#     used the same floor for "covered");
#   - DENSITY_MAX: semantic families run 1–4 kinds per language (M1
#     527/155, M3 501/152, M9 301/121, roots 276/275); weak-spec blobs
#     run 5–20+ (giants ~13.6). Cap kinds/languages at 5.0;
#   - OWN_FRAC_MAX: a containing cluster dominated by the mapped
#     language's own kinds is self-affinity, not agreement — the
#     language's own kinds must be <= 1/3 of members.
MAX_LANGS = 300
MAX_KINDS = 3000
MIN_JOIN_LANGS = 10
DENSITY_MAX = 5.0
OWN_FRAC_MAX = 1 / 3
# Anchor criterion (basis_xref decision 3, reused verbatim). An
# anchor's PURITY is its name-match fraction; joins to anchors below
# PURITY_FLOOR never rate above weak confidence (the anchor itself is
# mixed, so co-clustering with it is soft evidence).
ANCHOR_MIN_HITS, ANCHOR_MIN_FRAC, ANCHOR_MIN_LANGS = 5, 0.40, 5
PURITY_FLOOR = 0.5
# Admission floor for PINNED anchors (pattern-routed ones clear 0.40
# by construction): below 10% the anchor is a family the regex can
# barely see, and joins to it proposed nonsense in trials — the M9
# interpolation cluster (121 languages, 3% name purity at t=0.40)
# falls here, so `interpolation` currently has NO anchor and stays a
# name-note until a purer slice is pinned.
ANCHOR_PURITY_MIN = 0.10
# Container re-route (step 1b).
CONTAINER_FRAC = 0.40
# Confidence knobs (step 4). COMPETE_MARGIN pools only joins at the
# SAME band slice (earlier is better evidence than wider — a band
# step of real height separates them; measured on rust, a wider
# margin let a 16-language closure cluster outvote the loop family's
# own earlier join). Within a pool the wider anchor wins. strong
# additionally needs a clean anchor: purity >= STRONG_PURITY, or an
# anchor so wide (>= WIDE_ANCHOR_LANGS languages) that purity noise
# cannot explain it.
T_STRONG, T_MODERATE = 0.55, 0.68
COMPETE_MARGIN = 0.05
STRONG_ANCHOR_LANGS = 10
STRONG_PURITY = 0.7
WIDE_ANCHOR_LANGS = 50
# Fallback floors (step 3).
CP_VOTE_FLOOR, CP_VOTE_MODERATE = 3, 8
ISO_LANGS = 2

# The RULED shape vocabulary (ur.py KINDS, 2026-08-12) — the only
# legal proposal values. Categories A–J are deliberately absent.
OBJECTS = ("value", "name", "operation", "sequence", "choice",
           "repetition", "function", "record", "collection",
           "mutation", "service call",
           "import", "try", "pair", "interpolation")
FORMS = ("type-form", "declarative-form", "proof-form",
         "container-form")
SHAPE_BUCKETS = OBJECTS + FORMS
CATEGORIES = {"A suspension": "A", "B channels": "B", "C optionals": "C",
              "D pattern matching": "D", "E dispatch": "E",
              "F generics": "F", "G scoped cleanup": "G",
              "H events": "H", "I operator overloading": "I",
              "J metaprogramming": "J"}

# Name patterns. The originals are basis_xref.py's PAT verbatim
# (each an interpretation decision, English-centric — log_015 §8);
# the four ruled additions and container-form get patterns in the
# same spirit. Name matches are EVIDENCE LABELS, never sufficient for
# an object proposal.
PAT = {
 "value": r"literal|number|integer|float|string(?!_interp)|bool|char|true|false|null|nil|none$",
 # one documented deviation from basis_xref's PAT: `type_identifier`
 # is excluded from `name` — the ruled form tier owns it (type-form),
 # and letting both patterns claim the same clusters made the
 # type_identifier cluster an ambiguous anchor.
 "name": r"(?<!type_)identifier$|^name$|_name$|variable$|path$",
 "operation": r"binary|unary|operator|arith|comparison|logical|cast",
 "sequence": r"^block$|statement_list|compound_statement|^body$|_body$|declaration_list|sequence|source_file|program$",
 "choice": r"^if|_if$|else|conditional|ternary|elif|elsif|unless",
 "repetition": r"while|^for|for_|loop|repeat|do_statement|break|continue|each",
 "function": r"function|method|lambda|closure|call|parameter|argument|return|proc|def$|arrow",
 "record": r"struct|class|field|record|enum|interface_body|object|property",
 "collection": r"array|list(?!_comprehension)|dict|map|tuple|set_|index|subscript|slice|element",
 "mutation": r"assign|augmented|update_expression|increment|decrement",
 "service call": r"extern|foreign|ffi|syscall|asm",
 "import": r"import|include(?!_expression)|require|^use_|use_declaration|using_directive|extern_crate|package_clause",
 "try": r"^try_|^try$|catch|finally|rescue|ensure|except",
 "pair": r"pair|match_arm|switch_case|case_clause|key_value|keyed_element|initializer_pair|label_pair|^entry$",
 "interpolation": r"interpolation|format_expression|format_specifier|string_interp|encapsed|template_substitution",
 "A suspension": r"async|await|yield|generator|coroutine|suspend",
 "B channels": r"channel|select_statement|send_statement|go_statement|isolate|actor",
 "C optionals": r"optional|nullable|null_(?!literal)|option_|elvis|safe_navigation|non_null",
 "D pattern matching": r"match|pattern|^case|case_|switch|when_|destructur",
 "E dispatch": r"trait|interface|protocol|impl(?!ort)|implements|extends|virtual",
 "F generics": r"generic|type_parameter|type_argument|template|where_clause|bound|constraint",
 "G scoped cleanup": r"defer|using_|with_statement|finally|ensure|resource|drop",
 "H events": r"event|delegate|signal_|listener|callback|stream",
 "I operator overloading": r"operator_(declaration|definition|function|overload)",
 "J metaprogramming": r"macro|annotation|attribute|decorator|reflect|preproc|pragma|directive|quote|splice",
 "type-form": r"_type$|^type_identifier|primitive_type|type_annotation|predefined_type",
 "declarative-form": r"comment|modifier|visibility|shebang|doc_",
 "proof-form": r"lifetime|borrow|reference_type|ownership|mutable_specifier|ref_",
 "container-form": r"source_file|^program$|^document$|^source$|^module$|_body$|^body$|declaration_list|enumerator_list|_block$",
}
RX = {b: re.compile(p) for b, p in PAT.items()}

# RULED-addition anchors (step 1c): t=0.40 cluster ids of the log_015
# §4 core clusters, each self-checked by an expected member. M1
# import/include; M2 error clauses; M3 pair/case; M9 interpolation.
# Pinned clusters below ANCHOR_MIN_LANGS are not admitted (the floor
# applies to additions too — e.g. python's private 3-language import
# trio is a seed for the eye, not an anchor).
ADDITION_ANCHORS = {
    "import": [(983, "c:preproc_include")],
    "try": [(673, "java:try_statement"), (716, "c-sharp:catch_clause")],
    "pair": [(628, "javascript:pair_pattern"), (627, "python:pair")],
    "interpolation": [(981, "python:interpolation")],
}


def kindname(m):
    return m.split(":", 1)[1]


def lang_of(m):
    return m.split(":", 1)[0]


class Basis:
    """The loaded ecosystem basis plus the derived anchor sets."""

    def __init__(self):
        self.labels, self.mult, self.Z, _ = load_spectrum_all()
        self.arch = json.load(open(os.path.join(HERE, "archetypes.json")))
        self.n = len(self.labels)
        self.leaf_of_hash = {h: i for i, h in enumerate(self.labels)}
        self.member_leaf = {}
        for i, h in enumerate(self.labels):
            for m in self.arch[h]["members"]:
                self.member_leaf[m] = i
        # partitions across the band (queries of the one tree)
        self.assign = {t: fcluster(self.Z, t=t, criterion="distance")
                       for t in BAND}
        a40 = self.assign[0.40]
        xref = json.load(open(os.path.join(HERE, "basis_xref_out.json")))
        n40 = len(set(int(c) for c in a40))
        assert n40 == xref["n_clusters"], \
            "t=0.40 partition drifted from basis_xref (%d vs %d)" % (
                n40, xref["n_clusters"])
        # per-threshold cluster stats: id -> (n_kinds, n_langs)
        self.stats = {}
        for t in BAND:
            leaves = {}
            for i, c in enumerate(self.assign[t]):
                leaves.setdefault(int(c), []).append(i)
            st = {}
            for c, idxs in leaves.items():
                ms = [m for i in idxs
                      for m in self.arch[self.labels[i]]["members"]]
                st[c] = (len(ms), len({lang_of(m) for m in ms}))
            self.stats[t] = st
        self.members40 = {}
        for i, c in enumerate(a40):
            self.members40.setdefault(int(c), []).extend(
                self.arch[self.labels[i]]["members"])
        self.anchors = self._build_anchors()
        # counterpart slice (secondary evidence channel)
        self.counterparts = json.load(
            open(os.path.join(HERE, "top_counterparts_all.json")))

    # ---------------------------------------------------- step 1: anchors
    def _build_anchors(self):
        """bucket -> list of anchor records; an anchor is a t=0.40
        cluster, carried as (cluster40_id, representative_leaf,
        n_kinds, n_langs, sample)."""
        a40 = self.assign[0.40]
        rep = {}
        for i, c in enumerate(a40):
            rep.setdefault(int(c), i)
        # basis_xref criterion, uncapped, every bucket
        hits = {}  # cluster40 -> list of (bucket, frac)
        for bucket, rx in RX.items():
            if bucket == "container-form":
                continue        # derived by re-route below
            for c, ms in self.members40.items():
                nh = sum(1 for m in ms if rx.search(kindname(m)))
                frac = nh / len(ms)
                langs = len({lang_of(m) for m in ms})
                if (nh >= ANCHOR_MIN_HITS and frac >= ANCHOR_MIN_FRAC
                        and langs >= ANCHOR_MIN_LANGS):
                    hits.setdefault(c, []).append((bucket, frac))
        anchors = {b: [] for b in list(RX)}
        for c, blist in hits.items():
            blist.sort(key=lambda bf: -bf[1])
            if len(blist) > 1 and blist[0][1] == blist[1][1]:
                continue        # ambiguous anchor: dropped (step 1a)
            bucket, purity = blist[0]
            ms = self.members40[c]
            # step 1b: ruled container re-route, objects only
            if bucket in OBJECTS or bucket == "sequence":
                cf = sum(1 for m in ms
                         if RX["container-form"].search(kindname(m)))
                if cf / len(ms) >= CONTAINER_FRAC:
                    bucket, purity = "container-form", cf / len(ms)
            anchors[bucket].append(self._anchor(c, rep, purity))
        # step 1c: ruled additions, pinned + self-checked. A pin is a
        # RULING (log_015 §4's hand-glossed family cores): it takes
        # precedence over pattern routing, so a pinned cluster is
        # removed from wherever the regexes put it first.
        pinned = {cid for pins in ADDITION_ANCHORS.values()
                  for cid, _ in pins}
        for b in anchors:
            anchors[b] = [a for a in anchors[b]
                          if a["cluster40"] not in pinned]
        for bucket, pins in ADDITION_ANCHORS.items():
            for cid, expect in pins:
                assert expect in self.members40.get(cid, []), \
                    "addition anchor %d for %r lost its expected " \
                    "member %r — re-pin against the current tree" % (
                        cid, bucket, expect)
                ms = self.members40[cid]
                purity = sum(1 for m in ms
                             if RX[bucket].search(kindname(m))) / len(ms)
                a = self._anchor(cid, rep, purity)
                if (a["langs"] >= ANCHOR_MIN_LANGS
                        and purity >= ANCHOR_PURITY_MIN):
                    anchors[bucket].append(a)
        # anchor cluster -> bucket, for the counterpart channel
        self.anchor_bucket = {}
        for b, rows in anchors.items():
            for a in rows:
                self.anchor_bucket[a["cluster40"]] = b
        return anchors

    def _anchor(self, c, rep, purity):
        ms = self.members40[c]
        names = Counter(kindname(m) for m in ms)
        return {"cluster40": c, "leaf": rep[c], "kinds": len(ms),
                "langs": len({lang_of(m) for m in ms}),
                "purity": round(purity, 3),
                "sample": [n for n, _ in names.most_common(4)]}

    def set_language(self, lang):
        """Precompute, per band threshold, how many of the mapped
        language's own kinds each containing cluster holds (for the
        own-language dilution test)."""
        own_leaves = [self.member_leaf[m] for m in self.member_leaf
                      if m.startswith(lang + ":")]
        self.own_count = {}
        for t in BAND:
            at = self.assign[t]
            cnt = Counter(int(at[i]) for i in own_leaves)
            self.own_count[t] = cnt

    # ------------------------------------------------ step 2: evidence
    def joins(self, leaf):
        """For one kind's leaf: bucket -> the lowest-threshold guarded
        join, over shape AND category anchors."""
        out = {}
        for t in BAND:
            at = self.assign[t]
            mine = at[leaf]
            nk, nl = self.stats[t][int(mine)]
            if (nk >= MAX_KINDS or nl >= MAX_LANGS
                    or nl < MIN_JOIN_LANGS
                    or nk / nl > DENSITY_MAX
                    or self.own_count[t][int(mine)] / nk > OWN_FRAC_MAX):
                continue        # dilution guard (all four tests)
            for bucket, rows in self.anchors.items():
                if bucket in out:
                    continue
                for a in rows:
                    if at[a["leaf"]] == mine:
                        out[bucket] = {
                            "t_join": t, "anchor": a["cluster40"],
                            "anchor_langs": a["langs"],
                            "anchor_kinds": a["kinds"],
                            "anchor_purity": a["purity"],
                            "anchor_sample": a["sample"],
                            "cluster_kinds_at_join": nk,
                            "cluster_langs_at_join": nl}
                        break
        return out

    def counterpart_votes(self, h):
        """Secondary channel: which anchored buckets the top-10
        nearest counterpart archetypes sit in (t=0.40)."""
        row = self.counterparts.get(h)
        if not row:
            return Counter(), []
        a40 = self.assign[0.40]
        votes, examples = Counter(), []
        for cp in row["counterparts"]:
            j = self.leaf_of_hash.get(cp["hash"])
            if j is None:
                continue
            b = self.anchor_bucket.get(int(a40[j]))
            if b is not None:
                votes[b] += 1
            examples.append({"sim": cp["sim"], "bucket": b,
                             "examples": cp["examples"][:2]})
        return votes, examples


# ------------------------------------------------------- steps 3 and 4
def propose(basis, lang, kind):
    m = "%s:%s" % (lang, kind)
    leaf = basis.member_leaf[m]
    h = basis.labels[leaf]
    joins = basis.joins(leaf)
    shape_joins = {b: j for b, j in joins.items() if b in SHAPE_BUCKETS}
    cat_joins = {b: j for b, j in joins.items() if b in CATEGORIES}
    votes, cp_examples = basis.counterpart_votes(h)
    name_hits = [b for b, rx in RX.items() if rx.search(kind)]
    name_shape = [b for b in name_hits if b in SHAPE_BUCKETS]
    name_cats = [b for b in name_hits if b in CATEGORIES]
    iso_langs = basis.stats[0.40][int(basis.assign[0.40][leaf])][1]

    row = {"kind": kind, "proposed": None, "confidence": None,
           "residue": False, "channel": None,
           "evidence": {
               "cluster_joins": {b: j for b, j in sorted(
                   shape_joins.items(), key=lambda bj: bj[1]["t_join"])},
               "category_joins": cat_joins,
               "counterpart_votes": dict(votes.most_common()),
               "counterpart_top": cp_examples[:3],
               "name_evidence_shape": name_shape,
               "cluster40_langs": iso_langs},
           "intention_note": None}

    notes = []
    for b, j in sorted(cat_joins.items(), key=lambda bj: bj[1]["t_join"]):
        notes.append("co-clusters with %s anchors at t=%.2f (cluster "
                     "evidence)" % (b, j["t_join"]))
    cat_votes = {b: n for b, n in votes.items() if b in CATEGORIES}
    if cat_votes:
        notes.append("counterpart evidence: %s" % ", ".join(
            "%s %d/10" % (b, n) for b, n in
            sorted(cat_votes.items(), key=lambda bn: -bn[1])))
    if name_cats:
        notes.append("name evidence (name only, unweighed): %s"
                     % ", ".join(sorted(name_cats)))
    if notes:
        row["intention_note"] = "; ".join(notes)

    # channel 1: cluster joins. Candidates within COMPETE_MARGIN of
    # the earliest join form a pool; the widest anchor wins it.
    if shape_joins:
        tmin = min(j["t_join"] for j in shape_joins.values())
        pool = sorted(
            [(b, j) for b, j in shape_joins.items()
             if j["t_join"] - tmin <= COMPETE_MARGIN],
            key=lambda bj: (-bj[1]["anchor_langs"], bj[1]["t_join"],
                            -bj[1]["anchor_purity"]))
        best, bj = pool[0]
        competitors = [b for b, j in shape_joins.items()
                       if b != best
                       and j["t_join"] - bj["t_join"] <= COMPETE_MARGIN]
        conflict = bool(name_shape) and best not in name_shape
        if bj["anchor_purity"] < PURITY_FLOOR:
            conf = "weak"       # mixed anchor: soft evidence
        elif (bj["t_join"] <= T_STRONG
                and bj["anchor_langs"] >= STRONG_ANCHOR_LANGS
                and (bj["anchor_purity"] >= STRONG_PURITY
                     or bj["anchor_langs"] >= WIDE_ANCHOR_LANGS)
                and not competitors and not conflict):
            conf = "strong"
        elif bj["t_join"] <= T_MODERATE:
            conf = "moderate"
        else:
            conf = "weak"
        row.update(proposed=best, confidence=conf, channel="cluster")
        row["evidence"]["competing_buckets"] = competitors
        row["evidence"]["name_conflict"] = conflict
        return row

    # channel 2: counterparts (secondary; SHAPE buckets only — a
    # category lead here goes to the intention note, never to ur_kind).
    # A name-evidence conflict caps it at weak; and when the vote is
    # weak while the name evidence points unanimously at
    # declarative-form/proof-form, the row falls through to channel 3
    # (a 3-vote drift should not outrank the labeled form route).
    shape_votes = Counter({b: n for b, n in votes.items()
                           if b in SHAPE_BUCKETS})
    if shape_votes:
        (best, nv), = shape_votes.most_common(1)
        second = (shape_votes.most_common(2)[1][1]
                  if len(shape_votes) > 1 else 0)
        if nv >= CP_VOTE_FLOOR and nv > second:
            conflict = bool(name_shape) and best not in name_shape
            conf = ("weak" if conflict or nv < CP_VOTE_MODERATE
                    else "moderate")
            falls_through = (conf == "weak" and name_shape and
                             set(name_shape) <= {"declarative-form",
                                                 "proof-form"})
            if not falls_through:
                row.update(proposed=best, confidence=conf,
                           channel="counterpart")
                row["evidence"]["name_conflict"] = conflict
                return row

    # channel 3: name-only, forms only, always weak, always LABELED.
    # Two variants, both grounded in log_015:
    #  - any form, if the kind is cluster-isolated (<= ISO_LANGS
    #    languages at t=0.40) — §6's form-tier absorption of a
    #    language's private apparatus;
    #  - declarative-form and proof-form even without isolation:
    #    declarative-form's shape is a structureless extra (a grammar
    #    that gives comments internal structure leaves the 265-language
    #    archetype without ceasing to be trivia), and proof-form HAS no
    #    ecosystem cluster anywhere (§3 row Pf) — name evidence is the
    #    only evidence that can ever exist for it. type-form and
    #    container-form get no such relaxation: their families are
    #    cluster-visible, so a kind claiming them should meet them in
    #    the tree.
    for form in ("proof-form", "type-form", "container-form",
                 "declarative-form"):
        if form in name_shape and (
                iso_langs <= ISO_LANGS
                or form in ("declarative-form", "proof-form")):
            row.update(proposed=form, confidence="weak",
                       channel="name-only (labeled; form tier)")
            return row

    row["residue"] = True
    return row


# ------------------------------------------------------ step 5: totality
def grammar_kinds(lang):
    """Named visible kinds from the pinned node-types file. Supertype
    entries are the grammar's hidden "_"-prefixed nodes — excluded, as
    is every anonymous token."""
    for d in ("raw", "raw_all"):
        p = os.path.join(HERE, d, "%s.node-types.json" % lang)
        if os.path.exists(p):
            break
    else:
        raise SystemExit("no node-types file for %r" % lang)
    nt = json.load(open(p))
    return sorted({e["type"] for e in nt
                   if e.get("named") and not e["type"].startswith("_")})


# ---------------------------------------------------------------- emit
def emit(lang):
    basis = Basis()
    basis.set_language(lang)
    kinds = grammar_kinds(lang)
    in_data = sorted(k.split(":", 1)[1] for k in basis.member_leaf
                     if k.startswith(lang + ":"))
    assert kinds == in_data, \
        "totality: grammar kinds != cluster-data kinds (%d vs %d)" % (
            len(kinds), len(in_data))
    rows = [propose(basis, lang, k) for k in kinds]
    assert len(rows) == len(kinds)
    assert len({r["kind"] for r in rows}) == len(rows)

    summary = {
        "language": lang, "n_kinds": len(rows),
        "proposed": sum(1 for r in rows if not r["residue"]),
        "residue": sum(1 for r in rows if r["residue"]),
        "by_confidence": dict(Counter(
            r["confidence"] for r in rows if not r["residue"])),
        "by_bucket": dict(Counter(
            r["proposed"] for r in rows if not r["residue"]).most_common()),
        "band": list(BAND),
        "guards": {"max_langs": MAX_LANGS, "max_kinds": MAX_KINDS,
                   "cp_vote_floor": CP_VOTE_FLOOR,
                   "iso_langs": ISO_LANGS},
    }
    out = {"summary": summary,
           "anchors": {b: [{k: a[k] for k in
                            ("cluster40", "kinds", "langs", "sample")}
                           for a in rows_]
                       for b, rows_ in basis.anchors.items() if rows_},
           "rows": rows}
    jp = os.path.join(HERE, "proposed_kind_map_%s.json" % lang)
    json.dump(out, open(jp, "w"), indent=1)

    mp = os.path.join(HERE, "proposed_kind_map_%s.md" % lang)
    with open(mp, "w") as f:
        f.write("# proposed ts_kind -> ur_kind map: %s (MACHINE "
                "PROPOSAL, for review)\n\n" % lang)
        f.write("Generated by `pack_generator.py` from the ecosystem "
                "basis; evidence per row. `none` rows are the "
                "RESIDUE (the review list). Intention notes are duals "
                "per the two-layer ruling, never mappings.\n\n")
        f.write("%d kinds: %d proposed (%s), %d residue.\n\n" % (
            summary["n_kinds"], summary["proposed"],
            ", ".join("%d %s" % (v, k) for k, v in
                      sorted(summary["by_confidence"].items())),
            summary["residue"]))
        f.write("| kind | proposed | conf | evidence | intention note |\n")
        f.write("| --- | --- | --- | --- | --- |\n")
        for r in rows:
            ev = []
            for b, j in list(r["evidence"]["cluster_joins"].items())[:2]:
                ev.append("%s: joins anchor cl%d (%d langs) at t=%.2f "
                          "(containing cluster %d kinds / %d langs)"
                          % (b, j["anchor"], j["anchor_langs"],
                             j["t_join"], j["cluster_kinds_at_join"],
                             j["cluster_langs_at_join"]))
            cv = r["evidence"]["counterpart_votes"]
            if cv:
                ev.append("counterparts: " + ", ".join(
                    "%s %d/10" % (b, n) for b, n in
                    list(cv.items())[:3]))
            if r["evidence"]["name_evidence_shape"]:
                ev.append("name evidence (labeled): %s" % ", ".join(
                    r["evidence"]["name_evidence_shape"]))
            f.write("| `%s` | %s | %s | %s | %s |\n" % (
                r["kind"], r["proposed"] or "**none**",
                r["confidence"] or "—",
                "; ".join(ev) or "—",
                r["intention_note"] or "—"))
    print("wrote", jp)
    print("wrote", mp)
    print(json.dumps(summary, indent=1))
    return out


if __name__ == "__main__":
    emit(sys.argv[1] if len(sys.argv) > 1 else "rust")
