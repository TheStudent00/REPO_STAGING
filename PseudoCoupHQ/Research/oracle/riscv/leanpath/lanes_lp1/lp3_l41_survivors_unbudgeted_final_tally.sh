#!/bin/bash
# lp3_l41_survivors_unbudgeted_final_tally.sh -- the units of pass A whose
# candidates survived the evaluation but were not proved within the
# budget (the constructed adders among them): equals again over those
# units only, with no budget (each stage keeps its own 120 s), two Lean
# jobs; then the final tallies over everything, these rows replacing
# lane l40's for the same units. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
cd $A
echo "[1/3] the units that survived evaluation without a proof, listed"
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
json.dump({"summary":{}, "rows":rows}, open("%s/walk_corpus_survivors.json" % A,"w"))
print("  units:", len(rows)); [print("   ", u[:70]) for u in want[:40]]
PY
echo "[2/3] equals over them, no budget, two Lean jobs"
export EQUALS_JOBS=2 EQUALS_UNIT_BUDGET_S=100000; start=$(date +%s)
python3 -u -m leanpath equals $P $PLIB $S $A/walk_corpus_survivors.json $A/equals_corpus_survivors 120 64 2>&1 | grep -E "F over|survive|PROVED|equals:|Traceback" | cut -c1-150
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[3/3] the final tallies over everything"
python3 -m leanpath tally $A/tally_corpus_final.json $A/walk_corpus_0 $A/walk_corpus_1 $A/walk_corpus_2 $A/walk_corpus_3 $A/walk_corpus_fix2 -- $A/equals_corpus_j_0_0 $A/equals_corpus_j_0_1 $A/equals_corpus_j_1_0 $A/equals_corpus_j_1_1 $A/equals_corpus_j_2_0 $A/equals_corpus_j_2_1 $A/equals_corpus_j_3_0 $A/equals_corpus_j_3_1 $A/equals_corpus_j_fix2 $A/equals_corpus_survivors 2>&1 | cut -c1-200
echo done
