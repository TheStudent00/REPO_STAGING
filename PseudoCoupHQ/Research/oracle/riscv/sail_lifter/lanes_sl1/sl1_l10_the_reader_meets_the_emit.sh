#!/bin/bash
# sl1 lane 10 -- the reader's parser over the real emit (lane 8's): how
# many definitions parse, which do not and why (LITERAL), what the
# execute clauses' parameters and register accesses look like, and three
# execute definitions quoted whole. No evaluation yet: the grammar first.
set -u
total=4
export HOME=/work
SL=PseudoCoupHQ/Research/oracle/riscv/sail_lifter
E=$SL/lean_emit
echo "[1/$total] the emit on disk"
find $E -name '*.lean' | wc -l; du -sh $E; cat $E/SAIL_MODEL_COMMIT.txt 2>/dev/null
find $E -name '*.lean' | head -30
echo "[2/$total] the parser over every file"
timeout 900 python3 $SL/lean_reader.py $E 2>&1 | head -120
echo "[3/$total] register access and the monad, LITERAL"
grep -rn -m3 'def rX\b\|def rX ' $E --include='*.lean' | head; F=$(grep -rl 'def rX ' $E --include='*.lean' | head -1); echo "file: $F"; grep -n -A45 '^def rX ' "$F" | head -60
grep -rn -A14 '^def wX ' $E --include='*.lean' | head -30
grep -rn -A6 '^def rX_bits\|^def wX_bits\|^def regidx_to_regno\|^def creg2reg_idx' $E --include='*.lean' | head -40
grep -rn 'readReg\|writeReg' $E --include='*.lean' | head -8
grep -rn -B2 -A3 'def regidx\|abbrev regidx\|structure regidx\|inductive regidx\|def regno\|abbrev regno' $E --include='*.lean' | head -30
head -30 "$F"
echo "[4/$total] three execute definitions, LITERAL, and the encdec backwards head"
F2=$(grep -rl '^def execute_' $E --include='*.lean' | head -1); echo "file: $F2"
grep -n '^def execute_' "$F2" | head -80
awk '/^def execute_RTYPE /,/^def [a-zA-Z_]+ .*(:=|:)$/ {print}' "$F2" | head -60
awk '/^def execute_SHIFTIOP /,/^$/' "$F2" | head -40
awk '/^def execute_LOAD /,/^$/' "$F2" | head -60
grep -rn -A40 '^def encdec_backwards ' $E --include='*.lean' | head -60
grep -rn -A12 '^def encdec_compressed_backwards ' $E --include='*.lean' | head -16
grep -rn -c '^def ' $E --include='*.lean' | sort -t: -k2 -n | tail -8
echo "done $(date -u +%FT%TZ)"
