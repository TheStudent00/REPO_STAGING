#!/bin/bash
# lp3_l104_the_nonzero_test_probed_on_the_real_goals.sh
#
# THE THREE THAT l102/l103 LEFT. On the `abi` statement the gate stands at
# seven of ten proved, no statement false, and three blocked by ONE shape --
# Sail's "is this bitvector non-zero" test, which l103 caught bv_decide
# abstracting whole:
#
#   match 0 <b Int.ofNat (…).toNat with | true => 1#1 | false => 0#1
#
# au_445 also carries `.sshiftRight (Int.ofNat …)`, the same escape into Int
# under an arithmetic shift.
#
# THE HYPOTHESIS, AND IT IS THE OPPOSITE OF MORE UNFOLDING. The simp set
# currently unfolds `zopz0zI_u` (Sail's `<_u`) and `Sail.BitVec.toNatInt`, and
# THAT UNFOLDING IS WHAT PRODUCES THE SHAPE: it takes a comparison that was
# already about bitvectors and re-spells it over Int. l101's note on
# CORE_NORMALISE says it outright -- the bridge must go TOWARDS BitVec and
# never away, because unfolding `BitVec.ult` into Nat breaks goals bv_decide
# proves natively. So the thing to measure is whether LEAVING Sail's compare
# folded lets the bitblaster see it.
#
# NOT AN ARTIFICIAL SHAPE. Probing a hand-written imitation of the goal proves
# nothing about the goal, so this lane re-runs THE REAL FILES l102 wrote, with
# their `simp only` list edited and nothing else touched. Each variant is one
# Lean run over one unchanged theorem.
#
#   V0  the list exactly as l102 put it                     (known UNDECIDED)
#   V1  minus zopz0zI_u, zopz0zI_s, Sail.BitVec.toNatInt    (leave it folded)
#   V2  V0 plus whichever candidate lemmas elaborate
#   V3  V1 plus the same
#
# Stage 1 puts every candidate NAME to `#check` on its own line first, exactly
# as l101 did, because `try simp only [...]` swallows an unknown identifier and
# then skips the WHOLE set -- which reads as hard mathematics and is not.
#
# Reads l102's files. Writes $G/probe104 only. Budget: fifteen minutes.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
P=/work/proof
G=$A/runs/gate_emul_norm
R=$G/probe104; mkdir -p $R
t0=$(date +%s)
[ -d $G/equals ] || { echo "FLAG: no $G/equals -- l102 is the lane that writes it"; exit 3; }
cd $P

UNITS="au_319_c_lor_u64_i32_abi au_407_c_ne_i32_i32_abi au_445_go_shr_i32_u64_abi"

echo "[1/3] which candidate names elaborate at all  ($(( $(date +%s) - t0 ))s)"
cat > $R/Check.lean <<'EOF'
import LeanIM
#check @BitVec.ofBool
#check @BitVec.ult
#check @BitVec.ult_iff_lt
#check @BitVec.lt_def
#check @BitVec.toNat_eq_zero
#check @BitVec.toNat_ne_zero
#check @Int.ofNat_pos
#check @Int.ofNat_lt
#check @Int.toNat_natCast
#check @Nat.pos_iff_ne_zero
#check @decide_eq_true_eq
#check @Bool.cond_eq_ite
#check @BitVec.sshiftRight_eq
#check @BitVec.ofBool_eq_iff
EOF
timeout 300 lake env lean $R/Check.lean > $R/check.txt 2>&1
GOOD=""
while read -r nm; do
  if grep -q "unknown \(identifier\|constant\).*$nm" $R/check.txt; then
    printf "  %-28s ABSENT\n" "$nm"
  else
    printf "  %-28s present\n" "$nm"; GOOD="$GOOD $nm"
  fi
done < <(grep -oE "^#check @[A-Za-z0-9_.]+" $R/Check.lean | sed 's/^#check @//')
echo "  candidates that elaborate:$GOOD"
# the ones worth ADDING to a simp set (a `#check` name is not automatically a
# rewrite; these are the rewrite-shaped ones among those that exist)
ADD=""
for nm in BitVec.ofBool BitVec.ult_iff_lt BitVec.toNat_ne_zero Int.ofNat_pos decide_eq_true_eq Bool.cond_eq_ite; do
  case " $GOOD " in *" $nm "*) ADD="$ADD, $nm" ;; esac
done
echo "  will be appended as V2/V3:${ADD:-none}"

echo "[2/3] four variants per unit, on l102's own files  ($(( $(date +%s) - t0 ))s)"
DROP='zopz0zI_u\|zopz0zI_s\|Sail.BitVec.toNatInt'
for u in $UNITS; do
  src=$G/equals/Equals_${u}_fixed_width.lean
  [ -f "$src" ] || { echo "  $u: no file"; continue; }
  for V in V0 V1 V2 V3; do
    f=$R/${u}_$V.lean
    cp "$src" "$f"
    # the simp list is one line beginning with `  try simp only [`
    case $V in
      V0) : ;;
      V1) python3 - "$f" <<'PY'
import re, sys
p = sys.argv[1]; s = open(p).read()
def cut(m):
    inner = m.group(1)
    keep = [x for x in (t.strip() for t in inner.split(","))
            if x and x not in ("zopz0zI_u", "zopz0zI_s", "Sail.BitVec.toNatInt")]
    return "simp only [" + ", ".join(keep) + "]"
s = re.sub(r"simp only \[(.*?)\]", cut, s, flags=re.S)
open(p, "w").write(s)
PY
          ;;
      V2) python3 - "$f" "$ADD" <<'PY'
import re, sys
p, add = sys.argv[1], sys.argv[2]
s = open(p).read()
s = re.sub(r"simp only \[(.*?)\]", lambda m: "simp only [" + m.group(1) + add + "]", s, flags=re.S)
open(p, "w").write(s)
PY
          ;;
      V3) python3 - "$f" "$ADD" <<'PY'
import re, sys
p, add = sys.argv[1], sys.argv[2]
s = open(p).read()
def cut(m):
    keep = [x for x in (t.strip() for t in m.group(1).split(","))
            if x and x not in ("zopz0zI_u", "zopz0zI_s", "Sail.BitVec.toNatInt")]
    return "simp only [" + ", ".join(keep) + add + "]"
s = re.sub(r"simp only \[(.*?)\]", cut, s, flags=re.S)
open(p, "w").write(s)
PY
          ;;
    esac
    timeout 300 lake env lean "$f" > $R/${u}_$V.txt 2>&1; rc=$?
    err=$(grep -c "error" $R/${u}_$V.txt)
    spur=$(grep -c "potentially spurious" $R/${u}_$V.txt)
    cex=$(grep -c "The prover found a counterexample" $R/${u}_$V.txt)
    unk=$(grep -c "unknown \(identifier\|constant\)" $R/${u}_$V.txt)
    if   [ "$unk" -gt 0 ];  then v="BAD NAME -- set skipped, means nothing"
    elif [ "$rc" -eq 0 ] && [ "$err" -eq 0 ]; then v="PROVED"
    elif [ "$cex" -gt 0 ];  then v="FALSE -- counterexample"
    elif [ "$spur" -gt 0 ]; then v="still abstract"
    else                         v="other (rc=$rc, $err error lines)"
    fi
    printf "  %-30s %-3s %s\n" "$u" "$V" "$v"
  done
done

echo "[3/3] what stayed abstract in the best variant  ($(( $(date +%s) - t0 ))s)"
for u in $UNITS; do
  for V in V3 V1 V2 V0; do
    f=$R/${u}_$V.txt
    [ -f "$f" ] || continue
    if grep -q "abstracted the following unsupported" "$f"; then
      echo "  --- $u $V ---"
      grep -A5 "abstracted the following unsupported" "$f" | head -7 | cut -c1-180 | sed 's/^/      /'
      break
    fi
  done
done
echo "wall=$(( $(date +%s) - t0 ))s"
echo done
