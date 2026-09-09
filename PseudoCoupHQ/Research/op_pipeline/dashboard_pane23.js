/* dashboard_pane23.js -- panes 2 and 3, hardened over the FULL population.
 *
 * Node: hq.research.compiler_graph.dashboard, methods `selector` and
 * `opcode_index`.  Brief: log_172 task 70.
 *
 * WHAT THIS FILE IS.  the owner numbered six things on the page.  Number 2 is
 * the SELECTOR -- random, and language then operator then type signature,
 * plus free text by unit id.  Number 3 is the ARCH OPCODE INDEX -- every
 * arch opcode, and the operator groups and signatures it appears in.
 * Task 68 built both against the whole corpus except for one hole it
 * named: a unit's SIGNATURE was only knowable once its probe manifest row
 * had been read, and a unit's row was only read when the unit was
 * clicked, so the signature menu was empty and the opcode pane's groups
 * all said "no signature recorded".  This file closes that hole over all
 * 31,078 units and hardens both panes for that size.
 *
 * IT IS A SEPARATE FILE ON PURPOSE.  Task 76 is editing dashboard.html at
 * the same time, so everything here lives in its own module and the live
 * page gains exactly one script tag.  It changes no behaviour of
 * dashboard_join.js or dashboard_loader.js: it WRAPS three of their
 * functions, and every wrap calls the original first.
 *
 *   DashboardJoin.mount              -> attach() after the panes exist
 *   LiveSource.prototype.absorb      -> keep the probe number and the OUT
 *                                       row's own width per index row
 *   LiveSource.prototype.indexAll    -> know when the index is complete
 *
 * THE SPELLING BAN, and how this file obeys it.  No operator token is a
 * key, a group, a pair, a row structure, a candidate set or a comparison
 * scope here.  Every grouping in this file is
 *
 *     lang + "#" + opGroup + "#" + sig
 *
 * where `opGroup` is the opaque per-language id the page mints (`c#g07`)
 * and `sig` is a type signature.  Neither is a token.  The token is
 * carried once, as `label`, on the unit's own row, and is read by nothing
 * but the text of an <option> and a table cell -- and `?labels=glyph`
 * replaces even that.  check_dashboard_js_no_spelling.py is run over this
 * file: no string literal in it is an operator token.
 *
 * THE SIGNATURE, and why it is read the way it is.  The signature is the
 * probe's DECLARED types -- what the probe generator asked the compiler
 * for -- with the result read off the OUT row's own width when the
 * compiler did not state a result type.  That rule is
 * DashboardJoin.signatureOf and this file calls it rather than restating
 * it.  Its two inputs come from two places:
 *
 *   the declared types   probe_manifest_<lang>.json   (original units)
 *                        probe_manifest2_<lang>.json  (regenerated units)
 *   the OUT row's width  the unit's own ledger, seen while the index is
 *                        being built
 *
 * The two regenerated manifests are 37 MB and 50 MB, because every probe
 * carries its full source text.  Parsing 92 MB of json in the browser to
 * keep three fields per probe is waste, so this file runs ONE regular
 * expression (SIG_RE) over the text and keeps only those three fields.
 * That shortcut is not asserted: pane23_manifest_regex_check.py runs the
 * same expression in python over all ten manifests and compares it, probe
 * for probe, with json.load -- 133,993 probes, identical.
 */

/* eslint-env browser */
var DashboardPane23 = (function () {
  "use strict";

  var LANGS = ["c", "cpp", "go", "rust", "swift"];

  /* the three declared type fields of one probe, in the order every
   * probe_manifest writes them, and always before the probe's `source`.
   * Proved equal to json.load by pane23_manifest_regex_check.py. */
  var SIG_RE = new RegExp(
    '"n"\\s*:\\s*(\\d+)\\s*,' +
    '[\\s\\S]*?"lhs_type"\\s*:\\s*(null|"(?:[^"\\\\]|\\\\.)*")' +
    '[\\s\\S]*?"rhs_type"\\s*:\\s*(null|"(?:[^"\\\\]|\\\\.)*")' +
    '[\\s\\S]*?"result_type"\\s*:\\s*(null|"(?:[^"\\\\]|\\\\.)*")',
    "g"
  );

  /* a match longer than this has run past the end of one probe object,
   * which would mean a probe is missing a field.  Counted, never
   * silently kept.  Measured: 0 over all ten manifests. */
  var SPAN_CEILING = 2000;

  /* pane 2 over the full population needs ceilings, because the biggest
   * arch opcode is in 30,432 units and 29,653 groups.  Both ceilings are
   * printed with the number they cut down from; nothing is hidden. */
  var GROUPS_DRAWN = 200;
  var IDS_DRAWN = 12;

  /* a map with no inherited keys.  A plain {} answers `true` for the key
   * "constructor", so an arch opcode of that spelling would make
   * `if (!map[m]) { map[m] = [] }` skip the assignment and then throw on
   * push.  Nothing in the corpus spells one today; the map is still made
   * this way so that nothing can. */
  function bare() {
    return Object.create(null);
  }

  function unq(s) {
    if (s === "null") {
      return null;
    }
    return JSON.parse(s);
  }

  function say() {
    var parts = Array.prototype.slice.call(arguments);
    console.log("[pane23] " + parts.join(" "));
  }

  /* ---------------------------------------------------------------- *
   * 1.  the declared types of every probe, over the full population
   * ---------------------------------------------------------------- */

  function manifestName(lang, pop) {
    if (pop === "regenerated") {
      return "probe_manifest2_" + lang + ".json";
    }
    return "probe_manifest_" + lang + ".json";
  }

  /* read one manifest as TEXT and keep three fields per probe. */
  function readTypes(dir, name, into, lang, pop, tally) {
    return dir.getFileHandle(name).then(function (fh) {
      return fh.getFile();
    }).then(function (f) {
      tally.bytes += f.size;
      return f.text();
    }).then(function (text) {
      var n = 0;
      var over = 0;
      SIG_RE.lastIndex = 0;
      var m = SIG_RE.exec(text);
      while (m) {
        if (m[0].length > SPAN_CEILING) {
          over += 1;
        } else {
          into[lang + "#" + pop + "#" + m[1]] = [
            unq(m[2]), unq(m[3]), unq(m[4])
          ];
          n += 1;
        }
        m = SIG_RE.exec(text);
      }
      tally.files += 1;
      tally.probes += n;
      tally.over += over;
      tally.per.push(lang + " " + pop + ": " + n + " probes");
      return n;
    }).catch(function (err) {
      tally.missing.push(name + " (" + (err && err.message ? err.message
        : err) + ")");
      return 0;
    });
  }

  function readAllTypes(dir) {
    var into = bare();
    var tally = {
      files: 0, probes: 0, over: 0, bytes: 0, per: [], missing: []
    };
    var jobs = [];
    LANGS.forEach(function (lang) {
      jobs.push(readTypes(dir, manifestName(lang, "original"), into, lang,
        "original", tally));
      jobs.push(readTypes(dir, manifestName(lang, "regenerated"), into, lang,
        "regenerated", tally));
    });
    return Promise.all(jobs).then(function () {
      return { types: into, tally: tally };
    });
  }

  /* ---------------------------------------------------------------- *
   * 2.  the wraps.  Each calls the original first and adds only.
   * ---------------------------------------------------------------- */

  function wrapLoader() {
    if (typeof DashboardLoader === "undefined" ||
        !DashboardLoader.LiveSource) {
      return;
    }
    var proto = DashboardLoader.LiveSource.prototype;
    if (proto.__pane23Wrapped) {
      return;
    }
    proto.__pane23Wrapped = true;

    /* absorb() already pushes one index row per unit.  Two more things
     * are needed per row and both are in the shard document that is open
     * at that moment: the probe number, which is how the manifest is
     * looked up, and the width of the unit's own OUT row, which is what
     * the signature uses when the compiler stated no result type.
     * Reading them later would mean re-reading 233 MB of shards. */
    var origAbsorb = proto.absorb;
    proto.absorb = function (doc, job) {
      var self = this;
      if (!self.__hardened) {
        self.__hardened = true;
        /* MEASURED DEFECT, and why this is setPrototypeOf and not a new
         * object.  The first cut of this wrap replaced both maps with
         * fresh ones.  DashboardJoin.mount had already read
         * source.opcodeIndex() at mount time and kept THAT object as
         * state.opcodeIndex, so every arch opcode absorbed afterwards
         * landed in a map nothing drew: the click-through reported
         * "arch opcode entries in the index: 0".  Stripping the
         * prototype in place keeps the identity the panes hold. */
        Object.setPrototypeOf(self.opcodeRows, null);
        Object.setPrototypeOf(self.shardOf, null);
      }
      var before = self.indexRows.length;
      origAbsorb.call(self, doc, job);
      var extra = bare();
      DashboardJoin.unitsOf(doc).forEach(function (u) {
        if (!u || !u.unit) {
          return;
        }
        var outSize = null;
        var ledger = u.ledger || [];
        for (var i = 0; i < ledger.length; i += 1) {
          if (String(ledger[i].row).indexOf("OUT") === 0) {
            outSize = ledger[i].size;
            break;
          }
        }
        extra[u.unit] = { n: u.n, outSize: outSize };
      });
      for (var i = before; i < self.indexRows.length; i += 1) {
        var row = self.indexRows[i];
        var e = extra[row.id];
        if (e) {
          row.probeNumber = e.n;
          row.outSize = e.outSize;
        }
      }
    };

    /* indexAll() is the background pass.  Wrapping it is how this module
     * learns that the index is complete without watching for a note
     * string on the population line. */
    var origIndexAll = proto.indexAll;
    proto.indexAll = function (onTick) {
      var self = this;
      var p = origIndexAll.call(self, onTick);
      return p.then(function (rows) {
        if (self.__pane23) {
          return self.__pane23.afterIndex(rows).then(function () {
            return rows;
          });
        }
        self.__indexArrived = rows;
        return rows;
      });
    };
  }

  function wrapMount() {
    if (typeof DashboardJoin === "undefined" || DashboardJoin.__pane23) {
      return;
    }
    DashboardJoin.__pane23 = true;
    var origMount = DashboardJoin.mount;
    DashboardJoin.mount = function (source, root) {
      return Promise.resolve(origMount(source, root)).then(function (api) {
        try {
          attach(source, api, root || document.body);
        } catch (err) {
          say("attach failed:", err && err.message ? err.message : err);
        }
        return api;
      });
    };
  }

  /* ---------------------------------------------------------------- *
   * 3.  attach -- panes 2 and 3, drawn from the source the join mounted
   * ---------------------------------------------------------------- */

  function attach(source, api, root) {
    var $ = function (s) {
      return root.querySelector(s);
    };

    var pane = {
      byId: bare(),
      opcodeIndex: bare(),
      sigTally: null,
      typeTally: null,
      osel: null,
      seedApplied: null
    };

    /* --- 3a. the two scope lines, one per pane, beside the population
     *         line the shell already paints.  The population line says
     *         what was READ; a scope line says what THIS pane holds. --- */

    function insertScopeLines() {
      if ($("#pop-selector")) {
        return;
      }
      /* full width, directly under the shell's own population line and
       * above the two-column split, so a line reads as a line. */
      function add(id, tab, text) {
        var el = document.createElement("div");
        el.className = "pop";
        el.id = id;
        el.textContent = text;
        var section = $(tab);
        var split = section ? section.querySelector(".split") : null;
        if (section && split) {
          section.insertBefore(el, split);
        }
      }
      add("pop-selector", "#t-units", "selector: the index is still arriving.");
      add("pop-opcode-index", "#t-opcodes",
        "arch opcode index: the index is still arriving.");
    }

    function drawScopeLines() {
      var t = pane.sigTally;
      var el = $("#pop-selector");
      if (el) {
        if (!t) {
          el.textContent = "selector: the index is still arriving; " +
            DashboardJoin.num(api.state.index.length) + " rows so far.";
        } else {
          el.textContent = "selector: " + DashboardJoin.num(t.rows) +
            " rows in the index · " + t.langs + " languages · " +
            DashboardJoin.num(t.groups) + " operator groups · " +
            DashboardJoin.num(t.sigs) + " type signatures over " +
            DashboardJoin.num(t.withSig) + " of " + DashboardJoin.num(t.rows) +
            " units · " + DashboardJoin.num(t.withoutSig) +
            " units have no signature (" + t.withoutWhy + ") · " +
            DashboardJoin.num(t.probes) + " probes read from " +
            t.probeFiles + " manifest files";
        }
      }
      var oel = $("#pop-opcode-index");
      if (oel) {
        var keys = Object.keys(pane.opcodeIndex);
        var totalGroups = 0;
        keys.forEach(function (k) {
          totalGroups += groupsOf(k).keys.length;
        });
        oel.textContent = "arch opcode index: " + DashboardJoin.num(keys.length) +
          " arch opcodes over " + DashboardJoin.num(api.state.index.length) +
          " units · " + DashboardJoin.num(totalGroups) +
          " (language, operator group, signature) groups · the token is a " +
          "label on the member, never a key";
      }
    }

    /* --- 3b. the language menu.  The shell fills it once, at mount; on
     *         the live page the index is empty at that moment, so it was
     *         filled with nothing and never refilled.  Refilled here on
     *         every repaint, from the index as it stands. --- */

    function refillLanguages() {
      var el = $("#f-lang");
      if (!el) {
        return;
      }
      var seen = bare();
      var langs = [];
      api.state.index.forEach(function (u) {
        if (u.lang && !seen[u.lang]) {
          seen[u.lang] = true;
          langs.push(u.lang);
        }
      });
      langs.sort();
      if (el.options.length === langs.length + 1) {
        return;
      }
      var keep = el.value;
      el.innerHTML = '<option value="">every language</option>' +
        langs.map(function (v) {
          return '<option value="' + DashboardJoin.esc(v) + '">' +
            DashboardJoin.esc(v) + "</option>";
        }).join("");
      if (langs.indexOf(keep) !== -1) {
        el.value = keep;
      }
    }

    /* --- 3c. pane 3: the arch opcode index --- */

    var groupCache = bare();

    function groupsOf(mnem) {
      if (groupCache[mnem]) {
        return groupCache[mnem];
      }
      var ids = pane.opcodeIndex[mnem] || [];
      var map = bare();
      var keys = [];
      var langs = bare();
      ids.forEach(function (id) {
        var u = pane.byId[id];
        if (!u) {
          return;
        }
        var k = u.lang + "#" + (u.opGroup || "no-group") + "#" +
          (u.sig || "no-signature-recorded");
        if (!map[k]) {
          map[k] = [];
          keys.push(k);
        }
        map[k].push(u);
        if (!langs[u.lang]) {
          langs[u.lang] = { units: 0, groups: bare(), sigs: bare() };
        }
        langs[u.lang].units += 1;
        langs[u.lang].groups[u.opGroup || "no-group"] = true;
        langs[u.lang].sigs[u.sig || "no-signature-recorded"] = true;
      });
      keys.sort();
      var out = { map: map, keys: keys, langs: langs, units: ids.length };
      groupCache[mnem] = out;
      return out;
    }

    function drawOpcodeList() {
      var box = $("#olist");
      if (!box) {
        return;
      }
      var txt = ($("#o-txt") && $("#o-txt").value || "").trim().toLowerCase();
      var keys = Object.keys(pane.opcodeIndex).filter(function (k) {
        return !txt || k.indexOf(txt) !== -1;
      });
      keys.sort(function (a, b) {
        return pane.opcodeIndex[b].length - pane.opcodeIndex[a].length;
      });
      var count = $("#ocount");
      if (count) {
        count.textContent = DashboardJoin.num(keys.length) +
          " arch opcodes shown of " +
          DashboardJoin.num(Object.keys(pane.opcodeIndex).length) +
          " in the index";
      }
      box.innerHTML = keys.map(function (k) {
        var on = pane.osel === k ? "on" : "";
        return '<div data-o="' + DashboardJoin.esc(k) + '" class="' + on +
          '"><span class="mono">' + DashboardJoin.esc(k) + "</span>" +
          '<span class="tag">' +
          DashboardJoin.num(pane.opcodeIndex[k].length) + "</span></div>";
      }).join("");
      box.querySelectorAll("div[data-o]").forEach(function (d) {
        d.onclick = function () {
          pane.osel = d.dataset.o;
          drawOpcodeList();
          drawOpcodePane();
        };
      });
    }

    function drawOpcodePane() {
      var box = $("#opane");
      if (!box || !pane.osel) {
        return;
      }
      var g = groupsOf(pane.osel);
      var langKeys = Object.keys(g.langs).sort();

      var head = '<div class="kv"><span><b>selected arch opcode</b> ' +
        '<span class="mono" style="font-size:15px">' +
        DashboardJoin.esc(pane.osel) + "</span></span>" +
        "<span><b>units</b> " + DashboardJoin.num(g.units) + "</span>" +
        "<span><b>groups</b> " + DashboardJoin.num(g.keys.length) +
        "</span></div>" +
        '<p class="note">A group is one (language, operator group, type ' +
        "signature). The operator group is an opaque per-language id; the " +
        "token beside it is a display label and is read by nothing.</p>";

      var summary = '<table><tr><th>language</th><th class="num">units</th>' +
        '<th class="num">operator groups</th>' +
        '<th class="num">type signatures</th></tr>' +
        langKeys.map(function (L) {
          var row = g.langs[L];
          return "<tr><td>" + DashboardJoin.esc(L) + "</td>" +
            '<td class="num">' + DashboardJoin.num(row.units) + "</td>" +
            '<td class="num">' +
            DashboardJoin.num(Object.keys(row.groups).length) + "</td>" +
            '<td class="num">' +
            DashboardJoin.num(Object.keys(row.sigs).length) + "</td></tr>";
        }).join("") + "</table>";

      /* the narrowing menus.  They are the reason this pane survives an
       * opcode that is in 30,432 units: without them the pane would try
       * to draw 29,653 groups. */
      var langOpts = '<option value="">every language</option>' +
        langKeys.map(function (L) {
          return '<option value="' + DashboardJoin.esc(L) + '">' +
            DashboardJoin.esc(L) + "</option>";
        }).join("");
      var sigSeen = bare();
      var sigs = [];
      g.keys.forEach(function (k) {
        var u = g.map[k][0];
        var s = u.sig || "no-signature-recorded";
        if (!sigSeen[s]) {
          sigSeen[s] = true;
          sigs.push(s);
        }
      });
      sigs.sort();
      var sigOpts = '<option value="">every signature</option>' +
        sigs.map(function (s) {
          return '<option value="' + DashboardJoin.esc(s) + '">' +
            DashboardJoin.esc(s) + "</option>";
        }).join("");

      var keepL = pane.oLang || "";
      var keepS = pane.oSig || "";
      var menus = '<div class="card"><h2>narrow these groups</h2>' +
        '<select id="og-lang">' + langOpts + "</select>" +
        '<select id="og-sig">' + sigOpts + "</select></div>";

      var shown = g.keys.filter(function (k) {
        var u = g.map[k][0];
        if (keepL && u.lang !== keepL) {
          return false;
        }
        if (keepS && (u.sig || "no-signature-recorded") !== keepS) {
          return false;
        }
        return true;
      });
      var cut = shown.length;
      var drawn = shown.slice(0, GROUPS_DRAWN);

      var bodyHtml = drawn.map(function (k) {
        var members = g.map[k];
        var u0 = members[0];
        var title = u0.lang + " · " +
          DashboardJoin.label(u0.label) + " · " +
          (u0.sig || "(no signature recorded)");
        var lines = members.slice(0, IDS_DRAWN).map(function (u) {
          return '<div class="mono jump" data-jump="' +
            DashboardJoin.esc(u.id) + '" style="margin-bottom:4px;' +
            'cursor:pointer">' + DashboardJoin.esc(u.id) + "</div>";
        }).join("");
        var more = "";
        if (members.length > IDS_DRAWN) {
          more = '<p class="note">…' +
            DashboardJoin.num(members.length - IDS_DRAWN) +
            " more unit ids in this group, not drawn</p>";
        }
        return "<details><summary>" + DashboardJoin.esc(title) +
          '<span class="tag"> — ' + DashboardJoin.num(members.length) +
          " unit" + (members.length > 1 ? "s" : "") + "</span></summary>" +
          '<div class="body">' + lines + more +
          '<p class="note">key: <span class="mono">' +
          DashboardJoin.esc(k) + "</span> — machine form; the token " +
          "above it is a label.</p></div></details>";
      }).join("");

      var ceiling = "";
      if (cut > GROUPS_DRAWN) {
        ceiling = '<p class="note">Drawing ' + DashboardJoin.num(GROUPS_DRAWN) +
          " of " + DashboardJoin.num(cut) + " groups that match the menus " +
          "above, out of " + DashboardJoin.num(g.keys.length) +
          " groups this arch opcode appears in. Narrow by language or " +
          "signature to see the rest.</p>";
      } else {
        ceiling = '<p class="note">Drawing all ' + DashboardJoin.num(cut) +
          " groups that match the menus above, out of " +
          DashboardJoin.num(g.keys.length) + " groups this arch opcode " +
          "appears in.</p>";
      }

      box.innerHTML = head + summary + menus + ceiling + bodyHtml;
      var lsel = box.querySelector("#og-lang");
      var ssel = box.querySelector("#og-sig");
      if (lsel) {
        lsel.value = keepL;
        lsel.onchange = function () {
          pane.oLang = lsel.value;
          drawOpcodePane();
        };
      }
      if (ssel) {
        ssel.value = keepS;
        ssel.onchange = function () {
          pane.oSig = ssel.value;
          drawOpcodePane();
        };
      }
      box.querySelectorAll("div[data-jump]").forEach(function (d) {
        d.onclick = function () {
          var b = root.querySelector('nav button[data-t="units"]');
          if (b) {
            b.click();
          }
          api.selectUnit(d.dataset.jump);
        };
      });
    }

    /* --- 3d. the seeded random sampler, and the seed in the address --- *
     *
     * A sample is only reproducible if BOTH halves of it are in the
     * address: the seed, and the scope the seed indexes into.  The
     * address therefore carries seed= and scope=, the scope being the
     * four selector controls.  Reloading restores the controls, then
     * indexes the same filtered list with the same seed, so the same
     * unit is selected.  Pressing the button again advances the seed by
     * the same linear congruential step and rewrites the address. */

    function readHash() {
      var h = window.location.hash || "";
      var seed = null;
      var scope = null;
      var m = /seed=(\d+)/.exec(h);
      if (m) {
        seed = Number(m[1]);
      }
      var s = /scope=([^&]*)/.exec(h);
      if (s && s[1]) {
        try {
          scope = JSON.parse(decodeURIComponent(s[1]));
        } catch (e) {
          scope = null;
        }
      }
      return { seed: seed, scope: scope };
    }

    function currentScope() {
      return {
        lang: $("#f-lang") ? $("#f-lang").value : "",
        group: $("#f-op") ? $("#f-op").value : "",
        sig: $("#f-sig") ? $("#f-sig").value : "",
        text: $("#f-txt") ? $("#f-txt").value : ""
      };
    }

    function writeHash(seed) {
      window.location.hash = "seed=" + seed + "&scope=" +
        encodeURIComponent(JSON.stringify(currentScope()));
    }

    function restoreScope(scope) {
      if (!scope) {
        return;
      }
      var order = [["#f-lang", "lang"], ["#f-op", "group"],
        ["#f-sig", "sig"]];
      order.forEach(function (pair) {
        var el = $(pair[0]);
        if (!el) {
          return;
        }
        var want = scope[pair[1]] || "";
        var ok = false;
        for (var i = 0; i < el.options.length; i += 1) {
          if (el.options[i].value === want) {
            ok = true;
          }
        }
        el.value = ok ? want : "";
        el.dispatchEvent(new Event("change"));
      });
      var t = $("#f-txt");
      if (t) {
        t.value = scope.text || "";
        t.dispatchEvent(new Event("input"));
      }
    }

    /* the same step the shell used: a linear congruential advance, so a
     * seed written into the address reproduces one sample and pressing
     * the button walks a stated sequence rather than a hidden one. */
    function nextSeed(seed) {
      return (seed * 1664525 + 1013904223) % 4294967296;
    }

    function applySeed(seed, why) {
      var f = api.filtered();
      if (!f.length) {
        say("seed", seed, "selected nothing:", "the filter matches 0 rows");
        return null;
      }
      var pick = f[seed % f.length];
      api.selectUnit(pick.id);
      pane.seedApplied = seed;
      say("seed", seed, "over", f.length, "filtered rows ->", pick.id,
        "(" + why + ")");
      return pick.id;
    }

    function takeOverSampler() {
      var btn = $("#rand");
      if (!btn) {
        return;
      }
      btn.onclick = function () {
        var h = readHash();
        var seed = h.seed === null
          ? Math.floor(Math.random() * 4294967296)
          : nextSeed(h.seed);
        writeHash(seed);
        applySeed(seed, "button");
      };
    }

    function applyHashOnLoad() {
      var h = readHash();
      if (h.seed === null) {
        return;
      }
      restoreScope(h.scope);
      applySeed(h.seed, "address bar on load");
    }

    /* --- 3e. the signature fill over the full population --- */

    function tallySignatures() {
      var rows = api.state.index;
      var seenSig = bare();
      var seenGroup = bare();
      var seenLang = bare();
      var withSig = 0;
      var why = bare();
      rows.forEach(function (r) {
        if (r.lang) {
          seenLang[r.lang] = true;
        }
        if (r.opGroup) {
          seenGroup[r.opGroup] = true;
        }
        if (r.sig) {
          withSig += 1;
          seenSig[r.sig] = true;
        } else {
          var k = r.lang + ", population " + (r.pop || "unstated");
          why[k] = (why[k] || 0) + 1;
        }
      });
      var causes = Object.keys(why).sort().map(function (k) {
        return k + ": " + why[k];
      });
      pane.sigTally = {
        rows: rows.length,
        withSig: withSig,
        withoutSig: rows.length - withSig,
        withoutWhy: causes.length ? causes.join("; ") : "none",
        sigs: Object.keys(seenSig).length,
        groups: Object.keys(seenGroup).length,
        langs: Object.keys(seenLang).length,
        probes: pane.typeTally ? pane.typeTally.probes : 0,
        probeFiles: pane.typeTally ? pane.typeTally.files : 0
      };
      return pane.sigTally;
    }

    function fillFromTypes(types) {
      var filled = 0;
      api.state.index.forEach(function (r) {
        if (r.sig) {
          return;
        }
        if (r.probeNumber === null || r.probeNumber === undefined) {
          return;
        }
        var t = types[r.lang + "#" + (r.pop || "original") + "#" +
          String(r.probeNumber)];
        if (!t) {
          return;
        }
        var ledger = [];
        if (r.outSize !== null && r.outSize !== undefined) {
          ledger.push({ row: "OUT-0", size: r.outSize });
        }
        r.sig = DashboardJoin.signatureOf(
          { lhs_type: t[0], rhs_type: t[1], result_type: t[2] },
          { ledger: ledger }
        );
        if (r.sig) {
          filled += 1;
        }
      });
      return filled;
    }

    /* the snapshot carries its unit bodies already, so its signatures are
     * filled by running the ONE join over each of them -- the same
     * packUnit the live page runs, not a second rule. */
    function fillFromSnapshot() {
      var filled = 0;
      api.state.index.forEach(function (r) {
        if (r.sig) {
          return;
        }
        var u = source.unit(r.id);
        if (u && u.sig) {
          r.sig = u.sig;
          filled += 1;
        }
      });
      return filled;
    }

    function rebuildById() {
      pane.byId = bare();
      api.state.index.forEach(function (u) {
        pane.byId[u.id] = u;
      });
      /* the panes hold ONE opcode map, the source's own.  It is not
       * copied here: the source fills it shard by shard while the page
       * is live, and a copy would freeze at the moment it was taken. */
      pane.opcodeIndex = api.state.opcodeIndex || bare();
      groupCache = bare();
    }

    /* --- 3f. the wiring --- */

    insertScopeLines();
    takeOverSampler();

    var otxt = $("#o-txt");
    if (otxt) {
      otxt.oninput = drawOpcodeList;
    }

    var origRepaint = api.repaintIndexPanes;
    api.repaintIndexPanes = function () {
      origRepaint();
      refillLanguages();
      rebuildById();
      drawOpcodeList();
      if (pane.osel) {
        drawOpcodePane();
      }
      drawScopeLines();
    };

    var pane23 = {
      afterIndex: function () {
        var t0 = window.performance.now();
        return readAllTypes(source.op).then(function (got) {
          pane.typeTally = got.tally;
          var read = window.performance.now();
          say("declared types read:", got.tally.probes, "probes from",
            got.tally.files, "manifest files,",
            (got.tally.bytes / 1e6).toFixed(1), "MB of text,",
            got.tally.over, "spans over the ceiling,",
            got.tally.missing.length, "files missing, in",
            (read - t0).toFixed(0), "ms");
          if (got.tally.missing.length) {
            say("missing manifests:", got.tally.missing.join("; "));
          }
          var filled = fillFromTypes(got.types);
          var t = tallySignatures();
          say("signatures filled:", filled, "of", t.rows, "rows;",
            t.withSig, "rows now carry one;", t.withoutSig, "do not (" +
            t.withoutWhy + ");", t.sigs, "distinct signatures;", t.groups,
            "operator groups;", t.langs, "languages");
          api.repaintIndexPanes();
          applyHashOnLoad();
          window.__pane23 = { tally: t, types: got.tally };
          say("PANES 2 AND 3 READY over the full population in",
            (window.performance.now() - t0).toFixed(0), "ms");
          return t;
        }).catch(function (err) {
          say("signature fill failed:",
            err && err.message ? err.message : err);
          return null;
        });
      }
    };

    if (source.kind === "live") {
      source.__pane23 = pane23;
      if (source.__indexArrived) {
        pane23.afterIndex(source.__indexArrived);
      }
    } else {
      var filled = fillFromSnapshot();
      var t = tallySignatures();
      say("snapshot: signatures filled:", filled, "of", t.rows, "rows;",
        t.sigs, "distinct signatures;", t.groups, "operator groups;",
        t.langs, "languages");
      api.repaintIndexPanes();
      applyHashOnLoad();
      window.__pane23 = { tally: t, types: null };
    }

    api.repaintIndexPanes();

    api.pane23 = {
      drawOpcodeList: drawOpcodeList,
      drawOpcodePane: drawOpcodePane,
      selectOpcode: function (m) {
        pane.osel = m;
        drawOpcodeList();
        drawOpcodePane();
      },
      applySeed: applySeed,
      nextSeed: nextSeed,
      readHash: readHash,
      writeHash: writeHash,
      state: pane
    };
    window.__pane23api = api;
  }

  wrapLoader();
  wrapMount();

  return {
    attach: attach,
    readAllTypes: readAllTypes,
    SIG_RE: SIG_RE,
    SPAN_CEILING: SPAN_CEILING,
    GROUPS_DRAWN: GROUPS_DRAWN
  };
}());
