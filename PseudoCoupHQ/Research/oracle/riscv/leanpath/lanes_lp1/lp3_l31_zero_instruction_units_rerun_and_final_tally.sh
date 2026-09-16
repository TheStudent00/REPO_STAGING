#!/bin/bash
# lp3_l31_zero_instruction_units_rerun_and_final_tally.sh -- the 363 units
# that walk no instruction (an identity on the answering register), whose
# certificate lacked the binder of the unknown it names; walked again with
# the repaired text, equals on them, and the final tallies over
# everything (lane l30's equals over the four shards, this re-run
# replacing lane l29's rows). Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:/opt/cargo/bin:/usr/lib/go-1.26/bin:$PATH
export XDG_CACHE_HOME=/work/cache GOCACHE=/work/gocache GOPATH=/work/gopath GOFLAGS=-mod=mod; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
cd $A
echo "[1/3] the 363 walked again, four Lean jobs"
export WALK_JOBS=4; start=$(date +%s)
python3 -u -m leanpath walk $P $X $PLIB $S $A/corpus_units_failed.json $A/walk_corpus_fix2 300 2>&1 | grep -E "decode:|walk:|Traceback" | head -8 | cut -c1-200
python3 - <<'PY'
import json, collections
d=json.load(open("PseudoCoupHQ/Research/oracle/riscv/leanpath/walk_corpus_fix2/walk.json"))
print("  ", d["summary"]); f=[r for r in d["rows"] if r["verdict"]=="FAILED"]
for r in f[:4]: print("   FAILED", r["unit"][:60], r["proposal"][:40], (r["errors"] or [""])[0][-120:])
PY
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[2/3] equals on the re-run"
export EQUALS_JOBS=4 EQUALS_UNIT_BUDGET_S=150; start=$(date +%s)
python3 -u -m leanpath equals $P $PLIB $S $A/walk_corpus_fix2/walk.json $A/equals_corpus_fix2 120 64 2>&1 | grep -E "equals:|Traceback" | tail -2
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[3/3] the final tallies over everything"
python3 -m leanpath tally $A/tally_corpus_final.json $A/walk_corpus_0 $A/walk_corpus_1 $A/walk_corpus_2 $A/walk_corpus_3 $A/walk_corpus_fix2 -- $A/equals_corpus_all_0 $A/equals_corpus_all_1 $A/equals_corpus_all_2 $A/equals_corpus_all_3 $A/equals_corpus_fix2 2>&1 | cut -c1-200
echo done
