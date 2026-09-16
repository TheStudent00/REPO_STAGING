#!/bin/bash
# lp3_l22_pass_a_c_cpp.sh -- pass A over the rendered corpus, c and cpp
# (980 sources, both routes): the handful first as the gate (the alias
# unfold, the job pool), then four shards walked concurrently, then
# equals with the first proof stopping, then the tallies. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
SRC=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/emulations_riscv64
cd $A
echo "[0/4] resources: $(nproc) cores; $(free -g | awk '/Mem:/{print $2" GB, "$7" GB available"}'); work free $(df -h /work | awk 'NR==2{print $4}')"
echo "[1/4] the gate: the handful again with the alias unfold, 4 Lean jobs"
export WALK_JOBS=4; W=$A/walk_handful_all_v6; start=$(date +%s)
python3 -u -m leanpath walk $P $X $PLIB $S $A/handful_units.json $W 600 2>&1 | grep -vE "^\s*$" | tail -24 | cut -c1-200
echo "  wall seconds=$(( $(date +%s) - start ))"
python3 - <<PY
import json; d=json.load(open("$W/walk.json")); f=[r["unit"] for r in d["rows"] if r["verdict"]=="FAILED"]; print("  gate: failed", f, "certified", d["summary"]["certified"]); raise SystemExit(1 if f else 0)
PY
[ $? -eq 0 ] || { echo "FLAG: the gate did not pass; the corpus is not walked"; exit 3; }
echo "[2/4] the corpus, c and cpp, four shards walked concurrently (one Lean job each)"
python3 -m leanpath corpus $SRC $A/corpus_units_c_cpp 4 c,cpp
export WALK_JOBS=1; start=$(date +%s)
for k in 0 1 2 3; do
  ( python3 -u -m leanpath walk $P $X $PLIB $S $A/corpus_units_c_cpp_$k.json $A/walk_corpus_c_cpp_$k 600 > $A/walk_corpus_c_cpp_$k.log 2>&1 ) &
done
wait
echo "  wall seconds=$(( $(date +%s) - start ))"
for k in 0 1 2 3; do echo "  shard $k:"; grep -E "decode:|register expr|walk:|Traceback|Error" $A/walk_corpus_c_cpp_$k.log | tail -5 | cut -c1-200; done
echo "[3/4] equals over every certified unit, the first proof stopping, four shards concurrently"
start=$(date +%s)
for k in 0 1 2 3; do
  ( python3 -u -m leanpath equals $P $PLIB $S $A/walk_corpus_c_cpp_$k/walk.json $A/equals_corpus_c_cpp_$k 120 64 > $A/equals_corpus_c_cpp_$k.log 2>&1 ) &
done
wait
echo "  wall seconds=$(( $(date +%s) - start ))"
for k in 0 1 2 3; do grep -E "equals:|Traceback" $A/equals_corpus_c_cpp_$k.log | tail -2; done
echo "[4/4] the tallies"
python3 - <<'PY'
import json, collections, re
A="PseudoCoupHQ/Research/oracle/riscv/leanpath"
rows=[]; 
for k in range(4): rows += json.load(open("%s/walk_corpus_c_cpp_%d/walk.json" % (A,k)))["rows"]
print("units", len(rows)); print("verdicts", collections.Counter(r["verdict"] for r in rows).most_common())
why=collections.Counter(re.sub(r"\d+", "N", (r.get("why") or "")[:60]) for r in rows if r["verdict"]=="REFUSED"); print("refusals:"); [print("  %5d  %s" % (n,w)) for w,n in why.most_common(14)]
by=collections.Counter((r["cell_display"].split("(")[1].rstrip(")") if r.get("cell_display") else "?", r["verdict"]) for r in rows)
print("by language/route:"); [print("  %-28s %-10s %d" % (k[0],k[1],n)) for k,n in sorted(by.items())]
cells=collections.defaultdict(list)
for r in rows:
    if r["verdict"]=="CERTIFIED": cells[r["cell_display"].split(" (")[0]].append(r["proposal"])
print("certified cells", len(cells)); 
for c in sorted(cells)[:60]: print("  %-32s %d  %s" % (c, len(cells[c]), cells[c][0][:100]))
fails=[r for r in rows if r["verdict"]=="FAILED"]; print("failed:"); [print("  %-60s %s | %s" % (r["unit"][:60], r["proposal"][:60], (r["errors"] or [""])[0][-90:])) for r in fails[:20]]
eq=[]; 
for k in range(4):
    try: eq += json.load(open("%s/equals_corpus_c_cpp_%d/equals.json" % (A,k)))["rows"]
    except Exception as ex: print("equals shard", k, ex)
print("equals units", len(eq), "with a proved definition", sum(1 for r in eq if r["proved"]))
print("stages", collections.Counter(p[2] for r in eq for p in r["proved"][:1]).most_common())
print("definitions proved:", collections.Counter(p[0] for r in eq for p in r["proved"][:1]).most_common(40))
PY
echo done
