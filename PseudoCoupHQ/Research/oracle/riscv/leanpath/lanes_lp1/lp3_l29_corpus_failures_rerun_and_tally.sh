#!/bin/bash
# lp3_l29_corpus_failures_rerun_and_tally.sh -- after pass A (lane l28):
# the units its walk left FAILED are walked again with the repaired
# certificate text (the empty simp list of a unit that walks nothing),
# equals runs on those, and the tallies are taken over everything with
# the re-run's rows replacing the failed ones. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:/opt/cargo/bin:/usr/lib/go-1.26/bin:$PATH
export XDG_CACHE_HOME=/work/cache GOCACHE=/work/gocache GOPATH=/work/gopath GOFLAGS=-mod=mod; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
cd $A
echo "[1/4] the failed units of pass A, listed"
python3 - <<'PY'
import json
A="PseudoCoupHQ/Research/oracle/riscv/leanpath"
units={u["name"]:u for k in range(4) for u in json.load(open("%s/corpus_units_%d.json" % (A,k)))}
failed=[r["unit"] for k in range(4) for r in json.load(open("%s/walk_corpus_%d/walk.json" % (A,k)))["rows"] if r["verdict"]=="FAILED"]
json.dump([units[n] for n in failed], open("%s/corpus_units_failed.json" % A,"w"), indent=1); print("  failed units:", len(failed))
PY
echo "[2/4] walked again, four Lean jobs"
export WALK_JOBS=4; start=$(date +%s)
python3 -u -m leanpath walk $P $X $PLIB $S $A/corpus_units_failed.json $A/walk_corpus_fix 300 2>&1 | grep -E "decode:|walk:|FAILED|Traceback" | head -20 | cut -c1-200
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[3/4] equals on the re-run"
start=$(date +%s)
python3 -u -m leanpath equals $P $PLIB $S $A/walk_corpus_fix/walk.json $A/equals_corpus_fix 120 64 2>&1 | grep -E "equals:|Traceback" | tail -2
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[4/4] the tallies over everything"
python3 -m leanpath tally $A/tally_corpus.json $A/walk_corpus_0 $A/walk_corpus_1 $A/walk_corpus_2 $A/walk_corpus_3 $A/walk_corpus_fix -- $A/equals_corpus_0 $A/equals_corpus_1 $A/equals_corpus_2 $A/equals_corpus_3 $A/equals_corpus_fix 2>&1 | cut -c1-200
echo done
