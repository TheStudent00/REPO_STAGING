#!/bin/bash
# bb2_l3_the_gate_render_refusal_named.sh -- task bb2, lane 3: lane 2
# recorded "the gate render refused" on every one of its 60 attempts,
# at every size and on every target, INCLUDING a place whose circuit is
# zero gates.  A refusal that is universal is a defect in this task's
# own machinery and not a finding about any cell, so this lane asks the
# same call for its own words and the frame it came from.
#
#   [1/3] two cells, both ends of the size distribution, with the
#         refusal LITERAL and the frame it was raised in
#   [2/3] the same call by hand, with the whole traceback
#   [3/3] peak resident
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_bb2_brief.md
set -u

HQ=PseudoCoupHQ
G="$HQ/Research/oracle/cross_construction/emulation/construct/general"
total=3

i=1
echo "[$i/$total] the sample over ONE cell, the refusal named"
timeout 1800 python3 "$G/bb2_run.py" sample 1
echo "  exit: $?"

i=2
echo ""
echo "[$i/$total] the same call by hand, whole traceback, on a small cell"
timeout 1800 python3 - <<'PY'
import os, sys, traceback
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
asked = ("add", "gpr_gpr", 32)
for held, place, working, note in BB2.every_place(shared, cells, asked):
    if working is None:
        print("  %s: %s" % (place["writes"], note))
        continue
    print("  place %s, %s bits, home %s, families %s"
          % (place["writes"], working.get("bits"),
             working["home"], working["families"]))
    ordered = H.renderer_input(working["term"])
    circuit = BB.blast(ordered)
    print("    gates: %d, input bits: %d" % (len(circuit.gates),
                                             len(circuit.inputs)))
    for lang in AP.TARGETS:
        try:
            made = BB.render_gates(circuit, lang, working["families"],
                                   working["home"]["family"],
                                   working["bits"], "probe_%s" % lang,
                                   working.get("text") or "")
            print("    %s: %d statements, %d source lines"
                  % (lang, made["statements"], made["source_lines"]))
        except Exception as problem:
            print("    %s RAISED:" % lang)
            traceback.print_exc()
    break
PY
echo "  exit: $?"

i=3
echo ""
echo "[$i/$total] peak resident of the lane's own shell"
python3 -c "import resource; print('peak resident: %d kB' % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)"
echo "done"
