#!/usr/bin/env python3
"""t95_show.py -- read one fact off the arch-opcode-node artifacts and
print it. Read-only, one argument, deterministic output.

Node: hq.research.compiler_graph.graph, the heading "the arch-opcode-node
-- a shape this node lacks, added 2026-09-05" (task 95).

WHY IT EXISTS. log_200's claims must each carry a command that reproduces
them (hq.conventions, and task 90's checker). A python one-liner long
enough to do that is unreadable in a log and fragile in a shell -- lane
t95_l10 lost two claims to a `&` the lane shell escaped. This file is the
readable form of those one-liners.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation). No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope. This
program groups nothing and pairs nothing: it prints fields of one
artifact, keyed by region name and by ARCH OPCODE, which is machine form
and a legitimate key.

usage:  python3 t95_show.py <declarations <lang> | shrink | reasons
                            | cost | frontier | emitterfiles <lang>>
"""

import json
import sys

GRAPHS = "PseudoCoupGraphs"
LANGUAGES = ("go", "cpp", "rust", "swift")


def load(language):
    return json.load(open("%s/arch_opcode_nodes_%s.json" % (GRAPHS, language)))


def declarations(language):
    doc = load(language)
    rows = doc["emitter_declarations"]
    print("%s: %d declarations of the arch opcode type" % (language, len(rows)))
    for row in rows:
        print("  %s:%d  %s" % (row["file"], row["line"], row["role"]))
        print("     %s" % row["declaration"])


def shrink():
    print("region  definitions  emitters  +direct  +all  emits_nothing  kept")
    for language in LANGUAGES:
        doc = load(language)
        s = doc["shrink"]
        n = s["definitions"]
        print("%-6s  %11d  %8d  %7d  %4d  %13d  %.1f%%"
              % (language, n, s["emitters_only"],
                 s["emitters_and_their_direct_callers"],
                 s["emitters_and_all_their_callers"],
                 doc["by_state"]["emits_nothing"],
                 100.0 * s["emitters_and_all_their_callers"] / n))


def reasons():
    for language in LANGUAGES:
        doc = load(language)
        print("%s %s" % (language,
                         json.dumps(doc["hop_not_resolved_by_reason"],
                                    sort_keys=True)))


def cost():
    key = ("state_three_definitions_that_name_arch_opcodes_elsewhere_"
           "in_their_own_body")
    for language in LANGUAGES:
        doc = load(language)
        print("%-6s wall %4.1f s  peak %6.1f MB  ceiling %d MB  refusal %s  "
              "files %3d  co-located %d"
              % (language, doc["cost"]["wall_seconds"],
                 doc["cost"]["peak_resident_mb"],
                 doc["cost"]["memory_ceiling_mb"],
                 doc["cost"]["refusal_name"],
                 doc["cost"]["region_files_read"], doc[key]))


def frontier():
    doc = load("cpp")
    for one in doc["named_frontiers"]:
        print(one)


def emitterfiles(language):
    doc = load(language)
    rows = [r for r in doc["definitions_marked"]
            if r["state"] != "emits_nothing"]
    counted = {}
    for row in rows:
        counted[row["file"]] = counted.get(row["file"], 0) + 1
    print("%s: %d emitter definitions over %d files"
          % (language, len(rows), len(counted)))
    for name in sorted(counted, key=lambda k: (-counted[k], k)):
        print("  %-52s %d" % (name, counted[name]))


if __name__ == "__main__":
    what = sys.argv[1]
    if what in ("declarations", "emitterfiles"):
        globals()[what](sys.argv[2])
    else:
        globals()[what]()
