#!/usr/bin/env python3
"""build_explorer2.py -- write cluster_explorer2.html from verdicts3.json.

The page is the same instrument as cluster_explorer.html: pick a row,
walk the evidence tiers (bytes -> anchored sem -> z3 -> differs-by-
design links), watch the units consolidate.

Two things are different, and both are the point:

  * The rows are the MACHINE-FORM groups of verdicts3.json -- a byte
    cluster, a sem cluster, or a shared-core connection, each on one
    operand type pair.  The dropdown entry is that group's canonical
    description.  No entry is named by an operator token; the token
    appears only on the member dots' tooltips, as a display label.
  * The CSS defect is not reintroduced.  The view sections are hidden
    by id and shown by `#overview-view.active` / `#detail-view.active`,
    so the shown rule has the same specificity as the hidden one and
    actually wins.  That fix is carried over from cluster_explorer.html
    unchanged.

usage:
  build_explorer2.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

MAXLEN = 120


def clip(text, n=MAXLEN):
    if text is None:
        return ""
    text = str(text)
    if len(text) <= n:
        return text
    return text[:n - 1] + "…"


def payload():
    doc = json.load(open(os.path.join(HERE, "verdicts3.json")))
    rows = []
    for r in doc["rows"]:
        units = []
        seen = set()
        for m in r["members"]:
            uid = "%s/op_%s" % (m["lang"], m["n"])
            if uid in seen:
                continue
            seen.add(uid)
            units.append(dict(u=uid, lang=m["lang"], n=m["n"],
                              operator=m["operator"],
                              type_pair=m["type_pair"]))
        pairs = []
        for p in r["pairs"]:
            pairs.append(dict(a=p["left"], b=p["right"], v=p["verdict"],
                              g=p.get("ground", ""),
                              d=clip(p.get("detail", "")),
                              lvl=p.get("connection_level", "")))
        rows.append(dict(name=r["name"], ground=r["ground"],
                         tp=r["type_pair"], langs=r["languages"],
                         units=units, pairs=pairs))
    rows.sort(key=lambda r: (r["ground"], r["tp"], r["name"]))
    return dict(z3=doc["z3"], lifter=doc["lifter"], tally=doc["tally"],
                units_considered=doc["units_considered"],
                distinct_pairs=doc["distinct_pairs"],
                newly_paired=doc["newly_paired"],
                connection_levels=doc["connection_levels"],
                rows=rows)


HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>Operator-equivalence group explorer (machine-form rows)</title>
<style>
:root{
  --bg:#f6f5f2; --panel:#ffffff; --ink:#1c1c1c; --muted:#6b6b6b;
  --border:#d8d5cf; --hull:#e9e6df; --hull-border:#b9b4a9;
  --c-c:#2b6cb0; --c-cpp:#c05621; --c-go:#2f855a; --c-rust:#9b2c2c;
  --c-swift:#805ad5; --gray:#9a9a9a; --dbd:#c53030; --accent:#1c1c1c;
}
@media (prefers-color-scheme: dark){
  :root{
    --bg:#17181a; --panel:#202124; --ink:#e8e6e1; --muted:#9a9a9a;
    --border:#3a3b3d; --hull:#2a2c2f; --hull-border:#46484b;
    --c-c:#6ea8dc; --c-cpp:#e2985c; --c-go:#6fbf8f; --c-rust:#e08787;
    --c-swift:#b39ddb; --gray:#6f7276; --dbd:#e07070; --accent:#e8e6e1;
  }
}
*{box-sizing:border-box;}
body{margin:0;background:var(--bg);color:var(--ink);
  font:14px/1.4 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;}
header{padding:14px 18px;border-bottom:1px solid var(--border);
  display:flex;align-items:center;gap:16px;flex-wrap:wrap;}
header h1{font-size:15px;margin:0;font-weight:600;}
header .sub{color:var(--muted);font-size:12px;}
button.nav{background:var(--panel);border:1px solid var(--border);
  color:var(--ink);border-radius:6px;padding:5px 10px;cursor:pointer;font-size:12px;}
button.nav:hover{border-color:var(--accent);}
main{padding:18px;}

/* the id-vs-class specificity fix, carried over unchanged:
   hidden by id, shown by id+class, so the shown rule wins. */
#overview-view, #detail-view{display:none;}
#overview-view.active, #detail-view.active{display:block;}

#search{padding:6px 10px;border:1px solid var(--border);border-radius:6px;
  background:var(--panel);color:var(--ink);width:380px;font-size:13px;}
#rowlist{margin-top:14px;border:1px solid var(--border);border-radius:8px;overflow:hidden;}
.rowitem{display:flex;align-items:center;gap:14px;padding:8px 12px;
  border-bottom:1px solid var(--border);cursor:pointer;background:var(--panel);}
.rowitem:last-child{border-bottom:none;}
.rowitem:hover{background:var(--hull);}
.rowitem .label{width:520px;font-family:ui-monospace,SFMono-Regular,Menlo,monospace;
  font-size:12px;flex:none;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
.rowitem .langs{width:60px;color:var(--muted);flex:none;font-size:12px;}
.dots{display:flex;gap:3px;align-items:center;}
.dot{width:9px;height:9px;border-radius:50%;display:inline-block;}
.mini-legend{color:var(--muted);font-size:11px;margin-left:auto;flex:none;}
.controls{display:flex;align-items:center;gap:18px;flex-wrap:wrap;margin-bottom:10px;}
.controls select{padding:5px 8px;border:1px solid var(--border);border-radius:6px;
  background:var(--panel);color:var(--ink);font-size:13px;max-width:640px;}
#slider-wrap{display:flex;align-items:center;gap:10px;}
#tierlabel{font-weight:600;min-width:230px;}
input[type=range]{width:260px;}
.legend{display:flex;gap:12px;flex-wrap:wrap;color:var(--muted);font-size:12px;margin:6px 0 12px;}
.legend span.sw{width:10px;height:10px;border-radius:50%;display:inline-block;margin-right:4px;vertical-align:-1px;}
svg{background:var(--panel);border:1px solid var(--border);border-radius:10px;display:block;max-width:100%;}
.node text{fill:var(--ink);font-size:11px;}
#tooltip{position:fixed;pointer-events:none;background:var(--panel);
  border:1px solid var(--border);border-radius:6px;padding:6px 9px;font-size:12px;
  max-width:360px;box-shadow:0 4px 14px rgba(0,0,0,.25);display:none;z-index:10;color:var(--ink);}
footer{padding:14px 18px;color:var(--muted);font-size:11px;
  border-top:1px solid var(--border);margin-top:10px;}
.demo-note{color:var(--muted);font-size:12px;margin-top:8px;max-width:760px;}
</style>
</head>
<body>

<header>
  <h1>Operator-equivalence group explorer</h1>
  <span class="sub">rows are machine-form groups &middot; c / cpp / go / rust / swift</span>
  <button class="nav" id="btn-overview">Overview</button>
</header>

<main>

  <section id="overview-view">
    <p>Every group the machine-form candidate set produced: a byte
    cluster, an anchored-sem cluster, or a shared-core connection, on
    one operand type pair. Rows are named by the shared machine form,
    never by an operator token. Click a row to inspect it.</p>
    <input id="search" placeholder="Filter by machine form or type pair, e.g. Xor32 or bool,bool">
    <div class="mini-legend" style="margin-top:6px">dots = largest merged group reached at: byte &rarr; +sem &rarr; +z3 &nbsp;&middot;&nbsp; red dot = has a differs-by-design pair</div>
    <div id="rowlist"></div>
  </section>

  <section id="detail-view">
    <div class="controls">
      <label>Group: <select id="rowselect"></select></label>
      <div id="slider-wrap">
        <input type="range" min="0" max="3" value="0" step="1" id="tierslider">
        <span id="tierlabel"></span>
      </div>
    </div>
    <div class="legend" id="legend"></div>
    <svg id="canvas" width="920" height="480" viewBox="0 0 920 480"></svg>
    <div class="demo-note" id="rownote"></div>
  </section>

</main>

<footer>
  Byte matches are artifact facts (identical machine bytes). Sem and z3
  matches are all-runs bounds resting on the lifter; they hold for every
  input the lifted model covers, not beyond it. Operator tokens on this
  page are display labels on members only: no row, group, dropdown entry
  or comparison scope is keyed on one.
</footer>

<div id="tooltip"></div>

<script type="application/json" id="data">"""

TAIL = """</script>
<script>
'use strict';
var DATA = JSON.parse(document.getElementById('data').textContent);
var ROWS = DATA.rows;

var LANGS = ['c','cpp','go','rust','swift'];
var LANG_LABEL = {c:'C', cpp:'C++', go:'Go', rust:'Rust', swift:'Swift'};
var LANG_COLOR = {c:'var(--c-c)', cpp:'var(--c-cpp)', go:'var(--c-go)',
                  rust:'var(--c-rust)', swift:'var(--c-swift)'};

var TIER_GROUNDS = [
  ['byte identity'],
  ['byte identity', 'sem identity (anchored)'],
  ['byte identity', 'sem identity (anchored)',
   'z3 over the two lifted forms', 'z3 over the two lifted forms (tier 1)'],
  ['byte identity', 'sem identity (anchored)',
   'z3 over the two lifted forms', 'z3 over the two lifted forms (tier 1)']
];
var TIER_LABELS = [
  'Tier 1 \\u00b7 byte identity only',
  'Tier 2 \\u00b7 + anchored sem identity',
  'Tier 3 \\u00b7 + z3 proofs',
  'Tier 4 \\u00b7 + differs-by-design links'
];
var TIER_SHOW_DBD = [false, false, false, true];

function unitIds(row){ return row.units.map(function(u){ return u.u; }); }
function unitLabel(row, id){
  var hit = null;
  row.units.forEach(function(u){ if (u.u === id) hit = u; });
  return hit;
}
function unitLang(u){ return u.split('/')[0]; }

function UnionFind(items){
  this.parent = {};
  items.forEach(function(i){ this.parent[i] = i; }, this);
}
UnionFind.prototype.find = function(x){
  while (this.parent[x] !== x){ this.parent[x] = this.parent[this.parent[x]]; x = this.parent[x]; }
  return x;
};
UnionFind.prototype.union = function(a, b){
  var ra = this.find(a), rb = this.find(b);
  if (ra !== rb) this.parent[ra] = rb;
};

function groupsForTier(row, tier){
  var allowed = TIER_GROUNDS[tier];
  var ids = unitIds(row);
  var uf = new UnionFind(ids);
  row.pairs.forEach(function(p){
    if (p.v === 'MATCHED' && allowed.indexOf(p.g) !== -1) uf.union(p.a, p.b);
  });
  var buckets = {};
  ids.forEach(function(u){
    var r = uf.find(u);
    (buckets[r] = buckets[r] || []).push(u);
  });
  return Object.keys(buckets).map(function(k){ return buckets[k]; });
}

function reasonsFor(row, unit){
  return row.pairs.filter(function(p){ return p.a === unit || p.b === unit; })
    .map(function(p){
      var other = p.a === unit ? p.b : p.a;
      return other + ': ' + p.v.toLowerCase() + ' (' + p.g + ') \\u2014 ' + p.d;
    });
}

function layoutRow(row, tier){
  var groups = groupsForTier(row, tier);
  groups.sort(function(a,b){ return LANGS.indexOf(unitLang(a[0])) - LANGS.indexOf(unitLang(b[0])); });
  var NODE_R = 22, PAD = 22, GAP = 34, SPACING = 78, ROWSTEP = 74;
  var boxes = groups.map(function(g){
    var k = g.length;
    var perRow = k <= 3 ? k : Math.ceil(k / 2);
    var rows = Math.ceil(k / perRow);
    return { g: g, perRow: perRow, rows: rows,
      w: PAD * 2 + (perRow - 1) * SPACING + NODE_R * 2,
      h: PAD * 2 + (rows - 1) * ROWSTEP + NODE_R * 2 };
  });
  var totalW = boxes.reduce(function(s,b){ return s + b.w; }, 0) + GAP * (boxes.length - 1);
  var cx = 460 - totalW / 2;
  var cy = 240;
  var nodePos = {};
  var groupBoxes = [];
  boxes.forEach(function(b){
    var top = cy - b.h / 2;
    groupBoxes.push({ x: cx, y: top, w: b.w, h: b.h, size: b.g.length });
    b.g.forEach(function(u, i){
      var row2 = Math.floor(i / b.perRow), col = i % b.perRow;
      var rowCount = (row2 === b.rows - 1) ? (b.g.length - row2 * b.perRow) : b.perRow;
      var rowW = (rowCount - 1) * SPACING;
      var x = cx + b.w / 2 - rowW / 2 + col * SPACING;
      var y = top + PAD + NODE_R + row2 * ROWSTEP;
      nodePos[u] = { x: x, y: y };
    });
    cx += b.w + GAP;
  });
  return { groupBoxes: groupBoxes, nodePos: nodePos, nodeR: NODE_R };
}

var SVGNS = 'http://www.w3.org/2000/svg';
function el(name, attrs){
  var e = document.createElementNS(SVGNS, name);
  for (var k in attrs) e.setAttribute(k, attrs[k]);
  return e;
}
var tooltip = document.getElementById('tooltip');
function showTip(evt, html){
  tooltip.innerHTML = html;
  tooltip.style.display = 'block';
  tooltip.style.left = (evt.clientX + 14) + 'px';
  tooltip.style.top = (evt.clientY + 14) + 'px';
}
function hideTip(){ tooltip.style.display = 'none'; }

var currentRow = 0, currentTier = 0;

function renderLegend(){
  var l = document.getElementById('legend');
  l.innerHTML = LANGS.map(function(la){
    return '<span><span class="sw" style="background:' + LANG_COLOR[la] + '"></span>' + LANG_LABEL[la] + '</span>';
  }).join('') + '<span><span class="sw" style="background:var(--gray)"></span>isolated at this tier</span>' +
    '<span><span class="sw" style="background:var(--dbd)"></span>differs-by-design</span>';
}

function rowLabel(row){
  return row.name;
}

function renderDetail(){
  var row = ROWS[currentRow];
  document.getElementById('tierlabel').textContent = TIER_LABELS[currentTier];
  var svg = document.getElementById('canvas');
  svg.innerHTML = '';
  var showDbd = TIER_SHOW_DBD[currentTier];
  var layout = layoutRow(row, currentTier);
  var groupsThisTier = groupsForTier(row, currentTier);
  var multiMember = {};
  groupsThisTier.forEach(function(g){ if (g.length > 1) g.forEach(function(u){ multiMember[u] = true; }); });

  layout.groupBoxes.forEach(function(b){
    if (b.size < 2) return;
    svg.appendChild(el('rect', { x: b.x, y: b.y, width: b.w, height: b.h,
      rx: 18, ry: 18, fill: 'var(--hull)', stroke: 'var(--hull-border)',
      'stroke-width': 1.5 }));
  });

  if (showDbd){
    row.pairs.forEach(function(p){
      if (p.v !== 'DIFFERS-BY-DESIGN') return;
      var pa = layout.nodePos[p.a], pb = layout.nodePos[p.b];
      if (!pa || !pb) return;
      var line = el('line', { x1: pa.x, y1: pa.y, x2: pb.x, y2: pb.y,
        stroke: 'var(--dbd)', 'stroke-width': 2, 'stroke-dasharray': '6 5' });
      line.addEventListener('mousemove', function(e){
        showTip(e, '<b>differs by design</b><br>' + p.d);
      });
      line.addEventListener('mouseleave', hideTip);
      svg.appendChild(line);
    });
  }

  unitIds(row).forEach(function(u){
    var pos = layout.nodePos[u];
    if (!pos) return;
    var lang = unitLang(u);
    var isolated = !multiMember[u];
    var g = el('g', { class: 'node', transform: 'translate(' + pos.x + ',' + pos.y + ')' });
    g.appendChild(el('circle', { r: layout.nodeR,
      fill: isolated ? 'var(--gray)' : LANG_COLOR[lang],
      stroke: 'var(--ink)', 'stroke-opacity': 0.15, 'stroke-width': 1 }));
    var label = el('text', { 'text-anchor': 'middle', y: 4 });
    label.textContent = LANG_LABEL[lang];
    label.setAttribute('fill', '#fff');
    label.setAttribute('font-weight', '600');
    g.appendChild(label);
    g.addEventListener('mousemove', function(e){
      var info = unitLabel(row, u);
      var html = '<b>' + LANG_LABEL[lang] + '</b> &middot; ' + u;
      if (info) html += '<br>label on this member: <code>' + info.operator + '</code>';
      if (isolated){
        var reasons = reasonsFor(row, u);
        html += '<br>' + (reasons.length ? reasons.join('<br>') : 'no comparable unit');
      } else {
        html += '<br>merged at ' + TIER_LABELS[currentTier].toLowerCase();
      }
      showTip(e, html);
    });
    g.addEventListener('mouseleave', hideTip);
    svg.appendChild(g);
  });

  document.getElementById('rownote').textContent =
    row.units.length + ' unit(s) across ' + row.langs.length +
    ' language(s); grouped by ' + row.ground +
    ' evidence on operand types (' + row.tp + ').';
}

function populateRowSelect(){
  var sel = document.getElementById('rowselect');
  sel.innerHTML = ROWS.map(function(r, i){
    return '<option value="' + i + '">' + rowLabel(r) + '</option>';
  }).join('');
}

document.getElementById('rowselect').addEventListener('change', function(e){
  currentRow = parseInt(e.target.value, 10);
  renderDetail();
});
document.getElementById('tierslider').addEventListener('input', function(e){
  currentTier = parseInt(e.target.value, 10);
  renderDetail();
});

function tierDot(row, groundList){
  var ids = unitIds(row);
  var uf = new UnionFind(ids);
  row.pairs.forEach(function(p){
    if (p.v === 'MATCHED' && groundList.indexOf(p.g) !== -1) uf.union(p.a, p.b);
  });
  var biggest = 0, buckets = {};
  ids.forEach(function(u){ var r = uf.find(u); buckets[r] = (buckets[r]||0)+1; });
  Object.keys(buckets).forEach(function(k){ biggest = Math.max(biggest, buckets[k]); });
  return biggest;
}

function renderOverview(filter){
  var list = document.getElementById('rowlist');
  list.innerHTML = '';
  var f = (filter || '').toLowerCase().trim();
  ROWS.forEach(function(row, i){
    var label = rowLabel(row);
    if (f && label.toLowerCase().indexOf(f) === -1) return;
    var n1 = tierDot(row, TIER_GROUNDS[0]);
    var n2 = tierDot(row, TIER_GROUNDS[1]);
    var n3 = tierDot(row, TIER_GROUNDS[2]);
    var hasDbd = row.pairs.some(function(p){ return p.v === 'DIFFERS-BY-DESIGN'; });
    var item = document.createElement('div');
    item.className = 'rowitem';
    item.innerHTML =
      '<div class="label">' + label + '</div>' +
      '<div class="langs">' + row.langs.length + ' langs</div>' +
      '<div class="dots">' +
        '<span class="dot" style="background:var(--muted)"></span>' +
        '<span class="dot" style="background:var(--c-go)"></span>' +
        '<span class="dot" style="background:var(--c-c)"></span>' +
        (hasDbd ? '<span class="dot" style="background:var(--dbd)"></span>' : '') +
      '</div>' +
      '<div class="mini-legend">' + n1 + ' &rarr; ' + n2 + ' &rarr; ' + n3 + ' of ' + row.units.length + '</div>';
    item.addEventListener('click', function(){
      currentRow = i; currentTier = 0;
      document.getElementById('rowselect').value = i;
      document.getElementById('tierslider').value = 0;
      renderDetail();
      showView('detail');
    });
    list.appendChild(item);
  });
}

document.getElementById('search').addEventListener('input', function(e){
  renderOverview(e.target.value);
});

function showView(name){
  document.getElementById('overview-view').className = name === 'overview' ? 'active' : '';
  document.getElementById('detail-view').className = name === 'detail' ? 'active' : '';
}
document.getElementById('btn-overview').addEventListener('click', function(){ showView('overview'); });

renderLegend();
populateRowSelect();
renderOverview('');
var demoIdx = -1;
ROWS.forEach(function(r, i){
  if (demoIdx >= 0) return;
  if (r.tp === 'bool,bool' && r.ground === 'cluster' && r.units.length >= 5) demoIdx = i;
});
currentRow = demoIdx >= 0 ? demoIdx : 0;
document.getElementById('rowselect').value = currentRow;
renderDetail();
showView('detail');
</script>
</body>
</html>
"""


def main():
    data = payload()
    text = json.dumps(data)
    out = HEAD + text + TAIL
    path = os.path.join(HERE, "cluster_explorer2.html")
    open(path, "w").write(out)
    print("wrote %s (%d bytes)" % (os.path.basename(path), len(out)))
    print("   rows          %d" % len(data["rows"]))
    print("   cluster rows  %d"
          % sum(1 for r in data["rows"] if r["ground"] == "cluster"))
    print("   connection rows %d"
          % sum(1 for r in data["rows"] if r["ground"] == "connection"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
