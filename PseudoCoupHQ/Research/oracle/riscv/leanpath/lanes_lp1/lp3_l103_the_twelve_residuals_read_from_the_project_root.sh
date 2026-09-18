#!/bin/bash
# lp3_l103_the_twelve_residuals_read_from_the_project_root.sh
#
# l102's step [4/4] IS WRONG AND THIS LANE REPLACES IT. It ran `lake env lean`
# from $A, the leanpath artifact folder, instead of from $P, the proof
# project; every one of the twelve files answered
#
#   error: unknown module prefix 'LeanIM'
#   No directory 'LeanIM' or file 'LeanIM.olean' in the search path
#
# and the lane then counted zero "potentially spurious" and zero "found a
# counterexample" in twelve files that had never been elaborated. That count
# said nothing and is retracted. l102's VERDICTS are unaffected -- `equals`
# runs Lean through `walk.lean_run(proof_project, ...)`, which sets the
# project itself -- so "8 of 20" stands; only the residual reading was void.
#
# WHAT THIS LANE IS ACTUALLY FOR. l102 moved three theorems and every one was
# an `abi` statement. After it, the split is total:
#
#   abi     8 of 10 proved
#   plain   0 of 10 proved
#
# Two readings, and they are not the same thing at all:
#
#   * `plain` puts the arch expression against the emulation expression with
#     NO psABI widening on the operands. For a 32-bit result the compiler
#     guarantees only the low 32 bits, so the two sides may genuinely DIFFER
#     in the high bits and the goal is then FALSE. `bv_decide` would say
#     "found a counterexample" and give the inputs.
#   * or the goal is true and something in it is still outside the BitVec
#     fragment, in which case `bv_decide` says "potentially spurious" and
#     names the atom it abstracted.
#
# The first is a WRONG STATEMENT and the `plain` form should stop being put.
# The second is more normalisation to do. Only Lean's own words separate them,
# so this lane elaborates each file FROM $P and prints what it says.
#
# Reads l102's files, re-elaborates them, writes $G2/residuals2 only.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
P=/work/proof
G2=$A/runs/gate_emul_norm
R=$G2/residuals2; mkdir -p $R
t0=$(date +%s)

[ -f $G2/gate.json ] || { echo "FLAG: no $G2/gate.json -- l102 is the lane that writes it"; exit 3; }
[ -f $P/.lake/packages/Sail/Sail/Common.lean ] || { echo "FLAG: $P is not a built tree"; exit 3; }

python3 - <<'PY' > $R/still.txt
import json
G2 = "PseudoCoupHQ/Research/oracle/riscv/leanpath/runs/gate_emul_norm"
for r in json.load(open(G2 + "/gate.json"))["rows"]:
    for k in ("plain", "abi"):
        v = (r.get(k) or {}).get("verdict")
        if v not in (None, "PROVED", "NOT REACHED"):
            print("%s_%s" % (r["unit"], k))
PY
n=$(wc -l < $R/still.txt); echo "still not proved: $n"

cd $P                                   # THE FIX: elaborate from the project
i=0
while read -r f; do
  [ -z "$f" ] && continue
  i=$((i+1))
  src=$G2/equals/Equals_${f}_fixed_width.lean
  if [ ! -f "$src" ]; then echo "[$i/$n] $f -- no fixed_width file"; continue; fi
  timeout 300 lake env lean "$src" > $R/$f.txt 2>&1; rc=$?
  spur=$(grep -c "potentially spurious" $R/$f.txt)
  cex=$(grep -c "The prover found a counterexample" $R/$f.txt)
  mod=$(grep -c "unknown module prefix" $R/$f.txt)
  if   [ "$mod"  -gt 0 ]; then verdict="HARNESS STILL WRONG"
  elif [ "$cex"  -gt 0 ]; then verdict="FALSE -- real counterexample, the statement is wrong"
  elif [ "$spur" -gt 0 ]; then verdict="NORMALISATION -- an atom stayed abstract"
  elif [ "$rc"   -eq 0 ]; then verdict="NO ERROR -- it elaborates; re-read the verdict"
  else                         verdict="OTHER (rc=$rc)"
  fi
  printf "[%2d/%2d] %-34s %s\n" "$i" "$n" "$f" "$verdict"
  if [ "$cex" -gt 0 ]; then
    grep -A8 "The prover found a counterexample" $R/$f.txt | head -10 | cut -c1-200 | sed 's/^/        /'
  elif [ "$spur" -gt 0 ]; then
    grep -A6 "abstracted the following unsupported" $R/$f.txt | head -8 | cut -c1-200 | sed 's/^/        /'
  else
    head -6 $R/$f.txt | cut -c1-200 | sed 's/^/        /'
  fi
done < $R/still.txt

echo
echo "SUMMARY by cause"
for k in "potentially spurious" "The prover found a counterexample" "unknown module prefix"; do
  printf "  %-38s %d file(s)\n" "$k" "$(grep -l "$k" $R/*.txt 2>/dev/null | wc -l)"
done
echo "wall=$(( $(date +%s) - t0 ))s"
echo done
