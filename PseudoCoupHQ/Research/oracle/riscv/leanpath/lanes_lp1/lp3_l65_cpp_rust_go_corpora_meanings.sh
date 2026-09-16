#!/bin/bash
# lp3_l65_cpp_rust_go_corpora_meanings.sh -- plan node
# hq.research.lean_proof_path_resistant_to_churn.language.compiler_corpus for
# cpp, rust and go: EVERY compiler-operator of each (the operator pipeline's
# manifests), compiled at the corpus's own ship flags for riscv64, each body
# cut out at its symbol, decoded by Sail's decoder, its meaning composed from
# Sail's definitions and certified in Lean. One language after another, four
# shards each. the owner, 2026-09-15: "run it". Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:/opt/cargo/bin:/usr/lib/go-1.26/bin:$PATH
export XDG_CACHE_HOME=/work/cache GOCACHE=/work/gocache GOPATH=/work/gopath GOFLAGS=-mod=mod; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
cd $A; t0=$(date +%s); i=0
for lang in cpp rust go; do
  i=$((i+1)); R=$A/runs/corpus_$lang; rm -rf $R/walk_[0-3] $R/walk_[0-3].log
  echo "[$i/3] $lang: $(python3 -c "import json; print(len(json.load(open('$R/units.json'))))") probes; compile, carve, decode, compose, certify; four shards  ($(( $(date +%s) - t0 ))s)"
  python3 - <<PY
import json
R="$R"; u=json.load(open(R+"/units.json"))
for k in range(4): json.dump(u[k::4], open("%s/units_%d.json" % (R,k), "w"))
PY
  export WALK_JOBS=1 WALK_MAX_WORDS=400
  for k in 0 1 2 3; do
    ( python3 -u -m leanpath walk $P $X $PLIB $S $R/units_$k.json $R/walk_$k 600 > $R/walk_$k.log 2>&1 ) &
  done
  wait
  echo "  $lang: certified $(cat $R/walk_[0-3].log | grep -c CERTIFIED), refused $(cat $R/walk_[0-3].log | grep -c REFUSED), failed $(cat $R/walk_[0-3].log | grep -c FAILED)  ($(( $(date +%s) - t0 ))s)"
  cat $R/walk_[0-3].log | grep REFUSED | sed -E 's/^ +[^ ]+ +REFUSED +//' | sed -E 's/[0-9]+/N/g' | cut -c1-60 | sort | uniq -c | sort -rn | head -4
done
echo "wall seconds=$(( $(date +%s) - t0 ))"
echo done
