#!/usr/bin/env python3
"""viewer_build.py -- the SNAPSHOT builder for the dashboard.

Node: hq.research.compiler_graph.dashboard (CORE_0_3_5_10_dashboard.md),
the `loader` method's stated fallback: "the embedded-data build
(viewer_build.py) for a shareable snapshot".

WHAT CHANGED IN TASK 68.  This file used to be the ONLY way to get a
page: it read the artifacts in python, wrote its own copy of the join in
python, and produced dashboard.html.  It is no longer the only way and it
no longer holds a join of its own.

  - `dashboard.html` is now the LIVE page.  It reads the artifact folder
    itself in the browser, so the owner's ruling holds: no server, no terminal,
    double-click, and every number is a count over a file on disk at the
    moment the page is opened.
  - THE JOIN IS WRITTEN ONCE, IN JAVASCRIPT: `dashboard_join.js`.  The
    live page loads it with a script tag; THIS PROGRAM EMBEDS THE SAME
    FILE VERBATIM.  Nothing here re-implements it.  What python still
    does is READ the artifacts -- the same reads the live loader makes in
    the browser -- and hand the result to that one join.
  - The output is `dashboard_snapshot.html`, not `dashboard.html`: one
    file with the data inside it, for sending to someone who does not
    have the folder, and for browsers without the File System Access API.

    /tmp/reconnect_venv/bin/python3 \
        ~/Programming/PseudoCoupHQ/Research/op_pipeline/viewer_build.py

POPULATIONS, stated on the page rather than implied here:
  - the stats pane counts EVERY unit of the current artifacts.
  - the unit viewer and the arch opcode index carry a SAMPLE: every
    original and interpreter unit, plus a stride sample of the
    regenerated ones, so the file stays openable.  The live page carries
    no sample -- it reads the whole population.

THE GUARD.  The data this program emits is written beside the page as
`dashboard_snapshot_data.json` and walked by the UNMODIFIED
`check_no_spelling_keys.py`.  This program REFUSES ITS OWN OUTPUT when
the guard fails.
"""

import datetime
import glob
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "dashboard_snapshot.html")
DATA_OUT = os.path.join(HERE, "dashboard_snapshot_data.json")
JOIN = os.path.join(HERE, "dashboard_join.js")
TEMPLATE = os.path.join(HERE, "viewer_template.html")
PANE6 = os.path.join(HERE, "dashboard_pane6.js")
PANE23 = os.path.join(HERE, "dashboard_pane23.js")
PANE1 = os.path.join(HERE, "dashboard_pane1.js")
PANE4 = os.path.join(HERE, "dashboard_pane4.js")
PANE5 = os.path.join(HERE, "dashboard_pane5.js")
CHRONOLOGY = os.path.join(HERE, "chronology.json")
GUARD = os.path.join(HERE, "check_no_spelling_keys.py")

LANGS = ["c", "cpp", "go", "rust", "swift"]
REGEN_STRIDE = 44          # ~650 of 28,660

FILES_READ = []


def load(path):
    full = os.path.join(HERE, path)
    FILES_READ.append(full)
    with open(full) as fh:
        return json.load(fh)


def units_of(doc):
    """the python twin of DashboardJoin.unitsOf, kept because python has
    to READ the artifacts before the one join can be given them."""
    u = doc.get("units", doc)
    if isinstance(u, dict):
        out = []
        for key, row in u.items():
            if isinstance(row, dict) and not row.get("unit"):
                row["unit"] = key
            out.append(row)
        return out
    return u


# ------------------------------------------------------------------
# THE OPERATOR GROUP KEY -- the python twin of
# DashboardJoin.OperatorGroups.  A machine id minted per language in
# first-appearance order; the token rides beside it as a display label
# and is read by nothing that groups, selects or compares.
# ------------------------------------------------------------------

class OperatorGroups(object):

    def __init__(self):
        self.by_lang = {}
        self.labels = {}

    def mint(self, lang, token):
        if not token:
            return None
        seen = self.by_lang.setdefault(lang, {})
        if token not in seen:
            gid = "%s#g%02d" % (lang, len(seen))
            seen[token] = gid
            self.labels[gid] = token
        return seen[token]


# ------------------------------------------------------------------
# 1. the corpus: every canon39 record counted, a sample carried in full
# ------------------------------------------------------------------

def read_corpus():
    per_lang = {}
    sample = []
    for lang in LANGS:
        doc = load("canon39_wrapped_%s.json" % lang)
        us = units_of(doc)
        proved = 0
        for x in us:
            if x.get("outcome") == "WRAPPED_TEXT_PROVED":
                proved += 1
        per_lang[lang] = {"units": len(us), "proved": proved}
        for x in us:
            x["_store"] = "canon39_wrapped_%s.json" % lang
        sample.extend(us)

    interp = units_of(load("canon39_interp.json"))
    for x in interp:
        x["_store"] = "canon39_interp.json"
        lang = x.get("lang") or x["unit"].split("/")[0]
        row = per_lang.setdefault(lang, {"units": 0, "proved": 0})
        row["units"] += 1
        if x.get("outcome") == "WRAPPED_TEXT_PROVED":
            row["proved"] += 1
    sample.extend(interp)

    n = 0
    shards = sorted(glob.glob(os.path.join(HERE, "canon39_regen_store/*.json")))
    for path in shards:
        FILES_READ.append(path)
        store = "canon39_regen_store__" + os.path.basename(path)
        with open(path) as fh:
            doc = json.load(fh)
        for x in units_of(doc):
            lang = x.get("lang") or x["unit"].split("/")[0]
            row = per_lang.setdefault(lang, {"units": 0, "proved": 0})
            row["units"] += 1
            if x.get("outcome") == "WRAPPED_TEXT_PROVED":
                row["proved"] += 1
            if n % REGEN_STRIDE == 0:
                x["_store"] = store
                sample.append(x)
            n += 1
    return per_lang, sample


# ------------------------------------------------------------------
# 2. the joins python must resolve: probe source, term, pool, rendered
# ------------------------------------------------------------------

def read_manifests():
    """two families, keyed the same way:
       probe_manifest_<lang>   -- the original corpus
       probe_manifest2_<lang>  -- the regenerated corpus
    """
    out = {"original": {}, "regenerated": {}}
    for path in glob.glob(os.path.join(HERE, "probe_manifest*.json")):
        name = os.path.basename(path)
        if "_asg_" in name:
            continue
        if name.startswith("probe_manifest2_"):
            pop = "regenerated"
            lang = name[len("probe_manifest2_"):-len(".json")]
        else:
            pop = "original"
            lang = name[len("probe_manifest_"):-len(".json")]
        try:
            with open(path) as fh:
                probes = json.load(fh).get("probes", {})
        except Exception:
            continue
        FILES_READ.append(path)
        if isinstance(probes, list):
            probes = {str(p.get("n")): p for p in probes}
        out[pop][lang] = probes
    return out


def read_store(folder):
    """term65_store / render_back_store, both keyed by unit id."""
    out = {}
    for path in sorted(glob.glob(os.path.join(HERE, folder, "*.json"))):
        FILES_READ.append(path)
        with open(path) as fh:
            doc = json.load(fh)
        for x in units_of(doc):
            uid = x.get("unit")
            if uid:
                out[uid] = x
    return out


def read_pool(doc=None):
    """the pool's summary and its per-unit rows.

    `doc` was added 2026-09-04 (task 85) so that ONE implementation of
    this rule can be given a pool document that did not come from the
    working tree -- the chronology's outer controller hands it the pool
    as git held it at a past commit.  With no argument the behaviour is
    exactly what it was: the pool beside this file.
    """
    if doc is None:
        doc = load("the_pool5.json")
    entries = doc["entries"]
    if not isinstance(entries, list):
        entries = list(entries.values())
    by_unit = {}
    for e in entries:
        for m in e["members"]:
            by_unit[m["unit"]] = {
                "entry": e["entry_id"],
                "members": e["member_count"],
                "languages": e["languages"],
                "rep": e["representative"],
            }
    return doc["summary"], by_unit


# ------------------------------------------------------------------
# 3. one unit -> the record the ONE JOIN's panes read.  The field names
#    below are the contract stated at the top of dashboard_join.js
#    (packUnit); the transformations themselves -- gloss, mnems,
#    signature -- are done there, in the browser, so there is one
#    implementation of each and not two.  What is done HERE is only what
#    a snapshot needs done ahead of time: the raw records are handed
#    over already read.
# ------------------------------------------------------------------

UNIT_FIELDS_THE_JOIN_READS = [
    "unit", "lang", "n", "operator", "population", "outcome",
    "arrival_annotation", "body_as_read", "wrapped_text", "ledger",
]


def trim_unit(unit):
    """carry only the fields DashboardJoin.packUnit and mnemsOf read.
    A snapshot is meant to be sendable; the live page reads the whole
    record off disk and needs no trim."""
    out = {}
    for key in UNIT_FIELDS_THE_JOIN_READS:
        if key in unit:
            out[key] = unit[key]
    return out


def trim_rendered(row):
    """only the two fields the rendered-back mode shows."""
    if not row:
        return None
    return {
        "layer3_wrapped_text": row.get("layer3_wrapped_text"),
        "character_identical_to_layer_3":
            row.get("character_identical_to_layer_3"),
    }


def pack_for_join(unit, manifests, terms, rendered, pool_by_unit):
    uid = unit["unit"]
    lang = unit.get("lang") or uid.split("/")[0]
    pop = unit.get("population") or "original"
    family = manifests.get(pop) or manifests.get("original") or {}
    probe = (family.get(lang) or {}).get(str(unit.get("n")))
    if probe:
        # only what the one join reads: the declared types and the probe's
        # own source text.  The manifest's `operator` field is NOT carried
        # into the page's data -- the display label the page shows comes
        # from the unit record, once, and nothing else needs the token.
        probe = {
            "n": probe.get("n"),
            "lhs_type": probe.get("lhs_type"),
            "rhs_type": probe.get("rhs_type"),
            "result_type": probe.get("result_type"),
            "source": probe.get("source"),
        }
    term_row = terms.get(uid) or {}
    term = {}
    if term_row:
        term = {
            "l5": term_row.get("layer5_normalized_text"),
            "outcome": term_row.get("outcome"),
            "reason": term_row.get("reason"),
            "holes": term_row.get("holes") or [],
        }
    return {
        "unit": trim_unit(unit),
        "probe": probe,
        "term": term,
        "rendered": trim_rendered(rendered.get(uid)),
        "pool": pool_by_unit.get(uid) or {},
    }


# ------------------------------------------------------------------
# 4. the stats pane
# ------------------------------------------------------------------

def census_name(p):
    """the python twin of DashboardJoin.censusName."""
    if isinstance(p, dict):
        m = p.get("mnem")
        if isinstance(m, list):
            return " + ".join(m)
        return m or p.get("phrase") or p.get("callee") or "unnamed"
    if isinstance(p, list):
        return " + ".join(p)
    return p


def read_stats(per_lang, pool_summary):
    stats = {"per_lang": per_lang, "pool": pool_summary}
    try:
        fam = load("the_families5.json")
        f = fam.get("families", fam)
        stats["families"] = len(f)
    except Exception:
        stats["families"] = None
    try:
        cen = load("name_census5.json")
        rows = []
        for e in cen["entries"][:12]:
            rows.append({
                "producer": census_name(e.get("producer")),
                "rows": e.get("rows_blocked", e.get("rows")),
                "units": e.get("units_blocked", e.get("units")),
            })
        stats["census"] = {"producers": len(cen["entries"]), "rows": rows}
    except Exception as exc:
        stats["census"] = {"producers": None, "rows": [], "error": str(exc)}
    try:
        stats["terms"] = load("audit65.json")
    except Exception:
        stats["terms"] = None
    return stats


# ------------------------------------------------------------------
# 5. the coverage pane -- the same head-of-file read the live loader
#    makes in the browser, done here with a file seek instead.
# ------------------------------------------------------------------

def carve(text, key):
    """the python twin of DashboardLoader.carveObject."""
    needle = '"%s"' % key
    at = text.find(needle)
    if at == -1:
        return None
    i = text.find(":", at + len(needle))
    if i == -1:
        return None
    i += 1
    while i < len(text) and text[i].isspace():
        i += 1
    if i >= len(text):
        return None
    opener = text[i]
    if opener not in "{[":
        return None
    closer = "}" if opener == "{" else "]"
    depth = 0
    in_str = False
    escaped = False
    j = i
    while j < len(text):
        ch = text[j]
        if in_str:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                in_str = False
        elif ch == '"':
            in_str = True
        elif ch == opener:
            depth += 1
        elif ch == closer:
            depth -= 1
            if depth == 0:
                try:
                    return json.loads(text[i:j + 1])
                except Exception:
                    return None
        j += 1
    return None


def read_coverage():
    # THE GRAPHS MOVED, 2026-09-04.  The four compiler graphs live in the
    # companion folder `PseudoCoupGraphs` (see
    # Research/compiler_graph/graphs_home.py), which has no remote by
    # design; the small summaries and the coverage summary stay here and
    # stay tracked.  The head read below is unchanged: `pins` and
    # `counts` still sit inside the first 256 KB of a graph, in the
    # compact form as in the old one.
    cg = os.path.join(os.path.dirname(HERE), "compiler_graph")
    graph_code = cg
    if graph_code not in sys.path:
        sys.path.insert(0, graph_code)
    try:
        import graphs_home
        graph_folder = graphs_home.home()
    except ImportError:
        graph_folder = cg
    wanted = [
        ("graph_go.json", "go"),
        ("graph_cpp.json", "c and cpp (clang)"),
        ("graph_rust.json", "rust"),
        ("graph_swift.json", "swift"),
    ]
    graphs = []
    missing = []
    for name, lang in wanted:
        path = os.path.join(graph_folder, name)
        if not os.path.exists(path):
            path = os.path.join(cg, name)
        if not os.path.exists(path):
            missing.append(lang)
            continue
        with open(path) as fh:
            head = fh.read(262144)
        counts = carve(head, "counts")
        pins = carve(head, "pins") or {}
        if not counts:
            missing.append(lang)
            continue
        FILES_READ.append(path)
        graphs.append({
            "lang": lang,
            "file": name,
            "counts": counts,
            "directories": pins.get("directories") or [],
        })
    cov = None
    summary = os.path.join(cg, "coverage_go_summary.json")
    if os.path.exists(summary):
        FILES_READ.append(summary)
        with open(summary) as fh:
            cov = json.load(fh)
        cov["lang"] = "go"
    graphs.sort(key=lambda g: g["lang"])
    return {
        "graphs": graphs,
        "probe_coverage": cov,
        "missing": missing + ["java", "cpython", "php", "ruby"],
    }


# ------------------------------------------------------------------
# 6. the build
# ------------------------------------------------------------------

def run_guard(path):
    """the UNMODIFIED guard, over the json this program emits.  A
    failure refuses the build."""
    proc = subprocess.run(
        [sys.executable, GUARD, path],
        capture_output=True,
        text=True,
    )
    sys.stdout.write(proc.stdout)
    sys.stderr.write(proc.stderr)
    return proc.returncode


def main():
    per_lang, sample = read_corpus()
    manifests = read_manifests()
    terms = read_store("term65_store")
    rendered = read_store("render_back_store")
    pool_summary, pool_by_unit = read_pool()

    groups = OperatorGroups()
    raw = []
    for u in sample:
        raw.append(pack_for_join(u, manifests, terms, rendered, pool_by_unit))
    raw.sort(key=lambda r: (r["unit"].get("lang") or
                            r["unit"]["unit"].split("/")[0],
                            r["unit"]["unit"]))

    index = []
    for r in raw:
        unit = r["unit"]
        uid = unit["unit"]
        lang = unit.get("lang") or uid.split("/")[0]
        index.append({
            "id": uid,
            "lang": lang,
            "opGroup": groups.mint(lang, unit.get("operator")),
            "label": unit.get("operator"),
            "sig": None,
            "pop": unit.get("population"),
            "outcome": unit.get("outcome"),
        })

    data = {
        "raw": raw,
        "index": index,
        "stats": read_stats(per_lang, pool_summary),
        "coverage": read_coverage(),
        "meta": {
            "built_at": datetime.datetime.now().isoformat(timespec="seconds"),
            "units_counted": sum(v["units"] for v in per_lang.values()),
            "units_carried": len(raw),
            "files_read": len(set(FILES_READ)),
            "regen_stride": REGEN_STRIDE,
        },
    }

    with open(DATA_OUT, "w") as fh:
        json.dump(data, fh, indent=1, sort_keys=True)
    rc = run_guard(DATA_OUT)
    if rc != 0:
        print("REFUSED: the spelling-key guard failed on %s; no page was "
              "written." % DATA_OUT)
        return rc

    with open(JOIN) as fh:
        join_js = fh.read()
    with open(TEMPLATE) as fh:
        tpl = fh.read()
    blob = json.dumps(data, separators=(",", ":")).replace("</", "<\\/")
    html = tpl.replace("/*JOIN*/", join_js)
    html = html.replace("/*DATA*/", blob)

    # --- panes 2 and 3 (task 70), embedded VERBATIM.  Unlike pane 6 this
    # module has to be parsed BEFORE the snapshot's own script, because it
    # wraps DashboardJoin.mount and the snapshot calls mount at parse time.
    # So it is inserted at the one seam between the join script and the
    # data script.  The /*JOIN*/ substitution above is untouched, so the
    # byte-for-byte join proof of log_176 section 2.2 still holds.
    pane23_js = ""
    if os.path.exists(PANE23):
        with open(PANE23) as fh:
            pane23_js = fh.read()
    if pane23_js:
        seam = "<script>\nvar SNAPSHOT"
        if seam not in html:
            print("REFUSED: dashboard_pane23.js could not be placed before "
                  "the snapshot's own script; the seam %r is not in the "
                  "built page. No page was written." % seam)
            return 1
        html = html.replace(
            seam, "<script>" + pane23_js + "</script>\n" + seam, 1)

    # --- pane 1's own modes (task 69), embedded VERBATIM, at the same
    # seam and for the same reason as panes 2 and 3: the module has to be
    # parsed before the snapshot calls mount.  Purely additive.
    pane1_js = ""
    if os.path.exists(PANE1):
        with open(PANE1) as fh:
            pane1_js = fh.read()
    if pane1_js:
        seam1 = "<script>\nvar SNAPSHOT"
        if seam1 not in html:
            print("REFUSED: dashboard_pane1.js could not be placed before "
                  "the snapshot's own script; the seam %r is not in the "
                  "built page. No page was written." % seam1)
            return 1
        html = html.replace(
            seam1, "<script>" + pane1_js + "</script>\n" + seam1, 1)

    # --- pane 4 (task 73), embedded VERBATIM at the same seam and for the
    # same reason as panes 1, 2 and 3: it wraps DashboardJoin.mount and the
    # snapshot calls mount at parse time.  The compiler-graph summaries ride
    # with it, because a snapshot has no folder to read them from -- the
    # FILE-LEVEL summaries only (456 KB for four compilers, plus 2.6 MB of
    # go coverage).  Neither graph_<lang>.json (608 MB for four) nor
    # coverage_go2.json (515 MB) nor the per-definition artifacts are
    # carried, so in the snapshot the pane draws the file level and says
    # that expanding a file and reading a probe's full path need the live
    # page.  Purely additive: nothing above changes.
    pane4_js = ""
    if os.path.exists(PANE4):
        with open(PANE4) as fh:
            pane4_js = fh.read()
    if pane4_js:
        seam4 = "<script>\nvar SNAPSHOT"
        if seam4 not in html:
            print("REFUSED: dashboard_pane4.js could not be placed before "
                  "the snapshot's own script; the seam %r is not in the "
                  "built page. No page was written." % seam4)
            return 1
        graphs = {}
        cg = os.path.join(HERE, "..", "compiler_graph")
        for key in ("go", "cpp", "rust", "swift"):
            path = os.path.join(cg, "graph_%s_files.json" % key)
            if os.path.exists(path):
                with open(path) as fh:
                    graphs[key] = json.load(fh)
        cover = None
        cpath = os.path.join(cg, "coverage_go_files.json")
        if os.path.exists(cpath):
            with open(cpath) as fh:
                cover = json.load(fh)
        pane4_data = json.dumps({"graphs": graphs, "coverage": cover},
                                separators=(",", ":")).replace("</", "<\\/")
        html = html.replace(
            seam4,
            "<script>window.__PANE4__ = " + pane4_data + ";</script>\n" +
            "<script>" + pane4_js + "</script>\n" + seam4, 1)
        print("pane 4: %d file-level graph summaries and %s go coverage "
              "embedded (%d bytes)"
              % (len(graphs), "1" if cover else "0", len(pane4_data)))

    # --- pane 6, added the same way the live page adds it: the module is
    # embedded VERBATIM beside the join, and chronology.json (written by
    # chronology_build.py) rides with it, because a snapshot has no folder
    # to read it from.  Purely additive: nothing above changes, and the
    # template is untouched -- the block is appended before </body>. ---
    pane6_js = ""
    chron = "null"
    if os.path.exists(PANE6):
        with open(PANE6) as fh:
            pane6_js = fh.read()
    if os.path.exists(CHRONOLOGY):
        with open(CHRONOLOGY) as fh:
            chron = fh.read().replace("</", "<\\/")
    if pane6_js:
        block = ("<script>window.__CHRONOLOGY__ = " + chron + ";</script>\n"
                 "<script>" + pane6_js + "</script>\n"
                 "<script>DashboardChronology.attach(document.body, null);"
                 "</script>\n")
        html = html.replace("</body>", block + "</body>")

    # --- pane 5 (task 74), embedded VERBATIM before </body>, the same way
    # pane 6 is: it wraps DashboardJoin.mount, and the three small artifacts
    # it reads (audit65.json, the_pool5.json, and the HIGHEST-numbered
    # name_census*.json present -- never a hard-coded generation) ride with
    # it as window.__PANE5__, because a snapshot has no folder to read them
    # from. Purely additive: nothing above changes. ---
    pane5_js = ""
    if os.path.exists(PANE5):
        with open(PANE5) as fh:
            pane5_js = fh.read()
    pane5_data = "null"
    if pane5_js:
        audit65_path = os.path.join(HERE, "audit65.json")
        pool5_path = os.path.join(HERE, "the_pool5.json")
        census_candidates = glob.glob(os.path.join(HERE, "name_census*.json"))

        def census_gen(path):
            base = os.path.basename(path)
            digits = "".join(ch for ch in base if ch.isdigit())
            return int(digits) if digits else 1

        census_path = None
        if census_candidates:
            census_path = max(census_candidates, key=census_gen)
        audit65_doc = None
        pool5_doc = None
        census_doc = None
        if os.path.exists(audit65_path):
            with open(audit65_path) as fh:
                audit65_doc = json.load(fh)
        if os.path.exists(pool5_path):
            with open(pool5_path) as fh:
                pool5_doc = json.load(fh)
        if census_path:
            with open(census_path) as fh:
                census_doc = json.load(fh)
        if audit65_doc and pool5_doc and census_doc:
            pane5_data = json.dumps({
                "audit65": audit65_doc,
                "pool5": pool5_doc,
                "census": census_doc,
                "census_name": os.path.basename(census_path)
            }, separators=(",", ":")).replace("</", "<\\/")
    if pane5_js and pane5_data != "null":
        block5 = ("<script>window.__PANE5__ = " + pane5_data + ";</script>\n"
                  "<script>" + pane5_js + "</script>\n"
                  "<script>DashboardStats.attach(document.body, null);"
                  "</script>\n")
        html = html.replace("</body>", block5 + "</body>")

    with open(OUT, "w") as fh:
        fh.write(html)
    print("wrote %s  (%.1f MB, %d unit bodies carried, %d units counted, "
          "%d files read)"
          % (OUT, os.path.getsize(OUT) / 1e6, len(raw),
             data["meta"]["units_counted"], data["meta"]["files_read"]))
    print("the join embedded above is dashboard_join.js, verbatim (%d bytes)"
          % len(join_js))
    if pane23_js:
        print("panes 2 and 3 embedded verbatim from dashboard_pane23.js "
              "(%d bytes), before the snapshot script" % len(pane23_js))
    else:
        print("panes 2 and 3 NOT embedded: dashboard_pane23.js is not beside "
              "this program")
    if pane1_js:
        print("pane 1's modes embedded verbatim from dashboard_pane1.js "
              "(%d bytes), before the snapshot script" % len(pane1_js))
    else:
        print("pane 1's modes NOT embedded: dashboard_pane1.js is not beside "
              "this program")
    if pane6_js:
        print("pane 6 embedded verbatim from dashboard_pane6.js (%d bytes) "
              "with chronology.json (%d bytes)" % (len(pane6_js), len(chron)))
    else:
        print("pane 6 NOT embedded: dashboard_pane6.js is not beside this "
              "program")
    if pane5_js and pane5_data != "null":
        print("pane 5 embedded verbatim from dashboard_pane5.js (%d bytes) "
              "with audit65.json + the_pool5.json + %s (%d bytes)"
              % (len(pane5_js), os.path.basename(census_path),
                 len(pane5_data)))
    else:
        print("pane 5 NOT embedded: dashboard_pane5.js and/or "
              "audit65.json/the_pool5.json/name_census*.json are not beside "
              "this program")
    return 0


if __name__ == "__main__":
    sys.exit(main())
