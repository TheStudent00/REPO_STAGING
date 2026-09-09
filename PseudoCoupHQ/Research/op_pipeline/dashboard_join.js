/* dashboard_join.js -- the ONE join, shared by the live page and the snapshot.
 *
 * Node: hq.research.compiler_graph.dashboard (CORE_0_3_5_10_dashboard.md).
 * This file is the realization of the CORE's `unit_viewer`, `selector`,
 * `opcode_index`, `coverage_view` and `stats` methods, plus the style and
 * markup of the shell.  It is loaded two ways and only two ways:
 *
 *   1. dashboard.html   -- <script src="dashboard_join.js"> beside a live
 *                          source that reads the artifact folder in the
 *                          browser (dashboard_loader.js).
 *   2. dashboard_snapshot.html -- viewer_build.py embeds THIS FILE VERBATIM
 *                          beside a snapshot source whose data was pre-read
 *                          in python.  The embedded text is byte-identical
 *                          to this file; that is the shared-code proof.
 *
 * THE SOURCE INTERFACE.  Both sources answer the same seven questions, all
 * async, so the panes never know which one they are drawing:
 *
 *   source.kind          "live" | "snapshot"
 *   source.population()  {units, files, openedAt, note}
 *   source.stats()       the stats pane's record
 *   source.coverage()    the coverage pane's record
 *   source.index()       [{id, lang, opGroup, label, sig, outcome, pop}]
 *   source.opcodeIndex() {mnem: [unit id, ...]}
 *   source.unit(id)      the packed unit record (see packUnit)
 *
 * THE SPELLING BAN.  No operator token is a key here.  Every grouping,
 * selection and comparison in this file runs on `opGroup`, an opaque id
 * minted per language in first-appearance order (`c#g07`).  The token
 * rides as `label`, a display label on the member, and is read by
 * nothing but the text of an <option> and a table cell.  Opening the page
 * with `?labels=glyph` in the address replaces every label with a glyph;
 * every pane must still work, which is the CORE's stated test.
 */

/* eslint-env browser */
var DashboardJoin = (function () {
  "use strict";

  /* ---------------------------------------------------------------- *
   * 0.  small helpers
   * ---------------------------------------------------------------- */

  function esc(s) {
    if (s === null || s === undefined) {
      return "";
    }
    return String(s).replace(/[&<>]/g, function (c) {
      if (c === "&") {
        return "&amp;";
      }
      if (c === "<") {
        return "&lt;";
      }
      return "&gt;";
    });
  }

  function num(n) {
    if (n === null || n === undefined) {
      return "—";
    }
    return Number(n).toLocaleString();
  }

  function clockOf(d) {
    var hh = String(d.getHours()).padStart(2, "0");
    var mm = String(d.getMinutes()).padStart(2, "0");
    return hh + ":" + mm;
  }

  /* the label filter.  `?labels=glyph` is the spelling-ban test: it swaps
   * every operator label for one glyph.  Nothing else changes, because
   * nothing else reads the label. */
  var GLYPH_MODE = false;
  try {
    GLYPH_MODE = /(\?|&)labels=glyph/.test(window.location.search);
  } catch (e) {
    GLYPH_MODE = false;
  }

  function label(token) {
    if (GLYPH_MODE) {
      return "◆";
    }
    if (token === null || token === undefined || token === "") {
      return "—";
    }
    return token;
  }

  /* ---------------------------------------------------------------- *
   * 1.  the join -- ported from viewer_build.py, function for function
   * ---------------------------------------------------------------- */

  /* viewer_build.units_of */
  function unitsOf(doc) {
    var u = doc;
    if (doc && Object.prototype.hasOwnProperty.call(doc, "units")) {
      u = doc.units;
    }
    if (u && !Array.isArray(u) && typeof u === "object") {
      return Object.keys(u).map(function (k) {
        var row = u[k];
        if (row && !row.unit) {
          row.unit = k;
        }
        return row;
      });
    }
    if (Array.isArray(u)) {
      return u;
    }
    return [];
  }

  /* viewer_build.gloss_of */
  function glossOf(row) {
    var p = row.produced_by || {};
    if (p.kind === "non_opcode_phrase") {
      return p.phrase || "";
    }
    var who;
    if (p.kind === "flag_pair") {
      who = (p.mnem || []).join(" + ");
    } else {
      who = p.mnem || p.callee || "unnamed";
    }
    var ops = (row.operands || []).join(", ");
    var half = row.written_half;
    var tail = "";
    if (half) {
      tail = " [" + half + "]";
    }
    return row.row + " = " + who + "(" + ops + ")" + tail;
  }

  /* viewer_build.mnems_of */
  var LEADING_MNEM = /^\s*([a-z][a-z0-9]*)/;

  function mnemsOf(unit) {
    var out = {};
    var ledger = unit.ledger || [];
    var i;
    for (i = 0; i < ledger.length; i += 1) {
      var p = ledger[i].produced_by || {};
      if (p.kind === "arch_opcode") {
        out[p.mnem] = true;
      } else if (p.kind === "flag_pair") {
        (p.mnem || []).forEach(function (m) {
          out[m] = true;
        });
      } else if (p.kind === "runtime_callee") {
        out.call = true;
      }
    }
    var body = unit.body_as_read || [];
    for (i = 0; i < body.length; i += 1) {
      var m = LEADING_MNEM.exec(body[i]);
      if (m) {
        out[m[1]] = true;
      }
    }
    return Object.keys(out).sort();
  }

  /* viewer_build.signature -- the probe's declared types, with the result
   * read off the OUT row's own width when the compiler did not state it. */
  function signatureOf(probe, unit) {
    if (!probe) {
      return null;
    }
    var lhs = probe.lhs_type;
    var rhs = probe.rhs_type;
    var res = probe.result_type;
    if (!res) {
      var ledger = unit.ledger || [];
      var out = ledger.filter(function (r) {
        return String(r.row).indexOf("OUT") === 0;
      });
      if (out.length) {
        res = String(out[0].size * 8) + "-bit";
      } else {
        res = "compiler-stated";
      }
    }
    if (rhs) {
      return "(a: " + lhs + ", b: " + rhs + ") -> " + res;
    }
    return "(a: " + lhs + ") -> " + res;
  }

  /* viewer_build.census_name */
  function censusName(p) {
    if (p && typeof p === "object" && !Array.isArray(p)) {
      var m = p.mnem;
      if (Array.isArray(m)) {
        return m.join(" + ");
      }
      return m || p.phrase || p.callee || "unnamed";
    }
    if (Array.isArray(p)) {
      return p.join(" + ");
    }
    return p;
  }

  /* THE OPERATOR GROUP KEY.  A machine key minted per language, in
   * first-appearance order, so that everything the page groups, selects
   * and compares by runs on an id and never on a token.  The token is
   * carried once, beside it, as a display label.
   *
   * The one place the token is read is here, to decide which units came
   * from one probe family within ONE language.  That is generator
   * provenance -- what the probe generator asked the compiler for --
   * which check_no_spelling_keys.py exempts by name (THE
   * GENERATOR-PROVENANCE EXEMPTION, the owner 2026-08-26: the ban is on
   * spell-MATCHING).  No cross-language pairing, no comparison and no
   * verdict in this page ever touches it. */
  function OperatorGroups() {
    this.byLang = {};
    this.labels = {};
  }

  OperatorGroups.prototype.mint = function (lang, token) {
    if (token === null || token === undefined || token === "") {
      return null;
    }
    if (!this.byLang[lang]) {
      this.byLang[lang] = {};
    }
    var seen = this.byLang[lang];
    if (!seen[token]) {
      var n = Object.keys(seen).length;
      var gid = lang + "#g" + String(n).padStart(2, "0");
      seen[token] = gid;
      this.labels[gid] = token;
    }
    return seen[token];
  };

  OperatorGroups.prototype.labelOf = function (gid) {
    return this.labels[gid];
  };

  /* rebuild the gid -> display-label map from index rows.  Each token sits
   * on its own unit row (which carries `lang` and `id`), which is the one
   * placement the spelling ban allows and the one the guard exempts.  No
   * file this line writes holds a gid -> token table. */
  function groupsFromIndex(rows) {
    var g = new OperatorGroups();
    (rows || []).forEach(function (r) {
      if (!r.opGroup) {
        return;
      }
      if (!g.byLang[r.lang]) {
        g.byLang[r.lang] = {};
      }
      g.byLang[r.lang][r.label] = r.opGroup;
      g.labels[r.opGroup] = r.label;
    });
    return g;
  }

  /* viewer_build.pack -- one unit becomes the record the page shows.
   * `joins` carries what the source could resolve: probe, term, pool,
   * rendered-back. */
  function packUnit(unit, joins, groups) {
    joins = joins || {};
    groups = groups || null;
    var uid = unit.unit;
    var lang = unit.lang || String(uid).split("/")[0];
    var probe = joins.probe || null;
    var term = joins.term || {};
    var pool = joins.pool || {};
    var rendered = joins.rendered || null;
    var ledger = (unit.ledger || []).map(function (row) {
      return {
        row: row.row,
        size: row.size,
        type: row.type,
        gloss: glossOf(row)
      };
    });
    var token = unit.operator;
    var opGroup = null;
    if (groups) {
      opGroup = groups.mint(lang, token);
    }
    var holes = (term.holes || []).slice(0, 3).map(function (h) {
      if (h && typeof h === "object") {
        return h.cause;
      }
      return String(h);
    });
    return {
      id: uid,
      lang: lang,
      opGroup: opGroup,
      label: token,
      sig: signatureOf(probe, unit),
      pop: unit.population,
      outcome: unit.outcome,
      arrival: unit.arrival_annotation,
      src: probe ? probe.source : null,
      raw: unit.body_as_read || [],
      canon: unit.wrapped_text,
      ledger: ledger,
      l5: term.l5,
      verdict: term.outcome,
      reason: term.reason,
      holes: holes,
      rendered: rendered,
      entry: pool.entry,
      entry_members: pool.members,
      entry_langs: pool.languages,
      entry_rep: pool.rep,
      mnems: mnemsOf(unit)
    };
  }

  /* ---------------------------------------------------------------- *
   * 2.  the shell -- style and markup, so both pages are one shell
   * ---------------------------------------------------------------- */

  var STYLE = [
    ":root{--bg:#f7f7f5;--panel:#fff;--ink:#1b1b1a;--dim:#6a6a66;",
    "--line:#dedcd6;--accent:#1f5f8b;--good:#2c6e49;--warn:#9a5b13;",
    "--bad:#8b2f2f;--code:#f2f1ec}",
    "@media (prefers-color-scheme:dark){:root{--bg:#16181a;--panel:#1e2124;",
    "--ink:#e6e6e3;--dim:#9a9a95;--line:#32363a;--accent:#7fb3d5;",
    "--good:#7fc9a0;--warn:#e0aa63;--bad:#e08a8a;--code:#15181b}}",
    "*{box-sizing:border-box}",
    "body{margin:0;background:var(--bg);color:var(--ink);",
    "font:14px/1.5 -apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,sans-serif}",
    "code,pre,.mono{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}",
    "header{display:flex;align-items:baseline;gap:16px;padding:12px 18px;",
    "border-bottom:1px solid var(--line);background:var(--panel);flex-wrap:wrap}",
    "h1{font-size:15px;margin:0;font-weight:600;letter-spacing:.02em}",
    ".sub{color:var(--dim);font-size:12px}",
    "nav{display:flex;gap:2px;padding:0 12px;background:var(--panel);",
    "border-bottom:1px solid var(--line);overflow-x:auto}",
    "nav button{background:none;border:0;border-bottom:2px solid transparent;",
    "padding:9px 14px;color:var(--dim);cursor:pointer;font-size:13px;white-space:nowrap}",
    "nav button.on{color:var(--ink);border-bottom-color:var(--accent);font-weight:600}",
    "main{padding:16px 18px;max-width:1500px}",
    ".tab{display:none}.tab.on{display:block}",
    ".split{display:grid;grid-template-columns:330px 1fr;gap:16px;align-items:start}",
    "@media(max-width:900px){.split{grid-template-columns:1fr}}",
    ".card{background:var(--panel);border:1px solid var(--line);border-radius:6px;",
    "padding:12px 14px;margin-bottom:14px}",
    ".card h2{font-size:12px;text-transform:uppercase;letter-spacing:.08em;",
    "color:var(--dim);margin:0 0 10px;font-weight:600}",
    "select,input,button.act{font:inherit;padding:5px 8px;border:1px solid var(--line);",
    "border-radius:4px;background:var(--panel);color:var(--ink);width:100%;margin-bottom:8px}",
    "button.act{cursor:pointer;background:var(--accent);color:#fff;border-color:transparent;",
    "font-weight:600}",
    ".list{max-height:62vh;overflow:auto;border:1px solid var(--line);border-radius:4px}",
    ".list div{padding:5px 9px;cursor:pointer;border-bottom:1px solid var(--line);",
    "font-size:12.5px;display:flex;justify-content:space-between;gap:8px}",
    ".list div:hover{background:var(--code)}",
    ".list div.on{background:var(--accent);color:#fff}",
    ".list .tag{color:var(--dim);font-size:11px}",
    ".list div.on .tag{color:#dbe9f2}",
    ".modes{display:flex;gap:6px;flex-wrap:wrap;margin-bottom:12px}",
    ".modes button{background:var(--panel);border:1px solid var(--line);border-radius:4px;",
    "padding:5px 11px;cursor:pointer;color:var(--dim);font-size:12.5px}",
    ".modes button.on{background:var(--ink);color:var(--bg);border-color:var(--ink)}",
    "pre{background:var(--code);border:1px solid var(--line);border-radius:4px;",
    "padding:11px 13px;overflow-x:auto;margin:0 0 12px;font-size:12.5px;line-height:1.55}",
    "table{border-collapse:collapse;width:100%;font-size:13px;margin-bottom:6px}",
    "th,td{text-align:left;padding:5px 9px;border-bottom:1px solid var(--line)}",
    "th{color:var(--dim);font-weight:600;font-size:11.5px;text-transform:uppercase;",
    "letter-spacing:.05em}",
    "td.num,th.num{text-align:right;font-family:ui-monospace,Menlo,monospace}",
    ".kv{display:flex;flex-wrap:wrap;gap:6px 16px;margin-bottom:12px;font-size:12.5px}",
    ".kv b{color:var(--dim);font-weight:600}",
    ".pill{display:inline-block;padding:1px 7px;border-radius:9px;font-size:11px;",
    "border:1px solid var(--line)}",
    ".ok{color:var(--good);border-color:var(--good)}",
    ".no{color:var(--bad);border-color:var(--bad)}",
    ".mid{color:var(--warn);border-color:var(--warn)}",
    ".big{font-size:26px;font-weight:600;font-family:ui-monospace,Menlo,monospace}",
    ".grid3{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:12px}",
    "details{border:1px solid var(--line);border-radius:4px;margin-bottom:8px;",
    "background:var(--panel)}",
    "summary{cursor:pointer;padding:7px 11px;font-size:12.5px}",
    "details[open] summary{border-bottom:1px solid var(--line)}",
    "details .body{padding:11px}",
    ".note{color:var(--dim);font-size:12px;margin:0 0 10px}",
    ".gloss{color:var(--dim)}",
    ".pop{color:var(--dim);font-size:11.5px;font-family:ui-monospace,Menlo,monospace;",
    "border-left:2px solid var(--accent);padding-left:8px;margin:0 0 12px}",
    "#gate{padding:40px 22px;max-width:760px}",
    "#gate h2{font-size:16px;margin:0 0 10px}",
    "#gate button.act{width:auto;padding:8px 18px}",
    ".warnbox{border:1px solid var(--warn);color:var(--warn);border-radius:6px;",
    "padding:12px 14px;margin:0 0 16px}"
  ].join("\n");

  var MARKUP = [
    '<header><h1>arch-unit dashboard</h1>',
    '<span class="sub" id="hdr"></span></header>',
    '<nav id="nav"></nav>',
    '<main>',
    '<section class="tab" id="t-units"><div class="pop" id="pop-units"></div>',
    '<div class="split"><div><div class="card"><h2>select</h2>',
    '<button class="act" id="rand">random arch-unit</button>',
    '<select id="f-lang"></select><select id="f-op"></select>',
    '<select id="f-sig"></select>',
    '<input id="f-txt" placeholder="filter by unit id…">',
    '<div class="sub" id="count"></div></div>',
    '<div class="list" id="ulist"></div></div>',
    '<div><div class="card" id="upane"><p class="note">pick a unit.</p></div></div>',
    '</div></section>',
    '<section class="tab" id="t-opcodes"><div class="pop" id="pop-opcodes"></div>',
    '<div class="split"><div><div class="card"><h2>arch opcode</h2>',
    '<input id="o-txt" placeholder="filter opcodes…">',
    '<div class="sub" id="ocount"></div></div>',
    '<div class="list" id="olist"></div></div>',
    '<div><div class="card" id="opane"><p class="note">pick an opcode.</p></div></div>',
    '</div></section>',
    '<section class="tab" id="t-coverage"><div class="pop" id="pop-coverage"></div>',
    '<div id="cov"></div></section>',
    '<section class="tab" id="t-stats"><div class="pop" id="pop-stats"></div>',
    '<div id="stats"></div></section>',
    '<section class="tab" id="t-spec"><div class="pop" id="pop-spec"></div>',
    '<div id="spec"></div></section>',
    '</main>'
  ].join("\n");

  /* ---------------------------------------------------------------- *
   * 3.  the population line -- one per pane, the mechanical-update rule
   *     made visible.  Every pane says what it counted and when.
   * ---------------------------------------------------------------- */

  function populationLine(pop, what) {
    var when = clockOf(pop.openedAt || new Date());
    var line = num(pop.units) + " units read from " + num(pop.files) +
      " files, opened at " + when;
    if (what) {
      line = what + ": " + line;
    }
    if (pop.note) {
      line = line + " — " + pop.note;
    }
    return line;
  }

  function paintPopulation(pop) {
    var panes = [
      ["#pop-units", "pane 1, arch-unit viewer and selector"],
      ["#pop-opcodes", "pane 2, arch opcode index"],
      ["#pop-coverage", "pane 3, compiler coverage"],
      ["#pop-stats", "pane 4, stats"],
      ["#pop-spec", "pane 5, what was asked for"]
    ];
    panes.forEach(function (row) {
      var el = document.querySelector(row[0]);
      if (el) {
        el.textContent = populationLine(pop, row[1]);
      }
    });
  }

  /* ---------------------------------------------------------------- *
   * 4.  mount -- draws every pane from one source
   * ---------------------------------------------------------------- */

  function mount(source, root) {
    root = root || document.body;
    root.innerHTML = MARKUP;

    var $ = function (s) {
      return root.querySelector(s);
    };

    var state = {
      index: [],
      groups: null,
      opcodeIndex: {},
      stats: null,
      coverage: null,
      sel: null,
      mode: "src",
      osel: null,
      cache: {}
    };

    /* --- tabs --- */
    var TABS = [
      ["units", "1 · arch-unit viewer"],
      ["opcodes", "2 · arch opcode index"],
      ["coverage", "3 · compiler coverage"],
      ["stats", "4 · stats"],
      ["spec", "5 · what was asked for"]
    ];
    $("#nav").innerHTML = TABS.map(function (t, i) {
      var on = i === 0 ? "on" : "";
      return '<button data-t="' + t[0] + '" class="' + on + '">' + t[1] + "</button>";
    }).join("");
    root.querySelectorAll("nav button").forEach(function (b) {
      b.onclick = function () {
        root.querySelectorAll("nav button").forEach(function (x) {
          x.classList.remove("on");
        });
        b.classList.add("on");
        root.querySelectorAll(".tab").forEach(function (x) {
          x.classList.remove("on");
        });
        $("#t-" + b.dataset.t).classList.add("on");
      };
    });
    $("#t-units").classList.add("on");

    /* --- 4a. selector: language -> operator group -> signature --- */

    function opts(el, vals, all, labelFn) {
      var head = '<option value="">' + all + "</option>";
      var body = vals.map(function (v) {
        var text = labelFn ? labelFn(v) : v;
        return '<option value="' + esc(v) + '">' + esc(text) + "</option>";
      }).join("");
      el.innerHTML = head + body;
    }

    function distinct(list) {
      var seen = {};
      var out = [];
      list.forEach(function (v) {
        if (v !== null && v !== undefined && v !== "" && !seen[v]) {
          seen[v] = true;
          out.push(v);
        }
      });
      out.sort();
      return out;
    }

    function filtered() {
      var L = $("#f-lang").value;
      var G = $("#f-op").value;
      var S = $("#f-sig").value;
      var T = $("#f-txt").value.trim().toLowerCase();
      return state.index.filter(function (u) {
        if (L && u.lang !== L) {
          return false;
        }
        if (G && u.opGroup !== G) {
          return false;
        }
        if (S && u.sig !== S) {
          return false;
        }
        if (T && String(u.id).toLowerCase().indexOf(T) === -1) {
          return false;
        }
        return true;
      });
    }

    function refreshMenus() {
      var L = $("#f-lang").value;
      var keepG = $("#f-op").value;
      var groups = distinct(state.index.filter(function (u) {
        return !L || u.lang === L;
      }).map(function (u) {
        return u.opGroup;
      }));
      opts($("#f-op"), groups, "every operator", function (gid) {
        return label(state.groups ? state.groups.labelOf(gid) : gid);
      });
      if (groups.indexOf(keepG) !== -1) {
        $("#f-op").value = keepG;
      }
      var G = $("#f-op").value;
      var keepS = $("#f-sig").value;
      var sigs = distinct(state.index.filter(function (u) {
        if (L && u.lang !== L) {
          return false;
        }
        if (G && u.opGroup !== G) {
          return false;
        }
        return true;
      }).map(function (u) {
        return u.sig;
      }));
      opts($("#f-sig"), sigs, "every signature");
      if (sigs.indexOf(keepS) !== -1) {
        $("#f-sig").value = keepS;
      }
    }

    function drawList() {
      var f = filtered();
      $("#count").textContent = num(f.length) + " of " + num(state.index.length) +
        " shown";
      var rows = f.slice(0, 600).map(function (u) {
        var on = state.sel && state.sel.id === u.id ? "on" : "";
        return '<div data-id="' + esc(u.id) + '" class="' + on + '">' +
          '<span class="mono">' + esc(u.id) + "</span>" +
          '<span class="tag">' + esc(label(u.label)) + "</span></div>";
      }).join("");
      var more = "";
      if (f.length > 600) {
        more = '<div class="tag" style="padding:8px">…' +
          num(f.length - 600) + " more, narrow the filter</div>";
      }
      $("#ulist").innerHTML = rows + more;
      $("#ulist").querySelectorAll("div[data-id]").forEach(function (d) {
        d.onclick = function () {
          selectUnit(d.dataset.id);
        };
      });
    }

    ["#f-lang", "#f-op", "#f-sig"].forEach(function (s) {
      $(s).onchange = function () {
        refreshMenus();
        drawList();
      };
    });
    $("#f-txt").oninput = drawList;

    /* the random sampler is seeded and the seed rides in the address, so
     * a unit the owner saw can be reached again. */
    function seedFromHash() {
      var m = /seed=(\d+)/.exec(window.location.hash || "");
      if (m) {
        return Number(m[1]);
      }
      return null;
    }

    function nextSeeded(seed) {
      var x = (seed * 1664525 + 1013904223) % 4294967296;
      return x;
    }

    $("#rand").onclick = function () {
      var f = filtered();
      if (!f.length) {
        return;
      }
      var seed = seedFromHash();
      if (seed === null) {
        seed = Math.floor(Math.random() * 4294967296);
      } else {
        seed = nextSeeded(seed);
      }
      window.location.hash = "seed=" + seed;
      var pick = f[seed % f.length];
      selectUnit(pick.id);
    };

    /* --- 4b. the unit viewer --- */

    var MODES = [
      ["src", "high-level source"],
      ["raw", "raw extracted"],
      ["canon", "canonical form"],
      ["ledger", "ledger"],
      ["z3", "z3 / normalized"],
      ["rendered", "rendered back"],
      ["pool", "pool entry"]
    ];

    /* pane 1's own modes, added by dashboard_pane1.js when it is
     * loaded (task 69).  Nothing here reads them; they are drawn by
     * that file. */
    if (typeof window !== "undefined" && window.DashboardPane1) {
      MODES = MODES.concat(window.DashboardPane1.modes);
    }

    function verdictPill(u) {
      var v = u.verdict || u.outcome || "";
      var cls = "mid";
      if (/PROVED/.test(v)) {
        cls = "ok";
      } else if (/DISPROVED|REFUSED/.test(v)) {
        cls = "no";
      }
      return '<span class="pill ' + cls + '">' + esc(v || "no term") + "</span>";
    }

    function body(u) {
      if (state.mode === "src") {
        if (u.src) {
          return "<pre>" + esc(u.src) + "</pre>";
        }
        return '<p class="note">no probe source recorded for this unit ' +
          "(interpreter handlers have none).</p>";
      }
      if (state.mode === "raw") {
        return "<pre>" + esc((u.raw || []).join("\n")) + "</pre>";
      }
      if (state.mode === "canon") {
        if (u.canon) {
          return "<pre>" + esc(u.canon.split("; ").join("\n")) + "</pre>";
        }
        return '<p class="note">refused: ' + esc(u.outcome) + "</p>";
      }
      if (state.mode === "ledger") {
        if (!u.ledger.length) {
          return '<p class="note">no ledger.</p>';
        }
        var head = "<table><tr><th>row</th><th class='num'>size</th>" +
          "<th>type</th><th>produced by</th></tr>";
        var rows = u.ledger.map(function (r) {
          return '<tr><td class="mono">' + esc(r.row) + '</td>' +
            '<td class="num">' + esc(r.size) + "</td>" +
            "<td>" + esc(r.type) + "</td>" +
            '<td class="mono gloss">' + esc(r.gloss) + "</td></tr>";
        }).join("");
        return head + rows + "</table>";
      }
      if (state.mode === "z3") {
        var h = u.l5 ? "<pre>" + esc(u.l5) + "</pre>"
          : '<p class="note">no term was built.</p>';
        if (u.reason) {
          h += '<p class="note">' + esc(u.reason) + "</p>";
        }
        if (u.holes && u.holes.length) {
          h += '<p class="note">holes: ' + u.holes.map(esc).join(" · ") + "</p>";
        }
        return h;
      }
      if (state.mode === "rendered") {
        if (!u.rendered) {
          return '<p class="note">no rendered-back text recorded for this unit ' +
            "(render_back_store carries only units with a proved term).</p>";
        }
        var txt = u.rendered.layer3_wrapped_text || u.rendered.text || "";
        var same = u.rendered.character_identical_to_layer_3;
        var note = same === true
          ? "character-identical to the canonical form"
          : "differs from the canonical form in characters";
        return "<pre>" + esc(String(txt).split("; ").join("\n")) + "</pre>" +
          '<p class="note">' + esc(note) + "</p>";
      }
      if (typeof window !== "undefined" && window.DashboardPane1) {
        var extra = window.DashboardPane1.body(u, state.mode);
        if (extra !== null && extra !== undefined) {
          return extra;
        }
      }
      if (state.mode === "pool") {
        if (!u.entry) {
          return '<p class="note">not in the pool.</p>';
        }
        return '<div class="kv"><span><b>entry</b> ' + esc(u.entry) + "</span>" +
          "<span><b>members</b> " + num(u.entry_members) + "</span>" +
          "<span><b>languages</b> " + esc((u.entry_langs || []).join(", ")) + "</span>" +
          '<span><b>representative</b> <span class="mono">' + esc(u.entry_rep) +
          "</span></span></div>" +
          '<p class="note">every member of this entry was proved to compute the ' +
          "same thing.</p>";
      }
      return "";
    }

    function drawUnit() {
      var u = state.sel;
      if (!u) {
        return;
      }
      $("#upane").innerHTML =
        '<div class="kv">' +
        '<span class="mono" style="font-size:15px">' + esc(u.id) + "</span>" +
        "<span><b>operator</b> " + esc(label(u.label)) + "</span>" +
        "<span><b>signature</b> " + esc(u.sig || "—") + "</span>" +
        "<span><b>arrival</b> " + esc(u.arrival || "—") + "</span>" +
        "<span><b>population</b> " + esc(u.pop || "—") + "</span>" +
        verdictPill(u) + "</div>" +
        '<div class="modes">' + MODES.map(function (m) {
          var on = state.mode === m[0] ? "on" : "";
          return '<button data-m="' + m[0] + '" class="' + on + '">' + m[1] +
            "</button>";
        }).join("") + "</div>" +
        '<div id="ubody">' + body(u) + "</div>";
      $("#upane").querySelectorAll(".modes button").forEach(function (b) {
        b.onclick = function () {
          state.mode = b.dataset.m;
          drawUnit();
        };
      });
    }

    function selectUnit(id) {
      if (state.cache[id]) {
        state.sel = state.cache[id];
        drawList();
        drawUnit();
        return;
      }
      $("#upane").innerHTML = '<p class="note">reading the unit from disk…</p>';
      Promise.resolve(source.unit(id)).then(function (u) {
        if (u && typeof window !== "undefined" && window.DashboardPane1) {
          return window.DashboardPane1.enrich(source, u);
        }
        return u;
      }).then(function (u) {
        if (!u) {
          $("#upane").innerHTML = '<p class="note">this unit is not in the ' +
            "artifacts on disk.</p>";
          return;
        }
        state.cache[id] = u;
        state.sel = u;
        drawList();
        drawUnit();
      }).catch(function (err) {
        $("#upane").innerHTML = '<p class="note">could not read this unit: ' +
          esc(err && err.message ? err.message : err) + "</p>";
      });
    }

    /* --- 4c. the arch opcode index --- */

    function drawOList() {
      var t = $("#o-txt").value.trim().toLowerCase();
      var keys = Object.keys(state.opcodeIndex).filter(function (k) {
        return !t || k.indexOf(t) !== -1;
      });
      keys.sort(function (a, b) {
        return state.opcodeIndex[b].length - state.opcodeIndex[a].length;
      });
      $("#ocount").textContent = keys.length + " arch opcodes";
      $("#olist").innerHTML = keys.map(function (k) {
        var on = state.osel === k ? "on" : "";
        return '<div data-o="' + esc(k) + '" class="' + on + '">' +
          '<span class="mono">' + esc(k) + "</span>" +
          '<span class="tag">' + num(state.opcodeIndex[k].length) +
          "</span></div>";
      }).join("");
      $("#olist").querySelectorAll("div[data-o]").forEach(function (d) {
        d.onclick = function () {
          state.osel = d.dataset.o;
          drawOList();
          drawOPane();
        };
      });
    }

    /* the groups are keyed lang + operator GROUP ID + signature.  No token
     * is in the key; the token is printed beside it. */
    function drawOPane() {
      var ids = state.opcodeIndex[state.osel] || [];
      var byId = {};
      state.index.forEach(function (u) {
        byId[u.id] = u;
      });
      var groups = {};
      ids.forEach(function (id) {
        var u = byId[id];
        if (!u) {
          return;
        }
        var k = u.lang + "#" + (u.opGroup || "no-group") + "#" +
          (u.sig || "no-signature-recorded");
        if (!groups[k]) {
          groups[k] = [];
        }
        groups[k].push(u);
      });
      var keys = Object.keys(groups).sort();
      var head = '<div class="kv"><span><b>selected arch opcode</b> ' +
        '<span class="mono" style="font-size:15px">' + esc(state.osel) +
        "</span></span>" +
        "<span><b>units</b> " + num(ids.length) + "</span>" +
        "<span><b>groups (language, operator, signature)</b> " + keys.length +
        "</span></div>";
      var bodyHtml = keys.map(function (k) {
        var g = groups[k];
        var u0 = g[0];
        var title = u0.lang + " · " + label(u0.label) + " · " +
          (u0.sig || "(no signature recorded)");
        var lines = g.slice(0, 12).map(function (u) {
          return '<div class="mono" style="margin-bottom:4px">' + esc(u.id) +
            "</div>";
        }).join("");
        var more = "";
        if (g.length > 12) {
          more = '<p class="note">…' + num(g.length - 12) +
            " more in this group</p>";
        }
        return "<details><summary>" + esc(title) +
          '<span class="tag"> — ' + num(g.length) + " unit" +
          (g.length > 1 ? "s" : "") + "</span></summary>" +
          '<div class="body">' + lines + more +
          '<p class="note">key: <span class="mono">' + esc(k) +
          "</span> — machine form; the token above is a label.</p>" +
          "</div></details>";
      }).join("");
      $("#opane").innerHTML = head + bodyHtml;
    }

    $("#o-txt").oninput = drawOList;

    /* --- 4d. coverage --- */

    function drawCoverage() {
      var C = state.coverage || {};
      var graphs = C.graphs || [];
      var html = '<div class="card"><h2>the compiler graph, per language</h2>';
      if (!graphs.length) {
        html += '<p class="note">Not measured: no graph file was found in ' +
          "<span class='mono'>Research/compiler_graph/</span>. This pane needs " +
          "<span class='mono'>graph_&lt;lang&gt;.json</span> for each compiler.</p>";
      } else {
        html += '<div style="overflow-x:auto">';
        html += "<table><tr><th>language</th><th>compiler region</th>" +
          "<th class='num'>files</th><th class='num'>defs</th>" +
          "<th class='num'>call edges</th><th class='num'>frontier</th></tr>";
        html += graphs.map(function (g) {
          var c = g.counts || {};
          var kinds = c.nodes_by_kind || {};
          var rel = c.edges_by_relation || {};
          return "<tr><td>" + esc(g.lang) + "</td>" +
            '<td class="mono" style="font-size:11.5px">' +
            (g.directories || []).map(esc).join("<br>") + "</td>" +
            '<td class="num">' + num(c.files) + "</td>" +
            '<td class="num">' + num(kinds.def) + "</td>" +
            '<td class="num">' + num(rel.calls) + "</td>" +
            '<td class="num">' + num(c.frontier) + "</td></tr>";
        }).join("");
        html += "</table></div>";
        html += '<p class="note">The frontier column is the graph’s own ' +
          "honesty column: every reference or call the builder could not " +
          "resolve, counted rather than hidden.</p>";
      }
      html += "</div>";

      var cov = C.probe_coverage;
      html += '<div class="card"><h2>probe coverage of compiler logic</h2>';
      if (!cov) {
        html += '<p class="note">Not measured. This pane needs a diary per ' +
          "probe — the ordered list of compiler-source nodes that " +
          "probe’s compilation visited — and a coverage summary " +
          "beside the graph. Only go has one today.</p>";
      } else {
        html += "<table>" +
          "<tr><td>compiler definitions in the region</td><td class='num'>" +
          num(cov.population_defs) + "</td></tr>" +
          "<tr><td>probes with a recorded diary</td><td class='num'>" +
          num(cov.population_probes) + "</td></tr>" +
          "<tr><td>definitions visited by at least one probe</td><td class='num'>" +
          num(cov.defs_visited_by_at_least_one_probe) + "</td></tr>" +
          "<tr><td>never visited</td><td class='num'>" +
          num(cov.never_visited_count) + "</td></tr>" +
          "</table>";
        html += '<p class="note">Measured for ' + esc(cov.lang || "go") +
          " only. Every other language says “not measured” above.</p>";
      }
      html += "</div>";

      if (C.missing && C.missing.length) {
        html += '<div class="card"><h2>what is NOT measured</h2>' +
          '<p class="note">No compiler graph exists for: ' +
          esc(C.missing.join(", ")) + ".</p></div>";
      }
      $("#cov").innerHTML = html;
    }

    /* --- 4e. stats --- */

    function drawStats() {
      var S = state.stats || {};
      var P = S.pool || {};
      var langRows = Object.keys(S.per_lang || {}).map(function (k) {
        return [k, S.per_lang[k]];
      });
      langRows.sort(function (a, b) {
        return b[1].units - a[1].units;
      });
      var totalUnits = langRows.reduce(function (n, r) {
        return n + r[1].units;
      }, 0);
      var totalProved = langRows.reduce(function (n, r) {
        return n + r[1].proved;
      }, 0);

      var html = '<div class="grid3">' +
        '<div class="card"><h2>arch-units extracted</h2><div class="big">' +
        num(totalUnits) + "</div></div>" +
        '<div class="card"><h2>distinct computations (pool entries)</h2>' +
        '<div class="big">' + num(P.entries) + "</div></div>" +
        '<div class="card"><h2>dominant-operator families</h2>' +
        '<div class="big">' + num(S.families) + "</div></div></div>";

      html += '<div class="card"><h2>by language</h2><table>' +
        "<tr><th>language</th><th class='num'>arch-units</th>" +
        "<th class='num'>wrapped &amp; proved</th></tr>";
      html += langRows.map(function (r) {
        return "<tr><td>" + esc(r[0]) + "</td>" +
          '<td class="num">' + num(r[1].units) + "</td>" +
          '<td class="num">' + num(r[1].proved) + "</td></tr>";
      }).join("");
      html += "<tr><td><b>total</b></td><td class='num'><b>" + num(totalUnits) +
        "</b></td><td class='num'><b>" + num(totalProved) +
        "</b></td></tr></table></div>";

      html += '<div class="card"><h2>the pool</h2><table>' +
        "<tr><td>members</td><td class='num'>" + num(P.members) + "</td></tr>" +
        "<tr><td>entries</td><td class='num'>" + num(P.entries) + "</td></tr>" +
        "<tr><td>entries spanning more than one language</td><td class='num'>" +
        num(P.entries_spanning_more_than_one_language) + "</td></tr>" +
        "<tr><td>entries spanning compiled and interpreted</td><td class='num'>" +
        num(P.entries_spanning_compiled_and_interpreted) + "</td></tr>" +
        "<tr><td>members with a proved term</td><td class='num'>" +
        num(P.members_with_a_proved_term) + "</td></tr>" +
        "<tr><td>members whose term was withdrawn</td><td class='num'>" +
        num(P.members_whose_term_was_withdrawn) + "</td></tr>" +
        "</table></div>";

      var cen = S.census || {};
      html += '<div class="card"><h2>what is not modelled yet (census)</h2>' +
        '<p class="note">' + num(cen.producers) +
        " producers have no term builder.</p>" +
        "<table><tr><th>producer</th><th class='num'>rows</th>" +
        "<th class='num'>units</th></tr>";
      html += (cen.rows || []).map(function (r) {
        return '<tr><td class="mono">' + esc(r.producer) + "</td>" +
          '<td class="num">' + num(r.rows) + "</td>" +
          '<td class="num">' + num(r.units) + "</td></tr>";
      }).join("");
      html += "</table></div>";

      var t = S.terms;
      if (t && t.layer5) {
        html += '<div class="card"><h2>terms</h2><table>' +
          "<tr><td>proved terms</td><td class='num'>" +
          num(t.layer5.proved_terms) + "</td></tr>" +
          "<tr><td>distinct normalized texts</td><td class='num'>" +
          num(t.layer5.distinct_texts) + "</td></tr>" +
          "<tr><td>normalization refused</td><td class='num'>" +
          num(t.layer5.normalization_refused) + "</td></tr></table></div>";
      }
      $("#stats").innerHTML = html;
    }

    /* --- 4f. the spec pane --- */

    function drawSpec() {
      var kind = source.kind === "live"
        ? "This page read the artifact folder itself, in the browser, when you " +
          "opened it. There is no server and no build step: every number above " +
          "is a count over a file on disk at the moment shown in each pane’s " +
          "population line."
        : "This file is a SNAPSHOT: viewer_build.py read the artifacts once and " +
          "embedded them here, so it can be sent to someone who does not have " +
          "the folder. The live page (dashboard.html) reads the folder itself.";
      $("#spec").innerHTML =
        '<div class="card"><h2>what you asked for, and where it is</h2>' +
        "<table><tr><th>#</th><th>asked</th><th>pane</th><th>state</th></tr>" +
        "<tr><td>1</td><td>viewer with modes</td><td>pane 1</td><td>" +
        '<span class="pill ok">7 modes</span> source · raw · canonical ' +
        "· ledger · z3 · rendered back · pool entry. " +
        "<b>context is still missing</b> — the body names its constants by " +
        "relocation and the bytes are not stored per unit (task 69).</td></tr>" +
        "<tr><td>2</td><td>random sampler; language / operator / signature menus" +
        "</td><td>pane 1</td><td><span class='pill ok'>done</span> — the " +
        "sampler is seeded and the seed rides in the address bar</td></tr>" +
        "<tr><td>3</td><td>every arch opcode, and the operators and signatures " +
        "it appears in</td><td>pane 2</td><td><span class='pill ok'>done</span>" +
        "</td></tr>" +
        "<tr><td>4</td><td>compiler graph per language, probe coverage</td>" +
        "<td>pane 3</td><td>the four graphs are read live; probe coverage is " +
        "measured for go only and the pane says so</td></tr>" +
        "<tr><td>5</td><td>stats</td><td>pane 4</td>" +
        "<td><span class='pill ok'>done</span></td></tr>" +
        "<tr><td>6</td><td>a chronology over the version-control history</td>" +
        "<td>—</td><td><span class='pill no'>not built</span> — " +
        "task 76</td></tr></table></div>" +
        '<div class="card"><h2>how it updates</h2><p class="note">' + kind +
        "</p></div>";
    }

    /* --- 4g. the boot sequence: summaries first, bodies on demand --- */

    function paintHeader() {
      var S = state.stats || {};
      var P = S.pool || {};
      var n = Object.keys(state.index).length;
      $("#hdr").textContent =
        num(state.population ? state.population.units : n) + " arch-units · " +
        Object.keys(state.opcodeIndex).length + " arch opcodes · pool " +
        num(P.entries) + " entries over " + num(P.members) + " members";
    }

    function repaintIndexPanes() {
      refreshMenus();
      drawList();
      drawOList();
      paintHeader();
    }

    var api = {
      state: state,
      repaintIndexPanes: function () {
        state.groups = groupsFromIndex(state.index);
        repaintIndexPanes();
      },
      paintPopulation: function (pop) {
        state.population = pop;
        paintPopulation(pop);
      },
      drawStats: drawStats,
      drawCoverage: drawCoverage,
      drawSpec: drawSpec,
      /* task 70: the two selector functions a module beside this file
       * needs and cannot reach, because both are closed over `state`.
       * `filtered` is the list the seeded sampler indexes into and
       * `selectUnit` is how a unit anywhere in the population is opened
       * without depending on it being one of the 600 rows drawn. */
      filtered: filtered,
      selectUnit: selectUnit
    };

    /* first paint: whatever the source can answer from summaries alone. */
    return Promise.resolve(source.population()).then(function (pop) {
      api.paintPopulation(pop);
      return Promise.all([source.stats(), source.coverage()]);
    }).then(function (both) {
      state.stats = both[0];
      state.coverage = both[1];
      drawStats();
      drawCoverage();
      drawSpec();
      paintHeader();
      /* the index and the opcode index arrive later on the live page; the
       * snapshot has them already. */
      return Promise.all([source.index(), source.opcodeIndex()]);
    }).then(function (both) {
      state.index = both[0] || [];
      state.opcodeIndex = both[1] || {};
      state.groups = groupsFromIndex(state.index);
      opts($("#f-lang"), distinct(state.index.map(function (u) {
        return u.lang;
      })), "every language");
      repaintIndexPanes();
      return api;
    });
  }

  return {
    esc: esc,
    num: num,
    label: label,
    glyphMode: function () {
      return GLYPH_MODE;
    },
    unitsOf: unitsOf,
    glossOf: glossOf,
    mnemsOf: mnemsOf,
    signatureOf: signatureOf,
    censusName: censusName,
    packUnit: packUnit,
    OperatorGroups: OperatorGroups,
    groupsFromIndex: groupsFromIndex,
    populationLine: populationLine,
    STYLE: STYLE,
    MARKUP: MARKUP,
    mount: mount
  };
}());
