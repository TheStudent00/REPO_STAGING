#!/usr/bin/env bash
# rv2 lane 12 -- THE INHERITANCE. Every preferred proved/agreed
# certificate in the bank whose x86 cell a RISC-V cell twins by TERM: the
# certificate's own SOURCE taken unchanged, compiled for riscv64 at the
# corpus's ship flags, carved, lifted with the RISC-V reference, and gated
# against the same term -- at the cell's own key_width for the headline
# and at the whole written place beside it. Interpreted targets transfer
# as they are and nothing is compiled for them.
# THIS RUN fixes the alignment: lane 11 bound arrival register a<k> to the
# k-th PRINTED SYMBOL of the term, and a certificate's source is a function
# whose k-th ARGUMENT is what matters. The k-th argument is in rdi/rsi/...
# (rax/rbx/... for go) on x86-64 and in a0.. on riscv64, and a float
# argument in xmm0.. and fa0.., so the join is an argument's POSITION.
# Lane 11's 13 DISPROVED rows were that misalignment, not a finding.
set -u
RV=PseudoCoupHQ/Research/oracle/riscv
OP=PseudoCoupHQ/Research/op_pipeline
MODEL=PseudoCoupHQ/Research/oracle/arch_opcodes/model
ORIG=PseudoCoupHQ/Research/oracle/arch_opcodes/level0/ref2_originals
BANK=PseudoCoupHQ/Research/oracle/cross_construction/emulation/autopoly
export HOME=/work
export GOCACHE=/work/rv2gocache GOPATH=/work/rv2gopath
mkdir -p "$GOCACHE" "$GOPATH" /work/rv2inherit
total=3

echo "[1/$total] the plan"
python3 $RV/inherit.py plan $RV/twins.json $BANK/certificates.jsonl \
  $RV/inherit_plan

echo "[2/$total] the run"
python3 $RV/inherit.py run $ORIG $OP $MODEL/model_table_rows.json \
  $RV/twins.json $BANK/certificates.jsonl $BANK \
  $RV/certificates_riscv64 /work/rv2inherit

echo "[3/$total] the spelling guard"
python3 $OP/check_no_spelling_keys.py $RV/inherit_plan.json \
  $RV/certificates_riscv64.json
echo "guard rc=$?"
echo "--- lane finished"
