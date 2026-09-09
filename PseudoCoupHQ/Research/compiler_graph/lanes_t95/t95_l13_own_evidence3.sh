#!/usr/bin/env bash
# t95 lane 13 -- more of log_200's claims turned from ATTRIBUTIONS into
# things that RE-RUN. Read-only, container paths only.
#
# Node: hq.research.compiler_graph.graph, heading "the arch-opcode-node".
# Convention: hq.conventions. Lane t95_l12 scored log_200 at 11 MATCHES /
# 0 DIFFERS / 13 UNVERIFIABLE, and most of the 13 were LITERALS quoted
# from lane logs, which live outside the sandbox. Every one of them can
# be re-derived from an artifact or from the pinned source instead, and
# that is what this lane prints.
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
set -u
run() { echo; echo "\$ $*"; eval "$@" 2>&1; }
say() { echo; echo "======== $* ========"; }
G=PseudoCoupGraphs
L=PseudoCoupHQ/Research/compiler_graph/lanes_t95

say "[1/8] go -- the seven declarations of the arch opcode type, and each role"
run "python3 $L/t95_show.py declarations go"

say "[2/8] rust and swift -- the whole-checkout search for an instruction emitter"
run "grep -rl --include='*.rs' --include='*.cpp' --include='*.h' -e 'BuildMI(' -e 'MCInst' -e 'MachineInstr' -e 'X86::' /sources/rust | wc -l"
run "grep -rl --include='*.cpp' --include='*.h' -e 'BuildMI(' -e 'MCInst' -e 'MachineInstr' -e 'X86::' /sources/swift-6.0.3-RELEASE | wc -l"

say "[3/8] swift -- the one line where the compiler spells an instruction, from the pin"
run "git -C /sources/swift-6.0.3-RELEASE show 6a862d2eb7128ff1f317b07e8ad1a6da939775f3:lib/IRGen/IRGenSIL.cpp | sed -n '5571,5580p'"

say "[4/8] go -- the emitter, from the pin"
run "git -C /sources/golang_src show 9f1012d9a1aa0831ff44ac9c767e96f9943d13fe:src/cmd/compile/internal/ssagen/ssa.go | sed -n '6742,6743p'"
run "git -C /sources/golang_src show 9f1012d9a1aa0831ff44ac9c767e96f9943d13fe:src/cmd/compile/internal/ssa/opGen.go | sed -n '115435p'"

say "[5/8] the shrink, as a table"
run "python3 $L/t95_show.py shrink"

say "[6/8] the reasons a site could not be named, per region"
run "python3 $L/t95_show.py reasons"

say "[7/8] the cost of each pass, and the co-location count"
run "python3 $L/t95_show.py cost"

say "[8/8] the .td named frontier, quoted from the cpp artifact"
run "python3 $L/t95_show.py frontier"
run "python3 $L/t95_show.py emitterfiles go"

say "lane 13 done"
