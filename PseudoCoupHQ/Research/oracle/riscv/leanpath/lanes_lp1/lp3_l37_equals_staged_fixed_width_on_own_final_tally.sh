#!/bin/bash
# lp3_l37_equals_staged_fixed_width_on_own_final_tally.sh -- equals over every
# certified unit of pass A, staged: the same text over every candidate in
# one Lean run, the integer level over the unit's own clauses then the
# rest (runs of 12), the fixed width on the own clauses before the rest, within
# 150 s per unit, rfl capped at 10,000 heartbeats, grind at 40,000, 12 candidates per run; eight processes;
# then the final tallies over everything (lane l31's identity units and
# their equals included). Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
cd $A
echo "[1/2] equals, eight processes, one Lean job each, 150 s per unit"
python3 - <<'PY'
import json
A="PseudoCoupHQ/Research/oracle/riscv/leanpath"
for k in range(4):
    d=json.load(open("%s/walk_corpus_%d/walk.json" % (A,k))); rows=[r for r in d["rows"] if r["verdict"]=="CERTIFIED"]
    for h in (0,1):
        json.dump({"summary": d["summary"], "rows": rows[h::2]}, open("%s/walk_corpus_%d_half%d.json" % (A,k,h), "w"))
    print("  shard", k, "certified", len(rows))
PY
export EQUALS_JOBS=1 EQUALS_UNIT_BUDGET_S=150; start=$(date +%s)
for k in 0 1 2 3; do for h in 0 1; do
  ( python3 -u -m leanpath equals $P $PLIB $S $A/walk_corpus_${k}_half$h.json $A/equals_corpus_g_${k}_$h 120 64 > $A/equals_corpus_g_${k}_$h.log 2>&1 ) &
done; done
wait
echo "  wall seconds=$(( $(date +%s) - start ))"
for k in 0 1 2 3; do for h in 0 1; do grep -E "equals:|Traceback" $A/equals_corpus_g_${k}_$h.log | tail -2; done; done
echo "[2/2] the final tallies over everything"
python3 -m leanpath tally $A/tally_corpus_final.json $A/walk_corpus_0 $A/walk_corpus_1 $A/walk_corpus_2 $A/walk_corpus_3 $A/walk_corpus_fix2 -- $A/equals_corpus_g_0_0 $A/equals_corpus_g_0_1 $A/equals_corpus_g_1_0 $A/equals_corpus_g_1_1 $A/equals_corpus_g_2_0 $A/equals_corpus_g_2_1 $A/equals_corpus_g_3_0 $A/equals_corpus_g_3_1 $A/equals_corpus_fix2 2>&1 | cut -c1-200
echo done
