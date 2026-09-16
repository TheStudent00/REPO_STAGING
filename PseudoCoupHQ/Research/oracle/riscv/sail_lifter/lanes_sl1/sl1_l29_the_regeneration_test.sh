#!/bin/bash
# sl1 lane 29 -- THE REGENERATION TEST (brief section 2 item 4): the
# generated table -- the emit under lean_emit/ -- is copied aside, DELETED,
# and produced again by the same command lane 8 ran; then compared file by
# file: byte-identical, or the diff named. Then the drop-in is walked once
# more over the carved bodies to show the lifter is back.
set -u
export HOME=/work
SL=PseudoCoupHQ/Research/oracle/riscv/sail_lifter
OUT=$SL/lean_emit
W=/work/sl1r
mkdir -p $W
echo "[1/4] the table as it stands, copied aside, then deleted"
rm -rf $W/before; cp -r $OUT $W/before; find $W/before -type f | wc -l
rm -rf $OUT; ls $SL | grep -c lean_emit || echo "lean_emit is gone"
echo "[2/4] the same command as lane 8, again: started $(date -u +%FT%TZ)"
LEAVES=$(python3 $SL/select_modules.py /sources/sail-riscv/model/riscv.sail_project I M B FD C Zicond Zicsr Zifencei)
sail_riscv_sim --print-default-config > $W/config.json
mkdir -p $OUT
cd /sources/sail-riscv/model
S=$(date +%s)
timeout 7200 sail --project riscv.sail_project $LEAVES postlude main --strict-var --strict-bitvector --strict-exponentials --memo-z3-path /work/sl1_smt_cache --memo-z3 --config $W/config.json --lean --lean-output-dir $OUT --lean-force-output --lean-non-beq-type instruction --lean-non-beq-type ExecutionResult --lean-non-beq-type Step --lean-noncomputable --lean-noncomputable-function encdec_forwards --lean-noncomputable-function encdec_backwards --lean-noncomputable-function encdec_forwards_matches --lean-noncomputable-function encdec_backwards_matches --lean-noncomputable-function encdec_compressed_forwards --lean-noncomputable-function encdec_compressed_backwards --lean-noncomputable-function encdec_compressed_forwards_matches --lean-noncomputable-function encdec_compressed_backwards_matches --lean-import-file ../handwritten_support/RiscvExtras.lean -o Sl1Lean > $W/emit.out 2>&1
echo "  exit: $? seconds: $(( $(date +%s) - S ))"
git -C /sources/sail-riscv rev-parse HEAD > $OUT/SAIL_MODEL_COMMIT.txt
echo "[3/4] before against after, file by file"
diff -rq $W/before $OUT && echo "BYTE-IDENTICAL: every file of the emit is the same" || echo "DIFFERS: the files named above"
find $OUT -type f | wc -l; find $OUT -name '*.lean' | xargs cat | sha256sum; find $W/before -name '*.lean' | xargs cat | sha256sum
echo "[4/4] the drop-in over the carved bodies, on the regenerated table"
mkdir -p /work/sl1f/work; export SL1_WORK=/work/sl1f/work
sed -n '/^timeout 1800 python3 - <<.PYEOF.$/,/^PYEOF$/p' $SL/lanes_sl1/sl1_l19_the_drop_in_tuple_fix.sh | sed '1d;$d' > $W/compare.py
timeout 1800 python3 $W/compare.py 2>&1 | grep "^|\|census\|ready" | cut -c1-200
echo "done $(date -u +%FT%TZ)"
