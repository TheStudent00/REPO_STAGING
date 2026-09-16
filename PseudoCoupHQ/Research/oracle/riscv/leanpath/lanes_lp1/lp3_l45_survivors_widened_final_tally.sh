#!/bin/bash
# lp3_l45_survivors_widened_final_tally.sh -- the units whose
# candidates survived the evaluation but were not proved within lane
# l40's budget (constructed adders and shifts, zero-extensions): equals
# again over those only, evaluation first so no prover sees 52 copies of
# a big composite, no budget (each stage keeps its 120 s), four processes
# with two Lean jobs each; then the final tallies over everything, these
# rows replacing lane l40's; lean-sail's helpers now unfold by the index. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
cd $A
echo "[1/3] the survivors, listed and split four ways"
python3 - <<'PY'
import json, glob
A="PseudoCoupHQ/Research/oracle/riscv/leanpath"
walk={}
for k in range(4):
    for r in json.load(open("%s/walk_corpus_%d/walk.json" % (A,k)))["rows"]: walk[r["unit"]]=r
want=[]
for f in sorted(glob.glob("%s/equals_corpus_j_*/equals.json" % A)):
    for r in json.load(open(f))["rows"]:
        if r["proved"]: continue
        if any(x["verdict"] in ("UNDECIDED","NOT_TRIED") for x in r["results"]) and any(x["verdict"]!="REFUTED_BY_EVALUATION" for x in r["results"]):
            want.append(r["unit"])
rows=[walk[u] for u in want if u in walk]
for q in range(4): json.dump({"summary":{}, "rows":rows[q::4]}, open("%s/walk_corpus_survivors2_%d.json" % (A,q),"w"))
print("  units:", len(rows))
PY
echo "[2/3] equals over them, evaluation first, no budget, four processes"
export EQUALS_JOBS=2 EQUALS_UNIT_BUDGET_S=100000 EQUALS_EVAL_FIRST=1; start=$(date +%s)
for q in 0 1 2 3; do
  ( python3 -u -m leanpath equals $P $PLIB $S $A/walk_corpus_survivors2_$q.json $A/equals_corpus_survivors2_$q 120 64 > $A/equals_corpus_survivors2_$q.log 2>&1 ) &
done
wait
echo "  wall seconds=$(( $(date +%s) - start ))"
for q in 0 1 2 3; do grep -E "F over|survive|PROVED|equals:|Traceback" $A/equals_corpus_survivors2_$q.log | cut -c1-140; done
echo "[3/3] the final tallies over everything"
python3 -m leanpath tally $A/tally_corpus_final.json $A/walk_corpus_0 $A/walk_corpus_1 $A/walk_corpus_2 $A/walk_corpus_3 $A/walk_corpus_fix2 -- $A/equals_corpus_j_0_0 $A/equals_corpus_j_0_1 $A/equals_corpus_j_1_0 $A/equals_corpus_j_1_1 $A/equals_corpus_j_2_0 $A/equals_corpus_j_2_1 $A/equals_corpus_j_3_0 $A/equals_corpus_j_3_1 $A/equals_corpus_j_fix2 $A/equals_corpus_survivors2_0 $A/equals_corpus_survivors2_1 $A/equals_corpus_survivors2_2 $A/equals_corpus_survivors2_3 2>&1 | cut -c1-200
echo done
