#!/usr/bin/env bash
# ref1 lane 4 -- the twenty-file sample the brief asks for before any bulk
# run: one whole rule file per family the parser must cover, so the grammar
# is written against the objects.  Also the whole register-variant name list,
# written to the artifact folder as NAMES ONLY (no rule text leaves /sources).
set -euo pipefail
S=/sources/X86-64-semantics/semantics
OUT=PseudoCoupHQ/Research/oracle/arch_opcodes/level0
mkdir -p $OUT
total=4

echo "[1/$total] the twenty-file sample, each whole"
i=0
for f in negl_r32 notl_r32 andl_r32_r32 xorl_r32_r32 imull_r32_r32 \
         shll_r32_cl shrl_r32_cl sarl_r32_cl testl_r32_r32 cmpl_r32_r32 \
         movslq_r32_r64 movzbl_r8_r32 setne_r8 seta_r8 cmovel_r32_r32 \
         adcl_r32_r32 sbbl_r32_r32 addq_r64_r64 addw_r16_r16 addb_r8_r8 ; do
    i=$((i+1))
    p=$S/registerInstructions/$f.k
    echo "===== [$i] $f ====="
    if [ -f "$p" ]; then head -c 6000 "$p"; echo; else echo "(absent)"; fi
done

echo "[2/$total] the immediate and one-operand samples"
for f in $S/immediateInstructions/addl_r32_imm32.k $S/immediateInstructions/shll_r32_imm8.k \
         $S/registerInstructions/imull_r32.k $S/registerInstructions/idivl_r32.k \
         $S/registerInstructions/mull_r32.k $S/registerInstructions/incl_r32.k ; do
    echo "===== $(basename $f) ====="
    if [ -f "$f" ]; then head -c 5000 "$f"; echo; else echo "(absent)"; fi
done

echo "[3/$total] every variant name, by folder, written to the artifact folder"
for d in registerInstructions immediateInstructions memoryInstructions systemInstructions mmx pseudoTestInstructions extras; do
    ls $S/$d 2>/dev/null | sed 's/\.k$//' | sed "s|^|$d/|"
done > $OUT/their_variant_names.txt
wc -l $OUT/their_variant_names.txt
head -5 $OUT/their_variant_names.txt

echo "[4/$total] which one-operand register variants exist"
ls $S/registerInstructions | grep -E '^[a-z0-9]+_(r8|r16|r32|r64|rh)\.k$' | head -60
