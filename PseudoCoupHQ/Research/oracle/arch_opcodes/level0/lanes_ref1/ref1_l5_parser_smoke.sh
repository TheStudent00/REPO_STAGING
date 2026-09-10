#!/usr/bin/env bash
# ref1 lane 5 -- the parser over the twenty-file sample, and the function
# vocabulary of all 3,098 rule files with the ones the grammar does not know
# named.  Memory bound 6g, named abort ABORT_MEMORY_REF1, peak RSS printed.
set -euo pipefail
S=/sources/X86-64-semantics/semantics
L0=PseudoCoupHQ/Research/oracle/arch_opcodes/level0
total=3

echo "[1/$total] the grammar over the twenty-file sample"
python3 $L0/k_to_z3.py \
  $S/registerInstructions/addl_r32_r32.k \
  $S/registerInstructions/subl_r32_r32.k \
  $S/registerInstructions/andl_r32_r32.k \
  $S/registerInstructions/xorl_r32_r32.k \
  $S/registerInstructions/orl_r32_r32.k \
  $S/registerInstructions/imull_r32_r32.k \
  $S/registerInstructions/negl_r32.k \
  $S/registerInstructions/notl_r32.k \
  $S/registerInstructions/testl_r32_r32.k \
  $S/registerInstructions/cmpl_r32_r32.k \
  $S/registerInstructions/shll_r32_cl.k \
  $S/registerInstructions/shrl_r32_cl.k \
  $S/registerInstructions/sarl_r32_cl.k \
  $S/registerInstructions/setne_r8.k \
  $S/registerInstructions/seta_r8.k \
  $S/registerInstructions/cmovel_r32_r32.k \
  $S/registerInstructions/adcl_r32_r32.k \
  $S/registerInstructions/addq_r64_r64.k \
  $S/registerInstructions/addw_r16_r16.k \
  $S/registerInstructions/addb_r8_r8.k \
  2>&1 | cut -c1-400

echo "[2/$total] the function vocabulary of every rule file, known and not"
python3 $L0/k_to_z3.py --vocabulary $S 2>&1 | tail -160

echo "[3/$total] peak resident memory of this lane"
python3 -c "
import resource
peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024.0
print('peak RSS of the children: %.1f MB' % peak)
if peak > 6144:
    raise SystemExit('ABORT_MEMORY_REF1')
"
