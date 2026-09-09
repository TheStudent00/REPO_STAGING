#!/bin/bash
# L1 lane 14 — the names Lean 4.24's own BitVec library gives the facts the
# renderer's hard cases need, read out of the toolchain's shipped source
# rather than remembered. Core only; Mathlib is not installed and is not used.
set -u
SRC=/opt/elan/toolchains/leanprover--lean4---v4.24.0/src/lean/Init/Data/BitVec
echo '[1/1] the shipped BitVec lemma names'
echo "--- where the library lives"
ls "$SRC"
echo "--- shiftLeft / ushiftRight at or past the width"
grep -rn "theorem shiftLeft_eq_zero\|theorem ushiftRight_eq_zero\|shiftLeft_eq_zero_iff\|ushiftRight_eq_zero_iff" "$SRC" | head -20
echo "--- getLsbD lemmas for the three shifts"
grep -rn "theorem getLsbD_shiftLeft\b\|theorem getLsbD_ushiftRight\b\|theorem getLsbD_sshiftRight\b\|theorem getLsbD_sshiftRight'" "$SRC" | head -20
echo "--- the statements themselves"
grep -rn -A3 "theorem getLsbD_shiftLeft\b" "$SRC" | head -12
grep -rn -A3 "theorem getLsbD_ushiftRight\b" "$SRC" | head -12
grep -rn -A4 "theorem getLsbD_sshiftRight\b" "$SRC" | head -14
echo "--- append and extractLsb"
grep -rn -A3 "theorem getLsbD_append\b" "$SRC" | head -12
grep -rn -A3 "theorem extractLsb_eq\|def extractLsb\b\|def extractLsb'\b" "$SRC" ../ 2>/dev/null | head -20
grep -rn -A3 "theorem getLsbD_extractLsb'\|theorem getLsbD_extract" "$SRC" | head -14
echo "--- sshiftRight' in terms of sshiftRight"
grep -rn -A3 "sshiftRight'" "$SRC" | head -20
echo "--- what core calls n < 2^n"
grep -rn "lt_two_pow" /opt/elan/toolchains/leanprover--lean4---v4.24.0/src/lean/Init/Data/Nat/*.lean | head -10
echo "--- the extensionality lemma"
grep -rn "eq_of_getLsbD_eq\|@\[ext\]" "$SRC/Lemmas.lean" | head -10
