#!/bin/bash
# ap6_l7_which_setter_cells_compose.sh -- task ap6, lane 7.
#
# WHAT THIS LANE DOES: lane 6 showed that the outer set carries no
# cell-granular flag-pair attestation on the SETTER side -- m1b records
# a setter by `mnem` and the sweep's own rows give that mnemonic its
# cells -- so the population of setter cells the driver can be asked
# about is the join of those two readings, 2,901 held cells against the
# 253 the loop walked.  This lane asks, for every one of them, whether
# the driver can BUILD the held cell at all: `handful.cell_input` with
# the setter cell stated does the whole composition except the render,
# the compile and the gate, and it either answers a held cell or
# refuses BY CAUSE.  It costs no compiler and no solver.
#
# WHY IT MATTERS: a held cell that refuses at the composition is a
# result the loop can record without running anything, and one that
# builds is a run.  This is what says how large the loop becomes, which
# is the thing to know BEFORE a pass is submitted.
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_AP6, checked
# per consumer cell.  Nothing here forks.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_ap6_brief.md
set -u

E=PseudoCoupHQ/Research/oracle/cross_construction/emulation
A=$E/autopoly
H=$E/handful
total=1

echo "[1/$total] every attested setter cell of every consumer, built"
python3 - "$H" "$A" <<'PY'
import sys, json, collections, resource
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2])
BOUND = 6 * 1024 * 1024


def check(where):
    peak = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if peak > BOUND:
        raise SystemExit("ABORT_MEMORY_AP6: %d kB at %s" % (peak, where))
    return peak


import autopoly as AP
import handful as H
cells = json.load(open(AP.CELLS))
causes = collections.Counter()
built = 0
asked_total = 0
per = []
same_width = 0
for record in cells["asked"]:
    asked = (record["asked"]["mnem"], record["asked"]["shape"],
             record["asked"]["key_width"])
    first = H.cell_input(cells, asked)
    if first.get("setter") is None:
        continue
    wanted = H.attested_setter_cells(cells, asked)
    here_built = 0
    for entry in wanted:
        asked_total = asked_total + 1
        held = H.cell_input(cells, asked, entry)
        if held.get("refusal_cause") is not None:
            causes[held["refusal_cause"]] += 1
            continue
        built = built + 1
        here_built = here_built + 1
        if entry["key_width"] == asked[2]:
            same_width = same_width + 1
        continue
    per.append((here_built, len(wanted), asked))
    check("consumer %s" % (asked,))
    continue
per.sort(reverse=True)
print("| what | count |")
print("|---|---|")
print("| attested setter cells asked about, over every consumer | %d |"
      % asked_total)
print("| of them, held cells the driver BUILDS | %d |" % built)
print("| of those, at the consumer's own `key_width` | %d |" % same_width)
print("| refused at the composition, by cause | %d |"
      % sum(causes.values()))
print("")
print("| the cause | count |")
print("|---|---|")
for cause, count in causes.most_common():
    print("| %s | %d |" % (cause, count))
    continue
print("")
print("| consumer `mnem` | shape | `key_width` | built | asked |")
print("|---|---|---|---|---|")
for here, many, asked in per[:20]:
    print("| `%s` | %s | %s | %d | %d |"
          % (asked[0], asked[1], asked[2], here, many))
    continue
print("")
print("peak resident: %d kB" % check("done"))
PY
echo
echo "lane done"
