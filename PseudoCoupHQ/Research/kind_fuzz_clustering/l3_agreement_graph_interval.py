#!/usr/bin/env python3
"""l3_agreement_graph_interval.py -- the operator agreement graph
REBUILT over the interval pilot: rust and ruby operator nodes ONLY,
edge-value rows PLUS interval rows, with the owner's input-overlap criterion
applied as a filter.

Assembly only; no probe runs.

Nodes: every `rust.<op>` and `ruby.<op>` matrix.  The other ten
languages are deliberately absent -- this is the pilot.

Pair space per node = the edge-value rows of `matrices/<lang>.<op>.csv`
UNION the interval samples of `matrices_interval/<lang>.<op>.csv`.  An
interval row contributes one (lhs_canon, rhs_canon) -> output_canon
entry per sample, so the 32 samples of a row enter the same pair space
the edge values already live in.  That is the whole mechanism: the
sweep manufactures input pairs the edge classes never produced, and a
coincidental agreement that survived six values per side has 32 more
chances to fail.

Edge weight (log 048's settled rule, unchanged): align by input pair;
for each pair present in BOTH nodes, score 1 if ANY row of A and ANY
row of B for that pair share a byte-identical output_canon; weight =
matched / shared; pairs in only one node are excluded; no shared pairs
or no matched pairs -> no edge.  Each edge also carries the VALUE-only
rate with REFUSE / RAISE:* / ABORT excluded from both sides.

DEE'S EDGE CRITERION (settled 2026-08-21): an edge between two
operator-nodes counts only when

    input_overlap >= weight,   input_overlap = shared / union

Two nodes that agree on 95 percent of what they share, while sharing 3
percent of what they span, are not neighbours -- the agreement is an
artefact of a thin intersection.  The criterion is applied as a FILTER:
every edge is still emitted, still carries every raw number, and
carries `criterion_pass`, so the filter is inspectable and reversible.
The explorer has a checkbox for it.

Each edge additionally carries the EDGE-ONLY numbers (the same weight
computed over the edge-value rows alone), which is what makes the
coincidence-cull count measurable.

VOCABULARY (absolute): super-node / sub-node / co-node / sub-tree;
the OS-stopped outcome is ABORT.
"""

import csv
import json
import os
import sys
import time

csv.field_size_limit(sys.maxsize)

HERE = os.path.dirname(os.path.abspath(__file__))
MAT_DIR = os.path.join(HERE, "matrices")
IV_DIR = os.path.join(HERE, "matrices_interval")

LANGS = ("rust", "ruby")
SEP = ";"


def is_decline(s):
    return s == "REFUSE" or s == "ABORT" or s.startswith("RAISE:")


# ------------------------------------------------------------------
# load the two pair spaces
# ------------------------------------------------------------------

def load_edge():
    idx = json.load(open(os.path.join(MAT_DIR, "index.json")))
    cols = {}
    for key, meta in idx["matrices"].items():
        if key.partition(".")[0] not in LANGS:
            continue
        per = {}
        for r in csv.DictReader(open(os.path.join(MAT_DIR,
                                                  meta["file"]))):
            per.setdefault((r["lhs_canon"], r["rhs_canon"]),
                           set()).add(r["output_canon"])
        cols[key] = per
    return cols


def load_interval():
    idx = json.load(open(os.path.join(IV_DIR, "index.json")))
    cols = {}
    for key, meta in idx["matrices"].items():
        if key.partition(".")[0] not in LANGS:
            continue
        per = {}
        for r in csv.DictReader(open(os.path.join(IV_DIR,
                                                  meta["file"]))):
            lv = r["lhs_canon_vector"].split(SEP)
            rv = r["rhs_canon_vector"].split(SEP)
            ov = r["output_canon_vector"].split(SEP)
            assert len(lv) == len(rv) == len(ov) == int(r["n_samples"])
            for a, b, o in zip(lv, rv, ov):
                per.setdefault((a, b), set()).add(o)
        cols[key] = per
    return cols


def merge(a, b):
    out = {k: set(v) for k, v in a.items()}
    for k, v in b.items():
        out.setdefault(k, set()).update(v)
    return out


def value_view(per):
    return {k: frozenset(x for x in v if not is_decline(x))
            for k, v in per.items()}


# ------------------------------------------------------------------
# the edge
# ------------------------------------------------------------------

def score(fa, fb):
    """(weight, n_shared, n_matched, n_union, overlap) or None."""
    shared = fa.keys() & fb.keys()
    union = len(fa.keys() | fb.keys())
    if not shared:
        return None
    nm = sum(1 for k in shared if fa[k] & fb[k])
    return (nm / len(shared), len(shared), nm, union,
            len(shared) / union if union else 0.0)


def value_score(va, vb):
    shared = va.keys() & vb.keys()
    nsv = nmv = 0
    for k in shared:
        a, b = va[k], vb[k]
        if a and b:
            nsv += 1
            if a & b:
                nmv += 1
    return ((nmv / nsv) if nsv else None), nsv, nmv


COMPARE_OPS = {"==", "!=", "<", ">", "<=", ">=", "<=>", "===", "!==",
               "eq", "ne", "lt", "gt", "le", "ge", "equal?", "eql?",
               "not_eq"}


def is_compare(col):
    return col.partition(".")[2] in COMPARE_OPS


def components(keys, edges, t, criterion=True):
    # union-find over the node set; `root` is the super-node of a
    # merged group (the vocabulary is absolute -- no p-word here)
    root = {k: k for k in keys}

    def find(x):
        while root[x] != x:
            root[x] = root[root[x]]
            x = root[x]
        return x

    for e in edges:
        if criterion and not e["criterion_pass"]:
            continue
        if e["weight"] is not None and e["weight"] >= t:
            ra, rb = find(e["a"]), find(e["b"])
            if ra != rb:
                root[ra] = rb
    groups = {}
    for k in keys:
        groups.setdefault(find(k), []).append(k)
    return sorted(groups.values(), key=len, reverse=True)


# ------------------------------------------------------------------

def main():
    print("interval-pilot agreement graph -- rust + ruby operator nodes "
          "only, edge rows PLUS interval rows, input-overlap criterion "
          "applied; assembly only")
    t0 = time.time()
    edge_cols = load_edge()
    iv_cols = load_interval()
    keys = sorted(set(edge_cols) | set(iv_cols))
    both = {k: merge(edge_cols.get(k, {}), iv_cols.get(k, {}))
            for k in keys}
    vboth = {k: value_view(v) for k, v in both.items()}
    eonly = {k: {p: frozenset(v) for p, v in edge_cols.get(k, {}).items()}
             for k in keys}
    print("  %d nodes (%d with interval rows), %.1f s"
          % (len(keys), len(iv_cols), time.time() - t0))
    npair_e = sum(len(v) for v in eonly.values())
    npair_b = sum(len(v) for v in both.values())
    print("  input pairs: %d edge-only -> %d with the sweep (+%d)"
          % (npair_e, npair_b, npair_b - npair_e))

    edges = []
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            r = score(both[a], both[b])
            if r is None or r[2] == 0:
                continue
            w, ns, nm, nu, ov = r
            vw, nsv, nmv = value_score(vboth[a], vboth[b])
            e0 = score(eonly[a], eonly[b])
            edges.append(dict(
                a=a, b=b, weight=round(w, 6), n_shared=ns, n_matched=nm,
                n_union=nu, input_overlap=round(ov, 6),
                criterion_pass=bool(ov >= w),
                value_weight=(None if vw is None else round(vw, 6)),
                n_shared_value=nsv, n_matched_value=nmv,
                edge_only_weight=(None if e0 is None
                                  else round(e0[0], 6)),
                edge_only_n_shared=(0 if e0 is None else e0[1]),
                edge_only_n_matched=(0 if e0 is None else e0[2]),
                edge_only_input_overlap=(None if e0 is None
                                         else round(e0[4], 6))))
    npass = sum(1 for e in edges if e["criterion_pass"])
    print("  %d edges, %d pass the input-overlap criterion, %d filtered "
          "out (%.1f s)" % (len(edges), npass, len(edges) - npass,
                            time.time() - t0))

    nodes = [dict(id=k, language=k.partition(".")[0],
                  operator=k.partition(".")[2], compare=is_compare(k),
                  n_pairs_edge=len(eonly[k]), n_pairs_total=len(both[k]),
                  has_interval=(k in iv_cols)) for k in keys]

    # -------------------------------------------------- sanity numbers
    print("SANITY")
    by_pair = {}
    for e in edges:
        by_pair[(e["a"], e["b"])] = by_pair[(e["b"], e["a"])] = e
    for a, b in (("rust.+", "ruby.+"), ("rust.*", "ruby.*"),
                 ("rust.<", "ruby.<")):
        e = by_pair.get((a, b))
        if e is None:
            print("  %s ~ %s : NO EDGE" % (a, b))
            continue
        print("  %s ~ %s : BEFORE (edge values only) %s "
              "(n_shared=%d, n_matched=%d)"
              % (a, b,
                 "%.4f" % e["edge_only_weight"]
                 if e["edge_only_weight"] is not None else "no edge",
                 e["edge_only_n_shared"], e["edge_only_n_matched"]))
        print("  %s ~ %s : AFTER  (with the sweep)   %.4f "
              "(n_shared=%d, n_matched=%d, input_overlap=%.4f, "
              "criterion %s, value_weight=%s)"
              % (a, b, e["weight"], e["n_shared"], e["n_matched"],
                 e["input_overlap"],
                 "PASS" if e["criterion_pass"] else "FAIL",
                 "%.4f" % e["value_weight"]
                 if e["value_weight"] is not None else "None"))

    # ------------------------------------------ the coincidence cull
    perfect_before = [e for e in edges
                      if e["edge_only_weight"] == 1.0]
    perfect_after = [e for e in perfect_before if e["weight"] == 1.0]
    dropped = [e for e in edges
               if e["edge_only_weight"] is not None
               and e["weight"] < e["edge_only_weight"] - 1e-12]
    # the input-pair grain: pairs the SWEEP manufactured, split by
    # whether the two nodes agree on them.  A disagreement here is a
    # coincidence the six edge values could never have caught -- the
    # pair did not exist before the sweep.
    sweep_dis = sweep_agr = 0
    clean_before_dirty_after = 0
    for e in edges:
        a, b = e["a"], e["b"]
        eshared = eonly[a].keys() & eonly[b].keys()
        shared = both[a].keys() & both[b].keys()
        new = shared - eshared
        d = sum(1 for k in new if not (both[a][k] & both[b][k]))
        sweep_dis += d
        sweep_agr += len(new) - d
        if e["edge_only_n_shared"] == e["edge_only_n_matched"] \
                and e["edge_only_n_shared"] > 0 and d > 0:
            clean_before_dirty_after += 1
    print("COINCIDENCE CULL -- what the sweep took away")
    print("  node pairs at weight 1.0000 on the edge values alone: %d"
          % len(perfect_before))
    print("  of those still 1.0000 once the sweep runs:            %d"
          % len(perfect_after))
    print("  CULLED (perfect agreement that was coincidental):     %d"
          % (len(perfect_before) - len(perfect_after)))
    print("  node pairs whose weight FELL at all:                  %d"
          % len(dropped))
    print("  node pairs clean on edge values, dirty under the sweep:%d"
          % clean_before_dirty_after)
    print("  input pairs the sweep MANUFACTURED, agreeing:         %d"
          % sweep_agr)
    print("  input pairs the sweep MANUFACTURED, DISAGREEING:      %d"
          % sweep_dis)
    print("  node pairs the input-overlap criterion then removes:  %d"
          % (len(edges) - npass))
    culled_pairs = sweep_dis
    # the same cull counted where it shows -- at the drawn threshold
    at_threshold = {}
    for t in (0.95, 0.85, 0.70):
        was = [e for e in edges if e["edge_only_weight"] is not None
               and e["edge_only_weight"] >= t]
        still = [e for e in was if e["weight"] >= t]
        at_threshold["%.2f" % t] = dict(
            edge_values_alone=len(was), with_sweep=len(still),
            coincidental_removed=len(was) - len(still))
        print("  t=%.2f : %d edges reach the threshold on the edge "
              "values alone, %d survive the sweep -- %d were "
              "COINCIDENTAL" % (t, len(was), len(still),
                                len(was) - len(still)))

    for t in (0.95, 0.85, 0.70):
        comps = components(keys, edges, t, criterion=True)
        raw = components(keys, edges, t, criterion=False)
        multi = [c for c in comps if len(c) > 1]
        print("  t=%.2f : %d components (%d multi-node, largest %d) "
              "with the criterion; %d without it"
              % (t, len(comps), len(multi),
                 len(comps[0]) if comps else 0, len(raw)))

    out = dict(
        status="OPERATOR AGREEMENT GRAPH -- INTERVAL PILOT (rust + "
               "ruby), EDGE ROWS PLUS INTERVAL ROWS, INPUT-OVERLAP "
               "CRITERION APPLIED, ASSEMBLY ONLY",
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        pilot="rust (static) + ruby (route C) only; the other ten wait",
        design="edge weight = matched shared input pairs / shared input "
               "pairs, a pair matching when ANY row of A and ANY row of "
               "B share a byte-identical output_canon; an interval row "
               "contributes one input pair per sample, so the sweep and "
               "the edge values share one pair space; pairs in only one "
               "node excluded; no shared or no matched pairs -> no edge",
        criterion="an edge counts only when input_overlap >= weight, "
                  "input_overlap = shared input pairs / union of input "
                  "pairs; every edge is still emitted with its raw "
                  "numbers and a criterion_pass flag, so the filter is "
                  "inspectable and reversible",
        source="matrices/ (edge values) + matrices_interval/ (the "
               "tensor)",
        vocabulary="super-node / sub-node / co-node / sub-tree; the "
                   "OS-stopped outcome is ABORT",
        input_pairs_edge_only=npair_e, input_pairs_with_sweep=npair_b,
        coincidence_cull=dict(
            perfect_before=len(perfect_before),
            perfect_after=len(perfect_after),
            culled=len(perfect_before) - len(perfect_after),
            weight_fell=len(dropped),
            clean_before_dirty_after=clean_before_dirty_after,
            sweep_input_pairs_agreeing=sweep_agr,
            sweep_input_pairs_disagreeing=culled_pairs,
            removed_by_criterion=len(edges) - npass,
            at_threshold=at_threshold),
        nodes=nodes, edges=edges)
    jp = os.path.join(HERE, "agreement_graph_interval_pilot.json")
    json.dump(out, open(jp, "w"), separators=(",", ":"))
    print("  wrote %s (%.2f MB)" % (jp, os.path.getsize(jp) / 1e6))

    html = HTML_TEMPLATE.replace("__GRAPH__",
                                 json.dumps(out, separators=(",", ":")))
    hp = os.path.join(HERE, "graph_explorer_interval_pilot.html")
    with open(hp, "w") as f:
        f.write(html)
    print("  wrote %s (%.2f MB)" % (hp, os.path.getsize(hp) / 1e6))

    # ---------------------------------------------- headless verify
    print("HEADLESS VERIFY")
    back = json.load(open(jp))
    assert len(back["nodes"]) == len(keys)
    assert len(back["edges"]) == len(edges)
    print("  [json] well-formed; %d nodes, %d edges consistent"
          % (len(back["nodes"]), len(back["edges"])))
    assert all(e["weight"] > 0 for e in back["edges"])
    print("  [edges] no 0-weight edges")
    ids = {n["id"] for n in back["nodes"]}
    assert all(e["a"] in ids and e["b"] in ids for e in back["edges"])
    print("  [refs] every edge endpoint is a node")
    assert all(n["language"] in LANGS for n in back["nodes"])
    print("  [pilot] every node is rust or ruby -- the other ten are "
          "untouched")
    assert all(e["criterion_pass"] ==
               (e["input_overlap"] >= e["weight"]) for e in back["edges"])
    print("  [criterion] the flag equals input_overlap >= weight on "
          "every edge (filter reversible from the raw numbers)")
    txt = open(hp).read()
    assert '"nodes"' in txt and '"edges"' in txt and "__GRAPH__" not in txt
    assert "<script src" not in txt
    print("  [html] embedded data present, placeholder gone, no "
          "external scripts")


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Interval pilot &mdash; operator agreement graph</title>
<style>
 body{margin:0;font:13px/1.4 system-ui,sans-serif;background:#14161a;
      color:#d7dae0;display:flex;flex-direction:column;height:100vh}
 #bar{padding:8px 14px;background:#1d2026;display:flex;
      gap:16px;align-items:center;flex-wrap:wrap;border-bottom:1px solid #2b2f36}
 #bar b{color:#fff}
 input[type=range]{width:220px}
 #search{background:#14161a;border:1px solid #3a3f48;color:#d7dae0;
         padding:3px 7px;border-radius:4px}
 #stats{color:#9aa2ad}
 canvas{flex:1;display:block}
 #tip{position:fixed;pointer-events:none;background:#22262d;
      border:1px solid #3a3f48;border-radius:5px;padding:6px 9px;
      display:none;max-width:380px;z-index:9}
 label{cursor:pointer}
</style></head><body>
<div id="bar">
 <b>Interval pilot &mdash; rust + ruby</b>
 <span>threshold <input type="range" id="thr" min="0" max="100" value="85">
 <span id="thrv">0.85</span></span>
 <label><input type="checkbox" id="usevw"> weight by value_weight</label>
 <label><input type="checkbox" id="crit" checked> input-overlap criterion</label>
 <input id="search" placeholder="search lang.op">
 <span id="stats"></span>
</div>
<canvas id="cv"></canvas><div id="tip"></div>
<script>
const G=__GRAPH__;
const N=G.nodes,E=G.edges;
const langs=[...new Set(N.map(n=>n.language))].sort();
const PAL=["#e6553f","#4f9cf0","#58c26a","#e0b83e","#b57ee0","#3ec8c0",
 "#e07ab0","#98a832","#f08b3e","#7a8cf0","#50b08a","#c0625a"];
const lcolor={};langs.forEach((l,i)=>lcolor[l]=PAL[i%PAL.length]);
const idx={};N.forEach((n,i)=>{idx[n.id]=i;});
E.forEach(e=>{e.ai=idx[e.a];e.bi=idx[e.b];});
const cv=document.getElementById("cv"),ctx=cv.getContext("2d"),
 tip=document.getElementById("tip"),thr=document.getElementById("thr"),
 thrv=document.getElementById("thrv"),usevw=document.getElementById("usevw"),
 crit=document.getElementById("crit"),
 search=document.getElementById("search"),stats=document.getElementById("stats");
N.forEach((n,i)=>{const t=6.283*i/N.length;n.x=Math.cos(t)*340;n.y=Math.sin(t)*340;n.vx=0;n.vy=0;});
let T=0.85,VW=false,CR=true,q="",act=[],hover=null,hoverE=null,drag=null;
let ox=0,oy=0,scale=1,heat=1;
function w(e){return VW?e.value_weight:e.weight;}
function refresh(){T=thr.value/100;thrv.textContent=T.toFixed(2);
 VW=usevw.checked;CR=crit.checked;q=search.value.trim().toLowerCase();
 act=E.filter(e=>(!CR||e.criterion_pass)&&w(e)!=null&&w(e)>=T);
 const p=N.map((_,i)=>i);const f=x=>{while(p[x]!=x){p[x]=p[p[x]];x=p[x];}return x;};
 act.forEach(e=>{const a=f(e.ai),b=f(e.bi);if(a!=b)p[a]=b;});
 const comps=new Set(N.map((_,i)=>f(i))).size;
 stats.textContent=act.length+" edges | "+comps+" components | "+N.length+" nodes";
 heat=1;}
thr.oninput=refresh;usevw.onchange=refresh;crit.onchange=refresh;
search.oninput=refresh;refresh();
function size(){cv.width=innerWidth;cv.height=innerHeight-cv.offsetTop;}
addEventListener("resize",size);size();
function step(){ // force layout over ACTIVE edges -- clamped, cannot explode
 if(heat>0.01){
  for(let i=0;i<N.length;i++)for(let j=i+1;j<N.length;j++){
   const a=N[i],b=N[j];let dx=a.x-b.x,dy=a.y-b.y;
   let d2=dx*dx+dy*dy; if(d2<1)d2=1;
   if(d2>250000)continue;                 // ignore far apart
   const d=Math.sqrt(d2), f=Math.min(900/d2,4);
   a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f;}
  act.forEach(e=>{const a=N[e.ai],b=N[e.bi];
   let dx=b.x-a.x,dy=b.y-a.y,d=Math.sqrt(dx*dx+dy*dy);if(d<1)d=1;
   const f=Math.min((d-90)*0.02*w(e),6);   // LINEAR in distance, capped
   a.vx+=dx/d*f;a.vy+=dy/d*f;b.vx-=dx/d*f;b.vy-=dy/d*f;});
  N.forEach(n=>{
   n.vx-=n.x*0.004;n.vy-=n.y*0.004;        // gravity to centre
   const v=Math.hypot(n.vx,n.vy);
   if(v>30){n.vx*=30/v;n.vy*=30/v;}        // velocity clamp
   n.x+=n.vx*0.25*heat;n.y+=n.vy*0.25*heat;n.vx*=0.75;n.vy*=0.75;
   const r=Math.hypot(n.x,n.y);
   if(r>1400){n.x*=1400/r;n.y*=1400/r;}}); // hard boundary
  heat*=0.99;}
 draw();requestAnimationFrame(step);}
function fit(){ // frame everything in view
 let mnx=1e9,mny=1e9,mxx=-1e9,mxy=-1e9;
 N.forEach(n=>{mnx=Math.min(mnx,n.x);mxx=Math.max(mxx,n.x);
  mny=Math.min(mny,n.y);mxy=Math.max(mxy,n.y);});
 const w2=Math.max(mxx-mnx,10),h2=Math.max(mxy-mny,10);
 scale=Math.min((cv.width-80)/w2,(cv.height-80)/h2,3);
 ox=-(mnx+mxx)/2;oy=-(mny+mxy)/2;}
setInterval(()=>{if(heat<0.35)fit();},1200);
function sx(x){return cv.width/2+(x+ox)*scale;}
function sy(y){return cv.height/2+(y+oy)*scale;}
function draw(){ctx.clearRect(0,0,cv.width,cv.height);
 ctx.lineWidth=1;
 act.forEach(e=>{ctx.strokeStyle=e===hoverE?"#fff":
  "rgba(140,150,165,"+(0.08+0.5*(w(e)-T)/(1.001-T))+")";
  ctx.beginPath();ctx.moveTo(sx(N[e.ai].x),sy(N[e.ai].y));
  ctx.lineTo(sx(N[e.bi].x),sy(N[e.bi].y));ctx.stroke();});
 N.forEach(n=>{const hit=q&&n.id.toLowerCase().includes(q);
  ctx.beginPath();ctx.arc(sx(n.x),sy(n.y),hit?7:(n===hover?6:5),0,6.283);
  ctx.fillStyle=lcolor[n.language];ctx.globalAlpha=q&&!hit?0.15:1;
  ctx.fill();ctx.globalAlpha=1;
  if(n.compare){ctx.strokeStyle="#fff";ctx.stroke();}
  ctx.fillStyle="#d7dae0";
  ctx.fillText(n.operator,sx(n.x)+7,sy(n.y)+3);});
 let lx=10,ly=cv.height-14;ctx.font="11px sans-serif";
 langs.forEach(l=>{ctx.fillStyle=lcolor[l];ctx.fillRect(lx,ly-8,8,8);
  ctx.fillStyle="#9aa2ad";ctx.fillText(l,lx+11,ly);
  lx+=20+ctx.measureText(l).width;});ctx.font="13px sans-serif";}
function pick(mx,my){hover=null;hoverE=null;
 for(const n of N){const dx=sx(n.x)-mx,dy=sy(n.y)-my;
  if(dx*dx+dy*dy<80){hover=n;return;}}
 let best=25;
 for(const e of act){const x1=sx(N[e.ai].x),y1=sy(N[e.ai].y),
  x2=sx(N[e.bi].x),y2=sy(N[e.bi].y);
  const L2=(x2-x1)**2+(y2-y1)**2;if(!L2)continue;
  let t=((mx-x1)*(x2-x1)+(my-y1)*(y2-y1))/L2;t=Math.max(0,Math.min(1,t));
  const dx=mx-(x1+t*(x2-x1)),dy=my-(y1+t*(y2-y1)),d2=dx*dx+dy*dy;
  if(d2<best){best=d2;hoverE=e;}}}
function mxy(ev){const r=cv.getBoundingClientRect();
 return[ev.clientX-r.left,ev.clientY-r.top];}
function f4(x){return x==null?"&mdash;":x.toFixed(4);}
cv.onmousemove=ev=>{const[mx,my]=mxy(ev);
 if(drag){if(drag.node){drag.node.x=(mx-cv.width/2)/scale-ox;
   drag.node.y=(my-cv.height/2)/scale-oy;heat=Math.max(heat,0.3);}
  else{ox+=(mx-drag.px)/scale;oy+=(my-drag.py)/scale;
   drag.px=mx;drag.py=my;}return;}
 pick(mx,my);
 if(hover){tip.style.display="block";
  tip.innerHTML="<b>"+hover.id+"</b><br>language "+hover.language+
   " &middot; operator "+hover.operator+(hover.compare?" (comparison)":"")+
   "<br>input pairs "+hover.n_pairs_edge+" edge &rarr; "+
   hover.n_pairs_total+" with the sweep";}
 else if(hoverE){tip.style.display="block";
  tip.innerHTML="<b>"+hoverE.a+" ~ "+hoverE.b+"</b><br>weight "+
   f4(hoverE.weight)+" ("+hoverE.n_matched+"/"+hoverE.n_shared+")"+
   "<br>edge values alone "+f4(hoverE.edge_only_weight)+" ("+
   hoverE.edge_only_n_matched+"/"+hoverE.edge_only_n_shared+")"+
   "<br>input_overlap "+f4(hoverE.input_overlap)+" ("+hoverE.n_shared+
   "/"+hoverE.n_union+") &middot; criterion "+
   (hoverE.criterion_pass?"PASS":"FAIL")+
   "<br>value_weight "+f4(hoverE.value_weight)+
   " ("+hoverE.n_matched_value+"/"+hoverE.n_shared_value+")";}
 else tip.style.display="none";
 tip.style.left=(ev.clientX+14)+"px";tip.style.top=(ev.clientY+14)+"px";};
cv.onmousedown=ev=>{const[mx,my]=mxy(ev);pick(mx,my);
 drag=hover?{node:hover}:{px:mx,py:my};};
addEventListener("mouseup",()=>drag=null);
cv.onwheel=ev=>{ev.preventDefault();
 scale*=ev.deltaY<0?1.1:0.9;scale=Math.max(0.2,Math.min(6,scale));};
step();
</script></body></html>
"""


if __name__ == "__main__":
    main()
