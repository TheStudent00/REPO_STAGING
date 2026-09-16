#!/bin/bash
# lp3_l38_equals_evaluate_then_prove_final_tally.sh -- equals over every
# certified unit of pass A, testing before proving: one Lean run evaluates
# the proposal and every candidate on four sample inputs, and only the
# survivors go to the provers (the same text by with_reducible rfl, the
# integer level, the fixed width) within 150 s per unit; eight processes;
# then the final tallies over everything. A probe of #eval on the proof
# emit comes first. Fetches nothing.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath; P=/work/proof
PLIB=$(grep -A1 '\[\[lean_lib\]\]' $P/lakefile.toml | grep -oE 'name = "[^"]+"' | head -1 | cut -d'"' -f2)
S=$A/strip_6266b40c_8eb1fb6b_all_v5/strip.json
cd $A
echo "[0/3] the probe: does the proof emit evaluate?"
f=$(ls $A/equals_corpus_g_3_0/Equals_*same_text*.lean | head -1)
python3 - "$f" > /work/Eval_probe.lean <<'PY'
import sys, re; t=open(sys.argv[1]).read()
i=t.index("set_option linter.unusedVariables false"); j=t.rindex("set_option maxHeartbeats 10000 in")
head=t[:j]; tail=t[t.index("end Functions"):]
print(head); print('#eval IO.println s!"E probe {repr (pure_RTYPE 3#64 5#64 rop.ADD)}"'); print(tail)
PY
cd $P; timeout 300 lake env lean /work/Eval_probe.lean 2>&1 | grep -E "^E probe|error" | head -3; cd $A
echo "[1/3] equals, eight processes, 150 s per unit"
export EQUALS_JOBS=1 EQUALS_UNIT_BUDGET_S=150; start=$(date +%s)
for k in 0 1 2 3; do for h in 0 1; do
  ( python3 -u -m leanpath equals $P $PLIB $S $A/walk_corpus_${k}_half$h.json $A/equals_corpus_h_${k}_$h 120 64 > $A/equals_corpus_h_${k}_$h.log 2>&1 ) &
done; done
wait
echo "  wall seconds=$(( $(date +%s) - start ))"
for k in 0 1 2 3; do for h in 0 1; do grep -E "equals:|Traceback" $A/equals_corpus_h_${k}_$h.log | tail -2; done; done
echo "[2/3] equals on the identity units, the same way"
export EQUALS_JOBS=2; start=$(date +%s)
python3 -u -m leanpath equals $P $PLIB $S $A/walk_corpus_fix2/walk.json $A/equals_corpus_h_fix2 120 64 2>&1 | grep -E "equals:|Traceback" | tail -2
echo "  wall seconds=$(( $(date +%s) - start ))"
echo "[3/3] the final tallies over everything"
python3 -m leanpath tally $A/tally_corpus_final.json $A/walk_corpus_0 $A/walk_corpus_1 $A/walk_corpus_2 $A/walk_corpus_3 $A/walk_corpus_fix2 -- $A/equals_corpus_h_0_0 $A/equals_corpus_h_0_1 $A/equals_corpus_h_1_0 $A/equals_corpus_h_1_1 $A/equals_corpus_h_2_0 $A/equals_corpus_h_2_1 $A/equals_corpus_h_3_0 $A/equals_corpus_h_3_1 $A/equals_corpus_h_fix2 2>&1 | cut -c1-200
echo done
