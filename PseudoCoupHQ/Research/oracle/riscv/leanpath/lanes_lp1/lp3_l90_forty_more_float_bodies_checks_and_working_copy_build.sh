#!/bin/bash
# lp3_l90_forty_more_float_bodies_checks_and_working_copy_build.sh -- the forty
# float axioms that had no body now have one, so this lane re-runs the two
# things that only the container can say:
#
#   1  Kinds.lean's own checks under the EMIT'S toolchain (lean-toolchain
#      v4.29.0). They were written and run on the laptop's v4.30.0, where
#      Universal.lean's `sailToBitsTruncate_eq_ofInt` does not compile -- the
#      `simpa` closing it wants v4.29.0's `Int.toNat` simp set -- so the laptop
#      run carried a one-line scratch patch to that proof and NOTHING else. Here
#      the file is the repo's, unpatched, on the toolchain it was written for.
#   2  the LEVEL-0 gate, unchanged: the 27 operations whose shapes the level-0
#      harness knows, against Sail's own softfloat, as a regression guard that
#      the forty additions disturbed none of them. gen.py refuses the forty --
#      their type shapes (three operands; one operand with a different result
#      width; one operand and a Bool) are three the harness does not yet call --
#      so the gate's denominator is still 27 of 67. The forty were checked on the
#      laptop instead, against a Berkeley SoftFloat 3 built from the model's own
#      `dependencies/softfloat` sources with the model's own CMake flags and the
#      RISCV specialization: 11,239,890 points, every operation, every rounding
#      mode, result bits and all five flag bits, 0 disagreements.
#   3  the WORKING COPY of the emit built whole, with all 67 float axioms given
#      bodies (it was 27). `make_working_copy.sh build` prints its own five
#      steps and ends by asking Lean, over the imported model, what the
#      rewritten constants are -- `#print axioms riscv_f64Add` naming no axiom
#      is the statement that the body is really the model's.
#
# Never the cache, never /work/proof. Fetches nothing. Step 3 took 489 s when it
# rewrote 27; step 2's gate is minutes.
set -uo pipefail
LP=PseudoCoupHQ/Research/oracle/riscv/leanpath
KS=$LP/lp1_harness/leanpath_src
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
total=3
t0=$(date +%s)

echo "[1/$total] Kinds.lean's own checks, on the emit's toolchain, the file unpatched"
W=/work/kinds_checks_l90
rm -rf $W; mkdir -p $W/src
cp $KS/Universal.lean $KS/Kinds.lean $W/src/
cp $LP/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules/lean-toolchain $W/
cat > $W/lakefile.toml <<'EOF'
name = "kindschecks"
defaultTargets = ["KindsLib"]

[[lean_lib]]
name = "KindsLib"
srcDir = "src"
roots = ["Universal", "Kinds"]
EOF
echo "  toolchain: $(cat $W/lean-toolchain)"
echo "  bodies in Kinds.Axioms: $(sed -n '/^namespace Axioms$/,/^end Axioms$/p' $KS/Kinds.lean | grep -c '^def ')"
s=$(date +%s); (cd $W && timeout 900 lake build KindsLib > $W/lake.log 2>&1); rc=$?
echo "  lake rc=$rc seconds=$(( $(date +%s) - s ))"
grep -E -- "^info: .*== |-- [0-9]+/[0-9]+ ok|FAIL|error" $W/lake.log | cut -c1-200 | sed 's/^/  /'
awk '/-- [0-9]+\/[0-9]+ ok/ { n=split($0,a,"-- "); split(a[n],b,"/"); g++; got+=b[1]+0; sub(/ ok.*/,"",b[2]); want+=b[2]+0 }
     END { printf("  %d check groups, %d of %d ok\n", g, got, want) }' $W/lake.log
[ $rc -eq 0 ] || { tail -30 $W/lake.log | cut -c1-240; exit 3; }

echo "[2/$total] the level-0 gate, unchanged, as a regression guard on the 27"
bash $LP/softfloat_level0/run_level0.sh gate /work/sf_level0_gate_l90 gate_level0_after_forty

echo "[3/$total] the working copy with all 67 bodies, built whole (make_working_copy.sh prints its own five steps)"
bash $LP/float_emit/make_working_copy.sh build

echo "wall seconds=$(( $(date +%s) - t0 ))"
echo done
