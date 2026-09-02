#!/usr/bin/env python3
"""l3_dendro_extended.py -- the THRESHOLD-SPECTRUM visual for the
EXTENDED CLUSTERING MATRIX.  Assembly only; no probe runs.

the owner ruled the design 2026-08-20 (settled, not proposed).  The governing
rule, quoted from
Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/
SUPPORT_conversion_spec.md:

    never compare raw answers, compare their decompositions, and let
    WHICH coordinate disagrees be the feature.

This file reads `matrix_extended.json` (and `matrix_extended_base.csv`
where the base cell is simpler) -- both already on disk, emitted by
`l3_matrix_extended.py` -- and builds ONE merge tree PER COORDINATE
FAMILY.  A column is a `lang.op` signature; a leaf is a column; a family
is a coordinate the decomposition carries.  Similarity is measured
BETWEEN COLUMNS, over the coordinate the family names, never over a raw
answer.

The five coordinate families (the owner, 2026-08-20):

  form       similarity over the 64 base cells (form sets).  REFUSE,
             RAISE and ABORT are first-class answers and compared as
             tokens; UNPROBED is excluded from BOTH sides -- a row where
             either column is UNPROBED is skipped, never counted as a
             disagreement.
  sign       numeric cells only: agreement of the sign coordinate over
             shared input cells.
  mant       numeric cells only: agreement of the exact absolute value
             (the mant coordinate).  A pair linked by a RECORDED
             CONGRUENCE counts as RELATED -- a match with a note --
             never as a disagreement; that is the whole point of the
             congruence layer.
  container  container cells only: agreement of sorted-values, with
             key-format and order-flag agreement folded in as separate
             sub-scores (spec).
  text       text cells only: per-layer agreement over
             bytes / codepoint-length / grapheme-length / normalized.

A column that carries NO cell of a family is ABSENT from that family's
tree -- never forced in at similarity 0.  Per-family leaf counts are
printed and recorded, so which columns each family stands on is on the
record.

CONGRUENCES ARE NOT DISTANCES.  A wrap relation is a typed edge between
two columns on one input cell (`sign flip, mant sum = 2^64
(=== mod 2^64)` and its kin).  It is carried as a CROSS-LINK overlaid on
the tree, never folded into a merge height -- except in the mant family,
where an existing congruence lifts a would-be mismatch to a match with a
note, exactly as the spec asks.

Merge machinery: UPGMA / average linkage, the same method logs 030-038
used (`l3_cluster.py`, `l3_construct_cluster.py`), here with the exact
Lance-Williams running-mean update so the group average never needs
recomputing.  The sweep is the result; no cut is chosen.  Plateaus are
the runs of threshold over which the clustering does not move.

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree only;
the stopped-process outcome element is ABORT.

DECISIONS (each numbered, each overturnable):
  1  form similarity is the MEAN per-row Jaccard of the two form sets
     over the rows both columns probed.  Set equality would be harsher;
     Jaccard credits partial overlap ({whole} vs {whole,fractional}).
  2  sign / mant / container / text similarity is the MEAN per-shared-
     input-cell score; a family leaf is a column with at least one cell
     of that family.  Columns with no shared cell score 0 to each other
     but still stand as their own leaves.
  3  a mant pair whose exact-value sets do not intersect but which a
     recorded congruence links on that input cell scores 1.0 on that
     cell (a match with a note).  This is the only place a congruence
     touches a height.
  4  container fold: 0.6 * sorted-values Jaccard + 0.2 * key-format
     Jaccard + 0.2 * order-flag Jaccard.  The three sub-scores are the
     spec's three container coordinates; the weights are mechanical.
  5  text fold: the mean of four per-layer Jaccards (bytes, codepoint
     length, grapheme length, NFC).  Equal weight; overturnable.
  6  congruence cross-links are aggregated to COLUMN-PAIR grain: the
     representative relation is the one with the largest `w`, carried
     with the count of records and w.  A family draws only the cross-
     links whose BOTH endpoints are leaves of that family.
"""

import csv
import json
import os
import sys
import time
import collections

HERE = os.path.dirname(os.path.abspath(__file__))

NA = "not-applicable"


# --------------------------------------------------------------------
# load
# --------------------------------------------------------------------

def load():
    d = json.load(open(os.path.join(HERE, "matrix_extended.json")))
    base = {}
    with open(os.path.join(HERE, "matrix_extended_base.csv")) as f:
        r = csv.reader(f)
        hdr = next(r)
        cols = hdr[1:]
        for c in cols:
            base[c] = []
        for row in r:
            for c, cell in zip(cols, row[1:]):
                base[c].append(cell)
    return d, base, cols


# --------------------------------------------------------------------
# per-family per-column feature extraction
# --------------------------------------------------------------------

DECLINE = frozenset(("REFUSE", "RAISE", "ABORT"))


def feat_form(base):
    """column -> {row_index: frozenset(VALUE form tokens)}; the owner's
    ruling 2026-08-20: a decline is a 0 whatever its spelling --
    REFUSE, RAISE and ABORT all strip to the empty set, and two
    empty rows AGREE.  UNPROBED rows are omitted (excluded from
    both sides, never a disagreement)."""
    out = {}
    for c, cells in base.items():
        m = {}
        for i, cell in enumerate(cells):
            if cell == "UNPROBED":
                continue
            m[i] = frozenset(cell.split("+")) - DECLINE
        out[c] = m
    return out


def feat_sign(cells, dec):
    out = {}
    for c, cc in cells.items():
        m = {}
        for key, toks in cc.items():
            signs = set()
            for t in toks:
                nm = dec[t]["numeric"]
                if isinstance(nm, dict) and nm.get("sign") != NA \
                        and nm.get("special") == NA:
                    signs.add(nm["sign"])
            if signs:
                m[key] = frozenset(signs)
        if m:
            out[c] = m
    return out


def feat_mant(cells, dec):
    """column -> {key: frozenset(exact absolute value strings)}."""
    out = {}
    for c, cc in cells.items():
        m = {}
        for key, toks in cc.items():
            vals = set()
            for t in toks:
                nm = dec[t]["numeric"]
                if not isinstance(nm, dict) or nm.get("special") != NA:
                    continue
                if nm.get("sign") == 0:
                    vals.add("0")
                elif nm.get("exact") is not None:
                    vals.add(nm["exact"])
            if vals:
                m[key] = frozenset(vals)
        if m:
            out[c] = m
    return out


def feat_container(cells, dec):
    """column -> {key: (fs sorted-values tuples, fs key-formats,
    fs order-flags)}."""
    out = {}
    for c, cc in cells.items():
        m = {}
        for key, toks in cc.items():
            sv, kf, of = set(), set(), set()
            for t in toks:
                cn = dec[t]["container"]
                if not isinstance(cn, dict) or cn.get("sorted_values") == NA:
                    continue
                if isinstance(cn.get("sorted_values"), list):
                    sv.add(tuple(cn["sorted_values"]))
                kf.add(cn.get("key_format"))
                of.add(cn.get("order_flag"))
            if sv or kf or of:
                m[key] = (frozenset(sv), frozenset(kf), frozenset(of))
        if m:
            out[c] = m
    return out


def feat_text(cells, dec):
    """column -> {key: (fs bytes, fs codepoints, fs graphemes, fs nfc)}."""
    out = {}
    for c, cc in cells.items():
        m = {}
        for key, toks in cc.items():
            b, cp, gr, nf = set(), set(), set(), set()
            for t in toks:
                tx = dec[t]["text"]
                if not isinstance(tx, dict):
                    continue
                b.add(tx.get("utf8_bytes"))
                cp.add(tx.get("codepoints"))
                gr.add(tx.get("graphemes"))
                nf.add(tx.get("nfc"))
            if b or cp or gr or nf:
                m[key] = (frozenset(b), frozenset(cp), frozenset(gr),
                          frozenset(nf))
        if m:
            out[c] = m
    return out


# --------------------------------------------------------------------
# per-family pairwise similarity
# --------------------------------------------------------------------

def jac(a, b):
    u = a | b
    return (len(a & b) / len(u)) if u else 0.0


def sim_form(fa, fb):
    shared = fa.keys() & fb.keys()
    if not shared:
        return 0.0
    tot = 0.0
    for k in shared:
        a, b = fa[k], fb[k]
        if not a and not b:
            tot += 1.0                 # both decline: agreement
        elif a and b:
            tot += jac(a, b)
        # one declines, one answers: 0
    return tot / len(shared)


def sim_sign(fa, fb):
    shared = fa.keys() & fb.keys()
    if not shared:
        return 0.0
    return sum(jac(fa[k], fb[k]) for k in shared) / len(shared)


def sim_mant(fa, fb, ca, cb, congr_keys):
    shared = fa.keys() & fb.keys()
    if not shared:
        return 0.0
    linked = congr_keys.get((ca, cb)) or congr_keys.get((cb, ca)) or frozenset()
    tot = 0.0
    for k in shared:
        j = jac(fa[k], fb[k])
        if j == 0.0 and k in linked:
            j = 1.0          # a match with a note (decision 3)
        tot += j
    return tot / len(shared)


def sim_container(fa, fb):
    shared = fa.keys() & fb.keys()
    if not shared:
        return 0.0
    tot = 0.0
    for k in shared:
        sva, kfa, ofa = fa[k]
        svb, kfb, ofb = fb[k]
        tot += 0.6 * jac(sva, svb) + 0.2 * jac(kfa, kfb) + 0.2 * jac(ofa, ofb)
    return tot / len(shared)


def sim_text(fa, fb):
    shared = fa.keys() & fb.keys()
    if not shared:
        return 0.0
    tot = 0.0
    for k in shared:
        a, b = fa[k], fb[k]
        tot += (jac(a[0], b[0]) + jac(a[1], b[1]) + jac(a[2], b[2])
                + jac(a[3], b[3])) / 4.0
    return tot / len(shared)


# --------------------------------------------------------------------
# UPGMA average linkage with the Lance-Williams running mean
# --------------------------------------------------------------------

def upgma(keys, simfn):
    """average linkage all the way to one super-node.  Returns
    (merge_history, sim_dict) -- the history is the sweep read at every
    similarity it passes through."""
    n = len(keys)
    S = {}                               # symmetric similarity, live ids
    for i in range(n):
        for j in range(i + 1, n):
            S[(i, j)] = simfn(keys[i], keys[j])
    live = list(range(n))
    size = {i: 1 for i in range(n)}
    nxt = n
    hist = []

    def get(a, b):
        return S[(a, b)] if a < b else S[(b, a)]

    while len(live) > 1:
        best, ba, bb = None, None, None
        for x in range(len(live)):
            for y in range(x + 1, len(live)):
                a, b = live[x], live[y]
                v = get(a, b)
                if best is None or v > best:
                    best, ba, bb = v, a, b
        na, nb = size[ba], size[bb]
        hist.append(dict(node=nxt, similarity=round(best, 6),
                         left=dict(id=ba, size=na),
                         right=dict(id=bb, size=nb),
                         size=na + nb))
        # Lance-Williams for the mean: new cluster nxt vs every other l
        for l in live:
            if l in (ba, bb):
                continue
            v = (na * get(ba, l) + nb * get(bb, l)) / (na + nb)
            lo, hi = (nxt, l) if nxt < l else (l, nxt)
            S[(lo, hi)] = v
        size[nxt] = na + nb
        live = [l for l in live if l not in (ba, bb)] + [nxt]
        nxt += 1
    return hist


# --------------------------------------------------------------------
# sweep -- cluster count curve and stability plateaus
# --------------------------------------------------------------------

def sweep(n_leaves, hist):
    sims = sorted((h["similarity"] for h in hist), reverse=True)
    rows = []
    for step in range(100, -1, -1):
        t = step / 100.0
        n = n_leaves - sum(1 for s in sims if s >= t)
        rows.append(dict(threshold=round(t, 2), clusters=n))
    plats = []
    run = None
    for r in rows:
        if run and run["clusters"] == r["clusters"]:
            run["low"] = r["threshold"]
            run["width"] = round(run["high"] - run["low"], 6)
        else:
            if run:
                plats.append(run)
            run = dict(clusters=r["clusters"], high=r["threshold"],
                       low=r["threshold"], width=0.0)
    if run:
        plats.append(run)
    plats.sort(key=lambda p: -p["width"])
    return rows, plats, sims


# --------------------------------------------------------------------
# tree -- merge history to an icicle with a leaf order and a band per node
# --------------------------------------------------------------------

def build_tree(keys, hist):
    """A node's BAND is [death, birth]: birth is the similarity it came
    into existence at (1.0 for a leaf), death is its super-node's birth.
    The band width is exactly the cluster's stability under the sweep."""
    node = {}
    for i, k in enumerate(keys):
        lang, _, op = k.partition(".")
        node[i] = dict(id=i, label=k, language=lang, operation=op,
                       birth=1.0, subs=[])
    for m in hist:
        a, b, nn = m["left"]["id"], m["right"]["id"], m["node"]
        node[nn] = dict(id=nn, label=None, language=None, operation=None,
                        birth=m["similarity"], subs=[node[a], node[b]])
    root = node[max(node)]
    order = []

    def walk(r, death):
        r["death"] = death
        if r["label"] is not None:
            r["x0"] = len(order)
            order.append(r["label"])
            r["x1"] = len(order)
            r["counts"] = {r["language"]: 1}
            r["size"] = 1
            return
        for s in r["subs"]:
            walk(s, r["birth"])
        r["x0"] = r["subs"][0]["x0"]
        r["x1"] = r["subs"][-1]["x1"]
        r["size"] = sum(s["size"] for s in r["subs"])
        c = {}
        for s in r["subs"]:
            for k, v in s["counts"].items():
                c[k] = c.get(k, 0) + v
        r["counts"] = c

    walk(root, 0.0)
    flat = []

    def flatten(r):
        flat.append(dict(id=r["id"], label=r["label"], x0=r["x0"], x1=r["x1"],
                         birth=round(r["birth"], 6), death=round(r["death"], 6),
                         size=r["size"], counts=r["counts"],
                         subs=[s["id"] for s in r["subs"]],
                         language=r["language"], operation=r["operation"]))
        for s in r["subs"]:
            flatten(s)

    flatten(root)
    return dict(n_leaves=len(keys), leaf_order=order, nodes=flat,
                root_id=root["id"])


# --------------------------------------------------------------------
# congruence cross-links, aggregated to column-pair grain
# --------------------------------------------------------------------

def build_congr(congruences):
    """(colA, colB) -> dict(relation, w, count).  Also a per-pair set of
    input-cell keys, for the mant match-with-a-note lift."""
    agg = {}
    keyset = {}
    for r in congruences:
        a, b = r["a"], r["b"]
        pair = (a, b) if a <= b else (b, a)
        w = r["w"]
        rec = agg.get(pair)
        if rec is None:
            agg[pair] = dict(a=pair[0], b=pair[1], relation=r["relation"],
                             w=w, count=1)
            keyset[pair] = {r["input_cell"]}
        else:
            rec["count"] += 1
            keyset[pair].add(r["input_cell"])
            if w > rec["w"]:
                rec["w"] = w
                rec["relation"] = r["relation"]
    congr_keys = {pair: frozenset(ks) for pair, ks in keyset.items()}
    return agg, congr_keys


def family_crosslinks(agg, leafset):
    out = []
    for pair, rec in agg.items():
        if pair[0] in leafset and pair[1] in leafset:
            out.append(dict(a=rec["a"], b=rec["b"], relation=rec["relation"],
                            w=rec["w"], count=rec["count"]))
    out.sort(key=lambda r: (-r["w"], -r["count"]))
    return out


# --------------------------------------------------------------------
# one family end to end
# --------------------------------------------------------------------

def do_family(name, feats, simfn):
    keys = sorted(feats)
    t0 = time.time()
    hist = upgma(keys, simfn)
    rows, plats, sims = sweep(len(keys), hist)
    tree = build_tree(keys, hist)
    assert tree["n_leaves"] == len(keys)
    # monotone check: merge heights are non-increasing in merge order
    for x in range(1, len(sims)):
        assert sims[x] <= sims[x - 1] + 1e-9
    print("  [%s] %d leaves, %d merges, %.1fs"
          % (name, len(keys), len(hist), time.time() - t0))
    return dict(name=name, n_leaves=len(keys), leaves=keys,
                merge_history=hist, cluster_count_curve=rows,
                stability_plateaus=plats, tree=tree)


# --------------------------------------------------------------------
def main():
    print("extended dendro spectrum -- assembly over the extended matrix, "
          "no runs")
    d, base, cols = load()
    cells = d["cells"]
    dec = d["token_decompositions"]
    congruences = d["congruences"]
    agg, congr_keys = build_congr(congruences)
    print("  %d columns, %d congruence records -> %d column-pair cross-links"
          % (len(cols), len(congruences), len(agg)))

    fform = feat_form(base)
    fsign = feat_sign(cells, dec)
    fmant = feat_mant(cells, dec)
    fcont = feat_container(cells, dec)
    ftext = feat_text(cells, dec)

    fams = {}
    fams["form"] = do_family("form", fform, lambda a, b: sim_form(fform[a], fform[b]))
    fams["sign"] = do_family("sign", fsign, lambda a, b: sim_sign(fsign[a], fsign[b]))
    fams["mant"] = do_family("mant", fmant,
                             lambda a, b: sim_mant(fmant[a], fmant[b], a, b, congr_keys))
    fams["container"] = do_family("container", fcont,
                                  lambda a, b: sim_container(fcont[a], fcont[b]))
    fams["text"] = do_family("text", ftext, lambda a, b: sim_text(ftext[a], ftext[b]))

    # congruence cross-links per family (both endpoints must be leaves)
    for name, fam in fams.items():
        fam["crosslinks"] = family_crosslinks(agg, set(fam["leaves"]))

    # -------------------------------------------------- sanity checks
    print("SANITY CHECKS")
    for name in ("form", "sign", "mant", "container", "text"):
        print("  [leaves] %-9s %3d leaves" % (name, fams[name]["n_leaves"]))

    def sim_lookup(fam, a, b):
        """the birth similarity of the smallest super-node holding both a
        and b -- the threshold at which they first share a cluster."""
        tree = fam["tree"]
        byid = {n["id"]: n for n in tree["nodes"]}
        pos = {n["label"]: n["x0"] for n in tree["nodes"] if n["label"]}
        if a not in pos or b not in pos:
            return None
        xa, xb = pos[a], pos[b]
        lo, hi = min(xa, xb), max(xa, xb)
        best = None
        for n in tree["nodes"]:
            if n["label"] is None and n["x0"] <= lo and n["x1"] > hi:
                if best is None or n["birth"] > best:
                    best = n["birth"]
        return best

    # [form] go.+ and rust.+ merge early -- pairwise sim and join height
    s_gr = sim_form(fform["go.+"], fform["rust.+"]) if "go.+" in fform and "rust.+" in fform else None
    j_gr = sim_lookup(fams["form"], "go.+", "rust.+")
    print("  [form] go.+ ~ rust.+ pairwise form similarity = %.4f ; "
          "first shared cluster at threshold %.4f"
          % (s_gr, j_gr) if s_gr is not None else "  [form] go.+/rust.+ absent")

    # [mant] go.+ ~ python.+ congruence cross-link exists (mod 2^64)
    ml = fams["mant"]["crosslinks"]
    hit = [c for c in ml
           if {c["a"], c["b"]} == {"go.+", "python.+"}]
    if hit:
        print("  [mant] go.+ ~ python.+ cross-link: %s  (w=%d, %d records)"
              % (hit[0]["relation"], hit[0]["w"], hit[0]["count"]))
    else:
        # look wider in the raw aggregate in case one endpoint lacks numeric cells
        raw = agg.get(("go.+", "python.+")) or agg.get(("python.+", "go.+"))
        print("  [mant] go.+ ~ python.+ cross-link in mant family: NONE "
              "(raw aggregate: %s)" % (raw["relation"] if raw else "none"))

    # [text] concatenation columns cohere
    concat = [c for c in fams["text"]["leaves"] if c.endswith(".+")]
    print("  [text] %d text-family leaves end in '.+' (concatenation): %s"
          % (len(concat), ", ".join(concat[:12])
             + (" ..." if len(concat) > 12 else "")))
    if len(concat) >= 2:
        import itertools
        ss = []
        for a, b in itertools.combinations(concat, 2):
            ss.append(sim_text(ftext[a], ftext[b]))
        ss.sort()
        print("        pairwise text similarity among the '.+' columns: "
              "median %.3f  lowest %.3f  highest %.3f"
              % (ss[len(ss) // 2], ss[0], ss[-1]))
        jt = sim_lookup(fams["text"], concat[0], concat[1])
        print("        %s ~ %s first shared cluster at threshold %.4f"
              % (concat[0], concat[1], jt if jt is not None else float("nan")))

    # widest plateaus per family
    print("WIDEST PLATEAUS (per family, top 3)")
    for name in ("form", "sign", "mant", "container", "text"):
        ps = fams[name]["stability_plateaus"][:3]
        print("  [%s] " % name + " | ".join(
            "%.2f..%.2f w=%.2f %dc" % (p["low"], p["high"], p["width"],
                                       p["clusters"]) for p in ps))

    out = dict(
        status="EXTENDED DENDRO SPECTRUM, ASSEMBLY ONLY",
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        design="one merge tree per coordinate family; shared threshold "
               "slice; congruences as typed cross-links, not distances",
        spec="Planning/node_0_3_research/node_0_3_2_kind_fuzz_clustering/"
             "SUPPORT_conversion_spec.md",
        governing_rule="never compare raw answers, compare their "
                       "decompositions, and let WHICH coordinate "
                       "disagrees be the feature",
        source_matrix="matrix_extended.json",
        vocabulary="super-node / sub-node / co-node / sub-tree; the "
                   "stopped-process outcome element is ABORT",
        family_order=["form", "sign", "mant", "container", "text"],
        families={k: dict(name=v["name"], n_leaves=v["n_leaves"],
                          leaves=v["leaves"], merge_history=v["merge_history"],
                          cluster_count_curve=v["cluster_count_curve"],
                          stability_plateaus=v["stability_plateaus"],
                          tree=v["tree"], crosslinks=v["crosslinks"])
                  for k, v in fams.items()},
    )
    jp = os.path.join(HERE, "dendro_extended.json")
    json.dump(out, open(jp, "w"), separators=(",", ":"), default=str)
    print("  wrote %s (%.2f MB)" % (jp, os.path.getsize(jp) / 1e6))

    # -------------------------------------------------- explorer HTML
    html = HTML_TEMPLATE.replace(
        "__DENDRO__", json.dumps(out, separators=(",", ":"), default=str))
    hp = os.path.join(HERE, "dendrogram_extended.html")
    with open(hp, "w") as f:
        f.write(html)
    print("  wrote %s (%.2f MB)" % (hp, os.path.getsize(hp) / 1e6))
    return out


# --------------------------------------------------------------------
# the explorer -- one self-contained file, inline JS/CSS, no CDN, the
# same interaction grammar as dendrogram_answers.html: icicle of the
# merge tree, draggable threshold slice, live cluster count, search.
# Added: a family toggle and the congruence cross-links as arcs.
# --------------------------------------------------------------------

HTML_TEMPLATE = r"""<!doctype html>
<meta charset="utf-8">
<title>Extended clustering &mdash; threshold spectrum, per coordinate family</title>
<style>
 :root { color-scheme: light dark; }
 body { font: 14px/1.5 ui-sans-serif, system-ui, sans-serif; margin: 0;
        padding: 18px 24px; }
 h1 { font-size: 18px; margin: 0 0 4px; }
 h2 { font-size: 15px; margin: 22px 0 4px; }
 .meta { opacity: .65; margin-bottom: 10px; font-size: 13px; max-width: 60em; }
 #fambar { display: flex; gap: 8px; align-items: center; flex-wrap: wrap;
           margin-bottom: 10px; }
 #bar { display: flex; gap: 14px; align-items: center; flex-wrap: wrap;
        margin-bottom: 8px; }
 input[type=text] { font: inherit; padding: 4px 8px; border-radius: 6px;
         border: 1px solid rgba(128,128,128,.5); background: transparent;
         color: inherit; width: 240px; }
 button { font: inherit; padding: 3px 10px; border-radius: 6px;
          border: 1px solid rgba(128,128,128,.5); background: transparent;
          color: inherit; cursor: pointer; }
 button.fam.on { background: #ff2d78; border-color: #ff2d78; color: #fff;
                 font-weight: 650; }
 .legend { display: flex; gap: 12px; font-size: 12px; align-items: center;
           flex-wrap: wrap; }
 .sw { display: inline-block; width: 11px; height: 11px; border-radius: 2px;
       margin-right: 4px; vertical-align: -1px; }
 #count { font-weight: 650; font-variant-numeric: tabular-nums; }
 #chart, #curve { position: relative; overflow-x: auto; }
 svg { display: block; user-select: none; }
 #tip { position: fixed; pointer-events: none; display: none; max-width: 460px;
        font-size: 12px; line-height: 1.4; background: rgba(30,30,30,.96);
        color: #eee; padding: 8px 10px; border-radius: 6px; z-index: 5; }
 #tip .hd { font-weight: 650; margin-bottom: 3px; }
 .hint { font-size: 12px; opacity: .6; margin-top: 6px; max-width: 62em; }
 table { border-collapse: collapse; font-size: 12px; margin-top: 6px; }
 th, td { border: 1px solid rgba(128,128,128,.35); padding: 2px 8px;
          text-align: left; }
 td.n { text-align: right; font-variant-numeric: tabular-nums; }
 label { font-size: 12px; opacity: .8; }
</style>
<h1>Extended clustering &mdash; threshold spectrum, per coordinate family</h1>
<div class="meta">One merge tree per COORDINATE FAMILY over the 239
 <code>lang.op</code> columns of the extended matrix &middot; a leaf is a
 column, a family is a coordinate the decomposition carries, similarity is
 measured between columns over that coordinate &mdash; never over a raw
 answer &middot; average linkage (UPGMA), and there is NO chosen cut, the
 sweep is the result &middot; CONGRUENCES are typed cross-links (wrap
 relations, <code>=== mod 2^w</code>), NOT distances: they are overlaid as
 arcs and, in the mant family alone, lift a would-be mismatch to a match
 with a note &middot; a column with no cell of a family is ABSENT from its
 tree, not forced in. Vocabulary: super-node / sub-node / co-node /
 sub-tree; the stopped-process outcome element is ABORT.</div>
<div id="fambar"><span style="opacity:.7">coordinate family:</span></div>
<div id="bar">
 <span>threshold <span id="thval">0.700</span> &rarr;
   <span id="count">?</span> clusters (of <span id="nleaf">?</span> leaves)</span>
 <input id="search" type="text" placeholder="search language.operation… (Enter)">
 <button id="reset">reset view</button>
 <label>width <input id="zoom" type="range" min="4" max="40" value="13"
        style="width:120px;vertical-align:-4px"></label>
 <label><input id="links" type="checkbox">
   show congruence cross-links (<span id="nlink">0</span>)</label>
</div>
<div id="bar2" style="margin-bottom:8px">
 <span class="legend" id="legend"></span>
 <span class="legend" style="margin-left:10px">
   <span class="sw" style="background:#8a8a8a"></span>single-language super-node
   <span class="sw" style="background:#b03ad6;margin-left:10px"></span>strong
   language mix
   <span class="sw" style="background:#00d0c0;margin-left:10px"></span>congruence
   cross-link</span>
</div>
<div id="chart"><div id="tip"></div></div>
<div class="hint">Drag the dashed line DOWN for fewer clusters (lower
 similarity) or UP toward singletons. Every rectangle is a cluster and its
 HEIGHT is its stability band &mdash; the range of thresholds over which it
 exists unchanged. <b>Tall blocks are the stable readings.</b> Hover any
 block for its members, or any arc for the wrap relation it carries. Yellow
 outline = a cluster at the current threshold. Cross-links join the two
 columns whose unbounded values wrap into each other on some input cell;
 they are edges, never merge heights (except the mant family's match-with-
 a-note lift).</div>

<h2>Cluster count against threshold &mdash; the sweep itself</h2>
<div id="curve"></div>
<div class="hint">Shaded bands are the stability plateaus: threshold ranges
 over which the clustering does not move at all. A WIDE band is a natural
 reading of the data in a way that a chosen number is not.</div>

<h2>The widest plateaus</h2>
<div id="plateaus"></div>

<script>
const DENDRO = __DENDRO__;
const LANG_COLOR = {"go":"#00ADD8","rust":"#dea584","cpp":"#f34b7d",
 "swift":"#F05138","dart":"#00B4AB","csharp":"#178600","kotlin":"#A97BFF",
 "java":"#b07219","typescript":"#3178c6","python":"#3572A5","ruby":"#701516",
 "php":"#4F5D95"};
const LANGS = Object.keys(LANG_COLOR);
const LINK_CAP = 2000;   // strongest-w cross-links drawn (they are pre-sorted)

// ---- svg helper ------------------------------------------------------
const svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
document.getElementById("chart").appendChild(svg);
const csvg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
document.getElementById("curve").appendChild(csvg);
function SV(tag, at) {
  const e = document.createElementNS("http://www.w3.org/2000/svg", tag);
  for (const k in at) e.setAttribute(k, at[k]);
  return e;
}
function lerp(a, b, t) { return a + (b - a) * t; }
function hex(c) { return "#" + c.map(v => Math.max(0, Math.min(255,
  Math.round(v))).toString(16).padStart(2, "0")).join(""); }
const GRAY = [138,138,138], PURPLE = [176,58,214];
function entropy(counts, total) {
  let e = 0, n = 0;
  for (const k in counts) { n++; const p = counts[k]/total; e -= p*Math.log2(p); }
  return n > 1 ? e/Math.log2(LANGS.length) : 0;
}

// ---- current family state -------------------------------------------
let FAM = null, nodes = null, byId = null, leaves = null, merge_sims = null,
    posOf = null, thr = 0.70, leafW = 13, matches = new Set(), showLinks = false;

function loadFamily(name) {
  FAM = DENDRO.families[name];
  nodes = FAM.tree.nodes;
  byId = new Map(nodes.map(r => [r.id, r]));
  leaves = nodes.filter(r => r.label !== null).sort((a, b) => a.x0 - b.x0);
  merge_sims = FAM.merge_history.map(m => m.similarity).sort((a, b) => b - a);
  posOf = new Map(leaves.map(l => [l.label, l.x0]));
  for (const r of nodes) {
    if (r.label !== null) r.fill = LANG_COLOR[r.language] || "#8a8a8a";
    else {
      const t = Math.min(1, entropy(r.counts, r.size) * 1.6);
      r.fill = hex([lerp(GRAY[0], PURPLE[0], t), lerp(GRAY[1], PURPLE[1], t),
                    lerp(GRAY[2], PURPLE[2], t)]);
    }
  }
  document.getElementById("nleaf").textContent = FAM.n_leaves;
  document.getElementById("nlink").textContent = FAM.crosslinks.length;
  // family buttons
  for (const b of document.querySelectorAll("button.fam"))
    b.classList.toggle("on", b.dataset.fam === name);
  buildLegend();
  setThr(thr);
  drawPlateaus();
}

function membersOf(r, cap) {
  const out = [];
  (function g(n) {
    if (out.length > cap + 1) return;
    if (n.label !== null) { out.push(n.label); return; }
    for (const sid of n.subs) g(byId.get(sid));
  })(r);
  return out;
}

// ---- layout ----------------------------------------------------------
const M = { top: 10, right: 14, bottom: 128, left: 52 };
const H = 620;
let W = 800;
function xs(v) { return M.left + v * leafW; }
function ys(t) { return M.top + (1 - t) * (H - M.top - M.bottom); }
function yinv(py) { return 1 - (py - M.top) / (H - M.top - M.bottom); }

function isCurrent(r) { return r.death < thr && thr <= r.birth; }
function clustersAt(t) {
  let c = 0;
  (function g(r) {
    if (r.birth >= t) { c++; return; }
    for (const sid of r.subs) g(byId.get(sid));
  })(byId.get(FAM.tree.root_id));
  return c;
}
function clustersExact(t) {
  return FAM.n_leaves - merge_sims.filter(s => s >= t).length;
}

function leafBaseY() { return H - M.bottom; }

function draw() {
  while (svg.firstChild) svg.removeChild(svg.firstChild);
  W = M.left + M.right + FAM.n_leaves * leafW;
  svg.setAttribute("width", W); svg.setAttribute("height", H);
  // axis
  const gA = SV("g", {});
  for (let i = 0; i <= 10; i++) {
    const t = i/10, py = ys(t);
    gA.appendChild(SV("line", { x1: M.left-5, x2: W-M.right, y1: py, y2: py,
      stroke: "currentColor", "stroke-opacity": i%5 ? .08 : .2 }));
    const tx = SV("text", { x: M.left-9, y: py+4, "text-anchor": "end",
      "font-size": 11, fill: "currentColor", "fill-opacity": .75 });
    tx.textContent = t.toFixed(1); gA.appendChild(tx);
  }
  const lab = SV("text", { transform: "translate(14,"+(H/2)+") rotate(-90)",
    "text-anchor": "middle", fill: "currentColor", "font-size": 12 });
  lab.textContent = "similarity threshold"; gA.appendChild(lab);
  svg.appendChild(gA);
  // segments
  const g = SV("g", {});
  for (const r of nodes) {
    const y0 = ys(r.birth), y1 = ys(r.death);
    const rect = SV("rect", {
      x: xs(r.x0)+0.25, width: Math.max(0.5, (r.x1-r.x0)*leafW-0.5),
      y: y0, height: Math.max(1, y1-y0), fill: r.fill,
      "fill-opacity": r.birth < thr ? 0.28 : (isCurrent(r) ? 1 : 0.85),
      stroke: matches.has(r.id) ? "#ff2d78" : (isCurrent(r) ? "#ffd400" : "none"),
      "stroke-width": matches.has(r.id) ? 1.5 : (isCurrent(r) ? 1.25 : 0) });
    rect.__d = r;
    g.appendChild(rect);
  }
  svg.appendChild(g);
  // cross-links (arcs) below the icicle, over the leaf axis
  if (showLinks) {
    const gc = SV("g", {});
    const baseY = leafBaseY();
    let drawn = 0;
    for (const lk of FAM.crosslinks) {
      if (drawn >= LINK_CAP) break;
      const xa = posOf.get(lk.a), xb = posOf.get(lk.b);
      if (xa === undefined || xb === undefined) continue;
      const px = xs(xa)+leafW/2, qx = xs(xb)+leafW/2;
      const span = Math.abs(qx - px);
      const dip = Math.min(90, 14 + span*0.18);
      const midx = (px+qx)/2, midy = baseY + dip;
      const hot = matches.size && (matches.has(byId2(lk.a)) || matches.has(byId2(lk.b)));
      const path = SV("path", {
        d: "M"+px+","+baseY+" Q"+midx+","+midy+" "+qx+","+baseY,
        fill: "none", stroke: hot ? "#ff2d78" : "#00d0c0",
        "stroke-width": hot ? 1.6 : Math.max(0.4, Math.min(1.4, lk.w/64)),
        "stroke-opacity": hot ? .95 : .35 });
      path.__L = lk;
      gc.appendChild(path);
      drawn++;
    }
    svg.appendChild(gc);
    if (FAM.crosslinks.length > LINK_CAP) {
      const note = SV("text", { x: M.left, y: baseY + 104, "font-size": 11,
        fill: "#00d0c0" });
      note.textContent = "drawing the " + LINK_CAP + " strongest of "
        + FAM.crosslinks.length + " cross-links (by w)";
      svg.appendChild(note);
    }
  }
  // leaf labels
  if (leafW >= 7) {
    const gl = SV("g", {});
    for (const l of leaves) {
      const t = SV("text", {
        transform: "translate(" + (xs(l.x0)+leafW/2+4) + ","
                   + (H-M.bottom+6+(showLinks?100:0)) + ") rotate(90)",
        "font-size": Math.min(11, leafW-1), fill: "currentColor",
        "fill-opacity": matches.has(l.id) ? 1 : .8,
        "font-weight": matches.has(l.id) ? 700 : 400 });
      t.textContent = l.label;
      gl.appendChild(t);
    }
    svg.appendChild(gl);
  }
  // threshold line
  const py = ys(thr);
  const gt = SV("g", { style: "cursor:ns-resize" });
  gt.appendChild(SV("line", { x1: M.left, x2: W-M.right, y1: py, y2: py,
    stroke: "#ff2d78", "stroke-width": 1.5, "stroke-dasharray": "6 4" }));
  const tag = SV("text", { x: W-M.right-4, y: py-5, "text-anchor": "end",
    "font-size": 12, fill: "#ff2d78", "font-weight": 650 });
  tag.textContent = clustersAt(thr) + " clusters";
  gt.appendChild(tag);
  svg.appendChild(gt);
}
function byId2(label) { const l = leaves.find(x => x.label === label); return l ? l.id : -1; }

function setThr(t) {
  thr = Math.max(0, Math.min(1, t));
  const c = clustersAt(thr), e = clustersExact(thr);
  if (c !== e) console.warn("cluster count mismatch at t="+thr+": walk "
    +c+" vs merge history "+e);
  document.getElementById("thval").textContent = thr.toFixed(3);
  document.getElementById("count").textContent = e;
  draw(); drawCurve();
}

// ---- legend ----------------------------------------------------------
function buildLegend() {
  const present = {};
  for (const l of leaves) present[l.language] = (present[l.language]||0)+1;
  const el = document.getElementById("legend");
  el.innerHTML = Object.keys(present).sort().map(k =>
    "<span><span class='sw' style='background:"+(LANG_COLOR[k]||"#888")
    +"'></span>"+k+" "+present[k]+"</span>").join("");
}

// ---- drag / click on threshold --------------------------------------
let dragging = false;
svg.addEventListener("mousedown", ev => {
  const r = svg.getBoundingClientRect();
  if (Math.abs(ev.clientY - r.top - ys(thr)) < 12) { dragging = true; ev.preventDefault(); }
});
window.addEventListener("mousemove", ev => {
  if (!dragging) return;
  const r = svg.getBoundingClientRect();
  setThr(yinv(ev.clientY - r.top));
});
window.addEventListener("mouseup", () => { dragging = false; });
svg.addEventListener("click", ev => {
  const r = svg.getBoundingClientRect();
  if (ev.shiftKey) setThr(yinv(ev.clientY - r.top));
});

// ---- hover -----------------------------------------------------------
const tip = document.getElementById("tip");
svg.addEventListener("mousemove", ev => {
  const lk = ev.target.__L;
  if (lk) {
    tip.style.display = "block";
    tip.innerHTML = "<div class='hd'>"+lk.a+" &nbsp;~&nbsp; "+lk.b+"</div>"
      + "<b>congruence cross-link</b><br>" + lk.relation
      + "<br>recorded on " + lk.count + " input cell"
      + (lk.count!==1?"s":"") + " &middot; w = " + lk.w
      + "<br><span style='opacity:.7'>a typed relation, not a distance</span>";
    tip.style.left = Math.min(ev.clientX+14, innerWidth-480) + "px";
    tip.style.top = (ev.clientY+12) + "px";
    return;
  }
  const r = ev.target.__d;
  if (!r) { tip.style.display = "none"; return; }
  const CAP = 24;
  const mem = membersOf(r, CAP);
  const shown = mem.slice(0, CAP).join(", ")
    + (mem.length > CAP ? " … ("+r.size+" columns total)" : "");
  const mix = Object.keys(r.counts).sort((a,b) => r.counts[b]-r.counts[a])
    .map(k => k+" "+r.counts[k]).join(" · ");
  tip.style.display = "block";
  tip.innerHTML = "<div class='hd'>"
    + (r.label !== null ? r.label
       : r.size+" columns over "+Object.keys(r.counts).length+" languages")
    + "</div>" + mix + "<br>exists as a cluster for thresholds ("
    + r.death.toFixed(3) + ", " + r.birth.toFixed(3) + "] — stability band "
    + (r.birth-r.death).toFixed(3) + "<br>" + shown;
  tip.style.left = Math.min(ev.clientX+14, innerWidth-480) + "px";
  tip.style.top = (ev.clientY+12) + "px";
});
svg.addEventListener("mouseleave", () => { tip.style.display = "none"; });

// ---- search ----------------------------------------------------------
document.getElementById("search").addEventListener("keydown", ev => {
  if (ev.key !== "Enter") return;
  const q = ev.target.value.trim().toLowerCase();
  matches = new Set();
  if (!q) { draw(); return; }
  const hit = leaves.filter(l => l.label.toLowerCase().includes(q));
  hit.forEach(l => matches.add(l.id));
  draw();
  if (hit.length) document.getElementById("chart").scrollLeft =
    Math.max(0, xs(hit[0].x0) - 300);
});
document.getElementById("reset").addEventListener("click", () => {
  matches = new Set(); document.getElementById("search").value = "";
  leafW = 13; document.getElementById("zoom").value = 13;
  setThr(0.70); document.getElementById("chart").scrollLeft = 0;
});
document.getElementById("zoom").addEventListener("input", ev => {
  leafW = +ev.target.value; draw();
});
document.getElementById("links").addEventListener("change", ev => {
  showLinks = ev.target.checked; draw();
});

// ---- cluster-count curve --------------------------------------------
const CM = { top: 10, right: 16, bottom: 30, left: 46 };
const CH = 220; let CW = 900;
function cx(t) { return CM.left + t*(CW-CM.left-CM.right); }
let cyMax = 1;
function cy(n) { return CH-CM.bottom - (n/cyMax)*(CH-CM.top-CM.bottom); }
function drawCurve() {
  while (csvg.firstChild) csvg.removeChild(csvg.firstChild);
  CW = Math.max(900, document.getElementById("curve").clientWidth || 900);
  csvg.setAttribute("width", CW); csvg.setAttribute("height", CH);
  cyMax = FAM.n_leaves;
  // plateaus
  for (const p of FAM.stability_plateaus) {
    if (p.width < 0.02) continue;
    csvg.appendChild(SV("rect", { x: cx(p.low), width: Math.max(1, cx(p.high)-cx(p.low)),
      y: CM.top, height: CH-CM.top-CM.bottom, fill: "#00d0c0",
      "fill-opacity": Math.min(.28, .05 + p.width) }));
  }
  // axes
  for (let i = 0; i <= 10; i++) {
    const t = i/10;
    csvg.appendChild(SV("line", { x1: cx(t), x2: cx(t), y1: CM.top, y2: CH-CM.bottom,
      stroke: "currentColor", "stroke-opacity": .08 }));
    const tx = SV("text", { x: cx(t), y: CH-CM.bottom+16, "text-anchor": "middle",
      "font-size": 11, fill: "currentColor", "fill-opacity": .7 });
    tx.textContent = t.toFixed(1); csvg.appendChild(tx);
  }
  // curve
  let dpath = "";
  for (const r of FAM.cluster_count_curve) {
    const X = cx(r.threshold), Y = cy(r.clusters);
    dpath += (dpath ? " L" : "M") + X + "," + Y;
  }
  csvg.appendChild(SV("path", { d: dpath, fill: "none", stroke: "#ff2d78",
    "stroke-width": 1.6 }));
  // threshold marker
  csvg.appendChild(SV("line", { x1: cx(thr), x2: cx(thr), y1: CM.top, y2: CH-CM.bottom,
    stroke: "#ff2d78", "stroke-width": 1, "stroke-dasharray": "4 3" }));
}
window.addEventListener("resize", drawCurve);

// ---- plateau table ---------------------------------------------------
function drawPlateaus() {
  const ps = FAM.stability_plateaus.filter(p => p.width >= 0.02).slice(0, 12);
  let h = "<table><tr><th>threshold band</th><th class='n'>width</th>"
        + "<th class='n'>clusters</th></tr>";
  for (const p of ps)
    h += "<tr><td>"+p.low.toFixed(3)+" .. "+p.high.toFixed(3)+"</td>"
       + "<td class='n'>"+p.width.toFixed(3)+"</td>"
       + "<td class='n'>"+p.clusters+"</td></tr>";
  document.getElementById("plateaus").innerHTML = h + "</table>";
}

// ---- family toggle buttons ------------------------------------------
(function () {
  const bar = document.getElementById("fambar");
  for (const name of DENDRO.family_order) {
    const f = DENDRO.families[name];
    const b = document.createElement("button");
    b.className = "fam"; b.dataset.fam = name;
    b.textContent = name + " (" + f.n_leaves + ")";
    b.addEventListener("click", () => loadFamily(name));
    bar.appendChild(b);
  }
})();

loadFamily(DENDRO.family_order[0]);
</script>
"""


if __name__ == "__main__":
    main()
