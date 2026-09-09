/* dashboard_pane1.js -- hq.research.compiler_graph.dashboard
 * (the unit_viewer sub-node), and hq.research.compiler_graph.arch_unit.context.
 *
 * Pane 1 completed: four more modes on the unit viewer, each reading a
 * file on disk at the moment the unit is opened, each printing the
 * population it counted over.
 *
 *   context                the bytes of every constant the body reaches
 *                          rip-relative, from canon39_context.json
 *   rendered back          the rendered text beside the wrapped text,
 *                          with the verdict, from render_back_store/
 *   verdicts               the wrapped-text verdict, BOTH term routes,
 *                          the reason strings and the counterexample,
 *                          from term65_store/ and regate64_store/
 *   interpreter source     the handler's C source where a record on
 *                          disk carries it, from
 *                          canon39_interp_source.json
 *
 * THE SPELLING BAN: every key here is a unit id, a file name or a
 * machine-form field name.  No operator token is written as a literal
 * anywhere in this file, so none can be a key
 * (check_dashboard_js_no_spelling.py proves it).
 *
 * This file adds; it rewrites nothing.  dashboard_join.js calls three
 * things on it: `modes`, `body(unit, mode)` and `enrich(source, unit)`.
 */

var DashboardPane1 = (function () {
  "use strict";

  /* ---------------------------------------------------------------- *
   * 1.  reading the sidecars.  One read per file per page, kept.
   * ---------------------------------------------------------------- */

  var cache = {};

  function readJson(source, name) {
    if (cache[name]) {
      return cache[name];
    }
    var dir = source && source.op;
    if (!dir || !dir.getFileHandle) {
      cache[name] = Promise.resolve(null);
      return cache[name];
    }
    cache[name] = dir.getFileHandle(name).then(function (h) {
      return h.getFile();
    }).then(function (f) {
      return f.text();
    }).then(function (t) {
      return JSON.parse(t);
    }).catch(function () {
      return null;
    });
    return cache[name];
  }

  function storeRow(source, which, unit) {
    if (!source || !source.storeRecord || !source.shardOf) {
      return Promise.resolve(null);
    }
    var where = source.shardOf[unit.id];
    if (!where) {
      return Promise.resolve(null);
    }
    return Promise.resolve(source.storeRecord(which, where.store, unit.id))
      .catch(function () {
        return null;
      });
  }

  /* ---------------------------------------------------------------- *
   * 2.  what pane 1 attaches to a unit before it is drawn
   * ---------------------------------------------------------------- */

  function enrich(source, unit) {
    return Promise.all([
      readJson(source, "canon39_context.json"),
      readJson(source, "canon39_interp_source.json"),
      readJson(source, "render_back_tally.json"),
      readJson(source, "audit65.json"),
      storeRow(source, "term65_store", unit),
      storeRow(source, "regate64_store", unit),
      storeRow(source, "render_back_store", unit)
    ]).then(function (all) {
      var ctx = all[0];
      var interp = all[1];
      unit.p1 = {
        hasFolder: !!(source && source.op && source.op.getFileHandle),
        contextDoc: ctx,
        context: ctx && ctx.units ? ctx.units[unit.id] : null,
        contextTally: ctx ? ctx.tally : null,
        interp: interp && interp.units ? interp.units[unit.id] : null,
        interpTally: interp ? interp.tally : null,
        renderTally: all[2] ? all[2].counts : null,
        termTally: all[3] ? all[3].term65 : null,
        termRow: all[4],
        gateRow: all[5],
        renderRow: all[6],
        readAt: new Date()
      };
      return unit;
    }).catch(function () {
      return unit;
    });
  }

  /* ---------------------------------------------------------------- *
   * 3.  drawing.  Small helpers of this file's own, so nothing in the
   *     join has to change.
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
    return String(n).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
  }

  function clock(d) {
    if (!d) {
      return "";
    }
    var h = String(d.getHours());
    var m = String(d.getMinutes());
    if (m.length < 2) {
      m = "0" + m;
    }
    return h + ":" + m;
  }

  function pop(text) {
    return '<p class="pop">' + esc(text) + "</p>";
  }

  function lines(text) {
    return esc(String(text || "").split("; ").join("\n"));
  }

  function needsLive() {
    return '<p class="note">this mode reads a file on disk when the ' +
      "unit is opened, so it needs the live page; the snapshot carries " +
      "no folder to read.</p>";
  }

  /* --- 3a. context --- */

  function contextBody(u) {
    var p1 = u.p1;
    if (!p1 || !p1.hasFolder) {
      return needsLive();
    }
    if (!p1.contextDoc) {
      return '<p class="note">canon39_context.json is not in the folder ' +
        "that was opened, so no constant can be shown.</p>";
    }
    var t = p1.contextTally || {};
    var line = "context: " + num(t.units_with_a_rip_relative_site) +
      " of 31,078 units reach a constant at an offset from the " +
      "instruction pointer; " + num(t.units_with_their_bytes) +
      " of those have their bytes, " +
      num(t.units_without_their_bytes) + " do not; " +
      num(t.rip_relative_sites) + " sites in all. Read from " +
      "canon39_context.json at " + clock(p1.readAt) + ".";
    var rec = p1.context;
    if (!rec) {
      return pop(line) + '<p class="note">the body of this unit reaches ' +
        "nothing at an offset from the instruction pointer, so it needs " +
        "no constant to run.</p>";
    }
    var html = pop(line);
    if (rec.built_with) {
      html += '<div class="kv"><span><b>sites</b> ' + num(rec.sites) +
        "</span><span><b>rebuilt bytes match the record</b> " +
        esc(String(rec.rebuilt_body_bytes_match_the_record)) +
        "</span><span><b>built with</b> " + esc(rec.built_with) +
        "</span></div>";
    }
    if (rec.context && rec.context.length) {
      html += "<table><tr><th>symbol</th><th class='num'>width</th>" +
        "<th>bytes</th><th>section</th></tr>";
      rec.context.forEach(function (c) {
        html += '<tr><td class="mono">' + esc(c.symbol) + "</td>" +
          '<td class="num">' + num(c.width) + "</td>" +
          '<td class="mono">' + esc(c.bytes) + "</td>" +
          "<td>" + esc(c.section) + "</td></tr>";
      });
      html += "</table>";
      html += '<p class="note">each row was read with ' +
        esc(rec.context[0].read_with) + ", off the object the lane's " +
        "own ship build produced again on this machine.</p>";
      html += "<pre>" + rec.context.map(function (c) {
        return esc(c.site) + "\n    " + esc(c.symbol) + " = " + esc(c.bytes);
      }).join("\n") + "</pre>";
    }
    if (rec.cause) {
      html += '<p class="note">no bytes: ' + esc(rec.cause) + "</p>";
    }
    if (rec.sites_with_no_bytes) {
      html += '<p class="note">' + rec.sites_with_no_bytes.map(esc)
        .join("<br>") + "</p>";
    }
    return html;
  }

  /* --- 3b. rendered back, beside the wrapped --- */

  function renderedBody(u) {
    var p1 = u.p1;
    if (!p1 || !p1.hasFolder) {
      return needsLive();
    }
    var c = p1.renderTally || {};
    var line = "rendered back: " + num(c.rendered) + " of " +
      num(c.units_with_a_proved_term) +
      " units with a proved term have a rendered text; " +
      num(c.assembled_by_as) + " assembled, " +
      num(c.round_tripped_through_objdump) +
      " round-tripped through objdump, " +
      num(c.character_identical_to_layer_3) +
      " character-identical to the wrapped text. Read from " +
      "render_back_tally.json and render_back_store/ at " +
      clock(p1.readAt) + ".";
    var r = p1.renderRow || u.rendered;
    if (!r) {
      return pop(line) + '<p class="note">render_back_store carries no ' +
        "record for this unit: a unit with no proved term is not " +
        "rendered back.</p>";
    }
    var html = pop(line);
    var v = r.verdict || {};
    html += '<div class="kv"><span><b>rendered</b> ' +
      esc(String(r.rendered)) + "</span>" +
      "<span><b>character-identical to the wrapped text</b> " +
      esc(String(r.character_identical_to_layer_3)) + "</span>" +
      "<span><b>verdict</b> " + esc(v.outcome || u.verdict) + "</span></div>";
    html += "<table><tr><th>the wrapped text</th>" +
      "<th>the rendered text</th></tr><tr>" +
      '<td><pre style="margin:0">' + lines(r.layer3_wrapped_text) +
      "</pre></td>" +
      '<td><pre style="margin:0">' +
      (r.rendered_wrapped_text
        ? lines(r.rendered_wrapped_text)
        : esc("not rendered")) +
      "</pre></td></tr></table>";
    if (v.reason) {
      html += '<p class="note">' + esc(v.reason) + "</p>";
    }
    if (r.why) {
      html += '<p class="note">' + esc(r.why) + "</p>";
    }
    if (r.refusal_cause) {
      html += '<p class="note">refused: ' + esc(r.refusal_cause) + "</p>";
    }
    if (r.assembly) {
      html += '<p class="note">the assembler wrote ' +
        num(r.assembly.instructions_written) + " instructions and read " +
        num(r.assembly.instructions_disassembled) + " back; round trips: " +
        esc(String(r.assembly.round_trips)) + ".</p>";
    }
    return html;
  }

  /* --- 3c. verdicts --- */

  function routeTable(rows) {
    var html = "<table><tr><th>route</th><th>outcome</th>" +
      "<th class='num'>solver ceiling, ms</th></tr>";
    rows.forEach(function (r) {
      html += "<tr><td>" + esc(r.route || "—") + "</td>" +
        "<td>" + esc(r.outcome || "—") + "</td>" +
        '<td class="num">' + num(r.solver_timeout_ms) + "</td></tr>";
    });
    return html + "</table>";
  }

  function verdictsBody(u) {
    var p1 = u.p1;
    if (!p1 || !p1.hasFolder) {
      return needsLive();
    }
    var t = p1.termTally || {};
    var line = "verdicts: " + num(t.records) +
      " units carry a record; " + num(t.proved) + " proved, " +
      num(t.disproved) + " disproved, " + num(t.undecided) +
      " undecided, " + num(t.no_term) +
      " with no term. Read from term65_store/, regate64_store/ and " +
      "audit65.json at " + clock(p1.readAt) + ".";
    var row = p1.termRow;
    var gate = p1.gateRow;
    if (!row && !gate) {
      return pop(line) + '<p class="note">no verdict record for this ' +
        "unit in term65_store or regate64_store.</p>";
    }
    row = row || {};
    var html = pop(line);
    html += '<div class="kv"><span><b>state</b> ' +
      esc(row.term_state || "—") + "</span>" +
      "<span><b>outcome</b> " + esc(row.outcome || "no term") + "</span>" +
      "<span><b>proved</b> " + esc(String(row.proved)) + "</span>" +
      "<span><b>the gate of record</b> " +
      esc(row.verdict_source || "regate64_store") + "</span></div>";
    var routes = [];
    if (row.verdict_ship) {
      routes.push(row.verdict_ship);
    }
    if (row.verdict_text) {
      routes.push(row.verdict_text);
    }
    if (routes.length) {
      html += routeTable(routes);
      routes.forEach(function (r) {
        html += '<p class="note"><b>' + esc(r.route) + "</b> — " +
          esc(r.reason) + "</p>";
        if (r.counterexample) {
          html += "<pre>" + esc(r.counterexample) + "</pre>";
        }
      });
    } else {
      html += '<p class="note">no route was run for this unit.</p>';
    }
    if (row.why_no_term) {
      html += '<p class="note">no term: ' + esc(row.why_no_term) + "</p>";
    }
    if (row.layer5_withdrawn) {
      html += '<p class="note">' + esc(row.layer5_withdrawn) + "</p>";
    }
    if (row.layer5_normalized_text) {
      html += "<pre>" + esc(row.layer5_normalized_text) + "</pre>";
    }
    if (gate && gate.guard_rows && gate.guard_rows.length) {
      html += '<p class="note">the gate of record counted ' +
        num(gate.guard_rows.length) + " guard rows, " +
        num(gate.branch_lines) + " branch lines and " +
        num(gate.call_lines) + " transfer lines on this body.</p>";
    }
    if (row.holes && row.holes.length) {
      html += "<table><tr><th>hole</th><th>line</th><th>why</th></tr>";
      row.holes.forEach(function (h) {
        if (!h || typeof h !== "object") {
          return;
        }
        html += "<tr><td>" + esc(h.row) + '</td><td class="mono">' +
          esc(h.line) + "</td><td>" + esc(h.why) + "</td></tr>";
      });
      html += "</table>";
    }
    return html;
  }

  /* --- 3d. the interpreter handler's own source --- */

  function interpBody(u) {
    var p1 = u.p1;
    if (!p1 || !p1.hasFolder) {
      return needsLive();
    }
    var t = p1.interpTally || {};
    var line = "interpreter units: " + num(t.interpreter_units) +
      " in the corpus; " + num(t.units_with_the_handler_c_source) +
      " carry the handler's C source, " +
      num(t.units_with_no_source_recorded) +
      " have no source recorded. Read from canon39_interp_source.json at " +
      clock(p1.readAt) + ".";
    var rec = p1.interp;
    if (!rec) {
      return pop(line) + '<p class="note">this is not an interpreter ' +
        "unit; it was compiled from a probe, and its high-level source is " +
        "the first mode.</p>";
    }
    var html = pop(line);
    html += '<div class="kv"><span><b>handler</b> <span class="mono">' +
      esc(rec.handler) + "</span></span></div>";
    if (!rec.source_recorded) {
      return html + '<p class="note">no source recorded — ' +
        esc(rec.cause) + "</p>";
    }
    html += '<div class="kv"><span><b>file</b> <span class="mono">' +
      esc(rec.file) + '</span></span><span><b>read from</b> <span ' +
      'class="mono">' + esc(rec.read_from) + "</span></span></div>";
    html += "<pre>" + rec.lines.map(function (l) {
      return esc(String(l.line)) + "  " + esc(l.text);
    }).join("\n") + "</pre>";
    if (rec.evidence) {
      html += '<p class="note">evidence: ' + esc(rec.evidence) + "</p>";
    }
    return html;
  }

  /* ---------------------------------------------------------------- *
   * 4.  what the join asks for
   * ---------------------------------------------------------------- */

  var MODES = [
    ["p1context", "context"],
    ["p1rendered", "rendered back, beside the wrapped"],
    ["p1verdicts", "verdicts"],
    ["p1interp", "interpreter handler source"]
  ];

  function body(unit, mode) {
    if (!unit) {
      return null;
    }
    if (mode === "p1context") {
      return contextBody(unit);
    }
    if (mode === "p1rendered") {
      return renderedBody(unit);
    }
    if (mode === "p1verdicts") {
      return verdictsBody(unit);
    }
    if (mode === "p1interp") {
      return interpBody(unit);
    }
    return null;
  }

  return {
    modes: MODES,
    body: body,
    enrich: enrich
  };
}());

if (typeof window !== "undefined") {
  window.DashboardPane1 = DashboardPane1;
}
