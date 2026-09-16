#!/bin/bash
# lp3_l1_reduce_decode_probe.sh -- can Lean's kernel evaluate Sail's decoder
# on one word in the PROOF build, with no compiled code? (#reduce on the
# decoder applied to the state the model's own init gives.) The cost per
# word is the measurement; a readable term is the proposal. Read-only
# volume; writes only under /work.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
P=/persist/lp1/Lean_IM_6266b40c_all; cd $P
echo "[1/3] the state by init, then #reduce of one 32-bit word (divw), timed"
cat > /work/R1.lean <<'L'
import LeanIM
open Sail Sail.ConcurrencyInterfaceV1 PreSail LeanIM LeanIM.Functions
set_option maxHeartbeats 1000000000
set_option maxRecDepth 1000000
noncomputable section
def blank : SequentialState RegisterType trivialChoiceSource :=
  { regs := ∅, choiceState := (), mem := ∅, tags := (), cycleCount := 0, sailOutput := #[] }
def s0 : SequentialState RegisterType trivialChoiceSource :=
  match (do sail_model_init (); init_model "") blank with | .ok _ s => s | .error _ s => s
set_option pp.maxSteps 100000
#reduce (match (encdec_backwards (0x02b5453b#32)) s0 with | .ok i _ => some i | .error _ _ => none)
L
start=$(date +%s); timeout 1500 lake env lean /work/R1.lean > /work/R1.out 2>&1; rc=$?
echo "  rc=$rc seconds=$(( $(date +%s) - start )) lines=$(wc -l < /work/R1.out)"; head -c 1500 /work/R1.out; echo
echo "[2/3] the same with `decide`-style: is the reduced term a constructor application? (grep)"
grep -oE "instruction\.[A-Z_a-z0-9]+" /work/R1.out | head -3
echo "[3/3] a 16-bit word (c.add), timed"
sed 's/encdec_backwards (0x02b5453b#32)/encdec_compressed_backwards (0x952e#16)/' /work/R1.lean > /work/R2.lean
start=$(date +%s); timeout 1500 lake env lean /work/R2.lean > /work/R2.out 2>&1; rc=$?
echo "  rc=$rc seconds=$(( $(date +%s) - start )) lines=$(wc -l < /work/R2.out)"; head -c 800 /work/R2.out; echo
echo done
