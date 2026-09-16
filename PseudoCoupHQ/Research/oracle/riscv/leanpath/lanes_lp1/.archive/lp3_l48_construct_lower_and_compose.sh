#!/bin/bash
# lp3_l48_construct_lower_and_compose.sh -- the construction stage on the
# tower: every emulation the construction printed (all readable Sail
# clauses, all variants, all places, four languages, both ways) is
# lowered (compiled, carved), decoded by Sail's own decoder, and its
# expression L composed from the pure forms; NO certificate is run
# (WALK_NO_CERTIFY=1). Then the side-by-side table. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:/opt/cargo/bin:/usr/lib/go-1.26/bin:$PATH
export XDG_CACHE_HOME=/work/cache GOCACHE=/work/gocache GOPATH=/work/gopath GOFLAGS=-mod=mod; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
cd $A
echo "[1/3] the units, split four ways"
python3 - <<'PY'
import json
A="PseudoCoupHQ/Research/oracle/riscv/leanpath"
u=json.load(open(A+"/construct_all/units.json")); print("  units:", len(u))
for k in range(4): json.dump(u[k::4], open("%s/construct_all/units_%d.json" % (A,k), "w"))
PY
echo "[2/3] lowered, decoded, composed; four shards at once; no certificate"
export WALK_JOBS=1 WALK_NO_CERTIFY=1 WALK_MAX_WORDS=400; start=$(date +%s)
for k in 0 1 2 3; do
  ( python3 -u -m leanpath walk $P $X $PLIB $S $A/construct_all/units_$k.json $A/construct_all/walk_$k 300 > $A/construct_all/walk_$k.log 2>&1 ) &
done
wait
echo "  wall seconds=$(( $(date +%s) - start ))"
for k in 0 1 2 3; do echo "  shard $k: $(grep -E "decode:|walk:|Traceback" $A/construct_all/walk_$k.log | tr '\n' ';' | cut -c1-220)"; done
echo "[3/3] the table"
python3 $A/construct_table.py $A/construct_all $A/construct_all/walk_0 $A/construct_all/walk_1 $A/construct_all/walk_2 $A/construct_all/walk_3 > $A/construct_all/table.md 2>&1
head -40 $A/construct_all/table.md | cut -c1-200
echo done
