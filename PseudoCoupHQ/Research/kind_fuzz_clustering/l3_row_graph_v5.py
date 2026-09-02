#!/usr/bin/env python3
"""l3_row_graph_v5.py -- the row graph over FULL GRIDS with the owner's
rulings of 2026-08-21 (log 054), and the DOMINANCE reading.

`l3_row_graph_v4.py`, `row_graph_v4.json`, `row_graph_explorer_v4.html`
and `verify_row_graph_v4.js` are left on disk unchanged, and so is
`matrices_cart/`.  This is a v5, not an edit: the comparability rule
changed (full grids + the compatibility gate), so the old products stay
readable for the audit.

SOURCE: `matrices_full/` -- every profile inflated to the FULL X set of
its form and level; a cell whose key involves an operand the holder
cannot represent carries the static token UNREPRESENTABLE (not a
decline: the language was never asked).  Built by `l3_cart_full.py` by
assembly over `matrices_cart/`; NO probe was run.

------------------------------------------------------------------
RULING 1 -- PROFILE COMPATIBILITY IS A HARD GATE
------------------------------------------------------------------
Two profiles connect ONLY if they were intended to process the same
inputs: same form pair, same level, same intended X set.  With full
grids the intended X set of a profile IS the form-level full set, so
the gate is (form_pair, level) -- and inside the gate every profile
carries the SAME key set, always.  A truth profile and a whole profile
are NEVER compatible, whatever cells they coincidentally share.  the owner,
verbatim: "the key-to-key/cell-to-cell attraction is never without the
context of the profile-to-profile attraction.  if the profiles arent
compatible, there is no attraction."  NO key-to-key clustering, ever.

GROUP RETIRES.  Full grids make a partial overlap impossible inside the
gate -- every compatible pair shares the identical key set -- so the
partial-overlap case has no instance and the group machinery is gone.
CONTRACT keeps its meaning: identical outputs at EVERY key over the
identical key set, plain identity, transitive, no clique test.

------------------------------------------------------------------
RULING 2 -- TWO SCORINGS RIDE ON EVERY CONNECTOR.  Neither is THE
weight; that ruling awaits the owner.
------------------------------------------------------------------
  (a) weight_value  agreement over VALUE cells only: a cell where
                    either side is UNREPRESENTABLE, REFUSE, RAISE:* or
                    ABORT leaves the numerator AND the denominator
                    (declines excluded as today; UNREPRESENTABLE
                    excluded the same way).  Zero value-comparable
                    cells -> weight_value is null, recorded, never a
                    zero.
  (b) weight_all    agreement over ALL cells of the full grid, with
                    UNREPRESENTABLE / REFUSE / RAISE:<kind> / ABORT
                    treated as ANSWERS: byte-identical token = agree.
                    The denominator is the full grid size, always
                    defined.  This is where representability and
                    overflow differences live.

------------------------------------------------------------------
RULING 3 -- DOMINANCE, the directed reading
------------------------------------------------------------------
Over COMPATIBLE profile pairs only: A DOMINATES B when at every key
where B answers a VALUE, A answers the IDENTICAL value (A may answer at
more keys).  Each pair reads as:

    contradicts   a key exists where both answer values and they differ
    equal_values  no contradiction, A dominates B AND B dominates A
                  (identical value-cell sets -- mutual nesting)
    nests         no contradiction, exactly one side dominates
    overlaps      no contradiction, neither side dominates (each
                  answers values at keys the other does not; pairs
                  whose shared value-cell count is ZERO are counted
                  separately inside this bucket as
                  disjoint_value_sets)

Emitted as `dominance_v5.json` with the full directed relation, the
strict-nest transitive reduction per gate block, and
`dominance_explorer_v5.html` as the lattice view.  The layer-3-era
`dominance_lattice.json` is precedent for the idea only; none of its
data is inherited.

EXPLORER -- the fixed requirements, preserved exactly:
  - autofit runs ONCE then never again; any wheel or mousedown disables
    it permanently; a "fit view" button exists;
  - internal connector springs near zero (0.0008 against 0.0060
    external);
  - the threshold slider cuts EXTERNAL connectors only;
  - components are counted on EXTERNAL connectors only;
  - single self-contained file, data embedded, no CDN;
  - NEW: a toggle between the two scorings.  Neither is preselected as
    THE weight; the start position is scoring (a) purely because it is
    the continuation of the current display, a display default and
    nothing else.

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree; the
OS-stopped outcome is ABORT.
"""

import csv
import itertools
import json
import os
import sys
import time
from collections import defaultdict

import numpy as np

csv.field_size_limit(sys.maxsize)

HERE = os.path.dirname(os.path.abspath(__file__))
FULL = os.path.join(HERE, "matrices_full")
SEP = ";"
UNREP = "UNREPRESENTABLE"
LANGS = ("rust", "ruby")

RENDER_CAP = 20000
INT_SPRING = 0.0008
EXT_SPRING = 0.0060
CHUNK_ELEMS = 3_000_000


def is_decline(c):
    return c == "REFUSE" or c == "ABORT" or c.startswith("RAISE:")


# ------------------------------------------------------------------
class Alphabet(object):
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
        self.unrep = np.zeros(n, dtype=bool)
        self.decl = np.zeros(n, dtype=bool)
        for i, s in enumerate(self.text):
            if s == UNREP:
                self.unrep[i] = True
            elif is_decline(s):
                self.decl[i] = True
        self.value = ~(self.unrep | self.decl)


AB = Alphabet()


def load_rows():
    idx = json.load(open(os.path.join(FULL, "index.json")))
    rows = []
    for key in sorted(idx["matrices"]):
        meta = idx["matrices"][key]
        if meta["language"] not in LANGS:
            continue
        p = os.path.join(FULL, meta["file"])
        for r in csv.DictReader(open(p)):
            n = int(r["n_probes"])
            cells = r["output_canon_vector"].split(SEP)
            assert len(cells) == n, (key, r["probe_id"])
            codes = np.fromiter((AB(c) for c in cells), dtype=np.int32,
                                count=n)
            rows.append(dict(
                key="%s.%s" % (meta["language"], meta["operator"]),
                language=meta["language"], operator=meta["operator"],
                level=int(r["level"]), probe_id=r["probe_id"],
                lhs_holder=r["lhs_holder"], rhs_holder=r["rhs_holder"],
                form_pair=r["form_pair"],
                x_set_a=r["x_set_a"], x_set_b=r["x_set_b"],
                src_x_set_a=r["src_x_set_a"],
                src_x_set_b=r["src_x_set_b"],
                n_probes=n, codes=codes,
                n_values=int(r["n_values"]),
                n_declines=int(r["n_declines"]),
                n_unrepresentable=int(r["n_unrepresentable"])))
    return rows, idx


def row_id(r):
    return "%s / L%d / %s / %s %s %s" % (
        r["key"], r["level"], r["probe_id"], r["lhs_holder"],
        r["operator"], r["rhs_holder"])


def contract(rows):
    """identity over the full grid: same (level, form_pair) -- hence the
    same key set by construction -- and byte-identical outputs at every
    key, UNREPRESENTABLE and outcome tokens included."""
    buckets = defaultdict(list)
    for i, r in enumerate(rows):
        buckets[(r["level"], r["form_pair"],
                 r["codes"].tobytes())].append(i)
    nodes = []
    for kk in sorted(buckets, key=lambda k: (k[0], k[1], buckets[k][0])):
        mem = buckets[kk]
        r0 = rows[mem[0]]
        nodes.append(dict(
            members=mem, level=r0["level"], form_pair=r0["form_pair"],
            codes=r0["codes"], n_probes=r0["n_probes"]))
    nodes.sort(key=lambda n: (n["level"], n["form_pair"], n["members"][0]))
    return nodes


def dist(vals):
    if not vals:
        return None
    v = sorted(vals)
    n = len(v)

    def q(p):
        return v[min(n - 1, int(p * n))]
    return dict(n=n, min=v[0], p25=q(0.25), median=q(0.50), p75=q(0.75),
                p90=q(0.90), max=v[-1],
                mean=round(sum(v) / float(n), 3))


def components(n, pairs):
    """`root` is the super-node of a merged set."""
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


# ------------------------------------------------------------------
def score_block(C, V, U):
    """all pairwise sums inside one gate block.
    C (n,K) int32 codes; V value mask; U unrepresentable mask.
    Returns dict of (n,n) int arrays:
      neq  cells byte-identical (scoring b numerator)
      nvv  cells where BOTH sides answer a value
      nmv  of those, byte-identical (scoring a numerator)
      nue  cells where EITHER side is UNREPRESENTABLE
      vab  cells where the COLUMN side answers a value and the ROW side
           differs -- row dominates column iff vab == 0
    """
    n, K = C.shape
    out = {k: np.zeros((n, n), dtype=np.int64)
           for k in ("neq", "nvv", "nmv", "nue", "vab")}
    fV = V.astype(np.float64)
    out["nvv"] = (fV @ fV.T).astype(np.int64)
    fU = U.astype(np.float64)
    # |either unrep| = nU_i + nU_j - both
    both_u = (fU @ fU.T)
    nu = U.sum(axis=1).astype(np.float64)
    out["nue"] = (nu[:, None] + nu[None, :] - both_u).astype(np.int64)
    step = max(1, int(CHUNK_ELEMS // max(1, n * K)))
    for lo in range(0, n, step):
        hi = min(n, lo + step)
        a = C[lo:hi][:, None, :]
        b = C[None, :, :]
        eq = (a == b)
        out["neq"][lo:hi] = eq.sum(axis=2, dtype=np.int64)
        vv = V[lo:hi][:, None, :] & V[None, :, :]
        out["nmv"][lo:hi] = (eq & vv).sum(axis=2, dtype=np.int64)
        # column j answers a value, row i differs
        out["vab"][lo:hi] = ((~eq) & V[None, :, :]).sum(axis=2,
                                                        dtype=np.int64)
        del a, b, eq, vv
    return out


def transitive_reduction(nodes, edges):
    """edges: set of (a,b), a dominates b, strict, transitive, acyclic.
    Returns the reduced edge set for the lattice drawing."""
    dominated_by = defaultdict(set)          # b -> set of a above it
    dominates = defaultdict(set)
    for a, b in edges:
        dominates[a].add(b)
        dominated_by[b].add(a)
    keep = set()
    for a, b in edges:
        # (a,b) is redundant if some c has a -> c -> b
        if not any(c in dominates[a] for c in dominated_by[b]
                   if c != a and c != b):
            keep.add((a, b))
    return keep


# ==================================================================
def main():
    print("ROW GRAPH v5 -- FULL GRIDS, the COMPATIBILITY GATE, two "
          "scorings, and DOMINANCE.  ASSEMBLY ONLY, no probes were run.")
    print("  gate: two profiles connect only if same form pair, same "
          "level, same intended X set -- with full grids that is "
          "(form_pair, level), and inside the gate every profile "
          "carries the SAME key set.  A truth profile and a whole "
          "profile are NEVER compatible.  No key-to-key clustering, "
          "ever.  GROUP retires; CONTRACT keeps its meaning.")
    t0 = time.time()

    rows, full_index = load_rows()
    AB.finalise()
    for r in rows:
        r["id"] = row_id(r)
    ids = [r["id"] for r in rows]
    assert len(set(ids)) == len(ids)
    langop_keys = sorted({r["key"] for r in rows})
    grid_of = {}
    for r in rows:
        k = (r["form_pair"], r["level"])
        assert grid_of.setdefault(k, r["n_probes"]) == r["n_probes"], (
            "full grids must agree inside a gate block")
    print("  %d raw rows (profiles), %d lang.op, %d distinct canon "
          "strings, %d gate blocks (form_pair x level), %d cells in all"
          "  (%.1f s)"
          % (len(rows), len(langop_keys), len(AB.text), len(grid_of),
             sum(r["n_probes"] for r in rows), time.time() - t0))

    # ------------------------------------------------------ CONTRACT
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
        node["probe_ids"] = sorted({r["probe_id"] for r in mem})
        node["label"] = "%s %s %s [L%d]%s" % (
            r0["lhs_holder"], r0["operator"], r0["rhs_holder"],
            r0["level"], "" if len(mem) == 1 else " x%d" % len(mem))
        node["value_mask"] = AB.value[node["codes"]]
        node["unrep_mask"] = AB.unrep[node["codes"]]
        node["n_value_cells"] = int(node["value_mask"].sum())
        node["n_unrepresentable"] = int(node["unrep_mask"].sum())
        node["n_declines"] = int(node["n_probes"]
                                 - node["n_value_cells"]
                                 - node["n_unrepresentable"])
    csz = sorted((n["n_members"] for n in cn), reverse=True)
    print("  CONTRACT (identity over the full grid, UNREPRESENTABLE and "
          "outcome tokens included): %d raw rows -> %d contracted nodes; "
          "%d carry more than one row; largest %d  (%.1f s)"
          % (len(rows), len(cn),
             sum(1 for n in cn if n["n_members"] > 1), csz[0],
             time.time() - t0))

    # v4 contract count, recomputed here for the before/after: v4
    # bucketed by (level, x_set_a, x_set_b, measured vector).  The
    # measured vector is the full vector with the UNREPRESENTABLE cells
    # removed, and (src_x_set_a, src_x_set_b) are the measured sets.
    v4b = defaultdict(list)
    for i, r in enumerate(rows):
        keep = ~AB.unrep[r["codes"]]
        v4b[(r["level"], r["src_x_set_a"], r["src_x_set_b"],
             r["codes"][keep].tobytes())].append(i)
    print("  before/after on the SAME rows: v4-rule contraction (same "
          "measured key set + identical measured outputs) gives %d "
          "nodes; the full-grid rule gives %d.  The difference is "
          "pairs whose measured vectors matched over DIFFERENT key "
          "sets -- exactly the coincidence the gate retires."
          % (len(v4b), len(cn)))

    # ------------------------------------------------ gate blocks
    blocks = defaultdict(list)
    for n in cn:
        blocks[(n["form_pair"], n["level"])].append(n["idx"])
    print("  gate blocks: %s"
          % "; ".join("%s L%d: %d nodes" % (fp, lv, len(v))
                      for (fp, lv), v in sorted(blocks.items())))

    pair = {}
    for (fp, lv), members in sorted(blocks.items()):
        K = grid_of[(fp, lv)]
        C = np.stack([cn[i]["codes"] for i in members])
        V = np.stack([cn[i]["value_mask"] for i in members])
        U = np.stack([cn[i]["unrep_mask"] for i in members])
        sc = score_block(C, V, U)
        for u in range(len(members)):
            for v in range(u + 1, len(members)):
                i, j = members[u], members[v]
                a, b = (i, j) if i < j else (j, i)
                # vab[u,v]: cells where v answers a value and u differs
                # -> u dominates v iff 0.  Map to node order (a,b).
                if (i, j) == (a, b):
                    va_b, vb_a = int(sc["vab"][u, v]), int(sc["vab"][v, u])
                else:
                    va_b, vb_a = int(sc["vab"][v, u]), int(sc["vab"][u, v])
                pair[(a, b)] = dict(
                    level=lv, form_pair=fp, n_cells=K,
                    n_eq_all=int(sc["neq"][u, v]),
                    n_value_comparable=int(sc["nvv"][u, v]),
                    n_matched_value=int(sc["nmv"][u, v]),
                    n_unrep_either=int(sc["nue"][u, v]),
                    viol_a_over_b=va_b,     # a dominates b iff 0
                    viol_b_over_a=vb_a)     # b dominates a iff 0
        del C, V, U, sc
        print("      block %s L%d: %d nodes, %d pairs scored, %.1f s"
              % (fp, lv, len(members),
                 len(members) * (len(members) - 1) // 2, time.time() - t0))
    print("  %d compatible contracted-node pairs in all -- the ENTIRE "
          "connector universe.  Every one of them shares the identical "
          "full key set, so GROUP (the partial-overlap case) has no "
          "instance and is retired."
          % len(pair))

    # ------------------------------------------- connectors
    external = []
    co_scores = defaultdict(lambda: defaultdict(list))
    n_value_null = 0
    for (i, j), rec in sorted(pair.items()):
        K = rec["n_cells"]
        wa = round(rec["n_eq_all"] / float(K), 6)
        nvv = rec["n_value_comparable"]
        wv = (round(rec["n_matched_value"] / float(nvv), 6)
              if nvv > 0 else None)
        rec["weight_all"] = wa
        rec["weight_value"] = wv
        if wv is None:
            n_value_null += 1
        a, b = cn[i], cn[j]
        shared_ops = set(a["operators"]) & set(b["operators"])
        if shared_ops:
            for k in shared_ops:
                co_scores[i][k].append((wv, wa))
                co_scores[j][k].append((wv, wa))
            rec["internalish"] = True
            continue
        external.append(dict(
            kind="external", a=a["id"], b=b["id"], level=rec["level"],
            form_pair=rec["form_pair"], n_cells=K,
            n_value_comparable=nvv,
            n_matched_value=rec["n_matched_value"],
            weight_value=wv,
            n_eq_all=rec["n_eq_all"], weight_all=wa,
            n_unrep_either=rec["n_unrep_either"],
            cross_language=len(set(a["languages"]) |
                               set(b["languages"])) > 1))
    n_internalish = sum(1 for r in pair.values() if r.get("internalish"))
    print("  connectors: %d EXTERNAL (no shared lang.op), %d pairs share "
          "a lang.op and feed the INTERNAL connectors; %d compatible "
          "pairs have NO value-comparable cell (weight_value null, "
          "weight_all still defined -- the connector exists because the "
          "gate passed)"
          % (len(external), n_internalish, n_value_null))

    internal = []
    for n in cn:
        sc = co_scores.get(n["idx"], {})
        for k in n["operators"]:
            lst = sc.get(k, [])
            wvs = [x[0] for x in lst if x[0] is not None]
            was = [x[1] for x in lst]
            internal.append(dict(
                kind="internal", a=n["id"], b=k,
                weight_value=(round(sum(wvs) / len(wvs), 6)
                              if wvs else None),
                weight_all=(round(sum(was) / len(was), 6)
                            if was else None),
                n_co_nodes_comparable=len(lst),
                no_comparison=not lst))
    nnc = sum(1 for e in internal if e["no_comparison"])
    print("  %d internal connectors (one per contracted node per "
          "lang.op); %d carry no_comparison" % (len(internal), nnc))

    # -------------------------- the gate, demonstrated on the old leak
    leak = [e for e in external
            if "truth" in e["form_pair"].split("|")
            and "whole" in e["form_pair"].split("|")]
    tw_cross = 0
    for (i, j) in pair:
        fa = set(cn[i]["form_pair"].split("|"))
        fb = set(cn[j]["form_pair"].split("|"))
        if cn[i]["form_pair"] != cn[j]["form_pair"]:
            tw_cross += 1
    assert tw_cross == 0, "a connector crossed the gate"
    print("  GATE CHECK: 0 connectors join two different form pairs.  "
          "The v4 truth/whole coincidence connectors (the {0,1} overlap "
          "-- 4,279 connectors on <= 4 keys in log 053) cannot exist "
          "here: a truth profile and a whole profile are never "
          "compatible.  (mixed form pairs like truth|whole gate only "
          "with themselves: %d such external connectors, all inside "
          "one identical-key-set block.)" % len(leak))

    # ------------------------------------------------ DOMINANCE
    relations = {}
    counts = defaultdict(int)
    nest_edges = []                      # (dominator idx, dominated idx)
    equal_pairs = []
    for (i, j), rec in sorted(pair.items()):
        contra = rec["n_matched_value"] < rec["n_value_comparable"]
        dom_ab = rec["viol_a_over_b"] == 0     # a dominates b
        dom_ba = rec["viol_b_over_a"] == 0
        if contra:
            rel = "contradicts"
        elif dom_ab and dom_ba:
            rel = "equal_values"
            equal_pairs.append((i, j))
        elif dom_ab:
            rel = "nests"
            nest_edges.append((i, j))
        elif dom_ba:
            rel = "nests"
            nest_edges.append((j, i))
        else:
            rel = "overlaps"
            if rec["n_value_comparable"] == 0:
                counts["overlaps_disjoint_value_sets"] += 1
        relations[(i, j)] = rel
        counts[rel] += 1
        if rel == "nests":
            lo = j if dom_ab else i
            if cn[lo]["n_value_cells"] == 0:
                counts["nests_trivial_dominated_has_no_value_cell"] += 1
    print("  DOMINANCE over the %d compatible pairs: nests %d (of which "
          "trivial -- the dominated side has NO value cell -- %d), "
          "equal_values %d, overlaps %d (of which disjoint value sets "
          "%d), contradicts %d"
          % (len(pair), counts["nests"],
             counts["nests_trivial_dominated_has_no_value_cell"],
             counts["equal_values"], counts["overlaps"],
             counts["overlaps_disjoint_value_sets"],
             counts["contradicts"]))
    assert (counts["nests"] + counts["equal_values"] + counts["overlaps"]
            + counts["contradicts"]) == len(pair)

    # transitive reduction per gate block, for the lattice drawing
    red_edges = []
    for (fp, lv), members in sorted(blocks.items()):
        ms = set(members)
        be = {(a, b) for (a, b) in nest_edges if a in ms}
        red = transitive_reduction(ms, be)
        red_edges.extend(sorted(red))
    print("  strict-nest lattice: %d directed nest connectors reduce to "
          "%d for drawing (transitive reduction per gate block; the "
          "full relation stays in the file)  (%.1f s)"
          % (len(nest_edges), len(red_edges), time.time() - t0))

    # ------------------------------- the overflow fracture, verified
    fracture = {}
    print("  THE OVERFLOW FRACTURE -- scoring (b) is where it must "
          "reappear:")
    for tag, sub_rust in (("i32", "i32 + i32"), ("i64", "i64 + i64")):
        # locate precisely by holder pair
        hits = [n for n in cn for m in n["member_rows"]
                if m.startswith("rust.+ / L1 /") and sub_rust in m]
        assert len(hits) == 1
        na = hits[0]
        nb = [n for n in cn for m in n["member_rows"]
              if m.startswith("ruby.+ / L1 /")
              and "Integer + Integer" in m]
        assert len(nb) == 1
        nb = nb[0]
        i, j = sorted((na["idx"], nb["idx"]))
        rec = pair[(i, j)]
        # sides by the LOCATED nodes, never by language lists -- the
        # ruby node may carry rust member profiles too (ruby Integer +
        # Integer contracts cross-language with rust i128 + i128)
        crust, cruby = na["codes"], nb["codes"]
        n_vv_diff = int((na["value_mask"] & nb["value_mask"]
                         & (crust != cruby)).sum())
        rust_decl = AB.decl[crust]
        ruby_val = nb["value_mask"]
        rust_unrep = na["unrep_mask"]
        n_overflow = int((rust_decl & ruby_val).sum())
        n_unrep_vs_val = int((rust_unrep & ruby_val).sum())
        xsf = full_index["x_sets"][
            full_index["full_sets"]["whole/L1"]]["spellings"]
        keys = []
        for pp in np.nonzero(rust_decl & ruby_val)[0]:
            keys.append("(%s, %s) -> %s vs %s"
                        % (xsf[pp // len(xsf)], xsf[pp % len(xsf)],
                           AB.text[crust[pp]], AB.text[cruby[pp]]))
        fracture[tag] = dict(
            rust_node=na["id"], ruby_node=nb["id"],
            n_cells=rec["n_cells"],
            weight_value=rec["weight_value"],
            weight_all=rec["weight_all"],
            n_value_comparable=rec["n_value_comparable"],
            n_matched_value=rec["n_matched_value"],
            n_value_disagreements=n_vv_diff,
            n_overflow_cells_rust_declines_ruby_answers=n_overflow,
            n_unrepresentable_vs_value=n_unrep_vs_val,
            overflow_keys=keys,
            relation=relations[(i, j)])
        print("     rust.+ %s x %s ~ ruby.+ Integer x Integer, L1: "
              "weight_value %s over %d value-comparable cells "
              "(%d matched); weight_all %.4f over %d cells; %d overflow "
              "cells where rust declines and ruby answers; %d "
              "UNREPRESENTABLE-vs-value cells; dominance reads %s"
              % (tag, tag,
                 ("%.4f" % rec["weight_value"]
                  if rec["weight_value"] is not None else "null"),
                 rec["n_value_comparable"], rec["n_matched_value"],
                 rec["weight_all"], rec["n_cells"], n_overflow,
                 n_unrep_vs_val, relations[(i, j)]))

    # --------------------------------------------------------- nodes
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
            language=n["languages"][0],
            operator=n["operators"][0].partition(".")[2],
            n_cells=n["n_probes"],
            n_value_cells=n["n_value_cells"],
            n_declines=n["n_declines"],
            n_unrepresentable=n["n_unrepresentable"]))
    nid = {n["id"]: i for i, n in enumerate(nodes)}
    edges = internal + external

    # --------------------------------------- thresholds, two scorings
    sanity_thresholds = {}
    for mode in ("value", "all"):
        w = "weight_" + mode
        for t in (0.95, 0.85, 0.70):
            act = [e for e in external
                   if e[w] is not None and e[w] >= t]
            xl = sum(1 for e in act if e["cross_language"])
            comps = components(len(nodes),
                               [(nid[e["a"]], nid[e["b"]]) for e in act])
            mult = [c for c in comps if len(c) > 1]
            rec = dict(external_edges=len(act), cross_language=xl,
                       same_language=len(act) - xl,
                       components_external_only=len(comps),
                       largest_component=len(comps[0]),
                       multi_node_components=len(mult),
                       by_level={"L%d" % l: sum(1 for e in act
                                                if e["level"] == l)
                                 for l in (1, 2)})
            sanity_thresholds["%s@%.2f" % (mode, t)] = rec
            print("  scoring %-5s t=%.2f : %d external (%d same-lang, "
                  "%d cross-lang; L1 %d, L2 %d); components (EXTERNAL "
                  "ONLY) %d (%d multi-node), largest %d"
                  % (mode, t, len(act), len(act) - xl, xl,
                     rec["by_level"]["L1"], rec["by_level"]["L2"],
                     len(comps), len(mult), len(comps[0])))

    # --------------------------------------------- the named pairs
    node_of_row = {}
    for n in cn:
        for m in n["member_rows"]:
            node_of_row[m] = n["idx"]

    def row_pairs(ka, kb, level):
        ra = [r for r in rows if r["key"] == ka and r["level"] == level]
        rb = [r for r in rows if r["key"] == kb and r["level"] == level]
        out = []
        for x in ra:
            for y in rb:
                if x["id"] == y["id"]:
                    continue
                i, j = node_of_row[x["id"]], node_of_row[y["id"]]
                if i == j:
                    out.append(dict(contracted=True, weight_value=1.0,
                                    weight_all=1.0, relation="contract"))
                    continue
                k = (i, j) if i < j else (j, i)
                rec = pair.get(k)
                if rec is None:
                    out.append(dict(contracted=False, gate="closed"))
                    continue
                out.append(dict(contracted=False,
                                weight_value=rec["weight_value"],
                                weight_all=rec["weight_all"],
                                relation=relations[k]))
        return out

    PAIRS = [("ruby.&&", "ruby.||"), ("ruby.&&", "ruby.and"),
             ("ruby.||", "ruby.or"), ("rust.+", "ruby.+"),
             ("rust.+", "rust.-"), ("ruby.*", "ruby.&")]
    named = {}
    print("  THE NAMED PAIRS under the gate (row pairs; 'gate closed' = "
          "incompatible profiles, no connector by rule)")
    for ka, kb in PAIRS:
        rec = {}
        for level in (1, 2):
            sel = row_pairs(ka, kb, level)
            gated = [s for s in sel if s.get("gate") == "closed"]
            open_ = [s for s in sel if s.get("gate") != "closed"]
            ctr = [s for s in open_ if s["contracted"]]
            con = [s for s in open_ if not s["contracted"]]
            wv = [s["weight_value"] for s in con
                  if s.get("weight_value") is not None]
            wa = [s["weight_all"] for s in con]
            rels = defaultdict(int)
            for s in con:
                rels[s["relation"]] += 1
            rec["L%d" % level] = dict(
                n_row_pairs=len(sel), gate_closed=len(gated),
                contracted=len(ctr), on_connector=len(con),
                weight_value=dist(wv), weight_all=dist(wa),
                relations=dict(rels))
            print("     %s ~ %s L%d: %d row pairs; %d gate-closed; %d "
                  "CONTRACTED; %d on a connector | value %s | all %s | "
                  "relations %s"
                  % (ka, kb, level, len(sel), len(gated), len(ctr),
                     len(con),
                     ("mean %.4f min %.4f max %.4f"
                      % (dist(wv)["mean"], dist(wv)["min"],
                         dist(wv)["max"])) if wv else "--",
                     ("mean %.4f min %.4f max %.4f"
                      % (dist(wa)["mean"], dist(wa)["min"],
                         dist(wa)["max"])) if wa else "--",
                     dict(rels)))
        named["%s ~ %s" % (ka, kb)] = rec

    # ------------------------------------------------------------ emit
    skeys = sorted(pair)
    out = dict(
        status="ROW GRAPH v5 -- FULL GRIDS (matrices_full/) with the owner's "
               "rulings of 2026-08-21 (log 054): the COMPATIBILITY GATE "
               "(same form pair, same level, same intended X set -- a "
               "hard gate, no key-to-key clustering ever), "
               "UNREPRESENTABLE as a static cell class, GROUP retired, "
               "CONTRACT kept, TWO scorings on every connector, and the "
               "directed DOMINANCE reading.  ASSEMBLY ONLY.",
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        scope="rust (static) + ruby (route C) only; the other ten wait",
        source="matrices_full/ -- every profile inflated to the FULL X "
               "set of its form and level; UNREPRESENTABLE fills the "
               "statically-known gaps; built by l3_cart_full.py over "
               "matrices_cart/, which is unchanged on disk.",
        gate_rule="PROFILE COMPATIBILITY IS A HARD GATE: two profiles "
                  "connect only if same form pair, same level, same "
                  "intended X set.  With full grids the gate is "
                  "(form_pair, level) and every profile inside it "
                  "carries the SAME key set.  A truth profile and a "
                  "whole profile are NEVER compatible, whatever cells "
                  "they coincidentally share.  Cell agreement counts "
                  "only inside a compatible profile pair.",
        group_rule="RETIRED.  Full grids make a partial overlap "
                   "impossible inside the gate: every compatible pair "
                   "shares the identical key set, so the "
                   "partial-overlap case has no instance.",
        contract_rule="KEPT: identical outputs at EVERY key over the "
                      "identical key set -- UNREPRESENTABLE and outcome "
                      "tokens included -- plain identity, transitive, "
                      "no clique test.",
        scoring_a_value="weight_value: agreement over VALUE cells only; "
                        "a cell where either side is UNREPRESENTABLE, "
                        "REFUSE, RAISE:* or ABORT leaves numerator and "
                        "denominator.  Zero value-comparable cells -> "
                        "null, never zero.",
        scoring_b_all="weight_all: agreement over ALL cells with "
                      "UNREPRESENTABLE / REFUSE / RAISE:<kind> / ABORT "
                      "treated as answers -- byte-identical token = "
                      "agree; denominator = the full grid.",
        which_weight="NOT DECIDED HERE.  Both ride on every connector; "
                     "the explorer toggles; the ruling awaits the owner.",
        dominance_rule="Over COMPATIBLE pairs only: A DOMINATES B when "
                       "at every key where B answers a value, A answers "
                       "the identical value (A may answer at more "
                       "keys).  Read as nests / overlaps / contradicts, "
                       "with equal_values the mutual-nest case and "
                       "disjoint value sets a recorded sub-case of "
                       "overlaps.",
        physics="internal springs near zero (%g against %g external); "
                "the threshold cuts EXTERNAL connectors only; "
                "components are counted on EXTERNAL connectors only; "
                "autofit runs ONCE then never again, any wheel or "
                "mousedown disables it permanently, a fit view button "
                "exists." % (INT_SPRING, EXT_SPRING),
        vocabulary="super-node / sub-node / co-node / sub-tree; the "
                   "OS-stopped outcome is ABORT",
        int_spring=INT_SPRING, ext_spring=EXT_SPRING,
        render_cap=RENDER_CAP,
        grid_sizes={"%s/L%d" % k: v for k, v in sorted(grid_of.items())},
        n_raw_rows=len(rows), n_contracted_nodes=len(cn),
        n_central_nodes=len(langop_keys),
        n_internal_edges=len(internal), n_external_edges=len(external),
        n_compatible_pairs=len(pair),
        n_value_null_pairs=n_value_null,
        v4_rule_contracted_nodes=len(v4b),
        totals=dict(cells=sum(r["n_probes"] for r in rows),
                    unrepresentable=sum(r["n_unrepresentable"]
                                        for r in rows),
                    values=sum(r["n_values"] for r in rows),
                    declines=sum(r["n_declines"] for r in rows)),
        dominance_counts=dict(counts),
        overflow_fracture=fracture,
        sanity=dict(thresholds=sanity_thresholds, named=named),
        pairs_compact=dict(
            note="every compatible pair (a,b) of contracted nodes, a<b, "
                 "indices counted from the FIRST contracted node (node "
                 "index minus n_central_nodes).  K = full grid size, "
                 "neq = cells byte-identical (scoring b numerator), "
                 "nvv = value-comparable cells, nmv = matched value "
                 "cells (scoring a numerator), nue = cells where either "
                 "side is UNREPRESENTABLE, vab = cells where b answers "
                 "a value and a differs (a dominates b iff 0), vba the "
                 "mirror.  rel = the dominance reading.",
            n=len(skeys),
            a=[k[0] for k in skeys], b=[k[1] for k in skeys],
            K=[pair[k]["n_cells"] for k in skeys],
            neq=[pair[k]["n_eq_all"] for k in skeys],
            nvv=[pair[k]["n_value_comparable"] for k in skeys],
            nmv=[pair[k]["n_matched_value"] for k in skeys],
            nue=[pair[k]["n_unrep_either"] for k in skeys],
            vab=[pair[k]["viol_a_over_b"] for k in skeys],
            vba=[pair[k]["viol_b_over_a"] for k in skeys],
            rel=[relations[k] for k in skeys]),
        nodes=nodes, edges=edges)

    jp = os.path.join(HERE, "row_graph_v5.json")
    json.dump(out, open(jp, "w"), separators=(",", ":"))
    print("  wrote %s (%.2f MB)" % (jp, os.path.getsize(jp) / 1e6))

    html = HTML_TEMPLATE.replace("__GRAPH__",
                                 json.dumps(out, separators=(",", ":")))
    hp = os.path.join(HERE, "row_graph_explorer_v5.html")
    with open(hp, "w") as f:
        f.write(html)
    print("  wrote %s (%.2f MB)" % (hp, os.path.getsize(hp) / 1e6))

    # ------------------------------------------------ dominance emit
    dom = dict(
        status="DOMINANCE v5 -- the directed containment relation over "
               "COMPATIBLE profile pairs, the owner's ruled next object (log "
               "054).  A dominates B when at every key where B answers "
               "a value, A answers the identical value.  Read as nests "
               "/ overlaps / contradicts.  The layer-3-era "
               "dominance_lattice.json is precedent for the idea only; "
               "none of its data is inherited.",
        built=out["built"], scope=out["scope"],
        source="row_graph_v5 contracted nodes over matrices_full/",
        gate_rule=out["gate_rule"],
        dominance_rule=out["dominance_rule"],
        vocabulary=out["vocabulary"],
        counts=dict(counts),
        n_nest_edges=len(nest_edges),
        n_reduced_edges=len(red_edges),
        nodes=[dict(id=n["id"], label=n["label"], level=n["level"],
                    form_pair=n["form_pair"], languages=n["languages"],
                    operators=n["operators"],
                    holder_pairs=n["holder_pairs"],
                    n_members=n["n_members"],
                    n_cells=n["n_probes"],
                    n_value_cells=n["n_value_cells"],
                    n_declines=n["n_declines"],
                    n_unrepresentable=n["n_unrepresentable"])
               for n in cn],
        nest_edges=[[cn[a]["id"], cn[b]["id"]] for a, b in nest_edges],
        reduced_edges=[[cn[a]["id"], cn[b]["id"]] for a, b in red_edges],
        equal_pairs=[[cn[a]["id"], cn[b]["id"]] for a, b in equal_pairs],
        blocks=sorted("%s/L%d" % k for k in blocks))
    dp = os.path.join(HERE, "dominance_v5.json")
    json.dump(dom, open(dp, "w"), separators=(",", ":"))
    print("  wrote %s (%.2f MB)" % (dp, os.path.getsize(dp) / 1e6))
    dhtml = DOM_TEMPLATE.replace("__DOM__",
                                 json.dumps(dom, separators=(",", ":")))
    dhp = os.path.join(HERE, "dominance_explorer_v5.html")
    with open(dhp, "w") as f:
        f.write(dhtml)
    print("  wrote %s (%.2f MB)" % (dhp, os.path.getsize(dhp) / 1e6))

    # ------------------------------------------- python-side verify
    print("PYTHON VERIFY")
    back = json.load(open(jp))
    assert len(back["nodes"]) == len(nodes)
    assert len(back["edges"]) == len(edges)
    idset = {n["id"] for n in back["nodes"]}
    assert all(e["a"] in idset for e in back["edges"])
    for e in back["edges"]:
        if e["kind"] == "external":
            assert e["b"] in idset
            assert 0.0 <= e["weight_all"] <= 1.0
            assert (e["weight_value"] is None
                    or 0.0 <= e["weight_value"] <= 1.0)
    byid = {n["id"]: n for n in back["nodes"]}
    for e in back["edges"]:
        if e["kind"] != "external":
            continue
        a, b = byid[e["a"]], byid[e["b"]]
        assert a["kind"] == b["kind"] == "contracted"
        assert not (set(a["operators"]) & set(b["operators"]))
        assert a["level"] == b["level"] == e["level"]
        assert a["form_pair"] == b["form_pair"] == e["form_pair"]
        assert a["n_cells"] == b["n_cells"] == e["n_cells"]
    print("  [external] every external connector joins two contracted "
          "nodes with NO shared lang.op, the SAME level, the SAME form "
          "pair and the SAME full grid -- the gate, checked on every "
          "one of %d" % len(external))
    assert sum(n["n_members"] for n in back["nodes"]
               if n["kind"] == "contracted") == len(rows)
    txt = open(hp).read()
    assert '"nodes"' in txt and "__GRAPH__" not in txt
    assert "<script src" not in txt and "http://" not in txt
    dtxt = open(dhp).read()
    assert "__DOM__" not in dtxt and "<script src" not in dtxt \
        and "http://" not in dtxt
    print("  [html] both explorers: data embedded, placeholder gone, "
          "no external script, no CDN, no network reference")
    print("  done in %.1f s" % (time.time() - t0))


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Full grids &mdash; row graph v5 (compatibility gate, two scorings)</title>
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
</style></head><body>
<div id="bar">
 <b>Full grids &mdash; row graph v5</b>
 <span>scoring <select id="smode">
  <option value="value">value cells only (a)</option>
  <option value="all">ALL cells, tokens as answers (b)</option>
 </select> <i>(neither is THE weight; that ruling awaits the owner)</i></span>
 <span>threshold
  <input type="range" id="thr" min="0" max="100" value="85">
  <span id="thrv">0.85</span></span>
 <label><input type="checkbox" id="showint" checked> internal
  connectors</label>
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
 <span id="stats"></span>
</div>
<div id="rule"></div>
<canvas id="cv"></canvas><div id="tip"></div>
<script>
const G=__GRAPH__;
const N=G.nodes,E=G.edges;
const idx={};N.forEach((n,i)=>{idx[n.id]=i;});
E.forEach(e=>{e.ai=idx[e.a];if(e.kind==="external")e.bi=idx[e.b];
 else e.bi=idx[e.b];});
const INT=E.filter(e=>e.kind==="internal");
const EXT=E.filter(e=>e.kind==="external").map((e,i)=>(e._o=i,e));
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
 thrv=$("thrv"),smode=$("smode"),showint=$("showint"),cmode=$("cmode"),
 lmode=$("lmode"),cap=$("cap"),search=$("search"),stats=$("stats"),
 rule=$("rule");
const NCON=N.filter(n=>n.kind==="contracted").length,
      NCEN=N.filter(n=>n.kind==="central").length;
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
let T=0.85,SM="value",SI=true,CM="lang",LM="all",
 CAP=20000,q="",act=[],actInt=[],hover=null,hoverE=null,drag=null;
let ox=0,oy=0,scale=1,heat=1;
// TWO SCORINGS ride on every connector; the toggle switches which one
// cuts and weights.  Neither is THE weight -- that ruling awaits the owner.
// In value mode a connector whose weight_value is null (no
// value-comparable cell) cannot clear any threshold and is not drawn;
// the connector still exists in the data because the gate passed.
function W(e){const w=SM==="value"?e.weight_value:e.weight_all;
 return w==null?-1:w;}
function vok(n){return LM==="all"||n.kind==="central"||
 String(n.level)===LM;}
function color(n){
 if(CM==="op")return ocolor[n.operator];
 if(CM==="level")return n.kind==="central"?"#ffffff"
  :vcolor[String(n.level)];
 if(CM==="form")return n.kind==="central"?"#ffffff":fcolor[n.form_pair];
 if(CM==="members")return n.kind==="central"?"#ffffff":mcolor[mbin(n)];
 return lcolor[n.language];}
function refresh(){
 T=thr.value/100;thrv.textContent=T.toFixed(2);
 SM=smode.value;SI=showint.checked;CM=cmode.value;LM=lmode.value;
 CAP=+cap.value;q=search.value.trim().toLowerCase();
 EXT.forEach(e=>{e._w=W(e);});
 // the threshold cuts EXTERNAL connectors ONLY
 const pass=EXT.filter(e=>e._w>=T&&vok(N[e.ai])&&vok(N[e.bi]))
  .sort((p,r)=>(r._w-p._w)||(p._o-r._o));
 const capped=pass.length>CAP;
 act=capped?pass.slice(0,CAP):pass;
 actInt=SI?INT.filter(e=>vok(N[e.ai])):[];
 // components are counted on EXTERNAL connectors ONLY
 const p=N.map((_,i)=>i);
 const f=x=>{while(p[x]!=x){p[x]=p[p[x]];x=p[x];}return x;};
 act.forEach(e=>{const a=f(e.ai),b=f(e.bi);if(a!=b)p[a]=b;});
 const roots=new Set(N.map((_,i)=>f(i)));
 const comps=roots.size;
 let multi=0;{const c={};N.forEach((_,i)=>{const r=f(i);c[r]=(c[r]||0)+1;});
  multi=Object.values(c).filter(v=>v>1).length;}
 const xl=act.filter(e=>e.cross_language).length;
 stats.textContent=N.length+" nodes | "+NCON+" contracted ("+
  G.n_raw_rows+" profiles) | "+NCEN+" central | "+act.length+
  " external ("+xl+" cross-language) | "+actInt.length+" internal | "+
  comps+" components ("+multi+" multi-node)";
 rule.textContent="RULE: PROFILE COMPATIBILITY IS A HARD GATE -- two "+
  "profiles connect only if same form pair, same level, same intended "+
  "X set; a truth profile and a whole profile are NEVER compatible; no "+
  "key-to-key clustering, ever.  Every compatible pair shares the "+
  "identical FULL key set (GROUP is retired; CONTRACT keeps its "+
  "meaning).  Scoring "+(SM==="value"
   ?"(a): agreement over VALUE cells only -- UNREPRESENTABLE and "+
    "declines excluded from numerator and denominator; a connector "+
    "with no value-comparable cell has weight null and is not drawn "+
    "in this mode."
   :"(b): agreement over ALL cells of the full grid, with "+
    "UNREPRESENTABLE / REFUSE / RAISE:* / ABORT treated as answers "+
    "(byte-identical token = agree).")+
  "  NEITHER SCORING IS CHOSEN AS THE WEIGHT.  The threshold cuts "+
  "EXTERNAL connectors only; internal springs are near zero ("+
  G.int_spring+" against "+G.ext_spring+" external); COMPONENTS ARE "+
  "COUNTED ON EXTERNAL CONNECTORS ONLY. "+(capped
   ?("DRAW CAP IN FORCE: "+pass.length+" clear "+T.toFixed(2)+
     ", the top "+CAP+" BY WEIGHT are drawn, "+(pass.length-CAP)+
     " are not.")
   :("all "+pass.length+" external connectors clearing "+T.toFixed(2)+
     " are drawn (cap "+(CAP>=1e6?"off":CAP)+")."));
 heat=Math.max(heat,0.25);}
[thr].forEach(e=>e.oninput=refresh);
[smode,showint,cmode,lmode,cap].forEach(e=>e.onchange=refresh);
search.oninput=refresh;
refresh();
function size(){cv.width=innerWidth;cv.height=innerHeight-cv.offsetTop;}
addEventListener("resize",size);size();
const CELL=170,INT_K=G.int_spring,EXT_K=G.ext_spring;
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
  // near-zero internal spring -- a visual tether, never the layout
  actInt.forEach(e=>{const a=N[e.ai],b=N[e.bi];
   let dx=b.x-a.x,dy=b.y-a.y,d=Math.sqrt(dx*dx+dy*dy);if(d<1)d=1;
   const f=Math.min((d-70)*INT_K,6);
   a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f;});
  // EXTERNAL connectors carry the layout
  act.forEach(e=>{const a=N[e.ai],b=N[e.bi];
   let dx=b.x-a.x,dy=b.y-a.y,d=Math.sqrt(dx*dx+dy*dy);if(d<1)d=1;
   const f=Math.min((d-140)*EXT_K*Math.max(0,e._w),6);
   a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f;});
  N.forEach(n=>{
   n.vx-=n.x*0.004;n.vy-=n.y*0.004;
   const v=Math.hypot(n.vx,n.vy);
   if(v>30){n.vx*=30/v;n.vy*=30/v;}
   n.x+=n.vx*0.25*heat;n.y+=n.vy*0.25*heat;n.vx*=0.75;n.vy*=0.75;
   const r=Math.hypot(n.x,n.y);
   if(r>2900){n.x*=2900/r;n.y*=2900/r;}});
  heat*=0.992;}
 draw();requestAnimationFrame(step);}
function fit(){
 let mnx=1e9,mny=1e9,mxx=-1e9,mxy=-1e9;
 N.forEach(n=>{mnx=Math.min(mnx,n.x);mxx=Math.max(mxx,n.x);
  mny=Math.min(mny,n.y);mxy=Math.max(mxy,n.y);});
 const w2=Math.max(mxx-mnx,10),h2=Math.max(mxy-mny,10);
 scale=Math.min((cv.width-80)/w2,(cv.height-80)/h2,3);
 ox=-(mnx+mxx)/2;oy=-(mny+mxy)/2;}
// AUTOFIT RUNS ONCE THEN NEVER AGAIN.  Any wheel or mousedown disables
// it permanently.  The "fit view" button is the only way back.
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
function draw(){ctx.clearRect(0,0,cv.width,cv.height);
 ctx.lineWidth=1;
 if(actInt.length){ctx.setLineDash([3,3]);
  actInt.forEach(e=>{const a=N[e.ai],b=N[e.bi];
   ctx.strokeStyle=e===hoverE?"#fff":"rgba(224,184,62,0.16)";
   ctx.beginPath();ctx.moveTo(sx(a.x),sy(a.y));
   ctx.lineTo(sx(b.x),sy(b.y));ctx.stroke();});
  ctx.setLineDash([]);}
 act.forEach(e=>{const a=N[e.ai],b=N[e.bi];
  ctx.strokeStyle=e===hoverE?"#fff":
  "rgba(120,170,220,"+(0.07+0.45*(Math.max(0,e._w)-T)/(1.001-T))+")";
  ctx.beginPath();ctx.moveTo(sx(a.x),sy(a.y));
  ctx.lineTo(sx(b.x),sy(b.y));ctx.stroke();});
 N.forEach((n,i)=>{if(!vok(n))return;
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
 ctx.font="12px sans-serif";
 N.forEach(n=>{if(n.kind!=="central")return;
  ctx.fillStyle="#fff";ctx.fillText(n.id,sx(n.x)+13,sy(n.y)+4);});
 if(scale>1.1||q){ctx.font="10px sans-serif";ctx.fillStyle="#9aa2ad";
  N.forEach((n,i)=>{if(n.kind!=="contracted"||!vok(n))return;
   if(q&&!hit(n))return;
   ctx.fillText(n.label,sx(n.x)+5,sy(n.y)+3);});}
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
 ctx.fillText("solid = external (carries the layout)   dashed = "+
  "internal (near-zero spring, a visual tether only)",10,ly-18);
 ctx.font="13px sans-serif";}
function pick(mx,my){hover=null;hoverE=null;
 for(let i=0;i<N.length;i++){const n=N[i];if(!vok(n))continue;
  const dx=sx(n.x)-mx,dy=sy(n.y)-my;
  const rr=n.kind==="central"?200:60;
  if(dx*dx+dy*dy<rr){hover=n;return;}}
 let best=25;
 const scan=act.concat(actInt);
 for(const e of scan){const a=N[e.ai],b=N[e.bi];
  const x1=sx(a.x),y1=sy(a.y),x2=sx(b.x),y2=sy(b.y);
  const L2=(x2-x1)**2+(y2-y1)**2;if(!L2)continue;
  let t=((mx-x1)*(x2-x1)+(my-y1)*(y2-y1))/L2;t=Math.max(0,Math.min(1,t));
  const dx=mx-(x1+t*(x2-x1)),dy=my-(y1+t*(y2-y1)),d2=dx*dx+dy*dy;
  if(d2<best){best=d2;hoverE=e;}}}
function mxy(ev){const r=cv.getBoundingClientRect();
 return[ev.clientX-r.left,ev.clientY-r.top];}
function f4(x){return x==null?"null":(+x).toFixed(4);}
function esc(s){return String(s).replace(/&/g,"&amp;")
 .replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function nodeTip(n){
 if(n.kind==="central")
  return "<b>"+esc(n.id)+"</b><br>CENTRAL node &middot; language "+
   esc(n.language)+" &middot; operator "+esc(n.operator)+
   "<br>profiles on this operator: "+n.n_rows+
   "<br>contracted nodes carrying it: "+n.n_contracted;
 return "<b>"+esc(n.id)+"</b> &middot; CONTRACTED node &middot; "+
  "<b>"+n.n_members+" member profile"+(n.n_members==1?"":"s")+"</b>"+
  "<br>level <b>"+n.level+"</b> &middot; form "+esc(n.form_pair)+
  " &middot; languages "+esc(n.languages.join(", "))+
  "<br>operators "+esc(n.operators.join(", "))+
  "<br>holder pairs "+esc(n.holder_pairs.join(" ; "))+
  "<br>full grid "+n.n_cells+" cells &middot; value "+n.n_value_cells+
  " &middot; declines "+n.n_declines+" &middot; UNREPRESENTABLE "+
  n.n_unrepresentable+
  "<br><i>member profiles (identity: identical full grid)</i>"+
  "<br>&nbsp;&nbsp;"+n.members.slice(0,24).map(esc)
   .join("<br>&nbsp;&nbsp;")+
  (n.members.length>24?("<br>&nbsp;&nbsp;&hellip; and "+
   (n.members.length-24)+" more"):"");}
function edgeTip(e){
 if(e.kind==="internal")
  return "<b>INTERNAL connector</b><br>"+esc(e.a)+"<br>&rarr; "+
   esc(e.b)+"<br>value-cells "+f4(e.weight_value)+
   " &middot; all-cells "+f4(e.weight_all)+
   (e.no_comparison?" (no compatible co-node of that lang.op &mdash; "+
    "no comparison)":(" &middot; over "+e.n_co_nodes_comparable+
    " co-node"+(e.n_co_nodes_comparable==1?"":"s")))+
   "<br>structure, not similarity: never cut by the threshold; its "+
   "spring is near zero";
 return "<b>EXTERNAL connector</b> (compatible profiles: same form "+
  "pair, same level, same full X set)<br>"+esc(e.a)+"<br>&harr; "+
  esc(e.b)+
  "<br><b>scoring (a) value cells: "+f4(e.weight_value)+"</b> ("+
  e.n_matched_value+"/"+e.n_value_comparable+" value-comparable cells)"+
  "<br><b>scoring (b) all cells: "+f4(e.weight_all)+"</b> ("+
  e.n_eq_all+"/"+e.n_cells+" cells byte-identical, tokens as answers)"+
  "<br>level "+e.level+" &middot; "+esc(e.form_pair)+
  " &middot; full grid "+e.n_cells+
  " &middot; UNREPRESENTABLE on either side at "+e.n_unrep_either+
  " cells<br>"+(e.cross_language?"CROSS-language":"same-language")+
  " &middot; identical key sets by construction (full grids)";}
cv.onmousemove=ev=>{const[mx,my]=mxy(ev);
 if(drag){if(drag.node){drag.node.x=(mx-cv.width/2)/scale-ox;
   drag.node.y=(my-cv.height/2)/scale-oy;heat=Math.max(heat,0.3);}
  else{ox+=(mx-drag.px)/scale;oy+=(my-drag.py)/scale;
   drag.px=mx;drag.py=my;}return;}
 pick(mx,my);
 if(hover){tip.style.display="block";tip.innerHTML=nodeTip(hover);}
 else if(hoverE){tip.style.display="block";tip.innerHTML=edgeTip(hoverE);}
 else tip.style.display="none";
 tip.style.left=(ev.clientX+14)+"px";tip.style.top=(ev.clientY+14)+"px";};
cv.onmousedown=ev=>{const[mx,my]=mxy(ev);pick(mx,my);
 drag=hover?{node:hover}:{px:mx,py:my};};
addEventListener("mouseup",()=>drag=null);
cv.onwheel=ev=>{ev.preventDefault();
 scale*=ev.deltaY<0?1.1:0.9;scale=Math.max(0.05,Math.min(8,scale));};
step();
</script></body></html>
"""


DOM_TEMPLATE = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Dominance v5 &mdash; the directed lattice over compatible profiles</title>
<style>
 body{margin:0;font:13px/1.4 system-ui,sans-serif;background:#14161a;
      color:#d7dae0;display:flex;flex-direction:column;height:100vh}
 #bar{padding:7px 12px;background:#1d2026;display:flex;
      gap:14px;align-items:center;flex-wrap:wrap;
      border-bottom:1px solid #2b2f36}
 #bar b{color:#fff}
 input[type=range]{width:140px;vertical-align:middle}
 select,button,#search{background:#14161a;border:1px solid #3a3f48;
        color:#d7dae0;padding:2px 5px;border-radius:4px}
 #stats{color:#9aa2ad}
 #rule{color:#7d8590;font-size:11px;padding:3px 12px;background:#191c21;
       border-bottom:1px solid #2b2f36}
 canvas{flex:1;display:block}
 #tip{position:fixed;pointer-events:none;background:#22262d;
      border:1px solid #3a3f48;border-radius:5px;padding:6px 9px;
      display:none;max-width:560px;z-index:9;font-size:12px}
</style></head><body>
<div id="bar">
 <b>Dominance v5 &mdash; lattice</b>
 <span>gate block <select id="bsel"></select></span>
 <span>min value cells (dominated side)
  <input type="range" id="thr" min="0" max="100" value="0">
  <span id="thrv">0</span></span>
 <input id="search" placeholder="search node / operator / holder">
 <button id="fitbtn">fit view</button>
 <span id="stats"></span>
</div>
<div id="rule"></div>
<canvas id="cv"></canvas><div id="tip"></div>
<script>
const D=__DOM__;
const $=s=>document.getElementById(s);
const cv=$("cv"),ctx=cv.getContext("2d"),tip=$("tip"),bsel=$("bsel"),
 thr=$("thr"),thrv=$("thrv"),search=$("search"),stats=$("stats"),
 rule=$("rule");
const byId={};D.nodes.forEach(n=>byId[n.id]=n);
const blockOf=n=>n.form_pair+"/L"+n.level;
D.blocks.forEach(b=>{const o=document.createElement("option");
 o.value=b;o.textContent=b;bsel.appendChild(o);});
// default to the block with the most nest connectors
{const cnt={};D.reduced_edges.forEach(e=>{const b=blockOf(byId[e[0]]);
  cnt[b]=(cnt[b]||0)+1;});
 let best=D.blocks[0],bc=-1;
 for(const b of D.blocks)if((cnt[b]||0)>bc){bc=cnt[b]||0;best=b;}
 bsel.value=best;}
let B=bsel.value,T=0,q="",nodes=[],edges=[],hover=null,hoverE=null,
 drag=null;
let ox=0,oy=0,scale=1;
function build(){
 B=bsel.value;T=+thr.value;thrv.textContent=T;
 q=search.value.trim().toLowerCase();
 nodes=D.nodes.filter(n=>blockOf(n)===B);
 const ids=new Set(nodes.map(n=>n.id));
 const red=D.reduced_edges.filter(e=>ids.has(e[0])&&ids.has(e[1]));
 // the slider cuts EXTERNAL connectors only (every nest connector here
 // is external -- it joins two distinct contracted nodes; there are no
 // internal connectors in the lattice view and that is stated)
 edges=red.filter(e=>byId[e[1]].n_value_cells>=T);
 // layering: a dominator sits HIGHER than what it dominates.  Layer =
 // longest dominator chain above (over the reduced connectors).
 const above={},below={};
 nodes.forEach(n=>{above[n.id]=[];below[n.id]=[];});
 edges.forEach(e=>{below[e[0]].push(e[1]);above[e[1]].push(e[0]);});
 const layer={},seen={};
 function depth(id){
  if(layer[id]!=null)return layer[id];
  if(seen[id])return 0;
  seen[id]=1;
  let d=0;above[id].forEach(a=>{d=Math.max(d,depth(a)+1);});
  layer[id]=d;return d;}
 nodes.forEach(n=>depth(n.id));
 const rows={};
 nodes.forEach(n=>{(rows[layer[n.id]]=rows[layer[n.id]]||[]).push(n);});
 Object.keys(rows).forEach(l=>{
  rows[l].sort((a,b)=>b.n_value_cells-a.n_value_cells||
   (a.id<b.id?-1:1));
  rows[l].forEach((n,i)=>{
   if(n._placed)return;
   n.x=(i-(rows[l].length-1)/2)*150;
   n.y=(+l)*160;n._placed=true;n._layer=+l;});});
 // components on the drawn EXTERNAL connectors only
 const im={};nodes.forEach((n,i)=>im[n.id]=i);
 const p=nodes.map((_,i)=>i);
 const f=x=>{while(p[x]!=x){p[x]=p[p[x]];x=p[x];}return x;};
 edges.forEach(e=>{const a=f(im[e[0]]),b=f(im[e[1]]);if(a!=b)p[a]=b;});
 const comps=new Set(nodes.map((_,i)=>f(i))).size;
 const full=D.nest_edges.filter(e=>ids.has(e[0])&&ids.has(e[1])).length;
 const eq=D.equal_pairs.filter(e=>ids.has(e[0])&&ids.has(e[1])).length;
 stats.textContent=nodes.length+" contracted nodes | "+edges.length+
  " reduced nest connectors drawn (of "+red.length+" reduced, "+full+
  " full nest relations in this block) | "+eq+" equal_values pairs | "+
  comps+" components (external connectors only)";
 rule.textContent="DOMINANCE (directed, the owner's ruling of 2026-08-21): "+
  "A DOMINATES B when at every key where B answers a value, A answers "+
  "the identical value (A may answer at more keys).  Read as nests / "+
  "overlaps / contradicts.  Over COMPATIBLE profile pairs only -- the "+
  "gate of row_graph_v5 -- so every pair here shares the identical "+
  "full key set.  Arrows point from the dominator (drawn HIGHER) to "+
  "the dominated (drawn LOWER); the drawing is the TRANSITIVE "+
  "REDUCTION, the full relation is in dominance_v5.json.  The slider "+
  "cuts EXTERNAL connectors only (all lattice connectors are "+
  "external; there are no internal connectors in this view); "+
  "components are counted on external connectors only.  Counts over "+
  "all blocks: nests "+D.counts.nests+", equal_values "+
  D.counts.equal_values+", overlaps "+D.counts.overlaps+
  ", contradicts "+D.counts.contradicts+".";}
bsel.onchange=()=>{D.nodes.forEach(n=>{n._placed=false;});build();
 userMoved=false;fitted=false;fit();};
thr.oninput=build;search.oninput=build;
build();
function size(){cv.width=innerWidth;cv.height=innerHeight-cv.offsetTop;}
addEventListener("resize",size);size();
function fit(){
 if(!nodes.length)return;
 let mnx=1e9,mny=1e9,mxx=-1e9,mxy=-1e9;
 nodes.forEach(n=>{mnx=Math.min(mnx,n.x);mxx=Math.max(mxx,n.x);
  mny=Math.min(mny,n.y);mxy=Math.max(mxy,n.y);});
 const w2=Math.max(mxx-mnx,10),h2=Math.max(mxy-mny,10);
 scale=Math.min((cv.width-80)/w2,(cv.height-120)/h2,3);
 ox=-(mnx+mxx)/2;oy=-(mny+mxy)/2;}
// AUTOFIT RUNS ONCE THEN NEVER AGAIN; any wheel or mousedown disables
// it permanently; the fit view button is the only way back.
let userMoved=false,fitted=false;
function autofit(){if(userMoved||fitted)return;fit();fitted=true;}
const _af=setInterval(()=>{autofit();if(fitted||userMoved)
 clearInterval(_af);},400);
addEventListener("wheel",()=>{userMoved=true;},{passive:true});
addEventListener("mousedown",()=>{userMoved=true;});
$("fitbtn").onclick=()=>{fit();};
function sx(x){return cv.width/2+(x+ox)*scale;}
function sy(y){return cv.height/2+(y+oy)*scale;}
function hit(n){return q&&((n.id.toLowerCase().includes(q))||
 (n.label&&n.label.toLowerCase().includes(q))||
 (n.operators.join(" ").toLowerCase().includes(q))||
 (n.holder_pairs.join(" ").toLowerCase().includes(q)));}
function esc(s){return String(s).replace(/&/g,"&amp;")
 .replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function draw(){ctx.clearRect(0,0,cv.width,cv.height);
 edges.forEach(e=>{const a=byId[e[0]],b=byId[e[1]];
  const x1=sx(a.x),y1=sy(a.y),x2=sx(b.x),y2=sy(b.y);
  ctx.strokeStyle=(hoverE===e)?"#fff":"rgba(120,170,220,0.45)";
  ctx.beginPath();ctx.moveTo(x1,y1);ctx.lineTo(x2,y2);ctx.stroke();
  const ang=Math.atan2(y2-y1,x2-x1);
  const mx2=x2-Math.cos(ang)*10,my2=y2-Math.sin(ang)*10;
  ctx.beginPath();ctx.moveTo(mx2,my2);
  ctx.lineTo(mx2-Math.cos(ang-0.4)*8,my2-Math.sin(ang-0.4)*8);
  ctx.lineTo(mx2-Math.cos(ang+0.4)*8,my2-Math.sin(ang+0.4)*8);
  ctx.closePath();ctx.fillStyle=(hoverE===e)?"#fff":
   "rgba(120,170,220,0.45)";ctx.fill();});
 nodes.forEach(n=>{
  const h=hit(n);
  const r=h?8:(n===hover?7:5);
  ctx.beginPath();ctx.arc(sx(n.x),sy(n.y),r,0,6.283);
  ctx.fillStyle=n.languages.length>1?"#b57ee0":
   (n.languages[0]==="rust"?"#e6553f":"#4f9cf0");
  ctx.globalAlpha=q&&!h?0.13:1;ctx.fill();ctx.globalAlpha=1;
  if(scale>0.55||h||n===hover){ctx.font="10px sans-serif";
   ctx.fillStyle="#9aa2ad";
   ctx.fillText(n.label,sx(n.x)+7,sy(n.y)+3);}});
 ctx.font="11px sans-serif";ctx.fillStyle="#7d8590";
 ctx.fillText("red = rust, blue = ruby, violet = cross-language "+
  "contract; arrow: dominator (higher) -> dominated (lower); drawing "+
  "= transitive reduction",10,cv.height-12);}
function pick(mx,my){hover=null;hoverE=null;
 for(const n of nodes){const dx=sx(n.x)-mx,dy=sy(n.y)-my;
  if(dx*dx+dy*dy<80){hover=n;return;}}
 let best=25;
 for(const e of edges){const a=byId[e[0]],b=byId[e[1]];
  const x1=sx(a.x),y1=sy(a.y),x2=sx(b.x),y2=sy(b.y);
  const L2=(x2-x1)**2+(y2-y1)**2;if(!L2)continue;
  let t=((mx-x1)*(x2-x1)+(my-y1)*(y2-y1))/L2;t=Math.max(0,Math.min(1,t));
  const dx=mx-(x1+t*(x2-x1)),dy=my-(y1+t*(y2-y1)),d2=dx*dx+dy*dy;
  if(d2<best){best=d2;hoverE=e;}}}
function mxy(ev){const r=cv.getBoundingClientRect();
 return[ev.clientX-r.left,ev.clientY-r.top];}
function nodeTip(n){
 return "<b>"+esc(n.id)+"</b> &middot; "+esc(n.label)+
  "<br>level "+n.level+" &middot; "+esc(n.form_pair)+
  " &middot; languages "+esc(n.languages.join(", "))+
  "<br>operators "+esc(n.operators.join(", "))+
  "<br>holder pairs "+esc(n.holder_pairs.join(" ; "))+
  "<br>full grid "+n.n_cells+" cells &middot; <b>value "+
  n.n_value_cells+"</b> &middot; declines "+n.n_declines+
  " &middot; UNREPRESENTABLE "+n.n_unrepresentable+
  "<br>member profiles: "+n.n_members;}
function edgeTip(e){const a=byId[e[0]],b=byId[e[1]];
 return "<b>NESTS</b> (reduced connector)<br><b>"+esc(a.id)+"</b> "+
  esc(a.label)+" ("+a.n_value_cells+" value cells)<br>DOMINATES<br><b>"+
  esc(b.id)+"</b> "+esc(b.label)+" ("+b.n_value_cells+" value cells)"+
  "<br>everywhere "+esc(b.id)+" answers a value, "+esc(a.id)+
  " answers the identical value; "+esc(a.id)+" answers at "+
  (a.n_value_cells-b.n_value_cells)+" more cells (over this pair's "+
  "identical full key set)";}
cv.onmousemove=ev=>{const[mx,my]=mxy(ev);
 if(drag){if(drag.node){drag.node.x=(mx-cv.width/2)/scale-ox;
   drag.node.y=(my-cv.height/2)/scale-oy;}
  else{ox+=(mx-drag.px)/scale;oy+=(my-drag.py)/scale;
   drag.px=mx;drag.py=my;}draw();return;}
 pick(mx,my);
 if(hover){tip.style.display="block";tip.innerHTML=nodeTip(hover);}
 else if(hoverE){tip.style.display="block";tip.innerHTML=edgeTip(hoverE);}
 else tip.style.display="none";
 tip.style.left=(ev.clientX+14)+"px";tip.style.top=(ev.clientY+14)+"px";
 draw();};
cv.onmousedown=ev=>{const[mx,my]=mxy(ev);pick(mx,my);
 drag=hover?{node:hover}:{px:mx,py:my};};
addEventListener("mouseup",()=>drag=null);
cv.onwheel=ev=>{ev.preventDefault();
 scale*=ev.deltaY<0?1.1:0.9;scale=Math.max(0.05,Math.min(8,scale));
 draw();};
function loop(){draw();requestAnimationFrame(loop);}
loop();
</script></body></html>
"""


if __name__ == "__main__":
    main()
