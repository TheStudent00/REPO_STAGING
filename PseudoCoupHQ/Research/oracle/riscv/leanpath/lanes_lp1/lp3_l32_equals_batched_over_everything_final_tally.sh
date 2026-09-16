#!/bin/bash
# lp3_l32_equals_batched_over_everything_final_tally.sh -- equals over
# every certified unit of pass A with round 1 batched into one Lean run
# per unit (every candidate's same-text and integer-level theorems in one
# file) and round 2 (the fixed width) pooled within the unit's budget;
# then the final tallies over everything (the four shards' walks and lane
# l31's re-run of the zero-instruction units). Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
cd $A
echo "[1/3] equals over the four shards, four at a time, two Lean jobs each, 150 s per unit"
export EQUALS_JOBS=2 EQUALS_UNIT_BUDGET_S=150; start=$(date +%s)
for k in 0 1 2 3; do
  ( python3 -u -m leanpath equals $P $PLIB $S $A/walk_corpus_$k/walk.json $A/equals_corpus_b_$k 120 64 > $A/equals_corpus_b_$k.log 2>&1 ) &
done
wait
echo "  wall seconds=$(( $(date +%s) - start ))"
for k in 0 1 2 3; do grep -E "equals:|Traceback" $A/equals_corpus_b_$k.log | tail -2; done
echo "[2/3] equals on the zero-instruction re-run (lane l31's walk), if it is there"
if [ -f $A/walk_corpus_fix2/walk.json ]; then
  export EQUALS_JOBS=4; python3 -u -m leanpath equals $P $PLIB $S $A/walk_corpus_fix2/walk.json $A/equals_corpus_b_fix2 120 64 2>&1 | grep -E "equals:|Traceback" | tail -2
  FIXW=$A/walk_corpus_fix2; FIXE=$A/equals_corpus_b_fix2
else
  echo "  no walk_corpus_fix2/walk.json"; FIXW=""; FIXE=""
fi
echo "[3/3] the final tallies over everything"
python3 -m leanpath tally $A/tally_corpus_final.json $A/walk_corpus_0 $A/walk_corpus_1 $A/walk_corpus_2 $A/walk_corpus_3 $FIXW -- $A/equals_corpus_b_0 $A/equals_corpus_b_1 $A/equals_corpus_b_2 $A/equals_corpus_b_3 $FIXE 2>&1 | cut -c1-200
echo done
