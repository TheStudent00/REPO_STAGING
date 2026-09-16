#!/bin/bash
# sl1 lane 8 -- route (b): the Lean backend over the LEAF modules of the
# subset the compilers target, with the flags log_274 §3 quotes from the
# model's own CMakeLists, the output into the repo (sync-back brings it
# here) so a reader of the emitted Lean can be written against it.
# MEMORY: the brief's bound is 6 GB; log_274 measured this emit at 17 GB
# for I+M alone, so the bound is expected to be passed and is a FLAG,
# not an abort (no cgroup of ours wraps sail); peak RSS is measured and
# printed. Ceiling 7,200 s.
set -u
total=4
export HOME=/work
SL=PseudoCoupHQ/Research/oracle/riscv/sail_lifter
OUT=$SL/lean_emit
W=/work/sl1d
mkdir -p $W
echo "[1/$total] the leaves of the subset"
LEAVES=$(python3 $SL/select_modules.py /sources/sail-riscv/model/riscv.sail_project I M B FD C Zicond Zicsr Zifencei)
echo "leaves: $LEAVES"
sail_riscv_sim --print-default-config > $W/config.json; echo "  config exit: $?"
git -C /sources/sail-riscv rev-parse HEAD > $W/commit.txt; cat $W/commit.txt
echo "[2/$total] sail --lean, timed, peak RSS measured (bound 6 GB stated; breach expected, FLAG)"
rm -rf $OUT; mkdir -p $OUT
cd /sources/sail-riscv/model
S=$(date +%s)
python3 - "$LEAVES" <<'PYEOF'
import resource, subprocess, sys, time
leaves = sys.argv[1].split()
cmd = ["timeout", "7200", "sail", "--project", "riscv.sail_project"] + leaves + ["postlude", "main",
       "--strict-var", "--strict-bitvector", "--strict-exponentials",
       "--memo-z3-path", "/work/sl1_smt_cache", "--memo-z3",
       "--config", "/work/sl1d/config.json", "--lean",
       "--lean-output-dir", "PseudoCoupHQ/Research/oracle/riscv/sail_lifter/lean_emit",
       "--lean-force-output",
       "--lean-non-beq-type", "instruction", "--lean-non-beq-type", "ExecutionResult",
       "--lean-non-beq-type", "Step", "--lean-noncomputable",
       "--lean-noncomputable-function", "encdec_forwards",
       "--lean-noncomputable-function", "encdec_backwards",
       "--lean-noncomputable-function", "encdec_forwards_matches",
       "--lean-noncomputable-function", "encdec_backwards_matches",
       "--lean-noncomputable-function", "encdec_compressed_forwards",
       "--lean-noncomputable-function", "encdec_compressed_backwards",
       "--lean-noncomputable-function", "encdec_compressed_forwards_matches",
       "--lean-noncomputable-function", "encdec_compressed_backwards_matches",
       "--lean-import-file", "../handwritten_support/RiscvExtras.lean",
       "-o", "Sl1Lean"]
print("command:", " ".join(cmd), flush=True)
t = time.time()
rc = subprocess.call(cmd)
peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024.0
print("exit %d, %.0f s, peak RSS of sail %.0f MB (bound 6144 MB, abort name ABORT_MEMORY_SL1 -- a FLAG when passed, the emit is not stopped)" % (rc, time.time() - t, peak), flush=True)
PYEOF
echo "  seconds: $(( $(date +%s) - S ))"
echo "[3/$total] what was written"
cp $W/commit.txt $OUT/SAIL_MODEL_COMMIT.txt 2>/dev/null
find $OUT -type f | wc -l; du -sh $OUT; find $OUT -name '*.lean' | xargs wc -l 2>/dev/null | tail -1
find $OUT -name '*.lean' | head -40
echo "[4/$total] execute clauses in the emit, counted, and one shown LITERAL"
grep -rh '^def execute_' $OUT --include='*.lean' | wc -l
grep -rh '^def execute_' $OUT --include='*.lean' | head -80
F=$(grep -rl '^def execute_' $OUT --include='*.lean' | head -1)
echo "file: $F"; grep -n -m1 -A25 '^def execute_' "$F"
echo "done $(date -u +%FT%TZ)"
