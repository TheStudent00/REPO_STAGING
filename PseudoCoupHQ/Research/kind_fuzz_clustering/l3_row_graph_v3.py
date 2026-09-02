#!/usr/bin/env python3
"""l3_row_graph_v3.py -- the two-tier row graph over the CARTESIAN rows.

`l3_row_graph.py` (byte identity, log 050) and `l3_row_graph_v2.py`
(rulings A/B/D/E over the interval rows) are left on disk unchanged for
the audit trail.  This is a v3, not an edit: a different probe design
needs a different builder, and the old products stay readable.

SOURCE: `matrices_cart/` -- level 1 `y = op(x0, x1)` over ALL ordered
pairs of a shared set X, and level 2 `z = op(op(x0,x1), op(x2,x3))` over
a subset X'.  Two rows compare position by position IF AND ONLY IF their
(x_set_a, x_set_b) pair and level match; both languages evaluate
identical expressions on identical inputs, so there is no alignment step
anywhere in this file.

BOTH NUMBERS RIDE ON EVERY CONNECTOR.  Neither is chosen for the owner.

  (a) `weight_exact`   exact-match rate: the fraction of COMPARABLE
                       positions where the two output_canon strings are
                       byte-identical.
  (b) `weight_graded`  graded element similarity: the ruling-A
                       per-element numeric comparison already implemented
                       in `l3_row_sim.py` -- sign distance |s0-s1|, mant
                       distance |m0-m1| with mants in [1,2), expo decay
                       1/(1+|d|), combined by euclidean distance from
                       (1,1,1) normalised by sqrt(3) -- averaged over the
                       COMPARABLE positions.

DECLINES ARE NEVER SCORED.  A position where EITHER side is REFUSE,
RAISE:* or ABORT is excluded from the numerator AND the denominator, for
both numbers alike.  Zero comparable positions -> NO connector at all,
not a zero-weight one.

THE EXPLORER'S SIGMOID, recorded here because it is a display rule and
not a measurement.  In graded mode the cut and the spring use

    w(g) = ( s(g) - s(0) ) / ( s(1) - s(0) ),   s(x) = 1/(1+exp(-k(x-m)))

with m the MIDPOINT slider and k the STEEPNESS slider.  As k -> 0 this
tends to w = g exactly, the raw graded score; as k grows it tends to a
step at m, which is the exact-match-style hard cut.  The exact-match
checkbox bypasses it and uses `weight_exact` directly.  No number in the
JSON is ever rewritten by the sliders.

EXPLORER PHYSICS -- preserved from v2, unchanged:
  - internal connector springs near zero (%s against %s external) so they
    never dominate the layout;
  - the threshold cuts EXTERNAL connectors only;
  - components are counted on EXTERNAL connectors ONLY, always;
  - AUTOFIT RUNS ONCE THEN NEVER AGAIN; any wheel or mousedown disables
    it permanently; a "fit view" button exists.

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree; the
OS-stopped outcome is ABORT.
"""

import csv
import hashlib
import json
import math
import os
import sys
import time

import numpy as np

csv.field_size_limit(sys.maxsize)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l3_row_sim as S                                       # noqa: E402

CART = os.path.join(HERE, "matrices_cart")
SEP = ";"
LANGS = ("rust", "ruby")

RENDER_CAP = 10000
INT_SPRING = 0.0008          # ruling D, preserved
EXT_SPRING = 0.0060

__doc__ = __doc__ % (INT_SPRING, EXT_SPRING)


# ------------------------------------------------------------------
# the canon alphabet -- every distinct output string gets one integer
# ------------------------------------------------------------------

class Alphabet(object):
    def __init__(self):
        self.code = {}
        self.text = []
        self.decline = []

    def __call__(self, s):
        c = self.code.get(s)
        if c is None:
            c = len(self.text)
            self.code[s] = c
            self.text.append(s)
            self.decline.append(S.is_decline(s))
        return c


AB = Alphabet()


# ------------------------------------------------------------------
# load
# ------------------------------------------------------------------

def load_rows():
    idx = json.load(open(os.path.join(CART, "index.json")))
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
            codes = np.fromiter((AB(c) for c in cells), dtype=np.int32,
                                count=n)
            rows.append(dict(
                key="%s.%s" % (lang, op), language=lang, operator=op,
                level=level, probe_id=r["probe_id"],
                lhs_holder=r["lhs_holder"], rhs_holder=r["rhs_holder"],
                form_pair=r["form_pair"],
                x_set_a=r["x_set_a"], x_set_b=r["x_set_b"],
                n_probes=n, codes=codes,
                n_values=int(r["n_values"]),
                n_declines=int(r["n_declines"])))
    return rows, idx


def row_id(r):
    return "%s / L%d / %s / %s %s %s" % (
        r["key"], r["level"], r["probe_id"], r["lhs_holder"],
        r["operator"], r["rhs_holder"])


def group_key(r):
    return (r["level"], r["x_set_a"], r["x_set_b"])


def input_key(r):
    h = hashlib.sha1()
    h.update(("L%d\x00%s\x00%s" % (r["level"], r["x_set_a"],
                                   r["x_set_b"])).encode())
    return h.hexdigest()[:16]


# ------------------------------------------------------------------
# the scored pair matrices for one group -- both numbers at once
# ------------------------------------------------------------------

def score_group(members, rows):
    """returns (n_comparable, n_matched_exact, sum_graded) as m x m
    numpy arrays over the group's rows, in group order."""
    m = len(members)
    L = rows[members[0]]["n_probes"]
    M = np.empty((m, L), dtype=np.int32)
    for a, i in enumerate(members):
        M[a] = rows[i]["codes"]
    decl = np.array(AB.decline, dtype=bool)
    D = decl[M]                              # True where the side declined
    n_cmp = np.zeros((m, m), dtype=np.int64)
    n_exa = np.zeros((m, m), dtype=np.int64)
    s_grd = np.zeros((m, m), dtype=np.float64)
    text = AB.text
    for p in range(L):
        valid = ~D[:, p]
        vi = np.nonzero(valid)[0]
        if vi.size < 2:
            continue
        c = M[vi, p]
        u, inv = np.unique(c, return_inverse=True)
        k = u.size
        sm = np.empty((k, k), dtype=np.float64)
        for x in range(k):
            tx = text[u[x]]
            sm[x, x] = 1.0
            for y in range(x + 1, k):
                v = S.sample_sim(tx, text[u[y]])
                sm[x, y] = sm[y, x] = 0.0 if v is None else v
        ix = np.ix_(vi, vi)
        s_grd[ix] += sm[np.ix_(inv, inv)]
        n_exa[ix] += (inv[:, None] == inv[None, :])
        n_cmp[ix] += 1
    return n_cmp, n_exa, s_grd


def components(n, pairs):
    """`root` is the super-node of a merged group; the vocabulary is
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
    groups = {}
    for i in range(n):
        groups.setdefault(find(i), []).append(i)
    return sorted(groups.values(), key=len, reverse=True)


def fmt(x, nd=4):
    return "--" if x is None else ("%.*f" % (nd, x))


def stat(vals):
    if not vals:
        return None
    v = sorted(vals)
    return dict(n=len(v), min=round(v[0], 6), max=round(v[-1], 6),
                mean=round(sum(v) / len(v), 6),
                median=round(v[len(v) // 2], 6))


# ==================================================================

def main():
    print("two-tier ROW agreement graph v3 -- the CARTESIAN design "
          "(2026-08-21).  LEVEL 1 y = op(x0,x1) over all ordered pairs of "
          "X; LEVEL 2 z = op(op(x0,x1), op(x2,x3)) over X'.  BOTH scorings "
          "ride on every connector: (a) exact-match rate, (b) graded "
          "element similarity (ruling A).  Declines are never scored.")
    print("  graded knobs: %s" % json.dumps(S.KNOBS))
    t0 = time.time()
    rows, cart_index = load_rows()
    for r in rows:
        r["id"] = row_id(r)
    ids = [r["id"] for r in rows]
    assert len(set(ids)) == len(ids), "row ids collide"
    keys = sorted({r["key"] for r in rows})
    print("  %d row nodes, %d central nodes, %d distinct canon strings; "
          "by language %s; by level %s  (%.1f s)"
          % (len(rows), len(keys), len(AB.text),
             ", ".join("%s %d" % (l, sum(1 for r in rows
                                         if r["language"] == l))
                       for l in LANGS),
             ", ".join("L%d %d" % (l, sum(1 for r in rows
                                          if r["level"] == l))
                       for l in (1, 2)), time.time() - t0))

    groups = {}
    for i, r in enumerate(rows):
        groups.setdefault(group_key(r), []).append(i)
    print("  %d comparable groups (level + both operand set ids); sizes %s"
          % (len(groups),
             sorted((len(v) for v in groups.values()), reverse=True)[:10]))

    # ------------------------------------------------- score every group
    external = []
    co_scores = {}                # row index -> [(exact, graded), ...]
    universe = same_op = no_comparable = 0
    for gk in sorted(groups, key=lambda k: -len(groups[k])):
        members = groups[gk]
        if len(members) < 2:
            continue
        n_cmp, n_exa, s_grd = score_group(members, rows)
        m = len(members)
        for x in range(m):
            i = members[x]
            ri = rows[i]
            for y in range(x + 1, m):
                j = members[y]
                rj = rows[j]
                universe += 1
                nc = int(n_cmp[x, y])
                if nc == 0:
                    no_comparable += 1
                    continue
                we = round(float(n_exa[x, y]) / nc, 6)
                wg = round(float(s_grd[x, y]) / nc, 6)
                if ri["key"] == rj["key"]:
                    same_op += 1
                    co_scores.setdefault(i, []).append((we, wg))
                    co_scores.setdefault(j, []).append((we, wg))
                    continue
                external.append(dict(
                    kind="external", a=ri["id"], b=rj["id"],
                    level=ri["level"],
                    n_probes=ri["n_probes"], n_comparable=nc,
                    n_excluded_declines=ri["n_probes"] - nc,
                    n_matched_exact=int(n_exa[x, y]),
                    weight_exact=we, weight_graded=wg,
                    cross_language=(ri["language"] != rj["language"])))
        print("      group %-58s %3d rows, %6d positions, %.1f s"
              % ("L%d %s" % (gk[0], gk[1].split(":")[0] + "|"
                             + gk[2].split(":")[0]),
                 m, rows[members[0]]["n_probes"], time.time() - t0))

    print("  comparable universe: %d row pairs share a level and both "
          "operand sets; %d of those are the SAME lang.op (internal "
          "connectors carry those); %d have ZERO comparable positions and "
          "get NO connector; %d external connectors remain  (%.1f s)"
          % (universe, same_op, no_comparable, len(external),
             time.time() - t0))

    # ------------------------------------------------------- INTERNAL
    internal = []
    for i, r in enumerate(rows):
        sc = co_scores.get(i, [])
        if sc:
            internal.append(dict(
                kind="internal", a=r["id"], b=r["key"],
                weight_exact=round(sum(x[0] for x in sc) / len(sc), 6),
                weight_graded=round(sum(x[1] for x in sc) / len(sc), 6),
                n_co_rows_comparable=len(sc), no_comparison=False))
        else:
            internal.append(dict(
                kind="internal", a=r["id"], b=r["key"],
                weight_exact=1.0, weight_graded=1.0,
                n_co_rows_comparable=0, no_comparison=True))
    nnc = sum(1 for e in internal if e["no_comparison"])
    print("  %d internal connectors (one per row node); %d carry "
          "no_comparison -- no co-node of the same lang.op shares their "
          "inputs with a comparable position" % (len(internal), nnc))

    # ---------------------------------------------------------- nodes
    nodes = []
    for key in keys:
        lang, _, op = key.partition(".")
        nodes.append(dict(id=key, kind="central", language=lang,
                          operator=op,
                          n_rows=sum(1 for r in rows if r["key"] == key)))
    for r in rows:
        nodes.append(dict(
            id=r["id"], kind="row", language=r["language"],
            operator=r["operator"], central=r["key"], level=r["level"],
            lhs_holder=r["lhs_holder"], rhs_holder=r["rhs_holder"],
            form_pair=r["form_pair"], x_set_a=r["x_set_a"],
            x_set_b=r["x_set_b"], probe_id=r["probe_id"],
            input_key=input_key(r), n_probes=r["n_probes"],
            n_values=r["n_values"], n_declines=r["n_declines"],
            label="%s %s %s [L%d]" % (r["lhs_holder"], r["operator"],
                                      r["rhs_holder"], r["level"])))
    edges = internal + external
    nid = {n["id"]: i for i, n in enumerate(nodes)}

    # -------------------------------------------------- SANITY numbers
    print("SANITY")
    print("  nodes by kind: %d row, %d central, %d total"
          % (len(rows), len(keys), len(nodes)))
    print("  edges by kind: %d internal, %d external, %d total"
          % (len(internal), len(external), len(edges)))

    sanity_thresholds = {}
    for mode in ("exact", "graded"):
        w = "weight_" + mode
        for t in (0.95, 0.85, 0.70):
            act = [e for e in external if e[w] >= t]
            xl = sum(1 for e in act if e["cross_language"])
            comps = components(len(nodes),
                               [(nid[e["a"]], nid[e["b"]]) for e in act])
            big = comps[0]
            langops = {nodes[i].get("central", nodes[i]["id"]) for i in big}
            multi = [c for c in comps if len(c) > 1]
            rec = dict(external_edges=len(act), cross_language=xl,
                       same_language=len(act) - xl,
                       components_external_only=len(comps),
                       largest_component=len(big),
                       largest_component_langops=sorted(langops),
                       multi_node_components=len(multi),
                       by_level={"L%d" % l: sum(1 for e in act
                                                if e["level"] == l)
                                 for l in (1, 2)})
            sanity_thresholds["%s@%.2f" % (mode, t)] = rec
            print("  %-6s t=%.2f : %d external (%d same-language, %d "
                  "cross-language; L1 %d, L2 %d); components (EXTERNAL "
                  "ONLY) %d (%d multi-node), largest %d nodes spanning %d "
                  "lang.op"
                  % (mode, t, len(act), len(act) - xl, xl,
                     rec["by_level"]["L1"], rec["by_level"]["L2"],
                     len(comps), len(multi), len(big), len(langops)))

    # ----------------------------------------- the named cross-checks
    def key_of(node_id):
        return node_id.partition(" / ")[0]

    def between(ka, kb, level=None):
        return [e for e in external
                if {key_of(e["a"]), key_of(e["b"])} == {ka, kb}
                and (level is None or e["level"] == level)]

    named = {}
    PAIRS = [("ruby.&&", "ruby.||"),
             ("ruby.&&", "ruby.and"),
             ("ruby.||", "ruby.or"),
             ("ruby.and", "ruby.or"),
             ("rust.+", "rust.-"),
             ("rust.+", "ruby.+")]
    for ka, kb in PAIRS:
        rec = {}
        print("  %s ~ %s" % (ka, kb))
        for level in (1, 2):
            sel = between(ka, kb, level)
            if not sel:
                print("      L%d  NO connector" % level)
                rec["L%d" % level] = dict(n_connectors=0)
                continue
            ex = stat([e["weight_exact"] for e in sel])
            gr = stat([e["weight_graded"] for e in sel])
            rec["L%d" % level] = dict(
                n_connectors=len(sel), exact=ex, graded=gr,
                n_comparable_mean=round(
                    sum(e["n_comparable"] for e in sel) / len(sel), 2),
                n_excluded_mean=round(
                    sum(e["n_excluded_declines"] for e in sel) / len(sel), 2))
            print("      L%d  %4d connectors | exact  max %s mean %s min %s"
                  " | graded max %s mean %s min %s | n_comparable mean "
                  "%.1f, excluded mean %.1f"
                  % (level, len(sel), fmt(ex["max"]), fmt(ex["mean"]),
                     fmt(ex["min"]), fmt(gr["max"]), fmt(gr["mean"]),
                     fmt(gr["min"]), rec["L%d" % level]["n_comparable_mean"],
                     rec["L%d" % level]["n_excluded_mean"]))
        named["%s ~ %s" % (ka, kb)] = rec

    # ------------------------- the boolean composition check, truth rows
    truth_check = {}
    print("  BOOLEAN COMPOSITION CHECK -- truth-form rows only, "
          "`and` against `or`")
    for level in (1, 2):
        sel = [e for e in between("ruby.and", "ruby.or", level)]
        tr = []
        byid_rows = {r["id"]: r for r in rows}
        for e in sel:
            ra, rb = byid_rows[e["a"]], byid_rows[e["b"]]
            if ra["form_pair"] == "truth|truth" == rb["form_pair"]:
                tr.append(e)
        if not tr:
            print("      L%d  no truth|truth connector" % level)
            truth_check["L%d" % level] = dict(n_connectors=0)
            continue
        ex = stat([e["weight_exact"] for e in tr])
        gr = stat([e["weight_graded"] for e in tr])
        truth_check["L%d" % level] = dict(
            n_connectors=len(tr), exact=ex, graded=gr,
            predicted_agreement="2/16 = 0.1250 (the owner's truth-table "
                                "prediction for the composed form)",
            n_comparable_mean=round(
                sum(e["n_comparable"] for e in tr) / len(tr), 2))
        print("      L%d  %d truth|truth connectors | exact-match "
              "agreement mean %s (max %s, min %s) | graded mean %s | "
              "prediction 2/16 = 0.1250"
              % (level, len(tr), fmt(ex["mean"]), fmt(ex["max"]),
                 fmt(ex["min"]), fmt(gr["mean"])))

    # ------------------- sample positions: && returns which operand?
    projection = sample_projection(rows, cart_index)

    # ------------------------------------------------------------ emit
    out = dict(
        status="TWO-TIER ROW AGREEMENT GRAPH v3 -- the CARTESIAN probe "
               "design settled 2026-08-21.  ROW NODES plus lang.op CENTRAL "
               "NODES, INTERNAL and EXTERNAL connectors.  BOTH scorings "
               "ride on every connector and neither is chosen for the owner.",
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        scope="rust (static) + ruby (route C) only; the other ten wait",
        source="matrices_cart/ -- level 1 y = op(x0,x1) over all ordered "
               "pairs of X, level 2 z = op(op(x0,x1), op(x2,x3)) over X'",
        scoring_a="EXACT-MATCH RATE: the fraction of COMPARABLE positions "
                  "where the two output_canon strings are byte-identical.",
        scoring_b="GRADED ELEMENT SIMILARITY: the ruling-A per-element "
                  "numeric comparison of l3_row_sim.py -- sign distance "
                  "|s0-s1| in {0,2} -> 1 - d/2; mant distance |m0-m1| with "
                  "mants in [1,2) -> 1 - d clamped at 0; expo distance "
                  "through the decay 1/(1+|d|); combined by euclidean "
                  "distance from (1,1,1) normalised by sqrt(3) -- averaged "
                  "over the COMPARABLE positions.",
        declines="NEVER SCORED.  A position where either side is REFUSE, "
                 "RAISE:* or ABORT is excluded from the numerator AND the "
                 "denominator, for both numbers alike.  Zero comparable "
                 "positions -> no connector at all.",
        comparability="two rows compare position by position if and only "
                      "if their level and both operand set ids match.  "
                      "Both languages evaluate identical expressions on "
                      "identical inputs, so there is no alignment step.",
        sigmoid_rule="graded mode maps g through w = (s(g)-s(0))/(s(1)-s(0))"
                     " with s(x) = 1/(1+exp(-k(x-m))), m the MIDPOINT "
                     "slider and k the STEEPNESS slider.  k -> 0 gives "
                     "w = g exactly (the raw graded score); large k gives "
                     "a step at m, which is the exact-match-style hard "
                     "cut.  It is a DISPLAY rule: no stored number is "
                     "rewritten.",
        physics="internal springs near zero (%g against %g external) so "
                "they never dominate the layout; the threshold cuts "
                "EXTERNAL connectors only; components are counted on "
                "EXTERNAL connectors ONLY; autofit runs ONCE then never "
                "again and any wheel or mousedown disables it permanently; "
                "a fit view button exists."
                % (INT_SPRING, EXT_SPRING),
        scoring_knobs=S.KNOBS,
        int_spring=INT_SPRING, ext_spring=EXT_SPRING,
        render_cap=RENDER_CAP,
        render_rule="the explorer draws at most %d external connectors, "
                    "highest weight first under the ACTIVE scoring, and "
                    "says so on screen" % RENDER_CAP,
        vocabulary="super-node / sub-node / co-node / sub-tree; the "
                   "OS-stopped outcome is ABORT",
        x_sets=cart_index["x_sets"],
        lane_timing=cart_index["lane_timing"],
        absent_values_per_row_family=cart_index[
            "absent_values_per_row_family"],
        ruby_stall_budget_s=cart_index["ruby_stall_budget_s"],
        ruby_stall_budget_note=cart_index["ruby_stall_budget_note"],
        n_comparable_groups=len(groups),
        n_row_nodes=len(rows), n_central_nodes=len(keys),
        n_internal_edges=len(internal), n_external_edges=len(external),
        comparable_universe=universe,
        comparable_same_operator=same_op,
        comparable_no_position=no_comparable,
        n_no_comparison=nnc,
        sanity=dict(thresholds=sanity_thresholds, named=named,
                    boolean_composition=truth_check,
                    ruby_projection_samples=projection),
        nodes=nodes, edges=edges)

    jp = os.path.join(HERE, "row_graph_v3.json")
    json.dump(out, open(jp, "w"), separators=(",", ":"))
    print("  wrote %s (%.2f MB)" % (jp, os.path.getsize(jp) / 1e6))

    html = HTML_TEMPLATE.replace("__GRAPH__",
                                 json.dumps(out, separators=(",", ":")))
    hp = os.path.join(HERE, "row_graph_explorer_v3.html")
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
    seen = {}
    for e in back["edges"]:
        if e["kind"] == "internal":
            seen[e["a"]] = seen.get(e["a"], 0) + 1
    rowids = {n["id"] for n in back["nodes"] if n["kind"] == "row"}
    assert set(seen) == rowids and all(v == 1 for v in seen.values())
    print("  [internal] exactly one internal connector per row node, %d "
          "of them" % len(seen))
    byid = {n["id"]: n for n in back["nodes"]}
    for e in back["edges"]:
        if e["kind"] != "external":
            continue
        a, b = byid[e["a"]], byid[e["b"]]
        assert a["kind"] == b["kind"] == "row"
        assert a["central"] != b["central"], "external inside one lang.op"
        assert a["level"] == b["level"]
        assert (a["x_set_a"], a["x_set_b"]) == (b["x_set_a"], b["x_set_b"])
        assert e["n_comparable"] > 0
        assert e["n_comparable"] + e["n_excluded_declines"] == e["n_probes"]
        assert e["n_matched_exact"] <= e["n_comparable"]
    print("  [external] every external connector joins two row nodes of "
          "DIFFERENT lang.op at the SAME level carrying IDENTICAL operand "
          "sets; n_comparable > 0 and n_comparable + n_excluded_declines "
          "== n_probes on every one")
    txt = open(hp).read()
    assert '"nodes"' in txt and '"edges"' in txt and "__GRAPH__" not in txt
    assert "<script src" not in txt
    print("  [html] embedded data present, placeholder gone, no external "
          "scripts, no CDN")
    print("  done in %.1f s" % (time.time() - t0))


# ------------------------------------------------------------------
# `&&` returns the RIGHT operand, `||` the LEFT -- shown, not asserted
# ------------------------------------------------------------------

def sample_projection(rows, cart_index):
    """A handful of level-1 truth positions with the operands spelled out
    beside what each operator answered, so the projection is visible."""
    want = {("ruby", "&&"), ("ruby", "||"), ("ruby", "and"),
            ("ruby", "or")}
    sets = cart_index["x_sets"]
    out = {}
    for r in rows:
        if (r["language"], r["operator"]) not in want:
            continue
        if r["level"] != 1 or r["form_pair"] != "truth|truth":
            continue
        sa, sb = sets[r["x_set_a"]], sets[r["x_set_b"]]
        na, nb = sa["n"], sb["n"]
        samples = []
        for p in range(r["n_probes"]):
            i0, i1 = divmod(p, nb)
            samples.append(dict(
                position=p,
                x0=sa["spellings"][i0], x1=sb["spellings"][i1],
                x0_canon=sa["canon"][i0], x1_canon=sb["canon"][i1],
                answer_canon=AB.text[int(r["codes"][p])]))
        out["ruby.%s" % r["operator"]] = dict(
            row=r["id"], n_probes=r["n_probes"], positions=samples)
        want.discard((r["language"], r["operator"]))
        if not want:
            break
    # the reading, stated from the data rather than assumed
    if "ruby.&&" in out and "ruby.||" in out:
        aa = out["ruby.&&"]["positions"]
        oo = out["ruby.||"]["positions"]
        right = sum(1 for s in aa if s["answer_canon"] == s["x1_canon"])
        left = sum(1 for s in oo if s["answer_canon"] == s["x0_canon"])
        out["reading"] = dict(
            n_positions=len(aa),
            and_answers_equal_the_RIGHT_operand=right,
            or_answers_equal_the_LEFT_operand=left,
            note="ruby's `&&`/`||`/`and`/`or` RETURN AN OPERAND rather "
                 "than a truth value, so they are projections.  Only "
                 "distinct non-boolean operands in X reveal that, which "
                 "is why X for truth carries 0, 1, \"\" and nil beside "
                 "true and false.")
        print("  RUBY PROJECTION (level 1, truth|truth, %d positions): "
              "`&&` answers the RIGHT operand at %d of %d positions; "
              "`||` answers the LEFT operand at %d of %d"
              % (len(aa), right, len(aa), left, len(oo)))
        for s in aa[:6]:
            o = oo[s["position"]]
            print("      x0=%-5s x1=%-5s   && -> %-12s   || -> %s"
                  % (s["x0"], s["x1"], s["answer_canon"],
                     o["answer_canon"]))
    return out


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Cartesian run &mdash; two-tier row graph v3</title>
<style>
 body{margin:0;font:13px/1.4 system-ui,sans-serif;background:#14161a;
      color:#d7dae0;display:flex;flex-direction:column;height:100vh}
 #bar{padding:7px 12px;background:#1d2026;display:flex;
      gap:14px;align-items:center;flex-wrap:wrap;
      border-bottom:1px solid #2b2f36}
 #bar b{color:#fff}
 input[type=range]{width:150px;vertical-align:middle}
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
      display:none;max-width:500px;z-index:9;font-size:12px}
 label{cursor:pointer;white-space:nowrap}
 .dim{opacity:.4}
</style></head><body>
<div id="bar">
 <b>Cartesian run &mdash; row graph v3</b>
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
 <label><input type="checkbox" id="fadeint"> fade internal by
  weight</label>
 <span>level <select id="lmode">
  <option value="all">both levels</option>
  <option value="1">level 1 only</option>
  <option value="2">level 2 only</option></select></span>
 <span>colour <select id="cmode">
  <option value="lang">by language</option>
  <option value="op">by operator</option>
  <option value="level">by level</option>
  <option value="form">by form pair</option></select></span>
 <span>draw cap <select id="cap">
  <option value="1000">1000</option>
  <option value="2000">2000</option>
  <option value="4000">4000</option>
  <option value="10000" selected>10000</option>
  <option value="1000000">no cap</option></select></span>
 <input id="search" placeholder="search node / operator / holder">
 <button id="fitbtn">fit view</button>
 <span id="stats"></span>
</div>
<div id="rule"></div>
<canvas id="cv"></canvas><div id="tip"></div>
<script>
const G=__GRAPH__;
const N=G.nodes,E=G.edges;
const idx={};N.forEach((n,i)=>{idx[n.id]=i;});
E.forEach(e=>{e.ai=idx[e.a];e.bi=idx[e.b];});
const INT=E.filter(e=>e.kind==="internal");
const EXT=E.filter(e=>e.kind==="external").map((e,i)=>(e._o=i,e));
const intOf={};INT.forEach(e=>{intOf[e.a]=e;});
const PAL=["#e6553f","#4f9cf0","#58c26a","#e0b83e","#b57ee0","#3ec8c0",
 "#e07ab0","#98a832","#f08b3e","#7a8cf0","#50b08a","#c0625a",
 "#d0a05a","#6fb0e0","#9ad04a","#e05a8a","#5ad0b0","#a07ae0",
 "#e09a4a","#4ac0a0","#c05a9a","#8ab04a","#d05a5a","#5a90d0"];
const langs=[...new Set(N.map(n=>n.language))].sort();
const ops=[...new Set(N.map(n=>n.operator))].sort();
const levels=["1","2"];
const forms=[...new Set(N.filter(n=>n.kind==="row").map(n=>n.form_pair))]
 .sort();
const lcolor={};langs.forEach((l,i)=>lcolor[l]=PAL[i%PAL.length]);
const ocolor={};ops.forEach((o,i)=>ocolor[o]=PAL[i%PAL.length]);
const vcolor={"1":"#4f9cf0","2":"#e6553f"};
const fcolor={};forms.forEach((f,i)=>fcolor[f]=PAL[(i*7)%PAL.length]);
const $=s=>document.getElementById(s);
const cv=$("cv"),ctx=cv.getContext("2d"),tip=$("tip"),thr=$("thr"),
 thrv=$("thrv"),mid=$("mid"),midv=$("midv"),stp=$("stp"),stpv=$("stpv"),
 exact=$("exact"),showint=$("showint"),fadeint=$("fadeint"),
 cmode=$("cmode"),lmode=$("lmode"),cap=$("cap"),search=$("search"),
 stats=$("stats"),rule=$("rule"),sigwrap=$("sigwrap");
const NROW=N.filter(n=>n.kind==="row").length,
      NCEN=N.filter(n=>n.kind==="central").length;
// seed the layout: central nodes on a wide ring, each row node beside its
// own central node -- the sub-tree starts where it belongs
const cpos={};let ci=0;
N.forEach(n=>{if(n.kind==="central"){
 const t=6.283*ci/NCEN;ci++;
 n.x=Math.cos(t)*1300;n.y=Math.sin(t)*1300;cpos[n.id]=[n.x,n.y];}});
let rk={};
N.forEach(n=>{if(n.kind==="row"){
 const c=cpos[n.central]||[0,0];const k=(rk[n.central]=(rk[n.central]||0)+1);
 const t=6.283*k/26;
 n.x=c[0]+Math.cos(t)*(90+4*k);n.y=c[1]+Math.sin(t)*(90+4*k);}});
N.forEach(n=>{n.vx=0;n.vy=0;});
let T=0.85,EX=false,MID=0.5,K=0,SI=true,FI=false,CM="lang",LM="all",
 CAP=10000,q="",act=[],actInt=[],hover=null,hoverE=null,drag=null;
let ox=0,oy=0,scale=1,heat=1;
// the SIGMOID -- a DISPLAY rule.  w(g)=(s(g)-s(0))/(s(1)-s(0)),
// s(x)=1/(1+exp(-K(x-MID))).  K=0 gives w=g exactly (the raw graded
// score); large K gives a step at MID, which is the exact-match-style
// hard cut.  No stored number is ever rewritten.
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
 if(CM==="level")return n.kind==="central"?"#ffffff":vcolor[String(n.level)];
 if(CM==="form")return n.kind==="central"?"#ffffff":fcolor[n.form_pair];
 return lcolor[n.language];}
function refresh(){
 T=thr.value/100;thrv.textContent=T.toFixed(2);
 EX=exact.checked;MID=mid.value/100;K=stp.value/10;
 midv.textContent=MID.toFixed(2);stpv.textContent=K.toFixed(1);
 sigwrap.className=EX?"dim":"";
 SI=showint.checked;FI=fadeint.checked;CM=cmode.value;LM=lmode.value;
 CAP=+cap.value;q=search.value.trim().toLowerCase();
 EXT.forEach(e=>{e._w=W(e);});
 // the threshold cuts EXTERNAL connectors ONLY; internal connectors are
 // structure and are never cut by it
 const pass=EXT.filter(e=>e._w>=T&&vok(N[e.ai])&&vok(N[e.bi]))
  .sort((p,r)=>(r._w-p._w)||(p._o-r._o));
 const capped=pass.length>CAP;
 act=capped?pass.slice(0,CAP):pass;
 actInt=SI?INT.filter(e=>vok(N[e.ai])):[];
 // components are counted on EXTERNAL connectors ONLY, whether or not
 // internal connectors are drawn
 const p=N.map((_,i)=>i);
 const f=x=>{while(p[x]!=x){p[x]=p[p[x]];x=p[x];}return x;};
 act.forEach(e=>{const a=f(e.ai),b=f(e.bi);if(a!=b)p[a]=b;});
 const comps=new Set(N.map((_,i)=>f(i))).size;
 let multi=0;{const c={};N.forEach((_,i)=>{const r=f(i);c[r]=(c[r]||0)+1;});
  multi=Object.values(c).filter(v=>v>1).length;}
 const xl=act.filter(e=>e.cross_language).length;
 stats.textContent=NROW+" row | "+NCEN+" central | "+act.length+
  " external ("+xl+" cross-language) | "+actInt.length+" internal | "+
  comps+" components ("+multi+" multi-node)";
 rule.textContent="RULE: cut and weight use "+
  (EX?"the EXACT-MATCH RATE -- the fraction of COMPARABLE positions whose "+
      "output_canon strings are byte-identical. The sigmoid is inactive."
    :("the GRADED element similarity (ruling A: sign, mant, expo through "+
      "the documented decay, combined euclidean) averaged over the "+
      "COMPARABLE positions, mapped through the sigmoid midpoint "+
      MID.toFixed(2)+" steepness "+K.toFixed(1)+
      (K<=0?" -- steepness 0 IS the raw graded score":
       " -- raise steepness to approach the exact-match style hard cut")))+
  " Declines are never scored: a position where either side is REFUSE / "+
  "RAISE:* / ABORT is out of numerator and denominator both, and two rows "+
  "with no comparable position have no connector at all. The threshold "+
  "cuts EXTERNAL connectors only; internal springs are near zero ("+
  G.int_spring+" against "+G.ext_spring+"); COMPONENTS ARE COUNTED ON "+
  "EXTERNAL CONNECTORS ONLY. "+(capped
   ?("DRAW CAP IN FORCE: "+pass.length+" clear "+T.toFixed(2)+
     ", the top "+CAP+" BY WEIGHT are drawn, "+(pass.length-CAP)+
     " are not.")
   :("all "+pass.length+" external connectors clearing "+T.toFixed(2)+
     " are drawn (cap "+(CAP>=1e6?"off":CAP)+")."));
 heat=Math.max(heat,0.25);}
[thr,mid,stp].forEach(e=>e.oninput=refresh);
[exact,showint,fadeint,cmode,lmode,cap].forEach(e=>e.onchange=refresh);
search.oninput=refresh;
refresh();
function size(){cv.width=innerWidth;cv.height=innerHeight-cv.offsetTop;}
addEventListener("resize",size);size();
// ---- physics unchanged from v2: clamped linear springs, velocity clamp,
// gravity, hard boundary, grid repulsion, near-zero internal spring
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
  // near-zero internal spring -- a visual tether, not a force that
  // decides the layout
  actInt.forEach(e=>{const a=N[e.ai],b=N[e.bi];
   let dx=b.x-a.x,dy=b.y-a.y,d=Math.sqrt(dx*dx+dy*dy);if(d<1)d=1;
   const f=Math.min((d-70)*INT_K,6);
   a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f;});
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
   if(r>2600){n.x*=2600/r;n.y*=2600/r;}}); // hard boundary
  heat*=0.992;}
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
 (n.label&&n.label.toLowerCase().includes(q)));}
function draw(){ctx.clearRect(0,0,cv.width,cv.height);
 ctx.lineWidth=1;
 if(actInt.length){ctx.setLineDash([3,3]);
  actInt.forEach(e=>{const w=EX?e.weight_exact:e.weight_graded;
   const al=FI?(0.05+0.25*w):0.16;
   ctx.strokeStyle=e===hoverE?"#fff":"rgba(224,184,62,"+al+")";
   ctx.beginPath();ctx.moveTo(sx(N[e.ai].x),sy(N[e.ai].y));
   ctx.lineTo(sx(N[e.bi].x),sy(N[e.bi].y));ctx.stroke();});
  ctx.setLineDash([]);}
 act.forEach(e=>{ctx.strokeStyle=e===hoverE?"#fff":
  "rgba(120,170,220,"+(0.07+0.45*(e._w-T)/(1.001-T))+")";
  ctx.beginPath();ctx.moveTo(sx(N[e.ai].x),sy(N[e.ai].y));
  ctx.lineTo(sx(N[e.bi].x),sy(N[e.bi].y));ctx.stroke();});
 N.forEach(n=>{if(!vok(n))return;const h=hit(n),cen=n.kind==="central";
  const r=cen?(h?13:11):(h?6:(n===hover?5:3));
  ctx.beginPath();ctx.arc(sx(n.x),sy(n.y),r,0,6.283);
  ctx.fillStyle=color(n);ctx.globalAlpha=q&&!h?0.13:1;
  ctx.fill();
  if(cen){ctx.strokeStyle="#fff";ctx.lineWidth=2;ctx.stroke();
   ctx.lineWidth=1;}
  ctx.globalAlpha=1;});
 ctx.font="12px sans-serif";
 N.forEach(n=>{if(n.kind!=="central")return;
  ctx.fillStyle="#fff";ctx.fillText(n.id,sx(n.x)+13,sy(n.y)+4);});
 if(scale>1.1||q){ctx.font="10px sans-serif";ctx.fillStyle="#9aa2ad";
  N.forEach(n=>{if(n.kind!=="row"||!vok(n))return;
   if(q&&!hit(n))return;
   ctx.fillText(n.label,sx(n.x)+5,sy(n.y)+3);});}
 if(hover&&hover.kind==="row"){ctx.font="11px sans-serif";
  ctx.fillStyle="#fff";ctx.fillText(hover.label,sx(hover.x)+7,
   sy(hover.y)-6);}
 let lx=10,ly=cv.height-12;ctx.font="11px sans-serif";
 const keys=CM==="op"?ops:(CM==="level"?levels:(CM==="form"?forms:langs)),
       tab=CM==="op"?ocolor:(CM==="level"?vcolor:(CM==="form"?fcolor
        :lcolor));
 keys.forEach(l=>{ctx.fillStyle=tab[l];ctx.fillRect(lx,ly-8,8,8);
  ctx.fillStyle="#9aa2ad";
  ctx.fillText(CM==="level"?("level "+l):l,lx+11,ly);
  lx+=20+ctx.measureText(CM==="level"?("level "+l):l).width;});
 ctx.fillStyle="#7d8590";
 ctx.fillText("solid = external (carries the layout)   dashed = internal"+
  " (near-zero spring, a visual tether only)",10,ly-18);
 ctx.font="13px sans-serif";}
function pick(mx,my){hover=null;hoverE=null;
 for(const n of N){if(!vok(n))continue;
  const dx=sx(n.x)-mx,dy=sy(n.y)-my;
  const rr=n.kind==="central"?200:60;
  if(dx*dx+dy*dy<rr){hover=n;return;}}
 let best=25;
 const scan=act.concat(actInt);
 for(const e of scan){const x1=sx(N[e.ai].x),y1=sy(N[e.ai].y),
  x2=sx(N[e.bi].x),y2=sy(N[e.bi].y);
  const L2=(x2-x1)**2+(y2-y1)**2;if(!L2)continue;
  let t=((mx-x1)*(x2-x1)+(my-y1)*(y2-y1))/L2;t=Math.max(0,Math.min(1,t));
  const dx=mx-(x1+t*(x2-x1)),dy=my-(y1+t*(y2-y1)),d2=dx*dx+dy*dy;
  if(d2<best){best=d2;hoverE=e;}}}
function mxy(ev){const r=cv.getBoundingClientRect();
 return[ev.clientX-r.left,ev.clientY-r.top];}
function f4(x){return x==null?"&mdash;":(+x).toFixed(4);}
function esc(s){return String(s).replace(/&/g,"&amp;")
 .replace(/</g,"&lt;").replace(/>/g,"&gt;");}
function nodeTip(n){
 if(n.kind==="central")
  return "<b>"+esc(n.id)+"</b><br>CENTRAL node &middot; language "+
   esc(n.language)+" &middot; operator "+esc(n.operator)+
   "<br>rows on this operator: "+n.n_rows;
 const ie=intOf[n.id];
 return "<b>"+esc(n.id)+"</b><br>ROW node &middot; language "+
  esc(n.language)+" &middot; operator "+esc(n.operator)+
  " &middot; <b>level "+n.level+"</b>"+
  "<br>lhs_holder "+esc(n.lhs_holder)+" &middot; rhs_holder "+
  esc(n.rhs_holder)+" &middot; form "+esc(n.form_pair)+
  "<br>x_set_a "+esc(n.x_set_a)+"<br>x_set_b "+esc(n.x_set_b)+
  "<br>probe "+esc(n.probe_id)+" &middot; input_key "+esc(n.input_key)+
  "<br>n_probes "+n.n_probes+" &middot; n_values "+n.n_values+
  " &middot; n_declines "+n.n_declines+
  "<br>central "+esc(n.central)+
  (ie?("<br>internal exact "+f4(ie.weight_exact)+" &middot; graded "+
   f4(ie.weight_graded)+
   (ie.no_comparison?" (no co-node with a comparable position &mdash; 1.0 "+
    "by convention)":(" over "+ie.n_co_rows_comparable+" co-node"+
     (ie.n_co_rows_comparable==1?"":"s")))):"");}
function edgeTip(e){
 if(e.kind==="internal")
  return "<b>INTERNAL connector</b><br>"+esc(e.a)+"<br>&rarr; "+
   esc(e.b)+"<br>exact-match "+f4(e.weight_exact)+
   " &middot; graded "+f4(e.weight_graded)+
   (e.no_comparison?" (no co-node with a comparable position &mdash; 1.0 "+
    "by convention)":(" &middot; over "+e.n_co_rows_comparable+
     " co-node"+(e.n_co_rows_comparable==1?"":"s")))+
   "<br>structure, not similarity: never cut by the threshold, and its "+
   "spring is near zero so it does not decide the layout";
 return "<b>EXTERNAL connector</b><br>"+esc(e.a)+"<br>&harr; "+
  esc(e.b)+"<br><b>exact-match "+f4(e.weight_exact)+"</b> ("+
  e.n_matched_exact+"/"+e.n_comparable+" comparable positions "+
  "byte-identical)"+
  "<br><b>graded "+f4(e.weight_graded)+"</b> (ruling A per-element "+
  "similarity, mean over the comparable positions)"+
  "<br>active weight after the sigmoid: <b>"+f4(e._w)+"</b>"+
  "<br>level "+e.level+" &middot; n_probes "+e.n_probes+
  " &middot; n_comparable "+e.n_comparable+
  " &middot; n_excluded_declines "+e.n_excluded_declines+
  "<br>"+(e.cross_language?"CROSS-language":"same-language")+
  " &middot; identical operand sets, position for position";}
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


if __name__ == "__main__":
    main()
