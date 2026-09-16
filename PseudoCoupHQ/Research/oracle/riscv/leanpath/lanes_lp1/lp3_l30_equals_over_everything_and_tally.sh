#!/bin/bash
# lp3_l30_equals_over_everything_and_tally.sh -- equals over every
# certified unit of pass A (the four shards; lane l29 covers the re-run
# of the failures) with the two-round, pooled equals; then the tallies
# over everything. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
cd $A
echo "[1/2] equals over the four shards, four at a time, two Lean jobs each, 150 s per unit"
export EQUALS_JOBS=2 EQUALS_UNIT_BUDGET_S=150; start=$(date +%s)
for k in 0 1 2 3; do
  ( python3 -u -m leanpath equals $P $PLIB $S $A/walk_corpus_$k/walk.json $A/equals_corpus_all_$k 120 64 > $A/equals_corpus_all_$k.log 2>&1 ) &
done
wait
echo "  wall seconds=$(( $(date +%s) - start ))"
for k in 0 1 2 3; do grep -E "equals:|Traceback" $A/equals_corpus_all_$k.log | tail -2; done
echo "[2/2] the tallies over everything"
python3 -m leanpath tally $A/tally_corpus_all.json $A/walk_corpus_0 $A/walk_corpus_1 $A/walk_corpus_2 $A/walk_corpus_3 $A/walk_corpus_fix -- $A/equals_corpus_all_0 $A/equals_corpus_all_1 $A/equals_corpus_all_2 $A/equals_corpus_all_3 $A/equals_corpus_fix 2>&1 | cut -c1-200
echo done
