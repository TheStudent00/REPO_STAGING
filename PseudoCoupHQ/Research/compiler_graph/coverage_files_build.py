#!/usr/bin/env python3
"""coverage_files_build.py -- the FILE-LEVEL COVERAGE INDEX, and the byte
index that lets one probe's full path be read without opening the join.

Node: hq.research.compiler_graph.graph (`coverage`), read by
hq.research.compiler_graph.dashboard (`coverage_view`, pane 4).

WHY THIS FILE EXISTS.  Task 72/75's join is `coverage_go2.json`,
515,160,866 bytes, holding 10,015,022 diary events.  The dashboard is a
page opened by double-click and may never hold that in memory.  This
builder streams it ONE LINE AT A TIME and writes one small artifact:

  coverage_go_files.json  the populations, the per-file coverage rows,
                          the never-visited listing with labels, the
                          per-definition visitor counts, and per probe:
                          its file-level path (consecutive repeats of the
                          same file collapsed to a run with a count) plus
                          the BYTE RANGE of that probe's full path inside
                          coverage_go2.json.

THE RANGED READ.  The page draws the file-level path from this summary.
When a file box is expanded it wants the function-level path for that one
probe, so it slices coverage_go2.json between `byte_start` and `byte_end`
-- one Blob.slice, a few hundred kilobytes, out of a 515 MB file -- and
parses the one array.  Nothing else of that file is ever read.

BOUNDED MEMORY, STATED.  Peak resident set is measured with
`resource.getrusage` and printed.  The builder ABORTS BY NAME
(`MemoryCeilingReached`) above the ceiling rather than being stopped by
the operating system, per the graph CORE's settled rule.

WHAT `coverage` MAY SPEAK ABOUT.  The CORE's settled rule: an entry hook
can only sit in a function body, so the population is the bodies an edit
was placed in (1,534 of go's 1,859 definitions) and the remaining 325 are
a NAMED FRONTIER, not never-visited nodes.  Both numbers are carried
through to the page and the page prints both.

THE SPELLING BAN.  Every key here is a machine identifier -- a source
path, a node id of the form file#line#kind#ordinal, or a probe's unit id.
No operator token appears in any key, grouping or pairing.  The emitted
json is walked by the unmodified check_no_spelling_keys.py.

    /tmp/reconnect_venv/bin/python3 coverage_files_build.py
"""

import importlib.util
import json
import os
import re
import resource
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

#: WHAT ANSWERS FOR WHICH COMPILER.  This builder was written for go
#: alone (task 73) and the go paths were literals; pane 4's DRAWING needs
#: the same per-file rows for the clang graph, so the three paths became
#: a table and the body below is unchanged.
#:
#:   join            the coverage join, in the COMPANION GRAPH FOLDER
#:                   since 2026-09-04 -- 515 MB for go, 417 MB for c and
#:                   cpp, streamed one line at a time and never held
#:   instrumented    the bodies an entry hook was actually placed in.
#:                   This is the population `coverage` may speak about
#:                   (graph CORE, settled rule)
#:   out             the summary the page reads, which stays TRACKED in
#:                   this repository so the chronology can recompute
#:                   pane 4 at a past moment
SOURCES = {
    "go": {
        "join": "coverage_go2.json",
        "instrumented": ("t72", "diary_targets_all.json"),
        "out": "coverage_go_files.json",
        "graph_summary": "graph_go_files.json",
    },
    "cpp": {
        "join": "coverage_c_and_cpp.json",
        "instrumented": ("t81", "inject_report_cpp2.json"),
        "out": "coverage_cpp_files.json",
        "graph_summary": "graph_cpp_files.json",
    },
}

LANG = "go"
SRC = None
TARGETS = None
OUT = None


def use(lang):
    """point this builder at one compiler's artifacts.

    The join lives in the companion graph folder; the instrumented-body
    record and the summary this writes both stay in this repository.
    """
    import graphs_home
    global LANG, SRC, TARGETS, OUT
    if lang not in SOURCES:
        raise SystemExit("no coverage join is named for %r; this builder "
                         "knows %s" % (lang, ", ".join(sorted(SOURCES))))
    LANG = lang
    row = SOURCES[lang]
    moved = graphs_home.path(row["join"])
    SRC = moved if os.path.exists(moved) else os.path.join(HERE, row["join"])
    TARGETS = os.path.join(HERE, *row["instrumented"])
    OUT = os.path.join(HERE, row["out"])
    return row

MEMORY_CEILING_MB = 6144

# THE ONE STATED BOUND OF THIS ARTIFACT.  A probe's file-level path is the
# ordered list of source files its compilation entered, consecutive repeats
# of the same file collapsed into one run with a count.  Those paths are
# tens of thousands of runs long and 590 of them will not fit in a summary
# the page may read whole, so the summary CARRIES THE FIRST `FILE_RUN_CAP`
# RUNS AND SAYS SO: every probe row states `file_runs_total` beside
# `file_runs_carried`, and the page prints both.  The full path is never
# lost -- it is one ranged read away, at `byte_start`..`byte_end` of
# coverage_go2.json.
FILE_RUN_CAP = 600

SCALAR = re.compile(rb'^ "([a-z_]+)": (\d+),?$')
KEY = re.compile(rb'^ "([a-z_]+)":')
ENTRY = re.compile(rb'^  "(.*)": \[')
STRING = re.compile(rb'^   "(.*)",?$')


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


def instrumented_by_file():
    """The bodies an entry hook was actually placed in, per file.  This is
    the population `coverage` may speak about (graph CORE, settled rule).

    Two record shapes, because the two injectors wrote two: go's task-72
    target list is an array of rows carrying `file`, and the clang
    injector's task-81 report carries `instrumented_ids` -- the ids of
    the bodies it actually edited, which is the tighter population (8,871
    of 9,108 targets; the 237 it skipped each carry a named cause and are
    a NAMED FRONTIER of this join)."""
    with open(TARGETS) as fh:
        doc = json.load(fh)
    per = {}
    if isinstance(doc, dict):
        ids = doc.get("instrumented_ids") or []
        for one in ids:
            path = str(one).split("#", 1)[0]
            per[path] = per.get(path, 0) + 1
        return per, len(ids)
    for row in doc:
        per[row["file"]] = per.get(row["file"], 0) + 1
    return per, len(doc)


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


def build(lang="go", report=print):
    use(lang)
    if not os.path.exists(SRC):
        report("REFUSED: %s is not on disk (regenerate with graph.py "
               "coverage; it is gitignored at 515 MB)" % SRC)
        return None
    t0 = time.time()
    instrumented, instrumented_total = instrumented_by_file()

    scalars = {}
    never_rows = []
    per_def_visitors = {}
    probes = []

    section = None
    offset = 0
    # per_node_visitors state
    node_id = None
    node_n = 0
    # per_probe_path state
    probe = None
    probe_start = 0
    probe_events = 0
    runs = None
    obj_buf = None

    file_order = []
    file_index = {}
    #: EVERY file any probe entered, collected while streaming.
    #: Found by drawing it (task 93): the `entered` flag was read off
    #: `file_runs`, which is the summary's CAPPED slice of a probe's path,
    #: so a file a probe reached only after its first 600 runs was drawn
    #: as never entered. The cap belongs to what the summary CARRIES, not
    #: to what it COUNTS.
    entered_slots = set()

    def file_slot(path):
        i = file_index.get(path)
        if i is None:
            i = len(file_order)
            file_index[path] = i
            file_order.append(path)
        return i

    with open(SRC, "rb") as fh:
        for line in fh:
            here = offset
            offset += len(line)

            head = KEY.match(line)
            if head:
                section = head.group(1).decode()
                mb = check_ceiling("at section %s" % section)
                report("   ... entering %s at byte %s, peak %.0f MB"
                       % (section, "{:,}".format(here), mb))
                got = SCALAR.match(line)
                if got:
                    scalars[got.group(1).decode()] = int(got.group(2))
                continue

            if section == "never_visited_rows":
                if line.startswith(b"  {"):
                    obj_buf = [line]
                elif obj_buf is not None:
                    obj_buf.append(line)
                    if line.startswith(b"  }"):
                        text = b"".join(obj_buf).rstrip().rstrip(b",")
                        never_rows.append(json.loads(text))
                        obj_buf = None
                continue

            if section == "per_node_visitors":
                start = ENTRY.match(line)
                if start:
                    node_id = start.group(1).decode()
                    node_n = 0
                    continue
                if node_id is None:
                    continue
                if line.startswith(b"  ]"):
                    per_def_visitors[node_id] = node_n
                    node_id = None
                elif STRING.match(line):
                    node_n += 1
                continue

            if section == "per_probe_path":
                start = ENTRY.match(line)
                if start:
                    probe = start.group(1).decode()
                    # the value opens at the '[' on this line
                    probe_start = here + line.index(b"[")
                    probe_events = 0
                    runs = []
                    continue
                if probe is None:
                    continue
                if line.startswith(b"  ]"):
                    for slot, _many in runs:
                        entered_slots.add(slot)
                    probes.append({
                        "probe": probe,
                        "events": probe_events,
                        "file_runs": runs[:FILE_RUN_CAP],
                        "file_runs_total": len(runs),
                        "file_runs_carried": min(len(runs), FILE_RUN_CAP),
                        "byte_start": probe_start,
                        "byte_end": here + line.index(b"]") + 1,
                    })
                    probe = None
                    runs = None
                    if len(probes) % 100 == 0:
                        check_ceiling("after %d probes" % len(probes))
                    continue
                got = STRING.match(line)
                if got:
                    probe_events += 1
                    where = got.group(1).decode()
                    path = where.rsplit(":", 1)[0]
                    slot = file_slot(path)
                    if runs and runs[-1][0] == slot:
                        runs[-1][1] += 1
                    else:
                        runs.append([slot, 1])

    check_ceiling("at the end of the stream")

    # ---- the per-file rows -------------------------------------------
    never_by_file = {}
    for row in never_rows:
        never_by_file[row["file"]] = never_by_file.get(row["file"], 0) + 1

    visited_by_file = {}
    visitors_by_file = {}
    for nid, n in per_def_visitors.items():
        path = nid.split("#", 1)[0]
        visited_by_file[path] = visited_by_file.get(path, 0) + 1
        visitors_by_file[path] = visitors_by_file.get(path, 0) + n

    entered_files = set(file_order[slot] for slot in entered_slots)

    paths = sorted(set(list(instrumented) + list(never_by_file) +
                       list(visited_by_file)))
    rows = []
    for path in paths:
        rows.append({
            "file": path,
            "instrumented": instrumented.get(path, 0),
            "visited": visited_by_file.get(path, 0),
            "never": never_by_file.get(path, 0),
            "visitor_total": visitors_by_file.get(path, 0),
            "entered": path in entered_files,
        })

    never_entered = [r["file"] for r in rows
                     if r["instrumented"] > 0 and r["visited"] == 0]

    doc = {
        "generated_by": "coverage_files_build.py, streaming %s one line "
                        "at a time" % os.path.basename(SRC),
        "source": os.path.basename(SRC),
        "source_folder": os.path.dirname(SRC),
        "lang": LANG,
        "graph_summary": SOURCES[LANG]["graph_summary"],
        "populations": {
            "region_nodes": scalars.get("population_region_nodes"),
            "defs": scalars.get("population_defs"),
            "instrumented_bodies": scalars.get("population_instrumented"),
            "instrumented_bodies_recounted_here": instrumented_total,
            "probes": scalars.get("population_probes"),
            "visited_by_at_least_one_probe":
                scalars.get("instrumented_visited_by_at_least_one_probe"),
            "never_visited": scalars.get("never_visited_count"),
            "uninstrumented_defs_a_named_frontier":
                scalars.get("uninstrumented_defs_a_named_frontier"),
            "probes_with_a_path": len(probes),
            "files_with_a_row": len(rows),
            "files_never_entered": len(never_entered),
            "file_run_cap": FILE_RUN_CAP,
        },
        "note": "coverage speaks only about instrumented bodies: an entry "
                "hook can sit in a function body and nowhere else, so the "
                "uninstrumented definitions are a NAMED FRONTIER and not "
                "never-visited nodes (graph CORE, settled rule).",
        "file_order": file_order,
        "by_file": rows,
        "never_entered_files": never_entered,
        "never_visited_rows": never_rows,
        "per_def_visitors": per_def_visitors,
        "probes": probes,
    }
    with open(OUT, "w") as fh:
        json.dump(doc, fh, separators=(",", ":"))

    refuse_on_spelling([OUT], report)
    secs = time.time() - t0
    report("%s coverage -> %s files, %s probes, %s never-visited rows, "
           "%s visited definitions, %s files never entered"
           % (LANG, "{:,}".format(len(rows)), "{:,}".format(len(probes)),
              "{:,}".format(len(never_rows)),
              "{:,}".format(len(per_def_visitors)),
              "{:,}".format(len(never_entered))))
    report("       wrote %s (%s bytes) in %.1f s; PEAK RESIDENT %.0f MB "
           "(ceiling %d MB)"
           % (os.path.basename(OUT), "{:,}".format(os.path.getsize(OUT)),
              secs, peak_mb(), MEMORY_CEILING_MB))
    return doc


def main():
    for lang in (sys.argv[1:] or ["go"]):
        try:
            build(lang)
        except MemoryCeilingReached as err:
            print("ABORTED BY NAME MemoryCeilingReached: %s" % err)
            return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
