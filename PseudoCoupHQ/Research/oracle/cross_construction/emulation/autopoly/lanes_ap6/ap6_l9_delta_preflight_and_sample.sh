#!/bin/bash
# ap6_l9_delta_preflight_and_sample.sh -- task ap6, lane 9: lane 8 again,
# after the population of setter cells was cut to the pairs the sweep
# actually posed.
#
# WHY LANE 8 IS NOT THE ANSWER.  The corpus attests a setter by `mnem`
# (task m1b's flag-pair rows carry a two-element `produced_by.mnem` and
# nothing else on the setter side), and the sweep gives every mnemonic
# every operand shape it walks, so the join of the two offers cells the
# corpus never recorded before a consumer -- `fucomi imm_xmm_gpr 80`
# before `setne gpr_one 8`.  Lane 8 ran 264 of them for ONE (consumer,
# target) and every one was a refusal by cause with no compile and no
# solver behind it.  Those two causes are properties of the outer set,
# not of a target, so `handful.cell_inputs` now keeps the held cells the
# sweep POSED and `handful.setter_cell_census` states the rest once, by
# cause, over the whole outer set.
#
# NOTHING IS DELETED: lane 8's store is moved beside itself as
# `ap6_delta_runs.jsonl.before_the_setter_cell_filter`, the way every
# earlier superseded store on this folder is kept.
#
# MEMORY: bound 6 GB resident, checked after EVERY run, named abort
# ABORT_MEMORY_AP6; lane 8's 264 runs peaked at 258,668 kB (4% of the
# bound).  CEILINGS: 3,000 ms per gate call, ONE re-pose at 30,000 ms.
#
# Node: hq.research.arch_unit_oracle.cross_construction.autopoly
# Brief: Research/briefs/task_ap6_brief.md
set -u

E=PseudoCoupHQ/Research/oracle/cross_construction/emulation
A=$E/autopoly
H=$E/handful
total=4

i=1
echo "[$i/$total] lane 8's store, moved beside itself"
if [ -f "$A/ap6_delta_runs.jsonl" ]; then
    mv "$A/ap6_delta_runs.jsonl" \
       "$A/ap6_delta_runs.jsonl.before_the_setter_cell_filter"
    echo "  moved: $(wc -l < "$A/ap6_delta_runs.jsonl.before_the_setter_cell_filter") line(s)"
else
    echo "  no store to move"
fi
echo

i=2
echo "[$i/$total] THE SETTER CELL CENSUS over the outer set"
python3 - "$H" "$A" <<'PY'
import sys, json, resource
sys.path.insert(0, sys.argv[1])
sys.path.insert(0, sys.argv[2])
import autopoly as AP
import handful as H
cells = json.load(open(AP.CELLS))
census = H.setter_cell_census(cells)
print("| what | count |")
print("|---|---|")
print("| asked cells that read an arriving flag state | %d |"
      % census["consumers"])
print("| setter cells the corpus attests before them | %d |"
      % census["setter_cells_attested"])
print("| of them, held cells the sweep POSED and the driver builds | %d |"
      % census["held_cells_built"])
print("| of those, at the consumer's own `key_width` | %d |"
      % census["at_the_consumers_own_key_width"])
print("| offered by the join and not posed by the sweep | %d |"
      % sum(census["refused_by_cause"].values()))
print("")
print("| the cause it was not posed | count |")
print("|---|---|")
for cause in sorted(census["refused_by_cause"],
                    key=lambda c: -census["refused_by_cause"][c]):
    print("| %s | %d |" % (cause, census["refused_by_cause"][cause]))
    continue
print("")
held = sorted(census["per_consumer"], key=lambda r: -r["built"])
print("| consumer `mnem` | shape | `key_width` | held cells |")
print("|---|---|---|---|")
for row in held[:12]:
    print("| `%s` | %s | %s | %d |"
          % (row["mnem"], row["shape"], row["key_width"],
             row["built"] + 1))
    continue
print("")
print("peak resident: %d kB"
      % resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)
PY
echo

i=3
echo "[$i/$total] THE PLAN of the delta pass"
python3 "$A/autopoly.py" --pass ap6_delta --bank preflight
echo

i=4
echo "[$i/$total] THE MEMORY SAMPLE: the first 40 runs of the delta"
python3 "$A/autopoly.py" --pass ap6_delta --bank run 40
echo
echo "lane done"
