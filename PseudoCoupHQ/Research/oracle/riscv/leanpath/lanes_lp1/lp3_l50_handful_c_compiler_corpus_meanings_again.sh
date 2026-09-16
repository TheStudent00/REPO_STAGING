#!/bin/bash
# lp3_l50_handful_c_compiler_corpus_meanings_again.sh -- the l49 run again,
# with `library_refs` no longer listing a type or namespace (`Sail.Vector`)
# among the definitions to unfold, which failed every certificate of l49.
# Plan node
# hq.research.lean_proof_path_resistant_to_churn.the_run.handful, step 1:
# c's compiler_corpus (EVERY compiler-operator of c, function-wrapped:
# the 750 probes of the operator pipeline's manifest) compiled at the
# corpus's own ship flags for riscv64 (Language.compile), each body cut
# out at its symbol, decoded word by word by Sail's own decoder, its
# meaning composed from Sail's definitions and certified in Lean
# (ArchUnit.meaning). Four shards at once. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:/opt/cargo/bin:/usr/lib/go-1.26/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
R=$A/runs/handful_c
cd $A
echo "[0/2] the proof project: where lean-sail lives (the library index reads .lake/packages)"
grep -nE "require|path|git" $P/lakefile.toml | head -6; ls $P/.lake/packages 2>&1 | head -4
rm -rf $R/walk_[0-3] $R/walk_[0-3].log
echo "[1/2] the units, split four ways"
python3 - <<'PY'
import json
R="PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/handful_c"
u=json.load(open(R+"/units.json")); print("  units:", len(u))
for k in range(4): json.dump(u[k::4], open("%s/units_%d.json" % (R,k), "w"))
PY
echo "[2/2] compile, carve, decode, compose, certify; four shards at once"
export WALK_JOBS=1 WALK_MAX_WORDS=400; start=$(date +%s)
for k in 0 1 2 3; do
  ( python3 -u -m leanpath walk $P $X $PLIB $S $R/units_$k.json $R/walk_$k 600 > $R/walk_$k.log 2>&1 ) &
done
wait
echo "  wall seconds=$(( $(date +%s) - start ))"
for k in 0 1 2 3; do echo "  shard $k: $(grep -E "decode:|walk:|Traceback" $R/walk_$k.log | tr '\n' ';' | cut -c1-220)"; done
python3 - <<'PY'
import json, collections
R="PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/handful_c"
c = collections.Counter()
for k in range(4):
    try: rows = json.load(open("%s/walk_%d/walk.json" % (R, k)))["rows"]
    except Exception as e: print("  shard", k, "no walk.json:", e); continue
    for r in rows: c[(r["verdict"], (r.get("why") or "")[:60])] += 1
for v, n in c.most_common(12): print("  %5d  %s" % (n, v))
PY
echo done
