#!/bin/bash
# lp3_l28_pass_a_four_languages.sh -- pass A over the rendered corpus in
# all four languages (1,960 sources, both routes). The handful first as
# the gate (the alias unfold, the unfolding rule, the job pool);
# then equals on the handful as the probe of the integer level with
# Sail's helpers unfolded; then four shards walked concurrently; then
# equals with the first proof stopping; then the tallies. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:/opt/cargo/bin:/usr/lib/go-1.26/bin:$PATH
export XDG_CACHE_HOME=/work/cache GOCACHE=/work/gocache GOPATH=/work/gopath GOFLAGS=-mod=mod; mkdir -p /work/cache
X=/work/Lean_IM_pr_exec; A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
SRC=PseudoCoupHQ/Research/oracle/cross_construction/emulation/construct/general/emulations_riscv64
cd $A
echo "[0/5] resources: $(nproc) cores; $(free -g | awk '/Mem:/{print $2" GB, "$7" GB available"}'); work free $(df -h /work | awk 'NR==2{print $4}')"
echo "[1/5] the gate: the handful with the register-index rule, 4 Lean jobs"
export WALK_JOBS=4; W=$A/walk_handful_all_v10; start=$(date +%s)
python3 -u -m leanpath walk $P $X $PLIB $S $A/handful_units.json $W 600 2>&1 | grep -vE "^\s*$" | tail -24 | cut -c1-200
echo "  wall seconds=$(( $(date +%s) - start ))"
python3 - <<PY
import json; d=json.load(open("$W/walk.json")); f=[r["unit"] for r in d["rows"] if r["verdict"]=="FAILED"]; print("  gate: failed", f, "certified", d["summary"]["certified"]); raise SystemExit(1 if f else 0)
PY
[ $? -eq 0 ] || { echo "FLAG: the gate did not pass; the corpus is not walked"; exit 3; }
echo "[2/5] equals on the handful, the first proof stopping, Sail's helpers unfolded at the integer level"
start=$(date +%s); E=$A/equals_handful_all_v10
python3 -u -m leanpath equals $P $PLIB $S $W/walk.json $E 120 64 2>&1 | grep -E "scanned|F over|PROVED|equals:" | cut -c1-170
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[3/5] the corpus, four languages, four shards walked concurrently (two Lean jobs each)"
python3 -m leanpath corpus $SRC $A/corpus_units 4
export WALK_JOBS=2; start=$(date +%s)
for k in 0 1 2 3; do
  ( python3 -u -m leanpath walk $P $X $PLIB $S $A/corpus_units_$k.json $A/walk_corpus_$k 300 > $A/walk_corpus_$k.log 2>&1 ) &
done
wait
echo "  wall seconds=$(( $(date +%s) - start ))"
for k in 0 1 2 3; do echo "  shard $k:"; grep -E "decode:|register expr|walk:|Traceback|Error" $A/walk_corpus_$k.log | tail -5 | cut -c1-200; done
echo "[4/5] equals over every certified unit, the first proof stopping, four shards concurrently"
start=$(date +%s)
for k in 0 1 2 3; do
  ( python3 -u -m leanpath equals $P $PLIB $S $A/walk_corpus_$k/walk.json $A/equals_corpus_$k 120 64 > $A/equals_corpus_$k.log 2>&1 ) &
done
wait
echo "  wall seconds=$(( $(date +%s) - start ))"
for k in 0 1 2 3; do grep -E "equals:|Traceback" $A/equals_corpus_$k.log | tail -2; done
echo "[5/5] the tallies"
python3 - <<'PY'
import json, collections, re
A="PseudoCoupHQ/Research/oracle/riscv/leanpath"
rows=[]
for k in range(4): rows += json.load(open("%s/walk_corpus_%d/walk.json" % (A,k)))["rows"]
print("units", len(rows)); print("verdicts", collections.Counter(r["verdict"] for r in rows).most_common())
why=collections.Counter(re.sub(r"\d+", "N", (r.get("why") or "")[:64]) for r in rows if r["verdict"]=="REFUSED"); print("refusals:"); [print("  %5d  %s" % (n,w)) for w,n in why.most_common(16)]
by=collections.Counter((r["cell_display"].split("(")[1].rstrip(")") if r.get("cell_display") else "?", r["verdict"]) for r in rows)
print("by language/route:"); [print("  %-28s %-10s %d" % (k[0],k[1],n)) for k,n in sorted(by.items())]
cells=collections.defaultdict(list)
for r in rows:
    if r["verdict"]=="CERTIFIED": cells[r["cell_display"].split(" (")[0]].append(r["proposal"])
print("certified cells", len(cells))
for c in sorted(cells): print("  %-32s %d  %s" % (c, len(cells[c]), cells[c][0][:100]))
fails=[r for r in rows if r["verdict"]=="FAILED"]; print("failed:", len(fails)); [print("  %-60s %s | %s" % (r["unit"][:60], r["proposal"][:60], (r["errors"] or [""])[0][-90:])) for r in fails[:24]]
eq=[]
for k in range(4):
    try: eq += json.load(open("%s/equals_corpus_%d/equals.json" % (A,k)))["rows"]
    except Exception as ex: print("equals shard", k, ex)
print("equals units", len(eq), "with a proved definition", sum(1 for r in eq if r["proved"]))
print("stages", collections.Counter(p[2] for r in eq for p in r["proved"][:1]).most_common())
print("definitions proved:", collections.Counter(p[0] for r in eq for p in r["proved"][:1]).most_common(40))
print("unproved units:"); [print("  %-60s %s" % (r["unit"][:60], r["proposal"][:80])) for r in eq if not r["proved"]][:30]
PY
echo done
