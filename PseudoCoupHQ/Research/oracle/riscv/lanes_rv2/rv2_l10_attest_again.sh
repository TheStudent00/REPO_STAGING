#!/usr/bin/env bash
# rv2 lane 10 -- the attestation sweep again, now cross-tabbed against the
# x86 unit store: a probe the x86 build refused is one the corpus's own
# COMPILE-OR-REFUSE gate already recorded as refused, and the question the
# BUILDFAIL count actually raises is whether the riscv64 build refuses the
# SAME probes. This lane answers that with the cross-tab.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
export HOME=/work
export GOCACHE=/work/rv2gocache GOPATH=/work/rv2gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv2attest2
total=2

echo "[1/$total] the sweep: 500 c probes and every go probe"
python3 $RV/rv_attest.py run $OP $RV/attest_rv /work/rv2attest2 500 all

echo "[2/$total] the spelling guard"
python3 $OP/check_no_spelling_keys.py $RV/attest_rv.json
echo "guard rc=$?"
echo "--- lane finished"
