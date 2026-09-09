/* dashboard_pane4.js -- PANE 4, THE COVERAGE VIEW.
 *
 * Node: hq.research.compiler_graph.dashboard, the `coverage_view` method.
 * Brief: log_172 task 73.  Data: task 71's four `graph_<lang>.json` and
 * task 72/75's `coverage_go2.json`, both through the file-level summaries
 * `graph_files_build.py` and `coverage_files_build.py` write.
 *
 * WHAT IT DRAWS, in the three parts the brief names.
 *
 *   (a) THE STATIC STRUCTURE.  The compiler's own lowering region as a
 *       wiring diagram: one box per source file, sized by how many graph
 *       nodes that file holds, grouped by directory (the better layout the
 *       brief asks for; a force layout is offered beside it), wired by the
 *       inter-file edges of the graph -- calls, reads, writes.  COLLAPSED
 *       TO FILE LEVEL BY DEFAULT.  Clicking one box expands that ONE file
 *       into its definitions, drawn as nodes with the definition-to-
 *       definition edges between them.  Nothing else is expanded, so the
 *       drawing is 83 to 330 boxes and never 174,159 nodes.
 *
 *   (b) THE DYNAMIC STRUCTURE.  A probe is picked from a selector keyed by
 *       its unit id.  The page then reads that ONE probe's path out of
 *       coverage_go2.json by a ranged read -- Blob.slice between the byte
 *       offsets the summary carries -- and lights the files up IN ORDER,
 *       stepping or playing.  Inside an expanded file the same path lights
 *       the definitions of that file in order.
 *
 *   (c) COVERAGE.  The union over the corpus: every file box is shaded by
 *       how many of the 590 probes entered it, every definition inside an
 *       expanded file by how many probes visited it, and the never-visited
 *       set is LISTED -- the files no probe ever entered first, then the
 *       810 never-visited bodies by file, with their names and lines.
 *
 * WHERE A LANGUAGE HAS A GRAPH AND NO DIARIES (cpp, rust, swift) the pane
 * draws (a) and says plainly that (b) and (c) are NOT MEASURED, and points
 * at task 72's cost page, which is what schedules the measurement.
 *
 * THE MEMORY RULE, WHICH THIS PANE OBEYS BY CONSTRUCTION.  graph_cpp.json
 * is 331,704,231 bytes and coverage_go2.json is 515,160,866.  This module
 * NEVER opens either whole.  It reads:
 *   - graph_<lang>_files.json     41 KB to 184 KB, whole, per language
 *   - graph_<lang>_defs.json      0.6 MB to 3.3 MB, whole, only when a
 *                                 file is first expanded for that language
 *   - coverage_go_files.json      2.6 MB, whole, once
 *   - coverage_go2.json           ONE Blob.slice, byte_start..byte_end of
 *                                 the chosen probe, only when a probe is
 *                                 chosen
 *
 * WHY IT IS A SEPARATE FILE.  Tasks 69, 70 and 76 were editing the
 * dashboard at the same time.  This module adds itself to the page the way
 * dashboard_pane6.js does: it wraps DashboardJoin.mount, lets every
 * existing pane draw exactly as it did, then appends one nav button and one
 * section.  It changes no line of dashboard_join.js.
 *
 * THE SPELLING BAN.  Nothing here groups, pairs, selects or compares by an
 * operator token.  Files are keyed by source path, graph nodes by the id
 * scheme `file#line#kind#ordinal`, probes by their unit id, edges by the
 * graph's own relation vocabulary (contains / calls / reads / writes).  A
 * definition's own name appears once, as a display label on that node.
 * `?labels=glyph` therefore cannot change anything this pane draws, which
 * is itself the test.  Checked by check_dashboard_js_no_spelling.py.
 */

var DashboardPane4 = (function () {
  "use strict";

  /* ---------------------------------------------------------------- *
   * 1.  the languages, keyed by the graph file each one has on disk
   * ---------------------------------------------------------------- */

  var LANGS = [
    { key: "go", files: "graph_go_files.json", defs: "graph_go_defs.json",
      title: "go — cmd/compile lowering region",
      coverage: "coverage_go_files.json", diaries: "coverage_go2.json" },
    { key: "cpp", files: "graph_cpp_files.json", defs: "graph_cpp_defs.json",
      title: "c and cpp (clang) — CodeGen and Target/X86",
      coverage: null, diaries: null },
    { key: "rust", files: "graph_rust_files.json",
      defs: "graph_rust_defs.json",
      title: "rust (rustc) — codegen_ssa, codegen_llvm, middle/mir",
      coverage: null, diaries: null },
    { key: "swift", files: "graph_swift_files.json",
      defs: "graph_swift_defs.json",
      title: "swift (swiftc) — SILGen and IRGen",
      coverage: null, diaries: null }
  ];

  var COST_PAGE = "DevComms/log_175_task72_go_diaries_coverage.md";

  var MAX_EDGES_DRAWN = 1500;

  /* ---------------------------------------------------------------- *
   * 2.  style
   * ---------------------------------------------------------------- */

  var STYLE = [
    "#t-graph4 .g4bar{display:flex;gap:10px;align-items:center;",
    "flex-wrap:wrap;margin:0 0 8px}",
    "#t-graph4 .g4bar label{font-size:12px;opacity:.8;display:inline}",
    "#t-graph4 .g4bar select,#t-graph4 .g4bar button{width:auto;",
    "display:inline-block;margin:0;flex:0 0 auto;max-width:340px}",
    "#t-graph4 .g4bar select{min-width:120px}",
    "#t-graph4 .g4bar input[type=range]{width:auto;margin:0}",
    "#t-graph4 canvas{width:100%;height:560px;display:block;",
    "background:#0e1117;border-radius:6px;cursor:pointer}",
    "#t-graph4 .g4legend{display:flex;gap:14px;flex-wrap:wrap;",
    "font-size:11.5px;margin:6px 0 0;opacity:.85}",
    "#t-graph4 .g4swatch{display:inline-block;width:11px;height:11px;",
    "border-radius:2px;margin-right:4px;vertical-align:-1px}",
    "#t-graph4 .g4note{font-size:12px;opacity:.8;margin:6px 0}",
    "#t-graph4 .g4warn{border-left:3px solid #d08a2a;padding:6px 10px;",
    "font-size:12.5px;margin:8px 0;background:rgba(208,138,42,.08)}",
    "#t-graph4 .g4cols{display:grid;grid-template-columns:1fr 1fr;gap:14px}",
    "#t-graph4 .g4tip{font-family:ui-monospace,Menlo,monospace;",
    "font-size:11.5px;white-space:pre-wrap}",
    "#t-graph4 .g4scroll{max-height:340px;overflow:auto}",
    "#t-graph4 table{font-size:12px}",
    "#t-graph4 .g4pop{font-size:12px;opacity:.8;margin:4px 0 10px}"
  ].join("");

  var MARKUP = [
    '<div class="pop" id="pop-graph4"></div>',
    '<div class="card">',
    '<h2>the compiler as a graph — static structure, diary path, coverage</h2>',
    '<div class="g4bar">',
    '<label>compiler</label><select id="g4-lang"></select>',
    '<label>layout</label><select id="g4-layout">',
    '<option value="grouped">grouped by directory</option>',
    '<option value="force">force</option></select>',
    '<label>probe</label><select id="g4-probe"></select>',
    '<button class="act" id="g4-play">play the diary path</button>',
    '<input type="range" id="g4-step" min="0" max="0" value="0" ',
    'style="flex:1 1 240px;min-width:180px">',
    '<span id="g4-stepn" style="font-size:11.5px;opacity:.85"></span>',
    '<button class="act" id="g4-back">collapse to file level</button>',
    "</div>",
    '<div class="g4pop" id="g4-pop"></div>',
    '<canvas id="g4-canvas" width="1400" height="1120"></canvas>',
    '<div class="g4legend" id="g4-legend"></div>',
    '<div class="g4note" id="g4-paint"></div>',
    '<div class="g4tip" id="g4-tip"></div>',
    "</div>",
    '<div id="g4-cover"></div>'
  ].join("\n");

  /* ---------------------------------------------------------------- *
   * 3.  reading the artifacts.  Every read is named and bounded.
   * ---------------------------------------------------------------- */

  function readWhole(dir, name) {
    if (!dir) {
      return Promise.reject(new Error("no compiler_graph folder"));
    }
    return dir.getFileHandle(name).then(function (h) {
      return h.getFile();
    }).then(function (f) {
      return f.text();
    }).then(function (t) {
      return JSON.parse(t);
    });
  }

  /* THE RANGED READ.  One probe's full ordered path out of a 515 MB join,
   * by the byte offsets the summary carries.  Nothing else of that file is
   * read, ever. */
  function readRange(dir, name, start, end) {
    return dir.getFileHandle(name).then(function (h) {
      return h.getFile();
    }).then(function (f) {
      return f.slice(start, end).text();
    }).then(function (t) {
      return JSON.parse(t);
    });
  }

  /* ---------------------------------------------------------------- *
   * 4.  layout.  Two of them, both over FILE BOXES, never over nodes.
   * ---------------------------------------------------------------- */

  function dirOf(path) {
    var cut = path.lastIndexOf("/");
    return cut === -1 ? "." : path.slice(0, cut);
  }

  function boxSide(nodes, biggest) {
    var t = biggest > 0 ? Math.sqrt(nodes) / Math.sqrt(biggest) : 0;
    return 16 + t * 74;
  }

  function layoutGrouped(rows, width) {
    var biggest = rows.reduce(function (m, r) {
      return Math.max(m, r.nodes);
    }, 1);
    var groups = {};
    rows.forEach(function (r) {
      var d = dirOf(r.file);
      (groups[d] = groups[d] || []).push(r);
    });
    var names = Object.keys(groups).sort(function (a, b) {
      var na = groups[a].reduce(function (n, r) { return n + r.nodes; }, 0);
      var nb = groups[b].reduce(function (n, r) { return n + r.nodes; }, 0);
      return nb - na;
    });
    var pad = 12;
    var gapx = 26;
    var gapy = 34;
    var x = pad;
    var y = pad + 18;
    var rowHeight = 0;
    var placed = [];
    var bands = [];
    names.forEach(function (d) {
      var mine = groups[d].slice().sort(function (a, b) {
        return b.nodes - a.nodes;
      });
      var sides = mine.map(function (r) {
        return boxSide(r.nodes, biggest);
      });
      var per = Math.max(1, Math.ceil(Math.sqrt(mine.length)));
      var colw = 0;
      var i;
      for (i = 0; i < per; i += 1) {
        colw += sides[i] || 0;
      }
      colw = Math.max(colw + (per - 1) * 8, 90);
      if (x + colw + pad > width) {
        x = pad;
        y += rowHeight + gapy;
        rowHeight = 0;
      }
      var bx = x;
      var by = y;
      var cx = bx;
      var cy = by;
      var lineH = 0;
      var maxx = bx;
      mine.forEach(function (r, k) {
        var s = sides[k];
        if (cx > bx && cx + s > bx + colw) {
          cx = bx;
          cy += lineH + 8;
          lineH = 0;
        }
        placed.push({ row: r, x: cx, y: cy, w: s, h: s });
        cx += s + 8;
        maxx = Math.max(maxx, cx);
        lineH = Math.max(lineH, s);
      });
      var bh = (cy + lineH) - by;
      bands.push({ name: d, x: bx - 6, y: by - 16, w: colw + 12, h: bh + 22 });
      rowHeight = Math.max(rowHeight, bh + 22);
      x = bx + colw + gapx;
    });
    return { boxes: placed, bands: bands, height: y + rowHeight + pad };
  }

  function layoutForce(rows, edges, width, height) {
    var biggest = rows.reduce(function (m, r) {
      return Math.max(m, r.nodes);
    }, 1);
    var n = rows.length;
    var pos = rows.map(function (r, i) {
      var a = (i / n) * Math.PI * 2;
      return {
        row: r,
        x: width / 2 + Math.cos(a) * width * 0.33,
        y: height / 2 + Math.sin(a) * height * 0.33,
        w: boxSide(r.nodes, biggest),
        h: boxSide(r.nodes, biggest)
      };
    });
    var links = edges.map(function (e) {
      return [e[0], e[1], e[3]];
    });
    var iters = 220;
    var i;
    var k;
    for (i = 0; i < iters; i += 1) {
      var t = 1 - (i / iters);
      for (k = 0; k < n; k += 1) {
        var a = pos[k];
        var m;
        for (m = k + 1; m < n; m += 1) {
          var b = pos[m];
          var dx = a.x - b.x;
          var dy = a.y - b.y;
          var d2 = dx * dx + dy * dy + 0.01;
          var f = 22000 / d2;
          if (f > 4) { f = 4; }
          var d = Math.sqrt(d2);
          a.x += (dx / d) * f * t;
          a.y += (dy / d) * f * t;
          b.x -= (dx / d) * f * t;
          b.y -= (dy / d) * f * t;
        }
      }
      links.forEach(function (l) {
        var a2 = pos[l[0]];
        var b2 = pos[l[1]];
        if (!a2 || !b2) { return; }
        var dx2 = b2.x - a2.x;
        var dy2 = b2.y - a2.y;
        var d3 = Math.sqrt(dx2 * dx2 + dy2 * dy2) + 0.01;
        var pull = Math.min(0.06 * Math.log(1 + l[2]), 0.6) * t;
        a2.x += dx2 * pull * 0.02;
        a2.y += dy2 * pull * 0.02;
        b2.x -= dx2 * pull * 0.02;
        b2.y -= dy2 * pull * 0.02;
      });
    }
    var minx = Infinity;
    var miny = Infinity;
    var maxx = -Infinity;
    var maxy = -Infinity;
    pos.forEach(function (p) {
      minx = Math.min(minx, p.x);
      miny = Math.min(miny, p.y);
      maxx = Math.max(maxx, p.x + p.w);
      maxy = Math.max(maxy, p.y + p.h);
    });
    var sx = (width - 24) / Math.max(1, maxx - minx);
    var sy = (height - 24) / Math.max(1, maxy - miny);
    var s = Math.min(sx, sy, 1.6);
    pos.forEach(function (p) {
      p.x = 12 + (p.x - minx) * s;
      p.y = 12 + (p.y - miny) * s;
    });
    return { boxes: pos, bands: [], height: height };
  }

  /* ---------------------------------------------------------------- *
   * 5.  colour.  One scale for coverage, one flat fill where coverage is
   *     NOT MEASURED -- the two never look alike, so the page cannot be
   *     misread as measuring what it did not measure.
   * ---------------------------------------------------------------- */

  function shade(t) {
    /* t in [0,1]: pale slate at 0 visits, warm at every probe */
    var r = Math.round(40 + t * 200);
    var g = Math.round(58 + t * 120);
    var b = Math.round(86 - t * 40);
    return "rgb(" + r + "," + g + "," + b + ")";
  }

  var UNMEASURED_FILL = "#2b3444";
  var NEVER_FILL = "#3b2230";
  var LIT = "#ffd166";
  var PAST = "#5ea9ff";

  /* ---------------------------------------------------------------- *
   * 6.  the pane
   * ---------------------------------------------------------------- */

  function attach(root, source) {
    if (root.querySelector("#t-graph4")) {
      return;
    }
    var esc = DashboardJoin.esc;
    var num = DashboardJoin.num;

    var style = document.createElement("style");
    style.textContent = STYLE;
    document.head.appendChild(style);

    var nav = root.querySelector("#nav");
    var main = root.querySelector("main");
    if (!nav || !main) {
      return;
    }
    var btn = document.createElement("button");
    btn.dataset.t = "graph4";
    btn.textContent = "compiler graph & coverage — pane 4";
    nav.appendChild(btn);

    var sec = document.createElement("section");
    sec.className = "tab";
    sec.id = "t-graph4";
    sec.innerHTML = MARKUP;
    main.appendChild(sec);

    /* retire the join's own draft "3 . compiler coverage" tab: this pane
     * realizes coverage_view, so the draft placeholder it stands in for is
     * removed rather than left beside it (task 82, log_182 coordinator
     * note -- the tab bar had eight entries where the CORE numbers the
     * panes six, because each concurrent pane module appended its own tab
     * instead of retiring the draft it replaces). Safe here because
     * attach() runs after the join's own drawCoverage() has already run
     * (see install(), below) -- the draft section's content is never
     * needed again once this pane's own tab exists. */
    var draftBtn = root.querySelector('nav button[data-t="coverage"]');
    var draftSec = root.querySelector("#t-coverage");
    if (draftBtn) {
      draftBtn.remove();
    }
    if (draftSec) {
      draftSec.remove();
    }

    btn.onclick = function () {
      root.querySelectorAll("nav button").forEach(function (x) {
        x.classList.remove("on");
      });
      btn.classList.add("on");
      root.querySelectorAll(".tab").forEach(function (x) {
        x.classList.remove("on");
      });
      sec.classList.add("on");
      draw();
    };

    var dir = source && source.graphDir ? source.graphDir : null;
    var embedded = window.__PANE4__ || null;

    var state = {
      lang: "go",
      layout: "grouped",
      graph: {},        /* lang -> the files summary */
      defs: {},         /* lang -> the defs artifact */
      coverage: null,   /* coverage_go_files.json */
      probe: "",
      probePath: null,  /* the full ordered path of the chosen probe */
      fileRuns: null,   /* that path collapsed to file runs */
      step: -1,
      playing: null,
      expanded: null,   /* the one expanded file path */
      boxes: [],
      bands: [],
      edges: [],
      view: { x: 0, y: 0, k: 1 },
      paint: null,
      openedAt: new Date()
    };

    var canvas = sec.querySelector("#g4-canvas");
    var ctx = canvas.getContext("2d");

    var langSel = sec.querySelector("#g4-lang");
    langSel.innerHTML = LANGS.map(function (L) {
      return '<option value="' + L.key + '">' + esc(L.title) + "</option>";
    }).join("");

    /* ---------------- data ---------------- */

    function graphFor(key) {
      if (state.graph[key]) {
        return Promise.resolve(state.graph[key]);
      }
      if (embedded && embedded.graphs && embedded.graphs[key]) {
        state.graph[key] = embedded.graphs[key];
        return Promise.resolve(state.graph[key]);
      }
      var L = langOf(key);
      return readWhole(dir, L.files).then(function (doc) {
        state.graph[key] = doc;
        return doc;
      });
    }

    function defsFor(key) {
      if (state.defs[key]) {
        return Promise.resolve(state.defs[key]);
      }
      var L = langOf(key);
      return readWhole(dir, L.defs).then(function (doc) {
        state.defs[key] = doc;
        return doc;
      });
    }

    function coverageDoc() {
      if (state.coverage) {
        return Promise.resolve(state.coverage);
      }
      if (embedded && embedded.coverage) {
        state.coverage = embedded.coverage;
        return Promise.resolve(state.coverage);
      }
      return readWhole(dir, "coverage_go_files.json").then(function (doc) {
        state.coverage = doc;
        return doc;
      }).catch(function () {
        state.coverage = null;
        return null;
      });
    }

    function langOf(key) {
      var out = null;
      LANGS.forEach(function (L) {
        if (L.key === key) { out = L; }
      });
      return out;
    }

    /* per-file coverage row, by path, for the language on screen */
    function coverRow(path) {
      if (state.lang !== "go" || !state.coverage) {
        return null;
      }
      if (!state.coverIndex) {
        state.coverIndex = {};
        state.coverage.by_file.forEach(function (r) {
          state.coverIndex[r.file] = r;
        });
      }
      return state.coverIndex[path] || null;
    }

    /* how many of the 590 probes entered this file */
    function probesEntering(path) {
      if (state.lang !== "go" || !state.coverage) {
        return null;
      }
      if (!state.enterCount) {
        var slot = {};
        state.coverage.file_order.forEach(function (p, i) {
          slot[i] = p;
        });
        var counts = {};
        state.coverage.probes.forEach(function (pr) {
          var seen = {};
          pr.file_runs.forEach(function (run) {
            seen[slot[run[0]]] = true;
          });
          Object.keys(seen).forEach(function (p) {
            counts[p] = (counts[p] || 0) + 1;
          });
        });
        state.enterCount = counts;
      }
      return state.enterCount[path] || 0;
    }

    /* ---------------- drawing ---------------- */

    function fitBoxes() {
      var doc = state.graph[state.lang];
      if (!doc) { return; }
      var rows = doc.files.slice().filter(function (r) {
        return r.nodes > 0;
      });
      var order = {};
      doc.files.forEach(function (r, i) { order[r.file] = i; });
      var W = canvas.width;
      var H = canvas.height;
      var laid;
      if (state.layout === "force") {
        var idx = {};
        rows.forEach(function (r, i) { idx[r.file] = i; });
        var eds = doc.file_edges.map(function (e) {
          return [idx[doc.files[e[0]].file], idx[doc.files[e[1]].file],
                  e[2], e[3]];
        }).filter(function (e) {
          return e[0] !== undefined && e[1] !== undefined;
        });
        laid = layoutForce(rows, eds, W, H);
      } else {
        laid = layoutGrouped(rows, W);
      }
      state.boxes = laid.boxes;
      state.bands = laid.bands;
      state.boxAt = {};
      state.boxes.forEach(function (b) {
        state.boxAt[b.row.file] = b;
      });
      state.edges = doc.file_edges.slice(0, MAX_EDGES_DRAWN).map(function (e) {
        return {
          a: doc.files[e[0]] && doc.files[e[0]].file,
          b: doc.files[e[1]] && doc.files[e[1]].file,
          rel: e[2],
          n: e[3]
        };
      });
      state.edgesTotal = doc.file_edges.length;
      state.layoutHeight = laid.height;
      autofit();
    }

    /* AUTOFIT RUNS ONCE per layout and never again: any wheel or drag sets
     * `touched` and from then on the view is the person's, not ours.  The
     * same rule the fuzz explorer settled on, for the same reason. */
    function autofit() {
      if (state.touched) { return; }
      var minx = Infinity;
      var miny = Infinity;
      var maxx = -Infinity;
      var maxy = -Infinity;
      state.boxes.forEach(function (b) {
        minx = Math.min(minx, b.x);
        miny = Math.min(miny, b.y - 18);
        maxx = Math.max(maxx, b.x + b.w);
        maxy = Math.max(maxy, b.y + b.h);
      });
      state.bands.forEach(function (b) {
        minx = Math.min(minx, b.x);
        miny = Math.min(miny, b.y);
        maxx = Math.max(maxx, b.x + b.w);
        maxy = Math.max(maxy, b.y + b.h);
      });
      if (!isFinite(minx)) { return; }
      var k = Math.min((canvas.width - 24) / Math.max(1, maxx - minx),
                       (canvas.height - 24) / Math.max(1, maxy - miny));
      k = Math.max(0.2, Math.min(k, 4));
      state.view.k = k;
      state.view.x = 12 - minx * k +
        Math.max(0, (canvas.width - 24 - (maxx - minx) * k) / 2);
      state.view.y = 12 - miny * k +
        Math.max(0, (canvas.height - 24 - (maxy - miny) * k) / 2);
    }

    function litSet() {
      /* which files are lit at the current step of the diary path */
      if (!state.fileRuns || state.step < 0) {
        return null;
      }
      var out = { now: null, past: {} };
      var i;
      for (i = 0; i <= state.step && i < state.fileRuns.length; i += 1) {
        var p = state.fileRuns[i][0];
        if (i === state.step) {
          out.now = p;
        } else {
          out.past[p] = true;
        }
      }
      return out;
    }

    function drawFileLevel() {
      var t0 = performance.now();
      var doc = state.graph[state.lang];
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.fillStyle = "#0e1117";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      if (!doc) {
        return;
      }
      ctx.save();
      ctx.translate(state.view.x, state.view.y);
      ctx.scale(state.view.k, state.view.k);

      /* the directory bands, so the grouping is visible and not implied */
      ctx.font = "12px ui-monospace,Menlo,monospace";
      state.bands.forEach(function (b) {
        ctx.strokeStyle = "rgba(255,255,255,.10)";
        ctx.lineWidth = 1;
        ctx.strokeRect(b.x, b.y, b.w, b.h);
        ctx.fillStyle = "rgba(255,255,255,.45)";
        ctx.fillText(b.name.split("/").slice(-2).join("/"), b.x + 2, b.y - 3);
      });

      /* the wires */
      state.edges.forEach(function (e) {
        var A = state.boxAt[e.a];
        var B = state.boxAt[e.b];
        if (!A || !B) { return; }
        var alpha = Math.min(0.45, 0.05 + Math.log(1 + e.n) / 22);
        ctx.strokeStyle = "rgba(140,170,220," + alpha.toFixed(3) + ")";
        ctx.lineWidth = 0.8;
        ctx.beginPath();
        ctx.moveTo(A.x + A.w / 2, A.y + A.h / 2);
        ctx.lineTo(B.x + B.w / 2, B.y + B.h / 2);
        ctx.stroke();
      });

      var lit = litSet();
      var measured = state.lang === "go" && !!state.coverage;

      /* the diary path, drawn as arrows over the wiring: the last steps the
       * probe took, oldest faint, newest bright.  Order is the point, so it
       * is drawn as direction and not only as colour. */
      if (state.fileRuns && state.step >= 0) {
        var from = Math.max(0, state.step - 24);
        var q;
        for (q = from; q < state.step; q += 1) {
          var A0 = state.boxAt[state.fileRuns[q][0]];
          var B0 = state.boxAt[state.fileRuns[q + 1][0]];
          if (!A0 || !B0) { continue; }
          var age = (q - from + 1) / (state.step - from + 1);
          ctx.strokeStyle = "rgba(255,209,102," + (0.15 + age * 0.75).toFixed(3) + ")";
          ctx.lineWidth = 1 + age * 2;
          ctx.beginPath();
          ctx.moveTo(A0.x + A0.w / 2, A0.y + A0.h / 2);
          ctx.lineTo(B0.x + B0.w / 2, B0.y + B0.h / 2);
          ctx.stroke();
        }
      }

      state.boxes.forEach(function (b) {
        var fill = UNMEASURED_FILL;
        if (measured) {
          var row = coverRow(b.row.file);
          var entered = probesEntering(b.row.file);
          if (!row || row.instrumented === 0) {
            fill = UNMEASURED_FILL;
          } else if (entered === 0) {
            fill = NEVER_FILL;
          } else {
            fill = shade(entered / (state.coverage.populations.probes || 1));
          }
        }
        ctx.fillStyle = fill;
        ctx.fillRect(b.x, b.y, b.w, b.h);
        var strokeColor = "rgba(255,255,255,.16)";
        var lw = 1;
        if (lit && lit.now === b.row.file) {
          ctx.fillStyle = LIT;
          ctx.fillRect(b.x, b.y, b.w, b.h);
          strokeColor = "#ffffff";
          lw = 3;
        } else if (lit && lit.past[b.row.file]) {
          strokeColor = PAST;
          lw = 1.6;
        }
        ctx.strokeStyle = strokeColor;
        ctx.lineWidth = lw;
        ctx.strokeRect(b.x, b.y, b.w, b.h);
        if (b.w > 42) {
          ctx.fillStyle = "rgba(255,255,255,.72)";
          ctx.font = "9px ui-monospace,Menlo,monospace";
          var nm = b.row.file.split("/").pop();
          ctx.fillText(nm.slice(0, Math.floor(b.w / 5.2)), b.x + 3,
                       b.y + b.h - 4);
        }
      });
      ctx.restore();
      state.paint = performance.now() - t0;
      reportPaint("file level");
    }

    function drawExpanded() {
      var t0 = performance.now();
      var doc = state.defs[state.lang];
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.fillStyle = "#0e1117";
      ctx.fillRect(0, 0, canvas.width, canvas.height);
      if (!doc) { return; }
      var mine = doc.by_file[state.expanded] || [];
      if (!doc.__flat) {
        var slotOf = {};
        var flat = [];
        Object.keys(doc.by_file).forEach(function (f) {
          doc.by_file[f].forEach(function (d) {
            slotOf[d.id] = flat.length;
            flat.push(d);
          });
        });
        doc.__flat = flat;
        doc.__slotOf = slotOf;
      }
      var flat = doc.__flat;
      var slotOf = doc.__slotOf;
      var mySlots = {};
      mine.forEach(function (d) {
        mySlots[slotOf[d.id]] = true;
      });

      var cols = Math.max(1, Math.ceil(Math.sqrt(mine.length * 1.7)));
      var cw = (canvas.width - 40) / cols;
      var ch = 46;
      var place = {};
      mine.forEach(function (d, i) {
        place[d.id] = {
          x: 20 + (i % cols) * cw,
          y: 46 + Math.floor(i / cols) * ch,
          w: cw - 10,
          h: ch - 12,
          def: d
        };
      });

      ctx.fillStyle = "rgba(255,255,255,.8)";
      ctx.font = "14px ui-monospace,Menlo,monospace";
      ctx.fillText(state.expanded + " — " + mine.length + " definitions",
                   20, 26);

      /* the definition-to-definition edges that stay inside this file */
      ctx.strokeStyle = "rgba(140,170,220,.30)";
      ctx.lineWidth = 0.8;
      doc.def_edges.forEach(function (e) {
        if (!mySlots[e[0]] || !mySlots[e[1]]) { return; }
        var A = place[flat[e[0]].id];
        var B = place[flat[e[1]].id];
        if (!A || !B) { return; }
        ctx.beginPath();
        ctx.moveTo(A.x + A.w / 2, A.y + A.h);
        ctx.lineTo(B.x + B.w / 2, B.y);
        ctx.stroke();
      });

      var visitors = (state.coverage && state.lang === "go")
        ? state.coverage.per_def_visitors : null;
      var probes = state.coverage
        ? (state.coverage.populations.probes || 1) : 1;
      var order = insideFileOrder();

      mine.forEach(function (d) {
        var p = place[d.id];
        var fill = UNMEASURED_FILL;
        if (visitors) {
          var n = visitors[d.id] || 0;
          fill = n === 0 ? NEVER_FILL : shade(n / probes);
        }
        ctx.fillStyle = fill;
        ctx.fillRect(p.x, p.y, p.w, p.h);
        var at = order ? order.lastIndexOf(d.start_line) : -1;
        ctx.strokeStyle = at === -1 ? "rgba(255,255,255,.16)"
          : (at === order.length - 1 ? LIT : PAST);
        ctx.lineWidth = at === -1 ? 1 : 2;
        ctx.strokeRect(p.x, p.y, p.w, p.h);
        ctx.fillStyle = "rgba(255,255,255,.85)";
        ctx.font = "10px ui-monospace,Menlo,monospace";
        var text = (d.label || "") + "  :" + d.start_line;
        ctx.fillText(text.slice(0, Math.floor(p.w / 5.6)), p.x + 4,
                     p.y + p.h / 2 + 3);
      });
      state.expandedPlaces = place;
      state.expandedEdges = doc.def_edges.reduce(function (n, e) {
        return n + ((mySlots[e[0]] && mySlots[e[1]]) ? 1 : 0);
      }, 0);
      state.expandedLit = order ? order.length : 0;
      state.paint = performance.now() - t0;
      reportPaint("one file expanded");
    }

    /* the function-level order the chosen probe walked INSIDE the expanded
     * file, up to the current step: the declaration lines, in order */
    function insideFileOrder() {
      if (!state.probePath || !state.expanded) {
        return null;
      }
      var want = state.expanded + ":";
      var out = [];
      var upto = state.probePath.length;
      if (state.fileRuns && state.step >= 0) {
        /* the diary path is ordered, so the current file-level step names
         * a position in the full event stream: sum the runs up to it. */
        var used = 0;
        var r;
        for (r = 0; r <= state.step && r < state.fileRuns.length; r += 1) {
          used += state.fileRuns[r][1];
        }
        upto = Math.min(upto, used);
      }
      var i;
      for (i = 0; i < upto; i += 1) {
        var ev = state.probePath[i];
        if (ev.lastIndexOf(want, 0) === 0) {
          var line = parseInt(ev.slice(want.length), 10);
          if (out[out.length - 1] !== line) {
            out.push(line);
          }
        }
      }
      return out;
    }

    function syncStep() {
      var sl = sec.querySelector("#g4-step");
      var n = state.fileRuns ? state.fileRuns.length : 0;
      sl.max = String(Math.max(0, n - 1));
      sl.value = String(Math.max(0, state.step));
      sl.disabled = n === 0;
      sec.querySelector("#g4-stepn").textContent = n
        ? ("step " + num(Math.max(0, state.step) + 1) + " of " + num(n) +
           " — " + (state.fileRuns[Math.max(0, state.step)] || [""])[0])
        : "";
    }

    function draw() {
      syncStep();
      if (state.expanded) {
        drawExpanded();
      } else {
        drawFileLevel();
      }
      paintLegend();
    }

    function reportPaint(what) {
      var doc = state.graph[state.lang];
      var boxes = state.expanded
        ? Object.keys(state.expandedPlaces || {}).length
        : state.boxes.length;
      var line = "PAINT " + state.paint.toFixed(1) + " ms — " + what +
        ", " + num(boxes) + " boxes and " +
        num(state.expanded ? (state.expandedEdges || 0) : state.edges.length) +
        " wires drawn" +
        (state.expanded
          ? " inside the file; " + num(state.expandedLit || 0) +
            " of its definitions are on the chosen probe's path so far"
          : " of " + num(state.edgesTotal || 0) + " inter-file edge pairs") +
        (doc ? "; the graph behind them is " + num(doc.counts.nodes) +
          " nodes and " + num(doc.counts.edges) + " edges in " +
          num(doc.counts.files) + " files" : "");
      sec.querySelector("#g4-paint").textContent = line;
      if (window.console) {
        window.console.log("[pane4] " + state.lang + " " + line);
      }
    }

    function paintLegend() {
      var measured = state.lang === "go" && !!state.coverage;
      var bits = [];
      function sw(color, text) {
        return '<span><span class="g4swatch" style="background:' + color +
          '"></span>' + esc(text) + "</span>";
      }
      if (measured) {
        bits.push(sw(shade(0.02), "entered by few probes"));
        bits.push(sw(shade(0.5), "entered by about half"));
        bits.push(sw(shade(1), "entered by every probe"));
        bits.push(sw(NEVER_FILL, "instrumented and never entered"));
        bits.push(sw(UNMEASURED_FILL,
                     "no instrumented body — a named frontier"));
      } else {
        bits.push(sw(UNMEASURED_FILL, "coverage NOT MEASURED for this " +
                     "compiler — no diaries exist"));
      }
      bits.push(sw(LIT, "the diary's current step"));
      bits.push(sw(PAST, "already walked by this probe"));
      sec.querySelector("#g4-legend").innerHTML = bits.join("");
    }

    /* ---------------- the population line ---------------- */

    function paintPop() {
      var doc = state.graph[state.lang];
      var when = state.openedAt.toTimeString().slice(0, 8);
      var parts = [];
      if (doc) {
        parts.push(num(doc.counts.nodes) + " graph nodes, " +
          num(doc.counts.edges) + " edges and " +
          num(doc.counts.frontier) + " frontier records over " +
          num(doc.counts.files) + " files, read as " +
          num(doc.files.length) + " file rows from " +
          esc(langOf(state.lang).files));
      } else {
        parts.push("no graph summary for " + esc(state.lang));
      }
      if (state.lang === "go" && state.coverage) {
        var P = state.coverage.populations;
        parts.push(num(P.probes) + " probes with a diary; " +
          num(P.instrumented_bodies) + " instrumented bodies of " +
          num(P.defs) + " definitions (" +
          num(P.uninstrumented_defs_a_named_frontier) +
          " uninstrumented — a named frontier); " +
          num(P.visited_by_at_least_one_probe) + " visited, " +
          num(P.never_visited) + " never");
      } else {
        parts.push("0 probes: the dynamic structure and the coverage are " +
          "NOT MEASURED for this compiler");
      }
      parts.push("opened at " + when);
      sec.querySelector("#g4-pop").textContent = parts.join(" — ");
    }

    /* ---------------- the coverage listing under the canvas ------- */

    function paintCoverage() {
      var host = sec.querySelector("#g4-cover");
      if (state.lang !== "go" || !state.coverage) {
        var L = langOf(state.lang);
        host.innerHTML = '<div class="card">' +
          "<h2>the dynamic structure and the coverage — NOT MEASURED</h2>" +
          '<div class="g4warn">This compiler has a STATIC STRUCTURE and ' +
          "nothing else. No probe of the corpus has been compiled through " +
          "an instrumented build of it, so there is no diary, no path to " +
          "light up, and no visited or never-visited set. The boxes above " +
          "are shaded by nothing and say so.</div>" +
          '<p class="g4note">What it would take is measured, not guessed: ' +
          "task 72's cost page states the build time, the disk and the " +
          "emission hook for each of clang, rustc and swiftc on this " +
          "machine — <span class='mono'>" + esc(COST_PAGE) + "</span>. " +
          "Only go was diaried this lap (590 probes).</p>" +
          "<p class='g4note'>Static structure that IS measured for " +
          esc(L.title) + ": see the population line above and the file " +
          "boxes, every one of them read from <span class='mono'>" +
          esc(L.files) + "</span>.</p></div>";
        return;
      }

      var C = state.coverage;
      var P = C.populations;
      var never = C.never_entered_files;
      var byFile = {};
      C.never_visited_rows.forEach(function (r) {
        (byFile[r.file] = byFile[r.file] || []).push(r);
      });
      var files = Object.keys(byFile).sort(function (a, b) {
        var na = never.indexOf(a) === -1 ? 0 : 1;
        var nb = never.indexOf(b) === -1 ? 0 : 1;
        if (na !== nb) { return nb - na; }
        return byFile[b].length - byFile[a].length;
      });

      var html = '<div class="card"><h2>coverage over the corpus</h2>';
      html += '<p class="g4note">Population, every number a count over a ' +
        "file on disk: " + num(P.probes) + " probes; " +
        num(P.instrumented_bodies) + " instrumented bodies; " +
        num(P.visited_by_at_least_one_probe) + " visited by at least one " +
        "probe; " + num(P.never_visited) + " never visited; " +
        num(P.uninstrumented_defs_a_named_frontier) + " definitions that " +
        "carry no entry hook and are a NAMED FRONTIER, not never-visited " +
        "nodes.</p>";

      html += '<div class="g4cols">';
      html += "<div><h2 style='font-size:14px'>" + num(never.length) +
        " files no probe ever entered</h2><div class='g4scroll'><table>" +
        "<tr><th>file</th><th class='num'>instrumented bodies</th></tr>" +
        never.map(function (f) {
          var row = coverRow(f) || {};
          return "<tr><td class='mono'>" + esc(f) + "</td><td class='num'>" +
            num(row.instrumented || 0) + "</td></tr>";
        }).join("") + "</table></div></div>";

      html += "<div><h2 style='font-size:14px'>every file, by how much of " +
        "it the corpus reaches</h2><div class='g4scroll'><table>" +
        "<tr><th>file</th><th class='num'>instrumented</th>" +
        "<th class='num'>visited</th><th class='num'>never</th>" +
        "<th class='num'>probes entering</th></tr>" +
        C.by_file.slice().sort(function (a, b) {
          return b.instrumented - a.instrumented;
        }).map(function (r) {
          return "<tr><td class='mono'>" + esc(r.file) + "</td>" +
            "<td class='num'>" + num(r.instrumented) + "</td>" +
            "<td class='num'>" + num(r.visited) + "</td>" +
            "<td class='num'>" + num(r.never) + "</td>" +
            "<td class='num'>" + num(probesEntering(r.file)) + "</td></tr>";
        }).join("") + "</table></div></div>";
      html += "</div>";

      html += "<h2 style='font-size:14px;margin-top:14px'>the " +
        num(P.never_visited) + " never-visited bodies, by file</h2>" +
        "<div class='g4scroll'><table><tr><th>file</th>" +
        "<th class='num'>never visited</th><th>the bodies</th></tr>" +
        files.map(function (f) {
          var rows = byFile[f];
          var head = never.indexOf(f) === -1 ? "" : "◆ ";
          return "<tr><td class='mono'>" + esc(head + f) + "</td>" +
            "<td class='num'>" + num(rows.length) + "</td>" +
            "<td class='mono' style='font-size:11px'>" +
            rows.slice(0, 40).map(function (r) {
              return esc((r.label || "(unnamed)") + ":" + r.start_line);
            }).join(", ") +
            (rows.length > 40 ? " … and " + (rows.length - 40) + " more" : "") +
            "</td></tr>";
        }).join("") + "</table></div>" +
        "<p class='g4note'>◆ marks a file no probe entered at all. The " +
        "listing is the finding: this is compiler logic the corpus never " +
        "exercises.</p>";
      html += "</div>";
      host.innerHTML = html;
    }

    /* ---------------- the probe selector and the path ------------- */

    function fillProbes() {
      var sel = sec.querySelector("#g4-probe");
      if (state.lang !== "go" || !state.coverage) {
        sel.innerHTML = '<option value="">no diary for this compiler</option>';
        sel.disabled = true;
        return;
      }
      sel.disabled = false;
      sel.innerHTML = '<option value="">pick a probe…</option>' +
        state.coverage.probes.map(function (p) {
          return '<option value="' + esc(p.probe) + '">' + esc(p.probe) +
            " — " + num(p.events) + " events, " + num(p.file_runs_total) +
            " file steps</option>";
        }).join("");
    }

    function chooseProbe(id) {
      state.probe = id;
      state.step = -1;
      state.probePath = null;
      state.fileRuns = null;
      stopPlaying();
      if (!id) {
        draw();
        tip("");
        return;
      }
      var rec = null;
      state.coverage.probes.forEach(function (p) {
        if (p.probe === id) { rec = p; }
      });
      if (!rec) {
        tip("no probe with the unit id " + esc(id) + " has a diary. The " +
          "selector lists every one that does: " +
          num(state.coverage.probes.length) + " of them.");
        return;
      }
      tip("reading probe " + id + "'s path: one ranged read of " +
        "coverage_go2.json, bytes " + num(rec.byte_start) + "–" +
        num(rec.byte_end) + " (" +
        num(rec.byte_end - rec.byte_start) + " bytes of 515,160,866)…");
      var t0 = performance.now();
      readRange(dir, "coverage_go2.json", rec.byte_start, rec.byte_end)
        .then(function (path) {
          var ms = performance.now() - t0;
          state.probePath = path;
          state.fileRuns = collapse(path);
          state.step = 0;
          tip("probe " + id + ": " + num(path.length) +
            " diary events read in " + ms.toFixed(0) + " ms by ONE ranged " +
            "read of " + num(rec.byte_end - rec.byte_start) + " bytes; " +
            num(state.fileRuns.length) + " file-level steps. " +
            "The summary carried the first " + num(rec.file_runs_carried) +
            " of " + num(rec.file_runs_total) + " for the preview; this is " +
            "the whole path.");
          draw();
        }).catch(function (err) {
          /* the snapshot has no folder to slice: fall back to the preview
           * runs the summary carries, and say so. */
          state.fileRuns = rec.file_runs.map(function (run) {
            return [state.coverage.file_order[run[0]], run[1]];
          });
          state.step = 0;
          tip("probe " + id + ": coverage_go2.json could not be sliced (" +
            esc(String(err && err.message ? err.message : err)) +
            "), so the path shown is the first " +
            num(rec.file_runs_carried) + " file-level steps of " +
            num(rec.file_runs_total) + " that the summary carries. The " +
            "function-level path needs the live page.");
          draw();
        });
    }

    function collapse(path) {
      var out = [];
      var i;
      for (i = 0; i < path.length; i += 1) {
        var ev = path[i];
        var cut = ev.lastIndexOf(":");
        var f = cut === -1 ? ev : ev.slice(0, cut);
        if (out.length && out[out.length - 1][0] === f) {
          out[out.length - 1][1] += 1;
        } else {
          out.push([f, 1]);
        }
      }
      return out;
    }

    function tip(text) {
      sec.querySelector("#g4-tip").innerHTML = text;
    }

    function stopPlaying() {
      if (state.playing) {
        window.clearInterval(state.playing);
        state.playing = null;
        sec.querySelector("#g4-play").textContent = "play the diary path";
      }
    }

    sec.querySelector("#g4-play").onclick = function () {
      if (!state.fileRuns) { return; }
      if (state.playing) {
        stopPlaying();
        return;
      }
      sec.querySelector("#g4-play").textContent = "stop";
      state.playing = window.setInterval(function () {
        state.step += 1;
        if (state.step >= state.fileRuns.length) {
          state.step = state.fileRuns.length - 1;
          stopPlaying();
        }
        draw();
      }, 90);
    };

    sec.querySelector("#g4-step").oninput = function () {
      stopPlaying();
      state.step = parseInt(sec.querySelector("#g4-step").value, 10);
      draw();
    };

    sec.querySelector("#g4-back").onclick = function () {
      state.expanded = null;
      draw();
    };

    langSel.onchange = function () {
      state.lang = langSel.value;
      state.expanded = null;
      state.touched = false;
      state.coverIndex = null;
      state.enterCount = null;
      state.probe = "";
      state.probePath = null;
      state.fileRuns = null;
      state.step = -1;
      stopPlaying();
      load();
    };

    sec.querySelector("#g4-layout").onchange = function () {
      state.layout = sec.querySelector("#g4-layout").value;
      state.touched = false;
      fitBoxes();
      draw();
    };

    sec.querySelector("#g4-probe").onchange = function () {
      chooseProbe(sec.querySelector("#g4-probe").value);
    };

    canvas.onclick = function (ev) {
      var r = canvas.getBoundingClientRect();
      var x = (ev.clientX - r.left) * (canvas.width / r.width);
      var y = (ev.clientY - r.top) * (canvas.height / r.height);
      if (state.expanded) {
        return;
      }
      x = (x - state.view.x) / state.view.k;
      y = (y - state.view.y) / state.view.k;
      var hit = null;
      state.boxes.forEach(function (b) {
        if (x >= b.x && x <= b.x + b.w && y >= b.y && y <= b.y + b.h) {
          hit = b;
        }
      });
      if (!hit) { return; }
      var path = hit.row.file;
      tip("expanding " + path + " — reading " +
        esc(langOf(state.lang).defs) + " (the definitions, not the graph)…");
      defsFor(state.lang).then(function () {
        state.expanded = path;
        draw();
        var row = coverRow(path);
        tip(path + ": " + num(hit.row.defs) + " definitions, " +
          num(hit.row.nodes) + " graph nodes, " + num(hit.row.frontier) +
          " frontier records" +
          (row ? "; " + num(row.instrumented) + " instrumented bodies, " +
            num(row.visited) + " visited by at least one probe, " +
            num(row.never) + " never" : "; coverage NOT MEASURED") +
          ". Use “collapse to file level” to go back.");
      }).catch(function (err) {
        tip("could not expand " + path + ": " +
          esc(String(err && err.message ? err.message : err)) +
          ". The definitions artifact is read only on the live page.");
      });
    };

    canvas.onwheel = function (ev) {
      if (state.expanded) { return; }
      ev.preventDefault();
      var r = canvas.getBoundingClientRect();
      var x = (ev.clientX - r.left) * (canvas.width / r.width);
      var y = (ev.clientY - r.top) * (canvas.height / r.height);
      state.touched = true;
      var f = ev.deltaY < 0 ? 1.12 : 1 / 1.12;
      var k = Math.max(0.3, Math.min(6, state.view.k * f));
      state.view.x = x - (x - state.view.x) * (k / state.view.k);
      state.view.y = y - (y - state.view.y) * (k / state.view.k);
      state.view.k = k;
      draw();
    };

    (function drag() {
      var on = false;
      var lx = 0;
      var ly = 0;
      var moved = false;
      canvas.onmousedown = function (ev) {
        on = true;
        state.touched = true;
        moved = false;
        lx = ev.clientX;
        ly = ev.clientY;
      };
      window.addEventListener("mousemove", function (ev) {
        if (!on) { return; }
        var dx = ev.clientX - lx;
        var dy = ev.clientY - ly;
        if (Math.abs(dx) + Math.abs(dy) > 2) { moved = true; }
        lx = ev.clientX;
        ly = ev.clientY;
        var r = canvas.getBoundingClientRect();
        state.view.x += dx * (canvas.width / r.width);
        state.view.y += dy * (canvas.height / r.height);
        draw();
      });
      window.addEventListener("mouseup", function () {
        on = false;
      });
    }());

    /* ---------------- load ---------------- */

    function load() {
      return graphFor(state.lang).then(function () {
        return coverageDoc();
      }).then(function () {
        fitBoxes();
        paintPop();
        fillProbes();
        paintCoverage();
        draw();
        return true;
      }).catch(function (err) {
        sec.querySelector("#g4-pop").textContent =
          "the file-level summaries were not found: " +
          String(err && err.message ? err.message : err) +
          " — build them with graph_files_build.py and " +
          "coverage_files_build.py in Research/compiler_graph/.";
        return false;
      });
    }

    state.api = {
      load: load,
      draw: draw,
      state: state,
      chooseProbe: chooseProbe,
      expand: function (path) {
        return defsFor(state.lang).then(function () {
          state.expanded = path;
          draw();
        });
      },
      setLang: function (key) {
        langSel.value = key;
        langSel.onchange();
      }
    };
    window.__PANE4API__ = state.api;
    load();
  }

  /* ---------------------------------------------------------------- *
   * 7.  self-installation: wrap mount, change nothing inside it
   * ---------------------------------------------------------------- */

  function install() {
    if (typeof DashboardJoin === "undefined" || DashboardJoin.__pane4) {
      return;
    }
    var inner = DashboardJoin.mount;
    DashboardJoin.mount = function (source, root) {
      var out = inner(source, root);
      var run = function () {
        try {
          attach(root || document.body, source);
        } catch (err) {
          if (window.console) {
            window.console.warn("[dashboard] pane 4 did not attach:", err);
          }
        }
      };
      if (out && typeof out.then === "function") {
        return out.then(function (api) {
          run();
          return api;
        });
      }
      run();
      return out;
    };
    DashboardJoin.__pane4 = true;
  }

  install();

  return {
    attach: attach,
    install: install,
    STYLE: STYLE,
    LANGS: LANGS
  };
}());
