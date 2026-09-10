#!/usr/bin/env bash
# rv2 lane 7 -- THE PLAN of the inheritance, and nothing run: which banked
# certificates have an x86 cell a RISC-V cell twins, per target and per
# kind, with the bank's sha256 so the population is dated.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
BANK=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
export HOME=/work
total=2

echo "[1/$total] the plan"
python3 $RV/inherit.py plan $RV/twins.json $BANK/certificates.jsonl \
  $RV/inherit_plan

echo "[2/$total] the spelling guard"
python3 $OP/check_no_spelling_keys.py $RV/inherit_plan.json
echo "guard rc=$?"
echo "--- lane finished"
