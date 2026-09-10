#!/usr/bin/env bash
# ref1 lane 9 -- the operand order the file NAME uses against the operand
# order the rule HEAD uses, and what a memory variant's rule looks like, so
# the key map reads the head rather than trusting the name.
set -euo pipefail
S=/sources/X86-64-semantics/semantics
total=3

echo "[1/$total] the head of six variants whose name is asymmetric"
for f in $S/immediateInstructions/addl_r32_imm32.k $S/immediateInstructions/addl_r32_imm8.k \
         $S/registerInstructions/shll_r32_cl.k $S/memoryInstructions/addl_m32_r32.k \
         $S/memoryInstructions/addl_r32_m32.k $S/registerInstructions/imulw_r16_r16.k ; do
    printf '%-28s ' "$(basename $f)"
    grep -o 'execinstr *([^)]*' "$f" | head -1
done

echo "[2/$total] one memory variant whole, both directions"
head -c 3000 $S/memoryInstructions/addl_m32_r32.k; echo
echo "-----"
head -c 3000 $S/memoryInstructions/addl_r32_m32.k; echo

echo "[3/$total] the distinct operand-sort lists the rule heads spell, most common first"
grep -ho 'execinstr *([^)]*)' $S/registerInstructions/*.k $S/immediateInstructions/*.k $S/memoryInstructions/*.k \
  | sed 's/execinstr *(//' | sed 's/[A-Za-z][A-Za-z0-9]*:/V:/g' | sed 's/^[a-z0-9]*[ :]*[A-Za-z]*//' \
  | sort | uniq -c | sort -rn | head -40
