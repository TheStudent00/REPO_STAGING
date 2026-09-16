#!/bin/bash
# run_level0.sh <gate|full> <scratch dir> <result prefix>
#
# LEVEL 0 for the bodies Kinds.lean gives Sail's float axioms: every
# operation with a body, every rounding mode, result bits AND the five flag
# bits, against Sail's own softfloat -- the C++ wrapper the model's
# simulator links (c_emulator/riscv_softfloat.cpp, as compiled in the built
# tree) over Berkeley SoftFloat 3 with the RISCV specialization.
#
# Called by `podman exec` for the gate (a small run read first) and by a lane
# for the full run. Writes the scratch under <scratch dir> and the two result
# files <prefix>.json / <prefix>.md beside this script. Fetches nothing.
set -uo pipefail
MODE=${1:?gate or full}; W=${2:?scratch dir}; PREFIX=${3:?result prefix}
HERE=PseudoCoupHQ/Research/oracle/riscv/leanpath/softfloat_level0
LP=PseudoCoupHQ/Research/oracle/riscv/leanpath
CACHE=$LP/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules
KS=$LP/lp1_harness/leanpath_src
MODEL=/persist/sail-riscv-6266b40c
SF=/opt/sail-riscv-src
OBJ=$SF/build/c_emulator/CMakeFiles/riscv_model.dir/riscv_softfloat.cpp.o
LIBSF=$SF/build/dependencies/softfloat/libsoftfloat.a
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
total=7
rm -rf "$W"; mkdir -p "$W"
t0=$(date +%s)

echo "[1/$total] Sail's softfloat: the built tree's sources against the emit's model commit, byte for byte"
for f in c_emulator/riscv_softfloat.cpp c_emulator/riscv_softfloat.h; do
  cmp -s $MODEL/$f $SF/$f && echo "  identical: $f" || echo "  DIFFERS: $f"
done
diff -rq $MODEL/dependencies/softfloat $SF/dependencies/softfloat > /dev/null \
  && echo "  identical: dependencies/softfloat (berkeley-softfloat-3 sources and the model's CMake for it)" \
  || echo "  DIFFERS: dependencies/softfloat"
echo "  model commit of the emit: $(git -C $MODEL rev-parse --short=8 HEAD 2>/dev/null); of the built tree: $(git -C $SF rev-parse --short=8 HEAD 2>/dev/null)"
grep -n "init_detectTininess\|define defaultNaNF64UI" $SF/dependencies/softfloat/berkeley-softfloat-3/source/RISCV/specialize.h | sed 's/^/  specialization: /'
ls -la $OBJ $LIBSF | awk '{print "  object: "$5" bytes "$NF}'

echo "[2/$total] the operations, from the texts"
python3 $HERE/gen.py --extras $CACHE/LeanIM/RiscvExtras.lean --kinds $KS/Kinds.lean \
  --sail $MODEL/model/core/softfloat_interface.sail --out "$W" || exit 3

echo "[3/$total] the points ($MODE)"
python3 $HERE/points.py --ops "$W/ops.json" --mode "$MODE" --out "$W/points.txt" --tags "$W/tags.txt" || exit 3

echo "[4/$total] the SoftFloat side: the generated harness against Sail's own header, linked with Sail's compiled object"
INC=$(grep '^CXX_INCLUDES' $SF/build/c_emulator/CMakeFiles/riscv_model.dir/flags.make | cut -d= -f2-)
g++ -O2 -std=gnu++17 $INC "$W/harness.cpp" $OBJ $LIBSF -o "$W/sf_harness" > "$W/gxx.log" 2>&1; rc=$?
echo "  g++ rc=$rc"
[ $rc -eq 0 ] || { head -30 "$W/gxx.log"; exit 3; }

echo "[5/$total] the Lean side: the repo's Universal.lean and Kinds.lean, the generated FloatCheck.lean, one executable"
mkdir -p "$W/lean/src"
cp $KS/Universal.lean $KS/Kinds.lean "$W/FloatCheck.lean" "$W/lean/src/"
cp $CACHE/lean-toolchain "$W/lean/"
cat > "$W/lean/lakefile.toml" <<'EOF'
name = "floatcheck"
defaultTargets = ["floatcheck"]

[[lean_lib]]
name = "KindsLib"
srcDir = "src"
roots = ["Universal", "Kinds"]

[[lean_exe]]
name = "floatcheck"
srcDir = "src"
root = "FloatCheck"
EOF
echo "  toolchain: $(cat $W/lean/lean-toolchain)"
(cd "$W/lean" && timeout 1500 lake build floatcheck > "$W/lake.log" 2>&1); rc=$?
echo "  lake rc=$rc"
grep -E -- "-- [0-9]+/[0-9]+ ok|FAIL" "$W/lake.log" | sed 's/^/  Kinds.lean own checks: /' | head -20
[ $rc -eq 0 ] || { grep -E "error" "$W/lake.log" | head -20; tail -20 "$W/lake.log"; exit 3; }

echo "[6/$total] both over the same $(wc -l < "$W/points.txt") points"
python3 - "$W" <<'PY'
import resource, subprocess, sys, time
W = sys.argv[1]
for label, exe, out in (("softfloat", W + "/sf_harness", W + "/sf_out.txt"),
                        ("lean", W + "/lean/.lake/build/bin/floatcheck", W + "/lean_out.txt")):
    t = time.time()
    rc = subprocess.run([exe], stdin=open(W + "/points.txt"), stdout=open(out, "w")).returncode
    print("  %s rc=%d ms=%d  peak RSS of the harnesses so far: %.1f MB" % (
        label, rc, (time.time() - t) * 1000, resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss / 1024.0))
PY
echo "  lines: points $(wc -l < "$W/points.txt"), softfloat $(wc -l < "$W/sf_out.txt"), lean $(wc -l < "$W/lean_out.txt")"

echo "[7/$total] compare"
python3 $HERE/compare.py --ops "$W/ops.json" --points "$W/points.txt" --tags "$W/tags.txt" \
  --sf "$W/sf_out.txt" --lean "$W/lean_out.txt" --json "$HERE/$PREFIX.json" --md "$HERE/$PREFIX.md" || exit 3
python3 PseudoCoupHQ/Research/op_pipeline/check_no_spelling_keys.py "$HERE/$PREFIX.json" 2>&1 | tail -1
head -45 "$HERE/$PREFIX.md"
echo "wall seconds=$(( $(date +%s) - t0 ))"
echo done
