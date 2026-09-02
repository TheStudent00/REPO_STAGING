#!/usr/bin/env python3
"""l3_row_graph_v2.py -- the two-tier row graph REBUILT under the owner's
rulings A, B, D and E (2026-08-21), over ALL interval rows: the log-049
diagonal rows PLUS the ruling-C shifted and composed rows.

`l3_row_graph.py` (byte-identity weights, diagonal rows only) is kept on
disk unchanged for the audit trail.  This is a v2, not an edit.

  RULING A  similarity is PER ELEMENT and NUMERIC, with a FORM
            CLASSIFIER rather than cast-and-catch.  Implemented in
            `l3_row_sim.py`; the knobs are constants there.
  RULING B  declines are not scored at all.  A sample position where
            EITHER row's output is REFUSE / RAISE:* / ABORT is excluded
            from numerator AND denominator.  Two rows that share an
            input ladder but have ZERO comparable positions get NO
            connector -- not a zero-weight one.  Every connector records
            n_comparable, n_excluded_declines, weight; the old
            byte-identity number rides along as `weight_byte`,
            SECONDARY.
  RULING C  the shifted and composed rows are ordinary interval rows
            here.  Nothing in the scoring knows about the variants; they
            differ only in their input vectors and their interval_id.
  RULING D  explorer physics.  Internal connectors must NOT dominate the
            layout: their spring strength is near zero (INT_SPRING),
            they exist to tether a row to its lang.op central node
            visually and for nothing else.  EXTERNAL connectors carry
            the layout.  COMPONENT COUNTING IS EXTERNAL-ONLY, always,
            whether or not internal connectors are drawn.  The clamped
            springs, velocity clamp, gravity, hard boundary and autofit
            are kept unchanged -- they do not explode.
  RULING E  the internal connector weight is rescored under A/B like
            everything else.

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree; the
OS-stopped outcome is ABORT.
"""

import csv
import hashlib
import json
import os
import sys
import time

csv.field_size_limit(sys.maxsize)

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import l3_row_sim as S                                     # noqa: E402

IV_DIRS = [os.path.join(HERE, "matrices_interval"),
           os.path.join(HERE, "matrices_interval_c")]
SEP = ";"
LANGS = ("rust", "ruby")

RENDER_CAP = 10000            # external connectors drawn, top by weight

# ruling D -- the internal spring is near zero; external carries layout
INT_SPRING = 0.0008
EXT_SPRING = 0.0060


def variant_of(interval_id):
    tail = interval_id.rsplit(":", 1)[-1]
    return tail if tail in ("shift", "comp1") else "diagonal"


# ------------------------------------------------------------------
# load -- the row is the unit and it is never split
# ------------------------------------------------------------------

def load_rows():
    rows = []
    for d in IV_DIRS:
        idx = json.load(open(os.path.join(d, "index.json")))
        for key in sorted(idx["matrices"]):
            meta = idx["matrices"][key]
            lang, _, op = key.partition(".")
            if lang not in LANGS:
                continue
            for r in csv.DictReader(open(os.path.join(d, meta["file"]))):
                n = int(r["n_samples"])
                lv = r["lhs_canon_vector"]
                rv = r["rhs_canon_vector"]
                ov = tuple(r["output_canon_vector"].split(SEP))
                assert len(lv.split(SEP)) == n, (key, r["probe_id"], "lhs")
                assert len(rv.split(SEP)) == n, (key, r["probe_id"], "rhs")
                assert len(ov) == n, (key, r["probe_id"], "out")
                rows.append(dict(
                    key=key, language=lang, operator=op,
                    probe_id=r["probe_id"], lhs_holder=r["lhs_holder"],
                    rhs_holder=r["rhs_holder"],
                    interval_id=r["interval_id"],
                    variant=variant_of(r["interval_id"]),
                    n_samples=n, lhs_vec=lv, rhs_vec=rv, out=ov,
                    n_values=int(r["n_values"]),
                    n_declines=int(r["n_declines"]),
                    source=os.path.basename(d)))
    return rows


def row_id(r):
    return "%s / %s / %s %s %s / %s" % (
        r["key"], r["probe_id"], r["lhs_holder"], r["operator"],
        r["rhs_holder"], r["interval_id"])


def input_key(r):
    h = hashlib.sha1()
    h.update(r["lhs_vec"].encode())
    h.update(b"\x00")
    h.update(r["rhs_vec"].encode())
    return h.hexdigest()[:16]


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


# ------------------------------------------------------------------

def main():
    print("two-tier ROW agreement graph v2 -- rulings A (per-element "
          "numeric similarity, form classifier), B (declines not scored "
          "at all), D (internal springs near zero, components counted on "
          "external only), E (internal weight rescored).  All interval "
          "rows: diagonal + shifted + composed.")
    print("  scoring knobs: %s" % json.dumps(S.KNOBS))
    t0 = time.time()
    rows = load_rows()
    for r in rows:
        r["id"] = row_id(r)
    ids = [r["id"] for r in rows]
    assert len(set(ids)) == len(ids), "row ids collide"
    keys = sorted({r["key"] for r in rows})
    byvar = {}
    for r in rows:
        byvar.setdefault(r["variant"], []).append(r)
    print("  %d row nodes, %d central nodes; by language %s; by variant %s"
          " (%.2f s)"
          % (len(rows), len(keys),
             ", ".join("%s %d" % (l, sum(1 for r in rows
                                         if r["language"] == l))
                       for l in LANGS),
             ", ".join("%s %d" % (v, len(byvar[v]))
                       for v in sorted(byvar)), time.time() - t0))

    # ------------------------------------------------- input grouping
    groups = {}
    for i, r in enumerate(rows):
        groups.setdefault((r["lhs_vec"], r["rhs_vec"]), []).append(i)
    print("  %d distinct input ladder pairs; group sizes %s"
          % (len(groups),
             sorted((len(v) for v in groups.values()), reverse=True)[:8]))

    # --------------------------------------------------- INTERNAL (E)
    for members in groups.values():
        by_op = {}
        for i in members:
            by_op.setdefault(rows[i]["key"], []).append(i)
        for mem in by_op.values():
            for i in mem:
                rows[i]["_co"] = [j for j in mem if j != i]
    internal = []
    for r in rows:
        co = r.get("_co", [])
        recs = [S.row_sim(r["out"], rows[j]["out"]) for j in co]
        recs = [x for x in recs if x is not None]
        if recs:
            w = sum(x["weight"] for x in recs) / len(recs)
            internal.append(dict(
                kind="internal", a=r["id"], b=r["key"],
                weight=round(w, 6), n_co_rows=len(co),
                n_co_rows_comparable=len(recs),
                n_comparable=sum(x["n_comparable"] for x in recs),
                n_excluded_declines=sum(x["n_excluded_declines"]
                                        for x in recs),
                weight_byte=round(sum(x["weight_byte"] for x in recs)
                                  / len(recs), 6),
                no_comparison=False))
        else:
            internal.append(dict(
                kind="internal", a=r["id"], b=r["key"], weight=1.0,
                n_co_rows=len(co), n_co_rows_comparable=0,
                n_comparable=0, n_excluded_declines=r["n_samples"] * len(co),
                weight_byte=1.0, no_comparison=True))
    nnc = sum(1 for e in internal if e["no_comparison"])
    print("  %d internal connectors (one per row node); %d carry "
          "no_comparison -- either no co-row shares their inputs or every "
          "shared position is a decline (ruling B)" % (len(internal), nnc))

    # --------------------------------------------------- EXTERNAL (A/B)
    external = []
    universe = same_op = no_comparable = 0
    for members in groups.values():
        for x in range(len(members)):
            i = members[x]
            ri = rows[i]
            for y in range(x + 1, len(members)):
                j = members[y]
                rj = rows[j]
                universe += 1
                if ri["key"] == rj["key"]:
                    same_op += 1
                    continue          # that is what internal connectors do
                rec = S.row_sim(ri["out"], rj["out"])
                if rec is None:
                    # ruling B: zero comparable positions -> NO connector
                    no_comparable += 1
                    continue
                external.append(dict(
                    kind="external", a=ri["id"], b=rj["id"],
                    n_samples=rec["n_samples"],
                    n_comparable=rec["n_comparable"],
                    n_excluded_declines=rec["n_excluded_declines"],
                    weight=rec["weight"],
                    n_matched_byte=rec["n_matched_byte"],
                    weight_byte=rec["weight_byte"],
                    variant=(ri["variant"] if ri["variant"] == rj["variant"]
                             else "%s/%s" % (ri["variant"], rj["variant"])),
                    cross_language=(ri["language"] != rj["language"])))
    print("  comparable universe: %d row pairs share an identical input "
          "ladder pair; %d of those are the SAME operator (internal "
          "connectors carry those); %d cross-operator pairs have ZERO "
          "comparable positions after ruling B and get NO connector; "
          "%d external connectors remain (%.1f s)"
          % (universe, same_op, no_comparable, len(external),
             time.time() - t0))

    # ------------------------------------------------------- nodes
    nodes = []
    for key in keys:
        lang, _, op = key.partition(".")
        nodes.append(dict(id=key, kind="central", language=lang,
                          operator=op,
                          n_rows=sum(1 for r in rows if r["key"] == key)))
    for r in rows:
        nodes.append(dict(
            id=r["id"], kind="row", language=r["language"],
            operator=r["operator"], central=r["key"],
            lhs_holder=r["lhs_holder"], rhs_holder=r["rhs_holder"],
            interval_id=r["interval_id"], variant=r["variant"],
            probe_id=r["probe_id"], input_key=input_key(r),
            n_samples=r["n_samples"], n_values=r["n_values"],
            n_declines=r["n_declines"],
            label="%s %s %s [%s]" % (r["lhs_holder"], r["operator"],
                                     r["rhs_holder"], r["variant"])))
    edges = internal + external
    nid = {n["id"]: i for i, n in enumerate(nodes)}

    # ------------------------------------------------ SANITY numbers
    print("SANITY")
    print("  nodes by kind: %d row, %d central, %d total"
          % (len(rows), len(keys), len(nodes)))
    print("  edges by kind: %d internal, %d external, %d total"
          % (len(internal), len(external), len(edges)))
    dist = dict(exactly_0=sum(1 for e in external if e["weight"] == 0.0),
                exactly_1=sum(1 for e in external if e["weight"] == 1.0),
                between=sum(1 for e in external if 0.0 < e["weight"] < 1.0))
    print("  external weight distribution: %d at exactly 0.0, %d at "
          "exactly 1.0, %d strictly between"
          % (dist["exactly_0"], dist["exactly_1"], dist["between"]))

    sanity_thresholds = {}
    for t in (1.0, 0.95, 0.85, 0.70):
        act = [e for e in external if e["weight"] >= t]
        xl = sum(1 for e in act if e["cross_language"])
        # ruling D: components are counted on EXTERNAL connectors only
        comps = components(len(nodes),
                           [(nid[e["a"]], nid[e["b"]]) for e in act])
        big = comps[0]
        langops = {nodes[i].get("central", nodes[i]["id"]) for i in big}
        multi = [c for c in comps if len(c) > 1]
        sanity_thresholds["%.2f" % t] = dict(
            external_edges=len(act), cross_language=xl,
            same_language=len(act) - xl,
            components_external_only=len(comps),
            largest_component=len(big),
            largest_component_langops=sorted(langops),
            largest_mixes_operators=(len(langops) > 1),
            multi_node_components=len(multi),
            by_variant={v: sum(1 for e in act if e["variant"] == v)
                        for v in sorted({e["variant"] for e in external})})
        print("  t=%.2f : %d external connectors (%d same-language, %d "
              "cross-language); components (EXTERNAL ONLY) %d (%d "
              "multi-node), largest %d nodes spanning %d lang.op %s"
              % (t, len(act), len(act) - xl, xl, len(comps), len(multi),
                 len(big), len(langops),
                 "(MIXES OPERATORS)" if len(langops) > 1
                 else "(one operator only)"))
        print("        by variant: %s"
              % ", ".join("%s %d" % (k, v) for k, v in
                          sorted(sanity_thresholds["%.2f" % t]
                                 ["by_variant"].items())))

    # ---------------------------------------- the named cross-checks
    def key_of(node_id):
        return node_id.partition(" / ")[0]

    def between(ka, kb):
        return [e for e in external
                if {key_of(e["a"]), key_of(e["b"])} == {ka, kb}]

    named = {}
    for ka, kb, before in (("rust.+", "ruby.+", "0.9062 byte-identity "
                            "max on 13 row pairs (log 050 s4.1)"),
                           ("rust.+", "rust.-", "0.0312 byte-identity on "
                            "6 row pairs (log 050 s4.2)"),
                           ("ruby.<=>", "rust.-", "1.0000 byte-identity "
                            "on 13 row pairs (log 050 s4.3)")):
        sel = between(ka, kb)
        rec = dict(before=before, n_connectors=len(sel), by_variant={})
        print("  %s ~ %s   (before: %s)" % (ka, kb, before))
        if not sel:
            print("      NO connector: no row pair shares an identical "
                  "input ladder with a comparable position")
            named["%s ~ %s" % (ka, kb)] = rec
            continue
        for v in sorted({e["variant"] for e in sel}):
            sv = [e for e in sel if e["variant"] == v]
            ws = sorted((e["weight"] for e in sv), reverse=True)
            wb = sorted((e["weight_byte"] for e in sv), reverse=True)
            rec["by_variant"][v] = dict(
                n_connectors=len(sv), max=ws[0], min=ws[-1],
                mean=round(sum(ws) / len(ws), 6),
                byte_max=wb[0], byte_mean=round(sum(wb) / len(wb), 6),
                n_comparable_mean=round(
                    sum(e["n_comparable"] for e in sv) / len(sv), 3),
                n_excluded_mean=round(
                    sum(e["n_excluded_declines"] for e in sv) / len(sv), 3),
                examples=[dict(a=e["a"], b=e["b"], weight=e["weight"],
                               n_comparable=e["n_comparable"],
                               n_excluded_declines=e["n_excluded_declines"],
                               weight_byte=e["weight_byte"])
                          for e in sorted(sv, key=lambda e: -e["weight"])[:3]])
            print("      %-16s %3d connectors  weight max %s mean %s min %s"
                  "  | n_comparable mean %.1f, excluded mean %.1f  | old "
                  "byte-identity max %s mean %s"
                  % (v, len(sv), fmt(ws[0]), fmt(sum(ws) / len(ws)),
                     fmt(ws[-1]),
                     rec["by_variant"][v]["n_comparable_mean"],
                     rec["by_variant"][v]["n_excluded_mean"],
                     fmt(wb[0]), fmt(sum(wb) / len(wb))))
        named["%s ~ %s" % (ka, kb)] = rec

    # ---------------------------- the retired all-decline ruby cluster
    DECL_OPS = {"ruby.&", "ruby.|", "ruby.^", "ruby.<<", "ruby.>>",
                "ruby.=~"}
    FRAC_H = {"Float", "Rational", "BigDecimal"}
    WHOLE_H = {"Integer", "Rational", "BigDecimal"}
    rowbyid = {r["id"]: r for r in rows}

    def in_family(rid, holders):
        r = rowbyid.get(rid)
        return (r is not None and r["key"] in DECL_OPS
                and r["lhs_holder"] in holders and r["rhs_holder"] in holders)

    def count_family(holders):
        emitted = sum(1 for e in external
                      if in_family(e["a"], holders)
                      and in_family(e["b"], holders))
        # what the OLD byte-identity rule would have produced over the
        # same comparable universe, for the before/after
        old = 0
        for members in groups.values():
            for x in range(len(members)):
                i = members[x]
                for y in range(x + 1, len(members)):
                    j = members[y]
                    if rows[i]["key"] == rows[j]["key"]:
                        continue
                    if (in_family(rows[i]["id"], holders)
                            and in_family(rows[j]["id"], holders)):
                        old += 1
        return emitted, old

    decl_report = {}
    for label, holders in (("Float/Rational/BigDecimal", FRAC_H),
                           ("Integer/Rational/BigDecimal", WHOLE_H)):
        emitted, old = count_family(holders)
        decl_report[label] = dict(connectors_now=emitted,
                                  comparable_pairs_before=old)
        print("  all-decline ruby family (%s on %s): %d comparable "
              "cross-operator row pairs under the OLD byte-identity rule, "
              "%d connectors under rulings A/B%s"
              % (", ".join(sorted(DECL_OPS)), label, old, emitted,
                 "  -- GONE" if emitted == 0 else "  -- NOT GONE"))

    # ------------------------------------------------------ emit
    out = dict(
        status="TWO-TIER ROW AGREEMENT GRAPH v2 -- INTERVAL PILOT (rust "
               "+ ruby).  ROW NODES PLUS lang.op CENTRAL NODES, INTERNAL "
               "AND EXTERNAL CONNECTORS.  Scored under the owner's ruling A "
               "(per-element NUMERIC similarity with a FORM CLASSIFIER) "
               "and ruling B (declines are not scored at all).  Carries "
               "ALL interval rows: the log-049 diagonal rows plus the "
               "ruling-C shifted and composed rows.",
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        pilot="rust (static) + ruby (route C) only; the other ten wait",
        source="matrices_interval/ + matrices_interval_c/ -- interval "
               "rows, numeric forms only",
        ruling_a="similarity is PER ELEMENT and NUMERIC.  sign distance "
                 "|s0-s1| in {0,2} -> sign_sim = 1 - d/2; mant distance "
                 "|m0-m1|, already bounded by 1 because mants live in "
                 "[1,2) -> mant_sim = 1 - d clamped at 0; expo distance "
                 "|e0-e1| through the documented decay 1/(1+d).  The "
                 "three combine by EUCLIDEAN distance from the perfect "
                 "point (1,1,1), normalised by sqrt(3).  Every knob is a "
                 "single constant in l3_row_sim.py.  A FORM CLASSIFIER, "
                 "not cast-and-catch: numeric `[`, text `t|`, container "
                 "`c|`, truth true/false, opaque `opaque:`, or an "
                 "outcome token.  Same form -> that form's rule; "
                 "different form -> 0.",
        ruling_b="declines are NOT SCORED AT ALL.  A sample position "
                 "where either row's output is REFUSE / RAISE:* / ABORT "
                 "is excluded from the numerator AND the denominator.  "
                 "Two rows sharing an input ladder with zero comparable "
                 "positions get NO connector, not a zero-weight one.  "
                 "Every connector records n_comparable, "
                 "n_excluded_declines and weight; weight_byte is the old "
                 "byte-identity number kept as a SECONDARY record.",
        ruling_c="the shifted (`:shift`) and composed (`:comp1`) rows "
                 "are ordinary interval rows here; the scoring does not "
                 "know about the variants.  The diagonal rows are "
                 "unchanged and still present.",
        ruling_d="explorer physics: internal connectors have a NEAR-ZERO "
                 "spring (%g against %g for external) -- they tether a "
                 "row to its lang.op central node visually and do "
                 "nothing else.  EXTERNAL connectors carry the layout.  "
                 "COMPONENTS ARE COUNTED ON EXTERNAL CONNECTORS ONLY, "
                 "whether or not internal connectors are drawn.  The "
                 "clamped springs, velocity clamp, gravity, hard "
                 "boundary and periodic autofit are unchanged."
                 % (INT_SPRING, EXT_SPRING),
        ruling_e="the internal connector weight is rescored under A/B "
                 "like everything else: the mean ruling-A/B similarity "
                 "with the co-rows of the same operator sharing this "
                 "row's inputs, over the co-rows that have at least one "
                 "comparable position.  None comparable -> 1.0 by "
                 "convention and no_comparison: true.",
        scoring_knobs=S.KNOBS,
        int_spring=INT_SPRING, ext_spring=EXT_SPRING,
        render_rule="the explorer draws at most %d external connectors, "
                    "highest weight first, and says so on screen"
                    % RENDER_CAP,
        render_cap=RENDER_CAP,
        vocabulary="super-node / sub-node / co-node / sub-tree; the "
                   "OS-stopped outcome is ABORT",
        n_input_ladder_pairs=len(groups),
        n_row_nodes=len(rows), n_central_nodes=len(keys),
        n_internal_edges=len(internal), n_external_edges=len(external),
        rows_by_variant={k: len(v) for k, v in sorted(byvar.items())},
        comparable_universe=universe,
        comparable_same_operator=same_op,
        comparable_no_position_after_ruling_b=no_comparable,
        n_no_comparison=nnc,
        weight_distribution=dist,
        sanity=dict(thresholds=sanity_thresholds, named=named,
                    all_decline_ruby_family=dict(
                        operators=sorted(DECL_OPS), by_holders=decl_report)),
        nodes=nodes, edges=edges)

    jp = os.path.join(HERE, "row_graph_v2.json")
    json.dump(out, open(jp, "w"), separators=(",", ":"))
    print("  wrote %s (%.2f MB)" % (jp, os.path.getsize(jp) / 1e6))

    html = HTML_TEMPLATE.replace("__GRAPH__",
                                 json.dumps(out, separators=(",", ":")))
    hp = os.path.join(HERE, "row_graph_explorer_v2.html")
    with open(hp, "w") as f:
        f.write(html)
    print("  wrote %s (%.2f MB)" % (hp, os.path.getsize(hp) / 1e6))

    # ------------------------------------------- python-side verify
    print("PYTHON VERIFY")
    back = json.load(open(jp))
    assert len(back["nodes"]) == len(nodes)
    assert len(back["edges"]) == len(edges)
    print("  [json] well-formed; %d nodes, %d connectors consistent"
          % (len(back["nodes"]), len(back["edges"])))
    idset = {n["id"] for n in back["nodes"]}
    assert all(e["a"] in idset and e["b"] in idset for e in back["edges"])
    assert all(0.0 <= e["weight"] <= 1.0 for e in back["edges"])
    print("  [refs] every connector endpoint is a node; every weight in "
          "[0,1]")
    seen = {}
    for e in back["edges"]:
        if e["kind"] == "internal":
            seen[e["a"]] = seen.get(e["a"], 0) + 1
    rowids = {n["id"] for n in back["nodes"] if n["kind"] == "row"}
    assert set(seen) == rowids and all(v == 1 for v in seen.values())
    print("  [internal] exactly one internal connector per row node, %d "
          "of them" % len(seen))
    byid = {n["id"]: n for n in back["nodes"]}
    vec = {r["id"]: (r["lhs_vec"], r["rhs_vec"]) for r in rows}
    for e in back["edges"]:
        if e["kind"] != "external":
            continue
        a, b = byid[e["a"]], byid[e["b"]]
        assert a["kind"] == b["kind"] == "row"
        assert a["central"] != b["central"], "external inside one operator"
        assert vec[e["a"]] == vec[e["b"]], "external across ladders"
        assert e["n_comparable"] > 0, "ruling B: zero-comparable emitted"
        assert (e["n_comparable"] + e["n_excluded_declines"]
                == e["n_samples"])
    print("  [external] every external connector joins two row nodes of "
          "DIFFERENT operators carrying identical input ladders, and "
          "every one has n_comparable > 0 with n_comparable + "
          "n_excluded_declines == n_samples (ruling B)")
    kg = {}
    for n in back["nodes"]:
        if n["kind"] == "row":
            kg.setdefault(n["input_key"], set()).add(n["id"])
    assert len(kg) == len(groups), "input_key collides or over-splits"
    print("  [input_key] the %d digests partition the row nodes exactly "
          "as the raw input vectors do" % len(kg))
    want = 0
    outv = {r["id"]: r["out"] for r in rows}
    for v in kg.values():
        v = sorted(v)
        for x in range(len(v)):
            for y in range(x + 1, len(v)):
                if byid[v[x]]["central"] == byid[v[y]]["central"]:
                    continue
                if S.row_sim(outv[v[x]], outv[v[y]]) is not None:
                    want += 1
    assert want == len(external), (want, len(external))
    print("  [completeness] %d cross-operator row pairs share a digest "
          "AND have a comparable position; %d external connectors exist "
          "-- none missing, none invented" % (want, len(external)))
    txt = open(hp).read()
    assert '"nodes"' in txt and '"edges"' in txt and "__GRAPH__" not in txt
    assert "<script src" not in txt
    print("  [html] embedded data present, placeholder gone, no external "
          "scripts, no CDN")
    print("  done in %.1f s" % (time.time() - t0))


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Interval pilot &mdash; two-tier row graph v2 (rulings A/B/D)</title>
<style>
 body{margin:0;font:13px/1.4 system-ui,sans-serif;background:#14161a;
      color:#d7dae0;display:flex;flex-direction:column;height:100vh}
 #bar{padding:7px 12px;background:#1d2026;display:flex;
      gap:14px;align-items:center;flex-wrap:wrap;
      border-bottom:1px solid #2b2f36}
 #bar b{color:#fff}
 input[type=range]{width:180px;vertical-align:middle}
 #search{background:#14161a;border:1px solid #3a3f48;color:#d7dae0;
         padding:3px 7px;border-radius:4px;width:190px}
 select{background:#14161a;border:1px solid #3a3f48;color:#d7dae0;
        padding:2px 5px;border-radius:4px}
 #stats{color:#9aa2ad}
 #rule{color:#7d8590;font-size:11px;padding:3px 12px;background:#191c21;
       border-bottom:1px solid #2b2f36}
 canvas{flex:1;display:block}
 #tip{position:fixed;pointer-events:none;background:#22262d;
      border:1px solid #3a3f48;border-radius:5px;padding:6px 9px;
      display:none;max-width:470px;z-index:9;font-size:12px}
 label{cursor:pointer;white-space:nowrap}
</style></head><body>
<div id="bar">
 <b>Interval pilot &mdash; row graph v2</b>
 <span>external threshold
  <input type="range" id="thr" min="0" max="100" value="85">
  <span id="thrv">0.85</span></span>
 <label><input type="checkbox" id="showint" checked> internal
  connectors</label>
 <label><input type="checkbox" id="fadeint"> fade internal by
  weight</label>
 <span>variant <select id="vmode">
  <option value="all">all rows</option>
  <option value="diagonal">diagonal only</option>
  <option value="shift">shifted only</option>
  <option value="comp1">composed only</option></select></span>
 <span>colour <select id="cmode">
  <option value="lang">by language</option>
  <option value="op">by operator</option>
  <option value="variant">by variant</option></select></span>
 <span>draw cap <select id="cap">
  <option value="1000">1000</option>
  <option value="2000">2000</option>
  <option value="4000">4000</option>
  <option value="10000" selected>10000</option>
  <option value="1000000">no cap</option></select></span>
 <input id="search" placeholder="search node / operator / holder">
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
// EXTERNAL connectors are held in ONE fixed order -- highest weight
// first, ties broken by original position -- so "top N by weight" is a
// deterministic rule, reproducible outside the page.
const EXT=E.filter(e=>e.kind==="external")
 .map((e,i)=>(e._o=i,e))
 .sort((p,q)=>(q.weight-p.weight)||(p._o-q._o));
const intOf={};INT.forEach(e=>{intOf[e.a]=e;});
const PAL=["#e6553f","#4f9cf0","#58c26a","#e0b83e","#b57ee0","#3ec8c0",
 "#e07ab0","#98a832","#f08b3e","#7a8cf0","#50b08a","#c0625a",
 "#d0a05a","#6fb0e0","#9ad04a","#e05a8a","#5ad0b0","#a07ae0",
 "#e09a4a","#4ac0a0","#c05a9a","#8ab04a"];
const langs=[...new Set(N.map(n=>n.language))].sort();
const ops=[...new Set(N.map(n=>n.operator))].sort();
const vars=[...new Set(N.filter(n=>n.kind==="row").map(n=>n.variant))].sort();
const lcolor={};langs.forEach((l,i)=>lcolor[l]=PAL[i%PAL.length]);
const ocolor={};ops.forEach((o,i)=>ocolor[o]=PAL[i%PAL.length]);
const vcolor={};vars.forEach((v,i)=>vcolor[v]=PAL[(i*5)%PAL.length]);
const cv=document.getElementById("cv"),ctx=cv.getContext("2d"),
 tip=document.getElementById("tip"),thr=document.getElementById("thr"),
 thrv=document.getElementById("thrv"),
 showint=document.getElementById("showint"),
 fadeint=document.getElementById("fadeint"),
 cmode=document.getElementById("cmode"),vmode=document.getElementById("vmode"),
 cap=document.getElementById("cap"),
 search=document.getElementById("search"),
 stats=document.getElementById("stats"),rule=document.getElementById("rule");
const NROW=N.filter(n=>n.kind==="row").length,
      NCEN=N.filter(n=>n.kind==="central").length;
// seed the layout: central nodes on a wide ring, each row node beside
// its own central node -- the sub-tree starts where it belongs
const cpos={};let ci=0;
N.forEach(n=>{if(n.kind==="central"){
 const t=6.283*ci/NCEN;ci++;
 n.x=Math.cos(t)*1200;n.y=Math.sin(t)*1200;cpos[n.id]=[n.x,n.y];}});
let rk={};
N.forEach(n=>{if(n.kind==="row"){
 const c=cpos[n.central]||[0,0];const k=(rk[n.central]=(rk[n.central]||0)+1);
 const t=6.283*k/26;
 n.x=c[0]+Math.cos(t)*(90+5*k);n.y=c[1]+Math.sin(t)*(90+5*k);}});
N.forEach(n=>{n.vx=0;n.vy=0;});
let T=0.85,SI=true,FI=false,CM="lang",VM="all",CAP=10000,q="",
 act=[],actInt=[],hover=null,hoverE=null,drag=null;
let ox=0,oy=0,scale=1,heat=1;
function vok(n){return VM==="all"||n.kind==="central"||n.variant===VM;}
function color(n){
 if(CM==="op")return ocolor[n.operator];
 if(CM==="variant")return n.kind==="central"?"#ffffff":vcolor[n.variant];
 return lcolor[n.language];}
function refresh(){
 T=thr.value/100;thrv.textContent=T.toFixed(2);
 SI=showint.checked;FI=fadeint.checked;CM=cmode.value;VM=vmode.value;
 CAP=+cap.value;q=search.value.trim().toLowerCase();
 // the threshold cuts EXTERNAL connectors only; internal connectors are
 // structure and are never cut by it
 const pass=EXT.filter(e=>e.weight>=T&&vok(N[e.ai])&&vok(N[e.bi]));
 const capped=pass.length>CAP;
 act=capped?pass.slice(0,CAP):pass;
 actInt=SI?INT.filter(e=>vok(N[e.ai])):[];
 // RULING D: components are counted on EXTERNAL connectors ONLY,
 // whether or not internal connectors are drawn.
 const p=N.map((_,i)=>i);
 const f=x=>{while(p[x]!=x){p[x]=p[p[x]];x=p[x];}return x;};
 act.forEach(e=>{const a=f(e.ai),b=f(e.bi);if(a!=b)p[a]=b;});
 const comps=new Set(N.map((_,i)=>f(i))).size;
 stats.textContent=NROW+" row nodes | "+NCEN+" central nodes | "+
  act.length+" external | "+actInt.length+" internal | "+
  comps+" components";
 rule.textContent="RULE: weight is the owner's ruling A -- per-element NUMERIC "+
  "similarity over [sign, mant, expo] with a FORM classifier -- averaged "+
  "over the COMPARABLE sample positions only. Ruling B: a position where "+
  "either side is REFUSE / RAISE:* / ABORT is excluded from numerator and "+
  "denominator both, and two rows with no comparable position have no "+
  "connector at all. Ruling D: internal springs are near zero ("+
  G.int_spring+" against "+G.ext_spring+" external) -- external "+
  "connectors carry the layout, and COMPONENTS ARE COUNTED ON EXTERNAL "+
  "CONNECTORS ONLY. "+(capped
   ?("DRAW CAP IN FORCE: "+pass.length+" external connectors clear "+
     T.toFixed(2)+", the top "+CAP+" BY WEIGHT are drawn, "+
     (pass.length-CAP)+" are not.")
   :("all "+pass.length+" external connectors clearing "+T.toFixed(2)+
     " are drawn (cap "+(CAP>=1e6?"off":CAP)+")."));
 heat=Math.max(heat,0.25);}
thr.oninput=refresh;showint.onchange=refresh;fadeint.onchange=refresh;
cmode.onchange=refresh;vmode.onchange=refresh;cap.onchange=refresh;
search.oninput=refresh;
refresh();
function size(){cv.width=innerWidth;cv.height=innerHeight-cv.offsetTop;}
addEventListener("resize",size);size();
// ---- physics: the pilot's shape unchanged (clamped linear springs,
// velocity clamp, gravity, hard boundary, autofit), repulsion on a
// uniform grid, and RULING D's near-zero internal spring
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
  // RULING D: near-zero internal spring -- a visual tether, not a force
  // that decides the layout
  actInt.forEach(e=>{const a=N[e.ai],b=N[e.bi];
   let dx=b.x-a.x,dy=b.y-a.y,d=Math.sqrt(dx*dx+dy*dy);if(d<1)d=1;
   const f=Math.min((d-70)*INT_K,6);
   a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f;});
  // EXTERNAL connectors carry the layout
  act.forEach(e=>{const a=N[e.ai],b=N[e.bi];
   let dx=b.x-a.x,dy=b.y-a.y,d=Math.sqrt(dx*dx+dy*dy);if(d<1)d=1;
   const f=Math.min((d-140)*EXT_K*e.weight,6);
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
setInterval(()=>{if(heat<0.35)fit();},1500);
function sx(x){return cv.width/2+(x+ox)*scale;}
function sy(y){return cv.height/2+(y+oy)*scale;}
function hit(n){return q&&((n.id.toLowerCase().includes(q))||
 (n.label&&n.label.toLowerCase().includes(q)));}
function draw(){ctx.clearRect(0,0,cv.width,cv.height);
 ctx.lineWidth=1;
 // internal connectors first, visually distinct: warm, dashed
 if(actInt.length){ctx.setLineDash([3,3]);
  actInt.forEach(e=>{const al=FI?(0.05+0.25*e.weight):0.16;
   ctx.strokeStyle=e===hoverE?"#fff":"rgba(224,184,62,"+al+")";
   ctx.beginPath();ctx.moveTo(sx(N[e.ai].x),sy(N[e.ai].y));
   ctx.lineTo(sx(N[e.bi].x),sy(N[e.bi].y));ctx.stroke();});
  ctx.setLineDash([]);}
 // external connectors: cool, solid
 act.forEach(e=>{ctx.strokeStyle=e===hoverE?"#fff":
  "rgba(120,170,220,"+(0.07+0.45*(e.weight-T)/(1.001-T))+")";
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
 // labels last so they sit on top
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
 const keys=CM==="op"?ops:(CM==="variant"?vars:langs),
       tab=CM==="op"?ocolor:(CM==="variant"?vcolor:lcolor);
 keys.forEach(l=>{ctx.fillStyle=tab[l];ctx.fillRect(lx,ly-8,8,8);
  ctx.fillStyle="#9aa2ad";ctx.fillText(l,lx+11,ly);
  lx+=20+ctx.measureText(l).width;});
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
  "<br>lhs_holder "+esc(n.lhs_holder)+" &middot; rhs_holder "+
  esc(n.rhs_holder)+"<br>interval "+esc(n.interval_id)+
  " &middot; variant <b>"+esc(n.variant)+"</b>"+
  "<br>probe "+esc(n.probe_id)+" &middot; input_key "+esc(n.input_key)+
  "<br>n_samples "+n.n_samples+" &middot; n_values "+n.n_values+
  " &middot; n_declines "+n.n_declines+
  "<br>central "+esc(n.central)+
  (ie?("<br>internal weight "+f4(ie.weight)+
   (ie.no_comparison?" (no co-row with a comparable position &mdash; 1.0 "+
    "by convention)":(" = mean ruling-A/B similarity over "+
     ie.n_co_rows_comparable+" of "+ie.n_co_rows+" co-row"+
     (ie.n_co_rows==1?"":"s")))):"");}
function edgeTip(e){
 if(e.kind==="internal")
  return "<b>INTERNAL connector</b><br>"+esc(e.a)+"<br>&rarr; "+
   esc(e.b)+"<br>weight "+f4(e.weight)+
   (e.no_comparison?" (no co-row with a comparable position &mdash; 1.0 "+
    "by convention)":(" = mean ruling-A/B similarity over "+
     e.n_co_rows_comparable+" of "+e.n_co_rows+" co-row"+
     (e.n_co_rows==1?"":"s")))+
   "<br>old byte-identity number "+f4(e.weight_byte)+" (secondary)"+
   "<br>structure, not similarity: never cut by the threshold, and its "+
   "spring is near zero so it does not decide the layout";
 return "<b>EXTERNAL connector</b><br>"+esc(e.a)+"<br>&harr; "+
  esc(e.b)+"<br><b>weight "+f4(e.weight)+"</b> (ruling A/B: mean "+
  "per-element numeric similarity over the comparable positions)"+
  "<br>n_samples "+e.n_samples+" &middot; n_comparable "+e.n_comparable+
  " &middot; n_excluded_declines "+e.n_excluded_declines+
  "<br>old byte-identity number "+f4(e.weight_byte)+" ("+
  e.n_matched_byte+"/"+e.n_samples+", secondary)"+
  "<br>variant "+esc(e.variant)+" &middot; "+
  (e.cross_language?"CROSS-language":"same-language")+
  " &middot; identical input ladders";}
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
