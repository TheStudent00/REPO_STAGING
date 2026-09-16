#!/bin/bash
# lp3_l99_emul_gate_read_the_residuals_in_full.sh
#
# The gate (l98) left ten of twelve pairs unproved and the four-line error
# excerpt it kept does not say WHICH of two very different things happened.
# `bv_decide` prints two different sentences:
#
#   "The prover found a counterexample, consider the following assignment"
#       -- the goal is FALSE and here is an input that breaks it.
#   "The prover found a potentially spurious counterexample"
#       -- the goal was not fully bit-blasted: some subterm stayed an
#       uninterpreted atom, so the model may not be a real input at all.
#       This is a gap in the NORMALISATION, not a disproof.
#
# Report by cause requires telling those apart and quoting each. This lane
# re-runs the Lean files l98 already wrote, unchanged, and prints their
# whole output. Nothing is re-proved and nothing new is stated: the files
# are the ones on disk.
#
# Fetches nothing. Writes $A/runs/gate_emul/residuals only.
set -uo pipefail
export ELAN_HOME=/persist/lp1/elan
export PATH=$ELAN_HOME/bin:/opt/elan/bin:$PATH
export XDG_CACHE_HOME=/work/cache; mkdir -p /work/cache
A=PseudoCoupHQ/Research/oracle/riscv/leanpath
P=/work/proof
G=$A/runs/gate_emul
R=$G/residuals; mkdir -p $R
cd $P; t0=$(date +%s)

i=0
FILES="
Equals_au_252_c_add_bool_i64_plain_fixed_width
Equals_au_344_c_bor_i32_i64_plain_fixed_width
Equals_au_182_c_pos_i32_abi_fixed_width
Equals_au_452_go_band_i32_i32_abi_fixed_width
Equals_au_319_c_lor_u64_i32_abi_fixed_width
Equals_au_407_c_ne_i32_i32_abi_fixed_width
Equals_au_445_go_shr_i32_u64_abi_fixed_width
"
total=$(echo $FILES | wc -w)
for f in $FILES; do
  i=$((i+1))
  echo "[$i/$total] $f  ($(( $(date +%s) - t0 ))s)"
  timeout 180 lake env lean $G/equals/$f.lean > $R/$f.txt 2>&1
  echo "  rc=$? bytes=$(wc -c < $R/$f.txt)"
  # the theorem as it was put, then everything Lean said
  grep -n "^theorem\|^set_option maxHeartbeats" $G/equals/$f.lean | tail -3 | sed 's/^/    stated: /' | cut -c1-300
  sed -n '1,60p' $R/$f.txt | cut -c1-300 | sed 's/^/    /'
  echo
done
echo "residuals wall seconds=$(( $(date +%s) - t0 ))"
echo done
