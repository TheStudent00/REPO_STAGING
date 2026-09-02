#!/usr/bin/env python3
"""l3_row_graph.py -- the TWO-TIER row agreement graph over the
interval pilot (rust + ruby).  Assembly only; no probes.

the owner's design, settled 2026-08-21, his words:

    "each row is its own node with a central node that connects all
     rows to its respective node.  meaning that `+` is a central node
     that `+` rows connect to.  so two types of connectors, internal
     and external"

This REPLACES `l3_agreement_graph_interval.py` for the interval data.
The older builder split an interval row into 32 per-sample input pairs
and scored operator-nodes against each other in that pair space.  Here
the ROW is the unit and it is never split: a row's 32 samples travel
together as one ladder-aligned vector, matched position by position.

NODES -- two kinds
  ROW      one per interval row.  908 of them (rust 116, ruby 792).
           id `<lang>.<op> / <probe_id> / <lhs> <op> <rhs> / <iv_id>`.
           Attributes: language, operator, lhs_holder, rhs_holder,
           interval_id, n_values, n_declines.
  CENTRAL  one per `lang.op`.  39 of them.  Attributes: language,
           operator, n_rows.

EDGES -- two kinds, kept distinct in the data and in the explorer
  INTERNAL  every row node to its own `lang.op` central node.  These
            are STRUCTURE, not similarity: they exist regardless of any
            threshold and the threshold slider never touches them.
            They carry a weight for display only -- the mean pairwise
            output-vector agreement between this row and the OTHER rows
            of the same operator that share its input vectors.  A row
            with no co-row on its own inputs carries weight 1.0 by
            convention and `no_comparison: true`.
  EXTERNAL  row node to row node, across DIFFERENT operators only
            (agreement inside one operator is what the internal edges
            already carry).  An external edge exists ONLY when the two
            rows carry IDENTICAL input vectors -- same
            `lhs_canon_vector` AND same `rhs_canon_vector`, i.e. the
            same ladder pair.  Different ladders are not comparable, so
            there is no edge at all, not a low-weight one.  Weight =
            the fraction of the 32 sample positions at which the two
            `output_canon_vector` entries are byte-identical.  Every
            edge records n_samples, n_matched, weight, and whether the
            two rows are same-language or cross-language.

SCOPE: interval rows only, numeric forms only.  Text and containers
are excluded by construction and stay excluded.  No fall-back to the
edge-value matrices in `matrices/` -- this graph reads
`matrices_interval/` and nothing else.

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
IV_DIR = os.path.join(HERE, "matrices_interval")
SEP = ";"
LANGS = ("rust", "ruby")

# the explorer draws at most this many external edges, highest weight
# first; the rule is printed in the UI so the picture is never silently
# partial
RENDER_CAP = 10000


def is_decline(s):
    return s == "REFUSE" or s == "ABORT" or s.startswith("RAISE:")


# ------------------------------------------------------------------
# load -- the row is the unit, and it is never split
# ------------------------------------------------------------------

def load_rows():
    idx = json.load(open(os.path.join(IV_DIR, "index.json")))
    rows = []
    for key in sorted(idx["matrices"]):
        meta = idx["matrices"][key]
        lang, _, op = key.partition(".")
        if lang not in LANGS:
            continue
        path = os.path.join(IV_DIR, meta["file"])
        for r in csv.DictReader(open(path)):
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
                rhs_holder=r["rhs_holder"], interval_id=r["interval_id"],
                n_samples=n, lhs_vec=lv, rhs_vec=rv, out=ov,
                n_values=int(r["n_values"]),
                n_declines=int(r["n_declines"])))
    return rows


def row_id(r):
    return "%s / %s / %s %s %s / %s" % (
        r["key"], r["probe_id"], r["lhs_holder"], r["operator"],
        r["rhs_holder"], r["interval_id"])


def input_key(r):
    """A short stable digest of the row's INPUT ladder pair.

    Two rows are comparable only when this digest matches; it is
    carried on every row node so a verifier outside python can re-check
    the identical-ladder rule without re-reading the CSVs.  It is NOT a
    proxy for interval_id: `w_s128` and `w_big128` are different ids
    that produce byte-identical vectors, and that is exactly how rust
    i128 rows reach ruby whole-holder rows.
    """
    h = hashlib.sha1()
    h.update(r["lhs_vec"].encode())
    h.update(b"\x00")
    h.update(r["rhs_vec"].encode())
    return h.hexdigest()[:16]


def agree(a, b):
    """(n_matched, weight) over byte-identical output positions."""
    n = len(a)
    m = sum(1 for i in range(n) if a[i] == b[i])
    return m, (m / n if n else 0.0)


# ------------------------------------------------------------------
# union-find -- `root` is the super-node of a merged group; the
# vocabulary is absolute, there is no p-word anywhere in this file
# ------------------------------------------------------------------

def components(n, pairs):
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


# ------------------------------------------------------------------

def main():
    print("two-tier ROW agreement graph -- interval pilot (rust + "
          "ruby); row nodes + lang.op central nodes, internal and "
          "external connectors; assembly only")
    t0 = time.time()
    rows = load_rows()
    for r in rows:
        r["id"] = row_id(r)
    ids = [r["id"] for r in rows]
    assert len(set(ids)) == len(ids), "row ids collide"
    keys = sorted({r["key"] for r in rows})
    print("  %d row nodes, %d central nodes (%s), %.2f s"
          % (len(rows), len(keys),
             ", ".join("%s %d" % (l, sum(1 for r in rows
                                         if r["language"] == l))
                       for l in LANGS), time.time() - t0))

    # ------------------------------------------------- input grouping
    # the comparable universe: two rows are comparable ONLY when their
    # input ladder pair is byte-identical
    groups = {}
    for i, r in enumerate(rows):
        groups.setdefault((r["lhs_vec"], r["rhs_vec"]), []).append(i)
    print("  %d distinct input ladder pairs; group sizes %s"
          % (len(groups),
             sorted((len(v) for v in groups.values()), reverse=True)[:8]))

    # --------------------------------------------------- INTERNAL
    # weight = mean pairwise output agreement with the co-rows of the
    # SAME operator that share this row's input vectors
    internal = []
    for gi, members in groups.items():
        by_op = {}
        for i in members:
            by_op.setdefault(rows[i]["key"], []).append(i)
        for key, mem in by_op.items():
            for i in mem:
                co = [j for j in mem if j != i]
                rows[i]["_co"] = co
    for i, r in enumerate(rows):
        co = r.get("_co", [])
        if co:
            w = sum(agree(r["out"], rows[j]["out"])[1] for j in co) / len(co)
            internal.append(dict(kind="internal", a=r["id"], b=r["key"],
                                 weight=round(w, 6), n_co_rows=len(co),
                                 no_comparison=False))
        else:
            internal.append(dict(kind="internal", a=r["id"], b=r["key"],
                                 weight=1.0, n_co_rows=0,
                                 no_comparison=True))
    nnc = sum(1 for e in internal if e["no_comparison"])
    print("  %d internal connectors (one per row node); %d carry "
          "no_comparison (no co-row shares their inputs)"
          % (len(internal), nnc))

    # --------------------------------------------------- EXTERNAL
    # row to row, DIFFERENT operators, identical input ladder pair
    external = []
    universe = 0
    for members in groups.values():
        for x in range(len(members)):
            i = members[x]
            ri = rows[i]
            for y in range(x + 1, len(members)):
                j = members[y]
                rj = rows[j]
                universe += 1
                if ri["key"] == rj["key"]:
                    continue          # that is what internal edges are
                m, w = agree(ri["out"], rj["out"])
                external.append(dict(
                    kind="external", a=ri["id"], b=rj["id"],
                    n_samples=ri["n_samples"], n_matched=m,
                    weight=round(w, 6),
                    cross_language=(ri["language"] != rj["language"])))
    print("  comparable universe: %d row pairs share an identical input "
          "ladder pair; %d of those cross operators -> %d external "
          "connectors (%.1f s)"
          % (universe, len(external), len(external), time.time() - t0))

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
            interval_id=r["interval_id"], probe_id=r["probe_id"],
            input_key=input_key(r),
            n_samples=r["n_samples"], n_values=r["n_values"],
            n_declines=r["n_declines"],
            label="%s %s %s" % (r["lhs_holder"], r["operator"],
                                r["rhs_holder"])))
    edges = internal + external

    # ------------------------------------------------ SANITY numbers
    print("SANITY")
    print("  nodes by kind: %d row, %d central, %d total"
          % (len(rows), len(keys), len(nodes)))
    print("  edges by kind: %d internal, %d external, %d total"
          % (len(internal), len(external), len(edges)))
    print("  comparable universe (row pairs with identical input "
          "ladders, any operator): %d" % universe)
    print("  of which SAME operator (carried by internal edges "
          "instead): %d" % (universe - len(external)))

    nid = {n["id"]: i for i, n in enumerate(nodes)}
    sanity_thresholds = {}
    for t in (1.0, 0.95, 0.85, 0.70):
        act = [e for e in external if e["weight"] >= t]
        xl = sum(1 for e in act if e["cross_language"])
        comps = components(len(nodes),
                           [(nid[e["a"]], nid[e["b"]]) for e in act])
        big = comps[0]
        ops = {nodes[i]["operator"] if nodes[i]["kind"] == "row"
               else nodes[i]["operator"] for i in big}
        langops = {nodes[i].get("central", nodes[i]["id"]) for i in big}
        multi = [c for c in comps if len(c) > 1]
        # the same union-find with the internal connectors present --
        # what the explorer shows with the internal toggle ON
        comps_i = components(
            len(nodes),
            [(nid[e["a"]], nid[e["b"]]) for e in act] +
            [(nid[e["a"]], nid[e["b"]]) for e in internal])
        sanity_thresholds["%.2f" % t] = dict(
            external_edges=len(act), cross_language=xl,
            same_language=len(act) - xl,
            components_external_only=len(comps),
            largest_component=len(big),
            largest_component_operators=sorted(ops),
            largest_component_langops=sorted(langops),
            largest_mixes_operators=(len(langops) > 1),
            multi_node_components=len(multi),
            components_with_internal=len(comps_i))
        print("  t=%.2f : %d external edges (%d same-language, %d "
              "cross-language); external-only components %d (%d "
              "multi-node), largest %d nodes spanning %d lang.op "
              "%s; with internal connectors on: %d components"
              % (t, len(act), len(act) - xl, xl, len(comps), len(multi),
                 len(big), len(langops),
                 "(MIXES OPERATORS)" if len(langops) > 1
                 else "(one operator only)", len(comps_i)))

    # -------------------------------- the two named cross-checks
    def between(ka, kb):
        return [e for e in external
                if {nid_key(e["a"]), nid_key(e["b"])} == {ka, kb}]

    def nid_key(node_id):
        return node_id.partition(" / ")[0]

    named = {}
    for ka, kb in (("rust.+", "ruby.+"), ("rust.+", "rust.-")):
        sel = between(ka, kb)
        ws = sorted((e["weight"] for e in sel), reverse=True)
        named["%s ~ %s" % (ka, kb)] = dict(
            n_edges=len(sel),
            weights=[round(w, 6) for w in ws],
            max=(ws[0] if ws else None), min=(ws[-1] if ws else None),
            mean=(round(sum(ws) / len(ws), 6) if ws else None),
            examples=[dict(a=e["a"], b=e["b"], n_matched=e["n_matched"],
                           n_samples=e["n_samples"], weight=e["weight"])
                      for e in sorted(sel, key=lambda e: -e["weight"])[:6]])
        if not sel:
            print("  %s ~ %s : NO row pair shares an identical input "
                  "ladder -- not comparable" % (ka, kb))
            continue
        print("  %s ~ %s : %d row pairs share identical input ladders; "
              "weight max %.4f, mean %.4f, min %.4f"
              % (ka, kb, len(sel), ws[0],
                 sum(ws) / len(ws), ws[-1]))
        for e in sorted(sel, key=lambda e: -e["weight"])[:4]:
            print("      %.4f  (%d/%d)  %s  ~  %s"
                  % (e["weight"], e["n_matched"], e["n_samples"],
                     e["a"], e["b"]))

    # ------------------------------------------------------ emit
    out = dict(
        status="TWO-TIER ROW AGREEMENT GRAPH -- INTERVAL PILOT (rust + "
               "ruby), ROW NODES PLUS lang.op CENTRAL NODES, INTERNAL "
               "AND EXTERNAL CONNECTORS, ASSEMBLY ONLY",
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        pilot="rust (static) + ruby (route C) only; the other ten wait",
        source="matrices_interval/ ONLY -- interval rows, numeric forms "
               "only; no fall-back to the edge-value matrices",
        design="two kinds of node and two kinds of connector.  A ROW "
               "node is one interval row; a CENTRAL node is one "
               "lang.op.  An INTERNAL connector joins a row node to its "
               "own central node, always, regardless of threshold -- it "
               "is structure, and its weight (mean pairwise output "
               "agreement with the co-rows of the same operator sharing "
               "its inputs) is for display only.  An EXTERNAL connector "
               "joins two row nodes of DIFFERENT operators and exists "
               "only when both rows carry IDENTICAL input vectors (same "
               "lhs_canon_vector and same rhs_canon_vector -- the same "
               "ladder pair); different ladders are not comparable, so "
               "there is no edge at all.  Its weight is the fraction of "
               "the 32 sample positions where the output_canon entries "
               "are byte-identical.  The row is the matching unit and "
               "is never split into per-sample input pairs.",
        scoring="only lhs_canon_vector, rhs_canon_vector and "
                "output_canon_vector contribute to scoring",
        render_rule="the explorer draws at most %d external connectors, "
                    "highest weight first, and says so on screen"
                    % RENDER_CAP,
        render_cap=RENDER_CAP,
        vocabulary="super-node / sub-node / co-node / sub-tree; the "
                   "OS-stopped outcome is ABORT",
        input_key_note="every row node carries `input_key`, a sha1 "
                       "digest of its lhs_canon_vector and "
                       "rhs_canon_vector; an external connector exists "
                       "exactly between two row nodes of different "
                       "operators whose input_key matches",
        n_input_ladder_pairs=len(groups),
        n_row_nodes=len(rows), n_central_nodes=len(keys),
        n_internal_edges=len(internal), n_external_edges=len(external),
        comparable_universe=universe,
        comparable_same_operator=universe - len(external),
        n_no_comparison=nnc,
        sanity=dict(thresholds=sanity_thresholds, named=named),
        nodes=nodes, edges=edges)

    jp = os.path.join(HERE, "row_graph.json")
    json.dump(out, open(jp, "w"), separators=(",", ":"))
    print("  wrote %s (%.2f MB)" % (jp, os.path.getsize(jp) / 1e6))

    html = HTML_TEMPLATE.replace("__GRAPH__",
                                 json.dumps(out, separators=(",", ":")))
    hp = os.path.join(HERE, "row_graph_explorer.html")
    with open(hp, "w") as f:
        f.write(html)
    print("  wrote %s (%.2f MB)" % (hp, os.path.getsize(hp) / 1e6))

    # ------------------------------------------- python-side verify
    print("PYTHON VERIFY")
    back = json.load(open(jp))
    assert len(back["nodes"]) == len(nodes)
    assert len(back["edges"]) == len(edges)
    print("  [json] well-formed; %d nodes, %d edges consistent"
          % (len(back["nodes"]), len(back["edges"])))
    idset = {n["id"] for n in back["nodes"]}
    assert all(e["a"] in idset and e["b"] in idset for e in back["edges"])
    print("  [refs] every connector endpoint is a node")
    seen = {}
    for e in back["edges"]:
        if e["kind"] == "internal":
            seen[e["a"]] = seen.get(e["a"], 0) + 1
    rowids = {n["id"] for n in back["nodes"] if n["kind"] == "row"}
    assert set(seen) == rowids and all(v == 1 for v in seen.values())
    print("  [internal] exactly one internal connector per row node, "
          "%d of them" % len(seen))
    byid = {n["id"]: n for n in back["nodes"]}
    vec = {r["id"]: (r["lhs_vec"], r["rhs_vec"]) for r in rows}
    for e in back["edges"]:
        if e["kind"] != "external":
            continue
        a, b = byid[e["a"]], byid[e["b"]]
        assert a["kind"] == b["kind"] == "row"
        assert a["central"] != b["central"], "external inside one operator"
        assert vec[e["a"]] == vec[e["b"]], "external across ladders"
    print("  [external] every external connector joins two row nodes of "
          "DIFFERENT operators carrying identical input ladders")
    kg = {}
    for n in back["nodes"]:
        if n["kind"] == "row":
            kg.setdefault(n["input_key"], set()).add(n["id"])
    assert len(kg) == len(groups), "input_key collides or over-splits"
    for members in groups.values():
        assert {rows[i]["id"] for i in members} in \
            [set(v) for v in kg.values()]
    print("  [input_key] the %d digests partition the row nodes exactly "
          "as the raw input vectors do" % len(kg))
    want = 0
    for v in kg.values():
        v = sorted(v)
        for x in range(len(v)):
            for y in range(x + 1, len(v)):
                if byid[v[x]]["central"] != byid[v[y]]["central"]:
                    want += 1
    assert want == len(external), (want, len(external))
    print("  [completeness] %d cross-operator row pairs share a digest "
          "and %d external connectors exist -- no pair is missing, none "
          "is invented" % (want, len(external)))
    txt = open(hp).read()
    assert '"nodes"' in txt and '"edges"' in txt and "__GRAPH__" not in txt
    assert "<script src" not in txt
    print("  [html] embedded data present, placeholder gone, no "
          "external scripts")
    print("  done in %.1f s" % (time.time() - t0))


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Interval pilot &mdash; two-tier row agreement graph</title>
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
      display:none;max-width:430px;z-index:9;font-size:12px}
 label{cursor:pointer;white-space:nowrap}
</style></head><body>
<div id="bar">
 <b>Interval pilot &mdash; row graph</b>
 <span>external threshold
  <input type="range" id="thr" min="0" max="100" value="85">
  <span id="thrv">0.85</span></span>
 <label><input type="checkbox" id="showint" checked> internal
  connectors</label>
 <label><input type="checkbox" id="fadeint"> fade internal by
  weight</label>
 <span>colour <select id="cmode">
  <option value="lang">by language</option>
  <option value="op">by operator</option></select></span>
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
const lcolor={};langs.forEach((l,i)=>lcolor[l]=PAL[i%PAL.length]);
const ocolor={};ops.forEach((o,i)=>ocolor[o]=PAL[i%PAL.length]);
const cv=document.getElementById("cv"),ctx=cv.getContext("2d"),
 tip=document.getElementById("tip"),thr=document.getElementById("thr"),
 thrv=document.getElementById("thrv"),
 showint=document.getElementById("showint"),
 fadeint=document.getElementById("fadeint"),
 cmode=document.getElementById("cmode"),cap=document.getElementById("cap"),
 search=document.getElementById("search"),
 stats=document.getElementById("stats"),rule=document.getElementById("rule");
const NROW=N.filter(n=>n.kind==="row").length,
      NCEN=N.filter(n=>n.kind==="central").length;
// seed the layout: central nodes on a wide ring, each row node beside
// its own central node -- the sub-tree starts where it belongs
const cpos={};let ci=0;
N.forEach(n=>{if(n.kind==="central"){
 const t=6.283*ci/NCEN;ci++;
 n.x=Math.cos(t)*900;n.y=Math.sin(t)*900;cpos[n.id]=[n.x,n.y];}});
let rk={};
N.forEach(n=>{if(n.kind==="row"){
 const c=cpos[n.central]||[0,0];const k=(rk[n.central]=(rk[n.central]||0)+1);
 const t=6.283*k/24;
 n.x=c[0]+Math.cos(t)*(90+9*k);n.y=c[1]+Math.sin(t)*(90+9*k);}});
N.forEach(n=>{n.vx=0;n.vy=0;});
let T=0.85,SI=true,FI=false,CM="lang",CAP=10000,q="",
 act=[],actInt=[],hover=null,hoverE=null,drag=null;
let ox=0,oy=0,scale=1,heat=1;
function color(n){return CM==="op"?ocolor[n.operator]:lcolor[n.language];}
function refresh(){
 T=thr.value/100;thrv.textContent=T.toFixed(2);
 SI=showint.checked;FI=fadeint.checked;CM=cmode.value;CAP=+cap.value;
 q=search.value.trim().toLowerCase();
 // the threshold cuts EXTERNAL connectors only; internal connectors are
 // structure and are never cut by it
 const pass=EXT.filter(e=>e.weight>=T);
 const capped=pass.length>CAP;
 act=capped?pass.slice(0,CAP):pass;
 actInt=SI?INT:[];
 const p=N.map((_,i)=>i);
 const f=x=>{while(p[x]!=x){p[x]=p[p[x]];x=p[x];}return x;};
 const uni=e=>{const a=f(e.ai),b=f(e.bi);if(a!=b)p[a]=b;};
 actInt.forEach(uni);act.forEach(uni);
 const comps=new Set(N.map((_,i)=>f(i))).size;
 stats.textContent=NROW+" row nodes | "+NCEN+" central nodes | "+
  act.length+" external | "+actInt.length+" internal | "+
  comps+" components";
 rule.textContent="RULE: the threshold cuts EXTERNAL connectors only "+
  "(an external connector needs two rows of DIFFERENT operators "+
  "carrying IDENTICAL input ladders; weight = matched sample positions "+
  "/ 32). Internal connectors are structure and are never cut by the "+
  "threshold. "+(capped
   ?("DRAW CAP IN FORCE: "+pass.length+" external connectors clear "+
     T.toFixed(2)+", the top "+CAP+" BY WEIGHT are drawn, "+
     (pass.length-CAP)+" are not.")
   :("all "+pass.length+" external connectors clearing "+T.toFixed(2)+
     " are drawn (cap "+(CAP>=1e6?"off":CAP)+")."));
 heat=Math.max(heat,0.25);}
thr.oninput=refresh;showint.onchange=refresh;fadeint.onchange=refresh;
cmode.onchange=refresh;cap.onchange=refresh;search.oninput=refresh;
refresh();
function size(){cv.width=innerWidth;cv.height=innerHeight-cv.offsetTop;}
addEventListener("resize",size);size();
// ---- physics: exactly the pilot's shape (clamped linear springs,
// velocity clamp, gravity, hard boundary, autofit) with the repulsion
// put on a uniform grid, because 947 nodes is heavier than 43
const CELL=170;
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
  actInt.forEach(e=>{const a=N[e.ai],b=N[e.bi];
   let dx=b.x-a.x,dy=b.y-a.y,d=Math.sqrt(dx*dx+dy*dy);if(d<1)d=1;
   const f=Math.min((d-70)*0.030,6);      // LINEAR in distance, capped
   a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f;});
  act.forEach(e=>{const a=N[e.ai],b=N[e.bi];
   let dx=b.x-a.x,dy=b.y-a.y,d=Math.sqrt(dx*dx+dy*dy);if(d<1)d=1;
   const f=Math.min((d-140)*0.006*e.weight,6);
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
  actInt.forEach(e=>{const al=FI?(0.06+0.34*e.weight):0.22;
   ctx.strokeStyle=e===hoverE?"#fff":"rgba(224,184,62,"+al+")";
   ctx.beginPath();ctx.moveTo(sx(N[e.ai].x),sy(N[e.ai].y));
   ctx.lineTo(sx(N[e.bi].x),sy(N[e.bi].y));ctx.stroke();});
  ctx.setLineDash([]);}
 // external connectors: cool, solid
 act.forEach(e=>{ctx.strokeStyle=e===hoverE?"#fff":
  "rgba(120,170,220,"+(0.07+0.45*(e.weight-T)/(1.001-T))+")";
  ctx.beginPath();ctx.moveTo(sx(N[e.ai].x),sy(N[e.ai].y));
  ctx.lineTo(sx(N[e.bi].x),sy(N[e.bi].y));ctx.stroke();});
 N.forEach(n=>{const h=hit(n),cen=n.kind==="central";
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
  N.forEach(n=>{if(n.kind!=="row")return;
   if(q&&!hit(n))return;
   ctx.fillText(n.label,sx(n.x)+5,sy(n.y)+3);});}
 if(hover&&hover.kind==="row"){ctx.font="11px sans-serif";
  ctx.fillStyle="#fff";ctx.fillText(hover.label,sx(hover.x)+7,
   sy(hover.y)-6);}
 let lx=10,ly=cv.height-12;ctx.font="11px sans-serif";
 const keys=CM==="op"?ops:langs,tab=CM==="op"?ocolor:lcolor;
 keys.forEach(l=>{ctx.fillStyle=tab[l];ctx.fillRect(lx,ly-8,8,8);
  ctx.fillStyle="#9aa2ad";ctx.fillText(l,lx+11,ly);
  lx+=20+ctx.measureText(l).width;});
 ctx.fillStyle="#7d8590";
 ctx.fillText("solid = external   dashed = internal",10,ly-18);
 ctx.font="13px sans-serif";}
function pick(mx,my){hover=null;hoverE=null;
 for(const n of N){const dx=sx(n.x)-mx,dy=sy(n.y)-my;
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
  " &middot; probe "+esc(n.probe_id)+
  "<br>input_key "+esc(n.input_key)+
  "<br>n_samples "+n.n_samples+" &middot; n_values "+n.n_values+
  " &middot; n_declines "+n.n_declines+
  "<br>central "+esc(n.central)+
  (ie?("<br>internal weight "+f4(ie.weight)+
   (ie.no_comparison?" (no co-row shares its inputs &mdash; 1.0 by "+
    "convention)":(" over "+ie.n_co_rows+" co-row"+
     (ie.n_co_rows==1?"":"s")))):"");}
function edgeTip(e){
 if(e.kind==="internal")
  return "<b>INTERNAL connector</b><br>"+esc(e.a)+"<br>&rarr; "+
   esc(e.b)+"<br>weight "+f4(e.weight)+
   (e.no_comparison?" (no co-row shares its inputs &mdash; 1.0 by "+
    "convention)":(" = mean output agreement over "+e.n_co_rows+
     " co-row"+(e.n_co_rows==1?"":"s")))+
   "<br>structure, not similarity: never cut by the threshold";
 return "<b>EXTERNAL connector</b><br>"+esc(e.a)+"<br>&harr; "+
  esc(e.b)+"<br>n_samples "+e.n_samples+" &middot; n_matched "+
  e.n_matched+" &middot; weight "+f4(e.weight)+
  "<br>"+(e.cross_language?"CROSS-language":"same-language")+
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
