#!/usr/bin/env bash
# t95 lane 11 -- the two claims lane 10's shell mangled, re-printed.
#
# Node: hq.research.compiler_graph.graph, heading "the arch-opcode-node".
# Lane 10 step [7/8] wrote the set intersection with `&`, which the lane
# shell escaped into the python text; both commands died on a
# SyntaxError. Written with `.intersection()` and `.difference()` here,
# which no shell touches. Read-only.
#
# THE SPELLING BAN, ABSOLUTE (the owner, restated in anger 2026-08-25 after a
# second violation). No operator token may appear in ANY key, grouping,
# pairing, row structure, candidate selection, or comparison scope,
# anywhere in this line -- not in matching, not in "which pairs get
# compared", not in report rows, not in dropdowns. The candidate set for
# comparison comes from machine-form evidence (clusters, connections,
# type pairs) or from ratified intention -- never from the token. The
# token appears exactly once per unit: as a display label on the member.
# HISTORY OF VIOLATIONS, so the pattern is visible: (1) the arch
# campaign's cross-language matrix (caught by the owner 2026-08-24);
# (2) verdicts.py's row pairing (caught by the owner 2026-08-25 -- the fix
# brief itself reintroduced it as "same-operator pairs"). MECHANICAL
# GUARD REQUIRED: every pipeline stage that groups or pairs units must
# run the spelling-key check (op_pipeline/check_no_spelling_keys.py) and
# refuse its own output on failure.
#
# The pairing below is by the graph's own machine coordinate. No token
# takes part in it.
set -u
run() { echo; echo "\$ $*"; eval "$@" 2>&1; }
say() { echo; echo "======== $* ========"; }

say "[1/3] go -- the static emitter set against what running the compiler showed"
run "python3 PseudoCoupHQ/Research/compiler_graph/lanes_t95/t95_compare.py go"

say "[2/3] cpp -- the same"
run "python3 PseudoCoupHQ/Research/compiler_graph/lanes_t95/t95_compare.py cpp"

say "[3/3] the emitter definitions of go, by state, with the compiler's own name on each"
run "python3 -c \"import json;d=json.load(open('PseudoCoupGraphs/arch_opcode_nodes_go.json'));r=[x for x in d['definitions_marked'] if x['state']!='emits_nothing'];print(len(r),'emitter definitions');[print(x['state'].ljust(22), x['label'], x['file']+':'+str(x['start_line']), len(x['opcodes']),'opcodes') for x in r]\""

say "lane 11 done"
