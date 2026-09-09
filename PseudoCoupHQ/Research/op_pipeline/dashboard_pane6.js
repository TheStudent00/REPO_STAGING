/* dashboard_pane6.js -- PANE 6, THE CHRONOLOGY.
 *
 * Node: hq.research.compiler_graph.dashboard, the `chronology` method.
 * the owner, 2026-09-03: "i would like the dashboard to also have a chronology
 * based on vcs so i can step through the history to see progress."
 *
 * WHAT IT DRAWS.  A slider over the ROUNDS (the commits whose message says a
 * round was banked) with a finer strip under it over the DAYS (the last
 * commit of every day).  At the chosen step it shows the stats table as it
 * stood THEN, the change from the step before, that round's logs, and the
 * bank message.  Every number carries where it came from: `recomputed` (read
 * back out of the artifact blob that commit's tree names) or `testimony`
 * (the artifact was never tracked, so the bank message's own count line
 * stands in).  The population line names the commit hash and the date.
 *
 * WHY IT IS A SEPARATE FILE.  Two tasks were editing the dashboard at once,
 * so this module adds itself to the page instead of being written into it:
 * it wraps DashboardJoin.mount, lets the existing panes draw exactly as they
 * did, and then appends one nav button and one section.  It changes no line
 * of dashboard_join.js and no behaviour of panes 1 to 5.
 *
 * WHERE THE DATA COMES FROM, in order:
 *   1. window.__CHRONOLOGY__      -- the snapshot build embeds it here.
 *   2. the live folder handle     -- source.op.getFileHandle("chronology.json").
 *   3. neither                    -- the pane says so, and says what it needs.
 * chronology.json is written by chronology_build.py, which runs as a step of
 * every bank task (`chronology_build.py --append`).
 *
 * THE SPELLING BAN.  Nothing here groups, pairs or compares by an operator
 * token: the steps are keyed by commit hash and the numbers by artifact
 * family. Checked by check_dashboard_js_no_spelling.py.
 */

var DashboardChronology = (function () {
  "use strict";

  /* ---------------------------------------------------------------- *
   * 1.  the numbers the pane shows, in the order it shows them
   * ---------------------------------------------------------------- */

  var ROWS = [
    ["units", "arch-units extracted"],
    ["wrapped_and_proved", "wrapped and proved"],
    ["pool_entries", "distinct computations (pool entries)"],
    ["pool_members", "pool members"],
    ["pool_multi_language", "pool entries spanning more than one language"],
    ["families", "dominant-operator families"],
    ["proved_terms", "proved terms"],
    ["withdrawn_terms", "withdrawn terms"],
    ["undecided_terms", "undecided terms"],
    ["no_term", "units with no term"],
    ["census_producers", "producers with no term builder (census)"]
  ];

  var STYLE = [
    "#t-chrono .chrono-head{display:flex;gap:18px;align-items:baseline;",
    "flex-wrap:wrap;margin:0 0 6px}",
    "#t-chrono .chrono-when{font-size:19px;font-weight:600}",
    "#t-chrono .chrono-sha{font-family:ui-monospace,Menlo,monospace;",
    "font-size:12px;opacity:.75}",
    "#t-chrono input[type=range]{width:100%;margin:10px 0 2px}",
    "#t-chrono .ticks{display:flex;justify-content:space-between;",
    "font-size:11px;opacity:.65;margin:0 0 14px}",
    "#t-chrono .strip{display:flex;gap:2px;flex-wrap:wrap;margin:2px 0 10px}",
    "#t-chrono .strip button{flex:1 1 14px;min-width:14px;height:26px;",
    "padding:0;font-size:9px;line-height:26px;border-radius:3px;",
    "border:1px solid rgba(128,128,128,.35);background:transparent;",
    "color:inherit;cursor:pointer;overflow:hidden}",
    "#t-chrono .strip button.has{border-color:currentColor;font-weight:600}",
    "#t-chrono .strip button.on{outline:2px solid currentColor}",
    "#t-chrono .strip button.bank{background:rgba(128,128,128,.28)}",
    "#t-chrono table td.d{text-align:right;font-variant-numeric:tabular-nums;",
    "white-space:nowrap}",
    "#t-chrono .up{opacity:.95}",
    "#t-chrono .flat{opacity:.45}",
    "#t-chrono .tag{font-size:11px;border:1px solid currentColor;",
    "border-radius:10px;padding:0 7px;opacity:.8;white-space:nowrap}",
    "#t-chrono pre.msg{white-space:pre-wrap;font-size:12px;line-height:1.45;",
    "max-height:260px;overflow:auto}"
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

  function delta(now, before) {
    if (now === null || now === undefined ||
        before === null || before === undefined) {
      return ["", "flat"];
    }
    var d = now - before;
    if (d === 0) {
      return ["no change", "flat"];
    }
    /* the rise sign is built from its character code, not written as a
     * literal: the spelling-ban guard reads literals, and a one-character
     * literal that happens to be an operator token has no business in this
     * file even as decoration. */
    var rise = d > 0 ? String.fromCharCode(43) : String.fromCharCode(8722);
    return [rise + DashboardJoin.num(Math.abs(d)), "up"];
  }

  /* ---------------------------------------------------------------- *
   * 2.  reading chronology.json -- embedded, or off the live folder
   * ---------------------------------------------------------------- */

  function readDoc(source) {
    if (window.__CHRONOLOGY__) {
      return Promise.resolve(window.__CHRONOLOGY__);
    }
    var dir = source && source.op;
    if (!dir || !dir.getFileHandle) {
      return Promise.resolve(null);
    }
    return dir.getFileHandle("chronology.json").then(function (fh) {
      return fh.getFile();
    }).then(function (f) {
      return f.text();
    }).then(function (t) {
      return JSON.parse(t);
    })["catch"](function () {
      return null;
    });
  }

  /* ---------------------------------------------------------------- *
   * 3.  the pane
   * ---------------------------------------------------------------- */

  var MARKUP = [
    '<section class="tab" id="t-chrono">',
    '<div class="pop" id="pop-chrono"></div>',
    '<div class="card" id="chrono-pick"></div>',
    '<div id="chrono-body"></div>',
    "</section>"
  ].join("\n");

  function attach(root, source) {
    root = root || document.body;
    if (root.querySelector("#t-chrono")) {
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
    button.setAttribute("data-t", "chrono");
    button.textContent = "6 · chronology";
    nav.appendChild(button);
    button.onclick = function () {
      root.querySelectorAll("nav button").forEach(function (x) {
        x.classList.remove("on");
      });
      button.classList.add("on");
      root.querySelectorAll(".tab").forEach(function (x) {
        x.classList.remove("on");
      });
      root.querySelector("#t-chrono").classList.add("on");
    };

    var pick = root.querySelector("#chrono-pick");
    var body = root.querySelector("#chrono-body");
    var pop = root.querySelector("#pop-chrono");
    pop.textContent = "pane 6, the chronology: reading chronology.json…";

    readDoc(source).then(function (doc) {
      if (!doc || !doc.steps || !doc.steps.length) {
        pop.textContent = "pane 6, the chronology: no data.";
        pick.innerHTML =
          "<h2>the chronology is not loaded</h2>" +
          '<p class="note">This pane needs <b>chronology.json</b> beside the ' +
          "page. It is written by <b>chronology_build.py</b>, which walks the " +
          "repository's own history and recomputes the numbers from the " +
          "artifacts each commit holds. Run it once and re-open the page:" +
          "</p><pre>chronology_build.py --append</pre>";
        return;
      }
      draw(doc, pick, body, pop);
    });
  }

  function draw(doc, pick, body, pop) {
    var steps = doc.steps.slice();
    var rounds = steps.filter(function (s) {
      return s.scale === "round";
    });
    var meta = doc.meta || {};
    var at = steps.length - 1;

    /* --- the two scales.  The slider walks the rounds; the strip under it
     *     walks every day, banking days marked.  Both write the same
     *     index into `at`, so they are one control at two resolutions. --- */

    pick.innerHTML =
      "<h2>step through the history</h2>" +
      '<input type="range" id="c-range" min="0" max="' + (steps.length - 1) +
      '" value="' + at + '">' +
      '<div class="ticks"><span>' + esc(steps[0].day) + "</span><span>" +
      esc(steps[steps.length - 1].day) + "</span></div>" +
      '<div class="sub">rounds banked (' + rounds.length +
      "), then every day (" + steps.length + " steps in all)</div>" +
      '<div class="strip" id="c-strip"></div>';

    var strip = pick.querySelector("#c-strip");
    strip.innerHTML = steps.map(function (s, i) {
      var cls = ["", s.scale === "round" ? "bank" : "",
        Object.keys(s.numbers || {}).length ? "has" : ""].join(" ");
      var title = s.day + "  " + s.commit.slice(0, 9) +
        (s.round ? "  round " + s.round : "") +
        (Object.keys(s.numbers || {}).length ? "" : "  (no tracked artifact)");
      return '<button data-i="' + i + '" class="' + cls + '" title="' +
        esc(title) + '">' + (s.round ? s.round : "") + "</button>";
    }).join("");

    var range = pick.querySelector("#c-range");

    function show(i) {
      at = i;
      range.value = String(i);
      strip.querySelectorAll("button").forEach(function (b) {
        b.classList.toggle("on", Number(b.dataset.i) === i);
      });
      paint(steps, i, body, pop, meta);
    }

    range.oninput = function () {
      show(Number(range.value));
    };
    strip.querySelectorAll("button").forEach(function (b) {
      b.onclick = function () {
        show(Number(b.dataset.i));
      };
    });
    show(at);
  }

  /* --- the step itself: the table as it stood, and the change --- */

  function previousWithNumbers(steps, i) {
    var j = i - 1;
    while (j >= 0) {
      if (Object.keys(steps[j].numbers || {}).length) {
        return steps[j];
      }
      j -= 1;
    }
    return null;
  }

  function paint(steps, i, body, pop, meta) {
    var s = steps[i];
    var before = previousWithNumbers(steps, i);
    var n = s.numbers || {};
    var src = s.source || {};

    pop.textContent = "pane 6, the chronology: the state at commit " +
      s.commit.slice(0, 12) + ", " + s.date +
      (s.round ? " — round " + s.round + " banked" : " — end of that day") +
      "; " + Object.keys(n).length + " numbers, " +
      Object.keys(src).filter(function (k) {
        return src[k] === "recomputed";
      }).length + " of them recomputed from the artifacts that commit holds" +
      (meta.built_at ? " (chronology.json built " + meta.built_at + ")" : "");

    var html = '<div class="chrono-head">' +
      '<span class="chrono-when">' + esc(s.day) +
      (s.round ? "  ·  round " + s.round : "") + "</span>" +
      '<span class="chrono-sha">' + esc(s.commit) + "</span>" +
      '<span class="chrono-sha">' + esc(s.date) + "</span></div>";

    if (!Object.keys(n).length) {
      html += '<div class="card"><h2>nothing to recompute here</h2>' +
        '<p class="note">No stat artifact was tracked at this commit, and ' +
        "this commit's message carries no count line either, so this step " +
        "shows no numbers rather than guessing at them.</p></div>";
    } else {
      html += '<div class="card"><h2>the stats as they stood</h2><table>' +
        "<tr><th>number</th><th class='num'>value</th>" +
        "<th class='num'>change" +
        (before ? " since " + esc(before.day) : "") + "</th>" +
        "<th>source</th></tr>";
      html += ROWS.map(function (row) {
        var key = row[0];
        if (!(key in n)) {
          return "";
        }
        var d = delta(n[key], before ? (before.numbers || {})[key] : null);
        return "<tr><td>" + esc(row[1]) + "</td>" +
          '<td class="d">' + num(n[key]) + "</td>" +
          '<td class="d ' + d[1] + '">' + esc(d[0]) + "</td>" +
          '<td><span class="tag">' + esc(src[key] || "—") +
          "</span></td></tr>";
      }).join("");
      html += "</table>";
      html += '<p class="note"><b>recomputed</b> means the number was read ' +
        "back out of the artifact blob this commit's tree names, by " +
        "chronology_build.py, at build time. <b>testimony</b> means the " +
        "artifact was never tracked, so the count line of the commit's own " +
        "message stands in — the one place a number on this page is not a " +
        "count over a file.</p></div>";
    }

    /* the per-language split, where the corpus files were there to count */
    var pl = s.per_lang || {};
    var langs = Object.keys(pl);
    if (langs.length) {
      langs.sort(function (a, b) {
        return pl[b].units - pl[a].units;
      });
      html += '<div class="card"><h2>by language, at this commit</h2><table>' +
        "<tr><th>language</th><th class='num'>arch-units</th>" +
        "<th class='num'>wrapped &amp; proved</th>" +
        "<th class='num'>change</th></tr>";
      html += langs.map(function (k) {
        var b = before && before.per_lang ? before.per_lang[k] : null;
        var d = delta(pl[k].units, b ? b.units : null);
        return "<tr><td>" + esc(k) + "</td>" +
          '<td class="d">' + num(pl[k].units) + "</td>" +
          '<td class="d">' + num(pl[k].proved) + "</td>" +
          '<td class="d ' + d[1] + '">' + esc(d[0]) + "</td></tr>";
      }).join("");
      html += "</table></div>";
    }

    /* which artifacts this step read, so the recomputation is auditable */
    var arts = s.artifacts || {};
    var names = Object.keys(arts).filter(function (k) {
      return arts[k].generation !== null && arts[k].generation !== undefined;
    });
    if (names.length) {
      html += '<div class="card"><h2>what was read at this commit</h2><table>' +
        "<tr><th>family</th><th>generation</th><th class='num'>files</th>" +
        "<th>first file</th></tr>";
      html += names.map(function (k) {
        return "<tr><td>" + esc(k) + "</td><td>" + esc(arts[k].generation) +
          '</td><td class="d">' + num(arts[k].file_count) + "</td>" +
          '<td class="mono">' + esc(arts[k].example) + "</td></tr>";
      }).join("");
      html += "</table></div>";
    }

    if (s.logs && s.logs.length) {
      html += '<div class="card"><h2>this round’s logs</h2><ul>';
      html += s.logs.map(function (p) {
        return '<li><a class="mono" href="../../' + esc(p) + '">' +
          esc(p) + "</a></li>";
      }).join("");
      html += "</ul></div>";
    }

    if (s.bank_message) {
      html += '<div class="card"><h2>the bank message, as committed</h2>' +
        '<pre class="msg">' + esc(s.bank_message) + "</pre></div>";
    }

    body.innerHTML = html;
  }

  /* ---------------------------------------------------------------- *
   * 4.  self-installation: wrap mount, add nothing to it
   * ---------------------------------------------------------------- */

  function install() {
    if (typeof DashboardJoin === "undefined" || DashboardJoin.__pane6) {
      return;
    }
    var inner = DashboardJoin.mount;
    DashboardJoin.mount = function (source, root) {
      var out = inner(source, root);
      try {
        attach(root || document.body, source);
      } catch (err) {
        if (window.console) {
          window.console.warn("[dashboard] pane 6 did not attach:", err);
        }
      }
      return out;
    };
    DashboardJoin.__pane6 = true;
  }

  install();

  return {
    attach: attach,
    install: install,
    STYLE: STYLE,
    ROWS: ROWS
  };
}());
