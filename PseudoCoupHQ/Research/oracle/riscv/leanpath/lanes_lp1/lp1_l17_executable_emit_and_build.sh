#!/bin/bash
# lp1_l17_executable_emit_and_build.sh -- the EXECUTABLE variant of the same
# emit (the model's own CMake target `generated_lean_executable`: the same
# flags minus `--lean-noncomputable*`, with RiscvExtrasExecutable.lean), so
# that Sail's own decoder can be EVALUATED (`#eval`) on a unit's words. The
# proof variant stays the one every theorem is stated in. Fetches nothing
# unless lake insists (packages copied from the built project; said so).
set -uo pipefail
total=5
export OPAMROOT=/persist/opam
export ELAN_HOME=/persist/lp1/elan
export PATH=/persist/opam/default/bin:$ELAN_HOME/bin:/opt/elan/bin:$PATH
SRC=/persist/sail-riscv-6266b40c
CFG=$SRC/build/config/rv64d_v256_e64.json
MODS="I_insts M_insts Zca Zcb Zba Zbb Zbs postlude main"
P=/persist/lp1/Lean_IMZ_exec
echo "[1/$total] tools"; sail --version; ls $SRC/handwritten_support/RiscvExtrasExecutable.lean
echo "[2/$total] the executable emit"
OUT=/work/emit_exec; rm -rf $OUT /work/smtcache2; mkdir -p $OUT; cd $SRC/model
start=$(date +%s)
sail --strict-var --strict-bitvector --strict-exponentials --memo-z3-path /work/smtcache2 \
  --config $CFG --lean --memo-z3 --lean-output-dir $OUT --lean-force-output \
  --lean-non-beq-type instruction --lean-non-beq-type ExecutionResult --lean-non-beq-type Step \
  --lean-import-file ../handwritten_support/RiscvExtrasExecutable.lean -o Lean_IMZ_executable \
  $MODS riscv.sail_project > /work/emit_exec.log 2>&1
rc=$?; echo "  emit rc=$rc seconds=$(( $(date +%s) - start ))"
[ $rc -eq 0 ] || { echo "FLAG: the executable emit failed"; tail -12 /work/emit_exec.log; exit 3; }
ls $OUT; grep -E 'name|rev' $OUT/Lean_IMZ_executable/lakefile.toml; cat $OUT/Lean_IMZ_executable/lean-toolchain
echo "[3/$total] into /persist and build"
rm -rf $P; cp -a $OUT/Lean_IMZ_executable $P; mkdir -p $P/.lake
cp -a /persist/lp1/Lean_IMZ/.lake/packages $P/.lake/ && cp /persist/lp1/Lean_IMZ/lake-manifest.json $P/ && echo "  packages and manifest copied from the proof build"
cd $P; start=$(date +%s); lake build > /work/lake_exec.log 2>&1; rc=$?
echo "  lake rc=$rc seconds=$(( $(date +%s) - start ))"; grep -cE '^error' /work/lake_exec.log | sed 's/^/  error lines: /'; grep -E 'Build completed|error:' /work/lake_exec.log | head -8 | cut -c1-200
grep -qiE 'fetch|clon|download' /work/lake_exec.log && { echo "  FETCHED during lake build (LITERAL):"; grep -iE 'fetch|clon|download' /work/lake_exec.log | head -3; }
echo "[4/$total] can Sail's decoder be evaluated here? one word of the handful, LITERAL"
LIB=$(grep -oE 'name = "Lean[A-Za-z_]*"' $P/lakefile.toml | head -1 | cut -d'"' -f2)
cat > /work/Dec.lean <<L
import $LIB
open Sail Sail.ConcurrencyInterfaceV1 $LIB $LIB.Functions
-- the state the model's own init gives, then Sail's own decoder on one word
#eval (do
  let s0 : SequentialState RegisterType trivialChoiceSource := initState
  match (encdec_backwards (0x02b5453b#32)) s0 with
  | .ok i _ => pure (repr i)
  | .error e _ => pure s!"error {repr e}" : IO String)
L
timeout 600 lake env lean /work/Dec.lean 2>&1 | head -12 | cut -c1-220
echo "[5/$total] the state's own init: is there an initState, and is instruction Repr?"
grep -n "def initState\|initState :" $P/$LIB/*.lean | head -3; grep -n -A1 "^inductive instruction" $P/$LIB/Defs.lean | head -2; grep -n "deriving.*Repr" $P/$LIB/Defs.lean | head -3
echo done
