#!/usr/bin/env python3
"""report_super_ops.py -- task 75's reader over `super_ops_go.json`.

Plan node: hq.research.compiler_graph.graph, sub-node `super_ops`
(Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_9_graph/
CORE_0_3_5_9_graph.md).

Two commands, both PRINT-ONLY -- nothing here mines and nothing here
decides. They exist so a claim can be read off the compiler's own
source and off the arch-units, rather than inferred:

    top20    for each of the highest-ranked candidates: its source
             spans, an EXCERPT of the compiler's own code at that span
             taken with `git show <pin>:<path>` from the pinned tree,
             the probe count, and two of the arch-units those probes
             produced, quoted from canon39.

    compare  the both-ways join against the superseded output-side
             miner (op_pipeline/super_ops3.json): graph candidates with
             no output-side counterpart, and output-side candidates
             with no graph counterpart, each named.

THE SPELLING BAN (the owner, absolute, restated 2026-08-25). No operator
token appears in any key, grouping, pairing, row structure, candidate
selection or comparison scope here. Candidates are keyed by their
SOURCE NODE IDS; the comparison scope is fixed by the output-side
record's own `sample_unit_ids` and `emitting_function`, both machine
coordinates. Compiler function names and unit ids ride once per row as
display labels.

THE LANGUAGE IS AN ARGUMENT, added 2026-09-04 by task 81 (log_190).
Task 75 wrote `compare` for the go lap and spelled `go/` into the unit
prefix in three places. Task 81 runs the same join over the cpp lap, so
the prefix is now `--language`, DEFAULTING TO `go`. Every key the go
artifact carries is composed from that value -- `go_units_named` and
`output_side_records_naming_go_units` are what the default still
produces, byte for byte -- so re-running the go join writes the same
shape it wrote before. A LANGUAGE IS NOT AN OPERATOR TOKEN: `go` and
`cpp` name which corpus a unit id belongs to, which is a machine
coordinate, and the spelling ban is untouched by it.

Coding discipline of this node (CORE 0_3_5): no complex statements.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
OP_PIPELINE = HERE.parent / "op_pipeline"
GO_SOURCE = Path.home() / "Programming" / "Sources" / "golang_src"
GO_PIN = "9f1012d9a1aa0831ff44ac9c767e96f9943d13fe"


def show_file(relative_path):
    """The compiler's own source at the pin. `git show`, never the
    working tree, so the excerpt is the text the diaries were made
    from."""
    result = subprocess.run(
        ["git", "show", "%s:%s" % (GO_PIN, relative_path)],
        cwd=str(GO_SOURCE), capture_output=True, text=True,
    )
    if result.returncode != 0:
        return None
    return result.stdout.splitlines()


def excerpt(cache, relative_path, start_line, count):
    lines = cache.get(relative_path)
    if lines is None:
        lines = show_file(relative_path)
        cache[relative_path] = lines
    if lines is None:
        return ["<the pinned tree has no such file>"]
    first = max(0, start_line - 1)
    return lines[first:first + count]


def load_arch_units():
    """Every go arch-unit of the corpus, by unit id -> its canon39 body
    text. 107 original + 483 regenerated."""
    units = {}
    original = json.loads(
        (OP_PIPELINE / "canon39_wrapped_go.json").read_text())
    units.update(original["units"])
    store = OP_PIPELINE / "canon39_regen_store"
    for path in sorted(store.glob("op_units2_go_c*.json")):
        payload = json.loads(path.read_text())
        units.update(payload["units"])
    return units


def command_top20(arguments):
    payload = json.loads(Path(arguments.candidates).read_text())
    units = load_arch_units()
    cache = {}
    rows = payload["candidates"]
    if arguments.max_support:
        # THE DISCRIMINATING BAND. A candidate every probe walks is
        # compiler machinery the whole corpus shares; it is a true
        # recurrence and it is reported first, by rank. This filter
        # asks the other question -- which recurring paths separate
        # one part of the corpus from another -- and it is a FILTER ON
        # SUPPORT, a machine count, never on what the probes spell.
        rows = [row for row in rows
                if row["probe_support"] <= arguments.max_support]
    print("# super-op candidates from the diaries -- the top %d"
          % arguments.count)
    if arguments.max_support:
        print("# filtered to probe support <= %d of %d"
              % (arguments.max_support, payload["populations"]["probes"]))
    print()
    print("PARAMETERS, stated on the artifact:")
    print(json.dumps(payload["parameters"], indent=1))
    print()
    print("POPULATIONS:")
    print(json.dumps(payload["populations"], indent=1))
    print()
    print("PIN of the compiler source every excerpt is taken from:")
    print("  %s  %s" % (GO_SOURCE, GO_PIN))
    print("  arch-unit bodies: canon39_wrapped_go.json (107 units) and "
          "canon39_regen_store/op_units2_go_c000*.json (483 units)")
    print()
    for candidate in rows[:arguments.count]:
        print("=" * 72)
        print("%s   length %d nodes   probe support %d of %d"
              % (candidate["candidate_id"], candidate["length"],
                 candidate["probe_support"],
                 payload["populations"]["probes"]))
        print("-" * 72)
        for span in candidate["source_spans"]:
            if not span.get("in_the_region_graph"):
                print("  %s   NOT A NODE OF THE REGION GRAPH (a named "
                      "frontier)" % span["coordinate"])
                continue
            print("  %s:%s-%s   %s"
                  % (span["file"], span["start_line"], span["end_line"],
                     span["label"]))
            print("    node id: %s" % span["node_id"])
            print("    LITERAL, `git show %s:%s`, lines %s..:"
                  % (GO_PIN[:12], span["file"], span["start_line"]))
            for line in excerpt(cache, span["file"], span["start_line"],
                                arguments.excerpt_lines):
                print("      %s" % line)
        print("-" * 72)
        shown = 0
        for unit_id in candidate["arch_unit_ids"]:
            if shown >= 2:
                break
            record = units.get(unit_id)
            if record is None:
                continue
            shown = shown + 1
            print("  arch-unit %s -- canon39 body_text, LITERAL:"
                  % unit_id)
            for line in str(record.get("body_text", "")).splitlines():
                print("      %s" % line)
        print("  probes (%d): %s"
              % (candidate["probe_support"],
                 ", ".join(candidate["probes"][:12])
                 + (" ..." if len(candidate["probes"]) > 12 else "")))
        print()


def output_side_records(payload):
    """Every candidate record of super_ops3.json, from its four
    sections, each carrying which section it came from."""
    rows = []
    unchanged = payload["unchanged_from_super_ops2"]
    for name, records in (("resolved", unchanged["resolved"]),
                          ("frontier_non_ambiguous",
                           unchanged["frontier_non_ambiguous"]),
                          ("broken_this_lap", payload["broken_this_lap"]),
                          ("still_ambiguous_or_refused",
                           payload["still_ambiguous_or_refused"])):
        for record in records:
            rows.append((name, record))
    return rows


def command_compare(arguments):
    """The both-ways join. What it can and cannot say is stated in the
    output, not assumed by the reader."""
    payload = json.loads(Path(arguments.candidates).read_text())
    other = json.loads(Path(arguments.output_side).read_text())
    rows = output_side_records(other)

    # The comparison scope comes from the OUTPUT-SIDE RECORD'S OWN
    # machine coordinates: the unit ids it names in the language under
    # study, and (where it has one) the compiler function it says
    # emitted the idiom. No token.
    language = getattr(arguments, "language", "go")
    prefix = language + "/"
    go_rows = []
    for section, record in rows:
        go_units = [u for u in record.get("sample_unit_ids", [])
                    if u.startswith(prefix)]
        if go_units:
            go_rows.append((section, record, go_units))

    # The graph side, indexed the same two ways.
    by_unit = {}
    by_coordinate = {}
    for candidate in payload["candidates"]:
        for unit_id in candidate["arch_unit_ids"]:
            by_unit.setdefault(unit_id, []).append(candidate)
        for span in candidate["source_spans"]:
            if span.get("in_the_region_graph"):
                key = "%s:%s" % (span["file"], span["start_line"])
                by_coordinate.setdefault(key, []).append(candidate)

    matched_output_side = []
    unmatched_output_side = []
    graph_candidates_hit = set()
    for section, record, go_units in go_rows:
        hits = []
        for unit_id in go_units:
            for candidate in by_unit.get(unit_id, []):
                hits.append(candidate["candidate_id"])
        distinct = sorted(set(hits))
        row = {
            "idiom_id": record["idiom_id"],
            "section": section,
            "support": record.get("support"),
            "%s_units_named" % language: go_units,
            "graph_candidates_covering_all_of_them": [],
            "graph_candidates_covering_some": len(distinct),
        }
        every = None
        for unit_id in go_units:
            here = set(c["candidate_id"] for c in by_unit.get(unit_id, []))
            every = here if every is None else (every & here)
        row["graph_candidates_covering_all_of_them"] = sorted(every or [])
        # THE STRICT TEST, and why both are reported. "Covers every
        # unit this record names" is satisfied by any sub-path the
        # whole corpus walks, and 669 of the graph candidates are
        # walked by all 590 probes -- so the loose test alone would
        # report a coincidence that is really ubiquity. The strict
        # test asks for a sub-path whose probe set does NOT SPILL
        # outside the units the record names: it recurs there and
        # nowhere else.
        named = set(unit[len(prefix):] for unit in go_units)
        strict = []
        for candidate_id in row["graph_candidates_covering_all_of_them"]:
            for candidate in payload["candidates"]:
                if candidate["candidate_id"] != candidate_id:
                    continue
                if set(candidate["probes"]) <= named:
                    strict.append(candidate_id)
                break
        row["graph_candidates_confined_to_those_units"] = strict
        if row["graph_candidates_covering_all_of_them"]:
            matched_output_side.append(row)
            graph_candidates_hit.update(
                row["graph_candidates_covering_all_of_them"])
        else:
            unmatched_output_side.append(row)

    graph_without = []
    for candidate in payload["candidates"]:
        if candidate["candidate_id"] not in graph_candidates_hit:
            graph_without.append(candidate["candidate_id"])

    # The `why_both` sentence carries MEASURED numbers, computed here
    # from the artifact in hand rather than repeated from the go lap.
    probe_population = payload["populations"]["probes"]
    ubiquitous = len([c for c in payload["candidates"]
                      if c["probe_support"] == probe_population])
    result = {
        "what_this_join_is": (
            "for every candidate of the superseded output-side miner "
            "whose named sample units are %s units, does a diary "
            "sub-path recur across exactly those probes? The scope is "
            "the output-side record's own unit ids -- machine "
            "coordinates, no operator token anywhere in the pairing."
            % language),
        "populations": {
            "output_side_candidate_records": len(rows),
            "output_side_records_naming_%s_units" % language: len(go_rows),
            "graph_candidates": len(payload["candidates"]),
            "graph_candidate_probes": probe_population,
        },
        "the_two_tests": {
            "loose": "some graph candidate recurs in every %s unit the "
                     "output-side record names -- satisfied by any "
                     "sub-path the whole corpus walks" % language,
            "strict": "some graph candidate recurs in those units AND "
                      "IN NO OTHERS -- the sub-path is confined to the "
                      "record's own scope",
            # THE THOUSANDS SEPARATOR IS PART OF THE SHAPE. Task 75's
            # artifact reads "9,809"; a bare %d re-ran it as "9809" and
            # the byte-for-byte proof in lane 7 caught the one-character
            # difference. Formatted with a comma, the go re-run is
            # identical.
            "why_both": "{:,} of the {:,} graph candidates are walked "
                        "by all {:,} probes, so the loose test on its "
                        "own would report ubiquity as coincidence".format(
                            ubiquitous, len(payload["candidates"]),
                            probe_population),
            "what_neither_can_say": "the output-side records carry "
                                    "SAMPLE unit ids, not their full "
                                    "member lists, so a subset test is "
                                    "over the sample",
        },
        "output_side_with_a_graph_counterpart_loose":
            len(matched_output_side),
        "output_side_with_a_graph_counterpart_strict":
            len([row for row in matched_output_side
                 if row["graph_candidates_confined_to_those_units"]]),
        "output_side_with_a_graph_counterpart":
            len(matched_output_side),
        "output_side_without_a_graph_counterpart":
            len(unmatched_output_side),
        "graph_candidates_with_an_output_side_counterpart":
            len(graph_candidates_hit),
        "graph_candidates_without_an_output_side_counterpart":
            len(graph_without),
        "matched": matched_output_side,
        "unmatched_output_side": unmatched_output_side,
        "graph_candidates_without_counterpart_ids": graph_without,
    }
    Path(arguments.out).write_text(json.dumps(result, indent=1) + "\n")
    for name in ("output_side_with_a_graph_counterpart_loose",
                 "output_side_with_a_graph_counterpart_strict",
                 "output_side_without_a_graph_counterpart",
                 "graph_candidates_with_an_output_side_counterpart",
                 "graph_candidates_without_an_output_side_counterpart"):
        print("%-56s %d" % (name, result[name]))
    print(json.dumps(result["populations"], indent=1))
    print("wrote %s" % arguments.out)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    subs = parser.add_subparsers(dest="mode", required=True)
    p_top = subs.add_parser("top20")
    p_top.add_argument("--candidates", default="super_ops_go.json")
    p_top.add_argument("--count", type=int, default=20)
    p_top.add_argument("--excerpt-lines", type=int, default=6,
                       dest="excerpt_lines")
    p_top.add_argument("--max-support", type=int, default=0,
                       dest="max_support")
    p_top.set_defaults(run=command_top20)
    p_cmp = subs.add_parser("compare")
    p_cmp.add_argument("--candidates", default="super_ops_go.json")
    p_cmp.add_argument("--output-side",
                       default=str(OP_PIPELINE / "super_ops3.json"),
                       dest="output_side")
    p_cmp.add_argument("--out", default="super_ops_comparison_go.json")
    p_cmp.add_argument("--language", default="go",
                       help="which corpus the output-side record's unit "
                            "ids must belong to; composes every key the "
                            "artifact carries, so the default writes "
                            "exactly the shape the go lap wrote")
    p_cmp.set_defaults(run=command_compare)
    arguments = parser.parse_args()
    arguments.run(arguments)


if __name__ == "__main__":
    main()
