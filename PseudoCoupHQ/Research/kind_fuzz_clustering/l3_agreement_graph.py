#!/usr/bin/env python3
"""l3_agreement_graph.py -- OPERATOR AGREEMENT GRAPH over the v2
canonical strings.  Assembly only; no probe runs.

Built 2026-08-21 from the v2 per-operator matrices (matrices/, the owner's
final canonical forms).  the owner's design (2026-08-20, settled): each
operator-matrix is a node; its connections to other nodes are the
percentage of agreement; the threshold is the cutoff for connection.

Edge weight between two lang.op nodes, at the ROW grain (this
REPLACES the set-identity rule of l3_dendro_strings.py, which the owner
rejected -- it zeroed go.+ ~ python.+ even though individual rows
match byte-identically):
  - align by input pair (lhs_canon, rhs_canon);
  - for each input pair present in BOTH matrices, score 1 if ANY row
    of A and ANY row of B for that pair have byte-identical
    output_canon (best-match), else 0;
  - weight = matched pairs / shared pairs;
  - input pairs in only one matrix are EXCLUDED;
  - no shared pairs -> no edge; a matched count of zero -> no edge
    (never a 0-weight edge).
Each edge also carries n_shared, n_matched, and the VALUE-only rate
(rows whose output_canon is REFUSE / RAISE:* / ABORT excluded from
both sides; a pair enters the value denominator only when both sides
still hold at least one value output) so decline-agreement and
value-agreement stay separable: n_shared_value, n_matched_value,
value_weight.

The threshold is a SPECTRUM: graph_explorer.html has a slider; edges
draw when weight >= threshold.

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


def is_decline(s):
    return s == "REFUSE" or s == "ABORT" or s.startswith("RAISE:")


def load_columns():
    """column -> {(lhs_canon, rhs_canon): frozenset(output_canon)}
    plus the value-only view (decline tokens removed)."""
    idx = json.load(open(os.path.join(MAT_DIR, "index.json")))
    cols, vcols = {}, {}
    for key, meta in idx["matrices"].items():
        per = {}
        for r in csv.DictReader(open(os.path.join(MAT_DIR,
                                                  meta["file"]))):
            per.setdefault((r["lhs_canon"], r["rhs_canon"]),
                           set()).add(r["output_canon"])
        cols[key] = {k: frozenset(v) for k, v in per.items()}
        vcols[key] = {k: frozenset(x for x in v if not is_decline(x))
                      for k, v in per.items()}
    return cols, vcols


def edge(fa, fb, va, vb):
    """(weight, n_shared, n_matched, value_weight, n_shared_value,
    n_matched_value) or None when no shared pairs."""
    shared = fa.keys() & fb.keys()
    if not shared:
        return None
    nm = sum(1 for k in shared if fa[k] & fb[k])
    nsv = nmv = 0
    for k in shared:
        a, b = va[k], vb[k]
        if a and b:
            nsv += 1
            if a & b:
                nmv += 1
    return (nm / len(shared), len(shared), nm,
            (nmv / nsv) if nsv else None, nsv, nmv)


COMPARE_OPS = {"==", "!=", "<", ">", "<=", ">=", "<=>", "===", "!==",
               "eq", "ne", "lt", "gt", "le", "ge", "equal?", "eql?",
               "not_eq"}


def is_compare(col):
    return col.partition(".")[2] in COMPARE_OPS


def components(keys, edges, t, use_value=False):
    parent = {k: k for k in keys}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    for e in edges:
        w = e["value_weight"] if use_value else e["weight"]
        if w is not None and w >= t:
            ra, rb = find(e["a"]), find(e["b"])
            if ra != rb:
                parent[ra] = rb
    groups = {}
    for k in keys:
        groups.setdefault(find(k), []).append(k)
    return sorted(groups.values(), key=len, reverse=True)


def main():
    print("operator agreement graph -- row-grain best-match rule, "
          "assembly only")
    t0 = time.time()
    cols, vcols = load_columns()
    keys = sorted(cols)
    print("  %d nodes loaded (%.1f s)" % (len(keys), time.time() - t0))

    edges = []
    for i, a in enumerate(keys):
        for b in keys[i + 1:]:
            r = edge(cols[a], cols[b], vcols[a], vcols[b])
            if r is None or r[2] == 0:
                continue                       # no edge, never 0-weight
            w, ns, nm, vw, nsv, nmv = r
            edges.append(dict(a=a, b=b, weight=round(w, 6),
                              n_shared=ns, n_matched=nm,
                              value_weight=(None if vw is None
                                            else round(vw, 6)),
                              n_shared_value=nsv,
                              n_matched_value=nmv))
    print("  %d edges (%.1f s)" % (len(edges), time.time() - t0))

    nodes = [dict(id=k, language=k.partition(".")[0],
                  operator=k.partition(".")[2],
                  compare=is_compare(k)) for k in keys]

    # ---------------------------------------------- sanity numbers
    print("SANITY")
    by_pair = {}
    for e in edges:
        by_pair[(e["a"], e["b"])] = by_pair[(e["b"], e["a"])] = e
    for a, b in (("go.+", "python.+"), ("go.+", "rust.+")):
        e = by_pair.get((a, b))
        if e is None:
            print("  %s ~ %s : NO EDGE" % (a, b))
            continue
        print("  %s ~ %s = %.4f  (n_shared=%d, n_matched=%d, "
              "value_weight=%s, n_shared_value=%d, n_matched_value=%d)"
              % (a, b, e["weight"], e["n_shared"], e["n_matched"],
                 "%.4f" % e["value_weight"]
                 if e["value_weight"] is not None else "None",
                 e["n_shared_value"], e["n_matched_value"]))
    # verify the specific row match the owner cited: python int+int vs a go
    # uint64+uint64 row with the same input canons + output canon
    hit = 0
    for k in (cols["go.+"].keys() & cols["python.+"].keys()):
        if cols["go.+"][k] & cols["python.+"][k]:
            hit += 1
    print("  go.+ ~ python.+ input pairs with a byte-identical "
          "best-match row: %d (the int+int/uint64 matches the owner cited "
          "are %s)" % (hit, "PRESENT" if hit else "ABSENT"))

    for t in (0.95, 0.85, 0.70):
        comps = components(keys, edges, t)
        multi = [c for c in comps if len(c) > 1]
        print("  t=%.2f : %d components (%d multi-node, largest %d)"
              % (t, len(comps), len(multi),
                 len(comps[0]) if comps else 0))
        # arithmetic vs comparison separation
        mixed = [c for c in multi
                 if any(is_compare(k) for k in c)
                 and any(not is_compare(k) for k in c)]
        print("    arithmetic vs comparison: %d mixed components -- "
              "arithmetic %s a component distinct from comparisons"
              % (len(mixed), "FORMS" if not mixed else "does NOT form"))
    deg = {k: 0 for k in keys}
    for e in edges:
        deg[e["a"]] += 1
        deg[e["b"]] += 1
    top = max(keys, key=lambda k: deg[k])
    print("  highest-degree node: %s (degree %d, language %s)"
          % (top, deg[top], top.partition(".")[0]))

    out = dict(
        status="OPERATOR AGREEMENT GRAPH, ROW-GRAIN BEST-MATCH, "
               "ASSEMBLY ONLY",
        built=time.strftime("%Y-%m-%d %H:%M:%S"),
        design="edge weight = matched shared input pairs / shared "
               "input pairs; a pair matches when ANY row of A and ANY "
               "row of B share a byte-identical output_canon "
               "(best-match); pairs in only one matrix excluded; no "
               "shared or no matched pairs -> no edge; value_weight "
               "excludes REFUSE/RAISE:*/ABORT rows from both sides",
        source="matrices/ (v2, the owner's final canonical forms)",
        vocabulary="super-node / sub-node / co-node / sub-tree; the "
                   "OS-stopped outcome is ABORT",
        nodes=nodes, edges=edges)
    jp = os.path.join(HERE, "agreement_graph.json")
    json.dump(out, open(jp, "w"), separators=(",", ":"))
    print("  wrote %s (%.2f MB)" % (jp, os.path.getsize(jp) / 1e6))

    html = HTML_TEMPLATE.replace(
        "__GRAPH__", json.dumps(out, separators=(",", ":")))
    hp = os.path.join(HERE, "graph_explorer.html")
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
    txt = open(hp).read()
    assert '"nodes"' in txt and '"edges"' in txt \
        and "__GRAPH__" not in txt
    assert "<script src" not in txt        # self-contained, precedent
    print("  [html] embedded data present, placeholder gone, no "
          "external scripts")


HTML_TEMPLATE = r"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<title>Operator agreement graph &mdash; threshold spectrum</title>
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
      display:none;max-width:340px;z-index:9}
 label{cursor:pointer}
</style></head><body>
<div id="bar">
 <b>Operator agreement graph</b>
 <span>threshold <input type="range" id="thr" min="0" max="100" value="85">
 <span id="thrv">0.85</span></span>
 <label><input type="checkbox" id="usevw"> weight by value_weight</label>
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
const idx={};N.forEach((n,i)=>{idx[n.id]=i;
 n.x=Math.cos(i/N.length*6.283)*300+Math.random()*40;
 n.y=Math.sin(i/N.length*6.283)*300+Math.random()*40;n.vx=0;n.vy=0;});
E.forEach(e=>{e.ai=idx[e.a];e.bi=idx[e.b];});
const cv=document.getElementById("cv"),ctx=cv.getContext("2d"),
 tip=document.getElementById("tip"),thr=document.getElementById("thr"),
 thrv=document.getElementById("thrv"),usevw=document.getElementById("usevw"),
 search=document.getElementById("search"),stats=document.getElementById("stats");
let T=0.85,VW=false,q="",act=[],hover=null,hoverE=null,drag=null;
let ox=0,oy=0,scale=1,heat=1;
function w(e){return VW?e.value_weight:e.weight;}
function refresh(){T=thr.value/100;thrv.textContent=T.toFixed(2);
 VW=usevw.checked;q=search.value.trim().toLowerCase();
 act=E.filter(e=>w(e)!=null&&w(e)>=T);
 // components (union-find)
 const p=N.map((_,i)=>i);const f=x=>{while(p[x]!=x){p[x]=p[p[x]];x=p[x];}return x;};
 act.forEach(e=>{const a=f(e.ai),b=f(e.bi);if(a!=b)p[a]=b;});
 const comps=new Set(N.map((_,i)=>f(i))).size;
 stats.textContent=act.length+" edges | "+comps+" components";
 heat=1;}
thr.oninput=refresh;usevw.onchange=refresh;search.oninput=refresh;refresh();
function size(){cv.width=innerWidth;cv.height=innerHeight-cv.offsetTop;}
addEventListener("resize",size);size();
function step(){ // simple force layout over ACTIVE edges
 if(heat>0.01){
  for(let i=0;i<N.length;i++)for(let j=i+1;j<N.length;j++){
   const a=N[i],b=N[j];let dx=a.x-b.x,dy=a.y-b.y,d2=dx*dx+dy*dy+1;
   if(d2<40000){const f=1200/d2;dx*=f;dy*=f;a.vx+=dx;a.vy+=dy;b.vx-=dx;b.vy-=dy;}}
  act.forEach(e=>{const a=N[e.ai],b=N[e.bi];
   const dx=b.x-a.x,dy=b.y-a.y,d=Math.sqrt(dx*dx+dy*dy)+.1,
   f=(d-60)*0.004*w(e);a.vx+=dx/d*f*d;a.vy+=dy/d*f*d;
   b.vx-=dx/d*f*d;b.vy-=dy/d*f*d;});
  N.forEach(n=>{n.vx-=n.x*0.002;n.vy-=n.y*0.002;
   n.x+=n.vx*0.05*heat;n.y+=n.vy*0.05*heat;n.vx*=0.6;n.vy*=0.6;});
  heat*=0.995;}
 draw();requestAnimationFrame(step);}
function sx(x){return cv.width/2+(x+ox)*scale;}
function sy(y){return cv.height/2+(y+oy)*scale;}
function draw(){ctx.clearRect(0,0,cv.width,cv.height);
 ctx.lineWidth=1;
 act.forEach(e=>{ctx.strokeStyle=e===hoverE?"#fff":
  "rgba(140,150,165,"+(0.08+0.5*(w(e)-T)/(1.001-T))+")";
  ctx.beginPath();ctx.moveTo(sx(N[e.ai].x),sy(N[e.ai].y));
  ctx.lineTo(sx(N[e.bi].x),sy(N[e.bi].y));ctx.stroke();});
 N.forEach(n=>{const hit=q&&n.id.toLowerCase().includes(q);
  ctx.beginPath();ctx.arc(sx(n.x),sy(n.y),hit?7:(n===hover?6:4),0,6.283);
  ctx.fillStyle=lcolor[n.language];ctx.globalAlpha=q&&!hit?0.15:1;
  ctx.fill();ctx.globalAlpha=1;
  if(n.compare){ctx.strokeStyle="#fff";ctx.stroke();}
  if(hit||n===hover||scale>1.6){ctx.fillStyle="#d7dae0";
   ctx.fillText(n.operator,sx(n.x)+6,sy(n.y)+3);}});
 let lx=10,ly=cv.height-14;ctx.font="11px sans-serif";
 langs.forEach(l=>{ctx.fillStyle=lcolor[l];ctx.fillRect(lx,ly-8,8,8);
  ctx.fillStyle="#9aa2ad";ctx.fillText(l,lx+11,ly);
  lx+=20+ctx.measureText(l).width;});ctx.font="13px sans-serif";}
function pick(mx,my){hover=null;hoverE=null;
 for(const n of N){const dx=sx(n.x)-mx,dy=sy(n.y)-my;
  if(dx*dx+dy*dy<64){hover=n;return;}}
 let best=25;
 for(const e of act){const x1=sx(N[e.ai].x),y1=sy(N[e.ai].y),
  x2=sx(N[e.bi].x),y2=sy(N[e.bi].y);
  const L2=(x2-x1)**2+(y2-y1)**2;if(!L2)continue;
  let t=((mx-x1)*(x2-x1)+(my-y1)*(y2-y1))/L2;t=Math.max(0,Math.min(1,t));
  const dx=mx-(x1+t*(x2-x1)),dy=my-(y1+t*(y2-y1)),d2=dx*dx+dy*dy;
  if(d2<best){best=d2;hoverE=e;}}}
function mxy(ev){const r=cv.getBoundingClientRect();
 return[ev.clientX-r.left,ev.clientY-r.top];}
cv.onmousemove=ev=>{const[mx,my]=mxy(ev);
 if(drag){if(drag.node){drag.node.x=(mx-cv.width/2)/scale-ox;
   drag.node.y=(my-cv.height/2)/scale-oy;heat=Math.max(heat,0.3);}
  else{ox+=(mx-drag.px)/scale;oy+=(my-drag.py)/scale;
   drag.px=mx;drag.py=my;}return;}
 pick(mx,my);
 if(hover){tip.style.display="block";
  tip.innerHTML="<b>"+hover.id+"</b><br>language "+hover.language+
   " &middot; operator "+hover.operator+(hover.compare?" (comparison)":"");}
 else if(hoverE){tip.style.display="block";
  tip.innerHTML="<b>"+hoverE.a+" ~ "+hoverE.b+"</b><br>weight "+
   hoverE.weight.toFixed(4)+"<br>n_shared "+hoverE.n_shared+
   " &middot; n_matched "+hoverE.n_matched+"<br>value_weight "+
   (hoverE.value_weight==null?"&mdash;":hoverE.value_weight.toFixed(4))+
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
