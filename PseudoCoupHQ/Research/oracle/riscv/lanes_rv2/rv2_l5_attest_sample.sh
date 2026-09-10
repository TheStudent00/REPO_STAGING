#!/usr/bin/env bash
# rv2 lane 5 -- the memory SAMPLE the law asks for on the attestation
# sweep: 20 c probes and 20 go probes compiled for riscv64 at the corpus's
# own ship flags, carved, walked by the RISC-V reference, with the peak
# resident printed. Nothing is concluded here; the sample is the bound.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
export HOME=/work
export GOCACHE=/work/rv2gocache GOPATH=/work/rv2gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv2attest
total=2

echo "[1/$total] 20 probes per language"
python3 $RV/rv_attest.py sample $OP $RV/attest_rv_sample /work/rv2attest 20

echo "[2/$total] the spelling guard"
python3 $OP/check_no_spelling_keys.py $RV/attest_rv_sample.json
echo "guard rc=$?"
echo "--- lane finished"
