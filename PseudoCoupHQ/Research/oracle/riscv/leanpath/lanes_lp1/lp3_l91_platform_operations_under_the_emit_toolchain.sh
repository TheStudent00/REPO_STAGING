#!/bin/bash
# lp3_l90_platform_operations_under_the_emit_toolchain.sh -- the eight PLATFORM
# operations (the reservation four, the terminal two, the random bits, the
# experimental flag) checked under the emit's OWN Lean, and the two questions
# that stand between them and an end-to-end LR/SC.
#
# WHAT ALREADY HOLDS, on the host, and is only being re-checked here under a
# different toolchain: lp1_harness/leanpath_src/Platform.lean elaborates with no
# error and no warning, its 53 self-checks all pass, and `#print axioms` on all
# 43 of its theorems names nothing beyond Lean's own propext / Quot.sound -- no
# `sorry`, no `native_decide`, no `partial`. That was measured with Lean v4.34.0
# and again with v4.30.0. The emit is built with v4.29.0, which is what step 1
# measures.
#
# THE TWO QUESTIONS, which need the built emit and so cannot be asked on the host:
#
#   (a) `match_reservation : Arch.pa → Bool` compares addresses, so the binding
#       needs `DecidableEq Arch.pa`. The emit's `Arch` instance sets
#       `pa := BitVec (if 64 = 32 then 34 else 64)` (LeanIM/Defs.lean:2003), so it
#       should be there -- step 3 asks Lean, rather than assuming.
#
#   (b) The four state-bearing operations need the platform state to be reachable
#       from `SailM`. `SailM = PreSailM RegisterType trivialChoiceSource exception`
#       and its state is the register file; the Sail source says outright that the
#       reservation "is maintained external to the model" (sys/sys_reservation.sail
#       :11-13), which in C++ is a mutable field on the model object. Step 4 reads
#       what lean-sail's state actually holds, and step 5 asks the one question
#       that settles the binding: can `SailM` lift `IO`? If it can, an `IO.Ref`
#       carrying a `Platform.Plat` gives `MonadPlat SailM Arch.pa` in four lines
#       and the eight emit signatures are satisfied as written. If it cannot, the
#       report has to say which of the three resolutions in Platform.lean section 4
#       the harness must take instead.
#
# Touches nothing: /work/proof is only READ (lake env, which builds nothing, and a
# grep of its Sail package), /work/proof_float is not touched at all, the cache is
# not touched, and nothing under SOURCES/sail-riscv is touched. Fetches nothing.
# Writes only $G. Seconds, not minutes.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan; export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
SRC=$A/lp1_harness/leanpath_src
P=/work/proof
G=$A/runs/platform_ops
total=5
rm -rf $G; mkdir -p $G; t0=$(date +%s)

echo "[1/$total] Platform.lean under the emit's own toolchain  ($(( $(date +%s) - t0 ))s)"
TC=$(cat $A/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules/lean-toolchain)
echo "  the emit's toolchain: $TC"
cp $SRC/Platform.lean $G/Platform.lean
(cd $G && timeout 900 elan run "$TC" lean -M 4096 -t 200000 Platform.lean > $G/platform.log 2>&1); rc=$?
echo "  lean rc=$rc  errors=$(grep -c ': error' $G/platform.log)  warnings=$(grep -c ': warning' $G/platform.log)"
grep -E ': error|: warning' $G/platform.log | head -10 | cut -c1-220 | sed 's/^/  /'
echo "  the self-checks, group by group:"
grep -E '^==|-- [0-9]+/[0-9]+ ok|FAIL' $G/platform.log | sed 's/^/    /'

echo "[2/$total] nothing here rests on an axiom  ($(( $(date +%s) - t0 ))s)"
echo "  theorems audited: $(grep -c 'depends on axioms\|does not depend on any axioms' $G/platform.log)"
echo "  any sorryAx: $(grep -c 'sorryAx' $G/platform.log)   any native_decide: $(grep -c 'Lean.ofReduceBool' $G/platform.log)"
grep 'sorryAx\|ofReduceBool' $G/platform.log | head -5 | sed 's/^/  FLAG: /'
# Every line of the source mentioning one of the four forbidden words is PRINTED,
# not counted: the file's own prose says it uses none of them, so a bare count
# would read as three hits when all three are that sentence. A hit is real only
# if the line is code.
echo "  every line of the source naming one of the four (all of these should be prose):"
grep -nE '\bsorry\b|\badmit\b|native_decide|(^|[^_a-zA-Z])partial ' $SRC/Platform.lean | cut -c1-160 | sed 's/^/    /'

echo "[3/$total] question (a): is the address type comparable in the emit  ($(( $(date +%s) - t0 ))s)"
[ -f $P/.lake/build/lib/lean/LeanIM/Defs.olean ] || { echo "  FLAG: /work/proof is not built -- steps 3 to 5 need it"; echo done; exit 0; }
cat > $G/addr_probe.lean <<'EOF'
import LeanIM
open Sail
open LeanIM
#check (inferInstance : DecidableEq (Arch.pa))
#check (inferInstance : BEq (Arch.pa))
#reduce (Arch.pa)
#check @load_reservation
#check @match_reservation
#check @plat_term_write
EOF
(cd $P && timeout 900 lake env lean $G/addr_probe.lean > $G/addr_probe.log 2>&1); rc=$?
echo "  lean rc=$rc  errors=$(grep -c ': error' $G/addr_probe.log)"
cut -c1-220 $G/addr_probe.log | head -20 | sed 's/^/  /'

echo "[4/$total] question (b), first half: what SailM's state actually holds  ($(( $(date +%s) - t0 ))s)"
SP=$(ls -d $P/.lake/packages/Sail 2>/dev/null)
if [ -z "$SP" ]; then echo "  FLAG: no Sail package under $P/.lake/packages"; else
  echo "  the package: $SP"
  grep -rn "structure SequentialState\|abbrev PreSailM\|def PreSailM\|structure RegisterRef\|choiceState\|sailOutput" $SP --include=*.lean | head -12 | cut -c1-200 | sed 's/^/  /'
fi

echo "[5/$total] question (b), second half: can SailM lift IO  ($(( $(date +%s) - t0 ))s)"
cat > $G/monad_probe.lean <<'EOF'
import LeanIM
open Sail
open LeanIM
-- If THIS elaborates, the whole binding of the four state-bearing operations is
-- four lines: an IO.Ref holding a Platform.Plat, and a MonadPlat instance whose
-- getPlat / setPlat lift the ref's get / set. Nothing in the emit changes.
#check (inferInstance : MonadLiftT IO SailM)
-- and if not this, then whether the state is reachable directly
#check (inferInstance : MonadStateOf (SequentialState RegisterType trivialChoiceSource) SailM)
#print SailM
EOF
(cd $P && timeout 900 lake env lean $G/monad_probe.lean > $G/monad_probe.log 2>&1); rc=$?
echo "  lean rc=$rc  errors=$(grep -c ': error' $G/monad_probe.log)"
cut -c1-220 $G/monad_probe.log | head -24 | sed 's/^/  /'
echo "  VERDICT on the IO lift: $(grep -q 'MonadLiftT IO SailM' $G/monad_probe.log && echo 'see the line above -- an error on that #check means NO' || echo 'no error reported for it -- the lift is available')"

echo "wall seconds=$(( $(date +%s) - t0 ))"
echo done
