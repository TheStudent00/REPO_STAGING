/* dashboard_loader.js -- the LIVE source: the page reads the artifacts itself.
 *
 * Node: hq.research.compiler_graph.dashboard, method `loader`.
 * the owner's two rulings this file exists to obey:
 *   - no server, no terminal.  The page is opened by double-click and asks
 *     once for the folder (File System Access API); the handle is kept in
 *     IndexedDB so the next open is one click of confirmation.
 *   - update mechanically.  Every number this source hands the panes is a
 *     count over a file on disk at the moment the page was opened.
 *
 * HOW IT STAYS UNDER TWO SECONDS TO FIRST PAINT.  Every artifact this line
 * writes puts `meta` and `tally` FIRST and the bodies last, and the graph
 * files put `pins` and `counts` first.  So the first paint reads PREFIX
 * SLICES, never whole files:
 *
 *   the_pool5.json          32 MB  -> the last 16 KB (the summary object)
 *   canon39_wrapped_*.json  14 MB  -> the first 4 KB each (meta + tally)
 *   canon39_regen_store/*  219 MB  -> the first 4 KB of each of 326 shards
 *   ../compiler_graph/graph_*.json 600 MB -> the first 256 KB each
 *
 * The unit index (ids, operators, signatures, arch opcodes) is built AFTER
 * the first paint, shard by shard, in the background; each pane's
 * population line ticks up as it lands.  A unit's body is read on demand,
 * from the one shard that holds it.
 *
 * No path of this machine appears anywhere in this file.  The page asks.
 */

/* eslint-env browser */
var DashboardLoader = (function () {
  "use strict";

  var LANGS = ["c", "cpp", "go", "rust", "swift"];
  var DB_NAME = "dashboard_handles";
  var DB_STORE = "handles";

  /* ---------------------------------------------------------------- *
   * 0.  the remembered folder handles (IndexedDB)
   * ---------------------------------------------------------------- */

  /* MEASURED, 2026-09-03, Chrome on this machine: a page opened by
   * double-click has origin "null" (opaque) and `indexedDB.open` there
   * fires NO event at all -- not success, not error, not blocked.  So the
   * remembered folder is only possible when the page is served from an
   * origin; from a double-clicked file the folder is chosen each time, and
   * the gate says so rather than hanging. */
  function opaqueOrigin() {
    try {
      if (window.location.protocol === "file:") {
        return true;
      }
      return String(window.origin) === "null";
    } catch (e) {
      return true;
    }
  }

  function openDb() {
    if (opaqueOrigin()) {
      return Promise.reject(new Error("no storage on an opaque origin"));
    }
    return new Promise(function (resolve, reject) {
      var timer = window.setTimeout(function () {
        reject(new Error("indexedDB.open answered nothing"));
      }, 1500);
      var settle = function (fn, value) {
        window.clearTimeout(timer);
        fn(value);
      };
      var req = window.indexedDB.open(DB_NAME, 1);
      req.onupgradeneeded = function () {
        req.result.createObjectStore(DB_STORE);
      };
      req.onsuccess = function () {
        settle(resolve, req.result);
      };
      req.onerror = function () {
        settle(reject, req.error);
      };
      req.onblocked = function () {
        settle(reject, new Error("indexedDB.open blocked"));
      };
    });
  }

  function dbGet(key) {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(DB_STORE, "readonly");
        var req = tx.objectStore(DB_STORE).get(key);
        req.onsuccess = function () {
          resolve(req.result || null);
        };
        req.onerror = function () {
          reject(req.error);
        };
      });
    }).catch(function () {
      return null;
    });
  }

  function dbPut(key, value) {
    return openDb().then(function (db) {
      return new Promise(function (resolve, reject) {
        var tx = db.transaction(DB_STORE, "readwrite");
        tx.objectStore(DB_STORE).put(value, key);
        tx.oncomplete = function () {
          resolve(true);
        };
        tx.onerror = function () {
          reject(tx.error);
        };
      });
    }).catch(function () {
      return false;
    });
  }

  function supported() {
    return typeof window.showDirectoryPicker === "function";
  }

  /* one click of confirmation on a remembered handle; null if the person
   * says no or the folder is gone. */
  function reconfirm(handle) {
    if (!handle) {
      return Promise.resolve(null);
    }
    return handle.queryPermission({ mode: "read" }).then(function (state) {
      if (state === "granted") {
        return handle;
      }
      return handle.requestPermission({ mode: "read" }).then(function (s) {
        return s === "granted" ? handle : null;
      });
    }).catch(function () {
      return null;
    });
  }

  /* ---------------------------------------------------------------- *
   * 1.  reading files out of a directory handle
   * ---------------------------------------------------------------- */

  function fileOf(dir, name) {
    return dir.getFileHandle(name).then(function (fh) {
      return fh.getFile();
    });
  }

  function readWhole(dir, name) {
    return fileOf(dir, name).then(function (f) {
      return f.text();
    }).then(JSON.parse);
  }

  function readWholeOrNull(dir, name) {
    if (!dir) {
      return Promise.resolve(null);
    }
    return readWhole(dir, name).catch(function () {
      return null;
    });
  }

  /* THE PREFIX SLICE.  Reads the first `n` bytes of a json file and pulls
   * out the named top-level objects by balanced-brace scan.  This is how a
   * 331 MB graph file answers the coverage pane in milliseconds. */
  function headObjects(dir, name, keys, n) {
    return fileOf(dir, name).then(function (f) {
      return f.slice(0, n || 262144).text();
    }).then(function (text) {
      var out = {};
      keys.forEach(function (k) {
        out[k] = carveObject(text, k);
      });
      return out;
    });
  }

  /* THE TAIL SLICE.  Same idea from the other end, for a file whose
   * summary is written last (the_pool5.json). */
  function tailObject(dir, name, key, n) {
    return fileOf(dir, name).then(function (f) {
      var start = Math.max(0, f.size - (n || 16384));
      return f.slice(start, f.size).text();
    }).then(function (text) {
      return carveObject(text, key);
    });
  }

  /* carve the value of `"key":` out of a fragment of json text, by
   * counting braces.  Returns null when the fragment does not hold the
   * whole value. */
  function carveObject(text, key) {
    var needle = '"' + key + '"';
    var at = text.indexOf(needle);
    if (at === -1) {
      return null;
    }
    var i = text.indexOf(":", at + needle.length);
    if (i === -1) {
      return null;
    }
    i += 1;
    while (i < text.length && /\s/.test(text[i])) {
      i += 1;
    }
    var open = text[i];
    if (open !== "{" && open !== "[") {
      return null;
    }
    var close = open === "{" ? "}" : "]";
    var depth = 0;
    var inStr = false;
    var escaped = false;
    var j = i;
    while (j < text.length) {
      var ch = text[j];
      if (inStr) {
        if (escaped) {
          escaped = false;
        } else if (ch === "\\") {
          escaped = true;
        } else if (ch === '"') {
          inStr = false;
        }
      } else if (ch === '"') {
        inStr = true;
      } else if (ch === open) {
        depth += 1;
      } else if (ch === close) {
        depth -= 1;
        if (depth === 0) {
          try {
            return JSON.parse(text.slice(i, j + 1));
          } catch (e) {
            return null;
          }
        }
      }
      j += 1;
    }
    return null;
  }

  function listJson(dir, prefix) {
    var names = [];
    return (async function () {
      for await (var entry of dir.values()) {
        if (entry.kind !== "file") {
          continue;
        }
        if (!/\.json$/.test(entry.name)) {
          continue;
        }
        if (prefix && entry.name.indexOf(prefix) !== 0) {
          continue;
        }
        names.push(entry.name);
      }
      names.sort();
      return names;
    }());
  }

  function subDir(dir, name) {
    if (!dir) {
      return Promise.resolve(null);
    }
    return dir.getDirectoryHandle(name).catch(function () {
      return null;
    });
  }

  /* ---------------------------------------------------------------- *
   * 2.  the live source
   * ---------------------------------------------------------------- */

  function LiveSource(dirs, report) {
    this.kind = "live";
    this.op = dirs.op;
    this.graphDir = dirs.graph;
    this.report = report || function () { return undefined; };
    this.groupsObj = new DashboardJoin.OperatorGroups();
    this.openedAt = new Date();
    this.pop = {
      units: 0,
      files: 0,
      openedAt: this.openedAt,
      note: "summaries read; unit index still arriving"
    };
    this.indexRows = [];
    this.opcodeRows = {};
    this.shardOf = {};
    this.perLang = {};
    this.stores = {};
    this.manifests = {};
    this.poolByUnit = null;
    this.statsObj = null;
    this.coverageObj = null;
  }

  /* --- 2a. phase one: the summaries.  This is what the first paint waits
   *         for, and nothing else. --- */

  LiveSource.prototype.readSummaries = function () {
    var self = this;
    var op = this.op;
    var files = 0;

    var wrapped = Promise.all(LANGS.map(function (lang) {
      return headObjects(op, "canon39_wrapped_" + lang + ".json",
        ["tally"], 4096).then(function (head) {
        files += 1;
        var t = head.tally || {};
        var total = Object.keys(t).reduce(function (n, k) {
          return n + t[k];
        }, 0);
        self.perLang[lang] = {
          units: total,
          proved: t.WRAPPED_TEXT_PROVED || 0
        };
      }).catch(function () {
        return undefined;
      });
    }));

    var interp = headObjects(op, "canon39_interp.json", ["tally"], 4096)
      .then(function (head) {
        files += 1;
        var t = head.tally || {};
        var total = Object.keys(t).reduce(function (n, k) {
          return n + t[k];
        }, 0);
        self.perLang.interpreter = {
          units: total,
          proved: t.WRAPPED_TEXT_PROVED || 0
        };
      }).catch(function () {
        return undefined;
      });

    var regen = subDir(op, "canon39_regen_store").then(function (d) {
      if (!d) {
        return [];
      }
      self.regenDir = d;
      return listJson(d);
    }).then(function (names) {
      self.regenShards = names;
      return Promise.all(names.map(function (name) {
        return headObjects(self.regenDir, name, ["tally"], 4096)
          .then(function (head) {
            files += 1;
            var t = head.tally || {};
            var lang = /op_units2_([a-z]+)_/.exec(name);
            lang = lang ? lang[1] : "unknown";
            if (!self.perLang[lang]) {
              self.perLang[lang] = { units: 0, proved: 0 };
            }
            var total = Object.keys(t).reduce(function (n, k) {
              return n + t[k];
            }, 0);
            self.perLang[lang].units += total;
            self.perLang[lang].proved += (t.WRAPPED_TEXT_PROVED || 0);
          }).catch(function () {
            return undefined;
          });
      }));
    });

    var pool = tailObject(op, "the_pool5.json", "summary", 32768)
      .then(function (s) {
        files += 1;
        return s || {};
      }).catch(function () {
        return {};
      });

    var families = readWholeOrNull(op, "the_families5.json");
    var census = readWholeOrNull(op, "name_census5.json");
    var terms = readWholeOrNull(op, "audit65.json");

    return Promise.all([wrapped, interp, regen, pool, families, census, terms])
      .then(function (all) {
        var poolSummary = all[3];
        var fam = all[4];
        var cen = all[5];
        var aud = all[6];
        if (fam) {
          files += 1;
        }
        if (cen) {
          files += 1;
        }
        if (aud) {
          files += 1;
        }
        var famCount = null;
        if (fam) {
          var f = fam.families || fam;
          famCount = Array.isArray(f) ? f.length : Object.keys(f).length;
        }
        var censusOut = { producers: null, rows: [] };
        if (cen && cen.entries) {
          censusOut.producers = cen.entries.length;
          censusOut.rows = cen.entries.slice(0, 12).map(function (e) {
            return {
              producer: DashboardJoin.censusName(e.producer),
              rows: e.rows_blocked === undefined ? e.rows : e.rows_blocked,
              units: e.units_blocked === undefined ? e.units : e.units_blocked
            };
          });
        }
        self.statsObj = {
          per_lang: self.perLang,
          pool: poolSummary,
          families: famCount,
          census: censusOut,
          terms: aud,
          groups: self.groupsObj
        };
        var total = Object.keys(self.perLang).reduce(function (n, k) {
          return n + self.perLang[k].units;
        }, 0);
        self.pop.units = total;
        self.pop.files = files;
        return self.statsObj;
      });
  };

  /* --- 2b. the coverage pane, from the graph files' own head --- */

  LiveSource.prototype.readCoverage = function () {
    var self = this;
    if (!this.graphDir) {
      this.coverageObj = {
        graphs: [],
        probe_coverage: null,
        missing: ["c / cpp (clang)", "go", "rust", "swift"]
      };
      return Promise.resolve(this.coverageObj);
    }
    var wanted = [
      ["graph_go.json", "go"],
      ["graph_cpp.json", "c and cpp (clang)"],
      ["graph_rust.json", "rust"],
      ["graph_swift.json", "swift"]
    ];
    var got = [];
    var missing = [];
    return Promise.all(wanted.map(function (w) {
      return headObjects(self.graphDir, w[0], ["pins", "counts"], 262144)
        .then(function (head) {
          if (!head.counts) {
            missing.push(w[1]);
            return;
          }
          got.push({
            lang: w[1],
            file: w[0],
            counts: head.counts,
            directories: (head.pins || {}).directories || []
          });
        }).catch(function () {
          missing.push(w[1]);
        });
    })).then(function () {
      return readWholeOrNull(self.graphDir, "coverage_go_summary.json");
    }).then(function (cov) {
      if (cov) {
        cov.lang = "go";
      }
      got.sort(function (a, b) {
        return a.lang < b.lang ? -1 : 1;
      });
      self.coverageObj = {
        graphs: got,
        probe_coverage: cov,
        missing: missing.concat(["java", "cpython", "php", "ruby"])
      };
      return self.coverageObj;
    });
  };

  /* --- 2c. phase two: the unit index, in the background --- */

  LiveSource.prototype.indexAll = function (onTick) {
    var self = this;
    var jobs = [];
    LANGS.forEach(function (lang) {
      jobs.push({ dir: self.op, name: "canon39_wrapped_" + lang + ".json" });
    });
    jobs.push({ dir: self.op, name: "canon39_interp.json" });
    (self.regenShards || []).forEach(function (name) {
      jobs.push({ dir: self.regenDir, name: name, store: "canon39_regen_store__" });
    });

    var done = 0;
    var chain = Promise.resolve();
    jobs.forEach(function (job) {
      chain = chain.then(function () {
        return readWhole(job.dir, job.name).catch(function () {
          return null;
        });
      }).then(function (doc) {
        if (doc) {
          self.absorb(doc, job);
        }
        done += 1;
        if (done % 20 === 0 || done === jobs.length) {
          onTick(self.indexRows.length, done, jobs.length);
        }
        /* yield to the browser so the page stays live while this runs */
        return new Promise(function (r) {
          window.setTimeout(r, 0);
        });
      });
    });
    return chain.then(function () {
      return self.indexRows;
    });
  };

  LiveSource.prototype.absorb = function (doc, job) {
    var self = this;
    var storeName = (job.store || "") + job.name;
    var units = DashboardJoin.unitsOf(doc);
    units.forEach(function (u) {
      var uid = u.unit;
      if (!uid) {
        return;
      }
      var lang = u.lang || String(uid).split("/")[0];
      self.shardOf[uid] = { dir: job.dir, name: job.name, store: storeName };
      self.indexRows.push({
        id: uid,
        lang: lang,
        opGroup: self.groupsObj.mint(lang, u.operator),
        label: u.operator,
        sig: null,
        pop: u.population,
        outcome: u.outcome
      });
      DashboardJoin.mnemsOf(u).forEach(function (m) {
        if (!self.opcodeRows[m]) {
          self.opcodeRows[m] = [];
        }
        self.opcodeRows[m].push(uid);
      });
    });
  };

  /* --- 2d. phase three: one unit's body, read on demand --- */

  LiveSource.prototype.storeRecord = function (which, storeName, uid) {
    var self = this;
    var key = which + "/" + storeName;
    if (!this.stores[key]) {
      this.stores[key] = subDir(this.op, which).then(function (d) {
        if (!d) {
          return {};
        }
        return readWhole(d, storeName).catch(function () {
          return {};
        });
      });
    }
    return this.stores[key].then(function (doc) {
      var units = (doc && doc.units) || {};
      return units[uid] || null;
    });
  };

  LiveSource.prototype.manifestFor = function (lang, population) {
    var stem = population === "regenerated"
      ? "probe_manifest2_" : "probe_manifest_";
    var name = stem + lang + ".json";
    if (!this.manifests[name]) {
      this.manifests[name] = readWholeOrNull(this.op, name)
        .then(function (doc) {
          if (!doc) {
            return {};
          }
          var probes = doc.probes || {};
          if (Array.isArray(probes)) {
            var byN = {};
            probes.forEach(function (p) {
              byN[String(p.n)] = p;
            });
            return byN;
          }
          return probes;
        });
    }
    return this.manifests[name];
  };

  LiveSource.prototype.poolIndex = function () {
    var self = this;
    if (this.poolByUnit) {
      return this.poolByUnit;
    }
    this.poolByUnit = readWholeOrNull(this.op, "the_pool5.json")
      .then(function (doc) {
        var by = {};
        if (!doc) {
          return by;
        }
        var entries = doc.entries;
        if (!Array.isArray(entries)) {
          entries = Object.keys(entries).map(function (k) {
            return entries[k];
          });
        }
        entries.forEach(function (e) {
          e.members.forEach(function (m) {
            by[m.unit] = {
              entry: e.entry_id,
              members: e.member_count,
              languages: e.languages,
              rep: e.representative
            };
          });
        });
        return by;
      });
    return this.poolByUnit;
  };

  LiveSource.prototype.unit = function (uid) {
    var self = this;
    var where = this.shardOf[uid];
    if (!where) {
      return Promise.resolve(null);
    }
    return readWhole(where.dir, where.name).then(function (doc) {
      var unit = (doc.units || {})[uid];
      if (!unit) {
        return null;
      }
      unit.unit = uid;
      var lang = unit.lang || String(uid).split("/")[0];
      var population = unit.population || "original";
      return Promise.all([
        self.manifestFor(lang, population).catch(function () {
          return {};
        }),
        self.storeRecord("term65_store", where.store, uid),
        self.storeRecord("render_back_store", where.store, uid),
        self.poolIndex()
      ]).then(function (all) {
        var probes = all[0] || {};
        var termRow = all[1];
        var rendered = all[2];
        var pool = (all[3] || {})[uid] || {};
        var probe = probes[String(unit.n)] || null;
        var term = {};
        if (termRow) {
          term = {
            l5: termRow.layer5_normalized_text,
            outcome: termRow.outcome,
            reason: termRow.reason,
            holes: termRow.holes || []
          };
        }
        var packed = DashboardJoin.packUnit(unit, {
          probe: probe,
          term: term,
          pool: pool,
          rendered: rendered
        }, self.groupsObj);
        /* the signature is only knowable once the manifest is read, so
         * fill it back into the index row the list draws from. */
        for (var i = 0; i < self.indexRows.length; i += 1) {
          if (self.indexRows[i].id === uid) {
            self.indexRows[i].sig = packed.sig;
            break;
          }
        }
        return packed;
      });
    });
  };

  /* --- 2e. the source interface --- */

  LiveSource.prototype.population = function () {
    return this.pop;
  };

  LiveSource.prototype.stats = function () {
    return this.statsObj;
  };

  LiveSource.prototype.coverage = function () {
    return this.coverageObj;
  };

  LiveSource.prototype.index = function () {
    return this.indexRows;
  };

  LiveSource.prototype.opcodeIndex = function () {
    return this.opcodeRows;
  };

  LiveSource.prototype.groups = function () {
    return this.groupsObj;
  };

  /* ---------------------------------------------------------------- *
   * 3.  the gate: ask for the folder, or say plainly why we cannot
   * ---------------------------------------------------------------- */

  function gateHtml(state) {
    if (state === "unsupported") {
      return '<div id="gate">' +
        '<div class="warnbox"><b>This browser cannot read a folder.</b><br>' +
        "The live page needs <span class='mono'>window.showDirectoryPicker</span>, " +
        "the File System Access API. Firefox and Safari do not have it; " +
        "Chrome, Chromium and Edge do.</div>" +
        "<h2>Two ways forward</h2>" +
        "<p>Open this same file in Chrome, Chromium or Edge — nothing else " +
        "changes, it will ask for the folder and read it.</p>" +
        "<p>Or open <span class='mono'>dashboard_snapshot.html</span> beside " +
        "this file. That is the same page with the artifacts already read " +
        "into it: it works in every browser and can be sent to someone who " +
        "does not have the folder, but its numbers are from the moment the " +
        "snapshot was built rather than from now.</p></div>";
    }
    var remembering = opaqueOrigin()
      ? "This file was opened directly, so the browser gives it no storage " +
        "of its own (its origin is “null”) and the folder has to be chosen " +
        "each time. Nothing else is lost."
      : "The folder you choose is remembered, so the next open is one click " +
        "of confirmation.";
    return '<div id="gate"><h2>arch-unit dashboard</h2>' +
      "<p>This page reads the research artifacts itself. There is no server " +
      "and no build step. Choose the <span class='mono'>op_pipeline</span> " +
      "folder — or its super-directory <span class='mono'>Research</span>, " +
      "which lets the compiler-graph pane read " +
      "<span class='mono'>compiler_graph</span> as well.</p>" +
      "<p class='note'>" + remembering + "</p>" +
      '<button class="act" id="pick">choose the folder</button>' +
      '<p class="note" id="gate-note"></p></div>';
  }

  /* the picked handle may be op_pipeline itself, or its super-directory. */
  function resolveDirs(handle) {
    return handle.getFileHandle("canon39_interp.json").then(function () {
      return { op: handle, graph: null, picked: "op_pipeline" };
    }).catch(function () {
      return handle.getDirectoryHandle("op_pipeline").then(function (op) {
        return handle.getDirectoryHandle("compiler_graph").then(function (g) {
          return { op: op, graph: g, picked: "Research" };
        }).catch(function () {
          return { op: op, graph: null, picked: "Research" };
        });
      });
    });
  }

  function boot(root) {
    var t0 = window.performance.now();
    root = root || document.body;
    var style = document.createElement("style");
    style.textContent = DashboardJoin.STYLE;
    document.head.appendChild(style);

    if (!supported()) {
      root.innerHTML = gateHtml("unsupported");
      console.log("[dashboard] window.showDirectoryPicker is absent; " +
        "this browser cannot open the live page.");
      return Promise.resolve(null);
    }

    root.innerHTML = gateHtml("ask");

    function start(handle) {
      var tStart = window.performance.now();
      return resolveDirs(handle).then(function (dirs) {
        if (!dirs.graph) {
          console.log("[dashboard] compiler_graph was not reachable from the " +
            "picked folder; the coverage pane will say so.");
        }
        var source = new LiveSource(dirs);
        return source.readSummaries().then(function () {
          return source.readCoverage();
        }).then(function () {
          return DashboardJoin.mount(source, root);
        }).then(function (api) {
          var paint = window.performance.now();
          console.log("[dashboard] FIRST PAINT " +
            (paint - tStart).toFixed(0) + " ms after the folder was granted; " +
            (paint - t0).toFixed(0) + " ms after the page opened. " +
            source.pop.units.toLocaleString() + " units counted from " +
            source.pop.files + " summary reads.");
          /* phase two, in the background */
          source.indexAll(function (units, done, total) {
            source.pop.note = "unit index " + done + " of " + total +
              " files read";
            if (done === total) {
              source.pop.note = "every unit body indexed";
            }
            api.paintPopulation(source.pop);
            api.repaintIndexPanes();
          }).then(function (rows) {
            var end = window.performance.now();
            console.log("[dashboard] INDEX COMPLETE " +
              (end - tStart).toFixed(0) + " ms after the folder was granted; " +
              rows.length.toLocaleString() + " units, " +
              Object.keys(source.opcodeRows).length + " arch opcodes.");
            /* Explicit final repaint (task 82, log_182 coordinator note --
             * the header's own arch-opcode count read 122 in one capture
             * and 162 in another, because dashboard_join.js's header reads
             * the LIVE state.opcodeIndex at render time, and that count
             * only reaches its final value once every job above has run.
             * paintHeader() already re-reads a live-mutated object (the
             * SAME object indexAll() fills in, source.opcodeRows, aliased
             * into state.opcodeIndex when mount() first read it), so the
             * on-tick repaint above already carries every count that lands
             * before it fires; this call is the one made explicitly ONCE
             * MORE, after `rows` proves indexAll's own promise has fully
             * resolved, so a repaint is guaranteed to happen with the
             * complete count even if the last on-tick call and the final
             * absorbed job were ever to race. */
            source.pop.note = "every unit body indexed";
            api.paintPopulation(source.pop);
            api.repaintIndexPanes();
          });
          return api;
        });
      });
    }

    var note = document.getElementById("gate-note");
    var btn = document.getElementById("pick");

    /* the button is wired FIRST and unconditionally: asking the browser
     * for a remembered handle must never be able to leave the page dead. */
    btn.onclick = function () {
      window.showDirectoryPicker({ mode: "read" }).then(function (h) {
        return dbPut("root", h).then(function () {
          return start(h);
        });
      }).catch(function (err) {
        if (note) {
          note.textContent = "no folder chosen: " +
            (err && err.message ? err.message : err);
        }
        console.log("[dashboard] showDirectoryPicker: " + err);
      });
    };

    return dbGet("root").then(reconfirm).then(function (handle) {
      if (!handle) {
        return null;
      }
      if (note) {
        note.textContent = "using the folder you chose last time.";
      }
      return start(handle);
    }).catch(function () {
      return null;
    });
  }

  return {
    boot: boot,
    supported: supported,
    LiveSource: LiveSource,
    carveObject: carveObject
  };
}());
