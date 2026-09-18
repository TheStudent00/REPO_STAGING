#!/bin/bash
# rv1_l18_the_same_507_with_the_float_boxing_promise_too.sh
#
# l17 supplied the INTEGER arrival promises and took DIFFER from 184 to 86.
# The 86 were then sorted by cause and 49 of them were "a float term is a free
# function". Reading the same run at the ARCH-OPCODE level says something
# sharper: every SINGLE-precision opcode lands in "never agrees" --
#
#   feq.s  fadd.s  fsub.s  fmul.s  fdiv.s  fmv.w.x
#   fcvt.s.w  fcvt.s.l  fcvt.s.lu  fcvt.s.wu  fcvt.d.s
#
# -- while their DOUBLE-precision twins mostly agree: fcvt.d.w, fcvt.d.l,
# fcvt.d.wu and fdiv.d always, fadd.d / fsub.d / fmul.d / fmv.d.x mixed.
#
# That split is not a property of floating point. It is NAN-BOXING. RISC-V
# requires a single-precision value in a 64-bit f-register to carry all ones
# in bits 63:32, and its operations rely on it; x86 has no such rule. l17
# skipped every xmm place outright, so float arguments got NO promise at all
# -- the same omission that cost 92 units on the integer side, made again on
# the float side and not noticed because floats were filed under "free
# function" rather than "no precondition".
#
# `riscv_term` takes Extract(63, 0, symbol) as the f-register, so the promise
# is on bits 63:32 of the shared symbol, and the x86 side reads only 31:0 and
# is untouched. One line in `abi_assumptions`; this lane measures what it is
# worth.
#
# Reads l15's output. Writes $RV/xarch/claim_box* only. Budget: twenty minutes.
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
        $OUT/claim_box assume-abi > $OUT/claim_box.log 2>&1
echo "  rc=$?  units walked: $(grep -c '^\[' $OUT/claim_box.log)"
head -1 $OUT/claim_box.log | sed 's/^/  /'
[ -f $OUT/claim_box.json ] || { echo "  FLAG: no claim_box.json"; exit 3; }

echo "[3/3] the two runs side by side  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import json, collections
O = "PseudoCoupHQ/Research/oracle/riscv/xarch"
free = {r["unit"]: r for r in json.load(open(O + "/claim_all.json"))["rows"] if r.get("unit")}
abi  = {r["unit"]: r for r in json.load(open(O + "/claim_box.json"))["rows"] if r.get("unit")}
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
python3 $OP/check_no_spelling_keys.py $OUT/claim_box.json 2>&1 | tail -1
echo "wall=$(( $(date +%s) - t0 ))s"
echo done
