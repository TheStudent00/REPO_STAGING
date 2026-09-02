#!/usr/bin/env python3
"""l3_row_graph_v4.py -- the row graph over the CARTESIAN rows, rebuilt
with the owner's three rulings of 2026-08-21.

`l3_row_graph.py` (log 050), `l3_row_graph_v2.py` (log 051) and
`l3_row_graph_v3.py` (log 052) are left on disk unchanged, and so are
`row_graph_v3.json` / `row_graph_explorer_v3.html` / the v3 verifier.
This is a v4, not an edit: the alignment rule changed, so the old
products stay readable for the audit.

SOURCE: `matrices_cart/` -- level 1 `y = op(x0, x1)` over ALL ordered
pairs of a holder's set X, level 2 `z = op(op(x0,x1), op(x2,x3))` over a
subset X'.  Operands are recorded ONCE PER SET in `matrices_cart/
index.json`, never per row, and a position is reconstructed from the
probe-index rule:

    level 1   p = i0*|Xb| + i1
    level 2   p = ((i0*|Xb| + i1)*|Xa| + i2)*|Xb| + i3
              which is exactly   p = q01 * (|Xa|*|Xb|) + q23
              with q = i*|Xb| + j the level-1 pair index -- so the level-2
              key index is the OUTER PRODUCT of the level-1 one with
              itself, and the alignment below needs no extra machinery.

------------------------------------------------------------------
CHANGE 1 -- ALIGN ON INPUT PAIRS, NOT ON IDENTICAL VECTORS
------------------------------------------------------------------
v3 compared two rows only when their ENTIRE input vectors were
byte-identical -- same level AND both operand-set ids equal.  Holders
represent different subsets of X (rust `i32` cannot hold 2^53+1, `u64`
cannot hold -1, ruby `Integer` holds everything), so rows that ran dozens
of the SAME input pairs were declared incomparable.  v3's 68,725 "no
comparable positions" row pairs are largely that artifact.

THE RULE NOW:  the comparable set of two rows is the INTERSECTION of
their INPUT KEYS.

  - level 1 a key is the operand pair   (x0, x1)
  - level 2 a key is the operand quad   (x0, x1, x2, x3)
  - an operand is identified by its SPELLING, which is globally unique
    across every recorded set and carries exactly one canonical string
    (checked at load: 37 spellings, 37 distinct spelling->canon maps).
  - outputs are compared AT EACH SHARED KEY.
  - a shared key where EITHER side declines (REFUSE / RAISE:* / ABORT)
    is excluded from the numerator AND the denominator, both scorings
    alike -- ruling B, unchanged.
  - ZERO comparable keys after exclusion -> NO CONNECTOR.  That is a
    genuine absence of evidence and it is not a zero-weight connector.
  - LEVEL 1 IS NEVER MIXED WITH LEVEL 2 in one connector.  A level-1 key
    and a level-2 key are different objects and their intersection is
    empty by construction; the builder also refuses the pair outright.
    Every connector records its `level`.

------------------------------------------------------------------
CHANGE 2 -- TWO KINDS OF COLLAPSE, KEPT DISTINCT
------------------------------------------------------------------
CASE 1, CONTRACT (identity).  Rows whose INPUT KEY SET IS IDENTICAL and
whose outputs are BYTE-IDENTICAL AT EVERY KEY are the same function on
the same domain.  They are contracted into ONE node.  This is plain
identity: it is an equivalence relation, so it is transitive and needs no
clique test.  The contracted node carries its member row ids, its member
count, its languages and its operators.

CASE 2, GROUP (agreement over a partial overlap).  Contracted nodes that
are mutually exact-1.0 on their OVERLAPS but whose input key sets DIFFER
are NOT contracted.  They are GROUPED.  A group is a set in which EVERY
PAIR is mutually exact-1.0 with n_comparable >= 1 -- a MAXIMAL CLIQUE,
complete-linkage logic.  It is NEVER a connected component: chaining
through pairs that were never compared is exactly what this avoids.  The
group is a CONTAINER, NOT A MERGE -- members stay distinct nodes -- and
it carries every pair's overlap size plus the MINIMUM overlap as its
weakest evidence.

THE TRANSITIVITY HAZARD IS MEASURED, NOT ASSUMED.  The number of triples
(A,B,C) with A~B = 1.0 and B~C = 1.0 while A~C is < 1.0 or has no
comparable key at all is counted and reported.  Nothing is merged or
grouped on the strength of such a triple -- that is precisely what the
clique test refuses.

------------------------------------------------------------------
BOTH NUMBERS RIDE ON EVERY CONNECTOR.  Neither is chosen for the owner.
------------------------------------------------------------------
  (a) `weight_exact`   exact-match rate: the fraction of COMPARABLE keys
                       where the two output_canon strings are
                       byte-identical.
  (b) `weight_graded`  graded element similarity: the ruling-A
                       per-element numeric comparison of `l3_row_sim.py`
                       -- sign distance |s0-s1| in {0,2} -> 1 - d/2; mant
                       distance |m0-m1| with mants in [1,2) -> 1 - d
                       clamped at 0; expo distance through the decay
                       1/(1+|d|); combined by euclidean distance from
                       (1,1,1) normalised by sqrt(3) -- averaged over the
                       COMPARABLE keys.

EXPLORER PHYSICS -- preserved from v2/v3, unchanged:
  - internal connector springs near zero (%s against %s external) so they
    never dominate the layout;
  - the threshold cuts EXTERNAL connectors only;
  - components are counted on EXTERNAL connectors ONLY, always;
  - AUTOFIT RUNS ONCE THEN NEVER AGAIN; any wheel or mousedown disables
    it permanently; a "fit view" button exists.
  - NEW and stated rather than hidden: a group COHESION spring (%s) holds
    a group's members near each other so the hull is drawable.  It is not
    a connector, it carries no weight and it is never cut.

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree; the
OS-stopped outcome is ABORT.
"""

import csv
import itertools
import json
import math
import os
import sys
import time
from collections import defaultdict

import numpy as np

csv.field_size_limit(sys.maxsize)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l3_row_sim as S                                       # noqa: E402

CART = os.path.join(HERE, "matrices_cart")
SEP = ";"
LANGS = ("rust", "ruby")

RENDER_CAP = 20000
INT_SPRING = 0.0008          # ruling D, preserved
EXT_SPRING = 0.0060
GRP_SPRING = 0.0040          # group cohesion -- not a connector
CHUNK_ELEMS = 3_000_000      # broadcast block budget, ~3 M elements

__doc__ = __doc__ % (INT_SPRING, EXT_SPRING, GRP_SPRING)


# ==================================================================
# the canon alphabet, and the VECTORISED form of ruling A
# ==================================================================

FORM_ID = {S.DECLINE: 0, "numeric": 1, "text": 2, "container": 3,
           "truth": 4, "opaque": 5, "other": 6}


class Alphabet(object):
    """every distinct output string gets one integer, plus the element
    decomposition ruling A needs, so the similarity can be evaluated on
    whole arrays instead of one pair at a time."""

    def __init__(self):
        self.code = {}
        self.text = []

    def __call__(self, s):
        c = self.code.get(s)
        if c is None:
            c = len(self.text)
            self.code[s] = c
            self.text.append(s)
        return c

    def finalise(self):
        n = len(self.text)
        self.form = np.zeros(n, dtype=np.int8)
        self.decl = np.zeros(n, dtype=bool)
        self.numfin = np.zeros(n, dtype=bool)
        self.sgn = np.zeros(n, dtype=np.float64)
        self.mant = np.zeros(n, dtype=np.float64)
        self.expo = np.zeros(n, dtype=np.float64)
        self.t_len5 = np.zeros(n, dtype=bool)
        self.t_numok = np.zeros(n, dtype=bool)
        self.t_nfc = np.full(n, -1, dtype=np.int64)
        self.t2 = np.zeros(n, dtype=np.float64)
        self.t3 = np.zeros(n, dtype=np.float64)
        self.t4 = np.zeros(n, dtype=np.float64)
        nfc = {}
        for i, s in enumerate(self.text):
            f = S.form_of(s)
            self.form[i] = FORM_ID[f]
            if f == S.DECLINE:
                self.decl[i] = True
            elif f == "numeric":
                p = S.parse_numeric(s)
                if p is not None:
                    self.numfin[i] = True
                    self.sgn[i] = float(p[0])
                    self.mant[i] = float(p[1])
                    self.expo[i] = float(p[2])
            elif f == "text":
                fa = s.split("|")
                if len(fa) == 5:
                    self.t_len5[i] = True
                    k = nfc.setdefault(fa[1], len(nfc))
                    self.t_nfc[i] = k
                    try:
                        self.t2[i] = float(int(fa[2]))
                        self.t3[i] = float(int(fa[3]))
                        self.t4[i] = float(int(fa[4]))
                        self.t_numok[i] = True
                    except ValueError:
                        pass
        self.n_text_forms = int((self.form == FORM_ID["text"]).sum())

    # -------------------------------------------------- the vector sim
    def sim(self, a, b):
        """ruling-A similarity for two int32 code arrays of equal shape.
        Positions where either side declines are NOT masked here -- the
        caller multiplies by the validity mask, because ruling B removes
        them from the numerator and the denominator both."""
        same = (a == b)
        fa, fb = self.form[a], self.form[b]
        samef = (fa == fb)
        # ---- numeric, both finite: the ruling-A element comparison
        bn = samef & self.numfin[a] & self.numfin[b]
        s_s = 1.0 - np.abs(self.sgn[a] - self.sgn[b]) / S.SIGN_MAX_DISTANCE
        m_s = np.maximum(0.0, 1.0 - np.abs(self.mant[a] - self.mant[b]))
        e_s = 1.0 / (1.0 + S.EXPO_DECAY_K * np.abs(self.expo[a] -
                                                   self.expo[b]))
        d = np.sqrt((1.0 - s_s) ** 2 + (1.0 - m_s) ** 2 +
                    (1.0 - e_s) ** 2) / math.sqrt(3.0)
        num = np.clip(1.0 - d, 0.0, 1.0)
        # ---- text: identical NFC bytes -> 1, else the three-count decay
        tt = samef & (fa == FORM_ID["text"])
        out = np.where(bn, num, 0.0)
        if tt.any():
            ok = tt & self.t_len5[a] & self.t_len5[b]
            nfceq = ok & (self.t_nfc[a] == self.t_nfc[b])
            numok = ok & ~nfceq & self.t_numok[a] & self.t_numok[b]
            u2 = 1.0 / (1.0 + np.abs(self.t2[a] - self.t2[b]))
            u3 = 1.0 / (1.0 + np.abs(self.t3[a] - self.t3[b]))
            u4 = 1.0 / (1.0 + np.abs(self.t4[a] - self.t4[b]))
            td = np.sqrt((1.0 - u2) ** 2 + (1.0 - u3) ** 2 +
                         (1.0 - u4) ** 2) / math.sqrt(3.0)
            tv = np.clip(1.0 - td, 0.0, 1.0)
            out = np.where(nfceq, 1.0, np.where(numok, tv, out))
        # ---- every other form compares by identity; equal codes are 1.0
        return np.where(same, 1.0, out)


AB = Alphabet()


# ==================================================================
# load
# ==================================================================

def load_rows():
    idx = json.load(open(os.path.join(CART, "index.json")))
    # the operand sets are recorded ONCE, in index.json, never per row
    spell_canon = {}
    for name, xs in idx["x_sets"].items():
        for sp, cn in zip(xs["spellings"], xs["canon"]):
            if sp in spell_canon:
                assert spell_canon[sp] == cn, (
                    "spelling %r carries two canonical strings -- the "
                    "input key rule needs one" % sp)
            else:
                spell_canon[sp] = cn
    spell_id = {sp: i for i, sp in enumerate(sorted(spell_canon))}
    rows = []
    for key in sorted(idx["matrices"]):
        meta = idx["matrices"][key]
        lang = meta["language"]
        if lang not in LANGS:
            continue
        op, level = meta["operator"], meta["level"]
        p = os.path.join(CART, meta["file"])
        for r in csv.DictReader(open(p)):
            n = int(r["n_probes"])
            cells = r["output_canon_vector"].split(SEP)
            assert len(cells) == n, (key, r["probe_id"])
            sa, sb = r["x_set_a"], r["x_set_b"]
            na = idx["x_sets"][sa]["n"]
            nb = idx["x_sets"][sb]["n"]
            assert n == (na * nb if level == 1 else (na * nb) ** 2), (
                "probe count does not match the recorded operand sets")
            codes = np.fromiter((AB(c) for c in cells), dtype=np.int32,
                                count=n)
            rows.append(dict(
                key="%s.%s" % (lang, op), language=lang, operator=op,
                level=level, probe_id=r["probe_id"],
                lhs_holder=r["lhs_holder"], rhs_holder=r["rhs_holder"],
                form_pair=r["form_pair"], x_set_a=sa, x_set_b=sb,
                n_probes=n, codes=codes,
                n_values=int(r["n_values"]),
                n_declines=int(r["n_declines"])))
    return rows, idx, spell_id, spell_canon


def row_id(r):
    return "%s / L%d / %s / %s %s %s" % (
        r["key"], r["level"], r["probe_id"], r["lhs_holder"],
        r["operator"], r["rhs_holder"])


# ==================================================================
# CHANGE 1 -- the alignment itself
# ==================================================================

def key_positions(level, a_spell, b_spell, ia, ib):
    """the positions in a row's own probe vector, in shared-key order.

    `a_spell` / `b_spell` are the row's own operand spellings in
    enumeration order; `ia` / `ib` are the SHARED spellings, in the one
    order both sides agree on.  The probe-index rule of index.json is
    applied verbatim, and level 2 is the outer product of level 1 with
    itself because
        ((i0*|Xb| + i1)*|Xa| + i2)*|Xb| + i3 == q01*(|Xa|*|Xb|) + q23.
    """
    pa = {s: i for i, s in enumerate(a_spell)}
    pb = {s: i for i, s in enumerate(b_spell)}
    i0 = np.array([pa[s] for s in ia], dtype=np.int64)
    i1 = np.array([pb[s] for s in ib], dtype=np.int64)
    nb = len(b_spell)
    q = (i0[:, None] * nb + i1[None, :]).ravel()          # level-1 keys
    if level == 1:
        return q
    block = len(a_spell) * nb
    return (q[:, None] * block + q[None, :]).ravel()      # level-2 keys


class Aligner(object):
    """caches the shared-key index arrays per ORDERED pair of operand-set
    signatures.  Every row with the same signature shares them."""

    def __init__(self, x_sets):
        self.xs = x_sets
        self.cache = {}

    def shared(self, sig1, sig2):
        """(level, x_set_a, x_set_b) x2 -> (pos1, pos2, n_keys) or None"""
        k = (sig1, sig2)
        if k in self.cache:
            return self.cache[k]
        v = None
        if sig1[0] == sig2[0]:                 # NEVER mix level 1 and 2
            level = sig1[0]
            a1 = self.xs[sig1[1]]["spellings"]
            b1 = self.xs[sig1[2]]["spellings"]
            a2 = self.xs[sig2[1]]["spellings"]
            b2 = self.xs[sig2[2]]["spellings"]
            ia = sorted(set(a1) & set(a2))
            ib = sorted(set(b1) & set(b2))
            if ia and ib:
                p1 = key_positions(level, a1, b1, ia, ib)
                p2 = key_positions(level, a2, b2, ia, ib)
                assert p1.size == p2.size
                v = (p1, p2, int(p1.size), len(ia), len(ib))
        self.cache[k] = v
        return v


# ==================================================================
# CHANGE 2 CASE 1 -- CONTRACT
# ==================================================================

def contract(rows):
    """identity: same input key set AND byte-identical outputs at every
    key.  An equivalence relation, so no clique test is needed."""
    buckets = defaultdict(list)
    for i, r in enumerate(rows):
        sig = (r["level"], r["x_set_a"], r["x_set_b"])
        buckets[(sig, r["codes"].tobytes())].append(i)
    nodes = []
    for kk in sorted(buckets, key=lambda k: (k[0], buckets[k][0])):
        mem = buckets[kk]
        r0 = rows[mem[0]]
        nodes.append(dict(
            members=mem, sig=kk[0], level=r0["level"],
            x_set_a=r0["x_set_a"], x_set_b=r0["x_set_b"],
            codes=r0["codes"], n_probes=r0["n_probes"]))
    nodes.sort(key=lambda n: (n["level"], n["x_set_a"], n["x_set_b"],
                              n["members"][0]))
    return nodes


# ==================================================================
# scoring one ordered block pair, vectorised
# ==================================================================

def score_block(codes1, valid1, codes2, valid2, same_block):
    """(n1,K) x (n2,K) -> n_cmp, n_exact, sum_graded as (n1,n2) arrays."""
    n1, n2 = codes1.shape[0], codes2.shape[0]
    K = codes1.shape[1]
    f1 = valid1.astype(np.float64)
    f2 = valid2.astype(np.float64)
    n_cmp = (f1 @ f2.T)                       # BLAS, one shot
    n_exa = np.zeros((n1, n2), dtype=np.float64)
    s_grd = np.zeros((n1, n2), dtype=np.float64)
    step = max(1, int(CHUNK_ELEMS // max(1, n2 * K)))
    for lo in range(0, n1, step):
        hi = min(n1, lo + step)
        a = codes1[lo:hi][:, None, :]
        b = codes2[None, :, :]
        v = valid1[lo:hi][:, None, :] & valid2[None, :, :]
        eq = (a == b) & v
        n_exa[lo:hi] = eq.sum(axis=2, dtype=np.float64)
        aa = np.broadcast_to(a, (hi - lo, n2, K))
        bb = np.broadcast_to(b, (hi - lo, n2, K))
        s = AB.sim(aa, bb)
        s *= v
        s_grd[lo:hi] = s.sum(axis=2, dtype=np.float64)
        del a, b, v, eq, aa, bb, s
    if same_block:
        np.fill_diagonal(n_cmp, 0.0)
    return n_cmp, n_exa, s_grd


# ==================================================================
# maximal cliques -- Bron-Kerbosch with a pivot
# ==================================================================

def maximal_cliques(adj, min_size=2, cap=2_000_000):
    """adj: dict node -> set(node).  Yields every MAXIMAL clique.  A
    connected component is NOT a clique and is never returned; chaining
    through a pair that was never compared is exactly what this refuses.
    """
    out = []
    calls = [0]
    nodes = sorted(adj)

    def bk(R, P, X):
        calls[0] += 1
        if calls[0] > cap:
            raise RuntimeError("clique search exceeded %d calls" % cap)
        if not P and not X:
            if len(R) >= min_size:
                out.append(sorted(R))
            return
        piv = max(itertools.chain(P, X), key=lambda u: len(adj[u] & P))
        for v in sorted(P - adj[piv]):
            bk(R | {v}, P & adj[v], X & adj[v])
            P = P - {v}
            X = X | {v}

    seen = set()
    for comp_seed in nodes:                     # walk components, cheaply
        if comp_seed in seen:
            continue
        stack, comp = [comp_seed], set()
        while stack:
            u = stack.pop()
            if u in comp:
                continue
            comp.add(u)
            stack.extend(adj[u] - comp)
        seen |= comp
        if len(comp) < min_size:
            continue
        bk(set(), set(comp), set())
    out.sort(key=lambda c: (-len(c), c))
    return out, calls[0]


# ==================================================================
# helpers
# ==================================================================

def components(n, pairs):
    """`root` is the super-node of a merged set; the vocabulary is
    absolute and there is no p-word anywhere in this file."""
    root = list(range(n))

    def find(x):
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x

    for a, b in pairs:
        ra, rb = find(a), find(b)
        if ra != rb:
            root[ra] = rb
    grp = {}
    for i in range(n):
        grp.setdefault(find(i), []).append(i)
    return sorted(grp.values(), key=len, reverse=True)


def fmt(x, nd=4):
    return "--" if x is None else ("%.*f" % (nd, x))


def stat(vals):
    if not vals:
        return None
    v = sorted(vals)
    return dict(n=len(v), min=round(v[0], 6), max=round(v[-1], 6),
                mean=round(sum(v) / len(v), 6),
                median=round(v[len(v) // 2], 6))


def dist(vals):
    if not vals:
        return None
    v = sorted(vals)
    n = len(v)

    def q(p):
        return v[min(n - 1, int(p * n))]
    return dict(n=n, min=v[0], p25=q(0.25), median=q(0.50), p75=q(0.75),
                p90=q(0.90), max=v[-1],
                mean=round(sum(v) / float(n), 3),
                sum=int(sum(v)))


def histo(vals, edges):
    h = {}
    for i, e in enumerate(edges):
        lo = 1 if i == 0 else edges[i - 1] + 1
        h["%d-%d" % (lo, e)] = 0
    h["%d+" % (edges[-1] + 1)] = 0
    for v in vals:
        put = False
        for i, e in enumerate(edges):
            lo = 1 if i == 0 else edges[i - 1] + 1
            if lo <= v <= e:
                h["%d-%d" % (lo, e)] += 1
                put = True
                break
        if not put:
            h["%d+" % (edges[-1] + 1)] += 1
    return h


def selfcheck_sim(seed=20260821, n=40000):
    """the vectorised ruling A against `l3_row_sim.sample_sim`, one pair
    at a time, on a deterministic sample that forces every form."""
    import random
    rnd = random.Random(seed)
    m = len(AB.text)
    A = np.array([rnd.randrange(m) for _ in range(n)], dtype=np.int32)
    B = np.array([rnd.randrange(m) for _ in range(n)], dtype=np.int32)
    for f in sorted(set(int(x) for x in AB.form)):
        ids = [i for i in range(m) if AB.form[i] == f]
        if len(ids) < 2:
            continue
        for _ in range(n // 12):
            i = rnd.randrange(n)
            A[i] = rnd.choice(ids)
            B[i] = rnd.choice(ids)
    vec = AB.sim(A, B)
    worst, checked = 0.0, 0
    for i in range(n):
        ref = S.sample_sim(AB.text[A[i]], AB.text[B[i]])
        if ref is None:
            continue
        checked += 1
        worst = max(worst, abs(ref - float(vec[i])))
    assert worst < 1e-9, worst
    return checked, worst


# ==================================================================

def main():
    print("ROW GRAPH v4 -- the CARTESIAN probe design with the owner's three "
          "rulings of 2026-08-21.  ASSEMBLY ONLY, no probes were run.")
    print("  CHANGE 1 alignment: the comparable set of two rows is the "
          "INTERSECTION of their INPUT KEYS -- level 1 keyed by (x0,x1), "
          "level 2 by (x0,x1,x2,x3).  Level 1 is never mixed with level "
          "2.  Declines are never scored.  Zero comparable keys -> NO "
          "connector.")
    print("  CHANGE 2 collapse: CASE 1 CONTRACT is identity (same key "
          "set, byte-identical outputs) and needs no clique test; CASE 2 "
          "GROUP is a MAXIMAL CLIQUE of mutual exact-1.0 over partial "
          "overlaps and is a CONTAINER, not a merge.")
    print("  graded knobs: %s" % json.dumps(S.KNOBS))
    t0 = time.time()

    rows, cart_index, spell_id, spell_canon = load_rows()
    AB.finalise()
    for r in rows:
        r["id"] = row_id(r)
    ids = [r["id"] for r in rows]
    assert len(set(ids)) == len(ids), "row ids collide"
    langop_keys = sorted({r["key"] for r in rows})
    print("  %d raw rows, %d lang.op, %d distinct canon strings, %d "
          "operand spellings each with exactly one canon; by language %s; "
          "by level %s  (%.1f s)"
          % (len(rows), len(langop_keys), len(AB.text), len(spell_id),
             ", ".join("%s %d" % (l, sum(1 for r in rows
                                         if r["language"] == l))
                       for l in LANGS),
             ", ".join("L%d %d" % (l, sum(1 for r in rows
                                          if r["level"] == l))
                       for l in (1, 2)), time.time() - t0))
    nchk, worst = selfcheck_sim()
    print("  [selfcheck] the vectorised ruling A agrees with "
          "l3_row_sim.sample_sim on %d sampled non-decline canon pairs, "
          "worst absolute difference %.3e" % (nchk, worst))

    # ------------------------------------------------ CASE 1: CONTRACT
    cn = contract(rows)
    for k, node in enumerate(cn):
        node["idx"] = k
        node["id"] = "C%04d" % k
        mem = [rows[i] for i in node["members"]]
        r0 = mem[0]
        node["n_members"] = len(mem)
        node["member_rows"] = [r["id"] for r in mem]
        node["languages"] = sorted({r["language"] for r in mem})
        node["operators"] = sorted({r["key"] for r in mem})
        node["holder_pairs"] = sorted({"%s %s %s" % (r["lhs_holder"],
                                                     r["operator"],
                                                     r["rhs_holder"])
                                       for r in mem})
        node["form_pair"] = r0["form_pair"]
        node["probe_ids"] = sorted({r["probe_id"] for r in mem})
        node["label"] = "%s %s %s [L%d]%s" % (
            r0["lhs_holder"], r0["operator"], r0["rhs_holder"],
            r0["level"], "" if len(mem) == 1 else " x%d" % len(mem))
        d = AB.decl[node["codes"]]
        node["valid"] = ~d
        node["n_declines"] = int(d.sum())
        node["n_valid_keys"] = int(node["n_probes"] - node["n_declines"])
    print("  CONTRACT (case 1, identity): %d raw rows -> %d contracted "
          "nodes; %d nodes carry more than one row  (%.1f s)"
          % (len(rows), len(cn),
             sum(1 for n in cn if n["n_members"] > 1), time.time() - t0))
    csz = sorted((n["n_members"] for n in cn), reverse=True)
    print("     member-count histogram %s"
          % json.dumps(histo(csz, [1, 2, 4, 8, 16, 32, 64])))

    # --------------------------------------------- CHANGE 1: alignment
    aligner = Aligner(cart_index["x_sets"])
    bysig = defaultdict(list)
    for n in cn:
        bysig[n["sig"]].append(n["idx"])
    sigs = sorted(bysig)
    print("  %d operand-set signatures (level + both operand-set ids); "
          "sizes %s" % (len(sigs),
                        sorted((len(v) for v in bysig.values()),
                               reverse=True)[:10]))

    pair = {}                       # (i,j) i<j -> dict
    n_sig_pairs = n_sig_skipped = 0
    for x in range(len(sigs)):
        for y in range(x, len(sigs)):
            s1, s2 = sigs[x], sigs[y]
            sh = aligner.shared(s1, s2)
            if sh is None:
                n_sig_skipped += 1
                continue
            p1, p2, K, nia, nib = sh
            b1, b2 = bysig[s1], bysig[s2]
            same = (x == y)
            C1 = np.stack([cn[i]["codes"][p1] for i in b1])
            V1 = np.stack([cn[i]["valid"][p1] for i in b1])
            if same:
                C2, V2 = C1, V1
            else:
                C2 = np.stack([cn[i]["codes"][p2] for i in b2])
                V2 = np.stack([cn[i]["valid"][p2] for i in b2])
            ncmp, nexa, sgrd = score_block(C1, V1, C2, V2, same)
            n_sig_pairs += 1
            for u in range(len(b1)):
                i = b1[u]
                v0 = u + 1 if same else 0
                for v in range(v0, len(b2)):
                    j = b2[v]
                    nc = int(ncmp[u, v])
                    a, b = (i, j) if i < j else (j, i)
                    rec = pair.get((a, b))
                    if rec is None:
                        pair[(a, b)] = rec = dict(
                            level=s1[0], n_shared_keys=K, n_comparable=nc,
                            n_matched_exact=int(nexa[u, v]),
                            sum_graded=float(sgrd[u, v]),
                            n_shared_a=nia, n_shared_b=nib)
                    else:
                        assert False, "signature pair visited twice"
            del C1, V1, C2, V2, ncmp, nexa, sgrd
        print("      signatures %d/%d, %d pair records, %.1f s"
              % (x + 1, len(sigs), len(pair), time.time() - t0),
              end="\r")
    print(" " * 78, end="\r")
    print("  scored %d of %d signature pairs (%d had NO shared operand "
          "in one side or the other level, so no key can be shared); "
          "%d contracted-node pairs share at least one input key  "
          "(%.1f s)"
          % (n_sig_pairs, n_sig_pairs + n_sig_skipped, n_sig_skipped,
             len(pair), time.time() - t0))

    # self overlap of a contracted node with itself -- needed to count
    # ROW pairs inside one contracted node
    for n in cn:
        n["n_self_comparable"] = n["n_valid_keys"]

    # ------------------------------------------- BEFORE / AFTER, rows
    before_universe = before_conn = after_universe = after_conn = 0
    moved = 0
    ncmp_all = []
    for (i, j), rec in pair.items():
        mi, mj = cn[i]["n_members"], cn[j]["n_members"]
        rp = mi * mj
        same_sig = cn[i]["sig"] == cn[j]["sig"]
        has = rec["n_comparable"] > 0
        after_universe += rp
        if has:
            after_conn += rp
            ncmp_all.extend([rec["n_comparable"]] * rp)
        if same_sig:
            before_universe += rp
            if has:
                before_conn += rp
        if has and not same_sig:
            moved += rp
    for n in cn:
        m = n["n_members"]
        rp = m * (m - 1) // 2
        if rp:
            before_universe += rp
            after_universe += rp
            if n["n_self_comparable"] > 0:
                before_conn += rp
                after_conn += rp
                ncmp_all.extend([n["n_self_comparable"]] * rp)
    print("  ALIGNMENT BEFORE/AFTER, counted on RAW ROW PAIRS so it is "
          "directly comparable with log 052:")
    print("     v3 rule (entire input vector byte-identical): %d row "
          "pairs comparable, %d carry a connector, %d have ZERO "
          "comparable positions"
          % (before_universe, before_conn, before_universe - before_conn))
    print("     v4 rule (INTERSECTION of input keys):         %d row "
          "pairs comparable, %d carry a connector, %d have ZERO "
          "comparable keys"
          % (after_universe, after_conn, after_universe - after_conn))
    print("     %d row pairs GAIN a connector (%+.1f%%); %d of those were "
          "outside the v3 comparable universe altogether -- v3 could not "
          "see them at all"
          % (after_conn - before_conn,
             100.0 * (after_conn - before_conn) / max(1, before_conn),
             moved))
    print("     n_comparable over the row pairs that carry a connector: "
          "%s" % json.dumps(dist(ncmp_all)))
    print("     n_comparable histogram %s"
          % json.dumps(histo(ncmp_all, [1, 4, 16, 64, 256, 1024, 4096])))
    nc_nodes = [r["n_comparable"] for r in pair.values()
                if r["n_comparable"] > 0]
    print("     n_comparable over CONTRACTED-NODE connectors: %s"
          % json.dumps(dist(nc_nodes)))
    print("     n_comparable histogram %s"
          % json.dumps(histo(nc_nodes, [1, 4, 16, 64, 256, 1024, 4096])))

    # ----------------------------------------- connectors, ext vs int
    external = []
    co_scores = defaultdict(lambda: defaultdict(list))
    for (i, j), rec in pair.items():
        if rec["n_comparable"] == 0:
            continue
        nc = rec["n_comparable"]
        we = round(rec["n_matched_exact"] / float(nc), 6)
        wg = round(rec["sum_graded"] / float(nc), 6)
        rec["weight_exact"] = we
        rec["weight_graded"] = wg
        a, b = cn[i], cn[j]
        shared_ops = set(a["operators"]) & set(b["operators"])
        if shared_ops:
            for k in shared_ops:
                co_scores[i][k].append((we, wg))
                co_scores[j][k].append((we, wg))
            rec["internalish"] = True
            continue
        external.append(dict(
            kind="external", a=a["id"], b=b["id"], level=rec["level"],
            n_shared_keys=rec["n_shared_keys"],
            n_comparable=nc,
            n_excluded_declines=rec["n_shared_keys"] - nc,
            n_matched_exact=rec["n_matched_exact"],
            weight_exact=we, weight_graded=wg,
            cross_language=len(set(a["languages"]) |
                               set(b["languages"])) > 1,
            same_key_set=(a["sig"] == b["sig"])))
    n_internalish = sum(1 for r in pair.values()
                        if r.get("internalish"))
    print("  connectors: %d EXTERNAL (the two contracted nodes share no "
          "lang.op), %d contracted-node pairs share a lang.op and feed "
          "the INTERNAL connectors instead, %d pairs have zero comparable "
          "keys and get NO connector"
          % (len(external), n_internalish,
             sum(1 for r in pair.values() if r["n_comparable"] == 0)))

    internal = []
    for n in cn:
        sc = co_scores.get(n["idx"], {})
        for k in n["operators"]:
            lst = sc.get(k, [])
            if lst:
                internal.append(dict(
                    kind="internal", a=n["id"], b=k,
                    weight_exact=round(sum(x[0] for x in lst) / len(lst), 6),
                    weight_graded=round(sum(x[1] for x in lst) / len(lst), 6),
                    n_co_nodes_comparable=len(lst), no_comparison=False))
            else:
                internal.append(dict(
                    kind="internal", a=n["id"], b=k, weight_exact=1.0,
                    weight_graded=1.0, n_co_nodes_comparable=0,
                    no_comparison=True))
    nnc = sum(1 for e in internal if e["no_comparison"])
    print("  %d internal connectors (one per contracted node per lang.op "
          "it carries); %d carry no_comparison -- no co-node of that "
          "lang.op shares a comparable input key with them"
          % (len(internal), nnc))

    # ------------------------------------------------- CASE 2: GROUP
    adj = {n["idx"]: set() for n in cn}
    one_pairs = []
    for (i, j), rec in pair.items():
        if rec["n_comparable"] >= 1 and rec.get("weight_exact") == 1.0:
            adj[i].add(j)
            adj[j].add(i)
            one_pairs.append((i, j, rec["n_comparable"]))
    deg = sorted((len(v) for v in adj.values()), reverse=True)
    print("  GROUP graph (case 2): %d mutually exact-1.0 contracted-node "
          "pairs with n_comparable >= 1; %d nodes have at least one such "
          "co-node; largest degree %d"
          % (len(one_pairs), sum(1 for v in adj.values() if v),
             deg[0] if deg else 0))

    cliques, ncalls = maximal_cliques(adj, min_size=2)
    print("  %d MAXIMAL CLIQUES of size >= 2 found in %d Bron-Kerbosch "
          "calls.  A clique is COMPLETE LINKAGE: every pair inside it was "
          "actually compared and every pair scored exact 1.0.  A connected "
          "component is NOT used and never will be."
          % (len(cliques), ncalls))

    ovl = {}
    for i, j, nc in one_pairs:
        ovl[(i, j)] = nc
    groups = []
    for gi, cl in enumerate(cliques):
        po = []
        for a, b in itertools.combinations(cl, 2):
            k = (a, b) if a < b else (b, a)
            po.append(dict(a=cn[k[0]]["id"], b=cn[k[1]]["id"],
                           n_comparable=ovl[k]))
        mn = min(p["n_comparable"] for p in po)
        mx = max(p["n_comparable"] for p in po)
        lv = {cn[i]["level"] for i in cl}
        assert len(lv) == 1, "a group must not mix levels"
        groups.append(dict(
            id="G%03d" % gi, members=[cn[i]["id"] for i in cl],
            member_idx=list(cl), size=len(cl), level=lv.pop(),
            min_overlap=mn, max_overlap=mx,
            n_rows=sum(cn[i]["n_members"] for i in cl),
            languages=sorted({l for i in cl for l in cn[i]["languages"]}),
            operators=sorted({o for i in cl for o in cn[i]["operators"]}),
            pair_overlaps=po))
    groups.sort(key=lambda g: (-g["size"], g["min_overlap"]))
    for gi, g in enumerate(groups):
        g["id"] = "G%03d" % gi
    in_group = set()
    for g in groups:
        in_group.update(g["member_idx"])
    multi = defaultdict(int)
    for g in groups:
        for i in g["member_idx"]:
            multi[i] += 1
    n_multi = sum(1 for v in multi.values() if v > 1)
    print("     %d groups; sizes %s; %d contracted nodes sit in a group, "
          "%d of them in more than one (a maximal clique is not a "
          "partition and overlap is real, not an error)"
          % (len(groups), [g["size"] for g in groups[:15]],
             len(in_group), n_multi))

    # ------------------------------------- the transitivity HAZARD
    hazard = hazard_nocmp = hazard_lt1 = 0
    oneset = {i: set(v) for i, v in adj.items()}
    for b in sorted(adj):
        nb = sorted(oneset[b])
        for x in range(len(nb)):
            for y in range(x + 1, len(nb)):
                a, c = nb[x], nb[y]
                if c in oneset[a]:
                    continue
                k = (a, c) if a < c else (c, a)
                rec = pair.get(k)
                if rec is None or rec["n_comparable"] == 0:
                    hazard_nocmp += 1
                else:
                    hazard_lt1 += 1
                hazard += 1
    print("  TRANSITIVITY HAZARD: %d triples (A,B,C) with A~B = 1.0 and "
          "B~C = 1.0 while A~C is NOT 1.0 -- %d of them because A~C is "
          "< 1.0 on keys they do share, %d because A and C have NO "
          "comparable key at all.  None of them is merged and none is "
          "grouped: that is what the clique test is for."
          % (hazard, hazard_lt1, hazard_nocmp))

    # -------------------------------------------------------- nodes
    nodes = []
    for k in langop_keys:
        lang, _, op = k.partition(".")
        nodes.append(dict(
            id=k, kind="central", language=lang, operator=op,
            n_rows=sum(1 for r in rows if r["key"] == k),
            n_contracted=sum(1 for n in cn if k in n["operators"])))
    for n in cn:
        nodes.append(dict(
            id=n["id"], kind="contracted", level=n["level"],
            label=n["label"], n_members=n["n_members"],
            members=n["member_rows"], languages=n["languages"],
            operators=n["operators"], holder_pairs=n["holder_pairs"],
            probe_ids=n["probe_ids"], form_pair=n["form_pair"],
            language=n["languages"][0], operator=n["operators"][0]
            .partition(".")[2],
            x_set_a=n["x_set_a"], x_set_b=n["x_set_b"],
            n_probes=n["n_probes"], n_input_keys=n["n_probes"],
            n_declines=n["n_declines"],
            n_valid_keys=n["n_valid_keys"]))
    nid = {n["id"]: i for i, n in enumerate(nodes)}
    for g in groups:
        g["member_node_idx"] = [nid[cn[i]["id"]] for i in g["member_idx"]]
        del g["member_idx"]
    edges = internal + external

    # =============================================== SANITY, printed
    print("SANITY")
    print("  node counts: %d raw rows -> %d contracted nodes -> %d groups"
          % (len(rows), len(cn), len(groups)))
    print("  group sizes: %s" % [g["size"] for g in groups])
    print("  nodes emitted: %d contracted + %d central lang.op = %d"
          % (len(cn), len(langop_keys), len(nodes)))
    print("  connectors emitted: %d internal + %d external = %d"
          % (len(internal), len(external), len(edges)))

    def report_contracted(title, pool, k=6):
        recs = []
        for n in pool[:k]:
            recs.append(dict(id=n["id"], n_members=n["n_members"],
                             level=n["level"], form_pair=n["form_pair"],
                             languages=n["languages"],
                             operators=n["operators"],
                             members=n["member_rows"],
                             n_input_keys=n["n_probes"],
                             n_declines=n["n_declines"],
                             n_valid_keys=n["n_valid_keys"]))
            print("     %s  %d rows  L%d  %s  %d input keys, %d of them "
                  "carry a value  operators %s"
                  % (n["id"], n["n_members"], n["level"], n["form_pair"],
                     n["n_probes"], n["n_valid_keys"],
                     ", ".join(n["operators"])))
            for m in n["member_rows"]:
                print("         %s" % m)
        return recs

    print("  LARGEST CONTRACTED NODES (case 1, identity) -- ALL of them, "
          "including the ones whose every output is a decline")
    largest_contracted = report_contracted(
        "all", sorted(cn, key=lambda n: -n["n_members"]))
    print("  LARGEST CONTRACTED NODES THAT CARRY AT LEAST ONE VALUE -- "
          "the same rule, with the all-decline nodes set aside, because a "
          "node whose every key declines agrees with nothing and is "
          "compared with nothing")
    largest_contracted_with_value = report_contracted(
        "with value", sorted([n for n in cn if n["n_valid_keys"] > 0],
                             key=lambda n: -n["n_members"]))
    n_alldecline = sum(1 for n in cn if n["n_valid_keys"] == 0)
    print("     %d of the %d contracted nodes are all-decline (%d rows)"
          % (n_alldecline, len(cn),
             sum(n["n_members"] for n in cn if n["n_valid_keys"] == 0)))

    print("  THE ALIASES the owner named")
    alias_check = {}
    for want in (("ruby.&&", "ruby.and"), ("ruby.||", "ruby.or")):
        hit = [n for n in cn if set(want) <= set(n["operators"])]
        alias_check["%s + %s contracted together" % want] = dict(
            n_contracted_nodes=len(hit),
            n_rows=sum(n["n_members"] for n in hit),
            by_level={"L%d" % l: sum(1 for n in hit if n["level"] == l)
                      for l in (1, 2)},
            nodes=[n["id"] for n in hit])
        print("     %s and %s land in the SAME contracted node %d times "
              "(%d rows; L1 %d, L2 %d) -- case 1, identity, no clique "
              "test needed"
              % (want[0], want[1], len(hit),
                 sum(n["n_members"] for n in hit),
                 sum(1 for n in hit if n["level"] == 1),
                 sum(1 for n in hit if n["level"] == 2)))
    holder_check = {}
    for lang, hs in (("ruby", ("Integer", "Rational", "BigDecimal",
                               "Float")),):
        hit = []
        for n in cn:
            hh = {p.split(" ")[0] for p in n["holder_pairs"]}
            hh |= {p.split(" ")[-1] for p in n["holder_pairs"]}
            if len(hh & set(hs)) >= 3:
                hit.append((len(hh & set(hs)), n))
        hit.sort(key=lambda x: -x[0])
        holder_check[lang] = dict(
            n_nodes_spanning_3plus_holders=len(hit),
            top=[dict(id=n["id"], n_members=n["n_members"],
                      holders=sorted({p.split(" ")[0] for p in
                                      n["holder_pairs"]} |
                                     {p.split(" ")[-1] for p in
                                      n["holder_pairs"]}),
                      operators=n["operators"]) for _, n in hit[:6]])
        print("     %d contracted nodes span 3 or more of ruby's four "
              "numeric holder spellings %s" % (len(hit), list(hs)))
        for _, n in hit[:4]:
            hh = sorted({p.split(" ")[0] for p in n["holder_pairs"]} |
                        {p.split(" ")[-1] for p in n["holder_pairs"]})
            print("         %s  %d rows  L%d  holders %s  operators %s"
                  % (n["id"], n["n_members"], n["level"], hh,
                     ", ".join(n["operators"])))

    mo = [g["min_overlap"] for g in groups]
    print("  GROUP MINIMUM OVERLAP -- the weakest evidence each group "
          "rests on: %s" % json.dumps(dist(mo)))
    print("     histogram %s"
          % json.dumps(histo(mo, [1, 2, 4, 16, 64, 256, 1024])))
    thin = [g for g in groups if g["min_overlap"] <= 4]
    print("     %d of the %d groups rest on 4 or fewer shared keys at "
          "their weakest pair.  Those are REPORTED, not suppressed: the "
          "rule asks for the intersection and this is what the "
          "intersection gives.  The commonest cause is the two operand "
          "spellings `0` and `1`, which belong to the whole set AND to "
          "ruby's six-point truth set and carry the same canonical value "
          "in both, so a truth-form row and a whole-form row really do "
          "share those keys." % (len(thin), len(groups)))
    thin_conn = sum(1 for e in external if e["n_comparable"] <= 4)
    print("     %d of the %d external connectors likewise rest on 4 or "
          "fewer comparable keys" % (thin_conn, len(external)))

    def report_groups(pool, k=6):
        recs = []
        for g in pool[:k]:
            recs.append(dict(
                id=g["id"], size=g["size"], level=g["level"],
                min_overlap=g["min_overlap"],
                max_overlap=g["max_overlap"], n_rows=g["n_rows"],
                languages=g["languages"], operators=g["operators"],
                members=[dict(id=m, label=nodes[nid[m]]["label"],
                              n_members=nodes[nid[m]]["n_members"],
                              operators=nodes[nid[m]]["operators"])
                         for m in g["members"]]))
            print("     %s  %d contracted nodes (%d rows)  L%d  minimum "
                  "overlap %d keys, maximum %d  operators %s"
                  % (g["id"], g["size"], g["n_rows"], g["level"],
                     g["min_overlap"], g["max_overlap"],
                     ", ".join(g["operators"])))
            for m in g["members"]:
                nn = nodes[nid[m]]
                print("         %s  %-34s %d row(s)  %s"
                      % (m, nn["label"], nn["n_members"],
                         ", ".join(nn["operators"])))
        return recs

    print("  LARGEST GROUPS ON A MINIMUM OVERLAP OF AT LEAST 64 KEYS -- "
          "the groups whose weakest pair still rests on real evidence")
    strong_groups = report_groups(
        [g for g in groups if g["min_overlap"] >= 64])

    print("  LARGEST GROUPS (case 2, maximal clique over partial "
          "overlaps -- a CONTAINER, not a merge)")
    largest_groups = []
    for g in groups[:8]:
        rec = dict(id=g["id"], size=g["size"], level=g["level"],
                   min_overlap=g["min_overlap"],
                   max_overlap=g["max_overlap"], n_rows=g["n_rows"],
                   languages=g["languages"], operators=g["operators"],
                   members=[dict(id=m,
                                 label=nodes[nid[m]]["label"],
                                 n_members=nodes[nid[m]]["n_members"],
                                 operators=nodes[nid[m]]["operators"])
                            for m in g["members"]])
        largest_groups.append(rec)
        print("     %s  %d contracted nodes (%d rows)  L%d  minimum "
              "overlap %d keys, maximum %d  operators %s"
              % (g["id"], g["size"], g["n_rows"], g["level"],
                 g["min_overlap"], g["max_overlap"],
                 ", ".join(g["operators"])))
        for m in g["members"]:
            nn = nodes[nid[m]]
            print("         %s  %-34s %d row(s)  %s"
                  % (m, nn["label"], nn["n_members"],
                     ", ".join(nn["operators"])))

    # ------------------------------------------ thresholds, two views
    def collapse_pairs():
        out = []
        for g in groups:
            mi = g["member_node_idx"]
            for k in range(1, len(mi)):
                out.append((mi[0], mi[k]))
        return out

    sanity_thresholds = {}
    for view, extra in (("expanded", []), ("collapsed", collapse_pairs())):
        for mode in ("exact", "graded"):
            w = "weight_" + mode
            for t in (0.95, 0.85, 0.70):
                act = [e for e in external if e[w] >= t]
                xl = sum(1 for e in act if e["cross_language"])
                comps = components(
                    len(nodes),
                    [(nid[e["a"]], nid[e["b"]]) for e in act] + extra)
                big = comps[0]
                mult = [c for c in comps if len(c) > 1]
                rec = dict(view=view, external_edges=len(act),
                           cross_language=xl, same_language=len(act) - xl,
                           components_external_only=len(comps),
                           largest_component=len(big),
                           multi_node_components=len(mult),
                           by_level={"L%d" % l: sum(1 for e in act
                                                    if e["level"] == l)
                                     for l in (1, 2)})
                sanity_thresholds["%s/%s@%.2f" % (view, mode, t)] = rec
                print("  %-9s %-6s t=%.2f : %d external (%d same-language,"
                      " %d cross-language; L1 %d, L2 %d); components "
                      "(EXTERNAL ONLY) %d (%d multi-node), largest %d"
                      % (view, mode, t, len(act), len(act) - xl, xl,
                         rec["by_level"]["L1"], rec["by_level"]["L2"],
                         len(comps), len(mult), len(big)))

    # ------------------------------------------- the named cross-checks
    byrow = {r["id"]: r for r in rows}
    node_of_row = {}
    for n in cn:
        for m in n["member_rows"]:
            node_of_row[m] = n["idx"]

    def row_pairs(ka, kb, level):
        """every ROW pair with one side on lang.op ka and the other on
        kb at `level`, with the score the new alignment gives it.  Rows
        inside ONE contracted node are reported as CONTRACTED: identical
        outputs on an identical key set, which is a stronger statement
        than a 1.0 connector."""
        ra = [r for r in rows if r["key"] == ka and r["level"] == level]
        rb = [r for r in rows if r["key"] == kb and r["level"] == level]
        out = []
        for x in ra:
            for y in rb:
                if x["id"] == y["id"]:
                    continue
                i, j = node_of_row[x["id"]], node_of_row[y["id"]]
                if i == j:
                    out.append(dict(contracted=True,
                                    weight_exact=1.0, weight_graded=1.0,
                                    n_comparable=cn[i]["n_self_comparable"],
                                    n_shared_keys=cn[i]["n_probes"]))
                    continue
                k = (i, j) if i < j else (j, i)
                rec = pair.get(k)
                if rec is None or rec["n_comparable"] == 0:
                    continue
                out.append(dict(contracted=False,
                                weight_exact=rec["weight_exact"],
                                weight_graded=rec["weight_graded"],
                                n_comparable=rec["n_comparable"],
                                n_shared_keys=rec["n_shared_keys"]))
        return out

    def v3_row_pairs(ka, kb, level):
        """the same count under the v3 rule, for the before/after."""
        ra = [r for r in rows if r["key"] == ka and r["level"] == level]
        rb = [r for r in rows if r["key"] == kb and r["level"] == level]
        n = 0
        for x in ra:
            for y in rb:
                if x["id"] == y["id"]:
                    continue
                if (x["x_set_a"], x["x_set_b"]) != (y["x_set_a"],
                                                    y["x_set_b"]):
                    continue
                i, j = node_of_row[x["id"]], node_of_row[y["id"]]
                if i == j:
                    n += 1 if cn[i]["n_self_comparable"] > 0 else 0
                    continue
                k = (i, j) if i < j else (j, i)
                rec = pair.get(k)
                if rec is not None and rec["n_comparable"] > 0:
                    n += 1
        return n

    PAIRS = [("ruby.&&", "ruby.||"), ("ruby.&&", "ruby.and"),
             ("ruby.||", "ruby.or"), ("rust.+", "ruby.+"),
             ("rust.+", "rust.-")]
    named = {}
    print("  THE NAMED PAIRS under the new alignment -- expanded to ROW "
          "pairs so the numbers sit beside log 052's")
    for ka, kb in PAIRS:
        rec = {}
        print("     %s ~ %s" % (ka, kb))
        for level in (1, 2):
            sel = row_pairs(ka, kb, level)
            v3n = v3_row_pairs(ka, kb, level)
            if not sel:
                print("         L%d  NO connector and no contraction"
                      % level)
                rec["L%d" % level] = dict(n_row_pairs=0, v3_n_row_pairs=v3n)
                continue
            ctr = [s for s in sel if s["contracted"]]
            con = [s for s in sel if not s["contracted"]]
            ex = stat([s["weight_exact"] for s in sel])
            gr = stat([s["weight_graded"] for s in sel])
            rec["L%d" % level] = dict(
                n_row_pairs=len(sel), n_contracted_row_pairs=len(ctr),
                n_connector_row_pairs=len(con),
                v3_n_row_pairs=v3n, exact=ex, graded=gr,
                n_comparable=dist([s["n_comparable"] for s in sel]))
            print("         L%d  %4d row pairs (%d CONTRACTED into one "
                  "node, %d on a connector); v3 saw %d | exact max %s "
                  "mean %s min %s | graded max %s mean %s min %s | "
                  "n_comparable min %d median %d max %d"
                  % (level, len(sel), len(ctr), len(con), v3n,
                     fmt(ex["max"]), fmt(ex["mean"]), fmt(ex["min"]),
                     fmt(gr["max"]), fmt(gr["mean"]), fmt(gr["min"]),
                     rec["L%d" % level]["n_comparable"]["min"],
                     rec["L%d" % level]["n_comparable"]["median"],
                     rec["L%d" % level]["n_comparable"]["max"]))
        named["%s ~ %s" % (ka, kb)] = rec

    # ------------------------------------------------------------ emit
    out = dict(
        status="ROW GRAPH v4 -- the CARTESIAN probe design with the owner's "
               "three rulings of 2026-08-21: INPUT-KEY INTERSECTION "
               "alignment, CONTRACT (case 1, identity) and GROUP (case 2, "
               "maximal clique over partial overlaps).  ASSEMBLY ONLY -- "
               "no probe was run for this build.",
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        scope="rust (static) + ruby (route C) only; the other ten wait",
        source="matrices_cart/ -- level 1 y = op(x0,x1) over all ordered "
               "pairs of X, level 2 z = op(op(x0,x1), op(x2,x3)) over X'.  "
               "Operands are recorded ONCE PER SET in index.json, never "
               "per row; a position is reconstructed from the probe-index "
               "rule.",
        alignment_rule="THE COMPARABLE SET OF TWO ROWS IS THE INTERSECTION "
                       "OF THEIR INPUT KEYS.  A level-1 key is the operand "
                       "pair (x0,x1); a level-2 key is the operand quad "
                       "(x0,x1,x2,x3).  An operand is identified by its "
                       "SPELLING, globally unique and carrying exactly one "
                       "canonical string.  Outputs are compared at each "
                       "SHARED key.  A shared key where either side "
                       "declines is excluded from numerator and "
                       "denominator both.  ZERO comparable keys after "
                       "exclusion -> NO CONNECTOR, a genuine absence of "
                       "evidence.  LEVEL 1 IS NEVER MIXED WITH LEVEL 2 in "
                       "one connector and every connector records its "
                       "level.",
        contract_rule="CASE 1, CONTRACT (identity).  Rows whose INPUT KEY "
                      "SET is IDENTICAL and whose outputs are "
                      "BYTE-IDENTICAL AT EVERY KEY are the same function "
                      "on the same domain and are contracted into ONE "
                      "node.  This is plain identity, an equivalence "
                      "relation, so it is transitive and needs NO clique "
                      "test.  The contracted node carries its member row "
                      "ids, its member count, its languages and its "
                      "operators.",
        group_rule="CASE 2, GROUP (agreement over a partial overlap).  "
                   "Contracted nodes that are mutually exact-1.0 on their "
                   "OVERLAPS but whose input key sets DIFFER are NOT "
                   "contracted.  They are GROUPED: a group is a set in "
                   "which EVERY PAIR is mutually exact-1.0 with "
                   "n_comparable >= 1 -- a MAXIMAL CLIQUE, complete "
                   "linkage.  It is NEVER a connected component, because "
                   "chaining through never-compared pairs is exactly what "
                   "this avoids.  The group is a CONTAINER, NOT A MERGE: "
                   "members stay distinct nodes, and the group carries "
                   "every pair's overlap size plus the MINIMUM overlap as "
                   "its weakest evidence.",
        transitivity_rule="The transitivity hazard is MEASURED, not "
                          "assumed: the number of triples (A,B,C) with "
                          "A~B = 1.0 and B~C = 1.0 while A~C is < 1.0 or "
                          "has no comparable key.  Nothing is merged or "
                          "grouped on the strength of such a triple.",
        scoring_a="EXACT-MATCH RATE: the fraction of COMPARABLE keys where "
                  "the two output_canon strings are byte-identical.",
        scoring_b="GRADED ELEMENT SIMILARITY: the ruling-A per-element "
                  "numeric comparison of l3_row_sim.py -- sign distance "
                  "|s0-s1| in {0,2} -> 1 - d/2; mant distance |m0-m1| with "
                  "mants in [1,2) -> 1 - d clamped at 0; expo distance "
                  "through the decay 1/(1+|d|); combined by euclidean "
                  "distance from (1,1,1) normalised by sqrt(3) -- averaged "
                  "over the COMPARABLE keys.",
        declines="NEVER SCORED.  A key where either side is REFUSE, "
                 "RAISE:* or ABORT leaves the numerator AND the "
                 "denominator, for both numbers alike.  Zero comparable "
                 "keys -> no connector at all.",
        sigmoid_rule="graded mode maps g through w = (s(g)-s(0))/(s(1)-s(0))"
                     " with s(x) = 1/(1+exp(-k(x-m))), m the MIDPOINT "
                     "slider and k the STEEPNESS slider.  k -> 0 gives "
                     "w = g exactly (the raw graded score); large k gives "
                     "a step at m, the exact-match-style hard cut.  It is "
                     "a DISPLAY rule: no stored number is rewritten.",
        physics="internal springs near zero (%g against %g external) so "
                "they never dominate the layout; a group COHESION spring "
                "(%g) holds a group's members near each other so the hull "
                "is drawable -- it is not a connector, carries no weight "
                "and is never cut; the threshold cuts EXTERNAL connectors "
                "ONLY; components are counted on EXTERNAL connectors ONLY; "
                "autofit runs ONCE then never again and any wheel or "
                "mousedown disables it permanently; a fit view button "
                "exists." % (INT_SPRING, EXT_SPRING, GRP_SPRING),
        vocabulary="super-node / sub-node / co-node / sub-tree; the "
                   "OS-stopped outcome is ABORT",
        scoring_knobs=S.KNOBS,
        int_spring=INT_SPRING, ext_spring=EXT_SPRING,
        grp_spring=GRP_SPRING, render_cap=RENDER_CAP,
        x_sets={k: {kk: vv for kk, vv in v.items() if kk != "canon"}
                for k, v in cart_index["x_sets"].items()},
        n_raw_rows=len(rows), n_contracted_nodes=len(cn),
        n_central_nodes=len(langop_keys), n_groups=len(groups),
        n_internal_edges=len(internal), n_external_edges=len(external),
        alignment_before_after=dict(
            v3_comparable_row_pairs=before_universe,
            v3_row_pairs_with_connector=before_conn,
            v3_row_pairs_zero_comparable=before_universe - before_conn,
            v4_comparable_row_pairs=after_universe,
            v4_row_pairs_with_connector=after_conn,
            v4_row_pairs_zero_comparable=after_universe - after_conn,
            row_pairs_gained=after_conn - before_conn,
            row_pairs_outside_v3_universe_now_with_evidence=moved,
            n_comparable_row_pairs=dist(ncmp_all),
            n_comparable_row_pairs_histogram=histo(
                ncmp_all, [1, 4, 16, 64, 256, 1024, 4096]),
            n_comparable_node_connectors=dist(nc_nodes),
            n_comparable_node_connectors_histogram=histo(
                nc_nodes, [1, 4, 16, 64, 256, 1024, 4096])),
        contraction=dict(
            raw_rows=len(rows), contracted_nodes=len(cn),
            nodes_with_more_than_one_row=sum(1 for n in cn
                                             if n["n_members"] > 1),
            member_count_histogram=histo(csz, [1, 2, 4, 8, 16, 32, 64]),
            all_decline_nodes=n_alldecline,
            largest=largest_contracted,
            largest_with_a_value=largest_contracted_with_value,
            alias_check=alias_check, holder_check=holder_check),
        grouping=dict(
            n_one_pairs=len(one_pairs), n_groups=len(groups),
            sizes=[g["size"] for g in groups],
            nodes_in_a_group=len(in_group),
            nodes_in_more_than_one_group=n_multi,
            min_overlap=dist(mo),
            min_overlap_histogram=histo(mo, [1, 2, 4, 16, 64, 256, 1024]),
            groups_on_4_or_fewer_shared_keys=len(thin),
            external_connectors_on_4_or_fewer_comparable_keys=thin_conn,
            bron_kerbosch_calls=ncalls, largest=largest_groups,
            largest_on_min_overlap_64_or_more=strong_groups),
        transitivity=dict(
            violating_triples=hazard,
            because_A_C_below_1=hazard_lt1,
            because_A_C_have_no_comparable_key=hazard_nocmp),
        sanity=dict(thresholds=sanity_thresholds, named=named),
        # the COMPLETE contracted-node pair table, so the verifier can
        # recheck the contraction, the cliques and the transitivity count
        # without re-deriving anything from a connector list that only
        # carries the external pairs.  Parallel arrays keep it small.
        pairs_compact=dict(
            note="every ordered-by-index pair (a,b) of contracted nodes "
                 "that shares at least one INPUT KEY.  nc = n_comparable "
                 "after the decline exclusion, ne = n_matched_exact, "
                 "nk = n_shared_keys before the exclusion.  a and b are "
                 "indices into `nodes` counted from the FIRST contracted "
                 "node, i.e. node index minus n_central_nodes.",
            n=len(pair),
            a=[k[0] for k in sorted(pair)],
            b=[k[1] for k in sorted(pair)],
            nc=[pair[k]["n_comparable"] for k in sorted(pair)],
            ne=[pair[k]["n_matched_exact"] for k in sorted(pair)],
            nk=[pair[k]["n_shared_keys"] for k in sorted(pair)]),
        groups=groups, nodes=nodes, edges=edges)

    jp = os.path.join(HERE, "row_graph_v4.json")
    json.dump(out, open(jp, "w"), separators=(",", ":"))
    print("  wrote %s (%.2f MB)" % (jp, os.path.getsize(jp) / 1e6))

    html = HTML_TEMPLATE.replace("__GRAPH__",
                                 json.dumps(out, separators=(",", ":")))
    hp = os.path.join(HERE, "row_graph_explorer_v4.html")
    with open(hp, "w") as f:
        f.write(html)
    print("  wrote %s (%.2f MB)" % (hp, os.path.getsize(hp) / 1e6))

    # ------------------------------------------- python-side verify
    print("PYTHON VERIFY")
    back = json.load(open(jp))
    assert len(back["nodes"]) == len(nodes)
    assert len(back["edges"]) == len(edges)
    idset = {n["id"] for n in back["nodes"]}
    assert all(e["a"] in idset and e["b"] in idset for e in back["edges"])
    assert all(0.0 <= e["weight_exact"] <= 1.0 for e in back["edges"])
    assert all(0.0 <= e["weight_graded"] <= 1.0 for e in back["edges"])
    print("  [json] %d nodes, %d connectors; every endpoint is a node; "
          "both weights in [0,1] on every connector"
          % (len(back["nodes"]), len(back["edges"])))

    # every contracted node is a TRUE identity set
    byid_row = {r["id"]: r for r in rows}
    for n in back["nodes"]:
        if n["kind"] != "contracted":
            continue
        mm = [byid_row[m] for m in n["members"]]
        ks = {(r["level"], r["x_set_a"], r["x_set_b"]) for r in mm}
        assert len(ks) == 1, "contracted node mixes input key sets"
        vv = {r["codes"].tobytes() for r in mm}
        assert len(vv) == 1, "contracted node mixes outputs"
        assert n["n_members"] == len(mm)
    assert sum(n["n_members"] for n in back["nodes"]
               if n["kind"] == "contracted") == len(rows)
    print("  [contract] every one of the %d contracted nodes is a TRUE "
          "identity set -- one input key set, one byte-identical output "
          "vector; the %d member rows partition the %d raw rows exactly"
          % (len(cn), sum(n["n_members"] for n in back["nodes"]
                          if n["kind"] == "contracted"), len(rows)))

    # every group is a TRUE clique
    idx_of = {n["id"]: k for k, n in enumerate(cn)}
    for g in back["groups"]:
        mi = [idx_of[m] for m in g["members"]]
        assert len({cn[i]["level"] for i in mi}) == 1
        seen_ov = []
        for a, b in itertools.combinations(mi, 2):
            k = (a, b) if a < b else (b, a)
            rec = pair.get(k)
            assert rec is not None, "group pair was never compared"
            assert rec["n_comparable"] >= 1, "group pair has no overlap"
            assert rec["weight_exact"] == 1.0, "group pair is not 1.0"
            seen_ov.append(rec["n_comparable"])
        assert g["min_overlap"] == min(seen_ov)
        assert g["max_overlap"] == max(seen_ov)
        assert len(g["pair_overlaps"]) == g["size"] * (g["size"] - 1) // 2
    # and maximal
    for g in back["groups"]:
        ms = {idx_of[m] for m in g["members"]}
        for other in adj:
            if other in ms:
                continue
            if ms <= adj[other]:
                raise AssertionError("group %s is not maximal" % g["id"])
    print("  [group] every one of the %d groups is a TRUE MAXIMAL CLIQUE: "
          "every pair inside was actually compared, every pair has "
          "n_comparable >= 1 and weight_exact == 1.0, min/max overlap "
          "agree with the pair list, and no node outside is joined to all "
          "of them" % len(groups))

    # external connectors
    byid = {n["id"]: n for n in back["nodes"]}
    for e in back["edges"]:
        if e["kind"] != "external":
            continue
        a, b = byid[e["a"]], byid[e["b"]]
        assert a["kind"] == b["kind"] == "contracted"
        assert not (set(a["operators"]) & set(b["operators"]))
        assert a["level"] == b["level"] == e["level"]
        assert e["n_comparable"] > 0
        assert (e["n_comparable"] + e["n_excluded_declines"] ==
                e["n_shared_keys"])
        assert e["n_matched_exact"] <= e["n_comparable"]
        assert e["n_shared_keys"] <= min(a["n_input_keys"],
                                         b["n_input_keys"])
    print("  [external] every external connector joins two contracted "
          "nodes with NO lang.op in common at the SAME level; "
          "n_comparable > 0, n_comparable + n_excluded_declines == "
          "n_shared_keys, and n_shared_keys never exceeds either side's "
          "own key count")
    got = defaultdict(set)
    for e in back["edges"]:
        if e["kind"] == "internal":
            got[e["a"]].add(e["b"])
    for n in cn:
        assert got[n["id"]] == set(n["operators"])
    print("  [internal] exactly one internal connector per contracted "
          "node per lang.op it carries, %d in all" % len(internal))
    txt = open(hp).read()
    assert '"nodes"' in txt and '"edges"' in txt and "__GRAPH__" not in txt
    assert "<script src" not in txt and "http://" not in txt
    print("  [html] embedded data present, placeholder gone, no external "
          "script, no CDN, no network reference")
    print("  done in %.1f s" % (time.time() - t0))


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Cartesian run &mdash; row graph v4 (input-key alignment, contract, group)</title>
<style>
 body{margin:0;font:13px/1.4 system-ui,sans-serif;background:#14161a;
      color:#d7dae0;display:flex;flex-direction:column;height:100vh}
 #bar{padding:7px 12px;background:#1d2026;display:flex;
      gap:14px;align-items:center;flex-wrap:wrap;
      border-bottom:1px solid #2b2f36}
 #bar b{color:#fff}
 input[type=range]{width:140px;vertical-align:middle}
 #search{background:#14161a;border:1px solid #3a3f48;color:#d7dae0;
         padding:3px 7px;border-radius:4px;width:190px}
 select,button{background:#14161a;border:1px solid #3a3f48;color:#d7dae0;
        padding:2px 5px;border-radius:4px}
 #stats{color:#9aa2ad}
 #rule{color:#7d8590;font-size:11px;padding:3px 12px;background:#191c21;
       border-bottom:1px solid #2b2f36}
 canvas{flex:1;display:block}
 #tip{position:fixed;pointer-events:none;background:#22262d;
      border:1px solid #3a3f48;border-radius:5px;padding:6px 9px;
      display:none;max-width:560px;z-index:9;font-size:12px}
 label{cursor:pointer;white-space:nowrap}
 .dim{opacity:.4}
</style></head><body>
<div id="bar">
 <b>Cartesian run &mdash; row graph v4</b>
 <label><input type="checkbox" id="exact"> <b>exact-match</b> cut/weight
  (unchecked = graded similarity)</label>
 <span>threshold
  <input type="range" id="thr" min="0" max="100" value="85">
  <span id="thrv">0.85</span></span>
 <span id="sigwrap">sigmoid midpoint
  <input type="range" id="mid" min="0" max="100" value="50">
  <span id="midv">0.50</span>
  &nbsp;steepness
  <input type="range" id="stp" min="0" max="6000" value="0">
  <span id="stpv">0.0</span></span>
 <label><input type="checkbox" id="showint" checked> internal
  connectors</label>
 <label><input type="checkbox" id="hulls" checked> group hulls</label>
 <label><input type="checkbox" id="collapseall"> collapse ALL groups</label>
 <span>level <select id="lmode">
  <option value="all">both levels</option>
  <option value="1">level 1 only</option>
  <option value="2">level 2 only</option></select></span>
 <span>colour <select id="cmode">
  <option value="lang">by language</option>
  <option value="op">by operator</option>
  <option value="level">by level</option>
  <option value="form">by form pair</option>
  <option value="members">by member count</option></select></span>
 <span>draw cap <select id="cap">
  <option value="1000">1000</option>
  <option value="4000">4000</option>
  <option value="20000" selected>20000</option>
  <option value="1000000">no cap</option></select></span>
 <input id="search" placeholder="search node / operator / holder / row">
 <button id="fitbtn">fit view</button>
 <button id="expandall">expand all groups</button>
 <span id="stats"></span>
</div>
<div id="rule"></div>
<canvas id="cv"></canvas><div id="tip"></div>
<script>
const G=__GRAPH__;
const N=G.nodes,E=G.edges,GR=G.groups;
const idx={};N.forEach((n,i)=>{idx[n.id]=i;});
E.forEach(e=>{e.ai=idx[e.a];e.bi=idx[e.b];});
const INT=E.filter(e=>e.kind==="internal");
const EXT=E.filter(e=>e.kind==="external").map((e,i)=>(e._o=i,e));
const intOf={};INT.forEach(e=>{(intOf[e.a]=intOf[e.a]||[]).push(e);});
// a group is a CONTAINER, not a merge: its members stay distinct nodes.
// `gof` lists every group a node sits in -- a maximal clique is not a
// partition, so a node can sit in more than one.
const gof={};
GR.forEach((g,gi)=>{g._i=gi;g.mi=g.member_node_idx;g.collapsed=false;
 g.mi.forEach(i=>{(gof[i]=gof[i]||[]).push(gi);});});
const PAL=["#e6553f","#4f9cf0","#58c26a","#e0b83e","#b57ee0","#3ec8c0",
 "#e07ab0","#98a832","#f08b3e","#7a8cf0","#50b08a","#c0625a",
 "#d0a05a","#6fb0e0","#9ad04a","#e05a8a","#5ad0b0","#a07ae0",
 "#e09a4a","#4ac0a0","#c05a9a","#8ab04a","#d05a5a","#5a90d0"];
const langs=[...new Set(N.map(n=>n.language))].sort();
const ops=[...new Set(N.map(n=>n.operator))].sort();
const levels=["1","2"];
const forms=[...new Set(N.filter(n=>n.kind==="contracted")
 .map(n=>n.form_pair))].sort();
const membins=["1","2-3","4-7","8+"];
const lcolor={};langs.forEach((l,i)=>lcolor[l]=PAL[i%PAL.length]);
const ocolor={};ops.forEach((o,i)=>ocolor[o]=PAL[i%PAL.length]);
const vcolor={"1":"#4f9cf0","2":"#e6553f"};
const fcolor={};forms.forEach((f,i)=>fcolor[f]=PAL[(i*7)%PAL.length]);
const mcolor={"1":"#4f9cf0","2-3":"#58c26a","4-7":"#e0b83e","8+":"#e6553f"};
function mbin(n){const m=n.n_members||1;
 return m<=1?"1":(m<=3?"2-3":(m<=7?"4-7":"8+"));}
const $=s=>document.getElementById(s);
const cv=$("cv"),ctx=cv.getContext("2d"),tip=$("tip"),thr=$("thr"),
 thrv=$("thrv"),mid=$("mid"),midv=$("midv"),stp=$("stp"),stpv=$("stpv"),
 exact=$("exact"),showint=$("showint"),hulls=$("hulls"),
 collapseall=$("collapseall"),cmode=$("cmode"),lmode=$("lmode"),
 cap=$("cap"),search=$("search"),stats=$("stats"),rule=$("rule"),
 sigwrap=$("sigwrap");
const NCON=N.filter(n=>n.kind==="contracted").length,
      NCEN=N.filter(n=>n.kind==="central").length;
// seed the layout: central nodes on a wide ring, each contracted node
// beside the first lang.op it carries -- the sub-tree starts where it
// belongs
const cpos={};let ci=0;
N.forEach(n=>{if(n.kind==="central"){
 const t=6.283*ci/NCEN;ci++;
 n.x=Math.cos(t)*1500;n.y=Math.sin(t)*1500;cpos[n.id]=[n.x,n.y];}});
let rk={};
N.forEach(n=>{if(n.kind==="contracted"){
 const c=cpos[n.operators[0]]||[0,0];
 const k=(rk[n.operators[0]]=(rk[n.operators[0]]||0)+1);
 const t=6.283*k/26;
 n.x=c[0]+Math.cos(t)*(90+4*k);n.y=c[1]+Math.sin(t)*(90+4*k);}});
N.forEach(n=>{n.vx=0;n.vy=0;});
let T=0.85,EX=false,MID=0.5,K=0,SI=true,HU=true,CM="lang",LM="all",
 CAP=20000,q="",act=[],actInt=[],hover=null,hoverE=null,hoverG=null,
 drag=null;
let ox=0,oy=0,scale=1,heat=1;
// the SIGMOID -- a DISPLAY rule.  w(g)=(s(g)-s(0))/(s(1)-s(0)),
// s(x)=1/(1+exp(-K(x-MID))).  K=0 gives w=g exactly (the raw graded
// score); large K gives a step at MID, the exact-match-style hard cut.
// No stored number is ever rewritten.
function sig(g){
 if(EX)return g;
 if(K<=1e-9)return g;
 const s=x=>1/(1+Math.exp(-K*(x-MID)));
 const a=s(0),b=s(1);
 if(b-a<1e-12)return g;
 return Math.max(0,Math.min(1,(s(g)-a)/(b-a)));}
function W(e){return sig(EX?e.weight_exact:e.weight_graded);}
function vok(n){return LM==="all"||n.kind==="central"||
 String(n.level)===LM;}
function color(n){
 if(CM==="op")return ocolor[n.operator];
 if(CM==="level")return n.kind==="central"?"#ffffff"
  :vcolor[String(n.level)];
 if(CM==="form")return n.kind==="central"?"#ffffff":fcolor[n.form_pair];
 if(CM==="members")return n.kind==="central"?"#ffffff":mcolor[mbin(n)];
 return lcolor[n.language];}
// ---- collapse: a collapsed group draws as ONE node at its members'
// centroid and its members' connectors are rerouted to it.  Members are
// never destroyed and never merged in the data -- this is a VIEW.
function collapsedHost(){
 // node index -> group index whose collapsed node hosts it.  When two
 // collapsed groups overlap the lower group index wins and the two are
 // joined, which is the honest reading of overlapping maximal cliques.
 const host={};
 GR.forEach((g,gi)=>{if(!g.collapsed)return;
  g.mi.forEach(i=>{if(host[i]===undefined)host[i]=gi;});});
 return host;}
let HOST={},GX={},GY={};
function recomputeCentroids(){
 GX={};GY={};
 GR.forEach((g,gi)=>{let x=0,y=0;g.mi.forEach(i=>{x+=N[i].x;y+=N[i].y;});
  GX[gi]=x/g.mi.length;GY[gi]=y/g.mi.length;});}
function endA(e){const h=HOST[e.ai];return h===undefined?null:h;}
function endB(e){const h=HOST[e.bi];return h===undefined?null:h;}
function ptA(e){const h=HOST[e.ai];
 return h===undefined?[N[e.ai].x,N[e.ai].y]:[GX[h],GY[h]];}
function ptB(e){const h=HOST[e.bi];
 return h===undefined?[N[e.bi].x,N[e.bi].y]:[GX[h],GY[h]];}
function refresh(){
 T=thr.value/100;thrv.textContent=T.toFixed(2);
 EX=exact.checked;MID=mid.value/100;K=stp.value/10;
 midv.textContent=MID.toFixed(2);stpv.textContent=K.toFixed(1);
 sigwrap.className=EX?"dim":"";
 SI=showint.checked;HU=hulls.checked;CM=cmode.value;LM=lmode.value;
 CAP=+cap.value;q=search.value.trim().toLowerCase();
 HOST=collapsedHost();recomputeCentroids();
 EXT.forEach(e=>{e._w=W(e);});
 // the threshold cuts EXTERNAL connectors ONLY; internal connectors are
 // structure and are never cut by it
 const pass=EXT.filter(e=>e._w>=T&&vok(N[e.ai])&&vok(N[e.bi]))
  .sort((p,r)=>(r._w-p._w)||(p._o-r._o));
 const capped=pass.length>CAP;
 act=capped?pass.slice(0,CAP):pass;
 actInt=SI?INT.filter(e=>vok(N[e.ai])):[];
 // components are counted on EXTERNAL connectors ONLY, whether or not
 // internal connectors are drawn.  In the COLLAPSED view a collapsed
 // group's members are one node, so they are unioned first.
 const p=N.map((_,i)=>i);
 const f=x=>{while(p[x]!=x){p[x]=p[p[x]];x=p[x];}return x;};
 GR.forEach(g=>{if(!g.collapsed)return;
  for(let k=1;k<g.mi.length;k++){const a=f(g.mi[0]),b=f(g.mi[k]);
   if(a!=b)p[a]=b;}});
 act.forEach(e=>{const a=f(e.ai),b=f(e.bi);if(a!=b)p[a]=b;});
 const roots=new Set(N.map((_,i)=>f(i)));
 const comps=roots.size;
 let multi=0;{const c={};N.forEach((_,i)=>{const r=f(i);c[r]=(c[r]||0)+1;});
  multi=Object.values(c).filter(v=>v>1).length;}
 const xl=act.filter(e=>e.cross_language).length;
 const ncol=GR.filter(g=>g.collapsed).length;
 const visNodes=N.length-Object.keys(HOST).length+
  new Set(Object.values(HOST)).size;
 stats.textContent=visNodes+" nodes drawn | "+NCON+" contracted ("+
  G.n_raw_rows+" rows) | "+NCEN+" central | "+GR.length+" groups ("+
  ncol+" collapsed) | "+act.length+" external ("+xl+" cross-language) | "+
  actInt.length+" internal | "+comps+" components ("+multi+" multi-node)";
 rule.textContent="RULE: two nodes are compared on the INTERSECTION of "+
  "their INPUT KEYS (level 1 keyed by (x0,x1), level 2 by "+
  "(x0,x1,x2,x3)); level 1 is never mixed with level 2. Declines are "+
  "never scored and zero comparable keys means NO connector. CONTRACTED "+
  "nodes are an IDENTITY set (same key set, byte-identical outputs). "+
  "GROUPS are MAXIMAL CLIQUES of mutual exact-1.0 over partial overlaps "+
  "-- a container, not a merge; click a hull to collapse it, click the "+
  "collapsed node to expand. Cut and weight use "+
  (EX?"the EXACT-MATCH RATE over the comparable keys. The sigmoid is "+
      "inactive."
    :("the GRADED element similarity (ruling A) averaged over the "+
      "comparable keys, mapped through the sigmoid midpoint "+
      MID.toFixed(2)+" steepness "+K.toFixed(1)+
      (K<=0?" -- steepness 0 IS the raw graded score":
       " -- raise steepness to approach the exact-match style hard cut")))+
  " The threshold cuts EXTERNAL connectors only; internal springs are "+
  "near zero ("+G.int_spring+" against "+G.ext_spring+
  " external, group cohesion "+G.grp_spring+"); COMPONENTS ARE COUNTED "+
  "ON EXTERNAL CONNECTORS ONLY. "+(capped
   ?("DRAW CAP IN FORCE: "+pass.length+" clear "+T.toFixed(2)+
     ", the top "+CAP+" BY WEIGHT are drawn, "+(pass.length-CAP)+
     " are not.")
   :("all "+pass.length+" external connectors clearing "+T.toFixed(2)+
     " are drawn (cap "+(CAP>=1e6?"off":CAP)+")."));
 heat=Math.max(heat,0.25);}
[thr,mid,stp].forEach(e=>e.oninput=refresh);
[exact,showint,hulls,cmode,lmode,cap].forEach(e=>e.onchange=refresh);
collapseall.onchange=()=>{GR.forEach(g=>g.collapsed=collapseall.checked);
 refresh();};
$("expandall").onclick=()=>{GR.forEach(g=>g.collapsed=false);
 collapseall.checked=false;refresh();};
search.oninput=refresh;
refresh();
function size(){cv.width=innerWidth;cv.height=innerHeight-cv.offsetTop;}
addEventListener("resize",size);size();
// ---- physics unchanged from v2/v3: clamped linear springs, velocity
// clamp, gravity, hard boundary, grid repulsion, near-zero internal
// spring.  The one addition is the GROUP COHESION spring, which is not a
// connector, carries no weight and is never cut.
const CELL=170,INT_K=G.int_spring,EXT_K=G.ext_spring,GRP_K=G.grp_spring;
function step(){
 if(heat>0.01){
  const grid=new Map();
  for(let i=0;i<N.length;i++){
   const n=N[i];
   const k=((n.x/CELL)|0)+","+((n.y/CELL)|0);
   let b=grid.get(k);if(!b){b=[];grid.set(k,b);}b.push(i);}
  for(const [k,b] of grid){
   const p=k.split(","),gx=+p[0],gy=+p[1];
   for(let dx=0;dx<=1;dx++)for(let dy=(dx?-1:0);dy<=1;dy++){
    const o=grid.get((gx+dx)+","+(gy+dy));if(!o)continue;
    const same=(dx===0&&dy===0);
    for(let x=0;x<b.length;x++)for(let y=same?x+1:0;y<o.length;y++){
     const a=N[b[x]],c=N[o[y]];if(a===c)continue;
     let ddx=a.x-c.x,ddy=a.y-c.y;let d2=ddx*ddx+ddy*ddy;
     if(d2<1)d2=1; if(d2>90000)continue;
     const d=Math.sqrt(d2),f=Math.min(2600/d2,5);
     a.vx+=ddx/d*f;a.vy+=ddy/d*f;c.vx-=ddx/d*f;c.vy-=ddy/d*f;}}}
  // near-zero internal spring -- a visual tether, not a force that
  // decides the layout
  actInt.forEach(e=>{const a=N[e.ai],b=N[e.bi];
   let dx=b.x-a.x,dy=b.y-a.y,d=Math.sqrt(dx*dx+dy*dy);if(d<1)d=1;
   const f=Math.min((d-70)*INT_K,6);
   a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f;});
  // GROUP COHESION -- so a group's members stay close enough to draw a
  // hull around.  Not a connector; never cut by the threshold.
  GR.forEach((g,gi)=>{const cx=GX[gi],cy=GY[gi];
   g.mi.forEach(i=>{const n=N[i];
    let dx=cx-n.x,dy=cy-n.y,d=Math.sqrt(dx*dx+dy*dy);if(d<1)d=1;
    const f=Math.min((d-30)*GRP_K,4);
    n.vx+=dx/d*f;n.vy+=dy/d*f;});});
  // EXTERNAL connectors carry the layout
  act.forEach(e=>{const a=N[e.ai],b=N[e.bi];
   let dx=b.x-a.x,dy=b.y-a.y,d=Math.sqrt(dx*dx+dy*dy);if(d<1)d=1;
   const f=Math.min((d-140)*EXT_K*e._w,6);
   a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f;});
  N.forEach(n=>{
   n.vx-=n.x*0.004;n.vy-=n.y*0.004;        // gravity to centre
   const v=Math.hypot(n.vx,n.vy);
   if(v>30){n.vx*=30/v;n.vy*=30/v;}        // velocity clamp
   n.x+=n.vx*0.25*heat;n.y+=n.vy*0.25*heat;n.vx*=0.75;n.vy*=0.75;
   const r=Math.hypot(n.x,n.y);
   if(r>2900){n.x*=2900/r;n.y*=2900/r;}}); // hard boundary
  heat*=0.992;
  recomputeCentroids();}
 draw();requestAnimationFrame(step);}
function fit(){
 let mnx=1e9,mny=1e9,mxx=-1e9,mxy=-1e9;
 N.forEach(n=>{mnx=Math.min(mnx,n.x);mxx=Math.max(mxx,n.x);
  mny=Math.min(mny,n.y);mxy=Math.max(mxy,n.y);});
 const w2=Math.max(mxx-mnx,10),h2=Math.max(mxy-mny,10);
 scale=Math.min((cv.width-80)/w2,(cv.height-80)/h2,3);
 ox=-(mnx+mxx)/2;oy=-(mny+mxy)/2;}
// AUTOFIT RUNS ONCE THEN NEVER AGAIN.  Any wheel or mousedown disables it
// permanently.  The "fit view" button is the only way back.
let userMoved=false,fitted=false;
function autofit(){if(userMoved||fitted)return;if(heat<0.35){fit();
 fitted=true;}}
const _af=setInterval(()=>{autofit();if(fitted||userMoved)
 clearInterval(_af);},800);
addEventListener("wheel",()=>{userMoved=true;},{passive:true});
addEventListener("mousedown",()=>{userMoved=true;});
$("fitbtn").onclick=()=>{fit();};
function sx(x){return cv.width/2+(x+ox)*scale;}
function sy(y){return cv.height/2+(y+oy)*scale;}
function hit(n){return q&&((n.id.toLowerCase().includes(q))||
 (n.label&&n.label.toLowerCase().includes(q))||
 (n.operators&&n.operators.join(" ").toLowerCase().includes(q))||
 (n.members&&n.members.join(" ").toLowerCase().includes(q)));}
// ---- convex hull (monotone chain) + rounded polygon, so a group draws
// as an ENCLOSING CONTAINER around its members rather than a point
function hullOf(pts){
 if(pts.length<3)return pts;
 const p=pts.slice().sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
 const cr=(o,a,b)=>(a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0]);
 const lo=[];for(const q of p){
  while(lo.length>=2&&cr(lo[lo.length-2],lo[lo.length-1],q)<=0)lo.pop();
  lo.push(q);}
 const up=[];for(let i=p.length-1;i>=0;i--){const q=p[i];
  while(up.length>=2&&cr(up[up.length-2],up[up.length-1],q)<=0)up.pop();
  up.push(q);}
 lo.pop();up.pop();return lo.concat(up);}
// the hull is taken over each member's own PAD RING rather than over the
// member points, so every member is inside its group's container by at
// least `pad` -- a radial push from the centroid does not guarantee that
// on a long thin group and this does.
function padPts(pts,pad){
 const out=[];
 for(const p of pts)for(let a=0;a<8;a++){const t=a*0.7854;
  out.push([p[0]+Math.cos(t)*pad,p[1]+Math.sin(t)*pad]);}
 return out;}
function roundedPath(h,r){
 ctx.beginPath();
 const n=h.length;
 if(n<3){const p=h[0]||[0,0];
  ctx.arc(p[0],p[1],r+6,0,6.283);return;}
 for(let i=0;i<n;i++){
  const a=h[i],b=h[(i+1)%n],c=h[(i+2)%n];
  const m1=[(a[0]+b[0])/2,(a[1]+b[1])/2],
        m2=[(b[0]+c[0])/2,(b[1]+c[1])/2];
  if(i===0)ctx.moveTo(m1[0],m1[1]);
  ctx.quadraticCurveTo(b[0],b[1],m2[0],m2[1]);}
 ctx.closePath();}
function groupScreenPts(g){
 return g.mi.map(i=>[sx(N[i].x),sy(N[i].y)]);}
function pointInPoly(pt,poly){
 let c=false;
 for(let i=0,j=poly.length-1;i<poly.length;j=i++){
  const a=poly[i],b=poly[j];
  if(((a[1]>pt[1])!=(b[1]>pt[1]))&&
     (pt[0]<(b[0]-a[0])*(pt[1]-a[1])/(b[1]-a[1])+a[0]))c=!c;}
 return c;}
let hullCache=[];
function draw(){ctx.clearRect(0,0,cv.width,cv.height);
 ctx.lineWidth=1;
 // ---- group hulls first, underneath everything
 hullCache=[];
 if(HU){GR.forEach((g,gi)=>{
  if(LM!=="all"&&String(g.level)!==LM)return;
  if(g.collapsed){
   const p=[sx(GX[gi]),sy(GY[gi])];
   hullCache.push({gi:gi,poly:[[p[0]-16,p[1]-16],[p[0]+16,p[1]-16],
    [p[0]+16,p[1]+16],[p[0]-16,p[1]+16]],collapsed:true});
   return;}
  const pts=groupScreenPts(g);
  const h=hullOf(padPts(pts,16));
  hullCache.push({gi:gi,poly:h,collapsed:false});
  const on=(hoverG===gi);
  ctx.fillStyle=on?"rgba(88,194,106,0.16)":"rgba(88,194,106,0.07)";
  ctx.strokeStyle=on?"rgba(120,220,140,0.95)":"rgba(88,194,106,0.42)";
  ctx.lineWidth=on?2:1;
  roundedPath(h,16);ctx.fill();ctx.stroke();ctx.lineWidth=1;});}
 if(actInt.length){ctx.setLineDash([3,3]);
  actInt.forEach(e=>{const w=EX?e.weight_exact:e.weight_graded;
   const al=0.16;
   const A=ptA(e),B=ptB(e);
   ctx.strokeStyle=e===hoverE?"#fff":"rgba(224,184,62,"+al+")";
   ctx.beginPath();ctx.moveTo(sx(A[0]),sy(A[1]));
   ctx.lineTo(sx(B[0]),sy(B[1]));ctx.stroke();});
  ctx.setLineDash([]);}
 act.forEach(e=>{const A=ptA(e),B=ptB(e);
  ctx.strokeStyle=e===hoverE?"#fff":
  "rgba(120,170,220,"+(0.07+0.45*(e._w-T)/(1.001-T))+")";
  ctx.beginPath();ctx.moveTo(sx(A[0]),sy(A[1]));
  ctx.lineTo(sx(B[0]),sy(B[1]));ctx.stroke();});
 // ---- nodes; a member of a COLLAPSED group is not drawn on its own
 N.forEach((n,i)=>{if(!vok(n))return;if(HOST[i]!==undefined)return;
  const h=hit(n),cen=n.kind==="central";
  const mm=n.n_members||1;
  const r=cen?(h?13:11):(h?7:(n===hover?6:(mm>1?3+Math.min(5,
   Math.log2(mm)):3)));
  ctx.beginPath();ctx.arc(sx(n.x),sy(n.y),r,0,6.283);
  ctx.fillStyle=color(n);ctx.globalAlpha=q&&!h?0.13:1;
  ctx.fill();
  if(cen){ctx.strokeStyle="#fff";ctx.lineWidth=2;ctx.stroke();
   ctx.lineWidth=1;}
  else if(mm>1){ctx.strokeStyle="#cfd6e0";ctx.lineWidth=1;ctx.stroke();}
  ctx.globalAlpha=1;});
 // ---- collapsed groups draw as ONE node at the centroid
 GR.forEach((g,gi)=>{if(!g.collapsed)return;
  if(LM!=="all"&&String(g.level)!==LM)return;
  const X=sx(GX[gi]),Y=sy(GY[gi]);
  ctx.beginPath();ctx.arc(X,Y,11,0,6.283);
  ctx.fillStyle="#58c26a";ctx.fill();
  ctx.strokeStyle=hoverG===gi?"#fff":"#cfe8d4";ctx.lineWidth=2;
  ctx.stroke();ctx.lineWidth=1;
  ctx.fillStyle="#0d1410";ctx.font="10px sans-serif";
  ctx.textAlign="center";ctx.fillText(String(g.size),X,Y+3);
  ctx.textAlign="left";});
 ctx.font="12px sans-serif";
 N.forEach(n=>{if(n.kind!=="central")return;
  ctx.fillStyle="#fff";ctx.fillText(n.id,sx(n.x)+13,sy(n.y)+4);});
 if(scale>1.1||q){ctx.font="10px sans-serif";ctx.fillStyle="#9aa2ad";
  N.forEach((n,i)=>{if(n.kind!=="contracted"||!vok(n))return;
   if(HOST[i]!==undefined)return;
   if(q&&!hit(n))return;
   ctx.fillText(n.label,sx(n.x)+5,sy(n.y)+3);});}
 if(HU){ctx.font="10px sans-serif";ctx.fillStyle="#8fd8a0";
  hullCache.forEach(hc=>{const g=GR[hc.gi];
   let mx=1e9,my=1e9;hc.poly.forEach(p=>{if(p[1]<my){my=p[1];mx=p[0];}});
   ctx.fillText(g.id+" ("+g.size+", min overlap "+g.min_overlap+")",
    mx+6,my-4);});}
 if(hover&&hover.kind==="contracted"){ctx.font="11px sans-serif";
  ctx.fillStyle="#fff";ctx.fillText(hover.label,sx(hover.x)+7,
   sy(hover.y)-6);}
 let lx=10,ly=cv.height-12;ctx.font="11px sans-serif";
 const keys=CM==="op"?ops:(CM==="level"?levels:(CM==="form"?forms
        :(CM==="members"?membins:langs))),
       tab=CM==="op"?ocolor:(CM==="level"?vcolor:(CM==="form"?fcolor
        :(CM==="members"?mcolor:lcolor)));
 keys.forEach(l=>{ctx.fillStyle=tab[l];ctx.fillRect(lx,ly-8,8,8);
  ctx.fillStyle="#9aa2ad";
  const t=CM==="level"?("level "+l):(CM==="members"?(l+" rows"):l);
  ctx.fillText(t,lx+11,ly);
  lx+=20+ctx.measureText(t).width;});
 ctx.fillStyle="#7d8590";
 ctx.fillText("solid = external (carries the layout)   dashed = internal"+
  " (near-zero spring, a visual tether only)   green hull = GROUP, a "+
  "container of nodes that are mutually exact-1.0 on their overlaps "+
  "(click to collapse / expand)",10,ly-18);
 ctx.font="13px sans-serif";}
function pick(mx,my){hover=null;hoverE=null;hoverG=null;
 for(let i=0;i<N.length;i++){const n=N[i];if(!vok(n))continue;
  if(HOST[i]!==undefined)continue;
  const dx=sx(n.x)-mx,dy=sy(n.y)-my;
  const rr=n.kind==="central"?200:60;
  if(dx*dx+dy*dy<rr){hover=n;return;}}
 for(const hc of hullCache){if(!hc.collapsed)continue;
  const g=GR[hc.gi];const dx=sx(GX[hc.gi])-mx,dy=sy(GY[hc.gi])-my;
  if(dx*dx+dy*dy<200){hoverG=hc.gi;return;}}
 let best=25;
 const scan=act.concat(actInt);
 for(const e of scan){const A=ptA(e),B=ptB(e);
  const x1=sx(A[0]),y1=sy(A[1]),x2=sx(B[0]),y2=sy(B[1]);
  const L2=(x2-x1)**2+(y2-y1)**2;if(!L2)continue;
  let t=((mx-x1)*(x2-x1)+(my-y1)*(y2-y1))/L2;t=Math.max(0,Math.min(1,t));
  const dx=mx-(x1+t*(x2-x1)),dy=my-(y1+t*(y2-y1)),d2=dx*dx+dy*dy;
  if(d2<best){best=d2;hoverE=e;}}
 if(hoverE)return;
 for(const hc of hullCache){
  if(pointInPoly([mx,my],hc.poly)){hoverG=hc.gi;return;}}}
function mxy(ev){const r=cv.getBoundingClientRect();
 return[ev.clientX-r.left,ev.clientY-r.top];}
function f4(x){return x==null?"&mdash;":(+x).toFixed(4);}
function esc(s){return String(s).replace(/&/g,"&amp;")
 .replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function nodeTip(n){
 if(n.kind==="central")
  return "<b>"+esc(n.id)+"</b><br>CENTRAL node &middot; language "+
   esc(n.language)+" &middot; operator "+esc(n.operator)+
   "<br>raw rows on this operator: "+n.n_rows+
   "<br>contracted nodes carrying it: "+n.n_contracted;
 const i=idx[n.id];
 const gs=(gof[i]||[]).map(gi=>GR[gi].id+" (size "+GR[gi].size+
  ", min overlap "+GR[gi].min_overlap+")");
 const mem=n.members.slice(0,24).map(esc).join("<br>&nbsp;&nbsp;");
 return "<b>"+esc(n.id)+"</b> &middot; CONTRACTED node &middot; "+
  "<b>"+n.n_members+" member row"+(n.n_members==1?"":"s")+"</b>"+
  "<br>level <b>"+n.level+"</b> &middot; form "+esc(n.form_pair)+
  " &middot; languages "+esc(n.languages.join(", "))+
  "<br>operators "+esc(n.operators.join(", "))+
  "<br>holder pairs "+esc(n.holder_pairs.join(" ; "))+
  "<br>x_set_a "+esc(n.x_set_a)+"<br>x_set_b "+esc(n.x_set_b)+
  "<br>input keys "+n.n_input_keys+" &middot; keys carrying a value "+
  n.n_valid_keys+" &middot; declines "+n.n_declines+
  (gs.length?("<br>in group"+(gs.length==1?"":"s")+": "+esc(gs.join(", "))
   +" &mdash; a group is a CONTAINER, not a merge"):"")+
  "<br><i>member rows (identity: same key set, byte-identical outputs)"+
  "</i><br>&nbsp;&nbsp;"+mem+
  (n.members.length>24?("<br>&nbsp;&nbsp;&hellip; and "+
   (n.members.length-24)+" more"):"");}
function groupTip(gi){const g=GR[gi];
 const po=g.pair_overlaps.slice(0,10).map(p=>esc(p.a)+"~"+esc(p.b)+
  " on "+p.n_comparable).join("; ");
 return "<b>"+esc(g.id)+"</b> &middot; GROUP (case 2) &middot; "+
  g.size+" contracted nodes, "+g.n_rows+" raw rows &middot; level "+
  g.level+
  "<br>a MAXIMAL CLIQUE: every pair inside is mutually exact-1.0 with "+
  "n_comparable &ge; 1. Complete linkage, never a connected component."+
  "<br><b>minimum overlap "+g.min_overlap+" keys</b> (the weakest "+
  "evidence in the group) &middot; maximum "+g.max_overlap+
  "<br>languages "+esc(g.languages.join(", "))+
  "<br>operators "+esc(g.operators.join(", "))+
  "<br>members "+esc(g.members.join(", "))+
  "<br>pair overlaps: "+po+
  (g.pair_overlaps.length>10?(" &hellip; and "+
   (g.pair_overlaps.length-10)+" more"):"")+
  "<br><i>click to "+(g.collapsed?"expand":"collapse")+"</i>";}
function edgeTip(e){
 if(e.kind==="internal")
  return "<b>INTERNAL connector</b><br>"+esc(e.a)+"<br>&rarr; "+
   esc(e.b)+"<br>exact-match "+f4(e.weight_exact)+
   " &middot; graded "+f4(e.weight_graded)+
   (e.no_comparison?" (no co-node of that lang.op shares a comparable "+
    "input key &mdash; 1.0 by convention)":(" &middot; over "+
     e.n_co_nodes_comparable+" co-node"+
     (e.n_co_nodes_comparable==1?"":"s")))+
   "<br>structure, not similarity: never cut by the threshold, and its "+
   "spring is near zero so it does not decide the layout";
 return "<b>EXTERNAL connector</b><br>"+esc(e.a)+"<br>&harr; "+
  esc(e.b)+"<br><b>exact-match "+f4(e.weight_exact)+"</b> ("+
  e.n_matched_exact+"/"+e.n_comparable+" comparable keys byte-identical)"+
  "<br><b>graded "+f4(e.weight_graded)+"</b> (ruling A per-element "+
  "similarity, mean over the comparable keys)"+
  "<br>active weight after the sigmoid: <b>"+f4(e._w)+"</b>"+
  "<br><b>level "+e.level+"</b> &middot; <b>n_comparable "+
  e.n_comparable+"</b> &middot; n_shared_keys "+e.n_shared_keys+
  " &middot; n_excluded_declines "+e.n_excluded_declines+
  " &middot; n_matched_exact "+e.n_matched_exact+
  "<br>"+(e.cross_language?"CROSS-language":"same-language")+
  " &middot; "+(e.same_key_set?"identical input key sets"
   :"PARTIAL overlap of the two input key sets")+
  "<br>aligned on the INTERSECTION of the two input key sets; level 1 is "+
  "never mixed with level 2";}
cv.onmousemove=ev=>{const[mx,my]=mxy(ev);
 if(drag){if(drag.node){drag.node.x=(mx-cv.width/2)/scale-ox;
   drag.node.y=(my-cv.height/2)/scale-oy;heat=Math.max(heat,0.3);}
  else{ox+=(mx-drag.px)/scale;oy+=(my-drag.py)/scale;
   drag.px=mx;drag.py=my;}return;}
 pick(mx,my);
 if(hover){tip.style.display="block";tip.innerHTML=nodeTip(hover);}
 else if(hoverE){tip.style.display="block";tip.innerHTML=edgeTip(hoverE);}
 else if(hoverG!==null){tip.style.display="block";
  tip.innerHTML=groupTip(hoverG);}
 else tip.style.display="none";
 tip.style.left=(ev.clientX+14)+"px";tip.style.top=(ev.clientY+14)+"px";};
cv.onmousedown=ev=>{const[mx,my]=mxy(ev);pick(mx,my);
 drag=hover?{node:hover}:{px:mx,py:my,sx:mx,sy:my};};
cv.onclick=ev=>{const[mx,my]=mxy(ev);pick(mx,my);
 if(hover||hoverE)return;
 if(hoverG!==null){GR[hoverG].collapsed=!GR[hoverG].collapsed;
  refresh();}};
addEventListener("mouseup",()=>drag=null);
cv.onwheel=ev=>{ev.preventDefault();
 scale*=ev.deltaY<0?1.1:0.9;scale=Math.max(0.05,Math.min(8,scale));};
step();
</script></body></html>
"""


if __name__ == "__main__":
    main()
