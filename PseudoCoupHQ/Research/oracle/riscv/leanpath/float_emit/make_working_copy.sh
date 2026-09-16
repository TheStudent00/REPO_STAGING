#!/bin/bash
# make_working_copy.sh <check|build> -- the WORKING COPY of the emit in which
# Sail's float axioms get their bodies from Kinds.lean. Never the cache; never
# /work/proof: /work/proof is only READ (its built lean-sail package and its
# built emit are copied, after the emit is checked byte-identical to the cache's,
# so the working copy starts from the same build and rebuilds only what the
# rewrite touches).
#
#   check  the copy, the rewrite, the two kinds modules built, and the rewritten
#          RiscvExtras.lean checked as ONE file against the copied build
#   build  the same copy and rewrite, then the whole project built (timed), then
#          one file that imports the model and asks Lean what the rewritten
#          constants are
#
# Prints [i/n]; writes /work/proof_float and float_emit/RiscvExtras_working_copy.diff.
# Fetches nothing.
set -uo pipefail
MODE=${1:?check or build}
LP=PseudoCoupHQ/Research/oracle/riscv/leanpath
CACHE=$LP/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules
KS=$LP/lp1_harness/leanpath_src
HERE=$LP/float_emit
SRC=/work/proof
W=/work/proof_float
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
total=5
t0=$(date +%s)

echo "[1/$total] free space, and the build to copy is the cache's emit"
df -h /work | tail -1 | awk '{print "  /work: "$4" free of "$2}'
diff -rq $CACHE/LeanIM $SRC/LeanIM > /dev/null \
  && echo "  /work/proof/LeanIM is byte-identical to the cache's LeanIM (read only)" \
  || { echo "FLAG: /work/proof/LeanIM differs from the cache's emit"; exit 3; }
du -sh $SRC/.lake | awk '{print "  the built package and emit to copy: "$1}'

echo "[2/$total] the working copy at $W"
rm -rf $W; mkdir -p $W/kinds_src
cp -a $CACHE/LeanIM $CACHE/LeanIM.lean $CACHE/lean-toolchain $W/
cp $SRC/lake-manifest.json $W/
cp -a $SRC/.lake $W/.lake
cp $KS/Universal.lean $KS/Kinds.lean $W/kinds_src/
cat > $W/lakefile.toml <<'EOF'
name = "Lean_IM"
defaultTargets = ["LeanIM"]
moreLeanArgs = ["--tstack=400000"]

[[lean_lib]]
name = "LeanIM"
leanOptions.weak.linter.style.nameCheck = false
moreLeancArgs= ["-fbracket-depth=500"]

[[lean_lib]]
name = "KindsLib"
srcDir = "kinds_src"
roots = ["Universal", "Kinds"]

[[require]]
name = "Sail"
git = "https://github.com/rems-project/lean-sail"
rev = "v5"
EOF
du -sh $W | awk '{print "  working copy: "$1}'

echo "[3/$total] the rewrite: the axioms whose name and type Kinds.Axioms defines get that body"
python3 $HERE/rewrite_axioms.py --cache-extras $CACHE/LeanIM/RiscvExtras.lean \
  --work-extras $W/LeanIM/RiscvExtras.lean --kinds $W/kinds_src/Kinds.lean \
  --diff-out $HERE/RiscvExtras_working_copy.diff || exit 3
echo "  diff lines: $(grep -c '^[-+]axiom \|^[-+]def ' $HERE/RiscvExtras_working_copy.diff) changed, $(grep -c '^+import' $HERE/RiscvExtras_working_copy.diff) import added"
cmp -s $CACHE/LeanIM/RiscvExtras.lean $W/LeanIM/RiscvExtras.lean && echo "FLAG: the working copy was not rewritten" || echo "  the cache's RiscvExtras.lean untouched: $(md5sum < $CACHE/LeanIM/RiscvExtras.lean | cut -c1-12)"

if [ "$MODE" = check ]; then
  echo "[4/$total] the kinds modules built in the working copy"
  (cd $W && timeout 900 lake build KindsLib > $W/lake_kinds.log 2>&1); rc=$?
  echo "  lake rc=$rc"; grep -E -- "-- [0-9]+/[0-9]+ ok|FAIL|error" $W/lake_kinds.log | head -14 | sed 's/^/  /'
  [ $rc -eq 0 ] || { tail -20 $W/lake_kinds.log; exit 3; }
  echo "[5/$total] the rewritten RiscvExtras.lean checked as one file against the copied build"
  s=$(date +%s); (cd $W && timeout 900 lake env lean LeanIM/RiscvExtras.lean > $W/extras_check.log 2>&1); rc=$?
  echo "  lean rc=$rc seconds=$(( $(date +%s) - s )); error lines: $(grep -c 'error' $W/extras_check.log)"
  grep 'error' $W/extras_check.log | head -10 | cut -c1-240
else
  echo "[4/$total] the whole working copy built (timed)"
  s=$(date +%s); (cd $W && timeout 3000 lake build > $W/lake_build.log 2>&1); rc=$?
  echo "  lake rc=$rc seconds=$(( $(date +%s) - s )); error lines: $(grep -c '^error' $W/lake_build.log)"
  grep -E "Build completed|^error" $W/lake_build.log | head -8 | cut -c1-240
  echo "  modules rebuilt: $(grep -c '^✔ \[\|Built ' $W/lake_build.log)"
  [ $rc -eq 0 ] || { tail -30 $W/lake_build.log | cut -c1-240; exit 3; }
  echo "[5/$total] what Lean says the rewritten constants are, importing the whole model"
  cat > $W/FloatBodies.lean <<'EOF'
import LeanIM
open LeanIM
#print axioms riscv_f64Add
#print axioms riscv_f32Lt
#eval riscv_f64Add 0#3 0x3FF0000000000000#64 0x4000000000000000#64
#eval riscv_f32Lt 0x3F800000#32 0x40000000#32
#check @riscv_f64MulAdd
EOF
  s=$(date +%s); (cd $W && timeout 900 lake env lean FloatBodies.lean > $W/float_bodies.log 2>&1); rc=$?
  echo "  lean rc=$rc seconds=$(( $(date +%s) - s ))"
  cut -c1-240 $W/float_bodies.log | head -20 | sed 's/^/  /'
fi
echo "wall seconds=$(( $(date +%s) - t0 ))"
echo done
