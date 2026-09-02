#!/usr/bin/env python3
"""build_dominant_explorer.py -- write dominant_explorer.html.

One page for everything the operator line has produced so far.  It
SUPERSEDES cluster_explorer2.html by including that page's instrument
as its second view.

  1. Table view (default) -- the dominant-operator table: one card per
     core equivalence class on one operand type pair.  Members are
     language chips carrying the operator token as a DISPLAY LABEL.
     The canonical core is collapsed and expandable.  Mode fences are
     badges; the condition is on the badge's hover text.  The weakest
     evidence in the class is shown as its own indicator, because a
     transitively closed class is only as strong as its weakest edge.
     `intention` is null on every card; the mechanical hint is shown
     as a "proposed" tag.
  2. Evidence view -- the tier slider (byte -> +sem -> +z3 ->
     +modes/differs edges) over the class's machine-form
     neighbourhood: every measured pair with one foot in the class.
  3. Landscape view -- every class as one dot: x = the operand type
     family, y = how many languages the class spans, colour = the
     weakest evidence, red ring = the class carries mode differences.

THE SPELLING BAN.  No dropdown entry, filter, group, row or dot is
named or keyed by an operator token.  The token is written once per
member, as a label on a unit chip.  Run check_no_spelling_keys.py
--html on the product.

usage:
  build_dominant_explorer.py
"""

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

LANGS = ["c", "cpp", "go", "rust", "swift"]

PAIR_CAP = 80


def clip(text, n=160):
    if text is None:
        return ""
    text = str(text)
    if len(text) <= n:
        return text
    return text[:n - 1] + "…"


def neighbourhood(table, v3b, v4):
    """for every class, the measured pairs with at least one foot in
    it.  These are the edges the evidence view walks."""
    member_class = {}
    for row in table["rows"]:
        for m in row["members"]:
            member_class[m["unit"]] = row["class_id"]
    # two budgets, so a big class's own pairs cannot crowd out the
    # neighbours -- the neighbours are what the tier slider is for.
    inside = {}
    outside = {}
    for row in table["rows"]:
        inside[row["class_id"]] = []
        outside[row["class_id"]] = []
    seen = {}
    for src, kind in [(v3b, "verdict"), (v4, "column")]:
        for r in src["rows"]:
            for p in r.get("pairs", []):
                left = p["left"]
                right = p["right"]
                cid = member_class.get(left)
                if cid is None:
                    cid = member_class.get(right)
                if cid is None:
                    continue
                key = (cid, left, right, kind)
                if key in seen:
                    continue
                seen[key] = True
                both = (member_class.get(left) == cid
                        and member_class.get(right) == cid)
                if both:
                    bucket = inside[cid]
                else:
                    bucket = outside[cid]
                if len(bucket) >= PAIR_CAP:
                    continue
                rec = {}
                rec["a"] = left
                rec["b"] = right
                if kind == "verdict":
                    rec["v"] = p.get("verdict")
                    rec["g"] = p.get("ground", "")
                    rec["d"] = clip(p.get("detail", ""))
                else:
                    rec["v"] = "COLUMN"
                    rec["g"] = p.get("column", "")
                    rec["d"] = ""
                bucket.append(rec)
    out = {}
    for cid in inside:
        out[cid] = inside[cid] + outside[cid]
    return out, member_class


def unit_labels(table, member_class):
    """the display label of every unit that appears on the page."""
    out = {}
    for row in table["rows"]:
        for m in row["members"]:
            rec = {}
            rec["lang"] = m["lang"]
            rec["n"] = m["n"]
            rec["operator"] = m["operator"]
            rec["klass"] = row["class_id"]
            out[m["unit"]] = rec
    return out


def type_family(type_pair):
    lhs = type_pair.split(",")[0]
    if lhs == "bool":
        return "bool"
    if lhs.startswith("f"):
        return "float"
    if lhs.startswith("i") or lhs.startswith("u"):
        return "int " + lhs[1:]
    return "other"


def payload():
    table = json.load(open(os.path.join(HERE, "dominant_table.json")))
    v3b = json.load(open(os.path.join(HERE, "verdicts3b.json")))
    v4 = json.load(open(os.path.join(HERE, "verdicts4.json")))
    nbr, member_class = neighbourhood(table, v3b, v4)
    labels = unit_labels(table, member_class)

    classes = []
    for row in table["rows"]:
        c = {}
        c["id"] = row["class_id"]
        c["tp"] = row["type_pair"]
        c["fam"] = type_family(row["type_pair"])
        c["size"] = row["size"]
        c["langs"] = row["languages"]
        c["members"] = []
        for m in row["members"]:
            c["members"].append(dict(unit=m["unit"], lang=m["lang"],
                                     n=m["n"], operator=m["operator"]))
        c["core"] = row["canonical_core"]
        c["core_from"] = row["canonical_core_from"]
        c["core_texts"] = row["distinct_core_texts"]
        fences = []
        for rec in row["mode_inventory"]:
            for f in rec["fences"]:
                fences.append(dict(unit=rec["unit"], lang=rec["lang"],
                                   n=rec["n"], operator=rec["operator"],
                                   condition=f["condition"],
                                   kind=f["response_kind"],
                                   raw=f["response_raw"],
                                   detection=f["detection"],
                                   name=f["interval_probe_name"]))
        c["fences"] = fences
        border = []
        for b in row["divergence_at_the_border"][:8]:
            item = {}
            item["kind"] = b["kind"]
            item["a"] = b["left"]
            item["b"] = b["right"]
            conds = []
            for x in b.get("divergence_conditions", []):
                conds.append(clip(x.get("condition")))
            for x in b.get("modes_only_left", []):
                conds.append(clip(x.get("condition")))
            for x in b.get("modes_only_right", []):
                conds.append(clip(x.get("condition")))
            item["conditions"] = conds
            item["other"] = b.get("other_class")
            border.append(item)
        c["border"] = border
        c["ev"] = row["evidence"]["member_pairs_by_class"]
        c["weakest"] = row["evidence"]["weakest_evidence"]
        c["weakest_text"] = row["evidence"]["weakest_evidence_text"]
        c["carried"] = row["evidence"][
            "member_pairs_carried_from_an_earlier_pass"]
        absent = []
        for a in row["coverage"]["languages_absent"]:
            absent.append(dict(lang=a["language"], why=clip(a["reason"],
                                                            220)))
        c["absent"] = absent
        c["hint"] = row["intention_candidates"]["proposed_ur_kind"]
        c["hint_why"] = row["intention_candidates"]["why"]
        c["hint_op"] = row["intention_candidates"]["from_top_operation"]
        c["pairs"] = nbr[row["class_id"]]
        classes.append(c)

    out = {}
    out["classes"] = classes
    out["labels"] = labels
    out["stats"] = table["stats"]
    out["units_considered"] = table["units_considered"]
    out["edges_used"] = table["edges_used"]
    out["lifter"] = table["lifter"]
    out["z3"] = table["z3"]
    out["languages"] = LANGS
    return out


HEAD = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>The dominant-operator table &middot; explorer</title>
<style>
:root{
  --bg:#f6f5f2; --panel:#ffffff; --ink:#1c1c1c; --muted:#6b6b6b;
  --border:#d8d5cf; --hull:#e9e6df; --hull-border:#b9b4a9;
  --c-c:#2b6cb0; --c-cpp:#c05621; --c-go:#2f855a; --c-rust:#9b2c2c;
  --c-swift:#805ad5; --gray:#9a9a9a; --dbd:#c53030; --accent:#1c1c1c;
  --byte:#2f855a; --sem:#2b6cb0; --coretext:#b7791f; --z3:#805ad5;
  --none:#9a9a9a;
}
@media (prefers-color-scheme: dark){
  :root{
    --bg:#17181a; --panel:#202124; --ink:#e8e6e1; --muted:#9a9a9a;
    --border:#3a3b3d; --hull:#2a2c2f; --hull-border:#46484b;
    --c-c:#6ea8dc; --c-cpp:#e2985c; --c-go:#6fbf8f; --c-rust:#e08787;
    --c-swift:#b39ddb; --gray:#6f7276; --dbd:#e07070; --accent:#e8e6e1;
    --byte:#6fbf8f; --sem:#6ea8dc; --coretext:#e0b055; --z3:#b39ddb;
    --none:#6f7276;
  }
}
*{box-sizing:border-box;}
body{margin:0;background:var(--bg);color:var(--ink);
  font:14px/1.45 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;}
header{padding:14px 18px;border-bottom:1px solid var(--border);
  display:flex;align-items:center;gap:14px;flex-wrap:wrap;}
header h1{font-size:15px;margin:0;font-weight:600;}
header .sub{color:var(--muted);font-size:12px;}
button.nav{background:var(--panel);border:1px solid var(--border);
  color:var(--ink);border-radius:6px;padding:5px 10px;cursor:pointer;font-size:12px;}
button.nav:hover{border-color:var(--accent);}
main{padding:18px;}

/* hidden by id, shown by id+class, so the shown rule wins */
#table-view, #evidence-view, #landscape-view{display:none;}
#table-view.active, #evidence-view.active, #landscape-view.active{display:block;}

.controls{display:flex;align-items:center;gap:14px;flex-wrap:wrap;margin-bottom:12px;}
.controls select, .controls input[type=text]{padding:5px 8px;
  border:1px solid var(--border);border-radius:6px;background:var(--panel);
  color:var(--ink);font-size:13px;max-width:520px;}
.note{color:var(--muted);font-size:12px;}
.card{background:var(--panel);border:1px solid var(--border);border-radius:10px;
  padding:12px 14px;margin-bottom:10px;}
.card h3{margin:0 0 6px;font-size:13px;font-weight:600;
  font-family:ui-monospace,SFMono-Regular,Menlo,monospace;}
.chips{display:flex;gap:6px;flex-wrap:wrap;margin:6px 0;}
.chip{border-radius:12px;padding:2px 9px;font-size:12px;color:#fff;}
.chip code{background:rgba(255,255,255,.22);border-radius:4px;padding:0 4px;}
.badge{display:inline-block;border-radius:6px;padding:1px 7px;font-size:11px;
  margin:2px 4px 2px 0;border:1px solid var(--border);background:var(--hull);}
.badge.panic{border-color:var(--dbd);color:var(--dbd);}
.badge.trap{border-color:var(--dbd);color:var(--dbd);}
.tag{display:inline-block;border:1px dashed var(--border);border-radius:6px;
  padding:1px 7px;font-size:11px;color:var(--muted);}
.weak{display:inline-block;width:9px;height:9px;border-radius:50%;
  margin-right:5px;vertical-align:-1px;}
details{margin:6px 0;}
details pre{background:var(--hull);border:1px solid var(--border);border-radius:6px;
  padding:8px;overflow-x:auto;font-size:12px;margin:6px 0 0;}
svg{background:var(--panel);border:1px solid var(--border);border-radius:10px;
  display:block;max-width:100%;}
.node text{fill:var(--ink);font-size:11px;}
#tooltip{position:fixed;pointer-events:none;background:var(--panel);
  border:1px solid var(--border);border-radius:6px;padding:6px 9px;font-size:12px;
  max-width:380px;box-shadow:0 4px 14px rgba(0,0,0,.25);display:none;z-index:10;
  color:var(--ink);}
.legend{display:flex;gap:12px;flex-wrap:wrap;color:var(--muted);font-size:12px;
  margin:6px 0 12px;}
.legend .sw{width:10px;height:10px;border-radius:50%;display:inline-block;
  margin-right:4px;vertical-align:-1px;}
footer{padding:14px 18px;color:var(--muted);font-size:11px;
  border-top:1px solid var(--border);margin-top:10px;}
#tierlabel{font-weight:600;min-width:240px;display:inline-block;}
input[type=range]{width:250px;vertical-align:middle;}
table.stats{border-collapse:collapse;font-size:12px;margin:6px 0 14px;}
table.stats td{border:1px solid var(--border);padding:3px 8px;}
</style>
</head>
<body>

<header>
  <h1>The dominant-operator table</h1>
  <span class="sub">step 8 &middot; c / cpp / go / rust / swift &middot; classes are machine-form, never spelling</span>
  <button class="nav" id="btn-table">Table</button>
  <button class="nav" id="btn-evidence">Evidence</button>
  <button class="nav" id="btn-landscape">Landscape</button>
</header>

<main>

  <section id="table-view">
    <div class="controls">
      <label>language present:
        <select id="f-lang"><option value="">any</option></select></label>
      <label>modes:
        <select id="f-modes">
          <option value="">any</option>
          <option value="yes">carries fences</option>
          <option value="no">no fence</option>
        </select></label>
      <label>weakest evidence:
        <select id="f-ev"><option value="">any</option></select></label>
      <label>operand type pair:
        <select id="f-tp"><option value="">any</option></select></label>
      <label>sort:
        <select id="f-sort">
          <option value="size">class size (largest first)</option>
          <option value="langs">languages spanned</option>
          <option value="id">class id</option>
        </select></label>
    </div>
    <div class="note" id="tablenote"></div>
    <div id="cards"></div>
  </section>

  <section id="evidence-view">
    <div class="controls">
      <label>class: <select id="classselect"></select></label>
      <span>
        <input type="range" min="0" max="3" value="0" step="1" id="tierslider">
        <span id="tierlabel"></span>
      </span>
    </div>
    <div class="legend" id="ev-legend"></div>
    <svg id="canvas" width="920" height="470" viewBox="0 0 920 470"></svg>
    <div class="note" id="evnote"></div>
  </section>

  <section id="landscape-view">
    <div class="note">Every core class as one dot. x = the operand
    type family of the class; y = how many of the five languages the
    class spans; colour = the weakest evidence any edge inside it
    rests on; a red ring means the class carries mode differences (a
    fence on a member, or a divergence at its border). Click a dot to
    open its card.</div>
    <div class="legend" id="ls-legend"></div>
    <svg id="landscape" width="920" height="520" viewBox="0 0 920 520"></svg>
  </section>

</main>

<footer>
  Byte identity is an artifact fact. Anchored sem identity is a fact
  about the lifted forms. z3 proves things about the lifter's MODEL of
  the machine, which is testimony. A class is the transitive closure of
  its edges and is only as strong as its weakest one, which every card
  states. `intention` is null everywhere on this page: the hint shown is
  mechanical and proposed, and the owner settles ur_kind. Operator tokens
  appear only as display labels on member chips.
</footer>

<div id="tooltip"></div>

<script type="application/json" id="data">"""


TAIL = """</script>
<script>
'use strict';
var DATA = JSON.parse(document.getElementById('data').textContent);
var CLASSES = DATA.classes;
var LABELS = DATA.labels;
var LANGS = DATA.languages;
var LANG_LABEL = {c:'C', cpp:'C++', go:'Go', rust:'Rust', swift:'Swift'};
var LANG_COLOR = {c:'var(--c-c)', cpp:'var(--c-cpp)', go:'var(--c-go)',
                  rust:'var(--c-rust)', swift:'var(--c-swift)'};
var EV_COLOR = {byte:'var(--byte)', sem:'var(--sem)',
                'core-text':'var(--coretext)', z3:'var(--z3)',
                'null':'var(--none)'};

var BY_ID = {};
CLASSES.forEach(function(c){ BY_ID[c.id] = c; });

function evKey(c){
  if (c.weakest === null || c.weakest === undefined) return 'null';
  return c.weakest;
}

function hasModes(c){
  if (c.fences.length > 0) return true;
  if (c.border.length > 0) return true;
  return false;
}

/* ------------------------------------------------------ table view */

function classTitle(c){
  var text = c.id + '  \\u00b7  operand types (' + c.tp + ')';
  text = text + '  \\u00b7  ' + c.size + ' member(s), ';
  text = text + c.langs.length + ' language(s)';
  return text;
}

function memberChips(c){
  var out = '';
  c.members.forEach(function(m){
    out += '<span class="chip" style="background:' + LANG_COLOR[m.lang] +
           '">' + LANG_LABEL[m.lang] + ' <code>' + escapeText(m.operator) +
           '</code> <span style="opacity:.8">op_' + m.n + '</span></span>';
  });
  return out;
}

function escapeText(text){
  var s = String(text);
  s = s.split('&').join('&amp;');
  s = s.split('<').join('&lt;');
  s = s.split('>').join('&gt;');
  return s;
}

function fenceBadges(c){
  if (c.fences.length === 0) return '<span class="note">no member carries a fence</span>';
  var out = '';
  c.fences.forEach(function(f){
    var cls = 'badge';
    if (f.kind === 'trap') cls = 'badge trap';
    if (f.kind === 'panic-call') cls = 'badge panic';
    var name = f.name ? (' \\u00b7 ' + f.name) : '';
    var hover = f.lang + ' op_' + f.n + ': when ' + f.condition +
                ' \\u2192 ' + f.raw + ' (' + f.detection + ')';
    out += '<span class="' + cls + '" title="' + escapeText(hover) + '">' +
           LANG_LABEL[f.lang] + ': ' + escapeText(f.kind) + escapeText(name) +
           '</span>';
  });
  return out;
}

function borderText(c){
  if (c.border.length === 0) return '<span class="note">no divergence recorded at the border of this class</span>';
  var out = '<ul style="margin:4px 0 0 16px;padding:0;font-size:12px">';
  c.border.forEach(function(b){
    var conds = b.conditions.length ? b.conditions.join('; ') : '(condition not recorded)';
    out += '<li>' + escapeText(b.kind) + ': ' + b.a + ' vs ' + b.b +
           ' \\u2014 ' + escapeText(conds) + '</li>';
  });
  out += '</ul>';
  return out;
}

function absentText(c){
  if (c.absent.length === 0) return 'all five languages are present';
  var out = '<ul style="margin:4px 0 0 16px;padding:0;font-size:12px">';
  c.absent.forEach(function(a){
    out += '<li>' + LANG_LABEL[a.lang] + ': ' + escapeText(a.why) + '</li>';
  });
  out += '</ul>';
  return out;
}

function cardHtml(c){
  var ev = c.ev;
  var evText = 'byte ' + ev.byte + ' \\u00b7 sem ' + ev.sem +
               ' \\u00b7 core-text ' + (ev['core-text'] || 0) +
               ' \\u00b7 z3 ' + ev.z3 + ' \\u00b7 carried ' + c.carried;
  var html = '';
  html += '<h3>' + classTitle(c) + '</h3>';
  html += '<div class="chips">' + memberChips(c) + '</div>';
  html += '<details><summary>canonical core (from ' + c.core_from +
          '; ' + c.core_texts + ' distinct core text(s) inside the class)' +
          '</summary><pre>' + escapeText(JSON.stringify(c.core, null, 1)) +
          '</pre></details>';
  html += '<div>' + fenceBadges(c) + '</div>';
  html += '<div style="margin-top:6px"><span class="weak" style="background:' +
          EV_COLOR[evKey(c)] + '"></span><b>weakest evidence:</b> ' +
          escapeText(c.weakest_text) + '<br><span class="note">member pairs: ' +
          evText + '</span></div>';
  html += '<div style="margin-top:6px"><b>divergence at the border:</b>' +
          borderText(c) + '</div>';
  html += '<div style="margin-top:6px"><b>coverage:</b> present: ' +
          c.langs.join(', ') + absentText(c) + '</div>';
  html += '<div style="margin-top:8px"><span class="tag">intention: null' +
          '</span> <span class="tag">proposed: ' + escapeText(c.hint) +
          (c.hint_op ? (' (top operation ' + escapeText(c.hint_op) + ')') : '') +
          ' \\u2014 the owner settles</span> ' +
          '<button class="nav" data-open="' + c.id + '">Evidence</button></div>';
  return html;
}

var RENDER_CAP = 150;

function filtered(){
  var lang = document.getElementById('f-lang').value;
  var modes = document.getElementById('f-modes').value;
  var ev = document.getElementById('f-ev').value;
  var tp = document.getElementById('f-tp').value;
  var sort = document.getElementById('f-sort').value;
  var out = CLASSES.filter(function(c){
    if (lang && c.langs.indexOf(lang) === -1) return false;
    if (modes === 'yes' && !hasModes(c)) return false;
    if (modes === 'no' && hasModes(c)) return false;
    if (ev && evKey(c) !== ev) return false;
    if (tp && c.tp !== tp) return false;
    return true;
  });
  out.sort(function(a, b){
    if (sort === 'id') return a.id < b.id ? -1 : 1;
    if (sort === 'langs'){
      if (b.langs.length !== a.langs.length) return b.langs.length - a.langs.length;
      return b.size - a.size;
    }
    if (b.size !== a.size) return b.size - a.size;
    return a.id < b.id ? -1 : 1;
  });
  return out;
}

function renderTable(){
  var rows = filtered();
  var host = document.getElementById('cards');
  host.innerHTML = '';
  var shown = rows.slice(0, RENDER_CAP);
  shown.forEach(function(c){
    var div = document.createElement('div');
    div.className = 'card';
    div.id = 'card-' + c.id;
    div.innerHTML = cardHtml(c);
    host.appendChild(div);
  });
  document.getElementById('tablenote').textContent =
    'showing ' + shown.length + ' of ' + rows.length +
    ' matching class(es); ' + CLASSES.length + ' classes in the table, ' +
    DATA.units_considered + ' units considered, ' + DATA.edges_used +
    ' total-equality edges.';
  var buttons = host.querySelectorAll('button[data-open]');
  Array.prototype.forEach.call(buttons, function(b){
    b.addEventListener('click', function(){
      openEvidence(b.getAttribute('data-open'));
    });
  });
}

/* --------------------------------------------------- evidence view */

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
  'Tier 4 \\u00b7 + mode / differs-by-design edges'
];
var TIER_SHOW_DBD = [false, false, false, true];

var currentClass = 0;
var currentTier = 0;

function unitsOf(c){
  var ids = {};
  c.members.forEach(function(m){ ids[m.unit] = true; });
  c.pairs.forEach(function(p){ ids[p.a] = true; ids[p.b] = true; });
  return Object.keys(ids).sort();
}

function UnionFind(items){
  this.up = {};
  var self = this;
  items.forEach(function(i){ self.up[i] = i; });
}
UnionFind.prototype.find = function(x){
  while (this.up[x] !== x){ this.up[x] = this.up[this.up[x]]; x = this.up[x]; }
  return x;
};
UnionFind.prototype.union = function(a, b){
  var ra = this.find(a);
  var rb = this.find(b);
  if (ra !== rb) this.up[ra] = rb;
};

function groupsForTier(c, tier){
  var allowed = TIER_GROUNDS[tier];
  var ids = unitsOf(c);
  var uf = new UnionFind(ids);
  c.pairs.forEach(function(p){
    if (p.v !== 'MATCHED') return;
    if (allowed.indexOf(p.g) === -1) return;
    uf.union(p.a, p.b);
  });
  var buckets = {};
  ids.forEach(function(u){
    var r = uf.find(u);
    if (!buckets[r]) buckets[r] = [];
    buckets[r].push(u);
  });
  return Object.keys(buckets).map(function(k){ return buckets[k]; });
}

function unitLang(u){ return u.split('/')[0]; }

function layout(c, tier){
  var groups = groupsForTier(c, tier);
  groups.sort(function(a, b){
    return LANGS.indexOf(unitLang(a[0])) - LANGS.indexOf(unitLang(b[0]));
  });
  var NODE_R = 20, PAD = 18, GAP = 26, SPACING = 64, ROWSTEP = 62;
  var boxes = groups.map(function(g){
    var k = g.length;
    var perRow = k <= 3 ? k : Math.ceil(k / 2);
    var rows = Math.ceil(k / perRow);
    return { g: g, perRow: perRow, rows: rows,
      w: PAD * 2 + (perRow - 1) * SPACING + NODE_R * 2,
      h: PAD * 2 + (rows - 1) * ROWSTEP + NODE_R * 2 };
  });
  var totalW = 0;
  boxes.forEach(function(b){ totalW += b.w; });
  totalW += GAP * (boxes.length - 1);
  var scale = 1;
  if (totalW > 880) scale = 880 / totalW;
  var cx = 460 - (totalW * scale) / 2;
  var cy = 235;
  var nodePos = {};
  var groupBoxes = [];
  boxes.forEach(function(b){
    var w = b.w * scale;
    var top = cy - b.h / 2;
    groupBoxes.push({ x: cx, y: top, w: w, h: b.h, size: b.g.length });
    b.g.forEach(function(u, i){
      var r2 = Math.floor(i / b.perRow);
      var col = i % b.perRow;
      var rowCount = (r2 === b.rows - 1) ? (b.g.length - r2 * b.perRow) : b.perRow;
      var rowW = (rowCount - 1) * SPACING * scale;
      var x = cx + w / 2 - rowW / 2 + col * SPACING * scale;
      var y = top + PAD + NODE_R + r2 * ROWSTEP;
      nodePos[u] = { x: x, y: y };
    });
    cx += w + GAP;
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

function renderEvidence(){
  var c = CLASSES[currentClass];
  document.getElementById('tierlabel').textContent = TIER_LABELS[currentTier];
  var svg = document.getElementById('canvas');
  svg.innerHTML = '';
  var lay = layout(c, currentTier);
  var groups = groupsForTier(c, currentTier);
  var multi = {};
  groups.forEach(function(g){
    if (g.length > 1) g.forEach(function(u){ multi[u] = true; });
  });
  lay.groupBoxes.forEach(function(b){
    if (b.size < 2) return;
    svg.appendChild(el('rect', { x: b.x, y: b.y, width: b.w, height: b.h,
      rx: 16, ry: 16, fill: 'var(--hull)', stroke: 'var(--hull-border)',
      'stroke-width': 1.5 }));
  });
  if (TIER_SHOW_DBD[currentTier]){
    c.pairs.forEach(function(p){
      var isDbd = p.v === 'DIFFERS-BY-DESIGN';
      var isModes = p.g === 'core equality, modes differ';
      if (!isDbd && !isModes) return;
      var pa = lay.nodePos[p.a];
      var pb = lay.nodePos[p.b];
      if (!pa || !pb) return;
      var line = el('line', { x1: pa.x, y1: pa.y, x2: pb.x, y2: pb.y,
        stroke: 'var(--dbd)', 'stroke-width': 2, 'stroke-dasharray': '6 5' });
      line.addEventListener('mousemove', function(e){
        showTip(e, '<b>' + p.g + '</b><br>' + p.a + ' vs ' + p.b + '<br>' + p.d);
      });
      line.addEventListener('mouseleave', hideTip);
      svg.appendChild(line);
    });
  }
  unitsOf(c).forEach(function(u){
    var pos = lay.nodePos[u];
    if (!pos) return;
    var lang = unitLang(u);
    var isolated = !multi[u];
    var g = el('g', { 'class': 'node',
      transform: 'translate(' + pos.x + ',' + pos.y + ')' });
    var inClass = false;
    c.members.forEach(function(m){ if (m.unit === u) inClass = true; });
    g.appendChild(el('circle', { r: lay.nodeR,
      fill: isolated ? 'var(--gray)' : LANG_COLOR[lang],
      stroke: inClass ? 'var(--ink)' : 'var(--muted)',
      'stroke-opacity': inClass ? 0.7 : 0.2,
      'stroke-width': inClass ? 2.5 : 1 }));
    var t = el('text', { 'text-anchor': 'middle', y: 4 });
    t.textContent = LANG_LABEL[lang];
    t.setAttribute('fill', '#fff');
    t.setAttribute('font-weight', '600');
    g.appendChild(t);
    g.addEventListener('mousemove', function(e){
      var info = LABELS[u];
      var html = '<b>' + LANG_LABEL[lang] + '</b> &middot; ' + u;
      if (info) html += '<br>label on this member: <code>' + info.operator + '</code>';
      if (info) html += '<br>class: ' + info.klass;
      html += '<br>' + (inClass ? 'a member of this class' :
                                  'a neighbour: measured against a member');
      showTip(e, html);
    });
    g.addEventListener('mouseleave', hideTip);
    svg.appendChild(g);
  });
  var note = c.id + ': ' + c.size + ' member(s) and ' +
    (unitsOf(c).length - c.size) + ' measured neighbour(s), on operand ' +
    'types (' + c.tp + '). Weakest evidence in the class: ' + c.weakest_text;
  document.getElementById('evnote').textContent = note;
}

function openEvidence(cid){
  var idx = 0;
  CLASSES.forEach(function(c, i){ if (c.id === cid) idx = i; });
  currentClass = idx;
  currentTier = 0;
  document.getElementById('classselect').value = String(idx);
  document.getElementById('tierslider').value = '0';
  renderEvidence();
  showView('evidence');
}

/* -------------------------------------------------- landscape view */

function famList(){
  var seen = {};
  CLASSES.forEach(function(c){ seen[c.fam] = true; });
  var out = Object.keys(seen);
  out.sort();
  return out;
}

function renderLandscape(){
  var svg = document.getElementById('landscape');
  svg.innerHTML = '';
  var fams = famList();
  var x0 = 70, x1 = 890, y0 = 60, y1 = 450;
  var colW = (x1 - x0) / fams.length;
  fams.forEach(function(f, i){
    var cx = x0 + colW * i + colW / 2;
    var t = el('text', { x: cx, y: y1 + 30, 'text-anchor': 'middle',
      fill: 'var(--muted)', 'font-size': 12 });
    t.textContent = f;
    svg.appendChild(t);
  });
  for (var k = 1; k <= 5; k++){
    var y = y1 - ((k - 1) / 4) * (y1 - y0);
    var line = el('line', { x1: x0 - 20, y1: y, x2: x1, y2: y,
      stroke: 'var(--border)', 'stroke-width': 1 });
    svg.appendChild(line);
    var lab = el('text', { x: x0 - 28, y: y + 4, 'text-anchor': 'end',
      fill: 'var(--muted)', 'font-size': 11 });
    lab.textContent = k + (k === 1 ? ' language' : ' languages');
    svg.appendChild(lab);
  }
  var counters = {};
  CLASSES.forEach(function(c){
    var fi = fams.indexOf(c.fam);
    var key = c.fam + '|' + c.langs.length;
    counters[key] = (counters[key] || 0) + 1;
    var seq = counters[key];
    var cx = x0 + colW * fi + colW / 2;
    var y = y1 - ((c.langs.length - 1) / 4) * (y1 - y0);
    var ring = Math.floor((seq - 1) / 12);
    var slot = (seq - 1) % 12;
    var dx = (slot - 5.5) * 7;
    var dy = ring * 8 - 4;
    var dot = el('circle', { cx: cx + dx, cy: y + dy,
      r: 3 + Math.min(c.size, 8) * 0.5,
      fill: EV_COLOR[evKey(c)],
      stroke: hasModes(c) ? 'var(--dbd)' : 'none',
      'stroke-width': hasModes(c) ? 1.6 : 0 });
    dot.setAttribute('class', 'lsdot');
    dot.addEventListener('mousemove', function(e){
      var html = '<b>' + c.id + '</b> &middot; operand types (' + c.tp + ')' +
        '<br>' + c.size + ' member(s), ' + c.langs.length + ' language(s)' +
        '<br>weakest evidence: ' + c.weakest_text +
        '<br>' + (hasModes(c) ? 'carries mode differences' : 'no mode difference');
      showTip(e, html);
    });
    dot.addEventListener('mouseleave', hideTip);
    dot.addEventListener('click', function(){
      document.getElementById('f-lang').value = '';
      document.getElementById('f-modes').value = '';
      document.getElementById('f-ev').value = '';
      document.getElementById('f-tp').value = c.tp;
      document.getElementById('f-sort').value = 'size';
      renderTable();
      showView('table');
      var card = document.getElementById('card-' + c.id);
      if (card && card.scrollIntoView) card.scrollIntoView();
    });
    svg.appendChild(dot);
  });
}

/* --------------------------------------------------------- chrome */

function showView(name){
  document.getElementById('table-view').className =
    name === 'table' ? 'active' : '';
  document.getElementById('evidence-view').className =
    name === 'evidence' ? 'active' : '';
  document.getElementById('landscape-view').className =
    name === 'landscape' ? 'active' : '';
}

function fillFilters(){
  var lang = document.getElementById('f-lang');
  LANGS.forEach(function(l){
    var o = document.createElement('option');
    o.value = l;
    o.textContent = LANG_LABEL[l];
    lang.appendChild(o);
  });
  var evs = {};
  var tps = {};
  CLASSES.forEach(function(c){ evs[evKey(c)] = true; tps[c.tp] = true; });
  var evsel = document.getElementById('f-ev');
  Object.keys(evs).sort().forEach(function(k){
    var o = document.createElement('option');
    o.value = k;
    o.textContent = k === 'null' ? 'no edge (single-member class)' : k;
    evsel.appendChild(o);
  });
  var tpsel = document.getElementById('f-tp');
  Object.keys(tps).sort().forEach(function(k){
    var o = document.createElement('option');
    o.value = k;
    o.textContent = k;
    tpsel.appendChild(o);
  });
  var sel = document.getElementById('classselect');
  var html = '';
  CLASSES.forEach(function(c, i){
    html += '<option value="' + i + '">' + c.id + ' \\u00b7 (' + c.tp +
            ') \\u00b7 ' + c.size + ' member(s) \\u00b7 ' + c.langs.join('/') +
            '</option>';
  });
  sel.innerHTML = html;
}

function renderLegends(){
  var html = '';
  LANGS.forEach(function(l){
    html += '<span><span class="sw" style="background:' + LANG_COLOR[l] +
            '"></span>' + LANG_LABEL[l] + '</span>';
  });
  html += '<span><span class="sw" style="background:var(--gray)"></span>' +
          'isolated at this tier</span>';
  html += '<span><span class="sw" style="background:var(--dbd)"></span>' +
          'mode / differs-by-design edge</span>';
  document.getElementById('ev-legend').innerHTML = html;
  var ls = '';
  ['byte', 'sem', 'core-text', 'z3', 'null'].forEach(function(k){
    ls += '<span><span class="sw" style="background:' + EV_COLOR[k] +
          '"></span>' + (k === 'null' ? 'no edge' : k) + '</span>';
  });
  ls += '<span>red ring = carries mode differences</span>';
  document.getElementById('ls-legend').innerHTML = ls;
}

['f-lang', 'f-modes', 'f-ev', 'f-tp', 'f-sort'].forEach(function(id){
  document.getElementById(id).addEventListener('change', renderTable);
});
document.getElementById('classselect').addEventListener('change', function(e){
  currentClass = parseInt(e.target.value, 10);
  renderEvidence();
});
document.getElementById('tierslider').addEventListener('input', function(e){
  currentTier = parseInt(e.target.value, 10);
  renderEvidence();
});
document.getElementById('btn-table').addEventListener('click', function(){
  showView('table');
});
document.getElementById('btn-evidence').addEventListener('click', function(){
  showView('evidence');
});
document.getElementById('btn-landscape').addEventListener('click', function(){
  showView('landscape');
});

fillFilters();
renderLegends();
renderTable();
currentClass = 0;
renderEvidence();
renderLandscape();
showView('table');
</script>
</body>
</html>
"""


def main():
    data = payload()
    text = json.dumps(data)
    out = HEAD + text + TAIL
    path = os.path.join(HERE, "dominant_explorer.html")
    fh = open(path, "w")
    fh.write(out)
    fh.close()
    print("wrote %s (%d bytes)" % (os.path.basename(path), len(out)))
    print("   classes    %d" % len(data["classes"]))
    print("   units      %d" % len(data["labels"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
