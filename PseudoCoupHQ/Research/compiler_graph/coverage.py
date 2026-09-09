#!/usr/bin/env python3
"""SUPERSEDED RECORD, 2026-09-03 (task 75). FOLDED INTO graph.py.

`load_august`, `diary_targets` and the four-population `coverage` of
this file now live in `class Graph` in graph.py, and the diary reader
there keeps the subject column. Task 71's file had settled (both
round-14 tasks landed), which is the condition this file's own header
named. Nothing imports this file. It is kept, unedited below this
header, as the record of the lap that found the two defects in §3 of
log_175.

ONE THING THIS FILE GOT WRONG, recorded because the re-join it
prescribes was run verbatim first and returned zeros: the `task71`
graph form below builds a key `<file>:<line>:<name>` and looks for
kinds `func`/`method`, while task 71's graph spells ids
`<file>#<line>#<kind>#<ordinal>` with the kind `def`. Both mismatches
make the join total-miss. graph.py joins on the DECLARATION
COORDINATE `<file>:<line>`, which is the one coordinate both id
schemes carry. The re-join command is now:

    /tmp/reconnect_venv/bin/python3 graph.py join \
        --graph graph_go.json --diaries diaries/go \
        --instrumented t72/diary_targets_all.json \
        --out coverage_go2.json

--------------------------------------------------------------------

coverage.py -- task 72's half of `Graph`: the diary PRODUCER's target
selection, the diary READER for the produced format, and `Graph.coverage`
as the join.

Plan node: hq.research.compiler_graph.graph
(Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_9_graph/
CORE_0_3_5_9_graph.md). The CORE's `## design` block names the methods
`build`, `diary`, `query_path`, `coverage`, `super_ops` on a class
`Graph`; this file adds to that class and coins no new vocabulary.

WHY THIS IS A SUBCLASS AND NOT AN EDIT TO graph.py
--------------------------------------------------
graph.py is task 71's file and landed while this task was running
(mtime 2026-09-03 18:26). Editing a file another task may still be
writing is how a round loses work. So the additions live here as
`class Graph(graph.Graph)` and are a strict superset: every method of
task 71's class is inherited unchanged, three are added, two are
overridden with wider readers that still accept the old input.

THIS FOLDS INTO graph.py. When task 71's file settles, move
`diary_targets`, `diary` and `coverage` from here into `class Graph`
there verbatim and delete this file. Nothing else references it.

WHICH GO GRAPH THE JOIN USES, TODAY
-----------------------------------
Task 71's `graph.py` writes `graph_<lang>.json` with node ids spelled
`<relative_path>:<start_line>:<name>` and kind `def`. At the moment
this task needed a graph to select injection targets from,
`graph_go.json` from `graph.py` DID NOT EXIST on disk -- the only
`graph_go*.json` files were the August lap's, written by
`build_graph3.py`, whose node ids are spelled
`<relative_path>:<start_byte>-<end_byte>:<kind>` with kinds `func` and
`method`.

So the join is against the August graph, and the diary line carries
BOTH keys, so the re-join is one command and no recompile:

    diary line:  seq \t subject \t <august id> \t <name> \t <file>:<line>

    august key   = column 3, string equality
    task-71 key  = "%s:%s:%s" % (file, line, name)   -- columns 5 and 4

The re-join, once graph_go.json from graph.py exists:

    /tmp/reconnect_venv/bin/python3 coverage.py join \
        --graph graph_go.json --graph-form task71 \
        --diaries diaries/go --out coverage_go.json

Byte offsets are needed to INJECT (the edit is placed at a byte
coordinate that comes from the parse, which is the v0 `inject_emitid`
pattern the CORE names), and task 71's graph records only lines. So
target selection stays on the August graph even after the re-join.

THE SPELLING BAN (the owner, absolute, restated 2026-08-25). No operator
token appears in any key, grouping, pairing, row structure, candidate
selection or comparison scope produced by this file. Nothing here
groups by a probe's operator; probes are keyed by their unit id and
graph nodes by their coordinate. `check_no_spelling_keys.py` is run
over this file's output.

Coding discipline of this node (CORE 0_3_5): no complex statements.
"""

from __future__ import annotations

import argparse
import collections
import json
import sys
from pathlib import Path

import graph as task71

HERE = Path(__file__).resolve().parent

# The kinds of the August graph that are a FUNCTION BODY -- the only
# node kinds an entry hook can be placed in. Every other kind in that
# graph (ref, call, param, local_var, package_const, ...) is a position
# inside a body, not a place a statement can be inserted, so it is not
# part of the instrumentable population. That distinction is stated in
# every report this file feeds: an uninstrumentable node is a NAMED
# FRONTIER, never a "never visited" node.
BODY_KINDS = ("func", "method")

DIARY_IMPORT = "cmd/compile/internal/diary"


class Graph(task71.Graph):
    """Task 71's Graph, plus the diary producer's target selection, the
    reader for the produced diary format, and the coverage join."""

    # ------------------------------------------------- the August graph --

    @classmethod
    def load_august(cls, path):
        """Read a graph written by build_graph3.py (the August lap).

        Kept apart from task 71's `load` because the two files are
        different shapes and pretending otherwise is how a join goes
        quietly wrong.
        """
        payload = json.loads(Path(path).read_text())
        instance = cls("go")
        instance.pins = {
            "graph_form": "august",
            "written_by": "build_graph3.py",
            "file": str(path),
        }
        for record in payload["nodes"]:
            instance.static_structure["nodes"][record["id"]] = record
            instance._by_file.setdefault(record.get("file"), []).append(
                record["id"]
            )
        instance.static_structure["edges"] = payload.get("edges", [])
        instance.frontier = payload.get("frontier", [])
        return instance

    # ---------------------------------------------- diary, the producer --

    def diary_targets(self):
        """static_structure -> one injection target per function body.

        This is the SELECTION half of `Graph.diary`'s producer. The
        other half -- editing the compiler's source at these byte
        coordinates, rebuilding it, and running the probes -- is a
        lane, because it needs the toolchain and Airlock.

        The August lap chose 56 spots by a call-hop rule out of one
        seed file. This chooses EVERY function body of the region, so
        that "the nodes no probe visits" is a statement about the
        region and not about a hand-picked neighbourhood.
        """
        targets = []
        for record in self.static_structure["nodes"].values():
            if record.get("kind") not in BODY_KINDS:
                continue
            target = {
                "id": record["id"],
                "kind": record["kind"],
                "file": record["file"],
                "name": record.get("name") or "anonymous",
                "start_line": record["start_line"],
                "start_byte": record["start_byte"],
                "end_byte": record.get("end_byte"),
            }
            targets.append(target)
        targets.sort(key=lambda item: (item["file"], item["start_line"]))
        return targets

    # ------------------------------------------------ diary, the reader --

    def diary(self, diary_directory, key="august"):
        """diary files -> dynamic_structure, ORDERED.

        Widens task 71's reader, which took one node id per line, to the
        record this task's hook actually writes. THE LITERAL LINE, from
        diaries/go/op_0.txt:

            1\t-\tsrc/.../rewrite.go:22841-22896:func|StringToAux|src/.../rewrite.go:815

        Three TAB fields -- sequence, subject, payload -- and the
        payload is three PIPE fields: the graph node id, the function's
        name, and its original file:line. That is inject_diary.py's
        August format unchanged, which is why the August diaries still
        read. (This reader first assumed five tab fields, read every
        line, matched nothing, and reported 0 of 1,549 bodies visited.
        The shape is taken from the file now, not from prose about it.)

        `key` picks which of the two graph spellings the visited ids
        come out in:

            "august"  -> the payload's first pipe field, verbatim
            "task71"  -> "<file>:<line>:<name>", from pipe fields 3 and 2

        Order is preserved exactly as written. This is a DIARY: the
        sequence of nodes visited, never a count of visits.
        """
        directory = Path(diary_directory)
        if not directory.is_dir():
            self.add_frontier(
                "no_diaries_on_disk",
                str(directory),
                "no diary directory; dynamic_structure is empty and no "
                "coverage claim may be made from it",
            )
            self.dynamic_structure = {}
            return self.dynamic_structure
        self.dynamic_structure = {}
        self.diary_subjects = {}
        paths = sorted(directory.glob("*.txt"))
        for path in paths:
            probe = path.stem
            visited = []
            subjects = []
            for line in path.read_text(errors="replace").splitlines():
                stripped = line.strip()
                if not stripped:
                    continue
                columns = stripped.split("\t")
                if len(columns) == 1:
                    visited.append(columns[0])
                    continue
                if len(columns) < 3:
                    continue
                pieces = columns[2].split("|")
                if len(pieces) < 3:
                    continue
                node_id = pieces[0]
                if node_id == "-":
                    continue
                if key == "task71":
                    place = pieces[2]
                    cut = place.rfind(":")
                    if cut < 0:
                        continue
                    node_id = "%s:%s:%s" % (
                        place[:cut], place[cut + 1:], pieces[1],
                    )
                visited.append(node_id)
                subjects.append(columns[1])
            self.dynamic_structure[probe] = visited
            self.diary_subjects[probe] = subjects
        return self.dynamic_structure

    # ---------------------------------------------------------- the join --

    def coverage(self, instrumented=None):
        """static_structure x dynamic_structure -> per node which probes
        visited it and in what order; per probe its path; the
        never-visited set.

        POPULATIONS, stated in the result because the caller writes
        them into a report and a number without its population cannot
        be checked:

          population_region_nodes    every node of the region graph,
                                     all kinds
          population_body_nodes      the function bodies -- the only
                                     kind an entry hook can sit in
          population_instrumented    the bodies an edit was actually
                                     placed in (<= body nodes; the
                                     difference is a named frontier,
                                     listed, never called
                                     "never visited")
          population_probes          diaries read

        `never_visited` is over the INSTRUMENTED population only. A
        body that was never instrumented was not observed; saying no
        probe visited it would be a claim the evidence does not carry.
        """
        nodes = self.static_structure["nodes"]
        bodies = []
        for node_id, record in nodes.items():
            if record.get("kind") in BODY_KINDS:
                bodies.append(node_id)
        if instrumented is None:
            instrumented = list(bodies)
        instrumented_set = set(instrumented)

        visitors = collections.OrderedDict()
        first_visit_order = {}
        for probe in sorted(self.dynamic_structure):
            visited = self.dynamic_structure[probe]
            seen_here = set()
            order = []
            for node_id in visited:
                if node_id in seen_here:
                    continue
                seen_here.add(node_id)
                order.append(node_id)
                visitors.setdefault(node_id, []).append(probe)
            first_visit_order[probe] = order

        visited_instrumented = []
        never = []
        for node_id in sorted(instrumented_set):
            if node_id in visitors:
                visited_instrumented.append(node_id)
            else:
                never.append(node_id)

        off_map = []
        for node_id in visitors:
            if node_id not in nodes:
                off_map.append(node_id)

        never_by_file = collections.Counter()
        never_rows = []
        for node_id in never:
            record = nodes[node_id]
            never_by_file[record["file"]] += 1
            never_rows.append({
                "id": node_id,
                "file": record["file"],
                "start_line": record["start_line"],
                "name": record.get("name") or "anonymous",
                "kind": record["kind"],
            })
        never_rows.sort(key=lambda row: (row["file"], row["start_line"]))

        return {
            "population_region_nodes": len(nodes),
            "population_body_nodes": len(bodies),
            "population_instrumented": len(instrumented_set),
            "population_probes": len(self.dynamic_structure),
            "bodies_visited_by_at_least_one_probe":
                len(visited_instrumented),
            "never_visited_count": len(never),
            "never_visited": never_rows,
            "never_visited_by_file": dict(
                sorted(never_by_file.items(), key=lambda row: -row[1])
            ),
            "visited_ids_not_in_the_graph": off_map,
            "per_node_visitors": {
                node_id: probes for node_id, probes in visitors.items()
            },
            # PER PROBE, ITS PATH -- as the FIRST-VISIT ORDER: the
            # sequence of DISTINCT nodes in the order the probe's
            # compilation first entered each. This is an order, not a
            # count: the diary rule is kept. The FULL ordered event
            # stream is not copied in here because it is already on
            # disk, unabridged, as the diary file the probe is named
            # after -- diaries/go/<unit>.txt, 8.7 million lines over
            # the corpus. Copying it into this file would duplicate a
            # gigabyte and abridge nothing.
            "per_probe_path_note":
                "first-visit order; the unabridged ordered stream is "
                "the diary file itself, diaries/<language>/<unit>.txt",
            "per_probe_path": {
                probe: first_visit_order[probe]
                for probe in sorted(first_visit_order)
            },
        }


# ------------------------------------------------------------ commands ---


def command_targets(arguments):
    instance = Graph.load_august(arguments.graph)
    targets = instance.diary_targets()
    Path(arguments.out).write_text(json.dumps(targets, indent=1) + "\n")
    per_file = collections.Counter()
    for target in targets:
        per_file[target["file"]] += 1
    print("region nodes, all kinds : %d"
          % len(instance.static_structure["nodes"]))
    print("function bodies chosen  : %d" % len(targets))
    print("files                   : %d" % len(per_file))
    print("wrote %s" % arguments.out)


def command_join(arguments):
    if arguments.graph_form == "august":
        instance = Graph.load_august(arguments.graph)
    else:
        instance = Graph.load(arguments.graph)
    instance.diary(arguments.diaries, key=arguments.graph_form)
    instrumented = None
    if arguments.instrumented:
        records = json.loads(Path(arguments.instrumented).read_text())
        instrumented = [record["id"] for record in records]
    result = instance.coverage(instrumented=instrumented)
    result["provenance"] = {
        "graph": str(arguments.graph),
        "graph_form": arguments.graph_form,
        "diaries": str(arguments.diaries),
        "instrumented_list": str(arguments.instrumented or ""),
    }
    Path(arguments.out).write_text(json.dumps(result, indent=1) + "\n")
    for name in (
        "population_region_nodes",
        "population_body_nodes",
        "population_instrumented",
        "population_probes",
        "bodies_visited_by_at_least_one_probe",
        "never_visited_count",
    ):
        print("%-42s %d" % (name, result[name]))
    print("wrote %s" % arguments.out)


def main():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest="mode", required=True)

    p_targets = subs.add_parser("targets")
    p_targets.add_argument("--graph", required=True)
    p_targets.add_argument("--out", required=True)
    p_targets.set_defaults(run=command_targets)

    p_join = subs.add_parser("join")
    p_join.add_argument("--graph", required=True)
    p_join.add_argument("--graph-form", default="august",
                        choices=("august", "task71"))
    p_join.add_argument("--diaries", required=True)
    p_join.add_argument("--instrumented", default="")
    p_join.add_argument("--out", required=True)
    p_join.set_defaults(run=command_join)

    arguments = parser.parse_args()
    arguments.run(arguments)


if __name__ == "__main__":
    main()
