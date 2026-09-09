#!/usr/bin/env python3
"""diary_inputs_build.py -- the two inputs the clang diary lap needs,
built on the host in BOUNDED MEMORY and written into `t81/`.

Plan node: hq.research.compiler_graph.graph, method `diary`
(Planning/node_0_3_research/node_0_3_5_compiler_graph/node_0_3_5_9_graph/
CORE_0_3_5_9_graph.md).

WHAT IT WRITES, and why each exists
-----------------------------------
  t81/probes_cpp.json
      One probe source per unit of the ORIGINAL corpus's c and cpp
      populations, keyed by unit id. The unit list is RECOUNTED from
      canon39_wrapped_c.json and canon39_wrapped_cpp.json rather than
      taken from a prior report's figure; the source text comes from
      probe_manifest_c.json / probe_manifest_cpp.json, joined on the
      manifest's own `n` field. The `operator` field of the manifest is
      NOT carried: a probe is keyed by its unit id only.

  t81/diary_targets_cpp.json
      One injection target per function body of the cpp region that an
      entry hook can actually be placed in. Read from task 73's
      `graph_cpp_defs.json` (3.3 MB) rather than from `graph_cpp.json`
      (331 MB), because every reader of this graph runs in bounded
      memory -- a settled rule of the node's CORE.

      THE INSTRUMENTED POPULATION IS `.cpp` BODIES ONLY. 1,664 of the
      region's 10,789 definitions sit in `.h` files, and 17 have no
      declared name (a lambda has no declarator, so `graph.py` records
      an empty label for it). Both groups are written into the file as
      NAMED FRONTIERS with their counts and their cause, so the
      coverage join can say "not observable by this instrument" rather
      than "no probe visited it" -- the CORE's settled rule that an
      uninstrumented node is a frontier, never a never-visited node.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope,
anywhere in this line -- not in matching, not in "which pairs get
compared", not in report rows, not in dropdowns. The candidate set for
comparison comes from machine-form evidence (clusters, connections,
type pairs) or from ratified intention -- never from the token. The
token appears exactly once per unit: as a display label on the member.
HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
campaign's cross-language matrix (caught by the owner 2026-08-24);
(2) verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix
brief itself reintroduced it as "same-operator pairs"). MECHANICAL
GUARD REQUIRED: every pipeline stage that groups or pairs units must
run the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
refuse its own output on failure. A brief handed to any subagent for
this line MUST paste this paragraph verbatim.

Coding discipline of this node (CORE 0_3_5): no complex statements.
"""

import json
import resource
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
GRAPH_HOME = HERE.parent
OP_PIPELINE = GRAPH_HOME.parent / "op_pipeline"

# The instrumentable extension. A `.h` body is excluded on this lap and
# recorded as a frontier; see the module docstring.
INSTRUMENTABLE_EXTENSION = ".cpp"


def peak_mb():
    usage = resource.getrusage(resource.RUSAGE_SELF)
    return usage.ru_maxrss / 1024.0


def read_units(language):
    """The unit ids of one original-corpus population, RECOUNTED."""
    path = OP_PIPELINE / ("canon39_wrapped_%s.json" % language)
    payload = json.loads(path.read_text())
    units = sorted(payload["units"])
    return units, payload["meta"], payload["tally"], path


def read_manifest(language):
    """unit number -> probe source, from the original probe manifest.

    Only two fields are taken: the probe's own number and its source
    text. The manifest's `operator` field is left where it is.
    """
    path = OP_PIPELINE / ("probe_manifest_%s.json" % language)
    payload = json.loads(path.read_text())
    by_number = {}
    for key, record in payload["probes"].items():
        by_number[int(record["n"])] = record["source"]
    return by_number, path


def build_probes():
    probes = {}
    populations = {}
    missing = {}
    sources_read = []
    for language in ("c", "cpp"):
        units, meta, tally, unit_path = read_units(language)
        by_number, manifest_path = read_manifest(language)
        sources_read.append(str(unit_path.name))
        sources_read.append(str(manifest_path.name))
        found = 0
        absent = []
        for unit in units:
            number = int(unit.split("/op_")[1])
            source = by_number.get(number)
            if source is None:
                absent.append(unit)
                continue
            probes[unit] = {
                "source": source,
                "manifest": manifest_path.name,
                "manifest_key": str(number),
                "population": "original",
                "language": language,
            }
            found = found + 1
        populations[language] = {
            "units_recounted_from": unit_path.name,
            "units": len(units),
            "tally_on_that_file": tally,
            "probe_source_found": found,
            "probe_source_absent": len(absent),
        }
        if absent:
            missing[language] = absent
    return probes, populations, missing, sources_read


def build_targets():
    """The injection targets, and the two named frontiers beside them."""
    defs_path = GRAPH_HOME / "graph_cpp_defs.json"
    files_path = GRAPH_HOME / "graph_cpp_files.json"
    defs = json.loads(defs_path.read_text())
    files = json.loads(files_path.read_text())

    targets = []
    header_bodies = 0
    unnamed_bodies = 0
    for file_name, rows in defs["by_file"].items():
        instrumentable = file_name.endswith(INSTRUMENTABLE_EXTENSION)
        for record in rows:
            label = record.get("label") or ""
            if not instrumentable:
                header_bodies = header_bodies + 1
                continue
            if not label:
                unnamed_bodies = unnamed_bodies + 1
                continue
            # THE ROW IS A TYPED UNIT OBJECT. `label` is the compiler
            # function's OWN name, and one of the region's functions is
            # named `consume`, which is also one of the 91 operator
            # tokens the corpus probes; the spelling guard read it as a
            # spelling on an object it could not tell was a single unit
            # and refused this artifact (2026-09-04, log_190). The ruled
            # remedy is a typed-object SHAPE, not a role key and not a
            # field whitelist, so the row carries a language field
            # beside its unit id. Nothing reads this field -- the
            # injector uses `id`, `file`, `start_line`, `end_line` and
            # `label` and nothing else -- so adding it changes no
            # injection.
            targets.append({
                "id": record["id"],
                "language": files["pins"]["region"],
                "file": file_name,
                "label": label,
                "start_line": record["start_line"],
                "end_line": record["end_line"],
            })
    targets.sort(key=lambda row: (row["file"], row["start_line"]))
    payload = {
        "generated_by": "t81/diary_inputs_build.py",
        "read_from": [defs_path.name, files_path.name],
        "pins": files["pins"],
        "region_counts_from_the_graph": files["counts"],
        "instrumentable_extension": INSTRUMENTABLE_EXTENSION,
        "population": {
            "region_defs": files["counts"]["nodes_by_kind"]["def"],
            "targets_selected": len(targets),
            "frontier_body_in_a_header_file": header_bodies,
            "frontier_body_with_no_declared_name": unnamed_bodies,
        },
        "frontier_note": (
            "A body this pass does not place an entry hook in is a NAMED "
            "FRONTIER, never a never-visited node (CORE 0_3_5_9, settled "
            "rule). Two causes are counted above: a body declared in a "
            "header file, which one edit would carry into every "
            "translation unit that includes it; and a body with no "
            "declared name, which is a lambda -- tree-sitter's "
            "lambda_expression has no declarator, so graph.py records an "
            "empty label for it."
        ),
        "targets": targets,
    }
    return payload


def main():
    probes, populations, missing, sources_read = build_probes()
    probes_payload = {
        "meta": {
            "role": (
                "the c and cpp probes of the ORIGINAL corpus, one source "
                "per unit; clang serves both languages, so they share one "
                "diary lap"
            ),
            "population": (
                "the original corpus: 610 c units of canon39_wrapped_c.json "
                "plus 770 cpp units of canon39_wrapped_cpp.json, both "
                "recounted by this program rather than quoted"
            ),
            "sources_read_from": sources_read,
            "note": (
                "the operator field is not carried here; a probe is keyed "
                "by its unit id only (spelling ban)"
            ),
            "populations": populations,
            "units_with_no_probe_source": missing,
        },
        "count": len(probes),
        "probes": probes,
    }
    probes_path = HERE / "probes_cpp.json"
    probes_path.write_text(json.dumps(probes_payload, indent=1) + "\n")

    targets_payload = build_targets()
    targets_path = HERE / "diary_targets_cpp.json"
    targets_path.write_text(json.dumps(targets_payload, indent=1) + "\n")

    print("probes written : %s" % probes_path)
    for language, row in populations.items():
        print("   %-4s units %4d  probe source found %4d  absent %d"
              % (language, row["units"], row["probe_source_found"],
                 row["probe_source_absent"]))
    print("   total probes  : %d" % len(probes))
    print("targets written: %s" % targets_path)
    for key, value in targets_payload["population"].items():
        print("   %-40s %d" % (key, value))
    print("peak resident  : %.1f MB" % peak_mb())
    if missing:
        print("REFUSING: some units have no probe source")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
