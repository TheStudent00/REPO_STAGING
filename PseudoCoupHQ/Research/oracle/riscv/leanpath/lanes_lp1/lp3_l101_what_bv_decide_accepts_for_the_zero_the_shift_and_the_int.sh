#!/bin/bash
# lp3_l101_what_bv_decide_accepts_for_the_zero_the_shift_and_the_int.sh
#
# TWO THINGS, and the first one decides whether the second is worth reading.
#
# [A] THE STATE OF THE PROOF PROJECT, MEASURED, NOT ASSUMED. l97..l100 all
#     ran against /work/proof, a copy of /persist/lp1/Lean_IM_6266b40c_all
#     made by l3. On the machine this lane is submitted from, checked before
#     it was written:
#
#       - there is no `lp1-persist` volume in the podman store (37 volumes,
#         newest sail0-persist, 2026-09-13); `up.sh --instance lp3` therefore
#         mounted a FRESH EMPTY one at /persist
#       - /persist is empty and /persist/lp1 does not exist -- no elan, no
#         model clone, no built Lean project
#       - /work is empty -- no /work/proof, no /work/Lean_IM_pr_exec
#       - <runs>/lp3 did not exist at all, so no lane of this instance
#         has ever run on this host through this checkout
#
#     Step [1] states that from inside the container, so the claim is the
#     container's and not the host's. If it finds a built tree after all, the
#     rest of this lane is still valid and the gate can be re-run at once.
#
# [B] WHAT `bv_decide` ACCEPTS FOR THE THREE SYMBOLS l100's residuals named.
#     l100 proved that the two path faults were real and fixed -- `zero_reg`
#     and `Sail.shift_bits_left` are in the simp line and gone from every
#     opaque list -- and that not one of the six UNDECIDED pairs moved. What
#     the residuals name now is one layer lower, and all three are LIBRARY
#     terms, not the gate's own:
#
#       au_182, au_409, au_452   BitVec.zero 64
#       au_319, au_407           BitVec.toNatInt, BitVec.zero 64
#       au_445                   BitVec.sshiftRight, BitVec.toNatInt, BitVec.zero 64
#
#     `BitVec.zero` and `BitVec.sshiftRight` are LEAN CORE. `BitVec.toNatInt`
#     is lean-sail's `Sail.BitVec.toNatInt` and needs the package present, so
#     the shape is put here with a STAND-IN whose body is stated in the file
#     and which is never claimed to be lean-sail's.
#
#     Nothing is guessed. Every candidate is put one at a time, and every
#     candidate NAME is first put to `#check` on its own line, because an
#     unknown name is the failure this lane exists to avoid. On the host, at
#     v4.30.0 and v4.34.0, `try simp only [zeros, BitVec.zero_eq, <a name
#     that does not exist>]` did NOT break the file and did NOT report an
#     unknown identifier: `try` swallowed the elaboration error and the WHOLE
#     simp set was silently skipped, so `zeros` stayed folded and bv_decide
#     answered with a spurious counterexample. A bad name in the unfolding
#     rule therefore looks exactly like hard mathematics. Probe [U] puts that
#     to this toolchain too.
#
# THE TOOLCHAIN GAP, SAID PLAINLY. The emit pins `leanprover/lean4:v4.29.0`
# (cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules/lean-toolchain). The
# host has v4.30.0 and v4.34.0; this container's image has whatever /opt/elan
# carries, which step [2] prints. v4.29.0 is installed nowhere reachable and
# this instance has proxy = no, so it cannot be fetched here. This lane
# therefore BRACKETS the pinned version rather than hitting it, and step [2]
# prints the version it actually used so the bracket is on the record.
#
# Fetches nothing. Writes $A/runs/gate_emul_lemmas only. Budget: five minutes.
set -uo pipefail
export ELAN_HOME=${ELAN_HOME:-/persist/lp1/elan}
export PATH=$ELAN_HOME/bin:/opt/elan/bin:/opt/cargo/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
P=/work/proof
R=$A/runs/gate_emul_lemmas
mkdir -p $R /work/bvprobe; t0=$(date +%s)

echo "[1/5] the state of the proof project and the persistent volume, from inside the container  ($(( $(date +%s) - t0 ))s)"
for d in /persist /persist/lp1 /persist/lp1/elan $P /work/Lean_IM_pr_exec $P/.lake/packages/Sail; do
  if [ -e "$d" ]; then echo "  present: $d   ($(ls -1 "$d" 2>/dev/null | wc -l) entries)"; else echo "  ABSENT:  $d"; fi
done
echo "  /work:"; ls -la /work 2>&1 | sed 's/^/    /' | head -12
echo "  /persist:"; ls -la /persist 2>&1 | sed 's/^/    /' | head -12
if [ -f $P/.lake/packages/Sail/Sail/Common.lean ]; then
  echo "  THE GATE IS RUNNABLE: the built tree is there after all."
else
  echo "  THE GATE IS NOT RUNNABLE FROM HERE: no built tree, so no /work/proof to run"
  echo "  'lake env lean' in. Every pair would report a build error, not a verdict."
  echo "  The cached EMIT SOURCE is still on the repo mount and is untouched:"
  du -sh $A/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules 2>/dev/null | sed 's/^/    /'
  echo "    pinned toolchain: $(cat $A/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules/lean-toolchain 2>/dev/null)"
  echo "    lean-sail required: $(grep -A3 'require' $A/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules/lakefile.toml 2>/dev/null | tr '\n' ' ')"
fi

echo "[2/5] the Lean this lane will actually use  ($(( $(date +%s) - t0 ))s)"
which lean lake 2>&1 | sed 's/^/  /'
lean --version 2>&1 | sed 's/^/  /'
echo "  toolchains present: $(ls /opt/elan/toolchains 2>/dev/null | tr '\n' ' ')$(ls /persist/lp1/elan/toolchains 2>/dev/null | tr '\n' ' ')"
echo "  the emit pins:      $(cat $A/cache/sail-riscv_6266b40c_sail_8eb1fb6b_all_modules/lean-toolchain 2>/dev/null)"

echo "[3/5] does every candidate NAME exist at this toolchain  ($(( $(date +%s) - t0 ))s)"
cd /work/bvprobe
cat > Names.lean <<'LEAN'
import Std.Tactic.BVDecide
-- one #check per line: an unknown one errors on its own line and the rest still run
#check @BitVec.zero
#check @BitVec.zero_eq
#check @BitVec.ofNat_eq_ofNat
#check @BitVec.sshiftRight
#check @BitVec.sshiftRight'
#check @BitVec.sshiftRight_eq
#check @BitVec.lt_def
#check @BitVec.ult
#check @BitVec.ult_iff_lt
#check @Int.ofNat_lt
#check @Int.toNat_natCast
LEAN
timeout 300 lean Names.lean > $R/names.txt 2>&1
echo "  rc=$?"
cat $R/names.txt | sed 's/^/    /'

echo "[4/5] every candidate put to bv_decide, one at a time  ($(( $(date +%s) - t0 ))s)"
cat > Cands.lean <<'LEAN'
import Std.Tactic.BVDecide
set_option linter.unusedSimpArgs false

-- the emit's own shape: Prelude.lean:263 and RegType.lean:215
def zeros {n : Nat} : BitVec n := BitVec.zero n
def zero_reg : BitVec 64 := zeros (n := 64)

-- Z0 BASELINE, the set the gate generates today
theorem z0 (a : BitVec 64) : (a ||| zero_reg) = a := by
  try simp only [zero_reg, zeros]
  all_goals bv_decide
-- Z1 candidate: BitVec.zero_eq
theorem z1 (a : BitVec 64) : (a ||| zero_reg) = a := by
  try simp only [zero_reg, zeros, BitVec.zero_eq]
  all_goals bv_decide
-- Z2 candidate: unfold BitVec.zero by name
theorem z2 (a : BitVec 64) : (a ||| zero_reg) = a := by
  try simp only [zero_reg, zeros, BitVec.zero]
  all_goals bv_decide
-- Z3 candidate: BitVec.ofNat_eq_ofNat
theorem z3 (a : BitVec 64) : (a ||| zero_reg) = a := by
  try simp only [zero_reg, zeros, BitVec.ofNat_eq_ofNat]
  all_goals bv_decide
-- Z4 the bare normalisation the whole thing turns on
theorem z4 : (BitVec.zero 64) = 0#64 := by
  simp only [BitVec.zero_eq]
-- Z5 bv_decide with no help at all
theorem z5 : (BitVec.zero 64) = 0#64 := by
  bv_decide

-- U0 ONE UNKNOWN NAME in a set that would otherwise fire
theorem u0 (a : BitVec 64) : (a ||| zero_reg) = a := by
  try simp only [zero_reg, zeros, BitVec.zero_eq, BitVec.this_name_does_not_exist]
  all_goals bv_decide

-- S0 a shift by a Nat that came from a BitVec: already in the fragment?
theorem s0 (a b : BitVec 64) : a.sshiftRight b.toNat = a.sshiftRight' b := by
  all_goals bv_decide
-- S1 the emit's own shape: the Nat came from an Int (Prelude.lean:414)
theorem s1 (a b : BitVec 64) : a.sshiftRight ((b.toNat : Int)).toNat = a.sshiftRight' b := by
  all_goals bv_decide
-- S2 the same with Int.toNat_natCast
theorem s2 (a b : BitVec 64) : a.sshiftRight ((b.toNat : Int)).toNat = a.sshiftRight' b := by
  try simp only [Int.toNat_natCast]
  all_goals bv_decide
-- S3 the au_445 shape: a 32-bit arithmetic shift by an Int-derived Nat
theorem s3 (a b : BitVec 64) :
    (BitVec.extractLsb' 0 32 a).sshiftRight (((BitVec.extractLsb' 0 5 b).toNat : Int)).toNat
      = (BitVec.extractLsb' 0 32 a).sshiftRight' (BitVec.extractLsb' 0 5 b) := by
  try simp only [Int.toNat_natCast]
  all_goals bv_decide

-- A STAND-IN, not lean-sail. Its body is stated here and is an ASSUMPTION
-- about Sail.BitVec.toNatInt, not a reading of it: the package is not present.
def toNatIntStandIn {n : Nat} (x : BitVec n) : Int := (x.toNat : Int)
def ltbStandIn (x y : Int) : Bool := decide (x < y)
-- I0 the au_319 shape, baseline
theorem i0 (x y : BitVec 64) :
    (match ltbStandIn (toNatIntStandIn x) (toNatIntStandIn y) with | true => 1#1 | false => 0#1)
      = (match x.ult y with | true => 1#1 | false => 0#1) := by
  all_goals bv_decide
-- I1 the OUTWARD bridge: unfold BitVec.ult into Nat
theorem i1 (x y : BitVec 64) :
    (match ltbStandIn (toNatIntStandIn x) (toNatIntStandIn y) with | true => 1#1 | false => 0#1)
      = (match x.ult y with | true => 1#1 | false => 0#1) := by
  try simp only [toNatIntStandIn, ltbStandIn, Int.ofNat_lt, BitVec.ult]
  all_goals bv_decide
-- I2 the INWARD bridge: rewrite the Int comparison back towards BitVec
theorem i2 (x y : BitVec 64) :
    (match ltbStandIn (toNatIntStandIn x) (toNatIntStandIn y) with | true => 1#1 | false => 0#1)
      = (match x.ult y with | true => 1#1 | false => 0#1) := by
  try simp only [toNatIntStandIn, ltbStandIn, Int.ofNat_lt, ← BitVec.lt_def, BitVec.ult_iff_lt]
  all_goals bv_decide

-- DOES THE PROPOSED ADDITION HARM WHAT ALREADY PROVES?
-- H0 a goal bv_decide proves natively, untouched
theorem h0 (x y : BitVec 64) : (x.ult y || x == y) = x.ule y := by
  all_goals bv_decide
-- H1 the same goal with the OUTWARD bridge added
theorem h1 (x y : BitVec 64) : (x.ult y || x == y) = x.ule y := by
  try simp only [BitVec.ult]
  all_goals bv_decide
-- H2 the same goal with the INWARD set this run proposes
theorem h2 (x y : BitVec 64) : (x.ult y || x == y) = x.ule y := by
  try simp only [BitVec.zero_eq, Int.toNat_natCast, Int.ofNat_lt, ← BitVec.lt_def, BitVec.ult_iff_lt]
  all_goals bv_decide
-- H3 plain arithmetic with the same set
theorem h3 (x y : BitVec 64) : (x + y) - y = x := by
  try simp only [BitVec.zero_eq, Int.toNat_natCast, Int.ofNat_lt, ← BitVec.lt_def, BitVec.ult_iff_lt]
  all_goals bv_decide
LEAN
grep -n "^theorem\|^  all_goals\|^  simp only\|^  bv_decide" Cands.lean | sed 's/^/    /'
timeout 900 lean Cands.lean > $R/cands.txt 2>&1
echo "  rc=$? bytes=$(wc -c < $R/cands.txt)"
echo "  Lean's whole output, no truncation:"
cat $R/cands.txt | sed 's/^/    /'

echo "[5/5] the verdict per candidate, read off the line numbers Lean reported  ($(( $(date +%s) - t0 ))s)"
python3 - <<'PY'
import re, os
R = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/gate_emul_lemmas"
src = open("/work/bvprobe/Cands.lean").read().split("\n")
out = open(R + "/cands.txt").read()
bad = set()
for m in re.finditer(r"Cands\.lean:(\d+):\d+: error", out):
    bad.add(int(m.group(1)))
# a theorem's closing tactic line is the last line before the next `--` or `theorem`
rows, cur = [], None
for i, ln in enumerate(src, 1):
    m = re.match(r"^theorem (\w+)", ln)
    if m:
        cur = [m.group(1), i, i]
        rows.append(cur)
    elif cur is not None and ln.startswith("  "):
        cur[2] = i
print("  | candidate | closing line | Lean said |")
print("  |---|---:|---|")
for name, a, b in rows:
    hit = [l for l in range(a, b + 1) if l in bad]
    print("  | %s | %d | %s |" % (name, b, "REFUSED at line %s" % hit[0] if hit else "PROVED"))
open(R + "/verdicts.txt", "w").write("\n".join(
    "%s %s" % (n, "REFUSED" if any(l in bad for l in range(a, b + 1)) else "PROVED") for n, a, b in rows) + "\n")
PY
cp /work/bvprobe/Cands.lean /work/bvprobe/Names.lean $R/ 2>/dev/null
echo "  wrote $R/{names.txt,cands.txt,verdicts.txt,Cands.lean,Names.lean}"
echo "lane wall seconds=$(( $(date +%s) - t0 ))"
echo done
