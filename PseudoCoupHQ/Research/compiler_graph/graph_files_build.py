#!/usr/bin/env python3
"""graph_files_build.py -- the FILE-LEVEL SUMMARY INDEX of a compiler graph.

Node: hq.research.compiler_graph.graph (`static_structure`), read by
hq.research.compiler_graph.dashboard (`coverage_view`, pane 4).

WHY THIS FILE EXISTS.  `graph_cpp.json` is 331,704,231 bytes and
`graph_swift.json` is 165,106,660.  The dashboard is a page opened by
double-click; it may never hold a whole graph in memory, and neither may
this builder.  So the builder streams each graph ONE RECORD AT A TIME and
writes two small artifacts per compiler:

  graph_<lang>_files.json   the boxes: one row per source file with its
                            node counts by kind and its frontier count,
                            plus the inter-file edge counts by relation.
                            This is what the page draws by default.
  graph_<lang>_defs.json    the nodes inside the boxes: per file, the
                            definitions with their labels and line spans,
                            and the definition-to-definition edges.  The
                            page reads this only when a file is expanded.

BOUNDED MEMORY, STATED.  Peak resident set is measured with
`resource.getrusage(RUSAGE_SELF).ru_maxrss` and printed at the end of every
run.  The builder ABORTS BY NAME (`MemoryCeilingReached`) above the ceiling
rather than being stopped by the operating system, per the graph CORE's
settled rule ("a stop by the operating system is not a measurement; a
refusal by name is").

HOW IT AVOIDS A NODE TABLE.  Task 71's id scheme is
`file#line#kind#ordinal` (log_174), so the file of a node and the kind of a
node are read off the id itself.  A file node's id is the path with no `#`.
No node dictionary is built, so memory is the size of the aggregates, not
of the graph.

THE SPELLING BAN.  Every key written here is a machine identifier -- a
source path, a node id, or a relation name of the graph's own edge
vocabulary (contains / calls / reads / writes).  No operator token appears
in any key, grouping or pairing.  The emitted json is walked by the
unmodified check_no_spelling_keys.py.

    /tmp/reconnect_venv/bin/python3 graph_files_build.py go
    /tmp/reconnect_venv/bin/python3 graph_files_build.py go cpp rust swift
"""

import importlib.util
import json
import os
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

MEMORY_CEILING_MB = 6144


class MemoryCeilingReached(Exception):
    """Raised by name when the run passes the stated ceiling."""


def peak_mb():
    return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0


def check_ceiling(where):
    mb = peak_mb()
    if mb > MEMORY_CEILING_MB:
        raise MemoryCeilingReached(
            "%s: peak resident %.0f MB is above the stated ceiling of %d MB"
            % (where, mb, MEMORY_CEILING_MB))
    return mb


def file_of(node_id):
    """The source file a node id belongs to, read off the id."""
    cut = node_id.find("#")
    return node_id if cut == -1 else node_id[:cut]


def kind_of(node_id):
    """The kind of a node, read off the id: file#line#kind#ordinal."""
    parts = node_id.split("#")
    return "file" if len(parts) < 3 else parts[2]


#: THE GRAPHS MOVED, 2026-09-04.  They live in the companion folder
#: `PseudoCoupGraphs` (see graphs_home.py), not in this repository, and
#: they are stored in the COMPACT form (graph_compact.py) rather than the
#: old expanded one.  `graph_path` answers where one is and `stream_any`
#: reads EITHER form, so every reader below this line is unchanged.


def graph_path(lang):
    """the graph of one compiler, wherever it lives.

    The companion folder first, because that is where the graphs are; a
    file still sitting beside this program second, so a graph that has
    not been moved is still found.
    """
    import graphs_home
    moved = graphs_home.path("graph_%s.json" % lang)
    if os.path.exists(moved):
        return moved
    return os.path.join(HERE, "graph_%s.json" % lang)


def stream_any(path):
    """(section, record) for a graph in EITHER form -- the old expanded
    one, or the compact one.

    The import of `graph_compact` is inside this function because that
    module imports THIS one for its own streaming reader, and a top-level
    import here would close the circle.
    """
    import graph_compact
    if graph_compact.is_compact(path):
        for section in graph_compact.RECORD_SECTIONS:
            for record in graph_compact.stream_records(path, section):
                yield section, record
        return
    for one in stream(path):
        yield one


def stream(path):
    """Yield (section, record) for every element of the graph's top-level
    arrays, one record at a time.  The graph files are written with
    json.dump(indent=1), so a top-level array element opens on a line of
    exactly two spaces and a brace and closes the same way."""
    section = None
    buf = None
    with open(path, "r") as fh:
        for line in fh:
            if line.startswith(' "'):
                section = line[2:line.index('"', 2)]
                buf = None
                continue
            if section not in ("nodes", "edges", "frontier"):
                continue
            if buf is None:
                if line.startswith("  {"):
                    buf = [line]
                continue
            buf.append(line)
            if line.startswith("  }"):
                text = "".join(buf).rstrip().rstrip(",")
                buf = None
                yield section, json.loads(text)


def head_objects(path, keys, limit=1 << 20):
    """The prefix slice, in python: the same trick the page's loader uses.
    `pins` and `counts` end within the first few kilobytes of every graph."""
    with open(path, "r") as fh:
        text = fh.read(limit)
    out = {}
    for key in keys:
        needle = '"%s"' % key
        at = text.find(needle)
        if at == -1:
            out[key] = None
            continue
        i = text.index(":", at + len(needle)) + 1
        while text[i].isspace():
            i += 1
        opener = text[i]
        closer = {"{": "}", "[": "]"}[opener]
        depth = 0
        j = i
        in_str = False
        esc = False
        while j < len(text):
            ch = text[j]
            if in_str:
                if esc:
                    esc = False
                elif ch == "\\":
                    esc = True
                elif ch == '"':
                    in_str = False
            elif ch == '"':
                in_str = True
            elif ch == opener:
                depth += 1
            elif ch == closer:
                depth -= 1
                if depth == 0:
                    out[key] = json.loads(text[i:j + 1])
                    break
            j += 1
        else:
            out[key] = None
    return out


def refuse_on_spelling(paths, report=print):
    """THE MECHANICAL GUARD.  The spelling ban requires every stage that
    groups or pairs units to run check_no_spelling_keys.py over its own
    output and REFUSE that output on failure.  The guard is imported
    unmodified from op_pipeline and run in this one process."""
    guard_path = os.path.join(HERE, "..", "op_pipeline",
                              "check_no_spelling_keys.py")
    guard_path = os.path.abspath(guard_path)
    spec = importlib.util.spec_from_file_location("spelling_guard",
                                                  guard_path)
    guard = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(guard)
    toks = guard.inventory()
    bad = []
    for path in paths:
        findings = guard.check(path, toks) if hasattr(guard, "check") else None
        if findings is None:
            with open(path) as fh:
                doc = json.load(fh)
            findings = []
            guard.walk(doc, toks, "$", findings)
        if findings:
            bad.append((path, findings))
            report("REFUSED %s -- %d spelling-keyed place(s)"
                   % (os.path.basename(path), len(findings)))
            for f in findings[:5]:
                report("    %s" % (f,))
        elif not hasattr(guard, "check"):
            report("PASS %s -- no operator token in any key, grouping, "
                   "pairing or row structure" % os.path.basename(path))
    if bad:
        for path, _f in bad:
            os.remove(path)
        raise SystemExit("the spelling guard refused this stage's own "
                         "output; the files above were removed")


def build(lang, report=print):
    src = graph_path(lang)
    if not os.path.exists(src):
        report("REFUSED: %s is not on disk" % src)
        return None
    t0 = time.time()
    head = head_objects(src, ["pins", "counts"])

    per_file = {}          # path -> {kind: n}
    frontier_by_file = {}  # path -> n
    frontier_kinds = {}    # path -> {kind: n}
    defs_by_file = {}      # path -> [[id, label, start, end]]
    def_index = {}         # def id -> integer
    def_edges = []         # [i, j, relation]
    file_edges = {}        # (src path, dst path, relation) -> n
    seen = 0

    def bump(path, kind):
        row = per_file.get(path)
        if row is None:
            row = {}
            per_file[path] = row
        row[kind] = row.get(kind, 0) + 1

    for section, rec in stream_any(src):
        seen += 1
        if seen % 250000 == 0:
            mb = check_ceiling("%s after %d records" % (lang, seen))
            report("   ... %s %s %s records, peak %.0f MB"
                   % (lang, "{:,}".format(seen), section, mb))
        if section == "nodes":
            nid = rec["id"]
            path = rec.get("file") or file_of(nid)
            kind = rec.get("kind") or kind_of(nid)
            bump(path, kind)
            if kind == "def":
                def_index[nid] = len(def_index)
                defs_by_file.setdefault(path, []).append({
                    "id": nid,
                    "language": rec.get("language"),
                    "label": rec.get("label"),
                    "start_line": rec.get("start_line"),
                    "end_line": rec.get("end_line"),
                })
        elif section == "edges":
            a = rec["src"]
            b = rec["dst"]
            rel = rec["rel"]
            fa = file_of(a)
            fb = file_of(b)
            if fa != fb:
                key = (fa, fb, rel)
                file_edges[key] = file_edges.get(key, 0) + 1
            ia = def_index.get(a)
            ib = def_index.get(b)
            if ia is not None and ib is not None:
                def_edges.append([ia, ib, rel])
        else:
            path = rec.get("file") or ""
            frontier_by_file[path] = frontier_by_file.get(path, 0) + 1
            kinds = frontier_kinds.setdefault(path, {})
            kind = rec.get("kind", "unnamed")
            kinds[kind] = kinds.get(kind, 0) + 1

    check_ceiling("%s at the end of the stream" % lang)

    paths = sorted(set(list(per_file) + list(frontier_by_file)) - {""})
    order = {p: i for i, p in enumerate(paths)}
    rows = []
    for path in paths:
        kinds = per_file.get(path, {})
        rows.append({
            "file": path,
            "nodes": sum(kinds.values()),
            "nodes_by_kind": kinds,
            "defs": kinds.get("def", 0),
            "frontier": frontier_by_file.get(path, 0),
            "frontier_by_kind": frontier_kinds.get(path, {}),
        })

    edge_rows = []
    for (fa, fb, rel), n in file_edges.items():
        if fa in order and fb in order:
            edge_rows.append([order[fa], order[fb], rel, n])
    edge_rows.sort(key=lambda r: -r[3])

    out_files = os.path.join(HERE, "graph_%s_files.json" % lang)
    doc = {
        "generated_by": "graph_files_build.py, streaming graph_%s.json "
                        "one record at a time" % lang,
        "source": "graph_%s.json" % lang,
        "population": {
            "files": len(rows),
            "records_streamed": seen,
            "inter_file_edge_pairs": len(edge_rows),
        },
        "pins": head.get("pins"),
        "counts": head.get("counts"),
        "files": rows,
        "file_edges": edge_rows,
    }
    with open(out_files, "w") as fh:
        json.dump(doc, fh, indent=1)

    out_defs = os.path.join(HERE, "graph_%s_defs.json" % lang)
    defs_doc = {
        "generated_by": "graph_files_build.py",
        "source": "graph_%s.json" % lang,
        "note": "the page reads this only when a file box is expanded. "
                "def_edges index into the flat order the defs were "
                "streamed in, which is the order by_file lists them. A "
                "definition's own name is carried in the `label` field of "
                "its record and nowhere else -- it is a display label on "
                "the member and is never a key, a grouping or a pairing.",
        "population": {"defs": len(def_index),
                       "def_to_def_edges": len(def_edges)},
        "by_file": defs_by_file,
        "def_edges": def_edges,
    }
    with open(out_defs, "w") as fh:
        json.dump(defs_doc, fh, indent=1)

    refuse_on_spelling([out_files, out_defs], report)
    secs = time.time() - t0
    mb = peak_mb()
    report("%-6s %s records -> %s files, %s inter-file pairs, %s defs, "
           "%s def-to-def edges" %
           (lang, "{:,}".format(seen), "{:,}".format(len(rows)),
            "{:,}".format(len(edge_rows)), "{:,}".format(len(def_index)),
            "{:,}".format(len(def_edges))))
    report("       wrote %s (%s bytes) and %s (%s bytes) in %.1f s; "
           "PEAK RESIDENT %.0f MB (ceiling %d MB)" %
           (os.path.basename(out_files),
            "{:,}".format(os.path.getsize(out_files)),
            os.path.basename(out_defs),
            "{:,}".format(os.path.getsize(out_defs)), secs, mb,
            MEMORY_CEILING_MB))
    return doc


def main():
    langs = sys.argv[1:] or ["go"]
    for lang in langs:
        try:
            build(lang)
        except MemoryCeilingReached as err:
            print("ABORTED BY NAME MemoryCeilingReached: %s" % err)
            return 2
    print("peak resident for the whole run: %.0f MB" % peak_mb())
    return 0


if __name__ == "__main__":
    sys.exit(main())
