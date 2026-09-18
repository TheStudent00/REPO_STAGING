#!/bin/bash
# rv1_l17_the_same_507_with_the_arrival_promises.sh
#
# l15 put all 507 units' riscv64 bodies against their own x86-64 bodies and
# got 184 DIFFER -- 36% of the corpus. That number is not believable as it
# stands and this lane says why, then measures it.
#
# THE COMPARISON l15 MADE. Both terms take their arguments as FREE 64-bit
# symbols. So the solver may put anything in the top half of a register that
# holds a 32-bit argument, and the counterexamples say exactly that:
#
#   c/op_0   !a   arg0 = 1946437878141681664     (high bits set)
#   c/op_103 a+b  arg0 = 2147483648              (0x80000000, the sign bit)
#   c/op_108 a+b  arg1 = 2147483648
#
# Neither compiler was answering that question. riscv64's psABI says a 32-bit
# integer arrives SIGN-extended; x86-64 SysV leaves the high half unspecified,
# so an x86 body may read it as garbage while the riscv body may not. Compare
# them over inputs the ABI forbids and they differ -- truthfully, and about a
# situation that cannot occur.
#
# This is the SAME distinction the Lean path hit independently, log 294
# section 2.3: every `plain` counterexample there was a high-bit input, and at
# the `abi` statement seven of ten proved with none false. Two different
# machines -- z3 over disassembly here, bv_decide over Sail there -- finding
# the same thing is worth more than either alone.
#
# WHAT THIS LANE DOES. The identical 507 units, the identical bodies, the one
# change being `assume-abi`: a 32-bit signed argument is the sign-extension of
# its low half, a 32-bit unsigned the zero-extension, a bool is 0 or 1, a
# 64-bit argument carries no promise and gets none. Then the two runs are put
# side by side, per unit, so every move is named.
#
# The default is still OFF, so l15 and the rv1 run of record both reproduce
# unchanged.
#
# Reads l15's output. Writes $RV/xarch/claim_abi* only. Budget: twenty minutes.
set -uo pipefail
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
R=PseudoCoupHQ
OP=$R/Research/op_pipeline
RV=$R/Research/oracle/riscv
OUT=$RV/xarch
t0=$(date +%s)
for f in $OUT/units_all.json $OUT/carved_all.json $OUT/claim_all.json; do
  [ -f "$f" ] || { echo "FLAG: missing $f -- rv1_l15 is the lane that writes it"; exit 3; }
done
grep -q "def abi_assumptions" $RV/claim_check.py || { echo "FLAG: claim_check.py has no abi_assumptions; the laptop copy did not reach here"; exit 3; }

echo "[1/3] the promises this assumes, printed before use  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import sys
sys.path.insert(0, "PseudoCoupHQ/Research/oracle/riscv")
import claim_check as C
print("  32-bit signed   ->", "arg == SignExt(32, low 32)")
print("  32-bit unsigned ->", "arg == ZeroExt(32, low 32)")
print("  bool            ->", "arg <=u 1")
print("  64-bit          ->", "no promise, no assumption")
print("  named signed:", sorted(C.NARROW_SIGNED))
print("  named unsigned:", sorted(C.NARROW_UNSIGNED))
PY

echo "[2/3] the same 507, with the promises  ($(( $(date +%s) - t0 ))s)"
python3 -u $RV/claim_check.py $OP $OUT/units_all.json $OUT/carved_all.json \
        $OUT/claim_abi assume-abi > $OUT/claim_abi.log 2>&1
echo "  rc=$?  units walked: $(grep -c '^\[' $OUT/claim_abi.log)"
head -1 $OUT/claim_abi.log | sed 's/^/  /'
[ -f $OUT/claim_abi.json ] || { echo "  FLAG: no claim_abi.json"; exit 3; }

echo "[3/3] the two runs side by side  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import json, collections
O = "PseudoCoupHQ/Research/oracle/riscv/xarch"
free = {r["unit"]: r for r in json.load(open(O + "/claim_all.json"))["rows"] if r.get("unit")}
abi  = {r["unit"]: r for r in json.load(open(O + "/claim_abi.json"))["rows"] if r.get("unit")}
ta = collections.Counter(r["outcome"] for r in abi.values())
tf = collections.Counter(r["outcome"] for r in free.values())
keys = sorted(set(list(tf) + list(ta)))
print("  %-28s %8s %8s" % ("outcome", "free", "abi"))
for k in keys:
    print("  %-28s %8d %8d" % (k, tf.get(k, 0), ta.get(k, 0)))

moved = [u for u in abi if free.get(u, {}).get("outcome") == "DIFFER"
         and abi[u]["outcome"] in ("EQUAL_BY_Z3", "IDENTICAL_AFTER_NORMALIZE")]
still = [u for u in abi if abi[u]["outcome"] == "DIFFER"]
lost  = [u for u in abi if free.get(u, {}).get("outcome") in ("EQUAL_BY_Z3", "IDENTICAL_AFTER_NORMALIZE")
         and abi[u]["outcome"] == "DIFFER"]
print()
print("  DIFFER under free arguments that AGREE once the ABI is promised: %d" % len(moved))
print("  DIFFER even with the promise -- the real divergences:            %d" % len(still))
print("  agreed free but differ with the promise (should be none):        %d" % len(lost))

if still:
    print()
    print("  THE REAL DIVERGENCES, by operand shape:")
    by = collections.Counter((abi[u].get("lang"), str(abi[u].get("lhs_type")),
                              str(abi[u].get("rhs_type"))) for u in still)
    for (lg, lt, rt), n in by.most_common(20):
        print("    %-4s %-14s %-14s x%d" % (lg, lt, rt, n))
    print()
    print("  each one, with the input that breaks it:")
    for u in sorted(still)[:40]:
        r = abi[u]
        print("    %-12s %-4s %-16s width %-4s %s"
              % (u, r.get("lang"), (r.get("expression") or "")[:16],
                 r.get("answer_width"), str(r.get("counterexample"))[:76]))
PY
python3 $OP/check_no_spelling_keys.py $OUT/claim_abi.json 2>&1 | tail -1
echo "wall=$(( $(date +%s) - t0 ))s"
echo done
