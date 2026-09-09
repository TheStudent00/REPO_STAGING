/* dashboard_pane5.js -- PANE 5, THE STATS.
 *
 * Node: hq.research.compiler_graph.dashboard.  Task 74, round 14.
 *
 * WHAT IT DRAWS.  Two cards over the FULL population (the pool, 1,831
 * entries / 30,432 members, from the_pool5.json's own summary):
 *   (a) the four TERM STATES -- proved, disproved-withdrawn, undecided,
 *       no term -- read from audit65.json's term65 tally at open time.
 *   (b) the census's TOP CAUSES -- the producers with no term builder,
 *       read from the HIGHEST-NUMBERED name_census*.json present beside
 *       the page, sorted by rows_blocked descending.  Task 76 (log_180)
 *       found pane 4 reading name_census5.json while name_census6.json
 *       was already the highest generation on disk; this pane picks the
 *       file generally -- by number, not by a hard-coded name -- and
 *       states which one it read.
 *
 * WHY IT IS A SEPARATE FILE.  Same reason as pane 6 (see its own header):
 * this wraps DashboardJoin.mount and adds one nav button and one section,
 * touching no line of dashboard_join.js and no behaviour of panes 1-4/6.
 *
 * WHERE THE DATA COMES FROM, in order:
 *   1. window.__PANE5__            -- the snapshot/viewer build embeds it.
 *   2. the live folder handle      -- source.op.getFileHandle(...).
 *   3. neither                     -- the pane says so, and says what it
 *      needs (audit65.json, the_pool5.json, and a name_census*.json).
 *
 * THE SPELLING BAN, pasted verbatim as required by the round-14 brief:
 * "THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
 * second violation). No operator token may appear in ANY key, grouping,
 * pairing, row structure, candidate selection, or comparison scope,
 * anywhere in this line -- not in matching, not in "which pairs get
 * compared", not in report rows, not in dropdowns. The candidate set for
 * comparison comes from machine-form evidence (clusters, connections,
 * type pairs) or from ratified intention -- never from the token. The
 * token appears exactly once per unit: as a display label on the member.
 * HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
 * campaign's cross-language matrix (caught by the owner 2026-08-24); (2)
 * verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix brief
 * itself reintroduced it as "same-operator pairs"). MECHANICAL GUARD
 * REQUIRED: every pipeline stage that groups or pairs units must run the
 * spelling-key check (op_pipeline/check_no_spelling_keys.py) and refuse
 * its own output on failure. A brief handed to any subagent for this
 * line MUST paste this paragraph verbatim."
 * This pane groups nothing by operator token: the term-state rows are
 * keyed by state name (proved/withdrawn/undecided/no_term) and the
 * census rows are keyed by producer object ({kind,mnem}/{kind,phrase}/
 * {kind,callee}), never by a spelling. Checked by
 * check_dashboard_js_no_spelling.py.
 */

var DashboardStats = (function () {
  "use strict";

  var STYLE = [
    "#t-pane5stats .stats-pop{margin:0 0 10px;font-size:13px;opacity:.8}",
    "#t-pane5stats .stats-grid{display:grid;grid-template-columns:1fr 1fr;",
    "gap:16px}",
    "@media (max-width:900px){#t-pane5stats .stats-grid{grid-template-columns:1fr}}",
    "#t-pane5stats table{border-collapse:collapse;width:100%;font-size:13px}",
    "#t-pane5stats td,#t-pane5stats th{padding:3px 8px;text-align:right;",
    "font-variant-numeric:tabular-nums;white-space:nowrap}",
    "#t-pane5stats th{text-align:left;opacity:.7;font-weight:600}",
    "#t-pane5stats td:first-child{text-align:left}",
    "#t-pane5stats .term-proved{opacity:1}",
    "#t-pane5stats .term-disproved{opacity:.85}",
    "#t-pane5stats .term-undecided{opacity:.85}",
    "#t-pane5stats .term-no_term{opacity:.7}",
    "#t-pane5stats .src{font-size:11px;opacity:.6;margin:6px 0 0}",
    "#t-pane5stats .causes td:nth-child(3){max-width:520px;white-space:normal;",
    "text-align:left}"
  ].join("\n");

  function esc(s) {
    return DashboardJoin.esc(String(s === null || s === undefined ? "" : s));
  }

  function num(v) {
    if (v === null || v === undefined) {
      return "—";
    }
    return DashboardJoin.num(v);
  }

  /* ---------------------------------------------------------------- *
   * 1.  reading the three artifacts off the live folder / snapshot
   * ---------------------------------------------------------------- */

  function readJSON(dir, name) {
    if (!dir || !dir.getFileHandle) {
      return Promise.resolve(null);
    }
    return dir.getFileHandle(name).then(function (fh) {
      return fh.getFile();
    }).then(function (f) {
      return f.text();
    }).then(function (t) {
      return JSON.parse(t);
    })["catch"](function () {
      return null;
    });
  }

  /* picks the highest-numbered name_census*.json present, by NUMBER --
   * not a hard-coded filename -- so this keeps working the round the
   * next generation lands. name_census.json itself (no digit) counts
   * as generation 1. */
  function pickCensus(dir) {
    if (!dir || !dir.entries) {
      /* no directory-listing API on this handle: fall back to counting
       * down from a generous ceiling. */
      var tryDown = function (n) {
        if (n < 1) {
          return Promise.resolve(null);
        }
        var name = n === 1 ? "name_census.json" : "name_census" + n + ".json";
        return readJSON(dir, name).then(function (doc) {
          if (doc) {
            return { name: name, doc: doc };
          }
          return tryDown(n - 1);
        });
      };
      return tryDown(20);
    }
    var names = [];
    return (function collect() {
      var it = dir.entries();
      function step() {
        return it.next().then(function (r) {
          if (r.done) {
            return names;
          }
          var nm = r.value[0];
          if (/^name_census\d*\.json$/.test(nm)) {
            names.push(nm);
          }
          return step();
        });
      }
      return step();
    }()).then(function (found) {
      if (!found.length) {
        return null;
      }
      found.sort(function (a, b) {
        var na = a === "name_census.json" ? 1
          : parseInt(a.replace(/[^\d]/g, ""), 10);
        var nb = b === "name_census.json" ? 1
          : parseInt(b.replace(/[^\d]/g, ""), 10);
        return nb - na;
      });
      var best = found[0];
      return readJSON(dir, best).then(function (doc) {
        return doc ? { name: best, doc: doc } : null;
      });
    });
  }

  function readAll(source) {
    if (window.__PANE5__) {
      return Promise.resolve(window.__PANE5__);
    }
    var dir = source && source.op;
    if (!dir) {
      return Promise.resolve(null);
    }
    return Promise.all([
      readJSON(dir, "audit65.json"),
      readJSON(dir, "the_pool5.json"),
      pickCensus(dir)
    ]).then(function (r) {
      if (!r[0] || !r[1] || !r[2]) {
        return null;
      }
      return { audit65: r[0], pool5: r[1], census: r[2].doc,
               census_name: r[2].name };
    });
  }

  /* ---------------------------------------------------------------- *
   * 2.  the pane
   * ---------------------------------------------------------------- */

  var MARKUP = [
    '<section class="tab" id="t-pane5stats">',
    '<div class="pop" id="pop-pane5"></div>',
    '<div class="stats-grid">',
    '<div class="card" id="pane5-terms"></div>',
    '<div class="card" id="pane5-causes"></div>',
    "</div>",
    "</section>"
  ].join("\n");

  var TERM_ROWS = [
    ["proved", "proved"],
    ["disproved", "disproved / withdrawn"],
    ["undecided", "undecided"],
    ["no_term", "no term"]
  ];

  function drawTerms(el, tally) {
    var total = num(tally.records);
    var rows = TERM_ROWS.map(function (r) {
      var v = tally[r[0]];
      var pct = tally.records ? (100 * v / tally.records).toFixed(1) : "0.0";
      return "<tr class=\"term-" + r[0] + "\"><td>" + esc(r[1]) +
        "</td><td>" + num(v) + "</td><td>" + pct + "%</td></tr>";
    }).join("\n");
    el.innerHTML = "<h3>the four term states</h3>" +
      "<table><thead><tr><th>state</th><th>members</th><th>share</th>" +
      "</tr></thead><tbody>" + rows +
      "<tr><td>records (all four states)</td><td>" + total +
      "</td><td>100.0%</td></tr></tbody></table>" +
      '<p class="src">audit65.json, term65 tally, read at open</p>';
  }

  function drawCauses(el, census, censusName) {
    var entries = (census.entries || []).slice();
    entries.sort(function (a, b) {
      return (b.rows_blocked || 0) - (a.rows_blocked || 0);
    });
    var top = entries.slice(0, 15);
    var rows = top.map(function (e) {
      var p = e.producer || {};
      var label = p.mnem !== undefined
        ? (Array.isArray(p.mnem) ? p.mnem.join(",") : p.mnem)
        : (p.phrase !== undefined ? p.phrase
          : (p.callee !== undefined ? p.callee : "(unlabeled)"));
      var reason = (e.reasons && e.reasons[0]) || "";
      return "<tr><td>" + esc(p.kind || "") + " · " + esc(label) +
        "</td><td>" + num(e.rows_blocked) + "</td><td>" + esc(reason) +
        "</td></tr>";
    }).join("\n");
    var tally = census.tally || {};
    el.innerHTML = "<h3>top causes (census, no term builder)</h3>" +
      "<table class=\"causes\"><thead><tr><th>producer</th>" +
      "<th>rows blocked</th><th>reason</th></tr></thead><tbody>" + rows +
      "</tbody></table>" +
      '<p class="src">' + esc(censusName) +
      " (highest generation present), " + num(tally.producers) +
      " producers over " + num(tally.layer4_records_read) +
      " layer-4 records, " + num(top.length) + " of " +
      num(entries.length) + " shown by rows blocked</p>";
  }

  function attach(root, source) {
    root = root || document.body;
    if (root.querySelector("#t-pane5stats")) {
      return;
    }
    var main = root.querySelector("main");
    var nav = root.querySelector("#nav");
    if (!main || !nav) {
      return;
    }

    var style = document.createElement("style");
    style.textContent = STYLE;
    document.head.appendChild(style);

    main.insertAdjacentHTML("beforeend", MARKUP);

    var button = document.createElement("button");
    button.setAttribute("data-t", "pane5stats");
    button.textContent = "term & census stats — pane 5";
    nav.appendChild(button);
    button.onclick = function () {
      root.querySelectorAll("nav button").forEach(function (x) {
        x.classList.remove("on");
      });
      button.classList.add("on");
      root.querySelectorAll(".tab").forEach(function (x) {
        x.classList.remove("on");
      });
      root.querySelector("#t-pane5stats").classList.add("on");
    };

    var pop = root.querySelector("#pop-pane5");
    var termsEl = root.querySelector("#pane5-terms");
    var causesEl = root.querySelector("#pane5-causes");
    pop.textContent = "pane 5, the stats: reading audit65.json, " +
      "the_pool5.json and the highest name_census*.json…";

    readAll(source).then(function (data) {
      if (!data) {
        pop.textContent = "pane 5, the stats: no data.";
        termsEl.innerHTML =
          "<h3>the stats are not loaded</h3>" +
          '<p class="note">This pane needs <b>audit65.json</b>, ' +
          "<b>the_pool5.json</b> and a <b>name_census*.json</b> beside " +
          "the page.</p>";
        causesEl.innerHTML = "";
        return;
      }
      var summary = data.pool5.summary || {};
      var tally = (data.audit65.term65) || {};
      pop.innerHTML = "population: <b>" + num(summary.entries) +
        "</b> entries / <b>" + num(summary.members) +
        "</b> members (the_pool5.json summary) &middot; term states " +
        "over <b>" + num(tally.records) + "</b> records (audit65.json)" +
        " &middot; census read from <b>" + esc(data.census_name) + "</b>";
      drawTerms(termsEl, tally);
      drawCauses(causesEl, data.census, data.census_name);
    });
  }

  /* ---------------------------------------------------------------- *
   * 3.  self-installation: wrap mount, add nothing to it
   * ---------------------------------------------------------------- */

  /* Retire the join's own draft "4 . stats" tab: this pane realizes
   * `stats`, so the draft placeholder it stands in for is removed rather
   * than left beside it (task 82, log_182 coordinator note -- the tab bar
   * had eight entries where the CORE numbers the panes six, because each
   * concurrent pane module appended its own tab instead of retiring the
   * draft it replaces). Deferred until `out` (the join's own mount
   * promise) resolves, NOT run inside attach() itself: attach() runs
   * synchronously, before the join's own drawStats() has populated
   * #t-stats, and removing the section first would make drawStats()
   * write into a detached node's since-removed child and throw. */
  function retireDraftStats(root) {
    var draftBtn = root.querySelector('nav button[data-t="stats"]');
    var draftSec = root.querySelector("#t-stats");
    if (draftBtn) {
      draftBtn.remove();
    }
    if (draftSec) {
      draftSec.remove();
    }
  }

  function install() {
    if (typeof DashboardJoin === "undefined" || DashboardJoin.__pane5) {
      return;
    }
    var inner = DashboardJoin.mount;
    DashboardJoin.mount = function (source, root) {
      var target = root || document.body;
      var out = inner(source, root);
      try {
        attach(target, source);
      } catch (err) {
        if (window.console) {
          window.console.warn("[dashboard] pane 5 did not attach:", err);
        }
      }
      if (out && typeof out.then === "function") {
        return out.then(function (api) {
          retireDraftStats(target);
          return api;
        });
      }
      retireDraftStats(target);
      return out;
    };
    DashboardJoin.__pane5 = true;
  }

  install();

  return {
    attach: attach,
    install: install,
    STYLE: STYLE,
    TERM_ROWS: TERM_ROWS
  };
}());
