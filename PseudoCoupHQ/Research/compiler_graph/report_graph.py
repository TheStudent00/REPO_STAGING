#!/usr/bin/env python3
"""report_graph.py -- the three measurements task 71 asks of graph.py.

Plan node: hq.research.compiler_graph.graph. This file does not build
anything; it reads the graph_<lang>.json files graph.py wrote and
answers, per compiler:

  1. the go diff -- the new go graph against lap one's own output
     (build_graph.py -> graph_go_lapone.json), at the level the two
     node models share: which FILES are in the region, and which
     FUNCTION DEFINITIONS were found in them. The node counts
     themselves are NOT comparable and this file never compares them:
     lap one mints a node per identifier occurrence, graph.py mints a
     node per def, param, local and file. Saying which comparison is
     valid is the point of the section.

  2. one path query per compiler -- where a function parameter's value
     reaches the code that assigns it a physical register. Answered
     with the printed path, or refused with a NAMED frontier.

  3. coverage with the diaries that exist today, which is none.

THE SPELLING BAN: the goal of each query below is expressed as a
predicate over a node's FILE and its structural kind, plus the
compiler's own internal function names read out of its own source.
No operator token enters any key, grouping or candidate set here.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import graph as G

HERE = Path(__file__).resolve().parent
import sys                                                    # noqa: E402
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))
import graphs_home                                            # noqa: E402

#: THE GRAPHS MOVED, 2026-09-04.  The graphs, the coverage joins and the
#: diaries live in the companion folder `PseudoCoupGraphs`; the programs
#: and the reports stay here.  `graphs_home.path` answers for one
#: artifact, and falls back to this folder for anything not yet moved.


def artifact(name):
    moved = Path(graphs_home.path(name))
    return moved if moved.exists() else (HERE / name)


def graph_document(name):
    """one graph as a document, in EITHER form -- the old expanded one, or
    the COMPACT one the graphs are stored in since 2026-09-04."""
    import graph_compact
    path = str(artifact(name))
    if graph_compact.is_compact(path):
        return graph_compact.expanded_document(path)
    return json.loads(Path(path).read_text())


def load(name):
    return G.Graph.load(artifact("graph_%s.json" % name))


# --------------------------------------------------------- the go diff --


def go_diff():
    """Lap one's output against graph.py's, on the two things both
    node models name: region files, and function definitions."""
    lap_one = json.loads((HERE / "graph_go_lapone.json").read_text())
    new = graph_document("graph_go.json")

    lap_one_files = set()
    lap_one_defs = set()
    for node in lap_one["nodes"]:
        if node.get("file"):
            lap_one_files.add(node["file"])
        if node.get("kind") in ("func", "method"):
            lap_one_defs.add((node["file"], node.get("name")))

    new_files = set()
    new_defs = set()
    for node in new["nodes"]:
        if node.get("file"):
            new_files.add(node["file"])
        if node.get("kind") == "def" and node.get("label"):
            new_defs.add((node["file"], node["label"]))

    return {
        "lap_one_files": len(lap_one_files),
        "new_files": len(new_files),
        "files_only_in_lap_one": sorted(lap_one_files - new_files),
        "files_only_in_new": sorted(new_files - lap_one_files),
        "lap_one_named_defs": len(lap_one_defs),
        "new_named_defs": len(new_defs),
        "defs_in_both": len(lap_one_defs & new_defs),
        "defs_only_in_lap_one": sorted(lap_one_defs - new_defs)[:20],
        "defs_only_in_lap_one_count": len(lap_one_defs - new_defs),
        "defs_only_in_new": sorted(new_defs - lap_one_defs)[:20],
        "defs_only_in_new_count": len(new_defs - lap_one_defs),
        "counts_not_compared": (
            "node and edge totals are NOT compared: lap one mints a node "
            "per identifier occurrence (105,367 ref nodes of its 182,935) "
            "and graph.py mints a node per file, def, param and local. The "
            "two are different resolutions of the same region, not two "
            "measurements of one quantity."
        ),
    }


# ------------------------------------------------- the parameter query --

# Per compiler: the START is a parameter slot inside the function that
# walks a function's parameter list during lowering; the GOAL is the
# def, inside the same region, that assigns a physical location. Both
# ends are named by the compiler's OWN function names, read out of its
# own source.

QUESTIONS = {
    "go": {
        "start_file_ends": "abi/abiutils.go",
        "start_def_label": "ABIAnalyzeFuncType",
        "goal_labels": ("allocateRegs",),
        "gloss": (
            "go's own ABI analyzer walks a function type's parameters and "
            "hands each to the code that takes registers out of the "
            "available set. The lap-one answer landed on "
            "abi.assignParamOrReturn -> tryAllocRegs -> allocateRegs."
        ),
    },
    "cpp": {
        "start_file_ends": "clang/lib/CodeGen/CGCall.cpp",
        "start_def_label": "EmitFunctionProlog",
        "goal_labels": ("LowerFormalArguments", "AnalyzeFormalArguments",
                        "AllocateReg", "getPhysReg", "CCAssignFn"),
        "gloss": (
            "clang serves BOTH c and cpp. clang/lib/CodeGen builds the "
            "call's argument list with its ABI classification; the "
            "physical-register assignment itself happens in the X86 "
            "backend's calling-convention code."
        ),
    },
    "rust": {
        "start_file_ends": "rustc_codegen_ssa/src/mir/mod.rs",
        "start_def_label": "arg_local_refs",
        "goal_labels": ("store_fn_arg", "store", "get_param"),
        "gloss": (
            "rustc's codegen walks the MIR body's argument locals and "
            "stores each incoming argument into its place; the physical "
            "register is chosen by LLVM, which is not in rustc's region."
        ),
    },
    "swift": {
        "start_file_ends": "lib/SILGen/SILGenProlog.cpp",
        "start_def_label": "emitProlog",
        "goal_labels": ("createFunctionArgument", "emitBBArguments",
                        "getExplosionSchema", "createArgument"),
        "gloss": (
            "SILGen's prolog turns each declared parameter into a SIL "
            "function argument; IRGen later gives it an explosion schema. "
            "The physical register is chosen by LLVM, outside swift's own "
            "source."
        ),
    },
}


def short_label(record):
    """A def's label may be qualified by the class it is defined out of
    line for (`X86TargetLowering::LowerFormalArguments`). The trailing
    segment is the function's own name."""
    label = record.get("label") or ""
    return label.split("::")[-1]


def find_start(graph, question):
    for node in graph.static_structure["nodes"].values():
        if node.get("kind") != "def":
            continue
        if short_label(node) != question["start_def_label"]:
            continue
        if not node.get("file", "").endswith(question["start_file_ends"]):
            continue
        return node["id"]
    return None


def find_start_parameter(graph, def_id):
    """A parameter slot the start def contains -- the query begins on a
    named high-level parameter, which is the question's whole point."""
    for edge in graph.static_structure["edges"]:
        if edge["src"] != def_id:
            continue
        if edge["rel"] != "contains":
            continue
        record = graph.static_structure["nodes"].get(edge["dst"])
        if record is not None and record.get("kind") == "param":
            return record["id"]
    return None


def ask(name):
    question = QUESTIONS[name]
    graph = load(name)
    start_def = find_start(graph, question)
    if start_def is None:
        return {
            "language": name,
            "found": False,
            "named_frontier": (
                "the def %r was not read in file %r: the region does not "
                "contain it, or the reader did not name it"
                % (question["start_def_label"], question["start_file_ends"])
            ),
        }
    start = find_start_parameter(graph, start_def) or start_def
    goals = set(question["goal_labels"])

    def reached(record):
        if record.get("kind") != "def":
            return False
        return short_label(record) in goals

    result = graph.query_path(
        start, reached,
        steps=(("contains", "reversed"), ("calls", "forward")),
    )
    nodes = graph.static_structure["nodes"]
    printed = []
    for step in result.get("path", []):
        target = nodes[step["to"]]
        printed.append(
            "%s (%s) -> %s:%s %s [%s]"
            % (step["rel"], step.get("direction"), target.get("file"),
               target.get("start_line"),
               target.get("label") or "", target.get("kind"))
        )
    naming_goal = []
    for record in graph.frontier:
        if record["kind"] not in ("unresolved_call", "ambiguous_call"):
            continue
        detail = record.get("detail") or ""
        trailing = detail.split(".")[-1].split("->")[-1].split("::")[-1]
        if trailing in goals:
            naming_goal.append(
                {"kind": record["kind"], "callee_text": detail,
                 "file": record.get("file"), "at_line": record.get("at_line"),
                 "from_node": record.get("from_node"),
                 "candidate_count": record.get("candidate_count")}
            )
    return {
        "language": name,
        "gloss": question["gloss"],
        "frontier_naming_the_goal_count": len(naming_goal),
        "frontier_naming_the_goal": naming_goal[:10],
        "start": start,
        "start_def": start_def,
        "goal_labels": sorted(goals),
        "found": result.get("found", False),
        "hops": len(result.get("path", [])),
        "path": result.get("path", []),
        "printed_path": printed,
        "visited": result.get("visited"),
        "named_frontier": result.get("frontier_at_boundary"),
        "reason": result.get("reason"),
    }


# ------------------------------------------------------------ coverage --


def coverage_today(name):
    graph = load(name)
    graph.diary(artifact("diaries") / name)
    report = graph.coverage()
    return {
        "language": name,
        "population_defs": report["population_defs"],
        "population_probes": report["population_probes"],
        "defs_visited": report["defs_visited_by_at_least_one_probe"],
        "never_visited_count": report["never_visited_count"],
        "visited_keys_outside_the_region":
            report["visited_keys_outside_the_region"],
        "statement": (
            "go: 590 diaries exist (task 72's output, diaries/go/*.txt) and "
            "are joined here on the declaration coordinate. cpp, rust and "
            "swift: 0 diaries, because those compilers have not been built "
            "instrumented -- their whole def population is never-visited BY "
            "ABSENCE OF MEASUREMENT, which is not the same fact as a def no "
            "probe reaches, and this report never states it as the latter."
        ),
    }


def main():
    what = sys.argv[1] if len(sys.argv) > 1 else "all"
    out = {}
    if what in ("all", "diff"):
        out["go_diff"] = go_diff()
    if what in ("all", "query"):
        out["queries"] = {n: ask(n) for n in sorted(QUESTIONS)}
    if what in ("all", "coverage"):
        out["coverage"] = {n: coverage_today(n) for n in sorted(QUESTIONS)}
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
