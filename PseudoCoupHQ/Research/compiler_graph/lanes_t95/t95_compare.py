#!/usr/bin/env python3
"""t95_compare.py -- THE STATIC EMITTER SET AGAINST WHAT RUNNING THE
COMPILER SHOWED, for one region, read-only, one argument.

Node: hq.research.compiler_graph.graph, the heading "the arch-opcode-node
-- a shape this node lacks, added 2026-09-05" (task 95).

ENTERING IS NOT EMITTING, and this program must not blur them.  A body a
probe walked through may emit no machine instruction, and a body that
emits one may never have been walked by these probes.  Both exclusive
parts are printed, and the population each is measured against is printed
beside it.

THE CORE'S OWN RULE decides the third bucket: "AN UNINSTRUMENTED NODE IS A
FRONTIER, NEVER A NEVER-VISITED NODE".  An entry hook can only sit in a
body an edit was placed in, so the split is three ways --
    entered by at least one probe
    instrumented, entered by none
    never instrumented, a NAMED FRONTIER
-- and never two.

THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
second violation).  No operator token may appear in ANY key, grouping,
pairing, row structure, candidate selection, or comparison scope.  The
pairing here is by the graph's own MACHINE COORDINATE
`<file>#<line>#<kind>#<ordinal>`; no token takes part in it, and this
program prints no label at all.

usage:  python3 t95_compare.py <go|cpp>
"""

import json
import sys

GRAPHS = "PseudoCoupGraphs"
HERE = "PseudoCoupHQ/Research/compiler_graph"


def main(language):
    arch = json.load(open("%s/arch_opcode_nodes_%s.json" % (GRAPHS, language)))
    cov = json.load(open("%s/coverage_%s_files.json" % (HERE, language)))
    entered = set(cov["per_def_visitors"])
    never = set(row["id"] for row in cov["never_visited_rows"])
    instrumented = entered.union(never)
    emitters = set(row["id"] for row in arch["definitions_marked"]
                   if row["state"] != "emits_nothing")
    defs = arch["populations"]["definitions"]
    probes = cov["populations"]["probes"]
    print("%s: %d definitions, %d instrumented bodies, %d probes"
          % (language, defs, len(instrumented), probes))
    print("  entered by at least one probe          %6d of %d definitions"
          % (len(entered), defs))
    print("  instrumented, entered by none          %6d of %d definitions"
          % (len(never), defs))
    print("  never instrumented, a NAMED FRONTIER   %6d of %d definitions"
          % (defs - len(instrumented), defs))
    print("  statically detected emitters           %6d of %d definitions"
          % (len(emitters), defs))
    print("  in BOTH sets                           %6d"
          % len(emitters.intersection(entered)))
    print("  emitters instrumented, entered by none %6d of %d emitters"
          % (len(emitters.intersection(never)), len(emitters)))
    print("  emitters never instrumented            %6d of %d emitters"
          % (len(emitters.difference(instrumented)), len(emitters)))
    print("  entered but emitting nothing           %6d of %d entered"
          % (len(entered.difference(emitters)), len(entered)))


if __name__ == "__main__":
    main(sys.argv[1])
