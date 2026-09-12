#!/bin/bash
# bb2_l4_the_sample_after_the_statement_shape.sh -- task bb2, lane 4:
# the six-cell sample again, after the statement-shape adapter lane 3
# named.  Lane 3's literal: `render_general.assemble`'s `statements`
# are now `(depth, line)` and `bitblast.render_gates` hands it
# `(name, line)`, so every gate render raised
# `TypeError: can only concatenate str (not "int") to str` inside
# `indented`.  The adapter is in `bb2_run.py`, on this task's own side
# of the call; `render_general.py` is task rd1's file and is untouched.
#
#   [1/4] the gate render on one small cell, all five targets, with the
#         statement and line counts -- the check that the adapter is
#         right before three hours of compiling
#   [2/4] the six largest circuits, every place, every target: the
#         sizes and the seconds
#   [3/4] the WORK every interpreted run would ask for, over the whole
#         population, nothing written and nothing run
#   [4/4] peak resident
#
# MEMORY: bound 6 GB resident, named abort ABORT_MEMORY_BB2.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bb2_brief.md
set -u

HQ=PseudoCoupHQ
G="$HQ/Research/oracle/cross_construction/emulation/construct/general"
total=4

i=1
echo "[$i/$total] the gate render on add gpr_gpr 32, all five targets"
timeout 1800 python3 - <<'PY'
import sys, traceback
G = "PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general"
sys.path.insert(0, G)
import bb2_run as BB2
import bitblast as BB
AP = BB2.configure()
import handful as H
import model_table as MTAB
MTAB._install_gpr_widths()
shared = H.build_shared()
cells = AP.read_json(AP.CELLS)
for asked in [("add", "gpr_gpr", 32), ("xor", "gpr_gpr", 8)]:
    for held, place, working, note in BB2.every_place(shared, cells, asked):
        if working is None:
            print("  %s %s %s / %s: %s" % (asked + (place["writes"], note)))
            continue
        ordered = H.renderer_input(working["term"])
        circuit = BB.blast(ordered)
        print("  %s %s %s / %s: %d gates, %d input bits"
              % (asked[0], asked[1], asked[2], place["writes"],
                 len(circuit.gates), len(circuit.inputs)))
        for lang in AP.TARGETS:
            try:
                made = BB.render_gates(circuit, lang, working["families"],
                                       working["home"]["family"],
                                       working["bits"], "probe_%s" % lang,
                                       working.get("text") or "")
                print("    %-6s %d statements, %d source lines"
                      % (lang, made["statements"], made["source_lines"]))
            except Exception:
                print("    %s RAISED:" % lang)
                traceback.print_exc()
PY
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] the six largest circuits, every place, every target"
timeout 14400 python3 "$G/bb2_run.py" sample 6
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] the interpreted work over the whole population"
timeout 3600 python3 "$G/bb2_run.py" interp_sizes
echo "  exit: $?"

i=4
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
